import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import {
  BookOpen, Sparkles, Star, Loader2, ArrowLeft,
  Bookmark, BookmarkCheck, Zap, ChevronRight, Crown
} from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const FOCUS_AREAS = [
  { value: 'guidance', label: 'Guidance' },
  { value: 'love',     label: 'Love' },
  { value: 'career',   label: 'Career' },
  { value: 'healing',  label: 'Healing' },
  { value: 'clarity',  label: 'Clarity' },
];

const ORIENTATION_BADGE = ({ orientation }) => (
  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
    orientation === 'upright' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-orange-500/10 text-orange-400'
  }`}>
    {orientation === 'upright' ? '↑ Upright' : '↓ Reversed'}
  </span>
);

const schema = {
  '@context': 'https://schema.org',
  '@type': 'WebPage',
  name: 'Tarot Card Reading — Vedic Cross-Reference',
  description: 'Daily Tarot card draw and premium spreads, cross-referenced with Vedic astrology for deeper cosmic guidance.',
  url: 'https://everydayhoroscope.in/tarot',
  publisher: { '@type': 'Organization', name: 'Everyday Horoscope', url: 'https://everydayhoroscope.in' },
};

export const TarotPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('daily'); // daily | spreads | history
  const [focusArea, setFocusArea] = useState('guidance');
  const [question, setQuestion] = useState('');
  const [reading, setReading] = useState(null);
  const [spreads, setSpreads] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [sceneIndex, setSceneIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const sceneTimer = useRef(null);
  const [selectedSpread, setSelectedSpread] = useState(null);
  const [spreadQuestion, setSpreadQuestion] = useState('');

  useEffect(() => {
    fetchSpreads();
    if (user) checkTodayReading();
  }, [user]);

  useEffect(() => {
    if (activeTab === 'history' && user) fetchHistory();
  }, [activeTab, user]);

  useEffect(() => {
    return () => clearTimeout(sceneTimer.current);
  }, []);

  const fetchSpreads = async () => {
    try {
      const res = await axios.get(`${API}/tarot/spreads`);
      setSpreads(res.data.spreads || []);
    } catch {}
  };

  const checkTodayReading = async () => {
    try {
      const res = await axios.get(`${API}/tarot/daily/today`, { withCredentials: true });
      if (res.data.has_reading) {
        setReading(res.data.reading);
        setSceneIndex(res.data.reading.story_scenes?.length - 1 || 0);
      }
    } catch {}
  };

  const fetchHistory = async () => {
    setHistoryLoading(true);
    try {
      const res = await axios.get(`${API}/tarot/history`, { withCredentials: true });
      setHistory(res.data.items || []);
    } catch {
      toast.error('Could not load history');
    } finally {
      setHistoryLoading(false);
    }
  };

  const startSceneSequence = (scenes) => {
    setSceneIndex(0);
    setPlaying(true);
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
    try {
      const res = await axios.post(`${API}/tarot/daily/draw`, {
        focus_area: focusArea,
        question: question || null,
        depth_level: 'simple',
      }, { withCredentials: true });
      setReading(res.data.reading);
      startSceneSequence(res.data.reading.story_scenes || []);
      if (!res.data.cached) toast.success(`+${res.data.gamification?.xp_awarded || 10} XP earned!`);
      else toast.info('Today\'s card already drawn — showing your reading.');
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Could not draw card');
    } finally {
      setLoading(false);
    }
  };

  const handleSpreadGenerate = async (spread) => {
    if (!user) { navigate('/login'); return; }
    setSelectedSpread(spread);
    setLoading(true);
    setReading(null);
    try {
      const res = await axios.post(`${API}/tarot/spread/generate`, {
        spread_code: spread.spread_code,
        question: spreadQuestion || null,
        depth_level: 'detailed',
      }, { withCredentials: true });
      setReading(res.data.reading);
      setActiveTab('daily'); // show result in main area
      startSceneSequence(res.data.reading.story_scenes || []);
      toast.success('Spread generated!');
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Could not generate spread');
    } finally {
      setLoading(false);
    }
  };

  const toggleBookmark = async (reportId, current) => {
    try {
      await axios.post(`${API}/tarot/history/${reportId}/bookmark`, { bookmarked: !current }, { withCredentials: true });
      if (reading?.report_id === reportId) setReading(r => ({ ...r, bookmarked: !current }));
      setHistory(h => h.map(i => i.report_id === reportId ? { ...i, bookmarked: !current } : i));
      toast.success(!current ? 'Bookmarked' : 'Removed bookmark');
    } catch {
      toast.error('Could not update bookmark');
    }
  };

  const openHistoryReading = async (reportId) => {
    try {
      const res = await axios.get(`${API}/tarot/reading/${reportId}`, { withCredentials: true });
      setReading(res.data);
      setSceneIndex((res.data.story_scenes?.length || 1) - 1);
      setActiveTab('daily');
    } catch {
      toast.error('Could not load reading');
    }
  };

  const currentScene = reading?.story_scenes?.[sceneIndex];

  return (
    <div className="max-w-2xl mx-auto px-4 py-10">
      <SEO
        title="Tarot Card Reading — Vedic Cross-Reference"
        description="Daily Tarot card draw and premium spreads. Western Tarot cross-referenced with Vedic astrology for deeper guidance."
        url="https://everydayhoroscope.in/tarot"
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
          <button
            key={t.key}
            onClick={() => !t.disabled && setActiveTab(t.key)}
            disabled={t.disabled}
            className={`px-4 py-2.5 text-sm font-medium transition-colors ${
              activeTab === t.key
                ? 'border-b-2 border-gold text-gold'
                : t.disabled
                ? 'text-muted-foreground/40 cursor-not-allowed'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* DAILY DRAW TAB */}
      {activeTab === 'daily' && (
        <div className="space-y-5">
          {/* Scene player — shown after draw */}
          {reading && currentScene && (
            <Card className={`p-6 border border-gold/30 bg-gold/5 text-center transition-all duration-700 ${
              playing ? 'opacity-100' : 'opacity-100'
            }`}>
              <p className="text-xs text-gold uppercase tracking-widest mb-3">{currentScene.scene_type.replace('_', ' ')}</p>
              {currentScene.title && <p className="font-playfair text-xl font-semibold mb-3">{currentScene.title}</p>}
              <p className="text-sm text-foreground leading-relaxed mb-4">{currentScene.text}</p>
              {currentScene.meta?.orientation && <ORIENTATION_BADGE orientation={currentScene.meta.orientation} />}
              {/* Scene navigation dots */}
              {reading.story_scenes?.length > 1 && (
                <div className="flex justify-center gap-1.5 mt-4">
                  {reading.story_scenes.map((_, i) => (
                    <button
                      key={i}
                      onClick={() => { clearTimeout(sceneTimer.current); setPlaying(false); setSceneIndex(i); }}
                      className={`w-1.5 h-1.5 rounded-full transition-all ${
                        i === sceneIndex ? 'bg-gold w-3' : 'bg-muted-foreground/30'
                      }`}
                    />
                  ))}
                </div>
              )}
            </Card>
          )}

          {/* Card display after sequence complete */}
          {reading && !playing && reading.cards?.length > 0 && (
            <Card className="p-5 border border-border">
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <Star className="h-4 w-4 text-gold" />
                    <p className="font-semibold">{reading.cards[0].name}</p>
                    <ORIENTATION_BADGE orientation={reading.cards[0].orientation} />
                  </div>
                  <p className="text-sm text-muted-foreground">{reading.cards[0].meaning_snippet}</p>
                  {reading.vedic_context_note && (
                    <p className="text-xs text-muted-foreground/70 mt-2 italic">{reading.vedic_context_note}</p>
                  )}
                </div>
                <button
                  onClick={() => toggleBookmark(reading.report_id, reading.bookmarked)}
                  className="text-muted-foreground hover:text-gold transition-colors flex-shrink-0"
                >
                  {reading.bookmarked ? <BookmarkCheck className="h-4 w-4 text-gold" /> : <Bookmark className="h-4 w-4" />}
                </button>
              </div>
              {reading.affirmation && (
                <div className="mt-4 pt-4 border-t border-border">
                  <p className="text-xs text-gold uppercase tracking-widest mb-1">Affirmation</p>
                  <p className="text-sm italic text-foreground">"{reading.affirmation}"</p>
                </div>
              )}
            </Card>
          )}

          {/* Multi-card spread result */}
          {reading && !playing && reading.cards?.length > 1 && (
            <Card className="p-5 border border-border">
              <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-4">The Spread</p>
              <div className="grid grid-cols-3 gap-3">
                {reading.cards.map(card => (
                  <div key={card.card_id + card.position_code} className="text-center p-3 rounded-sm border border-border bg-muted/20">
                    <p className="text-xs text-muted-foreground mb-1">{card.position_label}</p>
                    <p className="text-sm font-semibold mb-1">{card.name}</p>
                    <ORIENTATION_BADGE orientation={card.orientation} />
                    <p className="text-xs text-muted-foreground mt-1">{card.meaning_snippet}</p>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Draw controls — shown when no reading or after completion */}
          {!reading && !loading && (
            <>
              <Card className="p-5 border border-border">
                <p className="text-sm font-medium mb-3">Focus Area</p>
                <div className="flex flex-wrap gap-2 mb-4">
                  {FOCUS_AREAS.map(f => (
                    <button
                      key={f.value}
                      onClick={() => setFocusArea(f.value)}
                      className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                        focusArea === f.value
                          ? 'bg-gold text-primary-foreground'
                          : 'border border-border hover:border-gold/50 text-muted-foreground'
                      }`}
                    >
                      {f.label}
                    </button>
                  ))}
                </div>
                <input
                  type="text"
                  value={question}
                  onChange={e => setQuestion(e.target.value)}
                  placeholder="Optional: enter a specific question for the cards..."
                  className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40"
                />
              </Card>

              {/* Card face-down grid */}
              <div className="grid grid-cols-3 gap-3">
                {[0,1,2,3,4,5].map(i => (
                  <div key={i} className="aspect-[2/3] rounded-sm border border-gold/20 bg-gold/5 flex items-center justify-center">
                    <Star className="h-5 w-5 text-gold/30" />
                  </div>
                ))}
              </div>
            </>
          )}

          {loading && (
            <div className="text-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-gold mx-auto mb-3" />
              <p className="text-sm text-muted-foreground">The cards are being drawn...</p>
            </div>
          )}

          {/* CTA */}
          {!loading && (
            <div className="space-y-3">
              {!reading ? (
                <Button onClick={handleDraw} className="w-full bg-gold hover:bg-gold/90 text-primary-foreground font-semibold gap-2">
                  <Sparkles className="h-4 w-4" />
                  {user ? 'Draw Today\'s Card' : 'Sign In to Draw'}
                </Button>
              ) : (
                <Button onClick={() => { setReading(null); setPlaying(false); }} variant="outline" className="w-full border-border">
                  Draw Again Tomorrow
                </Button>
              )}
              {!user && (
                <p className="text-center text-xs text-muted-foreground">Free account required to save your readings</p>
              )}
            </div>
          )}
        </div>
      )}

      {/* SPREADS TAB */}
      {activeTab === 'spreads' && (
        <div className="space-y-4">
          <p className="text-sm text-muted-foreground">Premium 3-card spreads — deeper readings for specific areas of life.</p>

          <input
            type="text"
            value={spreadQuestion}
            onChange={e => setSpreadQuestion(e.target.value)}
            placeholder="Optional: your question for the spread..."
            className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40"
          />

          {spreads.map(spread => (
            <Card key={spread.spread_code} className="p-5 border border-border hover:border-gold/30 transition-all">
              <div className="flex items-start gap-3">
                <div className="w-9 h-9 rounded-sm bg-gold/10 flex items-center justify-center flex-shrink-0">
                  <Crown className="h-4 w-4 text-gold" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <p className="font-semibold text-sm">{spread.name}</p>
                    <span className="text-xs border border-gold/30 text-gold px-2 py-0.5 rounded-full">{spread.card_count} cards</span>
                  </div>
                  <p className="text-xs text-muted-foreground mb-3">{spread.description}</p>
                  <Button
                    onClick={() => handleSpreadGenerate(spread)}
                    disabled={loading}
                    size="sm"
                    className="bg-gold hover:bg-gold/90 text-primary-foreground gap-1.5"
                  >
                    {loading && selectedSpread?.spread_code === spread.spread_code
                      ? <><Loader2 className="h-3 w-3 animate-spin" /> Drawing...</>
                      : <><Zap className="h-3 w-3" /> Draw Spread</>
                    }
                  </Button>
                </div>
              </div>
            </Card>
          ))}

          {!user && (
            <div className="text-center py-6">
              <p className="text-sm text-muted-foreground mb-3">Sign in to access spreads</p>
              <Button onClick={() => navigate('/login')} variant="outline" size="sm">Sign In</Button>
            </div>
          )}
        </div>
      )}

      {/* HISTORY TAB */}
      {activeTab === 'history' && (
        <div className="space-y-3">
          {historyLoading && (
            <div className="text-center py-12"><Loader2 className="h-6 w-6 animate-spin text-gold mx-auto" /></div>
          )}
          {!historyLoading && history.length === 0 && (
            <div className="text-center py-12">
              <BookOpen className="h-10 w-10 text-muted-foreground/30 mx-auto mb-3" />
              <p className="text-muted-foreground">No readings yet. Draw your first card.</p>
              <Button onClick={() => setActiveTab('daily')} className="mt-4 bg-gold hover:bg-gold/90 text-primary-foreground" size="sm">Draw Now</Button>
            </div>
          )}
          {history.map(item => (
            <Card key={item.id} className="p-4 border border-border hover:border-gold/30 transition-colors">
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-sm bg-muted flex items-center justify-center flex-shrink-0">
                  <Star className="h-4 w-4 text-gold/60" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-0.5">
                    <p className="font-medium text-sm capitalize">{item.spread_code.replace(/_/g, ' ')}</p>
                    <span className="text-xs text-muted-foreground capitalize">{item.focus_area}</span>
                  </div>
                  <p className="text-xs text-muted-foreground line-clamp-1">{item.summary}</p>
                  <p className="text-xs text-muted-foreground mt-1">{item.prediction_date}</p>
                </div>
                <div className="flex items-center gap-2">
                  <button onClick={() => toggleBookmark(item.report_id, item.bookmarked)} className="text-muted-foreground hover:text-gold transition-colors">
                    {item.bookmarked ? <BookmarkCheck className="h-4 w-4 text-gold" /> : <Bookmark className="h-4 w-4" />}
                  </button>
                  <button onClick={() => openHistoryReading(item.report_id)} className="text-muted-foreground hover:text-foreground transition-colors">
                    <ChevronRight className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
