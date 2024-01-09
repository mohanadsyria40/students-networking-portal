document.addEventListener('DOMContentLoaded', function() {
    const threadChoice = document.getElementById('id_thread');
    const newThreadFields = document.getElementById('new-thread-fields');

    threadChoice.addEventListener('change', function() {
        if (threadChoice.value === 'new') {
            newThreadFields.style.display = 'block';
        } else {
            newThreadFields.style.display = 'none';
        }
    });
});

document.getElementById('submit-post').addEventListener('click', function () {
    var selectedOption = document.getElementById('id_thread').value;

    if (selectedOption === 'new') {
        // If a new thread is selected, submit both the new thread and the post
        document.getElementById('new-thread-form').submit();
    } else {
        // If an existing thread is selected, submit only the post
        document.getElementById('post-form').submit();
    }
});


// Updated JavaScript to handle button position
document.getElementById('id_thread').addEventListener('change', function () {
    var selectedOption = document.getElementById('id_thread').value;
    var postButton = document.getElementById('submit-post');

    if (selectedOption === 'new') {
        // If a new thread is selected, move the button under the new thread form
        document.getElementById('new-thread-fields').appendChild(postButton);
    } else {
        // If an existing thread is selected, move the button back to the main form
        document.getElementById('post-form').appendChild(postButton);
    }
});