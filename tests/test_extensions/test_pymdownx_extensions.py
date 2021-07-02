"""Mkdocs builds tests for mkdocs-mdpo-plugin PyMdown extensions support."""

import pytest


TESTS = (
    pytest.param(  # pymdownx.caret
        {
            'index.md': (
                "Hello, I'm text with ^^an insert^^.\n\n"
                "Hello, I'm text with^a\\ superscript^"
            ),
        },
        {
            'es/index.md.po': {
                "Hello, I'm text with ^^an insert^^.":
                'Hola, soy texto con ^^una inserción^^.',
                "Hello, I'm text with^a\\ superscript^":
                'Hola, soy texto con^un\\ superíndice^',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.caret',
            ],
        },
        {
            'es/index.html': [
                '<p>Hola, soy texto con <ins>una inserción</ins>.</p>\n'
                '<p>Hola, soy texto con<sup>un superíndice</sup></p>',
            ],
        },
        id='pymdownx.caret',
    ),
    pytest.param(  # pymdownx.details
        {
            'index.md': (
                '???+ note "Open styled details"\n\n'
                '    ??? danger "Nested details!"\n\n'
                '        And more content.'
            ),
        },
        {
            'es/index.md.po': {
                'Open styled details': 'Detalles con estilo abierto',
                'Nested details!': '¡Detalles anidados!',
                'And more content.': 'Y más contenido.',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.details',
            ],
        },
        {
            'es/index.html': [
                '<details class="note" open="open">'
                '<summary>Detalles con estilo abierto</summary>'
                '<details class="danger">'
                '<summary>¡Detalles anidados!</summary>'
                '<p>Y más contenido.</p>\n'
                '</details>\n'
                '</details>',
            ],
        },
        id='pymdownx.details',
    ),
    pytest.param(  # pymdownx.emoji
        {
            'index.md': 'I :heart: mdpo\n',
        },
        {
            'es/index.md.po': {
                'I :heart: mdpo': 'Me encanta mdpo :heart:',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.emoji',
            ],
        },
        {
            'es/index.html': [
                '<p>Me encanta mdpo <img alt="❤️" class="emojione" src="',
                '" title=":heart:" /></p>',
            ],
        },
        id='pymdownx.emoji',
    ),
    pytest.param(  # pymdownx.highlight
        {
            'index.md': (
                '<!-- mdpo-include-codeblock -->\n'
                '```python\n'
                'import mdpo\n'
                'print(mdpo.__version__)\n'
                '```'
            ),
        },
        {
            'es/index.md.po': {
                'import mdpo\nprint(mdpo.__version__)\n':
                'import mkdocs\nprint(mkdocs.__version__)\n',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.highlight',
            ],
        },
        {
            'index.html': [
                '<pre><code class="language-python">import mdpo\n'
                'print(mdpo.__version__)\n'
                '</code></pre>',
            ],
            'es/index.html': [
                '<pre><code class="language-python">import mkdocs\n'
                'print(mkdocs.__version__)\n'
                '</code></pre>',
            ],
        },
        id='pymdownx.highlight',
    ),
    pytest.param(  # pymdownx.inlinehilite
        {
            'index.md': (
                'Here is some code:'
                ' `#!py3 import pymdownx; pymdownx.__version__`.\n\n'
                'The mock shebang will be treated like text here:'
                ' ` #!js var test = 0;`.'
            ),
        },
        {
            'es/index.md.po': {
                'Here is some code:'
                ' `#!py3 import pymdownx; pymdownx.__version__`.':
                'Aquí hay algo de código:'
                ' `#!py3 import pymdownx; pymdownx.__version__`.',
                'The mock shebang will be treated like text here:'
                ' ` #!js var test = 0;`.':
                'El shebang simulado se tratará como texto aquí:'
                ' ` #!js var test = 0;`.',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.inlinehilite',
            ],
        },
        {
            'es/index.html': [
                '<p>Aquí hay algo de código:'
                ' <code class="highlight"><span class="kn">import</span>'
                ' <span class="nn">pymdownx</span><span class="p">;</span>'
                ' <span class="n">pymdownx</span><span class="o">.</span>'
                '<span class="n">__version__</span></code>.</p>\n'
                '<p>El shebang simulado se tratará como texto aquí:'
                ' <code>#!js var test = 0;</code>.</p>',
            ],
        },
        id='pymdownx.inlinehilite',
    ),
    pytest.param(  # pymdownx.keys
        {
            'index.md': '++ctrl+alt+delete++\n',
        },
        {
            'es/index.md.po': {
                '++ctrl+alt+delete++': '++ctrl+alt+f10++',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.keys',
            ],
        },
        {
            'es/index.html': [
                '<p><span class="keys"><kbd class="key-control">Ctrl</kbd>'
                '<span>+</span><kbd class="key-alt">Alt</kbd><span>+</span>'
                '<kbd class="key-f10">F10</kbd></span></p>',
            ],
        },
        id='pymdownx.keys',
    ),
    pytest.param(  # pymdownx.magiclink
        {
            'index.md': (
                'You can access to the mkdocs-mdpo-plugin documentation here:'
                ' https://mondeja.github.io/mkdocs-mdpo-plugin\n'
            ),
        },
        {
            'es/index.md.po': {
                'You can access to the mkdocs-mdpo-plugin documentation here:'
                ' https://mondeja.github.io/mkdocs-mdpo-plugin':
                'Puedes acceder a la documentación de mkdocs-mdpo-plugin aquí:'
                ' https://mondeja.github.io/mkdocs-mdpo-plugin/es',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.magiclink',
            ],
        },
        {
            'es/index.html': [
                '<p>Puedes acceder a la documentación de mkdocs-mdpo-plugin'
                ' aquí:'
                ' <a href="https://mondeja.github.io/mkdocs-mdpo-plugin/es">'
                'https://mondeja.github.io/mkdocs-mdpo-plugin/es</a>'
                '</p>',
            ],
        },
        id='pymdownx.magiclink',
    ),
    pytest.param(  # pymdownx.mark
        {
            'index.md': '==mark me==\n',
        },
        {
            'es/index.md.po': {
                '==mark me==': '==marcame==',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.mark',
            ],
        },
        {
            'es/index.html': [
                '<p><mark>marcame</mark></p>',
            ],
        },
        id='pymdownx.mark',
    ),
    pytest.param(  # pymdownx.progressbar
        {
            'index.md': '[=0% "0%"]\n\n[=45% "45%"]\n\n[=100% "100%"]\n',
        },
        {
            'es/index.md.po': {
                '[=0% "0%"]': '[=0% "vacío"]',
                '[=45% "45%"]': '[=45% "45 por ciento"]',
                '[=100% "100%"]': '[=100% "lleno"]',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.progressbar',
            ],
        },
        {
            'es/index.html': [
                '<p>\n'
                '<div class="progress progress-0plus">\n'
                '<div class="progress-bar" style="width:0.00%">\n'
                '<p class="progress-label">vacío</p>\n'
                '</div>\n'
                '</div>\n'
                '</p>\n'
                '<p>\n'
                '<div class="progress progress-40plus">\n'
                '<div class="progress-bar" style="width:45.00%">\n'
                '<p class="progress-label">45 por ciento</p>\n'
                '</div>\n'
                '</div>\n'
                '</p>\n'
                '<p>\n'
                '<div class="progress progress-100plus">\n'
                '<div class="progress-bar" style="width:100.00%">\n'
                '<p class="progress-label">lleno</p>\n'
                '</div>\n'
                '</div>\n'
                '</p>',
            ],
        },
        id='pymdownx.progressbar',
    ),
    pytest.param(  # pymdownx.smartsymbols
        {
            'index.md': 'Here are some symbols: (tm) (c) (r)\n',
        },
        {
            'es/index.md.po': {
                'Here are some symbols: (tm) (c) (r)':
                'Aquí hay algunos símbolos: (tm) (c) (r)',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.smartsymbols',
            ],
        },
        {
            'es/index.html': [
                '<p>Aquí hay algunos símbolos: &trade; &copy; &reg;</p>',
            ],
        },
        id='pymdownx.smartsymbols',
    ),
    pytest.param(  # pymdownx.snippets
        {
            'index.md': '--8<-- "docs/file-to-be-inserted.txt"\n',
        },
        {
            'es/index.md.po': {
                'Some inserted content from another file.':
                'Algo de contenido insertado desde otro archivo.',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.snippets',
            ],
        },
        {
            'es/index.html': [
                '<p>Algo de contenido insertado desde otro archivo.</p>',
            ],
        },
        id='pymdownx.snippets',
    ),
    pytest.param(  # pymdownx.tabbed
        {
            'index.md': '=== "Output"\n\n    Tab content\n',
        },
        {
            'es/index.md.po': {
                'Output': 'Salida',
                'Tab content': 'Contenido de pestaña',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.tabbed',
            ],
        },
        {
            'es/index.html': [
                '<div class="tabbed-set" data-tabs="1:1">'
                '<input checked="checked" id="__tabbed_1_1" name="__tabbed_1"'
                ' type="radio" /><label for="__tabbed_1_1">Salida</label>'
                '<div class="tabbed-content">\n'
                '<p>Contenido de pestaña</p>\n'
                '</div>\n'
                '</div>',
            ],
        },
        id='pymdownx.tabbed',
    ),
    pytest.param(  # pymdownx.tasklist
        {
            'index.md': (
                'Some text before tasks list.\n\n'
                '- [X] Task 1\n'
                '    * [X] Task A\n'
                '    * [ ] Task B\n'
                '        more text\n'
                '        + [x] Task δ\n'
                '        + [ ] Task ε\n'
                '        + [x] Task ζ\n'
                '    * [X] Task C\n'
                '- [ ] Task 2\n'
                '- [ ] Task 3\n'
            ),
        },
        {
            'es/index.md.po': {
                'Some text before tasks list.':
                'Algo de texto antes de lista de tareas.',
                'Task 1': 'Tarea 1',
                'Task A': 'Tarea A',
                'Task B more text': 'Tarea B más texto',
                'Task δ': 'Tarea δ',
                'Task ε': 'Tarea ε',
                'Task ζ': 'Tarea ζ',
                'Task C': 'Tarea C',
                'Task 2': 'Tarea 2',
                'Task 3': 'Tarea 3',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.tasklist',
            ],
        },
        {
            'es/index.html': [
                '<p>Algo de texto antes de lista de tareas.</p>\n'
                '<ul class="task-list">\n'
                '<li class="task-list-item"><input type="checkbox"'
                ' disabled checked/> Tarea 1</li>\n'
                '<li class="task-list-item"><input type="checkbox"'
                ' disabled checked/> Tarea A</li>\n'
                '<li class="task-list-item"><input type="checkbox"'
                ' disabled/> Tarea B más texto'
                '<ul class="task-list">\n'
                '<li class="task-list-item"><input type="checkbox"'
                ' disabled checked/> Tarea δ</li>\n'
                '<li class="task-list-item"><input type="checkbox"'
                ' disabled/> Tarea ε</li>\n'
                '<li class="task-list-item"><input type="checkbox"'
                ' disabled checked/> Tarea ζ</li>\n'
                '</ul>\n'
                '</li>\n'
                '<li class="task-list-item"><input type="checkbox"'
                ' disabled checked/> Tarea C</li>\n'
                '<li class="task-list-item"><input type="checkbox"'
                ' disabled/> Tarea 2</li>\n'
                '<li class="task-list-item"><input type="checkbox"'
                ' disabled/> Tarea 3</li>\n'
                '</ul>',
            ],
        },
        id='pymdownx.tasklist',
    ),
    pytest.param(  # pymdownx.tilde
        {
            'index.md': '~~Delete me~~\n\nCH~3~CH~2~OH\n',
        },
        {
            'es/index.md.po': {
                '~~Delete me~~': '~~Elimíname~~',
                'CH~3~CH~2~OH': 'H~2~O',
            },
        },
        {
            'languages': ['en', 'es'],
        },
        {
            'markdown_extensions': [
                'pymdownx.tilde',
            ],
        },
        {
            'es/index.html': [
                '<p><del>Elimíname</del></p>\n'
                '<p>H<sub>2</sub>O</p>',
            ],
        },
        id='pymdownx.tilde',
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
def test_pymdownx_extensions(
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
