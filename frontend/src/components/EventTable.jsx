import SeverityBadge from "./SeverityBadge";

export default function EventTable({ events }) {
  if (!events || events.length === 0) {
    return <p>No events found</p>;
  }

  return (
    <table width="100%" border="1" cellPadding="6">
      <thead>
        <tr>
          <th>Time</th>
          <th>Source</th>
          <th>Type</th>
          <th>Severity</th>
          <th>IP</th>
          <th>Message</th>
        </tr>
      </thead>
      <tbody>
        {events.map(e => (
          <tr key={e.id}>
            <td style={{ fontFamily: "monospace", fontSize: 12 }}>{new Date(e.ts).toISOString()}</td>
            <td>{e.source}</td>
            <td>{e.event_type}</td>
            <td><SeverityBadge severity={e.severity} /></td>
            <td>{e.ip || "-"}</td>
            <td>{e.message}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}