<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="dashboard">
    <nav class="navbar">
      <h1>Vocab App</h1>
      <div class="user-info">
        <span>{{ authStore.currentUser?.email }}</span>
        <button @click="handleLogout" class="btn-logout">Logout</button>
      </div>
    </nav>

    <main class="main-content">
      <h2>Welcome to your Dashboard!</h2>
      <p>Start building your vocabulary learning features here.</p>
    </main>
  </div>
</template>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #f5f5f5;
}

.navbar {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar h1 {
  color: #42b883;
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info span {
  color: #666;
}

.btn-logout {
  padding: 0.5rem 1rem;
  background: #ff6b6b;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-logout:hover {
  background: #ee5a52;
}

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  color: #333;
  margin-bottom: 1rem;
}

p {
  color: #666;
  font-size: 1.1rem;
}
</style>
