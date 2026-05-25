import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Sparkles } from 'lucide-react';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import LoShuGridBoard from '../../components/lo-shu/LoShuGridBoard';
import {
  ARROW_LINKS,
  buildBreadcrumbSchema,
  buildFaqSchema,
  HUB_FAQ_ITEMS,
  MISSING_NUMBER_LINKS,
  NUMBER_LINKS,
  PERSONAL_YEAR_LINKS,
  PROBLEM_LINKS,
  SITE,
} from './loShuContent';

const STATIC_COUNTS = { 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1 };

function buildSchema() {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebPage',
        name: 'Lo Shu Grid - Chinese Numerology Birth Chart Explained',
        url: `${SITE}/lo-shu-grid`,
        description: 'Discover the Lo Shu Grid, its missing numbers, active arrows, and the personal chart patterns hidden in your date of birth and name.',
      },
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Lo Shu Grid', url: `${SITE}/lo-shu-grid` },
      ]),
      buildFaqSchema(HUB_FAQ_ITEMS),
    ],
  };
}

export default function LoShuHubPage() {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.16),transparent_28%),linear-gradient(180deg,hsl(var(--background))_0%,rgba(197,160,89,0.04)_100%)] text-foreground">
      <SEO
        title="Lo Shu Grid - Chinese Numerology Calculator and Missing Numbers"
        description="Discover your Lo Shu Grid birth chart. Calculate missing numbers, active arrows, and what this Chinese numerology pattern reveals about your personality and path."
        url={`${SITE}/lo-shu-grid`}
        schema={buildSchema()}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <section className="grid gap-8 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.22em] text-gold">
              <Sparkles className="h-3.5 w-3.5" />
              Chinese Numerology
            </div>
            <h1 className="mt-6 max-w-3xl font-playfair text-4xl font-semibold leading-tight sm:text-5xl">
              Lo Shu Grid - Chinese Numerology Birth Chart Explained
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-8 text-muted-foreground">
              The Lo Shu Grid is a 3x3 numerology map built from your birth date and supporting number values. It highlights which energies are naturally active, which ones are missing, and which arrows form stronger themes in the way you think, feel, and act.
            </p>
            <p className="mt-4 max-w-2xl text-base leading-8 text-muted-foreground">
              This module combines the grid layout, missing number interpretations, and arrow analysis into one public learning hub, then lets you calculate your own personal chart in seconds.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                to="/lo-shu-grid/calculator"
                className="inline-flex items-center gap-2 rounded-full bg-gold px-6 py-3 text-sm font-semibold text-primary-foreground transition hover:opacity-90"
              >
                Generate Your Lo Shu Grid
                <ArrowRight className="h-4 w-4" />
              </Link>
              <a
                href="#missing-numbers"
                className="inline-flex items-center rounded-full border border-gold/20 bg-card/60 px-6 py-3 text-sm font-semibold text-foreground transition hover:border-gold/40"
              >
                Explore Missing Numbers
              </a>
            </div>
          </div>

          <div className="rounded-[2rem] border border-gold/20 bg-card/70 p-6 shadow-sm backdrop-blur">
            <LoShuGridBoard
              counts={STATIC_COUNTS}
              caption="Every Lo Shu chart uses the same number layout. What changes from person to person is which cells are active, repeated, or missing."
            />
          </div>
        </section>

        <section className="mt-10 rounded-[2rem] border border-gold/20 bg-gold/[0.04] p-8 shadow-sm">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Calculator</p>
              <h2 className="mt-2 font-playfair text-2xl font-semibold">Generate your personal Lo Shu pattern</h2>
              <p className="mt-3 max-w-3xl text-sm leading-7 text-muted-foreground">
                Enter your full name, date of birth, and gender to calculate the grid, identify missing numbers, detect active arrows, and see whether a Rajayoga diagonal is present.
              </p>
            </div>
            <Link
              to="/lo-shu-grid/calculator"
              className="inline-flex w-fit items-center gap-2 rounded-full border border-gold/30 bg-card/80 px-5 py-3 text-sm font-semibold text-gold transition hover:border-gold/50"
            >
              Open Calculator
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </section>

        <section className="mt-12">
          <div className="grid gap-6 md:grid-cols-3">
            {[
              {
                title: 'How the grid is built',
                body: 'The chart starts with your birth-date digits and then adds the Destiny, Kua, and name numbers. Each digit from 1 to 9 is checked against the fixed Lo Shu square.',
              },
              {
                title: 'What missing numbers show',
                body: 'A missing number usually marks a trait that grows more through repetition and awareness. It can affect confidence, structure, intuition, endurance, communication, or emotional balance.',
              },
              {
                title: 'Why arrows matter',
                body: 'Arrows are complete lines inside the grid. They compress three numbers into one stronger theme, such as intellect, action, spirituality, prosperity, or determination.',
              },
            ].map((item) => (
              <article key={item.title} className="rounded-[1.75rem] border border-gold/15 bg-card/75 p-6 shadow-sm">
                <h2 className="font-playfair text-xl font-semibold">{item.title}</h2>
                <p className="mt-3 text-sm leading-7 text-muted-foreground">{item.body}</p>
              </article>
            ))}
          </div>
        </section>

        <section id="missing-numbers" className="mt-12 rounded-[2rem] border border-gold/20 bg-card/75 p-8 shadow-sm">
          <h2 className="font-playfair text-3xl font-semibold">What does a missing number mean?</h2>
          <p className="mt-4 max-w-4xl text-sm leading-7 text-muted-foreground">
            In Lo Shu numerology, a missing number does not mean weakness forever. It usually points to an area that needs deliberate cultivation, stronger habits, or more self-awareness. Each number also carries a planetary tone that can guide simple balancing remedies.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            {MISSING_NUMBER_LINKS.map((item) => (
              <Link
                key={item.number}
                to={item.href}
                className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-primary-foreground"
              >
                {item.label}
              </Link>
            ))}
          </div>
        </section>

        <section className="mt-12 rounded-[2rem] border border-gold/20 bg-card/75 p-8 shadow-sm">
          <h2 className="font-playfair text-3xl font-semibold">Explore the meaning of each number when it is present</h2>
          <p className="mt-4 max-w-4xl text-sm leading-7 text-muted-foreground">
            These deep-dive pages focus on what each number adds to the grid when it appears, how repetition changes its expression, and what to watch if that energy becomes excessive.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            {NUMBER_LINKS.map((item) => (
              <Link
                key={item.number}
                to={item.href}
                className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-primary-foreground"
              >
                {item.label}
              </Link>
            ))}
          </div>
        </section>

        <section className="mt-12 rounded-[2rem] border border-gold/20 bg-card/75 p-8 shadow-sm">
          <h2 className="font-playfair text-3xl font-semibold">What are Lo Shu arrows?</h2>
          <p className="mt-4 max-w-4xl text-sm leading-7 text-muted-foreground">
            Arrows are full rows, columns, or diagonals that activate when all three numbers in that line appear in the chart. Some arrows show mental sharpness or planning ability, while the two diagonals are highlighted as Rajayoga patterns in the decoded source.
          </p>
          <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {ARROW_LINKS.map((arrow) => (
              <Link
                key={arrow.slug}
                to={`/lo-shu-grid/arrow/${arrow.slug}`}
                className="rounded-[1.5rem] border border-gold/15 bg-gold/[0.04] p-5 transition hover:-translate-y-0.5 hover:border-gold/30 hover:shadow-sm"
              >
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">{arrow.theme}</p>
                <h3 className="mt-3 font-playfair text-xl font-semibold">{arrow.name}</h3>
                <p className="mt-3 text-sm text-muted-foreground">{arrow.numbers.join(' - ')}</p>
              </Link>
            ))}
          </div>
        </section>

        <section className="mt-12 grid gap-6 lg:grid-cols-2">
          <article className="rounded-[2rem] border border-gold/20 bg-card/75 p-8 shadow-sm">
            <h2 className="font-playfair text-3xl font-semibold">Lo Shu pages for life problems</h2>
            <p className="mt-4 text-sm leading-7 text-muted-foreground">
              Explore focused remedy pages for career, money, relationships, health, family, fertility, legal issues, and other recurring life themes decoded from the source material.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              {PROBLEM_LINKS.map((item) => (
                <Link
                  key={item.slug}
                  to={`/lo-shu-grid/for/${item.slug}`}
                  className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-primary-foreground"
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </article>

          <article className="rounded-[2rem] border border-gold/20 bg-card/75 p-8 shadow-sm">
            <h2 className="font-playfair text-3xl font-semibold">Personal Year meanings</h2>
            <p className="mt-4 text-sm leading-7 text-muted-foreground">
              Learn what each Personal Year from 1 to 9 tends to emphasize, where the opportunities live, and how to work with the cycle instead of against it.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              {PERSONAL_YEAR_LINKS.map((item) => (
                <Link
                  key={item.number}
                  to={item.href}
                  className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-primary-foreground"
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </article>
        </section>

        <section className="mt-12 rounded-[2rem] border border-gold/20 bg-card/75 p-8 shadow-sm">
          <h2 className="font-playfair text-3xl font-semibold">Frequently asked questions</h2>
          <Accordion type="single" collapsible className="mt-5">
            {HUB_FAQ_ITEMS.map((item, index) => (
              <AccordionItem key={item.question} value={`faq-${index}`} className="border-gold/10">
                <AccordionTrigger className="text-left font-semibold text-foreground hover:no-underline">
                  {item.question}
                </AccordionTrigger>
                <AccordionContent className="text-sm leading-7 text-muted-foreground">
                  {item.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </section>
      </main>

      <Footer />
    </div>
  );
}
