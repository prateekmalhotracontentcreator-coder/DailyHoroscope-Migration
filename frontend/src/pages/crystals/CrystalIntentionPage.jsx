import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, LoaderCircle, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { API, SITE, buildArticleSchema, buildBreadcrumbSchema, buildFaqSchema } from './crystalShared';
import { CrystalFaqs, CrystalLinkCard, CrystalPageFrame, CrystalSection } from './CrystalUi';

export function CrystalIntentionPage() {
  const { intentionSlug } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;
    async function fetchIntention() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/intention/${intentionSlug}`);
        if (!ignore) {
          setData(response.data);
        }
      } catch (err) {
        if (!ignore) {
          setError(err?.response?.data?.detail || 'Unable to load this crystal intention page right now.');
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    if (intentionSlug) {
      fetchIntention();
    }
    return () => {
      ignore = true;
    };
  }, [intentionSlug]);

  const canonicalUrl = data ? `${SITE}/crystals/for/${data.slug}` : `${SITE}/crystals/for/${intentionSlug || ''}`;
  const schema = data ? {
    '@context': 'https://schema.org',
    '@graph': [
      buildArticleSchema({
        headline: `Best Crystals for ${data.display} - Top Stones & How to Use Them`,
        description: data.meta_description,
        url: canonicalUrl,
      }),
      buildFaqSchema(data.faq || []),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Crystals', url: `${SITE}/crystals` },
        { name: data.display, url: canonicalUrl },
      ]),
    ],
  } : null;

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(197,160,89,0.14),_transparent_28%),linear-gradient(180deg,_#fffdf8_0%,_#f8efe8_42%,_#fffaf3_100%)]">
      <SEO
        title={data?.meta_title || 'Best Crystals by Intention'}
        description={data?.meta_description || 'Explore crystal recommendations by life intention.'}
        canonical={canonicalUrl}
        jsonLd={schema}
        noindex={!data && !loading}
      />

      <CrystalPageFrame
        eyebrow="Intention Guide"
        title={data ? `Best Crystals for ${data.display} - Top ${data.top_crystal_cards?.length || ''} Stones & How to Use Them` : 'Crystal Intention Guide'}
        description={data?.intro || 'Loading intention guide...'}
      >
        <Link to="/crystals" className="inline-flex items-center gap-2 text-sm font-medium text-stone-600 transition hover:text-stone-900">
          <ArrowLeft className="h-4 w-4" />
          Back to crystal hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-2xl border border-gold/15 bg-white/70 p-12 text-stone-500">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading intention page...
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-red-300/40 bg-red-50 p-6 text-sm text-red-700">{error}</div>
        ) : (
          <>
            <CrystalSection title="Top Crystal Matches">
              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                {data.top_crystal_cards?.map((item) => (
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

            <div className="grid gap-6 lg:grid-cols-2">
              <CrystalSection title={`How to Use Crystals for ${data.display}`}>
                <ul className="space-y-3 text-sm leading-7 text-stone-600">
                  {data.how_to_use?.map((item) => <li key={item}>• {item}</li>)}
                </ul>
              </CrystalSection>

              <CrystalSection title="Affirmation">
                <blockquote className="rounded-2xl border border-gold/35 bg-gold/10 px-6 py-5 font-playfair text-2xl italic leading-relaxed text-stone-900">
                  "{data.affirmation}"
                </blockquote>
              </CrystalSection>
            </div>

            <CrystalFaqs title={`${data.display} Crystal FAQs`} items={data.faq || []} />

            <CrystalSection title="Need a More Personal Match?">
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <p className="max-w-2xl text-sm leading-7 text-stone-600">This page gives strong intention-based starting points. If you want the recommendation filtered through active dasha themes and weaker planets, try the birth-chart calculator next.</p>
                <Link to="/crystals/calculator" className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/10 px-5 py-3 text-sm font-semibold text-stone-900 transition hover:bg-gold/20">
                  <Sparkles className="h-4 w-4" />
                  Get your personal crystal recommendation
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

export default CrystalIntentionPage;
