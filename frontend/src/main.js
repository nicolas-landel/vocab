import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { orm } from "./models/index.js";
import router from './router'
import './style.css'
import App from './App.vue'
import i18n from './setup/i18n'
import { vuetify } from './setup/vuetify'

const pinia = createPinia().use(orm)
const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(i18n)
app.use(vuetify)
app.mount('#app')
