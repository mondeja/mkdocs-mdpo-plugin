/**
 * In pymdownx.snippets Markdown demo, the include line
 * must be escaped or the file would be included again,
 * so we must remove the escape ('\' character)
 **/
var removePyMdownxSnippetsMarkdownDemoEscapeChar = function() {
  var pyMdownSnippetsSection = document.getElementById('pymdownxsnippets');
  if (pyMdownSnippetsSection) {
    console.log(pyMdownSnippetsSection)
    var markdownCode = pyMdownSnippetsSection.nextElementSibling.children[5].children[0].children[0];
    for (let i=0; i<markdownCode.children.length; i++) {
      let child = markdownCode.children[i];
      if (child.tagName === 'CODE') {
        child.innerHTML = child.innerHTML.replace('\\', '');
        break;
      }
    }
  }
}

document.addEventListener("DOMContentLoaded", function(){
  removePyMdownxSnippetsMarkdownDemoEscapeChar()
});
