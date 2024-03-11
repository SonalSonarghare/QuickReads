function toggleHeart(icon) {
    if (icon.classList.contains('fa-regular')) {
        icon.classList.remove('fa-regular');
        icon.classList.add('fa-solid');
        icon.classList.add('fa-heart');
        // Increment the heart count
        var heartCount = parseInt(icon.nextElementSibling.innerText);
        icon.nextElementSibling.innerText = heartCount + 1;
    } else {
        icon.classList.remove('fa-solid');
        icon.classList.remove('fa-heart');
        icon.classList.add('fa-regular');
        // Decrease the heart count
        var heartCount = parseInt(icon.nextElementSibling.innerText);
        icon.nextElementSibling.innerText = heartCount - 1;
    }
    // Stop propagation of the click event
    event.stopPropagation();
}
  
// Function to toggle the visibility of the comment box
function toggleCommentBox(card) {
    var commentBox = card.querySelector('.comment-box');
    if (commentBox.style.display === 'block') {
      commentBox.style.display = 'none';
    } else {
      commentBox.style.display = 'block';
    }
}
  
// Function to handle comment submission
function submitComment(card) {
    // Get the textarea value
    var comment = card.querySelector('.comment-box textarea').value;
    // Clear the textarea
    card.querySelector('.comment-box textarea').value = '';
    // Display "Comment submitted" message
    alert('Comment submitted');
    // Increment the comment count
    var commentCount = parseInt(card.querySelector('.comment-count').innerText);
    card.querySelector('.comment-count').innerText = commentCount + 1;
    // Hide the comment box after submitting the comment
    toggleCommentBox(card);
}
  
// Add event listeners for comment icon click and comment submission
document.querySelectorAll('.fa-comment-dots').forEach(icon => {
    icon.addEventListener('click', function(event) {
      toggleCommentBox(this.closest('.flipper'));
    });
});
  
document.querySelectorAll('.submit-comment').forEach(button => {
    button.addEventListener('click', function() {
      submitComment(this.closest('.flipper'));
    });
});
  

function flipCard(card, event) {
    // Check if the clicked element is one of the elements that should not trigger the flip
    if (
      event.target.closest('.circle-logo') ||
      event.target.closest('.photo') ||
      event.target.closest('.title') ||
      event.target.closest('.userdata') ||
      event.target.closest('.comment-box')||
      event.target.closest('.read-aloud-btn') // Added read-aloud-btn here
    ) {
      return; // Do not flip if the clicked element is one of the specified elements or their children
    }
    
    card.classList.toggle('flipped'); // Flip the card otherwise
}


let speech = new SpeechSynthesisUtterance();
speech.rate = 1.5;
// Select the button by its class name and add event listener
document.querySelectorAll('.read-aloud-btn').forEach(button => {
    button.addEventListener("click", (event) => {
        // Prevent the default behavior of the button
        event.preventDefault();
        // Get the text content of the summary
        var summary = button.closest('.flipper').querySelector('.summary');
        speech.text = summary.innerText;
        // Toggle speech synthesis based on the current state
        if (window.speechSynthesis.speaking && window.speechSynthesis.paused && speech.text === summary.innerText) {
          window.speechSynthesis.resume();
        } else if (window.speechSynthesis.speaking && !window.speechSynthesis.paused) {
          window.speechSynthesis.pause();
        } else {
          // Speak the text
          window.speechSynthesis.speak(speech);
        }
    });
});