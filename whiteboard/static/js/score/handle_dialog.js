function openAddScoreDialog() {
  document.getElementById('addScoreDialog').style.display='block';
}
function closeAddScoreDialog() {
  document.getElementById('addScoreDialog').style.display='none';
}
function openEditScoreDialog(route, scoreId, element) {
  let scoreValue, scoreDatetime, scoreNote, scoreRx, parent;
  parent = element.parentNode.parentNode.parentNode;
  scoreValue = parent.getElementsByClassName('scoreValue')[0].innerText;
  scoreDatetime = parent.getElementsByClassName('scoreDatetime')[0].innerText;
  scoreNote = parent.getElementsByClassName('scoreNote')[0].innerText;
  scoreRx = parent.getElementsByClassName('scoreRx');
  document.getElementById('editScoreValue').value = scoreValue;
  document.getElementById('editScoreDatetime').value = scoreDatetime;
  document.getElementById('editScoreNote').value = scoreNote;
  document.getElementById('editScoreValue').value = scoreValue;
  if(scoreRx.length >= 1) {
    document.getElementById('editScoreRx').checked = true;
  } else {
    document.getElementById('editScoreRx').checked = false;
  }
  document.getElementById('editScoreForm').action = route + '/score/' + scoreId + '/update';
  document.getElementById('deleteScoreBtn').formAction = route + '/score/' + scoreId + '/delete';
  document.getElementById('editScoreDialog').style.display='block';
}
function closeEditScoreDialog() {
  document.getElementById('editScoreDialog').style.display='none';
}
function openDeleteScoreDialog(route, scoreId = '') {
  document.getElementById('deleteScoreForm').action = route + '/score/' + scoreId + '/delete';
  document.getElementById('deleteScoreDialog').style.display='block';
}
function closeDeleteScoreDialog() {
  document.getElementById('deleteScoreDialog').style.display='none';
}
