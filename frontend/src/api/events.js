const API_BASE = "http://127.0.0.1:8000/api/v1";

export async function getEvents({ limit = 20, offset = 0 } = {}) {
  const res = await fetch(`${API_BASE}/events?limit=${limit}&offset=${offset}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch events (${res.status})`);
  }
  return res.json();
}