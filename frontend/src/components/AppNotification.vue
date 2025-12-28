<template>
  <VSnackbar
    v-model="show"
    :color="color"
    :timeout="timeout"
    location="bottom"
    multi-line
  >
    <div class="d-flex align-center justify-space-between">
      <div>
        <div v-if="title" class="text-subtitle-1 font-weight-medium mb-1">
          {{ title }}
        </div>
        <div>{{ message }}</div>
      </div>
      <VBtn
        icon="mdi-close"
        variant="text"
        size="small"
        @click="close"
      ></VBtn>
    </div>
  </VSnackbar>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useNotificationsStore } from '@/stores/notification'

const notificationsStore = useNotificationsStore()

const show = ref(false)
const message = ref('')
const title = ref('')
const type = ref('info')
const timeout = ref(6000)

const color = computed(() => {
  switch (type.value) {
    case 'success':
      return 'success'
    case 'error':
      return 'error'
    case 'warning':
      return 'warning'
    default:
      return 'info'
  }
})

const lastNotification = computed(() => notificationsStore.getLastNotification)

watch(lastNotification, (notification) => {
  if (!notification) return
  
  message.value = notification.message || notification.text || ''
  title.value = notification.title || ''
  type.value = notification.type || 'info'
  timeout.value = notification.timeout ?? 6000
  show.value = true
  
  notificationsStore.setLastNotification(null)
})

const close = () => {
  show.value = false
}
</script>
