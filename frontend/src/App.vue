<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

onMounted(async () => {
  await authStore.initAuth()
})
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<style scoped>
#app {
  width: 100%;
  min-height: 100vh;
}
</style>
