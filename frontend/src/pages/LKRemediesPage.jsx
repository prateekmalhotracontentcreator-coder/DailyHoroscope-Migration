import React from 'react';
import { Link } from 'react-router-dom';
import { SEO } from '../components/SEO';

export default function LKRemediesPage() {
  return (
    <div className="min-h-screen bg-background text-foreground px-4 py-8 max-w-3xl mx-auto">
      <SEO
        title="Lal Kitab Remedies — Karmic Diagnostics & 43-Day Cycles"
        description="Ancient Lal Kitab wisdom for modern life. Karmic debt scans, dormant house awakening, 35-year planetary cycles, and personalised 43-day remedy protocols."
        url="https://www.everydayhoroscope.in/lk-remedies"
      />
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6 mb-6">
        <h1 className="text-2xl font-bold text-gold mb-2">Lal Kitab Remedies</h1>
        <p className="text-muted-foreground text-sm mb-4">
          Ancient Lal Kitab wisdom — personalised karmic diagnostics, 43-day remedy cycles, and ancestral debt clearing.
        </p>
        <div className="flex flex-col gap-3">
          <Link
            to="/lk-remedies/onboard"
            className="inline-block bg-gold text-background font-semibold rounded-lg px-5 py-2.5 text-center hover:opacity-90 transition"
          >
            Begin Your Diagnostic
          </Link>
          <Link
            to="/lk-remedies/remedies"
            className="inline-block border border-gold/40 text-gold rounded-lg px-5 py-2.5 text-center hover:bg-gold/10 transition text-sm"
          >
            Browse Remedies
          </Link>
        </div>
      </div>

      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5">
        <h2 className="text-base font-semibold text-gold mb-3">What You'll Discover</h2>
        <ul className="space-y-2 text-sm text-muted-foreground">
          <li className="flex items-start gap-2"><span className="text-amber-500 mt-0.5">⚠️</span><span>Gate 1 — Karmic Debt scan: ancestral obligations blocking your path</span></li>
          <li className="flex items-start gap-2"><span className="text-blue-400 mt-0.5">💤</span><span>Gate 2 — Dormant house awakening: sleeping potential in your chart</span></li>
          <li className="flex items-start gap-2"><span className="text-gold mt-0.5">🔄</span><span>Gate 3 — 35-Year cycle: your current planetary year-lord phase</span></li>
          <li className="flex items-start gap-2"><span className="text-muted-foreground mt-0.5">🔍</span><span>Gate 4 — Mercury scan: Empty Vessel or Rahu collision detection</span></li>
          <li className="flex items-start gap-2"><span className="text-emerald-500 mt-0.5">✅</span><span>Gate 5 — Geographical alignment: directional power for your city</span></li>
        </ul>
      </div>

      {/* ── On-page SEO content ──────────────────────────────────────────── */}
      <div className="mt-12 space-y-8 border-t border-border pt-10 text-sm text-muted-foreground">
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">What is Lal Kitab?</h2>
          <p className="leading-7">Lal Kitab (लाल किताब — "The Red Book") is a unique branch of Vedic astrology originating from 19th-century Punjab, distinct from classical Parashari Jyotish. Written in Urdu-Persian verse, it uses a simplified house-based chart system and focuses on karmic debt (rin) accumulated across lifetimes. Its remedies are remarkably practical — inexpensive, daily-life actions like offering water to the Sun, keeping copper coins, feeding birds — making Vedic wisdom accessible outside the domain of costly rituals.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">The 5-Gate Karmic Diagnostic</h2>
          <p className="leading-7">EverydayHoroscope's Lal Kitab engine runs your birth chart through 5 diagnostic gates. Gate 1 scans for active karmic debts — ancestral obligations encoded in specific planetary placements. Gate 2 identifies dormant houses — potential that is sleeping due to planetary affliction. Gate 3 locates your position within the 35-year planetary year-lord cycle. Gate 4 detects Mercury anomalies (Empty Vessel and Rahu collision) that suppress intelligence or communication. Gate 5 assesses your city's directional alignment with your planetary strengths.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">43-Day Remedy Cycles</h2>
          <p className="leading-7">Lal Kitab remedies are prescribed in structured cycles — typically 40 or 43 consecutive days — because sustained daily action is required to shift karmic patterns. A remedy broken mid-cycle must be restarted from day one. The 43-day protocol mirrors the Vedic understanding of neurological and karmic imprinting: 40 days to establish a new pattern, 3 extra days as a buffer. EverydayHoroscope tracks your active remedy cycles and streak days so you never lose your place.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Lal Kitab vs Classical Jyotish</h2>
          <p className="leading-7">Classical Parashari Jyotish reads planets by sign, aspect, and nakshatra with complex strength calculations. Lal Kitab reads planets purely by house position and uses a unique concept of "pakka ghar" (permanent house) — each planet's natural house — to assess whether it is in a friendly or hostile placement. The remedies differ too: classical Jyotish prescribes gemstones and elaborate puja; Lal Kitab focuses on simple daily actions, specific foods, and material offerings tied to the afflicting planet.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">How to Begin Your Remedy Journey</h2>
          <p className="leading-7">Begin with the Diagnostic — enter your birth details to generate your full 5-gate Lal Kitab report. The system identifies your active karmic debts and prescribes a personalised set of remedies in priority order. Start with the highest-priority remedy (Gate 1 debts) and commit to the full 43-day cycle before adding others. Use the Tracker to maintain your streak. Browse the full remedy library to understand the principles before beginning, so each daily action is done with awareness, not mechanical habit.</p>
        </div>
      </div>
    </div>
  );
}
