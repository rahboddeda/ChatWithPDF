document.addEventListener('DOMContentLoaded', () => {
  const chatBox = document.getElementById('chat-box');
  const input = document.getElementById('user-input');
  const sendBtn = document.getElementById('send-btn');
  const fileInput = document.getElementById('file-input');

  function renderMarkdown(text) {
    const html = window.marked.parse(text);
    const wrapper = document.createElement('div');
    wrapper.innerHTML = html;
    wrapper.querySelectorAll('pre code').forEach(block => {
      hljs.highlightElement(block);
    });
    return wrapper.innerHTML;
  }

  function addMessage(content, sender) {
    const msg = document.createElement('div');
    msg.className = `message ${sender}`;
    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    bubble.innerHTML = sender === 'bot' ? renderMarkdown(content) : content;
    msg.appendChild(bubble);
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function showTyping(callback) {
    const typing = document.createElement('div');
    typing.className = 'message bot';
    typing.innerHTML = '<div class="bubble typing"><span></span><span></span><span></span></div>';
    chatBox.appendChild(typing);
    chatBox.scrollTop = chatBox.scrollHeight;
    setTimeout(() => {
      typing.remove();
      callback();
    }, 1500);
  }

  sendBtn.addEventListener('click', () => {
    const question = input.value.trim();
    if (!question) return;

    addMessage(question, 'user');
    input.value = '';
    showTyping(() => {
      fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      })
        .then(res => res.json().then(data => ({ status: res.status, body: data })))
        .then(({ status, body }) => {
          if (status === 200) {
            addMessage(body.answer, 'bot');
          } else {
            addMessage("⚠️ " + (body.error || "Something went wrong."), 'bot');
          }
        })
        .catch(err => {
          console.error("Fetch failed:", err);
          addMessage("⚠️ Error fetching response.", 'bot');
        });
    });
  });

  fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', { method: 'POST', body: formData })
      .then(res => res.json())
      .then(() => {
        addMessage("✅ File uploaded! You can now ask questions.", 'bot');
        input.disabled = false;
        sendBtn.disabled = false;
      })
      .catch(() => {
        addMessage("❌ Upload failed. Try again.", 'bot');
      });
  });
});
