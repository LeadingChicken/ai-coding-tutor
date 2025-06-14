<template>
  <div class="app-container">
    <!-- Navigation Bar -->
    <nav class="bg-white shadow-sm">
      <div class="w-full px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-2xl font-bold text-gray-800">AI Programming Tutor</h1>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <router-link
              to="/"
              class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
              :class="{ 'bg-blue-600': $route.path === '/' }"
            >
              Lí thuyết
            </router-link>
            <router-link
              to="/practice"
              class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
              :class="{ 'bg-blue-600': $route.path === '/practice' }"
            >
              Bài tập
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <router-view class="router-view"></router-view>
  </div>
</template>

<script setup lang="ts">
// No setup needed for now
</script>

<style>
/* Reset CSS */
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

body {
  background-color: #f3f4f6;
}

#app {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
}

.app-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  background-color: #f3f4f6;
}

nav {
  flex-shrink: 0;
  width: 100%;
  background-color: white;
  z-index: 10;
}

.router-view {
  flex: 1;
  width: 100%;
  overflow-y: auto;
}
</style>
