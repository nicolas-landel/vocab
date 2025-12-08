import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createORM } from 'pinia-orm'
import router from './router'
import './style.css'
import App from './App.vue'
import i18n from './setup/i18n'
import apiClient from './setup/axios'
import { vuetify } from './setup/vuetify'

const pinia = createPinia().use(createORM())
const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(i18n)
app.use(vuetify)
app.mount('#app')
