import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Star, Sparkles, Download, Share2, Crown, Lock } from 'lucide-react';
import { PaymentModal } from './PaymentModal';
import { ShareModal } from './ShareModal';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ─── Small info card ──────────────────────────────────────────────────────────
const InfoCard = ({ icon, label, value, sub }) => (
  <Card className="p-4 border border-border text-center">
    <div className="text-2xl mb-1">{icon}</div>
    <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">{label}</p>
    <p className="font-playfair font-semibold text-base">{value}</p>
    {sub && <p className="text-xs text-gold mt-1">{sub}</p>}
  </Card>
);

// ─── Section parser — converts Claude text to styled sections ────────────────
const parseReportSections = (text) => {
  if (!text) return [];
  const SECTION_HEADINGS = [
    'Overview', 'Ascendant & Personality', 'Sun Sign & Core Identity',
    'Moon Sign & Emotional Nature', 'Planetary Positions & House Analysis',
    'Notable Yogas & Planetary Combinations', 'Career & Dharma',
    'Relationships & Marriage', 'Health & Wellness',
    'Dasha Period Analysis', 'Remedies & Guidance',
  ];
  const lines = text.split('\n');
  const sections = [];
  let currentSection = null;
  let reportTitle = '';

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    // Strip markdown bold markers
    const clean = trimmed.replace(/^\*\*|\*\*$/g, '').trim();
    // Detect report title line (contains "Complete" or "Janma Kundali Report")
    if (!reportTitle && (clean.includes('Kundali Report') || clean.includes('Complete Janma'))) {
      reportTitle = clean;
      continue;
    }
    // Detect section heading — matches known heading (with or without colon)
    const matchedHeading = SECTION_HEADINGS.find(h =>
      clean === h || clean === h + ':' || clean.startsWith(h + ':')
    );
    if (matchedHeading) {
      if (currentSection) sections.push(currentSection);
      currentSection = { heading: matchedHeading, body: [] };
    } else {
      if (!currentSection) currentSection = { heading: '', body: [] };
      currentSection.body.push(clean);
    }
  }
  if (currentSection) sections.push(currentSection);
  return { reportTitle, sections };
};

// ─── Section card — matches PDF layout ───────────────────────────────────────
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

export const BirthChartDisplay = ({ report, isLoading, profile }) => {
  const { user } = useAuth();
  const [hasPremium, setHasPremium] = useState(false);
  const [showPayment, setShowPayment] = useState(false);
  const [showShare, setShowShare] = useState(false);
  const [checkingAccess, setCheckingAccess] = useState(true);

  useEffect(() => {
    if (profile) {
      checkPremiumAccess();
    }
  }, [profile, user]);

  const checkPremiumAccess = async () => {
    const userEmail = user?.email;
    if (!userEmail || !profile) {
      setCheckingAccess(false);
      return;
    }

    try {
      const response = await axios.get(`${API}/premium/check`, {
        params: {
          user_email: userEmail,
          report_type: 'birth_chart',
          report_id: profile.id
        }
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
      toast.info('Preparing your PDF...');
      const response = await axios.get(`${API}/birthchart/${profile.id}/pdf`, {
        responseType: 'blob',
        withCredentials: true,
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Birth_Chart_Report_${profile.name.replace(/ /g, '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      const pwd = response.headers['x-pdf-password'];
      if (pwd) {
        toast.success(`PDF downloaded! Password: ${pwd}`, { duration: 10000 });
      } else {
        toast.success('PDF downloaded successfully!');
      }
    } catch (error) {
      console.error('PDF download error:', error);
      toast.error('Failed to download PDF. Please try again.');
    }
  };

  if (isLoading) {
    return (
      <Card className="p-8 border-2 border-gold/30 bg-card min-h-[400px] flex flex-col items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="relative">
            <Star className="h-16 w-16 text-gold animate-pulse" />
            <Sparkles className="h-8 w-8 text-mustard absolute -top-2 -right-2 animate-pulse" style={{ animationDelay: '0.3s' }} />
          </div>
          <p className="text-xl font-playfair italic text-muted-foreground text-center">
            Calculating planetary positions...
          </p>
        </div>
      </Card>
    );
  }

  if (!report) return null;

  // Show basic version (first 200 characters as preview)
  const isBasicView = !hasPremium && !checkingAccess;
  const displayContent = isBasicView 
    ? report.report_content.substring(0, 200) + '...' 
    : report.report_content;

  return (
    <>
      <Card className="p-8 border-2 border-gold/30 bg-card">
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-3">
              <Star className="h-6 w-6 text-gold" />
              <h3 className="text-3xl font-playfair font-semibold">
                Birth Chart Analysis
              </h3>
              {hasPremium && (
                <span className="inline-flex items-center space-x-1 bg-gold text-primary-foreground px-3 py-1 rounded-full text-xs font-semibold">
                  <Crown className="h-3 w-3" />
                  <span>PREMIUM</span>
                </span>
              )}
            </div>
            
            {hasPremium && (
              <div className="flex items-center space-x-2">
                <Button
                  data-testid="download-pdf-btn"
                  onClick={handleDownloadPDF}
                  variant="outline"
                  size="sm"
                  className="border-gold hover:bg-gold hover:text-primary-foreground"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Generate PDF
                </Button>
                <Button
                  data-testid="share-btn"
                  onClick={() => setShowShare(true)}
                  variant="outline"
                  size="sm"
                  className="border-gold hover:bg-gold hover:text-primary-foreground"
                >
                  <Share2 className="h-4 w-4 mr-2" />
                  Share
                </Button>
              </div>
            )}
          </div>
          
          {profile && (
            <p className="text-muted-foreground text-base">
              For {profile.name} • Born on {profile.date_of_birth} at {profile.time_of_birth} in {profile.location}
            </p>
          )}
        </div>

        {/* Header info cards */}
        {(report.lagna?.sign || report.moon_sign?.sign || report.nakshatra?.name) && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
            {report.lagna?.sign && (
              <InfoCard icon="⬆" label="Ascendant (Lagna)"
                value={report.lagna.sign_vedic || report.lagna.sign}
                sub={`Lord: ${report.lagna.lord || ''}`} />
            )}
            {report.moon_sign?.sign && (
              <InfoCard icon="🌙" label="Moon Sign (Rashi)"
                value={report.moon_sign.sign_vedic || report.moon_sign.sign} />
            )}
            {report.nakshatra?.name && (
              <InfoCard icon="✦" label="Nakshatra"
                value={report.nakshatra.name}
                sub={`Pada ${report.nakshatra.pada || ''} · ${report.nakshatra.lord || ''}`} />
            )}
            {report.current_dasha?.planet && (
              <InfoCard icon="🪐" label="Current Dasha"
                value={`${report.current_dasha.planet} Mahadasha`}
                sub={report.current_dasha.end ? `Until ${report.current_dasha.end}` : ''} />
            )}
          </div>
        )}

        {/* North Indian Kundali Chart */}
        {report.chart_svg && (
          <div className="mb-6">
            <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">
              Janma Kundali — North Indian Chart
            </p>
            <div className="flex justify-center"
              dangerouslySetInnerHTML={{ __html: report.chart_svg }}
            />
          </div>
        )}

        {/* Structured section rendering — matches PDF layout */}
        <div className="relative">
          {(() => {
            const { reportTitle, sections } = parseReportSections(report.report_content);
            const visibleSections = isBasicView ? sections.slice(0, 1) : sections;
            return (
              <div className="relative">
                {/* Report title */}
                {reportTitle && (
                  <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-4">
                    {reportTitle}
                  </p>
                )}
                {/* Sections */}
                <div className="divide-y divide-border">
                  {visibleSections.map((sec, i) => (
                    <ReportSection key={i} heading={sec.heading} body={sec.body} />
                  ))}
                </div>
                {/* Paywall overlay for basic view */}
                {isBasicView && (
                  <div className="absolute inset-0 bg-gradient-to-b from-transparent via-background/70 to-background flex items-end justify-center pb-8">
                    <div className="text-center space-y-4">
                      <div className="inline-flex items-center space-x-2 bg-card border-2 border-gold px-6 py-3 rounded-sm">
                        <Lock className="h-5 w-5 text-gold" />
                        <span className="font-semibold text-lg">Premium Content Locked</span>
                      </div>
                      <p className="text-muted-foreground">Unlock your full comprehensive Kundali analysis</p>
                      <Button
                        data-testid="upgrade-to-premium-btn"
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
