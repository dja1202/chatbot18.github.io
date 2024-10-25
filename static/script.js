// Get DOM elements
const messagesDiv = document.getElementById('messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// Function to add messages with streaming effect
async function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    messageDiv.appendChild(messageContent);
    messagesDiv.appendChild(messageDiv);
    
    if (!isUser) {
        // Add formal letter opening for bot messages
        messageContent.innerHTML = 'Mon cher ami,<br><br>';
        
        // Create typing effect
        let i = 0;
        messageContent.innerHTML += '<span class="typing"></span>';
        
        // Stream each character
        for (const char of content) {
            await new Promise(resolve => setTimeout(resolve, 50));
            const typing = messageContent.querySelector('.typing');
            if (typing) {
                typing.textContent += char;
            }
        }
        
        // Add signature after typing is complete
        messageContent.innerHTML = 'Mon cher ami,<br><br>' + content + '<br><br>Cordialement,<br>Claude Monet';
    } else {
        messageContent.textContent = content;
    }

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Main send function
async function handleSend() {
    const userMessage = userInput.value.trim();
    if (userMessage === '') return;

    // Display user message
    await addMessage(userMessage, true);
    userInput.value = '';

    try {
        const response = await fetch('/api/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage }),
        });

        const data = await response.json();
        // Display bot response with streaming effect
        await addMessage(data.response, false);
    } catch (error) {
        console.error('Error:', error);
        await addMessage("Je suis désolé, there seems to be an issue with our correspondence.", false);
    }
}

// Event listeners
sendButton.addEventListener('click', handleSend);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSend();
    }
});

// Add welcome message when the page loads
window.addEventListener('load', async () => {
    await addMessage("Bonjour! It is with great pleasure that I greet you today. My name is Claude Monet, and I am a painter, a lover of nature, and a captivated observer of the interplay of light. I hope that my words have given you a sense of my passion for painting, my love for nature, and my deep reverence for the interplay of light. I would be honored to converse with you, to share more of my thoughts and experiences. Please, do not hesitate to ask me anything.", false);
});