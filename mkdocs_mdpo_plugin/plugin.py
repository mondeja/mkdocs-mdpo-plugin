"""mkdocs-mdpo-plugin module"""

import functools
import logging
import math
import os
import re
import sys
from urllib.parse import urljoin

import jinja2
import mkdocs
import polib
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
    remove_mdpo_setting_tags_from_po_entry,
)
from mkdocs_mdpo_plugin.mkdocs_utils import (
    MkdocsBuild,
    get_lunr_languages,
    set_on_build_error_event,
)
from mkdocs_mdpo_plugin.search_indexes import TranslationsSearchPatcher
from mkdocs_mdpo_plugin.translations import Translation, Translations
from mkdocs_mdpo_plugin.utils import (
    po_messages_stats,
    readable_float,
    removepreffix,
    removesuffix,
)


logger = logging.getLogger('mkdocs.plugins.mdpo')


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
    def _translation_languages(self):
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

    on_config = on_config_event

    def on_pre_build(self, config):
        """Create locales folders inside documentation directory."""
        for language in self._translation_languages():
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

                for language in self._translation_languages():
                    # render destination path
                    context = {'file': file, 'language': language}
                    context.update(self.config)
                    dest_path = jinja2.Template(
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

        for language in self._translation_languages():
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

                # translate metadata and config settings
                #
                # translate title
                translated_page_title, _title_in_pofile = (None, False)
                # translated custom description
                page_meta_description = page.meta.get('description')
                translated_page_desc, _desc_in_pofile = (None, False)

                # translate site_name and site_description
                translated_config_settings = {
                    key: None for key in self.config['translate']
                }
                _config_settings_in_pofile = {
                    key: False for key in self.config['translate']
                }

                if page_meta_description:
                    for entry in po:
                        if entry.msgid == page.title:
                            # matching title found
                            entry.obsolete = False
                            translated_page_title = entry.msgstr
                            _title_in_pofile = True
                            if entry.msgstr:
                                _translated_entries_msgstrs.append(
                                    entry.msgstr,
                                )

                        if entry.msgid == page_meta_description:
                            # matching description found
                            entry.obsolete = False
                            translated_page_desc = entry.msgstr
                            _desc_in_pofile = True
                            if entry.msgstr:
                                _translated_entries_msgstrs.append(
                                    page_meta_description,
                                )

                    # add description to PO file if not added
                    if not _desc_in_pofile:
                        po.insert(
                            0,
                            polib.POEntry(
                                msgid=page_meta_description,
                                msgstr='',
                            ),
                        )

                        _translated_entries_msgids.append(
                            page_meta_description,
                        )
                else:
                    for entry in po:
                        if entry.msgid == page.title:
                            # matching title found
                            entry.obsolete = False
                            translated_page_title = entry.msgstr
                            _title_in_pofile = True
                            if entry.msgstr:
                                _translated_entries_msgstrs.append(
                                    entry.msgstr,
                                )

                for entry in compendium_pofile:
                    for setting in translated_config_settings:
                        if entry.msgid == config[setting]:
                            # matching translated setting found
                            entry.obsolete = False
                            translated_config_settings[setting] = entry.msgstr
                            _config_settings_in_pofile[setting] = True
                            _translated_entries_msgids.append(config[setting])
                            if entry.msgstr:
                                _translated_entries_msgstrs.append(
                                    entry.msgstr,
                                )
                            if f'mdpo-{setting}' not in entry.flags:
                                entry.flags.append(f'mdpo-{setting}')

                # add title to PO file if not added
                if not _title_in_pofile:
                    po.insert(
                        0,
                        polib.POEntry(msgid=page.title, msgstr=''),
                    )
                    _translated_entries_msgids.append(page.title)

                # add translatable configuration settings to PO file
                for setting, _translated in _config_settings_in_pofile.items():
                    if not _translated:
                        compendium_pofile.insert(
                            0,
                            polib.POEntry(
                                msgid=config[setting],
                                msgstr='',
                                flags=[f'mdpo-{setting}'],
                            ),
                        )
                compendium_pofile.save(compendium_filepath)

                # add temporally compendium entries to language pofiles
                for entry in compendium_pofile:
                    if entry not in po and entry.msgstr:
                        po.append(entry)
                po.save(po_filepath)

                # if a minimum number of translations are required to include
                # the file, compute number of untranslated messages
                if min_translated:
                    n_translated, n_total = po_messages_stats(po)
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
                if page_meta_description:
                    po2md.translated_entries.append(
                        polib.POEntry(
                            msgid=page_meta_description,
                            msgstr='',
                        ),
                    )
                po2md.translated_entries.append(
                    polib.POEntry(
                        msgid=page.title,
                        msgstr='',
                    ),
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
                translated_page_desc = None
                _disabled_msgids = []
                _translated_entries_msgstrs = []
                _translated_entries_msgids = []
                po, po_filepath = [], None
                translated_config_settings = {}

            temp_abs_path = self.translations.files[
                page.file.src_path
            ][language]
            temp_abs_dirpath = os.path.dirname(temp_abs_path)
            os.makedirs(temp_abs_dirpath, exist_ok=True)
            with open(temp_abs_path, 'w', encoding='utf-8') as f:
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

            new_page_title = translated_page_title or page.title
            new_page = mkdocs.structure.pages.Page(
                new_page_title,
                new_file,
                config,
            )
            if translated_page_desc:
                new_page.meta['description'] = translated_page_desc

            # overwrite the edit uri for the translated page targetting
            # the PO file located in the repository
            if config.get('repo_url') and config.get('edit_uri'):
                new_page.edit_url = urljoin(
                    config['repo_url'],
                    os.path.normpath(
                        os.path.join(
                            config['edit_uri'],
                            os.path.relpath(po_filepath, config['docs_dir']),
                        ),
                    ),
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
            if language not in self.translations.config_settings:
                self.translations.config_settings[language] = (
                    translated_config_settings
                )
            if language not in self.translations.page_metas:
                self.translations.page_metas[language] = {}
            if (
                new_file.src_path
                not in self.translations.page_metas[language]
            ):
                self.translations.page_metas[
                    language
                ][new_file.src_path] = new_page.meta

            # change file url
            url = removesuffix(new_page.file.url, '.md') + '.html'
            if config['use_directory_urls']:
                url = removesuffix(url, 'index.html')
            new_page.file.url = url

            # the title of the page will be 'page.title' (the original)
            # if the file is being excluded from translations using the
            # 'exclude' plugin's config setting
            self.translations.nav[page.title][language] = [
                new_page_title, new_page.file.url,
            ]

            # set languages for search when 'cross_language_search'
            # is disabled
            #
            # if it is enabled, this configuration is handled in the
            # `on_config` event
            if self.config['cross_language_search'] is False:
                if (
                    config['theme'].name != 'material' and
                    'search' in config['plugins']
                ):
                    # Mkdocs theme languages
                    lunr_languages = get_lunr_languages()
                    search_langs = (
                        config['plugins']['search'].config['lang'] or []
                    )
                    if language in lunr_languages:
                        if language not in search_langs:
                            # set only the language to search
                            config['plugins']['search'].config['lang'] = (
                                [language]
                            )
                            logger.debug(
                                f"[mdpo] Setting ['{language}'] for"
                                " 'plugins.search.lang' option",
                            )
                    elif language != 'en':
                        logger.info(
                            f"[mdpo] Language '{language}' is not supported by"
                            ' lunr.js, not setting it for'
                            " 'plugins.search.lang' option",
                        )

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

        # reconfigure default language for plugins and themes after
        # translated pages are built
        if (
            config['theme'].name != 'material'
            and 'search' in config['plugins']
            and hasattr(config['plugins']['search'], 'lang')
        ):
            config['plugins']['search'].config['lang'] = [
                self.config['default_language'],
            ]

        # set languages to render in sitemap.xml
        page.file._mdpo_languages = _mdpo_languages

        return remove_mdpo_commands_preserving_escaped(markdown)

    def on_post_page(self, output, page, config):
        if hasattr(page.file, '_mdpo_language'):
            language = page.file._mdpo_language

            # if the language should be included from the build, ignore it
            min_translated = self.config['min_translated_messages']
            if min_translated:

                stats = self.translations.stats[language]
                if abs(min_translated) != min_translated:  # percent
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
                        if min_translated > stats['total']:
                            logger.warning(
                                '[mdpo] Found more required translated'
                                f' messages ({min_translated}) than total of'
                                f' them ({stats["total"]}). Using'
                                f' {stats["total"]} for'
                                ' "min_translated_messages" value.',
                            )
                            min_translated = stats['total']

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

            # translate title and description replacing directly in HTML
            if language in self.translations.config_settings:
                tr_settings = self.translations.config_settings[language]

                if tr_settings.get('site_name'):
                    output = output.replace(
                        f'{config["site_name"]}</title>',
                        f'{tr_settings["site_name"]}</title>',
                    )

                meta_description = self.translations.page_metas[
                    language
                ][page.file.src_path].get('description')

                if (
                    meta_description or
                    tr_settings.get('site_description') or
                    config.get('site_description')
                ):
                    if meta_description:
                        tr_description = meta_description
                    elif tr_settings.get('site_description'):
                        tr_description = tr_settings['site_description']
                    elif config.get('site_description'):
                        tr_description = config['site_description']

                    if '<meta name="description"' not in output:
                        output = output.replace(
                            '/title>',
                            (
                                '/title><meta name="description"'
                                ' content="">'
                            ),
                        )

                    if not (
                        config['theme'].name in {'mkdocs', 'readthedocs'} and
                        removepreffix(page.file.url, language).count('/') > 1
                    ):
                        output = re.sub(
                            r'<meta name="description" content="[^"]*"',
                            (
                                '<meta name="description"'
                                f' content="{tr_description}"'
                            ),
                            output,
                        )

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

            with open(render_path, 'w', encoding='utf-8') as f:
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
                    _entry_found = None
                    for entry in translation.po:
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
                        translation.po.remove(_entry_found)
                        translation.po.save(translation.po_filepath)

            for entry in compendium_pofile:
                if entry.msgid not in repeated_msgids:
                    # translation of site_name and site_description
                    if (
                        'mdpo-site_description' in entry.flags or
                        'mdpo-site_name' in entry.flags
                    ):
                        remove_mdpo_setting_tags_from_po_entry(entry)
                    else:
                        entry.obsolete = True
                else:
                    remove_mdpo_setting_tags_from_po_entry(entry)

            if len(compendium_pofile):
                compendium_pofile.save(compendium_filepath)
            else:
                # remove empty compendium files
                os.remove(compendium_filepath)

            # mark not found msgstrs as obsolete
            for translation in translations:
                # po_filepath is None if the file has been excluded from
                # translations using 'exclude' config setting
                if translation.po_filepath is not None:
                    for entry in translation.po:
                        if entry.msgid not in translation.translated_msgids:
                            entry.obsolete = True
                    translation.po.save(translation.po_filepath)

        # reset mkdocs build instance
        MkdocsBuild._instance = None

    def on_serve(self, *args, **kwargs):  # pragma: no cover
        """When serving with livereload server, prevent a infinite loop
        if the user edits a PO file if is placed inside documentation
        directory.
        """
        if '..' not in self.config['locale_dir']:
            logger.error(
                '[mdpo] '
                "You need to set 'locale_dir' configuration setting"
                ' pointing to a directory placed outside'
                " the documentation directory ('docs_dir') in order to"
                ' use the Mkdocs livereload server.\n',
            )
            sys.exit(1)


set_on_build_error_event(MdpoPlugin)
