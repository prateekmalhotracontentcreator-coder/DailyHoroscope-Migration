import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { HoroscopeCard } from '../components/HoroscopeCard';
import { ZodiacCard } from '../components/ZodiacCard';

import { SEO } from '../components/SEO';
import { ArrowLeft } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const DailyHoroscope = () => {
  const navigate = useNavigate();
  const [signs, setSigns] = useState([]);
  const [selectedSign, setSelectedSign] = useState(null);
  const [selectedSignData, setSelectedSignData] = useState(null);
  const [horoscope, setHoroscope] = useState(null);
  const [loading, setLoading] = useState(false);
  const [signsLoading, setSignsLoading] = useState(true);

  useEffect(() => {
    fetchSigns();
  }, []);

  useEffect(() => {
    if (selectedSign && signs.length > 0) {
      const signData = signs.find(s => s.id === selectedSign);
      setSelectedSignData(signData || null);
      fetchHoroscope(selectedSign);
    }
  }, [selectedSign, signs]);

  const fetchSigns = async () => {
    try {
      const response = await axios.get(`${API}/signs`);
      setSigns(response.data);
    } catch (error) {
      console.error('Error fetching signs:', error);
    } finally {
      setSignsLoading(false);
    }
  };

  const fetchHoroscope = async (sign) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/horoscope/${sign}/daily`);
      setHoroscope(response.data);
    } catch (error) {
      console.error('Error fetching horoscope:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSignSelect = (sign) => {
    setSelectedSign(sign.id);
    localStorage.setItem('selected-sign', sign.id);
  };

  return (
    <div className="min-h-screen pb-24 lg:pb-0">
      <SEO
        title="Daily Horoscope — All 12 Zodiac Signs"
        description="Read today's daily horoscope for all 12 zodiac signs. Free Vedic astrology predictions for Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, and Pisces."
        url="https://everydayhoroscope.in/horoscope/daily"
        schema={{
          "@context": "https://schema.org",
          "@type": "FAQPage",
          "mainEntity": [
            { "@type": "Question", "name": "Is the daily horoscope free?", "acceptedAnswer": { "@type": "Answer", "text": "Yes, daily horoscopes for all 12 zodiac signs are completely free on Everyday Horoscope." } },
            { "@type": "Question", "name": "How often is the daily horoscope updated?", "acceptedAnswer": { "@type": "Answer", "text": "Daily horoscopes are refreshed every midnight IST using Vedic astrology analysis." } }
          ]
        }}
      />

      <div className="py-8 px-4 sm:px-6 lg:px-8">
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

          <div className="text-center mb-10">
            <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
              ✦ Daily Vedic Horoscope
            </div>
            <h1 className="text-4xl font-playfair font-semibold mb-3">Daily Horoscope</h1>
            <p className="text-muted-foreground">Select your zodiac sign to receive today's personalised Vedic guidance</p>
          </div>

          {!selectedSign ? (
            <>
              {signsLoading ? (
                <div className="text-center py-12">
                  <p className="text-muted-foreground">Loading zodiac signs...</p>
                </div>
              ) : (
                <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
                  {signs.map((sign) => (
                    <ZodiacCard key={sign.id} sign={sign} onClick={handleSignSelect} selected={false} />
                  ))}
                </div>
              )}
            </>
          ) : (
            <div className="space-y-6">
              <Button onClick={() => setSelectedSign(null)} variant="outline" size="sm">
                Change Sign
              </Button>
              <HoroscopeCard
                title="Today's Horoscope"
                content={horoscope?.content}
                isLoading={loading}
                type="daily"
                signName={selectedSignData?.name}
                signSymbol={selectedSignData?.symbol}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
