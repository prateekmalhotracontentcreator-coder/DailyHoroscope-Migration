import { SEO } from '../../components/SEO';
import { PremiumGateCard } from '../../components/PremiumRoute';
import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../../context/AuthContext";

import KrishnaOracleGrid from "../../components/KrishnaOracleGrid";
import KPChartPanel from "../../components/KPChartPanel";
import SharedBirthCityPicker from "../../components/SharedBirthCityPicker";
import KrishnaShareCard from "../../components/KrishnaShareCard";
import { ShareButtons } from "../../components/ShareCard";
import KrishnaRitualScreen from "../../components/kp/KrishnaRitualScreen";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
const API = `${BACKEND_URL}/api/oracle/krishna-prashnavali`;
const KP_CHART_API = `${BACKEND_URL}/api/kp/birth-chart`;

function normalizeKPTimeZone(value) {
  if (!value) return "Asia/Kolkata";
  return /^[+-]\d{2}:\d{2}$/.test(value) ? "Asia/Kolkata" : value;
}

function formatTimestamp(value) {
  try {
    return new Intl.DateTimeFormat("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit",
    }).format(new Date(value));
  } catch {
    return "";
  }
}

function SectionCard({ title, eyebrow, children, className = "" }) {
  return (
    <section className={`rounded-[1.75rem] border border-amber-200/70 bg-[#fff8ec]/92 p-5 shadow-[0_18px_60px_rgba(120,72,20,0.12)] dark:border-amber-900/60 dark:bg-[#140e08]/95 dark:shadow-[0_18px_60px_rgba(0,0,0,0.32)] ${className}`}>
      {eyebrow ? <p className="m-0 text-[11px] uppercase tracking-[0.3em] text-amber-700/80 dark:text-amber-300/70">{eyebrow}</p> : null}
      {title ? <h2 className="m-0 mt-2 text-2xl font-semibold text-stone-900 dark:text-amber-50">{title}</h2> : null}
      <div className="mt-4">{children}</div>
    </section>
  );
}

function OracleGlassCard({ title, className = "", children, delay = "0s" }) {
  return (
    <section
      className={`rounded-xl border border-amber-300/30 bg-amber-500/[0.04] p-5 shadow-sm backdrop-blur-sm dark:border-amber-300/15 ${className}`}
      style={{ animation: `kpFadeInUp 0.7s ease-out ${delay} both` }}
    >
      {title ? <p className="m-0 text-[11px] font-semibold uppercase tracking-[0.26em] text-amber-700/80 dark:text-amber-300/70">{title}</p> : null}
      {children}
    </section>
  );
}

function VerdictBadge({ verdict }) {
  const classes = {
    YES: "bg-green-900/40 border-green-500/40 text-green-300",
    WAIT: "bg-blue-900/40 border-blue-500/40 text-blue-300",
    NO: "bg-red-900/40 border-red-500/40 text-red-300",
    PRAY: "bg-purple-900/40 border-purple-500/40 text-purple-300",
  };
  return (
    <span className={`inline-flex items-center rounded-full border px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.3em] ${classes[verdict] || classes.WAIT}`}>
      {verdict}
    </span>
  );
}

function DetailLine({ label, value }) {
  if (!value) return null;
  return (
    <div className="rounded-2xl border border-amber-200/80 bg-white/70 p-4 dark:border-amber-900/60 dark:bg-stone-950/40">
      <p className="m-0 text-[11px] font-semibold uppercase tracking-[0.24em] text-amber-700/80 dark:text-amber-300/70">{label}</p>
      <p className="m-0 mt-2 text-sm leading-7 text-stone-700 dark:text-amber-100/80">{value}</p>
    </div>
  );
}

// ─── Public landing page (shown to logged-out visitors) ──────────────────────
const KP_FAQS = [
  { q: "What is Krishna Prashnavali?", a: "Krishna Prashnavali is an ancient Vedic oracle rooted in Srimad Bhagavad Gita and traditional Prashna Shastra. The 18×18 grid (324 cells) maps to 36 canonical answers -- YES, WAIT, NO, or PRAY -- each drawn from Krishna's sacred chaupais. Your selection is guided by your intent, not by chance." },
  { q: "How is it different from a regular online oracle?", a: "Unlike random-number generators, EverydayHoroscope's KP Oracle overlays your live Vedic dasha, planetary transits, and yogas onto your answer -- so every reading carries your actual astrological fingerprint at that moment." },
  { q: "What does each verdict mean?", a: "YES (Pratibha) -- move forward with confidence. WAIT (Dhairya) -- pause and prepare; timing is not yet ripe. NO (Pratrodha) -- the path is obstructed; reconsider. PRAY (Bhakti) -- surrender and seek divine alignment before acting." },
  { q: "What is the 'Sacred Remedy' shown after a reading?", a: "Each of the 36 answers carries its own module-specific sacred remedy and behavioural practice -- drawn directly from Lord Krishna's teachings and precisely matched to the chaupai and verdict received. These are optional -- they support, not override, your own wisdom." },
  { q: "Can I ask any question?", a: "Yes -- personal, professional, spiritual, or relational. The oracle responds to sincere intent. The more specific and clear your question, the more precise the guidance." },
];

function KrishnaOracleLanding() {
  const navigate = useNavigate();
  const verdicts = [
    { v: "YES", label: "Pratibha", color: "#16a34a", desc: "Move forward with faith and disciplined action." },
    { v: "WAIT", label: "Dhairya", color: "#ca8a04", desc: "Pause. Timing is not yet aligned. Prepare within." },
    { v: "NO",   label: "Pratrodha", color: "#dc2626", desc: "The path is obstructed. Reconsider before acting." },
    { v: "PRAY", label: "Bhakti", color: "#7c3aed", desc: "Surrender. Seek divine alignment first." },
  ];

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(217,168,74,0.14),_transparent_50%),linear-gradient(180deg,_#fffaf0_0%,_#f6ead6_55%,_#efe2cd_100%)] text-stone-900">
      <SEO
        title="Krishna Prashnavali -- Ancient Vedic Oracle by Lord Krishna"
        description="Consult the 18×18 Krishna Prashnavali -- India's most sacred Vedic oracle. Get a YES, WAIT, NO, or PRAY answer from Lord Krishna, enriched with your live Dasha, planetary transits, temple remedy, and mantra."
        url="https://www.everydayhoroscope.in/krishna-prashnavali"
        schema={{
          "@context": "https://schema.org",
          "@type": "FAQPage",
          "mainEntity": KP_FAQS.map(f => ({
            "@type": "Question",
            "name": f.q,
            "acceptedAnswer": { "@type": "Answer", "text": f.a }
          }))
        }}
      />

      {/* Hero */}
      <section className="max-w-4xl mx-auto px-4 py-16 text-center">
        <p className="text-xs uppercase tracking-[0.3em] text-amber-700/70 mb-3">Ancient Vedic Oracle</p>
        <h1 className="text-4xl sm:text-5xl font-playfair font-bold text-stone-900 mb-4 leading-tight">
          Krishna Prashnavali
        </h1>
        <p className="text-lg text-stone-600 max-w-2xl mx-auto mb-2">
          The sacred 18×18 oracle rooted in Srimad Bhagavad Gita
        </p>
        <p className="text-sm text-amber-700/80 mb-10 italic">
          "Sarva-dharmān parityajya mām ekaṁ śaraṇaṁ vraja" -- Gita 18.66
        </p>
        <button
          onClick={() => navigate('/login')}
          className="inline-flex items-center gap-2 rounded-xl bg-amber-600 px-8 py-4 text-base font-semibold text-white shadow-lg hover:bg-amber-500 transition"
        >
          Consult Lord Krishna →
        </button>
        <p className="mt-4 text-xs text-stone-500">Free for all registered seekers · No credit card required</p>
      </section>

      {/* 4 Verdicts */}
      <section className="max-w-4xl mx-auto px-4 pb-14">
        <h2 className="text-center text-2xl font-playfair font-semibold text-stone-800 mb-8">The Four Sacred Verdicts</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {verdicts.map(v => (
            <div key={v.v} className="rounded-2xl border border-amber-200/60 bg-white/70 p-5 text-center shadow-sm">
              <p className="text-2xl font-bold mb-1" style={{ color: v.color }}>{v.v}</p>
              <p className="text-xs uppercase tracking-widest text-amber-700/60 mb-2">{v.label}</p>
              <p className="text-xs text-stone-600 leading-5">{v.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="bg-amber-50/60 border-y border-amber-200/40 py-14">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-center text-2xl font-playfair font-semibold text-stone-800 mb-10">How It Works</h2>
          <div className="grid sm:grid-cols-3 gap-8 text-center">
            {[
              { n: "1", title: "Hold your question", body: "Frame one sincere, clear question -- personal, professional, or spiritual." },
              { n: "2", title: "Choose a cell", body: "Close your eyes, breathe, and tap any cell in the 18×18 grid. Your live planetary chart is read at that exact moment." },
              { n: "3", title: "Receive Krishna's answer", body: "A verdict (YES/WAIT/NO/PRAY) arrives with sacred verse, practical action, and a behavioural remedy drawn directly from Lord Krishna's teachings." },
            ].map(s => (
              <div key={s.n}>
                <div className="w-10 h-10 rounded-full bg-amber-600/10 border border-amber-400/40 text-amber-700 font-bold flex items-center justify-center mx-auto mb-3 text-lg">{s.n}</div>
                <h3 className="font-semibold text-stone-800 mb-2">{s.title}</h3>
                <p className="text-sm text-stone-600 leading-6">{s.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="max-w-3xl mx-auto px-4 py-14">
        <h2 className="text-center text-2xl font-playfair font-semibold text-stone-800 mb-8">Frequently Asked Questions</h2>
        <div className="space-y-4">
          {KP_FAQS.map((f, i) => (
            <div key={i} className="rounded-2xl border border-amber-200/60 bg-white/70 p-5">
              <p className="font-semibold text-stone-800 mb-2">{f.q}</p>
              <p className="text-sm text-stone-600 leading-6">{f.a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="text-center pb-16 px-4">
        <h2 className="text-2xl font-playfair font-semibold text-stone-800 mb-4">Ready to ask your question?</h2>
        <p className="text-stone-500 text-sm mb-6">Join thousands of seekers who consult Lord Krishna daily.</p>
        <button
          onClick={() => navigate('/register')}
          className="inline-flex items-center gap-2 rounded-xl bg-amber-600 px-8 py-4 text-base font-semibold text-white shadow-lg hover:bg-amber-500 transition"
        >
          Create Free Account →
        </button>
        <p className="mt-3 text-xs text-stone-500">Already registered? <button onClick={() => navigate('/login')} className="text-amber-700 underline">Sign in</button></p>
      </section>
    </div>
  );
}

// ─── Main export -- auth-aware + premium-aware ─────────────────────────────────
export default function KrishnaOraclePage() {
  const { user, loading: authLoading } = useAuth();

  if (authLoading) return null;

  // Logged-out visitors → public landing (indexed by Google)
  if (!user) return <KrishnaOracleLanding />;

  // Logged-in but not premium → premium gate
  if (!user.is_premium) return (
    <PremiumGateCard
      feature="Krishna Prashnavali"
      description="Receive guidance from Lord Krishna's sacred oracle -- an exclusive Premium feature. Upgrade to ask your question and receive a divine answer."
    />
  );

  // Premium → full oracle
  return <KrishnaOracleApp />;
}

function KrishnaOracleApp() {
  const { user } = useAuth();
  const [metadata, setMetadata] = useState(null);
  const [history, setHistory] = useState([]);
  const [loadingMeta, setLoadingMeta] = useState(true);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [questionText, setQuestionText] = useState("");
  const [focusArea, setFocusArea] = useState("guidance");
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [reading, setReading] = useState(null);
  const [loadingPastReading, setLoadingPastReading] = useState(false);
  const [ritualComplete, setRitualComplete] = useState(() => window.sessionStorage.getItem("kp_ritual_done") === "1");
  const guidanceRef = useRef(null);
  const shareCardRef = useRef(null);
  const historyRef = useRef(null);

  // Scroll to Guidance Report whenever a reading is loaded (new or past)
  useEffect(() => {
    if (reading && guidanceRef.current) {
      guidanceRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [reading]);
  const [questionError, setQuestionError] = useState("");

  // Birth details for dasha computation
  const [birthForm, setBirthForm] = useState({ date_of_birth: "", time_of_birth: "", latitude: "", longitude: "", timezone_offset: "+05:30", timezone_name: "Asia/Kolkata", place_label: "", city_slug: "" });
  const [birthFormOpen, setBirthFormOpen] = useState(false);
  const [birthAutoFilled, setBirthAutoFilled] = useState(false);
  const [kpChart, setKpChart] = useState(null);
  const [kpChartLoading, setKpChartLoading] = useState(false);
  const [kpChartError, setKpChartError] = useState("");

  const gridMatrix = metadata?.grid_matrix || [];

  useEffect(() => {
    document.title = "Krishna Prashnavali | Everyday Horoscope";
  }, []);

  useEffect(() => {
    let active = true;
    async function loadMetadata() {
      setLoadingMeta(true);
      setError("");
      try {
        const response = await axios.get(`${API}/meta`, { withCredentials: true });
        if (!active) return;
        setMetadata(response.data);
      } catch (fetchError) {
        if (!active) return;
        setError(fetchError?.response?.data?.detail || "Unable to load Krishna oracle metadata.");
      } finally {
        if (active) setLoadingMeta(false);
      }
    }
    loadMetadata();
    return () => {
      active = false;
    };
  }, []);

  async function loadHistory() {
    setLoadingHistory(true);
    try {
      const response = await axios.get(`${API}/history`, {
        params: { page: 1, limit: 8 },
        withCredentials: true,
      });
      setHistory(response.data?.items || []);
    } catch (fetchError) {
      setError(fetchError?.response?.data?.detail || "Unable to load Krishna reading history.");
    } finally {
      setLoadingHistory(false);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  // Auto-populate birth form from saved profile
  useEffect(() => {
    if (!user) return;
    const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
    axios.get(`${BACKEND_URL}/api/profile/birth`, { withCredentials: true })
      .then(res => {
        const profiles = Array.isArray(res.data) ? res.data : [];
        if (profiles.length === 0) { setBirthFormOpen(true); return; }
        const p = profiles[0];
        // Convert timezone name to offset -- default IST if not stored as offset
        const tzOffset = p.timezone?.includes(":") ? p.timezone : "+05:30";
        setBirthForm({
          date_of_birth: p.date_of_birth || "",
          time_of_birth: p.time_of_birth || "",
          latitude: p.latitude ?? "",
          longitude: p.longitude ?? "",
          timezone_offset: tzOffset,
          timezone_name: normalizeKPTimeZone(p.timezone),
          place_label: p.location || "",
          city_slug: "",
        });
        setBirthAutoFilled(true);
      })
      .catch(() => { setBirthFormOpen(true); });
  }, [user]);

  useEffect(() => {
    if (!user) {
      setKpChart(null);
      setKpChartError("");
      return;
    }
    const hasCompleteBirthData = Boolean(
      birthForm.date_of_birth &&
      birthForm.time_of_birth &&
      birthForm.latitude !== "" &&
      birthForm.longitude !== "",
    );
    if (!hasCompleteBirthData) {
      setKpChart(null);
      setKpChartError("");
      return;
    }

    let active = true;
    async function loadKPChart() {
      setKpChartLoading(true);
      setKpChartError("");
      try {
        const response = await axios.post(KP_CHART_API, {
          date_of_birth: birthForm.date_of_birth,
          time_of_birth: birthForm.time_of_birth,
          latitude: Number(birthForm.latitude),
          longitude: Number(birthForm.longitude),
          timezone: normalizeKPTimeZone(birthForm.timezone_name),
          place_label: birthForm.place_label || null,
        });
        if (!active) return;
        setKpChart(response.data || null);
      } catch (fetchError) {
        if (!active) return;
        setKpChart(null);
        setKpChartError(fetchError?.response?.data?.detail || "Unable to load your KP chart right now.");
      } finally {
        if (active) setKpChartLoading(false);
      }
    }

    loadKPChart();
    return () => {
      active = false;
    };
  }, [user, birthForm.date_of_birth, birthForm.time_of_birth, birthForm.latitude, birthForm.longitude, birthForm.place_label, birthForm.timezone_name]);

  async function loadPastReading(reportId) {
    if (!reportId) return;
    setLoadingPastReading(true);
    setError("");
    try {
      const response = await axios.get(`${API}/reports/${reportId}`, { withCredentials: true });
      setReading(response.data || null);
    } catch {
      setError("Could not load that reading. Please try again.");
    } finally {
      setLoadingPastReading(false);
    }
  }

  function validateQuestion(value) {
    const trimmed = value.trim();
    if (!trimmed) return "";
    if (trimmed.length < 12 || trimmed.split(/\s+/).length < 3) {
      return "Enter one clear question with at least 3 words so Krishna's response can address it properly.";
    }
    return "";
  }

  function handleRitualComplete() {
    window.sessionStorage.setItem("kp_ritual_done", "1");
    setRitualComplete(true);
  }

  function handleAskAgain() {
    setReading(null);
    setSelectedIndex(null);
    guidanceRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  async function handleCellSelect({ row, col, index }) {
    const nextQuestionError = validateQuestion(questionText);
    if (nextQuestionError) {
      setQuestionError(nextQuestionError);
      setError("");
      return;
    }
    setSelectedIndex(index);
    setSubmitting(true);
    setError("");
    setQuestionError("");
    try {
      const birthPayload = (birthForm.date_of_birth && birthForm.time_of_birth && birthForm.latitude !== "" && birthForm.longitude !== "")
        ? {
            date_of_birth: birthForm.date_of_birth,
            time_of_birth: birthForm.time_of_birth,
            latitude: Number(birthForm.latitude),
            longitude: Number(birthForm.longitude),
            timezone_offset: birthForm.timezone_offset || "+05:30",
          }
        : {};
      const response = await axios.post(
        `${API}/select`,
        {
          row,
          col,
          question_text: questionText.trim() || null,
          focus_area: focusArea,
          language_preference: "bilingual",
          reveal_mode: "ritual",
          ...birthPayload,
        },
        { withCredentials: true }
      );
      setReading(response.data?.reading || null);
      await loadHistory();
    } catch (submitError) {
      setError(submitError?.response?.data?.detail || "Unable to generate Krishna guidance right now.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(217,168,74,0.18),_transparent_42%),linear-gradient(180deg,_#fffaf0_0%,_#f6ead6_52%,_#efe2cd_100%)] px-4 py-8 text-stone-900 dark:bg-[radial-gradient(circle_at_top,_rgba(180,83,9,0.18),_transparent_40%),linear-gradient(180deg,_#0a0604_0%,_#120a06_48%,_#090605_100%)] dark:text-white md:px-8">
      <SEO title="Krishna Prashnavali Oracle" noindex={true} />
      <style>{`
        @keyframes kpFadeInUp {
          from { opacity: 0; transform: translateY(18px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
      <div className="mx-auto max-w-7xl space-y-6">
        <div className="flex items-center justify-between">
          <Link
            to="/strategist"
            className="inline-flex items-center gap-1.5 rounded-lg border border-amber-400/40 bg-amber-50/60 px-3 py-1.5 text-xs font-medium text-amber-800 transition hover:bg-amber-100/80 dark:border-amber-700/40 dark:bg-amber-900/20 dark:text-amber-300 dark:hover:bg-amber-900/40"
          >
            ← War Room
          </Link>
        </div>
        <SectionCard eyebrow="Krishna Oracle" title="Ask Lord Krishna Through the 18 × 18 Prashnavali">
          <div className="grid gap-6 lg:grid-cols-[1.15fr,0.85fr]">
            <div className="space-y-4">
              <p className="m-0 max-w-3xl text-sm leading-7 text-stone-700 dark:text-amber-100/75">
                Phase 1 is hard-frozen to the Krishna 18 × 18 grid. The clicked cell becomes position 0, and the backend advances every 12 letters across 9 deterministic steps.
              </p>
              <div className="grid gap-4 md:grid-cols-2">
                <label className="rounded-2xl border border-amber-200/80 bg-white/75 p-4 dark:border-amber-900/60 dark:bg-stone-950/40">
                  <span className="block text-[11px] uppercase tracking-[0.26em] text-amber-700/80 dark:text-amber-300/70">Focus area</span>
                  <select
                    value={focusArea}
                    onChange={(event) => setFocusArea(event.target.value)}
                    className="mt-3 w-full rounded-xl border border-amber-300 bg-white px-3 py-2 text-sm text-stone-900 outline-none dark:border-amber-900/60 dark:bg-[#1d120b] dark:text-amber-50"
                  >
                    <option value="guidance">General guidance</option>
                    <option value="career">Career</option>
                    <option value="love">Love</option>
                    <option value="health">Health</option>
                    <option value="spiritual">Spiritual</option>
                  </select>
                </label>
                <div className="rounded-2xl border border-amber-200/80 bg-white/75 p-4 dark:border-amber-900/60 dark:bg-stone-950/40">
                  <span className="block text-[11px] uppercase tracking-[0.26em] text-amber-700/80 dark:text-amber-300/70">Ritual Flow</span>
                  <p className="mt-3 text-sm leading-7 text-stone-700 dark:text-amber-100/75">
                    A white-light meditation opens once per browser session. After it fades, the grid and letter sequence reveal remain fully deterministic.
                  </p>
                </div>
              </div>
              <label className="block rounded-2xl border border-amber-200/80 bg-white/75 p-4 dark:border-amber-900/60 dark:bg-stone-950/40">
                <span className="block text-[11px] uppercase tracking-[0.26em] text-amber-700/80 dark:text-amber-300/70">Your Question</span>
                <div className="mt-2 rounded-xl border border-amber-300/60 bg-amber-50/60 px-3 py-2 dark:border-amber-700/40 dark:bg-amber-900/20">
                  <p className="m-0 text-xs font-semibold text-amber-800 dark:text-amber-300">Important: Ask a direct, decisive question only.</p>
                  <p className="m-0 mt-1 text-xs text-amber-700/90 dark:text-amber-400/80">
                    Krishna Prashnavali answers YES, WAIT, NO, or PRAY -- it is designed for single, clear questions. Questions that can be answered with a decisive choice qualify. Examples: "Should I accept this job offer?", "Is this the right time to move cities?", "Should I invest in this opportunity?"
                  </p>
                  <p className="m-0 mt-1 text-xs text-amber-700/70 dark:text-amber-400/60">
                    Vague or descriptive questions ("What is my purpose?", "Tell me about my career") do not qualify and will produce a general response.
                  </p>
                </div>
                <textarea
                  value={questionText}
                  onChange={(event) => {
                    const value = event.target.value;
                    setQuestionText(value);
                    if (questionError) {
                      setQuestionError(validateQuestion(value));
                    }
                  }}
                  onBlur={() => setQuestionError(validateQuestion(questionText))}
                  rows={3}
                  placeholder="Should I proceed with this decision? (Frame as a direct question)"
                  className="mt-3 w-full rounded-xl border border-amber-300 bg-white px-3 py-3 text-sm text-stone-900 outline-none placeholder:text-stone-400 dark:border-amber-900/60 dark:bg-[#1d120b] dark:text-amber-50 dark:placeholder:text-amber-100/30"
                />
                {questionError ? <p className="mt-2 text-sm leading-6 text-rose-700 dark:text-rose-200">{questionError}</p> : null}
              </label>
            </div>

            <div className="rounded-[1.75rem] border border-amber-200/80 bg-white/75 p-5 dark:border-amber-900/60 dark:bg-stone-950/40">
              <p className="m-0 text-[11px] uppercase tracking-[0.3em] text-amber-700/80 dark:text-amber-300/70">Implementation status</p>
              <ul className="mt-4 space-y-3 text-sm leading-7 text-stone-700 dark:text-amber-100/80">
                <li>Grid size: {metadata?.grid_size || 18} × {metadata?.grid_size || 18}</li>
                <li>Jump interval: {metadata?.jump_interval || 12}</li>
                <li>Sequence length: {metadata?.sequence_length || 9}</li>
                <li>Canonical answers: {metadata?.canonical_answer_count || 36}</li>
                <li>Content status: {metadata?.content_status || "loading"}</li>
                <li>Mapping status: {metadata?.mapping_status || "loading"}</li>
              </ul>
            </div>
          </div>
        </SectionCard>

        {error ? (
          <SectionCard title="Oracle notice">
            <p className="m-0 text-sm leading-7 text-rose-700 dark:text-rose-200">{error}</p>
          </SectionCard>
        ) : null}

        {/* Birth Details -- for live Dasha context */}
        <div className="rounded-[1.75rem] border border-amber-200/70 bg-[#fff8ec]/92 p-5 shadow-sm dark:border-amber-900/60 dark:bg-[#140e08]/95">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="m-0 text-[11px] uppercase tracking-[0.3em] text-amber-700/80 dark:text-amber-300/70">Vedic Context</p>
              <h2 className="m-0 mt-1 text-lg font-semibold text-stone-900 dark:text-amber-50">Your Birth Details</h2>
              {birthAutoFilled && !birthFormOpen && (
                <p className="m-0 mt-1 text-xs text-amber-700/80 dark:text-amber-400/70">
                  Auto-filled from your saved profile -- {birthForm.place_label || "birth location"}. Your current Dasha will be included in every reading.
                </p>
              )}
              {!birthAutoFilled && !birthFormOpen && (
                <p className="m-0 mt-1 text-xs text-stone-500 dark:text-amber-100/50">
                  Add your birth details to include your live Mahadasha in this reading.
                </p>
              )}
            </div>
            <button
              type="button"
              onClick={() => setBirthFormOpen(v => !v)}
              className="shrink-0 rounded-lg border border-amber-300/60 px-3 py-1.5 text-xs font-medium text-amber-800 transition hover:bg-amber-50 dark:border-amber-700/40 dark:text-amber-300 dark:hover:bg-amber-900/20"
            >
              {birthFormOpen ? "Collapse" : birthAutoFilled ? "Edit" : "Add Details"}
            </button>
          </div>
          {birthFormOpen && (
            <div className="mt-4 grid gap-4 sm:grid-cols-2">
              <label className="space-y-1">
                <span className="text-xs font-medium text-stone-600 dark:text-amber-200/70">Date of Birth</span>
                <input
                  type="date"
                  value={birthForm.date_of_birth}
                  onChange={e => setBirthForm(f => ({ ...f, date_of_birth: e.target.value }))}
                  className="w-full rounded-xl border border-amber-300/60 bg-white px-3 py-2 text-sm text-stone-900 outline-none dark:border-amber-900/50 dark:bg-stone-900 dark:text-amber-50"
                />
              </label>
              <label className="space-y-1">
                <span className="text-xs font-medium text-stone-600 dark:text-amber-200/70">Time of Birth</span>
                <input
                  type="time"
                  value={birthForm.time_of_birth}
                  onChange={e => setBirthForm(f => ({ ...f, time_of_birth: e.target.value }))}
                  className="w-full rounded-xl border border-amber-300/60 bg-white px-3 py-2 text-sm text-stone-900 outline-none dark:border-amber-900/50 dark:bg-stone-900 dark:text-amber-50"
                />
              </label>
              <div className="sm:col-span-2">
                <SharedBirthCityPicker
                  inputId="kp-birth-city"
                  label={<span className="text-xs font-medium text-stone-600 dark:text-amber-200/70">Place of Birth</span>}
                  placeholder="Search city, country, or timezone..."
                  value={birthForm.city_slug}
                  onChange={city => {
                    // Convert IANA timezone to +HH:MM offset for vedic_calculator
                    let tzOffset = "+05:30";
                    try {
                      const d = new Date();
                      const utc = new Date(d.toLocaleString("en-US", { timeZone: "UTC" }));
                      const local = new Date(d.toLocaleString("en-US", { timeZone: city.timezone }));
                      const diff = (local - utc) / 60000;
                      const h = String(Math.floor(Math.abs(diff) / 60)).padStart(2, "0");
                      const m = String(Math.abs(diff) % 60).padStart(2, "0");
                      tzOffset = `${diff >= 0 ? "+" : "-"}${h}:${m}`;
                    } catch { /* keep IST default */ }
                    setBirthForm(f => ({
                      ...f,
                      city_slug: city.slug,
                      place_label: `${city.city_name}, ${city.country || city.country_name}`,
                      latitude: city.latitude,
                      longitude: city.longitude,
                      timezone_offset: tzOffset,
                      timezone_name: city.timezone || "Asia/Kolkata",
                    }));
                  }}
                  wrapperStyle={{ width: "100%" }}
                  labelStyle={{ display: "block" }}
                />
                {birthForm.place_label && (
                  <p className="mt-1 text-xs text-amber-700/70 dark:text-amber-400/60">
                    Selected: {birthForm.place_label}
                  </p>
                )}
              </div>
              <div className="sm:col-span-2">
                <button
                  type="button"
                  onClick={() => { setBirthFormOpen(false); setBirthAutoFilled(true); }}
                  disabled={!birthForm.date_of_birth || !birthForm.time_of_birth || birthForm.latitude === ""}
                  className="rounded-xl bg-amber-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-amber-500 disabled:opacity-40"
                >
                  Save & Use These Details
                </button>
              </div>
            </div>
          )}
        </div>

        {birthForm.date_of_birth && birthForm.time_of_birth && birthForm.latitude !== "" && birthForm.longitude !== "" ? (
          kpChartLoading && !kpChart ? (
            <SectionCard title="Your KP Chart" eyebrow="Natal Foundation">
              <div className="space-y-4">
                <div className="h-4 w-48 rounded-full bg-amber-200/20 dark:bg-amber-100/10" />
                <div className="grid gap-3 md:grid-cols-3">
                  <div className="h-20 rounded-2xl border border-amber-200/40 bg-white/40 dark:border-amber-900/30 dark:bg-stone-950/30" />
                  <div className="h-20 rounded-2xl border border-amber-200/40 bg-white/40 dark:border-amber-900/30 dark:bg-stone-950/30" />
                  <div className="h-20 rounded-2xl border border-amber-200/40 bg-white/40 dark:border-amber-900/30 dark:bg-stone-950/30" />
                </div>
              </div>
            </SectionCard>
          ) : kpChart ? (
            <KPChartPanel
              kpChart={kpChart}
              theme="oracle"
              title="Your KP Chart"
              eyebrow="Natal Foundation"
              description="This natal KP layer stays available above the oracle grid, so each reading rests on your Placidus cusps, sub-lords, and significator map."
            />
          ) : kpChartError ? (
            <SectionCard title="Your KP Chart" eyebrow="Natal Foundation">
              <p className="m-0 text-sm leading-7 text-rose-700 dark:text-rose-200">{kpChartError}</p>
            </SectionCard>
          ) : null
        ) : (
          <SectionCard title="Your KP Chart" eyebrow="Natal Foundation">
            <p className="m-0 text-sm leading-7 text-stone-700 dark:text-amber-100/75">
              Add your full birth details, including birthplace coordinates, to unlock your persistent KP natal chart above the oracle grid.
            </p>
            <div className="mt-5">
              <button
                type="button"
                onClick={() => setBirthFormOpen(true)}
                className="inline-flex items-center rounded-full border border-amber-300/60 bg-amber-50/60 px-5 py-3 text-sm font-semibold text-amber-800 transition hover:bg-amber-100/80 dark:border-amber-700/40 dark:bg-amber-900/20 dark:text-amber-300 dark:hover:bg-amber-900/40"
              >
                Add Birth Details
              </button>
            </div>
          </SectionCard>
        )}

        <SectionCard title="Selection Grid" eyebrow="Deterministic Matrix">
          {loadingMeta ? (
            <p className="m-0 text-sm text-stone-600 dark:text-amber-100/75">Loading Krishna grid...</p>
          ) : (
            <div className="relative overflow-hidden rounded-[1.75rem]">
              {!ritualComplete ? <KrishnaRitualScreen onComplete={handleRitualComplete} /> : null}
              <div
                className={`transition-opacity ${ritualComplete ? "opacity-100" : "pointer-events-none opacity-0"}`}
                style={{ transitionDuration: "1500ms" }}
              >
                <KrishnaOracleGrid
                  gridMatrix={gridMatrix}
                  selectedIndex={selectedIndex}
                  disabled={submitting}
                  revealEnabled={true}
                  onSelect={handleCellSelect}
                />
              </div>
            </div>
          )}
        </SectionCard>

        {reading ? (
          <>
          <div ref={guidanceRef}>
          <SectionCard title="Guidance Report" eyebrow={`Answer slot ${reading.answer_slot}`}>
            <div className="space-y-5">
              {reading.question_text ? (
                <div className="rounded-2xl border border-amber-200/80 bg-white/70 p-4 dark:border-amber-900/60 dark:bg-stone-950/40">
                  <p className="m-0 text-[11px] font-semibold uppercase tracking-[0.26em] text-amber-700/80 dark:text-amber-300/70">Your Question</p>
                  <p className="m-0 mt-3 text-base leading-8 text-stone-900 dark:text-amber-50">{reading.question_text}</p>
                  <p className="m-0 mt-2 text-sm leading-7 text-stone-600 dark:text-amber-100/70">
                    Focus area: {(reading.focus_area || "guidance").replace(/_/g, " ")}
                  </p>
                </div>
              ) : null}

              <OracleGlassCard className="text-center" delay="0s">
                <div className="flex flex-col items-center gap-4">
                  <VerdictBadge verdict={reading.answer.verdict_display} />
                  <p className="m-0 font-serif text-2xl leading-10 text-amber-700 dark:text-amber-300 md:text-3xl">
                    {reading.answer.chaupai_phrase || reading.chaupai_string?.sanskrit_block}
                  </p>
                  <p className="m-0 text-sm font-semibold uppercase tracking-[0.24em] text-stone-500 dark:text-amber-100/60">
                    {reading.answer.title?.english_block}
                  </p>
                  <p className="m-0 max-w-3xl font-playfair text-xl italic leading-9 text-stone-800/90 dark:text-amber-50/85">
                    {reading.answer.krishna_answer?.english_block}
                  </p>
                </div>
              </OracleGlassCard>

              <div className="grid gap-5 md:grid-cols-2">
                <OracleGlassCard title="Your Cosmic Context" delay="0.15s">
                  {reading.birth_data_present ? (
                    <div className="space-y-4">
                      <p className="m-0 text-sm leading-7 text-stone-700 dark:text-amber-100/80">
                        You are in {reading.current_mahadasha} · {reading.current_antardasha}
                      </p>
                      {reading.astro_context ? (
                        <p className="m-0 text-sm leading-7 text-stone-700 dark:text-amber-100/80">{reading.astro_context}</p>
                      ) : null}
                      <div className="rounded-2xl border border-amber-200/80 bg-white/70 p-4 dark:border-amber-900/60 dark:bg-stone-950/40">
                        <p className="m-0 text-[11px] font-semibold uppercase tracking-[0.24em] text-amber-700/80 dark:text-amber-300/70">What this means for you</p>
                        <p className="m-0 mt-3 text-sm leading-7 text-stone-700 dark:text-amber-100/80">
                          {reading.answer.meaning?.english_block}
                        </p>
                      </div>
                    </div>
                  ) : (
                    <div className="rounded-2xl border border-amber-400/40 bg-amber-50/80 p-4 text-sm leading-7 text-amber-900 dark:border-amber-700/40 dark:bg-amber-900/20 dark:text-amber-200">
                      <p className="m-0">Add your birth details to unlock your personal cosmic context.</p>
                      <Link to="/birth-chart" className="mt-3 inline-flex font-semibold text-amber-700 underline dark:text-amber-300">
                        Add birth details →
                      </Link>
                    </div>
                  )}
                </OracleGlassCard>

                <OracleGlassCard title="Your Path Forward" delay="0.3s">
                  <div className="space-y-4">
                    <p className="m-0 text-sm leading-7 text-stone-700 dark:text-amber-100/80">
                      {reading.answer.what_to_do?.english_block}
                    </p>
                    <DetailLine
                      label="Inner shift required"
                      value={(reading.summary_report?.behavioral_remedy || reading.answer.behavioral_remedy)?.english_block}
                    />
                    <DetailLine
                      label="Sacred Remedy"
                      value={reading.answer.remedy?.english_block}
                    />
                    <DetailLine
                      label="Watch for"
                      value={reading.answer.precaution?.english_block}
                    />
                    <DetailLine
                      label="Timeframe"
                      value={reading.answer.duration?.english_block}
                    />
                  </div>
                </OracleGlassCard>
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <button
                  type="button"
                  onClick={handleAskAgain}
                  className="rounded-full border border-amber-300 bg-white/80 px-4 py-2 text-sm font-medium text-stone-900 transition hover:bg-amber-50 dark:border-amber-700/60 dark:bg-stone-950/40 dark:text-amber-50 dark:hover:bg-stone-900"
                >
                  Ask again
                </button>
                <button
                  type="button"
                  onClick={() => historyRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })}
                  className="rounded-full border border-amber-300 bg-white/80 px-4 py-2 text-sm font-medium text-stone-900 transition hover:bg-amber-50 dark:border-amber-700/60 dark:bg-stone-950/40 dark:text-amber-50 dark:hover:bg-stone-900"
                >
                  View history
                </button>
              </div>

              {/* KrishnaShareCard is offscreen -- position:fixed left:-9999 -- capture target only */}
              <KrishnaShareCard
                ref={shareCardRef}
                reading={{
                  verdict_display: reading.answer.verdict_display,
                  chaupai_phrase: reading.answer.chaupai_phrase || reading.chaupai_string?.sanskrit_block || "",
                  title: reading.answer.title,
                  krishna_answer: reading.answer.krishna_answer,
                  what_to_do: reading.answer.what_to_do,
                  krishna_message: reading.answer.krishna_message,
                }}
              />
            </div>
          </SectionCard>
          </div>
          {/* Share bar -- full-width below reading, matching Panchang/Horoscope pattern */}
          <ShareButtons
            pageUrl={`${window.location.origin}/krishna-prashnavali`}
            shareText={`${reading.answer.krishna_answer.english_block}\nVerdict: ${reading.answer.verdict_display}\n${reading.answer.what_to_do.english_block}`}
            cardRef={shareCardRef}
            filename={`krishna-prashnavali-${reading.answer.answer_id || reading.answer_id || reading.report_id || 'reading'}`}
            fbPageCaption={localStorage.getItem('admin_token') ? `🪔 Krishna Prashnavali -- ${reading.answer.verdict_display}\n\n${reading.answer.krishna_answer.english_block}\n\n${reading.answer.what_to_do.english_block}\n\n🔮 everydayhoroscope.in/krishna-prashnavali` : null}
          />
          </>
        ) : null}

        <div ref={historyRef}>
        <SectionCard title="Recent Krishna Readings" eyebrow="History">
          {loadingHistory ? (
            <p className="m-0 text-sm text-stone-600 dark:text-amber-100/75">Loading history...</p>
          ) : history.length === 0 ? (
            <p className="m-0 text-sm text-stone-600 dark:text-amber-100/75">Your Krishna readings will appear here after the first selection.</p>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
              {history.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => loadPastReading(item.report_id)}
                  disabled={loadingPastReading}
                  className="rounded-2xl border border-amber-200/80 bg-white/75 p-4 text-left transition hover:border-amber-400 hover:shadow-md dark:border-amber-900/60 dark:bg-stone-950/40 dark:hover:border-amber-600/60 disabled:opacity-50"
                >
                  <p className="m-0 text-[11px] uppercase tracking-[0.24em] text-amber-700/80 dark:text-amber-300/70">{item.verdict_display}</p>
                  <h3 className="m-0 mt-2 text-lg font-semibold text-stone-900 dark:text-amber-50">{item.summary}</h3>
                  <p className="m-0 mt-2 text-sm leading-7 text-stone-700 dark:text-amber-100/75">
                    Cell [{item.row}][{item.col}] • slot {item.answer_slot}
                  </p>
                  <p className="m-0 mt-2 text-xs text-stone-500 dark:text-amber-100/50">{formatTimestamp(item.created_at)}</p>
                  <p className="m-0 mt-3 text-[11px] font-medium text-amber-600 dark:text-amber-400">Tap to reload reading →</p>
                </button>
              ))}
            </div>
          )}
        </SectionCard>
        </div>

        {/* ── On-page SEO content ─────────────────────────────────────────── */}
        <div className="mt-12 space-y-8 border-t border-amber-200/50 pt-10 text-sm text-stone-600 dark:border-amber-900/40 dark:text-amber-100/60">
          <div>
            <h2 className="mb-2 text-base font-semibold text-stone-800 dark:text-amber-100">What is Krishna Prashnavali?</h2>
            <p className="leading-7">Krishna Prashnavali (कृष्ण प्रश्नावली) is one of the most revered Prashna oracles in the Vedic tradition. Rooted in the sacred chaupais of Srimad Bhagavad Gita and traditional Prashna Shastra, it presents 36 divine answers arranged in an 18×18 grid of 324 cells. Each cell, when selected with sincere intent, resolves to a verdict -- YES (Pratibha), WAIT (Dhairya), NO (Pratrodha), or PRAY (Bhakti) -- drawn directly from Lord Krishna's teachings to Arjuna.</p>
          </div>
          <div>
            <h2 className="mb-2 text-base font-semibold text-stone-800 dark:text-amber-100">How the 18×18 Grid Works</h2>
            <p className="leading-7">The oracle operates on a sacred 9-step chaupai sequence. When you select a cell, the system treats it as position 0 and advances deterministically through 9 chaupai letters using a 12-letter interval -- always producing the same answer for a given grid position regardless of when it is consulted. This is not randomness; it is structured Vedic Prashna logic, where the sincerity of your question, not chance, guides your hand.</p>
          </div>
          <div>
            <h2 className="mb-2 text-base font-semibold text-stone-800 dark:text-amber-100">Understanding the Four Verdicts</h2>
            <p className="leading-7"><strong className="text-stone-800 dark:text-amber-100">YES -- Pratibha:</strong> Lord Krishna signals a clear forward path. Act with confidence and discipline. <strong className="text-stone-800 dark:text-amber-100">WAIT -- Dhairya:</strong> The timing is not yet aligned. Pause, prepare internally, and let circumstances mature. <strong className="text-stone-800 dark:text-amber-100">NO -- Pratrodha:</strong> An obstacle is present on the current path. Reconsider your approach, not your goal. <strong className="text-stone-800 dark:text-amber-100">PRAY -- Bhakti:</strong> Surrender the outcome. Seek divine alignment through devotion before any action is taken.</p>
          </div>
          <div>
            <h2 className="mb-2 text-base font-semibold text-stone-800 dark:text-amber-100">What is Prashna Shastra?</h2>
            <p className="leading-7">Prashna Shastra is the Vedic science of answering questions -- an ancient branch of Jyotish (Vedic astrology) in which the moment of the question itself is cast as a horoscope. Unlike natal astrology, which requires a birth chart, Prashna works solely from the energy of the query and the moment it is posed. EverydayHoroscope layers this with your live dasha, planetary transits, and current yogas to give each reading an astrological fingerprint unique to you and the moment of asking.</p>
          </div>
          <div>
            <h2 className="mb-2 text-base font-semibold text-stone-800 dark:text-amber-100">Behavioural Remedy & Sacred Practice</h2>
            <p className="leading-7">Each of the 36 answers carries a module-specific behavioural remedy -- a contemplative practice drawn from Krishna's own teachings and aligned to the verdict received. These are not generic prescriptions; they are precisely paired to the chaupai, the verdict, and the spiritual intent of Lord Krishna's answer. The remedy guides how to carry the oracle's wisdom into your daily life.</p>
          </div>
          <div>
            <h2 className="mb-2 text-base font-semibold text-stone-800 dark:text-amber-100">Using Krishna Prashnavali Effectively</h2>
            <p className="leading-7">Approach each session with one sincere, clearly framed question. Avoid repeating the same question in one session -- the oracle is consulted for genuine matters, not for confirmation. Hold your question in mind as you close your eyes, breathe, and let your hand fall on a cell. Read the full answer including the sacred verse (chaupai), meaning, practical action, and behavioural remedy before forming your response. Your Historical Readings above allow you to track patterns across multiple consultations over time.</p>
          </div>
        </div>

      </div>
    </div>
  );
}
