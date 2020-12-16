function openAddTagDialog() {
  document.getElementById('addTagDialog').style.display='block';
}
function closeAddTagDialog() {
  document.getElementById('addTagDialog').style.display='none';
}
function openEditTagDialog(route, tagId, element) {
  tagName = element.parentNode.parentNode.parentNode.getElementsByClassName('tagName')[0].innerText;
  document.getElementById('editTagName').value = tagName;
  document.getElementById('editTagForm').action = route + tagId + '/update';
  document.getElementById('editTagDialog').style.display='block';
}
function closeEditTagDialog() {
  document.getElementById('editTagDialog').style.display='none';
}
function openDeleteTagDialog(route, tagId) {
  document.getElementById('deleteTagForm').action = route + tagId + '/delete';
  document.getElementById('deleteTagDialog').style.display='block';
}
function closeDeleteTagDialog() {
  document.getElementById('deleteTagDialog').style.display='none';
}
