# [API documentation building][api-documentation-building]

<!-- mdpo-disable -->

<span class="versions-support">0.15.0 < 0.16.0</span>

## [mkdocstrings][mkdocstrings-github-link]

<!-- mdpo-enable -->
You can translate your docstrings using mkdocstrings with mdpo.

!!! warning

    - Starting from v0.16.0 the plugin works but function parameters
    names and types are also added to the PO file as
    ``msgid "**value:** `str` – Value to check."``.

<!-- mdpo-disable -->

=== "Output"

    ### **`mkdocs_mdpo_plugin.docs_helper.function`**

    ::: mkdocs_mdpo_plugin.docs_helper.function

    ### **`mkdocs_mdpo_plugin.docs_helper.other_function`**

    ::: mkdocs_mdpo_plugin.docs_helper.other_function

=== "Markdown"

    ```markdown
    ### **`mkdocs_mdpo_plugin.docs_helper.function`**

    ::: mkdocs_mdpo_plugin.docs_helper.function

    ### **`mkdocs_mdpo_plugin.docs_helper.other_function`**

    ::: mkdocs_mdpo_plugin.docs_helper.other_function
    ```

=== "PO file content"

    ```po
    msgid "Function documentation."
    msgstr "Documentación de función."

    msgid "Value to check."
    msgstr "Valor a comprobar."

    msgid "**`mkdocs_mdpo_plugin.docs_helper.function`**"
    msgstr "**`mkdocs_mdpo_plugin.docs_helper.function`**"

    msgid "Other function documentation."
    msgstr "Documentación de otra función."

    msgid "Return value."
    msgstr "Valor de retorno."

    msgid "**`mkdocs_mdpo_plugin.docs_helper.other_function`**"
    msgstr "**`mkdocs_mdpo_plugin.docs_helper.other_function`**"
    ```

<!-- mdpo-enable -->

[mkdocstrings-github-link]: https://github.com/pawamoy/mkdocstrings

[api-documentation-building]: https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins#api-documentation-building
