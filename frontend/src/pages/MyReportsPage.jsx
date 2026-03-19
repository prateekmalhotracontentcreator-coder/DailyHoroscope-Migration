import React from 'react';
import { useNavigate } from 'react-router-dom';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { FileText, Download, Share2, Sparkles, ArrowRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const MyReportsPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <SEO title="My Reports — Everyday Horoscope" description="Access your saved Vedic astrology reports — Birth Chart, Kundali Milan, and premium reports." />
      <div className="mb-8">
        <h1 className="text-3xl font-playfair font-semibold mb-2">My Reports</h1>
        <p className="text-muted-foreground text-sm">Your saved Vedic astrology reports. Premium reports are stored permanently under your account.</p>
      </div>

      {/* Report type cards */}
      <div className="space-y-4 mb-10">
        {[
          { title: 'Birth Chart', subtitle: 'Janma Kundali', desc: 'Your complete Vedic birth chart analysis', path: '/birth-chart', color: 'text-amber-500' },
          { title: 'Kundali Milan', subtitle: 'Marriage Compatibility', desc: 'Ashtakoot Guna Milan compatibility reports', path: '/kundali-milan', color: 'text-pink-500' },
          { title: 'Brihat Kundli Pro', subtitle: 'Comprehensive Life Report', desc: '40+ page detailed Vedic life analysis', path: '/brihat-kundli', color: 'text-purple-500' },
        ].map((item) => (
          <Card key={item.title} className="p-5 border border-border flex items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-sm bg-muted flex items-center justify-center flex-shrink-0">
                <FileText className={`h-5 w-5 ${item.color}`} />
              </div>
              <div>
                <p className="font-semibold text-sm">{item.title}</p>
                <p className="text-xs text-muted-foreground">{item.subtitle} · {item.desc}</p>
              </div>
            </div>
            <Button
              onClick={() => navigate(item.path)}
              variant="outline"
              size="sm"
              className="border-gold/40 hover:border-gold gap-1.5 flex-shrink-0"
            >
              View <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          </Card>
        ))}
      </div>

      {/* Coming soon note */}
      <Card className="p-6 border border-gold/20 bg-gold/5 text-center">
        <Sparkles className="h-8 w-8 text-gold mx-auto mb-3" />
        <p className="font-playfair text-lg font-semibold mb-2">Saved Reports Library — Coming Soon</p>
        <p className="text-sm text-muted-foreground max-w-md mx-auto">
          Your generated reports will be automatically saved here. Re-download PDFs, view past analyses, and share reports — all in one place.
        </p>
      </Card>
    </div>
  );
};
