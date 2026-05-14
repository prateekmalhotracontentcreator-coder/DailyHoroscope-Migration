import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { SEO } from '../../components/SEO';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { useAuth } from '../../context/AuthContext';
import {
  fetchPunyaLeaderboard,
  fetchPunyaLedger,
  fetchPunyaPublicConfig,
  fetchPunyaSpins,
  fetchPunyaSummary,
  spinPunyaWheel,
} from '../../lib/punyaRewards';
import { ArrowRight, Coins, Sparkles, Trophy, Gift, Loader2 } from 'lucide-react';

const WHEEL_COLORS = ['#c5a059', '#8f5f2a', '#f2d089', '#6e4e1f', '#ddba71', '#9d6f34', '#f5dfab', '#7d5730'];

function formatPrize(segment) {
  if (!segment) return 'Temple blessing recorded';
  if (segment.prize_type === 'points') return `${segment.prize_value} Punya Points`;
  if (segment.prize_type === 'soft_loss') return segment.label;
  return segment.label;
}

export default function PunyaRewardsPage() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [publicConfig, setPublicConfig] = useState(null);
  const [summary, setSummary] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [ledger, setLedger] = useState([]);
  const [spins, setSpins] = useState([]);
  const [loading, setLoading] = useState(true);
  const [spinning, setSpinning] = useState(false);
  const [rotation, setRotation] = useState(0);
  const [spinResult, setSpinResult] = useState(null);
  const [error, setError] = useState('');

  const segments = (summary?.wheel_segments?.length ? summary.wheel_segments : publicConfig?.wheel_segments) || [];
  const actionRules = publicConfig?.action_rules || {};

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      setError('');
      try {
        const [configData, leaderboardData] = await Promise.all([
          fetchPunyaPublicConfig(),
          fetchPunyaLeaderboard(),
        ]);
        if (cancelled) return;
        setPublicConfig(configData);
        setLeaderboard(leaderboardData.leaderboard || []);

        if (user?.email) {
          const [summaryData, ledgerData, spinsData] = await Promise.all([
            fetchPunyaSummary(),
            fetchPunyaLedger(),
            fetchPunyaSpins(),
          ]);
          if (cancelled) return;
          setSummary(summaryData);
          setLedger(ledgerData);
          setSpins(spinsData);
        } else {
          setSummary(null);
          setLedger([]);
          setSpins([]);
        }
      } catch (loadError) {
        if (!cancelled) {
          setError(loadError?.response?.data?.detail || 'Punya Rewards is waking up. Please try again.');
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [user?.email]);

  const wheelStyle = useMemo(() => {
    if (!segments.length) return {};
    const slice = 360 / segments.length;
    const stops = segments.map((segment, index) => {
      const start = index * slice;
      const end = start + slice;
      return `${WHEEL_COLORS[index % WHEEL_COLORS.length]} ${start}deg ${end}deg`;
    });
    return {
      background: `conic-gradient(${stops.join(', ')})`,
      transform: `rotate(${rotation}deg)`,
      transition: spinning ? 'transform 4.5s cubic-bezier(0.12, 0.72, 0, 1)' : 'transform 0.9s ease',
    };
  }, [rotation, segments, spinning]);

  const earnRows = Object.entries(actionRules).map(([actionCode, rule]) => ({
    actionCode,
    label: rule.label,
    points: rule.points,
    capWindow: rule.cap_window,
    capCount: rule.cap_count,
  }));

  async function handleSpin(spinMode = 'auto') {
    if (!user?.email || !segments.length || spinning) return;
    setSpinning(true);
    setSpinResult(null);
    try {
      const response = await spinPunyaWheel(spinMode);
      const nextSpin = response.spin;
      const index = Math.max(segments.findIndex(segment => segment.segment_id === nextSpin.segment_id), 0);
      const slice = 360 / segments.length;
      const targetCenter = index * slice + slice / 2;
      const targetRotation = rotation + 1800 + (360 - targetCenter);
      setRotation(targetRotation);
      setSummary(response.summary || null);
      setSpinResult(nextSpin);
      setSpins(current => [nextSpin, ...current].slice(0, 20));
      setLeaderboard((response.summary?.leaderboard || leaderboard));
      const refreshedLedger = await fetchPunyaLedger();
      setLedger(refreshedLedger);
    } catch (spinError) {
      setError(spinError?.response?.data?.detail || 'Spin could not complete right now.');
    } finally {
      setTimeout(() => setSpinning(false), 4500);
    }
  }

  return (
    <div className="min-h-screen px-4 py-10 sm:px-6 lg:px-8">
      <SEO
        title="Punya Rewards — Earn Points, Spin the Wheel"
        description="Earn Punya Points across EverydayHoroscope, claim your Daily Blessing, and spin the wheel for rewards."
        url="https://www.everydayhoroscope.in/punya-rewards"
      />

      <div className="mx-auto max-w-6xl space-y-8">
        <section className="overflow-hidden rounded-3xl border border-gold/20 bg-[radial-gradient(circle_at_top_left,rgba(197,160,89,0.18),transparent_30%),linear-gradient(135deg,rgba(197,160,89,0.08),rgba(12,10,6,0.96))] p-8">
          <div className="grid gap-8 lg:grid-cols-[1.2fr,0.8fr]">
            <div className="space-y-4">
              <div className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.28em] text-gold">
                <Sparkles className="h-3.5 w-3.5" />
                Punya Rewards
              </div>
              <h1 className="font-playfair text-4xl font-semibold text-foreground sm:text-5xl">
                Earn Punya Points across the Temple.
              </h1>
              <p className="max-w-2xl text-sm leading-7 text-muted-foreground sm:text-base">
                Punya Rewards is the shared merit layer for EverydayHoroscope. Read, generate, share, and return daily to build your balance, unlock extra spins, and land blessings from the wheel.
              </p>

              {user?.email && summary ? (
                <div className="grid gap-3 sm:grid-cols-3">
                  <Card className="border-gold/25 bg-gold/10 p-5">
                    <p className="text-xs uppercase tracking-[0.24em] text-gold/80">Balance</p>
                    <p className="mt-2 text-3xl font-semibold text-foreground">{summary.balance}</p>
                    <p className="mt-1 text-xs text-muted-foreground">Punya Points</p>
                  </Card>
                  <Card className="border-gold/25 bg-gold/10 p-5">
                    <p className="text-xs uppercase tracking-[0.24em] text-gold/80">Daily Blessing</p>
                    <p className="mt-2 text-lg font-semibold text-foreground">
                      {summary.daily_free_spin_available ? 'Ready to spin' : 'Already used today'}
                    </p>
                    <p className="mt-1 text-xs text-muted-foreground">1 free spin each IST day</p>
                  </Card>
                  <Card className="border-gold/25 bg-gold/10 p-5">
                    <p className="text-xs uppercase tracking-[0.24em] text-gold/80">Login Streak</p>
                    <p className="mt-2 text-3xl font-semibold text-foreground">{summary.login_streak}</p>
                    <p className="mt-1 text-xs text-muted-foreground">Consecutive Temple days</p>
                  </Card>
                </div>
              ) : (
                <Card className="max-w-xl border-gold/20 bg-gold/10 p-5">
                  <p className="text-sm text-muted-foreground">
                    Sign in to see your Punya Points balance, claim your Daily Blessing, and store every spin in your account history.
                  </p>
                  <Button onClick={() => navigate('/login')} className="mt-4 bg-gold text-primary-foreground hover:bg-gold/90">
                    Sign In to Earn
                  </Button>
                </Card>
              )}
            </div>

            <div className="flex flex-col items-center justify-center">
              <div className="relative">
                <div className="absolute left-1/2 top-[-18px] z-20 h-0 w-0 -translate-x-1/2 border-l-[16px] border-r-[16px] border-b-[28px] border-l-transparent border-r-transparent border-b-gold" />
                <div
                  className="relative h-[300px] w-[300px] rounded-full border-[10px] border-gold/40 shadow-[0_18px_60px_rgba(0,0,0,0.35)]"
                  style={wheelStyle}
                >
                  <div className="absolute inset-[18px] rounded-full border border-white/10" />
                  <div className="absolute left-1/2 top-1/2 z-10 flex h-20 w-20 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full border border-gold/30 bg-background/90 text-center shadow-lg">
                    <span className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Spin</span>
                  </div>
                </div>
              </div>

              <div className="mt-6 flex flex-wrap justify-center gap-3">
                <Button
                  onClick={() => handleSpin(summary?.daily_free_spin_available ? 'free' : 'auto')}
                  disabled={!user?.email || loading || spinning}
                  className="bg-gold text-primary-foreground hover:bg-gold/90"
                >
                  {spinning ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Gift className="mr-2 h-4 w-4" />}
                  {summary?.daily_free_spin_available ? 'Use Daily Blessing' : 'Spin the Wheel'}
                </Button>
                <Button
                  onClick={() => handleSpin('paid')}
                  disabled={!user?.email || loading || spinning || (summary?.balance || 0) < (summary?.spin_cost_points || publicConfig?.spin_cost_points || 50)}
                  variant="outline"
                  className="border-gold/40 text-gold hover:bg-gold/10"
                >
                  Extra Spin for {summary?.spin_cost_points || publicConfig?.spin_cost_points || 50}
                </Button>
              </div>

              {spinResult ? (
                <p className="mt-4 max-w-sm text-center text-sm text-muted-foreground">
                  Wheel result: <span className="font-semibold text-foreground">{formatPrize(spinResult)}</span>
                </p>
              ) : null}
            </div>
          </div>
        </section>

        {error ? (
          <Card className="border-red-400/30 bg-red-500/10 p-4 text-sm text-red-200">
            {error}
          </Card>
        ) : null}

        <section className="grid gap-6 lg:grid-cols-[1fr,1fr]">
          <Card className="border-gold/20 p-6">
            <div className="mb-4 flex items-center gap-2">
              <Coins className="h-4 w-4 text-gold" />
              <h2 className="font-playfair text-2xl font-semibold">How You Earn</h2>
            </div>
            <div className="space-y-3">
              {earnRows.map(row => (
                <div key={row.actionCode} className="flex items-start justify-between gap-4 rounded-2xl border border-border/70 bg-card/60 px-4 py-3">
                  <div>
                    <p className="text-sm font-medium text-foreground">{row.label}</p>
                    <p className="text-xs text-muted-foreground">
                      {row.capWindow === 'reference'
                        ? 'Per unique action'
                        : row.capWindow === 'week'
                          ? `Up to ${row.capCount}x per week`
                          : row.capWindow === 'month'
                            ? `Up to ${row.capCount}x per month`
                            : row.capWindow === 'day'
                              ? `Up to ${row.capCount}x per day`
                              : 'No cap'}
                    </p>
                  </div>
                  <div className="rounded-full border border-gold/30 bg-gold/10 px-3 py-1 text-sm font-semibold text-gold">
                    +{row.points}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card className="border-gold/20 p-6">
            <div className="mb-4 flex items-center gap-2">
              <Trophy className="h-4 w-4 text-gold" />
              <h2 className="font-playfair text-2xl font-semibold">This Week's Leaders</h2>
            </div>
            <div className="space-y-3">
              {leaderboard.length ? leaderboard.map(entry => (
                <div key={entry.rank + entry.user_id} className="flex items-center justify-between rounded-2xl border border-border/70 px-4 py-3">
                  <div>
                    <p className="text-sm font-medium text-foreground">
                      #{entry.rank} {entry.user_name}
                    </p>
                    <p className="text-xs text-muted-foreground">{entry.user_email}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold text-gold">{entry.weekly_points} pts</p>
                    <p className="text-xs text-muted-foreground">Balance {entry.balance}</p>
                  </div>
                </div>
              )) : (
                <p className="text-sm text-muted-foreground">The leaderboard will populate as this week's earning activity comes in.</p>
              )}
            </div>
          </Card>
        </section>

        <section className="grid gap-6 lg:grid-cols-[0.9fr,1.1fr]">
          <Card className="border-gold/20 p-6">
            <div className="mb-4 flex items-center gap-2">
              <Gift className="h-4 w-4 text-gold" />
              <h2 className="font-playfair text-2xl font-semibold">Wheel Segments</h2>
            </div>
            <div className="space-y-3">
              {segments.map((segment, index) => (
                <div key={segment.segment_id || segment.label} className="flex items-center gap-3 rounded-2xl border border-border/70 px-4 py-3">
                  <span
                    className="h-4 w-4 rounded-full border border-white/20"
                    style={{ backgroundColor: WHEEL_COLORS[index % WHEEL_COLORS.length] }}
                  />
                  <div>
                    <p className="text-sm font-medium text-foreground">{segment.label}</p>
                    <p className="text-xs text-muted-foreground">{segment.prize_type}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <div className="grid gap-6">
            <Card className="border-gold/20 p-6">
              <div className="mb-4 flex items-center gap-2">
                <Coins className="h-4 w-4 text-gold" />
                <h2 className="font-playfair text-2xl font-semibold">Recent Ledger</h2>
              </div>
              {user?.email ? (
                <div className="space-y-3">
                  {ledger.length ? ledger.slice(0, 8).map(entry => (
                    <div key={entry.transaction_id} className="flex items-center justify-between rounded-2xl border border-border/70 px-4 py-3">
                      <div>
                        <p className="text-sm font-medium text-foreground">{entry.reason_code.replace(/_/g, ' ')}</p>
                        <p className="text-xs text-muted-foreground">{new Date(entry.created_at).toLocaleString('en-IN')}</p>
                      </div>
                      <div className={`text-sm font-semibold ${entry.direction === 'credit' ? 'text-emerald-400' : 'text-red-300'}`}>
                        {entry.direction === 'credit' ? '+' : '-'}
                        {entry.amount}
                      </div>
                    </div>
                  )) : (
                    <p className="text-sm text-muted-foreground">Your Punya ledger will appear here after your first earning event.</p>
                  )}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">Sign in to open your personal transaction ledger.</p>
              )}
            </Card>

            <Card className="border-gold/20 p-6">
              <div className="mb-4 flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-gold" />
                <h2 className="font-playfair text-2xl font-semibold">Recent Spins</h2>
              </div>
              {user?.email ? (
                <div className="space-y-3">
                  {spins.length ? spins.slice(0, 6).map(entry => (
                    <div key={entry.spin_id} className="flex items-center justify-between rounded-2xl border border-border/70 px-4 py-3">
                      <div>
                        <p className="text-sm font-medium text-foreground">{entry.prize_segment}</p>
                        <p className="text-xs text-muted-foreground">
                          {entry.is_free_spin ? 'Daily Blessing' : `${entry.spin_cost_points} points`} · {new Date(entry.created_at).toLocaleString('en-IN')}
                        </p>
                      </div>
                      <div className="text-right text-xs text-muted-foreground">
                        <p>{entry.prize_type}</p>
                      </div>
                    </div>
                  )) : (
                    <p className="text-sm text-muted-foreground">Your spin history will appear here once the wheel turns.</p>
                  )}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">Sign in to save your Daily Blessing and spin history.</p>
              )}
            </Card>
          </div>
        </section>

        <Card className="border-gold/20 p-6">
          <div className="mb-4 flex items-center gap-2">
            <ArrowRight className="h-4 w-4 text-gold" />
            <h2 className="font-playfair text-2xl font-semibold">Implementation Notes</h2>
          </div>
          <p className="text-sm leading-7 text-muted-foreground">
            Spin probabilities are resolved server-side only. Balance, streaks, and every reward movement are kept in a centralized ledger so Temple Team can audit earnings, spends, spin costs, and spin prizes from one place.
          </p>
        </Card>
      </div>
    </div>
  );
}
