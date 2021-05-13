## [Officially supported extensions][officially-supported-extensions]

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
    "[link](https://mondeja.github.io/mkdocs-mdpo-plugin/es){: title=\"¡Con un "
    "título traducido!\" mdpo }"
    ```

<!-- mdpo-disable-next-line -->
### [**`def_list`**](https://python-markdown.github.io/extensions/definition_lists)

You must let a blank line between the term and its definition:

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
    msgstr "Esto es una nota al pie[^1]. Esto es otra[^2]."

    msgid "[^1]: This is a footnote content."
    msgstr "[^1]: Este es un contenido de nota al pie."

    msgid "[^2]: This is another footnote content."
    msgstr "[^2]: Este es otro contenido de nota al pie."
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
    msgstr "Primer encabezado"

    msgid "Second header"
    msgstr "Segundo encabezado"

    msgid "Content cell"
    msgstr "Contenido de celda"
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
    msgstr "Título de advertencia"

    msgid "The title will also be included in the PO file."
    msgstr "El título también será añadido en el archivo PO."

    msgid "Note"
    msgstr "Nota"

    msgid "Even the implicit title, which in this case would be \"Note\"."
    msgstr "Incluso el título implícito, el cual en este caso sería \"Nota\"."
    ```

[officially-supported-extensions]: https://python-markdown.github.io/extensions/#officially-supported-extensions
