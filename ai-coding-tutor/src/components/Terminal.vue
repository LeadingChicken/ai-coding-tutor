<template>
  <div class="terminal">
    <div class="tabs">
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'output' }"
        @click="$emit('tab-change', 'output')"
      >
        Output
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'test' }"
        @click="$emit('tab-change', 'test')"
      >
        Test
      </button>
    </div>
    <div class="output-container">
      <pre><code>{{ output }}</code></pre>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Terminal',
  props: {
    output: {
      type: String,
      default: '',
    },
    activeTab: {
      type: String,
      default: 'output',
    },
  },
  emits: ['tab-change'],
}
</script>

<style scoped>
.terminal {
  height: 100%;
  background-color: #1e1e1e;
  border-radius: 0.5rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.tabs {
  flex: 0 0 auto;
  display: flex;
  gap: 0.25rem;
  padding: 0.5rem;
  background-color: #252526;
  border-bottom: 1px solid #333;
}

.tab-btn {
  background: none;
  border: none;
  color: #9ca3af;
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  background-color: #2d2d2d;
  color: #e5e7eb;
}

.tab-btn.active {
  background-color: #323232;
  color: white;
}

.output-container {
  flex: 1;
  padding: 1rem;
  overflow: auto;
}

pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

code {
  font-family:
    ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New',
    monospace;
  font-size: 0.875rem;
  color: #e5e7eb;
}

.success {
  color: #34d399;
}

.error {
  color: #f87171;
}
</style>
