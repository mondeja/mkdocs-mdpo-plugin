# Extensions support

The plugin aims to provide basic support (at least) for the most used
extensions. Unfortunately, sometimes you must customize the messages
extraction process using HTML comments to exclude certain syntaxes that depends
on extensions, or change a bit the format of your Markdown files.

??? note

    If an extension is not listed here, just means that is not tested,
    not that doesn't works. If you doubt if using an extension the messages can
    be translated correctly, it is better to try it directly.

    If you
    [submit a pull request](https://github.com/mondeja/mkdocs-mdpo-plugin/pulls)
    adding tests evidencing that a extension works, it would be added here.

## [Officially supported extensions](https://python-markdown.github.io/extensions/#officially-supported-extensions)

<!-- mdpo-disable-next-line -->
### [**`abbr`**](https://python-markdown.github.io/extensions/abbreviations)

You must always let one newline between each reference:

=== "Output"

    The HTML specification is maintained by the W3C.

=== "Markdown"

    ```markdown
    The HTML specification is maintained by the W3C.

    *[HTML]: Hyper Text Markup Language

    *[W3C]:  World Wide Web Consortium
    ```

=== "PO file content"

    ```po
    msgid "The HTML specification is maintained by the W3C."
    msgstr ""

    msgid "*[HTML]: Hyper Text Markup Language"
    msgstr ""

    msgid "*[W3C]: World Wide Web Consortium"
    msgstr ""
    ```

*[HTML]: Hyper Text Markup Language

*[W3C]:  World Wide Web Consortium


<!-- mdpo-disable-next-line -->
### [**`attr_list`**](https://python-markdown.github.io/extensions/attr_list)

Only `title` attributes values are translated. Currently, this extension is a
bit tricky because, if you want to see the `title` attribute value included in
your PO file, you must add an attribute `mdpo`:

=== "Output"

    #### [link](https://mondeja.github.io/mkdocs-mdpo-plugin){: title="With a translated title!" mdpo }

=== "Markdown"

    ```markdown
    #### [link](https://mondeja.github.io/mkdocs-mdpo-plugin){: title="With a translated title!" mdpo }
    ```

=== "PO file content"

    ```po
    msgid ""
    "[link](https://mondeja.github.io/mkdocs-mdpo-plugin){: title=\"With a "
    "translated title!\" mdpo }"
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`def_list`**](https://python-markdown.github.io/extensions/definition_lists)

=== "Output"

    Apple
    :   Pomaceous fruit of plants of the genus Malus in
        the family Rosaceae.

    Orange
    :   The fruit of an evergreen tree of the genus Citrus.

=== "Markdown"

    ```markdown
    Apple
    :   Pomaceous fruit of plants of the genus Malus in
        the family Rosaceae.

    Orange
    :   The fruit of an evergreen tree of the genus Citrus.
    ```

=== "PO file content"

    ```po
    msgid "Apple"
    msgstr "Manzana"

    msgid "Pomaceous fruit of plants of the genus Malus in the family Rosaceae."
    msgstr "Fruto de orujo de plantas del género Malus de la familia Rosaceae."

    msgid "Orange"
    msgstr "Naranja"

    msgid "The fruit of an evergreen tree of the genus Citrus."
    msgstr "El fruto de un árbol de hoja perenne del género Citrus."
    ```

<!-- mdpo-disable-next-line -->
### [**`fenced_code`**](https://python-markdown.github.io/extensions/fenced_code)

Code blocks are not translated by default, but you can include a
[`<!-- mdpo-include-codeblock -->`](https://mdpo.readthedocs.io/en/master/commands.html#extracting-code-blocks)
HTML comment before each code block that you want translate.

=== "Output"

    ```javascript
    var hello = "world";
    ```

=== "Markdown"

    ````markdown
    \<!-- mdpo-include-codeblock -->
    ```javascript
    var hello = "world";
    ```
    ````

=== "PO file content"

    ```po
    msgid "var hello = \"world\"; "
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`footnotes`**](https://python-markdown.github.io/extensions/footnotes)

You must always let one newline between each footnote content:

=== "Output"

    This is a footnote[^1]. This is another[^2].

[^1]: This is a footnote content.

[^2]: This is another footnote content.

=== "Markdown"

    ```
    This is a footnote[^1]. This is another[^2].

    [^1]: This is a footnote content.

    [^2]: This is another footnote content.
    ```

=== "PO file content"

    ```po
    msgid "This is a footnote[^1]. This is another[^2]."
    msgstr ""

    msgid "[^1]: This is a footnote content."
    msgstr ""

    msgid "[^2]: This is another footnote content."
    msgstr ""
    ```


<!-- mdpo-disable-next-line -->
### [**`tables`**](https://python-markdown.github.io/extensions/tables)

=== "Output"

    First header  | Second header
    ------------- | -------------
    Content cell  | Content cell
    Content cell  | Content cell

=== "Markdown"

    ```markdown
    First Header  | Second Header
    ------------- | -------------
    Content Cell  | Content Cell
    Content Cell  | Content Cell
    ```

=== "PO file content"

    ```po
    msgid "First header"
    msgstr ""

    msgid "Second header"
    msgstr ""

    msgid "Content cell"
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`admonition`**](https://python-markdown.github.io/extensions/admonition)

=== "Output"

    !!! note "Admonition title"

        The title will also be included in the PO file.

    !!! note

        Even the implicit title, which in this case would be "Note".

=== "Markdown"

    ```markdown
    !!! note "Admonition title"

        Don't be afraid, the title will also be included in the PO file.

    !!! note

        Even the implicit title, which in this case would be "Note".
    ```

=== "PO file content"

    ```po
    msgid "Admonition title"
    msgstr ""

    msgid "The title will also be included in the PO file."
    msgstr ""

    msgid "Note"
    msgstr ""

    msgid "Even the implicit title, which in this case would be \"Note\"."
    msgstr ""
    ```

## [PyMdown extensions](https://facelessuser.github.io/pymdown-extensions/extensions)

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
    msgstr ""

    msgid "Hello, I'm text with^a\\ superscript^."
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.details`**](https://facelessuser.github.io/pymdown-extensions/extensions/details)

=== "Output"

    ???+ note "Open styled details"

        ??? danger "Nested details!"

            And more content again.

=== "Markdown"

    ```markdown
    ???+ note "Open styled details"

        ??? danger "Nested details!"

            And more content again.
    ```

=== "PO file content"

    ```po
    msgid "Open styled details"
    msgstr ""

    msgid "Nested details!"
    msgstr ""

    msgid "And more content again."
    msgstr ""
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
    msgstr "Me encanta mdpo :+1:"
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.highlight`**](https://facelessuser.github.io/pymdown-extensions/extensions/highlight)

Code blocks are not translated by default, but you can include a
[`<!-- mdpo-include-codeblock -->`](https://mdpo.readthedocs.io/en/master/commands.html#extracting-code-blocks)
HTML comment before each code block that you want translate.

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

    The mock shebang will be treated like text here: ` #!js var test = 0; `.

=== "Markdown"

    ```markdown
    Here is some code: `#!py3 import pymdownx; pymdownx.__version__`.

    The mock shebang will be treated like text here: ` #!js var test = 0; `.
    ```

=== "PO file content"

    ```po
    msgid "Here is some code: `#!py3 import pymdownx; pymdownx.__version__`."
    msgstr ""

    msgid ""
    "The mock shebang will be treated like text here: ` #!js var test = 0; `."
    msgstr ""
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
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.magiclink`**](https://facelessuser.github.io/pymdown-extensions/extensions/magiclink)

Sometimes the translation should edit links. See the next example linking to
this documentation depending on the current language:

=== "Output"

    You can access to the mdocs-mdpo-plugin documentation here: https://mondeja.github.io/mkdocs-mdpo-plugin

=== "Markdown"

    ```markdown
    You can access to the mdocs-mdpo-plugin documentation here: https://mondeja.github.io/mkdocs-mdpo-plugin
    ```

=== "PO file content"

    ```po
    msgid ""
    "You can access to the mdocs-mdpo-plugin documentation here: "
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
    msgstr "[=100% \"cien por cien\"]"
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

    --8<-- "docs/file-to-be-inserted.txt"

=== "Markdown"

    ```markdown
    \--8<-- "docs/file-to-be-inserted.txt"
    ```

=== "PO file content"

    ```po
    msgid "Some inserted content."
    msgstr "Algo de contenido insertado."
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.tabbed`**](https://facelessuser.github.io/pymdown-extensions/extensions/tabbed)

=== "Output"

    === "Output"

        Tab content

=== "Markdown"

    ```markdown
    === "Output"

        Tab content
    ```

=== "PO file content"

    ```po
    msgid "Output"
    msgstr "Salida"

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
    ```
