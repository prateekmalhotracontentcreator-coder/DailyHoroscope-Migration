import { SEO } from '../components/SEO';
import { PremiumGateCard } from '../components/PremiumRoute';
import React, { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/AuthContext";

import KrishnaOracleGrid from "../components/KrishnaOracleGrid";
import { extractChaupaiIndices } from "../utils/chaupaiExtractor";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
const API = `${BACKEND_URL}/api/oracle/krishna-prashnavali`;

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

function BilingualBlockView({ label, block }) {
  if (!block) return null;
  return (
    <div className="rounded-2xl border border-amber-200/80 bg-white/75 p-4 dark:border-amber-900/60 dark:bg-stone-950/40">
      <p className="m-0 text-[11px] font-semibold uppercase tracking-[0.26em] text-amber-700/80 dark:text-amber-300/70">{label}</p>
      <p className="m-0 mt-3 text-lg leading-8 text-stone-900 dark:text-amber-50">{block.sanskrit_block}</p>
      <p className="m-0 mt-2 text-sm leading-7 text-stone-700 dark:text-amber-100/80">{block.english_block}</p>
    </div>
  );
}

function SummaryBlock({ title, content }) {
  if (!content) return null;
  return (
    <div className="rounded-2xl border border-amber-200/80 bg-white/75 p-4 dark:border-amber-900/60 dark:bg-stone-950/40">
      <p className="m-0 text-[11px] font-semibold uppercase tracking-[0.26em] text-amber-700/80 dark:text-amber-300/70">{title}</p>
      <p className="m-0 mt-3 text-base leading-7 text-stone-900 dark:text-amber-50">{content.sanskrit_block}</p>
      <p className="m-0 mt-2 text-sm leading-7 text-stone-700 dark:text-amber-100/80">{content.english_block}</p>
    </div>
  );
}

// ─── Public landing page (shown to logged-out visitors) ──────────────────────
const KP_FAQS = [
  { q: "What is Krishna Prashnavali?", a: "Krishna Prashnavali is an ancient Vedic oracle rooted in Srimad Bhagavad Gita and traditional Prashna Shastra. The 18×18 grid (324 cells) maps to 36 canonical answers — YES, WAIT, NO, or PRAY — each drawn from Krishna's sacred chaupais. Your selection is guided by your intent, not by chance." },
  { q: "How is it different from a regular online oracle?", a: "Unlike random-number generators, EverydayHoroscope's KP Oracle overlays your live Vedic dasha, planetary transits, and yogas onto your answer — so every reading carries your actual astrological fingerprint at that moment." },
  { q: "What does each verdict mean?", a: "YES (Pratibha) — move forward with confidence. WAIT (Dhairya) — pause and prepare; timing is not yet ripe. NO (Pratrodha) — the path is obstructed; reconsider. PRAY (Bhakti) — surrender and seek divine alignment before acting." },
  { q: "What is the 'Sacred Remedy' shown after a reading?", a: "Each of the 36 answers carries its own module-specific sacred remedy and behavioural practice — drawn directly from Lord Krishna's teachings and precisely matched to the chaupai and verdict received. These are optional — they support, not override, your own wisdom." },
  { q: "Can I ask any question?", a: "Yes — personal, professional, spiritual, or relational. The oracle responds to sincere intent. The more specific and clear your question, the more precise the guidance." },
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
        title="Krishna Prashnavali — Ancient Vedic Oracle by Lord Krishna"
        description="Consult the 18×18 Krishna Prashnavali — India's most sacred Vedic oracle. Get a YES, WAIT, NO, or PRAY answer from Lord Krishna, enriched with your live Dasha, planetary transits, temple remedy, and mantra."
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
          "Sarva-dharmān parityajya mām ekaṁ śaraṇaṁ vraja" — Gita 18.66
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
              { n: "1", title: "Hold your question", body: "Frame one sincere, clear question — personal, professional, or spiritual." },
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

// ─── Main export — auth-aware + premium-aware ─────────────────────────────────
export default function KrishnaOraclePage() {
  const { user, loading: authLoading } = useAuth();

  if (authLoading) return null;

  // Logged-out visitors → public landing (indexed by Google)
  if (!user) return <KrishnaOracleLanding />;

  // Logged-in but not premium → premium gate
  if (!user.is_premium) return (
    <PremiumGateCard
      feature="Krishna Prashnavali"
      description="Receive guidance from Lord Krishna's sacred oracle — an exclusive Premium feature. Upgrade to ask your question and receive a divine answer."
    />
  );

  // Premium → full oracle
  return <KrishnaOracleApp />;
}

function KrishnaOracleApp() {
  const [metadata, setMetadata] = useState(null);
  const [history, setHistory] = useState([]);
  const [loadingMeta, setLoadingMeta] = useState(true);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [questionText, setQuestionText] = useState("");
  const [focusArea, setFocusArea] = useState("guidance");
  const [revealEnabled, setRevealEnabled] = useState(true);
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [reading, setReading] = useState(null);
  const [questionError, setQuestionError] = useState("");

  const gridMatrix = metadata?.grid_matrix || [];
  const revealIndices = useMemo(() => {
    if (selectedIndex == null) return [];
    return extractChaupaiIndices(selectedIndex);
  }, [selectedIndex]);

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

  function validateQuestion(value) {
    const trimmed = value.trim();
    if (!trimmed) return "";
    if (trimmed.length < 12 || trimmed.split(/\s+/).length < 3) {
      return "Enter one clear question with at least 3 words so Krishna’s response can address it properly.";
    }
    return "";
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
      const response = await axios.post(
        `${API}/select`,
        {
          row,
          col,
          question_text: questionText.trim() || null,
          focus_area: focusArea,
          language_preference: "bilingual",
          reveal_mode: revealEnabled ? "ritual" : "instant",
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

  async function handleShare() {
    if (!reading?.report_id) return;
    try {
      const response = await axios.post(
        `${API}/share`,
        { report_id: reading.report_id },
        { withCredentials: true }
      );
      const text = response.data?.share_text || "";
      if (navigator?.clipboard?.writeText) {
        await navigator.clipboard.writeText(text);
      }
    } catch (shareError) {
      setError(shareError?.response?.data?.detail || "Unable to prepare share text.");
    }
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(217,168,74,0.18),_transparent_42%),linear-gradient(180deg,_#fffaf0_0%,_#f6ead6_52%,_#efe2cd_100%)] px-4 py-8 text-stone-900 dark:bg-[radial-gradient(circle_at_top,_rgba(180,83,9,0.18),_transparent_40%),linear-gradient(180deg,_#0a0604_0%,_#120a06_48%,_#090605_100%)] dark:text-white md:px-8">
      <SEO title="Krishna Prashnavali Oracle" noindex={true} />
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
                <label className="rounded-2xl border border-amber-200/80 bg-white/75 p-4 dark:border-amber-900/60 dark:bg-stone-950/40">
                  <span className="block text-[11px] uppercase tracking-[0.26em] text-amber-700/80 dark:text-amber-300/70">Reveal mode</span>
                  <button
                    type="button"
                    onClick={() => setRevealEnabled((current) => !current)}
                    className="mt-3 inline-flex rounded-full border border-amber-300 bg-white px-4 py-2 text-sm text-stone-900 dark:border-amber-700/60 dark:bg-[#1d120b] dark:text-amber-50"
                  >
                    {revealEnabled ? "Ritual reveal" : "Instant reveal"}
                  </button>
                  <p className="mt-3 text-sm leading-6 text-stone-600 dark:text-amber-100/70">
                    {revealEnabled
                      ? "Letters illuminate before the answer appears. The answer itself stays deterministic."
                      : "Skips the ritual animation and shows the same answer immediately."}
                  </p>
                </label>
              </div>
              <label className="block rounded-2xl border border-amber-200/80 bg-white/75 p-4 dark:border-amber-900/60 dark:bg-stone-950/40">
                <span className="block text-[11px] uppercase tracking-[0.26em] text-amber-700/80 dark:text-amber-300/70">Question</span>
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
                  rows={4}
                  placeholder="What should I understand about this situation?"
                  className="mt-3 w-full rounded-xl border border-amber-300 bg-white px-3 py-3 text-sm text-stone-900 outline-none placeholder:text-stone-400 dark:border-amber-900/60 dark:bg-[#1d120b] dark:text-amber-50 dark:placeholder:text-amber-100/30"
                />
                <p className="mt-3 text-sm leading-6 text-stone-600 dark:text-amber-100/70">
                  Ask one clear question. Your result will now include a direct Krishna response framed against what you entered.
                </p>
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

        <SectionCard title="Selection Grid" eyebrow="Deterministic Matrix">
          {loadingMeta ? (
            <p className="m-0 text-sm text-stone-600 dark:text-amber-100/75">Loading Krishna grid…</p>
          ) : (
            <KrishnaOracleGrid
              gridMatrix={gridMatrix}
              selectedIndex={selectedIndex}
              disabled={submitting}
              revealEnabled={revealEnabled}
              onSelect={handleCellSelect}
            />
          )}
        </SectionCard>

        {reading ? (
          <SectionCard title="Guidance Report" eyebrow={`Answer slot ${reading.answer_slot}`}>
            <div className="grid gap-4 xl:grid-cols-[1.2fr,0.8fr]">
              <div className="space-y-4">
                {reading.question_text ? <BilingualBlockView label="Your Question" block={{ sanskrit_block: reading.question_text, english_block: reading.focus_area ? `Focus area: ${reading.focus_area}` : "Specific question submitted" }} /> : null}
                <BilingualBlockView label="Your Chaupai" block={reading.chaupai_string} />
                <BilingualBlockView label="Krishna's Answer" block={reading.answer.krishna_answer} />
                <BilingualBlockView label="Meaning" block={reading.answer.meaning} />
                <div className="grid gap-4 md:grid-cols-2">
                  <BilingualBlockView label="What to Do" block={reading.answer.what_to_do} />
                  {reading.summary_report?.behavioral_remedy
                    ? <BilingualBlockView label="Sacred Remedy" block={reading.summary_report.behavioral_remedy} />
                    : reading.answer.remedy
                      ? <BilingualBlockView label="Remedy" block={reading.answer.remedy} />
                      : null}
                  <BilingualBlockView label="Precaution" block={reading.answer.precaution} />
                  <BilingualBlockView label="Duration" block={reading.answer.duration} />
                </div>
                {reading.answer.behavioral_remedy && (
                  <BilingualBlockView label="Sacred Practice" block={reading.answer.behavioral_remedy} />
                )}
                <div className="grid gap-4 md:grid-cols-2">
                  {(reading.summary_report?.sacred_mantra || reading.answer.mantra)
                    ? <BilingualBlockView label="Mantra" block={reading.summary_report?.sacred_mantra || reading.answer.mantra} />
                    : null}
                  <BilingualBlockView label="Krishna's Message" block={reading.answer.krishna_message} />
                </div>
              </div>

              <div className="space-y-4">
                <div className="rounded-2xl border border-amber-200/80 bg-white/75 p-4 dark:border-amber-900/60 dark:bg-stone-950/40">
                  <p className="m-0 text-[11px] uppercase tracking-[0.26em] text-amber-700/80 dark:text-amber-300/70">Verdict</p>
                  <p className="m-0 mt-3 text-3xl font-semibold text-stone-900 dark:text-amber-50">{reading.answer.verdict_display}</p>
                  <p className="m-0 mt-2 text-sm leading-7 text-stone-700 dark:text-amber-100/80">
                    {reading.answer.verdict_traditional} → {reading.answer.verdict_backend}
                  </p>
                </div>
                <SummaryBlock title="Sacred Verse" content={reading.summary_report?.sacred_verse} />
                <SummaryBlock title="Question Response" content={reading.summary_report?.question_response} />
                <SummaryBlock title="Astro-Scientific Context" content={reading.summary_report?.astro_scientific_context} />
                <SummaryBlock title="Practical Action" content={reading.summary_report?.practical_action} />
                <div className="rounded-2xl border border-amber-200/80 bg-white/75 p-4 dark:border-amber-900/60 dark:bg-stone-950/40">
                  <p className="m-0 text-[11px] uppercase tracking-[0.26em] text-amber-700/80 dark:text-amber-300/70">Sequence indices</p>
                  <p className="m-0 mt-3 text-sm leading-7 text-stone-700 dark:text-amber-100/80">{revealIndices.join(", ")}</p>
                </div>
                <button
                  type="button"
                  onClick={handleShare}
                  className="w-full rounded-xl border border-amber-500 bg-amber-500 px-4 py-3 text-sm font-semibold text-stone-950 transition hover:bg-amber-400"
                >
                  Copy share text
                </button>
              </div>
            </div>
          </SectionCard>
        ) : null}

        <SectionCard title="Recent Krishna Readings" eyebrow="History">
          {loadingHistory ? (
            <p className="m-0 text-sm text-stone-600 dark:text-amber-100/75">Loading history…</p>
          ) : history.length === 0 ? (
            <p className="m-0 text-sm text-stone-600 dark:text-amber-100/75">Your Krishna readings will appear here after the first selection.</p>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
              {history.map((item) => (
                <div key={item.id} className="rounded-2xl border border-amber-200/80 bg-white/75 p-4 dark:border-amber-900/60 dark:bg-stone-950/40">
                  <p className="m-0 text-[11px] uppercase tracking-[0.24em] text-amber-700/80 dark:text-amber-300/70">{item.verdict_display}</p>
                  <h3 className="m-0 mt-2 text-lg font-semibold text-stone-900 dark:text-amber-50">{item.summary}</h3>
                  <p className="m-0 mt-2 text-sm leading-7 text-stone-700 dark:text-amber-100/75">
                    Cell [{item.row}][{item.col}] • slot {item.answer_slot}
                  </p>
                  <p className="m-0 mt-2 text-xs text-stone-500 dark:text-amber-100/50">{formatTimestamp(item.created_at)}</p>
                </div>
              ))}
            </div>
          )}
        </SectionCard>

        {/* ── On-page SEO content ─────────────────────────────────────────── */}
        <div className="mt-12 space-y-8 border-t border-amber-200/50 pt-10 text-sm text-stone-600 dark:border-amber-900/40 dark:text-amber-100/60">
          <div>
            <h2 className="mb-2 text-base font-semibold text-stone-800 dark:text-amber-100">What is Krishna Prashnavali?</h2>
            <p className="leading-7">Krishna Prashnavali (कृष्ण प्रश्नावली) is one of the most revered Prashna oracles in the Vedic tradition. Rooted in the sacred chaupais of Srimad Bhagavad Gita and traditional Prashna Shastra, it presents 36 divine answers arranged in an 18×18 grid of 324 cells. Each cell, when selected with sincere intent, resolves to a verdict — YES (Pratibha), WAIT (Dhairya), NO (Pratrodha), or PRAY (Bhakti) — drawn directly from Lord Krishna's teachings to Arjuna.</p>
          </div>
          <div>
            <h2 className="mb-2 text-base font-semibold text-stone-800 dark:text-amber-100">How the 18×18 Grid Works</h2>
            <p className="leading-7">The oracle operates on a sacred 9-step chaupai sequence. When you select a cell, the system treats it as position 0 and advances deterministically through 9 chaupai letters using a 12-letter interval — always producing the same answer for a given grid position regardless of when it is consulted. This is not randomness; it is structured Vedic Prashna logic, where the sincerity of your question, not chance, guides your hand.</p>
          </div>
          <div>
            <h2 className="mb-2 text-base font-semibold text-stone-800 dark:text-amber-100">Understanding the Four Verdicts</h2>
            <p className="leading-7"><strong className="text-stone-800 dark:text-amber-100">YES — Pratibha:</strong> Lord Krishna signals a clear forward path. Act with confidence and discipline. <strong className="text-stone-800 dark:text-amber-100">WAIT — Dhairya:</strong> The timing is not yet aligned. Pause, prepare internally, and let circumstances mature. <strong className="text-stone-800 dark:text-amber-100">NO — Pratrodha:</strong> An obstacle is present on the current path. Reconsider your approach, not your goal. <strong className="text-stone-800 dark:text-amber-100">PRAY — Bhakti:</strong> Surrender the outcome. Seek divine alignment through devotion before any action is taken.</p>
          </div>
          <div>
            <h2 className="mb-2 text-base font-semibold text-stone-800 dark:text-amber-100">What is Prashna Shastra?</h2>
            <p className="leading-7">Prashna Shastra is the Vedic science of answering questions — an ancient branch of Jyotish (Vedic astrology) in which the moment of the question itself is cast as a horoscope. Unlike natal astrology, which requires a birth chart, Prashna works solely from the energy of the query and the moment it is posed. EverydayHoroscope layers this with your live dasha, planetary transits, and current yogas to give each reading an astrological fingerprint unique to you and the moment of asking.</p>
          </div>
          <div>
            <h2 className="mb-2 text-base font-semibold text-stone-800 dark:text-amber-100">Behavioural Remedy & Sacred Practice</h2>
            <p className="leading-7">Each of the 36 answers carries a module-specific behavioural remedy — a contemplative practice drawn from Krishna's own teachings and aligned to the verdict received. These are not generic prescriptions; they are precisely paired to the chaupai, the verdict, and the spiritual intent of Lord Krishna's answer. The remedy guides how to carry the oracle's wisdom into your daily life.</p>
          </div>
          <div>
            <h2 className="mb-2 text-base font-semibold text-stone-800 dark:text-amber-100">Using Krishna Prashnavali Effectively</h2>
            <p className="leading-7">Approach each session with one sincere, clearly framed question. Avoid repeating the same question in one session — the oracle is consulted for genuine matters, not for confirmation. Hold your question in mind as you close your eyes, breathe, and let your hand fall on a cell. Read the full answer including the sacred verse (chaupai), meaning, practical action, and behavioural remedy before forming your response. Your Historical Readings above allow you to track patterns across multiple consultations over time.</p>
          </div>
        </div>

      </div>
    </div>
  );
}
