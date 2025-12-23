<template>
  <VContainer>
    <VCard v-if="!sessionStore.isSessionComplete" max-width="800" class="mx-auto">
      <!-- Progress -->
      <VCardTitle>
        <div class="d-flex justify-space-between align-center w-100">
          <span>{{ t('session.progress') }}</span>
          <span class="text-body-1">
            {{ sessionStore.currentWordIndex + 1 }} / {{ sessionStore.totalWords }}
          </span>
        </div>
      </VCardTitle>

      <VProgressLinear
        :model-value="progress"
        color="primary"
        height="8"
      ></VProgressLinear>

      <VCardText class="pt-8">
        <VRow v-if="sessionStore.currentWord">
          <!-- Word to translate -->
          <VCol cols="12" class="text-center">
            <div class="text-subtitle-1 text-grey mb-2">{{ t('session.translateWord') }}</div>
            <div class="text-h3 mb-6">{{ sessionStore.currentWord.text }}</div>
            
            <div v-if="sessionStore.currentWord.masterWord?.domain" class="mb-4">
              <VChip color="primary" variant="outlined">
                {{ t(`domains.${sessionStore.currentWord.masterWord.domain.code}`) }}
              </VChip>
            </div>
          </VCol>

          <!-- Answer Input -->
          <VCol cols="12">
            <VTextField
              v-model="userAnswer"
              :label="t('session.yourAnswer')"
              variant="outlined"
              size="large"
              autofocus
              @keyup.enter="submitAnswer"
              :disabled="showResult"
            ></VTextField>
          </VCol>

          <!-- Result Display -->
          <VCol cols="12" v-if="showResult">
            <VAlert
              :type="isCorrect ? 'success' : 'error'"
              :icon="isCorrect ? 'mdi-check-circle' : 'mdi-close-circle'"
              prominent
            >
              <div class="text-h6">{{ isCorrect ? t('session.correct') : t('session.incorrect') }}</div>
              <div v-if="!isCorrect" class="mt-2">
                {{ t('session.correctAnswer') }}: <strong>{{ correctAnswer }}</strong>
              </div>
            </VAlert>
          </VCol>

          <!-- Action Buttons -->
          <VCol cols="12">
            <div class="d-flex gap-2">
              <VBtn
                v-if="!showResult"
                color="warning"
                variant="outlined"
                @click="skipWord"
                block
              >
                {{ t('session.iForgot') }}
              </VBtn>
              
              <VBtn
                v-if="!showResult"
                color="primary"
                @click="submitAnswer"
                :disabled="!userAnswer"
                block
              >
                {{ t('session.checkAnswer') }}
              </VBtn>

              <VBtn
                v-if="showResult"
                color="primary"
                @click="nextWord"
                block
              >
                {{ t('session.nextWord') }}
              </VBtn>
            </div>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>

    <!-- Session Complete -->
    <VCard v-else max-width="800" class="mx-auto">
      <VCardTitle class="text-center">{{ t('session.complete') }}</VCardTitle>
      <VCardText>
        <div class="text-center mb-6">
          <div class="text-h2 mb-4">{{ sessionStore.sessionResults?.successRate }}%</div>
          <div class="text-subtitle-1 text-grey">{{ t('session.successRate') }}</div>
        </div>

        <VRow>
          <VCol cols="12" md="6">
            <VCard variant="outlined" color="success">
              <VCardText class="text-center">
                <div class="text-h4">{{ sessionStore.sessionResults?.correctFirstTime?.length || 0 }}</div>
                <div class="text-subtitle-2">{{ t('session.correctFirstTry') }}</div>
              </VCardText>
            </VCard>
          </VCol>

          <VCol cols="12" md="6">
            <VCard variant="outlined" color="error">
              <VCardText class="text-center">
                <div class="text-h4">{{ sessionStore.sessionResults?.failed?.length || 0 }}</div>
                <div class="text-subtitle-2">{{ t('session.needsPractice') }}</div>
              </VCardText>
            </VCard>
          </VCol>
        </VRow>

        <div class="d-flex gap-2 mt-6">
          <VBtn color="primary" @click="finishSession" block>
            {{ t('session.finish') }}
          </VBtn>
        </div>
      </VCardText>
    </VCard>
  </VContainer>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useSessionStore } from '@/stores/session'

const { t } = useI18n()
const props = defineProps(['id'])
const router = useRouter()
const sessionStore = useSessionStore()

const userAnswer = ref('')
const showResult = ref(false)
const isCorrect = ref(false)
const correctAnswer = ref('')

const progress = computed(() => {
  if (!sessionStore.totalWords) return 0
  return (sessionStore.currentWordIndex / sessionStore.totalWords) * 100
})

onMounted(async () => {
  // If session not loaded, redirect to home
  if (!sessionStore.currentSessionId) {
    router.push('/')
  }
})

const submitAnswer = () => {
  if (!userAnswer.value.trim()) return

  // Store correct answer from current word's master word translation
  correctAnswer.value = sessionStore.currentWord.masterWord?.text || ''
  
  // Submit answer to store
  sessionStore.submitAnswer(userAnswer.value)
  
  // Check if answer was correct
  const answerRecord = sessionStore.answers[sessionStore.answers.length - 1]
  isCorrect.value = answerRecord?.correct || false
  
  showResult.value = true
}

const skipWord = () => {
  sessionStore.skipWord()
  resetInputState()
}

const nextWord = () => {
  resetInputState()
}

const resetInputState = () => {
  userAnswer.value = ''
  showResult.value = false
  isCorrect.value = false
  correctAnswer.value = ''
}

const finishSession = async () => {
  try {
    await sessionStore.completeSession()
    router.push('/')
  } catch (error) {
    console.error(t('session.failedToComplete'), error)
    alert(t('session.failedToComplete'))
  }
}
</script>
