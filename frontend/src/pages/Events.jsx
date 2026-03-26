import { useEffect, useState } from "react";
import { getEvents } from "../api/events";
import EventTable from "../components/EventTable";

const PAGE_SIZE = 25;

export default function Events() {
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);

  const [offset, setOffset] = useState(0);
  const [severity, setSeverity] = useState("");
  const [source, setSource] = useState("");

  useEffect(() => {
    getEvents({
      limit: PAGE_SIZE,
      offset,
      severity,
      source,
    })
      .then(setEvents)
      .catch(err => setError(err.message));
  }, [offset, severity, source]);

  if (error) return <p>Erro: {error}</p>;

  return (
    <div>
      <h2>Events</h2>

      {/* Filters */}
      <div style={{ display: "flex", gap: 12, marginBottom: 16 }}>
        <label>
          Severity ≥{" "}
          <select
            value={severity}
            onChange={e => {
              setOffset(0);
              setSeverity(e.target.value);
            }}
          >
            <option value="">All</option>
            <option value="1">1+</option>
            <option value="2">2+</option>
            <option value="3">3+</option>
            <option value="4">4+</option>
            <option value="5">5+</option>
          </select>
        </label>

        <label>
          Source{" "}
          <select
            value={source}
            onChange={e => {
              setOffset(0);
              setSource(e.target.value);
            }}
          >
            <option value="">All</option>
            <option value="linux">linux</option>
            <option value="windows">windows</option>
            <option value="app">app</option>
          </select>
        </label>
      </div>

      {/* Table */}
      <EventTable events={events} />

      {/* Pagination */}
      <div style={{ marginTop: 16 }}>
        <button
          disabled={offset === 0}
          onClick={() => setOffset(o => Math.max(0, o - PAGE_SIZE))}
        >
          Previous
        </button>{" "}
        <button
          disabled={events.length < PAGE_SIZE}
          onClick={() => setOffset(o => o + PAGE_SIZE)}
        >
          Next
        </button>
      </div>
    </div>
  );
}