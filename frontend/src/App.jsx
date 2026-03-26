import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import Events from "./pages/Events";

export default function App() {
  const [page, setPage] = useState("dashboard");

  return (
    <div style={{ padding: 20 }}>
      <h1>Mini‑SIEM</h1>

      <nav style={{ marginBottom: 20 }}>
        <button onClick={() => setPage("dashboard")}>Dashboard</button>{" "}
        <button onClick={() => setPage("events")}>Events</button>
      </nav>

      {page === "dashboard" && <Dashboard />}
      {page === "events" && <Events />}
    </div>
  );
}