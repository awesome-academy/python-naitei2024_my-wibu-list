document.addEventListener('DOMContentLoaded', function() {
    // const
    const WEBSITE_NAME = "My Wibu List";
    const MAX_COMMENT_LENGTH = 220;

    // Get all forms related to comments
    const forms = document.querySelectorAll('.comment-form, .edit-cmt-form');

    // Iterate over each form
    forms.forEach(function(form) {
        // Get the corresponding textarea within the form
        const textarea = form.querySelector('textarea');

        // Check if the form and textarea exist
        if (form && textarea) {
            form.addEventListener('submit', function(event) {
                const commentText = textarea.value.trim(); // Define commentText here

                // Check if the comment is empty
                if (commentText === '') {
                    event.preventDefault(); // Prevent form submission
                    alert(`${WEBSITE_NAME}: Comment cannot be empty.`);
                    return; // Exit the function to ensure no further checks or submission
                }

                // Check the length of the comment
                if (commentText.length > MAX_COMMENT_LENGTH) {
                    event.preventDefault(); // Prevent form submission
                    alert(
                        `${WEBSITE_NAME}: Comment is too long. ` +
                        `Please limit your comment to ${MAX_COMMENT_LENGTH} ` +
                        `characters.`
                    );
                }
            });
        }
    });
});
