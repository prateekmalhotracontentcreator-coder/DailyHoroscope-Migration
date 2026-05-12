import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { SEO } from '../components/SEO';
import { ArrowRight, Sparkles, BookOpen, Layers, RotateCcw, Compass, AlertTriangle, Eye, ChevronDown, ChevronUp } from 'lucide-react';

// ─── Static data ─────────────────────────────────────────────────────────────

const GATES = [
  {
    icon: AlertTriangle,
    color: 'text-amber-500',
    bg: 'bg-amber-500/10',
    border: 'border-amber-500/30',
    gate: 'Gate 1',
    name: 'Karmic Debt Scan',
    subtitle: 'Pitru Rin — Ancestral Obligation',
    desc: 'Lal Kitab identifies specific planetary placements that indicate unresolved karmic debt inherited across generations. When these debts are active, they create invisible ceilings on wealth, health, and relationships — regardless of effort. The diagnostic identifies which of the 9 planetary debts are active in your chart and assigns the precise 43-day clearing sequence.',
    keyword: 'lal kitab karmic debt pitru rin',
  },
  {
    icon: Eye,
    color: 'text-blue-400',
    bg: 'bg-blue-400/10',
    border: 'border-blue-400/30',
    gate: 'Gate 2',
    name: 'Dormant House Awakening',
    subtitle: 'Sleeping Potential',
    desc: 'Certain houses in your Lal Kitab chart lie dormant — not malefic, just unawakened. These are untapped zones of talent, opportunity, and destiny waiting for the correct activation ritual. Gate 2 identifies which houses are asleep and prescribes the targeted remedy to unlock them.',
    keyword: 'lal kitab house awakening dormant planets',
  },
  {
    icon: RotateCcw,
    color: 'text-gold',
    bg: 'bg-gold/10',
    border: 'border-gold/30',
    gate: 'Gate 3',
    name: '35-Year Planetary Cycle',
    subtitle: 'Year-Lord Phase',
    desc: 'Lal Kitab divides life into 9 planetary periods spanning 35 years, each governed by a specific planet. The remedies that work for you today are entirely determined by your current year-lord. Gate 3 calculates your exact phase based on your age and prescribes phase-appropriate remedies — applying a remedy from the wrong phase actively suppresses results.',
    keyword: 'lal kitab year lord planetary cycle age',
  },
  {
    icon: Layers,
    color: 'text-purple-400',
    bg: 'bg-purple-400/10',
    border: 'border-purple-400/30',
    gate: 'Gate 4',
    name: 'Mercury Scan',
    subtitle: 'Empty Vessel & Rahu Collision',
    desc: 'Mercury in Lal Kitab governs logic, communication, and business. When Mercury occupies an empty house or collides with Rahu, it becomes a liability that silently undermines strategy, partnerships, and income. Gate 4 checks for these two critical Mercury configurations and applies protective counter-remedies before any expansion mission begins.',
    keyword: 'lal kitab mercury rahu remedies',
  },
  {
    icon: Compass,
    color: 'text-emerald-500',
    bg: 'bg-emerald-500/10',
    border: 'border-emerald-500/30',
    gate: 'Gate 5',
    name: 'Geographical Alignment',
    subtitle: 'Digbala — Directional Strength',
    desc: 'Each planet commands a specific compass direction where its power is amplified — called Digbala in Vedic astrology. Lal Kitab takes this further: your city of residence, the direction your workspace faces, and even the location of your cash drawer all affect planetary outcomes. Gate 5 maps your command planet to its power direction and prescribes alignment corrections.',
    keyword: 'lal kitab digbala directional remedies',
  },
];

const PLANETS = [
  { symbol: '☉', name: 'Sun',     role: 'Father, authority, career, government. Lal Kitab Sun remedies address ego debts and leadership blocks.' },
  { symbol: '☽', name: 'Moon',    role: 'Mother, mind, emotions, fluids. Moon debts manifest as anxiety, family disconnection, and cash-flow instability.' },
  { symbol: '♂', name: 'Mars',    role: 'Brothers, property, land, courage. Mars remedies activate dormant property luck and resolve sibling karmic debts.' },
  { symbol: '☿', name: 'Mercury', role: 'Sister, intellect, business, writing. Mercury remedies protect logic and communication from Rahu interference.' },
  { symbol: '♃', name: 'Jupiter', role: 'Husband/guru, wisdom, children, wealth. Jupiter debts block blessings and create guidance vacuums.' },
  { symbol: '♀', name: 'Venus',   role: 'Wife, luxury, beauty, comforts. Venus remedies restore material abundance and relationship harmony.' },
  { symbol: '♄', name: 'Saturn',  role: 'Servants, longevity, karma, discipline. Saturn karmic debts are the most persistent — requiring 43-day continuous protocols.' },
  { symbol: '☊', name: 'Rahu',    role: 'Paternal grandfather, ambition, technology, foreign. Rahu remedies neutralise obsessive patterns and illusion traps.' },
  { symbol: '☋', name: 'Ketu',    role: 'Maternal grandfather, spirituality, detachment. Ketu remedies resolve ancestral spiritual obligations.' },
];

const SAMPLE_REMEDIES = [
  {
    planet: 'Jupiter',
    title: 'The Saffron Thread Protocol',
    desc: 'For Jupiter karmic debt — wear a yellow thread on the index finger on Thursdays for 43 consecutive days. Offer yellow sweets at a Vishnu temple. This activates the guru principle and removes blessings blockage from the ancestral line.',
    days: 43,
    difficulty: 'Gentle',
  },
  {
    planet: 'Saturn',
    title: 'The Iron Anchor Sequence',
    desc: 'For Saturn karmic debt — feed black sesame seeds and mustard oil to a black dog every Saturday. Do not break the sequence. Saturn remedies require strict 43-day continuity — a single skip resets the cycle.',
    days: 43,
    difficulty: 'Strict',
  },
];

const FAQS = [
  {
    q: 'What is Lal Kitab astrology?',
    a: 'Lal Kitab ("The Red Book") is a 19th-century astrological system blending Vedic astrology with Arabic numerology and folk wisdom from Punjab. It was codified in five books published between 1939–1952 by Pandit Roop Chand Joshi. Unlike BPHS (Brihat Parasara Hora Shastra), Lal Kitab is prescription-first — it focuses on simple, inexpensive remedies that correct planetary imbalances without requiring complex rituals or expensive gemstones.',
  },
  {
    q: 'How is Lal Kitab different from Vedic astrology?',
    a: 'Standard Vedic astrology (Parashari) uses precise degree-based computations, divisional charts, and ashtakavarga. Lal Kitab uses a simplified house-based system where the ascendant is always Aries (house 1), making every chart immediately readable. Lal Kitab also introduces the concept of "sleeping planets" and "karmic debts" — concepts absent from Parashari — and its remedies are almost entirely practical and affordable.',
  },
  {
    q: 'What are Lal Kitab remedies (upay)?',
    a: 'Lal Kitab upay are corrective protocols — usually spanning 43 days — that use everyday objects (metals, grains, colours, plants, animals) to create planetary balance. They are non-invasive, inexpensive, and prescribe specific timing (day of week, lunar phase). The 43-day duration corresponds to the time required for a behavioural or energetic pattern to integrate at a cellular level.',
  },
  {
    q: 'What is Pitru Rin (ancestral debt)?',
    a: 'Pitru Rin is the Lal Kitab concept of karmic obligations inherited from your ancestral line. When a specific planetary debt goes unresolved across generations, it manifests in descendants as recurring patterns — financial ceilings, relationship failures, health conditions. The Lal Kitab diagnostic identifies active Pitru Rin and prescribes the exact surrogate or clearing ritual to resolve it.',
  },
  {
    q: 'How does the 43-day remedy cycle work?',
    a: 'Lal Kitab remedies are prescribed in 43-day unbroken cycles. Day 1 sets the planetary intention. Days 2–42 build cumulative energetic momentum. Day 43 is the integration and sealing day. Breaking the sequence — even once — cancels accumulated progress. Our tracker monitors your streak, sends reminders before the critical sunset window, and alerts you if a break risk is detected.',
  },
];

// ─── Collapsible FAQ item ─────────────────────────────────────────────────────
const FaqItem = ({ q, a }) => {
  const [open, setOpen] = useState(false);
  return (
    <div className="border border-border rounded-sm overflow-hidden">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between gap-3 px-5 py-4 text-left hover:bg-gold/[0.03] transition-colors"
      >
        <span className="text-sm font-semibold">{q}</span>
        {open ? <ChevronUp className="h-4 w-4 text-gold flex-shrink-0" /> : <ChevronDown className="h-4 w-4 text-muted-foreground flex-shrink-0" />}
      </button>
      {open && (
        <div className="px-5 pb-4 text-sm text-muted-foreground leading-relaxed border-t border-border bg-gold/[0.02]">
          <p className="pt-3">{a}</p>
        </div>
      )}
    </div>
  );
};

// ─── Page ─────────────────────────────────────────────────────────────────────
export default function LalKitabLandingPage() {
  const navigate = useNavigate();

  const schema = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebPage',
        '@id': 'https://www.everydayhoroscope.in/lal-kitab-remedies#webpage',
        'name': 'Lal Kitab Remedies — Karmic Diagnostics & 43-Day Upay Cycles',
        'description': 'Personalised Lal Kitab remedies based on your Vedic birth chart. Karmic debt scan, dormant house awakening, 35-year planetary cycles, and 43-day upay protocols.',
        'url': 'https://www.everydayhoroscope.in/lal-kitab-remedies',
        'isPartOf': { '@id': 'https://www.everydayhoroscope.in/#website' },
        'publisher': { '@id': 'https://www.everydayhoroscope.in/#organization' },
        'breadcrumb': {
          '@type': 'BreadcrumbList',
          'itemListElement': [
            { '@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://www.everydayhoroscope.in' },
            { '@type': 'ListItem', 'position': 2, 'name': 'Lal Kitab Remedies', 'item': 'https://www.everydayhoroscope.in/lal-kitab-remedies' },
          ],
        },
      },
      {
        '@type': 'Service',
        '@id': 'https://www.everydayhoroscope.in/lal-kitab-remedies#service',
        'name': 'Lal Kitab Karmic Diagnostic & Remedy Engine',
        'description': 'AI-powered Lal Kitab diagnostic that scans 5 karmic gates — ancestral debt, dormant houses, 35-year cycle, Mercury vulnerabilities, and directional alignment — and prescribes personalised 43-day upay protocols.',
        'provider': { '@id': 'https://www.everydayhoroscope.in/#organization' },
        'serviceType': 'Vedic Astrology',
        'areaServed': 'IN',
        'offers': {
          '@type': 'Offer',
          'price': '0',
          'priceCurrency': 'INR',
          'description': 'Free diagnostic with premium 43-day tracker',
        },
      },
      {
        '@type': 'FAQPage',
        'mainEntity': FAQS.map(f => ({
          '@type': 'Question',
          'name': f.q,
          'acceptedAnswer': { '@type': 'Answer', 'text': f.a },
        })),
      },
    ],
  };

  return (
    <div className="min-h-screen pb-24 lg:pb-0">
      <SEO
        title="Lal Kitab Remedies — Karmic Diagnostics & 43-Day Upay Cycles"
        description="Personalised Lal Kitab upay based on your Vedic birth chart. Pitru Rin scan, dormant house awakening, 35-year planetary cycles, Mercury protection, and directional alignment — 43-day remedy protocols."
        url="https://www.everydayhoroscope.in/lal-kitab-remedies"
        schema={schema}
      />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

        {/* ── HERO ── */}
        <div className="text-center mb-14">
          <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-[0.2em] px-4 py-2 rounded-full mb-6">
            <BookOpen className="h-3 w-3" /> Ancient Lal Kitab Wisdom
          </div>
          <h1 className="font-cinzel font-bold leading-tight mb-5" style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)' }}>
            Lal Kitab Remedies<br />
            <span className="text-gold">for the Modern Age</span>
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-3 leading-relaxed font-playfair">
            The 150-year-old Red Book system distilled into a 5-gate karmic diagnostic. Discover your ancestral debts, dormant potential, and the exact 43-day upay sequence to clear them.
          </p>
          <p className="text-sm text-muted-foreground max-w-xl mx-auto mb-8">
            Based on <strong className="text-foreground">666 curated Lal Kitab rules</strong> mapped to your natal chart — not generic advice.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <button
              onClick={() => navigate('/lk-remedies/onboard')}
              className="group inline-flex items-center gap-2 bg-gold hover:bg-gold/90 text-primary-foreground px-8 py-3.5 rounded-sm font-semibold text-sm transition-all hover:shadow-[0_8px_30px_-5px_rgba(197,160,89,0.5)] hover:-translate-y-0.5"
            >
              Begin Your Diagnostic <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </button>
            <button
              onClick={() => navigate('/lk-remedies/remedies')}
              className="inline-flex items-center gap-2 border border-border hover:border-gold/50 text-foreground px-8 py-3.5 rounded-sm font-medium text-sm transition-all hover:-translate-y-0.5"
            >
              Browse Remedy Library
            </button>
          </div>
        </div>

        {/* ── WHAT IS LAL KITAB ── */}
        <section className="rounded-sm border border-gold/20 bg-gold/[0.04] p-6 sm:p-8 mb-10">
          <h2 className="font-cinzel font-bold text-xl mb-4">What is Lal Kitab Astrology?</h2>
          <div className="grid sm:grid-cols-2 gap-6 text-sm text-muted-foreground leading-relaxed">
            <div>
              <p className="mb-3">
                <strong className="text-foreground">Lal Kitab</strong> — "The Red Book" — is a 19th-century astrological system
                codified in five volumes between 1939 and 1952 by Pandit Roop Chand Joshi. Born from the confluence
                of Vedic astrology, Arabic numerology, and Punjabi folk wisdom, it is today the most widely
                practised remedial astrology system in North India.
              </p>
              <p>
                Unlike classical Vedic (Parashari) astrology which focuses on precise planetary degrees and
                divisional charts, Lal Kitab is <strong className="text-foreground">prescription-first</strong> — every
                planetary placement maps directly to an inexpensive, practical remedy using everyday objects:
                grains, metals, plants, colours, and directional alignments.
              </p>
            </div>
            <div>
              <p className="mb-3">
                The system introduces concepts absent from classical astrology: <strong className="text-foreground">Pitru Rin</strong> (ancestral karmic debts
                that block descendants), <strong className="text-foreground">Soye Graha</strong> (sleeping planets with dormant potential),
                and the <strong className="text-foreground">43-day remedy cycle</strong> — the minimum unbroken duration for a planetary
                correction to integrate.
              </p>
              <p>
                Our engine processes your birth chart through <strong className="text-foreground">5 diagnostic gates</strong> — each scanning
                a different layer of your Lal Kitab profile — and prescribes a personalised, sequenced remedy
                protocol mapped to your current planetary year-lord phase.
              </p>
            </div>
          </div>
        </section>

        {/* ── 5 GATES ── */}
        <section className="mb-10">
          <div className="text-center mb-8">
            <div className="inline-flex items-center gap-2 text-gold text-xs font-semibold uppercase tracking-[0.2em] mb-3"><Sparkles className="h-3 w-3" /> The Diagnostic Engine</div>
            <h2 className="font-playfair text-2xl sm:text-3xl font-semibold">5 Karmic Gates</h2>
            <p className="text-muted-foreground text-sm mt-2 max-w-lg mx-auto">Each gate scans a different layer of your Lal Kitab chart. All 5 must clear before the remedy sequence is finalised.</p>
          </div>
          <div className="space-y-4">
            {GATES.map((g) => {
              const Icon = g.icon;
              return (
                <div key={g.gate} className={`rounded-sm border ${g.border} bg-card p-5 flex gap-4`}>
                  <div className={`${g.bg} ${g.color} w-10 h-10 rounded-sm flex items-center justify-center flex-shrink-0 mt-0.5`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="flex flex-wrap items-center gap-2 mb-1">
                      <span className={`text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-full ${g.bg} ${g.color}`}>{g.gate}</span>
                      <h3 className="font-semibold text-sm">{g.name}</h3>
                      <span className="text-xs text-muted-foreground">— {g.subtitle}</span>
                    </div>
                    <p className="text-sm text-muted-foreground leading-relaxed">{g.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* ── 9 PLANETS ── */}
        <section className="mb-10">
          <div className="text-center mb-8">
            <h2 className="font-playfair text-2xl sm:text-3xl font-semibold">The 9 Planets in Lal Kitab</h2>
            <p className="text-muted-foreground text-sm mt-2 max-w-lg mx-auto">Each planet governs a specific relative, life area, and karmic theme. Remedies are always planet-specific — never generic.</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {PLANETS.map((p) => (
              <div key={p.name} className="rounded-sm border border-border bg-card p-4 flex gap-3">
                <span className="text-2xl leading-none text-gold flex-shrink-0">{p.symbol}</span>
                <div>
                  <p className="text-sm font-semibold mb-1">{p.name}</p>
                  <p className="text-xs text-muted-foreground leading-relaxed">{p.role}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ── SAMPLE REMEDIES ── */}
        <section className="mb-10">
          <div className="text-center mb-8">
            <h2 className="font-playfair text-2xl sm:text-3xl font-semibold">Sample Remedy Protocols</h2>
            <p className="text-muted-foreground text-sm mt-2 max-w-lg mx-auto">Illustrative examples of Lal Kitab upay. Your personalised protocol is generated from your natal chart after the 5-gate diagnostic.</p>
          </div>
          <div className="grid sm:grid-cols-2 gap-5">
            {SAMPLE_REMEDIES.map((r) => (
              <div key={r.title} className="rounded-sm border border-gold/20 bg-gold/[0.04] p-5">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-bold uppercase tracking-widest text-gold">{r.planet} Remedy</span>
                  <div className="flex gap-2">
                    <span className="text-[10px] border border-border px-2 py-0.5 rounded-full text-muted-foreground">{r.days} days</span>
                    <span className="text-[10px] border border-border px-2 py-0.5 rounded-full text-muted-foreground">{r.difficulty}</span>
                  </div>
                </div>
                <h3 className="font-semibold text-sm mb-2">{r.title}</h3>
                <p className="text-xs text-muted-foreground leading-relaxed">{r.desc}</p>
              </div>
            ))}
          </div>
          <p className="text-center text-xs text-muted-foreground mt-4">
            Your actual remedy sequence is generated from your birth chart — not from a generic library.
          </p>
        </section>

        {/* ── 43-DAY TRACKER ── */}
        <section className="rounded-sm border border-border p-6 sm:p-8 mb-10">
          <div className="flex flex-col sm:flex-row gap-6 items-start">
            <div className="flex-1">
              <h2 className="font-cinzel font-bold text-lg mb-3">The 43-Day Tracker</h2>
              <p className="text-sm text-muted-foreground leading-relaxed mb-3">
                Lal Kitab remedies require strict continuity. A single skipped day resets Saturn and Rahu sequences entirely.
                The tracker monitors your daily ritual log, calculates discipline percentage, and shows
                your <strong className="text-foreground">debt clearance progress</strong> across all active planetary obligations.
              </p>
              <ul className="space-y-1.5 text-xs text-muted-foreground">
                {['Daily ritual check-in with sunset window reminder', 'Streak counter — broken streaks auto-flagged', 'Per-planet debt bar (X of 9 ancestral debts cleared)', 'Surrogate activation for missing family members', '43-day completion certificate'].map(f => (
                  <li key={f} className="flex items-center gap-2">
                    <span className="text-gold">✦</span> {f}
                  </li>
                ))}
              </ul>
            </div>
            <div className="rounded-sm border border-gold/30 bg-gold/[0.06] p-5 text-center min-w-[160px]">
              <p className="text-4xl font-cinzel font-bold text-gold mb-1">43</p>
              <p className="text-xs text-muted-foreground uppercase tracking-widest">Days to<br />Integration</p>
            </div>
          </div>
        </section>

        {/* ── FAQ ── */}
        <section className="mb-10">
          <h2 className="font-playfair text-2xl sm:text-3xl font-semibold text-center mb-6">Frequently Asked Questions</h2>
          <div className="space-y-2">
            {FAQS.map((f) => <FaqItem key={f.q} q={f.q} a={f.a} />)}
          </div>
        </section>

        {/* ── FINAL CTA ── */}
        <section className="rounded-sm border border-gold/20 bg-gold/[0.04] p-8 text-center">
          <Sparkles className="h-8 w-8 text-gold mx-auto mb-4 opacity-80" />
          <h2 className="font-cinzel font-bold text-xl mb-3">Run Your Lal Kitab Diagnostic</h2>
          <p className="text-sm text-muted-foreground max-w-md mx-auto mb-6 leading-relaxed">
            Enter your birth details. The engine scans all 5 gates, identifies your active karmic debts,
            and generates your personalised 43-day upay sequence — specific to your chart, your age, and your current planetary phase.
          </p>
          <button
            onClick={() => navigate('/lk-remedies/onboard')}
            className="group inline-flex items-center gap-2 bg-gold hover:bg-gold/90 text-primary-foreground px-10 py-3.5 rounded-sm font-semibold text-sm transition-all hover:shadow-[0_8px_30px_-5px_rgba(197,160,89,0.5)] hover:-translate-y-0.5"
          >
            Begin Free Diagnostic <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
          </button>
          <p className="mt-3 text-xs text-muted-foreground">Requires birth date and time · Report generated instantly</p>
        </section>

      </div>
    </div>
  );
}
