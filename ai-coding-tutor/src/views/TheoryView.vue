<template>
  <div class="theory-container">
    <div class="theory-content">
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
      <div
        v-else-if="error"
        class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded"
      >
        {{ error }}
      </div>
      <div v-else class="theory-messages">
        <!-- Chat Messages -->
        <div class="messages-container" ref="chatContainer">
          <div v-for="(message, index) in displayedMessages" :key="index" class="message-item">
            <div class="message-content">
              <h3 v-if="message.title" class="message-title">
                {{ message.title }}
              </h3>
              <div class="message-body markdown-body" v-html="formatContent(message.content)"></div>
            </div>
          </div>
        </div>

        <!-- Continue Button -->
        <div class="button-container">
          <button
            v-if="currentIndex < theoryContent.length - 1"
            @click="showNextContent"
            class="continue-button"
          >
            Tiếp tục
          </button>
          <div v-else class="completion-message">
            Bạn đã hoàn thành phần lý thuyết! Hãy chuyển sang phần Bài tập để kiểm tra kiến thức.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { marked } from 'marked'
import Prism from 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'
import 'prismjs/components/prism-python'
import 'prismjs/plugins/line-numbers/prism-line-numbers.css'
import 'prismjs/plugins/line-numbers/prism-line-numbers'
import 'prismjs/plugins/toolbar/prism-toolbar.css'
import 'prismjs/plugins/toolbar/prism-toolbar'
import 'prismjs/plugins/copy-to-clipboard/prism-copy-to-clipboard'

// Configure marked with Prism
marked.setOptions({
  highlight: function (code: string, lang: string) {
    if (Prism.languages[lang]) {
      return Prism.highlight(code, Prism.languages[lang], lang)
    }
    return code
  },
  breaks: true,
  gfm: true,
})

interface TheoryItem {
  title: string
  content: string
}

interface DisplayMessage {
  title?: string
  content: string
  isSystem: boolean
}

// Hardcoded theory content
const theoryContent: TheoryItem[] = [
  {
    title: 'Python cơ bản',
    content:
      'Python là một ngôn ngữ lập trình cao cấp, dễ học và phù hợp cho cả người mới học và người có kinh nghiệm.',
  },
  {
    title: 'Kiểu dữ liệu và biến trong Python',
    content:
      'Trong Python, bạn có thể lưu trữ dữ liệu trong các biến. Các kiểu dữ liệu chính là:\n\n- Số (int, float)\n- Chuỗi (text)\n- Boolean (True/False)\n- Danh sách (collections)\n\nVí dụ:\n```python\nage = 25          # số nguyên\nname = "John"     # chuỗi\nis_student = True # boolean\n```',
  },
  {
    title: 'Cấu trúc điều kiện trong Python',
    content:
      'Python sử dụng cấu trúc điều kiện để xác định các khối mã được thực thi. Dưới đây là cách hoạt động của các câu lệnh if:\n\n```python\nif condition:\n    # làm gì đó\nelif another_condition:\n    # làm gì đó khác\nelse:\n    # làm gì đó mặc định\n```',
  },
  {
    title: 'Vòng lặp trong Python',
    content:
      'Python có hai loại vòng lặp chính:\n\n1. Vòng lặp for:\n```python\nfor i in range(5):\n    print(i)\n```\n\n2. Vòng lặp while:\n```python\nwhile condition:\n    # làm gì đó\n```',
  },
  {
    title: 'Hàm trong Python',
    content:
      'Hàm giúp chúng ta tổ chức và tái sử dụng mã:\n\n```python\ndef greet(name):\n    return f"Hello, {name}!"\n\n# Sử dụng hàm\nresult = greet("Alice")\nprint(result)  # Outputs: Hello, Alice!\n```',
  },
]

const loading = ref(true)
const error = ref('')
const currentIndex = ref(-1)
const displayedMessages = ref<DisplayMessage[]>([])
const chatContainer = ref<HTMLElement | null>(null)

const formatContent = (content: string): string => {
  const html = marked(content) as string
  return html.replace(
    /<pre><code class="language-(\w+)">/g,
    '<pre class="line-numbers"><code class="language-$1">',
  )
}

const highlightCode = () => {
  nextTick(() => {
    Prism.highlightAll()
  })
}

const showNextContent = () => {
  if (currentIndex.value < theoryContent.length - 1) {
    currentIndex.value++
    const item = theoryContent[currentIndex.value]
    displayedMessages.value.push({
      title: item.title,
      content: item.content,
      isSystem: true,
    })

    nextTick(() => {
      highlightCode()
      if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight
      }
    })
  }
}

onMounted(() => {
  loading.value = false
  showNextContent()

  // Set up observer for dynamic content
  const observer = new MutationObserver(() => {
    highlightCode()
  })

  if (chatContainer.value) {
    observer.observe(chatContainer.value, {
      childList: true,
      subtree: true,
    })
  }
})
</script>

<style>
/* Container styles */
.theory-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f3f4f6;
  width: 100%;
  height: 100%;
}

.theory-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background: white;
}

.theory-messages {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.message-item {
  margin-bottom: 1rem;
}

.message-content {
  background-color: #e4e7e7;
  border-radius: 0.5rem;
  padding: 1.25rem;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.message-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
}

/* Code block styles */
pre[class*='language-'] {
  background: #282c34 !important;
  border-radius: 4px !important;
  margin: 0.75rem 0 !important;
  padding: 0.75rem !important;
  overflow: auto !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
}

code[class*='language-'] {
  font-family: 'JetBrains Mono', 'Fira Code', Consolas, 'Courier New', monospace !important;
  font-size: 0.875rem !important;
  line-height: 1.4 !important;
  text-shadow: none !important;
}

/* Markdown content */
.markdown-body {
  color: #24292e;
  line-height: 1.5;
}

.markdown-body p {
  margin: 0.5rem 0;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.markdown-body ul,
.markdown-body ol {
  margin: 0.25rem 0;
  padding-left: 1rem;
}

.markdown-body li {
  margin: 0.125rem 0;
  line-height: 1.4;
}

.markdown-body li > p {
  margin: 0;
}

.markdown-body li + li {
  margin-top: 0.125rem;
}

/* Nested lists */
.markdown-body li > ul,
.markdown-body li > ol {
  margin: 0.125rem 0;
  padding-left: 1rem;
}

/* Adjust spacing for paragraphs inside list items */
.markdown-body li > p + p {
  margin-top: 0.25rem;
}

/* Adjust spacing between list and other elements */
.markdown-body p + ul,
.markdown-body p + ol,
.markdown-body ul + p,
.markdown-body ol + p {
  margin-top: 0.5rem;
}

/* Line Numbers */
.line-numbers .line-numbers-rows {
  border-right: 1px solid #404040 !important;
  padding: 0 0.5em 0 0 !important;
}

.line-numbers-rows > span:before {
  color: #666 !important;
  padding-right: 0.75rem !important;
}

/* Copy Button */
div.code-toolbar > .toolbar {
  opacity: 1 !important;
  top: 0.25rem !important;
  right: 0.25rem !important;
}

div.code-toolbar > .toolbar > .toolbar-item > button {
  background: #363842 !important;
  color: #c5c8c6 !important;
  padding: 0.2em 0.5em !important;
  border-radius: 0.25rem !important;
  font-size: 0.75rem !important;
  transition: all 0.2s !important;
}

div.code-toolbar > .toolbar > .toolbar-item > button:hover {
  background: #4a4d5a !important;
  color: #ffffff !important;
}

/* Button container */
.button-container {
  padding: 1rem;
  background-color: white;
  border-top: 1px solid #e5e7eb;
}

.continue-button {
  width: 100%;
  background-color: #3b82f6;
  color: white;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
  font-size: 1rem;
}

.continue-button:hover {
  background-color: #2563eb;
}

.completion-message {
  text-align: center;
  color: #6b7280;
  padding: 0.75rem;
  font-size: 1rem;
}

/* Keep the syntax highlighting colors */
/* ... rest of your token color styles ... */
</style>
