<template>
  <div class="app-container">
    <nav class="navbar glass">
      <router-link to="/" class="logo">VOCAB</router-link>
      <div class="links">
        <router-link to="/">Home</router-link>
        <router-link to="/profile">Profile</router-link>
        <div class="lang-switch">
          <button @click="$i18n.locale = 'en'" :class="{ active: $i18n.locale === 'en' }">EN</button>
          <button @click="$i18n.locale = 'fr'" :class="{ active: $i18n.locale === 'fr' }">FR</button>
          <button @click="$i18n.locale = 'es'" :class="{ active: $i18n.locale === 'es' }">ES</button>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <RouterView v-slot="{ Component }">
        <Transition name="fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const goHome = () => router.push('/')
const goProfile = () => router.push('/profile')
</script>



<style scoped>
.app-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  margin-bottom: 32px;
  border-radius: var(--radius);
}

.brand {
  font-weight: 800;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.links {
  display: flex;
  gap: 20px;
  align-items: center;
}

.links a {
  text-decoration: none;
  color: var(--text-color);
  font-weight: 500;
  transition: color 0.3s;
}

.links a:hover,
.links a.router-link-active {
  color: var(--primary-color);
}

.lang-switch {
  display: flex;
  gap: 8px;
  margin-left: 16px;
}

.lang-switch button {
  background: transparent;
  border: 1px solid var(--text-muted);
  color: var(--text-muted);
  padding: 2px 6px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.lang-switch button.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.logo-icon {
  background: var(--primary-color);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  color: white;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 0.9rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
