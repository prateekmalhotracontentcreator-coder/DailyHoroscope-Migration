import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import SharedBirthCityPicker from "../../components/SharedBirthCityPicker";
import { SEO } from "../../components/SEO";

// Host app wiring:
// <Route path="/longevity" element={<LongevityReportPage />} />
// { label: "Ayur Jyotish", path: "/longevity" }

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
const API = `${BACKEND_URL}/api/longevity`;

const SECTION_PREVIEWS = [
  {
    id: "classification",
    title: "Longevity Classification",
    copy: "KP sub-lord scoring of Ayush potential through houses 1, 2, 7, 8, Saturn, and maraka pressure.",
  },
  {
    id: "prakriti",
    title: "Constitutional Health Profile",
    copy: "Prakriti balance from ascendant, Moon, Sun, and planetary dosha weighting.",
  },
  {
    id: "systems",
    title: "Vulnerable Body Systems & Organs",
    copy: "Sign-body, house-health, and planet-disease mapping ranked by pressure.",
  },
  {
    id: "windows",
    title: "Disease Susceptibility Windows",
    copy: "Dasha x transit windows for stronger watchfulness over the next cycle.",
  },
  {
    id: "alerts",
    title: "Critical Period Alerts",
    copy: "Maraka triggers, 22nd Drekkana, and 64th Navamsa sensitivity checks.",
  },
  {
    id: "guidance",
    title: "Remedial & Preventive Guidance",
    copy: "Planetary mantras, routine correction, and practical prevention priorities.",
  },
  {
    id: "forecast",
    title: "Decade-wise Quality of Life Forecast",
    copy: "A life-arc quality map from dasha dominance and vitality sensitivity.",
  },
];

const initialForm = {
  user_email: "",
  city_slug: "",
  place_label: "",
  date_of_birth: "",
  time_of_birth: "",
  latitude: "",
  longitude: "",
  timezone: "Asia/Kolkata",
  reference_date: "",
};

function fieldError(error, fallback) {
  return error?.response?.data?.detail || fallback;
}

function formatDate(value) {
  if (!value) return "";
  try {
    return new Intl.DateTimeFormat("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    }).format(new Date(value));
  } catch (error) {
    return value;
  }
}

function formatDateTime(value) {
  if (!value) return "";
  try {
    return new Intl.DateTimeFormat("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit",
    }).format(new Date(value));
  } catch (error) {
    return value;
  }
}

function Badge({ children, tone = "gold" }) {
  const tones = {
    gold: "border-[#d5a14a]/40 bg-[#d5a14a]/10 text-[#f3c978]",
    rose: "border-[#df8a8a]/35 bg-[#df8a8a]/10 text-[#f2b7b7]",
    sage: "border-[#87b493]/35 bg-[#87b493]/10 text-[#cce4d2]",
    ink: "border-white/15 bg-white/5 text-white/70",
  };
  return <span className={`inline-flex items-center rounded-full border px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.22em] ${tones[tone]}`}>{children}</span>;
}

function SectionCard({ title, eyebrow, children, className = "" }) {
  return (
    <section className={`rounded-[28px] border border-white/10 bg-[#101423]/88 p-5 shadow-[0_30px_80px_rgba(2,6,23,0.24)] backdrop-blur-xl sm:p-7 ${className}`}>
      <div className="mb-4 space-y-2">
        {eyebrow ? <p className="text-[11px] uppercase tracking-[0.3em] text-[#d5a14a]">{eyebrow}</p> : null}
        <h2 className="font-serif text-2xl text-[#fbf6ef] sm:text-[2rem]">{title}</h2>
      </div>
      {children}
    </section>
  );
}

function KeyValue({ label, value }) {
  return (
    <div className="rounded-2xl border border-white/8 bg-white/[0.03] px-4 py-3">
      <p className="mb-1 text-[11px] uppercase tracking-[0.24em] text-white/45">{label}</p>
      <p className="text-sm leading-6 text-white/82">{value}</p>
    </div>
  );
}

function SectionPreviewGrid() {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {SECTION_PREVIEWS.map((item, index) => (
        <div key={item.id} className="rounded-[24px] border border-white/10 bg-white/[0.04] p-5 transition-transform duration-300 hover:-translate-y-1">
          <div className="mb-4 flex items-center justify-between gap-3">
            <Badge tone={index % 3 === 0 ? "gold" : index % 3 === 1 ? "sage" : "rose"}>{`0${index + 1}`}</Badge>
            <span className="text-[11px] uppercase tracking-[0.24em] text-white/35">Included</span>
          </div>
          <h3 className="mb-2 text-lg font-semibold text-[#fbf6ef]">{item.title}</h3>
          <p className="text-sm leading-7 text-white/62">{item.copy}</p>
        </div>
      ))}
    </div>
  );
}

export default function LongevityReportPage() {
  const [access, setAccess] = useState(null);
  const [accessLoading, setAccessLoading] = useState(true);
  const [accessError, setAccessError] = useState("");

  const [form, setForm] = useState(() => {
    try {
      const raw = localStorage.getItem("longevity_form");
      return raw ? { ...initialForm, ...JSON.parse(raw) } : initialForm;
    } catch (error) {
      return initialForm;
    }
  });

  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState("");

  useEffect(() => {
    document.title = "Ayur Jyotish | EverydayHoroscope";
  }, []);

  useEffect(() => {
    localStorage.setItem("longevity_form", JSON.stringify(form));
  }, [form]);

  useEffect(() => {
    let active = true;
    async function loadAccess() {
      setAccessLoading(true);
      setAccessError("");
      try {
        const response = await axios.get(`${API}/eligibility`, { withCredentials: true });
        if (!active) return;
        setAccess(response.data);
      } catch (err) {
        if (!active) return;
        setAccessError(fieldError(err, "Could not check premium access right now."));
      } finally {
        if (active) setAccessLoading(false);
      }
    }
    loadAccess();
    return () => {
      active = false;
    };
  }, []);

  const generatedAt = useMemo(() => (report?.created_at ? formatDateTime(report.created_at) : ""), [report]);
  const output = report?.output_payload || {};
  const longevity = output?.longevity_classification || {};
  const prakriti = output?.constitutional_health_profile || {};
  const narrative = output?.narrative || {};
  const vulnerabilities = Array.isArray(output?.vulnerable_systems) ? output.vulnerable_systems : [];
  const windows = Array.isArray(output?.disease_susceptibility_windows) ? output.disease_susceptibility_windows : [];
  const alerts = Array.isArray(output?.critical_period_alerts) ? output.critical_period_alerts : [];
  const decadeForecast = Array.isArray(output?.decade_quality_forecast) ? output.decade_quality_forecast : [];
  const guidance = output?.remedial_guidance || {};
  const currentDasha = output?.current_dasha || {};

  const updateField = (key, value) => {
    setForm(prev => ({ ...prev, [key]: value }));
  };

  const buildPayload = (preview) => {
    const { city_slug, ...rest } = form;
    return { ...rest, latitude: Number(form.latitude), longitude: Number(form.longitude), preview };
  };

  const handleGenerate = async (preview) => {
    if (!form.date_of_birth || !form.time_of_birth || form.latitude === "" || form.longitude === "") {
      setError("Birth date, birth time, latitude, and longitude are required.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const response = await axios.post(`${API}/generate`, buildPayload(preview), {
        withCredentials: true,
      });
      setReport(response.data?.report || null);
      setAccess(response.data?.access || access);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      setError(fieldError(err, "The report could not be generated right now."));
    } finally {
      setLoading(false);
    }
  };

  const handleLoadHistory = async () => {
    setHistoryLoading(true);
    setHistoryError("");
    try {
      const response = await axios.get(`${API}/history`, { withCredentials: true });
      setHistory(Array.isArray(response.data?.items) ? response.data.items : []);
    } catch (err) {
      setHistory([]);
      setHistoryError(fieldError(err, "History is available after sign-in on an entitled account."));
    } finally {
      setHistoryLoading(false);
    }
  };

  const openHistoryItem = async (reportId) => {
    setLoading(true);
    setError("");
    try {
      const response = await axios.get(`${API}/reports/${reportId}`, { withCredentials: true });
      setReport(response.data || null);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      setError(fieldError(err, "That saved report could not be opened."));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#09101b] text-white">
      <SEO
        title="Ayur Jyotish -- Vedic Longevity & Health Report"
        description="Discover your Vedic health blueprint. KP-based longevity classification, prakriti analysis, vulnerable body systems, disease windows, and remedial guidance."
        url="https://www.everydayhoroscope.in/longevity"
      />
      <style>{`
        .longevity-shell {
          background:
            radial-gradient(circle at 15% 20%, rgba(213, 161, 74, 0.18), transparent 28%),
            radial-gradient(circle at 82% 14%, rgba(78, 133, 171, 0.22), transparent 32%),
            radial-gradient(circle at 50% 100%, rgba(127, 184, 154, 0.12), transparent 30%),
            linear-gradient(180deg, #09101b 0%, #0d1420 46%, #131c2a 100%);
        }
        .longevity-orbit {
          position: absolute;
          inset: auto auto 0 0;
          height: 520px;
          width: 520px;
          border-radius: 999px;
          border: 1px solid rgba(255,255,255,0.08);
          opacity: 0.4;
          transform: translate(-18%, 22%);
        }
        .longevity-orbit::after {
          content: "";
          position: absolute;
          inset: 12%;
          border-radius: 999px;
          border: 1px dashed rgba(213, 161, 74, 0.28);
        }
        .longevity-loader-ring {
          border: 1px solid rgba(255,255,255,0.14);
          border-top-color: rgba(213, 161, 74, 0.85);
          animation: longevitySpin 1s linear infinite;
        }
        @keyframes longevitySpin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>

      <div className="sticky top-0 z-30 border-b border-[#d5a14a]/25 bg-[#160f08]/92 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-3 sm:px-6 lg:px-8">
          <div>
            <p className="text-[11px] uppercase tracking-[0.34em] text-[#d5a14a]">Mandatory Medical Disclaimer</p>
            <p className="mt-1 max-w-4xl text-xs leading-6 text-[#f7ecde]/78">{access?.medical_disclaimer || "This spiritual health report does not replace licensed medical care, diagnosis, treatment, or emergency support."}</p>
          </div>
          <Badge tone="ink">{access?.entitled ? "Pro Unlocked" : "Premium Module"}</Badge>
        </div>
      </div>

      <div className="longevity-shell relative overflow-hidden">
        <div className="longevity-orbit pointer-events-none hidden lg:block" />
        <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8 lg:py-14">
          <div className="grid gap-8 lg:grid-cols-[1.15fr_0.85fr] lg:items-start">
            <div className="space-y-6">
              <Badge>Ayur Jyotish Premium</Badge>
              <div className="space-y-4">
                <h1 className="max-w-4xl font-serif text-4xl leading-tight text-[#fbf6ef] sm:text-5xl lg:text-6xl">
                  KP-led longevity and health intelligence for a calmer, more preventive life rhythm.
                </h1>
                <p className="max-w-3xl text-base leading-8 text-white/70">
                  This report combines KP sub-lord analysis, Placidus cusps, classical Vedic support, disease-window timing, maraka alerts, and practical preventive guidance. It is built for reflection, timing, and disciplined self-care, not for diagnosis.
                </p>
              </div>
              <SectionPreviewGrid />
            </div>

            <div className="rounded-[32px] border border-white/10 bg-[#111827]/88 p-5 shadow-[0_35px_90px_rgba(2,6,23,0.35)] backdrop-blur-xl sm:p-7">
              <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
                <div>
                  <p className="text-[11px] uppercase tracking-[0.32em] text-[#d5a14a]">Premium Access</p>
                  <h2 className="mt-2 text-2xl font-semibold text-[#fbf6ef]">Generate my report</h2>
                </div>
                {accessLoading ? <Badge tone="ink">Checking</Badge> : <Badge tone={access?.entitled ? "sage" : "rose"}>{access?.entitled ? "Unlocked" : "Locked"}</Badge>}
              </div>

              {accessError ? <p className="mb-4 rounded-2xl border border-[#df8a8a]/30 bg-[#df8a8a]/10 px-4 py-3 text-sm text-[#f6c8c8]">{accessError}</p> : null}

              {access ? (
                <div className="mb-6 rounded-[24px] border border-white/8 bg-white/[0.03] p-5">
                  <p className="text-sm leading-7 text-white/72">{access.reason}</p>
                  <div className="mt-4 flex flex-wrap gap-3">
                    {access.pricing?.map(plan => (
                      <div key={plan.code} className="rounded-2xl border border-white/8 bg-[#0b1220] px-4 py-3">
                        <p className="text-sm font-semibold text-[#fbf6ef]">{plan.label}</p>
                        <p className="mt-1 text-xs uppercase tracking-[0.24em] text-[#d5a14a]">₹{plan.price_inr}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ) : null}

              <div className="grid gap-4 sm:grid-cols-2">
                <label className="space-y-2">
                  <span className="text-xs uppercase tracking-[0.24em] text-white/45">Birth Date</span>
                  <input type="date" value={form.date_of_birth} onChange={e => updateField("date_of_birth", e.target.value)} className="w-full rounded-2xl border border-white/10 bg-[#09111e] px-4 py-3 text-sm text-white outline-none transition focus:border-[#d5a14a]/55" />
                </label>
                <label className="space-y-2">
                  <span className="text-xs uppercase tracking-[0.24em] text-white/45">Birth Time</span>
                  <input type="time" value={form.time_of_birth} onChange={e => updateField("time_of_birth", e.target.value)} className="w-full rounded-2xl border border-white/10 bg-[#09111e] px-4 py-3 text-sm text-white outline-none transition focus:border-[#d5a14a]/55" />
                </label>
                <div className="space-y-2 sm:col-span-2">
                  <SharedBirthCityPicker
                    inputId="longevity-birth-city"
                    label={<span className="text-xs uppercase tracking-[0.24em] text-white/45">Birth Location</span>}
                    placeholder="Search city, country, or timezone..."
                    value={form.city_slug}
                    helpText="Search by city, country, or timezone abbreviation."
                    onChange={(city) => setForm(prev => ({
                      ...prev,
                      city_slug: city.slug,
                      place_label: `${city.city_name}, ${city.country || city.country_name}`,
                      latitude: city.latitude,
                      longitude: city.longitude,
                      timezone: city.timezone,
                    }))}
                    wrapperStyle={{ width: "100%" }}
                    labelStyle={{ display: "block" }}
                    inputStyle={{
                      display: "block", width: "100%", borderRadius: "1rem",
                      border: "1px solid rgba(255,255,255,0.10)", background: "#09111e",
                      padding: "0.75rem 1rem", fontSize: "0.875rem", color: "#fff",
                      outline: "none", boxSizing: "border-box",
                    }}
                    selectStyle={{
                      display: "block", width: "100%", borderRadius: "1rem",
                      border: "1px solid rgba(255,255,255,0.10)", background: "#09111e",
                      padding: "0.75rem 1rem", fontSize: "0.875rem", color: "#fff",
                      outline: "none", boxSizing: "border-box",
                    }}
                  />
                </div>
                {form.latitude !== "" && (
                  <div className="space-y-1 sm:col-span-2">
                    <p className="text-[11px] uppercase tracking-[0.22em] text-white/40">Auto-populated coordinates</p>
                    <div className="flex flex-wrap gap-3 text-xs text-white/60">
                      <span className="rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2">
                        Lat: <strong className="text-white/80">{form.latitude}</strong>
                      </span>
                      <span className="rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2">
                        Lng: <strong className="text-white/80">{form.longitude}</strong>
                      </span>
                      <span className="rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2">
                        TZ: <strong className="text-white/80">{form.timezone}</strong>
                      </span>
                    </div>
                  </div>
                )}
                <label className="space-y-2">
                  <span className="text-xs uppercase tracking-[0.24em] text-white/45">Reference Date</span>
                  <input type="date" value={form.reference_date} onChange={e => updateField("reference_date", e.target.value)} className="w-full rounded-2xl border border-white/10 bg-[#09111e] px-4 py-3 text-sm text-white outline-none transition focus:border-[#d5a14a]/55" />
                </label>
                <label className="space-y-2 sm:col-span-2">
                  <span className="text-xs uppercase tracking-[0.24em] text-white/45">Email for save/history</span>
                  <input type="email" value={form.user_email} onChange={e => updateField("user_email", e.target.value)} placeholder="Only needed for local validation or guest save paths" className="w-full rounded-2xl border border-white/10 bg-[#09111e] px-4 py-3 text-sm text-white outline-none transition focus:border-[#d5a14a]/55" />
                </label>
              </div>

              <div className="mt-6 flex flex-col gap-3">
                <button
                  type="button"
                  disabled={loading || accessLoading}
                  onClick={() => handleGenerate(!(access?.entitled))}
                  className="rounded-full bg-[#d5a14a] px-5 py-3 text-sm font-semibold text-[#161310] transition hover:bg-[#ebb45a] disabled:cursor-not-allowed disabled:opacity-70"
                >
                  {loading ? "Generating..." : access?.entitled ? "Generate Full Premium Report" : "Preview the Report"}
                </button>
                {access?.entitled ? (
                  <button
                    type="button"
                    disabled={historyLoading}
                    onClick={handleLoadHistory}
                    className="rounded-full border border-white/12 bg-white/[0.03] px-5 py-3 text-sm font-semibold text-white/82 transition hover:bg-white/[0.08]"
                  >
                    {historyLoading ? "Loading history..." : "Load My Saved Reports"}
                  </button>
                ) : null}
              </div>

              {error ? <p className="mt-4 rounded-2xl border border-[#df8a8a]/30 bg-[#df8a8a]/10 px-4 py-3 text-sm text-[#f5c7c7]">{error}</p> : null}
              {historyError ? <p className="mt-4 rounded-2xl border border-white/10 bg-white/[0.04] px-4 py-3 text-sm text-white/65">{historyError}</p> : null}

              {history.length ? (
                <div className="mt-6 space-y-3">
                  <p className="text-[11px] uppercase tracking-[0.3em] text-[#d5a14a]">Saved Reports</p>
                  {history.map(item => (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() => openHistoryItem(item.id)}
                      className="flex w-full items-start justify-between gap-4 rounded-2xl border border-white/8 bg-white/[0.03] px-4 py-4 text-left transition hover:bg-white/[0.06]"
                    >
                      <div>
                        <p className="text-sm font-semibold text-[#fbf6ef]">{item.classification}</p>
                        <p className="mt-1 text-xs uppercase tracking-[0.24em] text-white/42">{formatDate(item.created_at)}</p>
                        <p className="mt-2 text-sm leading-6 text-white/62">{item.summary}</p>
                      </div>
                      <Badge tone="ink">{item.quality_band}</Badge>
                    </button>
                  ))}
                </div>
              ) : null}
            </div>
          </div>

          {loading && !report ? (
            <div className="mx-auto mt-10 max-w-3xl rounded-[32px] border border-white/10 bg-[#101423]/88 p-10 text-center shadow-[0_35px_80px_rgba(2,6,23,0.3)]">
              <div className="longevity-loader-ring mx-auto mb-6 h-16 w-16 rounded-full" />
              <h2 className="font-serif text-3xl text-[#fbf6ef]">Computing your Ayur Jyotish report</h2>
              <p className="mx-auto mt-3 max-w-xl text-sm leading-7 text-white/65">
                KP sub-lords, Placidus cusps, maraka pressure, dasha timing, and preventive health windows are being assembled now.
              </p>
            </div>
          ) : null}

          {report ? (
            <div className="mt-10 space-y-6">
              <SectionCard title="Report Overview" eyebrow="Generated Report">
                <div className="grid gap-4 lg:grid-cols-[1.3fr_0.7fr]">
                  <div className="space-y-4">
                    <div className="flex flex-wrap items-center gap-3">
                      <Badge tone={report.access_mode === "full" ? "sage" : "rose"}>{report.access_mode === "full" ? "Full Report" : "Preview Report"}</Badge>
                      <Badge tone="gold">{longevity?.label || "Longevity Reading"}</Badge>
                      {generatedAt ? <Badge tone="ink">{generatedAt}</Badge> : null}
                    </div>
                    <h2 className="font-serif text-3xl text-[#fbf6ef]">{narrative.executive_summary || output.summary || report.summary}</h2>
                    <p className="text-base leading-8 text-white/72">{narrative.timing_narrative || "This reading combines natal constitution, dasha timing, and transit sensitivity to map preventive health focus."}</p>
                    {Array.isArray(narrative.knowledge_engine_notes) && narrative.knowledge_engine_notes.length ? (
                      <div className="rounded-[24px] border border-[#87b493]/25 bg-[#87b493]/10 p-4">
                        <p className="text-[11px] uppercase tracking-[0.3em] text-[#b9d8c3]">Knowledge Engine Support</p>
                        <div className="mt-3 space-y-2">
                          {narrative.knowledge_engine_notes.map((item, index) => (
                            <p key={`${item}-${index}`} className="text-sm leading-7 text-[#eef8f1]/82">{item}</p>
                          ))}
                        </div>
                      </div>
                    ) : null}
                  </div>
                  <div className="grid gap-3">
                    <KeyValue label="Classification" value={longevity?.label || "Unavailable"} />
                    <KeyValue label="Traditional Band" value={longevity?.range_label || "Unavailable"} />
                    <KeyValue label="Confidence" value={longevity?.confidence || "Unavailable"} />
                    <KeyValue
                      label="Current Dasha"
                      value={`${currentDasha?.maha_dasha?.planet || "Unknown"} / ${currentDasha?.antar_dasha?.planet || "Unknown"}`}
                    />
                  </div>
                </div>
                <div className="mt-5 rounded-[24px] border border-[#d5a14a]/25 bg-[#1b1510] px-5 py-4 text-sm leading-7 text-[#f5e7d6]">
                  {output.medical_disclaimer}
                </div>
              </SectionCard>

              <div className="grid gap-6 xl:grid-cols-2">
                <SectionCard title="Longevity Classification" eyebrow="Section 01">
                  <p className="text-sm leading-7 text-white/72">{longevity?.summary}</p>
                  <div className="mt-5 grid gap-3">
                    {(longevity?.drivers || []).map(item => (
                      <div key={item.factor} className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
                        <div className="flex items-center justify-between gap-3">
                          <p className="text-sm font-semibold text-[#fbf6ef]">{item.factor}</p>
                          <Badge tone={item.score >= 0 ? "sage" : "rose"}>{item.score >= 0 ? `+${item.score}` : item.score}</Badge>
                        </div>
                        <p className="mt-2 text-sm leading-7 text-white/62">{Array.isArray(item.notes) ? item.notes.join(" ") : item.notes}</p>
                      </div>
                    ))}
                  </div>
                </SectionCard>

                <SectionCard title="Constitutional Health Profile" eyebrow="Section 02">
                  <div className="flex flex-wrap items-center gap-3">
                    <Badge tone="gold">{prakriti?.primary_prakriti || "Primary Dosha"}</Badge>
                    <Badge tone="ink">{prakriti?.secondary_prakriti || "Secondary Dosha"}</Badge>
                  </div>
                  <p className="mt-4 text-sm leading-7 text-white/72">{narrative.constitution_narrative || prakriti?.summary}</p>
                  <div className="mt-5 grid gap-3 sm:grid-cols-3">
                    {Object.entries(prakriti?.dosha_scores || {}).map(([key, value]) => (
                      <KeyValue key={key} label={key} value={value} />
                    ))}
                  </div>
                  <div className="mt-5 space-y-2">
                    {(prakriti?.maintenance_priorities || []).map(item => (
                      <p key={item} className="rounded-2xl border border-white/8 bg-white/[0.03] px-4 py-3 text-sm leading-7 text-white/72">{item}</p>
                    ))}
                  </div>
                </SectionCard>
              </div>

              <SectionCard title="Vulnerable Body Systems & Organs" eyebrow="Section 03">
                <div className="grid gap-4 lg:grid-cols-2">
                  {vulnerabilities.map(item => (
                    <div key={`${item.title}-${item.linked_planet}`} className="rounded-[24px] border border-white/8 bg-white/[0.03] p-5">
                      <div className="flex flex-wrap items-center gap-3">
                        <Badge tone={item.severity_score >= 5 ? "rose" : item.severity_score >= 4 ? "gold" : "sage"}>{`Pressure ${item.severity_score}`}</Badge>
                        <Badge tone="ink">{item.linked_sign}</Badge>
                        <Badge tone="ink">{`House ${item.linked_house}`}</Badge>
                      </div>
                      <h3 className="mt-4 text-xl font-semibold text-[#fbf6ef]">{item.title}</h3>
                      <p className="mt-2 text-sm leading-7 text-white/70">{item.body_system}</p>
                      <div className="mt-4 space-y-2">
                        {(item.indicators || []).map(line => (
                          <p key={line} className="text-sm leading-7 text-white/58">{line}</p>
                        ))}
                      </div>
                      <div className="mt-4 rounded-2xl border border-[#87b493]/20 bg-[#87b493]/10 px-4 py-3 text-sm leading-7 text-[#e8f4ec]">
                        {item.prevention_focus}
                      </div>
                    </div>
                  ))}
                </div>
              </SectionCard>

              <div className="grid gap-6 xl:grid-cols-2">
                <SectionCard title="Disease Susceptibility Windows" eyebrow="Section 04">
                  <p className="mb-4 text-sm leading-7 text-white/66">{narrative.timing_narrative || "These windows are for greater vigilance, not fear. Use them to tighten routines, watch symptoms earlier, and escalate medical care faster when needed."}</p>
                  <div className="space-y-4">
                    {windows.length ? windows.map(item => (
                      <div key={`${item.start_date}-${item.end_date}`} className="rounded-[24px] border border-white/8 bg-white/[0.03] p-5">
                        <div className="flex flex-wrap items-center gap-3">
                          <Badge tone={item.severity === "high" ? "rose" : item.severity === "elevated" ? "gold" : "ink"}>{item.severity}</Badge>
                          <Badge tone="ink">{`${formatDate(item.start_date)} - ${formatDate(item.end_date)}`}</Badge>
                          <Badge tone="ink">{`${item.dasha?.maha || "?"} / ${item.dasha?.antar || "?"}`}</Badge>
                        </div>
                        <h3 className="mt-4 text-lg font-semibold text-[#fbf6ef]">{item.headline}</h3>
                        <div className="mt-3 space-y-2">
                          {(item.why_it_matters || []).map(line => (
                            <p key={line} className="text-sm leading-7 text-white/60">{line}</p>
                          ))}
                        </div>
                        <p className="mt-4 rounded-2xl border border-[#d5a14a]/20 bg-[#d5a14a]/10 px-4 py-3 text-sm leading-7 text-[#f6ead6]">{item.care_note}</p>
                      </div>
                    )) : <p className="rounded-2xl border border-white/8 bg-white/[0.03] px-4 py-4 text-sm leading-7 text-white/64">No elevated windows were flagged in the current scan horizon. Maintain baseline discipline anyway, because quiet periods are best used for prevention.</p>}
                  </div>
                </SectionCard>

                <SectionCard title="Critical Period Alerts" eyebrow="Section 05">
                  <div className="space-y-4">
                    {alerts.length ? alerts.map(item => (
                      <div key={`${item.type}-${item.date}`} className="rounded-[24px] border border-white/8 bg-white/[0.03] p-5">
                        <div className="flex flex-wrap items-center gap-3">
                          <Badge tone={item.severity === "high" ? "rose" : "gold"}>{item.severity}</Badge>
                          <Badge tone="ink">{formatDate(item.date)}</Badge>
                        </div>
                        <h3 className="mt-4 text-lg font-semibold text-[#fbf6ef]">{item.type}</h3>
                        <p className="mt-2 text-sm leading-7 text-white/64">{item.detail}</p>
                        <p className="mt-4 rounded-2xl border border-[#87b493]/25 bg-[#87b493]/10 px-4 py-3 text-sm leading-7 text-[#eef7f1]">{item.support}</p>
                      </div>
                    )) : <p className="rounded-2xl border border-white/8 bg-white/[0.03] px-4 py-4 text-sm leading-7 text-white/64">No critical alerts were identified in the current scan horizon, but the module still expects consistent preventive care and symptom-based medical judgment.</p>}
                  </div>
                </SectionCard>
              </div>

              <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
                <SectionCard title="Remedial & Preventive Guidance" eyebrow="Section 06">
                  <p className="text-sm leading-7 text-white/66">{narrative.prevention_narrative || guidance?.body_focus}</p>
                  <div className="mt-5 space-y-3">
                    {(guidance?.preventive_guidance || []).map(item => (
                      <p key={item} className="rounded-2xl border border-white/8 bg-white/[0.03] px-4 py-3 text-sm leading-7 text-white/70">{item}</p>
                    ))}
                  </div>
                  <div className="mt-5 space-y-4">
                    {(guidance?.planetary_remedies || []).map(item => (
                      <div key={item.planet} className="rounded-[24px] border border-[#d5a14a]/20 bg-[#1b1510] p-4">
                        <div className="flex items-center justify-between gap-3">
                          <h3 className="text-sm font-semibold uppercase tracking-[0.24em] text-[#f0c77d]">{item.planet}</h3>
                          <Badge tone="gold">Support</Badge>
                        </div>
                        <p className="mt-3 text-sm leading-7 text-[#f4e4cd]">{item.why}</p>
                        <p className="mt-2 text-sm leading-7 text-[#f0cf9a]">{item.mantra}</p>
                      </div>
                    ))}
                  </div>
                  <div className="mt-5 space-y-4">
                    {(guidance?.risk_management || []).map(item => (
                      <div key={item.planet} className="rounded-[24px] border border-[#df8a8a]/20 bg-[#27161a] p-4">
                        <div className="flex items-center justify-between gap-3">
                          <h3 className="text-sm font-semibold uppercase tracking-[0.24em] text-[#f0b5b5]">{item.planet}</h3>
                          <Badge tone="rose">Risk</Badge>
                        </div>
                        <p className="mt-3 text-sm leading-7 text-[#f4d9d9]">{item.why}</p>
                        <p className="mt-2 text-sm leading-7 text-[#f1bdbd]">{item.advice}</p>
                      </div>
                    ))}
                  </div>
                </SectionCard>

                <SectionCard title="Decade-wise Quality of Life Forecast" eyebrow="Section 07">
                  <div className="space-y-4">
                    {decadeForecast.map(item => (
                      <div key={item.age_band} className={`rounded-[24px] border p-5 ${item.current_decade ? "border-[#d5a14a]/35 bg-[#1b1510]" : "border-white/8 bg-white/[0.03]"}`}>
                        <div className="flex flex-wrap items-center gap-3">
                          <Badge tone={item.quality === "supportive" ? "sage" : item.quality === "mixed" ? "gold" : "rose"}>{item.quality}</Badge>
                          <Badge tone="ink">{`Age ${item.age_band}`}</Badge>
                          <Badge tone="ink">{`Score ${item.quality_score}`}</Badge>
                          {item.current_decade ? <Badge tone="gold">Current</Badge> : null}
                        </div>
                        <h3 className="mt-4 text-lg font-semibold text-[#fbf6ef]">{item.focus}</h3>
                        <p className="mt-2 text-sm leading-7 text-white/64">{item.note}</p>
                        <p className="mt-3 text-xs uppercase tracking-[0.24em] text-white/42">{item.dominant_dashas}</p>
                      </div>
                    ))}
                  </div>
                </SectionCard>
              </div>

              <SectionCard title="Final Note" eyebrow="Always In Force">
                <div className="space-y-4 text-sm leading-7 text-white/72">
                  <p>{output.medical_disclaimer}</p>
                  <p>
                    The strongest use of this report is preventive: match timing with checkups, reduce avoidable overload during elevated windows,
                    and treat unusual symptoms as medical events first and symbolic signals second.
                  </p>
                </div>
              </SectionCard>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
