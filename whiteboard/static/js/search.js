function doSearch() {
  // Declare variables
  var input, filter, ul, li, i, value;
  input = document.getElementById('search-input');
  filter = input.value.toUpperCase();
  ul = document.getElementById('searchable');
  li = ul.getElementsByTagName('li');
  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    value = li[i].textContent || li[i].innerText;
    if (value.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = '';
    } else {
      li[i].style.display = 'none';
    }
  }
}

function toggleSearch() {
  let searchbar = document.getElementById('searchbar');
  let titlebar = document.getElementById('titlebar');
  if(searchbar.classList.contains('w3-hide')) {
    titlebar.classList.add("w3-hide");
    searchbar.classList.remove("w3-hide");
  } else {
    titlebar.classList.remove("w3-hide");
    searchbar.classList.add("w3-hide");
    search = document.getElementById('search-input');
    search.value = '';
    doSearch();
  }
}
