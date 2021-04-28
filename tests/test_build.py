"""mkdocs builds tests for mkdocs-mdpo-plugin"""

import os
import tempfile
import yaml
from tempfile import TemporaryDirectory

import pytest

import polib
from mkdocs import config
from mkdocs.commands.build import build as mkdocs_build

from tests.config_suite import CONFIGURATION_TESTS
from tests.extensions_suite import (
    EXTENSION_TO_TEST,
    OFFICIALLY_SUPPORTED_EXTENSIONS_TESTS,
)



@pytest.mark.parametrize(
    (
        "input_files",
        "translations",
        "locale_dir",
        "default_language",
        "languages",
        "dest_filename_template",
        "lc_messages",
        "additional_config",
        "expected_output_files",
    ),
    (
        #*CONFIGURATION_TESTS,
        *EXTENSION_TO_TEST,
    )
)
def test_mdpo_plugin_build(
    input_files,
    translations,
    locale_dir,
    default_language,
    languages,
    dest_filename_template,
    lc_messages,
    additional_config,
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

        mdpo_config = {}
        if locale_dir is not None:
            mdpo_config["locale_dir"] = locale_dir
        if dest_filename_template is not None:
            mdpo_config["dest_filename_template"] = dest_filename_template
        if default_language is not None:
            mdpo_config["default_language"] = default_language
        if languages is not None:
            mdpo_config["languages"] = languages
        if lc_messages is not None:
            mdpo_config["lc_messages"] = lc_messages

        mkdocs_config = {
            "site_name": "foo",
            "docs_dir": docs_dir,
            "site_dir": site_dir,
            "plugins": [
                {"mdpo": mdpo_config}
            ]
        }
        if additional_config:
            mkdocs_config.update(additional_config)

        config_filename = os.path.join(config_dir, "mkdocs.yml")
        with open(config_filename, "w") as f:
            yaml.dump(mkdocs_config, f)

        # first build, load content to translations (Markdown -> PO files)
        mkdocs_build(config.load_config(config_filename))

        # translate PO files
        for po_filename, translation_messages in translations.items():
            po_filename = os.path.join(docs_dir, os.path.normpath(po_filename))
            assert os.path.isfile(po_filename)

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

        # second build, dump translations in content (PO files -> Markdown)
        mkdocs_build(config.load_config(config_filename))

        # assert that files have been translated
        for filename, expected_lines in expected_output_files.items():
            filename = os.path.join(site_dir, os.path.normpath(filename))

            with open(filename, "r") as f:
                content = f.read()

            for expected_line in expected_lines:
                assert expected_line in content
