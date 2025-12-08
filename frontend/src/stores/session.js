import { defineStore } from 'pinia'
import apiClient from '@/setup/axios'
import { useRepo } from 'pinia-orm'
import { Session, SessionResult } from '../models'

export const useSessionStore = defineStore('session', {
  state: () => ({
    currentSessionId: null,
    loading: false,
    error: null
  }),

  getters: {
    currentSession: (state) => {
      if (!state.currentSessionId) return null
      return useRepo(Session).with('results', (query) => {
        query.with('word')
      }).find(state.currentSessionId)
    }
  },

  actions: {
    async startSession(config) {
      this.loading = true
      try {
        // Post to API
        const response = await apiClient.post('/sessions/start', config)
        const data = response.data

        // Save to ORM
        useRepo(Session).save(data)

        this.currentSessionId = data.id
        return data.id
      } catch (e) {
        console.error(e)
        this.error = e.message
        throw e
      } finally {
        this.loading = false
      }
    },

    async submitResults(results) {
      this.loading = true
      try {
        const response = await apiClient.post(`/sessions/${this.currentSessionId}/submit`, results)
        useRepo(Session).save(response.data)
        return response.data
      } catch (e) {
        this.error = e
      } finally {
        this.loading = false
      }
    }
  }
})
