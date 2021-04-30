# Extensions support

The plugin aims to provide basic support (at least) for the most used
extensions. Unfortunately, sometimes you must customize the messages
extraction process using HTML comments to exclude certain syntaxes that depends
on extensions, or change a bit the format of your Markdown files.

## [Officially supported extensions](https://python-markdown.github.io/extensions/#officially-supported-extensions)

<!-- mdpo-disable-next-line -->
### [**`abbr`**](https://python-markdown.github.io/extensions/abbreviations)

You must always let one newline between each reference:

<!-- mdpo-disable-next-line -->
=== "Output"

    The HTML specification
    is maintained by the W3C.

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    The HTML specification
    is maintained by the W3C.

    *[HTML]: Hyper Text Markup Language

    *[W3C]:  World Wide Web Consortium
    ```

<!-- mdpo-disable-next-line -->
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
bit tricky because, if you want to use the `title` attribute, you must add
an attribute `mdpo-no-title`:

<!-- mdpo-disable-next-line -->
=== "Output"

    #### [link](https://mondeja.github.io/mkdocs-mdpo-plugin){: title="With a translated title!" mdpo-no-title }

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    #### [link](https://mondeja.github.io/mkdocs-mdpo-plugin){: title="With a translated title!" mdpo-no-title }
    ```

<!-- mdpo-disable-next-line -->
=== "PO file content"

    ```po
    msgid ""
    "[link](https://mondeja.github.io/mkdocs-mdpo-plugin){: title=\"With a "
    "translated title!\" mdpo-no-title }"
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`def_list`**](https://python-markdown.github.io/extensions/def_list)

<!-- mdpo-disable-next-line -->
=== "Output"

    Apple
    :   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

    Orange
    :   The fruit of an evergreen tree of the genus Citrus.

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    Apple
    :   Pomaceous fruit of plants of the genus Malus in
        the family Rosaceae.

    Orange
    :   The fruit of an evergreen tree of the genus Citrus.
    ```

<!-- mdpo-disable-next-line -->
=== "PO file content"

    ```po
    msgid "Apple"
    msgstr ""

    msgid "Pomaceous fruit of plants of the genus Malus in the family Rosaceae."
    msgstr ""

    msgid "Orange"
    msgstr ""

    msgid "The fruit of an evergreen tree of the genus Citrus."
    msgstr ""
    ```


<!-- mdpo-disable-next-line -->
### [**`fenced_code`**](https://python-markdown.github.io/extensions/fenced_code)

Code blocks are not translated by default, but you can include a
[`<!-- mdpo-include-codeblock -->`](https://mdpo.readthedocs.io/en/master/commands.html#extracting-code-blocks)
HTML comment before each code block that you want translate.

<!-- mdpo-disable-next-line -->
=== "Output"

    ```javascript
    var hello = "world";
    ```

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ````markdown
    \<!-- mdpo-include-codeblock -->
    ```javascript
    var hello = "world";
    ```
    ````

<!-- mdpo-disable-next-line -->
=== "PO file content"

    ```po
    msgid "var hello = \"world\"; "
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`footnotes`**](https://python-markdown.github.io/extensions/footnotes)

You must always let one newline between each footnote content:

<!-- mdpo-disable-next-line -->
=== "Output"

    This is a footnote[^1]. This is another[^2].

[^1]: This is a footnote content.

[^2]: This is another footnote content.

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```
    This is a footnote[^1]. This is another[^2].

    [^1]: This is a footnote content.

    [^2]: This is another footnote content.
    ```

<!-- mdpo-disable-next-line -->
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

<!-- mdpo-disable-next-line -->
=== "Output"

    First header  | Second header
    ------------- | -------------
    Content cell  | Content cell
    Content cell  | Content cell

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    First Header  | Second Header
    ------------- | -------------
    Content Cell  | Content Cell
    Content Cell  | Content Cell
    ```

<!-- mdpo-disable-next-line -->
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

You must always include a
[`<!-- mdpo-disable-next-line -->`](https://mdpo.readthedocs.io/en/master/commands.html#disabling-extraction)
HTML comment before the admonition. 


<!-- mdpo-disable-next-line -->
=== "Output"

    !!! note "Admonition title"

        The title will also be included in the PO file.

    !!! note

        Even the implicit title, which in this case would be "Note".

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    \<!-- mdpo-disable-next-line -->
    !!! note "Admonition title"

        Don't be afraid, the title will also be included in the PO file.

    <!-- mdpo-disable-next-line -->
    !!! note

        Even the implicit title, which in this case would be "Note". 
    ```

<!-- mdpo-disable-next-line -->
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

<!-- mdpo-disable-next-line -->
=== "Output"

    Hello I'm text with ^^an insert^^.
    
    Hello I'm text with^a\ superscript^

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    Hello I'm text with ^^an insert^^.
    
    Hello I'm text with^a\ superscript^
    ```

<!-- mdpo-disable-next-line -->
=== "PO file content"

    ```po
    msgid "Hello I'm text with ^^an insert^^."
    msgstr ""

    msgid "Hello I'm text with^a\\ superscript^."
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.details`**](https://facelessuser.github.io/pymdown-extensions/extensions/details)

If after adding a details admonition a msgid starting with `???` is added to
your PO file, you can remove it adding a
[`<!-- mdpo-disable-next-line -->`](https://mdpo.readthedocs.io/en/master/commands.html#disabling-extraction)
HTML comment before the admonition.

<!-- mdpo-disable-next-line -->
=== "Output"

    ???+ note "Open styled details"

        ??? danger "Nested details!"
        
            And more content again.

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    \<!-- mdpo-disable-next-line -->
    ???+ note "Open styled details"

        ??? danger "Nested details!"
        
            And more content again.
    ```

<!-- mdpo-disable-next-line -->
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

Maybe your emoji expression can't be translated using the same emoji? Use another
directly from your PO file:

<!-- mdpo-disable-next-line -->
=== "Output"

    I :heart: mdpo

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    I :heart: mdpo
    ```

<!-- mdpo-disable-next-line -->
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

<!-- mdpo-disable-next-line -->
=== "Output"

    ```python
    import mdpo
    print(mdpo.__version__)
    ```

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ````
    \<!-- mdpo-include-codeblock -->
    ```python
    import mdpo
    print(mdpo.__version__)
    ```
    ````

<!-- mdpo-disable-next-line -->
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


<!-- mdpo-disable-next-line -->
=== "Output"

    Here is some code: `#!py3 import pymdownx; pymdownx.__version__`.

    The mock shebang will be treated like text here: ` #!js var test = 0; `.

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    Here is some code: `#!py3 import pymdownx; pymdownx.__version__`.

    The mock shebang will be treated like text here: ` #!js var test = 0; `.
    ```

<!-- mdpo-disable-next-line -->
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

<!-- mdpo-disable-next-line -->
=== "Output"

    ++ctrl+alt+delete++

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    ++ctrl+alt+delete++
    ```

<!-- mdpo-disable-next-line -->
=== "PO file content"

    ```po
    msgid "++ctrl+alt+delete++"
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.magiclink`**](https://facelessuser.github.io/pymdown-extensions/extensions/magiclink)

Sometimes the translation should edit links. See the next example linking to
this documentation depending on the current language:

<!-- mdpo-disable-next-line -->
=== "Output"

    You can access to the mdocs-mdpo-plugin documentation here: https://mondeja.github.io/mkdocs-mdpo-plugin

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    You can access to the mdocs-mdpo-plugin documentation here: https://mondeja.github.io/mkdocs-mdpo-plugin
    ```

<!-- mdpo-disable-next-line -->
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

<!-- mdpo-disable-next-line -->
=== "Output"

    ==mark me==

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    ==mark me==
    ```

<!-- mdpo-disable-next-line -->
=== "PO file content"

    ```po
    msgid "==mark me=="
    msgstr "==marcame=="
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.progressbar`**](https://facelessuser.github.io/pymdown-extensions/extensions/progressbar)

You must let one blank line between each progress bar.

<!-- mdpo-disable-next-line -->
=== "Output"

    [=0% "0%"]

    [=45% "45%"]

    [=100% "100%"]

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    [=0% "0%"]

    [=45% "45%"]

    [=100% "100%"]
    ```

<!-- mdpo-disable-next-line -->
=== "PO file content"

    ```po
    msgid "[=0% \"0%\"]"
    msgstr ""

    msgid "[=45% \"45%\"]"
    msgstr ""

    msgid "[=100% \"100%\"]"
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.smartsymbols`**](https://facelessuser.github.io/pymdown-extensions/extensions/smartsymbols)

<!-- mdpo-disable-next-line -->
=== "Output"

    Here are some symbols: (tm) (c) (r)

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    Here are some symbols: (tm) (c) (r)
    ```

<!-- mdpo-disable-next-line -->
=== "PO file content"

    ```po
    msgid "Here are some symbols: (tm) (c) (r)"
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.snippets`**](https://facelessuser.github.io/pymdown-extensions/extensions/snippets)

Block notation is not supported. You must add an
[`<!-- mdpo-disable-next-line -->`](https://mdpo.readthedocs.io/en/master/commands.html#disabling-extraction)
HTML comment before the line.

<!-- mdpo-disable-next-line -->
=== "Output"

    <!-- mdpo-disable-next-line -->
    --8<-- "docs/file-to-be-inserted.txt"

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    \<!-- mdpo-disable-next-line -->
    \--8<-- "docs/file-to-be-inserted.txt"
    ```

<!-- mdpo-disable-next-line -->
=== "PO file content"

    ```po
    msgid "Some inserted content."
    msgstr "Algo de contenido insertado."
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.tabbed`**](https://facelessuser.github.io/pymdown-extensions/extensions/tabbed)

You must add an
[`<!-- mdpo-disable-next-line -->`](https://mdpo.readthedocs.io/en/master/commands.html#disabling-extraction)
HTML comment before each tab.


<!-- mdpo-disable-next-line -->
=== "Output"

    <!-- mdpo-disable-next-line -->
    === "Output"
    
        Tab content

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    \<!-- mdpo-disable-next-line -->
    === "Output"
    
        Tab content
    ```

<!-- mdpo-disable-next-line -->
=== "PO file content"

    ```po
    msgid "Output"
    msgstr "Salida"
    
    msgid "Tab content"
    msgstr "Contenido de pestaña"
    ```

<!-- mdpo-disable-next-line -->
### [**`pymdownx.tasklist`**](https://facelessuser.github.io/pymdown-extensions/extensions/tasklist)

Text can't be added between tasklist items.

<!-- mdpo-disable-next-line -->
=== "Output"

    - [X] Task 1
        * [X] Task A
        * [ ] Task B    
            + [x] Task D
            + [ ] Task E
            + [x] Task F
        * [X] Task C
    - [ ] Task 2
    - [ ] Task 3

<!-- mdpo-disable-next-line -->
=== "Markdown"

    ```markdown
    - [X] Task 1
        * [X] Task A
        * [ ] Task B    
            + [x] Task D
            + [ ] Task E
            + [x] Task F
        * [X] Task C
    - [ ] Task 2
    - [ ] Task 3
    ```

<!-- mdpo-disable-next-line -->
=== "PO file content"

    ```po
    - [X] Task 1
        * [X] Task A
        * [ ] Task B    
            + [x] Task D
            + [ ] Task E
            + [x] Task F
        * [X] Task C
    - [ ] Task 2
    - [ ] Task 3
    ```
