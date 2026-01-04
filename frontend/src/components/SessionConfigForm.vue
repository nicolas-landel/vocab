<template>
  <VCard max-width="800" class="mx-auto">
    <VCardTitle class="text-h5">{{ t('sessionConfig.title') }}</VCardTitle>
    <VCardText>
      <VForm ref="formRef" @submit.prevent="startSession">
        <VRow>
          <VCol cols="12" md="6">
            <VSelect
              v-model="config.languageTested"
              :items="languages"
              item-title="name"
              item-value="code"
              :label="t('sessionConfig.languageToTest')"
              variant="outlined"
              :rules="[v => !!v || t('sessionConfig.languageRequired')]"
            ></VSelect>
          </VCol>

          <VCol cols="12" md="6">
            <VSelect
              v-model="config.domain"
              :items="translatedDomains"
              item-title="label"
              item-value="value"
              :label="t('sessionConfig.domain')"
              variant="outlined"
              :rules="[v => !!v || t('sessionConfig.domainRequired')]"
            ></VSelect>
          </VCol>

          <VCol cols="12" md="6">
            <VSelect
              v-model="config.difficulty"
              :items="translatedDifficulties"
              item-title="label"
              item-value="value"
              :label="t('sessionConfig.difficulty')"
              variant="outlined"
              :rules="[v => !!v || t('sessionConfig.difficultyRequired')]"
            ></VSelect>
          </VCol>

          <VCol cols="12" md="6">
            <VSelect
              v-model="config.sessionType"
              :items="sessionTypes"
              item-title="label"
              item-value="value"
              :label="t('sessionConfig.sessionType')"
              variant="outlined"
              :rules="[v => !!v || t('sessionConfig.sessionTypeRequired')]"
            ></VSelect>
          </VCol>
        </VRow>

        <VBtn
          type="submit"
          color="primary"
          size="large"
          block
          class="mt-4"
          :loading="loading"
        >
          {{ t('sessionConfig.startSession') }}
        </VBtn>
      </VForm>
    </VCardText>
  </VCard>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSessionStore } from '@/stores/session'
import { useVocabularyStore } from '@/stores/vocabulary'
import { useAuthStore } from '@/stores/auth'
import { UserLanguage } from "@/models"
import { useRepo } from 'pinia-orm'
import { useNotificationsStore } from '@/stores/notification'
import { SESSION_TYPES, DIFFICULTY_LEVELS } from "@/const"


const { t } = useI18n()
const emit = defineEmits(['start-session'])

const sessionStore = useSessionStore()
const vocabularyStore = useVocabularyStore()
const authStore = useAuthStore()
const userLanguageRepo = useRepo(UserLanguage)
const notificationsStore = useNotificationsStore()

const formRef = ref(null)
const loading = ref(false)

const config = ref({
  nativeLanguage: 'en',
  languageTested: '',
  domain: null,
  difficulty: '',
  sessionType: SESSION_TYPES.MIXED
})

const languages = ref([])
const domains = ref([])

const translatedDifficulties = computed(() => [
  { label: t('difficulties.easy'), value: DIFFICULTY_LEVELS.EASY },
  { label: t('difficulties.medium'), value: DIFFICULTY_LEVELS.MEDIUM },
  { label: t('difficulties.hard'), value: DIFFICULTY_LEVELS.HARD }
])

const translatedDomains = computed(() => 
  domains.value.map(domain => ({
    label: t(`domains.${domain.code}`),
    value: domain.code
  })).concat({ label: t('domains.all'), value: 'ALL' })
)

const sessionTypes = computed(() => [
  { label: t('sessionConfig.comprehension'), value: SESSION_TYPES.COMPREHENSION },
  { label: t('sessionConfig.expression'), value: SESSION_TYPES.EXPRESSION },
  { label: t('sessionConfig.both'), value: SESSION_TYPES.MIXED }
])

const userAppLanguage = computed(() => {
    const savedLanguage = authStore.getAppLanguage
    return savedLanguage || 'en'
})

const availableTestLanguages = computed(() => {
  const nativeLang = config.value.nativeLanguage
  const userLanguages = userLanguageRepo.query().all()
  console.log('User languages from repo:', userLanguages)
  // Prefer user's learning languages
  if (userLanguages.length > 0) {
    return userLanguages
      .filter(lang => lang.languageCode !== nativeLang)
      .map(lang => ({
        code: lang.languageCode,
        name: vocabularyStore.getLanguageName(lang.languageCode)
      }))
  }
  
  // Fallback to all available languages
  const allLanguages = vocabularyStore.languages || []
  return allLanguages.filter(lang => lang.code !== nativeLang)
})

watch(
  () => userAppLanguage.value,
  (newLang) => {
    config.value.nativeLanguage = newLang
    
    // Auto-select first available language if current selection is invalid
    if (config.value.languageTested === config.value.nativeLanguage || 
        !config.value.languageTested ||
        !availableTestLanguages.value.find(l => l.code === config.value.languageTested)) {
      config.value.languageTested = availableTestLanguages.value.length > 0 
        ? availableTestLanguages.value[0].code 
        : ''
    }
  },
  { immediate: true }
)

watch(
  () => availableTestLanguages.value,
  (newLanguages) => {
    languages.value = newLanguages
    
    // Update selected language if it's no longer available
    if (!newLanguages.find(l => l.code === config.value.languageTested)) {
      config.value.languageTested = newLanguages.length > 0 ? newLanguages[0].code : ''
    }
  }, { immediate: true }
)

const startSession = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return
  loading.value = true
  try {
    const sessionConfig = await sessionStore.createSessionConfig(config.value)
    const session = await sessionStore.startSession(sessionConfig.id)
    emit('start-session', session.id)
  } catch (error) {
    console.error(t('sessionConfig.failedToStart'), error)
    notificationsStore.notify({
      title: t('sessionConfig.errorTitle'),
      message: t('sessionConfig.failedToStart'),
      type: 'error'
    })
  } finally {
    loading.value = false
  }
}



onMounted(async () => {
  domains.value = vocabularyStore.domains

  if (domains.value.length > 0) {
    config.value.domain = domains.value[0].id
  }
  config.value.difficulty = DIFFICULTY_LEVELS.EASY

})
</script>
