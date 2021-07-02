"""Extensions compatibility tests.

Here is tested behaviour depending on multiple extensions at the same time.
"""

import pytest


TESTS = (
    pytest.param(
        {
            'index.md': (
                'I :heart: MARKDOWN.\n\n*[MARKDOWN]: Lightweight markup'
                ' language for creating formatted text.\n\n'
            ),
        },
        {
            'es/index.md.po': {
                'I :heart: MARKDOWN.': 'Me encanta MARKDOWN :heart:',
                (
                    '*[MARKDOWN]: Lightweight markup language for creating'
                    ' formatted text.'
                ): (
                 '*[MARKDOWN]: Lenguaje de marcado ligero para crear texto'
                 ' con formato.'
                ),
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'abbr',
                'pymdownx.emoji',
            ],
        },
        {
            'es/index.html': [
                '<p>Me encanta'
                ' <abbr title="Lenguaje de marcado ligero para crear texto'
                ' con formato.">MARKDOWN</abbr>'
                ' <img alt="❤️" class="emojione" src="',
                ' title=":heart:" /></p>',
            ],
        },
        id='abbr+pymdownx.emoji',
    ),
    pytest.param(
        {
            'index.md': (
                '# [qux :heart:](http://foobar.baz){: title="A title" mdpo }'
            ),
        },
        {
            'es/index.md.po': {
                '[qux :heart:](http://foobar.baz){: title="A title" mdpo }':
                '[enlace :heart:](https://foobar.es){:'
                ' title="Un título" mdpo }',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'abbr',
                'attr_list',
                'pymdownx.emoji',
            ],
        },
        {
            'es/index.html': [
                '<h1 id="enlace">'
                '<a href="https://foobar.es" mdpo="mdpo" title="Un título">'
                'enlace <img alt="❤️" class="emojione" src="',
                ' title=":heart:" /></a></h1>',
            ],
        },
        id='abbr+attr_list+pymdownx.emoji',
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
def test_extensions_compat(
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
