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
            <VDivider v-if="availableLanguages.length" class="my-4"></VDivider>
            <VRow v-if="availableLanguages.length" align="center">
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
import { useProfileStore } from '@/stores/profile'
import { useVocabularyStore } from '@/stores/vocabulary'
import { debounce } from 'lodash'

const { t } = useI18n()
const profileStore = useProfileStore()
const vocabularyStore = useVocabularyStore()

const loading = ref(false)
const profile = computed(() => profileStore.profile)
const userLanguages = computed(() => profileStore.getUserLanguage)
const languages = ref([])

const newLanguage = ref({
  languageCode: '',
  level: 'BEGINNER',
  isLearning: true
})
const successMessage = ref('')
const errorMessage = ref('')

const levels = ['BEGINNER', 'INTERMEDIATE', 'ADVANCED']

const availableLanguages = computed(() => {
  return profileStore.availableLanguages(languages.value)
})

const getLanguageName = (code) => {
  return profileStore.getLanguageName(code, languages.value)
}

const updateProfile = async () => {
  try {
    await profileStore.updateProfile({
      nativeLanguage: profile.value.nativeLanguage,
      fullName: profile.value.fullName
    })
    successMessage.value = t('profile.updated')
  } catch (e) {
    errorMessage.value = t('profile.updateFailed')
  }
}

const debouncedUpdateProfile = debounce(updateProfile, 400)

const addLanguage = async () => {
  try {
    await profileStore.addLanguage(newLanguage.value)
    newLanguage.value = { languageCode: '', level: 'BEGINNER', isLearning: true }
    successMessage.value = t('profile.languageAdded')
  } catch (e) {
    errorMessage.value = profileStore.error || t('profile.addFailed')
  }
}

const updateLanguage = async (lang) => {
  try {
    await profileStore.updateLanguage(lang.languageCode, {
      level: lang.level,
      isLearning: lang.isLearning
    })
    successMessage.value = t('profile.languageUpdated')
  } catch (e) {
    errorMessage.value = t('profile.updateFailed')
  }
}

const deleteLanguage = async (languageCode) => {
  try {
    await profileStore.deleteLanguage(languageCode)
    successMessage.value = t('profile.languageDeleted')
  } catch (e) {
    errorMessage.value = t('profile.deleteFailed')
  }
}

onMounted(async () => {
  await vocabularyStore.fetchLanguages()
  languages.value = vocabularyStore.languages
  await profileStore.fetchProfile()
})
</script>
