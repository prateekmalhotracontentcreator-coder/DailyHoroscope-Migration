import React from "react";

const DEFAULT_ROWS = [
  [{ number: 4, count: 0 }, { number: 9, count: 0 }, { number: 2, count: 0 }],
  [{ number: 3, count: 0 }, { number: 5, count: 0 }, { number: 7, count: 0 }],
  [{ number: 8, count: 0 }, { number: 1, count: 0 }, { number: 6, count: 0 }],
];

function normalizeRows(payload) {
  if (Array.isArray(payload?.grid_rows) && payload.grid_rows.length === 3) {
    return payload.grid_rows;
  }
  return DEFAULT_ROWS;
}

function planeLabel(key) {
  return key.replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function LoShuGrid({ payload }) {
  if (!payload) return null;

  const rows = normalizeRows(payload);
  const repeated = new Set((payload.repeated_numbers || []).map((value) => Number(value)));
  const missing = new Set((payload.missing_numbers || []).map((value) => Number(value)));
  const planeAnalysis = payload.plane_analysis || {};

  return (
    <section className="numerology-structured-card numerology-loshu">
      <div className="numerology-structured-card__header">
        <p className="numerology-structured-card__eyebrow">Lo Shu Grid</p>
        <h3>Visual Balance Map</h3>
      </div>

      <div className="numerology-loshu__grid" role="table" aria-label="Lo Shu numerology grid">
        {rows.map((row, rowIndex) => (
          <div key={`row-${rowIndex}`} className="numerology-loshu__row" role="row">
            {row.map((cell) => {
              const number = Number(cell?.number);
              const count = Number(cell?.count || 0);
              const isMissing = missing.has(number) || count === 0;
              const isRepeated = repeated.has(number) || count > 1;
              return (
                <div
                  key={number}
                  className={[
                    "numerology-loshu__cell",
                    isMissing ? "is-missing" : "",
                    isRepeated ? "is-repeated" : "",
                  ].join(" ").trim()}
                  role="cell"
                >
                  <div className="numerology-loshu__cell-number">{number}</div>
                  <div className="numerology-loshu__cell-value">
                    {count > 0 ? String(number).repeat(count) : "—"}
                  </div>
                  {isRepeated ? <span className="numerology-loshu__badge">x{count}</span> : null}
                </div>
              );
            })}
          </div>
        ))}
      </div>

      <div className="numerology-loshu__meta">
        <div className="numerology-chip-group">
          <span className="numerology-chip numerology-chip--soft">
            Present: {(payload.present_numbers || []).join(", ") || "None"}
          </span>
          <span className="numerology-chip numerology-chip--muted">
            Missing: {(payload.missing_numbers || []).join(", ") || "None"}
          </span>
          <span className="numerology-chip numerology-chip--accent">
            Repeated: {(payload.repeated_numbers || []).join(", ") || "None"}
          </span>
        </div>

        <div className="numerology-loshu__planes">
          {Object.entries(planeAnalysis).map(([key, value]) => (
            <article key={key} className="numerology-loshu__plane">
              <p>{planeLabel(key)}</p>
              <strong>{value ? "Active" : "Needs balance"}</strong>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export default LoShuGrid;
