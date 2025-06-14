import { createRouter, createWebHistory } from 'vue-router'
import TheoryView from '../views/TheoryView.vue'
import PracticeView from '../views/PracticeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'theory',
      component: TheoryView,
    },
    {
      path: '/practice',
      name: 'practice',
      component: PracticeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router
