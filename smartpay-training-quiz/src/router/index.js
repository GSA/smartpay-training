import { createRouter, createWebHistory } from 'vue-router'
import UserHome from '@/views/UserHome.vue'
import Loginless from '@/components/loginless/Loginless.vue'
import NotFound from '@/views/NotFound.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
        path: '/',
        name: 'home',
        component: Loginless
    },
    {
        path: '/start-quiz/:token',
        name: "userhome",
        component: UserHome,
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
