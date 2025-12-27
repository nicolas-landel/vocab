<template>
  <VContainer>
    <!-- Filter Form -->
    <VCard class="mb-6">
      <VCardTitle>{{ t('vocabulary.filterTitle') }}</VCardTitle>
      <VCardText>
        <VForm ref="filterFormRef">
          <VRow>
            <VCol cols="12" md="4">
              <VSelect
                v-model="filters.languageCode"
                :items="languages"
                item-title="name"
                item-value="code"
                :label="t('vocabulary.languageToStudy')"
                variant="outlined"
                :rules="[v => !!v || t('sessionConfig.languageRequired')]"
              ></VSelect>
            </VCol>

            <VCol cols="12" md="4">
              <VSelect
                v-model="filters.domains"
                :items="translatedDomains"
                item-title="label"
                item-value="value"
                :label="t('vocabulary.domains')"
                variant="outlined"
                multiple
                chips
                closable-chips
              ></VSelect>
            </VCol>

            <VCol cols="12" md="4">
              <VSelect
                v-model="filters.difficulties"
                :items="translatedDifficulties"
                item-title="title"
                item-value="value"
                :label="t('vocabulary.difficulties')"
                variant="outlined"
                multiple
                chips
                closable-chips
              ></VSelect>
            </VCol>

            <VCol cols="12">
              <VCheckbox
                v-model="filters.showKnown"
                :label="t('vocabulary.includeKnown')"
                hide-details
              ></VCheckbox>
            </VCol>
          </VRow>

          <VBtn
            color="primary"
            @click="loadVocabulary"
            :loading="loading"
            class="mt-4"
          >
            {{ t('vocabulary.loadVocabulary') }}
          </VBtn>
        </VForm>
      </VCardText>
    </VCard>

    <!-- Vocabulary Table -->
    <VCard v-if="translations.length > 0">
      <VCardTitle>{{ t('vocabulary.vocabularyList') }}</VCardTitle>
      <VCardText>
        <VTable hover>
          <thead>
            <tr>
              <th class="text-left">{{ nativeLanguageLabel }}</th>
              <th class="text-left">{{ targetLanguageLabel }}</th>
              <th class="text-left">{{ t('vocabulary.domain') }}</th>
              <th class="text-left">{{ t('vocabulary.difficulty') }}</th>
              <th class="text-left">{{ t('vocabulary.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="translation in translations"
              :key="translation.id"
              @click="openDetailModal(translation)"
              style="cursor: pointer"
            >
              <td>{{ translation.masterWord?.text || '-' }}</td>
              <td>{{ translation.text }}</td>
              <td>{{ translation.masterWord?.domain?.code ? t(`domains.${translation.masterWord.domain.code}`) : '-' }}</td>
              <td>
                <VChip :color="getDifficultyColor(translation.difficulty)" size="small">
                  {{ t(`difficulties.${translation.difficulty.toLowerCase()}`) }}
                </VChip>
              </td>
              <td @click.stop>
                <VBtn
                  :icon="translation.isKnown ? 'mdi-check-circle' : 'mdi-circle-outline'"
                  :color="translation.isKnown ? 'success' : 'grey'"
                  variant="text"
                  @click="toggleKnown(translation)"
                ></VBtn>
              </td>
            </tr>
          </tbody>
        </VTable>
      </VCardText>
    </VCard>

    <VAlert v-else-if="!loading && filterApplied" type="info" class="mt-4">
      {{ t('vocabulary.noVocabulary') }}
    </VAlert>

    <!-- Word Detail Modal -->
    <word-detail-modal
      v-model="detailDialog"
      :translation="selectedTranslation"
    />
  </VContainer>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useVocabularyStore } from '@/stores/vocabulary'
import WordDetailModal from '@/components/WordDetailModal.vue'

const { t } = useI18n()
const vocabularyStore = useVocabularyStore()

const filterFormRef = ref(null)
const loading = ref(false)
const filterApplied = ref(false)
const detailDialog = ref(false)
const selectedTranslation = ref(null)

const filters = ref({
  languageCode: '',
  domains: [],
  difficulties: [],
  showKnown: false
})

const languages = ref([])
const domains = ref([])
const translatedDifficulties = computed(() => [
  { title: t('difficulties.easy'), value: 'EASY' },
  { title: t('difficulties.medium'), value: 'MEDIUM' },
  { title: t('difficulties.hard'), value: 'HARD' }
])
const translatedDomains = computed(() => 
  domains.value.map(domain => ({
    label: t(`domains.${domain.code}`),
    value: domain.id
  }))
)
const translations = ref([])

const nativeLanguageLabel = computed(() => t('vocabulary.nativeLanguage'))
const targetLanguageLabel = computed(() => {
  const lang = languages.value.find(l => l.code === filters.value.languageCode)
  return lang?.name || t('vocabulary.translation')
})



const loadVocabulary = async () => {
  const { valid } = await filterFormRef.value.validate()
  if (!valid) return

  loading.value = true
  filterApplied.value = true
  
  try {
    const result = await vocabularyStore.fetchVocabulary(filters.value)
    translations.value = vocabularyStore.translations
  } catch (error) {
    console.error(t('vocabulary.failedToLoad'), error)
    alert(t('vocabulary.failedToLoad'))
  } finally {
    loading.value = false
  }
}

const getDifficultyColor = (difficulty) => {
  const colors = {
    EASY: 'green',
    MEDIUM: 'orange',
    HARD: 'red'
  }
  return colors[difficulty] || 'grey'
}

const toggleKnown = async (translation) => {
  try {
    const newKnownState = !translation.isKnown
    await vocabularyStore.toggleWordKnown(translation.id, newKnownState)
    
    // Update local state
    translation.isKnown = newKnownState
  } catch (error) {
    console.error(t('vocabulary.failedToToggle'), error)
    alert(t('vocabulary.failedToToggle'))
  }
}

const openDetailModal = (translation) => {
  selectedTranslation.value = translation
  detailDialog.value = true
}

// onMounted(async () => {
//   try {
//     await Promise.all([
//       vocabularyStore.fetchLanguages(),
//       vocabularyStore.fetchDomains()
//     ])
    
//     languages.value = vocabularyStore.languages
//     domains.value = vocabularyStore.domains
    
//     // Set default language
//     if (languages.value.length > 0) {
//       filters.value.languageCode = languages.value[0].code
//     }
//   } catch (error) {
//     console.error(t('errors.failedToLoadOptions'), error)
//   }
// })
</script>
