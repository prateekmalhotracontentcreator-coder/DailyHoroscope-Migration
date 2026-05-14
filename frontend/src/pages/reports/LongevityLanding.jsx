import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { SEO } from "../../components/SEO";

const PILLARS = [
  { icon: "◎", title: "Ayushkaraka Analysis", body: "Saturn as the Karaka of longevity -- examined through sign, house, dignity, and aspect to identify your constitutional baseline." },
  { icon: "⌂", title: "8th House Deep Dive", body: "The house of lifespan, transformation, and hidden vitality. Its lord, occupants, and afflictions shape your longevity signature." },
  { icon: "△", title: "Lagna & Lagna Lord", body: "The strength of your ascendant and its lord determines the body's resilience. A strong Lagna lord adds decades; a weak one signals areas to protect." },
  { icon: "◐", title: "Maraka Planets", body: "2nd and 7th house lords are traditionally designated Maraka -- identified and timed against your current Dasha to flag critical windows." },
  { icon: "↺", title: "Dasha Timing", body: "Vimshottari Dasha periods of Saturn, Rahu, Ketu, and 8th lord are mapped to show when protective action matters most." },
  { icon: "◌", title: "Remedial Guidance", body: "Practical, non-alarmist recommendations drawn from Jyotish tradition -- mantra, lifestyle, and spiritual practice aligned to your chart." },
];

const STEPS = [
  { n: "01", title: "Enter birth details", body: "Date, time, and city. The Krishnamurti Paddhati engine computes your natal chart to sub-degree precision." },
  { n: "02", title: "Chart is computed", body: "KP engine (pyswisseph, SIDM_LAHIRI) calculates house cusps, planetary dignities, Dasha balance, and longevity indicators." },
  { n: "03", title: "Report is generated", body: "A multi-section longevity report is produced by Claude claude-sonnet-4-6 against your specific chart -- not a template, not a generic reading." },
];

const FAQS = [
  { q: "What is a Vedic Longevity Report?", a: "A Jyotish-based analysis of your lifespan indicators -- Saturn, the 8th house, Lagna strength, and Maraka planets -- combined with Vimshottari Dasha timing to identify your constitutional vitality and periods that warrant protective action." },
  { q: "Is this medically predictive?", a: "No. This report is a traditional Jyotish reading, not a medical opinion. It identifies astrological indicators associated with health and vitality and suggests supportive practices. Always consult a qualified medical professional for health decisions." },
  { q: "Which astrological system does this use?", a: "Krishnamurti Paddhati (KP) system with Lahiri ayanamsha, computed using Swiss Ephemeris (pyswisseph). KP is favoured for its precision in house cusp calculation and its detailed approach to sub-lord analysis." },
  { q: "What is Ayushkaraka?", a: "In Vedic astrology, Saturn is designated the Ayushkaraka -- the planet that signifies longevity and lifespan. Its placement, dignity, aspects, and Dasha periods are central to any longevity analysis in Jyotish." },
  { q: "How long does the report take to generate?", a: "Approximately 30-60 seconds. The KP engine computes your chart first, then Claude generates a personalised multi-section report against your specific planetary positions and Dasha sequence." },
];

export default function LongevityLanding() {
  const navigate = useNavigate();
  const { user } = useAuth();

  function handleCTA() {
    if (user) {
      navigate("/longevity-report");
    } else {
      navigate("/login", { state: { from: { pathname: "/longevity-report" } } });
    }
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(ellipse_at_top_left,rgba(63,165,106,0.14),transparent_38%),radial-gradient(ellipse_at_bottom_right,rgba(197,160,89,0.10),transparent_40%),linear-gradient(180deg,#f5f9f6_0%,#eaf2ec_55%,#e2eee5_100%)] text-stone-900">
      <SEO
        title="Vedic Longevity Report -- KP Astrology Lifespan Analysis | EverydayHoroscope"
        description="A Krishnamurti Paddhati longevity report built from your natal chart. Saturn analysis, 8th house deep dive, Maraka identification, Dasha timing, and practical remedial guidance -- generated to arc-minute precision."
        url="https://www.everydayhoroscope.in/the-longevity-report"
        schema={{
          "@context": "https://schema.org",
          "@type": "FAQPage",
          "mainEntity": FAQS.map(f => ({
            "@type": "Question",
            "name": f.q,
            "acceptedAnswer": { "@type": "Answer", "text": f.a },
          })),
        }}
      />

      {/* ── Hero ── */}
      <section className="mx-auto max-w-4xl px-4 py-20 text-center">
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.3em] text-emerald-700/70">Krishnamurti Paddhati · KP Astrology</p>
        <h1 className="mb-4 font-cinzel text-4xl font-bold leading-tight text-stone-900 sm:text-5xl">
          Your Longevity,{" "}
          <span className="text-emerald-700">Written in the Chart</span>
        </h1>
        <p className="mx-auto mb-3 max-w-2xl font-playfair text-lg italic text-stone-600">
          Ayushkaraka Saturn. The 8th house. Maraka lords. Dasha timing. A complete Jyotish longevity portrait from your birth chart.
        </p>
        <p className="mx-auto mb-10 max-w-xl text-sm text-stone-500">
          KP System · Swiss Ephemeris · Lahiri Ayanamsha · Claude claude-sonnet-4-6 narrative generation
        </p>
        <button
          onClick={handleCTA}
          className="inline-flex items-center gap-2 rounded-full bg-emerald-700 px-8 py-4 text-base font-semibold text-white shadow-lg transition hover:bg-emerald-600"
        >
          {user ? "Generate My Report →" : "Get Started -- Free Account →"}
        </button>
        {!user && (
          <p className="mt-3 text-xs text-stone-500">
            Already registered?{" "}
            <button
              onClick={() => navigate("/login", { state: { from: { pathname: "/longevity-report" } } })}
              className="text-emerald-700 underline"
            >
              Sign in
            </button>
          </p>
        )}
      </section>

      {/* ── 6 pillars ── */}
      <section className="mx-auto max-w-6xl px-4 pb-16">
        <h2 className="mb-8 text-center font-playfair text-2xl font-semibold text-stone-800">What the Report Analyses</h2>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {PILLARS.map(p => (
            <div key={p.title} className="rounded-2xl border border-emerald-200/60 bg-white/80 p-6 shadow-sm backdrop-blur-sm">
              <p className="mb-3 text-2xl font-bold text-emerald-700/60">{p.icon}</p>
              <h3 className="mb-2 font-playfair text-base font-semibold text-stone-800">{p.title}</h3>
              <p className="text-sm leading-6 text-stone-500">{p.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── How it works ── */}
      <section className="bg-white/60 py-16 backdrop-blur-sm">
        <div className="mx-auto max-w-4xl px-4">
          <h2 className="mb-10 text-center font-cinzel text-2xl font-semibold text-stone-800">How It Works</h2>
          <div className="grid gap-8 sm:grid-cols-3">
            {STEPS.map(s => (
              <div key={s.n} className="text-center">
                <p className="mb-3 font-cinzel text-3xl font-bold text-emerald-700/50">{s.n}</p>
                <h3 className="mb-2 font-playfair text-base font-semibold text-stone-800">{s.title}</h3>
                <p className="text-sm leading-6 text-stone-500">{s.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Sample teaser ── */}
      <section className="mx-auto max-w-4xl px-4 py-16">
        <h2 className="mb-8 text-center font-playfair text-2xl font-semibold text-stone-800">Sample Report Section</h2>
        <div className="relative overflow-hidden rounded-2xl border border-emerald-200/60 bg-white/80 p-6 shadow-sm">
          <div className="space-y-4">
            <div className="flex items-center gap-3 border-b border-stone-100 pb-4">
              <span className="text-2xl text-emerald-700">◎</span>
              <div>
                <p className="text-xs font-semibold uppercase tracking-widest text-stone-400">Sample -- Ayushkaraka Analysis</p>
                <p className="font-playfair text-lg font-semibold text-stone-800">Saturn in Capricorn, 6th House</p>
              </div>
            </div>
            <div className="space-y-3 text-sm leading-7 text-stone-600 blur-[2px] select-none">
              <p>Saturn in its own sign Capricorn in the 6th house is a strong Ayushkaraka placement. The 6th house association brings Saturn into direct contact with the house of health, service, and resistance to disease. In KP analysis, the sub-lord of the 6th cusp is Mercury, which is placed in the 5th house and signifies...</p>
              <p>The Dasha sequence shows Saturn Mahadasha beginning in 2031. This is the single most significant longevity window to prepare for. Protective practices initiated before this period will materially strengthen the constitutional baseline. The recommended focus areas include...</p>
            </div>
          </div>
          <div className="absolute inset-0 flex items-end justify-center bg-gradient-to-t from-white/95 via-white/40 to-transparent pb-8">
            <button
              onClick={handleCTA}
              className="rounded-full bg-emerald-700 px-6 py-3 text-sm font-semibold text-white shadow-lg transition hover:bg-emerald-600"
            >
              Unlock Your Full Report →
            </button>
          </div>
        </div>
      </section>

      {/* ── Disclaimer ── */}
      <section className="mx-auto max-w-3xl px-4 pb-6">
        <div className="rounded-xl border border-stone-200/80 bg-stone-50/80 p-4 text-center">
          <p className="text-xs leading-5 text-stone-400">
            This report is a traditional Jyotish reading for spiritual and reflective purposes only. It is not medical advice. Always consult a qualified medical professional for health decisions.
          </p>
        </div>
      </section>

      {/* ── FAQ ── */}
      <section className="mx-auto max-w-3xl px-4 pb-16">
        <h2 className="mb-8 text-center font-playfair text-2xl font-semibold text-stone-800">Frequently Asked Questions</h2>
        <div className="space-y-4">
          {FAQS.map(f => (
            <div key={f.q} className="rounded-xl border border-emerald-200/60 bg-white/70 p-5">
              <p className="mb-2 font-semibold text-stone-800">{f.q}</p>
              <p className="text-sm leading-6 text-stone-500">{f.a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Bottom CTA ── */}
      <section className="bg-stone-900 py-16 text-center text-white">
        <p className="mb-2 font-cinzel text-xs uppercase tracking-[0.3em] text-emerald-400/80">Ready to begin</p>
        <h2 className="mb-4 font-cinzel text-3xl font-bold">Know Your Longevity Signature</h2>
        <p className="mx-auto mb-8 max-w-xl text-sm leading-7 text-stone-300">
          A KP astrology longevity report built specifically from your birth chart. No templates. No generic readings.
        </p>
        <button
          onClick={handleCTA}
          className="inline-flex items-center gap-2 rounded-full bg-emerald-600 px-8 py-4 text-base font-semibold text-white shadow-lg transition hover:bg-emerald-500"
        >
          {user ? "Generate My Report →" : "Create Free Account →"}
        </button>
      </section>
    </div>
  );
}
