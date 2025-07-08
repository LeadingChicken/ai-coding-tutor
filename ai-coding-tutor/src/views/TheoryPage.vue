<template>
  <div class="theory-page">
    <div class="theory-content">
      <div v-if="loading" class="loading">Loading theory content...</div>
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      <div v-else class="markdown-content" v-html="renderedContent"></div>
    </div>
    <div class="chat-section">
      <TheoryChatBox :lesson-id="lessonId" />
    </div>
  </div>
</template>

<script>
import TheoryChatBox from '@/components/TheoryChatBox.vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/dracula.css'

export default {
  name: 'TheoryPage',
  components: {
    TheoryChatBox,
  },
  props: {
    lessonId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      content: '',
      loading: true,
      error: null,
    }
  },
  computed: {
    renderedContent() {
      return marked(this.content, {
        highlight: function (code, lang) {
          if (lang && hljs.getLanguage(lang)) {
            return hljs.highlight(code, { language: lang }).value
          }
          return hljs.highlightAuto(code).value
        },
      })
    },
  },
  async created() {
    try {
      const response = await fetch(`http://localhost:8000/api/theory/${this.lessonId}`)
      if (!response.ok) {
        throw new Error('Failed to load theory content')
      }
      const data = await response.json()
      this.content = data.content
    } catch (err) {
      this.error = err.message
    } finally {
      this.loading = false
    }
  },
}
</script>

<style scoped>
.theory-page {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 2rem;
  height: 100vh;
  padding: 2rem;
  background: #f8f9fa;
}

.theory-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.chat-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.loading,
.error {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #dc3545;
}

:deep(.markdown-content) {
  font-family: 'Inter', sans-serif;
  line-height: 1.6;
  color: #2c3e50;
}

:deep(.markdown-content h1) {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

:deep(.markdown-content h2) {
  font-size: 2rem;
  margin: 2rem 0 1rem;
  color: #2c3e50;
}

:deep(.markdown-content h3) {
  font-size: 1.5rem;
  margin: 1.5rem 0 1rem;
  color: #2c3e50;
}

:deep(.markdown-content p) {
  margin-bottom: 1rem;
}

:deep(.markdown-content pre) {
  background: #282a36;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
  overflow-x: auto;
}

:deep(.markdown-content code) {
  font-family: 'Fira Code', monospace;
  font-size: 0.9rem;
}

:deep(.markdown-content ul) {
  margin: 1rem 0;
  padding-left: 2rem;
}

:deep(.markdown-content li) {
  margin-bottom: 0.5rem;
}

@media (max-width: 1024px) {
  .theory-page {
    grid-template-columns: 1fr;
  }

  .chat-section {
    height: 500px;
  }
}
</style>
