import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, LoaderCircle, Sparkles, SunMedium } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { API, SITE, buildArticleSchema, buildBreadcrumbSchema, buildFaqSchema } from './crystalShared';
import { CrystalFaqs, CrystalLinkCard, CrystalPageFrame, CrystalSection } from './CrystalUi';

export function CrystalPlanetPage() {
  const { planet } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;
    async function fetchPlanetPage() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/planet/${planet}`);
        if (!ignore) {
          setData(response.data);
        }
      } catch (err) {
        if (!ignore) {
          setError(err?.response?.data?.detail || 'Unable to load this planet crystal page right now.');
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    if (planet) {
      fetchPlanetPage();
    }
    return () => {
      ignore = true;
    };
  }, [planet]);

  const canonicalUrl = data ? `${SITE}/crystals/for/planet/${data.slug}` : `${SITE}/crystals/for/planet/${planet || ''}`;
  const schema = data ? {
    '@context': 'https://schema.org',
    '@graph': [
      buildArticleSchema({
        headline: `Best Crystals for ${data.display} - Vedic Gemstones & Healing Stones`,
        description: data.meta_description,
        url: canonicalUrl,
      }),
      buildFaqSchema(data.faq || []),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Crystals', url: `${SITE}/crystals` },
        { name: `${data.display} crystals`, url: canonicalUrl },
      ]),
    ],
  } : null;

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(197,160,89,0.15),_transparent_30%),linear-gradient(180deg,_#fffdf8_0%,_#f8efe3_44%,_#fffaf2_100%)]">
      <SEO
        title={data?.meta_title || 'Best Crystals for Your Planet'}
        description={data?.meta_description || 'Explore Vedic and healing crystals for a planetary theme.'}
        canonical={canonicalUrl}
        jsonLd={schema}
        noindex={!data && !loading}
      />

      <CrystalPageFrame
        eyebrow="Planet Guide"
        title={data ? `Best Crystals for ${data.display} - Vedic Gemstones & Healing Stones` : 'Planet Crystal Guide'}
        description={data?.intro || 'Loading planet crystal guide...'}
      >
        <Link to="/crystals" className="inline-flex items-center gap-2 text-sm font-medium text-stone-600 transition hover:text-stone-900">
          <ArrowLeft className="h-4 w-4" />
          Back to crystal hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-2xl border border-gold/15 bg-white/70 p-12 text-stone-500">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading planet page...
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-red-300/40 bg-red-50 p-6 text-sm text-red-700">{error}</div>
        ) : (
          <>
            <CrystalSection title="Primary Vedic Gemstone">
              <div className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
                <div className="rounded-2xl border border-gold/30 bg-gold/10 p-6">
                  <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.24em] text-gold/80">
                    <SunMedium className="h-4 w-4" />
                    Main Planetary Stone
                  </div>
                  <h2 className="mt-3 font-playfair text-3xl font-semibold text-stone-900">{data.primary_crystal.display_name}</h2>
                  <p className="mt-3 text-sm leading-7 text-stone-600">{data.primary_crystal.tagline}</p>
                  <p className="mt-4 text-sm leading-7 text-stone-600">{data.primary_crystal.who_should_wear}</p>
                </div>
                <div className="rounded-2xl border border-gold/20 bg-white/80 p-6 text-sm leading-7 text-stone-600">
                  <p><span className="font-semibold text-stone-900">Metal:</span> {data.primary_crystal.wearing?.metal}</p>
                  <p><span className="font-semibold text-stone-900">Finger:</span> {data.primary_crystal.wearing?.finger}</p>
                  <p><span className="font-semibold text-stone-900">Day:</span> {data.primary_crystal.wearing?.day}</p>
                  <p><span className="font-semibold text-stone-900">Mantra:</span> {data.primary_crystal.wearing?.mantra}</p>
                  <p><span className="font-semibold text-stone-900">Activation:</span> {data.primary_crystal.wearing?.activation}</p>
                </div>
              </div>
            </CrystalSection>

            <CrystalSection title="Supporting Healing Crystals">
              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                {data.supporting_crystals?.map((item) => (
                  <CrystalLinkCard
                    key={item.slug}
                    to={`/crystals/${item.slug}`}
                    eyebrow={item.color}
                    title={item.display_name}
                    body={`${item.why}${item.how_to_use ? ` ${item.how_to_use}` : ''}`}
                    accent="teal"
                  />
                ))}
              </div>
            </CrystalSection>

            <CrystalSection title="Crystals to Avoid or Combine Carefully">
              <div className="grid gap-4 md:grid-cols-2">
                {data.avoid_cards?.map((item) => (
                  <CrystalLinkCard
                    key={item.slug}
                    to={`/crystals/${item.slug}`}
                    eyebrow={item.color}
                    title={item.display_name}
                    body={item.why}
                    accent="blue"
                  />
                ))}
              </div>
            </CrystalSection>

            <CrystalSection title={`How to Work with ${data.display} Crystals`}>
              <ul className="space-y-3 text-sm leading-7 text-stone-600">
                {data.how_to_use?.map((item) => <li key={item}>• {item}</li>)}
              </ul>
            </CrystalSection>

            <CrystalFaqs title={`${data.display} Crystal FAQs`} items={data.faq || []} />

            <CrystalSection title="Need Chart-Specific Confirmation?">
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <p className="max-w-2xl text-sm leading-7 text-stone-600">This page gives a strong public starting point for {data.display} energy. Use the calculator if you want your dasha and chart context to influence the recommendation directly.</p>
                <Link to="/crystals/calculator" className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/10 px-5 py-3 text-sm font-semibold text-stone-900 transition hover:bg-gold/20">
                  <Sparkles className="h-4 w-4" />
                  Open crystal calculator
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

export default CrystalPlanetPage;
