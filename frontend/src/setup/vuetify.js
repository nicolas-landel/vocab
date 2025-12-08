import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

export const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'dark', // Matching premium dark mode requested earlier
    themes: {
      dark: {
        colors: {
          primary: '#6366f1', // Indigo 500
          secondary: '#8b5cf6', // Violet 500
          success: '#10b981',
          error: '#ef4444',
          background: '#0f172a',
          surface: '#1e293b',
        }
      }
    }
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})
