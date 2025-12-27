<template>
  <VContainer class="fill-height mt-n15" fluid>
    <VRow align="center" justify="center" class="">
      <VCol :cols="12" sm="8" md="6" lg="4" class="">
        <VCard class="elevation-12">
          <VToolbar color="primary" dark flat>
            <VToolbarTitle>{{ t('login.title') }}</VToolbarTitle>
          </VToolbar>
          <VCardText class="pa-3">
            <VForm ref="loginFormRef" @submit.prevent="handleLogin">
              <VTextField
                v-model="email"
                :label="t('login.email')"
                name="email"
                prepend-icon="mdi-email"
                type="email"
                :rules="[rules.required, rules.email]"
                variant="outlined"
                class="mb-2"
              ></VTextField>

              <VTextField
                v-model="password"
                :label="t('login.password')"
                name="password"
                prepend-icon="mdi-lock"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="showPassword = !showPassword"
                :rules="[rules.required]"
                variant="outlined"
              ></VTextField>

              <VAlert v-if="error" type="error" class="mb-4">
                {{ error }}
              </VAlert>

              <VBtn
                type="submit"
                color="primary"
                block
                size="large"
                :loading="loading"
                class="mb-4"
              >
                {{ t('login.loginButton') }}
              </VBtn>

              <VDivider class="my-4"></VDivider>

              <VBtn
                color="white"
                variant="outlined"
                block
                size="large"
                @click="loginWithGoogle"
                class="google-btn"
              >
                <VIcon start>mdi-google</VIcon>
                {{ t('login.googleLogin') }}
              </VBtn>

              <div class="text-center mt-4">
                <span class="text-grey">{{ t('login.noAccount') }}</span>
                <VBtn
                  variant="text"
                  color="primary"
                  @click="$router.push('/register')"
                  size="small"
                >
                  {{ t('login.register') }}
                </VBtn>
              </div>
            </VForm>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>
  </VContainer>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const router = useRouter()
const authStore = useAuthStore()

const loginFormRef = ref(null)
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const rules = {
  required: value => !!value || t('validation.required'),
  email: value => /.+@.+\..+/.test(value) || t('validation.email')
}

const handleLogin = async () => {
  const { valid } = await loginFormRef.value.validate()
  if (!valid) return

  loading.value = true
  error.value = ''

  try {
    await authStore.login(email.value, password.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || t('login.error')
  } finally {
    loading.value = false
  }
}

const loginWithGoogle = () => {
  window.location.href = `${import.meta.env.VITE_API_URL}/api/v1/auth/google/login`
}
</script>

<style scoped>
.google-btn {
  text-transform: none;
  font-weight: 500;
}
</style>
