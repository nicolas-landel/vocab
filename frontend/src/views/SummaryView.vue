<template>
    <div class="summary-page animate-fade-in" v-if="session">
        <div class="card glass text-center">
            <h2>{{ $t('summary.title') }}</h2>

            <div class="score-circle">
                <span class="score">{{ score }}%</span>
            </div>

            <div class="stats-grid">
                <div class="stat">
                    <span class="val">{{ session.results.length }}</span>
                    <span class="lbl">{{ $t('summary.words') }}</span>
                </div>
                <div class="stat">
                    <span class="val">{{session.results.filter(r => r.correct).length}}</span>
                    <span class="lbl">{{ $t('summary.correct') }}</span>
                </div>
            </div>

            <button @click="goHome" class="btn" style="margin-top: 32px;">{{ $t('summary.new_session') }}</button>
        </div>
    </div>
    <div v-else>Loading... (or Session Not Found)</div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useSessionStore } from '../stores/session'
import { useRouter } from 'vue-router'

const props = defineProps(['id'])
const router = useRouter()
const sessionStore = useSessionStore()

const session = computed(() => sessionStore.currentSession)
// If page reloaded, sessionStore might be empty for ID? 
// Store logic checks `currentSessionId`. 
// If props.id != currentSessionId, we might need to fetch from API (not implemented in store yet for retrieval).
// For MVP assuming single session flow.

const score = computed(() => session.value?.score ?? 0)

const goHome = () => router.push('/')
</script>

<style scoped>
.text-center {
    text-align: center;
}

.score-circle {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 4px solid var(--primary-color);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 32px auto;
    background: rgba(99, 102, 241, 0.1);
}

.score {
    font-size: 2.5rem;
    font-weight: 800;
}

.stats-grid {
    display: flex;
    justify-content: center;
    gap: 32px;
}

.stat {
    display: flex;
    flex-direction: column;
}

.val {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-color);
}

.lbl {
    font-size: 0.8rem;
    color: var(--text-muted);
    text-transform: uppercase;
}
</style>
