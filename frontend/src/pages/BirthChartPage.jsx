import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Sparkles, ArrowLeft } from 'lucide-react';
import { BirthDetailsForm } from '../components/BirthDetailsForm';
import { BirthChartDisplay } from '../components/BirthChartDisplay';
import axios from 'axios';
import { Footer } from '../components/Footer';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const BirthChartPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [birthProfile, setBirthProfile] = useState(null);
  const [birthChart, setBirthChart] = useState(null);
  const [loading, setLoading] = useState({ birthChart: false });
  const [profileLoading, setProfileLoading] = useState(true);

  useEffect(() => {
    loadBirthProfile();
  }, []);

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

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
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

        <h1 className="text-4xl font-playfair font-semibold mb-8 text-center">Birth Chart Analysis</h1>

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
              <BirthChartDisplay
                report={birthChart}
                isLoading={loading.birthChart}
                profile={birthProfile}
              />
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

          {/* What's included */}
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
                  a: 'Vedic astrology uses the sidereal zodiac — aligned with actual star constellations — while Western astrology uses the tropical zodiac, which tracks the Sun's relationship to the Earth's equinoxes. Due to the precession of the equinoxes, there is currently about a 23-degree difference between the two systems. This means your Vedic (sidereal) Sun sign will often be one sign earlier than your Western sign. Most Vedic astrologers consider the sidereal system more accurate for predicting life events and timing.'
                },
                {
                  q: 'How important is the exact birth time?',
                  a: 'Very important. Your Ascendant (Lagna) can change sign every two hours, and even a few minutes can affect which Nakshatra Pada you fall in — changing your Vimshottari Dasha start date. If your birth time is approximate, your planetary positions will still be accurate, but the Ascendant and house cusps may shift. For the most accurate report, use the time from your official birth certificate. If unknown, our system will note the limitation.'
                },
                {
                  q: 'What is a Nakshatra and why does it matter?',
                  a: 'The zodiac in Vedic astrology is divided into 27 Nakshatras (lunar mansions), each spanning 13°20'. Your birth Nakshatra is determined by the Moon's position and is one of the most important placements in your chart. It governs your Vimshottari Dasha sequence (the planetary period system), your instinctive personality, and your compatibility in relationships. Each Nakshatra has a ruling planet, a deity, a symbol, and a set of characteristics that are far more nuanced than Sun sign descriptions.'
                },
                {
                  q: 'What is Mangal Dosha and is it serious?',
                  a: 'Mangal Dosha occurs when Mars is placed in the 1st, 2nd, 4th, 7th, 8th, or 12th house of the Lagna chart. It is associated with challenges in marriage and partnerships. However, Mangal Dosha has numerous cancellation rules — if both partners have it, the dosha cancels. Strong Jupiter in the chart also provides protection. Our report accurately identifies whether Mangal Dosha is present, its severity, applicable cancellation rules in your specific chart, and effective remedies. It is important information, not a cause for alarm.'
                },
                {
                  q: 'Can I download my Birth Chart as a PDF?',
                  a: 'Yes — once your report is generated, click the "Generate PDF" button to download a formatted PDF. The PDF includes your North Indian Kundali chart, 12-house map table, planetary positions, and the full interpretation. The PDF is password-protected for your privacy using a personalised formula based on your name and birth date. Your password is shown in a toast notification when the download completes.'
                },
                {
                  q: 'Do I need to create a profile to get a Birth Chart?',
                  a: 'Yes, a brief registration is required. This allows us to save your birth profile so you can access and re-download your report at any time without re-entering your details. Your profile is securely stored and is never shared. You can delete your account and all associated data at any time from Account Settings.'
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
        "provider": { "@type": "Organization", "name": "Everyday Horoscope", "url": "https://everydayhoroscope.in" },
        "serviceType": "Vedic Astrology Birth Chart",
        "url": "https://everydayhoroscope.in/birth-chart",
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