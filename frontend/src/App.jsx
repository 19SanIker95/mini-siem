import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import Events from "./pages/Events";
import Alerts from "./pages/Alerts";

export default function App() {
  const [page, setPage] = useState("dashboard");

  return (
    <div style={{ maxWidth: 1200, margin: "0 auto", padding: 20 }}>
      <h1 style={{ marginBottom: 10 }}>Mini‑SIEM</h1>

      <nav style={{ marginBottom: 20, display: "flex", gap: 10 }}>
        <button
          onClick={() => setPage("dashboard")}
          style={{ fontWeight: page === "dashboard" ? "bold" : "normal" }}
        >
          Dashboard
        </button>

        <button
          onClick={() => setPage("events")}
          style={{ fontWeight: page === "events" ? "bold" : "normal" }}
        >
          Events
        </button>

        <button
          onClick={() => setPage("alerts")}
          style={{ fontWeight: page === "alerts" ? "bold" : "normal" }}
        >
          Alerts
        </button>
      </nav>

      <div
        style={{
          backgroundColor: "var(--panel)",
          border: "1px solid var(--border)",
          borderRadius: 8,
          padding: 16,
        }}
      >
        {page === "dashboard" && <Dashboard />}
        {page === "events" && <Events />}
        {page === "alerts" && <Alerts />}
      </div>
    </div>
  );
}