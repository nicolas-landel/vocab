import apiClient from './client'

export const authAPI = {
  async register(email, password) {
    const response = await apiClient.post('/api/v1/auth/register', {
      email,
      password
    })
    return response.data
  },

  async login(email, password) {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await apiClient.post('/api/v1/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    return response.data
  },

  async getMe() {
    const response = await apiClient.get('/api/v1/auth/me')
    return response.data
  }
}
