import React, { useEffect, useMemo, useRef, useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import {
  Activity,
  BookOpen,
  Briefcase,
  Clock3,
  Compass,
  Crown,
  DollarSign,
  Flame,
  Heart,
  Home,
  Link2,
  MapPin,
  RefreshCcw,
  RefreshCw,
  ShieldOff,
  Sparkles,
  Star,
  Sunrise,
  TrendingUp,
  Users,
  Wind,
} from "lucide-react";

import { SEO } from "../../components/SEO";
import { ShareButtons } from "../../components/ShareCard";
import { useAuth } from "../../context/AuthContext";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
const API = `${BACKEND_URL}/api/oracle/krishna-prashnavali`;
const PROFILE_API = `${BACKEND_URL}/api/profile/birth`;

const FOCUS_AREAS = [
  { slug: "job_change_promotion", name: "Job Change / Promotion", icon: Briefcase, description: "Should I accept this or wait?" },
  { slug: "workplace_conflict", name: "Workplace Conflict", icon: Users, description: "How do I navigate a difficult colleague?" },
  { slug: "startup_business_risk", name: "Startup / Business Risk", icon: TrendingUp, description: "Is now the right time to launch?" },
  { slug: "leadership_decision", name: "Leadership Decision", icon: Crown, description: "What does ethical leadership look like here?" },
  { slug: "anxiety_stress", name: "Anxiety & Stress", icon: Wind, description: "I am overwhelmed -- what do I do?" },
  { slug: "grief_loss", name: "Grief & Loss", icon: Heart, description: "How do I process this loss?" },
  { slug: "anger_resentment", name: "Anger & Resentment", icon: Flame, description: "I want to react -- should I?" },
  { slug: "inner_peace", name: "Inner Peace", icon: Sunrise, description: "I need stillness -- where do I begin?" },
  { slug: "marriage_partnership", name: "Marriage & Partnership", icon: Link2, description: "Is this the right person or path?" },
  { slug: "parenting_family", name: "Parenting & Family", icon: Home, description: "How do I approach this family situation?" },
  { slug: "forgiveness", name: "Forgiveness", icon: RefreshCw, description: "Can I -- should I -- let this go?" },
  { slug: "exam_study_focus", name: "Exam / Study Focus", icon: BookOpen, description: "How do I trust the process and concentrate?" },
  { slug: "life_purpose", name: "Life Purpose", icon: Compass, description: "What is my Swadharma?" },
  { slug: "procrastination", name: "Procrastination", icon: Clock3, description: "I keep delaying -- what is Krishna's counsel?" },
  { slug: "financial_stability", name: "Financial Stability", icon: DollarSign, description: "How do I relate to this financial situation?" },
  { slug: "health_healing", name: "Health & Healing", icon: Activity, description: "How do I approach this physical challenge?" },
  { slug: "travel_relocation", name: "Travel & Relocation", icon: MapPin, description: "Is this move or journey auspicious?" },
  { slug: "toxic_relationship", name: "Toxic Relationship", icon: ShieldOff, description: "Do I stay, speak, or leave?" },
  { slug: "overcoming_habit", name: "Overcoming a Habit", icon: RefreshCcw, description: "How do I break this cycle?" },
  { slug: "daily_inspiration", name: "Daily Inspiration", icon: Star, description: "No specific question -- I seek wisdom for today." },
];

const LOADING_LINES = [
  "Reading the Bhagavad Gita...",
  "Listening to Krishna...",
  "Your answer is forming...",
];

const VERDICT_STYLES = {
  PROCEED: "border-emerald-500/30 bg-emerald-500/12 text-emerald-200",
  PAUSE: "border-sky-500/30 bg-sky-500/12 text-sky-200",
  REFLECT: "border-amber-400/30 bg-amber-400/12 text-amber-100",
  SURRENDER: "border-violet-500/30 bg-violet-500/12 text-violet-200",
};

function FocusAreaCard({ item, selected, onSelect }) {
  const Icon = item.icon;
  return (
    <button
      type="button"
      onClick={() => onSelect(item.slug)}
      className={`group rounded-[1.4rem] border p-4 text-left transition duration-200 ${
        selected
          ? "border-amber-300 bg-amber-300/10 shadow-[0_20px_40px_rgba(217,168,74,0.12)]"
          : "border-white/10 bg-white/[0.03] hover:border-amber-400/40 hover:bg-white/[0.05]"
      }`}
    >
      <div className="flex items-start gap-3">
        <div className={`flex h-11 w-11 items-center justify-center rounded-2xl border ${selected ? "border-amber-300/70 bg-amber-200/15 text-amber-100" : "border-white/10 bg-white/[0.04] text-amber-200/80"}`}>
          <Icon className="h-5 w-5" />
        </div>
        <div className="min-w-0">
          <p className="m-0 text-sm font-semibold text-white">{item.name}</p>
          <p className="m-0 mt-2 text-sm leading-6 text-white/62">{item.description}</p>
        </div>
      </div>
    </button>
  );
}

function GoldButton({ children, className = "", ...props }) {
  return (
    <button
      {...props}
      className={`inline-flex items-center justify-center rounded-full bg-[#d9a84a] px-6 py-3 text-sm font-semibold text-[#1d1207] transition hover:bg-[#e3b65d] disabled:cursor-not-allowed disabled:opacity-40 ${className}`}
    >
      {children}
    </button>
  );
}

function GhostButton({ children, className = "", ...props }) {
  return (
    <button
      {...props}
      className={`inline-flex items-center justify-center rounded-full border border-white/12 bg-white/[0.04] px-5 py-3 text-sm font-medium text-white/84 transition hover:bg-white/[0.08] disabled:cursor-not-allowed disabled:opacity-40 ${className}`}
    >
      {children}
    </button>
  );
}

function PillarCard({ eyebrow, title, children, className = "" }) {
  return (
    <section className={`rounded-[1.5rem] border border-[#d9a84a]/20 bg-[#d9a84a]/[0.04] p-5 shadow-[0_18px_50px_rgba(0,0,0,0.18)] ${className}`}>
      {eyebrow ? <p className="m-0 text-[11px] uppercase tracking-[0.28em] text-[#d9a84a]/80">{eyebrow}</p> : null}
      {title ? <h2 className="m-0 mt-2 text-xl font-semibold text-white">{title}</h2> : null}
      <div className="mt-4">{children}</div>
    </section>
  );
}

const AskQuestionShareCard = React.forwardRef(function AskQuestionShareCard({ reading }, ref) {
  if (!reading) return null;
  return (
    <div
      ref={ref}
      style={{
        width: 900,
        background: "linear-gradient(160deg, #0b0812 0%, #181224 60%, #0b0812 100%)",
        borderRadius: 24,
        padding: 52,
        color: "#f9f3e4",
        fontFamily: "Georgia, 'Times New Roman', serif",
        position: "fixed",
        left: -9999,
        top: 0,
        pointerEvents: "none",
        border: "1px solid rgba(217,168,74,0.24)",
        boxSizing: "border-box",
      }}
    >
      <p style={{ margin: 0, textTransform: "uppercase", letterSpacing: 5, fontSize: 13, color: "#d9a84a" }}>Ask Lord Krishna</p>
      <h1 style={{ margin: "12px 0 8px", fontSize: 42, lineHeight: 1.1 }}>Bhagavad Gita Guidance</h1>
      <p style={{ margin: 0, fontSize: 20, color: "rgba(249,243,228,0.78)", fontStyle: "italic" }}>{reading.focus_area_label}</p>
      <div style={{ marginTop: 28, display: "inline-block", borderRadius: 999, padding: "10px 20px", border: "1px solid rgba(217,168,74,0.28)", background: "rgba(217,168,74,0.08)", color: "#f5d189", fontWeight: 700, letterSpacing: 1.5 }}>
        {reading.verdict_label}
      </div>
      <p style={{ margin: "28px 0 0", fontSize: 16, lineHeight: 1.75, color: "rgba(249,243,228,0.72)" }}>Question</p>
      <p style={{ margin: "8px 0 0", fontSize: 24, lineHeight: 1.5 }}>{reading.question}</p>
      <p style={{ margin: "28px 0 0", fontSize: 17, lineHeight: 1.8, color: "#f5d189" }}>{reading.verse_ref}</p>
      <p style={{ margin: "12px 0 0", fontSize: 28, lineHeight: 1.7 }}>{reading.verse_sanskrit}</p>
      <p style={{ margin: "16px 0 0", fontSize: 21, lineHeight: 1.7, color: "rgba(249,243,228,0.86)", fontStyle: "italic" }}>{reading.krishna_voice}</p>
      <div style={{ marginTop: 26, paddingTop: 20, borderTop: "1px solid rgba(217,168,74,0.18)" }}>
        <p style={{ margin: 0, fontSize: 14, color: "rgba(249,243,228,0.44)" }}>everydayhoroscope.in/ask-question</p>
      </div>
    </div>
  );
});

export default function AskQuestionPage() {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [step, setStep] = useState("landing");
  const [focusArea, setFocusArea] = useState(FOCUS_AREAS[0].slug);
  const [question, setQuestion] = useState("");
  const [questionError, setQuestionError] = useState("");
  const [showAuthPrompt, setShowAuthPrompt] = useState(false);
  const [limitMessage, setLimitMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingLineIndex, setLoadingLineIndex] = useState(0);
  const [birthProfile, setBirthProfile] = useState(null);
  const [birthProfileLoading, setBirthProfileLoading] = useState(false);
  const [reading, setReading] = useState(null);
  const shareCardRef = useRef(null);

  const selectedFocus = useMemo(
    () => FOCUS_AREAS.find((item) => item.slug === focusArea) || FOCUS_AREAS[0],
    [focusArea],
  );
  const questionLength = question.trim().length;
  const isQuestionValid = questionLength >= 10 && questionLength <= 200;

  useEffect(() => {
    if (step !== "loading") return undefined;
    const timer = window.setInterval(() => {
      setLoadingLineIndex((current) => (current + 1) % LOADING_LINES.length);
    }, 1200);
    return () => window.clearInterval(timer);
  }, [step]);

  useEffect(() => {
    if (!user) {
      setBirthProfile(null);
      return;
    }
    let active = true;
    async function loadBirthProfile() {
      setBirthProfileLoading(true);
      try {
        const response = await axios.get(PROFILE_API, { withCredentials: true });
        if (!active) return;
        const profiles = Array.isArray(response.data) ? response.data : [];
        setBirthProfile(profiles[0] || null);
      } catch {
        if (!active) return;
        setBirthProfile(null);
      } finally {
        if (active) setBirthProfileLoading(false);
      }
    }
    loadBirthProfile();
    return () => {
      active = false;
    };
  }, [user]);

  function resetForAnotherQuestion() {
    setStep("focus");
    setQuestion("");
    setQuestionError("");
    setLoading(false);
    setShowAuthPrompt(false);
    setLimitMessage("");
    setReading(null);
  }

  async function handleSubmit() {
    const trimmedQuestion = question.trim();
    if (trimmedQuestion.length < 10 || trimmedQuestion.length > 200) {
      setQuestionError("Please enter a question between 10 and 200 characters.");
      return;
    }
    setQuestionError("");
    setLimitMessage("");

    if (!user) {
      setShowAuthPrompt(true);
      return;
    }

    const payload = {
      question: trimmedQuestion,
      focus_area: focusArea,
    };

    if (birthProfile?.date_of_birth && birthProfile?.time_of_birth) {
      payload.birth_date = birthProfile.date_of_birth;
      payload.birth_time = birthProfile.time_of_birth;
      payload.birth_place = birthProfile.location;
      payload.timezone_offset = birthProfile.timezone || "+05:30";
    }

    setLoading(true);
    setStep("loading");
    setLoadingLineIndex(0);

    try {
      const [response] = await Promise.all([
        axios.post(`${API}/ask`, payload, { withCredentials: true }),
        new Promise((resolve) => window.setTimeout(resolve, 1800)),
      ]);
      setReading(response.data);
      setStep("reveal");
      if (response.data.saved_to_history) {
        toast.success("Your Ask Question reading has been saved.");
      }
    } catch (error) {
      const detail = error?.response?.data?.detail || "Unable to receive Krishna's guidance right now.";
      if (error?.response?.status === 402) {
        setLimitMessage(detail);
      } else {
        toast.error(detail);
      }
      setStep("question");
    } finally {
      setLoading(false);
    }
  }

  const hero = (
    <section className="mx-auto flex min-h-[calc(100vh-5rem)] w-full max-w-6xl flex-col items-center justify-center px-4 py-16 text-center">
      <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-full border border-[#d9a84a]/25 bg-[#d9a84a]/10 shadow-[0_0_80px_rgba(217,168,74,0.18)]">
        <Sparkles className="h-9 w-9 text-[#f5d189]" />
      </div>
      <p className="m-0 text-xs uppercase tracking-[0.35em] text-[#d9a84a]/80">Bhagavad Gita Oracle</p>
      <h1 className="m-0 mt-4 max-w-3xl font-playfair text-4xl font-semibold leading-tight text-white md:text-6xl">
        Ask Lord Krishna
      </h1>
      <p className="m-0 mt-5 max-w-2xl text-lg leading-8 text-white/72">
        Type your question. Receive guidance rooted in the Bhagavad Gita, refined through Guna logic, and enriched by your live dasha context when available.
      </p>
      <div className="mt-10 flex flex-col gap-3 sm:flex-row">
        <GoldButton onClick={() => setStep("focus")}>Begin</GoldButton>
        <GhostButton onClick={() => navigate("/krishna-prashnavali")}>Open the 18×18 Grid Oracle</GhostButton>
      </div>
    </section>
  );

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(217,168,74,0.12),_transparent_45%),linear-gradient(180deg,_#0a0710_0%,_#140f1e_48%,_#09060d_100%)] text-white">
      <SEO
        title="Ask Lord Krishna -- Bhagavad Gita Oracle"
        description="Ask one natural-language question and receive a Bhagavad Gita answer, Guna classification, and live dasha context from Krishna's wisdom engine."
        url="https://www.everydayhoroscope.in/ask-question"
      />

      {authLoading ? null : (step === "landing" ? hero : null)}

      <div className="mx-auto w-full max-w-6xl px-4 pb-16">
        {step === "focus" ? (
          <section className="rounded-[2rem] border border-white/10 bg-white/[0.03] p-6 shadow-[0_26px_80px_rgba(0,0,0,0.28)] md:p-8">
            <p className="m-0 text-xs uppercase tracking-[0.32em] text-[#d9a84a]/80">Step 1</p>
            <h2 className="m-0 mt-3 text-3xl font-semibold text-white">Choose the area of your life Krishna should illuminate</h2>
            <p className="m-0 mt-3 max-w-3xl text-sm leading-7 text-white/65">Select one focus area. The question you ask next will be classified through the three Gunas before it is matched to a Bhagavad Gita answer.</p>
            <div className="mt-8 grid gap-4 sm:grid-cols-2 md:grid-cols-4">
              {FOCUS_AREAS.map((item) => (
                <FocusAreaCard key={item.slug} item={item} selected={item.slug === focusArea} onSelect={setFocusArea} />
              ))}
            </div>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-between">
              <GhostButton onClick={() => setStep("landing")} className="sm:w-auto">Back</GhostButton>
              <GoldButton onClick={() => setStep("question")} className="sm:w-auto">Next</GoldButton>
            </div>
          </section>
        ) : null}

        {step === "question" ? (
          <section className="rounded-[2rem] border border-white/10 bg-white/[0.03] p-6 shadow-[0_26px_80px_rgba(0,0,0,0.28)] md:p-8">
            <p className="m-0 text-xs uppercase tracking-[0.32em] text-[#d9a84a]/80">Step 2</p>
            <div className="mt-3 flex flex-wrap items-center gap-3">
              <h2 className="m-0 text-3xl font-semibold text-white">Type your question to Lord Krishna</h2>
              <span className="rounded-full border border-[#d9a84a]/25 bg-[#d9a84a]/10 px-4 py-1 text-xs font-semibold uppercase tracking-[0.22em] text-[#f5d189]">
                {selectedFocus.name}
              </span>
            </div>
            <p className="m-0 mt-3 max-w-3xl text-sm leading-7 text-white/65">Your question is private. Krishna hears, not the algorithm.</p>
            {user && !user.is_premium ? (
              <p className="m-0 mt-4 text-sm text-[#f5d189]">Free logged-in seekers receive 2 Ask Question readings per month. Premium seekers receive unlimited readings.</p>
            ) : null}
            {user && birthProfile ? (
              <p className="m-0 mt-2 text-sm text-[#f5d189]">Your cosmic context (Mahadasha) will be included automatically ✦</p>
            ) : null}
            {user && birthProfileLoading ? (
              <p className="m-0 mt-2 text-sm text-white/55">Checking your saved birth profile...</p>
            ) : null}
            <textarea
              value={question}
              onChange={(event) => {
                setQuestion(event.target.value.slice(0, 200));
                setQuestionError("");
                setShowAuthPrompt(false);
                setLimitMessage("");
              }}
              placeholder="Type your question to Lord Krishna..."
              className="mt-6 min-h-[180px] w-full rounded-[1.5rem] border border-white/10 bg-[#09070f]/85 px-5 py-4 text-base leading-8 text-white outline-none transition placeholder:text-white/35 focus:border-[#d9a84a]/55"
            />
            <div className="mt-3 flex flex-wrap items-center justify-between gap-3 text-sm text-white/58">
              <span>{questionLength < 10 ? `${10 - questionLength} more characters to begin` : `${questionLength}/200 characters`}</span>
              {questionError ? <span className="text-rose-300">{questionError}</span> : null}
            </div>

            {showAuthPrompt ? (
              <div className="mt-6 rounded-[1.4rem] border border-[#d9a84a]/25 bg-[#d9a84a]/10 p-5">
                <p className="m-0 text-sm font-semibold uppercase tracking-[0.24em] text-[#f5d189]">Sign in to receive your answer</p>
                <p className="m-0 mt-3 text-sm leading-7 text-white/75">You can explore the categories freely, but Krishna's personalised response unlocks after you sign in so we can save your reading and protect your monthly quota.</p>
                <div className="mt-5 flex flex-col gap-3 sm:flex-row">
                  <GoldButton onClick={() => navigate("/login")}>Sign In</GoldButton>
                  <GhostButton onClick={() => navigate("/register")}>Create Account</GhostButton>
                </div>
              </div>
            ) : null}

            {limitMessage ? (
              <div className="mt-6 rounded-[1.4rem] border border-rose-400/20 bg-rose-400/10 p-5">
                <p className="m-0 text-sm font-semibold uppercase tracking-[0.24em] text-rose-200">Free limit reached</p>
                <p className="m-0 mt-3 text-sm leading-7 text-white/75">{limitMessage}</p>
                <div className="mt-5">
                  <GoldButton onClick={() => navigate("/pricing")}>Upgrade to Premium</GoldButton>
                </div>
              </div>
            ) : null}

            <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-between">
              <GhostButton onClick={() => setStep("focus")}>Back</GhostButton>
              <GoldButton onClick={handleSubmit} disabled={!isQuestionValid || loading}>Submit</GoldButton>
            </div>
          </section>
        ) : null}

        {step === "loading" ? (
          <section className="flex min-h-[55vh] flex-col items-center justify-center rounded-[2rem] border border-white/10 bg-black/35 px-6 py-10 text-center shadow-[0_26px_80px_rgba(0,0,0,0.32)]">
            <div className="relative flex h-40 w-40 items-center justify-center">
              <div className="absolute h-28 w-28 rounded-full bg-[#fff5dc]/70 blur-2xl animate-pulse" />
              <div className="absolute h-20 w-20 rounded-full border border-[#f7dd9b]/40 bg-[#f7dd9b]/10" />
              <Sparkles className="relative z-10 h-10 w-10 text-[#f7dd9b]" />
            </div>
            <p className="m-0 mt-10 text-xs uppercase tracking-[0.35em] text-[#d9a84a]/80">Consultation in Progress</p>
            <h2 className="m-0 mt-4 text-3xl font-semibold text-white">{LOADING_LINES[loadingLineIndex]}</h2>
            <p className="m-0 mt-4 max-w-xl text-sm leading-7 text-white/62">The question is being routed through the three Gunas, matched to a Bhagavad Gita verse, and read through your available cosmic context.</p>
          </section>
        ) : null}

        {step === "reveal" && reading ? (
          <section className="space-y-6">
            <PillarCard eyebrow="The Verse" className="animate-[fadeIn_0.5s_ease]">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <span className={`inline-flex rounded-full border px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em] ${VERDICT_STYLES[reading.verdict_label] || VERDICT_STYLES.REFLECT}`}>
                    Krishna's guidance: {reading.verdict_label}
                  </span>
                  <p className="m-0 mt-5 text-xs uppercase tracking-[0.26em] text-[#d9a84a]/70">{reading.verse_ref}</p>
                </div>
                {!user?.is_premium && typeof reading.remaining_free_readings === "number" ? (
                  <p className="m-0 text-sm text-white/60">Free readings left this month: <span className="font-semibold text-[#f5d189]">{reading.remaining_free_readings}</span></p>
                ) : null}
              </div>
              <p className="m-0 mt-6 text-center font-cinzel text-2xl leading-[2.1] text-[#f5d189] md:text-3xl">{reading.verse_sanskrit}</p>
              <p className="m-0 mt-4 text-center font-playfair text-lg italic leading-8 text-white/82">{reading.verse_english}</p>
              <div className="mx-auto mt-8 max-w-3xl rounded-[1.3rem] border border-white/10 bg-black/20 p-5 text-center">
                <p className="m-0 text-xs uppercase tracking-[0.26em] text-[#d9a84a]/70">Krishna's voice</p>
                <p className="m-0 mt-3 text-base leading-8 text-white/86">{reading.krishna_voice}</p>
              </div>
            </PillarCard>

            <div className="grid gap-6 md:grid-cols-[0.95fr,1.05fr]">
              <PillarCard eyebrow="Cosmic Context" title="Your Cosmic Context" className="animate-[fadeIn_0.5s_ease_0.15s_both]">
                {reading.birth_data_present ? (
                  <>
                    <p className="m-0 rounded-2xl border border-[#d9a84a]/20 bg-[#d9a84a]/10 px-4 py-3 text-sm font-medium text-[#f5d189]">
                      You are in {reading.current_mahadasha}{reading.current_antardasha ? ` · ${reading.current_antardasha}` : ""}
                    </p>
                    <p className="m-0 mt-4 text-sm leading-7 text-white/76">{reading.astro_context || "Your dasha adds timing and emotional context to this Bhagavad Gita answer."}</p>
                    <div className="mt-5 rounded-[1.2rem] border border-white/10 bg-black/18 p-4">
                      <p className="m-0 text-xs uppercase tracking-[0.22em] text-[#d9a84a]/70">What this means for you</p>
                      <p className="m-0 mt-3 text-sm leading-7 text-white/78">{reading.guna} is the emotional-spiritual state Krishna sees beneath your question. Let the answer be read through that inner state rather than just the outer event.</p>
                    </div>
                  </>
                ) : (
                  <div className="rounded-[1.4rem] border border-[#d9a84a]/25 bg-[#d9a84a]/10 p-5">
                    <p className="m-0 text-sm font-semibold uppercase tracking-[0.24em] text-[#f5d189]">Unlock your cosmic layer</p>
                    <p className="m-0 mt-3 text-sm leading-7 text-white/74">Add your birth details to unlock your personal Mahadasha and Antardasha context for future Ask Question readings.</p>
                    <div className="mt-5">
                      <Link to="/birth-chart" className="inline-flex items-center rounded-full border border-[#d9a84a]/30 bg-black/20 px-5 py-3 text-sm font-semibold text-[#f5d189] transition hover:bg-black/35">
                        Add Birth Details
                      </Link>
                    </div>
                  </div>
                )}
              </PillarCard>

              <PillarCard eyebrow="Practical Action" title="Your Path Forward" className="animate-[fadeIn_0.5s_ease_0.25s_both]">
                <div className="space-y-4">
                  <div className="rounded-[1.2rem] border border-white/10 bg-black/18 p-4">
                    <p className="m-0 text-xs uppercase tracking-[0.22em] text-[#d9a84a]/70">What to do</p>
                    <p className="m-0 mt-3 text-sm leading-7 text-white/82">{reading.what_to_do}</p>
                  </div>
                  <div className="rounded-[1.2rem] border border-white/10 bg-black/18 p-4">
                    <p className="m-0 text-xs uppercase tracking-[0.22em] text-[#d9a84a]/70">Inner shift</p>
                    <p className="m-0 mt-3 text-sm leading-7 text-white/82">{reading.inner_shift}</p>
                  </div>
                  <div className="rounded-[1.2rem] border border-white/10 bg-black/18 p-4">
                    <p className="m-0 text-xs uppercase tracking-[0.22em] text-[#d9a84a]/70">Timeframe</p>
                    <p className="m-0 mt-3 text-sm leading-7 text-white/82">{reading.timeframe}</p>
                  </div>
                </div>
              </PillarCard>
            </div>

            <div className="rounded-[1.6rem] border border-white/10 bg-white/[0.03] p-5">
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div>
                  <p className="m-0 text-xs uppercase tracking-[0.26em] text-[#d9a84a]/80">Question asked</p>
                  <p className="m-0 mt-3 max-w-3xl text-base leading-8 text-white/84">{reading.question}</p>
                </div>
                <div className="flex flex-wrap gap-3">
                  <GhostButton onClick={() => {
                    if (reading.saved_to_history) {
                      toast.success("This reading is already saved to your Ask Question history.");
                    } else {
                      toast.info("Sign in to save future Ask Question readings.");
                    }
                  }}>Save to History</GhostButton>
                  <GoldButton onClick={resetForAnotherQuestion}>Ask Again</GoldButton>
                </div>
              </div>
              <div className="mt-6 grid gap-4 md:grid-cols-[1fr,auto] md:items-start">
                <ShareButtons
                  pageUrl={`${window.location.origin}/ask-question`}
                  shareText={`${reading.krishna_voice}\n\n${reading.what_to_do}`}
                  cardRef={shareCardRef}
                  filename={`ask-question-${reading.reading_id}`}
                  visibleButtons={["whatsapp", "facebook", "save", "copy"]}
                />
                <div className="hidden text-right text-xs uppercase tracking-[0.24em] text-white/38 md:block">
                  {reading.guna} · {reading.logic_tag}
                </div>
              </div>
              <AskQuestionShareCard ref={shareCardRef} reading={reading} />
            </div>
          </section>
        ) : null}
      </div>
    </div>
  );
}

