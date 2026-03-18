import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Star, Sparkles, Download, Share2, Crown, Lock, Save } from 'lucide-react';
import { PaymentModal } from './PaymentModal';
import { ShareModal } from './ShareModal';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Clean markdown from report content
const cleanMarkdown = (text) => {
  if (!text) return '';
  return text
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/#{1,6}\s?/g, '')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/^[-*]\s+/gm, '• ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
};

// Parse birth chart content into labelled sections
const parseBirthChartContent = (content) => {
  if (!content) return [];
  const cleaned = cleanMarkdown(content);

  const SECTION_PATTERNS = [
    { regex: /Ascendant|Rising Sign|Lagna/i,           title: 'Ascendant & Lagna',          color: 'gold'   },
    { regex: /Sun.*Sign|Moon.*Sign|Core Identity/i,    title: 'Sun & Moon Signs',            color: 'amber'  },
    { regex: /Planetary Position/i,                    title: 'Planetary Positions',         color: 'blue'   },
    { regex: /House|Bhava/i,                           title: 'House Analysis',              color: 'green'  },
    { regex: /Yoga|yoga/i,                             title: 'Notable Yogas',               color: 'purple' },
    { regex: /Career|Profession|Work/i,                title: 'Career & Profession',         color: 'blue'   },
    { regex: /Relationship|Marriage|Love/i,            title: 'Relationships & Marriage',    color: 'pink'   },
    { regex: /Dasha|Mahadasha/i,                       title: 'Dasha Periods',               color: 'purple' },
    { regex: /Remedy|Gemstone|Mantra/i,                title: 'Remedies & Recommendations',  color: 'green'  },
  ];

  const lines = cleaned.split('\n');
  const sections = [];
  let currentTitle = 'Overview';
  let currentColor = 'gold';
  let currentLines = [];

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    // Check if this line is a section heading
    let isHeading = false;
    if (trimmed.length < 70 && (
      /^\d+\./.test(trimmed) ||           // numbered: "1. Ascendant"
      trimmed.endsWith(':') ||             // ends with colon
      /^[A-Z][A-Za-z\s&]+$/.test(trimmed) // all-caps-style heading
    )) {
      for (const pat of SECTION_PATTERNS) {
        if (pat.regex.test(trimmed)) {
          // Save current section
          if (currentLines.length > 0) {
            sections.push({ title: currentTitle, color: currentColor, content: currentLines.join('\n') });
          }
          currentTitle = pat.title;
          currentColor = pat.color;
          currentLines = [];
          isHeading = true;
          break;
        }
      }
    }

    if (!isHeading) {
      currentLines.push(trimmed);
    }
  }

  if (currentLines.length > 0) {
    sections.push({ title: currentTitle, color: currentColor, content: currentLines.join('\n') });
  }

  // If parsing found nothing useful, return whole content as one block
  if (sections.length === 0 || (sections.length === 1 && sections[0].title === 'Overview')) {
    return [{ title: 'Birth Chart Analysis', color: 'gold', content: cleaned }];
  }

  return sections;
};

const sectionColors = {
  gold:   { bg: 'bg-amber-50/50 dark:bg-amber-950/20',   border: 'border-amber-200 dark:border-amber-800',   title: 'text-amber-800 dark:text-amber-300',   dot: 'bg-amber-500' },
  amber:  { bg: 'bg-orange-50/50 dark:bg-orange-950/20', border: 'border-orange-200 dark:border-orange-800', title: 'text-orange-800 dark:text-orange-300', dot: 'bg-orange-500' },
  blue:   { bg: 'bg-blue-50/50 dark:bg-blue-950/20',     border: 'border-blue-200 dark:border-blue-800',     title: 'text-blue-800 dark:text-blue-300',     dot: 'bg-blue-500' },
  green:  { bg: 'bg-emerald-50/50 dark:bg-emerald-950/20', border: 'border-emerald-200 dark:border-emerald-800', title: 'text-emerald-800 dark:text-emerald-300', dot: 'bg-emerald-500' },
  purple: { bg: 'bg-purple-50/50 dark:bg-purple-950/20', border: 'border-purple-200 dark:border-purple-800', title: 'text-purple-800 dark:text-purple-300', dot: 'bg-purple-500' },
  pink:   { bg: 'bg-pink-50/50 dark:bg-pink-950/20',     border: 'border-pink-200 dark:border-pink-800',     title: 'text-pink-800 dark:text-pink-300',     dot: 'bg-pink-500' },
};

export const BirthChartDisplay = ({ report, isLoading, profile }) => {
  const { user } = useAuth();
  const [hasPremium, setHasPremium] = useState(false);
  const [showPayment, setShowPayment] = useState(false);
  const [showShare, setShowShare] = useState(false);
  const [checkingAccess, setCheckingAccess] = useState(true);

  useEffect(() => {
    if (profile) checkPremiumAccess();
  }, [profile, user]);

  const checkPremiumAccess = async () => {
    const userEmail = user?.email;
    if (!userEmail || !profile) { setCheckingAccess(false); return; }
    try {
      const response = await axios.get(`${API}/premium/check`, {
        params: { user_email: userEmail, report_type: 'birth_chart', report_id: profile.id }
      });
      setHasPremium(response.data.has_premium_access);
    } catch (error) {
      console.error('Error checking premium access:', error);
    } finally {
      setCheckingAccess(false);
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const response = await axios.get(`${API}/birthchart/${profile.id}/pdf`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `birth_chart_${profile.name.replace(/ /g, '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      toast.success('PDF downloaded successfully!');
    } catch (error) {
      toast.error('Failed to download PDF. Please try again.');
    }
  };

  if (isLoading) {
    return (
      <Card className="p-8 border border-gold/30 min-h-[400px] flex flex-col items-center justify-center">
        <Star className="h-14 w-14 text-gold animate-pulse mb-4" />
        <p className="text-lg font-playfair italic text-muted-foreground text-center">
          Calculating planetary positions...
        </p>
      </Card>
    );
  }

  if (!report) return null;

  const isBasicView = !hasPremium && !checkingAccess;
  const sections = parseBirthChartContent(report.report_content);
  const previewSections = isBasicView ? sections.slice(0, 1) : sections;

  return (
    <>
      {/* Report header */}
      <Card className="p-6 border border-gold/30 bg-gold/5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Crown className="h-5 w-5 text-gold" />
              <span className="text-xs font-semibold uppercase tracking-widest text-gold">
                Janma Kundali — Birth Chart Analysis
              </span>
              {hasPremium && (
                <span className="bg-gold text-primary-foreground px-2 py-0.5 rounded-full text-xs font-semibold">
                  PREMIUM
                </span>
              )}
            </div>
            {profile && (
              <p className="text-sm text-muted-foreground">
                {profile.name} · {profile.date_of_birth} · {profile.time_of_birth} · {profile.location}
              </p>
            )}
          </div>
          {hasPremium && (
            <div className="flex gap-2 flex-wrap">
              <Button
                data-testid="download-pdf-btn"
                onClick={handleDownloadPDF}
                variant="outline"
                size="sm"
                className="border-gold/40 hover:border-gold hover:bg-gold/10 gap-1.5"
              >
                <Download className="h-3.5 w-3.5" /> Download PDF
              </Button>
              <Button
                data-testid="share-btn"
                onClick={() => setShowShare(true)}
                variant="outline"
                size="sm"
                className="border-gold/40 hover:border-gold hover:bg-gold/10 gap-1.5"
              >
                <Share2 className="h-3.5 w-3.5" /> Share
              </Button>
            </div>
          )}
        </div>
      </Card>

      {/* Sections */}
      <div className="space-y-4 relative">
        {previewSections.map((section, i) => {
          const c = sectionColors[section.color] || sectionColors.gold;
          return (
            <Card key={i} className={`p-5 border ${c.border} ${c.bg}`}>
              <div className="flex items-center gap-2 mb-3">
                <div className={`w-2 h-2 rounded-full ${c.dot}`} />
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

        {/* Paywall overlay */}
        {isBasicView && (
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-b from-transparent to-background z-10 pointer-events-none" style={{ height: '80px' }} />
            <Card className="p-8 border-2 border-gold/40 text-center">
              <Lock className="h-8 w-8 text-gold mx-auto mb-3" />
              <p className="font-playfair text-xl font-semibold mb-2">Premium Report</p>
              <p className="text-sm text-muted-foreground mb-4">
                Unlock your complete birth chart — planetary positions, house analysis, yogas, dasha timeline, and remedies.
              </p>
              <Button
                data-testid="upgrade-to-premium-btn"
                onClick={() => setShowPayment(true)}
                className="bg-gold hover:bg-gold/90 text-primary-foreground font-semibold gap-2"
              >
                <Crown className="h-4 w-4" /> Unlock Full Report
              </Button>
            </Card>
          </div>
        )}
      </div>

      <PaymentModal
        isOpen={showPayment}
        onClose={() => setShowPayment(false)}
        reportType="birth_chart"
        reportId={profile?.id}
        onSuccess={checkPremiumAccess}
      />
      <ShareModal
        isOpen={showShare}
        onClose={() => setShowShare(false)}
        reportType="birth_chart"
        reportId={profile?.id}
      />
    </>
  );
};
