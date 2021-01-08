function collapseEntry(element) {
  parent = element.parentNode; // parent li element
  target = parent.getElementsByClassName('collapsable')[0]; // element with collapsable class in parent
  icon = element.getElementsByClassName('collapsable-icon')[0]; // element with collapsable-icon class in parent
  // Hiding all elements with exception the clicked element
  for(elem of document.getElementsByClassName('collapsable')) {
    if(!elem.classList.contains('w3-hide') && elem != target) {
      elem.classList.add('w3-hide');
    }
  }
  // Changing icon to arrow down with exception the clicked element
  for(elemIcon of document.getElementsByClassName('collapsable-icon')) {
    if(elemIcon.parentNode != element) {
      elemIcon.classList.remove("fa-angle-down");
      elemIcon.classList.remove("fa-angle-up");
      elemIcon.classList.add("fa-angle-down");
    }
  }
  for(elemLi of document.getElementsByTagName('li')) {
    if(elemLi != element.parentNode) {
      elemLi.classList.remove("w3-topbar-sm");
      elemLi.classList.remove("w3-bottombar");
      elemLi.classList.remove("w3-border-grey");
    }
  }
  // Handle the clicked element
  if(target) {
    if(target.classList.contains('w3-hide')) {
      target.classList.remove("w3-hide");
    } else {
      target.classList.add("w3-hide");
    }
  }
  if(icon) {
    if(icon.classList.contains('fa-angle-down')) {
      icon.classList.remove("fa-angle-down");
      icon.classList.add("fa-angle-up");
    } else {
      icon.classList.remove("fa-angle-up");
      icon.classList.add("fa-angle-down");
    }
  }
  if(parent) {
    if(parent.classList.contains('w3-bottombar')) {
      parent.classList.remove("w3-topbar-sm");
      parent.classList.remove("w3-bottombar");
      parent.classList.remove("w3-border-grey");
    } else {
      parent.classList.add("w3-topbar-sm");
      parent.classList.add("w3-bottombar");
      parent.classList.add("w3-border-grey");
    }
  }
}
