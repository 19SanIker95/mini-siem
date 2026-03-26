const API_BASE = "http://127.0.0.1:8000/api/v1";

export async function getAlerts() {
  const res = await fetch(`${API_BASE}/alerts`);
  if (!res.ok) {
    throw new Error(`Failed to fetch alerts (${res.status})`);
  }
  return res.json();
}