/**
 * In pymdownx.snippets Markdown demo, the include line
 * must be escaped or the file would be included again,
 * so we must remove the escape ('\' character)
 **/
var removePyMdownxSnippetsMarkdownDemoEscapeChar = function() {
  var pyMdownSnippetsSection = document.getElementById('pymdownxsnippets');
  if (pyMdownSnippetsSection) {
    var markdownCodeBlock = pyMdownSnippetsSection.nextElementSibling.nextElementSibling.children[5].children[0].children[0];
    markdownCodeBlock.innerHTML = markdownCodeBlock.innerHTML.replace('\\', '');
  }
}

document.addEventListener("DOMContentLoaded", function(){
  removePyMdownxSnippetsMarkdownDemoEscapeChar()
});
