<template>
  <VContainer>
    <VCard max-width="800" class="mx-auto">
      <VCardTitle>{{ t('profile.title') }}</VCardTitle>

      <VCardText v-if="loading">
        {{ t('profile.loading') }}
      </VCardText>

      <VCardText v-else-if="stats">
        <VRow>
          <VCol cols="12" md="6">
            <VCard variant="outlined">
              <VCardTitle>{{ t('profile.progress') }}</VCardTitle>
              <VCardText class="text-center">
                <div class="text-h2 mb-2 text-primary">{{ stats.correct_rate }}%</div>
                <div class="text-subtitle-1 text-grey mb-4">{{ t('profile.correctRate') }}</div>
                <div class="text-body-1">
                  {{ t('profile.wordsReviewed', { count: stats.total_words_reviewed }) }}
                </div>
              </VCardText>
            </VCard>
          </VCol>

          <VCol cols="12" md="6">
            <VCard variant="outlined">
              <VCardTitle>{{ t('profile.focusWords') }}</VCardTitle>
              <VCardText>
                <div class="text-body-2 text-grey mb-3">{{ t('profile.weakWordsDesc') }}</div>
                <VList v-if="stats.weakest_words.length" density="compact">
                  <VListItem
                    v-for="word in stats.weakest_words"
                    :key="word"
                    :title="word"
                    class="text-error"
                  ></VListItem>
                </VList>
                <div v-else class="text-success font-italic">
                  {{ t('profile.noWeakWords') }}
                </div>
              </VCardText>
            </VCard>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>
  </VContainer>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import axios from 'axios'

const { t } = useI18n()
const stats = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
    const res = await axios.get(`${API_URL}/profile`)
    stats.value = res.data
  } catch (e) {
    console.error(t('profile.failedToLoad'), e)
  } finally {
    loading.value = false
  }
})
</script>
