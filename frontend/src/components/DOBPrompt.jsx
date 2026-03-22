import React, { useState } from 'react';
import { X, Sparkles, Star } from 'lucide-react';
import { getSignFromDOB } from '../hooks/useHoroscope';

// ─── Banner variant (top of horoscope page) ───────────────────────────────────
export const DOBBanner = ({ onSave, onDismiss }) => {
  const [dob, setDob] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = () => {
    if (!dob) { setError('Please enter your date of birth'); return; }
    const sign = getSignFromDOB(dob);
    if (!sign) { setError('Could not determine sign. Please check date.'); return; }
    onSave(dob, sign);
  };

  return (
    <div className="mb-6 rounded-xl border border-gold/40 bg-gradient-to-r from-gold/10 via-card to-gold/10 p-4">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 flex-1">
          <div className="bg-gold/20 rounded-full p-2 flex-shrink-0">
            <Star className="h-4 w-4 text-gold" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-semibold mb-1">Personalise your horoscope</p>
            <p className="text-xs text-muted-foreground mb-3">Enter your date of birth to auto-detect your sign and get readings instantly every visit.</p>
            <div className="flex flex-col sm:flex-row gap-2">
              <input
                type="date"
                value={dob}
                onChange={e => { setDob(e.target.value); setError(''); }}
                max={new Date().toISOString().split('T')[0]}
                className="px-3 py-2 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 focus:border-gold transition-all w-full sm:w-auto"
              />
              <button
                onClick={handleSubmit}
                className="px-4 py-2 rounded-lg bg-gold hover:bg-gold/90 text-primary-foreground text-sm font-semibold transition-colors whitespace-nowrap"
              >
                <Sparkles className="h-3.5 w-3.5 inline mr-1.5" />
                Detect my sign
              </button>
            </div>
            {error && <p className="text-xs text-red-500 mt-1.5">{error}</p>}
          </div>
        </div>
        <button
          onClick={onDismiss}
          className="p-1.5 rounded-full hover:bg-muted/60 transition-colors flex-shrink-0 text-muted-foreground hover:text-foreground"
          aria-label="Dismiss"
        >
          <X className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
};

// ─── Modal variant (first visit overlay) ─────────────────────────────────────
export const DOBModal = ({ onSave, onDismiss }) => {
  const [dob, setDob] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = () => {
    if (!dob) { setError('Please enter your date of birth'); return; }
    const sign = getSignFromDOB(dob);
    if (!sign) { setError('Could not determine sign. Please check date.'); return; }
    onSave(dob, sign);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-background/80 backdrop-blur-sm" onClick={onDismiss} />

      {/* Card */}
      <div className="relative z-10 w-full max-w-sm bg-card border-2 border-gold/40 rounded-2xl p-7 shadow-2xl">
        <button
          onClick={onDismiss}
          className="absolute top-4 right-4 p-1.5 rounded-full hover:bg-muted/60 transition-colors text-muted-foreground hover:text-foreground"
        >
          <X className="h-4 w-4" />
        </button>

        <div className="text-center mb-6">
          <div className="text-5xl mb-3">✨</div>
          <h2 className="text-2xl font-playfair font-semibold mb-1">Know your sign?</h2>
          <p className="text-sm text-muted-foreground">
            Enter your date of birth and we'll detect your zodiac sign automatically. No re-selection needed on future visits.
          </p>
        </div>

        <div className="space-y-3">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-1.5">Date of Birth</label>
            <input
              type="date"
              value={dob}
              onChange={e => { setDob(e.target.value); setError(''); }}
              max={new Date().toISOString().split('T')[0]}
              className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 focus:border-gold transition-all"
            />
            {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
          </div>
          <button
            onClick={handleSubmit}
            className="w-full py-2.5 rounded-lg bg-gold hover:bg-gold/90 text-primary-foreground font-semibold text-sm transition-colors"
          >
            <Sparkles className="h-4 w-4 inline mr-2" />
            Detect my sign
          </button>
          <button
            onClick={onDismiss}
            className="w-full py-2 rounded-lg text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            Skip for now
          </button>
        </div>
      </div>
    </div>
  );
};
