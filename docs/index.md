{%
   include-markdown "../README.md"
   start="<!--intro-start-->"
   end="<!--intro-end-->"
%}

## Known limitations

- Link references are not supported, all link addresses must be inlined.
- The command `mkdocs serve` doesn't work because triggers a lot of rebuilds.
 It doesn't seem easy to fix with the current `mkdocs serve` implementation
 (see mkdocs/mkdocs#2061).



