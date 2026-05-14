import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { SEO } from "../../components/SEO";

const FEATURES = [
  { icon: "🃏", title: "Daily Draw", body: "One card from the full 78-card Rider-Waite deck, contextualised against your Vedic dasha and current transits." },
  { icon: "✦", title: "Spread Readings", body: "Celtic Cross, Three-Card, Relationship, Career, and Healing spreads -- each with positional meaning and Vedic cross-reference." },
  { icon: "📖", title: "Manifestation Journal", body: "Set daily intentions linked to your draw. Track streaks, moon phases, and your most-recurring cards over time." },
  { icon: "⚡", title: "Gamification & XP", body: "Earn experience points and streak badges with every reading. Level up your Tarot practice." },
  { icon: "🌙", title: "Moon Phase Awareness", body: "Every draw is stamped with the current lunar phase -- new moon intentions, full moon releases, and everything in between." },
  { icon: "⏳", title: "Favorable Timing", body: "Premium timing layer maps planetary periods to ideal windows for action, rest, and reflection." },
];

const SPREADS = [
  { name: "Single Card", cards: 1, use: "Daily guidance, yes/no clarity, a single focused theme." },
  { name: "Three Card", cards: 3, use: "Past · Present · Future -- the simplest narrative arc in Tarot." },
  { name: "Celtic Cross", cards: 10, use: "The complete situational map -- ten positions, one full portrait of your reality." },
  { name: "Relationship Spread", cards: 11, use: "Two people, one mirror. What truly exists between you -- beyond hope and fear." },
  { name: "Career Spread", cards: 5, use: "Strengths, blocks, opportunity, action, outcome -- mapped to your professional path." },
  { name: "Shadow Self", cards: 4, use: "The deep dive -- shadow, gift, integration, and the step forward." },
];

const FAQS = [
  { q: "How does EverydayHoroscope cross-reference Tarot with Vedic astrology?", a: "Every Tarot card carry a planetary and elemental correspondence. When you draw, the system maps your card's energy against your current Vimshottari Mahadasha and active transits -- so the interpretation speaks to what is actually alive in your chart right now, not just the card's generic meaning." },
  { q: "Is the daily draw random?", a: "The draw uses a cryptographically random selection from the full 78-card deck, including upright and reversed orientations. Randomness is the mechanism -- your sincere intent at the moment of drawing is what makes it meaningful." },
  { q: "What is a Manifestation Journal entry?", a: "After each draw, you can set a daily intention linked to the card you received. The journal tracks your streak, most-drawn cards, and moon phase at the time of each entry -- building a personal record of your practice over time." },
  { q: "What is the moon phase badge on each reading?", a: "The lunar phase at the moment of your draw is shown on every reading. New moons favour intention-setting, waxing moons support growth and action, full moons are for release, and waning moons call for reflection and rest." },
];

export default function TarotLanding() {
  const navigate = useNavigate();
  const { user } = useAuth();

  function handleCTA() {
    if (user) {
      navigate("/tarot");
    } else {
      navigate("/login", { state: { from: { pathname: "/tarot" } } });
    }
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(ellipse_at_top,rgba(197,160,89,0.16),transparent_40%),linear-gradient(180deg,#0d0c0a_0%,#18150f_55%,#0d0c0a_100%)] text-amber-50">
      <SEO
        title="Tarot Card Reading -- Vedic Cross-Reference | EverydayHoroscope"
        description="Daily Tarot draws, Celtic Cross spreads, Manifestation Journal, and moon phase awareness -- each reading cross-referenced with your live Vedic Mahadasha and planetary transits."
        url="https://www.everydayhoroscope.in/the-tarot"
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
      <section className="mx-auto max-w-4xl px-4 py-24 text-center">
        <p className="mb-4 text-xs font-semibold uppercase tracking-[0.3em] text-amber-400/70">Western Tarot · Vedic Cross-Reference</p>
        <h1 className="mb-5 font-cinzel text-4xl font-bold leading-tight sm:text-5xl">
          Read the Cards.{" "}
          <span className="text-amber-400">Know the Moment.</span>
        </h1>
        <p className="mx-auto mb-3 max-w-2xl font-playfair text-lg italic text-amber-100/70">
          Every draw is contextualised against your live Vedic dasha and the current lunar phase -- not a generic reading, a reading for right now.
        </p>
        <p className="mx-auto mb-10 max-w-xl text-sm text-amber-100/40">
          78-card Rider-Waite · 6 spread types · Manifestation Journal · Moon phase stamps · XP & streaks
        </p>
        <button
          onClick={handleCTA}
          className="inline-flex items-center gap-2 rounded-full bg-amber-500 px-8 py-4 text-base font-semibold text-stone-900 shadow-lg transition hover:bg-amber-400"
        >
          {user ? "Open Tarot →" : "Start Reading -- Free →"}
        </button>
        {!user && (
          <p className="mt-3 text-xs text-amber-100/40">
            Have an account?{" "}
            <button onClick={() => navigate("/login", { state: { from: { pathname: "/tarot" } } })} className="text-amber-400 underline">
              Sign in
            </button>
          </p>
        )}
      </section>

      {/* ── Feature tiles ── */}
      <section className="mx-auto max-w-6xl px-4 pb-20">
        <h2 className="mb-10 text-center font-cinzel text-2xl font-semibold text-amber-200">What's Inside</h2>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map(f => (
            <div key={f.title} className="rounded-2xl border border-amber-400/10 bg-white/[0.04] p-6 backdrop-blur-sm">
              <p className="mb-3 text-3xl">{f.icon}</p>
              <h3 className="mb-2 font-playfair text-base font-semibold text-amber-100">{f.title}</h3>
              <p className="text-sm leading-6 text-amber-100/55">{f.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Spread menu ── */}
      <section className="border-y border-amber-400/10 bg-white/[0.03] py-16">
        <div className="mx-auto max-w-4xl px-4">
          <h2 className="mb-10 text-center font-cinzel text-2xl font-semibold text-amber-200">Available Spreads</h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {SPREADS.map(s => (
              <div key={s.name} className="rounded-xl border border-amber-400/10 bg-white/[0.04] p-5">
                <div className="mb-2 flex items-center gap-2">
                  <p className="font-playfair font-semibold text-amber-100">{s.name}</p>
                  <span className="rounded-full border border-amber-400/30 px-2 py-0.5 text-[11px] text-amber-400">{s.cards} {s.cards === 1 ? "card" : "cards"}</span>
                </div>
                <p className="text-xs leading-5 text-amber-100/50">{s.use}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Journal / moon teaser ── */}
      <section className="mx-auto max-w-4xl px-4 py-16">
        <div className="grid gap-6 sm:grid-cols-2">
          <div className="rounded-2xl border border-amber-400/10 bg-white/[0.04] p-8">
            <p className="mb-3 text-3xl">📖</p>
            <h3 className="mb-3 font-cinzel text-lg font-semibold text-amber-200">Manifestation Journal</h3>
            <p className="text-sm leading-7 text-amber-100/55">
              Every draw is an opportunity to set an intention. The Journal tracks what you asked for, which card answered, and the moon phase when you asked it -- building a living record of your practice over weeks and months.
            </p>
            <p className="mt-4 text-xs text-amber-400/60">Streak tracking · Most-drawn card · Linked readings</p>
          </div>
          <div className="rounded-2xl border border-amber-400/10 bg-white/[0.04] p-8">
            <p className="mb-3 text-3xl">🌙</p>
            <h3 className="mb-3 font-cinzel text-lg font-semibold text-amber-200">Moon Phase Awareness</h3>
            <p className="text-sm leading-7 text-amber-100/55">
              The moon governs cycles of growth, release, and reflection. Every reading on EverydayHoroscope is stamped with the current lunar phase -- so you always know whether to act, wait, release, or go inward with what the cards reveal.
            </p>
            <p className="mt-4 text-xs text-amber-400/60">New · Waxing · Full · Waning · Dark</p>
          </div>
        </div>
      </section>

      {/* ── FAQ ── */}
      <section className="mx-auto max-w-3xl px-4 pb-16">
        <h2 className="mb-8 text-center font-playfair text-2xl font-semibold text-amber-200">Frequently Asked Questions</h2>
        <div className="space-y-4">
          {FAQS.map(f => (
            <div key={f.q} className="rounded-xl border border-amber-400/10 bg-white/[0.04] p-5">
              <p className="mb-2 font-semibold text-amber-100">{f.q}</p>
              <p className="text-sm leading-6 text-amber-100/55">{f.a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Bottom CTA ── */}
      <section className="border-t border-amber-400/10 py-16 text-center">
        <p className="mb-2 font-cinzel text-xs uppercase tracking-[0.3em] text-amber-400/60">Begin your practice</p>
        <h2 className="mb-4 font-cinzel text-3xl font-bold text-amber-100">Draw Your First Card</h2>
        <p className="mx-auto mb-8 max-w-md text-sm leading-7 text-amber-100/40">
          Daily draws are free. Spreads, timing guidance, and the full Journal are available with Premium.
        </p>
        <button
          onClick={handleCTA}
          className="inline-flex items-center gap-2 rounded-full bg-amber-500 px-8 py-4 text-base font-semibold text-stone-900 shadow-lg transition hover:bg-amber-400"
        >
          {user ? "Open Tarot →" : "Get Started -- Free →"}
        </button>
      </section>
    </div>
  );
}
