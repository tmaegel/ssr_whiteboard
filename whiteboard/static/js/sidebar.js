document.addEventListener('click', function() {
  let sidebar = document.getElementById('sidebar');
  sidebar.style.display = 'none';
});

function toggleSidebar(event) {
  let sidebar = document.getElementById('sidebar');
  if(sidebar.style.display == 'block') {
    sidebar.style.display = 'none';
  } else {
    sidebar.style.display = 'block';
  }
  event.stopPropagation();
}
