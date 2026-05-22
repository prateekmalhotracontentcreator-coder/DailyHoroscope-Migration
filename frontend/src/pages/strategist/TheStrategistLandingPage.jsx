// ─────────────────────────────────────────────────────────────────────────────
// TheStrategistLandingPage.jsx
// STR-R2-A · Public Landing V1
//
// Fresh design, 9 sections. Replaces the previous Codex draft in full.
// Delivered by Claude Design 2026-05-20. Integrated by Claude Code.
// ─────────────────────────────────────────────────────────────────────────────

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ArrowRight, ChevronDown,
  Trophy, ListChecks, Clock, AlertTriangle, Zap,
} from 'lucide-react';

import { SEO } from '@/components/SEO';
import { useAuth } from '@/context/AuthContext';
import { cn } from '@/lib/utils';

import {
  StrategistThemeProvider, useStrategistTheme,
} from '@/components/strategist/StrategistThemeProvider';
import { StrategistThemeToggle } from '@/components/strategist/StrategistThemeToggle';
import { StrategistGoldSeal } from '@/components/strategist/StrategistGoldSeal';
import { ControlRoomBackdrop } from '@/components/strategist/ControlRoomBackdrop';
import { GlassCard } from '@/components/strategist/GlassCard';
import { Footer } from '@/components/Footer';

import '@/styles/strategist-tokens.css';

// ─────────────────────────────────────────────────────────────────────────────
// Locked copy
// ─────────────────────────────────────────────────────────────────────────────
const HERO = {
  headline: 'Run your career like a war room.',
  subhead:  'KP Oracle decides your entry. Dashas time your missions. You command the war room.',
};

const ORACLE_PROMPT = 'What weighs on your career most right now?';

const PROBLEMS = [
  {
    n: '01',
    title: "You're working hard at the wrong thing.",
    body: 'Without a Dasha-aware compass, effort is mistimed. The right action in the wrong sub-period returns nothing.',
  },
  {
    n: '02',
    title: "You're carrying debts you can't see.",
    body: 'Pitru-Rin and karmic blockers compound silently. Strategy that ignores ancestral debt under-reads every result.',
  },
  {
    n: '03',
    title: "Your remedies need people you can't reach.",
    body: "Many Vedic remedies require a Command-Planet relative. When they're absent, the Surrogate Bridge takes over.",
  },
];

const LAYERS = [
  { n: '05', name: 'Golden Hour Windows', sub: 'Live ephemeris timing for offensive vs. defensive lanes.',    Icon: Clock },
  { n: '04', name: 'Pitru-Rin Status',    sub: 'Ancestral debt ledger. Until cleared, results under-read.',  Icon: AlertTriangle },
  { n: '03', name: 'Dasha Timeline',      sub: 'Mahadasha · Antardasha · Pratyantar -- what governs each day.', Icon: Zap },
  { n: '02', name: 'Mission Board',       sub: 'Sub-Lord-routed missions across 9 strategic parameters.',    Icon: ListChecks },
  { n: '01', name: 'Conquest Score',      sub: 'The single number that summarises strategic standing.',      Icon: Trophy },
];

const MECHANISMS = [
  { n: 'I',   title: 'Missions',  body: 'Each mission carries a Command Planet, a 9-parameter schema, decision logic and a pivot rule.' },
  { n: 'II',  title: 'Pitru-Rin', body: 'Surfaces ancestral debt blocking the current Dasha. Cleared first, before any offensive mission runs.' },
  { n: 'III', title: 'Surrogate', body: "When a Command-Planet relative is absent, the Surrogate Bridge maps the remedy to an available stand-in." },
];

const CREDIBILITY = [
  'KP Sub-Lord Theory',
  'Brihat Parashara Hora Shastra',
  'Lal Kitab',
  'Vimshottari Dasha',
  'Live Swiss Ephemeris',
];

const FAQ = [
  {
    q: 'Do I need to be a Vedic astrology expert?',
    a: 'No. The Strategist speaks in plain strategic language -- Mission, Dasha, Window, Remedy -- and only renders the underlying KP / Lal Kitab logic when you ask for it.',
  },
  {
    q: 'Is this guaranteed?',
    a: 'No. The system is diagnostic, not deterministic. It surfaces the strategic shape of a window. You still run the play.',
  },
  {
    q: 'What is Gate 0?',
    a: 'A free KP Oracle reading on a single career question. The reading returns one of four verdicts -- YES, WAIT, NO, PRAY -- and routes you accordingly.',
  },
  {
    q: 'Can I use The Strategist without completing KP Oracle?',
    a: 'No. The Oracle is the gate. Until you have a verdict, the War Room is locked.',
  },
  {
    q: 'How is this different from horoscopes?',
    a: 'A horoscope describes weather. The Strategist routes missions, tracks debts, and gates entry on diagnosis. It is a command system, not a forecast.',
  },
  {
    q: "What happens if my Command Planet's relative isn't available?",
    a: 'The Surrogate Bridge maps the required remedy to a substitute relation, preserving the karmic vector. Detailed inside the War Room.',
  },
  {
    q: 'Is there a free tier?',
    a: 'Yes -- the Gate 0 oracle reading is free. The War Room is Premium and only opens after the verdict permits it.',
  },
];

// ─────────────────────────────────────────────────────────────────────────────
// Small reusable atoms
// ─────────────────────────────────────────────────────────────────────────────
function Eyebrow({ children, className }) {
  return (
    <div className={cn(
      'font-cinzel text-[11px] font-semibold uppercase tracking-[0.22em]',
      'text-[color:var(--strategist-gold)]',
      className,
    )}>
      {children}
    </div>
  );
}

function SectionHead({ kicker, title, sub, center }) {
  return (
    <div className={cn(
      'flex flex-col gap-2 max-w-[760px]',
      center && 'mx-auto text-center',
    )}>
      <Eyebrow>{kicker}</Eyebrow>
      <h2 className={cn(
        'font-cinzel font-medium leading-[1.08] tracking-[-0.005em]',
        'text-[1.875rem] md:text-[2.75rem]',
        'text-[color:var(--strategist-text-primary)]',
        'mt-1.5',
      )}>{title}</h2>
      {sub && (
        <p className={cn(
          'font-playfair italic leading-[1.5] mt-1.5',
          'text-base md:text-[1.1875rem]',
          'text-[color:var(--strategist-text-muted)]',
        )}>{sub}</p>
      )}
    </div>
  );
}

function PrimaryCTA({ children, onClick, size = 'md', className }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        'inline-flex items-center gap-2.5 rounded-full',
        'bg-gold text-[#1b1610] font-cinzel font-semibold uppercase',
        'tracking-[0.14em]',
        'shadow-[0_1px_2px_rgba(0,0,0,0.10),0_0_0_1px_rgba(197,160,89,0.30)]',
        'hover:bg-gold-hover transition-colors',
        size === 'lg' ? 'px-9 py-[18px] text-[17px]' : 'px-[26px] py-[14px] text-sm',
        className,
      )}
    >
      {children}
      <ArrowRight className="opacity-70" size={size === 'lg' ? 16 : 14} />
    </button>
  );
}

function GhostCTA({ children, href = '#problem', size = 'md', className }) {
  return (
    <a
      href={href}
      className={cn(
        'inline-flex items-center gap-2 rounded-full',
        'font-cinzel font-medium uppercase tracking-[0.14em]',
        'border border-[color:var(--strategist-card-border)]',
        'text-[color:var(--strategist-text-primary)]',
        'hover:border-gold/50 hover:text-[color:var(--strategist-gold)] transition-colors',
        size === 'lg' ? 'px-8 py-[17px] text-[15px]' : 'px-[22px] py-[13px] text-xs',
        className,
      )}
    >
      {children}
    </a>
  );
}

function DiamondDot({ className }) {
  return (
    <span
      aria-hidden
      className={cn('text-[10px] leading-none text-[color:var(--strategist-gold)] opacity-70', className)}
    >&#9670;</span>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Top nav
// ─────────────────────────────────────────────────────────────────────────────
function TopNav({ onSignIn }) {
  const { mode } = useStrategistTheme();
  const isDark = mode !== 'light';
  return (
    <header className={cn(
      'sticky top-0 z-20 flex items-center justify-between',
      'px-5 py-3.5 md:px-14 md:py-5',
      'backdrop-blur-md',
      'border-b border-[color:var(--strategist-card-border)]',
      isDark ? 'bg-[#0a0d14]/70' : 'bg-[hsl(var(--background))]/70',
    )}>
      <div className="flex items-center gap-2.5">
        <StrategistGoldSeal size={28} />
        <div className="flex flex-col leading-none">
          <span className="font-cinzel text-sm font-semibold tracking-[0.10em] text-[color:var(--strategist-text-primary)]">
            The Strategist
          </span>
          <span className="font-playfair italic text-[11px] mt-0.5 text-[color:var(--strategist-text-muted)]">
            Everyday Horoscope
          </span>
        </div>
      </div>

      <div className="flex items-center gap-2 md:gap-3.5">
        <nav className="hidden md:flex gap-[18px] mr-2.5">
          {[
            ['How it works', '#problem'],
            ['KP Oracle',    '#gating'],
            ['War Room',     '#layers'],
            ['FAQ',          '#faq'],
          ].map(([label, href]) => (
            <a key={label} href={href} className="font-cinzel text-[11px] font-medium uppercase tracking-[0.16em] text-[color:var(--strategist-text-muted)] hover:text-[color:var(--strategist-gold)] transition-colors">
              {label}
            </a>
          ))}
        </nav>
        <StrategistThemeToggle />
        <button
          type="button"
          onClick={onSignIn}
          className="font-cinzel text-[11px] font-semibold uppercase tracking-[0.18em] text-[color:var(--strategist-gold)] px-3.5 py-2 rounded-full border border-gold/35 hover:bg-gold/10 transition-colors"
        >
          Sign in
        </button>
      </div>
    </header>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Section 1 -- Hero
// ─────────────────────────────────────────────────────────────────────────────
function SecHero({ onEnter }) {
  return (
    <section
      id="hero"
      className="px-5 py-9 md:px-20 md:pt-24 md:pb-20 grid items-center gap-8 md:gap-16 md:grid-cols-[1.15fr_0.85fr] md:min-h-[88vh]"
    >
      <div className="order-2 md:order-1">
        <Eyebrow>The Strategist &middot; Premium</Eyebrow>
        <h1 className="font-cinzel font-medium leading-[1.05] tracking-[-0.005em] text-[38px] md:text-[64px] mt-3.5 mb-4 text-pretty text-[color:var(--strategist-text-primary)]">
          {HERO.headline}
        </h1>
        <p className="font-playfair italic text-[17px] md:text-[21px] leading-[1.45] max-w-[560px] text-[color:var(--strategist-text-muted)]">
          {HERO.subhead}
        </p>

        <div className="flex flex-wrap gap-3.5 mt-8">
          <PrimaryCTA size="lg" onClick={onEnter}>Enter the War Room</PrimaryCTA>
          <GhostCTA size="lg" href="#problem">See how it works</GhostCTA>
        </div>

        <div className="flex flex-wrap gap-x-5 gap-y-2.5 mt-8">
          {[
            'Gated by KP Oracle',
            'Vimshottari Dasha aware',
            'No LLM guesswork',
          ].map((t) => (
            <div key={t} className="flex items-center gap-2 font-cinzel text-[10.5px] font-medium uppercase tracking-[0.16em] text-[color:var(--strategist-text-muted)]">
              <DiamondDot />
              {t}
            </div>
          ))}
        </div>
      </div>

      <div className="order-1 md:order-2 grid place-items-center">
        <HeroSeal />
      </div>
    </section>
  );
}

function HeroSeal() {
  return (
    <div className="relative grid place-items-center w-[200px] h-[200px] md:w-[320px] md:h-[320px]">
      <svg viewBox="0 0 200 200" className="absolute inset-0 w-full h-full" aria-hidden>
        <defs>
          <radialGradient id="hexg" cx="50%" cy="50%" r="50%">
            <stop offset="0%"   stopColor="#C5A059" stopOpacity="0.12" />
            <stop offset="65%"  stopColor="#C5A059" stopOpacity="0.02" />
            <stop offset="100%" stopColor="#C5A059" stopOpacity="0" />
          </radialGradient>
        </defs>
        <polygon points="100,8 180,52 180,148 100,192 20,148 20,52"
          fill="url(#hexg)" stroke="#C5A059" strokeOpacity="0.45" strokeWidth="1" />
        <polygon points="100,28 162,64 162,136 100,172 38,136 38,64"
          fill="none" stroke="#C5A059" strokeOpacity="0.18" strokeWidth="1" />
      </svg>
      <StrategistGoldSeal size={96} rotating className="md:hidden" />
      <StrategistGoldSeal size={160} rotating className="hidden md:inline-block" />
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Section 2 -- The Problem
// ─────────────────────────────────────────────────────────────────────────────
function SecProblem() {
  return (
    <section id="problem" className="px-5 py-14 md:px-20 md:py-[110px]">
      <SectionHead
        kicker="&#9670; The Problem &middot; Why most systems fail"
        title="Three strategic failures."
        sub="The Strategist is built to solve all three -- using Vedic diagnostics, not motivational copy."
      />
      <div className="grid gap-3.5 md:gap-5 md:grid-cols-3 mt-6 md:mt-11">
        {PROBLEMS.map((it) => (
          <GlassCard key={it.n} className="p-6 md:p-7">
            <div className="font-strategist-mono text-[11px] tracking-[0.20em] text-[color:var(--strategist-gold)] mb-4">
              {it.n} / 03
            </div>
            <h3 className="font-cinzel text-xl font-medium leading-[1.25] mb-3 text-[color:var(--strategist-text-primary)]">
              {it.title}
            </h3>
            <p className="font-playfair text-[15px] leading-[1.6] text-[color:var(--strategist-text-muted)]">
              {it.body}
            </p>
          </GlassCard>
        ))}
      </div>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Section 3 -- The Gating Model
// ─────────────────────────────────────────────────────────────────────────────
function SecGating({ onBeginReading }) {
  return (
    <section id="gating" className="px-5 py-14 md:px-20 md:py-[110px]">
      <SectionHead
        kicker="&#9670; The Gating Model &middot; Signature"
        title="Entry is by oracle, not by payment."
        sub="The Strategist gates on diagnosis. You only enter the War Room when the KP Oracle returns the right verdict."
      />

      <div className="mt-7 md:mt-11 mb-7 md:mb-10">
        <OraclePromptSlot onBegin={onBeginReading} />
      </div>

      <div className="grid gap-3.5 md:gap-4 md:grid-cols-[1fr_auto_1fr_auto_1fr] items-stretch">
        <GateStep n="01" name="KP Oracle 18x18"
          desc="Ask Krishna one question. The 18x18 sub-lord matrix returns a verdict from the live ephemeris." />
        <FlowArrow />
        <GateStep n="02" name="Gate 0 Verdict" highlight
          desc="YES · WAIT · NO · PRAY. Each verdict routes you to a different next surface. Only YES opens the War Room." />
        <FlowArrow />
        <GateStep n="03" name="The War Room"
          desc="Five layers unlock: Conquest Score, Mission Board, Dasha Timeline, Pitru-Rin Status, Golden Hour windows." />
      </div>

      <div className="mt-7 md:mt-11 text-center">
        <div className="font-cinzel font-medium leading-[1.3] tracking-[0.02em] text-lg md:text-[26px] max-w-[660px] mx-auto text-[color:var(--strategist-text-primary)]">
          <DiamondDot />&nbsp; "Entry is by oracle, not by payment." &nbsp;<DiamondDot />
        </div>
        <div className="font-playfair italic text-[13px] mt-2 text-[color:var(--strategist-text-muted)]">
          Gate 0 is free. The War Room is Premium -- but only opens after the verdict.
        </div>
      </div>
    </section>
  );
}

function OraclePromptSlot({ onBegin }) {
  return (
    <GlassCard variant="highlight" className="relative overflow-hidden p-5 md:p-8 max-w-[880px] mx-auto">
      <div className="grid gap-4 md:gap-7 md:grid-cols-[auto_1fr_auto] items-center">
        <div className="grid place-items-center">
          <StrategistGoldSeal size={56} className="md:hidden" />
          <StrategistGoldSeal size={72} className="hidden md:inline-block" />
        </div>
        <div>
          <div className="font-cinzel text-[10px] font-semibold uppercase tracking-[0.26em] text-[color:var(--strategist-gold)] mb-2">
            &#9670; Oracle Trigger &middot; Gate 0 Entry Prompt
          </div>
          <div className="font-playfair italic leading-[1.35] text-lg md:text-2xl text-[color:var(--strategist-text-primary)]">
            "{ORACLE_PROMPT}"
          </div>
          <div className="font-strategist-mono text-[11px] tracking-[0.10em] mt-2.5 text-[color:var(--strategist-text-muted)]">
            ONE QUESTION &middot; ONE READING &middot; ASKED OF KRISHNA, NOT OF THE APP
          </div>
        </div>
        <div className="md:contents">
          <PrimaryCTA onClick={onBegin} className="hidden md:inline-flex">Begin a reading</PrimaryCTA>
        </div>
      </div>
      <div className="md:hidden mt-4">
        <PrimaryCTA onClick={onBegin}>Begin a reading</PrimaryCTA>
      </div>
      <span aria-hidden className="absolute top-3 right-3.5 font-strategist-mono text-[10px] tracking-[0.10em] text-[color:var(--strategist-text-muted)]">
        GATE-0
      </span>
    </GlassCard>
  );
}

function GateStep({ n, name, desc, highlight }) {
  const verdicts = ['YES', 'WAIT', 'NO', 'PRAY'];
  return (
    <GlassCard variant={highlight ? 'highlight' : 'default'} className="p-5 md:p-6 h-full relative">
      <div className="flex items-center gap-3 mb-3.5">
        <StrategistGoldSeal size={36} />
        <div className="font-strategist-mono text-[10.5px] tracking-[0.20em] text-[color:var(--strategist-text-muted)]">
          STEP {n}
        </div>
      </div>
      <h3 className="font-cinzel text-[19px] font-medium leading-[1.25] mb-2 text-[color:var(--strategist-text-primary)]">{name}</h3>
      <p className="font-playfair text-sm leading-[1.55] text-[color:var(--strategist-text-muted)]">{desc}</p>
      {highlight && (
        <div className="mt-4 pt-3.5 border-t border-dashed border-[color:var(--strategist-card-border)] flex flex-wrap gap-1.5">
          {verdicts.map((v) => (
            <span key={v} className={cn(
              'font-cinzel text-[10px] font-semibold tracking-[0.18em] px-2.5 py-1 rounded-full border',
              v === 'YES'
                ? 'border-emerald-500/40 text-emerald-500 bg-emerald-500/10'
                : 'border-gold/35 text-[color:var(--strategist-text-primary)]',
            )}>{v}</span>
          ))}
        </div>
      )}
    </GlassCard>
  );
}

function FlowArrow() {
  return (
    <>
      <div className="grid place-items-center h-9 md:hidden">
        <svg width="20" height="36" viewBox="0 0 20 36" aria-hidden>
          <line x1="10" y1="0" x2="10" y2="28" stroke="#C5A059" strokeWidth="1.5" />
          <polyline points="3,22 10,32 17,22" fill="none" stroke="#C5A059" strokeWidth="1.5" strokeLinejoin="round" />
        </svg>
      </div>
      <div className="hidden md:grid place-items-center min-w-[40px]">
        <svg width="60" height="20" viewBox="0 0 60 20" aria-hidden>
          <defs>
            <linearGradient id="arrgrad" x1="0" x2="1">
              <stop offset="0%"   stopColor="#C5A059" stopOpacity="0.2" />
              <stop offset="100%" stopColor="#C5A059" stopOpacity="0.95" />
            </linearGradient>
          </defs>
          <line x1="2" y1="10" x2="52" y2="10" stroke="url(#arrgrad)" strokeWidth="1.5" />
          <polyline points="48,4 56,10 48,16" fill="none" stroke="#C5A059" strokeWidth="1.5" strokeLinejoin="round" />
        </svg>
      </div>
    </>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Section 4 -- The 5-Layer War Room
// ─────────────────────────────────────────────────────────────────────────────
function SecLayers() {
  return (
    <section id="layers" className="px-5 py-14 md:px-20 md:py-[110px]">
      <SectionHead
        kicker="&#9670; The 5-Layer War Room"
        title="Anatomy of a Strategist session."
        sub="Five layers, one card language. Each is its own diagnostic surface."
      />

      <div className="mt-7 md:mt-11">
        {/* Mobile: horizontal scroll strip · Desktop: 5 equal columns */}
        <div className="flex gap-3 overflow-x-auto pb-2 md:pb-0 md:grid md:grid-cols-5 md:gap-4 snap-x snap-mandatory">
          {LAYERS.map((l, i) => (
            <LayerCard key={l.n} layer={l} idx={i} />
          ))}
        </div>
      </div>
    </section>
  );
}

function LayerCard({ layer, idx }) {
  const intensity = 0.03 + idx * 0.022;
  const Icon = layer.Icon;
  return (
    <div
      className="flex-shrink-0 w-[160px] md:w-auto snap-start flex flex-col items-center text-center gap-3 px-3 py-5 md:py-6 rounded-xl border border-[color:var(--strategist-card-border)]"
      style={{ background: `rgba(197,160,89,${intensity})` }}
    >
      {/* Icon */}
      <div className="grid place-items-center w-10 h-10 rounded-lg border border-gold/35 text-[color:var(--strategist-gold)] bg-gold/[0.06]">
        <Icon size={20} strokeWidth={1.6} />
      </div>

      {/* Layer number */}
      <div className="font-strategist-mono text-[10px] tracking-[0.22em] text-[color:var(--strategist-gold)]">
        LAYER &middot; {layer.n}
      </div>

      {/* Name */}
      <div className="font-cinzel text-[13px] md:text-[14px] font-medium leading-[1.25] text-[color:var(--strategist-text-primary)]">
        {layer.name}
      </div>

      {/* Sub -- hidden on smallest screens */}
      <div className="font-playfair text-[11.5px] leading-[1.45] text-[color:var(--strategist-text-muted)] hidden sm:block">
        {layer.sub}
      </div>

      {/* Badge */}
      <span className="mt-auto px-2.5 py-1 rounded-full border border-[color:var(--strategist-card-border)] font-cinzel text-[9px] font-semibold tracking-[0.20em] text-[color:var(--strategist-text-muted)]">
        SURFACE
      </span>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Section 5 -- The Mission Engine
// ─────────────────────────────────────────────────────────────────────────────
function SecMissionEngine() {
  return (
    <section id="engine" className="px-5 py-14 md:px-20 md:py-[110px]">
      <SectionHead
        kicker="&#9670; The Mission Engine"
        title="Mission &rarr; Dasha &rarr; Surrogate."
        sub="The three primitives that route every Strategist action. One mission is never one variable."
      />

      <div className="mt-7 md:mt-11 grid gap-4 md:gap-9 md:grid-cols-[1.05fr_0.95fr] items-stretch">
        <MissionFlowDiagram />
        <div className="grid gap-3.5 content-start">
          {MECHANISMS.map((m, i) => (
            <GlassCard key={m.n} variant={i === 0 ? 'highlight' : 'default'} className="p-5 md:p-6">
              <div className="flex items-baseline gap-3.5">
                <span className="font-cinzel text-[22px] font-semibold tracking-[0.04em] min-w-[28px] text-[color:var(--strategist-gold)]">
                  {m.n}
                </span>
                <div>
                  <h3 className="font-cinzel text-lg font-medium text-[color:var(--strategist-text-primary)]">{m.title}</h3>
                  <p className="font-playfair text-sm leading-[1.55] mt-1.5 text-[color:var(--strategist-text-muted)]">{m.body}</p>
                </div>
              </div>
            </GlassCard>
          ))}
        </div>
      </div>
    </section>
  );
}

function MissionFlowDiagram() {
  return (
    <GlassCard className="p-5 md:p-7 min-h-[320px] md:min-h-[420px] relative overflow-hidden">
      <Eyebrow className="text-[10px] text-[color:var(--strategist-text-muted)]">&#9670; FLOW &middot; MISSION ROUTING</Eyebrow>

      <div className="mt-5 grid gap-4">
        <FlowNode tone="primary" label="MISSION &middot; OP-MERCURY-WEST" sub="Closing window &middot; Q2 enterprise tier" />
        <FlowConnector ok label="DASHA ALIGNMENT &middot; Mercury sub-period active" />
        <FlowNode tone="success" label="DECISION &middot; Run sprint" sub="Shadbala &gt; 340 &middot; H7 clear &middot; no Mars aspect" />
        <FlowConnector label="PIVOT RULE &middot; CTR check at day 14" />
        <FlowNode tone="muted" label="SURROGATE &middot; Bridge fires" sub="Command-Planet relative absent &rarr; stand-in mapped" />
      </div>

      <span aria-hidden className="absolute bottom-3 right-3.5 font-strategist-mono text-[10px] tracking-[0.10em] text-[color:var(--strategist-text-muted)]">
        ID&middot;1019 &middot; LIVE
      </span>
    </GlassCard>
  );
}

function FlowNode({ label, sub, tone }) {
  const dot =
    tone === 'success' ? 'bg-emerald-500 shadow-[0_0_0_4px_rgba(63,170,122,0.18)]' :
    tone === 'muted'   ? 'bg-[color:var(--strategist-text-muted)] shadow-[0_0_0_4px_rgba(138,133,118,0.18)]' :
                         'bg-[color:var(--strategist-gold)] shadow-[0_0_0_4px_rgba(197,160,89,0.18)]';
  const border =
    tone === 'success' ? 'border-emerald-500/35' :
    tone === 'muted'   ? 'border-[color:var(--strategist-card-border)]' :
                         'border-gold/35';
  return (
    <div className={cn('grid grid-cols-[auto_1fr] gap-3 items-center px-3.5 py-3 rounded-[10px] border', border)}>
      <span className={cn('w-2.5 h-2.5 rounded-full', dot)} />
      <div>
        <div className="font-cinzel text-[12.5px] font-semibold tracking-[0.10em] text-[color:var(--strategist-text-primary)]">{label}</div>
        <div className="font-playfair italic text-[12.5px] mt-0.5 text-[color:var(--strategist-text-muted)]">{sub}</div>
      </div>
    </div>
  );
}

function FlowConnector({ label, ok }) {
  return (
    <div className="pl-[22px] ml-1 py-1 border-l-2 border-dashed border-gold/35 font-strategist-mono text-[10.5px] tracking-[0.12em] text-[color:var(--strategist-text-muted)]">
      <span className={ok ? 'text-emerald-500 mr-1.5' : 'text-[color:var(--strategist-gold)] mr-1.5'}>
        {ok ? '✓' : '↓'}
      </span>
      {label}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Section 6 -- Control Room preview
// Renders a CR backdrop preview regardless of page-level mode.
// Local A/B toggle lets users compare Variant A (Ambient) vs B (Tactical)
// independently of the global theme toggle.
// When page mode = 'light', preview uses CR-A/B grid on the host background
// with light GlassCards. When mode = 'dark' or CR, uses dark card surfaces.
// ─────────────────────────────────────────────────────────────────────────────
function SecControlRoom() {
  const { mode } = useStrategistTheme();
  // Local A/B toggle -- independent of global mode
  const globalVariant = mode === 'cr-tactical' ? 'tactical' : 'ambient';
  const [localVariant, setLocalVariant] = React.useState(globalVariant);
  const isLight = mode === 'light';

  return (
    <section id="control-room">
      <ControlRoomBackdrop variant={localVariant} className="px-5 py-14 md:px-20 md:py-28 min-h-[540px]">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <SectionHeadOnDark
            kicker={`&#9670; Control Room Preview &middot; Variant ${localVariant === 'tactical' ? 'B · Tactical' : 'A · Ambient'}`}
            title="The signature aesthetic."
            sub="Same card language. Different canvas behind. Toggle Control Room mode anywhere in The Strategist."
          />
          {/* Local A/B toggle -- switches just this preview section */}
          <div className="flex items-center gap-1.5 rounded-full border border-gold/30 bg-black/20 px-1 py-1 backdrop-blur-sm">
            {[{ key: 'ambient', label: 'A' }, { key: 'tactical', label: 'B' }].map(({ key, label }) => (
              <button
                key={key}
                type="button"
                onClick={() => setLocalVariant(key)}
                className={`rounded-full px-3 py-1 text-[11px] font-cinzel font-semibold uppercase tracking-[0.18em] transition ${
                  localVariant === key
                    ? 'bg-gold text-black'
                    : 'text-gold/70 hover:text-gold'
                }`}
              >
                {label}
              </button>
            ))}
          </div>
        </div>

        <div className="mt-6 md:mt-10 grid gap-4 md:gap-7 md:grid-cols-[1.2fr_0.8fr] items-stretch">
          {isLight ? <GlassWarCardSample /> : <CRWarCardSample />}
          {isLight ? <GlassSeriesSample /> : <CRSeriesSample />}
        </div>

        <div className="mt-6 md:mt-8 text-center font-playfair italic text-sm text-[#8A8576]">
          Variant A &mdash; grid is felt, not seen. Variant&nbsp;B &mdash; grid visible, tactical display.
        </div>
      </ControlRoomBackdrop>
    </section>
  );
}

function SectionHeadOnDark({ kicker, title, sub }) {
  return (
    <div className="flex flex-col gap-2 max-w-[760px]">
      <div className="font-cinzel text-[11px] font-semibold uppercase tracking-[0.22em] text-[color:var(--strategist-gold)]"
        dangerouslySetInnerHTML={{ __html: kicker }} />
      <h2 className="font-cinzel font-medium leading-[1.08] tracking-[-0.005em] text-[1.875rem] md:text-[2.75rem] text-[#ECE6D6] mt-1.5">
        {title}
      </h2>
      <p className="font-playfair italic leading-[1.5] mt-1.5 text-base md:text-[1.1875rem] text-[#8A8576]">
        {sub}
      </p>
    </div>
  );
}

function CRCard({ children, variant = 'default', className }) {
  const surface =
    variant === 'highlight' ? 'border-gold/40 bg-[#1c2230]'
  : variant === 'muted'     ? 'border-gold/10 bg-[#161b27]/60'
  : variant === 'warning'   ? 'border-red-500/30 bg-[#1c2230]'
                            : 'border-gold/20 bg-[#161b27]';
  return (
    <div className={cn('rounded-xl border shadow-sm', surface, className)}>
      {children}
    </div>
  );
}

function CRWarCardSample() {
  return (
    <CRCard variant="highlight" className="p-5 md:p-7">
      <div className="flex items-center justify-between mb-3.5">
        <div className="font-cinzel text-[11px] font-semibold uppercase tracking-[0.22em] text-[color:var(--strategist-gold)]">
          &#9670; Active Mission &middot; OP-MERCURY-WEST
        </div>
        <span className="font-strategist-mono text-[10.5px] tracking-[0.18em] text-[#8A8576]">PEAK &middot; 64%</span>
      </div>
      <h3 className="font-cinzel text-[22px] font-medium leading-[1.2] mb-2 text-[#ECE6D6]">
        Closing Window &mdash; Q2 Enterprise Tier
      </h3>
      <p className="font-playfair text-sm leading-[1.55] text-[#8A8576]">
        Mercury sub-period closes in 11 days. Push contract signatures before pre-rx shadow.
      </p>

      <div className="mt-4">
        <div className="flex justify-between font-strategist-mono text-[10.5px] tracking-[0.10em] text-[#8A8576]">
          <span>ORGANIC CTR</span>
          <span>3.2 / 3.0 pts &nbsp;&middot;&nbsp; +64%</span>
        </div>
        <div className="mt-2 h-1.5 rounded-full bg-white/5 overflow-hidden">
          <div className="h-full rounded-full bg-[color:var(--strategist-gold)]" style={{ width: '64%' }} />
        </div>
      </div>

      <div className="flex gap-2 mt-4 flex-wrap">
        {['ME · BUDH', 'H7 · 25°02′', 'PRE-RX', 'OP-1019'].map((t) => (
          <span key={t} className="font-strategist-mono text-[10px] px-2 py-1 rounded-md border border-gold/20 text-[#8A8576] tracking-[0.10em]">
            {t}
          </span>
        ))}
      </div>
    </CRCard>
  );
}

function CRSeriesSample() {
  return (
    <div className="grid gap-2.5 content-start">
      <CRCard className="p-4">
        <div className="font-cinzel text-[10px] font-semibold uppercase tracking-[0.22em] text-[#8A8576]">&#9670; DASHA</div>
        <div className="font-cinzel text-base font-medium mt-1.5 text-[#ECE6D6]">Mercury &middot; Saturn &middot; Moon</div>
        <div className="font-playfair italic text-[13px] mt-1 text-[#8A8576]">Pratyantardasha &middot; 2y 4m remaining</div>
      </CRCard>
      <CRCard variant="muted" className="p-4">
        <div className="font-cinzel text-[10px] font-semibold uppercase tracking-[0.22em] text-[#8A8576]">&#9671; COMPLETED</div>
        <div className="font-cinzel text-sm mt-1.5 text-[#ECE6D6]">OP-SOLAR-SOUTH &middot; Pillar URL refresh</div>
      </CRCard>
      <CRCard variant="warning" className="p-4">
        <div className="font-cinzel text-[10px] font-semibold uppercase tracking-[0.22em] text-[#E25C4B]">&#9670; STREAK AT RISK</div>
        <div className="font-cinzel text-sm mt-1.5 text-[#ECE6D6]">Pitru-Rin &middot; Day 12 ritual missed</div>
      </CRCard>
    </div>
  );
}

// Light-mode equivalents for Section 6 preview (used when page theme = Light)
function GlassWarCardSample() {
  return (
    <GlassCard variant="highlight" className="p-5 md:p-7">
      <div className="flex items-center justify-between mb-3.5">
        <div className="font-cinzel text-[11px] font-semibold uppercase tracking-[0.22em] text-gold">
          &#9670; Active Mission &middot; OP-MERCURY-WEST
        </div>
        <span className="font-mono text-[10.5px] tracking-[0.18em] text-muted-foreground">PEAK &middot; 64%</span>
      </div>
      <h3 className="font-cinzel text-[22px] font-medium leading-[1.2] mb-2 text-foreground">
        Organic Authority Sprint
      </h3>
      <p className="font-playfair text-[13.5px] leading-[1.65] text-muted-foreground mb-4">
        Elevate domain rating by 10 points in 90 days via topical cluster completion during Mercury direct.
      </p>
      <div className="rounded-lg border border-gold/20 bg-gold/[0.04] p-3">
        <div className="font-cinzel text-[10px] uppercase tracking-[0.20em] text-gold/70">KPI</div>
        <div className="flex items-end justify-between mt-1.5">
          <span className="font-cinzel text-base font-medium text-foreground">ORGANIC CTR</span>
          <span className="text-xs text-muted-foreground">3.2 / 3.0 pts &nbsp;&middot;&nbsp; +64%</span>
        </div>
        <div className="mt-2 h-1.5 rounded-full bg-gold/10 overflow-hidden">
          <div className="h-full rounded-full bg-gold" style={{ width: '64%' }} />
        </div>
      </div>
    </GlassCard>
  );
}

function GlassSeriesSample() {
  return (
    <div className="grid gap-2.5 content-start">
      <GlassCard className="p-4">
        <div className="font-cinzel text-[10px] font-semibold uppercase tracking-[0.22em] text-muted-foreground">&#9670; DASHA</div>
        <div className="font-cinzel text-base font-medium mt-1.5 text-foreground">Mercury &middot; Saturn &middot; Moon</div>
        <div className="font-playfair italic text-[13px] mt-1 text-muted-foreground">Pratyantardasha &middot; 2y 4m remaining</div>
      </GlassCard>
      <GlassCard variant="muted" className="p-4">
        <div className="font-cinzel text-[10px] font-semibold uppercase tracking-[0.22em] text-muted-foreground">&#9671; COMPLETED</div>
        <div className="font-cinzel text-sm mt-1.5 text-foreground">OP-SOLAR-SOUTH &middot; Pillar URL refresh</div>
      </GlassCard>
      <GlassCard variant="warning" className="p-4">
        <div className="font-cinzel text-[10px] font-semibold uppercase tracking-[0.22em] text-red-500">&#9670; STREAK AT RISK</div>
        <div className="font-cinzel text-sm mt-1.5 text-foreground">Pitru-Rin &middot; Day 12 ritual missed</div>
      </GlassCard>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Section 7 -- Credibility Bar
// ─────────────────────────────────────────────────────────────────────────────
function SecCredibility() {
  return (
    <section
      id="credibility"
      className="px-5 py-11 md:px-20 md:py-[70px] border-y border-[color:var(--strategist-card-border)]"
    >
      <div className="flex flex-wrap justify-center items-center gap-2.5 md:gap-[22px]">
        {CREDIBILITY.map((t, i) => (
          <React.Fragment key={t}>
            <span className="font-cinzel font-medium uppercase tracking-[0.20em] text-[11px] md:text-[13px] text-[color:var(--strategist-text-primary)]">
              {t}
            </span>
            {i < CREDIBILITY.length - 1 && <DiamondDot />}
          </React.Fragment>
        ))}
      </div>
      <div className="text-center mt-3.5 md:mt-5 font-playfair italic text-[13px] text-[color:var(--strategist-text-muted)]">
        Diagnostic, not deterministic. No LLM guesswork. Every verdict is derivable from the chart.
      </div>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Section 8 -- FAQ
// ─────────────────────────────────────────────────────────────────────────────
function SecFaq() {
  const [openIdx, setOpenIdx] = useState(0);

  const handleFaqClick = (i, q) => {
    const isOpening = openIdx !== i;
    setOpenIdx(openIdx === i ? -1 : i);
    // GA4 tracking -- fires only when a row is opened (not on close)
    if (isOpening && typeof window !== 'undefined' && window.gtag) {
      window.gtag('event', 'faq_opened', {
        event_category: 'Strategist Landing',
        faq_index: i + 1,
        faq_question: q,
      });
    }
  };

  return (
    <section id="faq" className="px-5 py-14 md:px-20 md:py-[110px]">
      <SectionHead kicker="&#9670; FAQ" title="Questions, answered." />
      <div className="mt-6 md:mt-10">
        <GlassCard className="px-4 md:px-8 py-1 md:py-3.5">
          {FAQ.map((it, i) => (
            <FaqRow
              key={i}
              q={it.q}
              a={it.a}
              open={openIdx === i}
              onClick={() => handleFaqClick(i, it.q)}
            />
          ))}
        </GlassCard>
      </div>
    </section>
  );
}

function FaqRow({ q, a, open, onClick }) {
  return (
    <div className="border-b border-[color:var(--strategist-card-border)] last:border-b-0">
      <button
        type="button"
        onClick={onClick}
        className="w-full grid grid-cols-[24px_1fr_auto] gap-3.5 items-center py-4 text-left"
      >
        <ChevronDown
          size={16}
          className={cn(
            'text-[color:var(--strategist-gold)] transition-transform duration-200',
            open ? 'rotate-180' : 'rotate-0',
          )}
        />
        <span className="font-cinzel font-medium text-base leading-[1.3] text-[color:var(--strategist-text-primary)]">
          {q}
        </span>
        <span className="font-strategist-mono text-[10px] tracking-[0.12em] text-[color:var(--strategist-text-muted)]">
          {open ? '- CLOSE' : '+ OPEN'}
        </span>
      </button>
      {open && (
        <div className="pl-[38px] pr-1 pb-5 font-playfair text-[15px] leading-[1.6] max-w-[720px] text-[color:var(--strategist-text-muted)]">
          {a}
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Section 9 -- Final CTA
// ─────────────────────────────────────────────────────────────────────────────
function SecFinalCta({ onEnter }) {
  return (
    <section id="final-cta" className="px-5 py-14 md:px-20 md:pt-[110px] md:pb-10 text-center">
      <div className="flex justify-center">
        <StrategistGoldSeal size={72} rotating className="md:hidden" />
        <StrategistGoldSeal size={96} rotating className="hidden md:inline-block" />
      </div>
      <h2 className="font-cinzel font-medium leading-[1.1] tracking-[-0.005em] text-[32px] md:text-[52px] max-w-[760px] mx-auto mt-5 mb-3.5 text-[color:var(--strategist-text-primary)]">
        {HERO.headline}
      </h2>
      <p className="font-playfair italic text-base md:text-[19px] leading-[1.5] max-w-[580px] mx-auto mb-8 text-[color:var(--strategist-text-muted)]">
        Begin with one oracle reading. The grid decides.
      </p>
      <PrimaryCTA size="lg" onClick={onEnter}>Enter the War Room</PrimaryCTA>

      <div className="mt-10 md:mt-14 pt-5 border-t border-[color:var(--strategist-card-border)] flex flex-wrap justify-between items-center gap-3">
        <div className="font-cinzel text-[11px] uppercase tracking-[0.18em] text-[color:var(--strategist-text-muted)]">
          &#9670; Everyday Horoscope &middot; The Strategist Module
        </div>
      </div>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Page composition
// ─────────────────────────────────────────────────────────────────────────────
function LandingInner() {
  const navigate = useNavigate();
  const { user } = useAuth() || {};

  const goEnter = () => {
    if (user) {
      navigate('/strategist/war-room');
    } else {
      navigate('/login', { state: { from: { pathname: '/strategist/war-room' } } });
    }
  };

  const goReading = () => {
    if (user) {
      navigate('/kp/oracle');
    } else {
      navigate('/login', { state: { from: { pathname: '/kp/oracle' } } });
    }
  };

  return (
    <>
      <SEO
        title="The Strategist · Run your career like a war room"
        description="A Vedic command system gated by KP Oracle. Dashas time your missions. You command the war room."
      />
      <TopNav onSignIn={goEnter} />
      <SecHero       onEnter={goEnter} />
      <SecProblem    />
      <SecGating     onBeginReading={goReading} />
      <SecLayers     />
      <SecMissionEngine />
      <SecControlRoom />
      <SecCredibility />
      <SecFaq        />
      <SecFinalCta   onEnter={goEnter} />
      <Footer />
    </>
  );
}

export default function TheStrategistLandingPage() {
  return (
    <StrategistThemeProvider>
      <LandingInner />
    </StrategistThemeProvider>
  );
}
