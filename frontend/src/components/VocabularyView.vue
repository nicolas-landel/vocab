<template>
  <v-container>
    <!-- Filter Form -->
    <v-card class="mb-6">
      <v-card-title>Filter Vocabulary</v-card-title>
      <v-card-text>
        <v-form ref="filterFormRef">
          <v-row>
            <v-col cols="12" md="4">
              <v-select
                v-model="filters.languageCode"
                :items="languages"
                item-title="name"
                item-value="code"
                label="Language to Study"
                variant="outlined"
                :rules="[v => !!v || 'Language is required']"
              ></v-select>
            </v-col>

            <v-col cols="12" md="4">
              <v-select
                v-model="filters.domains"
                :items="domains"
                item-title="name"
                item-value="id"
                label="Domains"
                variant="outlined"
                multiple
                chips
                closable-chips
              ></v-select>
            </v-col>

            <v-col cols="12" md="4">
              <v-select
                v-model="filters.difficulties"
                :items="difficulties"
                label="Difficulties"
                variant="outlined"
                multiple
                chips
                closable-chips
              ></v-select>
            </v-col>

            <v-col cols="12">
              <v-checkbox
                v-model="filters.showKnown"
                label="Include words I already know"
                hide-details
              ></v-checkbox>
            </v-col>
          </v-row>

          <v-btn
            color="primary"
            @click="loadVocabulary"
            :loading="loading"
            class="mt-4"
          >
            Load Vocabulary
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>

    <!-- Vocabulary Table -->
    <v-card v-if="translations.length > 0">
      <v-card-title>Vocabulary List</v-card-title>
      <v-card-text>
        <v-table hover>
          <thead>
            <tr>
              <th class="text-left">{{ nativeLanguageLabel }}</th>
              <th class="text-left">{{ targetLanguageLabel }}</th>
              <th class="text-left">Domain</th>
              <th class="text-left">Difficulty</th>
              <th class="text-left">Actions</th>
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
              <td>{{ translation.masterWord?.domain?.name || '-' }}</td>
              <td>
                <v-chip :color="getDifficultyColor(translation.difficulty)" size="small">
                  {{ translation.difficulty }}
                </v-chip>
              </td>
              <td @click.stop>
                <v-btn
                  :icon="translation.isKnown ? 'mdi-check-circle' : 'mdi-circle-outline'"
                  :color="translation.isKnown ? 'success' : 'grey'"
                  variant="text"
                  @click="toggleKnown(translation)"
                ></v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>

    <v-alert v-else-if="!loading && filterApplied" type="info" class="mt-4">
      No vocabulary found with the selected filters.
    </v-alert>

    <!-- Word Detail Modal -->
    <word-detail-modal
      v-model="detailDialog"
      :translation="selectedTranslation"
    />
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useVocabularyStore } from '@/stores/vocabulary'
import WordDetailModal from '@/components/WordDetailModal.vue'

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
const difficulties = ref(['EASY', 'MEDIUM', 'HARD'])
const translations = ref([])

const nativeLanguageLabel = computed(() => 'Native Language')
const targetLanguageLabel = computed(() => {
  const lang = languages.value.find(l => l.code === filters.value.languageCode)
  return lang?.name || 'Translation'
})

onMounted(async () => {
  try {
    await Promise.all([
      vocabularyStore.fetchLanguages(),
      vocabularyStore.fetchDomains()
    ])
    
    languages.value = vocabularyStore.languages
    domains.value = vocabularyStore.domains
    
    // Set default language
    if (languages.value.length > 0) {
      filters.value.languageCode = languages.value[0].code
    }
  } catch (error) {
    console.error('Failed to load filter options:', error)
  }
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
    console.error('Failed to load vocabulary:', error)
    alert('Failed to load vocabulary. Please try again.')
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
    console.error('Failed to toggle word known state:', error)
    alert('Failed to update word status.')
  }
}

const openDetailModal = (translation) => {
  selectedTranslation.value = translation
  detailDialog.value = true
}
</script>
