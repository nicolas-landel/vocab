<template>
  <VContainer>
    <VCard v-if="session" max-width="600" class="mx-auto">
      <VCardTitle class="text-center">
        {{ t('summary.title') }}
      </VCardTitle>

      <VCardText>
        <div class="text-center mb-6">
          <div class="score-circle">
            <span class="score">{{ score }}%</span>
          </div>
        </div>

        <VRow class="text-center">
          <VCol cols="6">
            <div class="text-h4">{{ session.results.length }}</div>
            <div class="text-subtitle-2 text-grey">{{ t('summary.words') }}</div>
          </VCol>
          <VCol cols="6">
            <div class="text-h4">{{ session.results.filter(r => r.correct).length }}</div>
            <div class="text-subtitle-2 text-grey">{{ t('summary.correct') }}</div>
          </VCol>
        </VRow>

        <div class="d-flex justify-center mt-6">
          <VBtn color="primary" @click="goHome" size="large">
            {{ t('summary.newSession') }}
          </VBtn>
        </div>
      </VCardText>
    </VCard>

    <VCard v-else max-width="600" class="mx-auto">
      <VCardText class="text-center">
        {{ t('summary.loading') }}
      </VCardText>
    </VCard>
  </VContainer>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSessionStore } from '@/stores/session'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const props = defineProps(['id'])
const router = useRouter()
const sessionStore = useSessionStore()

const session = computed(() => sessionStore.currentSession)
const score = computed(() => session.value?.score ?? 0)

const goHome = () => router.push('/')
</script>

<style scoped>
.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid rgb(var(--v-theme-primary));
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  background: rgba(99, 102, 241, 0.1);
}

.score {
  font-size: 2.5rem;
  font-weight: 800;
}
</style>
