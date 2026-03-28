import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { HoroscopeCard } from '../components/HoroscopeCard';
import { ZodiacCard } from '../components/ZodiacCard';
import { DOBBanner, DOBModal } from '../components/DOBPrompt';
import { SEO } from '../components/SEO';
import { HoroscopeShareCard, ShareButtons } from '../components/ShareCard';
import { ArrowLeft, Star } from 'lucide-react';
import { useHoroscope, ZODIAC_MAP } from '../hooks/useHoroscope';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const DailyHoroscope = () => {
  const navigate = useNavigate();
  const { primarySign, favourites, favouritesMeta, dobDone, saveDOB, toggleFavourite, dismissDOBPrompt, isFavourite } = useHoroscope();
  const shareCardRef = useRef(null);

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
    try { const r = await axios.get(`${API}/horoscope/${sign}/daily`); setHoroscope(r.data); }
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
    if (sign && signs.find(s => s.id === sign.id)) {
      setSelectedSign(sign.id);
    }
  };

  const handleDismiss = () => { dismissDOBPrompt(); setShowModal(false); };

  const schema = {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: 'Daily Horoscope — All 12 Zodiac Signs',
    description: 'Read today\'s free Vedic daily horoscope for all 12 zodiac signs. AI-powered personalised predictions.',
    url: 'https://everydayhoroscope.in/horoscope/daily',
    publisher: { '@type': 'Organization', name: 'Everyday Horoscope', url: 'https://everydayhoroscope.in' },
  };

  return (
    <div className="min-h-screen pb-24 lg:pb-0">
      <SEO
        title="Daily Horoscope — All 12 Zodiac Signs"
        description="Read today's free Vedic daily horoscope for all 12 zodiac signs. AI-powered personalised predictions rooted in 5,000 years of ancient wisdom."
        url="https://everydayhoroscope.in/horoscope/daily"
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
              ✦ Daily Vedic Horoscope
            </div>
            <h1 className="text-4xl font-playfair font-semibold mb-3">Daily Horoscope</h1>
            <p className="text-muted-foreground">Select your zodiac sign to receive today's personalised Vedic guidance</p>
          </div>

          {!dobDone && !showModal && (
            <DOBBanner onSave={handleDOBSave} onDismiss={handleDismiss} />
          )}

          {favouritesMeta.length > 0 && !selectedSign && (
            <div className="mb-6">
              <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3 flex items-center gap-1.5">
                <Star className="h-3.5 w-3.5 fill-gold" /> My Favourite Signs
              </p>
              <div className="flex flex-wrap gap-2">
                {favouritesMeta.map(sign => (
                  <button
                    key={sign.id}
                    onClick={() => handleSignSelect(sign)}
                    className="flex items-center gap-2 px-3 py-2 rounded-full border border-gold/40 bg-gold/5 hover:bg-gold/15 transition-colors text-sm font-medium"
                  >
                    <span>{sign.symbol}</span>
                    <span>{sign.name}</span>
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
                  <ZodiacCard
                    key={sign.id}
                    sign={sign}
                    onClick={handleSignSelect}
                    selected={false}
                    isFavourite={isFavourite(sign.id)}
                    onToggleFavourite={toggleFavourite}
                  />
                ))}
              </div>
            )
          ) : (
            <div className="space-y-6">
              <div className="flex items-center gap-3">
                <Button onClick={() => setSelectedSign(null)} variant="outline" size="sm">Change Sign</Button>
                {selectedSignData && (
                  <button
                    onClick={() => toggleFavourite(selectedSign)}
                    className={`flex items-center gap-1.5 text-sm px-3 py-1.5 rounded-full border transition-colors ${
                      isFavourite(selectedSign)
                        ? 'border-gold bg-gold/10 text-gold'
                        : 'border-border text-muted-foreground hover:border-gold/50 hover:text-gold'
                    }`}
                  >
                    <Star className={`h-3.5 w-3.5 ${isFavourite(selectedSign) ? 'fill-gold' : ''}`} />
                    {isFavourite(selectedSign) ? 'Saved to Favourites' : 'Add to Favourites'}
                  </button>
                )}
              </div>
              <HoroscopeCard
                title="Today's Horoscope"
                content={horoscope?.content}
                isLoading={loading}
                type="daily"
                signName={selectedSignData?.name}
                signSymbol={selectedSignData?.symbol}
              />
              {!loading && horoscope?.content && (
                <Card className="border border-gold/20 p-5">
                  <ShareButtons
                    pageUrl={`https://www.everydayhoroscope.in/horoscope/daily`}
                    shareText={`${selectedSignData?.name} Daily Horoscope — ${new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })} ✦`}
                    cardRef={shareCardRef}
                    filename={`horoscope-${selectedSign}-daily`}
                    fbPageCaption={`⭐ ${selectedSignData?.name} Daily Horoscope — ${new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })}

${horoscope?.content?.overview?.slice(0, 200)}...

🔮 Visit everydayhoroscope.in for your complete horoscope
#${selectedSignData?.name}Horoscope #DailyHoroscope #VedicAstrology #EverydayHoroscope`}
                  />
                </Card>
              )}
              <HoroscopeShareCard
                cardRef={shareCardRef}
                signName={selectedSignData?.name}
                signSymbol={selectedSignData?.symbol}
                signDates={selectedSignData?.dates}
                signElement={selectedSignData?.element}
                horoscopeType="daily"
                content={horoscope?.content}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
