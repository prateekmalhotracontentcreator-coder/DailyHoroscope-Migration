import React, { useState, useEffect } from 'react';
import { Cookie, X, Settings, Check } from 'lucide-react';
import { Button } from './ui/button';
import { useNavigate } from 'react-router-dom';

const COOKIE_KEY = 'eh_cookie_consent';
const COOKIE_VERSION = '1';

const defaultPrefs = {
  necessary: true,      // always on
  analytics: false,
  personalization: true,
  marketing: false,
};

export const CookieConsent = () => {
  const navigate = useNavigate();
  const [visible, setVisible] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [prefs, setPrefs] = useState(defaultPrefs);

  useEffect(() => {
    const stored = localStorage.getItem(COOKIE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored);
      // Re-prompt if it's been more than 7 days (weekly re-consent)
      const daysSince = (Date.now() - parsed.timestamp) / (1000 * 60 * 60 * 24);
      if (parsed.version !== COOKIE_VERSION || daysSince > 7) {
        setVisible(true);
      }
    } else {
      setVisible(true);
    }
  }, []);

  const save = (selectedPrefs) => {
    localStorage.setItem(COOKIE_KEY, JSON.stringify({
      version: COOKIE_VERSION,
      timestamp: Date.now(),
      prefs: selectedPrefs,
    }));
    setVisible(false);
  };

  const acceptAll = () => {
    const all = { necessary: true, analytics: true, personalization: true, marketing: true };
    setPrefs(all);
    save(all);
  };

  const acceptNecessary = () => {
    const necessary = { ...defaultPrefs };
    save(necessary);
  };

  const saveCustom = () => save(prefs);

  if (!visible) return null;

  return (
    <div style={{
      position: 'fixed', bottom: 0, left: 0, right: 0, zIndex: 9998,
      padding: '16px',
      background: 'var(--color-background-secondary)',
      borderTop: '1px solid var(--color-border-primary)',
      boxShadow: '0 -8px 32px rgba(0,0,0,0.25)'
    }}>
      {!showSettings ? (
        // Simple banner
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-start md:items-center gap-4">
          <div className="flex items-start space-x-3 flex-1">
            <Cookie className="h-5 w-5 text-gold shrink-0 mt-0.5" />
            <p className="text-sm text-muted-foreground leading-relaxed">
              We use cookies to personalise your experience and improve our services.
              By continuing you agree to our{' '}
              <span onClick={() => navigate('/cookie-policy')} className="text-gold hover:underline cursor-pointer">Cookie Policy</span>.
              {' '}You can manage your preferences at any time.
            </p>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <Button variant="outline" size="sm" onClick={() => setShowSettings(true)} className="text-xs border-border">
              <Settings className="h-3 w-3 mr-1" />Manage
            </Button>
            <Button variant="outline" size="sm" onClick={acceptNecessary} className="text-xs">
              Necessary only
            </Button>
            <Button size="sm" onClick={acceptAll} className="text-xs bg-gold hover:bg-gold/90 text-primary-foreground">
              <Check className="h-3 w-3 mr-1" />Accept all
            </Button>
          </div>
        </div>
      ) : (
        // Detailed settings
        <div className="max-w-2xl mx-auto">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold flex items-center gap-2">
              <Cookie className="h-4 w-4 text-gold" />Cookie Preferences
            </h3>
            <button onClick={() => setShowSettings(false)} className="text-muted-foreground hover:text-foreground">
              <X className="h-4 w-4" />
            </button>
          </div>

          <div className="space-y-3 mb-4">
            {[
              { key: 'necessary', label: 'Strictly Necessary', desc: 'Authentication, security, core functionality. Cannot be disabled.', locked: true },
              { key: 'personalization', label: 'Personalisation', desc: 'Customised astrological insights and UI preferences.' },
              { key: 'analytics', label: 'Analytics', desc: 'Help us understand how you use the app to improve it.' },
              { key: 'marketing', label: 'Marketing', desc: 'Referral tracking and campaign performance.' },
            ].map(({ key, label, desc, locked }) => (
              <div key={key} className="flex items-start justify-between p-3 rounded-lg border border-border bg-muted/20">
                <div className="flex-1 mr-4">
                  <p className="text-sm font-medium">{label}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{desc}</p>
                </div>
                <div className="shrink-0">
                  {locked ? (
                    <span className="text-xs text-gold font-medium">Always on</span>
                  ) : (
                    <button
                      onClick={() => setPrefs(p => ({ ...p, [key]: !p[key] }))}
                      className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors ${prefs[key] ? 'bg-gold' : 'bg-muted-foreground/30'}`}
                    >
                      <span className={`inline-block h-3.5 w-3.5 rounded-full bg-white transition-transform ${prefs[key] ? 'translate-x-4' : 'translate-x-0.5'}`} />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>

          <div className="flex gap-2 justify-end">
            <Button variant="outline" size="sm" onClick={acceptNecessary} className="text-xs">Necessary only</Button>
            <Button size="sm" onClick={saveCustom} className="text-xs bg-gold hover:bg-gold/90 text-primary-foreground">Save preferences</Button>
            <Button size="sm" onClick={acceptAll} className="text-xs bg-primary">Accept all</Button>
          </div>
        </div>
      )}
    </div>
  );
};

// Hook to read cookie preferences anywhere in the app
export const useCookiePrefs = () => {
  const stored = localStorage.getItem(COOKIE_KEY);
  if (!stored) return defaultPrefs;
  try {
    return JSON.parse(stored).prefs || defaultPrefs;
  } catch {
    return defaultPrefs;
  }
};
