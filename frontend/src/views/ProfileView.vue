<template>
    <div class="profile-page animate-fade-in">
        <h1>Your Profile</h1>

        <div v-if="loading">Loading stats...</div>

        <div v-else-if="stats" class="dashboard-grid">
            <div class="card glass">
                <h3>Progress</h3>
                <div class="big-stat">
                    {{ stats.correct_rate }}%
                    <span>Correct Rate</span>
                </div>
                <div class="detail-stat">
                    {{ stats.total_words_reviewed }} words reviewed
                </div>
            </div>

            <div class="card glass">
                <h3>Focus Words</h3>
                <p class="desc">Words you struggle with:</p>
                <ul class="weak-list" v-if="stats.weakest_words.length">
                    <li v-for="word in stats.weakest_words" :key="word">{{ word }}</li>
                </ul>
                <p v-else class="empty">Great job! No weak words found yet.</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const stats = ref(null)
const loading = ref(true)

onMounted(async () => {
    try {
        const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
        const res = await axios.get(`${API_URL}/profile`)
        stats.value = res.data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
})
</script>


<style scoped>
.dashboard-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;
}

.big-stat {
    font-size: 3rem;
    font-weight: 800;
    color: var(--primary-color);
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 16px 0;
}

.big-stat span {
    font-size: 0.9rem;
    color: var(--text-muted);
    font-weight: 500;
}

.detail-stat {
    text-align: center;
    color: var(--text-color);
    font-weight: 500;
}

.weak-list {
    list-style: none;
    padding: 0;
}

.weak-list li {
    padding: 8px 12px;
    background: rgba(239, 68, 68, 0.1);
    color: #fca5a5;
    margin-bottom: 8px;
    border-radius: 8px;
    border: 1px solid rgba(239, 68, 68, 0.2);
}

.desc {
    color: var(--text-muted);
    margin-bottom: 16px;
}

.empty {
    color: var(--success);
    font-style: italic;
}
</style>
