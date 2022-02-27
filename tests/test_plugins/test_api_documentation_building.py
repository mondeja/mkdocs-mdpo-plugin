"""Mkdocs builds tests for mkdocs-mdpo-plugin API documentation building
plugins support:
https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins#api-documentation-building
"""

import pytest


TESTS = (
    pytest.param(  # mkdocstrings (configuration before mdpo)
        {
            'index.md': (
                'Hello\n\n::: mkdocs_mdpo_plugin.docs_helper.'
                'function\n\nBye'
            ),
        },
        {
            'es/index.md.po': {
                'Hello': 'Hola',
                'Bye': 'Adiós',
                'Function documentation.': 'Documentación de función.',
                'Value to check.':  'Valor a comprobar.',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'plugins': [
                {
                    'mkdocstrings': {},
                },
            ],
        },
        {
            'index.html': [
                '<p>Hello</p>',
                '<p>Function documentation.</p>',
                '<td><p>Value to check.</p></td>',
            ],
            'es/index.html': [
                '<p>Hola</p>',
                '<p>Documentación de función.</p>',
                '<td><p>Valor a comprobar.</p></td>',
            ],
        },
        id='mkdocs-exclude (before mdpo)',
    ),
)


@pytest.mark.parametrize(
    (
        'input_files_contents',
        'translations',
        'plugin_config',
        'additional_config',
        'expected_output_files',
    ),
    TESTS,
)
def test_navigation_and_page_building_plugins(
    input_files_contents,
    translations,
    plugin_config,
    additional_config,
    expected_output_files,
    mkdocs_build,
):
    mkdocs_build(
        input_files_contents,
        translations,
        plugin_config,
        additional_config,
        expected_output_files,
    )
