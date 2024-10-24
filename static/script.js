document.getElementById('send-button').addEventListener('click', async () => {
    const inputField = document.getElementById('user-input');
    const userMessage = inputField.value;
    if (userMessage.trim() === '') return; // Prevent empty messages

    // Display the user's message in the chat box
    addMessage('User: ' + userMessage);

    // Clear the input field
    inputField.value = '';

    // Send the message to the Flask API
    try {
        const response = await fetch('/api/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage }),
        });

        const data = await response.json();
        addMessage('Chatbot: ' + data.response);
    } catch (error) {
        console.error('Error:', error);
        addMessage('Chatbot: Sorry, something went wrong.');
    }
});

function addMessage(message) {
    const messagesDiv = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to the bottom
}
