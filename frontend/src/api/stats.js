const API_BASE = "https://mini-siem-6s8m.onrender.com/api/v1";

export async function getEventStats() {
  const res = await fetch(`${API_BASE}/events/stats`);

  if (!res.ok) {
    throw new Error(`Failed to fetch stats (${res.status})`);
  }

  return res.json();
}