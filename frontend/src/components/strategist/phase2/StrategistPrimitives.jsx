// -----------------------------------------------------------------
// StrategistPrimitives.jsx
// Source: _assets/strategist-primitives.jsx  (CD delivery)
// Extracted + converted: 2026-05-29
//
// Shared primitives consumed by ALL Phase 2 Strategist components.
// Canvas-only items excluded: SEEKER stub, useTheme, ThemePill, ProtoTopBar.
//
// Exports:
//   SegPill        -- reusable toggle pill (size 'sm'|'md')
//   VerdictChip    -- YES / WAIT / NO / PRAY chip (locked v2)
//   SectionHeader  -- section title bar with diamond glyph + right slot
// -----------------------------------------------------------------

// Step 1 -- React import
import React from 'react';

// -----------------------------------------------------------------
// SegPill · the reusable toggle primitive
// Props: segments[] · value · onChange · size 'sm'|'md' · ariaLabel
// Segments can be strings OR { value, label } objects.
// Consumed by: 2C (size='md', 4 segments) · 2D · 2E · 2I (size='sm')
// CSS: .seg-pill defined in strategist-2f-scoreboard.css
// -----------------------------------------------------------------
export function SegPill({ segments, value, onChange, size = 'sm', ariaLabel }) {
  return (
    <div className={`seg-pill seg-pill--${size}`} role="tablist" aria-label={ariaLabel}>
      {segments.map((seg) => {
        const key = typeof seg === 'string' ? seg : seg.value;
        const label = typeof seg === 'string' ? seg : seg.label;
        const active = key === value;
        return (
          <button
            key={key}
            type="button"
            role="tab"
            aria-selected={active}
            className={`seg-pill__seg ${active ? 'seg-pill__seg--on' : ''}`}
            onClick={() => onChange(key)}
          >
            {label}
          </button>
        );
      })}
    </div>
  );
}

// -----------------------------------------------------------------
// VerdictChip · YES · WAIT · NO · PRAY
// PRAY v2 locked treatment: gold text on rahu-soft fill, full-gold border.
// Banner surfaces in 2C / 2I may carry gradient -- chip type stays gold.
// CSS: .verdict-chip defined in strategist-2f-scoreboard.css
// -----------------------------------------------------------------
export const VERDICT_META = {
  yes:  { label: 'Yes',  pip: true,  glyph: null },
  wait: { label: 'Wait', pip: true,  glyph: null },
  no:   { label: 'No',   pip: true,  glyph: null },
  pray: { label: 'Pray', pip: false, glyph: '◆' },
};

export function VerdictChip({ type, active = false, label }) {
  const meta = VERDICT_META[type] || VERDICT_META.yes;
  return (
    <span className={`verdict-chip verdict-chip--${type} ${active ? 'verdict-chip--active' : ''}`}>
      {meta.glyph ? <span aria-hidden="true">{meta.glyph}</span> : null}
      {meta.pip ? <span className="verdict-chip__pip" /> : null}
      {label || meta.label}
    </span>
  );
}

// -----------------------------------------------------------------
// SectionHeader · ◆ Title · meta · right-anchored slot
// Source: _assets/strategist-primitives.jsx SectionHeader
// CSS: .section-header defined in strategist-2f-scoreboard.css
// -----------------------------------------------------------------
export function SectionHeader({ title, meta, right }) {
  return (
    <div className="section-header">
      <h2 className="section-header__title">
        <span className="diamond">◆</span>
        {title}
      </h2>
      {meta != null
        ? <span className="section-header__meta">{meta}</span>
        : <span />}
      {right != null ? right : <span />}
    </div>
  );
}
