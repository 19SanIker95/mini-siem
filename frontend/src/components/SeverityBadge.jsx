function getColor(severity) {
  if (severity >= 5) return "#c0392b";   // red
  if (severity === 4) return "#e67e22";  // orange
  if (severity === 3) return "#f1c40f";  // yellow
  if (severity === 2) return "#3498db";  // blue
  return "#2ecc71";                      // green
}

export default function SeverityBadge({ severity }) {
  return (
    <span
      style={{
        backgroundColor: getColor(severity),
        color: "#fff",
        padding: "2px 8px",
        borderRadius: 12,
        fontSize: 12,
        fontWeight: "bold",
      }}
    >
      {severity}
    </span>
  );
}