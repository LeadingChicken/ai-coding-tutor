<template>
  <div class="exercise-panel">
    <div class="header">
      <h2>Bài tập</h2>
      <button class="generate-btn" @click="$emit('generate')" :disabled="isGenerating">
        <span v-if="!isGenerating">Tạo bài tập mới</span>
        <span v-else>Đang tạo...</span>
      </button>
    </div>

    <div class="content">
      <div class="section">
        <h3>Mô tả</h3>
        <div class="description markdown-content" v-html="renderedDescription"></div>
      </div>

      <div class="section">
        <h3>Ví dụ</h3>
        <div class="example markdown-content" v-html="renderedExample"></div>
      </div>

      <div class="section">
        <h3>Giải thích</h3>
        <div class="explanation markdown-content" v-html="renderedExplanation"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

// Configure marked to use highlight.js
marked.setOptions({
  highlight: function (code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (err) {}
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true,
  gfm: true,
})

// Override highlight.js theme
const style = document.createElement('style')
style.textContent = `
  .hljs {
    background: #282a36;
    color: #f8f8f2;
  }
  /* Keywords như def, class, return */
  .hljs-keyword,
  .hljs-selector-tag,
  .hljs-literal,
  .hljs-section,
  .hljs-link {
    color: #ff79c6;
  }
  /* Tên hàm */
  .hljs-function .hljs-title,
  .hljs-title.function_ {
    color: #50fa7b;
  }
  /* Strings */
  .hljs-string {
    color: #f1fa8c;
  }
  /* Numbers */
  .hljs-number {
    color: #bd93f9;
  }
  /* Built-in functions */
  .hljs-built_in {
    color: #8be9fd;
  }
  /* Comments */
  .hljs-comment {
    color: #6272a4;
  }
  /* Property names trong dictionary */
  .hljs-attr {
    color: #50fa7b;
  }
  /* Dấu ngoặc và các ký tự đặc biệt */
  .hljs-punctuation {
    color: #f8f8f2;
  }
  /* Boolean values */
  .hljs-literal {
    color: #bd93f9;
  }
  /* Class names */
  .hljs-class .hljs-title {
    color: #50fa7b;
  }
  /* Function parameters */
  .hljs-params {
    color: #f8f8f2;
  }
  /* Operators */
  .hljs-operator {
    color: #ff79c6;
  }
`
document.head.appendChild(style)

export default {
  name: 'ExercisePanel',
  props: {
    description: {
      type: String,
      default: '',
    },
    example: {
      type: String,
      default: '',
    },
    explanation: {
      type: String,
      default: '',
    },
    isGenerating: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    renderedDescription() {
      return this.renderMarkdown(this.description)
    },
    renderedExample() {
      // Xử lý nội dung
      let processedExample = this.example
        // Loại bỏ ```python và ``` nếu có
        .replace(/^```python\n?/, '')
        .replace(/```$/, '')
        // Tách thành các dòng
        .split('\n')
        // Xử lý indent cho mỗi dòng
        .map((line) => line.trimStart())
        // Nối lại thành chuỗi
        .join('\n')
        .trim()

      // Bọc lại trong code block Python
      return this.renderMarkdown('```python\n' + processedExample + '\n```')
    },
    renderedExplanation() {
      return this.renderMarkdown(this.explanation)
    },
  },
  methods: {
    renderMarkdown(text) {
      if (!text) return ''
      return marked(text)
    },
  },
  emits: ['generate'],
}
</script>

<style scoped>
.exercise-panel {
  height: 100%;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.header {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #1f2937;
}

.generate-btn {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.generate-btn:hover {
  background-color: #4338ca;
}

.generate-btn:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}

.section {
  margin-bottom: 2rem;
  background-color: #f8fafc;
  padding: 1.25rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

.section:last-child {
  margin-bottom: 0;
}

.section h3 {
  margin: 0 0 0.75rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #3b82f6;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
}

/* Markdown content styling */
.markdown-content {
  color: #1f2937;
  line-height: 1.5;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.markdown-content :deep(p) {
  margin: 1em 0;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 1.5em;
  margin: 1em 0;
}

.markdown-content :deep(li) {
  margin: 0.5em 0;
}

.markdown-content :deep(pre) {
  background-color: #282a36;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
  margin: 1em 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #44475a;
}

.markdown-content :deep(code) {
  font-family:
    'Fira Code', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono',
    'Courier New', monospace;
  font-size: 0.875rem;
  padding: 0.2em 0.4em;
  background-color: #282a36;
  color: #f8f8f2;
  border-radius: 0.25em;
}

.markdown-content :deep(pre code) {
  padding: 0;
  background-color: transparent;
  color: #f8f8f2;
  font-family:
    'Fira Code', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono',
    'Courier New', monospace;
  line-height: 1.5;
  tab-size: 2;
}

.markdown-content :deep(blockquote) {
  border-left: 4px solid #e5e7eb;
  padding-left: 1em;
  margin: 1em 0;
  color: #4b5563;
}

.markdown-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 0.5em;
  text-align: left;
}

.markdown-content :deep(th) {
  background-color: #f3f4f6;
}
</style>
