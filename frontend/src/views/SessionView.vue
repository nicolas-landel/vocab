<template>
  <VContainer>
    <VCard v-if="!sessionStore.isSessionComplete" max-width="800" class="mx-auto">
      <VCardTitle>
        <div class="d-flex justify-center align-center w-100">
           <VChip
            color="primary"
            variant="outlined"
          >{{ currentDomain?.name || '' }}</VChip>
          </div>
          <div class="d-flex justify-center align-center mt-4">
          <VProgressLinear
            :model-value="progress"
            color="primary"
            height="10"
            style="width: 70%;"
          />
        </div>
      </VCardTitle>

      <VCardText class="pt-8">
        <div v-if="currentWord">
          <VCol cols="12" class="text-center">
            <div class="text-subtitle-1 text-grey mb-2">
              {{ t('session.translateWord') }}
            </div>
            <div class="text-h3 mb-6 capitalize-text">
              {{ getTextToTranslate }}
            </div>
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
          <VCol>
            <VBtn
              v-if="!showResult"
              variant="text"
              class="text-decoration-underline"
              @click="skipWord"
              block
            >
              {{ t('session.iForgot') }}
            </VBtn>
          </VCol>

        </div>
          
      </VCardText>
    </VCard>

    <!-- Session Complete -->
    <!-- <VCard v-else max-width="800" class="mx-auto">
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
    </VCard> -->
  </VContainer>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useSessionStore } from '@/stores/session'
import { SessionWord, Domain } from "@/models"
import { useRepo } from "pinia-orm"
import { SESSION_TYPES } from "@/const"
import { generateRandomProbability } from '@/utils/helpers'

const { t } = useI18n()
const props = defineProps(['id'])
const router = useRouter()
const sessionStore = useSessionStore()
const sessionWordRepo = useRepo(SessionWord)

const currentWord = ref(null)
const currentIndex = ref(0)
const userAnswer = ref('')
const typeOfTranslation = ref('')
// const showResult = ref(false)
// const isCorrect = ref(false)
// const correctAnswer = ref('')

const currentDomain = computed(() => {
  const domainCode = sessionStore.currentConfig?.domain
  console.log("Current Domain Code:", domainCode, useRepo(Domain).find(domainCode))
  return useRepo(Domain).find(domainCode)
})

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
  if (allWords.value.length === 0) return 0
  return (answeredWords.value.length / allWords.value.length) * 100
})


const getTextToTranslate = computed(() => {
  if (!currentWord.value) return ''

  if (typeOfTranslation.value === 'to') {
    return currentWord.value.translationTo?.text || ''
  } else {
    return currentWord.value.translationFrom?.text || ''
  }
})



const submitAnswer = () => {
  console.log("Submitting answer for word:", userAnswer.value)
  if (!userAnswer.value.trim()) return
  // TODO : 
  // 1. Submit answer to store
  // 2. Check if correct (ie currentWord.translation.text OR synonyms)
  // display result + show correct answer if wrong
  // with button to go to next word


  // correctAnswer.value = currentWord.value.translation?.text || ''
  
  // // Submit answer to store
  // sessionStore.submitAnswer(userAnswer.value)
  
  // // Check if answer was correct
  // const answerRecord = sessionStore.answers[sessionStore.answers.length - 1]
  // isCorrect.value = answerRecord?.correct || false
  
  // showResult.value = true
}

// const skipWord = () => {
//   sessionStore.skipWord()
//   resetInputState()
// }

// const nextWord = () => {
//   resetInputState()
// }

// const resetInputState = () => {
//   userAnswer.value = ''
//   showResult.value = false
//   isCorrect.value = false
//   correctAnswer.value = ''
// }

// const finishSession = async () => {
//   try {
//     await sessionStore.completeSession()
//     router.push('/')
//   } catch (error) {
//     console.error(t('session.failedToComplete'), error)
//     alert(t('session.failedToComplete'))
//   }
// }

const getTypeOfTranslation = () => {
  // TODO call this if MIXED to next words
  const decideRandomTranslationType = () => {
    const rand = generateRandomProbability()
    console.log("Random Probability for mixed session type:", rand)
    return rand < 0.5 ? 'to' : 'from'
  }
  const sessionType = sessionStore.currentConfig?.sessionType
  if (sessionType === SESSION_TYPES.COMPREHENSION) {
    return 'to'
  }
  if (sessionType === SESSION_TYPES.EXPRESSION) {
    return 'from'
  }
  if (sessionType === SESSION_TYPES.MIXED) {
    return decideRandomTranslationType()
  }
}

onMounted(async () => {
  if (!sessionStore.currentSessionId) {
    router.push('/')
  }
  currentWord.value = allWords.value[currentIndex.value]
  typeOfTranslation.value = getTypeOfTranslation()
  console.log("Current Word:", currentWord.value)
})
</script>

<style scoped>

.capitalize-text {
  text-transform: capitalize !important;
}

</style>