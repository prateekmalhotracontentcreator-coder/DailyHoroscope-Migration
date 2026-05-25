import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { AlertCircle, ArrowLeft, LoaderCircle, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { API, SITE, buildArticleSchema, buildBreadcrumbSchema, buildFaqSchema } from './crystalShared';
import { CrystalChip, CrystalFaqs, CrystalLinkCard, CrystalPageFrame, CrystalSection } from './CrystalUi';

export function CrystalPage() {
  const { crystalSlug } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;
    async function fetchCrystal() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/${crystalSlug}`);
        if (!ignore) {
          setData(response.data);
        }
      } catch (err) {
        if (!ignore) {
          setError(err?.response?.data?.detail || 'Unable to load this crystal page right now.');
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    if (crystalSlug) {
      fetchCrystal();
    }
    return () => {
      ignore = true;
    };
  }, [crystalSlug]);

  const canonicalUrl = data ? `${SITE}/crystals/${data.slug}` : `${SITE}/crystals/${crystalSlug || ''}`;
  const schema = data ? {
    '@context': 'https://schema.org',
    '@graph': [
      buildArticleSchema({
        headline: `${data.display_name} - Meaning, Healing Properties & How to Use`,
        description: data.meta_description,
        url: canonicalUrl,
      }),
      buildFaqSchema(data.faq || []),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Crystals', url: `${SITE}/crystals` },
        { name: data.display_name, url: canonicalUrl },
      ]),
    ],
  } : null;

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(197,160,89,0.15),_transparent_30%),linear-gradient(180deg,_#fffdf8_0%,_#f6efe1_44%,_#fffaf1_100%)]">
      <SEO
        title={data?.meta_title || 'Crystal Meaning & Healing Properties'}
        description={data?.meta_description || 'Explore this crystal page on Everyday Horoscope.'}
        canonical={canonicalUrl}
        jsonLd={schema}
        noindex={!data && !loading}
      />

      <CrystalPageFrame
        eyebrow={data?.planet || 'Crystal Profile'}
        title={data ? `${data.display_name} - Meaning, Healing Properties & How to Use` : 'Crystal Profile'}
        description={data?.tagline || 'Loading crystal profile...'}
      >
        <Link to="/crystals" className="inline-flex items-center gap-2 text-sm font-medium text-stone-600 transition hover:text-stone-900">
          <ArrowLeft className="h-4 w-4" />
          Back to crystal hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-2xl border border-gold/15 bg-white/70 p-12 text-stone-500">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading crystal page...
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-red-300/40 bg-red-50 p-6 text-sm text-red-700">{error}</div>
        ) : (
          <>
            <CrystalSection title="Crystal Snapshot">
              <div className="flex flex-wrap gap-2">
                <CrystalChip>{data.color}</CrystalChip>
                {data.chakras.map((item) => <CrystalChip key={item}>{item}</CrystalChip>)}
                <CrystalChip>{data.element}</CrystalChip>
                <CrystalChip>{data.planet}</CrystalChip>
                {data.zodiac.slice(0, 3).map((item) => <CrystalChip key={item}>{item}</CrystalChip>)}
              </div>
              <p className="mt-5 text-sm leading-7 text-stone-600">{data.meta_description}</p>
            </CrystalSection>

            <div className="grid gap-6 lg:grid-cols-3">
              <CrystalSection title="Emotional Healing" className="lg:col-span-1">
                <ul className="space-y-3 text-sm leading-7 text-stone-600">
                  {data.healing_properties?.emotional?.map((item) => <li key={item}>• {item}</li>)}
                </ul>
              </CrystalSection>
              <CrystalSection title="Physical Support" className="lg:col-span-1">
                <ul className="space-y-3 text-sm leading-7 text-stone-600">
                  {data.healing_properties?.physical?.map((item) => <li key={item}>• {item}</li>)}
                </ul>
              </CrystalSection>
              <CrystalSection title="Spiritual Tone" className="lg:col-span-1">
                <ul className="space-y-3 text-sm leading-7 text-stone-600">
                  {data.healing_properties?.spiritual?.map((item) => <li key={item}>• {item}</li>)}
                </ul>
              </CrystalSection>
            </div>

            <div className="grid gap-6 lg:grid-cols-2">
              <CrystalSection title="Best Intentions">
                <div className="flex flex-wrap gap-3">
                  {data.intention_cards?.map((item) => (
                    <Link key={item.slug} to={`/crystals/for/${item.slug}`} className="inline-flex items-center rounded-full border border-gold/25 bg-gold/10 px-4 py-2 text-sm font-medium text-stone-700 transition hover:border-gold/45">
                      {item.display}
                    </Link>
                  ))}
                </div>
              </CrystalSection>
              <CrystalSection title="How to Use">
                <ul className="space-y-3 text-sm leading-7 text-stone-600">
                  {data.how_to_use?.map((item) => <li key={item}>• {item}</li>)}
                </ul>
              </CrystalSection>
            </div>

            <div className="grid gap-6 lg:grid-cols-2">
              <CrystalSection title="Pairs Well With">
                <div className="grid gap-4 md:grid-cols-2">
                  {data.pair_cards?.map((item) => (
                    <CrystalLinkCard
                      key={item.slug}
                      to={`/crystals/${item.slug}`}
                      eyebrow={item.color}
                      title={item.display_name}
                      body={item.tagline}
                      accent="teal"
                    />
                  ))}
                </div>
              </CrystalSection>

              <CrystalSection title="Cleansing Methods">
                <ul className="space-y-3 text-sm leading-7 text-stone-600">
                  {data.cleansing_methods?.map((item) => <li key={item}>• {item}</li>)}
                </ul>
              </CrystalSection>
            </div>

            <CrystalSection title="Affirmation">
              <blockquote className="rounded-2xl border border-gold/35 bg-gold/10 px-6 py-5 font-playfair text-2xl italic leading-relaxed text-stone-900">
                "{data.affirmation}"
              </blockquote>
            </CrystalSection>

            {data.wearing ? (
              <CrystalSection title="Vedic Gemstone Guidance">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="rounded-2xl border border-gold/20 bg-white/80 p-5">
                    <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold/80">Wearing Instructions</p>
                    <div className="mt-4 space-y-3 text-sm leading-7 text-stone-600">
                      <p><span className="font-semibold text-stone-900">Metal:</span> {data.wearing.metal}</p>
                      <p><span className="font-semibold text-stone-900">Finger:</span> {data.wearing.finger}</p>
                      <p><span className="font-semibold text-stone-900">Day:</span> {data.wearing.day}</p>
                      <p><span className="font-semibold text-stone-900">Activation:</span> {data.wearing.activation}</p>
                    </div>
                  </div>
                  <div className="rounded-2xl border border-gold/20 bg-white/80 p-5">
                    <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold/80">Mantra & Pairing Logic</p>
                    <div className="mt-4 space-y-4 text-sm leading-7 text-stone-600">
                      <p><span className="font-semibold text-stone-900">Mantra:</span> {data.wearing.mantra}</p>
                      <p><span className="font-semibold text-stone-900">Synergy:</span> {(data.synergy || []).map((item) => item.replace(/-/g, ' ')).join(', ')}</p>
                      <p><span className="font-semibold text-stone-900">Conflict:</span> {(data.conflict || []).map((item) => item.replace(/-/g, ' ')).join(', ')}</p>
                    </div>
                  </div>
                </div>
              </CrystalSection>
            ) : null}

            {data.caution ? (
              <CrystalSection title="Caution Note">
                <div className="flex items-start gap-3 rounded-2xl border border-amber-300/40 bg-amber-50 p-5 text-sm leading-7 text-amber-900">
                  <AlertCircle className="mt-1 h-5 w-5 shrink-0" />
                  <p>{data.caution}</p>
                </div>
              </CrystalSection>
            ) : null}

            <CrystalFaqs title={`${data.display_name} FAQs`} items={data.faq || []} />

            <CrystalSection title="Next Step">
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div className="max-w-2xl">
                  <p className="text-sm leading-7 text-stone-600">If you want a chart-based recommendation instead of browsing by resonance alone, the calculator can point you toward a primary Vedic gemstone and a smaller support set.</p>
                </div>
                <Link to="/crystals/calculator" className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/10 px-5 py-3 text-sm font-semibold text-stone-900 transition hover:bg-gold/20">
                  <Sparkles className="h-4 w-4" />
                  Find your crystal by birth chart
                </Link>
              </div>
            </CrystalSection>
          </>
        )}
      </CrystalPageFrame>
      <Footer />
    </div>
  );
}

export default CrystalPage;
