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
    </div>
  );
}
