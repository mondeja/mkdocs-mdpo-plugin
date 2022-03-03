# Useful recipes

## pre-commit PO hooks

You can use [pre-commit-po-hooks] to check for untranslated, obsolete
and fuzzy messages before each commit.

<!-- mdpo-disable-next-line -->
=== ".pre-commit-config.yaml"

    ```yaml
    - repo: https://github.com/mondeja/pre-commit-po-hooks
      rev: v1.7.3
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

<!-- mdpo-disable-next-line -->
## mdpo

[mdpo] is the core of **mkdocs-mdpo-plugin**. The package contains a set of
programs to translate Markdown files using [PO files][po-files], so you can
use them directly [as a command line interface][mdpo-cli] or through is
[pre-commit hooks][mdpo-pre-commit].

### Simple README file translation with pre-commit

<!-- mdpo-disable-next-block -->
=== "`md2po2md` command line interface"

    ```bash
    md2po2md README.md -l es fr -o locale/{lang}
    ```

=== "pre-commit hook configuration"

    ```yaml
    - repo: https://github.com/mondeja/mdpo
      rev: v0.3.85
      hooks:
        - id: md2po2md
          files: ^README\.md
          args: ['-l', 'es', 'fr', '-o', 'locale/{lang}']
    ```
<!-- mdpo-include-codeblocks -->
=== "Directories tree"

    ```
    📁 locale
    ├── 📁 es
    │   ├── 📄 README.md
    │   └── 📄 README.md.po
    └── 📁 fr
        ├── 📄 README.md
        └── 📄 README.md.po
    📄 README.md             <-- only existing file before execution
    ```

<!-- mdpo-disable-codeblocks -->

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

[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[mmrls]: https://github.com/mondeja/mkdocs-material-relative-language-selector
[pre-commit-po-hooks]: https://github.com/mondeja/pre-commit-po-hooks#readme
[mdpo]: https://mdpo.readthedocs.io/en/master/index.html
[mdpo-cli]: https://mdpo.readthedocs.io/en/master/cli.html
[mdpo-pre-commit]: https://mdpo.readthedocs.io/en/master/pre-commit-hooks.html
[po-files]: https://www.gnu.org/software/gettext/manual/gettext.html#PO-Files
