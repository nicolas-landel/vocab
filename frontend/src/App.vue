<template>
  <v-app>
    <v-app-bar color="primary" elevation="0">
      <v-toolbar-title class="ml-4">
        <router-link to="/" class="logo text-white text-decoration-none font-weight-bold">
          VOCAB
        </router-link>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-select
        v-model="nativeLanguage"
        :items="languages"
        item-title="name"
        item-value="code"
        label="Native Language"
        density="compact"
        variant="outlined"
        style="max-width: 200px"
        class="mr-4"
        hide-details
      ></v-select>

      <v-btn icon @click="goToProfile">
        <v-icon>mdi-account</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useVocabularyStore } from './stores/vocabulary'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const vocabularyStore = useVocabularyStore()
const authStore = useAuthStore()

const nativeLanguage = ref('fr')
const languages = ref([])

onMounted(async () => {
  try {
    await vocabularyStore.fetchLanguages()
    languages.value = vocabularyStore.languages
    
    // Set from user profile if available
    if (authStore.user?.nativeLanguage) {
      nativeLanguage.value = authStore.user.nativeLanguage
    }
  } catch (error) {
    console.error('Failed to load languages:', error)
  }
})

const goToProfile = () => {
  router.push('/profile')
}
</script>

<style>
.logo {
  font-size: 1.5rem;
  letter-spacing: 2px;
}
</style>
