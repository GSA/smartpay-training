import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import QuizStart from '../views/QuizStart.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/start-quiz/:token',
        name: "quizstart",
        component: QuizStart,
        props: true
    }
  ]
})

export default router
