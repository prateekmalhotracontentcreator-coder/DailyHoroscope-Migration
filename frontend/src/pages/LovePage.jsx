import React, { useEffect, useMemo, useRef, useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const LOVE_REPORTS = [
  { slug: "love-weather", label: "Love Weather", description: "90-day romantic forecast with best and caution dates", accent: "rgba(183, 60, 100, 0.12)", icon: "☁️" },
  { slug: "encounter-window", label: "Encounter Window", description: "Upcoming transit windows most likely to spark new meetings", accent: "rgba(183, 60, 100, 0.12)", icon: "✨" },
  { slug: "date-night", label: "Date Night Planner", description: "Best dates in the next 30 days for a memorable outing", accent: "rgba(183, 60, 100, 0.12)", icon: "🌙" },
  { slug: "digital-dating", label: "Digital Dating Edge", description: "Optimise your profile and message timing with your chart", accent: "rgba(183, 60, 100, 0.12)", icon: "💌" },
  { slug: "intimacy-vitality", label: "Intimacy & Vitality", description: "Mars-Venus windows for depth and physical connection", accent: "rgba(139, 30, 60, 0.12)", icon: "🔥" },
  { slug: "venus-retrograde", label: "Venus Retrograde", description: "How the current retrograde is affecting your love life", accent: "rgba(215, 175, 106, 0.14)", icon: "♀" },
  { slug: "soulmate-timing", label: "Soulmate Timing", description: "Jupiter and Dasha windows for long-term partnership", accent: "rgba(215, 175, 106, 0.14)", icon: "⏳" },
  { slug: "soul-connection", label: "Soul Connection", description: "Karmic and evolutionary patterns in your relationships", accent: "rgba(100, 60, 160, 0.12)", icon: "∞" },
];

const TRIGGERS = [
  { icon: "🌹", name: "First Date Magnet", text: "Venus within 3° of natal Sun, Ascendant, or 7th lord", tint: "rgba(183, 60, 100, 0.12)" },
  { icon: "🔥", name: "Steamy Encounter", text: "Mars trine natal Venus or entering your natal 8th", tint: "rgba(139, 30, 60, 0.12)" },
  { icon: "🌕", name: "Ex-Recovery Window", text: "Mercury or Venus retrograde crossing natal 5th/7th", tint: "rgba(124, 88, 166, 0.12)" },
  { icon: "🌿", name: "Long-Term Love Portal", text: "Jupiter entering natal 7th or trining Ascendant", tint: "rgba(120, 145, 78, 0.12)" },
  { icon: "💛", name: "Love Battery Score", text: "Daily Moon-natal Venus angle (always-on)", tint: "rgba(215, 175, 106, 0.14)" },
];

const pageStyle = {
  minHeight: "100vh",
  background:
    "radial-gradient(circle at top left, rgba(183,60,100,0.16), transparent 24%), radial-gradient(circle at 86% 10%, rgba(215,175,106,0.18), transparent 22%), linear-gradient(180deg, #faf6ef 0%, #f4ede2 100%)",
  color: "#2a2119",
  padding: "28px 18px 72px",
};

const cardStyle = {
  background: "rgba(255,251,245,0.88)",
  borderRadius: 22,
  border: "1px solid rgba(120,90,55,0.14)",
  boxShadow: "0 18px 46px rgba(74,50,22,0.09)",
  backdropFilter: "blur(10px)",
};

const primaryButtonStyle = {
  minHeight: 46,
  padding: "10px 18px",
  borderRadius: 999,
  border: "1px solid transparent",
  background: "linear-gradient(135deg, #b78646 0%, #d8af6a 100%)",
  color: "#241910",
  fontWeight: 700,
  textDecoration: "none",
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  cursor: "pointer",
};

const secondaryButtonStyle = {
  ...primaryButtonStyle,
  background: "rgba(255,255,255,0.76)",
  border: "1px solid rgba(120,90,55,0.16)",
  color: "#2a2119",
};

function ensureMeta(selector, attrs) {
  let node = document.head.querySelector(selector);
  if (!node) {
    node = document.createElement("meta");
    Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value));
    document.head.appendChild(node);
  }
  return node;
}

function useLoveSeo() {
  useEffect(() => {
    document.title = "Love & Relationship Astrology Reports | Everyday Horoscope";

    ensureMeta('meta[name="description"]', { name: "description" }).setAttribute(
      "content",
      "Eight Vedic astrology reports for your love life - Love Weather, Encounter Windows, Soulmate Timing, and more. Plus the daily Ritual Engine love score."
    );
    ensureMeta('meta[property="og:title"]', { property: "og:title" }).setAttribute("content", "Love Intelligence | Everyday Horoscope");
    ensureMeta('meta[property="og:description"]', { property: "og:description" }).setAttribute(
      "content",
      "Daily Vedic love scores, 90-day romantic forecasts, and planetary trigger alerts - all from your natal chart."
    );
    ensureMeta('meta[property="og:url"]', { property: "og:url" }).setAttribute("content", "https://www.everydayhoroscope.in/love");
    ensureMeta('meta[property="og:type"]', { property: "og:type" }).setAttribute("content", "website");

    let canonical = document.head.querySelector('link[rel="canonical"]');
    if (!canonical) {
      canonical = document.createElement("link");
      canonical.setAttribute("rel", "canonical");
      document.head.appendChild(canonical);
    }
    canonical.setAttribute("href", "https://www.everydayhoroscope.in/love");

    const existing = document.getElementById("love-page-jsonld");
    if (existing) existing.remove();
    const script = document.createElement("script");
    script.type = "application/ld+json";
    script.id = "love-page-jsonld";
    script.text = JSON.stringify({
      "@context": "https://schema.org",
      "@type": "WebPage",
      name: "Love & Relationship Astrology Reports",
      description: "Vedic astrology love reports and daily Ritual Engine score",
      url: "https://www.everydayhoroscope.in/love",
      publisher: {
        "@type": "Organization",
        name: "Everyday Horoscope",
        url: "https://www.everydayhoroscope.in",
      },
      mainEntity: {
        "@type": "ItemList",
        itemListElement: LOVE_REPORTS.map((report, index) => ({
          "@type": "ListItem",
          position: index + 1,
          name: report.label,
          description: report.description,
        })),
      },
    });
    document.head.appendChild(script);
    return () => script.remove();
  }, []);
}

function LovePage() {
  const navigate = useNavigate();
  const reportRef = useRef(null);
  const ritualRef = useRef(null);
  const [ritualState, setRitualState] = useState({ loading: true, authenticated: false, subscribed: false });
  const [showModal, setShowModal] = useState(false);

  useLoveSeo();

  useEffect(() => {
    let active = true;
    async function loadRitualState() {
      try {
        await axios.get(`${API}/ritual-engine/dashboard`, { withCredentials: true });
        if (active) setRitualState({ loading: false, authenticated: true, subscribed: true });
      } catch (error) {
        if (!active) return;
        const status = error?.response?.status;
        if (status === 404) {
          setRitualState({ loading: false, authenticated: true, subscribed: false });
          return;
        }
        setRitualState({ loading: false, authenticated: false, subscribed: false });
      }
    }
    loadRitualState();
    return () => {
      active = false;
    };
  }, []);

  const ritualCtaLabel = useMemo(() => {
    if (ritualState.loading) return "Checking Ritual Engine";
    if (ritualState.subscribed) return "Open Ritual Engine";
    return "Activate Ritual Engine";
  }, [ritualState]);

  function handleHeroRitualClick() {
    if (!ritualState.authenticated) {
      navigate("/login");
      return;
    }
    if (ritualState.subscribed) {
      navigate("/ritual-engine");
      return;
    }
    ritualRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    setShowModal(true);
  }

  return (
    <div style={pageStyle}>
      <div style={{ maxWidth: 1180, margin: "0 auto", display: "grid", gap: 18 }}>
        <section style={{ ...cardStyle, padding: "28px 24px", overflow: "hidden" }}>
          <div style={{ display: "grid", gap: 20, gridTemplateColumns: "minmax(0, 1.25fr) minmax(280px, 0.75fr)" }}>
            <div style={{ display: "grid", gap: 16 }}>
              <p style={{ margin: 0, fontSize: 12, letterSpacing: "0.2em", textTransform: "uppercase", color: "#8c6a39" }}>Love Bundle</p>
              <h1 style={{ margin: 0, fontSize: "clamp(2.6rem, 7vw, 4.8rem)", lineHeight: 0.94, fontFamily: "Georgia, Times New Roman, serif" }}>
                Your Love Intelligence. Powered by Vedic Astrology.
              </h1>
              <p style={{ margin: 0, fontSize: 18, lineHeight: 1.72, color: "#5f5348", maxWidth: 760 }}>
                Eight precision reports and a live Ritual Engine that tracks your Venus transits, Mars windows, and lunar love score - every single day.
              </p>
              <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
                <button type="button" onClick={() => reportRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })} style={primaryButtonStyle}>
                  Explore Reports
                </button>
                <button type="button" onClick={handleHeroRitualClick} style={secondaryButtonStyle}>
                  {ritualCtaLabel}
                </button>
              </div>
            </div>
            <div
              style={{
                borderRadius: 24,
                padding: 20,
                background:
                  "linear-gradient(180deg, rgba(183,60,100,0.12) 0%, rgba(255,251,245,0.76) 50%, rgba(215,175,106,0.14) 100%)",
                display: "grid",
                gap: 14,
                alignContent: "start",
              }}
            >
              <div style={{ display: "grid", gap: 6 }}>
                <p style={{ margin: 0, fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: "#8a4d5e" }}>What’s inside</p>
                <strong style={{ fontSize: 22, fontFamily: "Georgia, Times New Roman, serif" }}>Eight reports. One live engine.</strong>
              </div>
              <div style={{ display: "grid", gap: 10 }}>
                {["Transit timing", "Daily Love Battery", "Whole-sign Vedic logic", "History + ritual prompts"].map((item) => (
                  <div key={item} style={{ padding: "10px 12px", borderRadius: 16, background: "rgba(255,255,255,0.7)" }}>
                    {item}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section ref={reportRef} style={{ ...cardStyle, padding: 24 }}>
          <div style={{ marginBottom: 18 }}>
            <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: "#8c6a39" }}>Report Hub</p>
            <h2 style={{ margin: 0, fontSize: 34, fontFamily: "Georgia, Times New Roman, serif" }}>Choose the love question you want answered first.</h2>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 16 }}>
            {LOVE_REPORTS.map((report) => (
              <article key={report.slug} style={{ ...cardStyle, padding: 18, background: report.accent }}>
                <div style={{ fontSize: 28, marginBottom: 10 }}>{report.icon}</div>
                <h3 style={{ margin: "0 0 8px", fontSize: 24, fontFamily: "Georgia, Times New Roman, serif" }}>{report.label}</h3>
                <p style={{ margin: "0 0 14px", color: "#64584c", lineHeight: 1.62 }}>{report.description}</p>
                <Link to={`/love-reports?reportType=${report.slug}&tab=generate`} style={primaryButtonStyle}>
                  Generate
                </Link>
              </article>
            ))}
          </div>
        </section>

        <section ref={ritualRef} style={{ ...cardStyle, padding: 24 }}>
          <div style={{ display: "grid", gap: 10 }}>
            <p style={{ margin: 0, fontSize: 12, letterSpacing: "0.18em", textTransform: "uppercase", color: "#8c6a39" }}>Subscription Flagship</p>
            <h2 style={{ margin: 0, fontSize: 36, fontFamily: "Georgia, Times New Roman, serif" }}>The Ritual Engine - Your Daily Love Intelligence Feed</h2>
            <p style={{ margin: 0, color: "#605449", lineHeight: 1.72, maxWidth: 900 }}>
              Subscribe once. Every morning the engine evaluates your Venus transits, Mars activations, and Moon-Venus angle against your natal chart. You receive only what is astrologically active for you today.
            </p>
          </div>
          <div style={{ marginTop: 18, display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 14 }}>
            {TRIGGERS.map((trigger) => (
              <article key={trigger.name} style={{ ...cardStyle, padding: 16, background: trigger.tint }}>
                <div style={{ fontSize: 28, marginBottom: 8 }}>{trigger.icon}</div>
                <h3 style={{ margin: "0 0 8px", fontSize: 20, fontFamily: "Georgia, Times New Roman, serif" }}>{trigger.name}</h3>
                <p style={{ margin: 0, color: "#63574b", lineHeight: 1.6 }}>{trigger.text}</p>
              </article>
            ))}
          </div>
          <div style={{ marginTop: 18, display: "flex", gap: 12, flexWrap: "wrap" }}>
            <button
              type="button"
              onClick={() => {
                if (ritualState.subscribed) navigate("/ritual-engine");
                else if (!ritualState.authenticated) navigate("/login");
                else setShowModal(true);
              }}
              style={primaryButtonStyle}
            >
              {ritualState.subscribed ? "Open Ritual Engine" : "Activate Ritual Engine"}
            </button>
            <Link to="/love-reports" style={secondaryButtonStyle}>
              Explore Reports
            </Link>
          </div>
        </section>

        <section
          style={{
            ...cardStyle,
            padding: 24,
            background: "linear-gradient(135deg, rgba(215,175,106,0.2) 0%, rgba(255,251,245,0.9) 100%)",
            display: "flex",
            justifyContent: "space-between",
            gap: 12,
            flexWrap: "wrap",
            alignItems: "center",
          }}
        >
          <div>
            <p style={{ margin: "0 0 6px", fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: "#8c6a39" }}>Ready now</p>
            <h2 style={{ margin: 0, fontSize: 28, fontFamily: "Georgia, Times New Roman, serif" }}>Ready to see your Love Weather?</h2>
          </div>
          <Link to="/love-reports" style={primaryButtonStyle}>
            Open Love Reports
          </Link>
        </section>
      </div>

      {showModal ? (
        <div
          role="presentation"
          onClick={() => setShowModal(false)}
          style={{
            position: "fixed",
            inset: 0,
            background: "rgba(24,16,12,0.42)",
            display: "grid",
            placeItems: "center",
            padding: 18,
          }}
        >
          <div role="dialog" aria-modal="true" onClick={(event) => event.stopPropagation()} style={{ ...cardStyle, maxWidth: 520, width: "100%", padding: 24 }}>
            <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: "#8c6a39" }}>Ritual Engine</p>
            <h3 style={{ margin: "0 0 10px", fontSize: 30, fontFamily: "Georgia, Times New Roman, serif" }}>Open your enrollment flow</h3>
            <p style={{ margin: "0 0 18px", color: "#605449", lineHeight: 1.68 }}>
              Enrollment lives on the protected Ritual Engine page. Your birth details and trigger preferences are collected there once you are signed in.
            </p>
            <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
              <button
                type="button"
                onClick={() => {
                  setShowModal(false);
                  navigate(ritualState.authenticated ? "/ritual-engine" : "/login");
                }}
                style={primaryButtonStyle}
              >
                {ritualState.authenticated ? "Continue" : "Log In"}
              </button>
              <button type="button" onClick={() => setShowModal(false)} style={secondaryButtonStyle}>
                Close
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

export default LovePage;
