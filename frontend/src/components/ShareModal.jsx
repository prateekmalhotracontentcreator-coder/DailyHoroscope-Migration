import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Share2, Copy, Check, Twitter, Facebook, Mail } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const FRONTEND_URL = process.env.REACT_APP_FRONTEND_URL || 'https://everydayhoroscope.in';

export const ShareModal = ({ isOpen, onClose, reportType, reportId }) => {
  const [shareLink, setShareLink] = useState('');
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen && reportId) {
      generateShareLink();
    }
  }, [isOpen, reportId]);

  const generateShareLink = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/share/create`, null, {
        params: {
          report_type: reportType,
          report_id: reportId
        }
      });
      
      const fullLink = `${FRONTEND_URL}/share/${response.data.token}`;
      setShareLink(fullLink);
    } catch (error) {
      console.error('Error generating share link:', error);
      toast.error('Failed to generate share link');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(shareLink);
    setCopied(true);
    toast.success('Link copied to clipboard!');
    setTimeout(() => setCopied(false), 2000);
  };

  const getReportLabel = () => {
    const labels = {
      'birth_chart': 'Janma Kundali (Birth Chart)',
      'kundali_milan': 'Kundali Milan (Marriage Compatibility)',
      'brihat_kundli': 'Brihat Kundli Pro (Life Report)',
    };
    return labels[reportType] || 'Astrology Report';
  };

  const shareToWhatsApp = () => {
    const date = new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });
    const message = `${getReportLabel()} — Generated on ${date}\n\nView my detailed Vedic astrology report on Everyday Horoscope:\n${shareLink}\n\nGet your own free report at everydayhoroscope.in`;
    window.open(`https://wa.me/?text=${encodeURIComponent(message)}`, '_blank');
  };

  const downloadAndSharePDF = async () => {
    try {
      toast.info('Generating PDF for sharing...');
      
      const endpoint = reportType === 'birth_chart' 
        ? `${API}/birthchart/${reportId}/pdf`
        : `${API}/kundali-milan/${reportId}/pdf`;
      
      const response = await axios.get(endpoint, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      const filename = reportType === 'birth_chart' 
        ? `birth_chart_report.pdf`
        : `kundali_milan_report.pdf`;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('PDF downloaded! You can now share it via WhatsApp from your device.');
    } catch (error) {
      console.error('PDF download error:', error);
      toast.error('Failed to download PDF for sharing.');
    }
  };

  const shareToTwitter = () => {
    const text = `Just got my ${getReportLabel()} from Everyday Horoscope — Ancient Vedic Wisdom, Modern Precision 🌟`;
    window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(shareLink)}`, '_blank');
  };

  const shareToFacebook = () => {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareLink)}`, '_blank');
  };

  const shareViaEmail = () => {
    const date = new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });
    const subject = `${getReportLabel()} — Everyday Horoscope`;
    const body = `I just generated my ${getReportLabel()} on Everyday Horoscope (${date}).\n\nView the full report here:\n${shareLink}\n\nGet your own free Vedic astrology report at everydayhoroscope.in`;
    window.open(`mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`);
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <div className="flex items-center space-x-2 mb-2">
            <Share2 className="h-6 w-6 text-gold" />
            <DialogTitle className="text-2xl font-playfair">Share Report</DialogTitle>
          </div>
          <DialogDescription>
            Share your astrological insights with friends and family
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          {/* Share Link */}
          <div>
            <label className="text-sm font-semibold mb-2 block">Share Link</label>
            <div className="flex items-center space-x-2">
              <Input
                value={shareLink}
                readOnly
                className="flex-1 text-sm"
                placeholder={loading ? 'Generating link...' : 'Share link will appear here'}
              />
              <Button
                data-testid="copy-link-btn"
                onClick={copyToClipboard}
                variant="outline"
                size="icon"
                className="border-gold hover:bg-gold hover:text-primary-foreground"
                disabled={!shareLink}
              >
                {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
              </Button>
            </div>
          </div>

          {/* Social Share Buttons */}
          <div>
            <label className="text-sm font-semibold mb-3 block">Share via</label>
            <div className="grid grid-cols-2 gap-3">
              <Button
                data-testid="share-whatsapp"
                onClick={shareToWhatsApp}
                variant="outline"
                className="h-12 border-gold hover:bg-gold hover:text-primary-foreground"
                disabled={!shareLink}
              >
                <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                </svg>
                Share Link
              </Button>

              <Button
                data-testid="download-pdf-share"
                onClick={downloadAndSharePDF}
                variant="outline"
                className="h-12 border-gold hover:bg-gold hover:text-primary-foreground"
              >
                <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                </svg>
                Download PDF
              </Button>

              <Button
                data-testid="share-twitter"
                onClick={shareToTwitter}
                variant="outline"
                className="h-12 border-gold hover:bg-gold hover:text-primary-foreground"
                disabled={!shareLink}
              >
                <Twitter className="h-5 w-5 mr-2" />
                Twitter
              </Button>

              <Button
                data-testid="share-facebook"
                onClick={shareToFacebook}
                variant="outline"
                className="h-12 border-gold hover:bg-gold hover:text-primary-foreground"
                disabled={!shareLink}
              >
                <Facebook className="h-5 w-5 mr-2" />
                Facebook
              </Button>

              <Button
                data-testid="share-email"
                onClick={shareViaEmail}
                variant="outline"
                className="h-12 border-gold hover:bg-gold hover:text-primary-foreground"
                disabled={!shareLink}
              >
                <Mail className="h-5 w-5 mr-2" />
                Email
              </Button>
            </div>
          </div>

          <p className="text-xs text-center text-muted-foreground">
            Anyone with this link can view your report
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );
};