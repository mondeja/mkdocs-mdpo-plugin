"""Mkdocs builds tests for mkdocs-mdpo-plugin configuration."""

import pytest


tests = (
    (
        # abbr
        {
            'index.md': (
                'The HTML specification is maintained by the W3C.\n\n'
                '*[HTML]: Hyper Text Markup Language\n\n'
                '*[W3C]: World Wide Web Consortium'
            ),
        },
        {
            'es/index.md.po': {
                'The HTML specification is maintained by the W3C.':
                'La especificación HTML es mantenida por el W3C.',
                '*[HTML]: Hyper Text Markup Language':
                '*[HTML]: Lenguaje de Marcado de Hipertexto',
                '*[W3C]: World Wide Web Consortium':
                '*[W3C]: Consorcio Mundial de Internet',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'abbr',
            ],
        },
        {
            'index.html': [
                (
                    '<p>The <abbr title="Hyper Text Markup Language">HTML'
                    '</abbr> specification is maintained by the'
                    ' <abbr title="World Wide Web Consortium">W3C</abbr>.'
                    '</p>'
                ),
            ],
            'es/index.html': [
                (
                    '<p>La especificación <abbr'
                    ' title="Lenguaje de Marcado de Hipertexto">HTML</abbr>'
                    ' es mantenida por el'
                    ' <abbr title="Consorcio Mundial de Internet">W3C</abbr>.'
                    '</p>'
                ),
            ],
        },
    ),
    (
        # attr_list
        {
            'index.md': (
                '# [link](http://foobar.baz){: title="A title" mdpo }'
            ),
        },
        {
            'es/index.md.po': {
                '[link](http://foobar.baz){: title="A title" mdpo }': (
                    '[enlace](https://foobar.es){:'
                    ' title="Un título" mdpo }'
                ),
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'attr_list',
            ],
        },
        {
            'index.html': [],
            'es/index.html': [],
        },
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
    tests,
)
def test_official_extensions(
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
