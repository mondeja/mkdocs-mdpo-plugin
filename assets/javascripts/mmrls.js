var __MMRLSP_ORIGINAL_LANG = "en";

var getCurrentLang = function() {
  var pathSplit = window.location.pathname.split("/");
  for (let i=1; i<pathSplit.length; i++) {
    if (pathSplit[i].length == 2) {
      return pathSplit[i];
    }
  }
  return __MMRLSP_ORIGINAL_LANG;
}

document.addEventListener("DOMContentLoaded", function(){
  var MMRLSP_PATH_SPLITTER_INDEX = true ? 1 : 2;

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
    if (currentLang == __MMRLSP_ORIGINAL_LANG) {
      if (linkLang == __MMRLSP_ORIGINAL_LANG) {
        languageItemsToRemove.push(languageItem);
      } else {
        var pathSplit = window.location.pathname.split("/");
        var newLink = pathSplit.slice(0, MMRLSP_PATH_SPLITTER_INDEX).join('/') + '/' + linkLang + '/';
        newLink += pathSplit.slice(MMRLSP_PATH_SPLITTER_INDEX).join("/")
        link.setAttribute("href", newLink);
      }
    } else {
      if (linkLang == currentLang) {
        languageItemsToRemove.push(languageItem);
      } else {
        if (linkLang == __MMRLSP_ORIGINAL_LANG) {
          linkLang = '';
        }
        var pathSplit = window.location.pathname.split("/");
        var newLink = pathSplit.slice(0, MMRLSP_PATH_SPLITTER_INDEX).join('/') + '/';
        if (linkLang.length && linkLang != __MMRLSP_ORIGINAL_LANG) {
          newLink += (linkLang + '/');
        }
        newLink += pathSplit.slice(MMRLSP_PATH_SPLITTER_INDEX + 1).join("/")

        link.setAttribute("href", newLink);
      }
    }
  }

  for (let i=0; i<languageItemsToRemove.length; i++) {
    languageItemsToRemove[i].remove();
  }
});
