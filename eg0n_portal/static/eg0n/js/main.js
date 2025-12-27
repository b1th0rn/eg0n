// main.js
import { registerMessageStore } from "./stores/message.js";
import { registerUtilsStore } from "./stores/utils.js";
import { attributeCrud } from "./components/attributeCrud.js"

// Wait for Alpine and register components
document.addEventListener("alpine:init", () => {
    registerMessageStore()
    registerUtilsStore()
    Alpine.data("attributeCrud", attributeCrud)
})
