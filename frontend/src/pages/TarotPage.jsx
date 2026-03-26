import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import {
  BookOpen, Sparkles, Star, Loader2,
  Bookmark, BookmarkCheck, Zap, Crown, RotateCcw,
} from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const API  = `${process.env.REACT_APP_BACKEND_URL}/api`;
const SITE = 'https://everydayhoroscope.in';

const FOCUS_AREAS = [
  { value: 'guidance', label: 'Guidance', emoji: '🔮' },
  { value: 'love',     label: 'Love',     emoji: '❤️'  },
  { value: 'career',   label: 'Career',   emoji: '⭐'  },
  { value: 'healing',  label: 'Healing',  emoji: '🌿' },
  { value: 'clarity',  label: 'Clarity',  emoji: '✨' },
];

const schema = {
  '@context': 'https://schema.org',
  '@type': 'WebPage',
  name: 'Tarot Card Reading — Vedic Cross-Reference',
  description: 'Daily Tarot card draw and premium spreads, cross-referenced with Vedic astrology.',
  url: `${SITE}/tarot`,
  publisher: { '@type': 'Organization', name: 'Everyday Horoscope', url: SITE },
};

// ── Card visuals ────────────────────────────────────────────────────────────

function CardBack({ className = '' }) {
  return (
    <div className={`aspect-[2/3] rounded-xl border border-gold/30 bg-gradient-to-b from-neutral-900 to-neutral-950 flex items-center justify-center ${className}`}>
      <div className="w-12 h-12 rounded-full border border-gold/30 flex items-center justify-center">
        <Star className="h-5 w-5 text-gold/30" />
      </div>
    </div>
  );
}

function CardFace({ svgData, cardName, orientation, className = '' }) {
  if (!svgData) {
    return (
      <div className={`aspect-[2/3] rounded-xl bg-gold/5 border border-gold/20 flex items-center justify-center ${className}`}>
        <Star className="h-6 w-6 text-gold/30" />
      </div>
    );
  }
  const svgUrl = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svgData)}`;
  return (
    <div className={`aspect-[2/3] rounded-xl overflow-hidden ${orientation === 'reversed' ? 'rotate-180' : ''} ${className}`}>
      <img src={svgUrl} alt={cardName} className="w-full h-full object-cover" />
    </div>
  );
}

function FlippingCard({ cardId, cardName, orientation, svgData, flipped }) {
  // w-40 = 160px → height = 160 × 3/2 = 240px
  return (
    <div className="w-40 mx-auto" style={{ perspective: '800px' }}>
      <div
        className="relative transition-all duration-700"
        style={{ transformStyle: 'preserve-3d', transform: flipped ? 'rotateY(180deg)' : 'rotateY(0deg)', height: '240px' }}
      >
        <div className="absolute inset-0" style={{ backfaceVisibility: 'hidden' }}>
          <CardBack />
        </div>
        <div className="absolute inset-0" style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}>
          <CardFace svgData={svgData} cardName={cardName} orientation={orientation} />
        </div>
      </div>
    </div>
  );
}

function OrientationBadge({ orientation }) {
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
      orientation === 'upright' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-orange-500/10 text-orange-400'
    }`}>
      {orientation === 'upright' ? '↑ Upright' : '↓ Reversed'}
    </span>
  );
}

// ── Main component ──────────────────────────────────────────────────────────

export const TarotPage = () => {
  const { user }   = useAuth();
  const navigate   = useNavigate();
  const sceneTimer = useRef(null);

  const [cardSVGs,       setCardSVGs]       = useState({});
  const [activeTab,      setActiveTab]      = useState('daily');
  const [focusArea,      setFocusArea]      = useState('guidance');
  const [question,       setQuestion]       = useState('');
  const [reading,        setReading]        = useState(null);
  const [spreads,        setSpreads]        = useState([]);
  const [history,        setHistory]        = useState([]);
  const [loading,        setLoading]        = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [sceneIndex,     setSceneIndex]     = useState(0);
  const [playing,        setPlaying]        = useState(false);
  const [cardFlipped,    setCardFlipped]    = useState(false);
  const [spreadQuestion, setSpreadQuestion] = useState('');
  const [selectedSpreadId, setSelectedSpreadId] = useState(null);

  // Load card SVG bundle from frontend/public/tarot_cards.json
  useEffect(() => {
    fetch('/tarot_cards.json').then(r => r.json()).then(setCardSVGs).catch(() => {});
  }, []);

  useEffect(() => {
    fetchSpreads();
    if (user) checkTodayReading();
  }, [user]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (activeTab === 'history' && user) fetchHistory();
  }, [activeTab, user]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => () => clearTimeout(sceneTimer.current), []);

  // Flip card after scene sequence ends
  useEffect(() => {
    if (!playing && reading && !cardFlipped) {
      setTimeout(() => setCardFlipped(true), 400);
    }
  }, [playing, reading]); // eslint-disable-line react-hooks/exhaustive-deps

  // ── API helpers ───────────────────────────────────────────────────────────

  const fetchSpreads = async () => {
    try {
      const res = await axios.get(`${API}/tarot/spreads`);
      setSpreads(res.data.spreads || []);
    } catch {}
  };

  const checkTodayReading = async () => {
    try {
      const res = await axios.get(`${API}/tarot/daily/today`, { withCredentials: true });
      if (res.data.already_drawn && res.data.reading) {
        setReading(res.data.reading);
        setSceneIndex((res.data.reading.scenes?.length || 1) - 1);
        setCardFlipped(true);
      }
    } catch {}
  };

  const fetchHistory = async () => {
    setHistoryLoading(true);
    try {
      const res = await axios.get(`${API}/tarot/history`, { withCredentials: true });
      setHistory(res.data.history || []);
    } catch {
      toast.error('Could not load history');
    } finally {
      setHistoryLoading(false);
    }
  };

  const startSceneSequence = (scenes) => {
    setSceneIndex(0);
    setPlaying(true);
    setCardFlipped(false);
    let idx = 0;
    const advance = () => {
      idx++;
      if (idx < scenes.length) {
        setSceneIndex(idx);
        sceneTimer.current = setTimeout(advance, scenes[idx]?.duration_ms || 2500);
      } else {
        setPlaying(false);
      }
    };
    sceneTimer.current = setTimeout(advance, scenes[0]?.duration_ms || 2500);
  };

  const handleDraw = async () => {
    if (!user) { navigate('/login'); return; }
    setLoading(true);
    setReading(null);
    setCardFlipped(false);
    try {
      const res = await axios.post(`${API}/tarot/daily/draw`, {
        focus_area: focusArea,
        question: question || null,
        depth_level: 'simple',
      }, { withCredentials: true });
      const r = res.data.reading;
      setReading(r);
      if (res.data.message === 'Already drawn today.') {
        toast.info("Today's card already drawn — showing your reading.");
        setSceneIndex((r.scenes?.length || 1) - 1);
        setCardFlipped(true);
      } else {
        toast.success(`+${res.data.xp_earned} XP earned!`);
        startSceneSequence(r.scenes || []);
      }
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Could not draw card');
    } finally {
      setLoading(false);
    }
  };

  const handleSpreadGenerate = async (spread) => {
    if (!user) { navigate('/login'); return; }
    setSelectedSpreadId(spread.spread_id);
    setLoading(true);
    setReading(null);
    setCardFlipped(false);
    try {
      const res = await axios.post(`${API}/tarot/spread/generate`, {
        spread_id: spread.spread_id,
        focus_area: focusArea,
        question: spreadQuestion || null,
      }, { withCredentials: true });
      setReading(res.data.reading);
      setActiveTab('daily');
      toast.success(`+${res.data.xp_earned} XP earned!`);
      startSceneSequence(res.data.reading.scenes || []);
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Could not generate spread');
    } finally {
      setLoading(false);
      setSelectedSpreadId(null);
    }
  };

  const toggleBookmark = async (reportId, current) => {
    try {
      await axios.post(`${API}/tarot/bookmark`,
        { report_id: reportId, bookmarked: !current },
        { withCredentials: true },
      );
      if (reading?.report_id === reportId) setReading(r => ({ ...r, bookmarked: !current }));
      setHistory(h => h.map(i => i.report_id === reportId ? { ...i, bookmarked: !current } : i));
      toast.success(!current ? 'Bookmarked' : 'Removed bookmark');
    } catch {
      toast.error('Could not update bookmark');
    }
  };

  const resetDraw = () => {
    clearTimeout(sceneTimer.current);
    setReading(null);
    setCardFlipped(false);
    setPlaying(false);
  };

  // ── Derived ───────────────────────────────────────────────────────────────

  const currentScene = reading?.scenes?.[sceneIndex];
  const primaryCard  = reading?.cards?.[0];
  const primarySVG   = primaryCard ? cardSVGs[primaryCard.card_id] : null;

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <div className="max-w-2xl mx-auto px-4 py-10">
      <SEO
        title="Tarot Card Reading — Vedic Cross-Reference"
        description="Daily Tarot card draw and premium spreads. Western Tarot cross-referenced with Vedic astrology for deeper guidance."
        url={`${SITE}/tarot`}
        schema={schema}
      />

      {/* Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
          <BookOpen className="h-3 w-3" /> Vedic Tarot
        </div>
        <h1 className="text-3xl font-playfair font-semibold mb-2">Tarot Reading</h1>
        <p className="text-muted-foreground">Western Tarot cross-referenced with Vedic astrology for deeper cosmic guidance.</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-border mb-8">
        {[
          { key: 'daily',   label: 'Daily Draw' },
          { key: 'spreads', label: 'Spreads' },
          { key: 'history', label: 'History', disabled: !user },
        ].map(t => (
          <button key={t.key} onClick={() => !t.disabled && setActiveTab(t.key)} disabled={t.disabled}
            className={`px-4 py-2.5 text-sm font-medium transition-colors ${
              activeTab === t.key ? 'border-b-2 border-gold text-gold' :
              t.disabled ? 'text-muted-foreground/40 cursor-not-allowed' : 'text-muted-foreground hover:text-foreground'
            }`}>{t.label}
          </button>
        ))}
      </div>

      {/* ── DAILY DRAW TAB ── */}
      {activeTab === 'daily' && (
        <div className="space-y-5">

          {/* Scene player (shown while playing) */}
          {reading && currentScene && playing && (
            <Card className="p-6 border border-gold/30 bg-gold/5 text-center">
              <p className="text-xs text-gold uppercase tracking-widest mb-3">
                {currentScene.scene_type.replace('_', ' ')}
              </p>
              {currentScene.title && (
                <p className="font-playfair text-xl font-semibold mb-3">{currentScene.title}</p>
              )}
              <p className="text-sm text-foreground leading-relaxed">{currentScene.text}</p>
              <div className="flex justify-center gap-1.5 mt-4">
                {reading.scenes.map((_, i) => (
                  <div key={i} className={`rounded-full transition-all ${
                    i === sceneIndex ? 'bg-gold w-4 h-1.5' : 'bg-muted-foreground/30 w-1.5 h-1.5'
                  }`} />
                ))}
              </div>
            </Card>
          )}

          {/* Card reveal (shown after scene sequence) */}
          {reading && !playing && primaryCard && (
            <>
              <FlippingCard
                cardId={primaryCard.card_id}
                cardName={primaryCard.name}
                orientation={primaryCard.orientation}
                svgData={primarySVG}
                flipped={cardFlipped}
              />

              <Card className="p-5 border border-border">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2 flex-wrap">
                      <Star className="h-4 w-4 text-gold flex-shrink-0" />
                      <p className="font-semibold">{primaryCard.name}</p>
                      <OrientationBadge orientation={primaryCard.orientation} />
                    </div>
                    <p className="text-xs text-muted-foreground mb-1">{primaryCard.position_label}</p>
                    <p className="text-sm">{primaryCard.meaning_snippet}</p>
                  </div>
                  <button onClick={() => toggleBookmark(reading.report_id, reading.bookmarked)}
                    className="text-muted-foreground hover:text-gold transition-colors flex-shrink-0">
                    {reading.bookmarked
                      ? <BookmarkCheck className="h-4 w-4 text-gold" />
                      : <Bookmark className="h-4 w-4" />}
                  </button>
                </div>
                {reading.affirmation && (
                  <div className="mt-4 pt-4 border-t border-border">
                    <p className="text-xs text-gold uppercase tracking-widest mb-1">Affirmation</p>
                    <p className="text-sm italic">"{reading.affirmation}"</p>
                  </div>
                )}
              </Card>

              {/* Multi-card spread grid */}
              {reading.cards?.length > 1 && (
                <Card className="p-5 border border-border">
                  <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-4">The Spread</p>
                  <div className="grid grid-cols-3 gap-4">
                    {reading.cards.map(card => (
                      <div key={card.card_id + card.position_code} className="text-center">
                        <CardFace
                          svgData={cardSVGs[card.card_id]}
                          cardName={card.name}
                          orientation={card.orientation}
                          className="mb-2"
                        />
                        <p className="text-xs text-muted-foreground mb-0.5">{card.position_label}</p>
                        <p className="text-xs font-semibold mb-1 leading-tight">{card.name}</p>
                        <OrientationBadge orientation={card.orientation} />
                        <p className="text-xs text-muted-foreground mt-1">{card.meaning_snippet}</p>
                      </div>
                    ))}
                  </div>
                </Card>
              )}
            </>
          )}

          {/* Draw controls (no reading yet) */}
          {!reading && !loading && (
            <>
              <Card className="p-5 border border-border">
                <p className="text-sm font-medium mb-3">Focus Area</p>
                <div className="flex flex-wrap gap-2 mb-4">
                  {FOCUS_AREAS.map(f => (
                    <button key={f.value} onClick={() => setFocusArea(f.value)}
                      className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                        focusArea === f.value
                          ? 'bg-gold text-primary-foreground'
                          : 'border border-border hover:border-gold/50 text-muted-foreground'
                      }`}>{f.emoji} {f.label}
                    </button>
                  ))}
                </div>
                <input
                  type="text"
                  value={question}
                  onChange={e => setQuestion(e.target.value)}
                  placeholder="Optional: ask the cards a specific question..."
                  className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40"
                />
              </Card>

              {/* Face-down card grid */}
              <div className="grid grid-cols-3 gap-3">
                {[0, 1, 2, 3, 4, 5].map(i => <CardBack key={i} />)}
              </div>
            </>
          )}

          {loading && (
            <div className="text-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-gold mx-auto mb-3" />
              <p className="text-sm text-muted-foreground">The cards are being drawn...</p>
            </div>
          )}

          {/* CTA button */}
          {!loading && (
            <div className="space-y-3">
              {!reading ? (
                <Button onClick={handleDraw}
                  className="w-full bg-gold hover:bg-gold/90 text-primary-foreground font-semibold gap-2">
                  <Sparkles className="h-4 w-4" />
                  {user ? "Draw Today's Card" : 'Sign In to Draw'}
                </Button>
              ) : (
                <Button onClick={resetDraw} variant="outline" className="w-full border-border gap-2">
                  <RotateCcw className="h-4 w-4" />
                  Draw Again Tomorrow
                </Button>
              )}
              {!user && (
                <p className="text-center text-xs text-muted-foreground">
                  Free account required to save your readings
                </p>
              )}
            </div>
          )}
        </div>
      )}

      {/* ── SPREADS TAB ── */}
      {activeTab === 'spreads' && (
        <div className="space-y-4">
          <p className="text-sm text-muted-foreground">
            Premium 3-card spreads — deeper readings for specific areas of life.
          </p>

          <input
            type="text"
            value={spreadQuestion}
            onChange={e => setSpreadQuestion(e.target.value)}
            placeholder="Your question for the spread..."
            className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40"
          />

          <div>
            <p className="text-xs text-muted-foreground mb-2">Focus Area</p>
            <div className="flex flex-wrap gap-2">
              {FOCUS_AREAS.map(f => (
                <button key={f.value} onClick={() => setFocusArea(f.value)}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-all ${
                    focusArea === f.value
                      ? 'bg-gold text-primary-foreground'
                      : 'border border-border text-muted-foreground hover:border-gold/50'
                  }`}>{f.emoji} {f.label}
                </button>
              ))}
            </div>
          </div>

          {spreads.map(spread => (
            <Card key={spread.spread_id} className="p-5 border border-border hover:border-gold/30 transition-all">
              <div className="flex items-start gap-3">
                <div className="w-9 h-9 rounded-lg bg-gold/10 flex items-center justify-center flex-shrink-0">
                  <Crown className="h-4 w-4 text-gold" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <p className="font-semibold text-sm">{spread.name}</p>
                    <span className="text-xs border border-gold/30 text-gold px-2 py-0.5 rounded-full">
                      {spread.card_count} cards
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground mb-1">{spread.description}</p>
                  <p className="text-xs text-muted-foreground mb-3">
                    {spread.positions.join(' · ')}
                  </p>
                  <Button
                    onClick={() => handleSpreadGenerate(spread)}
                    disabled={loading}
                    size="sm"
                    className="bg-gold hover:bg-gold/90 text-primary-foreground gap-1.5"
                  >
                    {loading && selectedSpreadId === spread.spread_id
                      ? <><Loader2 className="h-3 w-3 animate-spin" /> Drawing...</>
                      : <><Zap className="h-3 w-3" /> Draw Spread</>}
                  </Button>
                </div>
              </div>
            </Card>
          ))}

          {!user && (
            <div className="text-center py-6">
              <p className="text-sm text-muted-foreground mb-3">Sign in to draw a spread</p>
              <Button onClick={() => navigate('/login')} variant="outline" size="sm">Sign In</Button>
            </div>
          )}
        </div>
      )}

      {/* ── HISTORY TAB ── */}
      {activeTab === 'history' && (
        <div className="space-y-3">
          {historyLoading && (
            <div className="text-center py-12">
              <Loader2 className="h-6 w-6 animate-spin text-gold mx-auto" />
            </div>
          )}
          {!historyLoading && history.length === 0 && (
            <div className="text-center py-12">
              <BookOpen className="h-10 w-10 text-muted-foreground/30 mx-auto mb-3" />
              <p className="text-muted-foreground">No readings yet. Draw your first card.</p>
              <Button onClick={() => setActiveTab('daily')}
                className="mt-4 bg-gold hover:bg-gold/90 text-primary-foreground" size="sm">
                Draw Now
              </Button>
            </div>
          )}
          {history.map(item => {
            const card = item.cards?.[0];
            const dateStr = item.created_at
              ? new Date(item.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
              : '';
            return (
              <Card key={item.id} className="p-4 border border-border hover:border-gold/30 transition-colors">
                <div className="flex items-start gap-3">
                  {/* Thumbnail */}
                  <div className="w-10 flex-shrink-0">
                    {card && cardSVGs[card.card_id]
                      ? <CardFace svgData={cardSVGs[card.card_id]} cardName={card.name} orientation={card.orientation} />
                      : <div className="aspect-[2/3] rounded bg-gold/10 flex items-center justify-center">
                          <Star className="h-3 w-3 text-gold/40" />
                        </div>
                    }
                  </div>
                  {/* Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-0.5 flex-wrap">
                      {card && <p className="font-medium text-sm">{card.name}</p>}
                      {card && <OrientationBadge orientation={card.orientation} />}
                    </div>
                    {item.focus_area && (
                      <p className="text-xs text-muted-foreground capitalize">{item.focus_area}</p>
                    )}
                    {item.affirmation && (
                      <p className="text-xs text-muted-foreground/70 italic mt-0.5 line-clamp-1">
                        "{item.affirmation}"
                      </p>
                    )}
                    <p className="text-xs text-muted-foreground mt-1">{dateStr}</p>
                  </div>
                  {/* Bookmark */}
                  <button
                    onClick={() => toggleBookmark(item.report_id, item.bookmarked)}
                    className="text-muted-foreground hover:text-gold transition-colors flex-shrink-0"
                  >
                    {item.bookmarked
                      ? <BookmarkCheck className="h-4 w-4 text-gold" />
                      : <Bookmark className="h-4 w-4" />}
                  </button>
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};
