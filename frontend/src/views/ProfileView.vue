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
                  v-model="profile.full_name"
                  :label="t('profile.fullName')"
                  variant="outlined"
                  density="compact"
                  @blur="updateProfile"
                ></VTextField>
              </VCol>
              <VCol cols="12" md="6">
                <VSelect
                  v-model="profile.native_language"
                  :items="languages"
                  item-title="name"
                  item-value="code"
                  :label="t('profile.nativeLanguage')"
                  variant="outlined"
                  density="compact"
                  @update:model-value="updateProfile"
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
                :key="lang.language_code"
                class="mb-2"
              >
                <VRow align="center">
                  <VCol cols="12" sm="4">
                    <strong>{{ getLanguageName(lang.language_code) }}</strong>
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
                      v-model="lang.is_learning"
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
                      @click="deleteLanguage(lang.language_code)"
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
                  v-model="newLanguage.language_code"
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
                  :disabled="!newLanguage.language_code || !newLanguage.level"
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
import axios from 'axios'

const { t } = useI18n()
const loading = ref(true)
const profile = ref({
  email: '',
  full_name: '',
  native_language: null
})
const userLanguages = ref([])
const languages = ref([])
const newLanguage = ref({
  language_code: '',
  level: 'BEGINNER',
  is_learning: true
})
const successMessage = ref('')
const errorMessage = ref('')

const levels = ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'NATIVE']

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const availableLanguages = computed(() => {
  const userLangCodes = userLanguages.value.map(l => l.language_code)
  return languages.value.filter(lang => 
    !userLangCodes.includes(lang.code) && lang.code !== profile.value.native_language
  )
})

const getLanguageName = (code) => {
  const lang = languages.value.find(l => l.code === code)
  return lang ? lang.name : code
}

const fetchProfile = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const res = await axios.get(`${API_URL}/api/v1/profile/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    profile.value = res.data
    userLanguages.value = res.data.languages || []
  } catch (e) {
    errorMessage.value = t('profile.failedToLoad')
    console.error('Failed to load profile:', e)
  }
}

const fetchLanguages = async () => {
  try {
    const res = await axios.get(`${API_URL}/api/v1/config/languages`)
    languages.value = res.data
  } catch (e) {
    console.error('Failed to load languages:', e)
  }
}

const updateProfile = async () => {
  try {
    const token = localStorage.getItem('access_token')
    await axios.patch(`${API_URL}/api/v1/profile/`, {
      native_language: profile.value.native_language,
      full_name: profile.value.full_name
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    successMessage.value = t('profile.updated')
  } catch (e) {
    errorMessage.value = t('profile.updateFailed')
    console.error('Failed to update profile:', e)
  }
}

const addLanguage = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const res = await axios.post(`${API_URL}/api/v1/profile/languages`, newLanguage.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    userLanguages.value.push(res.data)
    newLanguage.value = { language_code: '', level: 'BEGINNER', is_learning: true }
    successMessage.value = t('profile.languageAdded')
  } catch (e) {
    errorMessage.value = e.response?.data?.detail || t('profile.addFailed')
    console.error('Failed to add language:', e)
  }
}

const updateLanguage = async (lang) => {
  try {
    const token = localStorage.getItem('access_token')
    await axios.patch(`${API_URL}/api/v1/profile/languages/${lang.language_code}`, {
      level: lang.level,
      is_learning: lang.is_learning
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    successMessage.value = t('profile.languageUpdated')
  } catch (e) {
    errorMessage.value = t('profile.updateFailed')
    console.error('Failed to update language:', e)
  }
}

const deleteLanguage = async (languageCode) => {
  try {
    const token = localStorage.getItem('access_token')
    await axios.delete(`${API_URL}/api/v1/profile/languages/${languageCode}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    userLanguages.value = userLanguages.value.filter(l => l.language_code !== languageCode)
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
