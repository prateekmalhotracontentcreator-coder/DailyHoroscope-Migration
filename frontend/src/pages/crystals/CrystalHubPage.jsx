import React, { useDeferredValue, useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Compass, Gem, LoaderCircle, Search, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { buildBreadcrumbSchema, buildFaqSchema, HUB_FAQS, API, SITE } from './crystalShared';
import { CrystalChip, CrystalFaqs, CrystalLinkCard, CrystalPageFrame, CrystalSection } from './CrystalUi';

export function CrystalHubPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [chakra, setChakra] = useState('');
  const [element, setElement] = useState('');
  const [planet, setPlanet] = useState('');
  const deferredSearch = useDeferredValue(search);

  useEffect(() => {
    let ignore = false;
    async function fetchHub() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/list`);
        if (!ignore) {
          setData(response.data);
        }
      } catch (err) {
        if (!ignore) {
          setError(err?.response?.data?.detail || 'Unable to load the crystal hub right now.');
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    fetchHub();
    return () => {
      ignore = true;
    };
  }, []);

  const crystals = (data?.crystals || []).filter((item) => {
    const matchesSearch = !deferredSearch.trim() || `${item.display_name} ${item.tagline}`.toLowerCase().includes(deferredSearch.trim().toLowerCase());
    const matchesChakra = !chakra || item.chakras.includes(chakra);
    const matchesElement = !element || item.element === element;
    const matchesPlanet = !planet || item.planet === planet;
    return matchesSearch && matchesChakra && matchesElement && matchesPlanet;
  });

  const schema = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebPage',
        name: 'Crystal Healing - Stones for Every Intention',
        description: 'Explore crystal meanings, intention-based crystal guides, and a birth-chart crystal calculator.',
        url: `${SITE}/crystals`,
      },
      buildFaqSchema(HUB_FAQS),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Crystals', url: `${SITE}/crystals` },
      ]),
    ],
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(197,160,89,0.18),_transparent_30%),linear-gradient(180deg,_#fffdf8_0%,_#f4eddf_44%,_#fffaf2_100%)]">
      <SEO
        title="Crystal Healing - Stones for Every Intention"
        description="Explore crystal meanings, healing properties, intention guides, and a birth-chart crystal recommendation calculator."
        canonical={`${SITE}/crystals`}
        jsonLd={schema}
      />

      <CrystalPageFrame
        eyebrow="Crystal Healing Hub"
        title="Crystal Healing - Stones for Every Intention"
        description="Explore the energy of 50 widely loved crystals, move by intention, and use the calculator when you want a Vedic birth-chart layer added to your recommendation. This hub is built for both curious beginners and people who already work with stones as part of a steady practice."
      >
        <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <CrystalSection title="How This Hub Works">
            <div className="space-y-4 text-sm leading-7 text-stone-600">
              <p>Crystal healing is usually practiced as a ritual of attention, symbolism, and emotional alignment. Different stones are traditionally chosen for different intentions, such as protection, calm, confidence, communication, sleep, and spiritual growth.</p>
              <p>This hub helps you browse in three ways: by individual crystal, by life intention, or by a birth-chart-based calculator that layers in active dasha themes and softer support stones.</p>
            </div>
            <div className="mt-5 flex flex-wrap gap-2">
              <CrystalChip>50 crystal pages</CrystalChip>
              <CrystalChip>20 intention guides</CrystalChip>
              <CrystalChip>Birth-chart calculator</CrystalChip>
            </div>
          </CrystalSection>

          <CrystalLinkCard
            to="/crystals/calculator"
            eyebrow="Personalized Path"
            title="Find Your Crystal by Birth Chart"
            body="Get one primary Vedic gemstone plus softer support crystals based on your chart and the life theme you want to work on now."
          />
        </div>

        <CrystalSection title="Browse by Intention">
          <div className="flex flex-wrap gap-3">
            {(data?.intentions || []).map((item) => (
              <Link
                key={item.slug}
                to={`/crystals/for/${item.slug}`}
                className="inline-flex items-center rounded-full border border-gold/25 bg-white/80 px-4 py-2 text-sm font-medium text-stone-700 transition hover:border-gold/45 hover:bg-gold/10"
              >
                {item.display}
              </Link>
            ))}
          </div>
        </CrystalSection>

        <CrystalSection title="Crystal Grid">
          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            <label className="relative block">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-stone-400" />
              <input
                type="text"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Search crystals"
                className="w-full rounded-xl border border-gold/20 bg-white px-10 py-3 text-sm text-stone-700 outline-none transition focus:border-gold/50"
              />
            </label>
            <select value={chakra} onChange={(event) => setChakra(event.target.value)} className="rounded-xl border border-gold/20 bg-white px-4 py-3 text-sm text-stone-700 outline-none focus:border-gold/50">
              <option value="">All chakras</option>
              {(data?.filters?.chakras || []).map((item) => <option key={item} value={item}>{item}</option>)}
            </select>
            <select value={element} onChange={(event) => setElement(event.target.value)} className="rounded-xl border border-gold/20 bg-white px-4 py-3 text-sm text-stone-700 outline-none focus:border-gold/50">
              <option value="">All elements</option>
              {(data?.filters?.elements || []).map((item) => <option key={item} value={item}>{item}</option>)}
            </select>
            <select value={planet} onChange={(event) => setPlanet(event.target.value)} className="rounded-xl border border-gold/20 bg-white px-4 py-3 text-sm text-stone-700 outline-none focus:border-gold/50">
              <option value="">All planet links</option>
              {(data?.filters?.planets || []).map((item) => <option key={item} value={item}>{item}</option>)}
            </select>
          </div>

          {loading ? (
            <div className="mt-6 flex items-center justify-center rounded-2xl border border-gold/15 bg-white/70 p-12 text-stone-500">
              <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
              Loading crystal library...
            </div>
          ) : error ? (
            <div className="mt-6 rounded-2xl border border-red-300/40 bg-red-50 p-6 text-sm text-red-700">{error}</div>
          ) : (
            <>
              <div className="mt-5 flex items-center justify-between gap-4">
                <p className="text-sm text-stone-500">{crystals.length} crystal{crystals.length === 1 ? '' : 's'} matched</p>
                {(search || chakra || element || planet) ? (
                  <button onClick={() => { setSearch(''); setChakra(''); setElement(''); setPlanet(''); }} className="text-sm font-medium text-stone-700 underline decoration-gold/60 underline-offset-4">
                    Reset filters
                  </button>
                ) : null}
              </div>

              <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                {crystals.map((item) => (
                  <Link key={item.slug} to={`/crystals/${item.slug}`} className="group block">
                    <div className="h-full rounded-2xl border border-gold/20 bg-white/85 p-5 shadow-sm transition duration-200 group-hover:-translate-y-1 group-hover:border-gold/40">
                      <div className="flex items-center justify-between gap-3">
                        <div className="inline-flex items-center gap-2 rounded-full bg-gold/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.22em] text-gold">
                          <Gem className="h-3.5 w-3.5" />
                          {item.color}
                        </div>
                        <Sparkles className="h-4 w-4 text-gold/60" />
                      </div>
                      <h3 className="mt-4 font-playfair text-2xl font-semibold text-stone-900">{item.display_name}</h3>
                      <p className="mt-3 text-sm leading-6 text-stone-600">{item.tagline}</p>
                      <div className="mt-4 flex flex-wrap gap-2">
                        {item.chakras.slice(0, 2).map((entry) => <CrystalChip key={entry}>{entry}</CrystalChip>)}
                        <CrystalChip>{item.element}</CrystalChip>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </>
          )}
        </CrystalSection>

        <div className="grid gap-6 lg:grid-cols-2">
          <CrystalLinkCard
            to="/crystals/for/protection"
            eyebrow="Popular Intention"
            title="Protection & Grounding"
            body="Start with dense, shielding stones when life feels noisy, draining, or emotionally uncontained."
            accent="teal"
          />
          <CrystalLinkCard
            to="/crystals/for/love-relationships"
            eyebrow="Popular Intention"
            title="Love & Relationships"
            body="Explore heart-centered stones for attraction, emotional repair, and warmer connection."
            accent="blue"
          />
        </div>

        <CrystalFaqs title="Crystal Healing FAQs" items={HUB_FAQS} />

        <CrystalSection title="A Gentle Way In">
          <div className="flex flex-col gap-4 text-sm leading-7 text-stone-600 md:flex-row md:items-start md:justify-between">
            <div className="max-w-2xl">
              <p>You do not need a perfect ritual to start. Choose one intention, one crystal, and one place where you will actually remember to use it. Consistency matters more than complexity.</p>
            </div>
            <Link to="/crystals/calculator" className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/10 px-5 py-3 text-sm font-semibold text-stone-900 transition hover:bg-gold/20">
              <Compass className="h-4 w-4" />
              Try the calculator
            </Link>
          </div>
        </CrystalSection>
      </CrystalPageFrame>
      <Footer />
    </div>
  );
}

export default CrystalHubPage;
