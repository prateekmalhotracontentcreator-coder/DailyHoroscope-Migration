import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { HoroscopeCard } from '../components/HoroscopeCard';
import { ZodiacCard } from '../components/ZodiacCard';
import { DOBBanner, DOBModal } from '../components/DOBPrompt';
import { SEO } from '../components/SEO';
import { ArrowLeft, Star } from 'lucide-react';
import { useHoroscope } from '../hooks/useHoroscope';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const MonthlyHoroscope = () => {
  const navigate = useNavigate();
  const { primarySign, favouritesMeta, dobDone, saveDOB, toggleFavourite, dismissDOBPrompt, isFavourite } = useHoroscope();

  const [signs, setSigns] = useState([]);
  const [selectedSign, setSelectedSign] = useState(null);
  const [selectedSignData, setSelectedSignData] = useState(null);
  const [horoscope, setHoroscope] = useState(null);
  const [loading, setLoading] = useState(false);
  const [signsLoading, setSignsLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => { fetchSigns(); }, []);

  useEffect(() => {
    if (!dobDone) {
      const t = setTimeout(() => setShowModal(true), 600);
      return () => clearTimeout(t);
    }
  }, [dobDone]);

  useEffect(() => {
    if (signs.length > 0 && !selectedSign) {
      const saved = primarySign || localStorage.getItem('selected-sign');
      if (saved && signs.find(s => s.id === saved)) setSelectedSign(saved);
    }
  }, [signs, primarySign]);

  useEffect(() => {
    if (selectedSign && signs.length > 0) {
      const signData = signs.find(s => s.id === selectedSign);
      setSelectedSignData(signData || null);
      fetchHoroscope(selectedSign);
    }
  }, [selectedSign, signs]);

  const fetchSigns = async () => {
    try { const r = await axios.get(`${API}/signs`); setSigns(r.data); }
    catch (e) { console.error(e); }
    finally { setSignsLoading(false); }
  };

  const fetchHoroscope = async (sign) => {
    setLoading(true);
    try { const r = await axios.get(`${API}/horoscope/${sign}/monthly`); setHoroscope(r.data); }
    catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  const handleSignSelect = (sign) => {
    setSelectedSign(sign.id);
    localStorage.setItem('selected-sign', sign.id);
  };

  const handleDOBSave = (dob, sign) => {
    saveDOB(dob);
    setShowModal(false);
    if (sign && signs.find(s => s.id === sign.id)) setSelectedSign(sign.id);
  };

  const handleDismiss = () => { dismissDOBPrompt(); setShowModal(false); };

  const schema = {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: 'Monthly Horoscope — Your Month Ahead in the Stars',
    description: 'Free monthly Vedic horoscope for all 12 zodiac signs. Navigate the month ahead with AI-powered cosmic insights.',
    url: 'https://everydayhoroscope.in/horoscope/monthly',
    publisher: { '@type': 'Organization', name: 'Everyday Horoscope', url: 'https://everydayhoroscope.in' },
  };

  return (
    <div className="min-h-screen pb-24 lg:pb-0">
      <SEO
        title="Monthly Horoscope — Your Month Ahead in the Stars"
        description="Read your free monthly Vedic horoscope for all 12 zodiac signs. Navigate the month ahead with AI-powered cosmic insights."
        url="https://everydayhoroscope.in/horoscope/monthly"
        schema={schema}
      />

      {showModal && <DOBModal onSave={handleDOBSave} onDismiss={handleDismiss} />}

      <div className="py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          <Button data-testid="back-to-home" onClick={() => navigate('/')} variant="ghost" className="mb-6">
            <ArrowLeft className="h-4 w-4 mr-2" />Back to Home
          </Button>
          <div className="text-center mb-8">
            <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
              ✦ Monthly Vedic Horoscope
            </div>
            <h1 className="text-4xl font-playfair font-semibold mb-3">Monthly Horoscope</h1>
            <p className="text-muted-foreground">Select your zodiac sign to receive this month's personalised Vedic guidance</p>
          </div>

          {!dobDone && !showModal && <DOBBanner onSave={handleDOBSave} onDismiss={handleDismiss} />}

          {favouritesMeta.length > 0 && !selectedSign && (
            <div className="mb-6">
              <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3 flex items-center gap-1.5">
                <Star className="h-3.5 w-3.5 fill-gold" /> My Favourite Signs
              </p>
              <div className="flex flex-wrap gap-2">
                {favouritesMeta.map(sign => (
                  <button key={sign.id} onClick={() => handleSignSelect(sign)}
                    className="flex items-center gap-2 px-3 py-2 rounded-full border border-gold/40 bg-gold/5 hover:bg-gold/15 transition-colors text-sm font-medium">
                    <span>{sign.symbol}</span><span>{sign.name}</span>
                  </button>
                ))}
              </div>
              <div className="border-t border-border mt-4 pt-4">
                <p className="text-xs text-muted-foreground mb-3">All signs</p>
              </div>
            </div>
          )}

          {!selectedSign ? (
            signsLoading ? (
              <div className="text-center py-12"><p className="text-muted-foreground">Loading zodiac signs...</p></div>
            ) : (
              <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
                {signs.map(sign => (
                  <ZodiacCard key={sign.id} sign={sign} onClick={handleSignSelect} selected={false}
                    isFavourite={isFavourite(sign.id)} onToggleFavourite={toggleFavourite} />
                ))}
              </div>
            )
          ) : (
            <div className="space-y-6">
              <div className="flex items-center gap-3">
                <Button onClick={() => setSelectedSign(null)} variant="outline" size="sm">Change Sign</Button>
                {selectedSignData && (
                  <button onClick={() => toggleFavourite(selectedSign)}
                    className={`flex items-center gap-1.5 text-sm px-3 py-1.5 rounded-full border transition-colors ${
                      isFavourite(selectedSign) ? 'border-gold bg-gold/10 text-gold' : 'border-border text-muted-foreground hover:border-gold/50 hover:text-gold'
                    }`}>
                    <Star className={`h-3.5 w-3.5 ${isFavourite(selectedSign) ? 'fill-gold' : ''}`} />
                    {isFavourite(selectedSign) ? 'Saved to Favourites' : 'Add to Favourites'}
                  </button>
                )}
              </div>
              <HoroscopeCard title="This Month's Horoscope" content={horoscope?.content} isLoading={loading}
                type="monthly" signName={selectedSignData?.name} signSymbol={selectedSignData?.symbol} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
