<template>
  <div class="code-editor">
    <div class="toolbar">
      <div class="toolbar-buttons">
        <button class="editor-btn test-btn" @click="testCode">Test code</button>
        <button class="editor-btn run-btn" @click="runCode">Chạy code</button>
      </div>
    </div>
    <div class="editor-container" ref="editorContainer"></div>
  </div>
</template>

<script>
import * as monaco from 'monaco-editor'
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'

export default {
  name: 'CodeEditor',
  props: {
    templateFunction: {
      type: String,
      default: '# Viết code của bạn ở đây\n',
    },
  },
  emits: ['code-change', 'run-code', 'test-code'],
  setup(props, { emit }) {
    let editor = null
    const editorContainer = ref(null)

    onMounted(() => {
      // Khởi tạo Monaco Editor
      editor = monaco.editor.create(editorContainer.value, {
        value: props.templateFunction,
        language: 'python',
        theme: 'vs-dark',
        automaticLayout: true,
        minimap: {
          enabled: false,
        },
        fontSize: 14,
        lineNumbers: 'on',
        scrollBeyondLastLine: false,
        wordWrap: 'on',
        wrappingIndent: 'same',
        tabSize: 4,
        insertSpaces: true,
        folding: true,
        renderLineHighlight: 'all',
        scrollbar: {
          vertical: 'visible',
          horizontal: 'visible',
          useShadows: false,
          verticalScrollbarSize: 10,
          horizontalScrollbarSize: 10,
        },
      })

      // Lắng nghe sự thay đổi của code
      editor.onDidChangeModelContent(() => {
        emit('code-change', editor.getValue())
      })
    })

    // Watch for changes in templateFunction prop
    watch(
      () => props.templateFunction,
      (newValue) => {
        if (editor && newValue) {
          // Chỉ cập nhật nếu editor trống hoặc chứa template mặc định
          const currentValue = editor.getValue().trim()
          if (!currentValue || currentValue === '# Viết code của bạn ở đây') {
            editor.setValue(newValue)
            // Di chuyển con trỏ đến cuối file
            const lastLineNumber = editor.getModel().getLineCount()
            const lastLineLength = editor.getModel().getLineLength(lastLineNumber)
            editor.setPosition({
              lineNumber: lastLineNumber,
              column: lastLineLength + 1,
            })
            editor.focus()
          }
        }
      },
      { immediate: true },
    )

    onBeforeUnmount(() => {
      if (editor) {
        editor.dispose()
      }
    })

    const runCode = () => {
      if (editor) {
        emit('run-code', editor.getValue())
      }
    }

    const testCode = () => {
      if (editor) {
        emit('test-code', editor.getValue())
      }
    }

    return {
      editorContainer,
      runCode,
      testCode,
    }
  },
}
</script>

<style scoped>
.code-editor {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #1e1e1e;
  border-radius: 0.5rem;
  overflow: hidden;
}

.toolbar {
  flex: 0 0 auto;
  padding: 0.5rem;
  background-color: #252526;
  border-bottom: 1px solid #333;
  display: flex;
  justify-content: flex-end;
}

.toolbar-buttons {
  display: flex;
  gap: 0.5rem;
}

.editor-btn {
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.run-btn {
  background-color: #4f46e5;
}

.run-btn:hover {
  background-color: #4338ca;
}

.test-btn {
  background-color: #059669;
}

.test-btn:hover {
  background-color: #047857;
}

.editor-container {
  flex: 1;
  overflow: hidden;
}
</style>
