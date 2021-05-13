<!-- mdpo-disable-next-line -->
# mkdocs-mdpo-plugin

{%
   include-markdown "../README.md"
   start="<!--description-start-->"
   end="<!--description-end-->"
   rewrite_relative_urls=false
%}

{%
   include-markdown "../README.md"
   start="<!--intro-start-->"
   end="<!--intro-end-->"
   rewrite_relative_urls=false
%}

## Known limitations

- The command `mkdocs serve` doesn't work because triggers a lot of rebuilds.
 It doesn't seem easy to fix with the current `mkdocs serve` implementation
 (see [mkdocs/mkdocs#2061](https://github.com/mkdocs/mkdocs#2061)).
