import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, Gem, HeartPulse, LoaderCircle, ScrollText, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const SITE = 'https://www.everydayhoroscope.in';

const DOSHA_CONTENT = {
  'shani-sade-sati': {
    name: 'Shani Sade Sati',
    summary: 'Shani Sade Sati is the seven-and-a-half-year Saturn transit over the 12th, 1st, and 2nd houses from the natal Moon. It is often associated with karmic pressure, delay, responsibility, and emotional heaviness.',
    manifestations: ['career delays and slower results', 'financial pressure or duty-heavy periods', 'fatigue, isolation, or emotional weight'],
  },
  'manglik-dosha': {
    name: 'Manglik Dosha',
    summary: 'Manglik Dosha is linked with Mars occupying sensitive marriage houses. It is commonly discussed for marriage timing, temperament, conflict patterns, and high heat in relationships.',
    manifestations: ['marriage delays or hesitation', 'strong reactions and conflict loops', 'restlessness around commitment and domestic peace'],
  },
  'pitru-dosha': {
    name: 'Pitru Dosha',
    summary: 'Pitru Dosha is associated with unresolved ancestral karma, family lineage imbalance, or blocked blessings from the paternal line. It is often discussed when family progress feels delayed without a clear external cause.',
    manifestations: ['repeating family obstacles', 'ancestral heaviness around finances or marriage', 'difficulty feeling supported by family karma'],
  },
  'kaal-sarp-dosha': {
    name: 'Kaal Sarp Dosha',
    summary: 'Kaal Sarp Dosha is associated with all grahas falling between Rahu and Ketu. It is traditionally linked with intensity, inner pressure, sudden reversals, and karmic acceleration.',
    manifestations: ['extreme ups and downs', 'anxiety, fear, or recurring inner pressure', 'sudden blocks despite strong effort'],
  },
  'shani-mahadasha': {
    name: 'Shani Mahadasha',
    summary: 'Shani Mahadasha is Saturn\'s 19-year period. It emphasizes discipline, realism, accountability, and long-cycle karmic correction.',
    manifestations: ['slow but important career restructuring', 'heavier duties and responsibility', 'lessons around patience, boundaries, and endurance'],
  },
  'rahu-mahadasha': {
    name: 'Rahu Mahadasha',
    summary: 'Rahu Mahadasha is a transformative period that can amplify ambition, confusion, desire, foreign themes, and sudden changes in direction.',
    manifestations: ['obsession or overdrive', 'confusing choices and mixed signals', 'foreign, unconventional, or disruptive life shifts'],
  },
  'ketu-mahadasha': {
    name: 'Ketu Mahadasha',
    summary: 'Ketu Mahadasha often brings detachment, spiritual pull, loss of interest in former goals, and a sharper karmic focus on inner work.',
    manifestations: ['withdrawal from old ambitions', 'confusion about identity or direction', 'stronger spiritual or moksha themes'],
  },
  'guru-chandal-yoga': {
    name: 'Guru Chandal Yoga',
    summary: 'Guru Chandal Yoga is associated with Jupiter and Rahu joining closely. It may disturb wisdom, guidance, mentors, judgment, or the way belief systems are expressed.',
    manifestations: ['confusion around teachers or guidance', 'misjudgment despite intelligence', 'distortion of values, wisdom, or counsel'],
  },
  'grahan-yoga': {
    name: 'Grahan Yoga',
    summary: 'Grahan Yoga is linked with eclipse-style affliction involving the Sun or Moon with Rahu or Ketu. It can show identity fog, emotional swings, and heightened karmic intensity.',
    manifestations: ['mood volatility or identity confusion', 'eclipse-like highs and lows', 'disturbed peace or decision clarity'],
  },
  'nadi-dosha': {
    name: 'Nadi Dosha',
    summary: 'Nadi Dosha is one of the most discussed Ashta-Koota mismatches in marriage matching. It is traditionally linked with vitality, health, and family harmony concerns in compatibility analysis.',
    manifestations: ['concern during marriage matching', 'questions around health rhythm or long-term harmony', 'need for deeper birth-chart matching before commitment'],
  },
  'gana-dosha': {
    name: 'Gana Dosha',
    summary: 'Gana Dosha reflects temperament mismatch in Gun Milan. It points to the way two people instinctively react, compromise, and share emotional style.',
    manifestations: ['temperament mismatch', 'friction in emotional style', 'difficulty adjusting to each other\'s nature'],
  },
  'bhakoot-dosha': {
    name: 'Bhakoot Dosha',
    summary: 'Bhakoot Dosha is a moon-sign mismatch in Ashta-Koota matching. It is traditionally associated with domestic harmony, family growth, and emotional alignment in marriage.',
    manifestations: ['emotional mismatch in partnership', 'tension around family harmony', 'need for deeper compatibility review'],
  },
};

const TAB_LABELS = {
  all: 'All Remedies',
  gemstone: 'Gemstones',
  mantra: 'Mantras',
  donation: 'Donations',
  crystal: 'Crystals',
  ritual: 'Healing',
  lk_ritual: 'Lal Kitab',
};

const TYPE_BADGES = {
  gemstone: 'border-amber-400/30 bg-amber-500/15 text-amber-300',
  mantra: 'border-sky-400/30 bg-sky-500/15 text-sky-300',
  donation: 'border-emerald-400/30 bg-emerald-500/15 text-emerald-300',
  crystal: 'border-violet-400/30 bg-violet-500/15 text-violet-300',
  ritual: 'border-rose-400/30 bg-rose-500/15 text-rose-300',
  lk_ritual: 'border-gold/30 bg-gold/10 text-gold',
};

function buildFaqSchema(dosha, canonicalUrl) {
  if (!dosha) return null;
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: [
      {
        '@type': 'Question',
        name: `What is ${dosha.name}?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: dosha.summary,
        },
      },
      {
        '@type': 'Question',
        name: `How do I detect ${dosha.name}?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: `The best way to confirm ${dosha.name} is through a full Vedic birth chart reading that checks graha positions, houses, dashas, and matching factors instead of relying on one indicator alone.`,
        },
      },
      {
        '@type': 'Question',
        name: `How can I remedy ${dosha.name}?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: `Remedies for ${dosha.name} usually combine spiritual practices, gemstone or donation guidance, and when relevant Lal Kitab actions. Always match remedies to the full chart before following them seriously.`,
        },
      },
    ],
    url: canonicalUrl,
  };
}

export function RemedyHubPage() {
  const { dosha = '' } = useParams();
  const doshaInfo = DOSHA_CONTENT[dosha];
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!doshaInfo) {
      setLoading(false);
      setError('Remedy hub not found.');
      setData(null);
      return;
    }

    let ignore = false;

    async function fetchRemedies() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/remedies/${dosha}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.data?.detail || 'Unable to load remedies right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchRemedies();
    return () => {
      ignore = true;
    };
  }, [dosha, doshaInfo]);

  const canonicalUrl = doshaInfo ? `${SITE}/remedies/${dosha}` : `${SITE}/remedies`;
  const schema = useMemo(() => buildFaqSchema(doshaInfo, canonicalUrl), [canonicalUrl, doshaInfo]);
  const title = doshaInfo
    ? `${doshaInfo.name} Remedies - Mantras, Gemstones & Rituals`
    : 'Vedic Remedies';
  const description = doshaInfo
    ? `Effective Vedic remedies for ${doshaInfo.name}. Find gemstones, mantras, donations, and Lal Kitab rituals to reduce the impact.`
    : 'Vedic remedies by dosha.';
  const remedies = data?.remedies || [];
  const availableTabs = useMemo(() => {
    const types = new Set(remedies.map((item) => item.remedy_type));
    return ['all', ...Object.keys(TAB_LABELS).filter((key) => key !== 'all' && types.has(key))];
  }, [remedies]);

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title={title}
        description={description}
        canonical={canonicalUrl}
        hreflang={[
          { lang: 'en-in', href: canonicalUrl },
          { lang: 'en-us', href: canonicalUrl },
        ]}
        jsonLd={schema}
        noindex={!doshaInfo}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-6 flex items-center gap-2 text-sm text-muted-foreground">
          <Link to="/remedies" className="hover:text-gold transition">Remedies</Link>
          <span>/</span>
          <span className="text-foreground">{doshaInfo?.name || 'Hub'}</span>
        </div>

        <Link
          to="/remedies"
          className="mb-6 inline-flex items-center text-sm font-medium text-muted-foreground transition hover:text-gold"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          All remedies overview
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-2xl border border-gold/15 bg-background/80 p-12 text-muted-foreground">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading remedy hub...
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-red-400/20 bg-red-500/10 p-6 text-sm text-red-200">
            {error}
          </div>
        ) : doshaInfo ? (
          <>
            <section className="rounded-3xl border border-gold/20 bg-gradient-to-br from-gold/[0.08] via-background to-background p-8 shadow-sm">
              <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
                <div className="max-w-3xl">
                  <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.06] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
                    <ScrollText className="h-3.5 w-3.5" />
                    Affliction Remedy Hub
                  </div>
                  <h1 className="mt-4 text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                    {doshaInfo.name} Remedies
                  </h1>
                  <p className="mt-3 text-sm leading-7 text-muted-foreground">
                    {doshaInfo.summary}
                  </p>
                </div>

                <div className="rounded-2xl border border-gold/20 bg-background/80 px-5 py-4 text-sm shadow-sm">
                  <p className="font-semibold text-foreground">{remedies.length} remedies matched</p>
                  <p className="mt-1 text-muted-foreground">
                    Combined from interpretation rules and Lal Kitab knowledge rules
                  </p>
                </div>
              </div>
            </section>

            <section className="mt-8 grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <div className="flex items-center gap-2 text-gold">
                  <HeartPulse className="h-4 w-4" />
                  <h2 className="text-xl font-semibold text-foreground">How it often shows up</h2>
                </div>
                <ul className="mt-5 space-y-3 text-sm text-muted-foreground">
                  {doshaInfo.manifestations.map((item) => (
                    <li key={item} className="rounded-2xl border border-gold/10 bg-gold/[0.04] px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <div className="flex items-center gap-2 text-gold">
                  <Sparkles className="h-4 w-4" />
                  <h2 className="text-xl font-semibold text-foreground">Check if you have this dosha</h2>
                </div>
                <p className="mt-5 text-sm leading-7 text-muted-foreground">
                  A dosha should be confirmed from your full Vedic birth chart, not from moon sign alone. The right diagnosis checks houses, graha dignity, aspects, dashas, and the wider chart context.
                </p>
                <Link
                  to="/birth-chart"
                  className="mt-5 inline-flex items-center rounded-full bg-gold px-5 py-3 text-sm font-semibold text-background transition hover:opacity-90"
                >
                  Check this in your birth chart
                </Link>
              </div>
            </section>

            <section className="mt-8 rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
              <div className="flex items-center gap-2 text-gold">
                <Gem className="h-4 w-4" />
                <h2 className="text-xl font-semibold text-foreground">Matched remedy listings</h2>
              </div>
              <p className="mt-2 text-sm text-muted-foreground">
                Remedy results are filtered by `affliction_tags` across both MongoDB remedy collections.
              </p>

              <Tabs defaultValue="all" className="mt-6">
                <TabsList className="h-auto flex-wrap justify-start gap-2 bg-transparent p-0">
                  {availableTabs.map((tab) => (
                    <TabsTrigger
                      key={tab}
                      value={tab}
                      className="rounded-full border border-gold/20 bg-gold/[0.05] px-4 py-2 text-xs uppercase tracking-[0.16em] text-muted-foreground data-[state=active]:border-gold data-[state=active]:bg-gold data-[state=active]:text-background"
                    >
                      {TAB_LABELS[tab] || tab}
                    </TabsTrigger>
                  ))}
                </TabsList>

                {availableTabs.map((tab) => {
                  const filtered = tab === 'all' ? remedies : remedies.filter((item) => item.remedy_type === tab);
                  return (
                    <TabsContent key={tab} value={tab} className="mt-6">
                      {filtered.length ? (
                        <div className="grid gap-4 lg:grid-cols-2">
                          {filtered.map((item) => (
                            <article key={`${tab}-${item.rule_id}`} className="rounded-2xl border border-gold/10 bg-gold/[0.04] p-5">
                              <div className="flex flex-wrap items-center justify-between gap-3">
                                <span className={`inline-flex rounded-full border px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.16em] ${TYPE_BADGES[item.remedy_type] || TYPE_BADGES.ritual}`}>
                                  {TAB_LABELS[item.remedy_type] || item.remedy_type}
                                </span>
                                <span className="text-xs text-muted-foreground">{item.rule_id}</span>
                              </div>
                              <p className="mt-4 text-sm font-semibold text-foreground">{item.summary}</p>
                              <p className="mt-3 text-sm leading-6 text-muted-foreground">{item.detailed}</p>
                              <div className="mt-4 flex flex-wrap gap-2 text-xs text-muted-foreground">
                                {item.planet && (
                                  <span className="rounded-full border border-gold/10 px-3 py-1">
                                    Planet: {item.planet}
                                  </span>
                                )}
                                {(item.zodiac_signs || []).slice(0, 4).map((sign) => (
                                  <span key={`${item.rule_id}-${sign}`} className="rounded-full border border-gold/10 px-3 py-1">
                                    {sign}
                                  </span>
                                ))}
                              </div>
                            </article>
                          ))}
                        </div>
                      ) : (
                        <div className="rounded-2xl border border-gold/10 bg-gold/[0.04] p-5 text-sm text-muted-foreground">
                          No remedies were tagged for this tab yet.
                        </div>
                      )}
                    </TabsContent>
                  );
                })}
              </Tabs>
            </section>
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
