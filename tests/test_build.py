"""mkdocs builds tests for mkdocs-mdpo-plugin"""

import os
import tempfile
import yaml
from tempfile import TemporaryDirectory

import pytest

import polib
from mkdocs import config
from mkdocs.commands.build import build as mkdocs_build


@pytest.mark.parametrize(
    (
        "input_files",
        "translations",
        "locale_dir",
        "default_language",
        "languages",
        "dest_filename_template",
        "expected_output_files",
    ),
    (
        (
            # basic example with default configuration
            {
                "index.md": "# Foo\n\nbar\n",
            },
            {
                "es/index.md.po": {
                    "Foo": "Foo es",
                    "bar": "bar es",
                },
            },
            None,
            "en",
            ["en", "es"],
            None,
            {
                "index.html": [
                    '<h1 id="foo">Foo</h1>',
                    '<p>bar</p></div>',
                ],
                "es/index.html": [
                    '<h1 id="foo-es">Foo es</h1>',
                    '<p>bar es</p>',
                ],
            }
        ),
        (
            # nested files 
            {
                "index.md": "foo\n",
                "foo/bar/baz.md": "hello\n",
            },
            {
                "es/index.md.po": {
                    "foo": "foo es",
                },
                "es/foo/bar/baz.md.po": {
                    "hello": "hola",
                }
            },
            None,
            "en",
            ["en", "es"],
            None,
            {
                "index.html": ["<p>foo</p>"],
                "es/index.html": ["<p>foo es</p>"],
                "foo/bar/baz/index.html": ["<p>hello</p>"],
                "es/foo/bar/baz/index.html": ["<p>hola</p>"],
            }
        ),
        (
            # custom locale_dir
            {
                "index.md": "foo\n",
            },
            {
                "locales/es/index.md.po": {
                    "foo": "foo es",
                },
            },
            "locales",
            "en",
            ["en", "es"],
            None,
            {
                "index.html": ["<p>foo</p>"],
                "es/index.html": ["<p>foo es</p>"],
            }
        )
    )
)
def test_mdpo_plugin_build(
    input_files,
    translations,
    locale_dir,
    default_language,
    languages,
    dest_filename_template,
    expected_output_files,
):
    with TemporaryDirectory() as site_dir, TemporaryDirectory() as docs_dir, \
            TemporaryDirectory() as config_dir:
        
        # build input files
        for input_file_name, input_file_content in input_files.items():
            filename = os.path.join(docs_dir, input_file_name)
            os.makedirs(os.path.abspath(os.path.dirname(filename)), exist_ok=True)
            with open(filename, "w") as f:
                f.write(input_file_content)
        
        mdpo_config = {"default_language": default_language, "languages": languages}
        if locale_dir is not None:
            mdpo_config["locale_dir"] = locale_dir
        if dest_filename_template is not None:
            mdpo_config["dest_filename_template"] = dest_filename_template
        mkdocs_config = {
            "site_name": "foo",
            "docs_dir": docs_dir,
            "site_dir": site_dir,
            "plugins": [
                {"mdpo": mdpo_config}
            ]
        }

        config_filename = os.path.join(config_dir, "mkdocs.yml")
        with open(config_filename, "w") as f:
            yaml.dump(mkdocs_config, f)
        
        # first build, load content to translations (Markdown -> pofiles)
        mkdocs_build(config.load_config(config_filename))
        
        # translate pofiles
        for po_filename, translation_messages in translations.items():
            po_filename = os.path.join(docs_dir, os.path.normpath(po_filename))
            po = polib.pofile(po_filename)
    
            for msgid, msgstr in translation_messages.items():
                _msgid_in_pofile = False
                for entry in po:
                    if entry.msgid == msgid:
                        _msgid_in_pofile = True
                        break
                
                assert _msgid_in_pofile, (
                    f"'{msgid}' not found in pofile '{po_filename}'"
                )
            
                for entry in po:
                    if entry.msgid == msgid:
                        entry.msgstr = msgstr
                        break
            po.save(po_filename)
        
        # second build, dump translations in content (pofiles -> Markdown)
        mkdocs_build(config.load_config(config_filename))
        
        # assert that files have been translated
        for filename, expected_lines in expected_output_files.items():
            filename = os.path.join(site_dir, os.path.normpath(filename))
            
            with open(filename, "r") as f:
                content = f.read()

            for expected_line in expected_lines:
                assert expected_line in content
    