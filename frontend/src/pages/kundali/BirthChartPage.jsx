import { SEO } from '../../components/SEO';
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../../components/ui/button';
import { Card } from '../../components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '../../components/ui/collapsible';
import { Sparkles, ArrowLeft, Crown, Check, ChevronDown, Loader2, Orbit, ScrollText } from 'lucide-react';
import { BirthDetailsForm } from '../../components/BirthDetailsForm';
import { BirthChartDisplay } from '../../components/BirthChartDisplay';
import axios from 'axios';
import { Footer } from '../../components/Footer';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const DIGNITY_WEIGHTS = {
  debilitated: 0,
  enemy: 1,
  neutral: 2,
  friendly: 3,
  own_sign: 4,
  moolatrikona: 5,
  exalted: 6,
};

const HOUSE_DOMAIN_MAP = {
  1: 'health',
  2: 'wealth',
  3: 'career',
  4: 'family',
  5: 'children',
  6: 'enemies',
  7: 'marriage',
  8: 'mental',
  9: 'spiritual',
  10: 'career',
  11: 'wealth',
  12: 'mental',
};

const toPlainPlanet = (planetLabel = '') => planetLabel.split('(')[0].trim();

const formatLabel = (value = '') =>
  value
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase());

const scoreAffliction = (planetData = {}) => {
  const dignity = planetData?.dignity || 'neutral';
  const dignityScore = DIGNITY_WEIGHTS[dignity] ?? 2;
  const shadbala = Number(planetData?.shadbala?.total_rupas || 0);
  const minimum = Number(planetData?.shadbala?.minimum_rupas || 0);

  let score = (6 - dignityScore) * 10;
  if (planetData?.combust) score += 14;
  if (planetData?.retrograde) score += 4;
  if (minimum && shadbala) {
    if (shadbala < minimum) {
      score += 12;
    } else {
      score -= 4;
    }
  }
  return score;
};

const deriveAffliction = (planetData = {}) => {
  if (planetData?.combust) return 'combust';
  if (planetData?.dignity === 'debilitated') return 'debilitated';
  if (planetData?.dignity === 'enemy') return 'enemy_sign';
  if (planetData?.retrograde) return 'retrograde';
  if (planetData?.shadbala && planetData.shadbala.total_rupas < planetData.shadbala.minimum_rupas) {
    return 'low_shadbala';
  }
  return 'planetary_weakness';
};

const deriveIntensity = (planetData = {}) => {
  if (planetData?.combust || planetData?.dignity === 'debilitated') return 'severe';
  if (planetData?.dignity === 'enemy') return 'moderate';
  if (planetData?.shadbala && planetData.shadbala.total_rupas < planetData.shadbala.minimum_rupas) {
    return 'moderate';
  }
  return 'mild';
};

const getTopAfflictedPlanets = (report) => {
  const planets = Object.entries(report?.planets || {});
  return planets
    .map(([planetLabel, planetData]) => ({
      key: planetLabel,
      planet: toPlainPlanet(planetLabel),
      house: planetData?.house || null,
      dignity: planetData?.dignity || 'neutral',
      affliction: deriveAffliction(planetData),
      intensity: deriveIntensity(planetData),
      lifeDomain: HOUSE_DOMAIN_MAP[planetData?.house] || 'career',
      score: scoreAffliction(planetData),
      planetData,
    }))
    .sort((left, right) => right.score - left.score)
    .slice(0, 3);
};

const RemedyItemCard = ({ remedy }) => (
  <div className="rounded-sm border border-gold/20 bg-background/80 p-4 space-y-3">
    <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
      <div>
        <p className="font-semibold text-base">{remedy.title}</p>
        <p className="text-xs uppercase tracking-widest text-gold mt-1">
          {`${formatLabel(remedy.tradition)}_${formatLabel(remedy.category)}_${formatLabel(remedy.action_type)}`}
        </p>
      </div>
      <div className="text-xs text-muted-foreground">
        <p>Ease: {formatLabel(remedy.ease)}</p>
        <p>Confidence: {Math.round((remedy.confidence || 0) * 100)}%</p>
      </div>
    </div>
    <p className="text-sm leading-relaxed text-foreground/85">{remedy.description}</p>
    {remedy.behavioral_remedy && (
      <div className="rounded-sm border border-dashed border-gold/30 bg-gold/5 p-3">
        <p className="text-xs uppercase tracking-widest text-gold mb-1">Behavioral Support</p>
        <p className="text-sm text-foreground/80">{remedy.behavioral_remedy}</p>
      </div>
    )}
    <div className="flex flex-wrap gap-3 text-xs text-muted-foreground">
      <span>Duration: {remedy.duration}</span>
      <span>Source: {remedy.source_collection}</span>
      <span>Science: {remedy.science_id}</span>
    </div>
  </div>
);

export const BirthChartPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [birthProfile, setBirthProfile] = useState(null);
  const [birthChart, setBirthChart] = useState(null);
  const [loading, setLoading] = useState({ birthChart: false });
  const [profileLoading, setProfileLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('report');
  const [remediesLoading, setRemediesLoading] = useState(false);
  const [remediesError, setRemediesError] = useState('');
  const [remedyPacks, setRemedyPacks] = useState([]);

  useEffect(() => {
    loadBirthProfile();
  }, []);

  useEffect(() => {
    if (birthChart?.planets) {
      loadRemediesForChart(birthChart);
    } else {
      setRemedyPacks([]);
    }
  }, [birthChart]);

  const loadBirthProfile = async () => {
    const savedProfileId = localStorage.getItem('birth-profile-id');
    if (!savedProfileId) {
      setProfileLoading(false);
      return;
    }
    try {
      const response = await axios.get(`${API}/profile/birth/${savedProfileId}`);
      setBirthProfile(response.data);
    } catch (error) {
      // Profile not found or stale ID — clear so form is usable
      console.error('Stale birth profile ID, clearing cache:', error);
      localStorage.removeItem('birth-profile-id');
      setBirthProfile(null);
    } finally {
      setProfileLoading(false);
    }
  };

  const handleResetProfile = () => {
    localStorage.removeItem('birth-profile-id');
    setBirthProfile(null);
  };

  const handleBirthDetailsSubmit = async (formData) => {
    setLoading({ birthChart: true });
    try {
      const profileResponse = await axios.post(`${API}/profile/birth`, formData);
      localStorage.setItem('birth-profile-id', profileResponse.data.id);
      const profile = profileResponse.data;
      setBirthProfile(profile);
      localStorage.setItem('birth-profile-id', profile.id);
      
      toast.success('Birth details saved successfully!');
      
      const chartResponse = await axios.post(`${API}/birthchart/generate`, {
        profile_id: profile.id
      });
      setBirthChart(chartResponse.data);
      toast.success('Birth chart generated!');
    } catch (error) {
      console.error('Error creating birth profile:', error);
      toast.error('Failed to save birth details. Please try again.');
    } finally {
      setLoading({ birthChart: false });
    }
  };

  const handleGenerateBirthChart = async () => {
    if (!birthProfile) return;
    
    setLoading({ birthChart: true });
    try {
      const response = await axios.post(`${API}/birthchart/generate`, {
        profile_id: birthProfile.id
      });
      setBirthChart(response.data);
      toast.success('Birth chart generated!');
    } catch (error) {
      console.error('Error generating birth chart:', error);
      toast.error('Failed to generate birth chart. Please try again.');
    } finally {
      setLoading({ birthChart: false });
    }
  };

  const loadRemediesForChart = async (chartReport) => {
    const afflictedPlanets = getTopAfflictedPlanets(chartReport);
    if (!afflictedPlanets.length) {
      setRemedyPacks([]);
      return;
    }

    setRemediesLoading(true);
    setRemediesError('');
    try {
      const responses = await Promise.all(
        afflictedPlanets.map(async (planetContext) => {
          const payload = {
            trigger: 'birth_chart',
            planet: planetContext.planet,
            house: planetContext.house,
            affliction: planetContext.affliction,
            dasha_planet: chartReport?.current_dasha?.planet || null,
            life_domain: planetContext.lifeDomain,
            nakshatra: chartReport?.nakshatra?.name || null,
            intensity: planetContext.intensity,
            remedy_type_filter: 'both',
          };
          const response = await axios.post(`${API}/remedies/suggest`, payload);
          return {
            ...planetContext,
            pack: response.data,
          };
        })
      );
      setRemedyPacks(responses);
    } catch (error) {
      console.error('Error loading remedy suggestions:', error);
      setRemediesError('Remedy suggestions are not available yet. Please try again after the engine data is installed.');
      setRemedyPacks([]);
    } finally {
      setRemediesLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <SEO title="Vedic Birth Chart — Your Kundali Report" noindex={true} />
      <div className="max-w-5xl mx-auto">
        <Button
          data-testid="back-to-home"
          onClick={() => navigate('/home')}
          variant="ghost"
          className="mb-6"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Home
        </Button>

        {/* Crown badge + title */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center gap-2 bg-gold/10 border border-gold/30 text-gold px-4 py-1.5 rounded-full text-xs font-semibold uppercase tracking-widest mb-3">
            <Crown className="h-3.5 w-3.5" />
            Vedic Astrology Report · ₹499
          </div>
          <h1 className="text-4xl font-playfair font-semibold mb-2">Birth Chart Analysis</h1>
          <p className="text-muted-foreground text-sm">Your complete Janma Kundali — planets, houses, dashas & personalised guidance</p>
        </div>

        {/* What's included snapshot */}
        <div className="border border-gold/20 rounded-lg bg-gold/5 p-5 mb-8">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-4">What's Included in Your Report</p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-x-8 gap-y-2">
            {[
              'North Indian Kundali Chart', 'Career & Dharma analysis',
              'Ascendant & personality profile', 'Relationships & marriage',
              'Moon sign & Nakshatra reading', 'Health & wellness guidance',
              'All 9 planets in their houses', 'Current & future Dasha periods',
              'Notable Yogas identified', 'Mangal Dosha assessment',
              'Remedies & gemstone guidance', 'PDF download included',
            ].map(item => (
              <div key={item} className="flex items-center gap-2 text-sm text-foreground/80">
                <Check className="h-3.5 w-3.5 text-gold flex-shrink-0" />
                {item}
              </div>
            ))}
          </div>
        </div>

        {profileLoading ? (
          <div className="flex items-center justify-center py-20">
            <Sparkles className="h-8 w-8 text-gold animate-pulse" />
          </div>
        ) : (
          <div className="space-y-6">
          {!birthProfile ? (
            <BirthDetailsForm
              onSubmit={handleBirthDetailsSubmit}
              isLoading={loading.birthChart}
            />
          ) : (
            <>
              <BirthDetailsForm
                existingProfile={birthProfile}
                isLoading={false}
              />
              {!birthChart && (
                <Button
                  data-testid="generate-birthchart"
                  onClick={handleGenerateBirthChart}
                  disabled={loading.birthChart}
                  className="w-full h-12 text-base font-semibold bg-primary hover:bg-gold hover:text-primary-foreground transition-all duration-300"
                >
                  {loading.birthChart ? 'Generating...' : 'Generate Birth Chart'}
                </Button>
              )}
              {birthChart && (
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                  <TabsList className="grid w-full grid-cols-2 mb-6 bg-muted p-1 rounded-sm h-auto">
                    <TabsTrigger value="report" className="text-sm data-[state=active]:bg-background">
                      Report
                    </TabsTrigger>
                    <TabsTrigger value="remedies" className="text-sm data-[state=active]:bg-background">
                      Remedies
                    </TabsTrigger>
                  </TabsList>

                  <TabsContent value="report">
                    <BirthChartDisplay
                      report={birthChart}
                      isLoading={loading.birthChart}
                      profile={birthProfile}
                    />
                  </TabsContent>

                  <TabsContent value="remedies">
                    <Card className="p-6 border-2 border-gold/20 bg-card space-y-5">
                      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                        <div>
                          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-2">
                            Context-Driven Remedy Layer
                          </p>
                          <h3 className="text-2xl font-playfair font-semibold">Remedies For Your Chart</h3>
                          <p className="text-sm text-muted-foreground mt-2 max-w-3xl">
                            These suggestions use the weakest visible planets in your computed chart and return a mixed remedy pack across Jyotish, Lal Kitab, crystal, chakra, and Krishna-ready structures where available.
                          </p>
                        </div>
                        <Button
                          type="button"
                          variant="outline"
                          className="border-gold hover:bg-gold hover:text-primary-foreground"
                          onClick={() => loadRemediesForChart(birthChart)}
                          disabled={remediesLoading}
                        >
                          {remediesLoading ? 'Refreshing...' : 'Refresh Remedies'}
                        </Button>
                      </div>

                      {remediesLoading && (
                        <div className="rounded-sm border border-gold/20 bg-background/70 p-6 flex items-center gap-3 text-sm text-muted-foreground">
                          <Loader2 className="h-5 w-5 animate-spin text-gold" />
                          Building your cross-tradition remedy pack from the current chart context...
                        </div>
                      )}

                      {!remediesLoading && remediesError && (
                        <div className="rounded-sm border border-destructive/30 bg-destructive/5 p-4 text-sm text-foreground/85">
                          {remediesError}
                        </div>
                      )}

                      {!remediesLoading && !remediesError && remedyPacks.length === 0 && (
                        <div className="rounded-sm border border-gold/20 bg-background/70 p-6 text-sm text-muted-foreground">
                          Remedy suggestions will appear here once approved remedy records are available for the current chart context.
                        </div>
                      )}

                      <div className="space-y-4">
                        {remedyPacks.map((entry, index) => (
                          <Collapsible key={`${entry.planet}-${entry.house || index}`} defaultOpen={index === 0}>
                            <div className="rounded-sm border border-gold/20 bg-background/60 overflow-hidden">
                              <CollapsibleTrigger className="w-full text-left p-4 flex items-center justify-between gap-4 hover:bg-gold/5 transition-colors">
                                <div>
                                  <div className="flex items-center gap-2 text-gold text-xs uppercase tracking-widest mb-1">
                                    <Orbit className="h-3.5 w-3.5" />
                                    <span>Planet Trigger</span>
                                  </div>
                                  <p className="font-playfair text-xl font-semibold">{entry.planet}</p>
                                  <p className="text-sm text-muted-foreground mt-1">
                                    House {entry.house || '—'} • {formatLabel(entry.dignity)} • {formatLabel(entry.affliction)}
                                  </p>
                                  <p className="text-sm text-foreground/80 mt-2">
                                    {entry.pack?.context_summary || 'Remedy context unavailable.'}
                                  </p>
                                </div>
                                <ChevronDown className="h-5 w-5 text-gold" />
                              </CollapsibleTrigger>
                              <CollapsibleContent className="border-t border-gold/10">
                                <div className="p-4 space-y-4">
                                  <div className="flex flex-wrap gap-3 text-xs text-muted-foreground">
                                    <span>Life domain: {formatLabel(entry.lifeDomain)}</span>
                                    <span>Intensity: {formatLabel(entry.intensity)}</span>
                                    <span>Mode: {formatLabel(entry.pack?.advisory_mode || 'supportive')}</span>
                                  </div>

                                  {entry.pack?.remedies?.length ? (
                                    <div className="space-y-3">
                                      {entry.pack.remedies.map((remedy) => (
                                        <RemedyItemCard key={remedy.remedy_id} remedy={remedy} />
                                      ))}
                                    </div>
                                  ) : (
                                    <div className="rounded-sm border border-dashed border-border p-4 text-sm text-muted-foreground">
                                      No approved remedies matched this trigger yet.
                                    </div>
                                  )}
                                </div>
                              </CollapsibleContent>
                            </div>
                          </Collapsible>
                        ))}
                      </div>
                    </Card>
                  </TabsContent>
                </Tabs>
              )}
            </>
          )}
          </div>
        )}
      </div>

      {/* ── SEO Content Section ──────────────────────────────────────────── */}
      <section className="bg-muted/30 border-t border-border mt-12 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto space-y-12">

          {/* What is a Birth Chart */}
          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-4">What is a Vedic Birth Chart?</h2>
            <p className="text-muted-foreground leading-relaxed mb-3">
              A Vedic Birth Chart — also known as Janam Kundali, Natal Chart, or Janma Patrika — is a precise astronomical snapshot of the sky at the exact moment and location of your birth. It maps the positions of the Sun, Moon, and seven planets across 12 houses and 12 zodiac signs, creating a unique cosmic blueprint that Vedic astrologers use to interpret your personality, destiny, and life events.
            </p>
            <p className="text-muted-foreground leading-relaxed">
              Unlike a generic horoscope based only on your Sun sign, a full Birth Chart analysis uses your Ascendant (Lagna) as the primary lens — the sign that was rising on the eastern horizon at your birth. This makes every Birth Chart unique, even for twins born minutes apart. The Ascendant determines your house structure, which in turn governs every dimension of life from career and marriage to health and spiritual path.
            </p>
          </div>

          {/* What is included */}
          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-4">What Your Birth Chart Analysis Includes</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {[
                { title: 'North Indian Kundali Chart', desc: 'Your birth chart rendered in traditional North Indian diamond grid format — all 9 Vedic planets placed in their correct houses with Ascendant clearly marked.' },
                { title: 'Ascendant & Personality', desc: 'Your rising sign (Lagna) determines your outward personality, physical appearance, and the framework for your entire chart.' },
                { title: 'Moon Sign (Rashi)', desc: 'Your Moon sign reveals your emotional nature, subconscious patterns, and how you experience and respond to the world internally.' },
                { title: 'Nakshatra Placement', desc: 'Your birth Nakshatra (lunar mansion) is one of the most important placements in Vedic astrology — governing personality nuances, dasha periods, and compatibility.' },
                { title: 'Planetary House Analysis', desc: 'All 9 planets (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Rahu, Ketu) analysed in their houses — their strength, status, and influence on your life.' },
                { title: 'Notable Yogas', desc: 'Special planetary combinations (Yogas) in your chart that amplify or challenge specific areas of life — wealth, career, marriage, or spiritual growth.' },
                { title: 'Career & Dharma', desc: 'Natural aptitudes, best career paths, and the professional themes written into your 10th house and its lord.' },
                { title: 'Relationships & Marriage', desc: '7th house analysis covering partnership nature, ideal spouse qualities, and relationship patterns.' },
                { title: 'Health & Wellness', desc: 'Constitutional analysis based on your Ascendant and planetary placements — identifying vulnerable areas and preventive guidance.' },
                { title: 'Vimshottari Dasha', desc: 'Your current planetary period (Mahadasha) and what it means for the next several years of your life.' },
                { title: 'Mangal Dosha Assessment', desc: 'Precise Mangal Dosha detection based on Mars house position, with severity and applicable cancellation rules.' },
                { title: 'Remedies & Guidance', desc: 'Practical Jyotish remedies including gemstone guidance, mantra recommendations, and lifestyle practices.' },
              ].map(({ title, desc }) => (
                <div key={title} className="flex gap-3 p-4 rounded-sm border border-border bg-card">
                  <span className="text-gold mt-0.5">✦</span>
                  <div>
                    <p className="font-semibold text-sm mb-1">{title}</p>
                    <p className="text-xs text-muted-foreground leading-relaxed">{desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* How it works */}
          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-4">How Our Birth Chart Calculation Works</h2>
            <p className="text-muted-foreground leading-relaxed mb-3">
              Our Birth Chart is powered by a two-layer system. Layer 1 uses the Swiss Ephemeris — the gold standard in planetary calculation software — with the Lahiri ayanamsha for Vedic sidereal positioning. Every planet is placed to the exact degree based on your birth date, time, and geographic coordinates. The result is the same every time for the same input — mathematically deterministic, not estimated.
            </p>
            <p className="text-muted-foreground leading-relaxed mb-3">
              Layer 2 applies deep Jyotish interpretation to these calculations. Rather than using pre-written template paragraphs, our AI interprets your specific chart — referencing actual house numbers, planetary degrees, and house lord placements throughout. Every sentence in your report is grounded in your unique chart data.
            </p>
            <p className="text-muted-foreground leading-relaxed">
              Your Ascendant degree is computed using the exact latitude and longitude of your birth city, matched to the precise sidereal time at your moment of birth. Nakshatra and Pada are derived from the Moon's exact degree position. The Vimshottari Dasha start date is calculated from your Nakshatra lord at birth.
            </p>
          </div>

          {/* FAQ */}
          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-6">Frequently Asked Questions</h2>
            <div className="space-y-5">
              {[
                {
                  q: 'Why is my Vedic Sun sign different from my Western sign?',
                  a: "Vedic astrology uses the sidereal zodiac — aligned with actual star constellations — while Western astrology uses the tropical zodiac, which tracks the Sun's relationship to the Earth's equinoxes. Due to the precession of the equinoxes, there is currently about a 23-degree difference between the two systems. This means your Vedic (sidereal) Sun sign will often be one sign earlier than your Western sign. Most Vedic astrologers consider the sidereal system more accurate for predicting life events and timing."
                },
                {
                  q: 'How important is the exact birth time?',
                  a: "Very important. Your Ascendant (Lagna) can change sign every two hours, and even a few minutes can affect which Nakshatra Pada you fall in — changing your Vimshottari Dasha start date. If your birth time is approximate, your planetary positions will still be accurate, but the Ascendant and house cusps may shift. For the most accurate report, use the time from your official birth certificate. If unknown, our system will note the limitation."
                },
                {
                  q: 'What is a Nakshatra and why does it matter?',
                  a: "The zodiac in Vedic astrology is divided into 27 Nakshatras (lunar mansions), each spanning 13 degrees 20 minutes. Your birth Nakshatra is determined by the Moon's position and is one of the most important placements in your chart. It governs your Vimshottari Dasha sequence (the planetary period system), your instinctive personality, and your compatibility in relationships. Each Nakshatra has a ruling planet, a deity, a symbol, and a set of characteristics that are far more nuanced than Sun sign descriptions."
                },
                {
                  q: 'What is Mangal Dosha and is it serious?',
                  a: "Mangal Dosha occurs when Mars is placed in the 1st, 2nd, 4th, 7th, 8th, or 12th house of the Lagna chart. It is associated with challenges in marriage and partnerships. However, Mangal Dosha has numerous cancellation rules — if both partners have it, the dosha cancels. Strong Jupiter in the chart also provides protection. Our report accurately identifies whether Mangal Dosha is present, its severity, applicable cancellation rules in your specific chart, and effective remedies. It is important information, not a cause for alarm."
                },
                {
                  q: 'Can I download my Birth Chart as a PDF?',
                  a: "Yes — once your report is generated, click the Generate PDF button to download a formatted PDF. The PDF includes your North Indian Kundali chart, 12-house map table, planetary positions, and the full interpretation. The PDF is password-protected for your privacy using a personalised formula based on your name and birth date. Your password is shown in a toast notification when the download completes."
                },
                {
                  q: 'Do I need to create a profile to get a Birth Chart?',
                  a: "Yes, a brief registration is required. This allows us to save your birth profile so you can access and re-download your report at any time without re-entering your details. Your profile is securely stored and is never shared. You can delete your account and all associated data at any time from Account Settings."
                },
              ].map(({ q, a }) => (
                <div key={q} className="border border-border rounded-sm p-5">
                  <h3 className="font-semibold mb-2 text-sm">{q}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{a}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Why Vedic */}
          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-4">The North Indian Chart Format</h2>
            <p className="text-muted-foreground leading-relaxed mb-3">
              Your Birth Chart is rendered in the North Indian diamond grid format — the traditional style used by astrologers across North India, Nepal, and parts of South-East Asia. In this format, the Ascendant is always placed in the top centre diamond, with the remaining 11 houses arranged clockwise around the grid. This fixed-sign layout means Aries is always in the same position relative to the Ascendant, making it easy to read planetary relationships at a glance.
            </p>
            <p className="text-muted-foreground leading-relaxed">
              Each house diamond shows the zodiac sign occupying that house, the planets placed there at your birth, and whether any special conditions apply. The Ascendant is marked with "ASC" for clarity. Planet abbreviations follow the standard Vedic convention: Su (Sun), Mo (Moon), Me (Mercury), Ve (Venus), Ma (Mars), Ju (Jupiter), Sa (Saturn), Ra (Rahu), Ke (Ketu).
            </p>
          </div>

        </div>
      </section>

      {/* JSON-LD Structured Data */}
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "Free Vedic Birth Chart Analysis — Janam Kundali Online",
        "description": "Generate your personalised Vedic birth chart online. Includes North Indian Kundali chart, 12-house analysis, nakshatra, planetary positions, Mangal Dosha, Dasha periods, and downloadable PDF.",
        "provider": { "@type": "Organization", "name": "Everyday Horoscope", "url": "https://www.everydayhoroscope.in" },
        "serviceType": "Vedic Astrology Birth Chart",
        "url": "https://www.everydayhoroscope.in/birth-chart",
        "offers": { "@type": "Offer", "price": "499", "priceCurrency": "INR" },
        "faqPage": {
          "@type": "FAQPage",
          "mainEntity": [
            { "@type": "Question", "name": "Why is my Vedic Sun sign different?", "acceptedAnswer": { "@type": "Answer", "text": "Vedic astrology uses the sidereal zodiac aligned with actual star constellations, while Western astrology uses the tropical zodiac. This creates approximately a 23-degree difference." } },
            { "@type": "Question", "name": "How important is exact birth time?", "acceptedAnswer": { "@type": "Answer", "text": "Very important. Your Ascendant changes sign every two hours, and minutes affect your Nakshatra Pada and Dasha timing." } },
          ]
        }
      })}} />

      <Footer />
    </div>
  );
};
