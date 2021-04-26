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
        ('locales_dir', mkdocs.config.config_options.Type(str, default='')),
        ("default_language", mkdocs.config.config_options.Type(str, required=True)),
        ('languages', mkdocs.config.config_options.Type(list, required=False)),
        (
            'dest_filename_template',
            mkdocs.config.config_options.Type(
                str,
                default='{{language}}/{{page.file.dest_path}}',
            ),
        )
    )
    
    def __init__(self, *args, **kwargs):
        self.__temp_pages_to_remove = []
        super().__init__(*args, **kwargs)
    
    def _non_default_languages(self):
        for language in self.config["languages"]:
            if language != self.config["default_language"]:
                yield language
    
    def _language_dir(self, language, base_dir):
        return os.path.join(base_dir, self.config["locales_dir"], language)

    def on_pre_build(self, config):
        """Create 'locales/' folders inside documentation directory."""
        for language in self._non_default_languages():
            os.makedirs(
                self._language_dir(language, config["docs_dir"]), exist_ok=True,
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

    
    def on_page_markdown(self, markdown, page, config, files):
        if hasattr(page, "_MdpoPlugin__abort_on_page_markdown"):
            return

        po_filename = f"{page.file.src_path.replace(os.sep, '_')}.po"

        for language in self._non_default_languages():
            po_filepath = os.path.join(
                self._language_dir(language, config["docs_dir"]),
                po_filename,
            )
            po = markdown_to_pofile(markdown, po_filepath=po_filepath)

            # translate title
            translated_page_title, _title_in_pofile = (None, False)
            for entry in po:
                if entry.msgid == page.title:
                    _title_in_pofile = True
                    translated_page_title = entry.msgstr
            if not _title_in_pofile:
                po.insert(0, polib.POEntry(msgid=page.title, msgstr=""))

            po.save(po_filepath)
            content = pofile_to_markdown(markdown, po_filepath)
            
            # create site language dir if not exists
            os.makedirs(
                self._language_dir(language, config["site_dir"]),
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
            # The current approach of Mkdocs doesn't provide a way to add new
            #   documentation pages on the fly when the first page is being
            #   populated, so we need to create a temporal page inside the
            #   locales directory and populate them manually
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
            files.append(new_file)

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
        """
        Derived from mkdocs commands build function.
        We build every language on its own directory.
        """
        for filepath in self.__temp_pages_to_remove:
            os.remove(filepath)
