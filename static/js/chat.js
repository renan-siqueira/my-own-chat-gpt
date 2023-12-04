document.addEventListener('DOMContentLoaded', function() {
    const askForm = document.querySelector('#ask-form');
    const clearChatButton = document.getElementById('clear-chat');
    const messageArea = document.getElementById('message-area');
    
    askForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const questionInput = document.querySelector('input[name="question"]');
        const languageSelect = document.querySelector('select[name="language"]');
        const question = questionInput.value.trim();
        const language = languageSelect.value;

        if (question === "") return;

        const userMessageDiv = document.createElement('div');
        userMessageDiv.className = 'message user-message';
        userMessageDiv.textContent = question;
        messageArea.appendChild(userMessageDiv);

        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'message bot-message typing-indicator';
        typingIndicator.innerHTML = '<em>Typing</em><span>.</span><span>.</span><span>.</span>';
        messageArea.appendChild(typingIndicator);

        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ 'question': question, 'language': language })
        })
        .then(response => response.json())
        .then(data => {
            typingIndicator.remove();
            const botMessageDiv = document.createElement('div');
            botMessageDiv.className = 'message bot-message';
            botMessageDiv.textContent = data.answer;
            messageArea.appendChild(botMessageDiv);
            messageArea.scrollTop = messageArea.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
            typingIndicator.innerHTML = '<em>An error has occurred.</em>';
        });

        questionInput.value = '';
    });

    clearChatButton.addEventListener('click', function() {
        fetch('/clear_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => {
            if (response.ok) {
                messageArea.innerHTML = '';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});