<template>
  <v-container>
    <v-card v-if="!sessionStore.isSessionComplete" max-width="800" class="mx-auto">
      <!-- Progress -->
      <v-card-title>
        <div class="d-flex justify-space-between align-center w-100">
          <span>Session Progress</span>
          <span class="text-body-1">
            {{ sessionStore.currentWordIndex + 1 }} / {{ sessionStore.totalWords }}
          </span>
        </div>
      </v-card-title>

      <v-progress-linear
        :model-value="progress"
        color="primary"
        height="8"
      ></v-progress-linear>

      <v-card-text class="pt-8">
        <v-row v-if="sessionStore.currentWord">
          <!-- Word to translate -->
          <v-col cols="12" class="text-center">
            <div class="text-subtitle-1 text-grey mb-2">Translate this word:</div>
            <div class="text-h3 mb-6">{{ sessionStore.currentWord.text }}</div>
            
            <div v-if="sessionStore.currentWord.masterWord?.domain" class="mb-4">
              <v-chip color="primary" variant="outlined">
                {{ sessionStore.currentWord.masterWord.domain.name }}
              </v-chip>
            </div>
          </v-col>

          <!-- Answer Input -->
          <v-col cols="12">
            <v-text-field
              v-model="userAnswer"
              label="Your answer"
              variant="outlined"
              size="large"
              autofocus
              @keyup.enter="submitAnswer"
              :disabled="showResult"
            ></v-text-field>
          </v-col>

          <!-- Result Display -->
          <v-col cols="12" v-if="showResult">
            <v-alert
              :type="isCorrect ? 'success' : 'error'"
              :icon="isCorrect ? 'mdi-check-circle' : 'mdi-close-circle'"
              prominent
            >
              <div class="text-h6">{{ isCorrect ? 'Correct!' : 'Incorrect' }}</div>
              <div v-if="!isCorrect" class="mt-2">
                Correct answer: <strong>{{ correctAnswer }}</strong>
              </div>
            </v-alert>
          </v-col>

          <!-- Action Buttons -->
          <v-col cols="12">
            <div class="d-flex gap-2">
              <v-btn
                v-if="!showResult"
                color="warning"
                variant="outlined"
                @click="skipWord"
                block
              >
                I forgot
              </v-btn>
              
              <v-btn
                v-if="!showResult"
                color="primary"
                @click="submitAnswer"
                :disabled="!userAnswer"
                block
              >
                Check Answer
              </v-btn>

              <v-btn
                v-if="showResult"
                color="primary"
                @click="nextWord"
                block
              >
                Next Word
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Session Complete -->
    <v-card v-else max-width="800" class="mx-auto">
      <v-card-title class="text-center">Session Complete!</v-card-title>
      <v-card-text>
        <div class="text-center mb-6">
          <div class="text-h2 mb-4">{{ sessionStore.sessionResults?.successRate }}%</div>
          <div class="text-subtitle-1 text-grey">Success Rate</div>
        </div>

        <v-row>
          <v-col cols="12" md="6">
            <v-card variant="outlined" color="success">
              <v-card-text class="text-center">
                <div class="text-h4">{{ sessionStore.sessionResults?.correctFirstTime?.length || 0 }}</div>
                <div class="text-subtitle-2">Correct First Try</div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card variant="outlined" color="error">
              <v-card-text class="text-center">
                <div class="text-h4">{{ sessionStore.sessionResults?.failed?.length || 0 }}</div>
                <div class="text-subtitle-2">Needs Practice</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <div class="d-flex gap-2 mt-6">
          <v-btn color="primary" @click="finishSession" block>
            Finish
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSessionStore } from '@/stores/session'

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
  // Assuming the word has the correct translation available
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
    console.error('Failed to complete session:', error)
    alert('Failed to save session results.')
  }
}
</script>

const submitCard = (correct) => {
    results.value.push({
        word_id: currentWord.value.id,
        correct: correct
    })

    userInput.value = ''
    showAnswer.value = false

    if (currentIndex.value < session.value.results.length - 1) {
        currentIndex.value++
    } else {
        finishSession()
    }
}

const finishSession = async () => {
    await sessionStore.submitResults(results.value)
    router.push({ name: 'Summary', params: { id: props.id } })
}
</script>

<style scoped>
.header {
    margin-bottom: 24px;
}

.progress-bar {
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    overflow: hidden;
    margin-top: 8px;
}

.fill {
    height: 100%;
    background: var(--success);
    transition: width 0.3s ease;
}

.flashcard {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 300px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.word-display h1 {
    font-size: 3rem;
    margin: 16px 0;
    background: linear-gradient(to right, var(--text-color), var(--primary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.label {
    text-transform: uppercase;
    font-size: 0.8rem;
    letter-spacing: 1px;
    color: var(--text-muted);
}

.actions {
    display: flex;
    gap: 16px;
    margin-top: 24px;
}

.btn-success {
    background: var(--success);
}

.btn-error {
    background: var(--error);
}

.input-section {
    width: 100%;
    max-width: 300px;
}
</style>
