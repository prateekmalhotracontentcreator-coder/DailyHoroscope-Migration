import React, { useEffect, useMemo, useRef, useState } from 'react';
import axios from 'axios';
import { ArrowLeft, Check, ChevronDown, Compass, Hand, Layers, LoaderCircle, MoonStar, Orbit, Shield, Sparkles, Star, SunMedium } from 'lucide-react';

import { SEO } from '../components/SEO';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { toast } from '../components/ui/sonner';
import { useAuth } from '../context/AuthContext';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API = `${BACKEND_URL}/api/palmistry`;

const QUESTIONS = [
  {
    id: 'dominant_hand',
    label: 'Question 1 of 12',
    question: 'Which is your dominant hand?',
    options: ['Right', 'Left'],
  },
  {
    id: 'palm_shape',
    label: 'Question 2 of 12',
    question: 'What best describes your palm shape?',
    options: ['Square', 'Rectangular'],
  },
  {
    id: 'finger_length',
    label: 'Question 3 of 12',
    question: 'How would you describe your fingers relative to your palm?',
    options: ['Short (equal to or shorter than palm)', 'Long (longer than palm)'],
  },
  {
    id: 'life_line',
    label: 'Question 4 of 12',
    question: 'How does your Life Line appear?',
    options: ['Long & deep', 'Short or faint', 'Broken or chained', 'Forked at the end'],
  },
  {
    id: 'heart_line',
    label: 'Question 5 of 12',
    question: 'How does your Heart Line appear?',
    options: ['Long & curved upward', 'Straight across', 'Short', 'Broken or chained'],
  },
  {
    id: 'head_line',
    label: 'Question 6 of 12',
    question: 'How does your Head Line appear?',
    options: ['Straight & horizontal', 'Sloping downward', 'Short & straight', 'Forked at the end'],
  },
  {
    id: 'fate_line',
    label: 'Question 7 of 12',
    question: 'Is a Fate Line (vertical line toward middle finger) present?',
    options: ['Strong & clear', 'Faint or partial', 'Not visible'],
  },
  {
    id: 'dominant_mount',
    label: 'Question 8 of 12',
    question: 'Which area of your palm appears most raised or prominent?',
    options: [
      'Base of index finger (Jupiter)',
      'Base of middle finger (Saturn)',
      'Base of ring finger (Sun)',
      'Base of pinky (Mercury)',
      'Base of thumb (Venus)',
      'Lower palm opposite thumb (Moon)',
      'Centre of palm (Plain of Mars)',
    ],
  },
  {
    id: 'thumb_type',
    label: 'Question 9 of 12',
    question: 'How does your thumb appear?',
    options: ['Long & flexible', 'Long & stiff', 'Short', 'Waisted (narrowed at middle)'],
  },
  {
    id: 'finger_style',
    label: 'Question 10 of 12',
    question: 'How do your fingers generally appear?',
    options: [
      'Smooth (no prominent knots at joints)',
      'Knotty (prominent joints)',
      'Tapering toward tips',
      'Spatulate (wider at tips)',
    ],
  },
  {
    id: 'hand_texture',
    label: 'Question 11 of 12',
    question: 'How does the skin of your palm feel?',
    options: ['Soft & fine', 'Firm & elastic', 'Rough or coarse'],
  },
  {
    id: 'special_marks',
    label: 'Question 12 of 12',
    question: 'Are there any prominent special marks on your palm?',
    options: ['Star or asterisk on a mount', 'Triangle on a mount', 'Cross or X', 'Ring around a finger base', 'None visible'],
  },
];

const FEATURE_CARDS = [
  { label: 'Heart Line', desc: 'Emotional nature and relationship patterns', icon: MoonStar },
  { label: 'Head Line', desc: 'Intelligence, logic, and communication style', icon: Orbit },
  { label: 'Life Line', desc: 'Vitality, health, and major life changes', icon: Shield },
  { label: 'Fate Line', desc: 'Career path and life purpose', icon: Compass },
  { label: '7 Planetary Mounts', desc: 'Jupiter, Saturn, Sun, Mercury, Venus, Mars, Moon', icon: Layers },
  { label: 'Hand Shape', desc: 'Earth, Air, Fire, or Water — elemental personality', icon: Hand },
];

// Hand SVG illustrations — shown for Q4 onwards to remove ambiguity about which line/mount is being asked
// Base palm outline is the same; each entry adds a highlighted overlay path.
const HAND_ILLUSTRATIONS = {
  life_line: {
    label: 'Life Line',
    caption: 'The Life Line curves from between your thumb and index finger, arcing around the base of your thumb to the wrist.',
    highlight: <path d="M105 65 C 95 90, 82 115, 78 145 C 74 170, 75 190, 80 210" fill="none" stroke="#c5a059" strokeWidth="6" strokeLinecap="round" />,
  },
  heart_line: {
    label: 'Heart Line',
    caption: 'The Heart Line runs across the upper palm, just below where the fingers meet the palm.',
    highlight: <path d="M78 88 C 95 82, 115 80, 135 82 C 148 84, 158 88, 165 92" fill="none" stroke="#c5a059" strokeWidth="6" strokeLinecap="round" />,
  },
  head_line: {
    label: 'Head Line',
    caption: 'The Head Line runs horizontally across the middle of your palm, often starting near the Life Line.',
    highlight: <path d="M90 122 C 108 118, 128 118, 148 120 C 158 122, 165 126, 168 130" fill="none" stroke="#c5a059" strokeWidth="6" strokeLinecap="round" />,
  },
  fate_line: {
    label: 'Fate Line',
    caption: 'The Fate Line is a vertical line rising from the base of the palm toward the middle (Saturn) finger.',
    highlight: <path d="M125 210 C 124 185, 123 160, 122 135 C 122 115, 122 95, 123 80" fill="none" stroke="#c5a059" strokeWidth="6" strokeLinecap="round" />,
  },
  dominant_mount: {
    label: 'Planetary Mounts',
    caption: 'The mounts are raised fleshy pads beneath each finger and at the base of the thumb and palm. Look for the most prominent one.',
    highlight: <>
      <circle cx="100" cy="68" r="10" fill="#c5a059" fillOpacity="0.35" stroke="#c5a059" strokeWidth="2" />
      <text x="100" y="56" textAnchor="middle" fontSize="8" fill="#c5a059" fontFamily="sans-serif">Jupiter</text>
      <circle cx="122" cy="62" r="10" fill="#c5a059" fillOpacity="0.35" stroke="#c5a059" strokeWidth="2" />
      <text x="122" y="50" textAnchor="middle" fontSize="8" fill="#c5a059" fontFamily="sans-serif">Saturn</text>
      <circle cx="144" cy="66" r="10" fill="#c5a059" fillOpacity="0.35" stroke="#c5a059" strokeWidth="2" />
      <text x="144" y="54" textAnchor="middle" fontSize="8" fill="#c5a059" fontFamily="sans-serif">Sun</text>
      <circle cx="162" cy="76" r="9" fill="#c5a059" fillOpacity="0.35" stroke="#c5a059" strokeWidth="2" />
      <text x="162" y="64" textAnchor="middle" fontSize="8" fill="#c5a059" fontFamily="sans-serif">Mercury</text>
      <circle cx="82" cy="150" r="13" fill="#c5a059" fillOpacity="0.35" stroke="#c5a059" strokeWidth="2" />
      <text x="82" y="170" textAnchor="middle" fontSize="8" fill="#c5a059" fontFamily="sans-serif">Venus</text>
      <circle cx="160" cy="180" r="11" fill="#c5a059" fillOpacity="0.35" stroke="#c5a059" strokeWidth="2" />
      <text x="160" y="200" textAnchor="middle" fontSize="8" fill="#c5a059" fontFamily="sans-serif">Moon</text>
      <circle cx="120" cy="155" r="9" fill="#c5a059" fillOpacity="0.35" stroke="#c5a059" strokeWidth="2" />
      <text x="120" y="172" textAnchor="middle" fontSize="8" fill="#c5a059" fontFamily="sans-serif">Mars</text>
    </>,
  },
  thumb_type: {
    label: 'Thumb',
    caption: 'Observe the thumb independently. Note its length relative to your index finger and how flexible it bends back.',
    highlight: <ellipse cx="76" cy="118" rx="14" ry="32" fill="#c5a059" fillOpacity="0.28" stroke="#c5a059" strokeWidth="3" />,
  },
  finger_style: {
    label: 'Fingers',
    caption: 'Look at the joints of all four fingers. Are they smooth or do the knuckle joints protrude? Do tips taper or widen?',
    highlight: <>
      <rect x="88" y="22" width="16" height="38" rx="8" fill="#c5a059" fillOpacity="0.28" stroke="#c5a059" strokeWidth="2" />
      <rect x="110" y="14" width="16" height="44" rx="8" fill="#c5a059" fillOpacity="0.28" stroke="#c5a059" strokeWidth="2" />
      <rect x="132" y="18" width="16" height="42" rx="8" fill="#c5a059" fillOpacity="0.28" stroke="#c5a059" strokeWidth="2" />
      <rect x="152" y="26" width="15" height="36" rx="7" fill="#c5a059" fillOpacity="0.28" stroke="#c5a059" strokeWidth="2" />
    </>,
  },
  hand_texture: {
    label: 'Palm Skin',
    caption: 'Press the back of your other hand\'s fingers lightly against your palm to feel texture. Compare skin fineness.',
    highlight: <rect x="82" y="80" width="102" height="145" rx="18" fill="#c5a059" fillOpacity="0.12" stroke="#c5a059" strokeWidth="2" strokeDasharray="6 4" />,
  },
  special_marks: {
    label: 'Special Marks',
    caption: 'Look on the raised mounts for small star (✶), triangle (△), or cross (✕) formations. These are rare — most hands have none.',
    highlight: <>
      <text x="100" y="72" textAnchor="middle" fontSize="14" fill="#c5a059" opacity="0.8">✶</text>
      <text x="122" y="66" textAnchor="middle" fontSize="11" fill="#c5a059" opacity="0.7">△</text>
      <text x="83" y="148" textAnchor="middle" fontSize="13" fill="#c5a059" opacity="0.75">✕</text>
    </>,
  },
};

function HandIllustration({ questionId }) {
  const illus = HAND_ILLUSTRATIONS[questionId];
  if (!illus) return null;
  return (
    <div className="mb-6 rounded-2xl border border-gold/20 bg-gold/5 p-4">
      <p className="mb-3 text-xs font-semibold uppercase tracking-[0.24em] text-gold">{illus.label} — Reference Diagram</p>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start">
        <div className="flex-shrink-0 mx-auto sm:mx-0">
          <svg viewBox="0 0 245 240" className="h-44 w-36" aria-label={`${illus.label} diagram`}>
            {/* Palm outline */}
            <path d="M75 200 C 63 191, 55 174, 55 157 V 95 C 55 85, 63 77, 73 77 S 91 85, 91 95 V 58 C 91 48, 99 40, 109 40 S 127 48, 127 58 V 92 C 127 83, 134 76, 143 76 S 159 83, 159 92 V 105 C 159 97, 165 90, 174 90 S 189 97, 189 105 V 152 C 189 186, 164 214, 130 218 L 107 221 C 95 223, 83 215, 75 200 Z"
              fill="hsl(var(--card))" stroke="hsl(var(--gold, 33 79% 55%))" strokeWidth="2.5" strokeLinejoin="round" />
            {/* Thumb */}
            <path d="M73 77 C 73 60, 68 45, 62 38 C 57 32, 50 30, 45 33 C 38 38, 36 50, 40 62 C 44 74, 55 84, 73 95"
              fill="hsl(var(--card))" stroke="hsl(var(--gold, 33 79% 55%))" strokeWidth="2.5" strokeLinejoin="round" />
            {/* Highlighted element */}
            {illus.highlight}
          </svg>
        </div>
        <p className="text-sm leading-7 text-muted-foreground">{illus.caption}</p>
      </div>
    </div>
  );
}

const REPORT_SECTIONS = [
  { id: 'overview', title: 'Overview', icon: SunMedium },
  { id: 'personality', title: 'Personality', icon: Sparkles },
  { id: 'career_purpose', title: 'Career & Purpose', icon: Compass },
  { id: 'love_relationships', title: 'Love & Relationships', icon: MoonStar },
  { id: 'health_vitality', title: 'Health & Vitality', icon: Shield },
  { id: 'wealth_prosperity', title: 'Wealth & Prosperity', icon: Star },
  { id: 'spiritual_karmic', title: 'Spiritual & Karmic', icon: Orbit },
];

function deriveHandShape(palmShape, fingerLength) {
  const palm = String(palmShape || '').toLowerCase();
  const fingers = String(fingerLength || '').toLowerCase();
  if (palm === 'square' && fingers.startsWith('short')) return 'Earth';
  if (palm === 'square' && fingers.startsWith('long')) return 'Air';
  if (palm === 'rectangular' && fingers.startsWith('short')) return 'Fire';
  if (palm === 'rectangular' && fingers.startsWith('long')) return 'Water';
  return '';
}

function formatDate(value) {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '';
  return date.toLocaleDateString(undefined, {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

function SectionCard({ title, icon: Icon, children, className = '' }) {
  return (
    <Card className={`border border-gold/25 bg-card/95 p-5 shadow-sm ${className}`}>
      <div className="mb-3 flex items-center gap-2 text-gold">
        <Icon className="h-4 w-4" />
        <h3 className="font-playfair text-xl font-semibold text-foreground">{title}</h3>
      </div>
      <div className="text-sm leading-7 text-muted-foreground">{children}</div>
    </Card>
  );
}

function PalmistryLoader() {
  return (
    <div className="relative overflow-hidden rounded-[1.75rem] border border-gold/25 bg-gradient-to-br from-card via-gold/5 to-card px-6 py-12 text-center shadow-sm">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(201,160,89,0.18),_transparent_45%)]" />
      <div className="relative mx-auto flex max-w-lg flex-col items-center">
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/5 px-4 py-1.5 text-[11px] font-semibold uppercase tracking-[0.26em] text-gold">
          <LoaderCircle className="h-3.5 w-3.5 animate-spin" />
          Samudrika Shastra in progress
        </div>
        <div className="palmistry-loader mb-6">
          <svg viewBox="0 0 240 240" className="h-48 w-48 text-gold/85">
            <path d="M75 200c-12-9-20-26-20-43V91c0-10 8-18 18-18s18 8 18 18V54c0-10 8-18 18-18s18 8 18 18v34c0-9 7-16 16-16s16 7 16 16v13c0-8 6-15 15-15s15 7 15 15v47c0 34-25 62-58 66l-23 3c-12 2-24-2-33-10Z" fill="none" stroke="currentColor" strokeWidth="9" strokeLinecap="round" strokeLinejoin="round" />
            <path className="pulse-line line-a" d="M93 138c10-10 24-18 43-20" fill="none" stroke="currentColor" strokeWidth="5" strokeLinecap="round" />
            <path className="pulse-line line-b" d="M88 154c15 1 34 7 54 19" fill="none" stroke="currentColor" strokeWidth="5" strokeLinecap="round" />
            <path className="pulse-line line-c" d="M88 171c10 2 24 8 36 16" fill="none" stroke="currentColor" strokeWidth="5" strokeLinecap="round" />
            <circle className="pulse-mount mount-jupiter" cx="102" cy="78" r="7" fill="currentColor" />
            <circle className="pulse-mount mount-saturn" cx="127" cy="72" r="7" fill="currentColor" />
            <circle className="pulse-mount mount-sun" cx="151" cy="78" r="7" fill="currentColor" />
            <circle className="pulse-mount mount-mercury" cx="173" cy="91" r="6" fill="currentColor" />
            <circle className="pulse-mount mount-venus" cx="72" cy="126" r="8" fill="currentColor" />
            <circle className="pulse-mount mount-moon" cx="176" cy="173" r="7" fill="currentColor" />
            <circle className="pulse-mount mount-mars" cx="118" cy="150" r="6" fill="currentColor" />
          </svg>
        </div>
        <h2 className="mb-3 font-playfair text-3xl font-semibold text-foreground">Reading your Hasta Rekha</h2>
        <p className="max-w-md text-sm leading-7 text-muted-foreground">
          The ancient science of Samudrika Shastra is reading your hand and tracing the planetary story carried through your mounts, lines, and elemental form.
        </p>
      </div>
    </div>
  );
}

export const PalmistryPage = () => {
  const { user } = useAuth();
  const historyRef = useRef(null);

  const [view, setView] = useState('intro');
  const [stepIndex, setStepIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [currentReading, setCurrentReading] = useState(null);
  const [history, setHistory] = useState([]);
  const [expandedHistoryId, setExpandedHistoryId] = useState('');
  const [historyDetails, setHistoryDetails] = useState({});
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  const currentQuestion = QUESTIONS[stepIndex];
  const progress = ((stepIndex + 1) / QUESTIONS.length) * 100;
  const derivedHandShape = useMemo(() => deriveHandShape(answers.palm_shape, answers.finger_length), [answers.palm_shape, answers.finger_length]);
  const isFinalStepAnswered = Boolean(answers.special_marks);
  const canViewHistory = Boolean(user?.email && history.length);

  useEffect(() => {
    if (!user?.email) {
      setHistory([]);
      setExpandedHistoryId('');
      setHistoryDetails({});
      return;
    }

    const fetchHistory = async () => {
      setHistoryLoading(true);
      try {
        const response = await axios.get(`${API}/reports`, {
          params: { user_email: user.email },
          withCredentials: true,
        });
        setHistory(Array.isArray(response.data) ? response.data : []);
      } catch (error) {
        setHistory([]);
      } finally {
        setHistoryLoading(false);
      }
    };

    fetchHistory();
  }, [user?.email]);

  const handleStart = () => {
    setView('questions');
    setStepIndex(0);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleAnswerSelect = (questionId, option) => {
    setAnswers(prev => ({ ...prev, [questionId]: option }));
    if (stepIndex < QUESTIONS.length - 1) {
      setStepIndex(prev => prev + 1);
    }
  };

  const handleBack = () => {
    if (stepIndex === 0) {
      setView('intro');
      return;
    }
    setStepIndex(prev => prev - 1);
  };

  const buildPayload = (withUserEmail = false) => ({
    user_email: withUserEmail ? user?.email || '' : '',
    user_name: withUserEmail ? user?.name || user?.full_name || '' : '',
    dominant_hand: answers.dominant_hand,
    palm_shape: answers.palm_shape,
    hand_shape: derivedHandShape,
    finger_length: answers.finger_length,
    life_line: answers.life_line,
    heart_line: answers.heart_line,
    head_line: answers.head_line,
    fate_line: answers.fate_line,
    dominant_mount: answers.dominant_mount,
    thumb_type: answers.thumb_type,
    finger_style: answers.finger_style,
    hand_texture: answers.hand_texture,
    special_marks: answers.special_marks,
  });

  const handleGenerate = async () => {
    if (!isFinalStepAnswered) return;

    setLoading(true);
    setView('loading');
    window.scrollTo({ top: 0, behavior: 'smooth' });

    try {
      const response = await axios.post(`${API}/analyse`, buildPayload(false), {
        withCredentials: true,
      });
      setCurrentReading(response.data);
      setView('report');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
      toast.error(error?.response?.data?.detail || 'Palm reading could not be generated right now.');
      setView('questions');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveReading = async () => {
    if (!user?.email) {
      toast.error('Please sign in to save this reading.');
      return;
    }
    if (!currentReading) return;

    setSaving(true);
    try {
      const response = await axios.post(`${API}/analyse`, buildPayload(true), {
        withCredentials: true,
      });
      setCurrentReading(response.data);
      toast.success('Palm reading saved to your history.');

      const historyResponse = await axios.get(`${API}/reports`, {
        params: { user_email: user.email },
        withCredentials: true,
      });
      setHistory(Array.isArray(historyResponse.data) ? historyResponse.data : []);
    } catch (error) {
      toast.error(error?.response?.data?.detail || 'Could not save this reading.');
    } finally {
      setSaving(false);
    }
  };

  const handleNewReading = () => {
    setAnswers({});
    setCurrentReading(null);
    setStepIndex(0);
    setView('intro');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleViewHistory = () => {
    if (!historyRef.current) return;
    historyRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const toggleHistoryItem = async (itemId) => {
    if (expandedHistoryId === itemId) {
      setExpandedHistoryId('');
      return;
    }

    setExpandedHistoryId(itemId);
    if (historyDetails[itemId]) return;

    try {
      const response = await axios.get(`${API}/reports/${itemId}`, {
        withCredentials: true,
      });
      setHistoryDetails(prev => ({ ...prev, [itemId]: response.data }));
    } catch (error) {
      toast.error('Could not open this saved reading.');
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <SEO title="Hasta Rekha — Vedic Palmistry" description="India's first AI-powered Vedic palmistry. Analyse your palm lines, mounts, and hand shape through the lens of Samudrika Shastra — the ancient Indian science of body reading." url="https://everydayhoroscope.in/palmistry" />

      <style>{`
        .palmistry-loader .pulse-mount { opacity: 0.35; animation: palmistryPulse 2.6s ease-in-out infinite; transform-origin: center; }
        .palmistry-loader .pulse-line { opacity: 0.3; animation: palmistryLine 2.2s ease-in-out infinite; }
        .palmistry-loader .mount-jupiter { animation-delay: 0s; }
        .palmistry-loader .mount-saturn { animation-delay: 0.15s; }
        .palmistry-loader .mount-sun { animation-delay: 0.3s; }
        .palmistry-loader .mount-mercury { animation-delay: 0.45s; }
        .palmistry-loader .mount-venus { animation-delay: 0.6s; }
        .palmistry-loader .mount-moon { animation-delay: 0.75s; }
        .palmistry-loader .mount-mars { animation-delay: 0.9s; }
        .palmistry-loader .line-a { animation-delay: 0.1s; }
        .palmistry-loader .line-b { animation-delay: 0.5s; }
        .palmistry-loader .line-c { animation-delay: 0.9s; }
        @keyframes palmistryPulse {
          0%, 100% { opacity: 0.28; transform: scale(1); }
          50% { opacity: 0.95; transform: scale(1.2); }
        }
        @keyframes palmistryLine {
          0%, 100% { opacity: 0.18; stroke-dasharray: 4 12; }
          50% { opacity: 0.9; stroke-dasharray: 36 8; }
        }
      `}</style>

      <div className="px-4 py-8 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-5xl">
          {view === 'intro' ? (
            <div className="space-y-8">
              <div className="text-center">
                <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/5 px-4 py-1.5 text-xs font-semibold uppercase tracking-widest text-gold">
                  <Layers className="h-3 w-3" /> Engine 5 · Samudrika Shastra
                </div>
                <h1 className="mb-3 font-playfair text-4xl font-semibold sm:text-5xl">Hasta Rekha</h1>
                <p className="mb-3 text-muted-foreground">Vedic Palmistry — Samudrika Shastra</p>
                <p className="mx-auto max-w-2xl text-sm leading-7 text-muted-foreground sm:text-base">
                  India's first AI-powered Vedic palmistry analysis. Unlike Western palmistry, Samudrika Shastra connects your hand features directly to planetary mounts — giving astrological depth no other palmistry app offers.
                </p>
              </div>

              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {FEATURE_CARDS.map(({ label, desc, icon: Icon }) => (
                  <Card key={label} className="border border-gold/20 bg-card/95 p-5 shadow-sm transition-transform duration-300 hover:-translate-y-1">
                    <div className="mb-3 inline-flex rounded-full border border-gold/25 bg-gold/5 p-2 text-gold">
                      <Icon className="h-4 w-4" />
                    </div>
                    <p className="mb-1 font-medium text-foreground">{label}</p>
                    <p className="text-sm leading-6 text-muted-foreground">{desc}</p>
                  </Card>
                ))}
              </div>

              <Card className="overflow-hidden border border-gold/25 bg-gradient-to-br from-card via-gold/5 to-card p-6 shadow-sm sm:p-8">
                <div className="grid gap-6 md:grid-cols-[1.1fr_0.9fr] md:items-center">
                  <div>
                    <p className="mb-2 text-xs font-semibold uppercase tracking-[0.26em] text-gold">Premium Palm Reading</p>
                    <h2 className="mb-3 font-playfair text-3xl font-semibold text-foreground">Your hand, decoded through planetary intelligence</h2>
                    <p className="text-sm leading-7 text-muted-foreground">
                      Answer 12 guided questions about your lines, mounts, thumb, texture, and elemental hand form. We’ll interpret the full palm through Jyotish-linked planetary signatures and generate your complete Hasta Rekha report.
                    </p>
                  </div>
                  <div className="rounded-[1.5rem] border border-gold/20 bg-background/70 p-5">
                    <div className="mb-4 flex items-center gap-3">
                      <div className="rounded-full border border-gold/30 bg-gold/5 p-2 text-gold">
                        <Hand className="h-5 w-5" />
                      </div>
                      <div>
                        <p className="font-medium text-foreground">12-step diagnostic</p>
                        <p className="text-sm text-muted-foreground">One question at a time, built for mobile clarity</p>
                      </div>
                    </div>
                    <Button onClick={handleStart} className="w-full bg-gold text-primary-foreground hover:bg-gold/90">
                      Begin My Reading
                    </Button>
                  </div>
                </div>
              </Card>
            </div>
          ) : null}

          {view === 'questions' ? (
            <div className="mx-auto max-w-3xl space-y-6">
              <div className="rounded-2xl border border-gold/20 bg-card/95 p-4 shadow-sm">
                <div className="mb-3 flex items-center justify-between gap-3 text-xs font-semibold uppercase tracking-[0.24em] text-gold">
                  <span>{currentQuestion.label}</span>
                  <span>{Math.round(progress)}%</span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-gold/10">
                  <div className="h-full rounded-full bg-gold transition-all duration-500" style={{ width: `${progress}%` }} />
                </div>
                {derivedHandShape ? (
                  <div className="mt-3 inline-flex items-center gap-2 rounded-full border border-gold/25 bg-gold/5 px-3 py-1 text-xs font-medium text-gold">
                    <Check className="h-3.5 w-3.5" />
                    Derived hand type: {derivedHandShape}
                  </div>
                ) : null}
              </div>

              <Card key={currentQuestion.id} className="border border-gold/25 bg-card/95 p-6 shadow-sm sm:p-8">
                <div className="mb-6 flex items-center justify-between gap-4">
                  <button onClick={handleBack} className="inline-flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-gold">
                    <ArrowLeft className="h-4 w-4" />
                    {stepIndex === 0 ? 'Back to Intro' : 'Previous Question'}
                  </button>
                  <div className="rounded-full border border-gold/25 bg-gold/5 px-3 py-1 text-xs font-medium text-gold">
                    Step {stepIndex + 1}
                  </div>
                </div>

                <HandIllustration questionId={currentQuestion.id} />
                <h2 className="mb-2 font-playfair text-3xl font-semibold text-foreground">{currentQuestion.question}</h2>
                <p className="mb-6 text-sm text-muted-foreground">Choose the option that feels closest to what you see on your palm.</p>

                <div className="grid gap-3">
                  {currentQuestion.options.map(option => {
                    const isSelected = answers[currentQuestion.id] === option;
                    const isLastQuestion = stepIndex === QUESTIONS.length - 1;
                    return (
                      <button
                        key={option}
                        type="button"
                        onClick={() => (isLastQuestion ? setAnswers(prev => ({ ...prev, [currentQuestion.id]: option })) : handleAnswerSelect(currentQuestion.id, option))}
                        className={`rounded-2xl border px-4 py-4 text-left transition-all sm:px-5 ${
                          isSelected
                            ? 'border-gold bg-gold/10 shadow-sm'
                            : 'border-border bg-background hover:border-gold/40 hover:bg-gold/5'
                        }`}
                      >
                        <div className="flex items-start justify-between gap-4">
                          <span className="text-sm font-medium leading-6 text-foreground">{option}</span>
                          <span className={`mt-1 h-5 w-5 rounded-full border ${isSelected ? 'border-gold bg-gold text-primary-foreground' : 'border-gold/30'} flex items-center justify-center`}>
                            {isSelected ? <Check className="h-3.5 w-3.5" /> : null}
                          </span>
                        </div>
                      </button>
                    );
                  })}
                </div>

                {stepIndex === QUESTIONS.length - 1 ? (
                  <div className="mt-6 flex flex-col gap-3 sm:flex-row">
                    <Button
                      onClick={handleGenerate}
                      disabled={!isFinalStepAnswered || loading}
                      className="bg-gold text-primary-foreground hover:bg-gold/90 sm:min-w-44"
                    >
                      View Results
                    </Button>
                    <p className="text-sm leading-6 text-muted-foreground">
                      Your report will be generated from the exact line, mount, and planetary signals you selected.
                    </p>
                  </div>
                ) : null}
              </Card>
            </div>
          ) : null}

          {view === 'loading' ? (
            <div className="mx-auto max-w-3xl">
              <PalmistryLoader />
            </div>
          ) : null}

          {view === 'report' && currentReading ? (
            <div className="space-y-6">
              <div className="rounded-[1.75rem] border border-gold/25 bg-gradient-to-br from-card via-gold/5 to-card p-6 shadow-sm sm:p-8">
                <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
                  <div>
                    <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-gold/25 bg-gold/5 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-gold">
                      <Sparkles className="h-3.5 w-3.5" />
                      Hasta Rekha Report
                    </div>
                    <h2 className="font-playfair text-3xl font-semibold text-foreground sm:text-4xl">{currentReading.hand_shape} Hand Reading</h2>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Dominant hand: {currentReading.dominant_hand} · Generated {formatDate(currentReading.created_at)}
                    </p>
                  </div>
                  <div className="rounded-2xl border border-gold/20 bg-background/70 px-4 py-3 text-sm text-muted-foreground">
                    Elemental type derived from {currentReading.answers.palm_shape} palm and {currentReading.answers.finger_length.toLowerCase()}.
                  </div>
                </div>
              </div>

              <div className="grid gap-4 lg:grid-cols-2">
                {REPORT_SECTIONS.map(({ id, title, icon }) => (
                  <SectionCard key={id} title={title} icon={icon} className={id === 'overview' ? 'lg:col-span-2' : ''}>
                    {currentReading.report[id]}
                  </SectionCard>
                ))}

                <SectionCard title="Planetary Remedies" icon={Layers} className="lg:col-span-2">
                  <div className="grid gap-4 md:grid-cols-2">
                    {[
                      ['Gemstone', currentReading.report.remedies.gemstone],
                      ['Mantra', currentReading.report.remedies.mantra],
                      ['Colour', currentReading.report.remedies.colour],
                      ['Practice', currentReading.report.remedies.practice],
                    ].map(([label, value]) => (
                      <div key={label} className="rounded-2xl border border-gold/20 bg-gold/5 p-4">
                        <p className="mb-2 text-xs font-semibold uppercase tracking-[0.22em] text-gold">{label}</p>
                        <p className="text-sm leading-7 text-muted-foreground">{value}</p>
                      </div>
                    ))}
                  </div>
                </SectionCard>

                <Card className="lg:col-span-2 border border-dashed border-gold/30 bg-card/95 p-5">
                  <p className="mb-2 text-xs font-semibold uppercase tracking-[0.24em] text-gold">Phase 2</p>
                  <h3 className="mb-2 font-playfair text-2xl font-semibold text-foreground">Upload your palm photo for AI Vision analysis</h3>
                  <p className="text-sm leading-7 text-muted-foreground">
                    Claude Vision-based palm photo reading is planned for the next phase. This phase will add mount inspection, line detection, and visual mark extraction from your actual palm image.
                  </p>
                </Card>
              </div>

              <Card className="border border-gold/25 bg-card/95 p-5 shadow-sm">
                <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                  <div>
                    <p className="font-medium text-foreground">Keep or revisit this reading</p>
                    <p className="text-sm text-muted-foreground">Save it to your account, start a fresh analysis, or jump to your history below.</p>
                  </div>
                  <div className="flex flex-col gap-3 sm:flex-row">
                    <Button onClick={handleSaveReading} disabled={saving} className="bg-gold text-primary-foreground hover:bg-gold/90">
                      {saving ? 'Saving...' : 'Save Reading'}
                    </Button>
                    <Button onClick={handleNewReading} variant="outline" className="border-gold/40 hover:border-gold hover:bg-gold/5">
                      New Reading
                    </Button>
                    {canViewHistory ? (
                      <Button onClick={handleViewHistory} variant="outline" className="border-gold/40 hover:border-gold hover:bg-gold/5">
                        View History
                      </Button>
                    ) : null}
                  </div>
                </div>
              </Card>
            </div>
          ) : null}

          <div ref={historyRef} className="mt-10">
            {user?.email && (historyLoading || history.length > 0) ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Saved Readings</p>
                    <h2 className="font-playfair text-3xl font-semibold text-foreground">Palmistry History</h2>
                  </div>
                  {historyLoading ? <p className="text-sm text-muted-foreground">Loading history...</p> : null}
                </div>

                {history.map(item => {
                  const expanded = expandedHistoryId === item.id;
                  const details = historyDetails[item.id];
                  return (
                    <Card key={item.id} className="border border-gold/20 bg-card/95 p-4 shadow-sm">
                      <button onClick={() => toggleHistoryItem(item.id)} className="flex w-full items-start justify-between gap-4 text-left">
                        <div>
                          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">{formatDate(item.created_at)} · {item.hand_shape} Hand</p>
                          <p className="mt-1 text-sm text-muted-foreground">Dominant hand: {item.dominant_hand}</p>
                          <p className="mt-3 text-sm leading-7 text-foreground">{item.overview}</p>
                        </div>
                        <ChevronDown className={`mt-1 h-5 w-5 shrink-0 text-gold transition-transform ${expanded ? 'rotate-180' : ''}`} />
                      </button>

                      {expanded ? (
                        <div className="mt-4 border-t border-gold/15 pt-4">
                          {!details ? (
                            <p className="text-sm text-muted-foreground">Opening saved reading...</p>
                          ) : (
                            <div className="grid gap-4 lg:grid-cols-2">
                              {REPORT_SECTIONS.map(({ id, title, icon }) => (
                                <SectionCard key={`${item.id}-${id}`} title={title} icon={icon} className={id === 'overview' ? 'lg:col-span-2' : ''}>
                                  {details.report[id]}
                                </SectionCard>
                              ))}
                              <SectionCard title="Planetary Remedies" icon={Layers} className="lg:col-span-2">
                                <div className="grid gap-4 md:grid-cols-2">
                                  {[
                                    ['Gemstone', details.report.remedies.gemstone],
                                    ['Mantra', details.report.remedies.mantra],
                                    ['Colour', details.report.remedies.colour],
                                    ['Practice', details.report.remedies.practice],
                                  ].map(([label, value]) => (
                                    <div key={`${item.id}-${label}`} className="rounded-2xl border border-gold/20 bg-gold/5 p-4">
                                      <p className="mb-2 text-xs font-semibold uppercase tracking-[0.22em] text-gold">{label}</p>
                                      <p className="text-sm leading-7 text-muted-foreground">{value}</p>
                                    </div>
                                  ))}
                                </div>
                              </SectionCard>
                            </div>
                          )}
                        </div>
                      ) : null}
                    </Card>
                  );
                })}
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PalmistryPage;
