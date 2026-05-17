import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { ChevronDown } from "lucide-react";

import { useAuth } from "../context/AuthContext";

const BASE_URL =
  process.env.REACT_APP_BACKEND_URL || "https://everydayhoroscope-api.onrender.com";

const ARC_ANGEL_DOMAINS = [
  { id: "health", label: "Health & Fitness", description: "Physical well-being, nutrition, exercise and energy levels" },
  { id: "career", label: "Career & Work", description: "Professional fulfillment, vocational growth and passion" },
  { id: "finances", label: "Finances", description: "Financial stability, wealth management and security" },
  { id: "learning", label: "Intellectual Life & Learning", description: "Continuous education, new skills and mental growth" },
  { id: "emotional", label: "Emotional Life", description: "Mental health, managing stress and self-awareness" },
  { id: "spirituality", label: "Spirituality", description: "Purpose, meaning in life and connection to something higher" },
  { id: "relationships", label: "Love Relationships", description: "Quality of romantic relationship or companionship" },
  { id: "family", label: "Family Life", description: "Relationships with family members and parenting" },
  { id: "social", label: "Social Life & Friendship", description: "Social connections, community and networking" },
  { id: "adventure", label: "Adventure & Travel", description: "Experiences, exploring new places and taking risks" },
  { id: "environment", label: "Environment", description: "Quality of your surroundings, home and workspace" },
  { id: "creativity", label: "Creativity & Hobbies", description: "Hobbies, artistic pursuits and leisure time" },
];

function formatMonthYear(value) {
  if (!value) return "-";
  const [yearValue, monthValue] = String(value).split("-");
  const year = Number(yearValue);
  const month = Number(monthValue);
  if (!year || !month || month < 1 || month > 12) return String(value);
  return new Intl.DateTimeFormat("en-US", { month: "short", year: "numeric" }).format(
    new Date(Date.UTC(year, month - 1, 1))
  );
}

function formatRange(start, end) {
  return `${formatMonthYear(start)} - ${formatMonthYear(end)}`;
}

function qualityBorderClass(quality) {
  if (quality === "auspicious") return "border-l-green-500";
  if (quality === "inauspicious") return "border-l-red-500";
  return "border-l-gray-400";
}

function Donut({ pct, size = 50, label }) {
  const safePct = Math.max(0, Math.min(100, Number(pct) || 0));
  const radius = (size - 6) / 2;
  const circumference = 2 * Math.PI * radius;
  const filled = (safePct / 100) * circumference;

  return (
    <div className="relative flex h-14 w-14 items-center justify-center">
      <svg width={size} height={size} className="rotate-[-90deg]">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth="4"
          className="text-muted-foreground/20"
          strokeDasharray={circumference}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth="4"
          className="text-gold"
          strokeDasharray={`${filled} ${circumference - filled}`}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center text-[11px] font-semibold text-foreground">
        {label || `${safePct}%`}
      </div>
    </div>
  );
}

function ProgressBar({ value }) {
  const safeValue = Math.max(0, Math.min(100, Number(value) || 0));
  return (
    <div className="space-y-2">
      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">
        Profile completeness: {safeValue}%
      </p>
      <svg viewBox="0 0 100 4" className="h-1.5 w-full overflow-hidden rounded-full">
        <rect x="0" y="0" width="100" height="4" rx="2" className="fill-muted-foreground/15" />
        <rect x="0" y="0" width={safeValue} height="4" rx="2" className="fill-gold" />
      </svg>
    </div>
  );
}

function LoadingRows() {
  return (
    <div className="space-y-2">
      {ARC_ANGEL_DOMAINS.map((domain, index) => (
        <div
          key={domain.id}
          className={`animate-pulse rounded-xl border border-gold/15 border-l-4 px-3 py-3 ${
            index % 2 === 0 ? "bg-card" : "bg-background/50"
          } border-l-gray-400`}
        >
          <div className="flex items-center justify-between gap-3">
            <div className="min-w-0 flex-1 space-y-2">
              <div className="h-4 w-32 rounded bg-muted-foreground/20" />
              <div className="h-3 w-full rounded bg-muted-foreground/15" />
            </div>
            <div className="h-12 w-12 rounded-full bg-muted-foreground/15" />
          </div>
        </div>
      ))}
    </div>
  );
}

function PeriodList({ title, periods }) {
  const visiblePeriods = periods.slice(0, 3);
  return (
    <div className="rounded-lg border border-gold/15 bg-background/50 p-3">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-gold">{title}</p>
      {visiblePeriods.length ? (
        <div className="mt-2 space-y-2">
          {visiblePeriods.map((period, index) => (
            <div key={`${title}-${period.start || "s"}-${period.end || "e"}-${index}`} className="text-xs">
              <p className="font-medium text-foreground">{formatRange(period.start, period.end)}</p>
              <p className="mt-1 text-muted-foreground">{period.driver || "Timing window available"}</p>
            </div>
          ))}
        </div>
      ) : (
        <p className="mt-2 text-xs text-muted-foreground">No major windows listed.</p>
      )}
    </div>
  );
}

export default function ArcAngelPanel() {
  const { user } = useAuth();
  const [birthProfile, setBirthProfile] = useState(null);
  const [profileLoading, setProfileLoading] = useState(false);
  const [payload, setPayload] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [expandedDomain, setExpandedDomain] = useState("");

  useEffect(() => {
    if (!user) {
      setBirthProfile(null);
      return;
    }
    let active = true;
    async function fetchProfile() {
      setProfileLoading(true);
      try {
        const res = await axios.get(`${BASE_URL}/api/profile/birth`, { withCredentials: true });
        if (!active) return;
        const profiles = Array.isArray(res.data) ? res.data : [];
        setBirthProfile(profiles[0] || null);
      } catch {
        if (active) setBirthProfile(null);
      } finally {
        if (active) setProfileLoading(false);
      }
    }
    fetchProfile();
    return () => {
      active = false;
    };
  }, [user]);

  useEffect(() => {
    if (!birthProfile) {
      setPayload(null);
      setError("");
      return;
    }
    let active = true;
    async function fetchPayload() {
      setLoading(true);
      setError("");
      try {
        const res = await axios.get(`${BASE_URL}/api/knowledge-engine/arc-angel-windows`, {
          params: {
            birth_date: birthProfile.date_of_birth,
            birth_time: birthProfile.time_of_birth,
            birth_place: birthProfile.location,
          },
          withCredentials: true,
        });
        if (!active) return;
        setPayload(res.data || null);
      } catch {
        if (!active) return;
        setPayload(null);
        setError("Unable to load your profile. Try again later.");
      } finally {
        if (active) setLoading(false);
      }
    }
    fetchPayload();
    return () => {
      active = false;
    };
  }, [birthProfile]);

  const windowsByDomain = useMemo(() => {
    const items = Array.isArray(payload?.arc_angel_windows) ? payload.arc_angel_windows : [];
    return items.reduce((acc, item) => {
      if (item?.domain_id) {
        acc[item.domain_id] = item;
      }
      return acc;
    }, {});
  }, [payload]);

  const rows = useMemo(
    () =>
      ARC_ANGEL_DOMAINS.map((domain) => {
        const item = windowsByDomain[domain.id] || {};
        return {
          ...domain,
          periodQualityNow: item.period_quality_now || payload?.domain_quality_now?.[domain.id] || "neutral",
          domainConfidencePct: Number(item.domain_confidence_pct) || 40,
          hasQualityBadge: Boolean(item.has_quality_badge),
          auspiciousPeriods: Array.isArray(item.auspicious_periods) ? item.auspicious_periods : [],
          inauspiciousPeriods: Array.isArray(item.inauspicious_periods) ? item.inauspicious_periods : [],
        };
      }),
    [payload, windowsByDomain]
  );

  if (!user) return null;

  if (!profileLoading && !birthProfile) {
    return (
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-4 space-y-3">
        <p className="text-sm leading-6 text-muted-foreground">
          Enter your birth details in Account Settings to activate your Janma Kundali Snapshot.
        </p>
        <Link
          to="/account"
          className="inline-flex items-center justify-center rounded-full border border-gold px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/10"
        >
          Go to Account Settings
        </Link>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm">
      <div className="space-y-4 p-4">
        <ProgressBar value={payload?.overall_confidence_pct || 0} />

        <div className="rounded-xl bg-gradient-to-br from-gold/15 to-gold/5 p-4">
          <div className="flex items-center gap-4">
            <Donut pct={payload?.overall_confidence_pct || 0} size={58} />
            <div className="min-w-0">
              <p className="text-sm font-semibold text-foreground">Arc Angel Confidence</p>
              <p className="text-xs text-muted-foreground">Vedic Astrology Engine Activated</p>
            </div>
          </div>
          <Link
            to="/questionnaire"
            className="mt-4 inline-flex text-sm font-semibold text-gold transition hover:opacity-80"
          >
            🔓 Unlock the Potential of Vedic Astrology in all 12 Areas of Life
          </Link>
        </div>

        {profileLoading || loading ? (
          <LoadingRows />
        ) : error ? (
          <p className="text-sm text-red-500">{error}</p>
        ) : (
          <div className="space-y-2">
            {rows.map((row, index) => {
              const open = expandedDomain === row.id;
              return (
                <div
                  key={row.id}
                  className={`overflow-hidden rounded-xl border border-gold/15 border-l-4 ${
                    index % 2 === 0 ? "bg-card" : "bg-background/50"
                  } ${qualityBorderClass(row.periodQualityNow)}`}
                >
                  <button
                    onClick={() => setExpandedDomain((current) => (current === row.id ? "" : row.id))}
                    className="flex w-full items-center justify-between gap-3 px-3 py-3 text-left"
                  >
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-semibold text-foreground">{row.label}</p>
                      <p className="mt-1 text-xs leading-5 text-muted-foreground">{row.description}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      {row.hasQualityBadge ? (
                        <span className="rounded-full border border-gold/25 bg-background/60 px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.14em] text-gold">
                          ⭐ Premium
                        </span>
                      ) : null}
                      <Donut pct={row.domainConfidencePct} label={`${row.domainConfidencePct}%`} />
                      <ChevronDown className={`h-4 w-4 text-gold transition-transform ${open ? "rotate-180" : ""}`} />
                    </div>
                  </button>
                  {open ? (
                    <div className="grid gap-3 border-t border-gold/15 px-3 py-3">
                      <PeriodList title="Favourable Periods" periods={row.auspiciousPeriods} />
                      <PeriodList title="Unfavourable Periods" periods={row.inauspiciousPeriods} />
                    </div>
                  ) : null}
                </div>
              );
            })}
          </div>
        )}

        {!user?.is_premium ? (
          <div className="rounded-xl border border-gold/20 bg-background/60 p-4">
            <p className="text-sm font-semibold text-gold">🔒 Upgrade to Arc Angel Pro</p>
            <p className="mt-1 text-sm leading-6 text-muted-foreground">
              Get High-Fidelity Forecasts with Individual Reports.
            </p>
            <Link
              to="/individual-reports"
              className="mt-3 inline-flex items-center rounded-full border border-gold px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/10"
            >
              Explore Reports &rarr;
            </Link>
          </div>
        ) : null}

        <Link to="/arc-angel" className="inline-flex text-sm font-semibold text-gold transition hover:opacity-80">
          View full 10-year outlook &rarr;
        </Link>
      </div>
    </div>
  );
}
