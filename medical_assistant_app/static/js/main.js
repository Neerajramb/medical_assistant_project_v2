document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const typingIndicator = document.getElementById('typing-indicator');

    // Function to append a message to the chat box with an animation
    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'assistant-message');
        
        // Simple text parsing for newlines
        const sanitizedMessage = message.replace(/</g, "<").replace(/>/g, ">");
        messageDiv.innerHTML = `<p>${sanitizedMessage.replace(/\n/g, '<br>')}</p>`;
        
        chatBox.appendChild(messageDiv);
        scrollToBottom();
    }

    // Function to scroll to the bottom of the chat box
    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Function to show/hide the typing indicator
    const showTypingIndicator = (show) => {
        typingIndicator.classList.toggle('hidden', !show);
        if (show) {
            scrollToBottom();
        }
    };
    
    // Function to fetch and display chat history on page load
    // medical_assistant_app/static/js/main.js

    async function loadInitialData() {
    showTypingIndicator(true);
    try {
        // Fetch history and the welcome message at the same time for efficiency
        const [historyResponse, welcomeResponse] = await Promise.all([
            fetch('/api/history/'),
            fetch('/api/welcome/')
        ]);

        if (!historyResponse.ok || !welcomeResponse.ok) {
            throw new Error('Failed to load initial chat data.');
        }

        const historyData = await historyResponse.json();
        const welcomeData = await welcomeResponse.json();

        chatBox.innerHTML = ''; // Clear the chat box

        // 1. Display the persistent, saved chat history
        historyData.history.forEach(msg => {
            appendMessage(msg.sender, msg.message);
        });

        // 2. Display the special, one-time welcome message
        if (welcomeData.welcome_message) {
            appendMessage('assistant', welcomeData.welcome_message);
        }

        // A slight delay to ensure the DOM is updated before scrolling
        setTimeout(scrollToBottom, 100);

        } catch (error) {
            console.error('Error loading initial data:', error);
            appendMessage('assistant', 'Error: Could not load the chat.');
        } finally {
            showTypingIndicator(false);
        }
    }

    // Function to send a message to the backend
    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') {
            return;
        }

        // Add user message to UI immediately
        appendMessage('user', message);
        userInput.value = '';
        userInput.focus();

        // Disable input and show typing indicator
        sendButton.disabled = true;
        userInput.disabled = true;
        showTypingIndicator(true);

        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ response: `Server error: ${response.status}` }));
                throw new Error(errorData.response || 'An error occurred.');
            }

            const data = await response.json();
            // Hide typing indicator before showing the new message
            showTypingIndicator(false);
            appendMessage('assistant', data.response);

        } catch (error) {
            console.error('Error sending message:', error);
            showTypingIndicator(false);
            appendMessage('assistant', `Sorry, an error occurred: ${error.message}`);
        } finally {
            // Re-enable input
            sendButton.disabled = false;
            userInput.disabled = false;
            userInput.focus();
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent new line on enter
            sendMessage();
        }
    });

    // Initial load
    loadInitialData();
});