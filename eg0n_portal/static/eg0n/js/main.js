// main.js
import { registerMessageStore } from "./stores/message.js";
import { attributeCrud } from "./components/attributeCrud.js"

// Wait for Alpine and register components
document.addEventListener("alpine:init", () => {
    registerMessageStore()
    Alpine.data("attributeCrud", attributeCrud)
})
