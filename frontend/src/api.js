/**
 * CareerPilot AI — API service
 * Wraps fetch/SSE calls to the FastAPI backend.
 */

const BASE = '/api'

// ── REST helpers ────────────────────────────────────────────

async function post(path, body) {
    const res = await fetch(`${BASE}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    })
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }))
        throw new Error(err.detail || `HTTP ${res.status}`)
    }
    return res.json()
}

async function get(path) {
    const res = await fetch(`${BASE}${path}`)
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }))
        throw new Error(err.detail || `HTTP ${res.status}`)
    }
    return res.json()
}

// ── SSE helper ───────────────────────────────────────────────
/**
 * Connect to an SSE endpoint using the native EventSource API.
 * onEvent receives a parsed JS object.
 * Returns a cleanup function to close the stream.
 */
export function subscribeSSE(path, onEvent, onError) {
    const es = new EventSource(`${BASE}${path}`)

    es.onmessage = (e) => {
        try {
            const parsed = JSON.parse(e.data)
            onEvent(parsed)
        } catch {
            // non-JSON line — ignore
        }
    }

    es.onerror = (e) => {
        // EventSource fires onerror on normal stream close too
        // Only treat as error if it was open before
        if (es.readyState === EventSource.CLOSED) return
        es.close()
        onError(new Error('SSE connection error'))
    }

    return () => es.close()
}


// ── API calls ────────────────────────────────────────────────

export const api = {
    /** POST /api/start — parse career goal, create session */
    start: (userInput) => post('/start', { user_input: userInput }),

    /** GET /api/session/:id — full session state */
    session: (sessionId) => get(`/session/${sessionId}`),

    /** POST /api/submit-answers/:id — store user answers */
    submitAnswers: (sessionId, answers) =>
        post(`/submit-answers/${sessionId}`, { answers }),

    /** Health check */
    health: () => get('/health'),
}
