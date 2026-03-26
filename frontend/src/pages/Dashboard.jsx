import { useEffect, useState } from "react";
import { getEventStats } from "../api/stats";
import StatCard from "../components/StatCard";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getEventStats()
      .then(setStats)
      .catch(err => setError(err.message));
  }, []);

  if (error) return <p>Erro: {error}</p>;
  if (!stats) return <p>Loading dashboard…</p>;

  return (
    <div>
      <h2>Dashboard</h2>

      <div style={{ display: "flex", gap: 16, marginBottom: 20 }}>
        <StatCard title="Total Events" value={stats.total} />
        <StatCard
          title="Auth Events"
          value={stats.by_event_type.authentication || 0}
        />
        <StatCard
          title="Network Events"
          value={stats.by_event_type.network || 0}
        />
        <StatCard
          title="Process Events"
          value={stats.by_event_type.process || 0}
        />
      </div>
    </div>
  );
}