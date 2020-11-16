document.getElementById('searchInput').style.display = 'none';

function doSearch() {
  // Declare variables
  var input, filter, ul, li, i, value;
  input = document.getElementById('searchInput');
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
  input = document.getElementById('searchInput');
  title = document.getElementById('pageTitle');
  if(input.style.display == 'none') {
    input.style.display = '';
    title.style.display = 'none';
  } else {
    input.style.display = 'none';
    title.style.display = '';
    input.value = '';
    doSearch();
  }

}
