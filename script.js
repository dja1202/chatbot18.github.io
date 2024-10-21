document.getElementById('send-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    const chatDisplay = document.getElementById('chat-display');
    
    // Create a new message element
    const newMessage = document.createElement('div');
    newMessage.textContent = userInput;
    newMessage.style.margin = '10px 0';
    
    // Append the new message to the chat display
    chatDisplay.appendChild(newMessage);

    // Clear the input field
    document.getElementById('user-input').value = '';

    // Scroll to the bottom of the chat display
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
});