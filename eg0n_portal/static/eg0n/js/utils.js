// utils.js
const API_BASE = '/api' // Modifica con la base della tua API

function getCsrfToken() {
    // Load and return CSRF token
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content')
}

function buildResponse({ ok, response, url, data = null, traceback = '' }) {
    // Return a standard response
    return {
        status: ok ? 'success' : 'error',
        http: {
            code: response?.status ?? 0,
            message: response?.statusText ?? 'Network Error',
            url
        },
        type: 'response',
        data,
        traceback
    }
}
async function parseJson(response) {
    // Convert reponse to JSON
    const contentType = response.headers.get('content-type') || ''
    if (contentType.includes('application/json')) {
        try {
            return await response.json()
        } catch {
            return null
        }
    }
    return null
}

export const api = {
    // Handle API requests

    async delete(endpoint) {
        // DELETE wrapper
        return this._request('DELETE', endpoint)
    },

    async get(endpoint) {
        // GET wrapper
        return this._request('GET', endpoint)
    },

    async patch(endpoint, body) {
        // PATCH wrapper
        return this._request('PATCH', endpoint, body)
    },

    async post(endpoint, body) {
        // POST wrapper
        return this._request('POST', endpoint, body)
    },

    async put(endpoint, body) {
        // PUT wrapper
        return this._request('PUT', endpoint, body)
    },

    async _request(method, endpoint, payload = null) {
        // Send an API request with automatic token and response handling
        const external_endpoint = endpoint.startsWith('https://')
        const options = {
            method,
            headers: {
                'Accept': 'application/json',
            }
        }

        if (payload) {
            // A payload must be sent
            options.headers['Content-Type'] = 'application/json'
            if (!external_endpoint) options.headers['X-CSRFToken'] = getCsrfToken()
            options.body = JSON.stringify(payload)
        }

        if (!external_endpoint) {
            endpoint = API_BASE + endpoint
        }

        try {
            const response = await fetch(endpoint, options)
            const data = await parseJson(response)
            if (response.ok) {
                // Success
                console.log(`✅ API ${method} ${endpoint} ${response.status} success`, data)
                return buildResponse({
                    ok: true,
                    response,
                    endpoint,
                    data
                })
            } else if (response.status >= 400 && response.status < 500) {
                // Client error
                console.error(`⚠️ API client error ${method} ${endpoint} ${response.status}`, data)
                return buildResponse({
                    ok: false,
                    response,
                    endpoint,
                    data
                })
            }
            // Server error (Fallback)
            console.error(`🔥 API Server error ${method} ${endpoint} ${response.status}`, data)
            return buildResponse({
                ok: false,
                response,
                endpoint,
                data
            })
        } catch (err) {
            console.error(`❌ API ${method} ${endpoint} network error:`, err)
            return {
                status: 'error',
                http: {
                    code: 0,
                    message: 'network error',
                    endpoint
                },
                type: 'response',
                data: null,
                traceback: err?.message || ''
            }
        }
    }
}
