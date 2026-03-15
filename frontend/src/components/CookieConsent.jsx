import React, { useState, useEffect } from 'react';
import { Cookie, X, Settings, Check } from 'lucide-react';
import { Button } from './ui/button';
import { useNavigate } from 'react-router-dom';

const COOKIE_KEY = 'eh_cookie_consent';
const COOKIE_VERSION = '1';

const defaultPrefs = {
  necessary: true,
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
    try {
      const stored = localStorage.getItem(COOKIE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        const daysSince = (Date.now() - parsed.timestamp) / (1000 * 60 * 60 * 24);
        if (parsed.version !== COOKIE_VERSION || daysSince > 7) {
          setVisible(true);
        } else {
          setPrefs(parsed.prefs || defaultPrefs);
        }
      } else {
        setVisible(true);
      }
    } catch {
      setVisible(true);
    }
  }, []);

  const save = (selectedPrefs) => {
    localStorage.setItem(COOKIE_KEY, JSON.stringify({
      version: COOKIE_VERSION,
      timestamp: Date.now(),
      prefs: selectedPrefs,
    }));
    setPrefs(selectedPrefs);
    setVisible(false);
    setShowSettings(false);
  };

  const acceptAll = () => save({ necessary: true, analytics: true, personalization: true, marketing: true });
  const acceptNecessary = () => save({ ...defaultPrefs });
  const saveCustom = () => save(prefs);

  if (!visible) return null;

  const bannerStyle = {
    position: 'fixed',
    bottom: 0,
    left: 0,
    right: 0,
    zIndex: 9998,
    padding: '20px 24px',
    backgroundColor: '#1a1a2e',
    borderTop: '2px solid #B8960C',
    boxShadow: '0 -8px 40px rgba(0,0,0,0.7)',
  };

  const textStyle = { color: '#d4d4d4', fontSize: '14px', lineHeight: '1.6' };
  const mutedStyle = { color: '#9ca3af', fontSize: '13px' };
  const goldStyle = { color: '#B8960C', cursor: 'pointer', textDecoration: 'underline' };
  const headingStyle = { color: '#f5f5f5', fontWeight: '600', fontSize: '15px' };

  return (
    <div style={bannerStyle}>
      {!showSettings ? (
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
            <Cookie style={{ color: '#B8960C', width: '20px', height: '20px', flexShrink: 0, marginTop: '2px' }} />
            <p style={textStyle}>
              We use cookies to personalise your experience and improve our services.
              By continuing you agree to our{' '}
              <span style={goldStyle} onClick={() => navigate('/cookie-policy')}>Cookie Policy</span>.
              You can manage your preferences below.
            </p>
          </div>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', justifyContent: 'flex-end' }}>
            <button
              onClick={() => setShowSettings(true)}
              style={{ padding: '8px 16px', background: 'transparent', border: '1px solid #555', color: '#d4d4d4', borderRadius: '6px', cursor: 'pointer', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              <Settings style={{ width: '14px', height: '14px' }} />
              Manage preferences
            </button>
            <button
              onClick={acceptNecessary}
              style={{ padding: '8px 16px', background: 'transparent', border: '1px solid #B8960C', color: '#B8960C', borderRadius: '6px', cursor: 'pointer', fontSize: '13px' }}
            >
              Necessary only
            </button>
            <button
              onClick={acceptAll}
              style={{ padding: '8px 16px', background: '#B8960C', border: 'none', color: '#1a1a2e', borderRadius: '6px', cursor: 'pointer', fontSize: '13px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              <Check style={{ width: '14px', height: '14px' }} />
              Accept all
            </button>
          </div>
        </div>
      ) : (
        <div style={{ maxWidth: '680px', margin: '0 auto' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <span style={{ ...headingStyle, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Cookie style={{ color: '#B8960C', width: '18px', height: '18px' }} />
              Cookie Preferences
            </span>
            <button onClick={() => setShowSettings(false)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#9ca3af' }}>
              <X style={{ width: '18px', height: '18px' }} />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '16px' }}>
            {[
              { key: 'necessary', label: 'Strictly Necessary', desc: 'Authentication, security, core functionality. Always active.', locked: true },
              { key: 'personalization', label: 'Personalisation', desc: 'Customised astrological insights and UI preferences.' },
              { key: 'analytics', label: 'Analytics', desc: 'Help us understand how you use the app to improve it.' },
              { key: 'marketing', label: 'Marketing', desc: 'Referral tracking and campaign performance measurement.' },
            ].map(({ key, label, desc, locked }) => (
              <div key={key} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px 14px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
                <div style={{ flex: 1, marginRight: '16px' }}>
                  <p style={{ ...headingStyle, fontSize: '13px', marginBottom: '2px' }}>{label}</p>
                  <p style={{ ...mutedStyle, fontSize: '12px' }}>{desc}</p>
                </div>
                {locked ? (
                  <span style={{ color: '#B8960C', fontSize: '12px', fontWeight: '500', whiteSpace: 'nowrap' }}>Always on</span>
                ) : (
                  <button
                    onClick={() => setPrefs(p => ({ ...p, [key]: !p[key] }))}
                    style={{
                      width: '40px', height: '22px', borderRadius: '11px', border: 'none', cursor: 'pointer',
                      background: prefs[key] ? '#B8960C' : 'rgba(255,255,255,0.2)',
                      position: 'relative', transition: 'background 0.2s', flexShrink: 0
                    }}
                  >
                    <span style={{
                      position: 'absolute', top: '3px', width: '16px', height: '16px',
                      background: 'white', borderRadius: '50%', transition: 'left 0.2s',
                      left: prefs[key] ? '21px' : '3px'
                    }} />
                  </button>
                )}
              </div>
            ))}
          </div>

          <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
            <button onClick={acceptNecessary} style={{ padding: '8px 14px', background: 'transparent', border: '1px solid #555', color: '#d4d4d4', borderRadius: '6px', cursor: 'pointer', fontSize: '13px' }}>
              Necessary only
            </button>
            <button onClick={saveCustom} style={{ padding: '8px 14px', background: 'transparent', border: '1px solid #B8960C', color: '#B8960C', borderRadius: '6px', cursor: 'pointer', fontSize: '13px' }}>
              Save my preferences
            </button>
            <button onClick={acceptAll} style={{ padding: '8px 14px', background: '#B8960C', border: 'none', color: '#1a1a2e', borderRadius: '6px', cursor: 'pointer', fontSize: '13px', fontWeight: '600' }}>
              Accept all
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export const useCookiePrefs = () => {
  try {
    const stored = localStorage.getItem(COOKIE_KEY);
    if (!stored) return defaultPrefs;
    return JSON.parse(stored).prefs || defaultPrefs;
  } catch {
    return defaultPrefs;
  }
};
