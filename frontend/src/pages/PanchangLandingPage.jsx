import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Link, useParams, useSearchParams } from "react-router-dom";

import PanchangLanguageToggle from "../components/PanchangLanguageToggle";
import { buildPanchangPath, getPanchangCopy, getPanchangLanguage } from "../components/panchangLocale";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const TITHI_NAMES = [
  "Pratipada",
  "Dvitiya",
  "Tritiya",
  "Chaturthi",
  "Panchami",
  "Shashthi",
  "Saptami",
  "Ashtami",
  "Navami",
  "Dashami",
  "Ekadashi",
  "Dwadashi",
  "Trayodashi",
  "Chaturdashi",
  "Purnima",
  "Pratipada",
  "Dvitiya",
  "Tritiya",
  "Chaturthi",
  "Panchami",
  "Shashthi",
  "Saptami",
  "Ashtami",
  "Navami",
  "Dashami",
  "Ekadashi",
  "Dwadashi",
  "Trayodashi",
  "Chaturdashi",
  "Amavasya",
];

const NAKSHATRA_NAMES = [
  "Ashwini",
  "Bharani",
  "Krittika",
  "Rohini",
  "Mrigashira",
  "Ardra",
  "Punarvasu",
  "Pushya",
  "Ashlesha",
  "Magha",
  "Purva Phalguni",
  "Uttara Phalguni",
  "Hasta",
  "Chitra",
  "Swati",
  "Vishakha",
  "Anuradha",
  "Jyeshtha",
  "Mula",
  "Purva Ashadha",
  "Uttara Ashadha",
  "Shravana",
  "Dhanishtha",
  "Shatabhisha",
  "Purva Bhadrapada",
  "Uttara Bhadrapada",
  "Revati",
];

const YOGA_NAMES = [
  "Vishkambha",
  "Priti",
  "Ayushman",
  "Saubhagya",
  "Shobhana",
  "Atiganda",
  "Sukarma",
  "Dhriti",
  "Shoola",
  "Ganda",
  "Vriddhi",
  "Dhruva",
  "Vyaghata",
  "Harshana",
  "Vajra",
  "Siddhi",
  "Vyatipata",
  "Variyana",
  "Parigha",
  "Shiva",
  "Siddha",
  "Sadhya",
  "Shubha",
  "Shukla",
  "Brahma",
  "Indra",
  "Vaidhriti",
];

const KARANA_NAMES = [
  "Kimstughna",
  "Bava",
  "Balava",
  "Kaulava",
  "Taitila",
  "Garaja",
  "Vanija",
  "Vishti",
  "Bava",
  "Balava",
  "Kaulava",
  "Taitila",
  "Garaja",
  "Vanija",
  "Vishti",
  "Bava",
  "Balava",
  "Kaulava",
  "Taitila",
  "Garaja",
  "Vanija",
  "Vishti",
  "Bava",
  "Balava",
  "Kaulava",
  "Taitila",
  "Garaja",
  "Vanija",
  "Vishti",
  "Shakuni",
  "Chatushpada",
  "Naga",
  "Kimstughna",
];

const ROW_TONES = {
  Tithi: "warm",
  Nakshatra: "sage",
  Yoga: "gold",
  Karana: "night",
};

const WINDOW_TONES = {
  "Rahu Kaal": "alert",
  Yamaganda: "alert",
  "Gulika Kaal": "warm",
  "Abhijit Muhurta": "gold",
  "Dur Muhurta": "alert",
  "Amrit Kalam": "sage",
  Varjyam: "alert",
};

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function formatHour(value) {
  const normalized = ((value % 24) + 24) % 24;
  const hour = Math.floor(normalized);
  const minute = Math.round((normalized - hour) * 60);
  const safeMinute = minute === 60 ? 0 : minute;
  const safeHour = minute === 60 ? (hour + 1) % 24 : hour;
  const suffix = safeHour >= 12 ? "PM" : "AM";
  const twelveHour = ((safeHour + 11) % 12) + 1;
  return `${twelveHour}:${String(safeMinute).padStart(2, "0")} ${suffix}`;
}

function hourFromDate(isoValue) {
  const moment = new Date(isoValue);
  return moment.getHours() + moment.getMinutes() / 60 + moment.getSeconds() / 3600;
}

function hourFromClock(dateValue, clockValue) {
  const [hours, minutes] = clockValue.split(":").map(Number);
  const moment = new Date(`${dateValue}T00:00:00`);
  moment.setHours(hours, minutes, 0, 0);
  return moment.getHours() + moment.getMinutes() / 60;
}

function buildTimelinePosition(hour, dayStart, dayEnd) {
  return ((hour - dayStart) / Math.max(dayEnd - dayStart, 1)) * 100;
}

function getSolarIntensity(hour, sunriseHour, sunsetHour) {
  const normalized = (hour - sunriseHour) / Math.max(sunsetHour - sunriseHour, 0.1);
  if (normalized <= 0 || normalized >= 1) return 0;
  return Math.sin(normalized * Math.PI);
}

function nextName(names, currentIndex) {
  const nextIndex = currentIndex % names.length;
  return names[nextIndex];
}

function toneForRow(label) {
  return ROW_TONES[label] || "gold";
}

function toneForWindow(label) {
  return WINDOW_TONES[label] || "warm";
}

function buildRowSegments(label, segment, dayStart, dayEnd, names) {
  if (!segment) return [];
  const segments = [];
  const startHour = segment.start ? hourFromDate(segment.start) : dayStart;
  const endHour = segment.end ? hourFromDate(segment.end) : dayEnd;
  const visibleStart = clamp(startHour, dayStart, dayEnd);
  const visibleEnd = clamp(endHour, dayStart, dayEnd);

  if (visibleEnd > visibleStart) {
    segments.push({
      start: visibleStart,
      end: visibleEnd,
      name: segment.name,
      tone: toneForRow(label),
    });
  }

  if (segment.end && endHour < dayEnd) {
    segments.push({
      start: clamp(endHour, dayStart, dayEnd),
      end: dayEnd,
      name: nextName(names, segment.index),
      tone: "gold",
    });
  }

  if (!segments.length) {
    segments.push({
      start: dayStart,
      end: dayEnd,
      name: segment.name,
      tone: toneForRow(label),
    });
  }

  return segments;
}

function buildWindowSegments(day, dayStart, dayEnd) {
  return [...(day.day_quality_windows || []), ...(day.special_timing_windows || [])]
    .map((window) => {
      const start = clamp(hourFromDate(window.start), dayStart, dayEnd);
      const end = clamp(hourFromDate(window.end), dayStart, dayEnd);
      return {
        label: window.label,
        start,
        end,
        tone: toneForWindow(window.label),
      };
    })
    .filter((window) => window.end > window.start);
}

function getActiveSegment(row, hour) {
  return row.segments.find((segment) => hour >= segment.start && hour < segment.end) || row.segments[row.segments.length - 1];
}

function buildLensTitle(activeWindow) {
  return activeWindow ? activeWindow.label : "Live Panchang balance";
}

function PanchangLandingPage() {
  const { lang } = useParams();
  const [searchParams] = useSearchParams();
  const language = getPanchangLanguage(lang);
  const copy = getPanchangCopy(language);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [day, setDay] = useState(null);
  const [focusHour, setFocusHour] = useState(12);
  const locationSlug = searchParams.get("location_slug") || "new-delhi-india";

  useEffect(() => {
    let active = true;
    async function load() {
      setLoading(true);
      setError("");
      try {
        const res = await axios.get(`${API}/panchang/daily`, {
          params: {
            location_slug: locationSlug,
          },
        });
        if (!active) return;
        setDay(res.data);
      } catch (err) {
        if (!active) return;
        setError(err?.response?.data?.detail || "Unable to load Panchang hero data right now.");
      } finally {
        if (active) setLoading(false);
      }
    }
    load();
    return () => {
      active = false;
    };
  }, [locationSlug]);

  const cosmicMap = useMemo(() => {
    if (!day) return null;
    const sunriseHour = hourFromClock(day.date, day.summary.sunrise);
    const sunsetHour = hourFromClock(day.date, day.summary.sunset);
    const dayStartHour = Math.max(Math.floor(sunriseHour) - 1, 0);
    const dayEndHour = Math.min(Math.ceil(sunsetHour) + 1, 24);
    const timeRows = [
      {
        label: "Tithi",
        segments: buildRowSegments("Tithi", day.panchang?.tithi, dayStartHour, dayEndHour, TITHI_NAMES),
      },
      {
        label: "Nakshatra",
        segments: buildRowSegments("Nakshatra", day.panchang?.nakshatra, dayStartHour, dayEndHour, NAKSHATRA_NAMES),
      },
      {
        label: "Yoga",
        segments: buildRowSegments("Yoga", day.panchang?.yoga, dayStartHour, dayEndHour, YOGA_NAMES),
      },
      {
        label: "Karana",
        segments: buildRowSegments("Karana", day.panchang?.karana, dayStartHour, dayEndHour, KARANA_NAMES),
      },
    ];
    const timeWindows = buildWindowSegments(day, dayStartHour, dayEndHour);
    const suggestedFocus =
      timeWindows.find((window) => window.label === "Abhijit Muhurta") ||
      timeWindows.find((window) => window.label === "Amrit Kalam") ||
      { start: (sunriseHour + sunsetHour) / 2, end: (sunriseHour + sunsetHour) / 2 };
    return {
      sunriseHour,
      sunsetHour,
      dayStartHour,
      dayEndHour,
      timeRows,
      timeWindows,
      suggestedFocus: (suggestedFocus.start + suggestedFocus.end) / 2,
    };
  }, [day]);

  useEffect(() => {
    if (!cosmicMap) return;
    setFocusHour(cosmicMap.suggestedFocus);
  }, [cosmicMap]);

  const activeRows = useMemo(
    () =>
      cosmicMap
        ? cosmicMap.timeRows.map((row) => ({
            label: row.label,
            segment: getActiveSegment(row, focusHour),
          }))
        : [],
    [cosmicMap, focusHour],
  );

  const activeWindow = useMemo(
    () => cosmicMap?.timeWindows.find((window) => focusHour >= window.start && focusHour <= window.end) || null,
    [cosmicMap, focusHour],
  );

  const focusLeft = cosmicMap ? buildTimelinePosition(focusHour, cosmicMap.dayStartHour, cosmicMap.dayEndHour) : 50;
  const intensity = cosmicMap ? getSolarIntensity(focusHour, cosmicMap.sunriseHour, cosmicMap.sunsetHour) : 0;

  function updateFocusFromPointer(event) {
    if (!cosmicMap) return;
    const bounds = event.currentTarget.getBoundingClientRect();
    const ratio = clamp((event.clientX - bounds.left) / bounds.width, 0, 1);
    setFocusHour(cosmicMap.dayStartHour + ratio * (cosmicMap.dayEndHour - cosmicMap.dayStartHour));
  }

  return (
    <div className="panchang-page panchang-landing-page">
      <section className="panchang-shell panchang-cosmic-map">
        <div className="panchang-cosmic-map__header">
          <div>
            <p className="panchang-eyebrow">Time Map</p>
            <h2>{day ? `${day.location.label} — ${day.date}` : "The living Panchang across a single day"}</h2>
          </div>
          <div className="panchang-cosmic-map__header-meta">
            <p className="panchang-cosmic-map__subcopy">
              {day
                ? "The cosmic map now reads directly from the live daily Panchang response, including sunrise, core limbs, and timing windows."
                : "Move across the parchment to inspect sunrise, solar intensity, and the active Panchang layers in one interactive lens."}
            </p>
            <PanchangLanguageToggle />
          </div>
        </div>

        {loading ? <div className="panchang-cosmic-map__status">Loading live Panchang time map...</div> : null}
        {error ? <div className="panchang-cosmic-map__status panchang-error">{error}</div> : null}

        {cosmicMap ? (
          <div
            className="panchang-cosmic-map__frame"
            onMouseMove={updateFocusFromPointer}
            onPointerMove={updateFocusFromPointer}
            onTouchMove={(event) => {
              const touch = event.touches[0];
              if (!touch || !cosmicMap) return;
              const bounds = event.currentTarget.getBoundingClientRect();
              const ratio = clamp((touch.clientX - bounds.left) / bounds.width, 0, 1);
              setFocusHour(cosmicMap.dayStartHour + ratio * (cosmicMap.dayEndHour - cosmicMap.dayStartHour));
            }}
          >
            <div className="panchang-cosmic-map__sunband">
              <div className="panchang-cosmic-map__sunband-fill" />
              <div
                className="panchang-cosmic-map__sun-marker panchang-cosmic-map__sun-marker--rise"
                style={{ left: `${buildTimelinePosition(cosmicMap.sunriseHour, cosmicMap.dayStartHour, cosmicMap.dayEndHour)}%` }}
              >
                <span>Sunrise</span>
                <strong>{day.summary.sunrise}</strong>
              </div>
              <div
                className="panchang-cosmic-map__sun-marker panchang-cosmic-map__sun-marker--set"
                style={{ left: `${buildTimelinePosition(cosmicMap.sunsetHour, cosmicMap.dayStartHour, cosmicMap.dayEndHour)}%` }}
              >
                <span>Sunset</span>
                <strong>{day.summary.sunset}</strong>
              </div>
            </div>

            <svg className="panchang-cosmic-map__curve" viewBox="0 0 1000 180" preserveAspectRatio="none" aria-hidden="true">
              <defs>
                <linearGradient id="solarCurve" x1="0%" x2="100%">
                  <stop offset="0%" stopColor="#d99834" />
                  <stop offset="45%" stopColor="#ffe27f" />
                  <stop offset="100%" stopColor="#c7652e" />
                </linearGradient>
              </defs>
              <path
                d="M 40 136 Q 250 44 500 32 Q 760 44 960 136"
                fill="none"
                stroke="url(#solarCurve)"
                strokeWidth="6"
                strokeLinecap="round"
              />
              <path d="M 40 136 Q 250 44 500 32 Q 760 44 960 136" fill="rgba(233, 190, 98, 0.12)" stroke="none" />
            </svg>

            <div className="panchang-cosmic-map__hours">
              {Array.from({ length: cosmicMap.dayEndHour - cosmicMap.dayStartHour + 1 }).map((_, index) => {
                const hour = cosmicMap.dayStartHour + index;
                return (
                  <span
                    key={hour}
                    style={{ left: `${(index / Math.max(cosmicMap.dayEndHour - cosmicMap.dayStartHour, 1)) * 100}%` }}
                  >
                    {hour}
                  </span>
                );
              })}
            </div>

            <div className="panchang-cosmic-map__rows">
              {cosmicMap.timeRows.map((row) => (
                <div key={row.label} className="panchang-cosmic-map__row">
                  <span className="panchang-cosmic-map__row-label">{row.label}</span>
                  <div className="panchang-cosmic-map__track">
                    {row.segments.map((segment) => (
                      <div
                        key={`${row.label}-${segment.name}-${segment.start}`}
                        className={`panchang-cosmic-map__segment panchang-cosmic-map__segment--${segment.tone}`}
                        style={{
                          left: `${buildTimelinePosition(segment.start, cosmicMap.dayStartHour, cosmicMap.dayEndHour)}%`,
                          width: `${buildTimelinePosition(segment.end, cosmicMap.dayStartHour, cosmicMap.dayEndHour) - buildTimelinePosition(segment.start, cosmicMap.dayStartHour, cosmicMap.dayEndHour)}%`,
                        }}
                      >
                        <span>{segment.name}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div className="panchang-cosmic-map__windows">
              {cosmicMap.timeWindows.map((window) => (
                <div
                  key={`${window.label}-${window.start}`}
                  className={`panchang-cosmic-map__window panchang-cosmic-map__window--${window.tone}`}
                  style={{
                    left: `${buildTimelinePosition(window.start, cosmicMap.dayStartHour, cosmicMap.dayEndHour)}%`,
                    width: `${buildTimelinePosition(window.end, cosmicMap.dayStartHour, cosmicMap.dayEndHour) - buildTimelinePosition(window.start, cosmicMap.dayStartHour, cosmicMap.dayEndHour)}%`,
                  }}
                >
                  <span>{window.label}</span>
                </div>
              ))}
            </div>

            <div className="panchang-cosmic-map__cursor" style={{ left: `${focusLeft}%` }}>
              <div className="panchang-cosmic-map__cursor-ring" />
              <div className="panchang-cosmic-map__cursor-dot" />
            </div>

            <div className="panchang-cosmic-map__lens" style={{ left: `${clamp(focusLeft, 18, 82)}%` }}>
              <div className="panchang-cosmic-map__lens-glow" />
              <div className="panchang-cosmic-map__lens-card">
                <p className="panchang-cosmic-map__lens-time">{formatHour(focusHour)}</p>
                <h3>{buildLensTitle(activeWindow)}</h3>
                <p>
                  Solar intensity is at <strong>{Math.round(intensity * 100)}%</strong> of the day peak.
                </p>
                <div className="panchang-cosmic-map__lens-grid">
                  {activeRows.map((row) => (
                    <div key={row.label}>
                      <span>{row.label}</span>
                      <strong>{row.segment?.name || "Unavailable"}</strong>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ) : null}
      </section>

      <section className="panchang-shell panchang-hero">
        <p className="panchang-eyebrow">{copy.landingEyebrow}</p>
        <h1>{copy.landingTitle}</h1>
        <p>{copy.landingBody}</p>
        <div className="panchang-hero__actions">
          <Link to={buildPanchangPath(language, "/today")} className="panchang-button">
            {copy.ctaToday}
          </Link>
          <Link to={buildPanchangPath(language, "/tomorrow")} className="panchang-button panchang-button--secondary">
            {copy.ctaTomorrow}
          </Link>
          <Link to={buildPanchangPath(language, `/calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}`)} className="panchang-button panchang-button--secondary">
            {copy.ctaCalendar}
          </Link>
        </div>
      </section>

      <section className="panchang-grid panchang-grid--double">
        <article className="panchang-card">
          <p className="panchang-card__label">Tamil Panchangam</p>
          <h2>Calendar-first Tamil month browsing</h2>
          <p>Explore a Tamil Panchangam surface built for monthly discovery, daily date opening, and future Tamil calendar SEO depth.</p>
          <Link to={buildPanchangPath("ta", `/tamil-calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}`)} className="panchang-button panchang-button--secondary">
            Open Tamil Panchangam
          </Link>
        </article>

        <article className="panchang-card">
          <p className="panchang-card__label">Telugu Panchangam</p>
          <h2>Calendar-first Telugu month browsing</h2>
          <p>Open a dedicated Telugu Panchangam month view designed for repeat use, date-level linking, and regional search entry.</p>
          <Link to={buildPanchangPath("te", `/telugu-calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}`)} className="panchang-button panchang-button--secondary">
            Open Telugu Panchangam
          </Link>
        </article>
      </section>

      <section className="panchang-grid panchang-grid--triple">
        <article className="panchang-card">
          <p className="panchang-card__label">Daily Utility</p>
          <h2>Today, tomorrow, and next observances</h2>
          <p>Open the day view for sunrise, sunset, tithi, nakshatra, yoga, karana, and day-quality windows.</p>
          <Link to={buildPanchangPath(language, "/today")} className="panchang-button">
            {copy.ctaToday}
          </Link>
        </article>
        <article className="panchang-card">
          <p className="panchang-card__label">Festival Discovery</p>
          <h2>Browse festival and vrat dates</h2>
          <p>Use the observance hub to move from one festival to exact date pages and monthly calendar views.</p>
          <Link to={buildPanchangPath(language, "/festivals")} className="panchang-button">
            {copy.navFestivals}
          </Link>
        </article>
        <article className="panchang-card">
          <p className="panchang-card__label">Calendar Depth</p>
          <h2>Month-level Hindu calendar navigation</h2>
          <p>Jump by month, browse observance-heavy dates, and use Panchang as a full utility suite instead of a single page.</p>
          <Link to={buildPanchangPath(language, `/calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}`)} className="panchang-button">
            {copy.navCalendar}
          </Link>
        </article>
      </section>
    </div>
  );
}

export default PanchangLandingPage;
