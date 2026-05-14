import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import QuestionnaireWidget from "./QuestionnaireWidget";

const BASE_URL =
  process.env.REACT_APP_BACKEND_URL || "https://everydayhoroscope-api.onrender.com";

// Domain definitions -- IDs match backend ARC_ANGEL_DOMAIN_SLUGS exactly
const ARC_ANGEL_DOMAINS = [
  { id: "health",        label: "Health & Fitness",             description: "Physical well-being, nutrition, exercise and energy levels" },
  { id: "career",        label: "Career & Work",                description: "Professional fulfillment, vocational growth and passion" },
  { id: "finances",      label: "Finances",                     description: "Financial stability, wealth management and security" },
  { id: "learning",      label: "Intellectual Life & Learning",  description: "Continuous education, new skills and mental growth" },
  { id: "emotional",     label: "Emotional Life",               description: "Mental health, managing stress and self-awareness" },
  { id: "spirituality",  label: "Spirituality",                 description: "Purpose, meaning in life and connection to something higher" },
  { id: "relationships", label: "Love Relationships",           description: "Quality of romantic relationship or companionship" },
  { id: "family",        label: "Family Life",                  description: "Relationships with family members and parenting" },
  { id: "social",        label: "Social Life & Friendship",     description: "Social connections, community and networking" },
  { id: "adventure",     label: "Adventure & Travel",           description: "Experiences, exploring new places and taking risks" },
  { id: "environment",   label: "Environment",                  description: "Quality of your surroundings, home and workspace" },
  { id: "creativity",    label: "Creativity & Hobbies",         description: "Hobbies, artistic pursuits and leisure time" },
];

// ─── Helpers ─────────────────────────────────────────────────────────────────

function formatMonthYear(value) {
  if (!value) return "";
  const [yearValue, monthValue] = String(value).split("-");
  const year = Number(yearValue);
  const month = Number(monthValue);
  if (!year || !month || month < 1 || month > 12) return value;
  return new Intl.DateTimeFormat("en-US", { month: "short", year: "numeric" }).format(
    new Date(Date.UTC(year, month - 1, 1))
  );
}

function formatRange(start, end) {
  const s = formatMonthYear(start);
  const e = formatMonthYear(end);
  if (s && e) return `${s} - ${e}`;
  return s || e || "-";
}

function getBorderClass(quality) {
  if (quality === "auspicious") return "border-l-green-500";
  if (quality === "inauspicious") return "border-l-red-500";
  return "border-l-gray-400";
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function Donut({ pct, label, size = 36 }) {
  const safePct = Math.max(0, Math.min(100, Number(pct) || 0));
  const r = (size - 4) / 2;
  const circ = 2 * Math.PI * r;
  const filled = (safePct / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} className="rotate-[-90deg]">
        <circle
          cx={size / 2} cy={size / 2} r={r}
          fill="none" stroke="currentColor" strokeWidth="4"
          className="text-muted-foreground/20"
          strokeDasharray={circ}
        />
        <circle
          cx={size / 2} cy={size / 2} r={r}
          fill="none" stroke="currentColor" strokeWidth="4"
          className="text-gold"
          strokeDasharray={`${filled} ${circ - filled}`}
          strokeLinecap="round"
        />
      </svg>
      <span className="text-[11px] font-medium text-muted-foreground">{label}</span>
    </div>
  );
}

function CompletenessBar({ value }) {
  const safe = Math.max(0, Math.min(100, Number(value) || 0));
  return (
    <div className="space-y-2">
      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">
        Profile completeness: {safe}%
      </p>
      <div className="h-1.5 overflow-hidden rounded-full bg-muted-foreground/15">
        <div className="h-full bg-gold transition-all" style={{ width: `${safe}%` }} />
      </div>
    </div>
  );
}

function PeriodCell({ periods, locked }) {
  if (locked) {
    return (
      <div className="flex min-h-[3rem] items-center justify-center text-center text-xs text-muted-foreground">
        <div>
          <div className="text-base leading-none">🔒</div>
          <div className="mt-1">Available for Premium members</div>
        </div>
      </div>
    );
  }
  if (!periods.length) {
    return <div className="text-xs text-muted-foreground">No major windows listed</div>;
  }
  return (
    <div className="space-y-1.5 text-xs text-foreground">
      {periods.map((period, index) => (
        <div key={`${period.start || "s"}-${period.end || "e"}-${index}`}>
          {formatRange(period.start, period.end)}
        </div>
      ))}
    </div>
  );
}

function LoadingRows() {
  return (
    <div className="overflow-x-auto">
      <div className="min-w-[48rem]">
        {ARC_ANGEL_DOMAINS.map((domain, index) => (
          <div
            key={domain.id}
            className={`grid grid-cols-[2.3fr,1.35fr,1.35fr,0.8fr] gap-3 border-l-4 border-l-gray-400 px-3 py-3 animate-pulse ${
              index % 2 === 0 ? "bg-card" : "bg-background/50"
            }`}
          >
            <div className="space-y-2">
              <div className="h-4 w-32 rounded bg-muted-foreground/20" />
              <div className="h-3 w-full rounded bg-muted-foreground/15" />
            </div>
            <div className="h-10 rounded bg-muted-foreground/15" />
            <div className="h-10 rounded bg-muted-foreground/15" />
            <div className="flex items-center justify-center">
              <div className="h-9 w-9 rounded-full bg-muted-foreground/15" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Main Panel ───────────────────────────────────────────────────────────────

export default function ArcAngelPanel() {
  const { user } = useAuth();

  // Birth profile fetched from /api/profile/birth (most recent)
  const [birthProfile, setBirthProfile] = useState(null);
  const [profileLoading, setProfileLoading] = useState(false);

  // Arc Angel windows fetched from /api/knowledge-engine/arc-angel-windows
  const [payload, setPayload] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const isPremium = user?.is_premium ?? false;

  // Step 1 -- Fetch birth profile when user logs in
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
        setBirthProfile(profiles.length > 0 ? profiles[0] : null);
      } catch {
        if (active) setBirthProfile(null);
      } finally {
        if (active) setProfileLoading(false);
      }
    }
    fetchProfile();
    return () => { active = false; };
  }, [user]);

  // Step 2 -- Fetch Arc Angel windows once birth profile is ready
  useEffect(() => {
    if (!birthProfile) {
      setPayload(null);
      setError("");
      return;
    }
    let active = true;
    async function loadWindows() {
      setLoading(true);
      setError("");
      try {
        // birth_profiles stores: date_of_birth, time_of_birth, location (city string)
        const res = await axios.get(
          `${BASE_URL}/api/knowledge-engine/arc-angel-windows`,
          {
            params: {
              birth_date: birthProfile.date_of_birth,
              birth_time: birthProfile.time_of_birth,
              birth_place: birthProfile.location,
            },
            withCredentials: true,
          }
        );
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
    loadWindows();
    return () => { active = false; };
  }, [birthProfile]);

  // Map arc_angel_windows list to keyed lookup
  const windowsByDomain = useMemo(() => {
    const items = Array.isArray(payload?.arc_angel_windows) ? payload.arc_angel_windows : [];
    return items.reduce((acc, item) => {
      if (item?.domain_id) acc[item.domain_id] = item;
      return acc;
    }, {});
  }, [payload]);

  const rows = useMemo(
    () =>
      ARC_ANGEL_DOMAINS.map((domain) => {
        const d = windowsByDomain[domain.id] || {};
        return {
          ...domain,
          auspiciousPeriods: Array.isArray(d.auspicious_periods) ? d.auspicious_periods : [],
          inauspiciousPeriods: Array.isArray(d.inauspicious_periods) ? d.inauspicious_periods : [],
          periodQualityNow: d.period_quality_now || payload?.domain_quality_now?.[domain.id] || "neutral",
          confidencePct: Number(d.confidence_pct) || 0,
        };
      }),
    [payload, windowsByDomain]
  );

  // Not logged in -- hide entirely
  if (!user) return null;

  // No birth profile -- prompt to add birth details
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
        {/* Completeness bar */}
        {payload && <CompletenessBar value={payload.overall_confidence_pct || 0} />}

        {/* Content states */}
        {profileLoading || loading ? (
          <LoadingRows />
        ) : error ? (
          <div className="space-y-3">
            <p className="text-sm text-red-500">{error}</p>
            <Link to="/arc-angel" className="inline-flex text-sm font-semibold text-gold hover:opacity-80 transition">
              View full 10-year outlook &rarr;
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="overflow-x-auto">
              <div className="min-w-[48rem]">
                {/* Column headers */}
                <div className="grid grid-cols-[2.3fr,1.35fr,1.35fr,0.8fr] gap-3 border-b border-gold/20 px-3 pb-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-gold">
                  <div>Domain</div>
                  <div>Auspicious Periods</div>
                  <div>Inauspicious Periods</div>
                  <div className="text-center">Confidence %</div>
                </div>

                {/* Domain rows */}
                {rows.map((row, index) => (
                  <div
                    key={row.id}
                    className={`grid grid-cols-[2.3fr,1.35fr,1.35fr,0.8fr] gap-3 border-l-4 px-3 py-3 ${
                      index % 2 === 0 ? "bg-card" : "bg-background/50"
                    } ${getBorderClass(row.periodQualityNow)}`}
                  >
                    <div className="min-w-0">
                      <p className="text-sm font-semibold text-foreground">{row.label}</p>
                      <p className="mt-1 text-xs leading-5 text-muted-foreground">{row.description}</p>
                    </div>

                    <PeriodCell periods={row.auspiciousPeriods} locked={!isPremium} />
                    <PeriodCell periods={row.inauspiciousPeriods} locked={!isPremium} />

                    <div className="flex items-center justify-center">
                      <Donut pct={row.confidencePct} label={`${row.confidencePct}%`} />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {user && payload && (payload.overall_confidence_pct || 0) < 100 && (
              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                <p className="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-gold">
                  Complete your profile to improve confidence
                </p>
                <QuestionnaireWidget compact={true} />
              </div>
            )}

            <Link
              to="/arc-angel"
              className="inline-flex text-sm font-semibold text-gold hover:opacity-80 transition"
            >
              View full 10-year outlook &rarr;
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
