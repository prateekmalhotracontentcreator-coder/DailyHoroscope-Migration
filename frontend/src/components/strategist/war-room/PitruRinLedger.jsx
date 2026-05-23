// =============================================================
// STR-R2B Step 3 · PitruRinLedger
// Brief §4.5 · Layer 4 · canvas ref 02/04 · ART 4.1 + 4.3
// -------------------------------------------------------------
// Severity-coloured rows (critical/high/medium/low → red/orange/amber/emerald).
// Streak badge turns red on >3 d lapsed. Cleared rows strikethrough at 72% opacity.
// Empty state when every debt is cleared -- seal glyph, emerald halo.
// =============================================================

const SEV_CHIP = {
  critical: 'red',
  high:     'orange',
  medium:   'amber',
  low:      'emerald',
};

function Streak({ days, lapsed, cleared, threshold }) {
  // breach = the row is active (not cleared) AND days >= threshold (default 3)
  const t = threshold ?? 3;
  const breach = !cleared && lapsed && lapsed >= t;
  let label = 'Day · Streak';
  if (cleared)        label = 'Day · Complete';
  else if (breach)    label = 'Day · Lapsed';
  else if (lapsed === t) label = 'Day · Threshold';
  const num = cleared ? days : (lapsed ?? days);

  return (
    <div className={`pr-streak ${breach ? 'pr-streak--breach' : ''}`}>
      <div className="pr-streak__n">{num}</div>
      <div className="pr-streak__l">{label}</div>
    </div>
  );
}

function PitruRinRow({ debt, onLogRitual }) {
  const sev = debt.cleared ? 'cleared' : (debt.severity || 'medium');
  const chip = debt.cleared ? null : SEV_CHIP[debt.severity];

  return (
    <div className="pr-row" data-sev={sev}>
      <span className="pr-row__bar" aria-hidden="true" />
      <div className="pr-row__main">
        <div className="pr-row__topline">
          <h4 className="pr-row__label">{debt.name}</h4>
          {debt.cleared
            ? <span className="wr-chip wr-chip--muted">✓ Cleared</span>
            : <span className={`wr-chip wr-chip--${chip}`}>
                <span className="wr-chip__pip" />
                {debt.severity.charAt(0).toUpperCase() + debt.severity.slice(1)}
              </span>}
          {debt.type && <span className="pr-row__type">{debt.type}</span>}
        </div>
        <p className="pr-row__ritual">{debt.ritual}</p>
      </div>
      <div className="pr-row__metrics">
        <Streak
          days={debt.streakDays || 0}
          lapsed={debt.daysSinceRitual}
          cleared={debt.cleared}
        />
        <button
          type="button"
          className="pr-cta"
          disabled={debt.cleared}
          onClick={() => onLogRitual?.(debt)}
        >
          {debt.cleared ? 'Closed' : 'Log Ritual ▸'}
        </button>
      </div>
    </div>
  );
}

function EmptyState({ lastClearance, lastStreak }) {
  return (
    <div className="pr-clear">
      <div className="pr-clear__seal" aria-hidden="true">
        <svg viewBox="0 0 88 88" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="44" cy="44" r="40" stroke="var(--emerald)" strokeWidth="1" opacity="0.45" />
          <circle cx="44" cy="44" r="32" stroke="var(--emerald)" strokeWidth="1.4" />
          <g stroke="var(--emerald)" strokeWidth="1.4" strokeLinecap="round">
            <path d="M44 16 L44 72" />
            <path d="M20 30 L68 58" />
            <path d="M20 58 L68 30" />
          </g>
          <circle cx="44" cy="44" r="6" fill="var(--emerald)" />
          <circle cx="44" cy="44" r="14" stroke="var(--emerald)" strokeWidth="1" opacity="0.5" />
        </svg>
      </div>
      <h3 className="pr-clear__title">No Active Debts</h3>
      <p className="pr-clear__body">
        Your ledger is balanced for this cycle. The Pitru gates are open --
        direct your remaining offerings toward the dasha lord above.
      </p>
      {(lastClearance || lastStreak) && (
        <div className="pr-clear__meta">
          {lastClearance && <>Last clearance · {lastClearance}</>}
          {lastClearance && lastStreak && <> · </>}
          {lastStreak && <>{lastStreak}-day streak</>}
        </div>
      )}
    </div>
  );
}

/**
 * PitruRinLedger
 *
 * props
 *   debts[]: { name, severity, streakDays, daysSinceRitual, cleared, ritual, type? }
 *   anchorLabel?: string
 *   netDelta?: number   negative reduces Conquest Score
 *   onLogRitual?: (debt) => void
 *
 *   showEmptyOnAllCleared (default true) -- render empty state when
 *   every debt has cleared = true.
 */
export default function PitruRinLedger({
  debts = [],
  anchorLabel,
  netDelta,
  onLogRitual,
  showEmptyOnAllCleared = true,
  emptyMeta,
}) {
  const allCleared = debts.length > 0 && debts.every(d => d.cleared);
  const empty = debts.length === 0;

  if ((empty || allCleared) && showEmptyOnAllCleared) {
    return <EmptyState {...(emptyMeta || {})} />;
  }

  const active = debts.filter(d => !d.cleared);
  const cleared = debts.filter(d => d.cleared);
  const severityCounts = active.reduce((acc, d) => {
    acc[d.severity] = (acc[d.severity] || 0) + 1;
    return acc;
  }, {});
  const skewParts = Object.entries(severityCounts).map(
    ([k, n]) => `${k.charAt(0).toUpperCase()}${k.slice(1)} ${n}`
  );

  return (
    <div className="wr-panel">
      <div className="wr-panel__head">
        <div>
          <h3 className="wr-panel__title">Pitru-Rin · Ledger</h3>
          <div className="wr-panel__sub" style={{ marginTop: 4 }}>
            {active.length} active debt{active.length === 1 ? '' : 's'}
            {cleared.length > 0 && <> · {cleared.length} cleared this cycle</>}
          </div>
        </div>
        {anchorLabel && <div className="wr-panel__sub">{anchorLabel}</div>}
      </div>

      {debts.map((d, i) => (
        <PitruRinRow key={d.id || d.name || i} debt={d} onLogRitual={onLogRitual} />
      ))}

      <div className="pr-summary">
        <span>
          Severity skew · <strong>{skewParts.join(' · ') || '--'}</strong>
        </span>
        {typeof netDelta === 'number' && (
          <span>
            Net contribution to Conquest Score ·{' '}
            <strong style={{ color: netDelta < 0 ? 'var(--red)' : 'var(--emerald)' }}>
              {netDelta > 0 ? `+${netDelta}` : netDelta}
            </strong>
          </span>
        )}
      </div>
    </div>
  );
}
