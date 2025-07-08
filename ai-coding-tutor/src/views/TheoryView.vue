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
            <div class="message-wrapper">
              <div class="avatar">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"
                  />
                </svg>
              </div>
              <div class="message-content">
                <h3 v-if="message.title" class="message-title">
                  {{ message.title }}
                </h3>
                <div
                  class="message-body markdown-body"
                  v-html="formatContent(message.content)"
                ></div>
              </div>
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
          <button v-else @click="goToPractice" class="practice-button">Chuyển đến Bài tập</button>
        </div>
      </div>
    </div>
    <TheoryChatBox
      :theory-context="
        displayedMessages.map((m) => (m.title ? m.title + '\n' : '') + m.content).join('\n\n')
      "
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/lib/languages/python'
import TheoryChatBox from '../components/TheoryChatBox.vue'
import { useRoute, useRouter } from 'vue-router'

// Configure marked
marked.setOptions({
  breaks: true,
  gfm: true,
})

// Add custom renderer for code blocks
const renderer = new marked.Renderer()
renderer.code = ({ text, lang }: { text: string; lang?: string }) => {
  const validLanguage = lang && hljs.getLanguage(lang) ? lang : 'plaintext'
  const highlighted = hljs.highlight(text, { language: validLanguage }).value
  return `<pre><code class="hljs language-${validLanguage}">${highlighted}</code></pre>`
}
marked.use({ renderer })

interface TheoryItem {
  title: string
  content: string
}

interface DisplayMessage {
  title?: string
  content: string
  isSystem: boolean
}

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const error = ref('')
const currentIndex = ref(-1)
const displayedMessages = ref<DisplayMessage[]>([])
const chatContainer = ref<HTMLElement | null>(null)
const theoryContent = ref<TheoryItem[]>([])

const formatContent = (content: string): string => {
  return marked(content) as string
}

const highlightCode = () => {
  nextTick(() => {
    document.querySelectorAll('pre code').forEach((block) => {
      hljs.highlightElement(block as HTMLElement)
    })
  })
}

const showNextContent = () => {
  if (currentIndex.value < theoryContent.value.length - 1) {
    currentIndex.value++
    const item = theoryContent.value[currentIndex.value]
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

const fetchTheoryContent = async () => {
  try {
    const lessonId = route.params.lessonId
    const response = await fetch(`http://localhost:8000/api/theory/${lessonId}`)
    if (!response.ok) {
      throw new Error('Failed to load theory content')
    }
    const data = await response.json()
    theoryContent.value = data.content
    loading.value = false
    showNextContent()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'An error occurred'
    loading.value = false
  }
}

const goToPractice = () => {
  router.push(`/practice/${route.params.lessonId}`)
}

onMounted(() => {
  fetchTheoryContent()

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

.message-wrapper {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.avatar {
  width: 40px;
  height: 40px;
  min-width: 40px;
  background-color: #3b82f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.avatar svg {
  width: 24px;
  height: 24px;
}

.message-content {
  background-color: #e4e7e7;
  border-radius: 0.5rem;
  padding: 1.25rem;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  flex: 1;
}

.message-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
}

/* Code block styles */
pre {
  background: #282a36 !important;
  border-radius: 4px !important;
  margin: 0.75rem 0 !important;
  padding: 0.75rem !important;
  overflow: auto !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
}

code {
  font-family: 'JetBrains Mono', 'Fira Code', Consolas, 'Courier New', monospace !important;
  font-size: 0.875rem !important;
  line-height: 1.4 !important;
  text-shadow: none !important;
}

/* Dracula theme colors */
.hljs {
  color: #f8f8f2;
  background: #282a36;
}

.hljs-keyword,
.hljs-selector-tag,
.hljs-literal,
.hljs-section,
.hljs-link {
  color: #ff79c6;
}

.hljs-function .hljs-keyword {
  color: #ff79c6;
}

.hljs-string,
.hljs-title,
.hljs-name,
.hljs-type,
.hljs-symbol,
.hljs-bullet,
.hljs-addition,
.hljs-variable,
.hljs-template-tag,
.hljs-template-variable {
  color: #f1fa8c;
}

.hljs-comment,
.hljs-quote,
.hljs-deletion {
  color: #6272a4;
}

.hljs-keyword,
.hljs-selector-tag,
.hljs-literal,
.hljs-title,
.hljs-section,
.hljs-doctag,
.hljs-type,
.hljs-name,
.hljs-strong {
  font-weight: bold;
}

.hljs-literal,
.hljs-number,
.hljs-params {
  color: #bd93f9;
}

.hljs-emphasis {
  font-style: italic;
}

.hljs-strong {
  font-weight: bold;
}

.hljs-link {
  text-decoration: underline;
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
  padding-left: 1.5rem;
  list-style-type: disc;
}

.markdown-body ul {
  list-style-position: inside;
}

.markdown-body li {
  margin: 0.1rem 0;
  line-height: 1.3;
  padding-left: 0;
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

/* Table styles */
.markdown-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.9rem;
}

.markdown-body table th,
.markdown-body table td {
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  text-align: left;
}

.markdown-body table th {
  background-color: #f3f4f6;
  font-weight: 600;
  color: #1f2937;
}

.markdown-body table tr:nth-child(even) {
  background-color: #f9fafb;
}

.markdown-body table tr:hover {
  background-color: #f3f4f6;
}

.markdown-body table code {
  background-color: #f1f5f9;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-size: 0.85em;
  color: #0f172a;
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
  display: flex;
  justify-content: center;
}

.continue-button {
  width: auto;
  min-width: 120px;
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

.practice-button {
  width: auto;
  min-width: 120px;
  background-color: #10b981;
  color: white;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
  font-size: 1rem;
}

.practice-button:hover {
  background-color: #059669;
}
</style>
