var ORIGINAL_LANG = "en";

var PATH_SPLITTER_INDEX = true ? 1 : 2;

var getCurrentLang = function() {
  var pathSplit = window.location.pathname.split("/");
  for (let i=1; i<pathSplit.length; i++) {
    if (pathSplit[i].length == 2) {
      return pathSplit[i];
    }
  }
  return ORIGINAL_LANG;
}

document.addEventListener("DOMContentLoaded", function(){
  if (window.location.protocol == "file:") {
    return;
  }

  var currentLang = getCurrentLang(),
      languageItemsToRemove = [],
      languageSelectorItems = document.getElementsByClassName('md-select__item');

  for (let i=0; i<languageSelectorItems.length; i++) {
    var languageItem = languageSelectorItems[i];
    var link = languageItem.childNodes[1];

    var linkLang = link.getAttribute("hreflang");
    if (currentLang == ORIGINAL_LANG) {
      if (linkLang == ORIGINAL_LANG) {
        languageItemsToRemove.push(languageItem);
      } else {
        var pathSplit = window.location.pathname.split("/");
        var newLink = pathSplit.slice(0, PATH_SPLITTER_INDEX).join('/') + '/' + linkLang + '/';
        if (pathSplit.length > 3) {
          newLink += pathSplit.slice(PATH_SPLITTER_INDEX).join("/")
        }
        link.setAttribute("href", newLink);
      }
    } else {
      if (linkLang == currentLang) {
        languageItemsToRemove.push(languageItem);
      } else {
        if (linkLang == ORIGINAL_LANG) {
          linkLang = '';
        }
        var pathSplit = window.location.pathname.split("/");
        var newLink = pathSplit.slice(0, PATH_SPLITTER_INDEX).join('/') + '/';
        if (linkLang.length && linkLang != ORIGINAL_LANG) {
          newLink += (linkLang + '/');
        }
        if (pathSplit.length > 4) {
          newLink += pathSplit.slice(PATH_SPLITTER_INDEX + 1).join("/")
        }

        link.setAttribute("href", newLink);
      }
    }
  }

  for (let i=0; i<languageItemsToRemove.length; i++) {
    languageItemsToRemove[i].remove();
  }
});
