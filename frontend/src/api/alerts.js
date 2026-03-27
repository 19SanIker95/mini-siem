const API_BASE = "https://mini-siem-6s8m.onrender.com/api/v1";

export async function getAlerts() {
  const res = await fetch(`${API_BASE}/alerts`);
  if (!res.ok) {
    throw new Error(`Failed to fetch alerts (${res.status})`);
  }
  return res.json();
}