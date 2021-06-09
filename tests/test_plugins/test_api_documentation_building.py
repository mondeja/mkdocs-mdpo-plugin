"""Mkdocs builds tests for mkdocs-mdpo-plugin API documentation building
plugins support:
https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins#api-documentation-building
"""

import pytest


TESTS = (
    pytest.param(  # mkdocstrings (configuration before mdpo)
        {
            'index.md': (
                'Hello\n\n::: mkdocs_mdpo_plugin.io.'
                'remove_empty_directories_from_dirtree\n\nBye'
            ),
        },
        {
            'es/index.md.po': {
                'Hello': 'Hola',
                'Bye': 'Adios',
                (
                    'Remove empty directories walking through all nested'
                    ' subdirectories.'
                ): (
                 'Elimina directorios vacíos caminando'
                 ' por todos los subdirectorios anidados.'
                ),
                'Top directory tree path.': (
                    'Path al directorio superior en el árbol.'
                ),
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
                (
                    '<p>Remove empty directories walking through all nested'
                    ' subdirectories.</p>'
                ),
                '<td><p>Top directory tree path.</p></td>',
            ],
            'es/index.html': [
                '<p>Hola</p>',
                (
                    '<p>Elimina directorios vacíos caminando por todos'
                    ' los subdirectorios anidados.</p>'
                ),
                '<td><p>Path al directorio superior en el árbol.</p></td>',
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
