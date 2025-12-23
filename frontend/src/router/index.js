import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfileView.vue')
  },
  {
    path: '/session/:id',
    name: 'SessionActive',
    component: () => import('@/views/SessionView.vue'),
    props: true
  },
  {
    path: '/summary/:id',
    name: 'Summary',
    component: () => import('@/views/SummaryView.vue'),
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
