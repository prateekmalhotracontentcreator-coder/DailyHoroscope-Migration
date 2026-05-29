// -----------------------------------------------------------------
// ReentryLoop.jsx
// Source: STR-2D · ReentryLoop.html  (CD delivery)
// Extracted + converted: 2026-05-29
// 6-step recipe: PROCESS_CD_INTEGRATION_PROTOCOL.md
//
// Render rule: conditionally mounted on NO / WAIT verdicts.
// The Action Plan page mounts this only when verdict is 'no' or 'wait'.
//
// Exports:
//   default  ReentryLoop  -- main component, receives { data, asOf }
//   named    PathStep     -- single ritual/action step with pip progress
//   named    PathCard     -- full ritual or action path card
//   named    ScoreBar     -- score-to-threshold progress bar with legend
//
// CSS: import '../../../styles/strategist-2d-reentry.css'
// -----------------------------------------------------------------

// Step 1 -- React import
import React, { useState } from 'react';

// Step 5 -- shared primitives
import { SegPill, VerdictChip, SectionHeader } from './StrategistPrimitives';

// -----------------------------------------------------------------
// REENTRY_PATHS · hardcoded interpretation content (ritual & action)
// Field map: reentry.paths = derived/hardcoded from interpretation
// The done/total progress will be wired from live API in STR-OP-13.
// -----------------------------------------------------------------
const REENTRY_PATHS = {
  ritual: {
    title: 'The Ritual Path',
    subtitle: 'steady · low-cost · ledger-clearing',
    steps: [
      { code: '01', label: 'Wednesday ritual · 9 of 9 weeks',  done: 0, total: 9 },
      { code: '02', label: 'Pitru tarpan · next amavasya',      done: 0, total: 1 },
      { code: '03', label: 'Dormant-house chore · 6H weekly',   done: 0, total: 3 },
    ],
    eta: '~5 weeks · Sovereign threshold',
  },
  action: {
    title: 'The Action Path',
    subtitle: 'sprint · ledger-front-loaded · higher friction',
    steps: [
      { code: '01', label: 'Charity sealing · 3 acts · 1 week', done: 0, total: 3 },
      { code: '02', label: 'Saturn-day fast · 4 consecutive',   done: 0, total: 4 },
      { code: '03', label: 'Apology / repair · 1 conversation', done: 0, total: 1 },
    ],
    eta: '~2 weeks · Sovereign threshold',
  },
};

// -----------------------------------------------------------------
// PipTrack -- discrete step progress pips
// -----------------------------------------------------------------
function PipTrack({ done, total }) {
  return (
    <div className="rl-step__pip-track" aria-hidden="true">
      {Array.from({ length: total }, (_, i) => (
        <span
          key={i}
          className={`rl-step__pip ${i < done ? 'rl-step__pip--done' : ''}`}
        />
      ))}
    </div>
  );
}

// -----------------------------------------------------------------
// PathStep -- single ritual or action step with pip progress track
// -----------------------------------------------------------------
export function PathStep({ step }) {
  const isDone = step.done >= step.total;
  return (
    <li className={`rl-step ${isDone ? 'rl-step--done' : ''}`}>
      <span className="rl-step__code">{step.code}</span>
      <div className="rl-step__body">{step.label}</div>
      <div className="rl-step__progress">
        <div className="rl-step__progress-head">
          <span>Progress</span>
          <b>{step.done} / {step.total}</b>
        </div>
        <PipTrack done={step.done} total={step.total} />
      </div>
    </li>
  );
}

// -----------------------------------------------------------------
// PathCard -- ritual or action path card with steps list
// Step 2: pathKey/path received as props (was window.SEEKER.reentry.paths)
// -----------------------------------------------------------------
export function PathCard({ pathKey, path }) {
  return (
    <section className="rl-path">
      <header className="rl-path__head">
        <h3 className="rl-path__title">
          <span style={{ marginRight: 10, color: 'var(--gold)' }}>◆</span>
          {path.title}
        </h3>
        <span className="rl-path__subtitle">{path.subtitle}</span>
        <span className="rl-path__eta">eta &middot; <b>{path.eta}</b></span>
      </header>
      <ul className="rl-steps">
        {path.steps.map((s) => <PathStep key={s.code} step={s} />)}
      </ul>
    </section>
  );
}

// -----------------------------------------------------------------
// ScoreBar -- score -> threshold progress bar with 4-cell legend
// Step 2: score/threshold received as props (was window.SEEKER.score)
// Props: { score, threshold, max, tier, nextTier }
// -----------------------------------------------------------------
export function ScoreBar({ score, threshold, max = 99, tier, nextTier }) {
  const fillPct = (score / max) * 100;
  const threshPct = (threshold / max) * 100;
  const distance = threshold - score;
  return (
    <>
      <div className="rl-bar">
        <div className="rl-bar__fill" style={{ width: fillPct + '%' }} />
        <div className="rl-bar__threshold" style={{ left: 'calc(' + threshPct + '% - 1px)' }}>
          <span className="rl-bar__threshold-label">{nextTier || 'Next'} &middot; {threshold}</span>
        </div>
      </div>
      <div className="rl-hero__legend" style={{ marginTop: 22 }}>
        <div className="rl-legend-cell rl-legend-cell--at">
          <span className="rl-legend-cell__l">You are at</span>
          <span className="rl-legend-cell__v rl-legend-cell__v--amber">{score}</span>
          <span className="rl-legend-cell__sub">{tier || '--'}</span>
        </div>
        <div className="rl-legend-cell rl-legend-cell--to">
          <span className="rl-legend-cell__l">Threshold</span>
          <span className="rl-legend-cell__v rl-legend-cell__v--gold">{threshold}</span>
          <span className="rl-legend-cell__sub">{nextTier || '--'} &middot; re-read unlocks</span>
        </div>
        <div className="rl-legend-cell">
          <span className="rl-legend-cell__l">Distance</span>
          <span className="rl-legend-cell__v">{distance} pts</span>
          <span className="rl-legend-cell__sub">karmic-cleared &middot; gates open</span>
        </div>
        <div className="rl-legend-cell">
          <span className="rl-legend-cell__l">Observed</span>
          <span className="rl-legend-cell__v">-- d</span>
          <span className="rl-legend-cell__sub">verdict held this long</span>
        </div>
      </div>
    </>
  );
}

// -----------------------------------------------------------------
// ReentryLoop -- main exported component
// Receives: { data, asOf }
//   data  -- live API response from /api/strategist/dashboard
//   asOf  -- display timestamp string
//
// Live API field map:
//   verdict       <- data.scoreboard.gate0_last_verdict (lowercased)
//   score         <- data.conquest_probability.score
//   nextThreshold <- data.scoreboard.next_threshold
//   nextTier      <- data.scoreboard.next_threshold_label
//   tier          <- data.scoreboard.score_tier
//   reentry paths <- REENTRY_PATHS hardcoded (field map: derived)
//
// Render rule: parent page should only mount this when
//   verdict === 'no' || verdict === 'wait'
// -----------------------------------------------------------------
// density: optional page-level density ('command'|'briefing').
// When null/undefined (standalone), foot-grid always visible.
// When 'command', foot-grid is hidden. When 'briefing', foot-grid shows.
export default function ReentryLoop({ data, asOf, density = null }) {
  const [pathKey, setPathKey] = useState('ritual');
  const showFootGrid = density === null || density === 'briefing';

  // Step 6 -- wire live API fields
  const verdict       = (data?.scoreboard?.gate0_last_verdict ?? 'no').toLowerCase();
  const score         = data?.conquest_probability?.score ?? 0;
  const nextThreshold = data?.scoreboard?.next_threshold ?? 75;
  const nextTier      = data?.scoreboard?.next_threshold_label ?? 'Sovereign';
  const tier          = data?.scoreboard?.score_tier ?? '--';
  const path          = REENTRY_PATHS[pathKey];

  return (
    <>
      <SectionHeader
        title="Re-entry Loop"
        meta={null}
        right={
          <SegPill
            segments={[
              { value: 'ritual', label: 'ritual' },
              { value: 'action', label: 'action' },
            ]}
            value={pathKey}
            onChange={setPathKey}
            size="sm"
            ariaLabel="Re-entry path"
          />
        }
      />

      {/* Verdict-precondition card */}
      <div className={`rl-preface rl-preface--${verdict}`}>
        <span className="rl-preface__lbl">Why this is showing</span>
        <p className="rl-preface__msg">
          The active verdict is <VerdictChip type={verdict} />{' '}
          &mdash; the chart denies <b>the named action</b>. Re-entry loop unlocks <b>{path.eta}</b> via the {pathKey} path.
          This panel hides automatically when the verdict returns to <VerdictChip type="yes" />.
        </p>
        <span></span>
      </div>

      {/* Score-bar hero */}
      <section className="rl-hero">
        <header className="rl-hero__head">
          <h3 className="rl-hero__title">Path to {nextTier}</h3>
          <span className="rl-hero__sub">re-read unlocks at score &middot; <b>{nextThreshold}</b></span>
        </header>
        <ScoreBar
          score={score}
          threshold={nextThreshold}
          max={99}
          tier={tier}
          nextTier={nextTier}
        />
      </section>

      {/* Path detail */}
      <PathCard pathKey={pathKey} path={path} />

      {/* Light vs heavy comparison -- hidden in Command density */}
      {showFootGrid && (
        <div className="rl-foot-grid">
          <div className="rl-foot-cell">
            <span className="rl-foot-cell__lbl">Ritual path</span>
            <p className="rl-foot-cell__body">
              <b>Steady &middot; low-cost &middot; ledger-clearing.</b> Three repeated observances over ~5 weeks. Best when the seeker has discipline but limited spare bandwidth &mdash; the streak does the work.
            </p>
          </div>
          <div className="rl-foot-divider" aria-hidden="true"></div>
          <div className="rl-foot-cell">
            <span className="rl-foot-cell__lbl">Action path</span>
            <p className="rl-foot-cell__body">
              <b>Sprint &middot; ledger-front-loaded &middot; higher friction.</b> Three pointed acts inside ~2 weeks. Best when the seeker can absorb short-term cost (money / time / a hard conversation) to compress the timeline.
            </p>
          </div>
        </div>
      )}
    </>
  );
}
