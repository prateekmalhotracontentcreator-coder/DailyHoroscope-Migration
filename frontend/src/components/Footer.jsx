import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Mail, Shield, FileText, Cookie, RefreshCw, ScrollText } from 'lucide-react';

export const Footer = () => {
  const navigate = useNavigate();
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-border bg-card/50 mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">

          {/* Brand */}
          <div className="md:col-span-1">
            <div className="flex items-center space-x-2 mb-4 cursor-pointer" onClick={() => navigate('/home')}>
              <Sparkles className="h-6 w-6 text-gold" />
              <span className="text-lg font-playfair font-semibold">Everyday Horoscope</span>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              AI-powered astrological insights for your daily journey. Operated by SkyHound Studios.
            </p>
            <a
              href="mailto:prateekmalhotra.contentcreator@gmail.com"
              className="flex items-center space-x-2 mt-4 text-sm text-gold hover:underline"
            >
              <Mail className="h-4 w-4" />
              <span>prateekmalhotra.contentcreator@gmail.com</span>
            </a>
          </div>

          {/* Explore */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-4">Explore</h3>
            <ul className="space-y-2">
              {[
                { label: 'Daily Horoscope', path: '/horoscope/daily' },
                { label: 'Weekly Horoscope', path: '/horoscope/weekly' },
                { label: 'Monthly Horoscope', path: '/horoscope/monthly' },
                { label: 'Birth Chart', path: '/birth-chart' },
                { label: 'Kundali Milan', path: '/kundali-milan' },
                { label: 'Brihat Kundli Pro', path: '/brihat-kundli' },
                { label: 'Pricing', path: '/pricing' },
                { label: 'Blog', path: '/blog' },
              ].map(({ label, path }) => (
                <li key={path}>
                  <span
                    onClick={() => navigate(path)}
                    className="text-sm text-muted-foreground hover:text-gold cursor-pointer transition-colors"
                  >
                    {label}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-4">Company</h3>
            <ul className="space-y-2">
              {[
                { label: 'About Us', path: '/about' },
                { label: 'Contact Us', path: '/contact' },
                { label: 'Blog', path: '/blog' },
              ].map(({ label, path }) => (
                <li key={path}>
                  <span
                    onClick={() => navigate(path)}
                    className="text-sm text-muted-foreground hover:text-gold cursor-pointer transition-colors"
                  >
                    {label}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-4">Legal</h3>
            <ul className="space-y-2">
              {[
                { label: 'Terms of Service', path: '/terms', icon: ScrollText },
                { label: 'Privacy Policy', path: '/privacy', icon: Shield },
                { label: 'Subscription Terms', path: '/subscription-terms', icon: FileText },
                { label: 'Refund Policy', path: '/refund-policy', icon: RefreshCw },
                { label: 'Cookie Policy', path: '/cookie-policy', icon: Cookie },
              ].map(({ label, path, icon: Icon }) => (
                <li key={path}>
                  <span
                    onClick={() => navigate(path)}
                    className="flex items-center space-x-2 text-sm text-muted-foreground hover:text-gold cursor-pointer transition-colors"
                  >
                    <Icon className="h-3 w-3" />
                    <span>{label}</span>
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-10 pt-6 border-t border-border flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-xs text-muted-foreground">
            © {currentYear} SkyHound Studios. All rights reserved.
          </p>
          <p className="text-xs text-muted-foreground text-center">
            For informational and reflective purposes only. Not a substitute for professional advice.
          </p>
          <div className="flex items-center space-x-4">
            <span onClick={() => navigate('/privacy')} className="text-xs text-muted-foreground hover:text-gold cursor-pointer">Privacy</span>
            <span onClick={() => navigate('/terms')} className="text-xs text-muted-foreground hover:text-gold cursor-pointer">Terms</span>
            <span onClick={() => navigate('/contact')} className="text-xs text-muted-foreground hover:text-gold cursor-pointer">Contact</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
