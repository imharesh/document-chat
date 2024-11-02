// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';
const ENDPOINTS = {
    upload: `${API_BASE_URL}/documents/upload`,
    chat: `${API_BASE_URL}/chat/ask`
};

// Chat history
let chatHistory = [];

// DOM Elements
const fileInput = document.getElementById('fileInput');
const chatForm = document.getElementById('chatForm');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const fileList = document.getElementById('fileList');

// File Upload Handler
fileInput.addEventListener('change', async () => {
    const files = fileInput.files;
    
    if (files.length === 0) return;

    const formData = new FormData();
    for (let file of files) {
        formData.append('files', file);
    }

    try {
        const response = await fetch(ENDPOINTS.upload, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        if (response.ok) {
            // Add files to the list
            for (let file of files) {
                const fileItem = createFileItem(file.name);
                fileList.appendChild(fileItem);
            }
            showNotification(`Successfully uploaded ${data.processed_files} files`);
        } else {
            showNotification(`Upload failed: ${data.detail || 'Unknown error'}`);
        }
    } catch (error) {
        showNotification(`Error: ${error.message}`);
    }

    fileInput.value = ''; // Reset file input
});

// Create File Item Element
function createFileItem(filename) {
    const div = document.createElement('div');
    div.className = 'file-item';
    div.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path>
            <polyline points="13 2 13 9 20 9"></polyline>
        </svg>
        <span>${filename}</span>
    `;
    return div;
}

// Chat Form Handler
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = messageInput.value.trim();

    if (!message) return;

    // Add user message
    addMessage(message, 'user');
    messageInput.value = '';

    try {
        const response = await fetch(ENDPOINTS.chat, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: message,
                chat_history: chatHistory
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            addMessage(data.answer, 'bot');
        } else {
            addMessage('Error: ' + (data.detail || 'Unknown error'), 'bot');
        }
    } catch (error) {
        addMessage('Error: ' + error.message, 'bot');
    }
});

// Add Message to Chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Update chat history
    chatHistory.push({
        role: sender === 'user' ? 'user' : 'assistant',
        content: text
    });
}

// Show Notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.className = 'notification';
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Initial message
addMessage("Hello! You can upload PDF documents and ask questions about them.", 'bot');