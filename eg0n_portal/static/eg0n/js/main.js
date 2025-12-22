import { attributeCrud } from "./components/attributeCrud.js"

// Wait for Alpine and register components
document.addEventListener("alpine:init", () => {
    Alpine.data("attributeCrud", attributeCrud)
})
