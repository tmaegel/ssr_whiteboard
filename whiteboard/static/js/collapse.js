function collapseEntry(element) {
  target = element.getElementsByClassName('collapsable')[0];
  elements = document.getElementsByClassName('collapsable');
  for(elem of elements) {
    if(!elem.classList.contains('w3-hide') && elem != target) {
      elem.classList.add('w3-hide');
    }
  }
  if(target) {
    if(target.classList.contains('w3-hide')) {
      target.classList.remove("w3-hide");
    } else {
      target.classList.add("w3-hide");
    }
  }
}
