/**
 * PodiumHQ Unified API Client
 * Uses relative `/api` paths with robust error envelope extraction.
 */

const handleResponse = async (response) => {
  if (response.status === 204) {
    return null;
  }
  const contentType = response.headers.get('content-type') || '';
  if (!response.ok) {
    let errorDetail = `HTTP ${response.status} ${response.statusText}`;
    if (contentType.includes('application/json')) {
      try {
        const errorData = await response.json();
        errorDetail = errorData.detail || JSON.stringify(errorData);
      } catch {
        // use default errorDetail
      }
    } else {
      const text = await response.text();
      if (text) errorDetail = text;
    }
    throw new Error(errorDetail);
  }
  if (contentType.includes('application/json')) {
    return response.json();
  }
  return response.text();
};

export const api = {
  // Events
  async getEvents(status = null, search = '', page = 1, pageSize = 20) {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (search) params.append('search', search);
    params.append('page', page);
    params.append('page_size', pageSize);
    const res = await fetch(`/api/events?${params.toString()}`);
    return handleResponse(res);
  },

  async getEvent(id) {
    const res = await fetch(`/api/events/${id}`);
    return handleResponse(res);
  },

  async createEvent(payload) {
    const res = await fetch('/api/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  // Teams
  async getTeams({ eventId, status, track, search, page = 1, pageSize = 10 } = {}) {
    const params = new URLSearchParams();
    if (eventId) params.append('event_id', eventId);
    if (status) params.append('status', status);
    if (track) params.append('track', track);
    if (search) params.append('search', search);
    params.append('page', page);
    params.append('page_size', pageSize);
    const res = await fetch(`/api/teams?${params.toString()}`);
    return handleResponse(res);
  },

  async getTeam(id) {
    const res = await fetch(`/api/teams/${id}`);
    return handleResponse(res);
  },

  async createTeam(payload) {
    const res = await fetch('/api/teams', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  async updateTeam(id, payload) {
    const res = await fetch(`/api/teams/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  async updateTeamStatus(id, status) {
    const res = await fetch(`/api/teams/${id}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    return handleResponse(res);
  },

  async deleteTeam(id) {
    const res = await fetch(`/api/teams/${id}`, {
      method: 'DELETE',
    });
    return handleResponse(res);
  },

  async getTeamStats(eventId = null) {
    const url = eventId ? `/api/teams/stats?event_id=${eventId}` : '/api/teams/stats';
    const res = await fetch(url);
    return handleResponse(res);
  },

  // Judges, Rounds, Criteria
  async getJudges(activeOnly = true) {
    const res = await fetch(`/api/judges?active_only=${activeOnly}`);
    return handleResponse(res);
  },

  async getRounds(eventId = null) {
    const url = eventId ? `/api/rounds?event_id=${eventId}` : '/api/rounds';
    const res = await fetch(url);
    return handleResponse(res);
  },

  async getCriteria(roundId = null) {
    const url = roundId ? `/api/criteria?round_id=${roundId}` : '/api/criteria';
    const res = await fetch(url);
    return handleResponse(res);
  },

  // Scores
  async submitScore(payload) {
    const res = await fetch('/api/scores', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  async submitBatchScores(payload) {
    const res = await fetch('/api/scores/batch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  // Leaderboard
  async getLeaderboard(eventId = null, eventSlug = null) {
    const params = new URLSearchParams();
    if (eventId) params.append('event_id', eventId);
    if (eventSlug) params.append('event_slug', eventSlug);
    const res = await fetch(`/api/leaderboard?${params.toString()}`);
    return handleResponse(res);
  },

  // Operations Telemetry
  async getHealth() {
    const res = await fetch('/health');
    return handleResponse(res);
  },

  async getReadiness() {
    const res = await fetch('/ready');
    return handleResponse(res);
  },

  async getMetrics() {
    const res = await fetch('/metrics');
    return handleResponse(res);
  },
};
