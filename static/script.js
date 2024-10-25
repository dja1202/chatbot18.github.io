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
        // Add formal letter opening
        const opening = document.createElement('div');
        opening.innerHTML = 'Mon cher ami,<br><br>';
        opening.className = 'fade-in-text';
        messageContent.appendChild(opening);
        
        // Create container for streaming text
        const textContainer = document.createElement('div');
        textContainer.style.whiteSpace = 'pre-wrap';  // Preserve whitespace and wrapping
        messageContent.appendChild(textContainer);
        
        // Stream each word with fade effect
        const words = content.split(' ').filter(word => word.trim() !== ''); // Filter out empty words
        for (let i = 0; i < words.length; i++) {
            const wordSpan = document.createElement('span');
            wordSpan.className = 'fade-in-text word-space';
            // Add space after word unless it's the last word
            wordSpan.textContent = words[i] + (i === words.length - 1 ? '' : ' '); // Add space conditionally
            textContainer.appendChild(wordSpan);
            await new Promise(resolve => setTimeout(resolve, 20));
        }
        
        // Add signature after all words are displayed
        await new Promise(resolve => setTimeout(resolve, 500));
        const signature = document.createElement('div');
        signature.innerHTML = '<br><br>Cordialement,<br>Claude Monet';
        signature.className = 'fade-in-text';
        messageContent.appendChild(signature);
    } else {
        messageContent.textContent = content;  // User input displayed directly
    }

    messagesDiv.scrollTop = messagesDiv.scrollHeight;  // Scroll to the bottom
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
        // Clean up the response to remove excessive whitespace or breaks
        const cleanedResponse = data.response.replace(/\n+/g, ' ').replace(/\s+/g, ' ').trim();
        // Display bot response with streaming effect
        await addMessage(cleanedResponse, false);
    } catch (error) {
        console.error('Error:', error);
        await addMessage("Je suis désolé, there seems to be an issue with our correspondence.", false);
    }
}

// Allow user to click send button or use Enter key
sendButton.addEventListener('click', handleSend);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        handleSend();
    }
});

// Add welcome message when the page loads
window.addEventListener('load', async () => {
    await addMessage("Bonjour! It is with great pleasure that I greet you today. My name is Claude Monet, and I am a painter, a lover of nature, and a captivated observer of the interplay of light. I hope that my words have given you a sense of my passion for painting, my love for nature, and my deep reverence for the interplay of light. I would be honored to converse with you, to share more of my thoughts and experiences. Please, do not hesitate to ask me anything about the impressionist era, inspiration behind my iconic paintings or my life as an artist.", false);
});
