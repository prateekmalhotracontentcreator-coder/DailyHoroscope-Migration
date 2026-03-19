import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import {
  Heart, Sparkles, Star, Download, Share2, Crown, Lock,
  Shield, Users, Gem, BookMarked, AlertTriangle, CheckCircle
} from 'lucide-react';
import { PaymentModal } from './PaymentModal';
import { ShareModal } from './ShareModal';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ─── Clean markdown from text ─────────────────────────────────────────────────
const clean = (text) => {
  if (!text) return '';
  return text
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/#{1,6}\s?/g, '')
    .replace(/^[-*]\s+/gm, '• ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
};

// ─── Parse detailed analysis into named sections ──────────────────────────────
const parseSections = (text) => {
  if (!text) return [];
  const cleaned = clean(text);

  const SECTION_PATTERNS = [
    { regex: /Compatibility Overview|Overview/i,           title: 'Compatibility Overview',      color: 'gold'   },
    { regex: /Ashtakoot Analysis|Koota Analysis|Guna Milan/i, title: 'Ashtakoot Guna Milan',     color: 'purple' },
    { regex: /Mangal Dosha|Manglik/i,                      title: 'Mangal Dosha Assessment',     color: 'red'    },
    { regex: /Planetary Harmony|Planetary Compat/i,        title: 'Planetary Harmony',           color: 'blue'   },
    { regex: /Relationship Strength|Strength/i,            title: 'Relationship Strengths',      color: 'green'  },
    { regex: /Challenge|Area.*Growth/i,                    title: 'Challenges & Growth Areas',   color: 'amber'  },
    { regex: /Marriage Timing|Timing/i,                    title: 'Marriage Timing',             color: 'blue'   },
    { regex: /Remed/i,                                     title: 'Remedies & Recommendations',  color: 'green'  },
  ];

  const lines = cleaned.split('\n');
  const sections = [];
  let currentTitle = 'Overview';
  let currentColor = 'gold';
  let currentLines = [];

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    let matched = false;
    // Check if line is a section heading
    if (trimmed.length < 80 && (trimmed.endsWith(':') || /^[A-Z]/.test(trimmed))) {
      for (const pat of SECTION_PATTERNS) {
        if (pat.regex.test(trimmed)) {
          if (currentLines.length > 0) {
            sections.push({ title: currentTitle, color: currentColor, content: currentLines.join('\n') });
          }
          currentTitle = pat.title;
          currentColor = pat.color;
          currentLines = [];
          matched = true;
          break;
        }
      }
    }
    if (!matched) currentLines.push(trimmed);
  }

  if (currentLines.length > 0) {
    sections.push({ title: currentTitle, color: currentColor, content: currentLines.join('\n') });
  }

  if (sections.length <= 1) {
    return [{ title: 'Compatibility Analysis', color: 'gold', content: cleaned }];
  }
  return sections;
};

// ─── Section color map ────────────────────────────────────────────────────────
const COLORS = {
  gold:   { bg: 'bg-amber-50/50 dark:bg-amber-950/20',   border: 'border-amber-200 dark:border-amber-800',   title: 'text-amber-800 dark:text-amber-300',   dot: 'bg-amber-500'   },
  purple: { bg: 'bg-purple-50/50 dark:bg-purple-950/20', border: 'border-purple-200 dark:border-purple-800', title: 'text-purple-800 dark:text-purple-300', dot: 'bg-purple-500' },
  red:    { bg: 'bg-red-50/50 dark:bg-red-950/20',       border: 'border-red-200 dark:border-red-800',       title: 'text-red-800 dark:text-red-300',       dot: 'bg-red-500'     },
  blue:   { bg: 'bg-blue-50/50 dark:bg-blue-950/20',     border: 'border-blue-200 dark:border-blue-800',     title: 'text-blue-800 dark:text-blue-300',     dot: 'bg-blue-500'    },
  green:  { bg: 'bg-emerald-50/50 dark:bg-emerald-950/20', border: 'border-emerald-200 dark:border-emerald-800', title: 'text-emerald-800 dark:text-emerald-300', dot: 'bg-emerald-500' },
  amber:  { bg: 'bg-orange-50/50 dark:bg-orange-950/20', border: 'border-orange-200 dark:border-orange-800', title: 'text-orange-800 dark:text-orange-300', dot: 'bg-orange-500'  },
};

// ─── Score helpers ────────────────────────────────────────────────────────────
const scoreColor = (s) =>
  s >= 28 ? 'text-green-600 dark:text-green-400' :
  s >= 24 ? 'text-amber-500' :
  s >= 18 ? 'text-orange-500' : 'text-red-500';

const scoreLabel = (s) =>
  s >= 32 ? 'Excellent Match — Highly Recommended' :
  s >= 24 ? 'Very Good Match' :
  s >= 18 ? 'Acceptable — Remedies Advised' :
  'Below Threshold — Consult Astrologer';

const scoreBg = (s) =>
  s >= 28 ? 'border-green-500/30 bg-green-50/30 dark:bg-green-950/20' :
  s >= 18 ? 'border-amber-500/30 bg-amber-50/30 dark:bg-amber-950/20' :
  'border-red-500/30 bg-red-50/30 dark:bg-red-950/20';

// ─── Main Component ───────────────────────────────────────────────────────────
export const KundaliMilanDisplay = ({ report, isLoading, person1, person2 }) => {
  const { user } = useAuth();
  const [hasPremium, setHasPremium] = useState(false);
  const [showPayment, setShowPayment] = useState(false);
  const [showShare, setShowShare] = useState(false);
  const [checkingAccess, setCheckingAccess] = useState(true);

  useEffect(() => {
    if (report) checkPremiumAccess();
  }, [report, user]);

  const checkPremiumAccess = async () => {
    if (!user?.email || !report) { setCheckingAccess(false); return; }
    try {
      const res = await axios.get(`${API}/premium/check`, {
        params: { user_email: user.email, report_type: 'kundali_milan', report_id: report.id }
      });
      setHasPremium(res.data.has_premium_access);
    } catch (e) {
      console.error('Premium check error:', e);
    } finally {
      setCheckingAccess(false);
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const res = await axios.get(`${API}/kundali-milan/${report.id}/pdf`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `kundali_milan_${person1?.name}_${person2?.name}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      toast.success('PDF downloaded!');
    } catch (e) {
      toast.error('PDF download failed. Please try again.');
    }
  };

  if (isLoading) {
    return (
      <Card className="p-10 border border-gold/30 min-h-[300px] flex flex-col items-center justify-center">
        <Heart className="h-14 w-14 text-gold animate-pulse mb-4" />
        <p className="text-lg font-playfair italic text-muted-foreground">
          Analysing cosmic compatibility...
        </p>
      </Card>
    );
  }

  if (!report) return null;

  const isBasicView = !hasPremium && !checkingAccess;
  const sections = parseSections(report.detailed_analysis);

  return (
    <div className="space-y-5">

      {/* ── Score card ─────────────────────────────────────────────────────── */}
      <Card className={`p-6 border-2 ${scoreBg(report.compatibility_score)}`}>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-5">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Heart className="h-5 w-5 text-gold" />
              <span className="text-xs font-semibold uppercase tracking-widest text-gold">
                Ashtakoot Guna Milan
              </span>
              {hasPremium && (
                <span className="bg-gold text-primary-foreground px-2 py-0.5 rounded-full text-xs font-semibold">
                  PREMIUM
                </span>
              )}
            </div>
            {person1 && person2 && (
              <p className="text-sm text-muted-foreground">
                {person1.name} &amp; {person2.name}
              </p>
            )}
          </div>
          {hasPremium && (
            <div className="flex gap-2">
              <Button onClick={handleDownloadPDF} variant="outline" size="sm"
                className="border-gold/40 hover:border-gold hover:bg-gold/10 gap-1.5">
                <Download className="h-3.5 w-3.5" /> PDF
              </Button>
              <Button onClick={() => setShowShare(true)} variant="outline" size="sm"
                className="border-gold/40 hover:border-gold hover:bg-gold/10 gap-1.5">
                <Share2 className="h-3.5 w-3.5" /> Share
              </Button>
            </div>
          )}
        </div>

        {/* Score display */}
        <div className="flex items-center justify-center gap-4 py-4">
          <div className="text-center">
            <div className={`text-7xl font-playfair font-bold leading-none ${scoreColor(report.compatibility_score)}`}>
              {report.compatibility_score}
            </div>
            <div className="text-lg text-muted-foreground font-medium">/ 36</div>
          </div>
          <div className="text-left max-w-[200px]">
            <p className={`font-semibold text-sm leading-snug ${scoreColor(report.compatibility_score)}`}>
              {scoreLabel(report.compatibility_score)}
            </p>
            <div className="mt-2 h-2 bg-muted rounded-full overflow-hidden w-32">
              <div
                className={`h-full rounded-full transition-all ${
                  report.compatibility_score >= 28 ? 'bg-green-500' :
                  report.compatibility_score >= 18 ? 'bg-amber-500' : 'bg-red-500'
                }`}
                style={{ width: `${(report.compatibility_score / 36) * 100}%` }}
              />
            </div>
          </div>
        </div>

        {/* Quick koota grid if available */}
        {report.ashtakoot_breakdown && (
          <div className="mt-4 pt-4 border-t border-border">
            <p className="text-xs text-muted-foreground uppercase tracking-wide mb-3">8 Koota Scores</p>
            <div className="grid grid-cols-4 gap-2">
              {Object.entries(report.ashtakoot_breakdown).map(([koota, data]) => (
                <div key={koota} className="text-center p-2 bg-background/60 rounded-sm border border-border">
                  <p className="text-xs text-muted-foreground capitalize">{koota}</p>
                  <p className={`font-bold text-sm ${data.score === data.max ? 'text-green-500' : data.score === 0 ? 'text-red-500' : 'text-amber-500'}`}>
                    {data.score}/{data.max}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </Card>

      {/* ── Detailed analysis sections ──────────────────────────────────────── */}
      {isBasicView ? (
        <Card className="p-8 border border-gold/30 text-center">
          <Lock className="h-8 w-8 text-gold mx-auto mb-3" />
          <p className="font-playfair text-xl font-semibold mb-2">Full Analysis — Premium</p>
          <p className="text-sm text-muted-foreground mb-4 max-w-md mx-auto">
            Unlock the complete 8-Koota breakdown, Mangal Dosha assessment, planetary harmony, relationship strengths, marriage timing, and personalised remedies.
          </p>
          <Button
            onClick={() => setShowPayment(true)}
            className="bg-gold hover:bg-gold/90 text-primary-foreground font-semibold gap-2"
          >
            <Crown className="h-4 w-4" /> Unlock Full Report
          </Button>
        </Card>
      ) : (
        <div className="space-y-4">
          {sections.map((section, i) => {
            const c = COLORS[section.color] || COLORS.gold;
            return (
              <Card key={i} className={`p-5 border ${c.border} ${c.bg}`}>
                <div className="flex items-center gap-2 mb-3">
                  <div className={`w-2 h-2 rounded-full flex-shrink-0 ${c.dot}`} />
                  <h4 className={`font-semibold text-sm uppercase tracking-wide ${c.title}`}>
                    {section.title}
                  </h4>
                </div>
                <div className="text-sm leading-relaxed text-foreground/85 whitespace-pre-line">
                  {section.content}
                </div>
              </Card>
            );
          })}
        </div>
      )}

      <PaymentModal
        isOpen={showPayment}
        onClose={() => setShowPayment(false)}
        reportType="kundali_milan"
        reportId={report?.id}
        onSuccess={checkPremiumAccess}
      />
      <ShareModal
        isOpen={showShare}
        onClose={() => setShowShare(false)}
        reportType="kundali_milan"
        reportId={report?.id}
      />
    </div>
  );
};
