# mkdocs-mdpo-plugin

[![PyPI version](https://img.shields.io/pypi/v/mkdocs-mdpo-plugin?label=version)](https://pypi.org/project/mkdocs-mdpo-plugin)
[![Downloads](https://img.shields.io/pypi/dm/mkdocs-mdpo-plugin)](https://pypistats.org/packages/mkdocs-mdpo-plugin)

[![Test](https://img.shields.io/github/workflow/status/mondeja/mkdocs-mdpo-plugin/CI?label=tests&logo=github)](https://github.com/mondeja/mkdocs-mdpo-plugin/actions?query=workflow%3ACI)
[![Documentation](https://img.shields.io/github/workflow/status/mondeja/mkdocs-mdpo-plugin/Github%20Pages?label=docs&logo=github)](https://mkdocs-mdpo.ga)
[![Cloudflare DNS](https://img.shields.io/github/workflow/status/mondeja/mkdocs-mdpo-plugin/website-check?label=dns&logo=cloudflare&logoColor=white)](https://github.com/mondeja/mkdocs-mdpo-plugin/actions/workflows/website-check.yml)

<!--description-start-->

Translations for Mkdocs using PO files, fully customizable.
Compatible with [mkdocs-material](https://squidfunk.github.io/mkdocs-material),
based on [mdpo][mdpo-docs].

<!--description-end-->

## Documentation: [en](https://mkdocs-mdpo.ga) - [es](https://mkdocs-mdpo.ga/es/)

<!--intro-start-->

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

#### With [mkdocs-material](https://squidfunk.github.io/mkdocs-material)

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

<!-- mdpo-include-codeblock -->
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

<!--intro-end-->

Simple and easy. The extraction of messages process and the produced
layout are fully customizable, you can even translate code blocks!
[Check the full documentation here](https://mkdocs-mdpo.ga).

[mdpo-docs]: https://mdpo.readthedocs.io
