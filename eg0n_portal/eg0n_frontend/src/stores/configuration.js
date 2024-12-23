import { defineStore } from 'pinia'

export const useConfigurationStore = defineStore('configuration', 
  {
  state: () => {
    return 
      {
        contextName : "";
        csrfToken : ""  
      }  
  },
  
  actions: {
    setContextName(value) {
      this.contextName = value;
    },

    setCsrfToken (value) {
      this.csrfToken = value;
    }
  },
})
