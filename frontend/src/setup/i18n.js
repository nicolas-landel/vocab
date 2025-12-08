import { createI18n } from 'vue-i18n'
import en from '@/locales/en.json'
import fr from '@/locales/fr.json'
import es from '@/locales/es.json'

const messages = {
  en: {
    $vuetify: en.$vuetify,
    ...en,
  },
  fr: {
    $vuetify: fr.$vuetify,
    ...fr,
  },
  es: {
    $vuetify: es.$vuetify,
    ...es,
  },
};


const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: messages,
  silentFallbackWarn: true,
  missingWarn: false,
  fallbackWarn: false,
})

export default i18n


