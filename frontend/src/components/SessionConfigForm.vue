<template>
  <v-card max-width="800" class="mx-auto">
    <v-card-title class="text-h5">Configure Your Session</v-card-title>
    <v-card-text>
      <v-form ref="formRef" @submit.prevent="startSession">
        <v-row>
          <v-col cols="12" md="6">
            <v-select
              v-model="config.languageTested"
              :items="languages"
              item-title="name"
              item-value="code"
              label="Language to Test"
              variant="outlined"
              :rules="[v => !!v || 'Language is required']"
            ></v-select>
          </v-col>

          <v-col cols="12" md="6">
            <v-select
              v-model="config.domain"
              :items="domains"
              item-title="name"
              item-value="id"
              label="Domain"
              variant="outlined"
              :rules="[v => !!v || 'Domain is required']"
            ></v-select>
          </v-col>

          <v-col cols="12" md="6">
            <v-select
              v-model="config.difficulty"
              :items="difficulties"
              label="Difficulty"
              variant="outlined"
              :rules="[v => !!v || 'Difficulty is required']"
            ></v-select>
          </v-col>

          <v-col cols="12" md="6">
            <v-select
              v-model="config.sessionType"
              :items="sessionTypes"
              item-title="label"
              item-value="value"
              label="Session Type"
              variant="outlined"
              :rules="[v => !!v || 'Session type is required']"
            ></v-select>
          </v-col>
        </v-row>

        <v-btn
          type="submit"
          color="primary"
          size="large"
          block
          class="mt-4"
          :loading="loading"
        >
          Start Session
        </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useSessionStore } from '@/stores/session'
import { useVocabularyStore } from '@/stores/vocabulary'

const emit = defineEmits(['start-session'])

const sessionStore = useSessionStore()
const vocabularyStore = useVocabularyStore()

const formRef = ref(null)
const loading = ref(false)

const config = ref({
  nativeLanguage: 'fr', // Will be set from App navbar selection
  languageTested: '',
  domain: null,
  difficulty: '',
  sessionType: 'comprehension'
})

const languages = ref([])
const domains = ref([])
const difficulties = ref(['EASY', 'MEDIUM', 'HARD'])
const sessionTypes = ref([
  { label: 'Comprehension', value: 'comprehension' },
  { label: 'Expression', value: 'expression' },
  { label: 'Both', value: 'both' }
])

onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([
      vocabularyStore.fetchLanguages(),
      vocabularyStore.fetchDomains()
    ])
    
    languages.value = vocabularyStore.languages
    domains.value = vocabularyStore.domains
    
    // Set defaults
    if (languages.value.length > 0) {
      config.value.languageTested = languages.value[0].code
    }
    if (domains.value.length > 0) {
      config.value.domain = domains.value[0].id
    }
    config.value.difficulty = difficulties.value[0]
  } catch (error) {
    console.error('Failed to load configuration options:', error)
  } finally {
    loading.value = false
  }
})

const startSession = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  try {
    // First create session config
    const sessionConfig = await sessionStore.createSessionConfig(config.value)
    
    // Then start the session
    const session = await sessionStore.startSession(sessionConfig.id)
    
    // Emit event to navigate to session
    emit('start-session', session.id)
  } catch (error) {
    console.error('Failed to start session:', error)
    alert('Failed to start session. Please try again.')
  } finally {
    loading.value = false
  }
}
</script>
