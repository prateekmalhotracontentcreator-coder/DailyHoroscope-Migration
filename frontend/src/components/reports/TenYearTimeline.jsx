import React from "react";

const STATUS_COLORS = {
  Auspicious: "#4E8F62",
  Inauspicious: "#B65447",
  Stabilized: "#9B9487",
};

export default function TenYearTimeline({ flags = [] }) {
  if (!Array.isArray(flags) || !flags.length) {
    return <p style={{ margin: 0, color: "#6f6255" }}>Timeline data will appear here after the enhancement layer loads.</p>;
  }

  return (
    <div style={{ display: "grid", gap: 12 }}>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: `repeat(${flags.length}, minmax(0, 1fr))`,
          gap: 8,
          alignItems: "stretch",
        }}
      >
        {flags.map((flag) => {
          const color = STATUS_COLORS[flag.status] || STATUS_COLORS.Stabilized;
          return (
            <div
              key={flag.year}
              title={`${flag.year}: ${flag.trigger}`}
              style={{
                minHeight: 72,
                borderRadius: 16,
                background: color,
                color: "#fffaf3",
                padding: "10px 8px",
                display: "grid",
                alignContent: "space-between",
                boxShadow: "inset 0 0 0 1px rgba(255,255,255,0.14)",
              }}
            >
              <div style={{ fontSize: 12, letterSpacing: "0.08em", textTransform: "uppercase", opacity: 0.9 }}>{flag.year}</div>
              <div style={{ fontSize: 12, fontWeight: 700 }}>{flag.status}</div>
            </div>
          );
        })}
      </div>
      <p style={{ margin: 0, color: "#6f6255", lineHeight: 1.6 }}>
        Hover each year block to see the trigger note behind the timing classification.
      </p>
    </div>
  );
}
