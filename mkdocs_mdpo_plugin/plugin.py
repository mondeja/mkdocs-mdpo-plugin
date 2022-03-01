"""mkdocs-mdpo-plugin module"""

import functools
import logging
import math
import os
import sys

import mkdocs
import polib
from jinja2 import Template
from mdpo.md2po import Md2Po
from mdpo.po2md import Po2Md

from mkdocs_mdpo_plugin.config import CONFIG_SCHEME, on_config_event
from mkdocs_mdpo_plugin.extensions import Extensions
from mkdocs_mdpo_plugin.mdpo_events import (
    build_md2po_events,
    build_po2md_events,
)
from mkdocs_mdpo_plugin.mdpo_utils import (
    remove_mdpo_commands_preserving_escaped,
)
from mkdocs_mdpo_plugin.mkdocs_utils import (
    MkdocsBuild,
    set_on_build_error_event,
)
from mkdocs_mdpo_plugin.search_indexes import TranslationsSearchPatcher
from mkdocs_mdpo_plugin.translations import Translation, Translations
from mkdocs_mdpo_plugin.utils import (
    po_messages_stats,
    readable_float,
    removesuffix,
)


# use Mkdocs build logger
logger = logging.getLogger('mkdocs.commands.build')


class MdpoPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = CONFIG_SCHEME

    def __init__(self, *args, **kwargs):
        # temporal translation files
        self.translations = Translations()

        # Markdown extensions configuration
        self.extensions = Extensions()

        # instance that represents the run
        # (needed by `mkdocs-mdpo` extension)
        MkdocsBuild.instance(self)

        super().__init__(*args, **kwargs)

    @functools.lru_cache(maxsize=None)
    def _non_default_languages(self):
        return [
            language for language in self.config['languages']
            if language != self.config['default_language']
        ]

    @functools.lru_cache(maxsize=None)
    def _language_dir(self, base_dir, language):
        return os.path.join(
            base_dir,
            self.config['locale_dir'],
            language,
            self.config['lc_messages'],
        )

    def on_config(self, config, **kwargs):
        """Configuration for `mkdocs_mdpo_plugin`."""
        return on_config_event(self, config, **kwargs)

    def on_pre_build(self, config):
        """Create locales folders inside documentation directory."""
        for language in self._non_default_languages():
            os.makedirs(
                os.path.join(
                    self._language_dir(config['docs_dir'], language),
                ),
                exist_ok=True,
            )

    def on_files(self, files, config):
        """Remove locales directory from collected files.

        NOTE: Since mkdocs 1.2.X, there is a new method ``remove`` for
              files which will simplify the code defined in this event.
        """
        new_files = mkdocs.structure.files.Files([])

        ignore_extensions = self.config['ignore_extensions']
        for file in files:
            # exclude all files with PO related extensions
            if os.path.splitext(file.src_path)[-1] not in ignore_extensions:
                new_files.append(file)

            if file.is_documentation_page():
                self.translations.files[file.src_path] = {}

                for language in self._non_default_languages():
                    # render destination path
                    context = {'file': file, 'language': language}
                    context.update(self.config)
                    dest_path = Template(
                        self.config['dest_filename_template'],
                    ).render(**context)
                    src_path = f"{removesuffix(dest_path, '.html')}.md"

                    self.translations.files[file.src_path][language] = (
                        os.path.join(
                            self.translations.tempdir.name,
                            src_path,
                        )
                    )
        return new_files

    def on_page_context(self, context, page, config, nav):
        """Navigation translation."""
        if not hasattr(page.file, '_mdpo_language'):
            return

        language = page.file._mdpo_language

        # using mkdocs-material, configure the language for each page
        if context['config']['theme'].name == 'material':
            context['config']['theme']['language'] = language

        def _translate_section_title(section):
            if section.title and section.title not in \
                    self.translations.compendium_msgids[language]:
                compendium_filepath = self.translations.compendium_files[
                    language
                ]
                compendium_pofile = polib.pofile(compendium_filepath)

                _section_title_in_compendium = False
                for entry in compendium_pofile:
                    if entry.msgid == section.title:
                        _section_title_in_compendium = True
                        entry.obsolete = False
                        if entry.msgstr:
                            section.title = entry.msgstr
                            self.translations.compendium_msgstrs_tr[
                                language
                            ].append(
                                entry.msgstr,
                            )
                        break
                if not _section_title_in_compendium:
                    compendium_pofile.insert(
                        0,
                        polib.POEntry(
                            msgid=section.title,
                            msgstr='',
                        ),
                    )
                    compendium_pofile.save(compendium_filepath)
                self.translations.compendium_msgids[language].append(
                    section.title,
                )

        def _translate_nav_section(items):
            for item in items:
                if isinstance(item, mkdocs.structure.nav.Section):
                    _translate_section_title(item)

                    if item.children:
                        _translate_nav_section(item.children)

                if (
                    item.title not in self.translations.nav or
                    language not in self.translations.nav[item.title]
                ):
                    # language not added because page has been excluded
                    # from translations
                    continue

                tr_title, tr_url = self.translations.nav[
                    item.title
                ][language]

                if tr_title:
                    item.title = tr_title
                if item.is_page:
                    item.file.url = tr_url

        # recursively translate navigation sections
        # (pages titles and section titles)
        _translate_nav_section(nav.items)

    def on_page_markdown(self, markdown, page, config, files):
        """Event executed when markdown content of a page is collected.

        Here happen most of the logic handled by the plugin:

        * For each documentation page, creates another documentation page
          for each language that will be translated (part here and part
          inside the `mkdocs-mdpo` extension, see
          :py:mod:`mkdocs_mdpo_plugin.extension` module).
        """
        # only process original files, pages created for translation
        # are ignored
        if hasattr(page.file, '_mdpo_language'):
            return

        # get minimum translation requirements
        min_translated = self.config['min_translated_messages']

        # check if the file is excluded to be translated
        #
        # the implementation here opts for create the file but
        # not creating the PO for translations
        #
        # other option would be to skip the languages loop entirely, but
        # this would not create the file for a language and the navigation
        # will do cross language linking, which worsens the user experience
        excluded_page = page.file.src_path in self.config['exclude']

        # navigation pages titles translations and new pages urls are
        # stored in dictionaries by language, so we can translate the
        # titles in their own PO files and then change the URLs
        # (see `on_page_context` event)
        if page.title not in self.translations.nav:
            # lang: [title, url]
            self.translations.nav[page.title] = {}

        # extract translations from original Markdown file
        md2po = Md2Po(
            markdown,
            events=build_md2po_events(self.extensions.markdown),
            mark_not_found_as_obsolete=False,
            location=False,
            ignore_msgids=self.config['ignore_msgids'],
        )
        original_po = md2po.extract()

        po2md_events = build_po2md_events(self.extensions.markdown)

        _mdpo_languages = {}  # {lang: file}

        for language in self._non_default_languages():
            if not excluded_page:
                # if the page has been excluded from being translated
                lang_docs_dir = self._language_dir(
                    config['docs_dir'],
                    language,
                )

                compendium_filepath = os.path.join(
                    lang_docs_dir,
                    '_compendium.po',
                )

                # create compendium if doesn't exists, load to memory
                if language not in self.translations.compendium_files:
                    if not os.path.isfile(compendium_filepath):
                        compendium_pofile = polib.POFile()
                        compendium_pofile.save(compendium_filepath)
                    self.translations.compendium_files[language] = \
                        compendium_filepath

                    # intialize compendium messages cache
                    self.translations.compendium_msgstrs_tr[language] = []
                    self.translations.compendium_msgids[language] = []

                compendium_pofile = polib.pofile(compendium_filepath)

                # create pofile of the page for each language
                po_filepath = os.path.join(
                    lang_docs_dir,
                    f'{page.file.src_path}.po',
                )
                os.makedirs(
                    os.path.abspath(os.path.dirname(po_filepath)),
                    exist_ok=True,
                )
                if not os.path.isfile(po_filepath):
                    po = polib.POFile()
                else:
                    po = polib.pofile(po_filepath)

                for entry in original_po:
                    if entry not in po:
                        po.append(entry)

                _translated_entries_msgids = []
                _translated_entries_msgstrs = []

                # translate title
                translated_page_title, _title_in_pofile = (None, False)
                for entry in po:
                    if entry.msgid == page.title:
                        # matching title found
                        entry.obsolete = False
                        translated_page_title = entry.msgstr
                        _title_in_pofile = True
                        _translated_entries_msgids.append(page.title)
                        if entry.msgstr:
                            _translated_entries_msgstrs.append(page.title)
                if not _title_in_pofile:
                    po.insert(
                        0,
                        polib.POEntry(
                            msgid=page.title,
                            msgstr='',
                        ),
                    )
                    _translated_entries_msgids.append(page.title)

                # add temporally compendium entries to language pofiles
                for entry in compendium_pofile:
                    if entry not in po and entry.msgstr:
                        po.append(entry)
                po.save(po_filepath)

                # if a minimum number of translations are required to include
                # the file, compute number of untranslated messages
                if min_translated:
                    n_translated, n_total = po_messages_stats(str(po))
                    if language not in self.translations.stats:
                        self.translations.stats[language] = {
                            'total': n_total,
                            'translated': n_translated,
                        }
                    else:
                        self.translations.stats[language][
                            'total'
                        ] += n_total
                        self.translations.stats[language][
                            'translated'
                        ] += n_translated

                # translate part of the markdown producing a translated file
                # content (the rest of the translations are handled by
                # extensions, see `extension` module)
                po2md = Po2Md(
                    [po_filepath, compendium_filepath],
                    events=po2md_events,
                    wrapwidth=math.inf,  # ignore line wrapping
                )
                content = po2md.translate(markdown)

                _disabled_msgids = [
                    entry.msgid for entry in po2md.disabled_entries
                ]
                _disabled_msgids.extend(self.config['ignore_msgids'])

                for entry in po2md.translated_entries:
                    _translated_entries_msgstrs.append(entry.msgstr)
                    _translated_entries_msgids.append(entry.msgid)
            else:
                # mock variables if the file is excluded from being translated
                content = markdown
                translated_page_title = None
                _disabled_msgids = []
                _translated_entries_msgstrs = []
                _translated_entries_msgids = []
                po, po_filepath = [], None

            temp_abs_path = self.translations.files[
                page.file.src_path
            ][language]
            temp_abs_dirpath = os.path.dirname(temp_abs_path)
            os.makedirs(temp_abs_dirpath, exist_ok=True)
            with open(temp_abs_path, 'w') as f:
                f.write(content)

            new_file = mkdocs.structure.files.File(
                temp_abs_path,
                temp_abs_dirpath,
                config['site_dir'],
                config['use_directory_urls'],
            )
            new_file.url = os.path.relpath(
                temp_abs_path,
                self.translations.tempdir.name,
            )
            new_file._mdpo_language = language
            new_page = mkdocs.structure.pages.Page(
                translated_page_title or page.title,
                new_file,
                config,
            )
            files.append(new_file)
            _mdpo_languages[language] = new_file

            # create translation object
            translation = Translation(
                language,
                po,
                po_filepath,
                [entry.msgid for entry in po],  # po_msgids
                _translated_entries_msgstrs,
                _translated_entries_msgids,
                _disabled_msgids,
            )
            self.translations.current = translation

            # change file url
            url = removesuffix(new_page.file.url, '.md') + '.html'
            if config['use_directory_urls']:
                url = removesuffix(url, 'index.html')
            new_page.file.url = url

            # the title of the page will be 'page.title' (the original)
            # if the file is being excluded from translations using the
            # 'exclude' plugin's config setting
            self.translations.nav[page.title][language] = [
                translated_page_title or page.title, new_page.file.url,
            ]

            mkdocs.commands.build._populate_page(
                new_page,
                config,
                files,
                dirty=(
                    '--dirty' in sys.argv and
                    '-c' not in sys.argv and '--clean' not in sys.argv
                ),
            )

            if language not in self.translations.all:
                self.translations.all[language] = []
            self.translations.all[language].append(translation)

        self.translations.current = None

        # set languages to render in sitemap.xml
        page.file._mdpo_languages = _mdpo_languages

        return remove_mdpo_commands_preserving_escaped(markdown)

    def on_post_page(self, output, page, config):
        if hasattr(page.file, '_mdpo_language'):
            # if the language should be included from the build, ignore it
            min_translated = self.config['min_translated_messages']
            if min_translated:
                language = page.file._mdpo_language
                stats = self.translations.stats[language]
                if abs(min_translated) != min_translated:
                    min_translated = abs(min_translated)
                    if 'percent_translated' in stats:
                        percent_translated = stats['percent_translated']
                    else:
                        percent_translated = (
                            stats['translated'] / stats['total'] * 100
                        )
                        stats['percent_translated'] = percent_translated
                    if percent_translated < min_translated:
                        if language in self.config['languages']:
                            logger.info(
                                '[mdpo] '
                                f'Excluding language "{language}". Translated'
                                f' {readable_float(percent_translated)}%'
                                f' ({stats["translated"]} of'
                                f' {stats["total"]} messages) but'
                                f' required {readable_float(min_translated)}%'
                                ' at least.\n',
                            )
                            self.config['languages'].remove(language)
                        return
                else:
                    if stats['translated'] < min_translated:
                        if language in self.config['languages']:
                            logger.info(
                                '[mdpo] '
                                f'Excluding language "{language}".'
                                f' Translated {stats["translated"]} messages'
                                f' of {stats["total"]} but required'
                                f' {min_translated} translated'
                                ' messages at least.\n',
                            )
                            self.config['languages'].remove(language)
                        return

            # write translated HTML file to 'site' directory
            os.makedirs(
                os.path.join(
                    config['site_dir'],
                    os.path.dirname(page.file.url),
                ),
                exist_ok=True,
            )

            render_path = os.path.join(
                config['site_dir'],
                page.file.url,
            )
            if config['use_directory_urls']:
                if render_path.endswith(('/', os.sep)):
                    render_path += 'index.html'
                elif not render_path.endswith('.html'):
                    render_path += '.html'

            # save locations of records with languages for search indexes usage
            location = os.path.relpath(
                removesuffix(render_path, 'index.html'),
                config['site_dir'],
            ) + '/'
            self.translations.locations[location] = page.file._mdpo_language

            with open(render_path, 'w') as f:
                f.write(output)
        return output

    def on_post_build(self, config):
        self.translations.tempdir.cleanup()

        if not self.config['cross_language_search']:
            # cross language search is disabled, so build indexes
            # for each language and patch the 'site_dir' directory
            search_patcher = TranslationsSearchPatcher(
                config['site_dir'],
                self.config['languages'],
                self.config['default_language'],
                # use mkdocs 'search' plugin if the theme
                # has not its own implementation
                (
                    config['theme'].name
                    if config['theme'].name
                    in TranslationsSearchPatcher.supported_themes
                    else 'mkdocs'
                ),
                self.translations.locations,
            )
            search_patcher.patch_site_dir()

        # save PO files for not excluded pages
        for translations in self.translations.all.values():
            for translation in translations:
                # po_filepath is None if the file has been excluded from
                # translations using 'exclude' config setting
                if translation.po_filepath is not None:
                    translation.po.save(translation.po_filepath)

        # dump repeated msgids from language files to compendium and
        # remove them from language files
        for language, translations in self.translations.all.items():
            msgids, repeated_msgids = ([], [])
            for translation in translations:
                for msgid in translation.po_msgids:
                    if msgid in msgids:
                        if msgid not in repeated_msgids:
                            repeated_msgids.append(msgid)
                    else:
                        msgids.append(msgid)
            compendium_filepath = self.translations.compendium_files[language]
            compendium_pofile = polib.pofile(compendium_filepath)

            # dump repeated msgids into compendium
            for repeated_msgid in repeated_msgids:
                _repeated_msgid_in_compendium = False
                for entry in compendium_pofile:
                    if entry.msgid == repeated_msgid:
                        _repeated_msgid_in_compendium = True
                        break

                _msgids_appended_to_compendium = []
                for translation in translations:
                    po = polib.pofile(translation.po_filepath)
                    _entry_found = None
                    for entry in po:
                        if entry.msgid == repeated_msgid:
                            if (
                                repeated_msgid not in
                                _msgids_appended_to_compendium and
                                not _repeated_msgid_in_compendium
                            ):
                                compendium_pofile.append(entry)
                                _msgids_appended_to_compendium.append(
                                    repeated_msgid,
                                )
                            _entry_found = entry
                            break
                    if _entry_found:
                        po.remove(_entry_found)
                        po.save(translation.po_filepath)

            for entry in compendium_pofile:
                if entry.msgid not in repeated_msgids:
                    entry.obsolete = True
            compendium_pofile.save(compendium_filepath)

            # mark not found msgstrs as obsolete
            for translation in translations:
                # po_filepath is None if the file has been excluded from
                # translations using 'exclude' config setting
                if translation.po_filepath is not None:
                    po = polib.pofile(translation.po_filepath)
                    for entry in po:
                        if entry.msgid not in translation.translated_msgids:
                            entry.obsolete = True
                    po.save(translation.po_filepath)

        # remove empty compendium files
        for compendium_filepath in self.translations.compendium_files.values():
            with open(compendium_filepath) as f:
                content = f.read()
            if content == '#\nmsgid ""\nmsgstr ""\n':
                os.remove(compendium_filepath)

        # reset mkdocs build instance
        MkdocsBuild._instance = None

    def on_serve(self, *args, **kwargs):  # pragma: no cover
        """When serving with livereload server, prevent a infinite loop
        if the user edits a PO file if is placed inside documentation
        directory.
        """
        if '..' not in self.config['locale_dir']:
            logger.error(
                '[mdpo] -  '
                "You need to set 'locale_dir' configuration setting"
                ' pointing to a directory placed outside'
                " the documentation directory ('docs_dir') in order to"
                ' use the Mkdocs livereload server.\n',
            )
            sys.exit(1)


set_on_build_error_event(MdpoPlugin)
