<template>
  <VContainer>
    <VCard v-if="!sessionStore.isSessionComplete" max-width="800" class="mx-auto">
      <VCardTitle>
        <div class="d-flex justify-space-between align-center w-100">
          <span>{{ t('session.progress') }}</span>
          <span class="text-body-1">
            {{ progress.toFixed(0) }}%
          </span>
        </div>
      </VCardTitle>

      <VProgressLinear
        :model-value="progress"
        color="primary"
        height="8"
      ></VProgressLinear>

      <VCardText class="pt-8">
        <div v-if="currentWord">
          <VCol cols="12" class="text-center">
            <div class="text-subtitle-1 text-grey mb-2">
              {{ t('session.translateWord') }}
            </div>
            <div class="text-h3 mb-6 capitalize-text">
              {{ getTextToTranslate }}
            </div>
            
            <!-- <div v-if="currentWord.masterWord?.domain" class="mb-4">
              <VChip color="primary" variant="outlined">
                {{ t(`domains.${sessionStore.currentWord.masterWord.domain.code}`) }}
              </VChip>
            </div> -->
          </VCol>

          <VCol>
            <VTextField
              v-model="userAnswer"
              :label="t('session.yourAnswer')"
              variant="outlined"
              size="large"
              autofocus
              @keyup.enter="submitAnswer"
            ></VTextField>

          </VCol>
          <VCol>
            <VBtn
              color="primary"
              @click="submitAnswer"
              :disabled="!userAnswer"
              block
            >
              {{ t('session.validate') }}
            </VBtn>
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

          <VCol cols="12">
            <div class="d-flex gap-2">
              <VBtn
                v-if="!showResult"
                variant="text"
                class="text-decoration-underline"
                @click="skipWord"
                block
              >
                {{ t('session.iForgot') }}
              </VBtn>
            </div>
          </VCol>
        </div>
      </VCardText>
    </VCard>

    <!-- Session Complete -->
    <VCard v-else max-width="800" class="mx-auto">
      <VCardTitle class="text-center">{{ t('session.complete') }}</VCardTitle>
      <VCardText>
        <div class="text-center mb-6">
          <div class="text-h2 mb-4">{{ sessionStore.sessionWords?.successRate }}%</div>
          <div class="text-subtitle-1 text-grey">{{ t('session.successRate') }}</div>
        </div>

        <VRow>
          <VCol cols="12" md="6">
            <VCard variant="outlined" color="success">
              <VCardText class="text-center">
                <div class="text-h4">{{ sessionStore.sessionWords?.correctFirstTime?.length || 0 }}</div>
                <div class="text-subtitle-2">{{ t('session.correctFirstTry') }}</div>
              </VCardText>
            </VCard>
          </VCol>

          <VCol cols="12" md="6">
            <VCard variant="outlined" color="error">
              <VCardText class="text-center">
                <div class="text-h4">{{ sessionStore.sessionWords?.failed?.length || 0 }}</div>
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
import { SessionWord } from "@/models"
import { useRepo } from "pinia-orm"

const { t } = useI18n()
const props = defineProps(['id'])
const router = useRouter()
const sessionStore = useSessionStore()
const sessionWordRepo = useRepo(SessionWord)

const currentWord = ref(null)
const currentIndex = ref(0)
const userAnswer = ref('')
// const showResult = ref(false)
// const isCorrect = ref(false)
// const correctAnswer = ref('')

const answeredWords = computed(() => {
  return sessionWordRepo.query()
    .where('sessionId', sessionStore.currentSessionId)
    .whereNotNull('userAnswer')
    .get()
})

const allWords = computed(() => {
  return sessionWordRepo.query()
    .where('sessionId', sessionStore.currentSessionId)
    .with('translationTo')
    .with('translationFrom')
    .get()
})

const progress = computed(() => {
  console.log("pppppppp", answeredWords.value, allWords.value)
  if (allWords.value.length === 0) return 0
  return (answeredWords.value.length / allWords.value.length) * 100
})

const getTextToTranslate = computed(() => {
  if (!currentWord.value) return ''
  // Assuming we want to show the text from the 'translationFrom' relationship
  return currentWord.value.translationFrom?.text || ''
})


const submitAnswer = () => {
  console.log("Submitting answer for word:", userAnswer.value)
  if (!userAnswer.value.trim()) return

  correctAnswer.value = currentWord.value.translation?.text || ''
  
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

onMounted(async () => {
  if (!sessionStore.currentSessionId) {
    router.push('/')
  }
  currentWord.value = allWords.value[currentIndex.value]
  console.log("Current Word:", currentWord.value)
})
</script>

<style scoped>

.capitalize-text {
  text-transform: capitalize !important;
}
</style>