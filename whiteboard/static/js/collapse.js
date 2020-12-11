function collapseEntry(element) {
  target = element.parentNode.getElementsByClassName('collapsable')[0];
  icon = element.getElementsByClassName('collapsable-icon')[0];
  for(elem of document.getElementsByClassName('collapsable')) {
    if(!elem.classList.contains('w3-hide') && elem != target) {
      elem.classList.add('w3-hide');
    }
  }
  for(elemIcon of document.getElementsByClassName('collapsable-icon')) {
    if(elemIcon.parentNode != element) {
      elemIcon.classList.remove("fa-angle-down");
      elemIcon.classList.remove("fa-angle-up");
      elemIcon.classList.add("fa-angle-down");
    }
  }
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
}
