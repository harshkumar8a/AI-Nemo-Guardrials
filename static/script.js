function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const inputElement = document.getElementById('userInput');
    const messageText = inputElement.value.trim();
    
    if (!messageText) return;

    // 1. Display User Message on UI
    appendMessage(messageText, 'user-message');
    inputElement.value = '';

    // 2. Add a temporary loading bubble
    const loadingId = appendMessage('Calculating...', 'bot-message');

    try {
        // 3. Post to FastAPI Endpoint
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: messageText })
        });

        const data = await response.json();
        
        // Remove loading state
        document.getElementById(loadingId).remove();

        // 4. Render output depending on Guardrail state
        const styleClass = data.status === 'blocked' ? 'blocked-message' : 'bot-message';
        appendMessage(data.reply, styleClass);

    } catch (error) {
        document.getElementById(loadingId).remove();
        appendMessage('Connection error. Failed to reach the calculation server.', 'blocked-message');
    }
}

function appendMessage(text, className) {
    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    const uniqueId = 'msg-' + Math.random().toString(36).substr(2, 9);
    
    messageDiv.id = uniqueId;
    messageDiv.className = `message ${className}`;
    messageDiv.innerText = text;
    
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to latest message
    
    return uniqueId;
}
