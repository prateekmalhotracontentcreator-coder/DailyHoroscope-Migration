import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";

// Host app wiring:
// <Route path="/lumina" element={<LuminaPage />} />
// { label: 'Lumina', icon: BookMarked, path: '/lumina' }

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
const API = `${BACKEND_URL}/api/lumina`;

const SCRIPTURE_MODES = ["BIBLE", "GITA"];
const TABS = [
  { id: "home", label: "Home" },
  { id: "bible", label: "Bible" },
  { id: "manifest", label: "Manifest" },
  { id: "spiritual", label: "Spiritual" },
  { id: "journal", label: "Journal" },
  { id: "chat", label: "Chat" },
];

const BIBLE_BOOKS = [
  { name: "Genesis", chapters: 50 }, { name: "Exodus", chapters: 40 }, { name: "Leviticus", chapters: 27 }, { name: "Numbers", chapters: 36 },
  { name: "Deuteronomy", chapters: 34 }, { name: "Joshua", chapters: 24 }, { name: "Judges", chapters: 21 }, { name: "Ruth", chapters: 4 },
  { name: "1 Samuel", chapters: 31 }, { name: "2 Samuel", chapters: 24 }, { name: "1 Kings", chapters: 22 }, { name: "2 Kings", chapters: 25 },
  { name: "1 Chronicles", chapters: 29 }, { name: "2 Chronicles", chapters: 36 }, { name: "Ezra", chapters: 10 }, { name: "Nehemiah", chapters: 13 },
  { name: "Esther", chapters: 10 }, { name: "Job", chapters: 42 }, { name: "Psalms", chapters: 150 }, { name: "Proverbs", chapters: 31 },
  { name: "Ecclesiastes", chapters: 12 }, { name: "Song of Solomon", chapters: 8 }, { name: "Isaiah", chapters: 66 }, { name: "Jeremiah", chapters: 52 },
  { name: "Lamentations", chapters: 5 }, { name: "Ezekiel", chapters: 48 }, { name: "Daniel", chapters: 12 }, { name: "Hosea", chapters: 14 },
  { name: "Joel", chapters: 3 }, { name: "Amos", chapters: 9 }, { name: "Obadiah", chapters: 1 }, { name: "Jonah", chapters: 4 },
  { name: "Micah", chapters: 7 }, { name: "Nahum", chapters: 3 }, { name: "Habakkuk", chapters: 3 }, { name: "Zephaniah", chapters: 3 },
  { name: "Haggai", chapters: 2 }, { name: "Zechariah", chapters: 14 }, { name: "Malachi", chapters: 4 }, { name: "Matthew", chapters: 28 },
  { name: "Mark", chapters: 16 }, { name: "Luke", chapters: 24 }, { name: "John", chapters: 21 }, { name: "Acts", chapters: 28 },
  { name: "Romans", chapters: 16 }, { name: "1 Corinthians", chapters: 16 }, { name: "2 Corinthians", chapters: 13 }, { name: "Galatians", chapters: 6 },
  { name: "Ephesians", chapters: 6 }, { name: "Philippians", chapters: 4 }, { name: "Colossians", chapters: 4 }, { name: "1 Thessalonians", chapters: 5 },
  { name: "2 Thessalonians", chapters: 3 }, { name: "1 Timothy", chapters: 6 }, { name: "2 Timothy", chapters: 4 }, { name: "Titus", chapters: 3 },
  { name: "Philemon", chapters: 1 }, { name: "Hebrews", chapters: 13 }, { name: "James", chapters: 5 }, { name: "1 Peter", chapters: 5 },
  { name: "2 Peter", chapters: 3 }, { name: "1 John", chapters: 5 }, { name: "2 John", chapters: 1 }, { name: "3 John", chapters: 1 },
  { name: "Jude", chapters: 1 }, { name: "Revelation", chapters: 22 },
];

const GITA_BOOKS = [{ name: "Bhagavad Gita", chapters: 18 }];
const VERSIONS = {
  BIBLE: ["KJV", "NIV", "ESV", "NASB"],
  GITA: ["Sivananda", "Prabhupada", "Gita Press"],
};

const CONFESSION_CATEGORIES = [
  "Physical Healing",
  "Marketplace Success",
  "Mental Peace",
  "Spiritual Authority",
];

const initialChat = [
  {
    role: "assistant",
    text: "Walk in the Divine Light. Share what is on your heart, and I’ll respond with scripture-grounded guidance.",
    sources: [],
  },
];

function fieldError(error, fallback) {
  return error?.response?.data?.detail || fallback;
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
  } catch (error) {
    return "Just now";
  }
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function SectionTitle({ eyebrow, title, copy, badge }) {
  return (
    <div className="lumina-animate space-y-3">
      <div className="flex flex-wrap items-center gap-3">
        <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/80">{eyebrow}</p>
        {badge ? <span className="rounded-full border border-amber-400/30 bg-amber-400/10 px-3 py-1 text-[10px] uppercase tracking-[0.25em] text-amber-300">{badge}</span> : null}
      </div>
      <h2 className="m-0 font-serif text-3xl italic text-white md:text-5xl">{title}</h2>
      {copy ? <p className="m-0 max-w-3xl text-sm leading-7 text-white/65 md:text-base">{copy}</p> : null}
    </div>
  );
}

function GlassCard({ className = "", children }) {
  return <div className={`rounded-[40px] border border-white/10 bg-white/5 backdrop-blur-xl shadow-[0_24px_80px_rgba(0,0,0,0.28)] ${className}`}>{children}</div>;
}

function PremiumUpsellCard() {
  return (
    <GlassCard className="lumina-animate p-7 md:p-9">
      <div className="grid gap-6 md:grid-cols-[90px,1fr] md:items-center">
        <div className="flex h-[90px] w-[90px] items-center justify-center rounded-full border border-amber-400/30 bg-amber-400/10 text-4xl text-amber-300">
          ✦
        </div>
        <div className="space-y-4">
          <div>
            <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Premium Spiritual Guide</p>
            <h3 className="m-0 mt-2 font-serif text-2xl italic text-white">Unlock deeper meditations and audio prayers.</h3>
          </div>
          <p className="m-0 max-w-2xl text-sm leading-7 text-white/65">
            Premium unlocks personalised audio prayers, priority chaplain access, multi-voice meditations, and deeper scripture dives without blocking the rest of Lumina.
          </p>
          <div className="flex flex-wrap items-center gap-3">
            <span className="rounded-full border border-white/10 bg-black/20 px-4 py-2 text-sm text-white/80">$4.99/mo</span>
            <button type="button" className="rounded-full bg-amber-500 px-5 py-3 text-sm font-semibold text-[#18171b] transition hover:bg-amber-400">
              Subscribe for $4.99/mo
            </button>
          </div>
        </div>
      </div>
    </GlassCard>
  );
}

function LuminaPage() {
  const [activeTab, setActiveTab] = useState("home");
  const [scriptureMode, setScriptureMode] = useState(() => localStorage.getItem("lumina_scripture_mode") || "BIBLE");
  const [profile, setProfile] = useState(() => ({
    userName: localStorage.getItem("lumina_user_name") || "",
    userEmail: localStorage.getItem("lumina_user_email") || "",
  }));

  const [dailyVerse, setDailyVerse] = useState(null);
  const [dailyLoading, setDailyLoading] = useState(true);
  const [dailyError, setDailyError] = useState("");

  const [scriptureBook, setScriptureBook] = useState("John");
  const [scriptureChapter, setScriptureChapter] = useState(1);
  const [scriptureVersion, setScriptureVersion] = useState("KJV");
  const [scriptureContent, setScriptureContent] = useState([]);
  const [scriptureLoading, setScriptureLoading] = useState(false);
  const [scriptureError, setScriptureError] = useState("");

  const [manifestation, setManifestation] = useState({ days: [], completed_days: [] });
  const [manifestLoading, setManifestLoading] = useState(false);
  const [manifestError, setManifestError] = useState("");
  const [selectedDay, setSelectedDay] = useState(1);

  const [kingdomGoal, setKingdomGoal] = useState("");
  const [kingdomVision, setKingdomVision] = useState(null);
  const [kingdomLoading, setKingdomLoading] = useState(false);

  const [prayerForm, setPrayerForm] = useState({ title: "", petition_seed: "", content: "" });
  const [prayers, setPrayers] = useState([]);
  const [prayerLoading, setPrayerLoading] = useState(false);
  const [prayerError, setPrayerError] = useState("");
  const [expandedPrayer, setExpandedPrayer] = useState("");

  const [confessionCategory, setConfessionCategory] = useState(CONFESSION_CATEGORIES[0]);
  const [confessionText, setConfessionText] = useState("");
  const [confessionLoading, setConfessionLoading] = useState(false);

  const [scrolls, setScrolls] = useState([]);
  const [scrollLoading, setScrollLoading] = useState(false);
  const [scrollError, setScrollError] = useState("");

  const [situationText, setSituationText] = useState("");
  const [situationResult, setSituationResult] = useState(null);
  const [situationLoading, setSituationLoading] = useState(false);

  const [chatMessages, setChatMessages] = useState(initialChat);
  const [chatInput, setChatInput] = useState("");
  const [chatImage, setChatImage] = useState(null);
  const [chatLoading, setChatLoading] = useState(false);

  const activeBooks = scriptureMode === "GITA" ? GITA_BOOKS : BIBLE_BOOKS;
  const activeBookMeta = activeBooks.find((book) => book.name === scriptureBook) || activeBooks[0];
  const totalChapters = activeBookMeta?.chapters || 1;
  const selectedManifest = manifestation.days.find((day) => day.day === selectedDay) || manifestation.days[0];
  const credits = useMemo(
    () => 750 + manifestation.completed_days.length * 25 + prayers.filter((prayer) => prayer.is_realized).length * 50,
    [manifestation.completed_days.length, prayers]
  );

  useEffect(() => {
    document.title = "Lumina | EverydayHoroscope";
  }, []);

  useEffect(() => {
    localStorage.setItem("lumina_scripture_mode", scriptureMode);
  }, [scriptureMode]);

  useEffect(() => {
    localStorage.setItem("lumina_user_name", profile.userName);
    localStorage.setItem("lumina_user_email", profile.userEmail);
  }, [profile]);

  useEffect(() => {
    if (scriptureMode === "GITA") {
      setScriptureBook("Bhagavad Gita");
      setScriptureVersion(VERSIONS.GITA[0]);
      setScriptureChapter((current) => Math.min(current, 18));
      return;
    }
    setScriptureBook((current) => (current === "Bhagavad Gita" ? "John" : current));
    setScriptureVersion((current) => (VERSIONS.BIBLE.includes(current) ? current : VERSIONS.BIBLE[0]));
  }, [scriptureMode]);

  useEffect(() => {
    let active = true;
    async function loadDailyVerse() {
      setDailyLoading(true);
      setDailyError("");
      try {
        const response = await axios.get(`${API}/daily-verse`, {
          params: { scripture_mode: scriptureMode },
          withCredentials: true,
        });
        if (!active) return;
        setDailyVerse(response.data);
      } catch (error) {
        if (!active) return;
        setDailyError(fieldError(error, "Unable to open today’s revelation."));
      } finally {
        if (active) setDailyLoading(false);
      }
    }
    loadDailyVerse();
    return () => {
      active = false;
    };
  }, [scriptureMode]);

  useEffect(() => {
    let active = true;
    async function loadScripture() {
      setScriptureLoading(true);
      setScriptureError("");
      try {
        const response = await axios.get(`${API}/scripture`, {
          params: {
            book: scriptureBook,
            chapter: scriptureChapter,
            version: scriptureVersion,
            scripture_mode: scriptureMode,
          },
          withCredentials: true,
        });
        if (!active) return;
        setScriptureContent(response.data?.paragraphs || []);
      } catch (error) {
        if (!active) return;
        setScriptureError(fieldError(error, "Unable to retrieve the scripture scroll right now."));
      } finally {
        if (active) setScriptureLoading(false);
      }
    }
    loadScripture();
    return () => {
      active = false;
    };
  }, [scriptureBook, scriptureChapter, scriptureVersion, scriptureMode]);

  useEffect(() => {
    if (!profile.userEmail) {
      setManifestation((current) => ({ ...current, completed_days: [] }));
      return;
    }
    let active = true;
    async function loadManifestation() {
      setManifestLoading(true);
      setManifestError("");
      try {
        const response = await axios.get(`${API}/manifestation`, {
          params: { user_email: profile.userEmail },
          withCredentials: true,
        });
        if (!active) return;
        const payload = response.data || { days: [], completed_days: [] };
        setManifestation(payload);
        const firstIncomplete = (payload.days || []).find((day) => !(payload.completed_days || []).includes(day.day));
        setSelectedDay(firstIncomplete?.day || payload.days?.[0]?.day || 1);
      } catch (error) {
        if (!active) return;
        setManifestError(fieldError(error, "Unable to sync your 21-day manifestation journey."));
      } finally {
        if (active) setManifestLoading(false);
      }
    }
    loadManifestation();
    return () => {
      active = false;
    };
  }, [profile.userEmail]);

  useEffect(() => {
    if (!profile.userEmail) {
      setPrayers([]);
      return;
    }
    let active = true;
    async function loadPrayers() {
      setPrayerLoading(true);
      setPrayerError("");
      try {
        const response = await axios.get(`${API}/prayers`, {
          params: { user_email: profile.userEmail },
          withCredentials: true,
        });
        if (!active) return;
        setPrayers(response.data || []);
      } catch (error) {
        if (!active) return;
        setPrayerError(fieldError(error, "Unable to load your declarations."));
      } finally {
        if (active) setPrayerLoading(false);
      }
    }
    loadPrayers();
    return () => {
      active = false;
    };
  }, [profile.userEmail]);

  useEffect(() => {
    if (!profile.userName) {
      setScrolls([]);
      return;
    }
    let active = true;
    async function loadScrolls() {
      setScrollLoading(true);
      setScrollError("");
      try {
        const response = await axios.get(`${API}/glory-scrolls`, {
          params: { user_name: profile.userName, scripture_mode: scriptureMode },
          withCredentials: true,
        });
        if (!active) return;
        setScrolls(response.data || []);
      } catch (error) {
        if (!active) return;
        setScrollError(fieldError(error, "Unable to retrieve your glory scrolls."));
      } finally {
        if (active) setScrollLoading(false);
      }
    }
    loadScrolls();
    return () => {
      active = false;
    };
  }, [profile.userName, scriptureMode]);

  async function refreshPrayers() {
    if (!profile.userEmail) return;
    const response = await axios.get(`${API}/prayers`, {
      params: { user_email: profile.userEmail },
      withCredentials: true,
    });
    setPrayers(response.data || []);
  }

  async function handlePrayerSubmit(isAiComposed) {
    if (!profile.userEmail) {
      setPrayerError("Add your email in the sanctuary profile so declarations can be saved.");
      return;
    }
    if (!prayerForm.petition_seed.trim()) {
      setPrayerError("Enter your petition or manifestation intent first.");
      return;
    }
    setPrayerLoading(true);
    setPrayerError("");
    try {
      await axios.post(
        `${API}/prayers`,
        {
          user_email: profile.userEmail,
          title: prayerForm.title,
          petition_seed: prayerForm.petition_seed,
          content: isAiComposed ? "" : prayerForm.content || prayerForm.petition_seed,
          is_ai_composed: isAiComposed,
          scripture_mode: scriptureMode,
        },
        { withCredentials: true }
      );
      setPrayerForm({ title: "", petition_seed: "", content: "" });
      await refreshPrayers();
    } catch (error) {
      setPrayerError(fieldError(error, "Unable to save your declaration."));
    } finally {
      setPrayerLoading(false);
    }
  }

  async function handlePrayerAction(prayerId, action) {
    try {
      await axios.patch(`${API}/prayers/${prayerId}`, { action }, { withCredentials: true });
      await refreshPrayers();
    } catch (error) {
      setPrayerError(fieldError(error, "Unable to update that declaration."));
    }
  }

  async function handleManifestDayComplete(day) {
    if (!profile.userEmail) {
      setManifestError("Add your email in the sanctuary profile so progress can sync.");
      return;
    }
    try {
      const response = await axios.post(`${API}/manifestation/${day}`, null, {
        params: { user_email: profile.userEmail },
        withCredentials: true,
      });
      setManifestation((current) => ({ ...current, completed_days: response.data?.completed_days || current.completed_days }));
    } catch (error) {
      setManifestError(fieldError(error, "Unable to mark this manifestation day complete."));
    }
  }

  async function handleKingdomVision() {
    if (!kingdomGoal.trim()) return;
    setKingdomLoading(true);
    try {
      const response = await axios.post(
        `${API}/kingdom-vision`,
        {
          goal: kingdomGoal,
          user_name: profile.userName || "Lumina Seeker",
        },
        { withCredentials: true }
      );
      setKingdomVision(response.data);
    } catch (error) {
      setManifestError(fieldError(error, "Unable to scribe your kingdom mandate."));
    } finally {
      setKingdomLoading(false);
    }
  }

  async function handleConfession() {
    setConfessionLoading(true);
    try {
      const response = await axios.post(
        `${API}/confessions`,
        {
          category: confessionCategory,
          user_name: profile.userName || "Lumina Seeker",
          scripture_mode: scriptureMode,
        },
        { withCredentials: true }
      );
      setConfessionText(response.data?.text || "");
    } catch (error) {
      setPrayerError(fieldError(error, "Unable to generate your confession."));
    } finally {
      setConfessionLoading(false);
    }
  }

  async function handleSituationSearch() {
    if (!situationText.trim()) return;
    setSituationLoading(true);
    try {
      const response = await axios.post(
        `${API}/situation`,
        {
          situation: situationText,
          scripture_mode: scriptureMode,
        },
        { withCredentials: true }
      );
      setSituationResult(response.data);
    } catch (error) {
      setScrollError(fieldError(error, "Unable to discern this situation right now."));
    } finally {
      setSituationLoading(false);
    }
  }

  async function handleChatImageChange(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    const data = await fileToBase64(file);
    setChatImage(data);
  }

  async function handleSendChat() {
    if ((!chatInput.trim() && !chatImage) || chatLoading) return;
    const userText = chatInput.trim() || "Please reflect on this image spiritually.";
    const nextUserMessage = {
      role: "user",
      text: userText,
      image: chatImage,
      sources: [],
    };
    setChatMessages((current) => [...current, nextUserMessage]);
    setChatInput("");
    setChatLoading(true);
    try {
      const response = await axios.post(
        `${API}/chaplain`,
        {
          question: userText,
          image_base64: chatImage,
          scripture_mode: scriptureMode,
        },
        { withCredentials: true }
      );
      setChatMessages((current) => [...current, { role: "assistant", text: response.data?.text || "", sources: response.data?.sources || [] }]);
      setChatImage(null);
    } catch (error) {
      setChatMessages((current) => [
        ...current,
        {
          role: "assistant",
          text: fieldError(error, "The chaplain is quiet for a moment. Try again shortly."),
          sources: [],
        },
      ]);
    } finally {
      setChatLoading(false);
    }
  }

  function renderHome() {
    if (dailyLoading) {
      return <GlassCard className="lumina-animate p-10 text-center text-white/60">Opening today’s verse...</GlassCard>;
    }
    if (dailyError) {
      return <GlassCard className="lumina-animate p-10 text-center text-amber-300">{dailyError}</GlassCard>;
    }
    if (!dailyVerse) return null;
    return (
      <div className="space-y-6">
        <GlassCard className="lumina-animate overflow-hidden p-8 md:p-12">
          <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Daily Verse</p>
          <blockquote className="m-0 mt-6 font-serif text-3xl italic leading-tight text-white md:text-5xl">
            “{dailyVerse.verse_text}”
          </blockquote>
          <p className="m-0 mt-5 text-sm uppercase tracking-[0.35em] text-amber-400">{dailyVerse.verse_reference}</p>
          <div className="mt-8 rounded-[32px] border border-white/10 bg-black/20 p-6">
            <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Revelation Context</p>
            <p className="m-0 mt-4 text-base leading-8 text-white/75">{dailyVerse.revelation_context}</p>
          </div>
        </GlassCard>

        <div className="grid gap-4 md:grid-cols-3">
          {[
            { label: "Speak It", value: dailyVerse.speak_it },
            { label: "Think It", value: dailyVerse.think_it },
            { label: "Do It", value: dailyVerse.do_it },
          ].map((item) => (
            <GlassCard key={item.label} className="lumina-animate p-6">
              <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">{item.label}</p>
              <p className="m-0 mt-4 text-base leading-8 text-white/75">{item.value}</p>
            </GlassCard>
          ))}
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <GlassCard className="lumina-animate p-6">
            <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">The Prophet&apos;s Promise</p>
            <p className="m-0 mt-4 text-base leading-8 text-white/75">{dailyVerse.prophets_promise}</p>
          </GlassCard>
          <GlassCard className="lumina-animate p-6">
            <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Daily Application</p>
            <p className="m-0 mt-4 text-base leading-8 text-white/75">{dailyVerse.daily_application}</p>
          </GlassCard>
        </div>
      </div>
    );
  }

  function renderBible() {
    return (
      <div className="space-y-6">
        <GlassCard className="lumina-animate p-6 md:p-8">
          <div className="grid gap-4 md:grid-cols-3">
            <label className="space-y-2 text-sm text-white/70">
              <span className="block text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Book</span>
              <select
                value={scriptureBook}
                onChange={(event) => {
                  setScriptureBook(event.target.value);
                  setScriptureChapter(1);
                }}
                className="w-full rounded-[24px] border border-white/10 bg-black/30 px-4 py-4 text-white outline-none transition focus:border-amber-400/50"
              >
                {activeBooks.map((book) => (
                  <option key={book.name} value={book.name}>
                    {book.name}
                  </option>
                ))}
              </select>
            </label>
            <label className="space-y-2 text-sm text-white/70">
              <span className="block text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Chapter</span>
              <select
                value={scriptureChapter}
                onChange={(event) => setScriptureChapter(Number(event.target.value))}
                className="w-full rounded-[24px] border border-white/10 bg-black/30 px-4 py-4 text-white outline-none transition focus:border-amber-400/50"
              >
                {Array.from({ length: totalChapters }, (_, index) => index + 1).map((chapter) => (
                  <option key={chapter} value={chapter}>
                    Chapter {chapter}
                  </option>
                ))}
              </select>
            </label>
            <label className="space-y-2 text-sm text-white/70">
              <span className="block text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Version</span>
              <select
                value={scriptureVersion}
                onChange={(event) => setScriptureVersion(event.target.value)}
                className="w-full rounded-[24px] border border-white/10 bg-black/30 px-4 py-4 text-white outline-none transition focus:border-amber-400/50"
              >
                {VERSIONS[scriptureMode].map((version) => (
                  <option key={version} value={version}>
                    {version}
                  </option>
                ))}
              </select>
            </label>
          </div>
        </GlassCard>

        {scriptureLoading ? <GlassCard className="lumina-animate p-8 text-center text-white/60">Unsealing the chapter...</GlassCard> : null}
        {scriptureError ? <GlassCard className="lumina-animate p-8 text-center text-amber-300">{scriptureError}</GlassCard> : null}

        {!scriptureLoading && !scriptureError
          ? scriptureContent.map((paragraph, index) => (
              <GlassCard key={`${index}-${paragraph.interpretation}`} className="lumina-animate p-6 md:p-8">
                <div className="space-y-5">
                  <div className="space-y-4">
                    {paragraph.verses.map((verse) => (
                      <p key={verse.ref} className="m-0 font-serif text-lg italic leading-8 text-white/90 md:text-2xl">
                        <span className="mr-2 text-sm not-italic uppercase tracking-[0.2em] text-amber-400">{verse.ref}</span>
                        {verse.text}
                      </p>
                    ))}
                  </div>
                  <div className="rounded-[28px] border border-white/10 bg-black/20 p-5">
                    <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Interpretation</p>
                    <p className="m-0 mt-4 text-base leading-8 text-white/72">{paragraph.interpretation}</p>
                  </div>
                </div>
              </GlassCard>
            ))
          : null}
      </div>
    );
  }

  function renderManifest() {
    return (
      <div className="space-y-6">
        <GlassCard className="lumina-animate p-6 md:p-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">21-Day Manifestation</p>
              <p className="m-0 mt-3 text-sm leading-7 text-white/65">Select a day, read the prompt, and mark it complete as you move through the cycle.</p>
            </div>
            <span className="rounded-full border border-amber-400/30 bg-amber-400/10 px-4 py-2 text-[10px] uppercase tracking-[0.25em] text-amber-300">Premium</span>
          </div>
          <div className="mt-6 grid grid-cols-7 gap-3">
            {(manifestation.days || []).map((day) => {
              const isComplete = manifestation.completed_days.includes(day.day);
              const isCurrent = selectedDay === day.day;
              return (
                <button
                  key={day.day}
                  type="button"
                  onClick={() => setSelectedDay(day.day)}
                  className={`relative aspect-square rounded-full border text-sm transition ${
                    isComplete ? "border-amber-400 bg-amber-500 text-[#18171b]" : "border-white/10 bg-black/20 text-white/75"
                  } ${isCurrent ? "lumina-pulse border-amber-300 shadow-[0_0_0_2px_rgba(245,158,11,0.35)]" : ""}`}
                >
                  {day.day}
                </button>
              );
            })}
          </div>
          {manifestError ? <p className="m-0 mt-4 text-sm text-amber-300">{manifestError}</p> : null}
        </GlassCard>

        {selectedManifest ? (
          <GlassCard className="lumina-animate p-6 md:p-8">
            <div className="grid gap-6 lg:grid-cols-[1.2fr,0.8fr]">
              <div className="space-y-5">
                <div>
                  <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Day {selectedManifest.day}</p>
                  <h3 className="m-0 mt-3 font-serif text-3xl italic text-white">{selectedManifest.title}</h3>
                  <p className="m-0 mt-4 text-base text-amber-300">{selectedManifest.verse}</p>
                </div>
                <p className="m-0 text-base leading-8 text-white/72">{selectedManifest.prompt}</p>
                <div className="flex flex-wrap gap-3">
                  <button
                    type="button"
                    onClick={() => handleManifestDayComplete(selectedManifest.day)}
                    className="rounded-full bg-amber-500 px-5 py-3 text-sm font-semibold text-[#18171b] transition hover:bg-amber-400"
                  >
                    Mark Day Complete
                  </button>
                  <span className="rounded-full border border-white/10 bg-black/20 px-4 py-3 text-sm text-white/70">
                    {manifestation.completed_days.length}/21 completed
                  </span>
                </div>
              </div>
              <div className="rounded-[32px] border border-white/10 bg-black/20 p-5">
                <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Audio Meditation</p>
                <div className="mt-5 space-y-4">
                  <div className="flex items-center gap-4">
                    <button type="button" className="flex h-14 w-14 items-center justify-center rounded-full border border-white/10 bg-white/5 text-white/80">
                      ▶
                    </button>
                    <div className="h-2 flex-1 rounded-full bg-white/10">
                      <div className="h-2 w-1/4 rounded-full bg-amber-400" />
                    </div>
                  </div>
                  <p className="m-0 text-sm leading-7 text-white/55">Phase 2 will wire the TTS track and scrubber state. The text journey is fully available now.</p>
                </div>
              </div>
            </div>
          </GlassCard>
        ) : null}

        <PremiumUpsellCard />

        <GlassCard className="lumina-animate p-6 md:p-8">
          <SectionTitle
            eyebrow="Marketplace Vision"
            title="Establish your mandate."
            copy="Scribe your professional vision and receive a scripturally fitted blueprint for marketplace dominion."
          />
          <div className="mt-6 space-y-4">
            <textarea
              value={kingdomGoal}
              onChange={(event) => setKingdomGoal(event.target.value)}
              placeholder="Promotion in career, launch a practice, build a healing business, lead a team..."
              className="min-h-[140px] w-full rounded-[32px] border border-white/10 bg-black/30 px-5 py-5 text-base text-white outline-none transition placeholder:text-white/25 focus:border-amber-400/45"
            />
            <button
              type="button"
              onClick={handleKingdomVision}
              disabled={kingdomLoading || !kingdomGoal.trim()}
              className="rounded-full bg-white px-5 py-3 text-sm font-semibold text-[#18171b] transition hover:bg-white/90 disabled:opacity-40"
            >
              {kingdomLoading ? "Scribing mandate..." : "Scribe Mandate"}
            </button>
          </div>

          {kingdomVision ? (
            <div className="mt-6 grid gap-4">
              <div className="rounded-[32px] border border-amber-400/25 bg-amber-500/10 p-6">
                <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-300">The Kingdom Mandate</p>
                <p className="m-0 mt-4 font-serif text-2xl italic leading-9 text-white">{kingdomVision.mandate}</p>
              </div>
              <div className="grid gap-4 md:grid-cols-2">
                <GlassCard className="p-6">
                  <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Scripture</p>
                  <p className="m-0 mt-4 text-base text-white/80">{kingdomVision.scripture}</p>
                </GlassCard>
                <GlassCard className="p-6">
                  <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Blueprint Prompt</p>
                  <p className="m-0 mt-4 text-base leading-7 text-white/72">{kingdomVision.blueprint_prompt}</p>
                </GlassCard>
              </div>
              <GlassCard className="p-6">
                <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Action Plan</p>
                <div className="mt-4 grid gap-3">
                  {(kingdomVision.action_plan || []).map((step, index) => (
                    <div key={`${index}-${step}`} className="rounded-[24px] border border-white/10 bg-black/20 px-4 py-4 text-white/75">
                      {index + 1}. {step}
                    </div>
                  ))}
                </div>
              </GlassCard>
            </div>
          ) : null}
        </GlassCard>
      </div>
    );
  }

  function renderSpiritual() {
    return (
      <div className="space-y-6">
        <GlassCard className="lumina-animate p-6 md:p-8">
          <SectionTitle eyebrow="Prayer Generator" title="Creative power in declaration." badge="Creative Power" />
          <div className="mt-6 grid gap-4">
            <input
              value={prayerForm.title}
              onChange={(event) => setPrayerForm((current) => ({ ...current, title: event.target.value }))}
              placeholder="Prayer title"
              className="w-full rounded-[24px] border border-white/10 bg-black/30 px-5 py-4 text-white outline-none transition placeholder:text-white/25 focus:border-amber-400/45"
            />
            <textarea
              value={prayerForm.petition_seed}
              onChange={(event) => setPrayerForm((current) => ({ ...current, petition_seed: event.target.value }))}
              placeholder="Enter your petition or manifestation intent..."
              className="min-h-[150px] w-full rounded-[32px] border border-white/10 bg-black/30 px-5 py-5 text-base text-white outline-none transition placeholder:text-white/25 focus:border-amber-400/45"
            />
            <div className="flex flex-wrap gap-3">
              <button
                type="button"
                onClick={() => handlePrayerSubmit(true)}
                disabled={prayerLoading}
                className="rounded-full bg-indigo-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-400 disabled:opacity-40"
              >
                AI Compose
              </button>
              <button
                type="button"
                onClick={() => handlePrayerSubmit(false)}
                disabled={prayerLoading}
                className="rounded-full border border-white/10 bg-black/25 px-5 py-3 text-sm font-semibold text-white/80 transition hover:bg-white/5 disabled:opacity-40"
              >
                Archive Seed
              </button>
            </div>
            {prayerError ? <p className="m-0 text-sm text-amber-300">{prayerError}</p> : null}
          </div>
        </GlassCard>

        <GlassCard className="lumina-animate p-6 md:p-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <SectionTitle eyebrow="Declarations" title="Active declarations" copy="Strength grows as a declaration is revisited and prayed." />
            <span className="rounded-full border border-white/10 bg-black/20 px-4 py-2 text-sm text-white/80">{prayers.length} archived</span>
          </div>
          <div className="mt-6 grid gap-4">
            {prayerLoading && !prayers.length ? <p className="m-0 text-white/60">Gathering declarations...</p> : null}
            {!prayerLoading && !prayers.length ? <p className="m-0 text-white/55">No declarations yet. Create one above to begin.</p> : null}
            {prayers.map((prayer) => (
              <GlassCard key={prayer.id} className="p-5">
                <div className="flex flex-wrap items-start justify-between gap-4">
                  <div className="space-y-3">
                    <div className="flex flex-wrap items-center gap-3">
                      <h3 className="m-0 font-serif text-2xl italic text-white">{prayer.title}</h3>
                      <span className="rounded-full border border-amber-400/25 bg-amber-500/10 px-3 py-1 text-[11px] uppercase tracking-[0.25em] text-amber-300">
                        Strength {prayer.strength}
                      </span>
                      {prayer.is_realized ? (
                        <span className="rounded-full border border-emerald-400/25 bg-emerald-500/10 px-3 py-1 text-[11px] uppercase tracking-[0.25em] text-emerald-300">
                          Realized
                        </span>
                      ) : null}
                    </div>
                    <p className="m-0 max-w-3xl font-serif text-base italic leading-8 text-white/70">
                      {(expandedPrayer === prayer.id ? prayer.content : prayer.content.slice(0, 170)) + (expandedPrayer === prayer.id || prayer.content.length <= 170 ? "" : "...")}
                    </p>
                    <p className="m-0 text-sm text-white/40">{formatTimestamp(prayer.timestamp)}</p>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <button
                      type="button"
                      onClick={() => handlePrayerAction(prayer.id, "STRENGTHEN")}
                      className="rounded-full bg-amber-500 px-4 py-2 text-sm font-semibold text-[#18171b] transition hover:bg-amber-400"
                    >
                      Strengthen
                    </button>
                    <button
                      type="button"
                      onClick={() => handlePrayerAction(prayer.id, "REALIZE")}
                      className="rounded-full border border-white/10 bg-black/25 px-4 py-2 text-sm font-semibold text-white/80 transition hover:bg-white/5"
                    >
                      Realize
                    </button>
                    <button
                      type="button"
                      onClick={() => setExpandedPrayer((current) => (current === prayer.id ? "" : prayer.id))}
                      className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm font-semibold text-white/80 transition hover:bg-white/10"
                    >
                      Review
                    </button>
                  </div>
                </div>
              </GlassCard>
            ))}
          </div>
        </GlassCard>

        <GlassCard className="lumina-animate p-6 md:p-8">
          <SectionTitle eyebrow="Voice of Faith" title="Generate a first-person confession." />
          <div className="mt-6 flex flex-wrap gap-3">
            {CONFESSION_CATEGORIES.map((category) => (
              <button
                key={category}
                type="button"
                onClick={() => setConfessionCategory(category)}
                className={`rounded-full border px-4 py-3 text-sm transition ${
                  confessionCategory === category
                    ? "border-amber-400 bg-amber-500/10 text-amber-300"
                    : "border-white/10 bg-black/20 text-white/70"
                }`}
              >
                {category}
              </button>
            ))}
          </div>
          <button
            type="button"
            onClick={handleConfession}
            disabled={confessionLoading}
            className="mt-5 rounded-full bg-white px-5 py-3 text-sm font-semibold text-[#18171b] transition hover:bg-white/90 disabled:opacity-40"
          >
            {confessionLoading ? "Generating..." : "Generate Scriptural Seed"}
          </button>
          {confessionText ? (
            <div className="mt-6 rounded-[32px] border border-white/10 bg-black/20 p-6">
              <p className="m-0 font-serif text-xl italic leading-9 text-white/90">“{confessionText}”</p>
            </div>
          ) : null}
        </GlassCard>
      </div>
    );
  }

  function renderJournal() {
    return (
      <div className="space-y-6">
        <div className="grid gap-4">
          {scrollLoading ? <GlassCard className="lumina-animate p-8 text-center text-white/60">Opening your scrolls...</GlassCard> : null}
          {scrollError ? <GlassCard className="lumina-animate p-8 text-center text-amber-300">{scrollError}</GlassCard> : null}
          {!scrollLoading && !scrolls.length ? <GlassCard className="lumina-animate p-8 text-center text-white/55">Add your name to the sanctuary profile to receive personal scrolls.</GlassCard> : null}
          {scrolls.map((scroll) => (
            <GlassCard key={scroll.category} className="lumina-animate p-6 md:p-8">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <span className="rounded-full border border-white/10 bg-black/20 px-4 py-2 text-[11px] uppercase tracking-[0.3em] text-white/75">
                  {scroll.category}
                </span>
                <span className="text-sm text-amber-300">{scroll.verse}</span>
              </div>
              <h3 className="m-0 mt-5 font-serif text-3xl italic text-white">{scroll.title}</h3>
              <p className="m-0 mt-4 font-serif text-lg italic leading-9 text-white/72">“{scroll.content}”</p>
            </GlassCard>
          ))}
        </div>

        <GlassCard className="lumina-animate p-6 md:p-8">
          <SectionTitle eyebrow="Scribe's Protocol" title="Journal vault placeholder" copy="Phase 1 keeps this visible so the journal architecture has a dedicated home inside Lumina." />
          <div className="mt-6 rounded-[32px] border border-dashed border-white/15 bg-black/20 p-6 text-white/55">
            Prayer history journaling, deeper reflection templates, and archive tooling can land here in the next phase without changing the tab structure.
          </div>
        </GlassCard>

        <GlassCard className="lumina-animate p-6 md:p-8">
          <SectionTitle eyebrow="Situation Discernment" title="Bring a real situation into the light." />
          <div className="mt-6 space-y-4">
            <textarea
              value={situationText}
              onChange={(event) => setSituationText(event.target.value)}
              placeholder="Describe the situation you want wisdom for..."
              className="min-h-[130px] w-full rounded-[32px] border border-white/10 bg-black/30 px-5 py-5 text-base text-white outline-none transition placeholder:text-white/25 focus:border-amber-400/45"
            />
            <button
              type="button"
              onClick={handleSituationSearch}
              disabled={situationLoading || !situationText.trim()}
              className="rounded-full bg-white px-5 py-3 text-sm font-semibold text-[#18171b] transition hover:bg-white/90 disabled:opacity-40"
            >
              {situationLoading ? "Discernment in progress..." : "Discern Situation"}
            </button>
          </div>
          {situationResult ? (
            <div className="mt-6 grid gap-4 md:grid-cols-3">
              <GlassCard className="p-5">
                <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Analysis</p>
                <p className="m-0 mt-4 text-base leading-7 text-white/72">{situationResult.analysis}</p>
              </GlassCard>
              <GlassCard className="p-5">
                <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Miracle Story</p>
                <p className="m-0 mt-4 text-base leading-7 text-white/72">{situationResult.miracle_story}</p>
              </GlassCard>
              <GlassCard className="p-5">
                <p className="m-0 text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Narrative</p>
                <p className="m-0 mt-4 text-base leading-7 text-white/72">{situationResult.narrative}</p>
              </GlassCard>
            </div>
          ) : null}
        </GlassCard>
      </div>
    );
  }

  function renderChat() {
    return (
      <GlassCard className="lumina-animate flex min-h-[70vh] flex-col p-4 md:p-6">
        <div className="flex-1 space-y-4 overflow-auto pr-2">
          {chatMessages.map((message, index) => (
            <div key={`${index}-${message.role}`} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-[88%] rounded-[28px] border px-5 py-4 ${message.role === "user" ? "border-indigo-400/30 bg-indigo-500/20 text-white" : "border-white/10 bg-white/5 text-white/85"}`}>
                {message.image ? <img src={message.image} alt="Uploaded context" className="mb-4 max-h-56 w-full rounded-[20px] object-cover" /> : null}
                <p className="m-0 text-sm leading-7">{message.text}</p>
                {message.sources?.length ? (
                  <div className="mt-4 flex flex-wrap gap-2">
                    {message.sources.map((source) => (
                      <a
                        key={`${source.title}-${source.uri}`}
                        href={source.uri}
                        target="_blank"
                        rel="noreferrer"
                        className="rounded-full border border-white/10 bg-black/20 px-3 py-2 text-[11px] uppercase tracking-[0.2em] text-amber-300"
                      >
                        {source.title}
                      </a>
                    ))}
                  </div>
                ) : null}
              </div>
            </div>
          ))}
          {chatLoading ? <p className="m-0 text-sm italic text-white/50">The chaplain is reflecting...</p> : null}
        </div>
        <div className="mt-5 border-t border-white/10 pt-4">
          {chatImage ? (
            <div className="mb-4 flex items-center gap-3">
              <img src={chatImage} alt="Preview" className="h-16 w-16 rounded-[20px] object-cover" />
              <button type="button" onClick={() => setChatImage(null)} className="rounded-full border border-white/10 bg-black/20 px-4 py-2 text-sm text-white/75">
                Remove image
              </button>
            </div>
          ) : null}
          <div className="flex flex-col gap-3 md:flex-row">
            <label className="flex cursor-pointer items-center justify-center rounded-full border border-white/10 bg-black/20 px-4 py-3 text-sm text-white/75 transition hover:bg-white/5">
              Upload Image
              <input type="file" accept="image/*" onChange={handleChatImageChange} className="hidden" />
            </label>
            <input
              value={chatInput}
              onChange={(event) => setChatInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  handleSendChat();
                }
              }}
              placeholder="Ask anything spiritual..."
              className="flex-1 rounded-[24px] border border-white/10 bg-black/30 px-5 py-4 text-white outline-none transition placeholder:text-white/25 focus:border-amber-400/45"
            />
            <button
              type="button"
              onClick={handleSendChat}
              disabled={chatLoading || (!chatInput.trim() && !chatImage)}
              className="rounded-full bg-white px-5 py-3 text-sm font-semibold text-[#18171b] transition hover:bg-white/90 disabled:opacity-40"
            >
              Send
            </button>
          </div>
        </div>
      </GlassCard>
    );
  }

  function renderActiveTab() {
    switch (activeTab) {
      case "bible":
        return renderBible();
      case "manifest":
        return renderManifest();
      case "spiritual":
        return renderSpiritual();
      case "journal":
        return renderJournal();
      case "chat":
        return renderChat();
      default:
        return renderHome();
    }
  }

  return (
    <div className="min-h-screen bg-[#0f1018] px-4 pb-32 pt-6 text-white md:px-8">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500;1,700&display=swap');
        .lumina-shell {
          background:
            radial-gradient(circle at top left, rgba(245, 158, 11, 0.08), transparent 28%),
            radial-gradient(circle at 86% 12%, rgba(99, 102, 241, 0.16), transparent 26%),
            linear-gradient(180deg, rgba(15,16,24,1) 0%, rgba(11,12,18,1) 100%);
        }
        .lumina-animate {
          animation: lumina-rise 0.6s ease both;
        }
        .lumina-pulse {
          animation: lumina-pulse 1.8s ease-in-out infinite;
        }
        @keyframes lumina-rise {
          from { opacity: 0; transform: translateY(16px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes lumina-pulse {
          0%, 100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.26); }
          50% { box-shadow: 0 0 0 10px rgba(245, 158, 11, 0); }
        }
      `}</style>

      <div className="lumina-shell mx-auto max-w-7xl rounded-[44px] border border-white/10 p-4 shadow-[0_40px_120px_rgba(0,0,0,0.45)] md:p-6">
        <header className="lumina-animate flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="m-0 font-serif text-4xl italic tracking-[0.02em] text-white md:text-5xl">Lumina</p>
            <p className="m-0 mt-2 text-sm text-white/55">Walk in the Divine Light.</p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <span className="rounded-full border border-amber-400/25 bg-amber-500/10 px-4 py-2 text-sm text-amber-300">
              {credits} points
            </span>
          </div>
        </header>

        <GlassCard className="lumina-animate mt-5 p-5 md:p-6">
          <div className="grid gap-4 lg:grid-cols-[1fr,auto]">
            <div className="grid gap-4 md:grid-cols-2">
              <label className="space-y-2 text-sm text-white/70">
                <span className="block text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Sanctuary Name</span>
                <input
                  value={profile.userName}
                  onChange={(event) => setProfile((current) => ({ ...current, userName: event.target.value }))}
                  placeholder="Your name"
                  className="w-full rounded-[24px] border border-white/10 bg-black/25 px-4 py-4 text-white outline-none transition placeholder:text-white/25 focus:border-amber-400/45"
                />
              </label>
              <label className="space-y-2 text-sm text-white/70">
                <span className="block text-[11px] uppercase tracking-[0.35em] text-amber-400/75">Sanctuary Email</span>
                <input
                  value={profile.userEmail}
                  onChange={(event) => setProfile((current) => ({ ...current, userEmail: event.target.value }))}
                  placeholder="you@example.com"
                  className="w-full rounded-[24px] border border-white/10 bg-black/25 px-4 py-4 text-white outline-none transition placeholder:text-white/25 focus:border-amber-400/45"
                />
              </label>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              {SCRIPTURE_MODES.map((mode) => (
                <button
                  key={mode}
                  type="button"
                  onClick={() => setScriptureMode(mode)}
                  className={`rounded-full px-4 py-3 text-sm font-semibold transition ${
                    scriptureMode === mode
                      ? "bg-amber-500 text-[#18171b]"
                      : "border border-white/10 bg-black/25 text-white/75 hover:bg-white/5"
                  }`}
                >
                  {mode}
                </button>
              ))}
            </div>
          </div>
        </GlassCard>

        <main className="mt-6">
          <SectionTitle
            eyebrow={TABS.find((tab) => tab.id === activeTab)?.label || "Home"}
            title={
              activeTab === "home"
                ? "Today’s living word"
                : activeTab === "bible"
                  ? "Scripture Reader"
                  : activeTab === "manifest"
                    ? "Manifest and build"
                    : activeTab === "spiritual"
                      ? "Declarations and confessions"
                      : activeTab === "journal"
                        ? "Scrolls and reflection"
                        : "AI Chaplain"
            }
            copy={
              activeTab === "chat"
                ? "Ask questions, upload an image if it matters, and receive scripture-grounded pastoral care."
                : activeTab === "manifest"
                  ? "Track the 21-day calendar and turn your calling into a kingdom-aligned blueprint."
                  : activeTab === "spiritual"
                    ? "Compose declarations, strengthen them over time, and speak truth in first person."
                    : undefined
            }
          />
          <div className="mt-6">{renderActiveTab()}</div>
        </main>

        <nav className="fixed bottom-4 left-1/2 z-50 w-[calc(100%-1.5rem)] max-w-4xl -translate-x-1/2 rounded-[36px] border border-white/10 bg-[#141622]/90 p-2 backdrop-blur-xl shadow-[0_24px_60px_rgba(0,0,0,0.45)]">
          <div className="grid grid-cols-6 gap-2">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                type="button"
                onClick={() => setActiveTab(tab.id)}
                className={`rounded-[28px] px-3 py-3 text-center text-xs font-medium transition md:text-sm ${
                  activeTab === tab.id ? "bg-amber-500 text-[#18171b]" : "text-white/70 hover:bg-white/5"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </nav>
      </div>
    </div>
  );
}

export default LuminaPage;
