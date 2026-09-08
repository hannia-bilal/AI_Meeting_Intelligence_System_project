// Thin fetch wrapper for the FastAPI backend described in the project
// spec (MeetingIntelligenceService, to_database_records, pgvector-backed
// Q&A). Swap the mockData.js imports used across the app for these calls
// once the backend is deployed.
//
// Response shapes are documented below with JSDoc typedefs so this file
// stays a useful contract even without full TypeScript. They mirror the
// AI Meeting Intelligence module's Pydantic schemas.

/**
 * @typedef {Object} TimestampReference
 * @property {number} seconds
 * @property {string} formatted - MM:SS
 *
 * @typedef {Object} KeyPoint
 * @property {string} id
 * @property {string} text
 * @property {TimestampReference} timestamp
 *
 * @typedef {Object} Decision
 * @property {string} id
 * @property {string} text
 * @property {string} rationale
 * @property {TimestampReference} timestamp
 *
 * @typedef {Object} ActionItem
 * @property {string} id
 * @property {string} task
 * @property {string} owner
 * @property {string} deadline - ISO-8601 date
 * @property {'low'|'medium'|'high'} priority
 *
 * @typedef {Object} UnresolvedIssue
 * @property {string} id
 * @property {string} text
 * @property {'low'|'medium'|'high'} urgency
 *
 * @typedef {Object} FollowUpItem
 * @property {string} id
 * @property {string} text
 * @property {string} owner
 * @property {string} timeframe
 *
 * @typedef {Object} SpeakerMetric
 * @property {string} label - e.g. SPEAKER_00
 * @property {string} name - resolved real name, if known
 * @property {number} speakingSeconds
 * @property {number} contributionPct
 * @property {number} turns
 *
 * @typedef {Object} Sentiment
 * @property {number} score - -1.0 to +1.0
 * @property {'positive'|'neutral'|'negative'} category
 * @property {string} summary - qualitative tone summary
 *
 * @typedef {Object} MeetingIntelligenceReport
 * @property {string} meetingId
 * @property {string} title
 * @property {string} summaryShort
 * @property {string} summaryDetailed
 * @property {KeyPoint[]} keyPoints
 * @property {Decision[]} decisions
 * @property {ActionItem[]} actionItems
 * @property {UnresolvedIssue[]} unresolved
 * @property {FollowUpItem[]} followUps
 * @property {SpeakerMetric[]} speakers
 * @property {Sentiment} sentiment
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

async function request(path, options = {}) {
  const token = localStorage.getItem('mi_token')

  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })

  if (!response.ok) {
    const message = await response.text().catch(() => response.statusText)
    throw new Error(message || 'Request failed')
  }

  const contentType = response.headers.get('content-type') || ''
  return contentType.includes('application/json') ? response.json() : response.text()
}

export const api = {
  // Auth
  login: (email, password) =>
    request('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  register: (payload) =>
    request('/auth/register', { method: 'POST', body: JSON.stringify(payload) }),
  getProfile: () => request('/auth/me'),
  updateProfile: (payload) =>
    request('/auth/me', { method: 'PATCH', body: JSON.stringify(payload) }),

  // Meetings
  getMeetings: () => request('/meetings'),
  getMeeting: (id) => request(`/meetings/${id}`),
  uploadMeeting: (formData) =>
    request('/meetings/upload', { method: 'POST', body: formData, headers: {} }),
  getProcessingStatus: (id) => request(`/meetings/${id}/status`),

  /** @returns {Promise<MeetingIntelligenceReport>} */
  analyzeMeeting: (id) => request(`/meetings/${id}/analyze`, { method: 'POST' }),

  // Meeting-scoped Q&A (pgvector-backed, per Absar Akbar's module)
  askQuestion: (meetingId, question) =>
    request(`/meetings/${meetingId}/ask`, { method: 'POST', body: JSON.stringify({ question }) }),
  getConversation: (meetingId) => request(`/meetings/${meetingId}/conversation`),

  // Search & history
  search: (query) => request(`/meetings/search?q=${encodeURIComponent(query)}`),
}
