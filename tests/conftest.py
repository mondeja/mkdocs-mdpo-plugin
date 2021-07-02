"""Configuration for mkdocs_mdpo_plugin tests."""

import os
import sys
from tempfile import TemporaryDirectory

import polib
import pytest
import yaml
from mkdocs import config
from mkdocs.commands.build import build

from mkdocs_mdpo_plugin.plugin import MdpoPlugin


ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


def _mkdocs_build(
    input_files_contents,
    translations,
    plugin_config,
    additional_config,
    expected_output_files,
    callback_after_first_build=None,
    insert_plugin_config_at_position=-1,
    interrupt_after_first_build=False,
):
    with TemporaryDirectory() as site_dir, TemporaryDirectory() as docs_dir, \
            TemporaryDirectory() as config_dir:

        # build input files
        for input_file_name, content in input_files_contents.items():
            filename = os.path.join(docs_dir, input_file_name)
            os.makedirs(
                os.path.abspath(os.path.dirname(filename)),
                exist_ok=True,
            )
            with open(filename, 'w') as f:
                f.write(content)

        mdpo_config = {}
        if plugin_config:
            for mdpo_plugin_config_field, _ in MdpoPlugin.config_scheme:
                if mdpo_plugin_config_field in plugin_config:
                    mdpo_config[mdpo_plugin_config_field] = plugin_config.get(
                        mdpo_plugin_config_field,
                    )

        mkdocs_config = {
            'site_name': 'My site',
            'site_url': 'https://foo.bar',
            'docs_dir': docs_dir,
            'site_dir': site_dir,
            'plugins': [],
        }
        if additional_config:
            mkdocs_config.update(additional_config)
        if insert_plugin_config_at_position == -1:
            mkdocs_config['plugins'].append({'mdpo': mdpo_config})
        else:
            mkdocs_config['plugins'].insert(
                insert_plugin_config_at_position,
                {'mdpo': mdpo_config},
            )

        config_filename = os.path.join(config_dir, 'mkdocs.yml')
        with open(config_filename, 'w') as f:
            yaml.dump(mkdocs_config, f)

        # first build, load content to translations (Markdown -> PO files)
        try:
            build(config.load_config(config_filename))
        except Exception:
            os.remove(config_filename)
            raise

        if callback_after_first_build:
            callback_after_first_build(locals())

        if interrupt_after_first_build:
            os.remove(config_filename)
            return

        # translate PO files
        for po_filename, translation_messages in translations.items():
            po_filename = os.path.join(docs_dir, os.path.normpath(po_filename))
            assert os.path.isfile(po_filename)
            po = polib.pofile(po_filename)

            for msgid_or_msgctxt, msgstr in translation_messages.items():
                if isinstance(msgstr, dict):
                    # case when msgctxt is passed as key
                    # and msgid-msgstr as value in a dict
                    msgid = list(msgstr.keys())[0]
                    msgstr = msgstr[msgid]
                    msgctxt = msgid_or_msgctxt
                else:
                    msgid = msgid_or_msgctxt
                    msgctxt = None

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
                        if msgctxt:
                            entry.msgctxt = msgctxt
                        break

            for entry in po:
                # 'Home' is the title given to the page by the default
                # Mkdocs theme
                if entry.msgid == 'Home':
                    continue
                assert entry.msgstr, (
                    f"Found '{entry.msgid}' not translated in pofile"
                )

            po.save(po_filename)

        # second build, dump translations in content (PO files -> Markdown)
        try:
            build(config.load_config(config_filename))
        except Exception:
            os.remove(config_filename)
            raise

        # assert that files have been translated
        for filename, expected_lines in expected_output_files.items():
            if not expected_lines:
                raise ValueError(
                    'Expected file defined without output lines',
                )

            filename = os.path.join(site_dir, os.path.normpath(filename))

            with open(filename) as f:
                content = f.read()

            for expected_line in expected_lines:
                assert expected_line in content

        os.remove(config_filename)


@pytest.fixture
def mkdocs_build():
    return _mkdocs_build
