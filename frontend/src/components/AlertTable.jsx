export default function AlertTable({ alerts }) {
  if (alerts.length === 0) {
    return <p>No alerts 🎉</p>;
  }

  return (
    <table width="100%" border="1" cellPadding="6">
      <thead>
        <tr>
          <th>Created</th>
          <th>Rule</th>
          <th>Severity</th>
          <th>IP</th>
          <th>Events</th>
          <th>Window</th>
        </tr>
      </thead>
      <tbody>
        {alerts.map(a => (
          <tr key={a.id}>
            <td>{new Date(a.created_at).toLocaleString()}</td>
            <td>{a.rule_name}</td>
            <td>{a.severity}</td>
            <td>{a.ip || "-"}</td>
            <td>{a.event_count}</td>
            <td>
              {new Date(a.window_start).toLocaleTimeString()} –{" "}
              {new Date(a.window_end).toLocaleTimeString()}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}