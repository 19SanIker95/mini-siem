export default function StatCard({ title, value }) {
  return (
    <div
      style={{
        border: "1px solid var(--border)",
        borderRadius: 8,
        padding: 16,
        minWidth: 160,
        backgroundColor: "#020617",
      }}
    >
      <div
        style={{
          fontSize: 12,
          color: "var(--muted)",
          marginBottom: 4,
        }}
      >
        {title}
      </div>

      <div
        style={{
          fontSize: 26,
          fontWeight: "bold",
          color: "var(--text)",
        }}
      >
        {value}
      </div>
    </div>
  );
}