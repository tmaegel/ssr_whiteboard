function openAddScoreDialog() {
  document.getElementById('addScoreDialog').style.display='block';
}
function closeAddScoreDialog() {
  document.getElementById('addScoreDialog').style.display='none';
}
function openEditScoreDialog(element) {
  let scoreId, scoreValue, scoreDatetime, scoreNote, scoreRx;
  scoreId = element.id;
  scoreValue = element.getElementsByClassName('scoreValue')[0].innerText;
  scoreDatetime = element.getElementsByClassName('scoreDatetime')[0].innerText;
  scoreNote = element.getElementsByClassName('scoreNote')[0].innerText;
  scoreRx = element.getElementsByClassName('scoreRx');
  document.getElementById('editScoreValue').value = scoreValue;
  document.getElementById('editScoreDatetime').value = scoreDatetime;
  document.getElementById('editScoreNote').value = scoreNote;
  document.getElementById('editScoreValue').value = scoreValue;
  if(scoreRx.length >= 1) {
    document.getElementById('editScoreRx').checked = true;
  } else {
    document.getElementById('editScoreRx').checked = false;
  }
  document.getElementById('editScoreForm').action = '{{ url_for(request.endpoint, workout_id=workout.id) }}/score/' + scoreId + '/update';
  document.getElementById('deleteScoreBtn').formAction = '{{ url_for(request.endpoint, workout_id=workout.id) }}/score/' + scoreId + '/delete';
  document.getElementById('editScoreDialog').style.display='block';
}
function closeEditScoreDialog() {
  document.getElementById('editScoreDialog').style.display='none';
}
