import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import {
  AlertTriangle,
  BookOpen,
  Briefcase,
  CheckCircle2,
  Coins,
  Compass,
  Heart,
  HeartHandshake,
  Home,
  Leaf,
  LoaderCircle,
  Palette,
  Search,
  Smile,
  Sparkles,
  Users,
} from "lucide-react";

import { SEO } from "../../components/SEO";
import QuestionnaireWidget from "../../components/QuestionnaireWidget";
import { useAuth } from "../../context/AuthContext";

// Host app wiring:
// <Route path="/arc-angel" element={<ArcAngelPage />} />

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
const ARC_ANGEL_API = `${BACKEND_URL}/api/knowledge-engine/arc-angel-windows`;
const LOCATIONS_API = `${BACKEND_URL}/api/panchang/locations`;
const LOCAL_STORAGE_KEY = "arcAngel_birthData";
const CONFIDENCE_VALUE = 42;

const INITIAL_FORM_DATA = {
  birth_date: "",
  birth_time: "",
  birth_place: "",
};

const DOMAINS = [
  { slug: "health", label: "Health & Fitness", icon: "Heart" },
  { slug: "career", label: "Career & Work", icon: "Briefcase" },
  { slug: "finances", label: "Finances", icon: "Coins" },
  { slug: "learning", label: "Intellectual Life", icon: "BookOpen" },
  { slug: "emotional", label: "Emotional Life", icon: "Smile" },
  { slug: "spirituality", label: "Spirituality", icon: "Sparkles" },
  { slug: "relationships", label: "Love & Relationships", icon: "HeartHandshake" },
  { slug: "family", label: "Family Life", icon: "Home" },
  { slug: "social", label: "Social Life", icon: "Users" },
  { slug: "adventure", label: "Adventure & Travel", icon: "Compass" },
  { slug: "environment", label: "Environment", icon: "Leaf" },
  { slug: "creativity", label: "Creativity & Hobbies", icon: "Palette" },
];

const DOMAIN_ICONS = {
  Heart,
  Briefcase,
  Coins,
  BookOpen,
  Smile,
  Sparkles,
  HeartHandshake,
  Home,
  Users,
  Compass,
  Leaf,
  Palette,
};

function readStoredBirthData() {
  try {
    const rawValue = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (!rawValue) {
      return null;
    }

    const parsedValue = JSON.parse(rawValue);
    if (!parsedValue || typeof parsedValue !== "object") {
      return null;
    }

    return {
      birth_date: typeof parsedValue.birth_date === "string" ? parsedValue.birth_date : "",
      birth_time: typeof parsedValue.birth_time === "string" ? parsedValue.birth_time : "",
      birth_place: typeof parsedValue.birth_place === "string" ? parsedValue.birth_place : "",
    };
  } catch (error) {
    return null;
  }
}

function isValidBirthData(value) {
  return Boolean(value?.birth_date && value?.birth_time && value?.birth_place);
}

function fieldError(error, fallback) {
  return error?.response?.data?.detail || error?.response?.data?.message || fallback;
}

// /api/panchang/locations returns a flat array: [{ slug, label, country, timezone, tz_abbr, ... }]
function flattenLocationGroups(locations) {
  return (locations || []).map((location) => ({
    ...location,
    search_text: [
      location.label,
      location.country,
      location.timezone,
      location.tz_abbr,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase(),
  }));
}

function formatMonthYear(value) {
  if (!value) {
    return "";
  }

  const [yearValue, monthValue] = String(value).split("-");
  const year = Number(yearValue);
  const month = Number(monthValue);

  if (!year || !month || month < 1 || month > 12) {
    return value;
  }

  return new Intl.DateTimeFormat("en-US", {
    month: "long",
    year: "numeric",
  }).format(new Date(Date.UTC(year, month - 1, 1)));
}

function formatWindowRange(start, end) {
  const startLabel = formatMonthYear(start);
  const endLabel = formatMonthYear(end);

  if (startLabel && endLabel) {
    return `${startLabel} - ${endLabel}`;
  }

  return startLabel || endLabel || "Date unavailable";
}

function getQualityClasses(quality) {
  if (quality === "auspicious") {
    return {
      dot: "bg-green-500",
      badge: "border-green-500/30 bg-green-500/10 text-green-500",
    };
  }

  if (quality === "inauspicious") {
    return {
      dot: "bg-red-500",
      badge: "border-red-500/30 bg-red-500/10 text-red-500",
    };
  }

  return {
    dot: "bg-gray-400",
    badge: "border-gray-400/30 bg-gray-400/10 text-gray-400",
  };
}

function GlassCard({ className = "", children }) {
  return <div className={`rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm ${className}`}>{children}</div>;
}

function QualityBadge({ quality }) {
  const tone = getQualityClasses(quality);
  const label = quality ? `${quality.charAt(0).toUpperCase()}${quality.slice(1)}` : "Neutral";

  return (
    <span className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-semibold ${tone.badge}`}>
      <span className={`h-2.5 w-2.5 rounded-full ${tone.dot}`} />
      {label}
    </span>
  );
}

function QualityDot({ quality }) {
  const tone = getQualityClasses(quality);
  return <span className={`h-2.5 w-2.5 rounded-full ${tone.dot}`} />;
}

function ConfidenceDonut() {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const progress = circumference * (CONFIDENCE_VALUE / 100);

  return (
    <GlassCard className="p-6">
      <div className="flex flex-col items-center gap-4 text-center">
        <div className="relative h-40 w-40">
          <svg viewBox="0 0 140 140" className="h-full w-full -rotate-90">
            <circle
              cx="70"
              cy="70"
              r={radius}
              className="stroke-border"
              fill="none"
              strokeWidth="12"
            />
            <circle
              cx="70"
              cy="70"
              r={radius}
              className="stroke-gold"
              fill="none"
              strokeWidth="12"
              strokeLinecap="round"
              strokeDasharray={`${progress} ${circumference}`}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="max-w-[6rem] text-center text-sm font-semibold leading-5 text-foreground">
              {CONFIDENCE_VALUE}% confidence
            </span>
          </div>
        </div>
        <div className="space-y-2">
          <p className="text-sm font-medium text-foreground">{CONFIDENCE_VALUE}% confidence</p>
          <p className="text-sm text-muted-foreground">
            Confidence grows as you complete your profile and run additional modules.
          </p>
        </div>
      </div>
    </GlassCard>
  );
}

function PeriodListCard({ title, periods, emptyMessage, type }) {
  const isAuspicious = type === "auspicious";
  const Icon = isAuspicious ? CheckCircle2 : AlertTriangle;
  const toneClasses = isAuspicious
    ? {
        accent: "border-l-green-500",
        icon: "text-green-500",
        heading: "text-green-500",
      }
    : {
        accent: "border-l-red-500",
        icon: "text-red-500",
        heading: "text-red-500",
      };

  return (
    <GlassCard className={`border-l-4 ${toneClasses.accent} p-5`}>
      <div className="mb-4 flex items-center gap-3">
        <Icon className={`h-5 w-5 ${toneClasses.icon}`} />
        <h3 className={`text-lg font-semibold ${toneClasses.heading}`}>{title}</h3>
      </div>
      {periods.length ? (
        <div className="space-y-4">
          {periods.map((period, index) => (
            <div key={`${period.start || "start"}-${period.end || "end"}-${index}`} className="flex gap-3">
              <Icon className={`mt-1 h-4 w-4 shrink-0 ${toneClasses.icon}`} />
              <div className="space-y-1">
                <p className="font-medium text-foreground">{formatWindowRange(period.start, period.end)}</p>
                <p className="text-sm text-muted-foreground">{period.driver || "Driver details unavailable."}</p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm text-muted-foreground">{emptyMessage}</p>
      )}
    </GlassCard>
  );
}

export default function ArcAngelPage() {
  const { user } = useAuth();
  const [formData, setFormData] = useState(() => readStoredBirthData() || INITIAL_FORM_DATA);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [apiResponse, setApiResponse] = useState(null);
  const [selectedDomain, setSelectedDomain] = useState("career");
  const [locationGroups, setLocationGroups] = useState([]);
  const [locationLoading, setLocationLoading] = useState(true);
  const [locationError, setLocationError] = useState("");
  const [locationSearch, setLocationSearch] = useState("");
  const [completionPct, setCompletionPct] = useState(100);

  const refetchCompletion = async () => {
    if (!user) return;
    try {
      const res = await axios.get(`${BACKEND_URL}/api/user/context-profile/completion`, {
        withCredentials: true,
      });
      setCompletionPct(res.data?.completion_pct ?? 100);
    } catch {
      // silent
    }
  };

  useEffect(() => {
    refetchCompletion();
  }, [user]);

  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(formData));
  }, [formData]);

  useEffect(() => {
    let active = true;

    async function loadLocations() {
      setLocationLoading(true);
      setLocationError("");

      try {
        const response = await axios.get(LOCATIONS_API, { withCredentials: true });
        if (!active) {
          return;
        }

        setLocationGroups(Array.isArray(response.data) ? response.data : []);
      } catch (requestError) {
        if (!active) {
          return;
        }

        setLocationGroups([]);
        setLocationError(fieldError(requestError, "Could not load the birth place catalogue."));
      } finally {
        if (active) {
          setLocationLoading(false);
        }
      }
    }

    loadLocations();

    return () => {
      active = false;
    };
  }, []);

  const submitBirthData = async (payload) => {
    if (!isValidBirthData(payload)) {
      setError("Birth date, birth time, and birth place are required.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await axios.get(ARC_ANGEL_API, {
        params: payload,
        withCredentials: true,
      });

      setApiResponse(response.data || null);
      setSelectedDomain("career");
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (requestError) {
      setApiResponse(null);
      setError(
        fieldError(
          requestError,
          "Could not calculate Arc Angel. Check your birth details and try again."
        )
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const storedBirthData = readStoredBirthData();
    if (isValidBirthData(storedBirthData)) {
      void submitBirthData(storedBirthData);
    }
  }, []);

  const locationOptions = useMemo(() => flattenLocationGroups(locationGroups), [locationGroups]);
  const filteredLocations = useMemo(() => {
    if (!locationSearch.trim()) {
      return locationOptions;
    }

    const needle = locationSearch.trim().toLowerCase();
    return locationOptions.filter((location) => location.search_text.includes(needle));
  }, [locationOptions, locationSearch]);

  const selectedLocation = useMemo(
    () => locationOptions.find((location) => location.slug === formData.birth_place) || null,
    [formData.birth_place, locationOptions]
  );

  const domainQualityNow = apiResponse?.domain_quality_now || {};
  const arcAngelWindows = Array.isArray(apiResponse?.arc_angel_windows) ? apiResponse.arc_angel_windows : [];
  const arcAngelWindowsByDomain = arcAngelWindows.reduce((accumulator, item) => {
    if (item?.domain_id) {
      accumulator[item.domain_id] = item;
    }
    return accumulator;
  }, {});
  const selectedDomainConfig = DOMAINS.find((domain) => domain.slug === selectedDomain) || DOMAINS[1];
  const SelectedDomainIcon = DOMAIN_ICONS[selectedDomainConfig.icon];
  const selectedQuality = domainQualityNow[selectedDomainConfig.slug] || "neutral";
  const selectedDomainWindows = arcAngelWindowsByDomain[selectedDomainConfig.slug] || {};
  const auspiciousPeriods = Array.isArray(selectedDomainWindows.auspicious_periods)
    ? selectedDomainWindows.auspicious_periods
    : [];
  const inauspiciousPeriods = Array.isArray(selectedDomainWindows.inauspicious_periods)
    ? selectedDomainWindows.inauspicious_periods
    : [];

  const handleInputChange = (key, value) => {
    setFormData((previousValue) => ({
      ...previousValue,
      [key]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    await submitBirthData(formData);
  };

  const handleReset = () => {
    setLoading(false);
    setError("");
    setApiResponse(null);
    setSelectedDomain("career");
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <SEO
        title="Arc Angel -- 12 Areas of Life | EverydayHoroscope"
        description="Discover your 10-year Vedic dasha windows across 12 life domains -- career, relationships, finances, health and more."
        canonical="https://www.everydayhoroscope.in/arc-angel"
      />

      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="mb-8 space-y-3">
          <div className="inline-flex items-center gap-2 rounded-full border border-gold/25 bg-gold/5 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.24em] text-gold">
            <Sparkles className="h-4 w-4" />
            Mahadasha guidance
          </div>
          <h1 className="font-playfair text-4xl font-semibold text-foreground sm:text-5xl">
            Arc Angel -- 12 Areas of Life
          </h1>
          <p className="max-w-3xl text-base leading-7 text-muted-foreground">
            Explore the next 10 years of favourable and challenging dasha windows across the 12 life domains that shape your journey.
          </p>
        </div>

        {loading ? (
          <GlassCard className="flex min-h-[28rem] flex-col items-center justify-center gap-4 p-8 text-center">
            <LoaderCircle className="h-10 w-10 animate-spin text-gold" />
            <div className="space-y-2">
              <h2 className="text-2xl font-semibold text-foreground">Calculating your Arc Angel...</h2>
              <p className="text-sm text-muted-foreground">
                We are reading your Mahadasha cycle and mapping the strongest windows across all 12 domains.
              </p>
            </div>
          </GlassCard>
        ) : error ? (
          <GlassCard className="border-red-500/30 p-6 sm:p-8">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div className="flex gap-3">
                <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-red-500" />
                <div className="space-y-2">
                  <h2 className="text-xl font-semibold text-foreground">Arc Angel could not be calculated</h2>
                  <p className="text-sm leading-7 text-muted-foreground">{error}</p>
                </div>
              </div>
              <button
                type="button"
                onClick={handleReset}
                className="inline-flex items-center justify-center rounded-full border border-gold px-5 py-2.5 text-sm font-semibold text-gold transition hover:bg-gold/10"
              >
                Try Again
              </button>
            </div>
          </GlassCard>
        ) : apiResponse ? (
          <div className="grid gap-6 md:grid-cols-[18rem,minmax(0,1fr)]">
            <GlassCard className="h-fit p-3">
              <div className="space-y-3">
                {DOMAINS.map((domain) => {
                  const DomainIcon = DOMAIN_ICONS[domain.icon];
                  const domainQuality = domainQualityNow[domain.slug] || "neutral";
                  const isActive = selectedDomain === domain.slug;

                  return (
                    <button
                      key={domain.slug}
                      type="button"
                      onClick={() => setSelectedDomain(domain.slug)}
                      className={`w-full rounded-xl border p-4 text-left transition ${
                        isActive
                          ? "border-gold bg-gold/10 shadow-sm"
                          : "border-gold/20 bg-card hover:border-gold/40 hover:bg-gold/5"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-gold/15 to-gold/5 text-gold">
                          <DomainIcon className="h-5 w-5" />
                        </div>
                        <div className="min-w-0 flex-1">
                          <p className="truncate font-medium text-foreground">{domain.label}</p>
                          <div className="mt-1 flex items-center gap-2 text-xs text-muted-foreground">
                            <QualityDot quality={domainQuality} />
                            <span className="capitalize">{domainQuality}</span>
                          </div>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </GlassCard>

            <div className="space-y-6">
              <GlassCard className="p-6 sm:p-8">
                <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
                  <div className="flex items-start gap-4">
                    <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-gold/15 to-gold/5 text-gold">
                      <SelectedDomainIcon className="h-8 w-8" />
                    </div>
                    <div className="space-y-2">
                      <h2 className="text-3xl font-semibold text-foreground">{selectedDomainConfig.label}</h2>
                      <QualityBadge quality={selectedQuality} />
                      <p className="text-sm text-muted-foreground">
                        Current period quality based on your Mahadasha cycle
                      </p>
                    </div>
                  </div>
                </div>
              </GlassCard>

              <ConfidenceDonut />

              {user && completionPct < 100 && (
                <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-4">
                  <p className="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-gold">
                    Complete your profile to improve confidence
                  </p>
                  <QuestionnaireWidget compact={true} onSaveSuccess={refetchCompletion} />
                </div>
              )}

              <PeriodListCard
                title="Favourable Windows"
                periods={auspiciousPeriods}
                emptyMessage="No strongly auspicious windows in the next 10 years."
                type="auspicious"
              />

              <PeriodListCard
                title="Challenging Windows"
                periods={inauspiciousPeriods}
                emptyMessage="No strongly challenging windows in the next 10 years."
                type="inauspicious"
              />

              <p className="text-sm leading-7 text-muted-foreground">
                Arc Angel windows are derived from Vedic Vimshottari Dasha cycles and are intended as guidance, not prediction.
              </p>
            </div>
          </div>
        ) : (
          <div className="grid gap-6 lg:grid-cols-[minmax(0,1.15fr),minmax(0,0.85fr)]">
            <GlassCard className="p-6 sm:p-8">
              <div className="space-y-4">
                <p className="text-sm font-semibold uppercase tracking-[0.24em] text-gold">Birth data form</p>
                <h2 className="text-3xl font-semibold text-foreground">Reveal your Arc Angel dashboard</h2>
                <p className="max-w-2xl text-sm leading-7 text-muted-foreground">
                  Enter your birth details to unlock current domain quality and 10-year windows for career, relationships, finances, health, and the rest of your life map.
                </p>
              </div>

              <form onSubmit={handleSubmit} className="mt-8 space-y-5">
                <div className="grid gap-5 sm:grid-cols-2">
                  <label className="space-y-2">
                    <span className="text-sm font-medium text-foreground">Date of birth</span>
                    <input
                      type="date"
                      value={formData.birth_date}
                      onChange={(event) => handleInputChange("birth_date", event.target.value)}
                      className="w-full rounded-xl border border-gold/20 bg-card px-4 py-3 text-foreground outline-none transition focus:border-gold"
                      required
                    />
                  </label>

                  <label className="space-y-2">
                    <span className="text-sm font-medium text-foreground">Time of birth</span>
                    <input
                      type="time"
                      value={formData.birth_time}
                      onChange={(event) => handleInputChange("birth_time", event.target.value)}
                      className="w-full rounded-xl border border-gold/20 bg-card px-4 py-3 text-foreground outline-none transition focus:border-gold"
                      required
                    />
                  </label>
                </div>

                <div className="space-y-2">
                  <span className="text-sm font-medium text-foreground">Place of birth</span>
                  <div className="relative">
                    <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                    <input
                      type="text"
                      value={locationSearch}
                      onChange={(event) => setLocationSearch(event.target.value)}
                      placeholder="Search city, country, or timezone"
                      className="w-full rounded-xl border border-gold/20 bg-card py-3 pl-11 pr-4 text-foreground outline-none transition focus:border-gold"
                      disabled={locationLoading}
                    />
                  </div>
                  <select
                    value={formData.birth_place}
                    onChange={(event) => handleInputChange("birth_place", event.target.value)}
                    className="w-full rounded-xl border border-gold/20 bg-card px-4 py-3 text-foreground outline-none transition focus:border-gold"
                    disabled={locationLoading}
                    required
                  >
                    <option value="">
                      {locationLoading ? "Loading birth place catalogue..." : "Select a birth place"}
                    </option>
                    {filteredLocations.slice(0, 200).map((location) => (
                      <option key={location.slug} value={location.slug}>
                        {location.label} | {location.country} | {location.tz_abbr || location.timezone}
                      </option>
                    ))}
                  </select>
                  {selectedLocation ? (
                    <p className="text-sm text-muted-foreground">
                      Selected: {selectedLocation.label}, {selectedLocation.country} ({selectedLocation.timezone})
                    </p>
                  ) : null}
                  {locationError ? <p className="text-sm text-red-500">{locationError}</p> : null}
                  {!locationLoading && !locationError && !filteredLocations.length ? (
                    <p className="text-sm text-muted-foreground">No matching places found. Try a broader search.</p>
                  ) : null}
                </div>

                <button
                  type="submit"
                  className="w-full rounded-full border border-gold bg-gold px-5 py-3 text-sm font-semibold text-primary-foreground transition hover:bg-gold/90 disabled:cursor-not-allowed disabled:opacity-60"
                  disabled={locationLoading}
                >
                  Reveal My Arc Angel
                </button>
              </form>
            </GlassCard>

            <GlassCard className="p-6 sm:p-8">
              <div className="space-y-5">
                <div className="inline-flex rounded-2xl bg-gradient-to-br from-gold/15 to-gold/5 p-4 text-gold">
                  <Sparkles className="h-8 w-8" />
                </div>
                <div className="space-y-3">
                  <h2 className="text-2xl font-semibold text-foreground">12 domains, one dasha map</h2>
                  <p className="text-sm leading-7 text-muted-foreground">
                    Arc Angel highlights where your current cycle is supportive, steady, or challenging across love, work, family, health, creativity, spirituality, and more.
                  </p>
                </div>
                <div className="grid gap-3 sm:grid-cols-2">
                  {DOMAINS.slice(0, 6).map((domain) => {
                    const DomainIcon = DOMAIN_ICONS[domain.icon];
                    return (
                      <div key={domain.slug} className="rounded-xl border border-gold/20 bg-card p-4">
                        <div className="mb-3 inline-flex rounded-xl bg-gradient-to-br from-gold/15 to-gold/5 p-2 text-gold">
                          <DomainIcon className="h-4 w-4" />
                        </div>
                        <p className="text-sm font-medium text-foreground">{domain.label}</p>
                      </div>
                    );
                  })}
                </div>
              </div>
            </GlassCard>
          </div>
        )}
      </div>
    </div>
  );
}
