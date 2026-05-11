import React, { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

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

export default function KrishnaOraclePage() {
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
                  {reading.summary_report?.ritual_remedy
                    ? <BilingualBlockView label="Temple Remedy" block={reading.summary_report.ritual_remedy} />
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
                  {reading.summary_report?.ritual_mantra
                    ? <BilingualBlockView label="Mantra" block={reading.summary_report.ritual_mantra} />
                    : reading.answer.mantra
                      ? <BilingualBlockView label="Mantra" block={reading.answer.mantra} />
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
      </div>
    </div>
  );
}
