<template>
  <VContainer>
    <VCard max-width="900" class="mx-auto">
      <VCardTitle class="text-h4 pa-6">{{ t('profile.title') }}</VCardTitle>

      <VCardText v-if="loading">
        <VProgressLinear indeterminate color="primary"></VProgressLinear>
      </VCardText>

      <VCardText v-else>
        <!-- User Info Section -->
        <VCard variant="outlined" class="mb-6">
          <VCardTitle>{{ t('profile.personalInfo') }}</VCardTitle>
          <VCardText>
            <VRow>
              <VCol cols="12" md="6">
                <VTextField
                  v-model="profile.email"
                  :label="t('profile.email')"
                  readonly
                  variant="outlined"
                  density="compact"
                ></VTextField>
              </VCol>
              <VCol cols="12" md="6">
                <VTextField
                  v-model="profile.fullName"
                  :label="t('profile.fullName')"
                  variant="outlined"
                  density="compact"
                  @update:model-value="debouncedUpdateProfile"
                ></VTextField>
              </VCol>
              <VCol cols="12" md="6">
                <VSelect
                  v-model="profile.nativeLanguage"
                  :items="languages"
                  item-title="name"
                  item-value="code"
                  :label="t('profile.nativeLanguage')"
                  variant="outlined"
                  density="compact"
                  @update:model-value="debouncedUpdateProfile"
                ></VSelect>
              </VCol>
            </VRow>
          </VCardText>
        </VCard>

        <!-- Learning Languages Section -->
        <VCard variant="outlined" class="mb-6">
          <VCardTitle>{{ t('profile.learningLanguages') }}</VCardTitle>
          <VCardText>
            <VList v-if="userLanguages.length">
              <VListItem
                v-for="lang in userLanguages"
                :key="lang.languageCode"
                class="mb-2"
              >
                <VRow align="center">
                  <VCol cols="12" sm="4">
                    <strong>{{ getLanguageName(lang.languageCode) }}</strong>
                  </VCol>
                  <VCol cols="12" sm="4">
                    <VSelect
                      v-model="lang.level"
                      :items="levels"
                      :label="t('profile.level')"
                      variant="outlined"
                      density="compact"
                      hide-details
                      @update:model-value="updateLanguage(lang)"
                    ></VSelect>
                  </VCol>
                  <VCol cols="12" sm="3">
                    <VCheckbox
                      v-model="lang.isLearning"
                      :label="t('profile.isLearning')"
                      hide-details
                      @update:model-value="updateLanguage(lang)"
                    ></VCheckbox>
                  </VCol>
                  <VCol cols="12" sm="1">
                    <VBtn
                      icon="mdi-delete"
                      size="small"
                      color="error"
                      variant="text"
                      @click="deleteLanguage(lang.languageCode)"
                    ></VBtn>
                  </VCol>
                </VRow>
              </VListItem>
            </VList>
            <div v-else class="text-grey text-center py-4">
              {{ t('profile.noLanguages') }}
            </div>

            <!-- Add Language Form -->
            <VDivider class="my-4"></VDivider>
            <VRow align="center">
              <VCol cols="12" sm="5">
                <VSelect
                  v-model="newLanguage.languageCode"
                  :items="availableLanguages"
                  item-title="name"
                  item-value="code"
                  :label="t('profile.addLanguage')"
                  variant="outlined"
                  density="compact"
                  hide-details
                ></VSelect>
              </VCol>
              <VCol cols="12" sm="4">
                <VSelect
                  v-model="newLanguage.level"
                  :items="levels"
                  :label="t('profile.level')"
                  variant="outlined"
                  density="compact"
                  hide-details
                ></VSelect>
              </VCol>
              <VCol cols="12" sm="3">
                <VBtn
                  color="primary"
                  block
                  @click="addLanguage"
                  :disabled="!newLanguage.languageCode || !newLanguage.level"
                >
                  {{ t('profile.add') }}
                </VBtn>
              </VCol>
            </VRow>
          </VCardText>
        </VCard>

        <VAlert v-if="successMessage" type="success" class="mb-4" closable @click:close="successMessage = ''">
          {{ successMessage }}
        </VAlert>
        <VAlert v-if="errorMessage" type="error" class="mb-4" closable @click:close="errorMessage = ''">
          {{ errorMessage }}
        </VAlert>
      </VCardText>
    </VCard>
  </VContainer>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import apiClient from "@/setup/axios"
  import { debounce } from "lodash";


const { t } = useI18n()
const loading = ref(true)
const profile = ref({
  email: '',
  fullName: '',
  nativeLanguage: null
})
const userLanguages = ref([])
const languages = ref([])
const newLanguage = ref({
  languageCode: '',
  level: 'BEGINNER',
  isLearning: true
})
const successMessage = ref('')
const errorMessage = ref('')

const levels = ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'NATIVE']

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const availableLanguages = computed(() => {
  const userLangCodes = userLanguages.value.map(l => l.languageCode)
  return languages.value.filter(lang => 
    !userLangCodes.includes(lang.code) && lang.code !== profile.value.nativeLanguage
  )
})

const getLanguageName = (code) => {
  const lang = languages.value.find(l => l.code === code)
  return lang ? lang.name : code
}

const fetchProfile = async () => {
  try {
    const res = await apiClient.get('/api/v1/profile/')
    profile.value = res.data
    userLanguages.value = res.data.languages || []
  } catch (e) {
    errorMessage.value = t('profile.failedToLoad')
    console.error('Failed to load profile:', e)
  }
}

const fetchLanguages = async () => {
  try {
    const res = await apiClient.get('/api/v1/config/languages')
    languages.value = res.data
  } catch (e) {
    console.error('Failed to load languages:', e)
  }
}

const updateProfile = async () => {
  try {
    await apiClient.patch('/api/v1/profile/', {
      nativeLanguage: profile.value.nativeLanguage,
      fullName: profile.value.fullName
    })
    successMessage.value = t('profile.updated')
  } catch (e) {
    errorMessage.value = t('profile.updateFailed')
    console.error('Failed to update profile:', e)
  }
}

// Create debounced version once
const debouncedUpdateProfile = debounce(updateProfile, 400)

const addLanguage = async () => {
  try {
    const res = await apiClient.post('/api/v1/profile/languages', newLanguage.value)
    userLanguages.value.push(res.data)
    newLanguage.value = { languageCode: '', level: 'BEGINNER', isLearning: true }
    successMessage.value = t('profile.languageAdded')
  } catch (e) {
    errorMessage.value = e.response?.data?.detail || t('profile.addFailed')
    console.error('Failed to add language:', e)
  }
}

const updateLanguage = async (lang) => {
  try {
    await apiClient.patch(`/api/v1/profile/languages/${lang.languageCode}`, {
      level: lang.level,
      isLearning: lang.isLearning
    })
    successMessage.value = t('profile.languageUpdated')
  } catch (e) {
    errorMessage.value = t('profile.updateFailed')
    console.error('Failed to update language:', e)
  }
}

const deleteLanguage = async (languageCode) => {
  try {
    await apiClient.delete(`/api/v1/profile/languages/${languageCode}`)
    userLanguages.value = userLanguages.value.filter(l => l.languageCode !== languageCode)
    successMessage.value = t('profile.languageDeleted')
  } catch (e) {
    errorMessage.value = t('profile.deleteFailed')
    console.error('Failed to delete language:', e)
  }
}

onMounted(async () => {
  loading.value = true
  await Promise.all([fetchProfile(), fetchLanguages()])
  loading.value = false
})
</script>
