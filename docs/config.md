# Configuration

Always put `mdpo` plugin in `mkdocs.yml` file after other plugins which could
edit the content of your files:

```yaml
- plugins
  - search 
  - include-markdown
  - mdpo
```

## Fields

The layout of the generated files can be customized using different
configuration fields:

<!-- mdpo-disable-next-line -->
### **`languages`**

Languages to translate your files into. Commonly defined as
[ISO 639 codes](https://en.wikipedia.org/wiki/ISO_639).

<!-- mdpo-disable-next-line -->
!!! note

    If you are using [mkdocs-material](https://squidfunk.github.io/mkdocs-material)
    theme, can also be defined in the `extra.alternate` configuration setting (see
    [Site language selector](https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/#site-language-selector)).
