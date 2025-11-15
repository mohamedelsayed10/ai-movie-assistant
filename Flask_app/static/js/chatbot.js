let sessionId = generateUUID();
let currentMode = 'text';
let mediaRecorder;
let audioChunks = [];
let logsData = []; // Store all logs

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Mode toggle
document.querySelectorAll('.mode-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        currentMode = this.dataset.mode;
        
        if (currentMode === 'text') {
            document.getElementById('textInputArea').style.display = 'flex';
            document.getElementById('voiceInputArea').style.display = 'none';
        } else {
            document.getElementById('textInputArea').style.display = 'none';
            document.getElementById('voiceInputArea').style.display = 'flex';
        }
    });
});

// Logs Modal
function toggleLogs() {
    const modal = document.getElementById('logsModal');
    modal.classList.toggle('active');
    if (modal.classList.contains('active')) {
        renderLogs();
    }
}

function renderLogs() {
    const logsBody = document.getElementById('logsBody');
    
    if (logsData.length === 0) {
        logsBody.innerHTML = '<p class="no-logs">No logs yet. Send a message to see the full response data.</p>';
        return;
    }
    
    logsBody.innerHTML = '';
    
    // Display logs in reverse order (newest first)
    logsData.slice().reverse().forEach((log, index) => {
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        
        const logId = `log-${logsData.length - index - 1}`;
        
        // Check if messages have pretty_print output
        let logContent = '';
        if (log.fullResponse && log.fullResponse.messages) {
            log.fullResponse.messages.forEach((msg, msgIndex) => {
                if (msg.pretty_print) {
                    // Use pretty_print output
                    logContent += `\n${'='.repeat(60)}\nMessage ${msgIndex + 1}: ${msg.type || 'Unknown'}\n${'='.repeat(60)}\n`;
                    logContent += msg.pretty_print;
                } else {
                    // Fallback to JSON
                    logContent += `\n${'='.repeat(60)}\nMessage ${msgIndex + 1}: ${msg.type || 'Unknown'}\n${'='.repeat(60)}\n`;
                    logContent += JSON.stringify(msg, null, 2);
                }
            });
        } else {
            logContent = JSON.stringify(log.fullResponse, null, 2);
        }
        
        logEntry.innerHTML = `
            <div class="log-entry-header">
                <span class="log-timestamp">${log.timestamp}</span>
                <button class="copy-log-btn" onclick="copyLog('${logId}')">📋 Copy</button>
            </div>
            <div class="log-user-message">
                <strong>User:</strong> ${escapeHtml(log.userMessage)}
            </div>
            <div class="log-response-preview">
                <strong>Bot Response:</strong> ${escapeHtml(log.response.substring(0, 150))}${log.response.length > 150 ? '...' : ''}
            </div>
            <div class="log-full-data" id="${logId}">
                <pre>${escapeHtml(logContent)}</pre>
            </div>
        `;
        
        logsBody.appendChild(logEntry);
    });
}

function copyLog(logId) {
    const logElement = document.getElementById(logId);
    const text = logElement.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '✓ Copied!';
        btn.classList.add('copied');
        
        setTimeout(() => {
            btn.textContent = originalText;
            btn.classList.remove('copied');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function addLog(userMessage, response, fullResponse) {
    const timestamp = new Date().toLocaleString();
    logsData.push({
        timestamp,
        userMessage,
        response,
        fullResponse
    });
}

// Text chat
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    addMessage(message, 'user');
    input.value = '';
    
    showTypingIndicator();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message, 
                session_id: sessionId,
                debug: true  // Always request debug mode to get full response
            })
        });
        
        const data = await response.json();
        hideTypingIndicator();
        
        if (data.error) {
            addMessage('Error: ' + data.error, 'bot');
        } else {
            addMessage(data.response, 'bot', true);
            sessionId = data.session_id;
            
            // Add to logs
            if (data.full_response) {
                addLog(message, stripHtml(data.response), data.full_response);
            }
        }
    } catch (error) {
        hideTypingIndicator();
        addMessage('Error: ' + error.message, 'bot');
    }
}

function stripHtml(html) {
    const tmp = document.createElement('div');
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || '';
}

// Voice recording
async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            await sendVoiceMessage(audioBlob);
            stream.getTracks().forEach(track => track.stop());
        };
        
        mediaRecorder.start();
        document.getElementById('recordBtn').style.display = 'none';
        document.getElementById('stopBtn').style.display = 'flex';
        document.getElementById('recordingIndicator').style.display = 'block';
    } catch (error) {
        alert('Error accessing microphone: ' + error.message);
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        document.getElementById('recordBtn').style.display = 'flex';
        document.getElementById('stopBtn').style.display = 'none';
        document.getElementById('recordingIndicator').style.display = 'none';
    }
}

async function sendVoiceMessage(audioBlob) {
    showTypingIndicator();
    
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');
    formData.append('session_id', sessionId);
    formData.append('debug', 'true');  // Enable debug mode for logs
    
    try {
        const response = await fetch('/chat/voice', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        hideTypingIndicator();
        
        if (data.error) {
            addMessage('Error: ' + data.error, 'bot');
        } else {
            addMessage(data.transcription, 'user');
            addMessage(data.response, 'bot', true);
            sessionId = data.session_id;
            
            // Add to logs if full response is available
            if (data.full_response) {
                addLog(data.transcription, stripHtml(data.response), data.full_response);
            }
        }
    } catch (error) {
        hideTypingIndicator();
        addMessage('Error: ' + error.message, 'bot');
    }
}

function addMessage(text, sender, includeAudio = false) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = text; // Use innerHTML to support HTML formatted responses
    
    if (includeAudio && sender === 'bot') {
        const audioBtn = document.createElement('button');
        audioBtn.textContent = '🔊 Play';
        audioBtn.style.cssText = 'margin-top: 8px; padding: 5px 10px; border: none; background: #667eea; color: white; border-radius: 5px; cursor: pointer;';
        audioBtn.onclick = () => playAudio(stripHtml(text));
        contentDiv.appendChild(document.createElement('br'));
        contentDiv.appendChild(audioBtn);
    }
    
    messageDiv.appendChild(contentDiv);
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function playAudio(text) {
    try {
        const response = await fetch('/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
    } catch (error) {
        console.error('Error playing audio:', error);
    }
}

function showTypingIndicator() {
    const messagesDiv = document.getElementById('chatMessages');
    const indicator = document.createElement('div');
    indicator.className = 'message bot';
    indicator.id = 'typingIndicator';
    indicator.innerHTML = '<div class="typing-indicator" style="display: block;"><span></span><span></span><span></span></div>';
    messagesDiv.appendChild(indicator);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

async function newChat() {
    try {
        const response = await fetch('/new-session', { method: 'POST' });
        const data = await response.json();
        sessionId = data.session_id;
        
        // Clear logs for new session
        logsData = [];
        
        document.getElementById('chatMessages').innerHTML = `
            <div class="message bot">
                <div class="message-content">
                    Hello! I'm your AI assistant. How can I help you today?
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error creating new session:', error);
    }
}

// Close logs modal when clicking outside
document.getElementById('logsModal').addEventListener('click', function(e) {
    if (e.target === this) {
        toggleLogs();
    }
});

// Enter key to send
document.getElementById('messageInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});