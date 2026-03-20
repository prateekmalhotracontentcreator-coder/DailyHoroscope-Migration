import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { KundaliMilanForm } from '../components/KundaliMilanForm';
import { KundaliMilanDisplay } from '../components/KundaliMilanDisplay';
import { ArrowLeft } from 'lucide-react';
import axios from 'axios';
import { Footer } from '../components/Footer';
import { toast } from 'sonner';

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

      {/* ── SEO Content Section ──────────────────────────────────────────── */}
      <section className="bg-muted/30 border-t border-border mt-12 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto space-y-12">

          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-4">What is Kundali Milan?</h2>
            <p className="text-muted-foreground leading-relaxed mb-3">
              Kundali Milan — also known as Kundli Matching, Horoscope Matching, or Vivah Milan — is the traditional Vedic astrology process of comparing two birth charts to assess marriage compatibility. It has been practised for thousands of years across India as an essential step before arranging a marriage, providing deep insight into how two people will relate emotionally, mentally, physically, and spiritually.
            </p>
            <p className="text-muted-foreground leading-relaxed">
              Our Kundali Milan uses the classical Ashtakoot (8-fold) Guna Milan system — the same system used by professional astrologers — with fully deterministic calculations powered by Swiss Ephemeris. The compatibility score of 36 Gunas is mathematically calculated from your actual birth chart data and is consistent every time. Claude AI then interprets these scores with detailed prose analysis covering all 8 Kootas, Mangal Dosha, planetary harmony, and personalised remedies.
            </p>
          </div>

          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-4">The 8 Kootas — What We Analyse</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {[
                { title: 'Varna (1 point)', desc: 'Spiritual compatibility and evolutionary alignment. Assesses whether both partners are working toward compatible life purposes and spiritual goals.' },
                { title: 'Vashya (2 points)', desc: 'Dominance and control dynamics in the relationship. Indicates mutual attraction, influence, and who naturally leads in the partnership.' },
                { title: 'Tara (3 points)', desc: 'Health, longevity, and wellbeing compatibility. Calculated from the birth Nakshatra distance between partners — affects overall health and prosperity of the marriage.' },
                { title: 'Yoni (4 points)', desc: 'Physical and intimate compatibility. Derived from the animal symbol of each Nakshatra — one of the most important factors for marital harmony.' },
                { title: 'Graha Maitri (5 points)', desc: 'Mental and intellectual compatibility. Based on the friendship or enmity between the Moon sign lords of both partners. Governs psychological bonding.' },
                { title: 'Gana (6 points)', desc: 'Temperament and nature compatibility. Each Nakshatra belongs to one of three Ganas — Deva (divine), Manushya (human), or Rakshasa (demon). Same Gana = highest compatibility.' },
                { title: 'Bhakoot (7 points)', desc: 'Financial prosperity and longevity of the relationship. Calculated from the relative positions of Moon signs — certain combinations are considered inauspicious for wealth and progeny.' },
                { title: 'Nadi (8 points)', desc: 'Genetic and constitutional compatibility. The highest-weighted Koota. Same Nadi = 0 points (Nadi Dosha). Different Nadi = full 8 points. Governs health of offspring and constitutional harmony.' },
              ].map(({ title, desc }) => (
                <div key={title} className="flex gap-3 p-4 rounded-sm border border-border bg-card">
                  <span className="text-gold mt-0.5">◆</span>
                  <div>
                    <p className="font-semibold text-sm mb-1">{title}</p>
                    <p className="text-xs text-muted-foreground leading-relaxed">{desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-4">How to Interpret Your Score</h2>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
              {[
                { range: '0 – 17', label: 'Not Recommended', color: 'text-red-600 dark:text-red-400', bg: 'bg-red-50 dark:bg-red-950/20', desc: 'Significant incompatibilities. Careful consideration and strong remedies recommended.' },
                { range: '18 – 23', label: 'Average Match', color: 'text-amber-600', bg: 'bg-amber-50 dark:bg-amber-950/20', desc: 'Workable compatibility with conscious effort and understanding.' },
                { range: '24 – 27', label: 'Good Match', color: 'text-blue-600', bg: 'bg-blue-50 dark:bg-blue-950/20', desc: 'Good compatibility — most marriages in India fall in this range.' },
                { range: '28 – 36', label: 'Excellent Match', color: 'text-green-600 dark:text-green-400', bg: 'bg-green-50 dark:bg-green-950/20', desc: 'Outstanding compatibility across most life dimensions.' },
              ].map(({ range, label, color, bg, desc }) => (
                <div key={range} className={`p-4 rounded-sm border border-border ${bg} text-center`}>
                  <p className={`text-xl font-playfair font-bold ${color} mb-1`}>{range}</p>
                  <p className={`text-xs font-semibold ${color} mb-2`}>{label}</p>
                  <p className="text-xs text-muted-foreground leading-relaxed">{desc}</p>
                </div>
              ))}
            </div>
            <p className="text-muted-foreground leading-relaxed text-sm">
              A score above 18 is generally considered acceptable for marriage in classical Jyotish. However, the score alone does not tell the full story — the individual Koota breakdown, presence of Mangal Dosha, and planetary positions of both charts provide a much more nuanced picture. Our detailed analysis covers all these dimensions.
            </p>
          </div>

          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-6">Frequently Asked Questions</h2>
            <div className="space-y-5">
              {[
                { q: "Is Kundali Milan necessary for love marriages?", a: "Many couples in love marriages also use Kundali Milan for insight rather than as a gatekeeping tool. It can reveal potential stress points in the relationship, areas requiring conscious effort, and the best timing for marriage. Even if you have already decided to marry, the detailed analysis provides valuable guidance for navigating your life together." },
                { q: "What is Mangal Dosha and how serious is it?", a: "Mangal Dosha occurs when Mars is placed in the 1st, 2nd, 4th, 7th, 8th, or 12th house of the Lagna chart. It is associated with potential friction in marriage. However, Mangal Dosha has important cancellation rules — if both partners have it, the doshas cancel each other out. Strong Jupiter in either chart also provides significant protection. Our report identifies Mangal Dosha precisely and explains all applicable cancellation rules." },
                { q: "Our score is below 18 — should we not marry?", a: "A low Ashtakoot score does not automatically mean an incompatible marriage. Individual Koota analysis matters more than the total score alone — for example, full Nadi points (8) and full Bhakoot points (7) together represent 15 of the 36 possible points and carry the most weight. Additionally, factors like shared values, communication, and family background are not captured by the score. Many successful marriages have scores below 18. Remedies can also mitigate specific Koota deficiencies." },
                { q: "How accurate are your calculations compared to other platforms?", a: "Our Ashtakoot calculations use Swiss Ephemeris with Lahiri ayanamsha — the same system used by professional astrology software. We follow classical Parashari rules for all 8 Kootas including the correct Vashya (one-way vs mutual), Bhakoot (forward/reverse axis counting), and Gana compatibility tables. Our score for any given birth pair will be consistent with AstroSage and other serious platforms within 1-2 points, with minor differences attributable to differing school-of-thought interpretations (e.g. Chitra Nakshatra Gana attribution)." },
                { q: "Can I download the Kundali Milan report as a PDF?", a: "Yes — premium users can click Generate PDF to download a fully formatted report including both Kundali charts, the Ashtakoot score table, and the complete analysis. The PDF is password-protected using a personalised formula. Your password is displayed when the download completes." },
              ].map(({ q, a }) => (
                <div key={q} className="border border-border rounded-sm p-5">
                  <h3 className="font-semibold mb-2 text-sm">{q}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{a}</p>
                </div>
              ))}
            </div>
          </div>

        </div>
      </section>

      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "Kundali Milan — Free Online Kundli Matching for Marriage",
        "description": "Free Vedic Kundali Milan based on Ashtakoot Guna Milan system. Get compatibility score out of 36 with detailed 8-Koota analysis, Mangal Dosha assessment, and personalised remedies.",
        "provider": { "@type": "Organization", "name": "Everyday Horoscope", "url": "https://everydayhoroscope.in" },
        "serviceType": "Vedic Astrology Compatibility",
        "url": "https://everydayhoroscope.in/kundali-milan",
        "offers": { "@type": "Offer", "price": "999", "priceCurrency": "INR" },
        "faqPage": {
          "@type": "FAQPage",
          "mainEntity": [
            { "@type": "Question", "name": "What is Kundali Milan?", "acceptedAnswer": { "@type": "Answer", "text": "Kundali Milan is the Vedic astrology process of comparing two birth charts using the Ashtakoot (8-fold) Guna Milan system to assess marriage compatibility." } },
            { "@type": "Question", "name": "What is a good Kundali Milan score?", "acceptedAnswer": { "@type": "Answer", "text": "A score above 18 is generally considered acceptable. Scores of 24 and above indicate good compatibility. 28 and above is considered excellent." } },
          ]
        }
      })}} />

      <Footer />
    </div>
  );
};