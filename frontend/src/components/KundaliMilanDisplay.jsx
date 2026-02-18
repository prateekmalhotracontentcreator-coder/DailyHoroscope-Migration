import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Heart, Sparkles, Star, Download, Share2, Crown, Lock } from 'lucide-react';
import { PaymentModal } from './PaymentModal';
import { ShareModal } from './ShareModal';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const KundaliMilanDisplay = ({ report, isLoading, person1, person2 }) => {
  const [hasPremium, setHasPremium] = useState(false);
  const [showPayment, setShowPayment] = useState(false);
  const [showShare, setShowShare] = useState(false);
  const [checkingAccess, setCheckingAccess] = useState(true);

  useEffect(() => {
    if (report) {
      checkPremiumAccess();
    }
  }, [report]);

  const checkPremiumAccess = async () => {
    const userEmail = localStorage.getItem('user_email');
    if (!userEmail || !report) {
      setCheckingAccess(false);
      return;
    }

    try {
      const response = await axios.get(`${API}/premium/check`, {
        params: {
          user_email: userEmail,
          report_type: 'kundali_milan',
          report_id: report.id
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
      const response = await axios.get(`${API}/kundali-milan/${report.id}/pdf`, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `kundali_milan_${person1.name}_${person2.name}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('PDF downloaded successfully!');
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
            <Heart className="h-16 w-16 text-gold animate-pulse" />
            <Sparkles className="h-8 w-8 text-mustard absolute -top-2 -right-2 animate-pulse" style={{ animationDelay: '0.3s' }} />
          </div>
          <p className="text-xl font-playfair italic text-muted-foreground text-center">
            Analyzing compatibility through the cosmic lens...
          </p>
        </div>
      </Card>
    );
  }

  if (!report) return null;

  const getScoreColor = (score) => {
    if (score >= 28) return 'text-green-600 dark:text-green-400';
    if (score >= 18) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-orange-600 dark:text-orange-400';
  };

  const getScoreLabel = (score) => {
    if (score >= 28) return 'Excellent Match';
    if (score >= 24) return 'Very Good Match';
    if (score >= 18) return 'Good Match';
    return 'Average Match';
  };

  const isBasicView = !hasPremium && !checkingAccess;

  return (
    <div className="space-y-6">
      {/* Score Card - Always visible (Basic feature) */}
      <Card className="p-8 border-2 border-gold bg-gradient-to-br from-card to-muted text-center relative">
        {hasPremium && (
          <div className="absolute top-4 right-4 flex items-center space-x-2">
            <Button
              data-testid="download-kundali-pdf-btn"
              onClick={handleDownloadPDF}
              variant="outline"
              size="sm"
              className="border-gold hover:bg-gold hover:text-primary-foreground"
            >
              <Download className="h-4 w-4 mr-2" />
              Download PDF
            </Button>
            <Button
              data-testid="share-kundali-btn"
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

        <div className="flex items-center justify-center mb-4">
          <Heart className="h-8 w-8 text-gold mr-3" />
          <h3 className="text-2xl font-playfair font-semibold">Compatibility Score</h3>
          {hasPremium && (
            <span className="inline-flex items-center space-x-1 bg-gold text-primary-foreground px-2 py-1 rounded-full text-xs font-semibold ml-3">
              <Crown className="h-3 w-3" />
              <span>PREMIUM</span>
            </span>
          )}
        </div>
        
        {person1 && person2 && (
          <p className="text-muted-foreground mb-6">
            {person1.name} & {person2.name}
          </p>
        )}
        
        <div className="flex items-center justify-center space-x-4 mb-4">
          <span className={`text-6xl font-playfair font-bold ${getScoreColor(report.compatibility_score)}`}>
            {report.compatibility_score}
          </span>
          <span className="text-3xl font-playfair text-muted-foreground">/ 36</span>
        </div>
        
        <div className="flex items-center justify-center space-x-2">
          <Star className="h-5 w-5 text-gold" />
          <span className="text-lg font-semibold text-gold">
            {getScoreLabel(report.compatibility_score)}
          </span>
        </div>
      </Card>

      {/* Detailed Analysis - Premium feature */}
      <Card className="p-8 border-2 border-gold/30 bg-card">
        <div className="mb-6">
          <div className="flex items-center justify-between">
            <h3 className="text-2xl font-playfair font-semibold">
              Detailed Compatibility Analysis
            </h3>
          </div>
          <p className="text-muted-foreground text-sm">
            Based on Vedic Astrology & Ashtakoot Guna Milan System
          </p>
        </div>

        <div className="prose prose-lg max-w-none relative">
          {isBasicView ? (
            <div className="min-h-[300px] flex items-center justify-center relative">
              <div className="absolute inset-0 bg-gradient-to-b from-transparent to-background/95 flex items-center justify-center">
                <div className="text-center space-y-4 z-10">
                  <div className="inline-flex items-center space-x-2 bg-card border-2 border-gold px-6 py-3 rounded-sm">
                    <Lock className="h-5 w-5 text-gold" />
                    <span className="font-semibold text-lg">Premium Analysis Locked</span>
                  </div>
                  <p className="text-muted-foreground max-w-md mx-auto">
                    Unlock comprehensive 8 Kootas breakdown, Manglik Dosha analysis, relationship insights, and personalized remedies
                  </p>
                  <Button
                    data-testid="upgrade-kundali-premium-btn"
                    onClick={() => setShowPayment(true)}
                    size="lg"
                    className="bg-gold hover:bg-gold-hover text-primary-foreground font-semibold"
                  >
                    <Crown className="h-5 w-5 mr-2" />
                    Unlock Premium Analysis - $14.99
                  </Button>
                </div>
              </div>
              
              {/* Blurred preview */}
              <div className="text-base md:text-lg leading-relaxed text-foreground/90 whitespace-pre-wrap blur-sm select-none pointer-events-none">
                {report.detailed_analysis.substring(0, 400)}...
              </div>
            </div>
          ) : (
            <div className="text-base md:text-lg leading-relaxed text-foreground/90 whitespace-pre-wrap">
              {report.detailed_analysis}
            </div>
          )}
        </div>
      </Card>

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
