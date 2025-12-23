import { defineStore } from 'pinia'
import { useRepo } from 'pinia-orm'
import apiClient from '@/setup/axios'
import { Session, SessionConfig, SessionResult } from '@/models'

export const useSessionStore = defineStore('session', {
  state: () => ({
    currentSessionId: null,
    currentConfigId: null,
    sessionWords: [],
    currentWordIndex: 0,
    answers: []
  }),

  getters: {
    currentSession: (state) => {
      if (!state.currentSessionId) return null
      return useRepo(Session).with('results', (query) => {
        query.with('translation')
      }).find(state.currentSessionId)
    },

    currentConfig: (state) => {
      if (!state.currentConfigId) return null
      return useRepo(SessionConfig).find(state.currentConfigId)
    },

    currentWord: (state) => {
      if (!state.sessionWords || state.currentWordIndex >= state.sessionWords.length) {
        return null
      }
      return state.sessionWords[state.currentWordIndex]
    },

    totalWords: (state) => state.sessionWords.length,
    
    isSessionComplete: (state) => state.currentWordIndex >= state.sessionWords.length,
    
    sessionResults: (state) => {
      if (!state.answers.length) return null
      
      const correctFirstTime = state.answers.filter(a => a.correct && a.attempts === 1)
      const failed = state.answers.filter(a => !a.correct || a.attempts > 1 || a.skipped)
      const successRate = (correctFirstTime.length / state.answers.length) * 100
      
      return {
        correctFirstTime,
        failed,
        successRate: Math.round(successRate),
        total: state.answers.length
      }
    }
  },

  actions: {
    async createSessionConfig(config) {
      const response = await apiClient.post('/sessions/config', {
        nativeLanguage: config.nativeLanguage,
        languageTested: config.languageTested,
        difficulty: config.difficulty,
        domain: config.domain,
        sessionType: config.sessionType
      })
      
      useRepo(SessionConfig).save(response.data)
      this.currentConfigId = response.data.id
      return response.data
    },

    async startSession(configId) {
      if (!this.currentConfig) {
        throw new Error('Config not found')
      }
      
      const response = await apiClient.post('/sessions/start', {
        configId: configId,
        sourceLangCode: this.currentConfig.nativeLanguage,
        targetLangCode: this.currentConfig.languageTested,
        domain: this.currentConfig.domain,
        difficulty: this.currentConfig.difficulty,
        sessionType: this.currentConfig.sessionType
      })
      
      // Save to ORM
      useRepo(Session).save(response.data)
      useRepo(SessionResult).save(response.data.results)
      
      this.currentSessionId = response.data.id
      this.sessionWords = response.data.results.map(r => ({
        ...r.translation,
        sessionResultId: r.id,
        attempts: 0,
        skipped: false
      }))
      this.currentWordIndex = 0
      this.answers = []
      
      return response.data
    },

    submitAnswer(userAnswer) {
      if (!this.currentWord) return
      
      const word = this.currentWord
      const isCorrect = userAnswer.toLowerCase().trim() === word.text.toLowerCase().trim()
      word.attempts++
      
      const existingAnswer = this.answers.find(a => a.translationId === word.id)
      
      if (existingAnswer) {
        // Word was shown again after failure
        existingAnswer.attempts++
        if (isCorrect) {
          existingAnswer.correct = true
          this.currentWordIndex++
        } else {
          // Move to end of list to try again
          const failedWord = this.sessionWords.splice(this.currentWordIndex, 1)[0]
          this.sessionWords.push(failedWord)
        }
      } else {
        // First attempt at this word
        this.answers.push({
          translationId: word.id,
          sessionResultId: word.sessionResultId,
          correct: isCorrect,
          attempts: 1,
          skipped: false,
          userAnswer
        })
        
        if (isCorrect) {
          this.currentWordIndex++
        } else {
          // Move to end of list to try again
          const failedWord = this.sessionWords.splice(this.currentWordIndex, 1)[0]
          this.sessionWords.push(failedWord)
        }
      }
    },

    skipWord() {
      if (!this.currentWord) return
      
      const word = this.currentWord
      word.skipped = true
      word.attempts++
      
      const existingAnswer = this.answers.find(a => a.translationId === word.id)
      
      if (!existingAnswer) {
        this.answers.push({
          translationId: word.id,
          sessionResultId: word.sessionResultId,
          correct: false,
          attempts: 1,
          skipped: true,
          userAnswer: null
        })
      }
      
      // Move to end to try again later
      const skippedWord = this.sessionWords.splice(this.currentWordIndex, 1)[0]
      this.sessionWords.push(skippedWord)
    },

    async completeSession() {
      const results = this.answers.map(a => ({
        translationId: a.translationId,
        correct: a.correct && a.attempts === 1 && !a.skipped
      }))
      
      const response = await apiClient.post(`/sessions/${this.currentSessionId}/submit`, results)
      useRepo(Session).save(response.data)
      
      return this.sessionResults
    },

    async fetchSessionHistory() {
      const response = await apiClient.get('/sessions/')
      useRepo(Session).save(response.data)
      return response.data
    },

    resetSession() {
      this.currentSessionId = null
      this.currentConfigId = null
      this.sessionWords = []
      this.currentWordIndex = 0
      this.answers = []
    }
  }
})


