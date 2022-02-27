## [PyMdown extensions][pymdown-extensions]

<!-- mdpo-disable-next-line -->
### [**`pymdownx.caret`**](https://facelessuser.github.io/pymdown-extensions/extensions/caret)

=== "Output"

    Hello, I'm text with ^^an insert^^.

    Hello, I'm text with^a\ superscript^

=== "Markdown"

    ```markdown
    Hello, I'm text with ^^an insert^^.

    Hello, I'm text with^a\ superscript^
    ```

=== "PO file content"

    ```po
    msgid "Hello, I'm text with ^^an insert^^."
    msgstr "Hola, soy texto con ^^una inserción^^."

    msgid "Hello, I'm text with^a\\ superscript^."
    msgstr "Hola, soy texto con^un\\ superíndice^"
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.details`**](https://facelessuser.github.io/pymdown-extensions/extensions/details)

=== "Output"

    ???+ note "Open styled details"

        ??? danger "Nested details!"

            And more content.

=== "Markdown"

    ```markdown
    ???+ note "Open styled details"

        ??? danger "Nested details!"

            And more content.
    ```

=== "PO file content"

    ```po
    msgid "Open styled details"
    msgstr "Detalles con estilo abierto"

    msgid "Nested details!"
    msgstr "¡Detalles anidados!"

    msgid "And more content."
    msgstr "Y más contenido."
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.emoji`**](https://facelessuser.github.io/pymdown-extensions/extensions/emoji)

=== "Output"

    I :heart: mdpo

=== "Markdown"

    ```markdown
    I :heart: mdpo
    ```

=== "PO file content"

    ```po
    msgid "I :heart: mdpo"
    msgstr "Me encanta mdpo :heart:"
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.highlight`**](https://facelessuser.github.io/pymdown-extensions/extensions/highlight)

Code blocks are not translated by default, but you can include a
[`<!-- mdpo-include-codeblock -->`](https://mdpo.readthedocs.io/en/master/commands.html#code-blocks-extraction)
HTML comment before each code block that you want translate.

!!! tip

    See [Code blocks extraction][mdpo-codeblocks-extraction].

=== "Output"

    ```python
    import mdpo
    print(mdpo.__version__)
    ```

=== "Markdown"

    ````
    \<!-- mdpo-include-codeblock -->
    ```python
    import mdpo
    print(mdpo.__version__)
    ```
    ````

=== "PO file content"

    ```po
    msgid ""
    "import mdpo\\n"
    "print(mdpo.__version__)\\n"
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.inlinehilite`**](https://facelessuser.github.io/pymdown-extensions/extensions/inlinehilite)

There is no way of skip inline codespan blocks from being included in translations:


=== "Output"

    Here is some code: `#!py3 import pymdownx; pymdownx.__version__`.

    The mock shebang will be treated like text here: ` #!js var test = 0;`.

=== "Markdown"

    ```markdown
    Here is some code: `#!py3 import pymdownx; pymdownx.__version__`.

    The mock shebang will be treated like text here: ` #!js var test = 0;`.
    ```

=== "PO file content"

    ```po
    msgid "Here is some code: `#!py3 import pymdownx; pymdownx.__version__`."
    msgstr ""
    "Aquí hay algo de código: `#!py3 import pymdownx; pymdownx.__version__`."

    msgid ""
    "The mock shebang will be treated like text here: ` #!js var test = 0;`."
    msgstr ""
    "El shebang simulado se tratará como texto aquí: ` #!js var test = 0;`."
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.keys`**](https://facelessuser.github.io/pymdown-extensions/extensions/keys)

=== "Output"

    ++ctrl+alt+delete++

=== "Markdown"

    ```markdown
    ++ctrl+alt+delete++
    ```

=== "PO file content"

    ```po
    msgid "++ctrl+alt+delete++"
    msgstr "++ctrl+alt+f10++"
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.magiclink`**](https://facelessuser.github.io/pymdown-extensions/extensions/magiclink)

Sometimes the translation should edit links. See the next example linking to
this documentation depending on the current active language:

=== "Output"

    You can access to the mkdocs-mdpo-plugin documentation here: https://mondeja.github.io/mkdocs-mdpo-plugin

=== "Markdown"

    ```markdown
    You can access to the mkdocs-mdpo-plugin documentation here: https://mondeja.github.io/mkdocs-mdpo-plugin
    ```

=== "PO file content"

    ```po
    msgid ""
    "You can access to the mkdocs-mdpo-plugin documentation here: "
    "https://mondeja.github.io/mkdocs-mdpo-plugin"
    msgstr ""
    "Puedes acceder a la documentación de mkdocs-mdpo-plugin aquí: "
    "https://mondeja.github.io/mkdocs-mdpo-plugin/es"
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.mark`**](https://facelessuser.github.io/pymdown-extensions/extensions/mark)

=== "Output"

    ==mark me==

=== "Markdown"

    ```markdown
    ==mark me==
    ```

=== "PO file content"

    ```po
    msgid "==mark me=="
    msgstr "==marcame=="
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.progressbar`**](https://facelessuser.github.io/pymdown-extensions/extensions/progressbar)

You must let one blank line between each progress bar.

=== "Output"

    [=0% "0%"]

    [=45% "45%"]

    [=100% "100%"]

=== "Markdown"

    ```markdown
    [=0% "0%"]

    [=45% "45%"]

    [=100% "100%"]
    ```

=== "PO file content"

    ```po
    msgid "[=0% \"0%\"]"
    msgstr "[=0% \"vacío\"]"

    msgid "[=45% \"45%\"]"
    msgstr "[=45% \"45 por ciento\"]"

    msgid "[=100% \"100%\"]"
    msgstr "[=100% \"lleno\"]"
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.smartsymbols`**](https://facelessuser.github.io/pymdown-extensions/extensions/smartsymbols)

=== "Output"

    Here are some symbols: (tm) (c) (r)

=== "Markdown"

    ```markdown
    Here are some symbols: (tm) (c) (r)
    ```

=== "PO file content"

    ```po
    msgid "Here are some symbols: (tm) (c) (r)"
    msgstr "Aquí hay algunos símbolos: (tm) (c) (r)"
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.snippets`**](https://facelessuser.github.io/pymdown-extensions/extensions/snippets)

=== "Output"

    --8<-- "docs/src/file-to-be-inserted.txt"

=== "Markdown"

    ```markdown
    \--8<-- "docs/src/file-to-be-inserted.txt"
    ```

=== "PO file content"

    ```po
    msgid "Some inserted content."
    msgstr "Algo de contenido insertado."
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.tabbed`**](https://facelessuser.github.io/pymdown-extensions/extensions/tabbed)

=== "Output"

    === "Tab title"

        Tab content

=== "Markdown"

    ```markdown
    === "Tab title"

        Tab content
    ```

=== "PO file content"

    ```po
    msgid "Tab title"
    msgstr "Título de pestaña"

    msgid "Tab content"
    msgstr "Contenido de pestaña"
    ```

??? warning

    Some content of certain extensions placed inside tabs will not be translated.

<!-- mdpo-disable-next-line -->
### [**`pymdownx.tasklist`**](https://facelessuser.github.io/pymdown-extensions/extensions/tasklist)

=== "Output"

    - [X] Task 1
        * [X] Task A
        * [ ] Task B
            more text
            + [x] Task δ
            + [ ] Task ε
            + [x] Task ζ
        * [X] Task C
    - [ ] Task 2
    - [ ] Task 3

=== "Markdown"

    ```markdown
    - [X] Task 1
        * [X] Task A
        * [ ] Task B
            more text
            + [x] Task δ
            + [ ] Task ε
            + [x] Task ζ
        * [X] Task C
    - [ ] Task 2
    - [ ] Task 3
    ```

=== "PO file content"

    ```po
    msgid "Task 1"
    msgstr ""

    msgid "Task A"
    msgstr ""

    msgid "Task B more text"
    msgstr ""

    msgid "Task δ"
    msgstr ""

    msgid "Task ε"
    msgstr ""

    msgid "Task ζ"
    msgstr ""

    msgid "Task C"
    msgstr ""

    msgid "Task 2"
    msgstr ""

    msgid "Task 3"
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.tilde`**](https://facelessuser.github.io/pymdown-extensions/extensions/tilde)

=== "Output"

    ~~Delete me~~

    CH~3~CH~2~OH

=== "Markdown"

    ```markdown
    ~~Delete me~~

    CH~3~CH~2~OH
    ```

=== "PO file content"

    ```po
    msgid "~~Delete me~~"
    msgstr "~~Elimíname~~"

    msgid "CH~3~CH~2~OH"
    msgstr "H~2~O"
    ```

[pymdown-extensions]: https://facelessuser.github.io/pymdown-extensions/extensions
[mdpo-codeblocks-extraction]: https://mdpo.readthedocs.io/en/master/commands.html#code-blocks-extraction
