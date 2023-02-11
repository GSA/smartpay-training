import { createRouter, createWebHistory } from 'vue-router'
import QuizStart from '../components/QuizStart.vue'
import StartInput from '../components/StartInput.vue'
import NotFound from '../views/NotFound.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
        path: '/',
        name: 'home',
        component: StartInput
    },
    {
        path: '/start-quiz/:token',
        name: "quizstart",
        component: QuizStart,
        props: true
    },
    { 
        path: '/:pathMatch(.*)*', 
        name: 'NotFound', 
        component: NotFound 
    },
  ]
})

export default router
