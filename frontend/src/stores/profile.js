import { defineStore } from 'pinia'
import apiClient from '@/setup/axios'
import { UserLanguage } from '@/models'
import { useRepo } from "pinia-orm";

export const useProfileStore = defineStore('profile', {
  state: () => ({
    profile: {
      id: null,
      email: '',
      fullName: '',
      nativeLanguage: null,
      isActive: false,
      oauthProvider: null,
      pictureUrl: null,
      createdAt: null,
      updatedAt: null
    },
  }),

  getters: {
    getUserLanguage: () => {
      return useRepo(UserLanguage).query().all()
    },

    availableLanguages: (state) => (allLanguages) => {
      const userLangCodes = useRepo(UserLanguage).query().all().map(l => l.languageCode)
      return allLanguages.filter(lang => 
        !userLangCodes.includes(lang.code) && lang.code !== state.profile.nativeLanguage
      )
    },
    
    getLanguageName: () => (code, languages) => {
      const lang = languages.find(l => l.code === code)
      return lang ? lang.name : code
    }
  },

  actions: {
    async fetchProfile() {
      const response = await apiClient.get('/api/v1/profile/')
      this.profile = response.data
      if (response.data.languages.length > 0) {
        useRepo(UserLanguage).save(response.data.languages)
      }
    },

    async updateProfile(updates) {
      const response = await apiClient.patch('/api/v1/profile/', updates)
      this.profile = response.data
      return response.data
    },

    async fetchUserLanguages() {
      const response = await apiClient.get('/api/v1/profile/languages')
      useRepo(UserLanguage).save(response.data)
    },

    async addLanguage(languageData) {
      const response = await apiClient.post('/api/v1/profile/languages', languageData)
      useRepo(UserLanguage).save(response.data)
      return response.data
    },

    async updateLanguage(languageCode, updates) {
      const response = await apiClient.patch(
        `/api/v1/profile/languages/${languageCode}`,
        updates
      )
      useRepo(UserLanguage).save(response.data)
      return response.data
    },

    async deleteLanguage(languageCode) {
      await apiClient.delete(`/api/v1/profile/languages/${languageCode}`)
      useRepo(UserLanguage).where('languageCode', languageCode).delete()
    },
  }
})
