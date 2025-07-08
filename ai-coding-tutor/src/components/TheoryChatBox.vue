<template>
  <div :class="['floating-chat', { expanded: isExpanded }]">
    <div class="chat-header" @click="toggleChat">
      <div class="header-content">
        <div class="avatar">AI</div>
        <span class="title">AI Tutor</span>
        <div class="status-dot"></div>
        <div v-if="!isExpanded && unreadCount > 0" class="unread-badge">{{ unreadCount }}</div>
      </div>
      <div class="header-actions">
        <button v-if="isExpanded" class="action-btn minimize" @click.stop="toggleChat">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
      </div>
    </div>
    <div v-show="isExpanded" class="chat-container">
      <div class="chat-messages" ref="messagesContainer">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.role === 'user' ? 'user-message' : 'tutor-message']"
        >
          <div class="message-content" v-html="renderMarkdown(message.content)"></div>
        </div>
      </div>
      <div class="chat-input">
        <textarea
          v-model="newMessage"
          @keydown.enter.prevent="sendMessage"
          placeholder="Nhập câu hỏi về lý thuyết..."
          rows="1"
        ></textarea>
        <button @click="sendMessage" :disabled="!newMessage.trim() || isLoading" class="send-btn">
          <svg
            v-if="!isLoading"
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M22 2L11 13"></path>
            <path d="M22 2L15 22L11 13L2 9L22 2z"></path>
          </svg>
          <span v-else>...</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, nextTick, toRefs } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/lib/languages/python'

// Configure marked to use highlight.js
marked.setOptions({
  highlight: function (code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  },
})

export default {
  name: 'TheoryChatBox',
  props: {
    theoryContext: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const { theoryContext } = toRefs(props)
    const messages = ref([])
    const newMessage = ref('')
    const isLoading = ref(false)
    const messagesContainer = ref(null)
    const isExpanded = ref(false)
    const unreadCount = ref(0)

    const toggleChat = () => {
      isExpanded.value = !isExpanded.value
      if (isExpanded.value) {
        unreadCount.value = 0
        nextTick(() => {
          scrollToBottom()
        })
      }
    }

    const scrollToBottom = async () => {
      await nextTick()
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }

    const addMessage = async (message) => {
      let content = message.content
      if (typeof content === 'object') {
        try {
          if (Array.isArray(content)) {
            content = content.join('\n')
          } else {
            content = Object.values(content).join('\n')
          }
        } catch (e) {
          content = String(content)
        }
      }
      messages.value.push({
        role: message.role,
        content: content,
      })
      if (message.role === 'assistant' && !isExpanded.value) {
        unreadCount.value++
      }
      await scrollToBottom()
    }

    const sendMessage = async () => {
      if (!newMessage.value.trim() || isLoading.value) return
      const messageContent = newMessage.value
      newMessage.value = ''
      isLoading.value = true
      await addMessage({ role: 'user', content: messageContent })
      try {
        const response = await fetch('http://localhost:8000/theory_chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: messageContent,
            history: messages.value.slice(-10),
            theory_context: theoryContext.value,
          }),
        })
        if (!response.ok) throw new Error('Network response was not ok')
        const data = await response.json()
        await addMessage({ role: 'assistant', content: data.response })
      } catch (error) {
        await addMessage({
          role: 'assistant',
          content: 'Xin lỗi, đã có lỗi xảy ra khi gửi tin nhắn. Vui lòng thử lại.',
        })
      } finally {
        isLoading.value = false
      }
    }

    const renderMarkdown = (content) => marked.parse(content)

    // Lời chào ban đầu
    addMessage({
      role: 'assistant',
      content:
        'Xin chào! Tôi là AI tutor. Bạn có thể hỏi bất cứ điều gì liên quan đến phần lý thuyết Python đang học.',
    })

    return {
      messages,
      newMessage,
      isLoading,
      isExpanded,
      unreadCount,
      messagesContainer,
      sendMessage,
      addMessage,
      toggleChat,
      renderMarkdown,
    }
  },
}
</script>

<style scoped>
.floating-chat {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 600px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: all 0.3s ease;
  overflow: hidden;
}
.floating-chat:not(.expanded) {
  width: 350px;
  height: 48px;
  cursor: pointer;
}
.floating-chat:not(.expanded):hover {
  background-color: #f5f5f5;
}
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: white;
  border-bottom: 1px solid #e5e7eb;
  height: 48px;
}
.header-content {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
}
.avatar {
  width: 32px;
  height: 32px;
  background-color: #4f46e5;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}
.title {
  font-weight: 500;
  color: #1f2937;
}
.status-dot {
  width: 8px;
  height: 8px;
  background-color: #10b981;
  border-radius: 50%;
  margin-left: 4px;
}
.unread-badge {
  position: absolute;
  top: -6px;
  right: -10px;
  background-color: #ef4444;
  color: white;
  border-radius: 12px;
  padding: 2px 6px;
  font-size: 12px;
  font-weight: 600;
  min-width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}
.header-actions {
  display: flex;
  gap: 8px;
}
.action-btn {
  background: none;
  border: none;
  padding: 4px;
  color: #6b7280;
  cursor: pointer;
  border-radius: 4px;
}
.action-btn:hover {
  background-color: #f3f4f6;
  color: #374151;
}
.chat-container {
  height: 500px;
  display: flex;
  flex-direction: column;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.message {
  margin-bottom: 0.5rem;
  max-width: 85%;
  display: flex;
  flex-direction: column;
}
.user-message {
  margin-left: auto;
  background-color: #3b82f6;
  border: none;
  border-radius: 18px 18px 4px 18px;
  padding: 12px 16px;
  align-self: flex-end;
}
.tutor-message {
  margin-right: auto;
  background-color: #f3f4f6;
  border: none;
  border-radius: 18px 18px 18px 4px;
  padding: 12px 16px;
  align-self: flex-start;
}
.message-content {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.6;
  min-width: 0;
  width: 100%;
  padding: 0;
}

/* Dracula theme for code blocks */
.message-content pre {
  background-color: #282a36;
  border-radius: 6px;
  padding: 1rem;
  margin: 0.5rem 0;
  overflow-x: auto;
}

.message-content code {
  font-family: 'Fira Code', monospace;
  font-size: 0.9em;
}

.message-content pre code {
  color: #f8f8f2;
}

/* Python syntax highlighting */
.message-content .hljs-keyword {
  color: #ff79c6;
}

.message-content .hljs-string {
  color: #f1fa8c;
}

.message-content .hljs-number {
  color: #bd93f9;
}

.message-content .hljs-comment {
  color: #6272a4;
}

.message-content .hljs-function {
  color: #50fa7b;
}

.message-content .hljs-class {
  color: #8be9fd;
}

.message-content .hljs-built_in {
  color: #ffb86c;
}

.message-content .hljs-operator {
  color: #ff79c6;
}

.message-content .hljs-variable {
  color: #f8f8f2;
}

.message-content .hljs-params {
  color: #f8f8f2;
}

.user-message .message-content,
.user-message .message-content * {
  background: transparent !important;
  color: white !important;
}
.tutor-message .message-content {
  color: #1f2937;
}
.chat-input {
  padding: 12px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
  align-items: flex-end;
}
.chat-input textarea {
  flex: 1;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 8px 12px;
  resize: none;
  font-size: 14px;
  line-height: 1.5;
  max-height: 120px;
  outline: none;
  transition: border-color 0.2s;
  color: #1f2937;
}
.chat-input textarea::placeholder {
  color: #1f2937;
  opacity: 0.8;
}
.chat-input textarea:focus {
  border-color: #4f46e5;
}
.send-btn {
  background-color: #4f46e5;
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}
.send-btn:hover:not(:disabled) {
  background-color: #4338ca;
}
.send-btn:disabled {
  background-color: #e5e7eb;
  cursor: not-allowed;
}
.chat-messages::-webkit-scrollbar {
  width: 6px;
}
.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}
.chat-messages::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 3px;
}
.chat-messages::-webkit-scrollbar-thumb:hover {
  background-color: #94a3b8;
}
</style>
