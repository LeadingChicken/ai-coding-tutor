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
          <div class="message-content">{{ message.content }}</div>
        </div>
      </div>
      <div class="chat-input">
        <textarea
          v-model="newMessage"
          @keydown.enter.prevent="sendMessage"
          placeholder="Nhập câu hỏi của bạn..."
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
import { ref, onMounted, nextTick, toRefs } from 'vue'

export default {
  name: 'ChatBox',
  props: {
    code: {
      type: String,
      default: '',
    },
    terminalOutput: {
      type: String,
      default: '',
    },
    exercise: {
      type: Object,
      default: () => ({}),
    },
  },
  setup(props) {
    const { code, terminalOutput, exercise } = toRefs(props)
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
          console.error('Error processing content:', e)
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

      await addMessage({
        role: 'user',
        content: messageContent,
      })

      try {
        const response = await fetch('http://localhost:8000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: messageContent,
            code: code.value,
            terminal_output: terminalOutput.value,
            history: messages.value.slice(-10),
            exercise: exercise.value,
          }),
        })

        if (!response.ok) {
          throw new Error('Network response was not ok')
        }

        const data = await response.json()

        await addMessage({
          role: 'assistant',
          content: data.response,
        })
      } catch (error) {
        console.error('Error:', error)
        await addMessage({
          role: 'assistant',
          content: 'Xin lỗi, đã có lỗi xảy ra khi gửi tin nhắn. Vui lòng thử lại.',
        })
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      addMessage({
        role: 'assistant',
        content: `Xin chào! Tôi là AI tutor. Tôi có thể giúp bạn:

- Review và giải thích code của bạn
- Gợi ý cách làm bài tập
- Giải đáp thắc mắc về lập trình
- Phân tích lỗi và đề xuất cách sửa

Hãy đặt câu hỏi cho tôi!`,
      })
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
    }
  },
}
</script>

<style>
.floating-chat {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 450px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: all 0.3s ease;
  overflow: hidden;
}

.floating-chat:not(.expanded) {
  width: 300px;
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
  padding: 1rem;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}

.message {
  margin-bottom: 1rem;
  max-width: 85%;
}

.user-message {
  margin-left: auto;
  background-color: #4f46e5;
  border-radius: 18px 18px 4px 18px;
  padding: 8px 12px;
}

.tutor-message {
  margin-right: auto;
  background-color: #f3f4f6;
  border-radius: 18px 18px 18px 4px;
  padding: 8px 12px;
}

.message-content {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.5;
  color: #1f2937;
}

.user-message .message-content {
  color: white;
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

/* Scrollbar styles */
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
