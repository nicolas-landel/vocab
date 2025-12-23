<template>
  <VContainer fluid>
    <VWindow :model-value="activeTab">
      <!-- Session Tab -->
      <VWindowItem value="session">
        <session-config-form @start-session="handleStartSession" />
      </VWindowItem>

      <!-- Vocabulary Tab -->
      <VWindowItem value="vocabulary">
        <vocabulary-view />
      </VWindowItem>
    </VWindow>
  </VContainer>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import SessionConfigForm from '@/components/SessionConfigForm.vue'
import VocabularyView from '@/components/VocabularyView.vue'

const router = useRouter()
const route = useRoute()
const activeTab = computed(() => route.query.tab || 'session')

const handleStartSession = (sessionId) => {
  router.push({ name: 'SessionActive', params: { id: sessionId } })
}
</script>

