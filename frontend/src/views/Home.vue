<template>
  <VContainer fluid>
    <VSkeletonLoader v-if="loading" type="article" :loading="loading" />

    <VWindow v-else :model-value="activeTab">
      <VWindowItem value="session">
        <SessionConfigForm @start-session="handleStartSession" />
      </VWindowItem>
      <VWindowItem value="vocabulary">
        <VocabularyView />
      </VWindowItem>
    </VWindow>
  </VContainer>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import SessionConfigForm from '@/components/SessionConfigForm.vue'
import VocabularyView from '@/components/VocabularyView.vue'
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSessionStore } from '@/stores/session'
import { useVocabularyStore } from '@/stores/vocabulary'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()

const sessionStore = useSessionStore()
const vocabularyStore = useVocabularyStore()
const authStore = useAuthStore()

const router = useRouter()
const route = useRoute()

const loading = ref(true)
const activeTab = computed(() => route.query.tab || 'session')

const handleStartSession = (sessionId) => {
  router.push({ name: 'SessionActive', params: { id: sessionId } })
}

onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([
      vocabularyStore.fetchLanguages(),
      vocabularyStore.fetchDomains(),
      
    ])
  
  } catch (error) {
    console.error(t('errors.failedToLoadOptions'), error)
  } finally {
    loading.value = false
  }
})


</script>

