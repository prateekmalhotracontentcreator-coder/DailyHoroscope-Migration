import React, { useEffect, useState } from 'react';
import { Navigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Crown, Lock, Sparkles } from 'lucide-react';

// ── Reusable premium gate card ──────────────────────────────────────────────────
// Used both by PremiumRoute wrapper and inline auth-aware pages (KP, Strategist)
export const PremiumGateCard = ({ feature = 'Premium Feature', description }) => (
  <div className="min-h-screen bg-background flex items-center justify-center px-4">
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm max-w-md w-full p-8 text-center space-y-5">
      <div className="flex justify-center">
        <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gold/10 text-gold">
          <Lock className="h-8 w-8" />
        </div>
      </div>
      <div className="space-y-2">
        <p className="text-xs uppercase tracking-widest text-gold/70">Premium Feature</p>
        <h1 className="text-2xl font-semibold text-foreground">{feature}</h1>
        <p className="text-sm leading-7 text-muted-foreground">
          {description ||
            `${feature} is exclusive to Premium subscribers. Upgrade to unlock full access.`}
        </p>
      </div>
      <Link
        to="/pricing"
        className="inline-flex items-center justify-center gap-2 rounded-full border border-gold bg-gold px-6 py-3 text-sm font-semibold text-primary-foreground transition hover:bg-gold/90"
      >
        <Crown className="h-4 w-4" />
        Upgrade to Premium
      </Link>
      <p className="text-xs text-muted-foreground">
        Already subscribed?{' '}
        <button
          type="button"
          onClick={() => window.location.reload()}
          className="text-gold hover:opacity-80 transition"
        >
          Refresh the page
        </button>
      </p>
    </div>
  </div>
);

// ── Route wrapper ───────────────────────────────────────────────────────────────
// • Not logged in → redirect to /login
// • Logged in, not premium → PremiumGateCard (view-only placeholder)
// • Logged in, premium → render children
export const PremiumRoute = ({ children, feature, description }) => {
  const { user, loading } = useAuth();
  const location = useLocation();
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!loading) setIsReady(true);
  }, [loading]);

  if (!isReady || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Sparkles className="h-16 w-16 text-gold mx-auto mb-4 animate-pulse" />
          <p className="text-xl font-playfair italic text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (!user.is_premium) {
    return <PremiumGateCard feature={feature} description={description} />;
  }

  return children;
};
