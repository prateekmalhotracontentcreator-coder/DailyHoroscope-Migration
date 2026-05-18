import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { SEO } from "../../components/SEO";

const REPORTS = [
  {
    slug: "karmic-debt",
    name: "Karmic Debt & Past Life",
    color: "#7f4be0",
    icon: "◎",
    hook: "Decode the spiritual loop you keep meeting in different disguises.",
    what: "Karmic themes, past-life echoes, soul lessons, and release practices drawn from your South Node, 12th house, and Saturn placement.",
    landingRoute: "/karmic-debt-report",
  },
  {
    slug: "career-blueprint",
    name: "Career & Success Blueprint",
    color: "#c9961f",
    icon: "▲",
    hook: "See the work pattern, public calling, and success rhythm written into your chart.",
    what: "Strengths, wealth signals, career timing, and practical next moves from your 10th house, 2nd house, and current Mahadasha.",
    landingRoute: "/career-blueprint-report",
  },
  {
    slug: "shadow-self",
    name: "Shadow Self & Hidden Qualities",
    color: "#3f7ae0",
    icon: "◐",
    hook: "Name the hidden pressure shaping your reactions before it chooses for you.",
    what: "Hidden strengths, blind spots, emotional drivers, and integration guidance from your Rahu, Ketu, and 8th house.",
    landingRoute: "/shadow-self-report",
  },
  {
    slug: "retrograde-survival",
    name: "Retrograde Survival Guide",
    color: "#e27c33",
    icon: "↺",
    hook: "Track the retrograde weather around you and move through it with less chaos.",
    what: "Mercury, Venus, and Mars retrograde timing mapped to your natal chart with grounded, practical remedies.",
    landingRoute: "/retrograde-survival-report",
  },
  {
    slug: "life-cycles",
    name: "Pattern of Life Cycles",
    color: "#3fa56a",
    icon: "◌",
    hook: "Understand the chapter you are in now and the one already rising behind it.",
    what: "Current chapter, sub-cycle, decade arc, and upcoming transitions from your Vimshottari Dasha sequence.",
    landingRoute: "/life-cycles-report",
  },
  {
    slug: "wealth-blueprint",
    name: "Wealth & Abundance Blueprint",
    color: "#c8930a",
    icon: "◈",
    hook: "See the wealth signals, abundance timing, and Dhana yogas written into your chart.",
    what: "Dhana yogas, 2nd house strength, Jupiter and Venus influence, and key abundance windows from your Vimshottari Dasha.",
    landingRoute: "/wealth-blueprint-report",
  },
  {
    slug: "romance-creative",
    name: "Romance & Creative Intelligence",
    color: "#d4538a",
    icon: "✦",
    hook: "Unlock the romantic and creative intelligence wired into your 5th house.",
    what: "Romantic timing, creative gifts, 5th lord strength, and the windows where both peak together.",
    landingRoute: "/romance-creative-report",
  },
  {
    slug: "vitality-health",
    name: "Vitality & Health Report",
    color: "#2a9d6f",
    icon: "⬡",
    hook: "Read the health rhythm your chart encodes and the periods that need the most care.",
    what: "6th house analysis, Mars and Saturn influence, vulnerable patterns, and daily rhythm guidance.",
    landingRoute: "/vitality-health-report",
  },
  {
    slug: "partnership-window",
    name: "Partnership & Marriage Window",
    color: "#6b4fbd",
    icon: "◇",
    hook: "Find the Vedic marriage timing and see the partnership pattern your 7th house reveals.",
    what: "Darakaraka, 7th lord, Upapada Lagna, and marriage and commitment dasha windows.",
    landingRoute: "/partnership-window-report",
  },
  {
    slug: "dharma-purpose",
    name: "Dharma & Soul Purpose Report",
    color: "#1e5fa8",
    icon: "☉",
    hook: "Trace the dharmic thread running through your chart to the purpose this life is asking you to fulfil.",
    what: "9th lord, Jupiter strength, Atmakaraka path, and the soul-level direction already written in your chart.",
    landingRoute: "/dharma-purpose-report",
  },
  {
    slug: "gains-network",
    name: "Gains & Network Activator",
    color: "#d46f22",
    icon: "◆",
    hook: "See the aspiration fulfilment windows and the social leverage points your 11th house encodes.",
    what: "11th lord strength, Saturn role in aspiration, key gains dasha windows, and network activation timing.",
    landingRoute: "/gains-network-report",
  },
];

const STEPS = [
  { n: "01", title: "Enter your birth details", body: "Date, time, and place of birth -- the same inputs used for your full Vedic chart." },
  { n: "02", title: "Your chart is calculated", body: "Pyswisseph (Swiss Ephemeris) computes planetary positions to arc-minute accuracy using the Lahiri ayanamsha." },
  { n: "03", title: "Receive your personalised report", body: "Each section of the report is generated specifically for your chart -- not a template, not a horoscope sign." },
];

const FAQS = [
  { q: "What are Individual Vedic Reports?", a: "Eleven in-depth Vedic astrology reports -- each focused on a single life domain -- generated from your personal birth chart using Swiss Ephemeris computation and Vimshottari Dasha timing. Unlike sun-sign horoscopes, these are calculated specifically for your chart." },
  { q: "How is this different from my birth chart?", a: "Your birth chart shows the full picture. Each Individual Report is a focused lens on one domain -- karmic patterns, career, wealth, shadow work, retrograde timing, life cycles, romance, vitality, partnership, dharma, or gains -- giving you depth rather than breadth." },
  { q: "What information do I need to generate a report?", a: "Date of birth, approximate time of birth (within 30 minutes for best accuracy), and city of birth. Time of birth affects house cusps and the Dasha start date significantly." },
  { q: "Can I generate all eleven reports?", a: "Yes. Each report is generated independently. You can run one per session or all eleven -- each request generates a fresh report. Past reports are saved to your account history." },
];

export default function PremiumReportsLanding() {
  const navigate = useNavigate();
  const { user } = useAuth();

  function handleCTA() {
    if (user) {
      navigate("/reports");
    } else {
      navigate("/login", { state: { from: { pathname: "/reports" } } });
    }
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(ellipse_at_top_left,rgba(127,75,224,0.18),transparent_40%),radial-gradient(ellipse_at_top_right,rgba(201,150,31,0.14),transparent_36%),linear-gradient(180deg,#f9f3ea_0%,#efe4d2_60%,#e8ddc8_100%)] text-stone-900">
      <SEO
        title="Individual Vedic Reports -- Karmic, Career, Wealth, Dharma & More"
        description="Eleven in-depth Vedic astrology reports generated from your personal birth chart -- Karmic Debt, Career Blueprint, Shadow Self, Retrograde Survival, Life Cycles, Wealth Blueprint, Romance, Vitality, Partnership, Dharma, and Gains. Each calculated to arc-minute precision with Swiss Ephemeris."
        url="https://www.everydayhoroscope.in/individual-reports"
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
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.3em] text-amber-700/70">Premium Vedic Reports</p>
        <h1 className="mb-4 font-cinzel text-4xl font-bold leading-tight text-stone-900 sm:text-5xl">
          Your Chart,{" "}
          <span className="text-[#c9961f]">Eleven Lenses</span>
        </h1>
        <p className="mx-auto mb-2 max-w-2xl font-playfair text-lg italic text-stone-600">
          Not a sun-sign reading. Not a template. A report generated specifically from your birth chart -- calculated to arc-minute precision.
        </p>
        <p className="mx-auto mb-10 max-w-xl text-sm text-stone-500">
          Swiss Ephemeris · Lahiri Ayanamsha · Vimshottari Dasha timing · Eleven focused domains
        </p>
        <button
          onClick={handleCTA}
          className="inline-flex items-center gap-2 rounded-full bg-[#c9961f] px-8 py-4 text-base font-semibold text-white shadow-lg transition hover:bg-[#b8861a]"
        >
          {user ? "Generate My Reports" : "Get Started -- Free Account"} →
        </button>
        {!user && (
          <p className="mt-3 text-xs text-stone-500">
            Already registered?{" "}
            <button
              onClick={() => navigate("/login", { state: { from: { pathname: "/reports" } } })}
              className="text-[#c9961f] underline"
            >
              Sign in
            </button>
          </p>
        )}
      </section>

      {/* ── 5 Report Tiles ── */}
      <section className="mx-auto max-w-6xl px-4 pb-16">
        <h2 className="mb-8 text-center font-playfair text-2xl font-semibold text-stone-800">
          Eleven Reports. Eleven Domains of Your Life.
        </h2>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {REPORTS.map((r) => (
            <div
              key={r.slug}
              className="rounded-2xl border border-stone-200/80 bg-white/80 p-6 shadow-sm backdrop-blur-sm transition hover:shadow-md"
              style={{ borderLeft: `4px solid ${r.color}` }}
            >
              <div className="mb-3 flex items-center gap-3">
                <span className="text-3xl leading-none" style={{ color: r.color }}>{r.icon}</span>
                <h3 className="font-playfair text-lg font-semibold text-stone-900">{r.name}</h3>
              </div>
              <p className="mb-3 text-sm font-medium leading-6 text-stone-700 italic">{r.hook}</p>
              <p className="text-xs leading-5 text-stone-500">{r.what}</p>
              <div className="mt-4">
                <Link
                  to={r.landingRoute}
                  className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.18em] text-stone-700 transition hover:opacity-75"
                >
                  Explore report
                  <span aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          ))}
          {/* CTA tile */}
          <div
            className="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-[#c9961f]/40 bg-[#c9961f]/[0.04] p-6 text-center"
          >
            <p className="mb-2 font-playfair text-base font-semibold text-stone-700">All eleven included with Premium</p>
            <p className="mb-4 text-xs text-stone-500">Generate any report, any time. History saved automatically.</p>
            <button
              onClick={handleCTA}
              className="rounded-full border border-[#c9961f] px-5 py-2 text-sm font-semibold text-[#c9961f] transition hover:bg-[#c9961f]/10"
            >
              Access Reports →
            </button>
          </div>
        </div>
      </section>

      {/* ── How It Works ── */}
      <section className="bg-white/60 py-16 backdrop-blur-sm">
        <div className="mx-auto max-w-4xl px-4">
          <h2 className="mb-10 text-center font-cinzel text-2xl font-semibold text-stone-800">How It Works</h2>
          <div className="grid gap-8 sm:grid-cols-3">
            {STEPS.map((s) => (
              <div key={s.n} className="text-center">
                <p className="mb-3 font-cinzel text-3xl font-bold text-[#c9961f]/60">{s.n}</p>
                <h3 className="mb-2 font-playfair text-base font-semibold text-stone-800">{s.title}</h3>
                <p className="text-sm leading-6 text-stone-500">{s.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Sample teaser ── */}
      <section className="mx-auto max-w-4xl px-4 py-16">
        <h2 className="mb-8 text-center font-playfair text-2xl font-semibold text-stone-800">What a Report Looks Like</h2>
        <div className="relative overflow-hidden rounded-2xl border border-stone-200/80 bg-white/80 p-6 shadow-sm">
          <div className="space-y-4">
            <div className="flex items-center gap-3 border-b border-stone-100 pb-4">
              <span className="text-2xl" style={{ color: "#7f4be0" }}>◎</span>
              <div>
                <p className="text-xs font-semibold uppercase tracking-widest text-stone-400">Sample -- Karmic Debt & Past Life</p>
                <p className="font-playfair text-lg font-semibold text-stone-800">South Node in Scorpio, 8th House</p>
              </div>
            </div>
            <div className="space-y-3 text-sm leading-7 text-stone-600 blur-[2px] select-none">
              <p>Your South Node in Scorpio in the 8th house describes a past-life pattern centred on intense merger, hidden power, and transformation through crisis. The soul's past was shaped by...</p>
              <p>Saturn's aspect to the South Node Lord Venus creates a karmic thread around worth, attachment, and the surrender of control. The release practice for this placement involves...</p>
              <p><strong>Soul lesson this lifetime:</strong> Building stable, boundaried self-reliance after lifetimes of surrendering identity to deep bonds...</p>
            </div>
          </div>
          <div className="absolute inset-0 flex items-end justify-center bg-gradient-to-t from-white/95 via-white/40 to-transparent pb-8">
            <button
              onClick={handleCTA}
              className="rounded-full bg-[#7f4be0] px-6 py-3 text-sm font-semibold text-white shadow-lg transition hover:bg-[#6d3fcb]"
            >
              Unlock Your Full Report →
            </button>
          </div>
        </div>
      </section>

      {/* ── FAQ ── */}
      <section className="mx-auto max-w-3xl px-4 pb-16">
        <h2 className="mb-8 text-center font-playfair text-2xl font-semibold text-stone-800">Frequently Asked Questions</h2>
        <div className="space-y-5">
          {FAQS.map((f) => (
            <div key={f.q} className="rounded-xl border border-stone-200/80 bg-white/70 p-5">
              <p className="mb-2 font-semibold text-stone-800">{f.q}</p>
              <p className="text-sm leading-6 text-stone-500">{f.a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Bottom CTA ── */}
      <section className="bg-stone-900 py-16 text-center text-white">
        <p className="mb-2 font-cinzel text-xs uppercase tracking-[0.3em] text-amber-400/80">Ready to begin</p>
        <h2 className="mb-4 font-cinzel text-3xl font-bold">See What Your Chart Really Says</h2>
        <p className="mx-auto mb-8 max-w-xl text-sm leading-7 text-stone-300">
          Eleven reports. One birth chart. Infinite clarity. Available to all Premium members with no extra cost per report.
        </p>
        <button
          onClick={handleCTA}
          className="inline-flex items-center gap-2 rounded-full bg-[#c9961f] px-8 py-4 text-base font-semibold text-white shadow-lg transition hover:bg-[#b8861a]"
        >
          {user ? "Open Report Library →" : "Create Free Account →"}
        </button>
      </section>
    </div>
  );
}
