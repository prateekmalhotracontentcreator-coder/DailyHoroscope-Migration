import React from "react";

const GOLD = "#C5A059";

export default function DonutChart({ percentage = 0 }) {
  const clamped = Math.max(0, Math.min(100, Number(percentage) || 0));
  const size = 180;
  const stroke = 14;
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const dashOffset = circumference - (clamped / 100) * circumference;

  return (
    <div
      style={{
        display: "grid",
        justifyItems: "center",
        gap: 10,
        width: "100%",
      }}
    >
      <svg
        viewBox={`0 0 ${size} ${size}`}
        style={{
          width: "min(180px, 44vw)",
          minWidth: 140,
          height: "auto",
          overflow: "visible",
        }}
        aria-label={`Structural Resilience ${clamped}%`}
      >
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(120,90,55,0.14)"
          strokeWidth={stroke}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={GOLD}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={dashOffset}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
        <text
          x="50%"
          y="48%"
          textAnchor="middle"
          dominantBaseline="middle"
          style={{
            fontSize: 34,
            fontWeight: 700,
            fill: "#2d2318",
            fontFamily: '"Cinzel", Georgia, serif',
          }}
        >
          {clamped}%
        </text>
      </svg>
      <div
        style={{
          fontSize: 12,
          letterSpacing: "0.16em",
          textTransform: "uppercase",
          color: "#8c6a39",
          textAlign: "center",
        }}
      >
        Structural Resilience
      </div>
    </div>
  );
}
