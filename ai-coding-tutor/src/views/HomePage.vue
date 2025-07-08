<template>
  <div class="home-page">
    <div class="header">
      <h1>Lập trình Python cơ bản</h1>
      <p>Học lập trình Python cơ bản với các bài học tương tác với AI</p>
    </div>

    <div class="lessons-grid">
      <div
        v-for="lesson in lessons"
        :key="lesson.id"
        class="lesson-card"
        @click="navigateToLesson(lesson.id)"
      >
        <div class="lesson-icon">
          <i :class="lesson.icon"></i>
        </div>
        <div class="lesson-content">
          <h2>{{ lesson.title }}</h2>
          <p>{{ lesson.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      lessons: [
        {
          id: 'list',
          title: 'Python Lists',
          // Icon số 1
          icon: 'fas fa-list',
        },
        {
          id: 'set',
          title: 'Python Sets',
          icon: 'fas fa-object-group',
        },
        {
          id: 'dict',
          title: 'Python Dictionaries',
          icon: 'fas fa-book',
        },
      ],
    }
  },
  methods: {
    navigateToLesson(lessonId) {
      this.$router.push(`/theory/${lessonId}`)
    },
  },
}
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.header p {
  font-size: 1.2rem;
  color: #666;
}

.lessons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.lesson-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  cursor: pointer;
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
}

.lesson-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
}

.lesson-icon {
  background: #f8f9fa;
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.lesson-icon i {
  font-size: 1.8rem;
  color: #3498db;
}

.lesson-content h2 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.lesson-content p {
  color: #666;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .home-page {
    padding: 1rem;
  }

  .header h1 {
    font-size: 2rem;
  }

  .lessons-grid {
    grid-template-columns: 1fr;
  }
}
</style>
