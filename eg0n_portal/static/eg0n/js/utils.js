// utils.js
const API_BASE = '/api' // Django API prefix

export function severityToClass(sev) {
    // Integer to string severity converter
    return {
        40: 'alert-danger',
        30: 'alert-warning',
        25: 'alert-success',
        20: 'alert-info',
    }[sev] ?? ''
}

export function severityToIcon(sev) {
    // Integer to SVG severity converter
    return {
        40: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon alert-icon icon-2">
                    <path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0"></path>
                    <path d="M12 8v4"></path>
                    <path d="M12 16h.01"></path>
                </svg>`,
        30: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon alert-icon icon-2">
                <path d="M12 9v4"></path>
                <path d="M10.363 3.591l-8.106 13.534a1.914 1.914 0 0 0 1.636 2.871h16.214a1.914 1.914 0 0 0 1.636 -2.87l-8.106 -13.536a1.914 1.914 0 0 0 -3.274 0z"></path>
                <path d="M12 16h.01"></path>
            </svg>`,
        25: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon alert-icon icon-2">
                <path d="M5 12l5 5l10 -10"></path>
            </svg>`,
        20: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon alert-icon icon-2">
                <path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0"></path>
                <path d="M12 9h.01"></path>
                <path d="M11 12h1v4h1"></path>
            </svg>`,
    }[sev] ?? ''
}


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
