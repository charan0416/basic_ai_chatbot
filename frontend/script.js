// File: frontend/script.js
document.addEventListener('DOMContentLoaded', () => {
    const chatbox = document.getElementById('chatbox');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    // IMPORTANT: Make sure this URL matches exactly where your Flask backend is running
    // Use 127.0.0.1 instead of localhost if you encounter issues sometimes
    const API_URL = 'http://127.0.0.1:5001/chat';

    /**
     * Appends a message to the chatbox UI.
     * @param {string} text The message content.
     * @param {'user' | 'bot'} sender Indicates who sent the message.
     */
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');

        if (sender === 'user') {
            messageDiv.classList.add('user-message');
        } else {
            messageDiv.classList.add('bot-message');
            // Check if the bot's message indicates an error for special styling
            const lowerText = text.toLowerCase();
            if (lowerText.includes('sorry') || lowerText.includes('error') || lowerText.includes('problem') || lowerText.includes('unable') || lowerText.includes('could not find')) {
                messageDiv.classList.add('error-message');
            }
        }

        // Basic sanitation (replace potential HTML tags - more robust sanitation needed for production)
        // For this example, just setting textContent is safer than innerHTML
        messageDiv.textContent = text;

        chatbox.appendChild(messageDiv);

        // Scroll to the bottom of the chatbox smoothly
        chatbox.scrollTo({ top: chatbox.scrollHeight, behavior: 'smooth' });
    }

    /**
     * Sends the user's message to the backend and displays the response.
     */
    async function sendMessage() {
        const messageText = userInput.value.trim();
        if (!messageText) {
            return; // Don't send empty messages
        }

        // Display user message immediately
        addMessage(messageText, 'user');
        userInput.value = ''; // Clear input field
        sendButton.disabled = true; // Disable button while waiting

        try {
            console.log(`Sending message to ${API_URL}: ${messageText}`);
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Add other headers if required by your backend CORS config
                },
                body: JSON.stringify({ message: messageText }),
            });

            console.log('Received response status:', response.status);

            if (!response.ok) {
                // Try to get error details from response body if possible
                let errorMsg = `Error: ${response.status} ${response.statusText}`;
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.error || errorData.message || JSON.stringify(errorData);
                    console.error('API Error Response Body:', errorData);
                } catch (e) {
                    // Response body wasn't JSON or couldn't be parsed
                    console.error('Could not parse error response body:', e);
                }
                 addMessage(`Sorry, there was a problem reaching the server. (${errorMsg})`, 'bot');

            } else {
                const data = await response.json();
                console.log('Received data:', data);
                 if (data && data.response) {
                    addMessage(data.response, 'bot');
                 } else {
                    console.error('Invalid response format from server:', data);
                    addMessage('Sorry, I received an unexpected response from the server.', 'bot');
                 }
            }

        } catch (error) {
            // Handle network errors (fetch failed completely)
            console.error('Fetch Error:', error);
            addMessage('Sorry, I could not connect to the chatbot server. Please ensure it is running and accessible.', 'bot');
        } finally {
             sendButton.disabled = false; // Re-enable button
             userInput.focus(); // Keep focus on input for easy typing
        }
    }

    // --- Event Listeners ---
    sendButton.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (event) => {
        // Send message if Enter key is pressed (and Shift key is not pressed)
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent default Enter behavior (like adding a newline)
            sendMessage();
        }
    });

     // Initial focus on the input field when the page loads
     userInput.focus();

     console.log("Chatbot UI Initialized. Ready to send messages to:", API_URL);
});