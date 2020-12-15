function openAddTagDialog() {
  document.getElementById('addTagDialog').style.display='block';
}
function closeAddTagDialog() {
  document.getElementById('addTagDialog').style.display='none';
}
function openEditTagDialog(element, tagId) {
  tagName = element.parentNode.parentNode.parentNode.getElementsByClassName('tagName')[0].innerText;
  document.getElementById('editTagName').value = tagName;
  document.getElementById('editTagForm').action = '{{ url_for(request.endpoint) }}' + tagId + '/update';
  document.getElementById('editTagDialog').style.display='block';
}
function closeEditTagDialog() {
  document.getElementById('editTagDialog').style.display='none';
}
function openDeleteTagDialog(tagId) {
  document.getElementById('deleteTagForm').action = '{{ url_for(request.endpoint) }}' + tagId + '/delete';
  document.getElementById('deleteTagDialog').style.display='block';
}
function closeDeleteTagDialog() {
  document.getElementById('deleteTagDialog').style.display='none';
}
