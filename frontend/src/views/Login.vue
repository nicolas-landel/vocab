<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const isRegister = ref(false)
const error = ref('')
const loading = ref(false)

const handleSubmit = async () => {
  error.value = ''
  loading.value = true

  const result = isRegister.value
    ? await authStore.register(email.value, password.value)
    : await authStore.login(email.value, password.value)

  loading.value = false

  if (result.success) {
    router.push('/dashboard')
  } else {
    error.value = result.error
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-box">
      <h2>{{ isRegister ? 'Create Account' : 'Sign In' }}</h2>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="your@email.com"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="••••••••"
          />
        </div>

        <div v-if="error" class="error">{{ error }}</div>

        <button type="submit" :disabled="loading" class="btn-primary">
          {{ loading ? 'Loading...' : isRegister ? 'Sign Up' : 'Sign In' }}
        </button>
      </form>

      <p class="toggle-mode">
        {{ isRegister ? 'Already have an account?' : "Don't have an account?" }}
        <a @click="isRegister = !isRegister">
          {{ isRegister ? 'Sign In' : 'Sign Up' }}
        </a>
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f5f5f5;
}

.login-box {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #42b883;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #42b883;
}

.error {
  padding: 0.75rem;
  background: #fee;
  color: #c33;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background: #35a372;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toggle-mode {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.toggle-mode a {
  color: #42b883;
  cursor: pointer;
  text-decoration: underline;
  margin-left: 0.25rem;
}
</style>
