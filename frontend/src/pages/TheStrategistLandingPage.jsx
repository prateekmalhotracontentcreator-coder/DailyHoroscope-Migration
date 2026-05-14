import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, ChevronDown } from 'lucide-react';
import { SEO } from '../components/SEO';
import { useAuth } from '../context/AuthContext';

const LOGIN_REDIRECT = { state: { from: { pathname: '/strategist' } } };

const LAYERS = [
  {
    badge: 'Layer 0',
    title: 'The Oracle Gate',
    body: 'Ask Krishna before any campaign. YES unlocks the War Room. WAIT triggers a remedy sequence. NO or PRAY activates specific recovery protocols.',
    accent: 'border-gold/30 bg-gold/[0.08]',
  },
  {
    badge: 'Layer 1',
    title: 'Astrology Engine',
    body: 'Your Vedic birth chart powers live dasha timing, command planet, and power-direction strategy inside the dashboard.',
    accent: 'border-white/10 bg-white/[0.03]',
  },
  {
    badge: 'Layer 2',
    title: 'Lal Kitab 5-Gate Diagnostic',
    body: 'Karmic debt, dormant houses, Mercury collisions, year-lord timing, and geography alignment stay visible in one diagnosis rail.',
    accent: 'border-white/10 bg-white/[0.03]',
  },
  {
    badge: 'Layer 3',
    title: 'Strategist Engine',
    body: 'Transit-triggered missions, hurdle alerts, Golden Hour state changes, and surrogate pivots convert the chart into operating intelligence.',
    accent: 'border-white/10 bg-white/[0.03]',
  },
  {
    badge: 'Layer 4',
    title: '43-Day Remedy Roadmap',
    body: 'Mission pivot actions and LK remedies merge into one execution sequence with streak tracking and debt-clearance momentum.',
    accent: 'border-white/10 bg-white/[0.03]',
  },
  {
    badge: 'Layer 5',
    title: 'Premium Executive Brief',
    body: 'A polished strategist report packages conquest probability, Gate 0 verdict, timeline, and tactical recommendations into one premium layer.',
    accent: 'border-gold/30 bg-gradient-to-br from-gold/12 to-gold/[0.03]',
  },
];

const WAR_STATES = [
  { icon: '⚔️', title: 'OFFENSIVE', sub: 'Rituals Open', tone: 'border-gold/25 bg-gold/[0.08]', color: '#FFD700 glow' },
  { icon: '🌅', title: 'GOLDEN HOUR', sub: 'Act Now — 30min window', tone: 'border-orange-500/25 bg-orange-500/[0.08]', color: '#FFC42E→#FF3131 pulse' },
  { icon: '🌙', title: 'DEFENSIVE', sub: 'Rituals Locked', tone: 'border-slate-700/60 bg-slate-950/80', color: '#000B1E bg' },
];

const SCORE_TIERS = [
  { range: '85–99%', title: 'Sovereign Dominance', sub: 'Expansion / All-In', tone: 'border-emerald-500/35 bg-emerald-500/10 text-emerald-300' },
  { range: '60–84%', title: 'Operational Friction', sub: 'Patch & Pivot', tone: 'border-amber-500/35 bg-amber-500/10 text-amber-300' },
  { range: '40–59%', title: 'Strategic Siege', sub: 'Hold Ground / Remedy', tone: 'border-orange-500/35 bg-orange-500/10 text-orange-300' },
  { range: '0–39%', title: 'Karmic Lockdown', sub: 'Withdraw / Full Reset', tone: 'border-red-500/35 bg-red-500/10 text-red-300' },
];

const GATE_PATHS = [
  { icon: '✅', title: 'YES', body: 'War Room unlocked' },
  { icon: '⏳', title: 'WAIT', body: 'Pre-Flight remedy plan' },
  { icon: '🛑', title: 'NO', body: 'Score to 60%' },
  { icon: '🙏', title: 'PRAY', body: 'Full Surrender path' },
];

const STATS = [
  { value: '361', label: 'LK Remedy Rules' },
  { value: '462', label: 'Strategist Mission Rules' },
  { value: '43', label: 'Days per Cycle' },
];

function StrategistStarField({ opacity = 0.62 }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return undefined;

    const context = canvas.getContext('2d');
    let frameId = 0;

    const resize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };

    resize();
    window.addEventListener('resize', resize);

    const stars = Array.from({ length: 135 }, () => ({
      x: Math.random(),
      y: Math.random(),
      radius: Math.random() * 1.6 + 0.25,
      speed: Math.random() * 0.008 + 0.002,
      phase: Math.random() * Math.PI * 2,
    }));

    const draw = (time) => {
      context.clearRect(0, 0, canvas.width, canvas.height);
      stars.forEach((star) => {
        const alpha = 0.24 + 0.72 * Math.abs(Math.sin(time * star.speed + star.phase));
        context.beginPath();
        context.arc(star.x * canvas.width, star.y * canvas.height, star.radius, 0, Math.PI * 2);
        context.fillStyle = `rgba(197,160,89,${alpha * opacity})`;
        context.fill();
      });
      frameId = requestAnimationFrame(draw);
    };

    frameId = requestAnimationFrame(draw);

    return () => {
      cancelAnimationFrame(frameId);
      window.removeEventListener('resize', resize);
    };
  }, [opacity]);

  return <canvas ref={canvasRef} className="pointer-events-none absolute inset-0 h-full w-full" />;
}

function formatFormValue(value) {
  if (!value) return '';
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toISOString().slice(0, 10);
}

export default function TheStrategistLandingPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [form, setForm] = useState({
    name: '',
    dob: '',
    tob: '',
    tob_unknown: false,
    city: '',
  });
  const layersRef = useRef(null);

  const schema = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebPage',
        '@id': 'https://www.everydayhoroscope.in/the-strategist#webpage',
        name: 'The Strategist — Premium Integrated Vedic Career Mentor',
        description: 'Bloomberg Terminal for Karma. 823 Lal Kitab rules, Krishna Prashnavali Gate 0 oracle, Conquest Probability scoring, transit-triggered missions, and 43-day remedy roadmap.',
        url: 'https://www.everydayhoroscope.in/the-strategist',
        isPartOf: { '@id': 'https://www.everydayhoroscope.in/#website' },
        publisher: { '@id': 'https://www.everydayhoroscope.in/#organization' },
        breadcrumb: {
          '@type': 'BreadcrumbList',
          itemListElement: [
            { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://www.everydayhoroscope.in' },
            { '@type': 'ListItem', position: 2, name: 'The Strategist', item: 'https://www.everydayhoroscope.in/the-strategist' },
          ],
        },
      },
      {
        '@type': 'Service',
        '@id': 'https://www.everydayhoroscope.in/the-strategist#service',
        name: 'The Strategist — Premium Integrated Vedic Career Mentor',
        description: 'Premium career and business intelligence combining Lal Kitab diagnostics, Krishna Prashnavali oracle, and Vedic birth chart analysis into a live war room with 823 rules, Conquest Probability scoring, and 43-day remedy protocols.',
        provider: { '@id': 'https://www.everydayhoroscope.in/#organization' },
        serviceType: 'Vedic Astrology Career Consulting',
        areaServed: 'IN',
        offers: {
          '@type': 'Offer',
          price: '1599',
          priceCurrency: 'INR',
          description: 'Premium Monthly subscription',
        },
      },
    ],
  };

  function goToWarRoom() {
    if (user) {
      navigate('/strategist');
      return;
    }
    navigate('/login', LOGIN_REDIRECT);
  }

  function updateField(key, value) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function handleSubmit(event) {
    event.preventDefault();

    const payload = {
      name: form.name.trim(),
      dob: formatFormValue(form.dob),
      tob: form.tob_unknown ? '' : form.tob,
      tob_unknown: form.tob_unknown,
      city: form.city.trim(),
      timestamp: Date.now(),
    };

    localStorage.setItem('strategist-profile-draft', JSON.stringify(payload));
    goToWarRoom();
  }

  return (
    <div className="min-h-screen overflow-x-hidden bg-background text-foreground">
      <SEO
        title="The Strategist — Premium Vedic Career Mentor | War Room"
        description="Bloomberg Terminal for Karma. 823 Lal Kitab rules, Krishna Prashnavali oracle, and live Vedic birth chart intelligence — all in one war room for founders and executives."
        url="https://www.everydayhoroscope.in/the-strategist"
        schema={schema}
      />

      <style>{`
        .strategist-shell {
          background:
            radial-gradient(circle at 16% 18%, rgba(197,160,89,0.18), transparent 24%),
            radial-gradient(circle at 82% 12%, rgba(249,115,22,0.12), transparent 20%),
            linear-gradient(180deg, #050b15 0%, #09111d 44%, #111925 100%);
        }
        .strategist-reveal {
          opacity: 0;
          transform: translateY(24px);
          animation: strategistReveal 0.8s ease forwards;
        }
        @keyframes strategistReveal {
          from {
            opacity: 0;
            transform: translateY(24px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>

      <div className="strategist-shell relative overflow-hidden">
        <StrategistStarField />
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-24">
          <div className="relative rounded-[34px] border border-gold/15 bg-black/10 px-6 py-12 shadow-[0_35px_120px_rgba(2,6,23,0.35)] backdrop-blur-[2px] sm:px-10 lg:px-12">
            <div className="pointer-events-none absolute inset-0 rounded-[34px] bg-[radial-gradient(circle_at_50%_18%,rgba(197,160,89,0.18),transparent_26%)]" />
            <div className="relative max-w-4xl strategist-reveal">
              <div className="inline-flex items-center gap-2 rounded-full border border-gold/25 bg-gold/[0.06] px-4 py-2 text-xs uppercase tracking-[0.3em] text-gold/80">
                <span>⚔️</span>
                <span>Premium Integrated Vedic Career Mentor</span>
              </div>
              <h1 className="mt-6 text-5xl font-cinzel text-foreground sm:text-6xl lg:text-7xl">The Strategist</h1>
              <p className="mt-5 max-w-3xl text-lg font-playfair leading-8 text-white/76 sm:text-xl">
                Bloomberg Terminal for Karma. 823 Rules. Six Intelligence Layers. One War Room.
              </p>
              <p className="mt-5 max-w-3xl text-base leading-8 text-white/70 sm:text-lg">
                A business intelligence system for founders, executives, and professionals. Your Vedic birth chart powers live missions, strategic timing, and karmic diagnostics — all in one command centre.
              </p>
              <div className="mt-9 flex flex-wrap gap-3">
                <button
                  type="button"
                  onClick={goToWarRoom}
                  className="inline-flex items-center gap-2 rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:bg-gold/90"
                >
                  Enter the War Room <ArrowRight className="h-4 w-4" />
                </button>
                <button
                  type="button"
                  onClick={() => layersRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })}
                  className="inline-flex items-center gap-2 rounded-full border border-white/12 bg-white/[0.03] px-6 py-3 text-sm font-semibold text-foreground transition hover:bg-white/[0.06]"
                >
                  See How It Works <ChevronDown className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>

          <div className="mt-10 grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
            <div className="strategist-reveal rounded-[30px] border border-gold/15 bg-card/90 p-6 shadow-[0_25px_90px_rgba(2,6,23,0.18)] sm:p-8" style={{ animationDelay: '120ms' }}>
              <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">Begin Your Karmic Intelligence Profile</p>
              <h2 className="mt-3 text-3xl font-cinzel text-foreground">30 seconds. Pre-loaded into your War Room after login.</h2>
              <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
                <div className="grid gap-4 sm:grid-cols-2">
                  <label className="space-y-2">
                    <span className="text-xs uppercase tracking-[0.24em] text-white/48">Name</span>
                    <input
                      type="text"
                      value={form.name}
                      onChange={(event) => updateField('name', event.target.value)}
                      className="w-full rounded-2xl border border-white/10 bg-[#09111e] px-4 py-3 text-sm text-white outline-none transition focus:border-gold/55"
                      placeholder="Your full name"
                      required
                    />
                  </label>
                  <label className="space-y-2">
                    <span className="text-xs uppercase tracking-[0.24em] text-white/48">Date of Birth</span>
                    <input
                      type="date"
                      value={form.dob}
                      onChange={(event) => updateField('dob', event.target.value)}
                      className="w-full rounded-2xl border border-white/10 bg-[#09111e] px-4 py-3 text-sm text-white outline-none transition focus:border-gold/55"
                      required
                    />
                  </label>
                  <label className="space-y-2">
                    <span className="text-xs uppercase tracking-[0.24em] text-white/48">Time of Birth</span>
                    <input
                      type="time"
                      value={form.tob}
                      onChange={(event) => updateField('tob', event.target.value)}
                      disabled={form.tob_unknown}
                      className="w-full rounded-2xl border border-white/10 bg-[#09111e] px-4 py-3 text-sm text-white outline-none transition disabled:cursor-not-allowed disabled:opacity-60 focus:border-gold/55"
                      required={!form.tob_unknown}
                    />
                  </label>
                  <label className="space-y-2">
                    <span className="text-xs uppercase tracking-[0.24em] text-white/48">City of Birth</span>
                    <input
                      type="text"
                      value={form.city}
                      onChange={(event) => updateField('city', event.target.value)}
                      className="w-full rounded-2xl border border-white/10 bg-[#09111e] px-4 py-3 text-sm text-white outline-none transition focus:border-gold/55"
                      placeholder="City, State"
                      required
                    />
                  </label>
                </div>

                <label className="flex items-start gap-3 rounded-2xl border border-white/10 bg-white/[0.03] px-4 py-3">
                  <input
                    type="checkbox"
                    checked={form.tob_unknown}
                    onChange={(event) => updateField('tob_unknown', event.target.checked)}
                    className="mt-1 h-4 w-4 rounded border-gray-300 text-gold focus:ring-gold"
                  />
                  <span className="text-sm text-muted-foreground">I don&apos;t know my birth time</span>
                </label>

                <button
                  type="submit"
                  className="inline-flex items-center gap-2 rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:bg-gold/90"
                >
                  Start My Intelligence Profile <ArrowRight className="h-4 w-4" />
                </button>
              </form>

              <button
                type="button"
                onClick={() => navigate('/login', LOGIN_REDIRECT)}
                className="mt-5 text-sm text-gold transition hover:text-gold/85"
              >
                Already have an account? Sign in →
              </button>
            </div>

            <div className="strategist-reveal grid gap-4" style={{ animationDelay: '220ms' }}>
              <div className="rounded-[28px] border border-gold/15 bg-card/90 p-6">
                <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">The War Room Never Sleeps</p>
                <div className="mt-5 grid gap-3 md:grid-cols-3">
                  {WAR_STATES.map((state) => (
                    <div key={state.title} className={`rounded-2xl border p-4 ${state.tone}`}>
                      <p className="text-sm font-semibold text-foreground">{state.icon} {state.title}</p>
                      <p className="mt-2 text-sm text-muted-foreground">{state.sub}</p>
                      <p className="mt-3 text-xs uppercase tracking-[0.2em] text-muted-foreground">{state.color}</p>
                    </div>
                  ))}
                </div>
                <p className="mt-4 text-sm leading-7 text-muted-foreground">
                  The War Room state changes with sunset. Golden Hour is your 30-minute execution window.
                </p>
              </div>

              <div className="rounded-[28px] border border-gold/15 bg-card/90 p-6">
                <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">823 Rules. Mapped to Your Chart.</p>
                <div className="mt-5 grid gap-3 sm:grid-cols-3">
                  {STATS.map((stat) => (
                    <div key={stat.label} className="rounded-2xl border border-white/8 bg-white/[0.03] p-4 text-center">
                      <p className="text-3xl font-bold text-gold">{stat.value}</p>
                      <p className="mt-2 text-sm text-muted-foreground">{stat.label}</p>
                    </div>
                  ))}
                </div>
                <p className="mt-4 text-sm leading-7 text-muted-foreground">
                  361 Lal Kitab remedy records and 462 strategist mission rules combine into one guided command system for timing, action, and karmic recovery.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div ref={layersRef} className="mx-auto max-w-7xl space-y-10 px-4 py-12 sm:px-6 lg:px-8 lg:py-16">
        <section className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="rounded-[30px] border border-gold/15 bg-card/90 p-6 shadow-[0_25px_90px_rgba(2,6,23,0.18)] sm:p-8">
            <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">Six Layers of Intelligence. Zero Guesswork.</p>
            <div className="mt-6 space-y-4">
              {LAYERS.map((layer, index) => (
                <div key={layer.title} className={`rounded-[24px] border p-5 strategist-reveal ${layer.accent}`} style={{ animationDelay: `${120 + index * 100}ms` }}>
                  <div className="flex items-center gap-3">
                    <span className="rounded-full border border-gold/20 bg-gold/[0.06] px-3 py-1 text-[11px] uppercase tracking-[0.22em] text-gold">
                      {layer.badge}
                    </span>
                    {index === 5 ? <span className="rounded-full border border-gold/30 bg-gold/12 px-3 py-1 text-[11px] uppercase tracking-[0.22em] text-gold">Premium</span> : null}
                  </div>
                  <p className="mt-3 text-xl font-cinzel text-foreground">{layer.title}</p>
                  <p className="mt-2 text-sm leading-7 text-muted-foreground">{layer.body}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-6">
            <div className="rounded-[30px] border border-gold/15 bg-card/90 p-6 sm:p-8">
              <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">Your Conquest Score. Recalculated Daily.</p>
              <div className="mt-5 grid gap-3 sm:grid-cols-2">
                {SCORE_TIERS.map((tier) => (
                  <div key={tier.title} className={`rounded-2xl border p-4 ${tier.tone}`}>
                    <p className="text-[11px] uppercase tracking-[0.24em]">{tier.range}</p>
                    <p className="mt-2 text-lg font-semibold">{tier.title}</p>
                    <p className="mt-1 text-sm opacity-80">{tier.sub}</p>
                  </div>
                ))}
              </div>
              <p className="mt-4 text-sm leading-7 text-muted-foreground">
                Computed from Shadbala strength, Digbala alignment, Karmic Debt, transit peak, and ritual streak.
              </p>
            </div>

            <div className="rounded-[30px] border border-gold/15 bg-card/90 p-6 sm:p-8">
              <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">Gate 0 — Ask Krishna Before You Act</p>
              <div className="mt-5 grid gap-3 sm:grid-cols-2">
                {GATE_PATHS.map((path) => (
                  <div key={path.title} className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
                    <p className="text-lg font-semibold text-foreground">{path.icon} {path.title}</p>
                    <p className="mt-2 text-sm leading-7 text-muted-foreground">{path.body}</p>
                  </div>
                ))}
              </div>
              <p className="mt-4 text-sm leading-7 text-muted-foreground">
                The 18×18 Krishna Prashnavali grid. One tap. Divine direction.
              </p>
            </div>
          </div>
        </section>

        <section className="rounded-[34px] border border-gold/18 bg-[linear-gradient(135deg,rgba(197,160,89,0.16),rgba(15,23,42,0.46))] px-6 py-10 text-center shadow-[0_30px_100px_rgba(2,6,23,0.22)] sm:px-10">
          <p className="text-[11px] uppercase tracking-[0.32em] text-gold/80">Your Karmic War Room Is Ready</p>
          <h2 className="mt-4 text-4xl font-cinzel text-foreground sm:text-5xl">Premium Vedic Career Intelligence, built like a command centre.</h2>
          <p className="mx-auto mt-4 max-w-3xl text-base leading-8 text-white/72 sm:text-lg">
            Free account. Premium access from ₹1,599/month. Save your birth details now and arrive inside the War Room ready for Gate 0.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            <button
              type="button"
              onClick={goToWarRoom}
              className="inline-flex items-center gap-2 rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:bg-gold/90"
            >
              Enter the War Room <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </section>
      </div>
    </div>
  );
}
