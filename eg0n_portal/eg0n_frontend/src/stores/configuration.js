import { defineStore } from "pinia";

export const useConfigurationStore = defineStore("configuration", {
  state: () => {
    return;
    {
      ("");
      ("");
    }
  },

  actions: {
    setContextName(value) {
      this.contextName = value;
    },

    setCsrfToken(value) {
      this.csrfToken = value;
    },
  },
});
