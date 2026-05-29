// -----------------------------------------------------------------
// PrayPath.jsx
// Source: STR-2I · PrayPath.html  (CD delivery)
// Extracted + converted: 2026-05-29
// 6-step recipe: PROCESS_CD_INTEGRATION_PROTOCOL.md
//
// Render rule: conditionally mounted on PRAY verdict.
// The Action Plan page mounts this only when verdict === 'pray'.
// Gradient header (gold<->rahu) is a pre-blessed v2 surface treatment.
//
// Exports:
//   default  PrayPath   -- main component, receives { data, asOf }
//   named    CTACard    -- single offering card (mantra/offering/pilgrimage)
//   named    FocusCard  -- single-primary focus mode with alt switcher
//   named    Triptych   -- 3-card horizontal layout
//
// CSS: import '../../../styles/strategist-2i-praypath.css'
// -----------------------------------------------------------------

// Step 1 -- React import
import React, { useState } from 'react';

// Step 5 -- shared primitives
import { SegPill, VerdictChip, SectionHeader } from './StrategistPrimitives';

// -----------------------------------------------------------------
// PRAY_DATA · hardcoded offering content (field map: pray = hardcoded)
// Source: _assets/strategist-primitives.jsx SEEKER.pray
// -----------------------------------------------------------------
const PRAY_DATA = {
  headline: 'The chart asks for offering before action.',
  sub: 'Saturn--Rahu fold in the 9H axis · the obstruction is karmic. Three offerings; pick the one your week can hold.',
  ctas: [
    {
      code: '01', kind: 'mantra',
      title: 'The Mantra',
      body: 'Aditya Hridayam · 7 recitations · sunrise · 9 consecutive days. Opens the surya channel for verdict re-read.',
      commitment: '~14 min/day',
      weight: 'lightest',
    },
    {
      code: '02', kind: 'offering',
      title: 'The Offering',
      body: 'Black sesame · running water · Saturday before sunset. Closes the saturn ledger thread named in Gate 03.',
      commitment: '~30 min · once',
      weight: 'middle',
    },
    {
      code: '03', kind: 'pilgrimage',
      title: 'The Yatra',
      body: 'Single-day visit to a Saturn-temple or river confluence inside 100km. The chart re-reads within 7 days of return.',
      commitment: '1 day · ~₹2k',
      weight: 'heaviest',
    },
  ],
};

// -----------------------------------------------------------------
// SVG icons -- Mantra · Offering · Pilgrimage (from CD)
// -----------------------------------------------------------------
const IconMantra = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="9" />
    <path d="M8 14c1.5 1.5 4 1.5 5.5 0 1.5-1.5 1.5-4 0-5.5-.6-.6-1.4-.9-2.2-.9" />
    <circle cx="14.5" cy="6.5" r="1" fill="currentColor" />
  </svg>
);
const IconOffering = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 11h16l-1.5 7a2 2 0 0 1-2 1.5h-9a2 2 0 0 1-2-1.5L4 11Z" />
    <path d="M12 4c-1.2 2 1.2 3 0 5" />
  </svg>
);
const IconYatra = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <path d="M5 19c0-3 2-5 4-5s4 2 4 5" />
    <circle cx="9" cy="11" r="2" />
    <path d="M16 7l4 0M20 7l-2-2M20 7l-2 2" />
    <path d="M16 14l4 0M20 14l-2-2M20 14l-2 2" />
  </svg>
);

const ICONS = { mantra: IconMantra, offering: IconOffering, pilgrimage: IconYatra };

// -----------------------------------------------------------------
// CTACard -- single offering card (triptych view)
// -----------------------------------------------------------------
export function CTACard({ cta, onBegin }) {
  const Icon = ICONS[cta.kind] || IconMantra;
  return (
    <article className="pp-card">
      <div className="pp-card__head">
        <span className="pp-card__code">offering &middot; {cta.code}</span>
        <span className="pp-card__weight">{cta.weight}</span>
      </div>
      <span className="pp-card__icon" aria-hidden="true"><Icon /></span>
      <span className="pp-card__kind">{cta.kind}</span>
      <h3 className="pp-card__title">{cta.title}</h3>
      <p className="pp-card__body">&ldquo;{cta.body}&rdquo;</p>
      <div className="pp-card__foot">
        <span className="pp-card__commit"><b>{cta.commitment}</b></span>
        <button type="button" className="pp-card__cta" onClick={onBegin}>
          Begin
          <svg width="11" height="11" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="2" y1="6" x2="10" y2="6"/><polyline points="7,3 10,6 7,9"/>
          </svg>
        </button>
      </div>
    </article>
  );
}

// -----------------------------------------------------------------
// Triptych -- 3 offering cards side-by-side
// -----------------------------------------------------------------
export function Triptych({ ctas, onBegin }) {
  return (
    <div className="pp-triptych">
      {ctas.map((c) => <CTACard key={c.code} cta={c} onBegin={() => onBegin && onBegin(c.code)} />)}
    </div>
  );
}

// -----------------------------------------------------------------
// FocusCard -- single primary offering in focus mode with alt switcher
// Step 2: ctas received as props (was window.SEEKER.pray.ctas)
// -----------------------------------------------------------------
export function FocusCard({ ctas, focusCode, onFocus, onBegin }) {
  const focus = ctas.find((c) => c.code === focusCode) || ctas[0];
  const alts = ctas.filter((c) => c.code !== focus.code);
  const Icon = ICONS[focus.kind] || IconMantra;
  return (
    <section className="pp-focus">
      <div className="pp-focus__icon-block">
        <span className="pp-focus__icon" aria-hidden="true"><Icon /></span>
        <span className="pp-focus__code">offering &middot; {focus.code}</span>
        <span className="pp-focus__weight">{focus.weight}</span>
      </div>
      <div className="pp-focus__right">
        <span className="pp-focus__kind">{focus.kind}</span>
        <h3 className="pp-focus__title">{focus.title}</h3>
        <p className="pp-focus__body">&ldquo;{focus.body}&rdquo;</p>
        <div className="pp-focus__row">
          <button type="button" className="pp-focus__cta" onClick={() => onBegin && onBegin(focus.code)}>
            Begin &middot; {focus.commitment}
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="2" y1="6" x2="10" y2="6"/><polyline points="7,3 10,6 7,9"/>
            </svg>
          </button>
        </div>
        <div className="pp-focus__alt-row">
          <span>or &middot; <b>switch focus</b> &middot;</span>
          {alts.map((alt) => (
            <button
              key={alt.code}
              type="button"
              className="pp-focus__alt"
              onClick={() => onFocus(alt.code)}
            >
              {alt.kind}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}

// -----------------------------------------------------------------
// PrayPath -- main exported component
// Receives: { data, asOf }
//   data  -- live API response from /api/strategist/dashboard
//   asOf  -- display timestamp string
//
// Live API field map:
//   pray content  <- PRAY_DATA hardcoded (field map: pray = hardcoded)
//   verdict       <- data.scoreboard.gate0_last_verdict (confirmation)
//
// Render rule: parent page should only mount this when
//   verdict === 'pray'
// -----------------------------------------------------------------
// view: optional override ('triptych'|'focus'). When provided, hides internal toggle.
export default function PrayPath({ data, asOf, onBegin, view: viewProp = null, showToggle }) {
  const [viewState, setViewState] = useState('triptych');
  const controlled = viewProp !== null;
  const view = controlled ? viewProp : viewState;
  const setView = controlled ? () => {} : setViewState;
  const showToggleActual = showToggle !== undefined ? showToggle : !controlled;
  const [focusCode, setFocusCode] = useState('02'); /* middleweight default */

  const p = PRAY_DATA;

  return (
    <>
      <SectionHeader
        title="The Pray Path"
        meta={null}
        right={showToggleActual ? (
          <SegPill
            segments={[
              { value: 'triptych', label: 'triptych' },
              { value: 'focus',    label: 'focus' },
            ]}
            value={view}
            onChange={setView}
            size="sm"
            ariaLabel="Pray path layout"
          />
        ) : null}
      />

      {/* Gradient header · v2 pre-blessed gold<->rahu surface */}
      <header className="pp-header">
        <div className="pp-header__top">
          <VerdictChip type="pray" />
          <span className="pp-header__sep" aria-hidden="true"></span>
          <span className="pp-header__eyebrow">The chart asks for offering</span>
          <span style={{ flexGrow: 1 }}></span>
          <span className="pp-header__seal">re-read &middot; within 7 days of offering</span>
        </div>
        <h2 className="pp-header__title">{p.headline}</h2>
        <p className="pp-header__sub">&ldquo;{p.sub}&rdquo;</p>
      </header>

      {view === 'triptych'
        ? <Triptych ctas={p.ctas} onBegin={onBegin} />
        : <FocusCard ctas={p.ctas} focusCode={focusCode} onFocus={setFocusCode} onBegin={onBegin} />
      }

      <div className="pp-proof">
        <span className="pp-proof__lbl">chip-vs-banner rule</span>
        <span className="pp-proof__chip"><VerdictChip type="pray" /></span>
        <span className="pp-proof__note">
          The chip stays full gold above. The gradient lives on the <em>header surface</em> &mdash; the page-level gold&harr;rahu treatment, plus the CTA gradient in focus mode. One rule, two patterns (v2 &sect;1).
        </span>
      </div>
    </>
  );
}
