search = document.getElementById('searchbar');
search.value = '';

function doSearch() {
  // Declare variables
  var input, filter, ul, li, i, value;
  input = document.getElementById('searchbar');
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
