"""Mkdocs builds tests for mkdocs-mdpo-plugin official extensions support."""

import pytest


TESTS = (
    pytest.param(  # abbr
        {
            'index.md': (
                'Some text [with a link](https://tonowhere.foo).\n\n'
                'The HTML specification is maintained by the W3C.\n\n'
                '*[HTML]: Hyper Text Markup Language\n\n'
                '*[W3C]: World Wide Web Consortium'
            ),
        },
        {
            'es/index.md.po': {
                'Some text [with a link](https://tonowhere.foo).':
                'Algo de texto [con un enlace](https://tonowhere.foo).',
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
                '<p>The <abbr title="Hyper Text Markup Language">HTML'
                '</abbr> specification is maintained by the'
                ' <abbr title="World Wide Web Consortium">W3C</abbr>.'
                '</p>',
            ],
            'es/index.html': [
                '<p>Algo de texto'
                ' <a href="https://tonowhere.foo">con un enlace</a>.</p>',
                '<p>La especificación <abbr'
                ' title="Lenguaje de Marcado de Hipertexto">HTML</abbr>'
                ' es mantenida por el'
                ' <abbr title="Consorcio Mundial de Internet">W3C</abbr>.'
                '</p>',
            ],
        },
        id='abbr',
    ),
    pytest.param(  # attr_list
        {
            'index.md': (
                '# [qux](http://foobar.baz){: title="A title" mdpo }'
            ),
        },
        {
            'es/index.md.po': {
                '[qux](http://foobar.baz){: title="A title" mdpo }':
                '[enlace](https://foobar.es){:'
                ' title="Un título" mdpo }',
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
            'index.html': [
                '<h1 id="qux"><a href="http://foobar.baz" mdpo="mdpo"'
                ' title="A title">qux</a></h1>',
            ],
            'es/index.html': [
                '<h1 id="enlace"><a href="https://foobar.es" mdpo="mdpo"'
                ' title="Un título">enlace</a></h1>',
            ],
        },
        id='attr_list',
    ),
    pytest.param(  # def_list
        {
            'index.md': (
                'Apple\n\n'
                ':   Pomaceous fruit of plants of the genus Malus in\n'
                '    the family Rosaceae.\n\n'
                'Orange\n\n'
                ':   The fruit of an evergreen tree of the genus Citrus.\n'
            ),
        },
        {
            'es/index.md.po': {
                'Apple': 'Manzana',
                'Pomaceous fruit of plants of the genus Malus in the family'
                ' Rosaceae.':
                'Fruto de orujo de plantas del género Malus de la familia'
                ' Rosaceae.',
                'Orange': 'Naranja',
                'The fruit of an evergreen tree of the genus Citrus.':
                'El fruto de un árbol de hoja perenne del género Citrus.',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'def_list',
            ],
        },
        {
            'index.html': [
                '<dt>Apple</dt>',
                (
                    '<dd>\n<p>Pomaceous fruit of plants of the genus Malus'
                    ' in\nthe family Rosaceae.</p>\n</dd>'
                ),
                '<dt>Orange</dt>',
                (
                    '<dd>\n<p>The fruit of an evergreen tree of the genus'
                    ' Citrus.</p>\n</dd>'
                ),
            ],
            'es/index.html': [
                '<dt>Manzana</dt>',
                (
                    '<dd>\n<p>Fruto de orujo de plantas del género Malus de la'
                    ' familia Rosaceae.</p>\n</dd>'
                ),
                '<dt>Naranja</dt>',
                (
                    '<dd>\n<p>El fruto de un árbol de hoja perenne del género'
                    ' Citrus.</p>\n</dd>'
                ),
            ],
        },
        id='def_list',
    ),
    pytest.param(  # fenced_code
        {
            'index.md': (
                '```javascript\n'
                'var hello = "world";\n'
                '```\n\n'
                '<!-- mdpo-include-codeblock -->\n'
                '```python\n'
                'hello = "world"\n'
                '```\n'
            ),
        },
        {
            'es/index.md.po': {
                'hello = "world"\n': 'hola = "mundo"\n',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'fenced_code',
            ],
        },
        {
            'index.html': [
                '<pre><code class="language-javascript">var hello ='
                ' &quot;world&quot;;\n</code></pre>',
                '<pre><code class="language-python">hello = &quot;world&quot;'
                '\n</code></pre>',
            ],
            'es/index.html': [
                '<pre><code class="language-javascript">var hello ='
                ' &quot;world&quot;;\n</code></pre>',
                '<pre><code class="language-python">hola = &quot;mundo&quot;\n'
                '</code></pre>',
            ],
        },
        id='fenced_code',
    ),
    pytest.param(  # footnotes
        {
            'index.md': (
                'This is a footnote[^1]. This is another[^2].\n\n'
                '[^1]: This is a footnote content.\n\n'
                '[^2]: This is another footnote content.\n'
            ),
        },
        {
            'es/index.md.po': {
                'This is a footnote[^1]. This is another[^2].':
                'Esto es una nota al pie[^1]. Esto es otra[^2].',
                '[^1]: This is a footnote content.':
                '[^1]: Esto es el contenido de una nota al pie',
                '[^2]: This is another footnote content.':
                '[^2]: Este es el contenido de otra nota al pie.',
                'Jump back to footnote 1 in the text':
                'Volver a la nota al pie 1 en el texto',
                'Jump back to footnote 2 in the text':
                'Volver a la nota al pie 2 en el texto',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'footnotes',
            ],
        },
        {
            'es/index.html': [
                '<p>Esto es una nota al pie<sup id="fnref:1">'
                '<a class="footnote-ref" href="#fn:1">1</a></sup>.'
                ' Esto es otra<sup id="fnref:2">'
                '<a class="footnote-ref" href="#fn:2">2</a></sup>.</p>',
                '<ol>\n'
                '<li id="fn:1">\n'
                '<p>Esto es el contenido de una nota al pie&#160;'
                '<a class="footnote-backref"'
                ' href="#fnref:1"'
                ' title="Volver a la nota al pie 1 en el texto">&#8617;</a>'
                '</p>\n'
                '</li>\n'
                '<li id="fn:2">\n'
                '<p>Este es el contenido de otra nota al pie.&#160;'
                '<a class="footnote-backref" href="#fnref:2"'
                ' title="Volver a la nota al pie 2 en el texto">&#8617;</a>'
                '</p>\n'
                '</li>\n'
                '</ol>\n',
            ],
        },
        id='footnotes',
    ),
    pytest.param(  # tables
        {
            'index.md': (
                'First header  | Second header\n'
                '------------- | -------------\n'
                'Content cell  | Content cell\n'
                'Content cell  | Content cell\n'
            ),
        },
        {
            'es/index.md.po': {
                'First header': 'Primer encabezado',
                'Second header': 'Segundo encabezado',
                'Content cell': 'Contenido de celda',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'tables',
            ],
        },
        {
            'es/index.html': [
                '<table>\n'
                '<thead>\n'
                '<tr>\n'
                '<th>Primer encabezado</th>\n'
                '<th>Segundo encabezado</th>\n'
                '</tr>\n'
                '</thead>\n'
                '<tbody>\n'
                '<tr>\n'
                '<td>Contenido de celda</td>\n'
                '<td>Contenido de celda</td>\n'
                '</tr>\n'
                '<tr>\n'
                '<td>Contenido de celda</td>\n'
                '<td>Contenido de celda</td>\n'
                '</tr>\n'
                '</tbody>\n'
                '</table>',
            ],
        },
        id='tables',
    ),
    pytest.param(  # admonition
        {
            'index.md': (
                '!!! note "Admonition title"\n\n'
                'The title will also be included in the PO file.\n'
            ),
        },
        {
            'es/index.md.po': {
                'Admonition title': 'Título de advertencia',
                'The title will also be included in the PO file.':
                'El título también será incluido en el archivo PO.',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'admonition',
            ],
        },
        {
            'es/index.html': [
                '<div class="admonition note">\n'
                '<p class="admonition-title">Título de advertencia</p>\n'
                '</div>\n'
                '<p>El título también será incluido en el archivo PO.</p>'
                '</div>',
            ],
        },
        id='admonition',
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
