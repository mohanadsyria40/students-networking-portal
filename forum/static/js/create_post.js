const threadChoiceSelect = document.getElementById('id_thread_choice');
const newThreadFields = document.getElementById('new-thread-fields');

threadChoiceSelect.addEventListener('change', function() {
  if (this.value === 'new') {
    newThreadFields.style.display = 'block';
  } else {
    newThreadFields.style.display = 'none';
  }
});
