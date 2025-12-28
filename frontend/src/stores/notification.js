import { defineStore } from "pinia";

export const useNotificationsStore = defineStore("notifications", {
  state: () => ({
    lastNotification: null,
  }),

  getters: {
    getLastNotification: (state) => state.lastNotification,
  },

  actions: {
    notify({ message, title, type = 'info', timeout = 6000 }) {
      this.lastNotification = {
        message,
        title,
        type,
        timeout
      };
    },

    showSuccessNotification(message, title) {
      this.notify({
        message,
        title,
        type: 'success',
        timeout: 3000
      });
    },

    showErrorNotification(message, title) {
      this.notify({
        message,
        title,
        type: 'error',
        timeout: 5000
      });
    },

    showWarningNotification(message, title) {
      this.notify({
        message,
        title,
        type: 'warning',
        timeout: 4000
      });
    },

    setLastNotification(notification) {
      this.lastNotification = notification;
    },
  },
});
