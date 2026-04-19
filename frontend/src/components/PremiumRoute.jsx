import React, { useEffect, useState } from 'react';
import { Navigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Crown, Sparkles } from 'lucide-react';

export const PremiumRoute = ({ children }) => {
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
    return (
      <div className="min-h-screen bg-background flex items-center justify-center px-4">
        <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm max-w-md w-full p-8 text-center space-y-5">
          <div className="flex justify-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gold/10 text-gold">
              <Crown className="h-8 w-8" />
            </div>
          </div>
          <div className="space-y-2">
            <h1 className="text-2xl font-semibold text-foreground">Premium Feature</h1>
            <p className="text-sm leading-7 text-muted-foreground">
              Arc Angel — 12 Areas of Life is exclusive to Premium subscribers. Upgrade to unlock
              your 10-year Vedic dasha map across all life domains.
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
  }

  return children;
};
