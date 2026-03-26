import { useEffect, useState } from "react";
import { getAlerts } from "../api/alerts";
import AlertTable from "../components/AlertTable";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getAlerts()
      .then(setAlerts)
      .catch(err => setError(err.message));
  }, []);

  if (error) return <p>Erro: {error}</p>;
  if (!alerts) return <p>Loading alerts…</p>;

  return (
    <div>
      <h2>Alerts</h2>
      <AlertTable alerts={alerts} />
    </div>
  );
}