import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Zap } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const ELEMENT_STYLES = {
  Fire:  { pill: 'text-orange-400 border-orange-400/30 bg-orange-400/8' },
  Earth: { pill: 'text-emerald-400 border-emerald-400/30 bg-emerald-400/8' },
  Air:   { pill: 'text-sky-400 border-sky-400/30 bg-sky-400/8' },
  Water: { pill: 'text-blue-400 border-blue-400/30 bg-blue-400/8' },
};

function SkeletonCard() {
  return (
    <div className="rounded-xl border border-border bg-card p-5 animate-pulse">
      <div className="overflow-hidden">
        <div className="float-left mr-4 mb-2 w-24 h-24 rounded-xl bg-border" />
        <div className="space-y-2 pt-1">
          <div className="h-4 bg-border rounded w-24" />
          <div className="h-3 bg-border rounded w-32" />
          <div className="h-5 bg-border rounded w-14" />
        </div>
        <div className="space-y-2 mt-3">
          <div className="h-3 bg-border rounded w-full" />
          <div className="h-3 bg-border rounded w-11/12" />
          <div className="h-3 bg-border rounded w-10/12" />
          <div className="h-3 bg-border rounded w-9/12" />
        </div>
      </div>
    </div>
  );
}

export function DailyQuickLookSection() {
  const navigate = useNavigate();
  const [quotes, setQuotes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const res = await fetch(`${BACKEND_URL}/api/horoscope/daily/quotes`);
        if (!res.ok) throw new Error('fetch failed');
        const data = await res.json();
        if (!cancelled) setQuotes(data);
      } catch {
        // silently fail -- section stays hidden
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => { cancelled = true; };
  }, []);

  if (!loading && quotes.length === 0) return null;

  return (
    <section className="py-20 px-4 border-t border-border/50">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 text-gold text-xs font-semibold uppercase tracking-[0.2em] mb-4">
            <Zap className="h-3 w-3" /> Daily Quick Look
          </div>
          <h2 className="font-playfair text-3xl md:text-4xl font-semibold mb-3">
            Today's energy for every sign
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto text-sm leading-relaxed">
            A cosmic mood for each sign, drawn from today's Vedic daily horoscope.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {loading
            ? Array.from({ length: 12 }).map((_, i) => <SkeletonCard key={i} />)
            : quotes.map((sign) => {
                const es = ELEMENT_STYLES[sign.element] || ELEMENT_STYLES.Air;
                return (
                  <button
                    key={sign.id}
                    type="button"
                    onClick={() => navigate(`/horoscope/daily/${sign.id}`)}
                    className="group text-left rounded-xl border border-border bg-card p-5 transition-all duration-300 hover:-translate-y-1 hover:border-gold/40 hover:shadow-[0_8px_30px_-5px_rgba(197,160,89,0.15)]"
                  >
                    {/*
                      Newspaper L-shape: symbol (96 px) floated top-left.
                      Header text fills the ~60 px to its right, then the quote
                      starts while the symbol is still floating -- so the first
                      line(s) of the quote wrap alongside the symbol's lower
                      portion before spanning full width below it.
                    */}
                    <div className="overflow-hidden">
                      <div className="float-left mr-4 mb-2">
                        <div
                          className="w-24 h-24 rounded-xl border border-gold/20 flex items-center justify-center text-4xl leading-none"
                          style={{ backgroundColor: 'rgba(197,160,89,0.07)' }}
                        >
                          {sign.symbol}
                        </div>
                      </div>

                      {/* Header block: shorter than 96 px so quote wraps alongside symbol bottom */}
                      <div className="mb-2">
                        <p className="text-base font-semibold font-playfair leading-tight group-hover:text-gold transition-colors">
                          {sign.name}
                        </p>
                        <p className="text-[11px] text-muted-foreground mt-1 leading-tight">
                          {sign.dates}
                        </p>
                        <span className={`inline-block mt-2 text-[9px] font-semibold uppercase tracking-wider border rounded-full px-2 py-0.5 ${es.pill}`}>
                          {sign.element}
                        </span>
                      </div>

                      {/* Quote is inside the BFC so it flows around the float -- L-shape */}
                      <p className="text-sm leading-6 text-muted-foreground font-playfair italic">
                        "{sign.quote}"
                      </p>
                    </div>

                    <div className="flex items-center gap-1 text-gold text-[10px] font-semibold uppercase tracking-wider mt-3 opacity-0 group-hover:opacity-100 transition-opacity">
                      Full reading <ArrowRight className="h-3 w-3 group-hover:translate-x-0.5 transition-transform" />
                    </div>
                  </button>
                );
              })}
        </div>

        <div className="mt-10 text-center">
          <button
            type="button"
            onClick={() => navigate('/horoscope/daily')}
            className="inline-flex items-center gap-2 border border-gold/30 hover:border-gold text-gold text-sm font-semibold px-6 py-3 rounded-sm transition-all hover:-translate-y-0.5 hover:bg-gold/5"
          >
            View All 12 Daily Horoscopes <ArrowRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </section>
  );
}
