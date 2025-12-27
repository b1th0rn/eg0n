// stores/message.js
export function registerMessageStore() {
    Alpine.store('message', {
        alerts: [],
        nextId: 1,
        createItem(message) {
            const id = this.nextId++
            this.alerts.push({ id, message })
        },
        deleteItem(id) {
            this.alerts = this.alerts.filter(a => a.id !== id)
        }
    })
}
