import React, { useMemo, useRef } from 'react';
import { ArrowRight, CheckCircle2 } from 'lucide-react';
import { SEO } from '../../../components/SEO';

const PROCESS_STEPS = [
  {
    number: '1',
    title: 'Enter your birth details',
    body: 'Date, time, and place of birth create the chart foundation used by this report.',
  },
  {
    number: '2',
    title: 'Our Vedic engine computes your chart',
    body: 'Swiss Ephemeris precision plus Vedic timing logic calculate the personalised report structure.',
  },
  {
    number: '3',
    title: 'Receive your personalised report',
    body: 'The final output is written in clear, actionable English with structured sections and remedies.',
  },
];

function buildFaqSchema(page) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: page.faqs.map((faq) => ({
      '@type': 'Question',
      name: faq.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.answer,
      },
    })),
  };
}

function AccentButton({ href, color, children }) {
  return (
    <a
      href={href}
      className="inline-flex items-center justify-center gap-2 rounded-full px-6 py-3 text-sm font-semibold text-white transition hover:opacity-90"
      style={{ backgroundColor: color, boxShadow: `0 18px 40px ${color}40` }}
    >
      {children}
    </a>
  );
}

function OutlineButton({ onClick, color, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="inline-flex items-center justify-center gap-2 rounded-full border bg-white/5 px-6 py-3 text-sm font-semibold text-white transition hover:bg-white/10"
      style={{ borderColor: `${color}88`, color }}
    >
      {children}
    </button>
  );
}

function FeatureGrid({ page }) {
  return (
    <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
      {page.features.map((feature) => {
        const Icon = feature.icon;
        return (
          <article
            key={feature.title}
            className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5 shadow-sm backdrop-blur-sm"
          >
            <div
              className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-2xl border"
              style={{ borderColor: `${page.color}55`, color: page.color, background: `${page.color}14` }}
            >
              <Icon className="h-5 w-5" />
            </div>
            <h3 className="font-playfair text-xl font-semibold text-foreground">{feature.title}</h3>
            <p className="mt-2 text-sm leading-7 text-muted-foreground">{feature.body}</p>
          </article>
        );
      })}
    </div>
  );
}

function SamplePreview({ page }) {
  return (
    <div className="relative overflow-hidden rounded-[28px] border border-gold/20 bg-[#10151f] p-6 text-white shadow-[0_28px_80px_rgba(2,6,23,0.32)]">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(255,255,255,0.08),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(255,255,255,0.05),transparent_26%)]" />
      <div className="relative space-y-5">
        <div className="flex items-center gap-4 border-b border-white/10 pb-5">
          <div
            className="grid h-14 w-14 place-items-center rounded-2xl text-2xl font-bold"
            style={{ background: `${page.color}22`, color: page.color, border: `1px solid ${page.color}55` }}
          >
            {page.icon}
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.28em] text-white/45">{page.sample.eyebrow}</p>
            <h3 className="mt-1 font-playfair text-2xl font-semibold">{page.sample.heading}</h3>
          </div>
        </div>

        <div className="grid gap-4 blur-[2.5px] select-none lg:grid-cols-[1.1fr_0.9fr]">
          <div className="space-y-4">
            {page.sample.sections.map((section) => (
              <section key={section.title} className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
                <h4 className="font-playfair text-lg font-semibold">{section.title}</h4>
                <p className="mt-2 text-sm leading-7 text-white/72">{section.body}</p>
              </section>
            ))}
          </div>

          <section className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
            <h4 className="font-playfair text-lg font-semibold">Supportive remedies</h4>
            <div className="mt-4 grid gap-3 sm:grid-cols-3 lg:grid-cols-1">
              <div className="rounded-2xl border border-white/10 bg-black/10 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-white/45">Mantra</p>
                <p className="mt-2 text-sm leading-6 text-white/78">{page.sample.remedies.mantra}</p>
              </div>
              <div className="rounded-2xl border border-white/10 bg-black/10 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-white/45">Gemstone</p>
                <p className="mt-2 text-sm leading-6 text-white/78">{page.sample.remedies.gemstone}</p>
              </div>
              <div className="rounded-2xl border border-white/10 bg-black/10 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-white/45">Ritual</p>
                <p className="mt-2 text-sm leading-6 text-white/78">{page.sample.remedies.ritual}</p>
              </div>
            </div>
          </section>
        </div>
      </div>

      <div className="absolute inset-x-0 bottom-0 top-0 flex items-end justify-center bg-gradient-to-t from-[#10151f] via-transparent to-transparent p-6">
        <div
          className="w-full max-w-xl rounded-full border px-5 py-3 text-center text-sm font-semibold uppercase tracking-[0.22em]"
          style={{ borderColor: `${page.color}66`, background: `${page.color}22`, color: '#fff7ef' }}
        >
          Premium -- Unlock Full Report
        </div>
      </div>
    </div>
  );
}

export default function ReportLandingPageShell({ page }) {
  const sampleRef = useRef(null);
  const schema = useMemo(() => buildFaqSchema(page), [page]);

  function scrollToSample() {
    sampleRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <SEO
        title={page.titleStem}
        description={page.seoDescription}
        url={page.seoUrl}
        schema={schema}
      />

      <div className="relative overflow-hidden bg-background">
        <div
          className="absolute inset-0"
          style={{
            background: `
              radial-gradient(circle at 14% 18%, ${page.color}22, transparent 24%),
              radial-gradient(circle at 82% 12%, rgba(255,255,255,0.05), transparent 20%),
              linear-gradient(180deg, #060c15 0%, #0b1320 42%, #121a25 100%)
            `,
          }}
        />
        <section className="relative mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-28">
          <div className="max-w-4xl">
            <div className="inline-flex items-center gap-3 rounded-full border border-gold/20 bg-gold/[0.06] px-4 py-2 text-xs uppercase tracking-[0.28em] text-gold/80">
              <span style={{ color: page.color }}>{page.icon}</span>
              <span>Public Vedic Report Preview</span>
            </div>
            <div
              className="mt-8 grid h-20 w-20 place-items-center rounded-[28px] border text-4xl shadow-[0_20px_40px_rgba(0,0,0,0.18)]"
              style={{ background: `${page.color}24`, color: page.color, borderColor: `${page.color}55` }}
            >
              {page.icon}
            </div>
            <h1 className="mt-8 max-w-3xl font-playfair text-5xl font-semibold leading-tight text-white sm:text-6xl">
              {page.hook}
            </h1>
            <p className="mt-6 max-w-3xl text-lg leading-8 text-white/72">{page.description}</p>
            <div className="mt-10 flex flex-wrap gap-4">
              <AccentButton href="/reports" color={page.color}>
                <span>{`Generate My ${page.name}`}</span>
                <ArrowRight className="h-4 w-4" />
              </AccentButton>
              <OutlineButton onClick={scrollToSample} color={page.color}>
                See Sample Report
              </OutlineButton>
            </div>
          </div>
        </section>
      </div>

      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="mb-10 flex items-end justify-between gap-6">
          <div>
            <p className="text-xs uppercase tracking-[0.26em] text-gold/80">What This Report Reveals</p>
            <h2 className="mt-3 font-playfair text-4xl font-semibold text-foreground">Six focused lenses inside one premium reading</h2>
          </div>
        </div>
        <FeatureGrid page={page} />
      </section>

      <section className="border-y border-gold/10 bg-gold/[0.03] py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <div className="mb-10 text-center">
            <p className="text-xs uppercase tracking-[0.26em] text-gold/80">How It Works</p>
            <h2 className="mt-3 font-playfair text-4xl font-semibold text-foreground">From birth data to finished insight</h2>
          </div>
          <div className="grid gap-5 md:grid-cols-3">
            {PROCESS_STEPS.map((step) => (
              <article key={step.number} className="rounded-[24px] border border-gold/20 bg-background p-6 shadow-sm">
                <div
                  className="inline-flex h-12 w-12 items-center justify-center rounded-full text-lg font-semibold"
                  style={{ background: `${page.color}16`, color: page.color }}
                >
                  {step.number}
                </div>
                <h3 className="mt-5 font-playfair text-2xl font-semibold text-foreground">{step.title}</h3>
                <p className="mt-3 text-sm leading-7 text-muted-foreground">{step.body}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section ref={sampleRef} className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="mb-10 max-w-3xl">
          <p className="text-xs uppercase tracking-[0.26em] text-gold/80">Sample Report Preview</p>
          <h2 className="mt-3 font-playfair text-4xl font-semibold text-foreground">A preview of the structure, tone, and remedies layer</h2>
          <p className="mt-4 text-sm leading-7 text-muted-foreground">
            The full report is personalised from your chart. This preview only shows the section style and presentation pattern.
          </p>
        </div>
        <SamplePreview page={page} />
        <div className="mt-8">
          <AccentButton href="/reports" color={page.color}>
            <span>{`Generate My ${page.name}`}</span>
            <ArrowRight className="h-4 w-4" />
          </AccentButton>
        </div>
      </section>

      <section className="border-t border-gold/10 bg-background py-16">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <div className="mb-10 text-center">
            <p className="text-xs uppercase tracking-[0.26em] text-gold/80">FAQ</p>
            <h2 className="mt-3 font-playfair text-4xl font-semibold text-foreground">Questions people usually ask first</h2>
          </div>
          <div className="grid gap-4">
            {page.faqs.map((faq) => (
              <article key={faq.question} className="rounded-[22px] border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
                <div className="flex items-start gap-4">
                  <div
                    className="mt-1 inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full"
                    style={{ background: `${page.color}16`, color: page.color }}
                  >
                    <CheckCircle2 className="h-5 w-5" />
                  </div>
                  <div>
                    <h3 className="font-playfair text-2xl font-semibold text-foreground">{faq.question}</h3>
                    <p className="mt-3 text-sm leading-7 text-muted-foreground">{faq.answer}</p>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="px-4 py-16 sm:px-6 lg:px-8">
        <div
          className="mx-auto max-w-6xl rounded-[30px] border p-8 text-white shadow-[0_28px_80px_rgba(2,6,23,0.24)] sm:p-10"
          style={{
            borderColor: `${page.color}55`,
            background: `linear-gradient(135deg, ${page.color} 0%, #111827 100%)`,
          }}
        >
          <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-3xl">
              <p className="text-xs uppercase tracking-[0.28em] text-white/70">Ready when you are</p>
              <h2 className="mt-3 font-playfair text-4xl font-semibold">{`Ready to see what ${page.name} reveals for you?`}</h2>
              <p className="mt-4 text-sm leading-7 text-white/80">{page.hook}</p>
            </div>
            <AccentButton href="/reports" color="#111827">
              <span>{`Generate My ${page.name}`}</span>
              <ArrowRight className="h-4 w-4" />
            </AccentButton>
          </div>
        </div>
      </section>
    </div>
  );
}
