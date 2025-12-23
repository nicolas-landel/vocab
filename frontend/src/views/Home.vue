<template>
  <v-container fluid>
    <v-tabs v-model="activeTab" bg-color="transparent" color="primary" class="mb-6">
      <v-tab value="session">Session</v-tab>
      <v-tab value="vocabulary">Vocabulary</v-tab>
    </v-tabs>

    <v-window v-model="activeTab">
      <!-- Session Tab -->
      <v-window-item value="session">
        <session-config-form @start-session="handleStartSession" />
      </v-window-item>

      <!-- Vocabulary Tab -->
      <v-window-item value="vocabulary">
        <vocabulary-view />
      </v-window-item>
    </v-window>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import SessionConfigForm from '@/components/SessionConfigForm.vue'
import VocabularyView from '@/components/VocabularyView.vue'

const router = useRouter()
const activeTab = ref('session')

const handleStartSession = (sessionId) => {
  router.push({ name: 'SessionActive', params: { id: sessionId } })
}
</script>

