//Like
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

//Comment
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
  
//Flip
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

//ReadAloud
const readAloudButtonsContainer = document.querySelector('.box-container');

// Initialize speech synthesis utterance
let speech = new SpeechSynthesisUtterance();
speech.rate = 1.5;

// Variable to track the current speech synthesis
let currentSpeech = null;

// Add event listener to the parent element using event delegation
readAloudButtonsContainer.addEventListener('click', event => {
    const button = event.target.closest('.read-aloud-btn');
    if (!button) return; // If the click wasn't on a "read aloud" button, exit

    event.preventDefault();

    const summary = button.closest('.flipper').querySelector('.summary');
    const words = summary.innerText.split(/\b(?=\w)/); // Split text into words

    // Create a function to highlight a word
    const highlightWord = index => {
      // Remove existing highlights
      summary.querySelectorAll('span.highlighted').forEach(element => {
          element.classList.remove('highlighted');
      });
  
      const word = words[index];
      const regex = new RegExp('\\b' + word + '\\b'); // Word boundary regex
  
      // Highlight the current word
      summary.innerHTML = summary.innerText.replace(regex, '<span class="highlighted" style="background-color: #C7ABAB;">$&</span>');
    };

    // Reset previous highlighting
    summary.innerHTML = summary.innerText;

    speech.text = summary.innerText;

    let wordIndex = 0;

    // Event listener for speech synthesis events
    speech.onstart = () => {
        // Highlight the first word when speech starts
        highlightWord(wordIndex);
    };

    speech.onboundary = event => {
        if (event.name === 'word') {
            // Highlight the next word
            wordIndex++;
            highlightWord(wordIndex);
        }
    };

    speech.onend = () => {
        // Remove highlighting when speech ends
        summary.innerHTML = summary.innerText;
    };

    if (currentSpeech && currentSpeech === speech && window.speechSynthesis.speaking) {
        // If the current speech is the same as the clicked article and speech synthesis is ongoing
        window.speechSynthesis.cancel(); // Stop speech synthesis
        currentSpeech = null; // Reset current speech
    } else if (currentSpeech === speech && window.speechSynthesis.paused) {
        // If the current speech is paused, resume it
        window.speechSynthesis.resume();
    } else {
        // Start speech synthesis
        window.speechSynthesis.cancel(); // Cancel any ongoing speech synthesis
        window.speechSynthesis.speak(speech); // Start speech synthesis
        currentSpeech = speech; // Set current speech
    }
});



//Dictionary
function toggleDialog() {
  var dialogBox = document.getElementById("dialogBox");
  var overlay = document.querySelector(".overlay");
  if (dialogBox.style.display === "none" || dialogBox.style.display === "") {
    dialogBox.style.display = "block";
    overlay.style.display = "block";
    // Set focus to the first interactive element in the dialog box
    dialogBox.querySelector("input").focus();
  } else {
    closeDialog();
  }
}

function closeDialog() {
  var dialogBox = document.getElementById("dialogBox");
  var overlay = document.querySelector(".overlay");
  dialogBox.style.display = "none";
  overlay.style.display = "none";
}

async function fetchandCreateCard() {
  const input = document.querySelector('input');
  const dictionaryArea = document.querySelector('.dictionary-app');
  const word = input.value;

  try {
    const res = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
    const data = await res.json();

    let partOfSpeechArray = [];
    for (let i = 0; i < data[0].meanings.length; i++) {
      partOfSpeechArray.push(data[0].meanings[i].partOfSpeech);
    }

    dictionaryArea.innerHTML = `
      <div class="card">
        <div class="property">
          <span>Word:</span>
          <span>${data[0].word}</span>
        </div>

        <div class="property">
          <span>Phonetics:</span>
          <span>${data[0].phonetic}</span>
        </div>

        <div class="property">
          <span>
            <audio controls src="${data[0].phonetics[0].audio}" volume="10.0"></audio>
          </span>
        </div>

        <div class="property">
          <span>Definition</span>
          <span>${data[0].meanings[0].definitions[0].definition}</span>
        </div>

        <div class="property">
          <span>${partOfSpeechArray.join(', ')}</span>
        </div>
      </div>
    `;
  } catch (error) {
    console.error("Error fetching dictionary content:", error);
  }
}

//ShareArticle
function shareArticle(articleLink, articleTitle) {
  // Construct the share message
  const shareMessage = `Check out this article: ${articleTitle} - ${articleLink}`;
  
  // Define platforms and their corresponding share URLs
  const sharePlatforms = {
    whatsapp: {
      url: `whatsapp://send?text=${encodeURIComponent(shareMessage)}`,
      color: '#25D366' // WhatsApp green
    },
    facebook: {
      url: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(articleLink)}`,
      color: '#1877F2' // Facebook blue
    },
    Email: {
      url: `https://mail.google.com/mail/?view=cm&fs=1&to=&su=${encodeURIComponent(articleTitle)}&body=${encodeURIComponent(shareMessage)}`,
      color: '#949494' // Email orange
    },
    twitter: {
      url: `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareMessage)}`,
      color: '#000000' // Twitter blue
    },
    reddit: {
      url: `https://www.reddit.com/submit?url=${encodeURIComponent(articleLink)}&title=${encodeURIComponent(articleTitle)}`,
      color: '#FF4500' // Reddit orange-red
  },
  pinterest: {
      url: `https://www.pinterest.com/pin/create/button/?url=${encodeURIComponent(articleLink)}&media=&description=${encodeURIComponent(articleTitle)}`,
      color: '#BD081C' // Pinterest red
  },
  linkedin: {
      url: `https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(articleLink)}&title=${encodeURIComponent(articleTitle)}`,
      color: '#0077B5' // LinkedIn blue
  }
    
    // Add more platforms as needed
  };

 // Create buttons for each platform with icons and authentic colors
  const shareButtonsContainer = document.createElement('div');
  for (const platform in sharePlatforms) {
    const shareButtonContainer = document.createElement('div');
    shareButtonContainer.style.margin = '10px'; // Add margin between button containers
    shareButtonsContainer.style.display = 'flex'; // Use flexbox
    shareButtonsContainer.style.flexWrap = 'wrap'; // Allow wrapping of buttons
    shareButtonContainer.style.textAlign = 'center'; // Center the label
    shareButtonContainer.style.marginTop = '50px'; // Increase margin at the bottom
          
    
    const shareButton = document.createElement('button');
    shareButton.style.width = '50px'; // Set width and height to ensure it's a circle
    shareButton.style.height = '50px'; 
    shareButton.style.marginRight = '10px';
    shareButton.style.marginBottom = '10px';
    shareButton.style.padding = '10px'; // Decrease padding to fit larger icons
    shareButton.style.backgroundColor = sharePlatforms[platform].color;
    shareButton.style.color = '#fff';
    shareButton.style.border = 'none';
    shareButton.style.borderRadius = '50%'; // Make it circular
    shareButton.style.cursor = 'pointer';
    shareButton.style.transition = 'background-color 0.3s';
    shareButton.innerHTML = platform === 'Email' ? '<i class="fa-solid fa-envelope" style="font-size: 30px;"></i>' :
    platform === 'twitter' ? '<i class="fab fa-x-twitter" style="color: #FFFFFF; font-size: 30px;"></i>' 
    : `<i class="fab fa-${platform}" style="font-size: 30px;"></i>`;

    const platformLabel = document.createElement('div');
    platformLabel.textContent = platform; // Add platform name
    platformLabel.style.fontSize = '18px'; // Adjust font size
   

    shareButton.addEventListener('click', () => {
      window.open(sharePlatforms[platform].url, platform, 'width=600,height=400');
    });
    
    shareButtonContainer.appendChild(shareButton);
    shareButtonContainer.appendChild(platformLabel); // Append label to button container
    shareButtonsContainer.appendChild(shareButtonContainer);
  }


  // Open a dialog box with platform buttons
  const dialog = document.createElement('div');
  dialog.appendChild(shareButtonsContainer);
  dialog.style.padding = '20px';
  dialog.style.backgroundColor = '#fff';
  dialog.style.borderRadius = '10px'; // Increase border radius for rounded corners
  dialog.style.boxShadow = '0px 2px 5px rgba(0, 0, 0, 0.2)';
  dialog.style.position = 'fixed';
  dialog.style.top = '50%';
  dialog.style.left = '50%';
  dialog.style.transform = 'translate(-50%, -50%)';
  dialog.style.zIndex = '1001'; // Ensure dialog is on top of other elements

  // Add the dialog to the body
  document.body.appendChild(dialog);

  // Add the "Share" text at the top left corner
  const shareText = document.createElement('div');
  shareText.textContent = 'Share';
  shareText.style.position = 'absolute';
  shareText.style.top = '20px';
  shareText.style.left = '35px';
  shareText.style.fontSize = '25px';
  shareText.style.fontWeight = 'bold';
  dialog.appendChild(shareText);
  
  // Close icon btn
  const closeButton = document.createElement('button');
  closeButton.innerHTML = '<i class="fas fa-times"></i>'; // Font Awesome close icon
  closeButton.style.position = 'absolute';
  closeButton.style.top = '10px';
  closeButton.style.right = '10px';
  closeButton.style.backgroundColor = 'transparent';
  closeButton.style.border = 'none';
  closeButton.style.cursor = 'pointer';
  closeButton.style.fontSize = '20px';
  closeButton.style.color = '#000'; // Set color for the icon
  
  // Add an event listener to close the dialog when the close button is clicked
  closeButton.addEventListener('click', () => {
    document.body.removeChild(dialog);
    document.body.removeChild(overlay);
  });
  // Append the close button to the dialog
  dialog.appendChild(closeButton);
  // Close the dialog when clicking outside of it
  const overlay = document.createElement('div');
  overlay.style.position = 'fixed';
  overlay.style.top = '0';
  overlay.style.left = '0';
  overlay.style.width = '100%';
  overlay.style.height = '100%';
  overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
  overlay.style.zIndex = '1000'; // Ensure overlay is below dialog
  overlay.addEventListener('click', () => {
    document.body.removeChild(dialog);
    document.body.removeChild(overlay);
  });
  document.body.appendChild(overlay);
}


//Bookmark
// Function to toggle bookmark
function toggleBookmark(event, articleId) {
  event.preventDefault(); // Prevent default link behavior

  // Send a POST request to your Django view to toggle the bookmark
  fetch(`/toggle_bookmark/${articleId}/`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'), // Ensure you have a function to get CSRF token
      },
      body: JSON.stringify({ article_id: articleId }),
  })
  .then(response => response.json())
  .then(data => {
      // Update the bookmark icon based on the response
      const bookmarkIcon = event.target.querySelector('i');
      if (data.is_bookmarked) {
          bookmarkIcon.classList.add('fa-bookmark');
          bookmarkIcon.classList.remove('fa-bookmark-o');
          bookmarkIcon.nextSibling.textContent = ' Remove Bookmark';
      } else {
          bookmarkIcon.classList.add('fa-bookmark-o');
          bookmarkIcon.classList.remove('fa-bookmark');
          bookmarkIcon.nextSibling.textContent = ' Save';
      }
  })
  .catch(error => console.error('Error toggling bookmark:', error));
}

// Function to get CSRF token from cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}
