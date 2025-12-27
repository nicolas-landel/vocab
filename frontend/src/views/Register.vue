<template>
  <VContainer class="fill-height mt-n15" fluid>
    <VRow align="center" justify="center">
      <VCol :cols="12" sm="8" md="6" lg="4" class="">
        <VCard class="elevation-12">
          <VToolbar color="primary" dark flat>
            <VToolbarTitle>{{ t('register.title') }}</VToolbarTitle>
          </VToolbar>
          <VCardText>
            <VForm ref="registerFormRef" @submit.prevent="handleRegister">
              <VTextField
                v-model="email"
                :label="t('register.email')"
                name="email"
                prepend-icon="mdi-email"
                type="email"
                :rules="[rules.required, rules.email]"
                variant="outlined"
                class="mb-2"
              ></VTextField>
              
              <VTextField
                v-model="username"
                :label="t('register.username')"
                name="username"
                prepend-icon="mdi-account"
                type="text"
                :rules="[rules.required]"
                variant="outlined"
                class="mb-2"
              ></VTextField>

              <VTextField
                v-model="password"
                :label="t('register.password')"
                name="password"
                prepend-icon="mdi-lock"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="showPassword = !showPassword"
                :rules="[rules.required, rules.minLength]"
                variant="outlined"
                class="mb-2"
              ></VTextField>

              <VTextField
                v-model="confirmPassword"
                :label="t('register.confirmPassword')"
                name="confirmPassword"
                prepend-icon="mdi-lock-check"
                :type="showConfirmPassword ? 'text' : 'password'"
                :append-inner-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="showConfirmPassword = !showConfirmPassword"
                :rules="[rules.required, rules.match]"
                variant="outlined"
              ></VTextField>

              <VAlert v-if="error" type="error" class="mb-4">
                {{ error }}
              </VAlert>

              <VAlert v-if="success" type="success" class="mb-4">
                {{ t('register.success') }}
              </VAlert>

              <VBtn
                type="submit"
                color="primary"
                block
                size="large"
                :loading="loading"
                class="mb-4"
              >
                {{ t('register.registerButton') }}
              </VBtn>

              <div class="text-center">
                <span class="text-grey">{{ t('register.hasAccount') }}</span>
                <VBtn
                  variant="text"
                  color="primary"
                  @click="$router.push('/login')"
                  size="small"
                >
                  {{ t('register.login') }}
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

const registerFormRef = ref(null)
const email = ref('')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const loading = ref(false)
const error = ref('')
const success = ref(false)

const rules = {
  required: value => !!value || t('validation.required'),
  email: value => /.+@.+\..+/.test(value) || t('validation.email'),
  minLength: value => value.length >= 8 || t('validation.minLength'),
  match: value => value === password.value || t('validation.passwordMatch')
}

const handleRegister = async () => {
  const { valid } = await registerFormRef.value.validate()
  if (!valid) return

  loading.value = true
  error.value = ''
  success.value = false

  try {
    await authStore.register(email.value, password.value, username.value)
    success.value = true
    // Login automatically and redirect to profile
    await authStore.login(email.value, password.value)
    router.push('/profile')
  } catch (err) {
    error.value = err.response?.data?.detail || t('register.error')
  } finally {
    loading.value = false
  }
}
</script>
