import React, { useEffect, useState } from 'react';
import { Navigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Crown, Lock, Sparkles, BookOpen } from 'lucide-react';

// ── SEO Resource Gate ────────────────────────────────────────────────────────────
// Gate for SEO Resource Content (Angel Numbers, Faith, Crystals, Lo Shu, Rudraksha, Tarot Library).
// Logic:
//   • Not logged in  → teaser (page visible, interactions locked) + SeoResourceGateCard
//   • Logged in (any tier, including free) → full access
//   • NB: this is intentionally NOT checking is_premium -- free registration unlocks all SEO Resource Content.

export const SeoResourceGateCard = ({ feature = 'Premium Content' }) => {
  const location = useLocation();
  return (
    <div className="flex justify-center px-4 py-12 bg-background">
      <div className="rounded-2xl border border-gold/25 bg-gold/[0.04] shadow-lg max-w-md w-full p-8 text-center space-y-6">

        {/* Capsule badge */}
        <div className="flex justify-center">
          <span className="inline-flex items-center gap-2 rounded-full bg-gold/15 border border-gold/35 px-5 py-1.5 text-xs font-semibold text-gold tracking-wide uppercase">
            <Crown className="h-3.5 w-3.5 shrink-0" />
            Login &amp; Subscribe for Premium Content -- It&apos;s Free
          </span>
        </div>

        {/* Lock icon */}
        <div className="flex justify-center">
          <div className="flex h-14 w-14 items-center justify-center rounded-full bg-gold/10 text-gold ring-1 ring-gold/20">
            <Lock className="h-7 w-7" />
          </div>
        </div>

        {/* Copy */}
        <div className="space-y-2">
          <h2 className="text-xl font-semibold text-foreground">{feature}</h2>
          <p className="text-sm leading-6 text-muted-foreground">
            Create a free account to unlock this library -- every guide, interpretation,
            and insight is included with your free membership.
          </p>
        </div>

        {/* CTAs */}
        <div className="flex flex-col gap-3">
          <Link
            to="/register"
            state={{ from: location }}
            className="inline-flex items-center justify-center gap-2 rounded-full bg-gold px-6 py-3 text-sm font-semibold text-primary-foreground hover:bg-gold/90 transition"
          >
            <Sparkles className="h-4 w-4 shrink-0" />
            Register Free -- Unlock Now
          </Link>
          <Link
            to="/login"
            state={{ from: location }}
            className="inline-flex items-center justify-center gap-2 rounded-full border border-gold/30 px-6 py-2.5 text-sm font-medium text-foreground hover:bg-gold/5 transition"
          >
            Already have an account? Login
          </Link>
        </div>

        {/* Reassurance */}
        <p className="text-xs text-muted-foreground">
          No credit card required &nbsp;·&nbsp; Free forever for registered members
        </p>
      </div>
    </div>
  );
};

export const SeoResourceGate = ({ children, feature }) => {
  const { user, loading } = useAuth();
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

  // Any logged-in user (free or premium) gets full access
  if (user) return children;

  // Not logged in: show teaser + gate card
  // The page renders fully so Google can read the DOM, but pointer-events-none
  // disables all interactions -- links, buttons, inputs -- forcing registration.
  return (
    <div className="relative">
      {/* Teaser window -- visible but non-interactive */}
      <div
        className="max-h-[68vh] overflow-hidden relative pointer-events-none select-none"
        aria-hidden="true"
      >
        {children}
        {/* Gradient fade-out at the bottom */}
        <div className="absolute bottom-0 left-0 right-0 h-48 bg-gradient-to-t from-background via-background/70 to-transparent" />
      </div>

      {/* Gate card appears below the teaser */}
      <SeoResourceGateCard feature={feature} />
    </div>
  );
};

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
