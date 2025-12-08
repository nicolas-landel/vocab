import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // Mock auth for now as per plan (User 1)
  const isAuthenticated = ref(true)
  const user = ref({ id: 1, email: 'test@example.com' })

  function login() {
    isAuthenticated.value = true
  }

  return { isAuthenticated, user, login }
})
