import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, LoaderCircle, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { API, SITE, buildArticleSchema, buildBreadcrumbSchema, buildFaqSchema } from './crystalShared';
import { CrystalFaqs, CrystalLinkCard, CrystalPageFrame, CrystalSection } from './CrystalUi';

export function CrystalProblemPage() {
  const { problem } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;
    async function fetchProblemPage() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/problem/${problem}`);
        if (!ignore) {
          setData(response.data);
        }
      } catch (err) {
        if (!ignore) {
          setError(err?.response?.data?.detail || 'Unable to load this crystal problem page right now.');
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    if (problem) {
      fetchProblemPage();
    }
    return () => {
      ignore = true;
    };
  }, [problem]);

  const canonicalUrl = data ? `${SITE}/crystals/for/problem/${data.slug}` : `${SITE}/crystals/for/problem/${problem || ''}`;
  const schema = data ? {
    '@context': 'https://schema.org',
    '@graph': [
      buildArticleSchema({
        headline: `Crystals for ${data.display} - Best Healing Stones & How to Use Them`,
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
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(197,160,89,0.14),_transparent_30%),linear-gradient(180deg,_#fffdf8_0%,_#f7eee5_44%,_#fffaf2_100%)]">
      <SEO
        title={data?.meta_title || 'Crystals for a Specific Problem'}
        description={data?.meta_description || 'Explore crystals for a specific energetic challenge.'}
        canonical={canonicalUrl}
        jsonLd={schema}
        noindex={!data && !loading}
      />

      <CrystalPageFrame
        eyebrow="Problem Guide"
        title={data ? `Crystals for ${data.display} - Best Healing Stones & How to Use Them` : 'Problem Crystal Guide'}
        description={data?.intro || 'Loading problem-area crystal guide...'}
      >
        <Link to="/crystals" className="inline-flex items-center gap-2 text-sm font-medium text-stone-600 transition hover:text-stone-900">
          <ArrowLeft className="h-4 w-4" />
          Back to crystal hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-2xl border border-gold/15 bg-white/70 p-12 text-stone-500">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading problem page...
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-red-300/40 bg-red-50 p-6 text-sm text-red-700">{error}</div>
        ) : (
          <>
            <CrystalSection title="Top 3 Crystals">
              <div className="grid gap-4 lg:grid-cols-3">
                {data.top_crystals?.map((item) => (
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

            <CrystalSection title="Supporting Crystals">
              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                {data.supporting_crystals?.map((item) => (
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

            <div className="grid gap-6 lg:grid-cols-2">
              <CrystalSection title={data.crystal_grid?.name || 'Crystal Grid Suggestion'}>
                <div className="flex flex-wrap gap-3">
                  {data.crystal_grid?.stones?.map((item) => (
                    <Link key={item.slug} to={`/crystals/${item.slug}`} className="inline-flex items-center rounded-full border border-gold/25 bg-gold/10 px-4 py-2 text-sm font-medium text-stone-700 transition hover:border-gold/45">
                      {item.display_name}
                    </Link>
                  ))}
                </div>
                <p className="mt-5 text-sm leading-7 text-stone-600">{data.crystal_grid?.how_to_use}</p>
              </CrystalSection>

              <CrystalSection title="Affirmation">
                <blockquote className="rounded-2xl border border-gold/35 bg-gold/10 px-6 py-5 font-playfair text-2xl italic leading-relaxed text-stone-900">
                  "{data.affirmation}"
                </blockquote>
              </CrystalSection>
            </div>

            <CrystalFaqs title={`${data.display} Crystal FAQs`} items={data.faq || []} />

            <CrystalSection title="Ready for a More Personal Recommendation?">
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <p className="max-w-2xl text-sm leading-7 text-stone-600">Problem pages are strong thematic starting points. If you want the recommendation filtered through active dasha and chart emphasis, the calculator is the best next step.</p>
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

export default CrystalProblemPage;
