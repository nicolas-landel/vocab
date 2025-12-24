<template>
  <VContainer class="fill-height" fluid>
    <VRow align="center" justify="center">
      <VCol cols="12" class="text-center">
        <VProgressCircular
          indeterminate
          color="primary"
          size="64"
        ></VProgressCircular>
        <div class="text-h6 mt-4">{{ t('auth.processing') }}</div>
      </VCol>
    </VRow>
  </VContainer>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

onMounted(async () => {
  const token = route.query.token
  const firstLogin = route.query.firstLogin === 'true'
  
  if (token) {
    // Store the token
    localStorage.setItem('access_token', token)
    authStore.token = token
    
    // Fetch user data
    try {
      await authStore.fetchUser()
      // Redirect to profile for first-time users, otherwise home
      if (firstLogin) {
        router.push('/profile')
      } else {
        router.push('/')
      }
    } catch (error) {
      console.error('Failed to fetch user:', error)
      router.push('/login')
    }
  } else {
    router.push('/login')
  }
})
</script>
