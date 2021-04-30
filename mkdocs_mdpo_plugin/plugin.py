"""mkdocs-mdpo-plugin module"""

import os
import re
import shutil
import sys

import mkdocs
import polib
from jinja2 import Template
from mdpo import Po2Md, markdown_to_pofile
from mdpo.md4c import DEFAULT_MD4C_GENERIC_PARSER_EXTENSIONS
from mdpo.command import COMMAND_SEARCH_RE

from mkdocs_mdpo_plugin.ignores import MSGID_IGNORES


COMMAND_SEARCH_RE_AT_LINE_START = re.compile(
    r'^(\s{2,})?[^\\]' + COMMAND_SEARCH_RE.pattern + r'\n?',
    re.M,
)
COMMAND_SEARCH_RE_ESCAPER = re.compile(
    r'\\(' + COMMAND_SEARCH_RE.pattern[:20] + ")(" + COMMAND_SEARCH_RE.pattern[20:38] + '?=' + COMMAND_SEARCH_RE.pattern[38:] + ')',
    re.M,
)
MKDOCS_MINOR_VERSION_INFO = tuple(int(n) for n in mkdocs.__version__.split(".")[:2])


def remove_mdpo_commands_preserving_escaped(text):
    return re.sub(
        # restore escaped commands
        '<!-- mdpo-0',
        '<!-- mdpo',
        re.sub(
            # remove commands
            COMMAND_SEARCH_RE_AT_LINE_START,
            '',
            # escaped commands
            re.sub(
                COMMAND_SEARCH_RE_ESCAPER,
                r'\g<1>0-\g<2>',
                text,
            ),
        )
    )


class MkdocsBuild(object):
    """Represents the mkdocs build process.

    Is a singleton, so only accepts one build. Should be initialized using
    the `instance` class method, which accepts an instance of the plugin class.
    """
    _instance = None

    @classmethod
    def instance(cls, mdpo_plugin):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls.mdpo_plugin = mdpo_plugin
        return cls._instance


class MdpoPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ('locale_dir', mkdocs.config.config_options.Type(str, default='')),
        ("default_language", mkdocs.config.config_options.Type(str, required=False)),
        ('languages', mkdocs.config.config_options.Type(list, required=False)),
        ("lc_messages", mkdocs.config.config_options.Type((str, bool), default="")),
        (
            'dest_filename_template',
            mkdocs.config.config_options.Type(
                str,
                default='{{language}}/{{page.file.dest_path}}',
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        #  temporal translated pages created by the plugin at runtime
        self._temp_pages_to_remove = []

        # md4c extensions used in mdpo translation (depend on Python-Markdown
        # configured extensions in `mkdocs.yml`)
        self._md4c_extensions = DEFAULT_MD4C_GENERIC_PARSER_EXTENSIONS

        # 'ignore' attribute for md2po
        self._msgids_to_ignore = []

        # navigation translation
        # {original_title: {lang: {title: [translation, url]}}}
        self.__translated_nav = {}

        # information needed by `mkdocs.mdpo` extension
        #
        #   instance that represents the run
        MkdocsBuild.instance(self)
        #   current page being rendered
        self.current_page = None
        #   configuration of the build (loaded at `on_config` method)
        self.mkdocs_build_config = None

        super().__init__(*args, **kwargs)

    def _non_default_languages(self):
        for language in self.config["languages"]:
            if language != self.config["default_language"]:
                yield language

    def _language_dir(self, base_dir, language):
        return os.path.join(
            base_dir,
            self.config["locale_dir"],
            language,
            self.config["lc_messages"],
        )

    def on_config(self, config, **kwargs):
        """Configuration for `mkdocs_mdpo_plugin`.

        * Define properly `lc_messages`, `languages` and `locale_dir`
          configuration settings.
        * Loads `mkdocs.mdpo` extension.
        * Configures md4c extensions accordingly to Python-Markdown extensions.
        * Stores the build configuration in `mkdocs_build_config` property
          of the plugin instance.
        """
        if self.config["lc_messages"] is True:
            self.config["lc_messages"] = "LC_MESSAGES"
        elif not self.config["lc_messages"]:
            self.config["lc_messages"] = ""

        def _type_error(plugin_setting, expected_type):
            return mkdocs.config.base.ValidationError(
                f"'plugins.mdpo.{plugin_setting}' must be a {expected_type}"
            )

        _using_material_theme = config["theme"].name == "material"

        # load language selection settings from material or mdpo configuration
        def _languages_required():
            msg = ("You must define the languages you will translate the"
                   " content into using"
                   f"{' either' if _using_material_theme else ' the'}"
                   " 'plugins.mdpo.languages'")
            if _using_material_theme:
                msg += " or 'extra.alternate'"
            msg += (" configuration setting"
                    f"{'s' if _using_material_theme else ''}.")
            return mkdocs.config.base.ValidationError(msg)

        def _default_language_required():
            msg = ("You must define the original language for translations using"
                   f" {'either ' if _using_material_theme else 'the '}"
                   " 'plugins.mdpo.default_language'")
            if _using_material_theme:
                msg += " or 'theme.language'"
            msg += (" configuration setting"
                    f"{'s' if _using_material_theme else ''}.")
            return mkdocs.config.base.ValidationError(msg)

        languages = self.config.get("languages")
        if not languages:
            if _using_material_theme:
                if "extra" not in config:
                    raise _languages_required()
                alternate = config["extra"].get("alternate")
                if not alternate:
                    raise _languages_required()
                self.config["languages"] = [l["lang"] for l in alternate]
            else:
                raise _languages_required()
        elif not isinstance(languages, list):
            raise _type_error("languages", "list")

        default_language = self.config.get("default_language")
        if not default_language:
            if _using_material_theme:
                if "language" not in config["theme"]:
                    raise _languages_required()
                self.config["default_language"] = config["theme"]["language"]
            else:
                self.config["default_language"] = self.config["languages"][0]
        elif not isinstance(default_language, str):
            raise _type_error("default_language", "str")

        # configure MD4C extensions
        if "tables" not in config["markdown_extensions"]:
            if "tables" in self._md4c_extensions:
                self._md4c_extensions.remove("tables")
        if "wikilinks" not in config["markdown_extensions"]:
            if "wikilinks" in self._md4c_extensions:
                self._md4c_extensions.remove("wikilinks")

        # spaces after '#' are optional in Python-Markdown for headers,
        # but the extension 'pymdownx.saneheaders' makes them mandatory
        if "pymdownx.saneheaders" in config["markdown_extensions"]:
            if "permissive_atx_headers" in self._md4c_extensions:
                self._md4c_extensions.remove("permissive_atx_headers")
        else:
            if "permissive_atx_headers" not in self._md4c_extensions:
                self._md4c_extensions.append("permissive_atx_headers")

        # 'pymdownx.tasklist' enables 'tasklists' MD4C extentsion
        if "pymdownx.tasklist" in config["markdown_extensions"]:
            if "tasklists" not in self._md4c_extensions:
                self._md4c_extensions.append("tasklists")
        else:
            if "tasklists" in self._md4c_extensions:
                self._md4c_extensions.remove("tasklists")

        # 'pymdownx.tilde' enables strikethrough syntax, but only works
        # if the MD4C extension is disabled
        if "pymdownx.tilde" in config["markdown_extensions"]:
            if "strikethrough" in self._md4c_extensions:
                self._md4c_extensions.remove("strikethrough")

        # configure internal 'mkdocs.mdpo' extension
        if "mkdocs.mdpo" in config["markdown_extensions"]:
            config["markdown_extensions"].remove("mkdocs.mdpo")
        config["markdown_extensions"].append("mkdocs.mdpo")

        # load msgid to ignore
        for extension, msgids in MSGID_IGNORES.items():
            if not extension or extension in config["markdown_extensions"]:
                self._msgids_to_ignore.extend(msgids)

        # store reference in plugin to configuration
        self.mkdocs_build_config = config

    def on_pre_build(self, config):
        """Create locales folders inside documentation directory."""

        for language in self._non_default_languages():
            os.makedirs(
                os.path.join(
                    self._language_dir(config["docs_dir"], language),
                ),
                exist_ok=True,
            )

    def on_files(self, files, config):
        """Remove locales directory from collected files.

        NOTE: Since mkdocs 1.2.X, there is a new method ``remove`` for
              files which will simplify the code defined in this event.
        """
        new_files = mkdocs.structure.files.Files([])
        for file in files:
            # exclude all files with PO related extensions
            if os.path.splitext(file.src_path)[-1] not in (".po", ".pot", ".mo"):
                new_files.append(file)
        return new_files

    def on_page_context(self, context, page, config, nav):
        """Navigation translation."""
        if not hasattr(page, "_language"):
            return

        # Si estamos usando el tema mkdocs-material, configuramos el idioma
        # correspondiente para cada página
        if context["config"]["theme"].name == "material":
            context["config"]["theme"]["language"] = (
                page._language if hasattr(page, "_language") else
                self.config["default_language"]
            )

        for item in nav:
            if item.title not in self.__translated_nav:
                continue
            tr_title, tr_url = self.__translated_nav[item.title][page._language]
            if tr_title:
                item.title = tr_title
            item.file.url = tr_url

    def on_page_content(self, content, *args, **kwargs):
        """Useful for debugging."""
        # print(content)
        pass

    def on_page_markdown(self, markdown, page, config, files):
        """Event executed when markdown content of a page is collected.

        Here happen most of the logic handled by the plugin:

        * For each documentation page, creates another documentation page
          for each language that will be translated (part here and part
          inside the `mkdocs.mdpo` extension, see
          :py:mod:`mkdocs_mdpo_plugin.extension` module).
        """
        # don't process again translated pages
        if hasattr(page, "_language"):
            return

        if page.title not in self.__translated_nav:
            # lang: [title, url]
            self.__translated_nav[page.title] = {}

        original_po = markdown_to_pofile(
            markdown,
            ignore_msgids=self._msgids_to_ignore,
        )

        for language in self._non_default_languages():
            po_filepath = os.path.join(
                self._language_dir(config["docs_dir"], language),
                f"{page.file.src_path}.po",
            )
            os.makedirs(
                os.path.abspath(os.path.dirname(po_filepath)),
                exist_ok=True,
            )
            if not os.path.isfile(po_filepath):
                po = polib.POFile()
            else:
                po = polib.pofile(po_filepath)
            po.merge(original_po)

            # translate title
            translated_page_title, _title_in_pofile = (None, False)
            for entry in po:
                if entry.msgid == page.title:
                    _title_in_pofile = True
                    if entry.obsolete:
                        entry.obsolete = False
                    translated_page_title = entry.msgstr
            if not _title_in_pofile:
                po.insert(0, polib.POEntry(msgid=page.title, msgstr=""))

            po.save(po_filepath)

            po2md = Po2Md(po_filepath)
            content = remove_mdpo_commands_preserving_escaped(
                po2md.translate(markdown),
            )

            # create site language dir if not exists
            os.makedirs(
                self._language_dir(config["site_dir"], language),
                exist_ok=True,
            )

            # render destination filepath
            context = locals()
            context.update(self.config)
            del context["self"]
            dest_path = Template(
                self.config["dest_filename_template"],
            ).render(**context)
            src_path = f"{dest_path.rstrip('.html')}.md"

            # This is really a hack but it works very well
            #
            # The current Mkdocs approach doesn't provide a way to add new
            #   documentation pages on the fly when a page is being populated,
            #   so we need to create a temporal page inside the locales
            #   directory and populate them manually
            src_abs_path = os.path.abspath(os.path.join(config["docs_dir"], src_path))
            self._temp_pages_to_remove.append(src_abs_path)
            os.makedirs(os.path.dirname(src_abs_path), exist_ok=True)
            with open(src_abs_path, "w") as f:
                f.write(content)

            new_file = mkdocs.structure.files.File(
                src_path,
                config["docs_dir"],
                config["site_dir"],
                config["use_directory_urls"],
            )
            new_page = mkdocs.structure.pages.Page(
                translated_page_title,
                new_file,
                config,
            )

            # attach useful information inside the new translated page object
            new_page._language = language
            new_page._po = po
            new_page._po_filepath = po_filepath
            new_page._po_disabled_entries = po2md.disabled_entries
            files.append(new_file)

            self.__translated_nav[page.title][language] = [
                translated_page_title, new_page.url,
            ]

            self.current_page = new_page

            mkdocs.commands.build._populate_page(
                new_page,
                config,
                files,
                dirty=(
                    '--dirty' in sys.argv and
                    '-c' not in sys.argv and '--clean' not in sys.argv
                )
            )

        self.current_page = page

        return remove_mdpo_commands_preserving_escaped(markdown)

    def _remove_temp_pages(self):
        """Remove temporal generated pages."""
        for filepath in self._temp_pages_to_remove:
            self._remove_temp_page(filepath)

    def _remove_temp_page(self, filepath):
        os.remove(filepath)

        parent_dir = os.path.abspath(os.path.dirname(filepath))
        if not os.listdir(parent_dir):
            os.rmdir(parent_dir)

    def on_post_build(self, config):
        self._remove_temp_pages()

        # remove empty directories from site_dir
        for root, dirs, files in os.walk(config["site_dir"], topdown=False):
            if not os.listdir(root):
                os.rmdir(root)


# mkdocs>=1.2.0 includes a `build_error` event executed when the build
# triggers a exception. The next patch provides the same cleanup functionality
# if the `build_error` event is not supported:
def __on_build_error(_self):
    for filepath in _self._temp_pages_to_remove:
        try:
            _self._remove_temp_page(filepath)
        except FileNotFoundError:
            pass

if MKDOCS_MINOR_VERSION_INFO >= (1, 2):
    def _on_build_error(self, error):
        return __on_build_error(self)

    MdpoPlugin.on_build_error = _on_build_error
else:
    import atexit

    def _on_build_error():
        build_instance = MkdocsBuild()
        if hasattr(build_instance, "mdpo_plugin"):
            return __on_build_error(build_instance.mdpo_plugin)

    atexit.register(_on_build_error)
