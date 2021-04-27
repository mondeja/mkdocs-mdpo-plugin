<!--intro-start-->

<!-- mdpo-disable-next-line -->
# mkdocs-mdpo-plugin

Translations for Mkdocs using PO files, fully customizable but simple and easy.
Compatible with [mkdocs-material](https://squidfunk.github.io/mkdocs-material/),
based on [mdpo][mdpo-link].

## Install

```
pip install mkdocs-mdpo-plugin
```

## Usage

Enable the plugin in your `mkdocs.yml`:

```yaml
plugins:
  - mdpo
```

### Minimal configuration

#### With [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)

```yaml
theme:
  name: material
  language: en

extra:
  alternate:
    - name: English
      lang: en
    - name: Español
      link: es
      lang: es

plugins:
  - mdpo
```

#### Standalone

```yaml
plugins:
  - mdpo:
      languages:
        - en     # first language is the original
        - es
```

Both previous configurations will create the same layout of files building the
documentation. Given the next layout in a `docs/` directory:

```
docs
└── index.md
```

After the build, you will get:

```
docs
├── es
│   └── index.md.po
└── index.md
```

Just translate the strings in `docs/es/index.md.po` into Spanish, build again
with `mkdocs build` and the `site/` directory will look like:

```
site
├── 404.html
├── assets
│   ├── images
│   ├── javascripts
│   └── stylesheets
├── es
│   └── index.html
├── index.html
├── sitemap.xml
└── sitemap.xml.gz
```

[mdpo-link]: https://mdpo.readthedocs.io/en/master/
[docs-link]: https://mondeja.github.io/mkdocs-mdpo-plugin/

<!--intro-end-->

Simple and easy. Of course, the extraction of messages is fully customizable,
and the produced layout is fully customizable: you can even translate code
blocks! [Check the full documentation here][docs-link].

