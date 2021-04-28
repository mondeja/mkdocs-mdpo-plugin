# Extensions support

The plugin aims to provide basic support (at least) for the most used
extensions. Unfortunately, sometimes you must customize the messages
extraction process using HTML comments to exclude certain syntaxes that are
extension-dependent, or change a bit the format of your Markdown files.

## [Officially supported extensions](https://python-markdown.github.io/extensions/#officially-supported-extensions)

<!-- mdpo-disable-next-line -->
### [**`abbr`**](https://python-markdown.github.io/extensions/abbreviations)

You must always let one newline between each reference:

<!-- mdpo-disable-next-line -->
=== "Input"

    ```markdown
    The HTML specification
    is maintained by the W3C.

    *[HTML]: Hyper Text Markup Language

    *[W3C]:  World Wide Web Consortium
    ```
    
<!-- mdpo-disable-next-line -->
=== "Output"

    The HTML specification
    is maintained by the W3C.

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

Only `title` attributes values are translated. Currently, this
extension is a bit tricky because the title should be translated two times.

<!-- mdpo-disable-next-line -->
=== "Input"

    ```markdown
    #### [link](https://mondeja.github.io/mkdocs-mdpo-plugin){: title="With a translated title!" }
    ```

<!-- mdpo-disable-next-line -->
=== "Output"

    #### [link](https://mondeja.github.io/mkdocs-mdpo-plugin){: title="With a translated title!" }

<!-- mdpo-disable-next-line -->
=== "PO file content"

    ```po
    msgid ""
    "[link](https://mondeja.github.io/mkdocs-mdpo-plugin){: title=\"With a "
    "translated title!\" }"
    msgstr ""

    msgid "With a translated title!"
    msgstr ""
    ```

<!-- mdpo-disable-next-line -->
### [**`def_list`**](https://python-markdown.github.io/extensions/def_list)

<!-- mdpo-disable-next-line -->
=== "Input"

    ```markdown
    Apple
    :   Pomaceous fruit of plants of the genus Malus in
        the family Rosaceae.

    Orange
    :   The fruit of an evergreen tree of the genus Citrus.
    ```

<!-- mdpo-disable-next-line -->
=== "Output"

    Apple
    :   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

    Orange
    :   The fruit of an evergreen tree of the genus Citrus.

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
=== "Input"

    ````javascript
    <!-- mdpo-include-codeblock -->
    ```
    var hello = "world";
    ```
    ````

<!-- mdpo-disable-next-line -->
=== "Output"

        var hello = "world";

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
=== "Input"

    ```
    This is a footnote[^1]. This is another[^2].

    [^1]: This is a footnote content.

    [^2]: This is another footnote content.
    ```

<!-- mdpo-disable-next-line -->
=== "Output"

    This is a footnote[^1]. This is another[^2].

[^1]: This is a footnote content.

[^2]: This is another footnote content.

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
=== "Input"

    ```markdown
    First Header  | Second Header
    ------------- | -------------
    Content Cell  | Content Cell
    Content Cell  | Content Cell
    ```

<!-- mdpo-disable-next-line -->
=== "Output"

    First header  | Second header
    ------------- | -------------
    Content cell  | Content cell
    Content cell  | Content cell


<!-- mdpo-disable-next-line -->
### [**`admonition`**](https://python-markdown.github.io/extensions/admonition)

You must always include a
[`<!-- mdpo-disable-next-line -->`](https://mdpo.readthedocs.io/en/master/commands.html#disabling-extraction)
HTML comment before the admonition. 

<!-- mdpo-disable-next-line -->
=== "Input"

    ```markdown
    <!-- mdpo-disable-next-line -->
    !!! note "Admonition title"

        Don't be afraid, the title will also be included in the PO file.

    <!-- mdpo-disable-next-line -->
    !!! note

        Even the implicit title, which in this case would be "Note". 
    ```

<!-- mdpo-disable-next-line -->
=== "Output"

    !!! note "Admonition title"

        The title will also be included in the PO file.

    !!! note

        Even the implicit title, which in this case would be "Note".

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

<!-- mdpo-disable-next-line -->
### [**`legacy_attrs`**](https://python-markdown.github.io/extensions/legacy_attrs)

Only `title` attribute values are included for translation. Currently, this
extension is a bit tricky because the title should be translated two times.


<!-- mdpo-disable-next-line -->
=== "Input"

    ```markdown
    Some *emphasized text with a title (hover me!){@title=Title for italics text}*.
    ```

<!-- mdpo-disable-next-line -->
=== "Output"

    Some *emphasized text with a title (hover me!){@title=Title for italics text}*.

<!-- mdpo-disable-next-line -->
=== "PO file content"

    ```po
    msgid "Title for italics text"
    msgstr ""

    msgid ""
    "Some *emphasized text with a title (hover me!){@title=Title for italics "
    "text}*."
    msgstr ""
    ```


<!-- mdpo-disable-next-line -->
### [**`wikilinks`**](https://python-markdown.github.io/extensions/wikilinks)

<!-- mdpo-disable-next-line -->
=== "Output"

    [[config]]

<!-- mdpo-disable-next-line -->
=== "PO file content"

    [[config]]
