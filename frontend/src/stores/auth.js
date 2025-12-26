import { defineStore } from 'pinia'
import apiClient from '@/setup/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token') || null,
    isAuthenticated: false,
    userLanguage: 'en'
  }),

  getters: {
    isLoggedIn: (state) => !!state.token && !!state.user,
    currentUser: (state) => state.user,
    getUserLanguage: (state) => state.userLanguage
  },

  actions: {
    async login(email, password) {
      const response = await apiClient.post('/api/v1/auth/login', {
        email,
        password
      })

      this.token = response.data.accessToken
      localStorage.setItem('access_token', this.token)
      
      await this.fetchUser()
    },

    async register(email, password, username) {
      await apiClient.post('/api/v1/auth/register', {
        email,
        password,
        full_name: username
      })
    },

    async fetchUser() {
      try {
        const response = await apiClient.get('/api/v1/auth/current-user')
        this.user = response.data
        this.isAuthenticated = true
      } catch (error) {
        this.logout()
        throw error
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('access_token')
    },

    async checkAuth() {
      if (this.token) {
        try {
          await this.fetchUser()
        } catch (error) {
          this.logout()
        }
      }
    },
    setUserLanguage(languageCode) {
      this.userLanguage = languageCode
    }
  }
})
