<template>
    <div class="config-page animate-fade-in">
        <h1>{{ $t('config.title') }}</h1>

        <div class="card glass">
            <label>{{ $t('config.source') }}</label>
            <select v-model="form.source_lang_code" class="select">
                <option v-for="l in languages" :key="l.code" :value="l.code">{{ l.name }}</option>
            </select>

            <label>{{ $t('config.target') }}</label>
            <select v-model="form.target_lang_code" class="select">
                <option v-for="l in languages" :key="l.code + 't'" :value="l.code">{{ l.name }}</option>
            </select>

            <label>{{ $t('config.domain') }}</label>
            <select v-model="form.domain" class="select">
                <option v-for="d in domains" :key="d" :value="d">{{ d }}</option>
            </select>

            <label>{{ $t('config.difficulty') }}</label>
            <select v-model="form.difficulty" class="select">
                <option v-for="d in difficulties" :key="d" :value="d">{{ d }}</option>
            </select>

            <label>{{ $t('config.type') }}</label>
            <select v-model="form.session_type" class="select">
                <option value="comprehension">Comprehension</option>
                <option value="expression">Expression</option>
            </select>

            <button @click="start" class="btn" :disabled="loading" style="width: 100%; margin-top: 20px;">
                {{ loading ? $t('config.starting') : $t('config.start') }}
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/setup/axios'
import { useRouter } from 'vue-router'
import { useSessionStore } from '@/stores/session'

const router = useRouter()
const sessionStore = useSessionStore()

const languages = ref([])
const domains = ref([])
const difficulties = ref([])

const form = ref({
    sourceLangCode: 'fr',
    targetLangCode: 'es',
    domain: '',
    difficulty: 'easy', // lowercase match enum in seeded data? Seed used Enum value.
    sessionType: 'comprehension'
})

const loading = ref(false)

onMounted(async () => {
    try {
        const [langRes, domRes, diffRes] = await Promise.all([
            apiClient.get('/config/languages'),
            apiClient.get('/config/domains'),
            apiClient.get('/config/difficulties')
        ])
        languages.value = langRes.data
        domains.value = domRes.data
        difficulties.value = diffRes.data

        // Default domain
        if (domains.value.length > 0) form.value.domain = domains.value[0]
    } catch (e) {
        console.error("Failed to load config", e)
    }
})

const start = async () => {
    loading.value = true
    try {
        const id = await sessionStore.startSession(form.value)
        router.push({ name: 'Session', params: { id } })
    } catch (e) {
        alert("Failed to start session: " + e.message)
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--text-muted);
}
</style>
