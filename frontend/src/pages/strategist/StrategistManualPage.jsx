import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import '../../styles/strategist-manual.css';

const THEMES = [
  { id: 'dark',        label: 'dark' },
  { id: 'light',       label: 'light' },
  { id: 'cr-ambient',  label: 'cr·amb' },
  { id: 'cr-tactical', label: 'cr·tac' },
];
const STORAGE_KEY = 'strategist_theme_mode';

function ThemePill({ theme, setTheme }) {
  return (
    <div className="theme-pill" role="group" aria-label="Theme">
      {THEMES.map((t) => (
        <button
          key={t.id}
          type="button"
          className={`theme-pill__seg${theme === t.id ? ' is-on' : ''}`}
          onClick={() => setTheme(t.id)}
        >
          {t.label}
        </button>
      ))}
    </div>
  );
}

export default function StrategistManualPage() {
  const [theme, setThemeState] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return THEMES.some((t) => t.id === saved) ? saved : 'dark';
    } catch {
      return 'dark';
    }
  });

  const [activeSection, setActiveSection] = useState('orientation');
  const [mobileSection, setMobileSection] = useState('#orientation');
  const railRef = useRef(null);

  const setTheme = (id) => {
    setThemeState(id);
    try { localStorage.setItem(STORAGE_KEY, id); } catch {}
  };

  // Scroll-spy via IntersectionObserver
  useEffect(() => {
    const sections = document.querySelectorAll('.str-manual .sec');
    if (!('IntersectionObserver' in window) || sections.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            setActiveSection(en.target.id);
            setMobileSection('#' + en.target.id);
          }
        });
      },
      { rootMargin: '-20% 0px -70% 0px', threshold: 0 }
    );
    sections.forEach((s) => observer.observe(s));
    return () => observer.disconnect();
  }, []);

  const handleMobileNav = (e) => {
    window.location.hash = e.target.value;
    setMobileSection(e.target.value);
  };

  return (
    <div className="str-manual" data-mode={theme}>
      <div className="manual">

        {/* ══════════════ DESKTOP SIDEBAR ══════════════ */}
        <aside className="rail" ref={railRef} aria-label="Manual navigation">
          <div className="rail__brand">
            <div className="rail__class">Field Manual · Strategist Eyes</div>
            <h2 className="rail__title">The Strategist</h2>
            <p className="rail__sub">A war room for karma</p>
          </div>
          <nav className="rail__nav" aria-label="Sections">
            <div className="rail__group">Brief</div>
            <a className={`rail__link${activeSection === 'orientation' ? ' is-active' : ''}`} href="#orientation">
              <span className="n">00</span><span>Orientation</span>
            </a>
            <a className={`rail__link${activeSection === 'flow' ? ' is-active' : ''}`} href="#flow">
              <span className="n">01</span><span>Navigation Flow</span>
            </a>
            <div className="rail__group">The Surfaces</div>
            <a className={`rail__link${activeSection === 'screens' ? ' is-active' : ''}`} href="#screens">
              <span className="n">02</span><span>The Eight Screens</span>
            </a>
            <a className={`rail__link${activeSection === 'layers' ? ' is-active' : ''}`} href="#layers">
              <span className="n">03</span><span>The Six Layers</span>
            </a>
            <div className="rail__group">Reading the Signals</div>
            <a className={`rail__link${activeSection === 'verdicts' ? ' is-active' : ''}`} href="#verdicts">
              <span className="n">04</span><span>Verdict States</span>
            </a>
            <a className={`rail__link${activeSection === 'bands' ? ' is-active' : ''}`} href="#bands">
              <span className="n">05</span><span>Score Bands</span>
            </a>
            <a className={`rail__link${activeSection === 'hurdles' ? ' is-active' : ''}`} href="#hurdles">
              <span className="n">06</span><span>Hurdle Alerts</span>
            </a>
            <a className={`rail__link${activeSection === 'surrogate' ? ' is-active' : ''}`} href="#surrogate">
              <span className="n">07</span><span>Surrogate Bridge</span>
            </a>
            <a className={`rail__link${activeSection === 'missions' ? ' is-active' : ''}`} href="#missions">
              <span className="n">08</span><span>Missions</span>
            </a>
            <div className="rail__group">Reference</div>
            <a className={`rail__link${activeSection === 'glossary' ? ' is-active' : ''}`} href="#glossary">
              <span className="n">09</span><span>Glossary · 18 terms</span>
            </a>
          </nav>
        </aside>

        {/* ══════════════ MOBILE TOP BAR ══════════════ */}
        <div className="mbar">
          <div className="mbar__row">
            <div className="mbar__brand">The <span>Strategist</span> · Manual</div>
            <ThemePill theme={theme} setTheme={setTheme} />
          </div>
          <select
            className="mbar__select"
            value={mobileSection}
            onChange={handleMobileNav}
            aria-label="Jump to section"
          >
            <option value="#orientation">00 · Orientation</option>
            <option value="#flow">01 · Navigation Flow</option>
            <option value="#screens">02 · The Eight Screens</option>
            <option value="#layers">03 · The Six Layers</option>
            <option value="#verdicts">04 · Verdict States</option>
            <option value="#bands">05 · Score Bands</option>
            <option value="#hurdles">06 · Hurdle Alerts</option>
            <option value="#surrogate">07 · Surrogate Bridge</option>
            <option value="#missions">08 · Missions</option>
            <option value="#glossary">09 · Glossary</option>
          </select>
        </div>

        {/* ══════════════ CONTENT ══════════════ */}
        <main className="content">
          <div className="content__inner">

            {/* MASTHEAD */}
            <header className="masthead">
              <div className="masthead__topline">
                <div className="masthead__route">
                  route · <b>/strategist/manual</b>
                </div>
                <ThemePill theme={theme} setTheme={setTheme} />
              </div>
              <div className="masthead__kicker">STR-UM-01 · User Field Manual</div>
              <h1>The Strategist<br />Field Manual</h1>
              <p className="lede">
                Everything the module does, in one brief -- the eight surfaces you can stand on,
                the six layers beneath each verdict, and the language the war room speaks. Read it
                once before your first consult; return to it whenever a signal needs decoding.
              </p>
              <div className="masthead__meta">
                <div><b>Module</b> The Strategist</div>
                <div><b>Platform</b> EverydayHoroscope</div>
                <div><b>Screens</b> 8</div>
                <div><b>Layers</b> 6 · Gate 0 → Brief</div>
                <div><b>Themes</b> light · dark · cr-ambient · cr-tactical</div>
              </div>
            </header>

            {/* 00 · ORIENTATION */}
            <section className="sec" id="orientation">
              <div className="sec__head">
                <span className="sec__n">00</span>
                <h2 className="sec__title">Orientation</h2>
                <p className="sec__lede">What you are looking at, and the posture it asks of you.</p>
              </div>
              <div className="prose">
                <p>
                  The Strategist is a <strong>business-intelligence war room for your karma</strong> -- a
                  Bloomberg terminal where the tickers are transits, the positions are planetary, and the
                  P&amp;L is the work you owe your ancestors. It reads your live birth chart, your current
                  dasha, today's transits, and your Lal Kitab diagnostic, then turns them into missions you
                  can actually execute.
                </p>
                <p>
                  Nothing here is guesswork. Every number on screen is computed from your chart through the
                  astrology engine and the <span className="mono-inline">Conquest Probability</span> algorithm --
                  never authored, never faked. The module speaks in tactics -- <strong>missions, hurdles,
                  pivots, golden hours</strong> -- but the discipline underneath it is devotional. You are
                  not beating the market. You are settling debts and timing your moves to the sky.
                </p>
                <p>
                  <strong>How to read the manual.</strong> §01 maps how the eight screens connect. §02
                  catalogues each screen -- its route, what it shows, how you get in and out. §03 opens the
                  six layers that sit beneath every verdict. §04-§08 decode the signals you will see most:
                  verdicts, score bands, hurdle alerts, the surrogate bridge, and missions. §09 is the
                  glossary. Use the rail on the left -- or the dropdown on a phone -- to jump anywhere.
                </p>
              </div>
            </section>

            {/* 01 · NAVIGATION FLOW */}
            <section className="sec" id="flow">
              <div className="sec__head">
                <span className="sec__n">01</span>
                <h2 className="sec__title">Navigation Flow</h2>
                <p className="sec__lede">How a consult moves through the eight surfaces, ① to ⑧.</p>
              </div>
              <div className="flow">
                <a className="flow__node" href="#screen-1">
                  <span className="flow__num">①</span>
                  <span className="flow__name">War Room Dashboard</span>
                  <span className="flow__route">/strategist</span>
                </a>
                <span className="flow__arrow">→</span>
                <a className="flow__node" href="#screen-2">
                  <span className="flow__num">②</span>
                  <span className="flow__name">Gate 0 · Oracle</span>
                  <span className="flow__route">/krishna-prashnavali</span>
                </a>
                <span className="flow__arrow">→</span>
                <a className="flow__node" href="#screen-3">
                  <span className="flow__num">③</span>
                  <span className="flow__name">Pre-Flight / Surrender Gate</span>
                  <span className="flow__route">/strategist · state</span>
                </a>
                <span className="flow__arrow">→</span>
                <a className="flow__node" href="#screen-4">
                  <span className="flow__num">④</span>
                  <span className="flow__name">Mission Board</span>
                  <span className="flow__route">/strategist/missions</span>
                </a>
                <span className="flow__arrow">→</span>
                <a className="flow__node" href="#screen-5">
                  <span className="flow__num">⑤</span>
                  <span className="flow__name">Surrogate Bridge</span>
                  <span className="flow__route">/strategist/surrogate</span>
                </a>
                <span className="flow__arrow">→</span>
                <a className="flow__node" href="#screen-6">
                  <span className="flow__num">⑥</span>
                  <span className="flow__name">Action Plan</span>
                  <span className="flow__route">/strategist/action-plan</span>
                </a>
                <span className="flow__arrow">→</span>
                <a className="flow__node" href="#screen-7">
                  <span className="flow__num">⑦</span>
                  <span className="flow__name">Executive Brief</span>
                  <span className="flow__route">/strategist/report</span>
                </a>
                <span className="flow__arrow">→</span>
                <a className="flow__node" href="#screen-8">
                  <span className="flow__num">⑧</span>
                  <span className="flow__name">Field Manual</span>
                  <span className="flow__route">/strategist/manual</span>
                </a>
              </div>
              <p className="flow__legend">
                ① is home base. ② is the gate every question passes through. ③ only appears on a{' '}
                <span className="mono-inline">WAIT</span> / <span className="mono-inline">NO</span> /{' '}
                <span className="mono-inline">PRAY</span> verdict -- clear it and you re-enter the loop at ①.{' '}
                ④-⑦ are the working surfaces a <span className="mono-inline">YES</span> unlocks. ⑧ is here.
              </p>
            </section>

            {/* 02 · THE EIGHT SCREENS */}
            <section className="sec" id="screens">
              <div className="sec__head">
                <span className="sec__n">02</span>
                <h2 className="sec__title">The Eight Screens</h2>
                <p className="sec__lede">Each surface with its route, what it shows, and how you move in and out.</p>
              </div>
              <div className="screens">

                {/* Screen 1 */}
                <article className="screen" id="screen-1">
                  <div className="screen__top">
                    <span className="screen__idx">①</span>
                    <div className="screen__heads">
                      <h3 className="screen__name">War Room Dashboard</h3>
                      <span className="route-chip">/strategist</span>
                    </div>
                    <div className="screen__layer">Layer 6 · live · home base</div>
                  </div>
                  <p className="screen__purpose">Your command surface. A full-viewport horizontal scroll that snaps through Layers 1-5, with the Gate 0 verdict held sticky above it -- the same on phone and desktop.</p>
                  <div className="screen__grid">
                    <div className="screen__block">
                      <div className="lbl">What it shows</div>
                      <ul className="screen__list">
                        <li>State banner -- OFFENSIVE / GOLDEN HOUR / DEFENSIVE</li>
                        <li>Conquest Probability gauge, 0-99%</li>
                        <li>Active mission ticker (transit-triggered)</li>
                        <li>Success &amp; Debt scoreboard -- streaks, discipline %, debt cleared</li>
                        <li>Hurdle alerts and the Golden Hour countdown</li>
                      </ul>
                    </div>
                    <div className="screen__block">
                      <div className="lbl">How to navigate</div>
                      <p className="nav-line"><b>In</b>The Strategist link in the top menu bar.</p>
                      <p className="nav-line" style={{ marginTop: 12 }}><b>Move</b>Swipe / arrow-key through Layers 1-5; the sticky Gate 0 chip stays pinned. Page-indicator dots show position.</p>
                      <p className="nav-line" style={{ marginTop: 12 }}><b>Out</b>Cards deep-link to the Oracle, Mission Board, Surrogate Bridge and Action Plan.</p>
                    </div>
                  </div>
                </article>

                {/* Screen 2 */}
                <article className="screen" id="screen-2">
                  <div className="screen__top">
                    <span className="screen__idx">②</span>
                    <div className="screen__heads">
                      <h3 className="screen__name">Krishna Prashnavali · Gate 0</h3>
                      <span className="route-chip">/krishna-prashnavali</span>
                    </div>
                    <div className="screen__layer">Layer 0 · the oracle gate</div>
                  </div>
                  <p className="screen__purpose">The oracle every question passes through first: <em>"Should I act on this at all?"</em> Lives both as a standalone page and embedded inline in the War Room as the "Consult the Oracle" card.</p>
                  <div className="screen__grid">
                    <div className="screen__block">
                      <div className="lbl">What it shows</div>
                      <ul className="screen__list">
                        <li>A field to type your question</li>
                        <li>An 18×18 selection grid -- 324 cells</li>
                        <li>One of 36 canonical answers + its behavioural remedy</li>
                        <li>A verdict: YES · WAIT · NO · PRAY</li>
                      </ul>
                    </div>
                    <div className="screen__block">
                      <div className="lbl">How to navigate</div>
                      <p className="nav-line"><b>In</b>Top-bar link, or the War Room "Consult the Oracle" card (returns the verdict inline -- never navigates away).</p>
                      <p className="nav-line" style={{ marginTop: 12 }}><b>Out</b>YES → straight into Layer 1. WAIT / NO / PRAY → the Pre-Flight / Surrender gate (③).</p>
                    </div>
                  </div>
                </article>

                {/* Screen 3 */}
                <article className="screen" id="screen-3">
                  <div className="screen__top">
                    <span className="screen__idx">③</span>
                    <div className="screen__heads">
                      <h3 className="screen__name">Pre-Flight / Surrender Gate</h3>
                      <span className="route-chip">/strategist · banner state</span>
                    </div>
                    <div className="screen__layer">conditional · verdict-driven</div>
                  </div>
                  <p className="screen__purpose">Not a separate page so much as a held state of the War Room. It appears only when Gate 0 returns anything but YES, and it tells you exactly what clears the hold.</p>
                  <div className="screen__grid">
                    <div className="screen__block">
                      <div className="lbl">What it shows</div>
                      <ul className="screen__list">
                        <li><b style={{ color: 'var(--amber)' }}>WAIT</b> → Pre-Flight banner: "Day X of 43 → Auto-Unlock"</li>
                        <li><b style={{ color: 'var(--red)' }}>NO</b> → Karmic Hold: "Score 47 / 60 needed"</li>
                        <li><b style={{ color: 'var(--gold)' }}>PRAY</b> → Full Surrender: 3-module plan, ≥75% to re-test</li>
                        <li>Assigned remedy plan + progress toward re-entry</li>
                      </ul>
                    </div>
                    <div className="screen__block">
                      <div className="lbl">How to navigate</div>
                      <p className="nav-line"><b>In</b>Automatically, on a WAIT / NO / PRAY verdict from Gate 0.</p>
                      <p className="nav-line" style={{ marginTop: 12 }}><b>Out</b>WAIT auto-unlocks on remedy completion. NO / PRAY unlock a Gate 0 re-test once the score clears its threshold -- see §04.</p>
                    </div>
                  </div>
                </article>

                {/* Screen 4 */}
                <article className="screen" id="screen-4">
                  <div className="screen__top">
                    <span className="screen__idx">④</span>
                    <div className="screen__heads">
                      <h3 className="screen__name">Mission Board</h3>
                      <span className="route-chip">/strategist/missions</span>
                    </div>
                    <div className="screen__layer">Layer 3 · the engine output</div>
                  </div>
                  <p className="screen__purpose">The grid of every mission your current transits have triggered -- each one a concrete move with a target and a linked remedy.</p>
                  <div className="screen__grid">
                    <div className="screen__block">
                      <div className="lbl">What it shows</div>
                      <ul className="screen__list">
                        <li>Mission cards: name, objective, pivot action, KPI target</li>
                        <li>Linked remedy ID, cross-referenced to the LK engine</li>
                        <li>"Add Remedy to Tracker" on each card</li>
                        <li>Filters: by planet, by house, by date range</li>
                      </ul>
                    </div>
                    <div className="screen__block">
                      <div className="lbl">How to navigate</div>
                      <p className="nav-line"><b>In</b>War Room mission ticker, or top-bar link.</p>
                      <p className="nav-line" style={{ marginTop: 12 }}><b>Out</b>"Add to Tracker" cross-links into the 43-Day Tracker in the LK Standalone module. See §08 for card anatomy.</p>
                    </div>
                  </div>
                </article>

                {/* Screen 5 */}
                <article className="screen" id="screen-5">
                  <div className="screen__top">
                    <span className="screen__idx">⑤</span>
                    <div className="screen__heads">
                      <h3 className="screen__name">Surrogate Bridge</h3>
                      <span className="route-chip">/strategist/surrogate</span>
                    </div>
                    <div className="screen__layer">Layer 3 · the family gate</div>
                  </div>
                  <p className="screen__purpose">When a remedy needs a relative who is no longer available, this surface finds the sanctioned substitute -- and rewards activating it.</p>
                  <div className="screen__grid">
                    <div className="screen__block">
                      <div className="lbl">What it shows</div>
                      <ul className="screen__list">
                        <li>Three selectors: planet · relative unavailable · industry</li>
                        <li>The matched surrogate record + its pivot action</li>
                        <li>Activation toggle -- adds <b style={{ color: 'var(--emerald)' }}>+12</b> to Conquest Probability</li>
                      </ul>
                    </div>
                    <div className="screen__block">
                      <div className="lbl">How to navigate</div>
                      <p className="nav-line"><b>In</b>Surfaces automatically when the family census shows an unavailable relative; also reachable from the War Room.</p>
                      <p className="nav-line" style={{ marginTop: 12 }}><b>Out</b>Activating writes back to the score and returns you to the War Room. See §07.</p>
                    </div>
                  </div>
                </article>

                {/* Screen 6 */}
                <article className="screen" id="screen-6">
                  <div className="screen__top">
                    <span className="screen__idx">⑥</span>
                    <div className="screen__heads">
                      <h3 className="screen__name">Strategist Action Plan</h3>
                      <span className="route-chip">/strategist/action-plan</span>
                    </div>
                    <div className="screen__layer">Layer 4 · the assembled page</div>
                  </div>
                  <p className="screen__purpose">The whole consult assembled into one chart-led page, driven by a single Command / Briefing density control.</p>
                  <div className="screen__grid">
                    <div className="screen__block">
                      <div className="lbl">What it shows</div>
                      <ul className="screen__list">
                        <li>Five sections in order: Digest → Diagnostics → Verdict → Active path → Action Queue</li>
                        <li>The Active-path slot renders four ways on the verdict</li>
                        <li>The Action Queue -- three moves distilled from verdict + gates</li>
                      </ul>
                    </div>
                    <div className="screen__block">
                      <div className="lbl">How to navigate</div>
                      <p className="nav-line"><b>In</b>War Room "Action Plan snapshot" card, or top-bar link.</p>
                      <p className="nav-line" style={{ marginTop: 12 }}><b>Control</b>One control only -- the sticky Command / Briefing strip sets density for every section.</p>
                    </div>
                  </div>
                </article>

                {/* Screen 7 */}
                <article className="screen" id="screen-7">
                  <div className="screen__top">
                    <span className="screen__idx">⑦</span>
                    <div className="screen__heads">
                      <h3 className="screen__name">Executive Intelligence Brief</h3>
                      <span className="route-chip">/strategist/report</span>
                    </div>
                    <div className="screen__layer">Layer 5 · premium output · PDF</div>
                  </div>
                  <p className="screen__purpose">The premium, gated export -- your consult bound into a four-part intelligence brief you can keep.</p>
                  <div className="screen__grid">
                    <div className="screen__block">
                      <div className="lbl">What it shows</div>
                      <ul className="screen__list">
                        <li>I · Conquest Probability + Gate 0 verdict</li>
                        <li>II · 7-Day Tactical Battle Plan</li>
                        <li>III · Karmic Remedy Override (active surrogate)</li>
                        <li>IV · Conquest Timeline -- the probability curve</li>
                      </ul>
                    </div>
                    <div className="screen__block">
                      <div className="lbl">How to navigate</div>
                      <p className="nav-line"><b>In</b>"Generate Brief" from the Action Plan or War Room.</p>
                      <p className="nav-line" style={{ marginTop: 12 }}><b>Gate</b>Premium (Razorpay). Renders to a downloadable PDF.</p>
                    </div>
                  </div>
                </article>

                {/* Screen 8 */}
                <article className="screen" id="screen-8">
                  <div className="screen__top">
                    <span className="screen__idx">⑧</span>
                    <div className="screen__heads">
                      <h3 className="screen__name">Field Manual</h3>
                      <span className="route-chip">/strategist/manual</span>
                    </div>
                    <div className="screen__layer">reference · this page</div>
                  </div>
                  <p className="screen__purpose">This document -- the reference you are reading now. Always one tap away from any screen.</p>
                  <div className="screen__grid">
                    <div className="screen__block">
                      <div className="lbl">What it shows</div>
                      <ul className="screen__list">
                        <li>The full screen + layer catalogue</li>
                        <li>Verdict, band, hurdle, surrogate and mission decoders</li>
                        <li>An 18-term glossary</li>
                      </ul>
                    </div>
                    <div className="screen__block">
                      <div className="lbl">How to navigate</div>
                      <p className="nav-line"><b>In</b>"Field Manual" link in the top bar, present on every Strategist surface.</p>
                      <p className="nav-line" style={{ marginTop: 12 }}><b>Move</b>Left rail on desktop; section dropdown on mobile.</p>
                    </div>
                  </div>
                </article>

              </div>
            </section>

            {/* 03 · THE SIX LAYERS */}
            <section className="sec" id="layers">
              <div className="sec__head">
                <span className="sec__n">03</span>
                <h2 className="sec__title">The Six Layers</h2>
                <p className="sec__lede">Gate 0 to Executive Brief -- the stack that produces every verdict and number.</p>
              </div>
              <div className="layers">

                {/* Layer 0 */}
                <div className="layer">
                  <div className="layer__head">
                    <span className="layer__tag">Layer 0 · Gate 0</span>
                    <h3 className="layer__name">Krishna Prashnavali</h3>
                    <span className="layer__src">kp_sessions</span>
                  </div>
                  <p className="layer__desc">The threshold question -- <strong>"Should I act on this?"</strong> Every consult begins here. The verdict it returns governs whether you proceed or enter a holding state.</p>
                  <table className="atable zebra">
                    <caption>Anatomy</caption>
                    <thead><tr><th>Element</th><th>Reads from</th><th>Output</th></tr></thead>
                    <tbody>
                      <tr><td>Question field</td><td>seeker input</td><td>free text</td></tr>
                      <tr><td>18×18 grid</td><td>324 cells</td><td>1 of 36 answers</td></tr>
                      <tr><td>Behavioural remedy</td><td>answer slot</td><td>conduct guidance</td></tr>
                      <tr><td>Verdict</td><td>answer mapping</td><td>YES · WAIT · NO · PRAY</td></tr>
                    </tbody>
                  </table>
                  <div className="note">
                    <div className="note__lbl">Verdict states</div>
                    <p><b style={{ color: 'var(--emerald)' }}>YES</b> (Pratibha) proceed · <b style={{ color: 'var(--amber)' }}>WAIT</b> (Dhairya) hold · <b style={{ color: 'var(--red)' }}>NO</b> (Pratrodha) remedy · <b style={{ color: 'var(--gold)' }}>PRAY</b> (Bhakti) surrender. Full re-entry logic in §04.</p>
                  </div>
                </div>

                {/* Layer 1 */}
                <div className="layer">
                  <div className="layer__head">
                    <span className="layer__tag">Layer 1</span>
                    <h3 className="layer__name">Astrology Engine</h3>
                    <span className="layer__src">vedic_calculator.py · mandatory</span>
                  </div>
                  <p className="layer__desc">The single source of truth for all live astronomy. It computes your chart, dasha and transits, and the strength scores that feed the Conquest Probability.</p>
                  <table className="atable zebra">
                    <caption>Anatomy</caption>
                    <thead><tr><th>Element</th><th>What it is</th><th>Feeds</th></tr></thead>
                    <tbody>
                      <tr><td>Birth chart</td><td>natal positions</td><td>mission triggers</td></tr>
                      <tr><td>Vimshottari Dasha</td><td>current period</td><td>timing context</td></tr>
                      <tr><td>Live transits</td><td>today's positions</td><td>active missions</td></tr>
                      <tr><td>Shadbala</td><td>command-planet strength</td><td>score ±10 / −5</td></tr>
                      <tr><td>Digbala</td><td>office vs power direction</td><td>score ±15 / −10</td></tr>
                    </tbody>
                  </table>
                </div>

                {/* Layer 2 */}
                <div className="layer">
                  <div className="layer__head">
                    <span className="layer__tag">Layer 2</span>
                    <h3 className="layer__name">Lal Kitab Diagnostic · 5 Gates</h3>
                    <span className="layer__src">POST /api/lk/diagnose</span>
                  </div>
                  <p className="layer__desc">Embedded inline in the dashboard. Five diagnostic gates surface the karmic conditions that bend your probability -- chief among them, ancestral debt.</p>
                  <table className="atable zebra">
                    <caption>The five gates</caption>
                    <thead><tr><th>Gate</th><th>Reads</th><th>Effect</th></tr></thead>
                    <tbody>
                      <tr><td>Gate 1</td><td>Karmic Debt -- Pitru Rin</td><td>score −20 if active</td></tr>
                      <tr><td>Gate 2</td><td>House Awakening</td><td>context</td></tr>
                      <tr><td>Gate 3</td><td>Year Cycle Planet</td><td>context</td></tr>
                      <tr><td>Gate 4</td><td>Mercury Scan</td><td>debt flag</td></tr>
                      <tr><td>Gate 5</td><td>Geographical Alignment</td><td>Digbala input</td></tr>
                    </tbody>
                  </table>
                </div>

                {/* Layer 3 */}
                <div className="layer">
                  <div className="layer__head">
                    <span className="layer__tag">Layer 3</span>
                    <h3 className="layer__name">Strategist Engine + Notifications</h3>
                    <span className="layer__src">strategist_engine.py</span>
                  </div>
                  <p className="layer__desc">Where the chart becomes action. It matches transits to missions, raises hurdle alerts, opens the surrogate bridge, runs the Golden Hour clock, and fires seven notification triggers -- always through the existing notification service, never directly.</p>
                  <table className="atable zebra">
                    <caption>Anatomy</caption>
                    <thead><tr><th>Module</th><th>Fires on</th></tr></thead>
                    <tbody>
                      <tr><td>Active Missions</td><td>transit matches trigger condition</td></tr>
                      <tr><td>Hurdle Alerts</td><td>retrograde · eclipse · combustion</td></tr>
                      <tr><td>Surrogate Bridge</td><td>family census gate</td></tr>
                      <tr><td>Golden Hour</td><td>sunset −30 min (state machine)</td></tr>
                      <tr><td>Notification Engine</td><td>7 Strategist triggers</td></tr>
                    </tbody>
                  </table>
                </div>

                {/* Layer 4 */}
                <div className="layer">
                  <div className="layer__head">
                    <span className="layer__tag">Layer 4</span>
                    <h3 className="layer__name">Remedies Action Plan</h3>
                    <span className="layer__src">merged timeline</span>
                  </div>
                  <p className="layer__desc">One unified timeline that braids together everything you need to <em>do</em> -- surfaced as the Action Plan page (⑥).</p>
                  <table className="atable zebra">
                    <caption>Merged sources</caption>
                    <thead><tr><th>Strand</th><th>Source</th></tr></thead>
                    <tbody>
                      <tr><td>Execution roadmap</td><td>LK days array</td></tr>
                      <tr><td>Mission pivots</td><td>Strategist pivot_actions</td></tr>
                      <tr><td>Surrogate activations</td><td>family-gate bridges</td></tr>
                      <tr><td>Tracker CTAs</td><td>43-Day Tracker</td></tr>
                    </tbody>
                  </table>
                </div>

                {/* Layer 5 */}
                <div className="layer">
                  <div className="layer__head">
                    <span className="layer__tag">Layer 5</span>
                    <h3 className="layer__name">Output · Premium Report</h3>
                    <span className="layer__src">GET /report/pdf · Razorpay</span>
                  </div>
                  <p className="layer__desc">The terminal layer: your consult bound into the Executive Intelligence Brief (⑦), a four-part PDF behind the premium gate.</p>
                  <table className="atable zebra">
                    <caption>Brief sections</caption>
                    <thead><tr><th>Section</th><th>Contents</th></tr></thead>
                    <tbody>
                      <tr><td>I</td><td>Conquest Probability + Gate 0 verdict</td></tr>
                      <tr><td>II</td><td>7-Day Tactical Battle Plan</td></tr>
                      <tr><td>III</td><td>Karmic Remedy Override (surrogate)</td></tr>
                      <tr><td>IV</td><td>Conquest Timeline -- probability curve</td></tr>
                    </tbody>
                  </table>
                </div>

              </div>
            </section>

            {/* 04 · VERDICT STATES */}
            <section className="sec" id="verdicts">
              <div className="sec__head">
                <span className="sec__n">04</span>
                <h2 className="sec__title">Verdict States</h2>
                <p className="sec__lede">The four answers Gate 0 can give -- and exactly what reopens the door.</p>
              </div>
              <div className="verdicts">
                <div className="vcard vcard--yes">
                  <div className="vcard__top">
                    <span className="verdict-chip verdict-chip--yes"><span className="verdict-chip__pip"></span>yes</span>
                    <span className="vcard__skt">Pratibha</span>
                  </div>
                  <p className="vcard__body">The sky is clear to act. You pass straight into Layer 1 and the working surfaces unlock.</p>
                  <div className="vcard__reentry"><b>Re-entry</b> -- none required. Proceed.</div>
                </div>
                <div className="vcard vcard--wait">
                  <div className="vcard__top">
                    <span className="verdict-chip verdict-chip--wait"><span className="verdict-chip__pip"></span>wait</span>
                    <span className="vcard__skt">Dhairya</span>
                  </div>
                  <p className="vcard__body">A temporal barrier. Pre-Flight Mode activates with a remedy plan; completing it auto-unlocks Layer 1.</p>
                  <div className="vcard__reentry"><b>Auto-unlock</b> -- no re-test. Banner: "Day X of 43 → Auto-Unlock".</div>
                </div>
                <div className="vcard vcard--no">
                  <div className="vcard__top">
                    <span className="verdict-chip verdict-chip--no"><span className="verdict-chip__pip"></span>no</span>
                    <span className="vcard__skt">Pratrodha</span>
                  </div>
                  <p className="vcard__body">A directional barrier. A remedy plan is assigned; on completion your score is checked.</p>
                  <div className="vcard__reentry"><b>Score ≥ 60</b> unlocks a Gate 0 re-test. Below 60, remedies continue with the deficit shown.</div>
                </div>
                <div className="vcard vcard--pray">
                  <div className="vcard__top">
                    <span className="verdict-chip verdict-chip--pray"><span className="verdict-chip__pip"></span>pray</span>
                    <span className="vcard__skt">Bhakti</span>
                  </div>
                  <p className="vcard__body">Full Surrender Mode. A 3-module plan: Mantra remedies, LK Debt Audit, and the 21-day PRAY Protocol.</p>
                  <div className="vcard__reentry"><b>Score ≥ 75</b> to re-test -- and the re-test must return YES or WAIT, not NO/PRAY again.</div>
                </div>
              </div>
            </section>

            {/* 05 · SCORE BANDS */}
            <section className="sec" id="bands">
              <div className="sec__head">
                <span className="sec__n">05</span>
                <h2 className="sec__title">Score Bands</h2>
                <p className="sec__lede">The Conquest Probability gauge resolves to one of four tactical postures.</p>
              </div>
              <div className="bands">
                <div className="band band--sov">
                  <div className="band__score"><span className="band__range">85-99</span><span className="band__pct">percent</span></div>
                  <div className="band__body"><p className="band__status">Sovereign Dominance</p><p className="band__directive"><b>Expansion / All-In.</b> Empire in high alignment -- execute the expansion mission immediately.</p></div>
                </div>
                <div className="band band--fri">
                  <div className="band__score"><span className="band__range">60-84</span><span className="band__pct">percent</span></div>
                  <div className="band__body"><p className="band__status">Operational Friction</p><p className="band__directive"><b>Patch &amp; Pivot.</b> Moderate friction -- settle Mercury debts before the next sales bid.</p></div>
                </div>
                <div className="band band--sie">
                  <div className="band__score"><span className="band__range">40-59</span><span className="band__pct">percent</span></div>
                  <div className="band__body"><p className="band__status">Strategic Siege</p><p className="band__directive"><b>Hold Ground / Remedy.</b> Fortify the interior; resolve karmic deficits before any offensive.</p></div>
                </div>
                <div className="band band--lock">
                  <div className="band__score"><span className="band__range">0-39</span><span className="band__pct">percent</span></div>
                  <div className="band__body"><p className="band__status">Karmic Lockdown</p><p className="band__directive"><b>Withdraw / Full Reset.</b> High risk -- pull back from offensive marketing and focus the internal fortress.</p></div>
                </div>
              </div>
              <div className="note">
                <div className="note__lbl">How the score is built</div>
                <p>Base <code>50</code>, then: Shadbala <code>+10 / −5</code> · Digbala <code>+15 / −10</code> · active Pitru Rin <code>−20</code> (a live surrogate buys back <code>+12</code>) · transit peak 25°-28° <code>+5</code> · ritual streak ≥ 7 <code>+10</code>, or a broken streak <code>−15</code>. Clamped to <code>0-99</code>.</p>
              </div>
            </section>

            {/* 06 · HURDLE ALERTS */}
            <section className="sec" id="hurdles">
              <div className="sec__head">
                <span className="sec__n">06</span>
                <h2 className="sec__title">Hurdle Alerts</h2>
                <p className="sec__lede">Red overlays that fire when the sky turns against an open move.</p>
              </div>
              <div className="prose">
                <p>Hurdle records (the Hurdle Library) carry a <span className="mono-inline">ui_warning</span> string and raise a red alert on the War Room when a retrograde, eclipse or combustion is detected against your chart. They tell you when to switch from offence to stealth.</p>
              </div>
              <table className="atable zebra" style={{ marginTop: 8 }}>
                <caption>Trigger classes</caption>
                <thead><tr><th>Class</th><th>What it flags</th><th>Posture</th></tr></thead>
                <tbody>
                  <tr><td>Retrograde</td><td>e.g. Mercury retrograde in H2 shadow</td><td>pause launches</td></tr>
                  <tr><td>Eclipse</td><td>authority eclipse on a command planet</td><td>move to stealth</td></tr>
                  <tr><td>Combustion</td><td>planet too close to the Sun</td><td>defer the bid</td></tr>
                  <tr><td>Degree 29</td><td>any transit planet at ≥ 29°</td><td>volatility -- hold</td></tr>
                </tbody>
              </table>
              <div className="note">
                <div className="note__lbl">Reading an alert</div>
                <p>Example payload: <code>"High Alert: Authority Eclipse detected. Move to stealth mode."</code> When a hurdle is live, treat any Sovereign-band directive as provisional until it clears.</p>
              </div>
            </section>

            {/* 07 · SURROGATE BRIDGE */}
            <section className="sec" id="surrogate">
              <div className="sec__head">
                <span className="sec__n">07</span>
                <h2 className="sec__title">Surrogate Bridge</h2>
                <p className="sec__lede">When the relative a remedy needs is unavailable, the bridge names the sanctioned stand-in.</p>
              </div>
              <div className="duo">
                <div className="panel">
                  <div className="panel__lbl">When it opens</div>
                  <h4>The family-census gate</h4>
                  <p>If your census marks the required relative as anything but living, the remedy can't run as written. The bridge opens automatically and asks for three things: the planet, the unavailable relative, and your industry.</p>
                </div>
                <div className="panel">
                  <div className="panel__lbl">What it returns</div>
                  <h4>A V2 surrogate record</h4>
                  <p>One matched record with a <span className="mono-inline">pivot_action</span> you can run instead. Activating it sets your bridge live and adds <b style={{ color: 'var(--emerald)' }}>+12</b> to the Conquest Probability -- the karmic remedy override.</p>
                </div>
              </div>
              <table className="atable zebra" style={{ marginTop: 18 }}>
                <caption>Inputs</caption>
                <thead><tr><th>Selector</th><th>Options</th></tr></thead>
                <tbody>
                  <tr><td>Planet</td><td>any of the nine command planets</td></tr>
                  <tr><td>Relative unavailable</td><td>Father · Mother · Sister · Brother · Grandfather · Uncle · Spouse · Son · In-laws</td></tr>
                  <tr><td>Industry</td><td>Tech · Operations · Legal/Consulting · Leadership · Creative · Sales-Defense · E-commerce</td></tr>
                </tbody>
              </table>
            </section>

            {/* 08 · MISSIONS */}
            <section className="sec" id="missions">
              <div className="sec__head">
                <span className="sec__n">08</span>
                <h2 className="sec__title">Missions</h2>
                <p className="sec__lede">The unit of action -- what a mission is made of, and the families they come from.</p>
              </div>
              <table className="atable">
                <caption>Mission card anatomy</caption>
                <thead><tr><th>Field</th><th>Meaning</th></tr></thead>
                <tbody>
                  <tr><td>Mission name</td><td>the operation, e.g. "Operation Solar South (Sun in H10)"</td></tr>
                  <tr><td>Objective</td><td>what victory looks like -- e.g. authority expansion</td></tr>
                  <tr><td>Trigger condition</td><td>the transit that fires it -- e.g. <span className="mono">Transit_Sun_H10</span></td></tr>
                  <tr><td>Pivot action</td><td>the concrete counter-move to run</td></tr>
                  <tr><td>KPI target</td><td>the metric that closes it</td></tr>
                  <tr><td>Remedy ID</td><td>cross-link into the LK remedies engine</td></tr>
                </tbody>
              </table>
              <div className="duo" style={{ marginTop: 22 }}>
                <div className="panel">
                  <div className="panel__lbl">Mission families</div>
                  <h4>Where missions come from</h4>
                  <p>CEO Forecast · Battle Cadence · Strategic Pivot · The Garrison · Technical Siege · The War Chest · Digital Siege · Sales Warfare · Peak Reach / Oracle State.</p>
                </div>
                <div className="panel">
                  <div className="panel__lbl">Variants &amp; filters</div>
                  <h4>Reading the board</h4>
                  <p>Missions are transit-triggered, so the board changes daily. Filter by planet, by house, or by date range to focus. Every card can push its remedy into the 43-Day Tracker.</p>
                </div>
              </div>
            </section>

            {/* 09 · GLOSSARY */}
            <section className="sec" id="glossary">
              <div className="sec__head">
                <span className="sec__n">09</span>
                <h2 className="sec__title">Glossary</h2>
                <p className="sec__lede">Eighteen terms the war room uses without explaining.</p>
              </div>
              <dl className="glossary">
                <div className="gterm"><dt>Gate 0</dt><dd>The Krishna Prashnavali oracle checkpoint every question passes through first.</dd></div>
                <div className="gterm"><dt>Conquest Probability</dt><dd>Your 0-99% success score, computed live by the ID 1022 algorithm.</dd></div>
                <div className="gterm"><dt>Shadbala</dt><dd>Six-fold strength of your command planet; drives the score ±10 / −5.</dd></div>
                <div className="gterm"><dt>Digbala</dt><dd>Directional strength -- your office location measured against the planet's power direction.</dd></div>
                <div className="gterm"><dt>Vimshottari Dasha</dt><dd>The planetary period you are currently living through; sets timing context.</dd></div>
                <div className="gterm"><dt>Pitru Rin</dt><dd>Ancestral / karmic debt, surfaced at LK Gate 1; the heaviest single drag on the score.</dd></div>
                <div className="gterm"><dt>Surrogate Bridge</dt><dd>A sanctioned biological-relative substitute when a remedy's relative is unavailable; worth +12.</dd></div>
                <div className="gterm"><dt>Golden Hour</dt><dd>The ritual window in the 30 minutes before sunset, when remedies count most.</dd></div>
                <div className="gterm"><dt>War Room State</dt><dd>The dashboard's mode -- OFFENSIVE, GOLDEN HOUR, or DEFENSIVE -- set by the sunset clock.</dd></div>
                <div className="gterm"><dt>Mission</dt><dd>A transit-triggered tactical directive, drawn from one of the nine mission families.</dd></div>
                <div className="gterm"><dt>Trigger Condition</dt><dd>The exact planetary position that fires a given mission.</dd></div>
                <div className="gterm"><dt>Pivot Action</dt><dd>The concrete counter-move a mission tells you to run.</dd></div>
                <div className="gterm"><dt>KPI Target</dt><dd>The metric that marks a mission complete.</dd></div>
                <div className="gterm"><dt>Hurdle Alert</dt><dd>A red overlay for a retrograde, eclipse or combustion working against an open move.</dd></div>
                <div className="gterm"><dt>Ritual Streak</dt><dd>Your consistency count from the LK Tracker; a streak ≥ 7 adds +10, a broken one −15.</dd></div>
                <div className="gterm"><dt>Pre-Flight Mode</dt><dd>The WAIT holding state -- complete the remedy plan and Layer 1 auto-unlocks.</dd></div>
                <div className="gterm"><dt>Full Surrender</dt><dd>The PRAY protocol -- a 3-module plan requiring a score ≥ 75 to re-test Gate 0.</dd></div>
                <div className="gterm"><dt>Executive Brief</dt><dd>The premium four-part PDF report -- the module's terminal output (Layer 5).</dd></div>
              </dl>
            </section>

            <footer className="colophon">
              <span>STR-UM-01 · Field Manual · The Strategist</span>
              <span>/strategist/manual · EverydayHoroscope</span>
            </footer>

          </div>
        </main>

      </div>
    </div>
  );
}
