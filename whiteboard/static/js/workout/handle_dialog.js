function openAddWorkoutDialog() {
  document.getElementById('addWorkoutDialog').style.display='block';
}
function closeAddWorkoutDialog() {
  document.getElementById('addWorkoutDialog').style.display='none';
}
function openEditWorkoutDialog(route, workoutId = '', element = null) {
  if(element != null) {
    let workoutName, workoutDescription, parent;
    parent = element.parentNode.parentNode.parentNode;
    workoutName = parent.getElementsByClassName('workoutName')[0].innerText;
    workoutDescription = parent.getElementsByClassName('workoutDescription')[0].innerText;
    document.getElementById('editWorkoutName').value = workoutName;
    document.getElementById('editWorkoutDescription').value = workoutDescription;
    document.getElementById('editWorkoutForm').action = route + workoutId + '/update';
  }
  document.getElementById('editWorkoutDialog').style.display='block';
}
function closeEditWorkoutDialog() {
  document.getElementById('editWorkoutDialog').style.display='none';
}
function openDeleteWorkoutDialog(route, workoutId = '') {
  document.getElementById('deleteWorkoutForm').action = route + workoutId + '/delete';
  document.getElementById('deleteWorkoutDialog').style.display='block';
}
function closeDeleteWorkoutDialog() {
  document.getElementById('deleteWorkoutDialog').style.display='none';
}
