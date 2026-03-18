import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { SEO } from '../components/SEO';
import { KundaliMilanForm } from '../components/KundaliMilanForm';
import { KundaliMilanDisplay } from '../components/KundaliMilanDisplay';
import { ArrowLeft, ChevronDown, ChevronUp, Heart, Star, Shield, Users } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const FAQ_DATA = [
  {
    q: 'What is Kundali Milan and why is it important?',
    a: 'Kundali Milan (also called Horoscope Matching or Guna Milan) is the Vedic astrology process of comparing two birth charts to determine compatibility for marriage. It analyses 8 key aspects — the Ashtakoota — to assess emotional, physical, mental, spiritual, and financial harmony between prospective partners. A good Guna Milan score helps identify potential challenges before marriage so they can be addressed proactively.',
  },
  {
    q: 'How many Gunas should match for a good marriage?',
    a: 'Out of a maximum of 36 Gunas: a score below 18 is not recommended for marriage; 18–24 is an acceptable match; 24–32 indicates a prosperous and successful marriage; 32–36 is considered an excellent, heaven-made match. However, the Guna score is only one factor — Mangal Dosha, Nadi Dosha, and the Navamsa chart are equally important.',
  },
  {
    q: 'What is Mangal Dosha and how does it affect marriage compatibility?',
    a: 'Mangal Dosha occurs when Mars is placed in the 1st, 2nd, 4th, 7th, 8th, or 12th house of a birth chart. A Manglik person is advised to marry another Manglik, as the doshas cancel each other out. There are also 14 classical cancellation rules (Parivartana) — if any apply, the dosha is neutralised. Our premium report analyses all cancellation rules automatically.',
  },
  {
    q: 'What is Nadi Dosha and why is it the most important Koota?',
    a: 'Nadi Koota carries 8 points — the highest of all 8 Kootas — because it governs health, genetic compatibility, and progeny. Nadi Dosha occurs when both partners share the same Nadi (Vata, Pitta, or Kapha). This is considered the most serious incompatibility as it can affect the health of children and the longevity of the marriage. Certain Nakshatra combinations can cancel Nadi Dosha.',
  },
  {
    q: 'What happens if Kundalis do not match (low score)?',
    a: 'A low score does not mean marriage is impossible. Vedic astrology provides remedies (Upayas) for almost every incompatibility: Mangal Dosha Nivaran Puja, Nadi Dosha remedies, specific mantras, gemstones, and rituals. Our premium Kundali Milan report includes personalised remedy prescriptions based on Engine 7 (Remedial Science) for any doshas identified.',
  },
  {
    q: 'Is Kundali matching by date of birth more accurate than by name?',
    a: 'Yes. Kundali matching by date of birth (Janam Patrika matching) uses precise planetary positions calculated from exact birth details, giving a mathematically accurate Guna Milan score. Name-based matching uses sound vibration numerology and is a rough approximation only. Our system uses actual planetary position calculations for maximum accuracy.',
  },
  {
    q: 'What is the Navamsa (D9) chart and why does it matter for marriage?',
    a: 'The Navamsa chart (D9) is the 9th divisional chart and is called the "hidden marriage chart" in Vedic astrology. While the Rashi (D1) chart shows the general life picture, the Navamsa reveals the deeper nature of the marriage itself — the quality of the relationship, the strength of the 7th house, and long-term compatibility. Our premium report includes Navamsa analysis for both partners.',
  },
  {
    q: 'How is the Guna Milan score calculated?',
    a: 'The score is calculated by comparing the Moon Nakshatra (birth star) and Moon sign of both partners across 8 Kootas: Varna (1 pt) — spiritual compatibility; Vashya (2 pts) — mutual attraction; Tara (3 pts) — birth star harmony; Yoni (4 pts) — physical compatibility; Graha Maitri (5 pts) — mental compatibility; Gana (6 pts) — temperament; Bhakoot (7 pts) — emotional bonding; Nadi (8 pts) — health compatibility. Total = 36 points.',
  },
];

const KOOTA_INFO = [
  { name: 'Varna', pts: 1, meaning: 'Spiritual evolution and work ethic compatibility', detail: 'Categorises individuals into Brahmin (spiritual), Kshatriya (warrior), Vaishya (merchant), or Shudra (service). The groom\'s Varna should be equal to or higher than the bride\'s for harmony.' },
  { name: 'Vashya', pts: 2, meaning: 'Mutual attraction and influence dynamics', detail: 'Determines the natural power balance and attraction between partners. Based on the relationship between the Moon signs of both individuals.' },
  { name: 'Tara', pts: 3, meaning: 'Birth star compatibility and health', detail: 'Compares the birth Nakshatras to assess health, longevity, and well-being compatibility. Calculated by counting from one Nakshatra to the other.' },
  { name: 'Yoni', pts: 4, meaning: 'Physical and intimate compatibility', detail: 'Each Nakshatra is assigned an animal symbol. Compatibility is assessed based on whether the animals are friends, neutral, or enemies. A matching Yoni gives the maximum 4 points.' },
  { name: 'Graha Maitri', pts: 5, meaning: 'Mental compatibility and intellectual bond', detail: 'Examines the friendship between the ruling planets of each partner\'s Moon sign. Friendly planets indicate good mental harmony and shared values.' },
  { name: 'Gana', pts: 6, meaning: 'Nature, temperament, and attitude', detail: 'Nakshatras are classified as Deva (divine), Manushya (human), or Rakshasa (intense). Ideal pairing is same Gana. Deva + Rakshasa is the most challenging combination.' },
  { name: 'Bhakoot', pts: 7, meaning: 'Love, financial prosperity, and family longevity', detail: 'Based on the positional relationship between the Moon signs. The 6-8, 2-12, and 5-9 axis relationships are considered unfavourable for Bhakoot.' },
  { name: 'Nadi', pts: 8, meaning: 'Health, genetic compatibility, and progeny', detail: 'The most important Koota. Each Nakshatra belongs to one of three Nadis: Adi (Vata), Madhya (Pitta), or Antya (Kapha). Same Nadi = Nadi Dosha, which can affect health and children.' },
];

const FAQItem = ({ q, a }) => {
  const [open, setOpen] = useState(false);
  return (
    <div className="border border-border rounded-sm overflow-hidden mb-3">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-5 py-4 text-left hover:bg-muted/30 transition-colors"
      >
        <span className="font-medium text-sm pr-4">{q}</span>
        {open ? <ChevronUp className="h-4 w-4 text-gold flex-shrink-0" /> : <ChevronDown className="h-4 w-4 text-muted-foreground flex-shrink-0" />}
      </button>
      {open && (
        <div className="px-5 pb-4 text-sm text-muted-foreground leading-relaxed border-t border-border pt-3">
          {a}
        </div>
      )}
    </div>
  );
};

export const KundaliMilanPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [kundaliMilan, setKundaliMilan] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleKundaliMilanSubmit = async (data) => {
    setLoading(true);
    try {
      const profile1Response = await axios.post(`${API}/profile/birth`, data.person1);
      const profile2Response = await axios.post(`${API}/profile/birth`, data.person2);

      const person1 = profile1Response.data;
      const person2 = profile2Response.data;

      const milanResponse = await axios.post(`${API}/kundali-milan/generate`, {
        person1_id: person1.id,
        person2_id: person2.id
      });

      setKundaliMilan({
        report: milanResponse.data,
        person1,
        person2
      });

      toast.success('Kundali Milan report generated!');
    } catch (error) {
      console.error('Error generating Kundali Milan:', error);
      toast.error('Failed to generate compatibility report. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const faqSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    'mainEntity': FAQ_DATA.map(item => ({
      '@type': 'Question',
      'name': item.q,
      'acceptedAnswer': { '@type': 'Answer', 'text': item.a },
    })),
  };

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <SEO
        title="Kundali Milan — Free Online Marriage Compatibility Analysis"
        description="Check marriage compatibility with free Kundali Milan. Get your Ashtakoot Guna Milan score out of 36, Mangal Dosha analysis, Nadi Dosha check, and detailed Vedic compatibility report. Most accurate online Kundli matching."
        url="https://everydayhoroscope.in/kundali-milan"
        schema={faqSchema}
      />

      <div className="max-w-5xl mx-auto">
        <Button
          data-testid="back-to-home"
          onClick={() => navigate('/')}
          variant="ghost"
          className="mb-6"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Home
        </Button>

        {/* Page header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
            <Heart className="h-3 w-3" /> Ashtakoot Guna Milan System
          </div>
          <h1 className="text-4xl font-playfair font-semibold mb-3">Kundali Milan</h1>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            The most trusted Vedic astrology method for marriage compatibility. Compare birth charts across 8 Kootas and get your Guna Milan score out of 36 — free.
          </p>
        </div>

        {/* Tool or results */}
        <div className="space-y-6 mb-12">
          {!kundaliMilan ? (
            <KundaliMilanForm
              onSubmit={handleKundaliMilanSubmit}
              isLoading={loading}
            />
          ) : (
            <>
              <KundaliMilanDisplay
                report={kundaliMilan.report}
                person1={kundaliMilan.person1}
                person2={kundaliMilan.person2}
                isLoading={loading}
              />
              <Button
                data-testid="new-kundali-milan"
                onClick={() => setKundaliMilan(null)}
                variant="outline"
                className="w-full h-12 text-base font-semibold border-gold hover:bg-gold hover:text-primary-foreground transition-all duration-300"
              >
                Check Another Compatibility
              </Button>
            </>
          )}
        </div>

        {/* What is Kundali Milan */}
        <section className="mb-12">
          <h2 className="text-2xl font-playfair font-semibold mb-4">What is Kundali Milan?</h2>
          <p className="text-muted-foreground leading-relaxed mb-4">
            Kundali Milan (also called Horoscope Matching, Kundli Matching, or Guna Milan) is the ancient Vedic astrology process of comparing two birth charts to determine compatibility for marriage. It is one of the most important rituals in Hindu marriage tradition, used for thousands of years to assess whether two individuals are suited for a happy and prosperous life together.
          </p>
          <p className="text-muted-foreground leading-relaxed mb-4">
            The process compares the Moon Nakshatra (birth star) and Moon sign of both partners across 8 aspects called Ashtakoota, assigning points to each. The total score out of 36 — the Guna Milan score — indicates the overall compatibility between the couple.
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
            {[
              { icon: Heart, label: 'Emotional Harmony', desc: 'Mental & spiritual bond' },
              { icon: Users, label: 'Physical Compatibility', desc: 'Yoni & temperament' },
              { icon: Shield, label: 'Dosha Analysis', desc: 'Mangal, Nadi, Bhakoot' },
              { icon: Star, label: 'Life Prosperity', desc: 'Financial & family' },
            ].map(({ icon: Icon, label, desc }) => (
              <div key={label} className="p-4 border border-border rounded-sm text-center">
                <Icon className="h-5 w-5 text-gold mx-auto mb-2" />
                <p className="text-sm font-semibold">{label}</p>
                <p className="text-xs text-muted-foreground mt-1">{desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Guna Score table */}
        <section className="mb-12">
          <h2 className="text-2xl font-playfair font-semibold mb-4">Guna Milan Score Guide</h2>
          <div className="border border-border rounded-sm overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-muted/50">
                  <th className="text-left px-5 py-3 font-semibold">Guna Score</th>
                  <th className="text-left px-5 py-3 font-semibold">Compatibility</th>
                  <th className="text-left px-5 py-3 font-semibold">Recommendation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                <tr><td className="px-5 py-3 text-red-500 font-semibold">Below 18</td><td className="px-5 py-3">Poor</td><td className="px-5 py-3 text-muted-foreground">Not recommended without astrologer guidance</td></tr>
                <tr><td className="px-5 py-3 text-amber-500 font-semibold">18 – 24</td><td className="px-5 py-3">Acceptable</td><td className="px-5 py-3 text-muted-foreground">Marriage possible with remedies</td></tr>
                <tr><td className="px-5 py-3 text-green-600 font-semibold">24 – 32</td><td className="px-5 py-3">Good</td><td className="px-5 py-3 text-muted-foreground">Prosperous and successful marriage</td></tr>
                <tr><td className="px-5 py-3 text-gold font-semibold">32 – 36</td><td className="px-5 py-3">Excellent</td><td className="px-5 py-3 text-muted-foreground">Match made in heaven — highly recommended</td></tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* 8 Kootas explained */}
        <section className="mb-12">
          <h2 className="text-2xl font-playfair font-semibold mb-2">The 8 Kootas of Ashtakoot Milan</h2>
          <p className="text-muted-foreground mb-6">Each of the 8 Kootas examines a different aspect of compatibility. Understanding each Koota helps interpret your Guna Milan score accurately.</p>
          <div className="space-y-3">
            {KOOTA_INFO.map((k) => (
              <div key={k.name} className="border border-border rounded-sm p-4">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-semibold text-sm">{k.name} Koota</span>
                  <span className="text-xs text-gold font-semibold bg-gold/10 px-2 py-0.5 rounded-full">{k.pts} {k.pts === 1 ? 'point' : 'points'}</span>
                </div>
                <p className="text-sm text-foreground mb-1">{k.meaning}</p>
                <p className="text-xs text-muted-foreground">{k.detail}</p>
              </div>
            ))}
          </div>
        </section>

        {/* FAQ section */}
        <section className="mb-12">
          <h2 className="text-2xl font-playfair font-semibold mb-6">Kundali Milan — Frequently Asked Questions</h2>
          {FAQ_DATA.map((item, i) => (
            <FAQItem key={i} q={item.q} a={item.a} />
          ))}
        </section>

        {/* CTA */}
        <section className="text-center p-8 border border-gold/30 bg-gold/5 rounded-sm mb-8">
          <p className="font-playfair text-xl font-semibold mb-2">Get the Complete Premium Analysis</p>
          <p className="text-muted-foreground text-sm mb-4">
            Free Kundali Milan gives you the Guna score. The premium report adds Navamsa D9 chart analysis, Dashakoot extended compatibility, Mangal Dosha cancellation rules, auspicious marriage muhurtas, and personalised Vedic remedies.
          </p>
          <Button
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
            className="bg-gold hover:bg-gold/90 text-primary-foreground font-semibold"
          >
            <Heart className="h-4 w-4 mr-2" /> Check Your Compatibility Now
          </Button>
        </section>
      </div>
    </div>
  );
};

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const KundaliMilanPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [kundaliMilan, setKundaliMilan] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleKundaliMilanSubmit = async (data) => {
    setLoading(true);
    try {
      const profile1Response = await axios.post(`${API}/profile/birth`, data.person1);
      const profile2Response = await axios.post(`${API}/profile/birth`, data.person2);
      
      const person1 = profile1Response.data;
      const person2 = profile2Response.data;
      
      const milanResponse = await axios.post(`${API}/kundali-milan/generate`, {
        person1_id: person1.id,
        person2_id: person2.id
      });
      
      setKundaliMilan({
        report: milanResponse.data,
        person1,
        person2
      });
      
      toast.success('Kundali Milan report generated!');
    } catch (error) {
      console.error('Error generating Kundali Milan:', error);
      toast.error('Failed to generate compatibility report. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <SEO
        title="Kundali Milan — Marriage Compatibility Analysis"
        description="Check marriage compatibility with Kundali Milan. Get your Guna Milan score, Mangal Dosha analysis, and relationship compatibility report based on Vedic astrology."
        url="https://everydayhoroscope.in/kundali-milan"
      />
          onClick={() => navigate('/')}
          variant="ghost"
          className="mb-6"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Home
        </Button>

        <h1 className="text-4xl font-playfair font-semibold mb-8 text-center">Kundali Milan</h1>
        <p className="text-center text-muted-foreground mb-8">Marriage Compatibility Analysis</p>

        <div className="space-y-6">
          {!kundaliMilan ? (
            <KundaliMilanForm
              onSubmit={handleKundaliMilanSubmit}
              isLoading={loading}
            />
          ) : (
            <>
              <KundaliMilanDisplay
                report={kundaliMilan.report}
                person1={kundaliMilan.person1}
                person2={kundaliMilan.person2}
                isLoading={loading}
              />
              <Button
                data-testid="new-kundali-milan"
                onClick={() => setKundaliMilan(null)}
                variant="outline"
                className="w-full h-12 text-base font-semibold border-gold hover:bg-gold hover:text-primary-foreground transition-all duration-300"
              >
                Check Another Compatibility
              </Button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};