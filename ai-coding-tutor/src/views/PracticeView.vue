<template>
  <div class="practice-container">
    <div class="app">
      <div class="left-panel">
        <ExercisePanel
          :description="exercise.description"
          :example="exercise.example"
          :explanation="exercise.explanation"
          :is-generating="isGenerating"
          @generate="generateExercise"
        />
      </div>
      <div class="center-panel">
        <CodeEditor
          ref="codeEditor"
          :template-function="exercise.function"
          @code-change="handleCodeChange"
          @run-code="handleRunCode"
          @test-code="handleTestCode"
        />
        <Terminal
          ref="terminal"
          :output="terminalOutput"
          :activeTab="activeTab"
          @tab-change="handleTabChange"
        />
      </div>
    </div>
    <ChatBox
      ref="chatBox"
      :code="currentCode"
      :terminal-output="terminalOutput"
      :exercise="exercise"
    />
    <div class="loading-overlay" :class="{ show: isGenerating }">
      <div class="loading-content">
        <div class="spinner"></div>
        <div class="loading-text">Đang tạo bài tập mới...</div>
      </div>
    </div>
  </div>
</template>

<script>
import ExercisePanel from '../components/ExercisePanel.vue'
import CodeEditor from '../components/CodeEditor.vue'
import Terminal from '../components/Terminal.vue'
import ChatBox from '../components/ChatBox.vue'
import { ref, onMounted } from 'vue'

export default {
  name: 'PracticeView',
  components: {
    ExercisePanel,
    CodeEditor,
    Terminal,
    ChatBox,
  },
  setup() {
    const codeEditor = ref(null)
    const terminal = ref(null)
    const chatBox = ref(null)
    const currentCode = ref('')
    const terminalOutput = ref('')
    const activeTab = ref('output')
    const isGenerating = ref(false)
    const exercise = ref({
      description: '',
      example: '',
      explanation: '',
      function: '',
      unit_test: '',
    })

    const handleCodeChange = (code) => {
      currentCode.value = code
    }

    const handleRunCode = async (code) => {
      try {
        // Chạy code
        const response = await fetch('http://localhost:8000/run_code', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ code }),
        })

        if (!response.ok) {
          throw new Error('Network response was not ok')
        }

        const data = await response.json()
        terminalOutput.value = data.output
        activeTab.value = 'output'

        // Sau khi chạy code xong, gửi request để agent đánh giá
        const agentResponse = await fetch('http://localhost:8000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: 'Hãy đánh giá code của học viên vừa chạy',
            code: code,
            terminal_output: data.output,
            exercise: exercise.value,
            history: [], // Không cần history vì đây là đánh giá độc lập
            is_code_evaluation: true, // Thêm flag để sử dụng prompt đánh giá code
          }),
        })

        if (!agentResponse.ok) {
          throw new Error('Network response was not ok')
        }

        const agentData = await agentResponse.json()

        // Thêm phản hồi của agent vào chat
        if (chatBox.value && chatBox.value.addMessage) {
          await chatBox.value.addMessage({
            role: 'assistant',
            content: agentData.response,
          })
        }
      } catch (error) {
        console.error('Error:', error)
        terminalOutput.value = 'Error running code: ' + error.message
      }
    }

    const handleTestCode = async (code) => {
      try {
        // Chạy unit test trước
        const testResponse = await fetch('http://localhost:8000/run_unit_tests', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            code: code,
            unit_test: exercise.value.unit_test,
          }),
        })

        if (!testResponse.ok) {
          throw new Error('Network response was not ok')
        }

        const testData = await testResponse.json()

        // Hiển thị kết quả test trong terminal và chuyển sang tab test
        terminalOutput.value = testData.test_output
        activeTab.value = 'test'

        // Đợi một chút để người dùng có thể xem kết quả test
        await new Promise((resolve) => setTimeout(resolve, 2000))
      } catch (error) {
        console.error('Error:', error)
        terminalOutput.value = 'Error testing code: ' + error.message
      }
    }

    const handleTabChange = (tab) => {
      activeTab.value = tab
    }

    const generateExercise = async () => {
      isGenerating.value = true
      try {
        const response = await fetch('http://localhost:8000/generate_exercise', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        })

        if (!response.ok) {
          throw new Error('Network response was not ok')
        }

        const data = await response.json()
        exercise.value = {
          description: data.description,
          example: data.example,
          explanation: data.explanation,
          function: data.function,
          unit_test: data.unit_test,
        }
      } catch (error) {
        console.error('Error:', error)
      } finally {
        isGenerating.value = false
      }
    }

    // Generate initial exercise
    onMounted(() => {
      generateExercise()
    })

    return {
      codeEditor,
      terminal,
      chatBox,
      currentCode,
      terminalOutput,
      activeTab,
      isGenerating,
      exercise,
      handleCodeChange,
      handleRunCode,
      handleTestCode,
      handleTabChange,
      generateExercise,
    }
  },
}
</script>

<style>
.practice-container {
  position: relative;
  min-height: calc(100vh - 64px); /* Subtract header height */
  background-color: #f3f4f6;
  display: flex;
  flex-direction: column;
}

.app {
  flex: 1;
  display: grid;
  grid-template-columns: minmax(300px, 1fr) 2fr;
  gap: 0.75rem;
  padding: 0.75rem;
  height: calc(100vh - 64px); /* Subtract header height */
  overflow: hidden;
}

.left-panel,
.center-panel {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow:
    0 1px 3px 0 rgba(0, 0, 0, 0.1),
    0 1px 2px 0 rgba(0, 0, 0, 0.06);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.center-panel {
  display: grid;
  grid-template-rows: minmax(0, 2fr) minmax(0, 1fr);
  gap: 0.75rem;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 50;
}

.loading-overlay.show {
  opacity: 1;
  visibility: visible;
}

.loading-content {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  text-align: center;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 1rem;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #4f46e5;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  color: #1f2937;
  font-size: 0.875rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .app {
    grid-template-columns: 1fr;
    padding: 0.5rem;
  }
  .left-panel {
    display: none;
  }
}
</style>
