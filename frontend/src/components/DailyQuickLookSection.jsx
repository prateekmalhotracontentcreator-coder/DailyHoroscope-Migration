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
      <div className="flex gap-4 items-start">
        <div className="flex-shrink-0 w-24">
          <div className="w-24 h-24 rounded-xl bg-border" />
          <div className="mt-2 space-y-1.5">
            <div className="h-3.5 bg-border rounded w-16 mx-auto" />
            <div className="h-3 bg-border rounded w-20 mx-auto" />
            <div className="h-4 bg-border rounded w-12 mx-auto" />
          </div>
        </div>
        <div className="flex-1 min-w-0 space-y-2 pt-1">
          <div className="h-3 bg-border rounded w-full" />
          <div className="h-3 bg-border rounded w-11/12" />
          <div className="h-3 bg-border rounded w-10/12" />
          <div className="h-3 bg-border rounded w-9/12" />
          <div className="h-3 bg-border rounded w-8/12" />
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
                    className="group w-full text-left rounded-xl border border-border bg-card p-5 transition-all duration-300 hover:-translate-y-1 hover:border-gold/40 hover:shadow-[0_8px_30px_-5px_rgba(197,160,89,0.15)]"
                  >
                    {/* Two-column layout: symbol+caption left, quote right -- both top-aligned */}
                    <div className="flex gap-4 items-start">
                      {/* Left column: symbol image with name / dates / element below */}
                      <div className="flex-shrink-0 w-24 text-center">
                        <div
                          className="w-24 h-24 rounded-xl border border-gold/20 flex items-center justify-center text-4xl leading-none"
                          style={{ backgroundColor: 'rgba(197,160,89,0.07)' }}
                        >
                          {sign.symbol}
                        </div>
                        <div className="mt-2">
                          <p className="text-sm font-semibold font-playfair leading-tight group-hover:text-gold transition-colors">
                            {sign.name}
                          </p>
                          <p className="text-[10px] text-muted-foreground mt-0.5 leading-tight">
                            {sign.dates}
                          </p>
                          <span className={`inline-block mt-1.5 text-[9px] font-semibold uppercase tracking-wider border rounded-full px-2 py-0.5 ${es.pill}`}>
                            {sign.element}
                          </span>
                        </div>
                      </div>

                      {/* Right column: quote starts at the same top row as the symbol */}
                      <div className="flex-1 min-w-0">
                        <p className="text-sm leading-6 text-muted-foreground font-playfair italic">
                          "{sign.quote}"
                        </p>
                      </div>
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
