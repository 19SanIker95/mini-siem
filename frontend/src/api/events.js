const API_BASE = "https://mini-siem-6s8m.onrender.com/api/v1";

export async function getEvents({
  limit = 25,
  offset = 0,
  severity = "",
  source = "",
} = {}) {
  const params = new URLSearchParams({
    limit,
    offset,
  });

  if (severity !== "") params.append("min_severity", severity);
  if (source !== "") params.append("source", source);

  const res = await fetch(`${API_BASE}/events?${params.toString()}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch events (${res.status})`);
  }
  return res.json();
}