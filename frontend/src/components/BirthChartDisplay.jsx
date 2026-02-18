import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Star, Sparkles, Download, Share2, Crown, Lock } from 'lucide-react';
import { PaymentModal } from './PaymentModal';
import { ShareModal } from './ShareModal';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const BirthChartDisplay = ({ report, isLoading, profile }) => {
  const [hasPremium, setHasPremium] = useState(false);
  const [showPayment, setShowPayment] = useState(false);
  const [showShare, setShowShare] = useState(false);
  const [checkingAccess, setCheckingAccess] = useState(true);

  useEffect(() => {
    if (profile) {
      checkPremiumAccess();
    }
  }, [profile]);

  const checkPremiumAccess = async () => {
    const userEmail = localStorage.getItem('user_email');
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
      const response = await axios.get(`${API}/birthchart/${profile.id}/pdf`, {
        responseType: 'blob'
      });

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
                  Download PDF
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

        <div className="prose prose-lg max-w-none">
          <div className="text-base md:text-lg leading-relaxed text-foreground/90 whitespace-pre-wrap relative">
            {displayContent}
            
            {isBasicView && (
              <div className="absolute inset-0 bg-gradient-to-b from-transparent via-background/50 to-background flex items-end justify-center pb-8">
                <div className="text-center space-y-4">
                  <div className="inline-flex items-center space-x-2 bg-card border-2 border-gold px-6 py-3 rounded-sm">
                    <Lock className="h-5 w-5 text-gold" />
                    <span className="font-semibold text-lg">Premium Content Locked</span>
                  </div>
                  <p className="text-muted-foreground">
                    Unlock full comprehensive analysis with detailed insights
                  </p>
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
