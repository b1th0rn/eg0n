// stores/message.js
export function registerMessageStore() {
    Alpine.store('message', {
        alerts: [],
        nextId: 1,
        createItem(message, severity = 20, timeout = 5) {
            const id = this.nextId++
            this.alerts.push({ id, message, severity, })

            // Auto-close after timeout
            setTimeout(() => {
                this.deleteItem(id)
            }, timeout * 1000)
        },
        deleteItem(id) {
            this.alerts = this.alerts.filter(a => a.id !== id)
        }
    })
}
