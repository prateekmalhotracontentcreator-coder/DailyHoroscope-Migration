import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { LoaderCircle, Sparkles, Star } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const SITE = 'https://www.everydayhoroscope.in';

const CATEGORY_STYLES = {
  all: 'border-gold/30 bg-gold/10 text-gold',
  bollywood: 'border-pink-400/30 bg-pink-500/15 text-pink-300',
  cricket: 'border-sky-400/30 bg-sky-500/15 text-sky-300',
  politics: 'border-amber-400/30 bg-amber-500/15 text-amber-300',
  business: 'border-emerald-400/30 bg-emerald-500/15 text-emerald-300',
  spiritual: 'border-violet-400/30 bg-violet-500/15 text-violet-300',
  historical: 'border-stone-400/30 bg-stone-500/15 text-stone-300',
  global: 'border-indigo-400/30 bg-indigo-500/15 text-indigo-300',
};

function formatDob(value) {
  return new Date(`${value}T12:00:00`).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

function buildSchema(items) {
  return {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: 'Celebrity Horoscopes',
    url: `${SITE}/celebrity-horoscopes`,
    description: 'Explore Vedic birth charts of celebrities, leaders, and legends.',
    mainEntity: {
      '@type': 'ItemList',
      itemListElement: items.slice(0, 20).map((item, index) => ({
        '@type': 'ListItem',
        position: index + 1,
        url: `${SITE}/celebrity-horoscopes/${item.slug}`,
        name: item.name,
      })),
    },
  };
}

export function CelebrityHubPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeCategory, setActiveCategory] = useState('all');

  useEffect(() => {
    let ignore = false;

    async function fetchCelebrities() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/celebrities`);
        if (!ignore) setItems(response.data || []);
      } catch {
        if (!ignore) {
          setItems([]);
          setError('Unable to load celebrity horoscopes right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchCelebrities();
    return () => {
      ignore = true;
    };
  }, []);

  const tabs = useMemo(() => {
    const categoryMap = new Map();
    for (const item of items) {
      if (!categoryMap.has(item.category)) {
        categoryMap.set(item.category, item.category_label);
      }
    }
    return [
      { key: 'all', label: 'All' },
      ...Array.from(categoryMap.entries()).map(([key, label]) => ({ key, label })),
    ];
  }, [items]);

  const visibleItems = useMemo(() => {
    if (activeCategory === 'all') return items;
    return items.filter((item) => item.category === activeCategory);
  }, [activeCategory, items]);

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title="Celebrity Horoscopes - Vedic Birth Charts"
        description="Explore Vedic birth charts of Bollywood stars, cricketers, politicians, and global icons. Calculated with KP Jyotish - Moon sign, Dasha, Nakshatra, and more."
        url={`${SITE}/celebrity-horoscopes`}
        schema={buildSchema(items)}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <section className="rounded-3xl border border-gold/20 bg-gradient-to-br from-gold/[0.08] via-background to-background p-8 shadow-sm">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.06] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
              <Sparkles className="h-3.5 w-3.5" />
              Public Vedic Charts
            </div>
            <h1 className="mt-4 text-3xl font-playfair font-bold text-foreground sm:text-4xl">
              Celebrity Horoscopes - Vedic Birth Charts of the Famous
            </h1>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
              Explore the Vedic birth charts of celebrities, leaders, and legends. Browse by category and open any chart to see Moon sign, Nakshatra, Dasha timeline, and key planetary placements.
            </p>
          </div>
        </section>

        <section className="mt-8">
          <div className="overflow-x-auto border-b border-gold/15">
            <div className="flex min-w-max gap-2">
              {tabs.map((tab) => {
                const active = activeCategory === tab.key;
                return (
                  <button
                    key={tab.key}
                    type="button"
                    onClick={() => setActiveCategory(tab.key)}
                    className={`border-b-2 px-4 py-3 text-sm font-medium transition ${
                      active
                        ? 'border-gold text-gold'
                        : 'border-transparent text-muted-foreground hover:text-foreground'
                    }`}
                  >
                    {tab.label}
                  </button>
                );
              })}
            </div>
          </div>

          {loading ? (
            <div className="mt-8 flex items-center justify-center rounded-2xl border border-gold/15 bg-background/80 p-10 text-muted-foreground">
              <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
              Loading celebrity charts...
            </div>
          ) : error ? (
            <div className="mt-8 rounded-2xl border border-red-400/20 bg-red-500/10 p-6 text-sm text-red-200">
              {error}
            </div>
          ) : (
            <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {visibleItems.map((item) => (
                <Link
                  key={item.slug}
                  to={`/celebrity-horoscopes/${item.slug}`}
                  className="group rounded-2xl border border-gold/20 bg-background/80 p-5 shadow-sm transition-all hover:-translate-y-0.5 hover:border-gold/40 hover:bg-gold/[0.04]"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h2 className="text-lg font-semibold text-foreground">{item.name}</h2>
                      <p className="mt-2 text-sm text-muted-foreground">{formatDob(item.dob)}</p>
                    </div>
                    <Star className="h-4 w-4 text-gold" />
                  </div>

                  <div className="mt-4">
                    <span className={`inline-flex rounded-full border px-3 py-1 text-xs font-medium ${CATEGORY_STYLES[item.category] || CATEGORY_STYLES.all}`}>
                      {item.category_label}
                    </span>
                  </div>

                  <p className="mt-4 text-sm leading-6 text-muted-foreground">
                    Born: {item.pob}
                  </p>
                  <p className="mt-2 text-xs text-muted-foreground">
                    {item.birth_time_confirmed ? `Birth time: ${item.tob}` : 'Birth time not confirmed'}
                  </p>

                  <p className="mt-5 text-sm font-semibold text-gold transition group-hover:text-gold/80">
                    View Chart
                  </p>
                </Link>
              ))}
            </div>
          )}
        </section>

        <section className="mt-12 rounded-2xl border border-gold/20 bg-gold/[0.05] p-8 text-center shadow-sm">
          <h2 className="text-2xl font-playfair font-bold text-foreground">Discover your own Vedic birth chart</h2>
          <p className="mt-3 text-sm leading-6 text-muted-foreground">
            Celebrity charts are fascinating, but your own Lagna, Dasha, and planetary timing matter far more for real-life guidance.
          </p>
          <Link
            to="/birth-chart"
            className="mt-5 inline-flex items-center justify-center rounded-lg bg-gold px-5 py-3 text-sm font-semibold text-primary-foreground transition hover:bg-gold/90"
          >
            Generate My Birth Chart
          </Link>
        </section>
      </main>

      <Footer />
    </div>
  );
}
