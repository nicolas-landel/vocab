import { defineStore } from 'pinia'
import { useRepo } from 'pinia-orm'
import apiClient from '@/setup/axios'
import { Translation, Language, Domain } from '@/models'

export const useVocabularyStore = defineStore('vocabulary', {
  state: () => ({
    selectedLanguage: null,
    selectedDomains: [],
    selectedDifficulties: [],
    showKnownWords: false
  }),

  getters: {
    translations: () => {
      return useRepo(Translation).with('language').with('masterWord').all()
    },
    
    languages: () => {
      return useRepo(Language).all()
    },
    
    domains: () => {
      return useRepo(Domain).all()
    },
    
    difficulties: () => {
      return ['EASY', 'MEDIUM', 'HARD']
    },
    getLanguageName: (state) => (code) => {
      const languages = useRepo(Language).all()
      const lang = languages.find(l => l.code === code)
      return lang ? lang.name : code
    }
  },

  actions: {
    async fetchLanguages() {
      const response = await apiClient.get('/api/v1/config/languages')
      useRepo(Language).save(response.data)
      return response.data
    },

    async fetchDomains() {
      const response = await apiClient.get('/api/v1/config/domains')
      useRepo(Domain).save(response.data)
      return response.data
    },

    async fetchDifficulties() {
      const response = await apiClient.get('/api/v1/config/difficulties')
      return response.data
    },

    async fetchVocabulary(filters) {
      const params = {
        languageCode: filters.languageCode,
        domains: filters.domains?.join(','),
        difficulties: filters.difficulties?.join(','),
        showKnown: filters.showKnown
      }
      
      const response = await apiClient.get('/api/vocabulary/list', { params })
      useRepo(Translation).save(response.data)
      return response.data
    },

    async toggleWordKnown(translationId, isKnown) {
      await apiClient.post(`/api/vocabulary/translations/${translationId}/known`, {
        isKnown: isKnown
      })
      
      useRepo(Translation).where('id', translationId).update({ isKnown: isKnown })
    },

    async getTranslationDetails(translationId) {
      const response = await apiClient.get(`/api/vocabulary/translations/${translationId}`)
      useRepo(Translation).save(response.data)
      return response.data
    }
  }
})


