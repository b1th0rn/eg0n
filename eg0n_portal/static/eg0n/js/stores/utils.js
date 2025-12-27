// stores/message.js
import { severityToClass, severityToIcon } from "../utils.js"


export function registerUtilsStore() {
    Alpine.store('utils', {
        severityToClass,
        severityToIcon
    })
}
