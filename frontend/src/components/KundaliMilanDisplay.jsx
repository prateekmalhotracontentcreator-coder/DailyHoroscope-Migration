import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Heart, Sparkles, Star, Download, Share2, Crown, Lock } from 'lucide-react';
import { PaymentModal } from './PaymentModal';
import { ShareModal } from './ShareModal';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ─── Section parser — same pattern as Birth Chart ────────────────────────────
const parseReportSections = (text) => {
  if (!text) return { sections: [] };
  const SECTION_HEADINGS = [
    'Compatibility Overview', 'Ashtakoot Analysis', 'Mangal Dosha Assessment',
    'Planetary Harmony', 'Relationship Strengths', 'Challenges',
    'Marriage Timing', 'Remedies',
  ];

  // Strip ALL markdown from a line and return clean text
  const stripMarkdown = (line) => line
    .replace(/^#{1,6}\s*/g, '')      // ## headings
    .replace(/\*\*(.*?)\*\*/g, '$1') // **bold**
    .replace(/\*(.*?)\*/g, '$1')     // *italic*
    .replace(/^[-*]\s+/g, '')        // bullet points
    .replace(/^>\s*/g, '')           // blockquotes
    .replace(/`([^`]*)`/g, '$1')     // inline code
    .replace(/_{2}(.*?)_{2}/g, '$1') // __bold__
    .replace(/^---+$/g, '')          // horizontal rules
    .trim();

  const lines = text.split('\n');
  const sections = [];
  let currentSection = null;

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    // Strip markdown to get clean comparison text
    const clean = stripMarkdown(trimmed);
    if (!clean) continue;

    // Check if clean line matches a known section heading
    const matchedHeading = SECTION_HEADINGS.find(h =>
      clean === h ||
      clean === h + ':' ||
      clean.toLowerCase() === h.toLowerCase() ||
      clean.toLowerCase() === h.toLowerCase() + ':'
    );

    if (matchedHeading) {
      if (currentSection) sections.push(currentSection);
      currentSection = { heading: matchedHeading, body: [] };
    } else {
      // Only add non-empty body lines that are not just markdown artefacts
      if (!currentSection) currentSection = { heading: '', body: [] };
      if (clean.length > 2) currentSection.body.push(clean);
    }
  }
  if (currentSection) sections.push(currentSection);
  return { sections };
};

// ─── Section card — matches Birth Chart / PDF layout ─────────────────────────
const ReportSection = ({ heading, body }) => (
  <div className="mb-1">
    <div className="flex items-center gap-2 py-3 border-b border-gold/30">
      <span className="text-gold font-bold text-base leading-none">◆</span>
      <h3 className="font-playfair font-semibold text-base tracking-wide">{heading}</h3>
    </div>
    <div className="pt-3 pb-2 space-y-3">
      {body.map((para, j) => (
        <p key={j} className="text-sm leading-relaxed text-foreground/90">{para}</p>
      ))}
    </div>
  </div>
);

// ─── Mini chart SVG display ───────────────────────────────────────────────────
const MiniChart = ({ chartSvg, name, label }) => (
  <div className="flex flex-col items-center gap-2">
    <p className="text-xs font-semibold uppercase tracking-widest text-gold">{label}</p>
    <p className="text-sm font-playfair font-semibold">{name}</p>
    {chartSvg ? (
      <div dangerouslySetInnerHTML={{ __html: chartSvg }} />
    ) : (
      <div className="w-32 h-32 border border-border rounded-sm flex items-center justify-center text-muted-foreground text-xs">
        Chart loading...
      </div>
    )}
  </div>
);

// ─── Koota score badge ────────────────────────────────────────────────────────
const KootaBadge = ({ name, score, max }) => {
  const pct = (score / max) * 100;
  const color = pct >= 75 ? 'text-green-600 dark:text-green-400'
              : pct >= 50 ? 'text-amber-600 dark:text-amber-400'
              : 'text-red-600 dark:text-red-400';
  return (
    <div className="flex items-center justify-between p-2.5 rounded-sm border border-border bg-muted/20 text-sm">
      <span className="text-muted-foreground">{name}</span>
      <span className={`font-bold ${color}`}>{score}/{max}</span>
    </div>
  );
};

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
    const userEmail = user?.email;
    if (!userEmail || !report) { setCheckingAccess(false); return; }
    try {
      const res = await axios.get(`${API}/premium/check`, {
        params: { user_email: userEmail, report_type: 'kundali_milan', report_id: report.id }
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
      toast.info('Preparing your PDF...');
      const res = await axios.get(`${API}/kundali-milan/${report.id}/pdf`, {
        responseType: 'blob',
        withCredentials: true,
      });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      const p1 = person1?.name?.replace(/\s+/g, '_') || 'Person1';
      const p2 = person2?.name?.replace(/\s+/g, '_') || 'Person2';
      link.setAttribute('download', `Kundali_Milan_Report_${p1}_${p2}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      const pwd = res.headers['x-pdf-password'];
      if (pwd) {
        toast.success(`PDF downloaded! Password: ${pwd}`, { duration: 10000 });
      } else {
        toast.success('PDF downloaded successfully!');
      }
    } catch (e) {
      console.error('PDF download error:', e);
      toast.error('Failed to download PDF. Please try again.');
    }
  };

  if (isLoading) {
    return (
      <Card className="p-8 border-2 border-gold/30 bg-card min-h-[400px] flex flex-col items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="relative">
            <Heart className="h-16 w-16 text-gold animate-pulse" />
            <Sparkles className="h-8 w-8 text-gold/60 absolute -top-2 -right-2 animate-pulse" style={{ animationDelay: '0.3s' }} />
          </div>
          <p className="text-xl font-playfair italic text-muted-foreground text-center">
            Analysing compatibility through the cosmic lens...
          </p>
        </div>
      </Card>
    );
  }

  if (!report) return null;

  const score = report.compatibility_score;
  const getScoreColor = (s) => s >= 28 ? 'text-green-600 dark:text-green-400'
                               : s >= 18 ? 'text-amber-600 dark:text-amber-400'
                               : 'text-red-600 dark:text-red-400';
  const getScoreLabel = (s) => s >= 28 ? 'Excellent Match' : s >= 24 ? 'Very Good Match'
                               : s >= 18 ? 'Good Match' : 'Average Match';

  const isBasicView = !hasPremium && !checkingAccess;

  // Ashtakoot koota data from report if available
  const kootas = report.ashtakoot_details || null;

  return (
    <div className="space-y-6">

      {/* ── Score card ── */}
      <Card className="p-8 border-2 border-gold bg-gradient-to-br from-card to-muted/30 text-center relative">
        {hasPremium && (
          <div className="absolute top-4 right-4 flex items-center gap-2">
            <Button variant="outline" size="sm"
              className="gap-2 border-gold/40 hover:border-gold hover:bg-gold/10"
              onClick={handleDownloadPDF}>
              <Download className="h-4 w-4" /> Generate PDF
            </Button>
            <Button variant="outline" size="sm"
              className="gap-2 border-gold/40 hover:border-gold"
              onClick={() => setShowShare(true)}>
              <Share2 className="h-4 w-4" /> Share
            </Button>
          </div>
        )}

        <div className="flex items-center justify-center gap-3 mb-2">
          <Heart className="h-6 w-6 text-gold" />
          <h3 className="text-2xl font-playfair font-semibold">Compatibility Score</h3>
          {hasPremium && (
            <span className="inline-flex items-center gap-1 bg-gold text-primary-foreground px-2 py-0.5 rounded-full text-xs font-semibold">
              <Crown className="h-3 w-3" /> PREMIUM
            </span>
          )}
        </div>

        {person1 && person2 && (
          <p className="text-muted-foreground mb-6 text-sm">
            {person1.name} &amp; {person2.name}
          </p>
        )}

        <div className="flex items-center justify-center gap-3 mb-3">
          <span className={`text-6xl font-playfair font-bold ${getScoreColor(score)}`}>{score}</span>
          <span className="text-3xl font-playfair text-muted-foreground">/ 36</span>
        </div>

        <div className="flex items-center justify-center gap-2">
          <Star className="h-5 w-5 text-gold" />
          <span className="text-lg font-semibold text-gold">{getScoreLabel(score)}</span>
        </div>

        {/* Score bar */}
        <div className="mt-4 mx-auto max-w-xs">
          <div className="h-2 bg-muted rounded-full overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-amber-500 to-gold transition-all duration-700"
              style={{ width: `${(score / 36) * 100}%` }}
            />
          </div>
          <p className="text-xs text-muted-foreground mt-1">{score} out of 36 Gunas matched</p>
        </div>
      </Card>

      {/* ── Ashtakoot breakdown (always visible) ── */}
      {kootas && (
        <Card className="p-6 border border-border">
          <h3 className="font-playfair font-semibold text-base mb-4 flex items-center gap-2">
            <span className="text-gold">◆</span> Ashtakoot Guna Milan
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            <KootaBadge name="Varna" score={kootas.varna ?? '–'} max={1} />
            <KootaBadge name="Vashya" score={kootas.vashya ?? '–'} max={2} />
            <KootaBadge name="Tara" score={kootas.tara ?? '–'} max={3} />
            <KootaBadge name="Yoni" score={kootas.yoni ?? '–'} max={4} />
            <KootaBadge name="Graha Maitri" score={kootas.graha_maitri ?? '–'} max={5} />
            <KootaBadge name="Gana" score={kootas.gana ?? '–'} max={6} />
            <KootaBadge name="Bhakoot" score={kootas.bhakoot ?? '–'} max={7} />
            <KootaBadge name="Nadi" score={kootas.nadi ?? '–'} max={8} />
          </div>
        </Card>
      )}

      {/* ── Both charts side by side ── */}
      {(report.chart_svg_person1 || report.chart_svg_person2) && (
        <Card className="p-6 border border-border">
          <h3 className="font-playfair font-semibold text-base mb-4 flex items-center gap-2">
            <span className="text-gold">◆</span> Janma Kundali Charts
          </h3>
          <div className="grid grid-cols-2 gap-6">
            <MiniChart
              chartSvg={report.chart_svg_person1}
              name={person1?.name || 'Person 1'}
              label="Birth Chart"
            />
            <MiniChart
              chartSvg={report.chart_svg_person2}
              name={person2?.name || 'Person 2'}
              label="Birth Chart"
            />
          </div>
        </Card>
      )}

      {/* ── Detailed analysis ── */}
      <Card className="p-8 border-2 border-gold/30 bg-card">
        <div className="mb-4">
          <h3 className="text-xl font-playfair font-semibold">Detailed Compatibility Analysis</h3>
          <p className="text-muted-foreground text-xs mt-1">
            Based on Vedic Astrology · Ashtakoot Guna Milan System · Parashari Jyotish
          </p>
        </div>

        <div className="relative">
          {(() => {
            const { sections } = parseReportSections(report.detailed_analysis);
            const visibleSections = isBasicView ? sections.slice(0, 1) : sections;
            return (
              <div className="relative">
                <div className="divide-y divide-border">
                  {visibleSections.map((sec, i) => (
                    <ReportSection key={i} heading={sec.heading} body={sec.body} />
                  ))}
                </div>
                {isBasicView && (
                  <div className="absolute inset-0 bg-gradient-to-b from-transparent via-background/70 to-background flex items-end justify-center pb-8">
                    <div className="text-center space-y-4">
                      <div className="inline-flex items-center gap-2 bg-card border-2 border-gold px-6 py-3 rounded-sm">
                        <Lock className="h-5 w-5 text-gold" />
                        <span className="font-semibold text-lg">Premium Analysis Locked</span>
                      </div>
                      <p className="text-muted-foreground max-w-sm mx-auto text-sm">
                        Unlock the full 8-Koota breakdown, Mangal Dosha analysis, relationship insights, marriage timing, and personalised remedies
                      </p>
                      <Button
                        data-testid="upgrade-kundali-premium-btn"
                        onClick={() => setShowPayment(true)}
                        size="lg"
                        className="bg-gold hover:bg-gold-hover text-primary-foreground font-semibold"
                      >
                        <Crown className="h-5 w-5 mr-2" />
                        Unlock Premium Analysis
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            );
          })()}
        </div>
      </Card>

      <PaymentModal isOpen={showPayment} onClose={() => setShowPayment(false)}
        reportType="kundali_milan" reportId={report?.id} onSuccess={checkPremiumAccess} />
      <ShareModal isOpen={showShare} onClose={() => setShowShare(false)}
        reportType="kundali_milan" reportId={report?.id} />
    </div>
  );
};
