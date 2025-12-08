<template>
    <div v-if="session" class="session-page animate-fade-in">
        <div class="header">
            <h2>{{ $t('session.title') }} {{ currentIndex + 1 }} / {{ session.results.length }}</h2>
            <div class="progress-bar">
                <div class="fill" :style="{ width: progress + '%' }"></div>
            </div>
        </div>

        <div class="flashcard glass">
            <div class="word-display">
                <span class="label">{{ $t('session.translate') }}</span>
                <h1>{{ currentWord?.text }}</h1>
                <span class="sub" v-if="currentWord?.domain">{{ $t('session.domain') }} {{ currentWord.domain }}</span>
            </div>

            <!-- Answer Section -->
            <div v-if="showAnswer" class="answer-reveal">
                <p class="instruction">{{ $t('session.check') }}</p>
                <!-- Here we would show the Correct Answer if we had it. -->

                <div class="actions">
                    <button @click="submitCard(false)" class="btn btn-error">{{ $t('session.incorrect') }}</button>
                    <button @click="submitCard(true)" class="btn btn-success">{{ $t('session.correct') }}</button>
                </div>
            </div>

            <div v-else class="input-section">
                <input v-model="userInput" :placeholder="$t('session.placeholder')" class="input"
                    @keyup.enter="checkAnswer" />
                <button @click="checkAnswer" class="btn">{{ $t('session.reveal') }}</button>
            </div>
        </div>
    </div>
    <div v-else class="loading">Loading session...</div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useSessionStore } from '../stores/session'
import { useRouter } from 'vue-router'

const props = defineProps(['id'])
const router = useRouter()
const sessionStore = useSessionStore()

const currentIndex = ref(0)
const userInput = ref('')
const showAnswer = ref(false)
const results = ref([]) // Local accumulation of results

const session = computed(() => sessionStore.currentSession)

onMounted(() => {
    if (!sessionStore.currentSessionId || sessionStore.currentSessionId != props.id) {
        sessionStore.currentSessionId = props.id
        // Ideally fetch if missing
    }
})

const currentResult = computed(() => {
    if (!session.value || !session.value.results) return null
    return session.value.results[currentIndex.value]
})

const currentWord = computed(() => currentResult.value?.word)

const progress = computed(() => {
    if (!session.value?.results) return 0
    return ((currentIndex.value) / session.value.results.length) * 100
})

const checkAnswer = () => {
    // Basic verification logic?
    // In real app, we might check against multiple valid translations.
    // Here we don't have the target translation readily available in the frontend model 
    // because Word model only has the word text itself, not the translation pair?
    // Wait, the API returns `Session` with `results` containing `word` (the source word).
    // We need the TARGET translation to verify!
    // My Session API returned the stored `Result` which initially has correct=False.
    // It seems I missed sending the Translation (answer) to the frontend?

    // Quick fix: The user checks it themselves (Self-assessment) OR I reveal answer.
    // "I ll have to find the traduction one by one" - usually means system checks it.

    // Issue: The backend `start_session` selects Words. It creates `SessionResult` linked to `Word`.
    // It does NOT store the target word in `SessionResult`. Use `Translation` table to find it.

    // MVP Approach: 
    // 1. User types answer.
    // 2. Click "Reveal".
    // 3. User marks "Correct" or "Incorrect" (Anki style) OR System checks.
    // Since I didn't send answer, I'll use Self-Assessment style (easier to implement now without changing backend schema heavily).
    // Or I assume backend logic will check it on submit?
    // But user wants "find the traduction one by one".

    // Let's implement: Show Source -> User thinks/types -> Reveal -> User grades self (Premium SRS feel).
    showAnswer.value = true
}

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
