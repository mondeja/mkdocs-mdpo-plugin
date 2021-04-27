"""mkdocs-mdpo-plugin module"""

import os
import shutil
import sys

import mkdocs
import polib
from jinja2 import Template
from mdpo import markdown_to_pofile, pofile_to_markdown


class MdpoPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ('locale_dir', mkdocs.config.config_options.Type(str, default='')),
        ("default_language", mkdocs.config.config_options.Type(str, required=False)),
        ('languages', mkdocs.config.config_options.Type(list, required=False)),
        (
            'dest_filename_template',
            mkdocs.config.config_options.Type(
                str,
                default='{{language}}/{{page.file.dest_path}}',
            ),
        ),
        ("lc_messages", mkdocs.config.config_options.Type((str, bool), default="")),
    )

    def __init__(self, *args, **kwargs):
        self.__temp_pages_to_remove = []
        self.__translated_nav = {} # original_title, translations, url
        
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
        if self.config["lc_messages"] is True:
            self.config["lc_messages"] = "LC_MESSAGES"
        elif not self.config["lc_messages"]:
            self.config["lc_messages"] = ""
            
        def _type_error(plugin_setting, expected_type):
            return mkdocs.config.base.ValidationError(
                f"'plugins.mdpo.{plugin_setting}' must be a {expected_type}"
            )
        
        _material_theme_configured = config["theme"].name == "material"

        # load language selection settings from material or mdpo configuration
        def _languages_required():
            msg = ("You must define the languages you will translate the"
                   " content into using"
                   f"{' either' if _material_theme_configured else ' the'}"
                   " 'plugins.mdpo.languages'")
            if _material_theme_configured:
                msg += " or 'extra.alternate'"
            msg += (" configuration setting"
                    f"{'s' if _material_theme_configured else ''}.")
            return mkdocs.config.base.ValidationError(msg)
        
        def _default_language_required():
            msg = ("You must define the original language for translations using"
                   f" {'either ' if _material_theme_configured else 'the '}"
                   " 'plugins.mdpo.default_language'")
            if _material_theme_configured:
                msg += " or 'theme.language'"
            msg += (" configuration setting"
                    f"{'s' if _material_theme_configured else ''}.")
            return mkdocs.config.base.ValidationError(msg)

        languages = self.config.get("languages")
        if not languages:
            if _material_theme_configured:
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
            if _material_theme_configured:
                if "language" not in config["theme"]:
                    raise _languages_required()
                self.config["default_language"] = config["theme"]["language"]
            else:
                self.config["default_language"] = self.config["languages"][0]
        elif not isinstance(default_language, str):
            raise _type_error("default_language", "str")

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
            if os.path.splitext(file.src_path)[-1] != ".po":
                new_files.append(file)
        return new_files
    
    def on_page_context(self, context, page, config, nav):
        """Navigation translation."""
        if not hasattr(page, "_language"):
            return
        
        for item in nav:
            if item.title not in self.__translated_nav:
                continue
            tr_title, tr_url = self.__translated_nav[item.title][page._language]
            item.title = tr_title
            item.file.url = tr_url

    def on_page_markdown(self, markdown, page, config, files):
        if hasattr(page, "_MdpoPlugin__abort_on_page_markdown"):
            return

        if page.title not in self.__translated_nav:
            # lang: [title, url]
            self.__translated_nav[page.title] = {}
        
        for language in self._non_default_languages():
            po_filepath = os.path.join(
                self._language_dir(config["docs_dir"], language),
                f"{page.file.src_path}.po",
            )
            os.makedirs(os.path.abspath(os.path.dirname(po_filepath)), exist_ok=True)
            po = markdown_to_pofile(markdown, po_filepath=po_filepath)
            

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
            content = pofile_to_markdown(markdown, po_filepath)
            
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
            #   documentation pages on the fly when a page is being  populated,
            #   so we need to create a temporal page inside the locales
            #   directory and populate them manually
            src_abs_path = os.path.abspath(os.path.join(config["docs_dir"], src_path))
            self.__temp_pages_to_remove.append(src_abs_path)
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
            new_page.__abort_on_page_markdown = True
            new_page._language = language
            files.append(new_file)
            
            self.__translated_nav[page.title][language] = [
                translated_page_title, new_page.url,
            ]
        
            mkdocs.commands.build._populate_page(
                new_page,
                config,
                files,
                dirty=(
                    '--dirty' in sys.argv and
                    '-c' not in sys.argv and '--clean' not in sys.argv
                )
            )

    def on_post_build(self, config):
        """Cleanup."""
        for filepath in self.__temp_pages_to_remove:
            os.remove(filepath)
            
            parent_dir = os.path.abspath(os.path.dirname(filepath))
            if not os.listdir(parent_dir):
                os.rmdir(parent_dir)
        
        # remove empty directories from site_dir
        for root, dirs, files in os.walk(config["site_dir"], topdown=False):
            if not os.listdir(root):
                os.rmdir(root)        
