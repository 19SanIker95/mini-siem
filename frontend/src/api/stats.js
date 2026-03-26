const API_BASE = "http://127.0.0.1:8000/api/v1";

export async function getEventStats() {
  const res = await fetch(`${API_BASE}/events/stats`);

  if (!res.ok) {
    throw new Error(`Failed to fetch stats (${res.status})`);
  }

  return res.json();
}