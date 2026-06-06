// =============================================================
// STR-R2B Step 3 · FactorTable
// Brief §4.3 · Layer 1 atom · canvas ref 02/01 · ART 1.2 right side
// -------------------------------------------------------------
// Tone-coded factor list under the gauge.
//   factors[]: { label, sub?, delta (number | string), tone }
//   tone: 'em' | 'warn' | 'crit' | 'neutral'
// =============================================================

function formatDelta(delta) {
  if (typeof delta !== 'number') return delta;
  if (delta === 0) return '0';
  return delta > 0 ? `+${delta}` : `${delta}`;
}

export default function FactorTable({ factors = [], eyebrow }) {
  const label = eyebrow || `Factor breakdown · ${factors.length} contributor${factors.length !== 1 ? 's' : ''}`;
  return (
    <div className="ft">
      <div className="ft__eyebrow">{label}</div>

      {factors.map((f, i) => (
        <div key={f.id || i} className={`ft-row ft-row--${f.tone || 'neutral'}`}>
          <span className="ft-row__bar" aria-hidden="true" />
          <div>
            <p className="ft-row__label">{f.label}</p>
            {f.sub && <p className="ft-row__sub">{f.sub}</p>}
          </div>
          <div className="ft-row__value">{formatDelta(f.delta)}</div>
        </div>
      ))}
    </div>
  );
}
