import { createRouter, createWebHashHistory } from 'vue-router'
import UserHome from '@/views/UserHome.vue'
import Index from '@/views/Index.vue'
import Loginless from '@/components/loginless/Loginless.vue'
import NotFound from '@/views/NotFound.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
        path: '/',
        name: 'index',
        component: Index
    },
    {
        path: '/get-started/',
        name: 'getstarted',
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
