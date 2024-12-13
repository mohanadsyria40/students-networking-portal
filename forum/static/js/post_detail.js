function indentReplies() {
  const comments = document.querySelectorAll('.box');

  comments.forEach(comment => {
    let level = comment.classList.contains('reply') ? 1 : 0;
    const parentReplies = comment.closest('.reply');
    if (parentReplies) {
      level += parentReplies.querySelectorAll('.reply').length;
    }

    comment.style.marginLeft = level * 40 + 'px'; // Adjust indentation as desired
  });
}

indentReplies(); // Call the function initially

const toggleButton = document.getElementById('toggle-comments');

toggleButton.addEventListener('click', () => {
  const commentsContainer = document.getElementById('comments-container');
  const isChevronDown = toggleButton.classList.contains('fa-chevron-down');

  if (isChevronDown) {
    commentsContainer.style.display = 'block';
    toggleButton.classList.remove('fa-chevron-down');
    toggleButton.classList.add('fa-chevron-up'); // Visually indicate expansion
  } else {
    commentsContainer.style.display = 'none';
    toggleButton.classList.remove('fa-chevron-up');
    toggleButton.classList.add('fa-chevron-down'); // Visually indicate collapse
  }
});

