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
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSessionStore } from '@/stores/session'
import { useVocabularyStore } from '@/stores/vocabulary'

const { t } = useI18n()
const emit = defineEmits(['start-session'])

const sessionStore = useSessionStore()
const vocabularyStore = useVocabularyStore()

const formRef = ref(null)
const loading = ref(false)

const config = ref({
  nativeLanguage: 'fr',
  languageTested: '',
  domain: null,
  difficulty: '',
  sessionType: 'comprehension'
})

const languages = ref([])
const domains = ref([])

const translatedDifficulties = computed(() => [
  { label: t('difficulties.easy'), value: 'EASY' },
  { label: t('difficulties.medium'), value: 'MEDIUM' },
  { label: t('difficulties.hard'), value: 'HARD' }
])

const translatedDomains = computed(() => 
  domains.value.map(domain => ({
    label: t(`domains.${domain.code}`),
    value: domain.code
  }))
)

const sessionTypes = computed(() => [
  { label: t('sessionConfig.comprehension'), value: 'COMPREHENSION' },
  { label: t('sessionConfig.expression'), value: 'EXPRESSION' },
  { label: t('sessionConfig.both'), value: 'MIXED' }
])

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
    alert(t('sessionConfig.failedToStart'))
  } finally {
    loading.value = false
  }
}

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
    config.value.difficulty = 'EASY'
  } catch (error) {
    console.error(t('errors.failedToLoadOptions'), error)
  } finally {
    loading.value = false
  }
})
</script>
