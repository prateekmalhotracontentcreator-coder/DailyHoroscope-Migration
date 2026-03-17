import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { HoroscopeCard } from '../components/HoroscopeCard';
import { ZodiacCard } from '../components/ZodiacCard';
import { Header } from '../components/Header';
import { SEO } from '../components/SEO';
import { ArrowLeft } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const DailyHoroscope = () => {
  const navigate = useNavigate();
  const [signs, setSigns] = useState([]);
  const [selectedSign, setSelectedSign] = useState(localStorage.getItem('selected-sign') || null);
  const [horoscope, setHoroscope] = useState(null);
  const [loading, setLoading] = useState(false);
  const [signsLoading, setSignsLoading] = useState(true);

  useEffect(() => {
    fetchSigns();
    if (selectedSign) {
      fetchHoroscope(selectedSign);
    }
  }, [selectedSign]);

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
    <div className="min-h-screen">
      <SEO
        title="Daily Horoscope — All 12 Zodiac Signs"
        description="Read today's daily horoscope for all 12 zodiac signs. Free AI-powered astrological predictions for Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, and Pisces."
        url="https://everydayhoroscope.in/horoscope/daily"
        schema={{
          "@context": "https://schema.org",
          "@type": "FAQPage",
          "mainEntity": [
            { "@type": "Question", "name": "Is the daily horoscope free?", "acceptedAnswer": { "@type": "Answer", "text": "Yes, daily horoscopes for all 12 zodiac signs are completely free on Everyday Horoscope." } },
            { "@type": "Question", "name": "How often is the daily horoscope updated?", "acceptedAnswer": { "@type": "Answer", "text": "Daily horoscopes are refreshed every midnight IST using AI-powered Vedic astrology analysis." } }
          ]
        }}
      />
      <Header />
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

          <h1 className="text-4xl font-playfair font-semibold mb-8 text-center">Daily Horoscope</h1>

          {!selectedSign ? (
            <>
              <p className="text-center text-muted-foreground mb-8">Select your zodiac sign</p>
              {signsLoading ? (
                <div className="text-center py-12">
                  <p className="text-muted-foreground">Loading zodiac signs...</p>
                </div>
              ) : (
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                  {signs.map((sign) => (
                    <ZodiacCard
                      key={sign.id}
                      sign={sign}
                      onClick={handleSignSelect}
                      selected={false}
                    />
                  ))}
                </div>
              )}
            </>
          ) : (
            <div className="space-y-6">
              <Button
                onClick={() => setSelectedSign(null)}
                variant="outline"
                size="sm"
              >
                Change Sign
              </Button>
              <HoroscopeCard
                title="Today's Horoscope"
                content={horoscope?.content}
                isLoading={loading}
                type="daily"
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
