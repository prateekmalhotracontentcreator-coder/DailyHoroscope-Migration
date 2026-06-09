import React, { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, ChevronDown, ChevronUp } from 'lucide-react';

import { SEO } from '../SEO';
import { Footer } from '../Footer';

const glassCardClass = 'rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm';

function FaqItem({ item, accentColor }) {
  const [open, setOpen] = useState(false);

  return (
    <div className={`${glassCardClass} overflow-hidden`}>
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="flex w-full items-center justify-between gap-4 px-5 py-4 text-left"
      >
        <span className="text-sm font-semibold text-foreground">{item.q}</span>
        {open ? (
          <ChevronUp className="h-4 w-4 shrink-0" style={{ color: accentColor }} />
        ) : (
          <ChevronDown className="h-4 w-4 shrink-0" style={{ color: accentColor }} />
        )}
      </button>
      {open && (
        <div className="border-t border-gold/10 px-5 py-4 text-sm leading-7 text-muted-foreground">
          {item.a}
        </div>
      )}
    </div>
  );
}

function PreviewFrame({ preview, accentColor }) {
  return (
    <div className={`relative overflow-hidden ${glassCardClass} p-6`}>
      {preview.tabs?.length ? (
        <div className="mb-5 flex flex-wrap gap-2">
          {preview.tabs.map((tab) => (
            <span
              key={tab}
              className="rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em]"
              style={{ borderColor: `${accentColor}55`, color: accentColor }}
            >
              {tab}
            </span>
          ))}
        </div>
      ) : null}

      {preview.columns?.length ? (
        <div className="grid gap-3 text-xs font-semibold uppercase tracking-[0.18em] text-muted-foreground" style={{ gridTemplateColumns: `repeat(${preview.columns.length}, minmax(0, 1fr))` }}>
          {preview.columns.map((column) => (
            <div key={column} className="border-b border-gold/10 pb-2">
              {column}
            </div>
          ))}
        </div>
      ) : null}

      {preview.rows?.length ? (
        <div className="mt-4 space-y-3 blur-[2px] select-none">
          {preview.rows.map((row, rowIndex) => (
            <div
              key={`${preview.title}-row-${rowIndex}`}
              className="grid gap-3 rounded-lg border border-gold/10 bg-background/40 px-3 py-3 text-sm text-foreground/80"
              style={{ gridTemplateColumns: `repeat(${row.length}, minmax(0, 1fr))` }}
            >
              {row.map((cell, cellIndex) => (
                <div key={`${preview.title}-cell-${rowIndex}-${cellIndex}`}>{cell}</div>
              ))}
            </div>
          ))}
        </div>
      ) : null}

      {preview.cards?.length ? (
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3 blur-[2px] select-none">
          {preview.cards.map((card) => (
            <div key={card.title} className="rounded-lg border border-gold/10 bg-background/50 p-4">
              <p className="text-sm font-semibold text-foreground">{card.title}</p>
              <p className="mt-2 text-xs leading-6 text-muted-foreground">{card.body}</p>
            </div>
          ))}
        </div>
      ) : null}

      {preview.lines?.length ? (
        <div className="mt-4 space-y-3 blur-[2px] select-none">
          {preview.lines.map((line) => (
            <div key={line.label} className="rounded-lg border border-gold/10 bg-background/45 px-4 py-3">
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-muted-foreground">{line.label}</p>
              <p className="mt-2 text-sm leading-6 text-foreground/80">{line.value}</p>
            </div>
          ))}
        </div>
      ) : null}

      <div className="absolute inset-x-0 bottom-0 top-0 flex items-center justify-center bg-gradient-to-t from-background via-background/50 to-transparent">
        <div
          className="rounded-full border px-5 py-3 text-sm font-semibold shadow-lg"
          style={{ borderColor: `${accentColor}66`, backgroundColor: `${accentColor}18`, color: accentColor }}
        >
          {preview.overlay}
        </div>
      </div>
    </div>
  );
}

export default function ModuleLandingPage({ config }) {
  const navigate = useNavigate();

  const schema = useMemo(() => ({
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: config.faqs.map((item) => ({
      '@type': 'Question',
      name: item.q,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.a,
      },
    })),
  }), [config.faqs]);

  const backgroundImage = `radial-gradient(circle at top left, ${config.accentColor}20, transparent 30%), radial-gradient(circle at bottom right, ${config.accentColor}14, transparent 34%), linear-gradient(180deg, rgba(10,10,10,0.98) 0%, rgba(16,16,16,0.96) 55%, rgba(10,10,10,1) 100%)`;

  return (
    <div className="min-h-screen bg-background text-foreground" style={{ backgroundImage }}>
      <SEO
        title={config.seo.title}
        description={config.seo.description}
        url={config.seo.url}
        schema={schema}
      />

      <main>
        <section className="mx-auto max-w-6xl px-4 py-20 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-4xl text-center">
            <div className="inline-flex items-center gap-3 rounded-full border border-gold/20 bg-gold/[0.04] px-5 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
              <span style={{ color: config.accentColor }}>{config.icon}</span>
              <span>{config.badge}</span>
            </div>
            <h1 className="mt-8 font-playfair text-4xl font-semibold leading-tight sm:text-5xl lg:text-6xl">
              {config.headline}
            </h1>
            <p className="mx-auto mt-6 max-w-3xl text-base leading-8 text-muted-foreground sm:text-lg">
              {config.subline}
            </p>
            <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <button
                type="button"
                onClick={() => navigate(config.primaryCta.href)}
                className="inline-flex items-center gap-2 rounded-full px-7 py-4 text-sm font-semibold text-background transition hover:opacity-90"
                style={{ backgroundColor: config.accentColor }}
              >
                {config.primaryCta.label}
                <ArrowRight className="h-4 w-4" />
              </button>
              <button
                type="button"
                onClick={() => document.getElementById('features-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' })}
                className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.04] px-7 py-4 text-sm font-semibold text-foreground transition hover:bg-gold/[0.08]"
              >
                {config.secondaryCta.label}
              </button>
            </div>
          </div>
        </section>

        <section id="features-section" className="mx-auto max-w-6xl px-4 py-6 sm:px-6 lg:px-8">
          <div className="mb-10 text-center">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">What You Get</p>
            <h2 className="mt-3 font-playfair text-3xl font-semibold">Six ways this module becomes useful immediately.</h2>
          </div>
          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
            {config.features.map((feature) => (
              <div key={feature.title} className={`${glassCardClass} p-6`}>
                <div
                  className="inline-flex h-11 w-11 items-center justify-center rounded-full border text-xl"
                  style={{ borderColor: `${config.accentColor}55`, color: config.accentColor, backgroundColor: `${config.accentColor}12` }}
                >
                  {feature.icon || config.icon}
                </div>
                <h3 className="mt-4 font-playfair text-xl font-semibold">{feature.title}</h3>
                <p className="mt-3 text-sm leading-7 text-muted-foreground">{feature.body}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6 lg:px-8">
          <div className="mb-10 text-center">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">How It Works</p>
            <h2 className="mt-3 font-playfair text-3xl font-semibold">Three simple steps from curiosity to insight.</h2>
          </div>
          <div className="grid gap-6 md:grid-cols-3">
            {config.steps.map((step, index) => (
              <div key={step.title} className={`${glassCardClass} p-6`}>
                <div
                  className="inline-flex h-11 w-11 items-center justify-center rounded-full text-sm font-semibold"
                  style={{ backgroundColor: `${config.accentColor}18`, color: config.accentColor }}
                >
                  {String(index + 1).padStart(2, '0')}
                </div>
                <h3 className="mt-4 font-playfair text-xl font-semibold">{step.title}</h3>
                <p className="mt-3 text-sm leading-7 text-muted-foreground">{step.body}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="mx-auto max-w-6xl px-4 py-4 sm:px-6 lg:px-8">
          <div className="mb-10 text-center">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Preview</p>
            <h2 className="mt-3 font-playfair text-3xl font-semibold">{config.preview.title}</h2>
            <p className="mx-auto mt-3 max-w-2xl text-sm leading-7 text-muted-foreground">{config.preview.subtitle}</p>
          </div>
          <PreviewFrame preview={config.preview} accentColor={config.accentColor} />
        </section>

        <section className="mx-auto max-w-4xl px-4 py-16 sm:px-6 lg:px-8">
          <div className="mb-10 text-center">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">FAQ</p>
            <h2 className="mt-3 font-playfair text-3xl font-semibold">Three questions people ask before they click.</h2>
          </div>
          <div className="space-y-4">
            {config.faqs.map((item) => (
              <FaqItem key={item.q} item={item} accentColor={config.accentColor} />
            ))}
          </div>
        </section>

        <section className="mx-auto max-w-6xl px-4 pb-10 pt-4 sm:px-6 lg:px-8">
          <div className={`${glassCardClass} px-6 py-10 text-center sm:px-10`}>
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">{config.banner.kicker}</p>
            <h2 className="mt-4 font-playfair text-3xl font-semibold">{config.banner.title}</h2>
            <p className="mx-auto mt-4 max-w-3xl text-sm leading-7 text-muted-foreground">{config.banner.body}</p>
            <button
              type="button"
              onClick={() => navigate(config.primaryCta.href)}
              className="mt-8 inline-flex items-center gap-2 rounded-full px-7 py-4 text-sm font-semibold text-background transition hover:opacity-90"
              style={{ backgroundColor: config.accentColor }}
            >
              {config.banner.ctaLabel || config.primaryCta.label}
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
