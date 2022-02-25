<!-- mdpo-disable-next-line -->
# mkdocs-mdpo-plugin

{%
   include-markdown "../../README.md"
   start="<!--description-start-->"
   end="<!--description-end-->"
   rewrite_relative_urls=false
   comments=false
%}

{%
   include-markdown "../../README.md"
   start="<!--intro-start-->"
   end="<!--intro-end-->"
   rewrite_relative_urls=false
   comments=false
%}

## How does it works

**mkdocs-mdpo-plugin** is based in [mdpo][mdpo-docs] which is a program to
translate [CommonMark][commonmark] compliant Markdown content using PO files.

!!! tip

    See also [the traditional approach for Markdown translations][mdpo-traditional-approach-docs]
    and [mdpo approach][mdpo-approach-docs].

As with [mkdocs][mkdocs-docs] you write
[Python-Markdown][python-markdown-docs]'s implementation of Markdown,
**mkdocs-mdpo-plugin** uses the
[`xml.etree.ElementTree`][xml.etree.ElementTree] to translate the rest messages
of custom HTML created by the [extensions][python-markdown-extensions-docs].
This is the reason why for some of them the translation process must be
adjusted somewhat to be supported correctly (see
[Extensions support][extensions-support-official]).

## Known limitations

- The command `mkdocs serve` doesn't work if you store the PO files inside
 the documentation folder. Use another layout like the explained in
 [`locale_dir` configuration](config/#locale_dir-str).
- Currently, edited messages are not marked as fuzzy like
 [xgtettext][xgettext-docs] does.

## Projects using mkdocs-mdpo-plugin

<!-- mdpo-disable -->
- [http-request-codegen][hrcgen-docs]
<!-- mdpo-enable -->

[mdpo-docs]: https://mdpo.readthedocs.io
[mdpo-approach-docs]: https://mdpo.readthedocs.io/en/master/rationale.html#mdpo-approach
[mdpo-traditional-approach-docs]: https://mdpo.readthedocs.io/en/master/before-using.html#the-traditional-approach
[commonmark]: https://spec.commonmark.org/0.29/
[mkdocs-docs]: https://www.mkdocs.org/
[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[python-markdown-docs]: https://python-markdown.github.io/
[python-markdown-extensions-docs]: https://python-markdown.github.io/extensions/
[xml.etree.ElementTree]: https://docs.python.org/3/library/xml.etree.elementtree.html
[mkdocs#2061]: https://github.com/mkdocs/mkdocs#2061
[xgettext-docs]: https://www.gnu.org/software/gettext/manual/gettext.html#xgettext-Invocation
[extensions-support-official]: https://mondeja.github.io/mkdocs-mdpo-plugin/es/extensions-support/official/
[hrcgen-docs]: https://hrcgen.ml
