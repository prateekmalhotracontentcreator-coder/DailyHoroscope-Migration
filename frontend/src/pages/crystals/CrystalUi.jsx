import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { GlassCard } from '@/components/strategist/GlassCard';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';

export function CrystalPageFrame({ eyebrow, title, description, children }) {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(197,160,89,0.16),_transparent_34%),linear-gradient(180deg,_#fffdf8_0%,_#f6f0e4_38%,_#fffaf1_100%)] text-stone-900">
      <main className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
        <GlassCard className="overflow-hidden border-gold/30 bg-white/75 p-8 backdrop-blur md:p-10">
          <div className="max-w-3xl">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold/80">{eyebrow}</p>
            <h1 className="mt-4 font-playfair text-3xl font-bold text-stone-900 md:text-5xl">{title}</h1>
            <p className="mt-4 max-w-2xl text-sm leading-7 text-stone-600 md:text-base">{description}</p>
          </div>
        </GlassCard>
        <div className="mt-8 space-y-8">{children}</div>
      </main>
    </div>
  );
}

export function CrystalSection({ title, children, className = '' }) {
  return (
    <GlassCard className={`border-gold/20 bg-white/80 p-6 md:p-8 ${className}`}>
      <h2 className="font-playfair text-2xl font-semibold text-stone-900">{title}</h2>
      <div className="mt-4">{children}</div>
    </GlassCard>
  );
}

export function CrystalChip({ children }) {
  return (
    <span className="inline-flex items-center rounded-full border border-gold/25 bg-gold/10 px-3 py-1 text-xs font-medium text-stone-700">
      {children}
    </span>
  );
}

export function CrystalFaqs({ title = 'Crystal FAQs', items }) {
  return (
    <CrystalSection title={title}>
      <Accordion type="single" collapsible className="mt-2">
        {items.map((item, index) => (
          <AccordionItem key={item.question || item.q} value={`faq-${index}`} className="border-gold/10">
            <AccordionTrigger className="text-left font-semibold text-stone-900 hover:no-underline">
              {item.question || item.q}
            </AccordionTrigger>
            <AccordionContent className="text-sm leading-7 text-stone-600">
              {item.answer || item.a}
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </CrystalSection>
  );
}

export function CrystalLinkCard({ to, title, body, eyebrow, accent = 'gold' }) {
  const accentClasses = accent === 'teal'
    ? 'border-teal-300/40 bg-teal-50/70'
    : accent === 'blue'
      ? 'border-sky-300/40 bg-sky-50/70'
      : 'border-gold/30 bg-gold/10';

  return (
    <Link to={to} className="block">
      <GlassCard className={`h-full border ${accentClasses} p-5 transition-transform duration-200 hover:-translate-y-1`}>
        {eyebrow ? <p className="text-xs font-semibold uppercase tracking-[0.24em] text-stone-500">{eyebrow}</p> : null}
        <h3 className="mt-2 font-playfair text-xl font-semibold text-stone-900">{title}</h3>
        <p className="mt-3 text-sm leading-6 text-stone-600">{body}</p>
        <div className="mt-4 inline-flex items-center gap-2 text-sm font-medium text-stone-900">
          Explore
          <ArrowRight className="h-4 w-4" />
        </div>
      </GlassCard>
    </Link>
  );
}
