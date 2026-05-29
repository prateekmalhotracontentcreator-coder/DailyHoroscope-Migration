// -----------------------------------------------------------------
// OracleVerdictBanners.jsx
// Source: STR-2C · OracleVerdictBanners.html  (CD delivery)
// Extracted + converted: 2026-05-29
// 6-step recipe: PROCESS_CD_INTEGRATION_PROTOCOL.md
//
// Exports:
//   default  OracleVerdictBanners  -- main component, receives { data, asOf }
//   named    Banner                -- single verdict banner (verdict, banners, signals)
//   named    ContextStrip          -- 4-cell seeker context bar (TT confirmed include)
//   named    OracleVerdictProofStrip -- VerdictChip proof set (CD canvas, retained per TT)
//
// CSS: import '../../../styles/strategist-2c-oracle.css'
//      (import in the page that uses this component)
// -----------------------------------------------------------------

// Step 1 -- React import
import React, { useState } from 'react';

// Step 5 -- shared primitives
import { SegPill, VerdictChip, SectionHeader } from './StrategistPrimitives';

// -----------------------------------------------------------------
// BANNERS · hardcoded per verdict (field map: banners{} = hardcoded)
// Source: _assets/strategist-primitives.jsx SEEKER.banners
// -----------------------------------------------------------------
const BANNERS = {
  yes: {
    headline: 'The path is clear. Move.',
    reasoning: 'Mars in 10H · Jupiter aspecting · transit window open through the lunar fortnight. No retrograde, no eclipse shadow, no pitru contraindication.',
    cta: 'Proceed with the action',
    window: 'Next 14 days',
  },
  wait: {
    headline: 'Hold. The window does not favor.',
    reasoning: 'Mercury in retrograde shadow until the 9th. Communication channels distort. The same action 48 hours later carries half the friction.',
    cta: 'Set a 48-hour hold',
    window: 'Re-read on 9 Jun',
  },
  no: {
    headline: 'Conditions deny. Do not proceed.',
    reasoning: 'Rahu transit in the 7H, Saturn aspect on the 1H lord. The chart actively counter-signals. A No now is cheaper than a reversal in 90 days.',
    cta: 'Reroute · see Re-entry Loop',
    window: 'Re-read at 75',
  },
  pray: {
    headline: 'The answer is not in action. Offer.',
    reasoning: 'The chart withdraws -- no clear yes, no clean no. This is the gold-rahu fold: the obstruction is karmic, not tactical. Offering precedes opening.',
    cta: 'Open the Pray Path',
    window: 'Re-read after offering',
  },
};

// -----------------------------------------------------------------
// SIGNALS · hardcoded interpretation labels per verdict
// These are chart signal descriptions, not dynamic API data
// -----------------------------------------------------------------
const SIGNALS = {
  yes:  ['Mars in 10H · gain axis open', 'Jupiter aspect on 1H · sealing', 'No retrograde in operative houses'],
  wait: ['Mercury in retrograde shadow · until 9 Jun', 'Lunar void 14-16h IST today', 'Comm channels distort short-form first'],
  no:   ['Rahu in 7H · partnership counter-signal', 'Saturn aspect on 1H lord · drag', 'Eclipse shadow within 30 days'],
  pray: ['Saturn--Rahu fold in 9H axis', 'Karmic ledger flag · gate G03', 'Offering window · next 9 days'],
};

const ArrowIcon = () => (
  <svg className="ov-banner__cta-arrow" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="2" y1="6" x2="10" y2="6"/><polyline points="7,3 10,6 7,9"/>
  </svg>
);

// -----------------------------------------------------------------
// Banner -- single verdict state panel
// Step 2: banner data from BANNERS constant (hardcoded per verdict)
//         signals from SIGNALS constant (hardcoded per verdict)
// -----------------------------------------------------------------
export function Banner({ verdict, onCtaClick, onReadChartClick }) {
  const b = BANNERS[verdict] || BANNERS.wait;
  const signals = SIGNALS[verdict] || [];
  const isPray = verdict === 'pray';
  return (
    <article className={`ov-banner ov-banner--${verdict}`}>
      <div className="ov-banner__left">
        <span className="ov-banner__eyebrow">
          Active verdict &middot; <b>{verdict.toUpperCase()}</b>
          <VerdictChip type={verdict} active />
        </span>
        <h2 className="ov-banner__headline">{b.headline}</h2>
        <p className="ov-banner__reasoning">&ldquo;{b.reasoning}&rdquo;</p>
        <div className="ov-banner__cta-row">
          <button
            type="button"
            className={`ov-banner__cta ${isPray ? 'ov-banner__cta--pray' : ''}`}
            onClick={onCtaClick}
          >
            {b.cta} <ArrowIcon />
          </button>
          <button
            type="button"
            className="ov-banner__cta-secondary"
            onClick={onReadChartClick}
          >
            Read the chart
          </button>
        </div>
      </div>
      <aside className="ov-banner__right">
        <div className="ov-banner__right-chip-line">
          <span className="ov-banner__right-lbl">Re-read window</span>
        </div>
        <div className="ov-banner__right-row">
          <span className="ov-banner__right-lbl">Validity</span>
          <b>{b.window}</b>
        </div>
        <div className="ov-banner__right-row">
          <span className="ov-banner__right-lbl">Signals informing this verdict</span>
          <div className="ov-banner__signals">
            {signals.map((s, i) => (
              <div key={i} className="ov-banner__signal">{s}</div>
            ))}
          </div>
        </div>
      </aside>
    </article>
  );
}

// -----------------------------------------------------------------
// ContextStrip -- 4-cell seeker context bar
// Below-banner context, stays put across verdicts.
// TT confirmed include (2026-05-29).
// Step 2: hardcoded SEEKER fields replaced with explicit props
//
// Props: { tier, score, streakDays, karmic, asOf }
// -----------------------------------------------------------------
export function ContextStrip({ tier, score, streakDays, karmic, asOf }) {
  return (
    <div className="ov-context">
      <div className="ov-context__cell">
        <span className="ov-context__l">Seeker</span>
        <span className="ov-context__v">{tier || '--'}</span>
        <span className="ov-context__sub">score {score || 0} / 99 &middot; streak {streakDays || 0}d</span>
      </div>
      <div className="ov-context__cell">
        <span className="ov-context__l">Question class</span>
        <span className="ov-context__v">Pre-flight</span>
        <span className="ov-context__sub">free-form &middot; short-horizon</span>
      </div>
      <div className="ov-context__cell">
        <span className="ov-context__l">Karmic</span>
        <span className="ov-context__v">{karmic || '--'}</span>
        <span className="ov-context__sub">ledger state</span>
      </div>
      <div className="ov-context__cell">
        <span className="ov-context__l">As of</span>
        <span className="ov-context__v">{asOf ? asOf.split(' · ')[1] || asOf : '--'}</span>
        <span className="ov-context__sub">{asOf ? asOf.split(' · ')[0] || '' : ''} &middot; re-read on demand</span>
      </div>
    </div>
  );
}

// -----------------------------------------------------------------
// OracleVerdictProofStrip -- VerdictChip proof set
// CD design canvas component. No live data. Retained per TT variant policy.
// -----------------------------------------------------------------
export function OracleVerdictProofStrip() {
  return (
    <div className="ov-proof">
      <div className="ov-proof__head">
        <span className="ov-proof__eyebrow">VerdictChip system &middot; proof set</span>
        <span className="ov-proof__note">
          Chip type &middot; always full gold &middot; banner surface (here) carries the gold&harr;rahu gradient on PRAY
        </span>
      </div>
      <div className="ov-proof__row">
        <VerdictChip type="yes" />
        <VerdictChip type="wait" />
        <VerdictChip type="no" />
        <VerdictChip type="pray" />
      </div>
    </div>
  );
}

// -----------------------------------------------------------------
// OracleVerdictBanners -- main exported component
// Receives: { data, asOf }
//   data   -- live API response from /api/strategist/dashboard
//   asOf   -- display timestamp string
//
// Live API field map (PROCESS_CD_INTEGRATION_PROTOCOL.md §5):
//   verdict     <- data.scoreboard.gate0_last_verdict (lowercased)
//   banners     <- hardcoded BANNERS constant (interpretation content)
//   score       <- data.conquest_probability.score
//   tier        <- data.scoreboard.score_tier
//   streakDays  <- data.scoreboard.streak_days
//   karmic      <- data.diagnosis_summary.karmic_debt_cleared
// -----------------------------------------------------------------
// showProofStrip defaults false on live page. Pass true only in dev / design review.
export default function OracleVerdictBanners({ data, asOf, onCtaClick, onReadChartClick, showProofStrip = false }) {
  // Step 6 -- wire live API fields
  // karmic_debt_cleared lives in scoreboard (boolean), not diagnosis_summary
  const verdict     = (data?.scoreboard?.gate0_last_verdict ?? 'wait').toLowerCase();
  const score       = data?.conquest_probability?.score ?? 0;
  const tier        = data?.scoreboard?.score_tier ?? '--';
  const streakDays  = data?.scoreboard?.streak_days ?? 0;
  const karmicRaw   = data?.scoreboard?.karmic_debt_cleared;
  const karmic      = karmicRaw === true ? 'Cleared' : karmicRaw === false ? 'Active' : '--';

  // Local toggle: allow seeker to preview other verdict states
  const [activeVerdict, setActiveVerdict] = useState(verdict);

  // Sync local state when live verdict changes
  React.useEffect(() => {
    setActiveVerdict(verdict);
  }, [verdict]);

  return (
    <>
      <SectionHeader
        title="Oracle Verdict"
        meta={null}
        right={
          <SegPill
            segments={[
              { value: 'yes',  label: 'yes'  },
              { value: 'wait', label: 'wait' },
              { value: 'no',   label: 'no'   },
              { value: 'pray', label: 'pray' },
            ]}
            value={activeVerdict}
            onChange={setActiveVerdict}
            size="md"
            ariaLabel="Verdict state"
          />
        }
      />

      <Banner
        verdict={activeVerdict}
        onCtaClick={onCtaClick}
        onReadChartClick={onReadChartClick}
      />

      <ContextStrip
        tier={tier}
        score={score}
        streakDays={streakDays}
        karmic={karmic}
        asOf={asOf}
      />

      {showProofStrip && <OracleVerdictProofStrip />}
    </>
  );
}
