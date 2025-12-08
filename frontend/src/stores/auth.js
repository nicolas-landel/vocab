import { defineStore } from 'pinia'
import { authAPI } from '../api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    loading: true,
    token: localStorage.getItem('access_token') || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user
  },

  actions: {
    async login(email, password) {
      try {
        const data = await authAPI.login(email, password)
        this.token = data.access_token
        localStorage.setItem('access_token', data.access_token)
        await this.fetchUser()
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Login failed' 
        }
      }
    },

    async register(email, password) {
      try {
        await authAPI.register(email, password)
        // Auto-login after registration
        return await this.login(email, password)
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Registration failed' 
        }
      }
    },

    async fetchUser() {
      try {
        this.user = await authAPI.getMe()
        this.loading = false
      } catch (error) {
        this.logout()
        this.loading = false
      }
    },

    async logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('access_token')
      return { success: true }
    },

    async initAuth() {
      if (this.token) {
        await this.fetchUser()
      } else {
        this.loading = false
      }
    }
  }
})
