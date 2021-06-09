"""Mkdocs builds tests for mkdocs-mdpo-plugin Navigation and page building
plugins support:
https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins#navigation--page-building
"""

import os

import pytest


def assert_path_not_in_site_dir(path):
    def wrapper(context):
        assert path not in os.listdir(context['site_dir'])
    return wrapper


TESTS = (
    pytest.param(  # mkdocs-exclude (configuration before mdpo)
        {
            'index.md': 'Hello\n',
            'file-to-be-excluded.md': 'This file should be excluded\n',
        },
        {
            'es/index.md.po': {
                'Hello': 'Hola',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'plugins': [
                {
                    'exclude': {
                        'glob': [
                            'file-to-be-excluded.md',
                        ],
                    },
                },
            ],
        },
        {
            'index.html': [
                (
                    '<p>Hello</p>'
                ),
            ],
            'es/index.html': [
                (
                    '<p>Hola</p>'
                ),
            ],
        },
        assert_path_not_in_site_dir('file-to-be-excluded'),
        -1,
        id='mkdocs-exclude (before mdpo)',
    ),
    pytest.param(  # mkdocs-exclude (configuration after mdpo)
        {
            'index.md': 'Hello\n',
            'file-to-be-excluded.md': 'This file should be excluded\n',
        },
        {
            'es/index.md.po': {
                'Hello': 'Hola',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'plugins': [
                {
                    'exclude': {
                        'glob': [
                            'file-to-be-excluded.md',
                        ],
                    },
                },
            ],
        },
        {
            'index.html': [
                (
                    '<p>Hello</p>'
                ),
            ],
            'es/index.html': [
                (
                    '<p>Hola</p>'
                ),
            ],
        },
        assert_path_not_in_site_dir('file-to-be-excluded'),
        0,
        id='mkdocs-exclude (after mdpo)',
    ),
)


@pytest.mark.parametrize(
    (
        'input_files_contents',
        'translations',
        'plugin_config',
        'additional_config',
        'expected_output_files',
        'callback_after_first_build',
        'insert_plugin_config_at_position',
    ),
    TESTS,
)
def test_navigation_and_page_building_plugins(
    input_files_contents,
    translations,
    plugin_config,
    additional_config,
    expected_output_files,
    callback_after_first_build,
    insert_plugin_config_at_position,
    mkdocs_build,
):
    mkdocs_build(
        input_files_contents,
        translations,
        plugin_config,
        additional_config,
        expected_output_files,
        callback_after_first_build=callback_after_first_build,
        insert_plugin_config_at_position=insert_plugin_config_at_position,
    )
