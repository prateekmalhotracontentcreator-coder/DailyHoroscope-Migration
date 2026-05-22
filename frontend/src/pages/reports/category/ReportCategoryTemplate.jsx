import React from 'react';
import { Link } from 'react-router-dom';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../../components/ui/accordion';
import { Footer } from '../../../components/Footer';
import { SEO } from '../../../components/SEO';
import { CATEGORY_STEPS, REPORT_CATEGORY_DATA, buildCategorySchema } from './reportCategoryData';

const BADGE_CLASSES = {
  'Most Popular': 'border border-gold/30 bg-gold/15 text-gold',
  Premium: 'border border-purple-400/30 bg-purple-500/15 text-purple-500',
  Free: 'border border-sky-400/30 bg-sky-500/10 text-sky-600',
};

export function ReportCategoryTemplate({ categoryKey }) {
  const config = REPORT_CATEGORY_DATA[categoryKey];

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,rgba(201,150,31,0.16),transparent_26%),linear-gradient(180deg,#fcfaf5_0%,#f6efe3_60%,#eee5d3_100%)] text-stone-900">
      <SEO
        title={config.seoTitle}
        description={config.metaDescription}
        url={`https://www.everydayhoroscope.in${config.route}`}
        schema={buildCategorySchema(config)}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <section className="rounded-[2rem] border border-gold/20 bg-white/75 p-8 shadow-sm backdrop-blur sm:p-10">
          <div className="max-w-3xl">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Premium Discovery Page</p>
            <h1 className="mt-4 font-cinzel text-4xl font-semibold tracking-tight text-stone-900 sm:text-5xl">
              {config.title}
            </h1>
            <p className="mt-4 max-w-2xl text-sm leading-7 text-stone-600">{config.description}</p>
            <div className="mt-6 flex flex-wrap gap-3">
              <Link
                to={config.primaryCta.href}
                className="rounded-full bg-gold px-5 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90"
              >
                {config.primaryCta.label}
              </Link>
              <Link
                to="/premium-reports"
                className="rounded-full border border-gold/30 px-5 py-3 text-sm font-semibold text-gold transition hover:bg-gold/10"
              >
                View all premium reports
              </Link>
            </div>
          </div>
        </section>

        <section className="mt-8">
          <h2 className="font-playfair text-2xl font-semibold text-stone-900">What you will discover</h2>
          <div className="mt-5 grid gap-5 md:grid-cols-3">
            {config.discover.map((item) => (
              <article key={item.title} className="rounded-[1.5rem] border border-gold/15 bg-white/80 p-6 shadow-sm">
                <h3 className="font-playfair text-xl font-semibold text-stone-900">{item.title}</h3>
                <p className="mt-3 text-sm leading-7 text-stone-600">{item.body}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="mt-8">
          <div className="flex flex-col gap-2">
            <h2 className="font-playfair text-2xl font-semibold text-stone-900">Reports in this category</h2>
            <p className="text-sm text-stone-600">Choose the lens that matches the question you actually want answered.</p>
          </div>
          <div className="mt-5 grid gap-5 lg:grid-cols-2">
            {config.reports.map((report) => (
              <article key={report.name} className="rounded-[1.75rem] border border-gold/15 bg-white/82 p-6 shadow-sm">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <h3 className="font-playfair text-2xl font-semibold text-stone-900">{report.name}</h3>
                    <p className="mt-3 max-w-2xl text-sm leading-7 text-stone-600">{report.description}</p>
                  </div>
                  <span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] ${BADGE_CLASSES[report.badge] || BADGE_CLASSES.Premium}`}>
                    {report.badge}
                  </span>
                </div>
                <div className="mt-5">
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">What it reveals</p>
                  <ul className="mt-3 space-y-2 text-sm leading-7 text-stone-600">
                    {report.reveals.map((point) => (
                      <li key={point} className="flex gap-3">
                        <span className="font-semibold text-gold">-</span>
                        <span>{point}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <Link
                  to={report.route}
                  className="mt-6 inline-flex rounded-full bg-gold px-4 py-2 text-sm font-semibold text-stone-950 transition hover:opacity-90"
                >
                  Get this report
                </Link>
              </article>
            ))}
          </div>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/82 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold text-stone-900">How it works</h2>
          <div className="mt-5 grid gap-5 md:grid-cols-3">
            {CATEGORY_STEPS.map((step) => (
              <article key={step.number} className="rounded-[1.5rem] border border-gold/15 bg-gold/5 p-5">
                <p className="font-cinzel text-3xl text-gold">{step.number}</p>
                <h3 className="mt-3 font-playfair text-xl font-semibold text-stone-900">{step.title}</h3>
                <p className="mt-3 text-sm leading-7 text-stone-600">{step.body}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/82 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold text-stone-900">Frequently asked questions</h2>
          <Accordion type="single" collapsible className="mt-4">
            {config.faq.map((item) => (
              <AccordionItem key={item.question} value={item.question}>
                <AccordionTrigger className="text-left text-base font-semibold text-stone-900">
                  {item.question}
                </AccordionTrigger>
                <AccordionContent className="text-sm leading-7 text-stone-600">
                  {item.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/82 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold text-stone-900">Related categories</h2>
          <div className="mt-5 flex flex-wrap gap-3">
            {config.related.map((key) => {
              const related = REPORT_CATEGORY_DATA[key];
              return (
                <Link
                  key={related.slug}
                  to={related.route}
                  className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-stone-950"
                >
                  {related.title}
                </Link>
              );
            })}
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
