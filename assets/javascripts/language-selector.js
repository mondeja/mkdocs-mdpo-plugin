var ORIGINAL_LANG = "en";

var getCurrentIsOriginalLang = function() {
  return window.location.pathname.length == 1 || window.location.pathname.split("/")[1].length != 2;
}

var getCurrentLang = function() {
  var pathSplit = window.location.pathname.split("/");
  if (pathSplit.length > 1) {
    if (pathSplit[1].length != 2) {
      return ORIGINAL_LANG;
    } else {
      return pathSplit[1]
    }
  } else {
    return ORIGINAL_LANG;
  }
}

document.addEventListener("DOMContentLoaded", function(){
  if (window.location.protocol == "file:") {
    return;
  }

  var currentIsOriginalLang = getCurrentIsOriginalLang(),
      currentLang = getCurrentLang();

  var languageItemsToRemove = [];

  var languageSelectorItems = document.getElementsByClassName('md-select__item');
  for (let i=0; i<languageSelectorItems.length; i++) {
    var languageItem = languageSelectorItems[i];
    var link = languageItem.childNodes[1];

    var linkLang = link.getAttribute("hreflang");
    if (currentIsOriginalLang) {
      if (linkLang == ORIGINAL_LANG) {
        languageItemsToRemove.push(languageItem);
      } else {
        link.setAttribute("href", '/' + linkLang + window.location.pathname);
      }
    } else {
      if (linkLang == currentLang) {
        languageItemsToRemove.push(languageItem);
      } else {
        link.setAttribute("href", window.location.pathname.slice(3));
      }
    }
  }

  for (let i=0; i<languageItemsToRemove.length; i++) {
    languageItemsToRemove[i].remove();
  }
})
