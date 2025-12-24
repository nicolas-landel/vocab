<template>
  <VApp>
    <VAppBar color="primary" elevation="0">
      <VAppBarNavIcon @click="drawer = !drawer" class="d-md-none"></VAppBarNavIcon>
      
      <VToolbarTitle class="ml-4">
        <router-link to="/" class="logo text-white text-decoration-none font-weight-bold">
          {{ t('nav.appName') }}
        </router-link>
      </VToolbarTitle>

      <VTabs
        v-if="route.path === '/'"
        :model-value="activeTab"
        @update:model-value="switchTab"
        bg-color="transparent"
        class="ml-8 d-none d-md-flex"
      >
        <VTab value="session">{{ t('tabs.session') }}</VTab>
        <VTab value="vocabulary">{{ t('tabs.vocabulary') }}</VTab>
      </VTabs>

      <VSpacer></VSpacer>

      <div style="width: 180px" class="mr-4 d-none d-md-flex">
        <VSelect
          v-model="nativeLanguage"
          :items="languages"
          item-title="name"
          item-value="code"
          :label="t('nav.nativeLanguage')"
          density="compact"
          variant="outlined"
          hide-details
        ></VSelect>
      </div>

      <VBtn icon @click="goToProfile" class="d-none d-md-flex">
        <VIcon>mdi-account</VIcon>
      </VBtn>

      <VBtn icon @click="handleLogout" class="d-none d-md-flex" :title="t('nav.logout')">
        <VIcon>mdi-logout</VIcon>
      </VBtn>
    </VAppBar>

    <VNavigationDrawer v-model="drawer" temporary>
      <VList>
        <VListItem :title="t('nav.appName')" class="text-h6 font-weight-bold"></VListItem>
        
        <VDivider></VDivider>

        <VListItem v-if="route.path === '/'" @click="switchTabMobile('session')" :class="{ 'bg-primary': activeTab === 'session' }">
          <VListItemTitle>{{ t('tabs.session') }}</VListItemTitle>
        </VListItem>

        <VListItem v-if="route.path === '/'" @click="switchTabMobile('vocabulary')" :class="{ 'bg-primary': activeTab === 'vocabulary' }">
          <VListItemTitle>{{ t('tabs.vocabulary') }}</VListItemTitle>
        </VListItem>

        <VDivider v-if="route.path === '/'"></VDivider>

        <VListItem>
          <VSelect
            v-model="nativeLanguage"
            :items="languages"
            item-title="name"
            item-value="code"
            :label="t('nav.nativeLanguage')"
            density="compact"
            variant="outlined"
            hide-details
            class="mt-4"
          ></VSelect>
        </VListItem>

        <VListItem @click="goToProfileMobile" prepend-icon="mdi-account">
          <VListItemTitle>{{ t('nav.profile') }}</VListItemTitle>
        </VListItem>

        <VListItem @click="handleLogoutMobile" prepend-icon="mdi-logout">
          <VListItemTitle>{{ t('nav.logout') }}</VListItemTitle>
        </VListItem>
      </VList>
    </VNavigationDrawer>

    <VMain>
      <RouterView />
    </VMain>
  </VApp>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useVocabularyStore } from './stores/vocabulary'
import { useAuthStore } from './stores/auth'

const { t, locale } = useI18n()
const router = useRouter()
const route = useRoute()
const vocabularyStore = useVocabularyStore()
const authStore = useAuthStore()

const nativeLanguage = ref('en')
const languages = ref([])
const drawer = ref(false)

// Watch for native language changes and update i18n locale
watch(nativeLanguage, (newLang) => {
  locale.value = newLang
  // Save to localStorage for persistence
  localStorage.setItem('appLanguage', newLang)
  authStore.setUserLanguage(newLang)
}, { immediate: true })

const activeTab = computed(() => route.query.tab || 'session')

const switchTab = (tab) => {
  router.push({ path: '/', query: { tab } })
}

const switchTabMobile = (tab) => {
  router.push({ path: '/', query: { tab } })
  drawer.value = false
}

const goToProfileMobile = () => {
  router.push('/profile')
  drawer.value = false
}

onMounted(async () => {
  try {
    await vocabularyStore.fetchLanguages()
    languages.value = vocabularyStore.languages
    
    // Set from localStorage first, then user profile
    const savedLanguage = localStorage.getItem('appLanguage')
    if (savedLanguage) {
      nativeLanguage.value = savedLanguage
      locale.value = savedLanguage
    } else if (authStore.user?.nativeLanguage) {
      nativeLanguage.value = authStore.user.nativeLanguage
      locale.value = authStore.user.nativeLanguage
    }
  } catch (error) {
    console.error(t('errors.failedToLoadLanguages'), error)
  }
})

const goToProfile = () => {
  router.push('/profile')
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

const handleLogoutMobile = async () => {
  drawer.value = false
  await authStore.logout()
  router.push('/login')
}
</script>

<style>
.logo {
  font-size: 1.5rem;
  letter-spacing: 2px;
}
</style>
