import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, LoaderCircle, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { API, SITE, buildArticleSchema, buildBreadcrumbSchema, buildFaqSchema } from './crystalShared';
import { CrystalFaqs, CrystalLinkCard, CrystalPageFrame, CrystalSection } from './CrystalUi';

export function CrystalSignPage() {
  const { sign } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;
    async function fetchSignPage() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/sign/${sign}`);
        if (!ignore) {
          setData(response.data);
        }
      } catch (err) {
        if (!ignore) {
          setError(err?.response?.data?.detail || 'Unable to load this sign crystal page right now.');
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    if (sign) {
      fetchSignPage();
    }
    return () => {
      ignore = true;
    };
  }, [sign]);

  const canonicalUrl = data ? `${SITE}/crystals/for/sign/${data.slug}` : `${SITE}/crystals/for/sign/${sign || ''}`;
  const schema = data ? {
    '@context': 'https://schema.org',
    '@graph': [
      buildArticleSchema({
        headline: `Best Crystals for ${data.display} - Healing Stones for ${data.display} Energy`,
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
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(197,160,89,0.14),_transparent_28%),linear-gradient(180deg,_#fffdf8_0%,_#f7f0e5_42%,_#fffaf3_100%)]">
      <SEO
        title={data?.meta_title || 'Best Crystals for Your Sign'}
        description={data?.meta_description || 'Explore crystals by zodiac sign.'}
        canonical={canonicalUrl}
        jsonLd={schema}
        noindex={!data && !loading}
      />

      <CrystalPageFrame
        eyebrow="Sign Guide"
        title={data ? `Best Crystals for ${data.display} - Healing Stones for ${data.display} Energy` : 'Sign Crystal Guide'}
        description={data?.intro || 'Loading sign crystal guide...'}
      >
        <Link to="/crystals" className="inline-flex items-center gap-2 text-sm font-medium text-stone-600 transition hover:text-stone-900">
          <ArrowLeft className="h-4 w-4" />
          Back to crystal hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-2xl border border-gold/15 bg-white/70 p-12 text-stone-500">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading sign page...
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-red-300/40 bg-red-50 p-6 text-sm text-red-700">{error}</div>
        ) : (
          <>
            <CrystalSection title={`${data.display} Energy Snapshot`}>
              <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
                <div className="rounded-2xl border border-gold/25 bg-gold/10 p-5 text-sm leading-7 text-stone-600">
                  <p><span className="font-semibold text-stone-900">Element:</span> {data.element}</p>
                  <p><span className="font-semibold text-stone-900">Ruling planet:</span> {data.ruling_planet}</p>
                  <p><span className="font-semibold text-stone-900">Key traits:</span> {data.traits}</p>
                </div>
                <p className="text-sm leading-7 text-stone-600">{data.intro}</p>
              </div>
            </CrystalSection>

            <CrystalSection title="Signature Crystals">
              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
                {data.signature_crystals?.map((item) => (
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

            <CrystalSection title={`Crystals for ${data.display}'s Shadow Side`}>
              <div className="grid gap-4 md:grid-cols-2">
                {data.shadow_crystals?.map((item) => (
                  <CrystalLinkCard
                    key={item.slug}
                    to={`/crystals/${item.slug}`}
                    eyebrow={item.challenge}
                    title={item.display_name}
                    body={`${item.why} This one is especially helpful when ${data.display} energy slips into ${item.challenge}.`}
                    accent="blue"
                  />
                ))}
              </div>
            </CrystalSection>

            <CrystalSection title="Monthly Crystal Ritual">
              <ul className="space-y-3 text-sm leading-7 text-stone-600">
                {data.monthly_ritual?.map((item) => <li key={item}>• {item}</li>)}
              </ul>
            </CrystalSection>

            <CrystalFaqs title={`${data.display} Crystal FAQs`} items={data.faq || []} />

            <CrystalSection title="Want a Birth-Chart Layer Too?">
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <p className="max-w-2xl text-sm leading-7 text-stone-600">Sign-based crystal guidance is a great energetic shortcut. If you want to go deeper, the calculator adds dasha timing and planetary emphasis on top of your sign resonance.</p>
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

export default CrystalSignPage;
