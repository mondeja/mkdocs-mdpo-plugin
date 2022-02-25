# Useful recipes

## Relative mkdocs-material's language selector

If you are using the [mkdocs-material theme][mkdocs-material], you can install
the [`mkdocs-material-relative-language-selector` plugin][mmrls] to make
relative links between languages inside the same page and remove the current
displayed language from the language selector:

=== "Install"

    ```
    pip install mkdocs-material-relative-language-selector
    ```

=== "Github Pages configuration"

    ```yaml
    plugins:
      - search
      - material-relative-language-selector
      - mdpo
    ```

=== "Custom root domain configuration"

    ```yaml
    plugins:
      - search
      - material-relative-language-selector:
          root_domain: true
      - mdpo
    ```

## pre-commit PO hooks

You can use [pre-commit-po-hooks] to check for untranslated, obsolete
and fuzzy messages before each commit.

<!-- mdpo-disable-next-line -->
=== ".pre-commit-config.yaml"

    ```yaml
    - repo: https://github.com/mondeja/pre-commit-po-hooks
      rev: v1.7.0
      hooks:
        - id: obsolete-messages
        - id: untranslated-messages
        - id: fuzzy-messages
    ```

=== "Example output"

    ```
    untranslated-messages....................................................Failed
    - hook id: untranslated-messages
    - exit code: 1

    Untranslated message at docs/locale/es/index.md.po:46

    obsolete-messages........................................................Passed
    fuzzy-messages...........................................................Failed
    - hook id: fuzzy-messages
    - exit code: 1

    Found fuzzy message at docs/locale/es/index.md.po:48
    ```

[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[mmrls]: https://github.com/mondeja/mkdocs-material-relative-language-selector
[pre-commit-po-hooks]: https://github.com/mondeja/pre-commit-po-hooks#readme
