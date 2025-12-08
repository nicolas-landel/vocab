import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'Config',
    component: () => import('../views/ConfigView.vue')
  },
  {
    path: '/session/:id',
    name: 'Session',
    component: () => import('../views/SessionView.vue'),
    props: true
  },
  {
    path: '/summary/:id',
    name: 'Summary',
    component: () => import('../views/SummaryView.vue'),
    props: true
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfileView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
