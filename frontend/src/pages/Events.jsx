import { useEffect, useState } from "react";
import { getEvents } from "../api/events";
import EventTable from "../components/EventTable";

export default function Events() {
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getEvents({ limit: 25 })
      .then(setEvents)
      .catch(err => setError(err.message));
  }, []);

  if (error) return <p>Erro: {error}</p>;
  if (!events) return <p>Loading events…</p>;

  return (
    <div>
      <h2>Events</h2>
      <EventTable events={events} />
    </div>
  );
}