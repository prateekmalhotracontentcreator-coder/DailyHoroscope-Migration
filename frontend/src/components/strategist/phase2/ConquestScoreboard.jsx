// -----------------------------------------------------------------
// ConquestScoreboard.jsx
// Source: STR-2F · ConquestScoreboard.html  (CD delivery)
// Extracted + converted: 2026-05-29
// 6-step recipe: PROCESS_CD_INTEGRATION_PROTOCOL.md
//
// Exports:
//   default  ConquestScoreboard  -- main page component, receives { data, asOf }
//   named    SegPill             -- reusable toggle primitive (2C, 2D, 2I consume this)
//   named    VerdictChip         -- YES / WAIT / NO / PRAY chip
//   named    KarmicChip          -- ledger cleared badge
//   named    Gauge               -- conquest score SVG gauge
//   named    ScoreboardExpanded  -- full hero card (default view)
//   named    ScoreboardCompact   -- single-row density view
//   named    VerdictStrip        -- live single-verdict display strip
//
// CSS: import '../../../styles/strategist-2f-scoreboard.css'
//      (import in the page that uses this component)
// -----------------------------------------------------------------

// Step 1 -- React import
import React, { useState } from 'react';

// Step 5 -- shared primitives (canonical location: StrategistPrimitives.jsx)
import { SegPill, VerdictChip } from './StrategistPrimitives';
// Re-export so callers that previously imported from ConquestScoreboard continue to work
export { SegPill, VerdictChip };

// -----------------------------------------------------------------
// Gauge -- SVG conquest score gauge
// 100r · 628.3 dasharray · band-coloured fill · 600ms transition
// Step 2: tier received as prop (was window.SEEKER.tier)
// -----------------------------------------------------------------
const CIRC = 628.3, RADIUS = 100, VIEW = 240;

export function Gauge({ score, max, tier, mini = false }) {
  const s = Math.max(0, Math.min(max, score));
  const offset = CIRC * (1 - s / max);
  return (
    <div className={mini ? 'board-compact__mini-gauge' : 'gauge'} aria-hidden="true">
      <svg viewBox={`0 0 ${VIEW} ${VIEW}`}>
        <circle
          className="gauge__track" cx={VIEW/2} cy={VIEW/2} r={RADIUS}
          strokeDasharray={CIRC} strokeDashoffset="0"
        />
        <circle
          className="gauge__fill" cx={VIEW/2} cy={VIEW/2} r={RADIUS}
          strokeDasharray={CIRC} strokeDashoffset={offset}
          style={mini ? { strokeWidth: 22 } : {}}
        />
      </svg>
      {!mini && (
        <div className="gauge__center">
          <div className="gauge__score">{s}</div>
          <div className="gauge__max">/ {max}</div>
          <div className="gauge__tier">{tier}</div>
        </div>
      )}
    </div>
  );
}

// -----------------------------------------------------------------
// KarmicChip -- ledger state badge
// -----------------------------------------------------------------
export function KarmicChip({ state }) {
  return (
    <span className="karmic-chip">
      <span className="karmic-chip__check" aria-hidden="true">
        <svg viewBox="0 0 12 12" width="10" height="10" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="2,6.5 5,9 10,3.5"/>
        </svg>
      </span>
      {state}
    </span>
  );
}

// Derive band label from score
function getBandLabel(score) {
  if (score >= 75) return '75 -- 99 band';
  if (score >= 50) return '50 -- 74 band';
  if (score >= 25) return '25 -- 49 band';
  return '0 -- 24 band';
}

// -----------------------------------------------------------------
// ScoreboardExpanded -- full hero card (default view)
// Step 2: all SEEKER.* replaced with explicit props
// -----------------------------------------------------------------
export function ScoreboardExpanded({
  score, max, tier, nextTier, pointsToNext, nextThreshold,
  verdict, karmic, streak, directive, asOf,
}) {
  return (
    <div className="board-hero">
      <div className="board-hero__left">
        <Gauge score={score} max={max} tier={tier} />
        <div className="board-hero__verdict">
          <span className="board-hero__verdict-lbl">Active verdict</span>
          <VerdictChip type={verdict} active />
        </div>
      </div>

      <div className="board-hero__rows">
        <div className="row-data">
          <div className="row-data__label">Rank</div>
          <div className="row-data__body">
            <strong>{tier}</strong> &middot; {getBandLabel(score)}
          </div>
          <div className="row-data__aside">
            next &middot; <b>{nextTier}</b> &middot; {pointsToNext} to {nextThreshold}
          </div>
        </div>

        <div className="row-data">
          <div className="row-data__label">Karmic</div>
          <div className="row-data__body">
            <KarmicChip state={karmic} />
            <span style={{ marginLeft: 10, fontFamily: 'var(--font-serif)', fontStyle: 'italic', color: 'var(--strategist-fg-2)', fontSize: 13 }}>
              ledger balanced &middot; gates open
            </span>
          </div>
          <div className="row-data__aside">&nbsp;</div>
        </div>

        <div className="row-data">
          <div className="row-data__label">Streak</div>
          <div className="row-data__body" style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <strong>{streak.days} days</strong>
            <span className="streak-chip">{streak.tier}</span>
          </div>
          <div className="row-data__aside">&nbsp;</div>
        </div>

        <div className="row-data">
          <div className="row-data__label">Directive</div>
          <div className="row-data__body">
            <span className="directive">&ldquo;{directive}&rdquo;</span>
          </div>
          <div className="row-data__aside">as of {asOf}</div>
        </div>
      </div>
    </div>
  );
}

// -----------------------------------------------------------------
// ScoreboardCompact -- single horizontal row density view
// Step 2: all SEEKER.* replaced with explicit props
// -----------------------------------------------------------------
export function ScoreboardCompact({ score, max, tier, verdict, directive, streak }) {
  return (
    <div className="board-compact">
      <Gauge score={score} max={max} tier={tier} mini />
      <div className="board-compact__score-block">
        <span className="board-compact__score">{score}</span>
        <span className="board-compact__tier">{tier}</span>
      </div>
      <VerdictChip type={verdict} active />
      <div className="board-compact__directive">&ldquo;{directive}&rdquo;</div>
      <div className="board-compact__streak">
        <b>{streak.days}-day</b> streak &middot; {streak.tier}
      </div>
    </div>
  );
}

// -----------------------------------------------------------------
// VerdictStrip -- live single-verdict display
// Shows only the active verdict chip (from live API data).
// -----------------------------------------------------------------
export function VerdictStrip({ verdict = 'wait' }) {
  return (
    <div className="chip-set">
      <div className="chip-set__row">
        <span className="chip-set__eyebrow">Verdict</span>
        <VerdictChip type={verdict} />
      </div>
    </div>
  );
}

// -----------------------------------------------------------------
// ConquestScoreboard -- main exported component
// Receives: { data, asOf }
//   data  -- live API response from /api/strategist/dashboard
//   asOf  -- display timestamp string e.g. '29 May · 09:42 IST'
//
// Live API field map (PROCESS_CD_INTEGRATION_PROTOCOL.md §5):
//   score          <- data.conquest_probability.score
//   tier           <- data.scoreboard.score_tier
//   nextTier       <- data.scoreboard.next_threshold_label
//   nextThreshold  <- data.scoreboard.next_threshold
//   pointsToNext   <- data.scoreboard.points_to_next
//   verdict        <- data.scoreboard.gate0_last_verdict (lowercased)
//   karmic         <- data.diagnosis_summary.karmic_debt_cleared
//   streak.days    <- data.scoreboard.streak_days
//   streak.tier    <- data.scoreboard.streak_tier
//   directive      <- data.scoreboard.score_directive
// -----------------------------------------------------------------
// view: optional override ('compact'|'expanded'). When provided, hides the
// internal toggle so the page-level density controls this module.
export default function ConquestScoreboard({ data, asOf, view: viewProp = null, showToggle }) {
  const [viewState, setViewState] = useState('expanded');
  const controlled = viewProp !== null;
  const view = controlled ? viewProp : viewState;
  const setView = controlled ? () => {} : setViewState;
  // showToggle: explicit override; defaults to false when controlled by parent
  const showToggleActual = showToggle !== undefined ? showToggle : !controlled;

  // Step 6 -- wire live API fields, safe fallbacks for loading state
  const score         = data?.conquest_probability?.score ?? 0;
  const max           = 99;
  const tier          = data?.scoreboard?.score_tier ?? '--';
  const nextTier      = data?.scoreboard?.next_threshold_label ?? '--';
  const nextThreshold = data?.scoreboard?.next_threshold ?? 99;
  const pointsToNext  = data?.scoreboard?.points_to_next ?? 0;
  const verdict       = (data?.scoreboard?.gate0_last_verdict ?? 'wait').toLowerCase();
  const karmic        = data?.diagnosis_summary?.karmic_debt_cleared ?? 'Pending';
  const streak = {
    days: data?.scoreboard?.streak_days ?? 0,
    tier: data?.scoreboard?.streak_tier ?? '--',
  };
  const directive = data?.scoreboard?.score_directive ?? '';

  const scoreboardProps = {
    score, max, tier, nextTier, nextThreshold, pointsToNext,
    verdict, karmic, streak, directive, asOf,
  };

  return (
    <>
      <div className="section-header">
        <h2 className="section-header__title">
          <span className="diamond">◆</span>
          Conquest Scoreboard
        </h2>
        <span className="section-header__meta">as of {asOf}</span>
        {showToggleActual && (
          <SegPill
            segments={['compact', 'expanded']}
            value={view}
            onChange={setView}
            size="sm"
            ariaLabel="Scoreboard density"
          />
        )}
      </div>

      {view === 'expanded'
        ? <ScoreboardExpanded {...scoreboardProps} />
        : <ScoreboardCompact {...scoreboardProps} />
      }

      <VerdictStrip verdict={verdict} />
    </>
  );
}
