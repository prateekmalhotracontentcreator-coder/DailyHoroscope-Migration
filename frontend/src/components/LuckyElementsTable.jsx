import React from "react";

function toRows(payload) {
  if (!payload) return [];

  const rows = [];
  if (payload.dominant_element) {
    rows.push({ label: "Dominant Element", value: payload.dominant_element });
  }
  if (payload.supportive_day) {
    rows.push({ label: "Supportive Day", value: payload.supportive_day });
  }
  if (Array.isArray(payload.supportive_colors) && payload.supportive_colors.length) {
    rows.push({ label: "Supportive Colours", value: payload.supportive_colors.join(", ") });
  }
  if (Array.isArray(payload.lucky_numbers) && payload.lucky_numbers.length) {
    rows.push({ label: "Lucky Numbers", value: payload.lucky_numbers.join(", ") });
  }
  if (Array.isArray(payload.supportive_gems) && payload.supportive_gems.length) {
    rows.push({ label: "Supportive Gems", value: payload.supportive_gems.join(", ") });
  }
  if (Array.isArray(payload.supportive_metals) && payload.supportive_metals.length) {
    rows.push({ label: "Supportive Metals", value: payload.supportive_metals.join(", ") });
  }
  return rows;
}

function LuckyElementsTable({ payload }) {
  const rows = toRows(payload);
  if (!rows.length) return null;

  return (
    <section className="numerology-structured-card numerology-lucky-elements">
      <div className="numerology-structured-card__header">
        <p className="numerology-structured-card__eyebrow">Lucky Elements</p>
        <h3>Supportive Colours, Days, and Symbolic Favourables</h3>
      </div>

      <div className="numerology-lucky-elements__table" role="table" aria-label="Lucky elements table">
        {rows.map((row) => (
          <div key={row.label} className="numerology-lucky-elements__row" role="row">
            <div className="numerology-lucky-elements__label" role="cell">
              {row.label}
            </div>
            <div className="numerology-lucky-elements__value" role="cell">
              {row.value}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default LuckyElementsTable;
