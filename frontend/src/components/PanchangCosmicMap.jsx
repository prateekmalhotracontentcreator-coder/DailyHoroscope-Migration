import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ─── Panchang name tables ─────────────────────────────────────────────────────
const TITHI_NAMES = [
  "Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami",
  "Ashtami","Navami","Dashami","Ekadashi","Dwadashi","Trayodashi","Chaturdashi",
  "Purnima","Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashthi",
  "Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi","Trayodashi",
  "Chaturdashi","Amavasya",
];
const NAKSHATRA_NAMES = [
  "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu",
  "Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta",
  "Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha",
  "Uttara Ashadha","Shravana","Dhanishtha","Shatabhisha","Purva Bhadrapada",
  "Uttara Bhadrapada","Revati",
];
const YOGA_NAMES = [
  "Vishkambha","Priti","Ayushman","Saubhagya","Shobhana","Atiganda","Sukarma",
  "Dhriti","Shoola","Ganda","Vriddhi","Dhruva","Vyaghata","Harshana","Vajra",
  "Siddhi","Vyatipata","Variyana","Parigha","Shiva","Siddha","Sadhya","Shubha",
  "Shukla","Brahma","Indra","Vaidhriti",
];
const KARANA_NAMES = [
  "Kimstughna","Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti",
  "Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti","Bava","Balava",
  "Kaulava","Taitila","Garaja","Vanija","Vishti","Bava","Balava","Kaulava",
  "Taitila","Garaja","Vanija","Vishti","Shakuni","Chatushpada","Naga","Kimstughna",
];

const ROW_TONES   = { Tithi:"warm", Nakshatra:"sage", Yoga:"gold", Karana:"night" };
const WINDOW_TONES = {
  "Rahu Kaal":"alert", Yamaganda:"alert", "Gulika Kaal":"warm",
  "Abhijit Muhurta":"gold", "Dur Muhurta":"alert", "Amrit Kalam":"sage",
  Varjyam:"alert",
};

// ─── Pure helpers ─────────────────────────────────────────────────────────────
function clamp(v, lo, hi) { return Math.min(Math.max(v, lo), hi); }

function formatHour(value) {
  const n = ((value % 24) + 24) % 24;
  const h = Math.floor(n);
  const m = Math.round((n - h) * 60);
  const sm = m === 60 ? 0 : m;
  const sh = m === 60 ? (h + 1) % 24 : h;
  const suffix = sh >= 12 ? "PM" : "AM";
  const t = ((sh + 11) % 12) + 1;
  return `${t}:${String(sm).padStart(2, "0")} ${suffix}`;
}

function hourFromDate(iso) {
  const d = new Date(iso);
  return d.getHours() + d.getMinutes() / 60 + d.getSeconds() / 3600;
}

function hourFromClock(dateVal, clock) {
  const [h, m] = clock.split(":").map(Number);
  const d = new Date(`${dateVal}T00:00:00`);
  d.setHours(h, m, 0, 0);
  return d.getHours() + d.getMinutes() / 60;
}

function pct(hour, dayStart, dayEnd) {
  return ((hour - dayStart) / Math.max(dayEnd - dayStart, 1)) * 100;
}

function solarIntensity(hour, rise, set) {
  const n = (hour - rise) / Math.max(set - rise, 0.1);
  if (n <= 0 || n >= 1) return 0;
  return Math.sin(n * Math.PI);
}

function nextName(names, idx) { return names[idx % names.length]; }

function buildRowSegments(label, segment, dayStart, dayEnd, names) {
  if (!segment) return [];
  const startH = segment.start ? hourFromDate(segment.start) : dayStart;
  const endH   = segment.end   ? hourFromDate(segment.end)   : dayEnd;
  const vs = clamp(startH, dayStart, dayEnd);
  const ve = clamp(endH,   dayStart, dayEnd);
  const segs = [];
  if (ve > vs) segs.push({ start: vs, end: ve, name: segment.name, tone: ROW_TONES[label] || "gold" });
  if (segment.end && endH < dayEnd)
    segs.push({ start: clamp(endH, dayStart, dayEnd), end: dayEnd, name: nextName(names, segment.index), tone: "gold" });
  if (!segs.length)
    segs.push({ start: dayStart, end: dayEnd, name: segment.name, tone: ROW_TONES[label] || "gold" });
  return segs;
}

function buildWindowSegments(day, dayStart, dayEnd) {
  return [...(day.day_quality_windows || []), ...(day.special_timing_windows || [])]
    .map(w => ({
      label: w.label,
      start: clamp(hourFromDate(w.start), dayStart, dayEnd),
      end:   clamp(hourFromDate(w.end),   dayStart, dayEnd),
      tone:  WINDOW_TONES[w.label] || "warm",
    }))
    .filter(w => w.end > w.start);
}

function getActiveSegment(row, hour) {
  return row.segments.find(s => hour >= s.start && hour < s.end) || row.segments[row.segments.length - 1];
}

// ─── Date helpers ─────────────────────────────────────────────────────────────
function getDateISO(dayOffset = 0) {
  const d = new Date(Date.now() + dayOffset * 86400000);
  try {
    const parts = new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Kolkata",
      year: "numeric", month: "2-digit", day: "2-digit",
    }).formatToParts(d);
    const map = Object.fromEntries(parts.map(p => [p.type, p.value]));
    return `${map.year}-${map.month}-${map.day}`;
  } catch {
    return d.toISOString().slice(0, 10);
  }
}

// ─── Component ────────────────────────────────────────────────────────────────
export default function PanchangCosmicMap({ locationSlug = "new-delhi-india", dayOffset = 0 }) {
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState("");
  const [day,     setDay]     = useState(null);
  const [focusHour, setFocusHour] = useState(12);

  useEffect(() => {
    let active = true;
    setLoading(true); setError(""); setDay(null);
    const dateStr = getDateISO(dayOffset);
    axios
      .get(`${API}/panchang/daily`, { params: { location_slug: locationSlug, date: dateStr } })
      .then(r  => { if (active) setDay(r.data); })
      .catch(e => { if (active) setError(e?.response?.data?.detail || "Unable to load Panchang time map."); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [locationSlug, dayOffset]);

  const cosmicMap = useMemo(() => {
    if (!day) return null;
    const sunriseH  = hourFromClock(day.date, day.summary.sunrise);
    const sunsetH   = hourFromClock(day.date, day.summary.sunset);
    const dayStart  = Math.max(Math.floor(sunriseH) - 1, 0);
    const dayEnd    = Math.min(Math.ceil(sunsetH)   + 1, 24);
    const timeRows  = [
      { label:"Tithi",     segments: buildRowSegments("Tithi",     day.panchang?.tithi,    dayStart, dayEnd, TITHI_NAMES)    },
      { label:"Nakshatra", segments: buildRowSegments("Nakshatra", day.panchang?.nakshatra,dayStart, dayEnd, NAKSHATRA_NAMES) },
      { label:"Yoga",      segments: buildRowSegments("Yoga",      day.panchang?.yoga,     dayStart, dayEnd, YOGA_NAMES)     },
      { label:"Karana",    segments: buildRowSegments("Karana",    day.panchang?.karana,   dayStart, dayEnd, KARANA_NAMES)   },
    ];
    const timeWindows   = buildWindowSegments(day, dayStart, dayEnd);
    const focusDefault  =
      timeWindows.find(w => w.label === "Abhijit Muhurta") ||
      timeWindows.find(w => w.label === "Amrit Kalam")     ||
      { start: (sunriseH + sunsetH) / 2, end: (sunriseH + sunsetH) / 2 };
    return { sunriseH, sunsetH, dayStart, dayEnd, timeRows, timeWindows,
             suggestedFocus: (focusDefault.start + focusDefault.end) / 2 };
  }, [day]);

  useEffect(() => {
    if (cosmicMap) setFocusHour(cosmicMap.suggestedFocus);
  }, [cosmicMap]);

  const activeRows = useMemo(
    () => cosmicMap
      ? cosmicMap.timeRows.map(row => ({ label: row.label, segment: getActiveSegment(row, focusHour) }))
      : [],
    [cosmicMap, focusHour],
  );

  const activeWindow = useMemo(
    () => cosmicMap?.timeWindows.find(w => focusHour >= w.start && focusHour <= w.end) || null,
    [cosmicMap, focusHour],
  );

  const focusLeft = cosmicMap ? pct(focusHour, cosmicMap.dayStart, cosmicMap.dayEnd) : 50;
  const intensity = cosmicMap ? solarIntensity(focusHour, cosmicMap.sunriseH, cosmicMap.sunsetH) : 0;

  function updateFocus(e) {
    if (!cosmicMap) return;
    const bounds = e.currentTarget.getBoundingClientRect();
    const ratio  = clamp((e.clientX - bounds.left) / bounds.width, 0, 1);
    setFocusHour(cosmicMap.dayStart + ratio * (cosmicMap.dayEnd - cosmicMap.dayStart));
  }

  function updateFocusTouch(e) {
    if (!cosmicMap) return;
    const touch  = e.touches[0];
    if (!touch) return;
    const bounds = e.currentTarget.getBoundingClientRect();
    const ratio  = clamp((touch.clientX - bounds.left) / bounds.width, 0, 1);
    setFocusHour(cosmicMap.dayStart + ratio * (cosmicMap.dayEnd - cosmicMap.dayStart));
  }

  return (
    <section className="panchang-shell panchang-cosmic-map">
      <div className="panchang-cosmic-map__header">
        <div>
          <p className="panchang-eyebrow">Time Map</p>
          <h2>{day ? `${day.location.label} — ${day.date}` : "The living Panchang across a single day"}</h2>
        </div>
        <div className="panchang-cosmic-map__header-meta">
          <p className="panchang-cosmic-map__subcopy">
            {day
              ? "The cosmic map reads directly from the live daily Panchang — sunrise, core limbs, and timing windows."
              : "Move across the parchment to inspect sunrise, solar intensity, and the active Panchang layers in one interactive lens."}
          </p>
        </div>
      </div>

      {loading && <div className="panchang-cosmic-map__status">Loading live Panchang time map…</div>}
      {error   && <div className="panchang-cosmic-map__status panchang-error">{error}</div>}

      {cosmicMap && (
        <div
          className="panchang-cosmic-map__frame"
          onMouseMove={updateFocus}
          onPointerMove={updateFocus}
          onTouchMove={updateFocusTouch}
        >
          {/* Sun band + markers */}
          <div className="panchang-cosmic-map__sunband">
            <div className="panchang-cosmic-map__sunband-fill" />
            <div
              className="panchang-cosmic-map__sun-marker panchang-cosmic-map__sun-marker--rise"
              style={{ left: `${pct(cosmicMap.sunriseH, cosmicMap.dayStart, cosmicMap.dayEnd)}%` }}
            >
              <span>Sunrise</span>
              <strong>{day.summary.sunrise}</strong>
            </div>
            <div
              className="panchang-cosmic-map__sun-marker panchang-cosmic-map__sun-marker--set"
              style={{ left: `${pct(cosmicMap.sunsetH, cosmicMap.dayStart, cosmicMap.dayEnd)}%` }}
            >
              <span>Sunset</span>
              <strong>{day.summary.sunset}</strong>
            </div>
          </div>

          {/* Solar arc SVG */}
          <svg className="panchang-cosmic-map__curve" viewBox="0 0 1000 180" preserveAspectRatio="none" aria-hidden="true">
            <defs>
              <linearGradient id="solarCurveMap" x1="0%" x2="100%">
                <stop offset="0%"   stopColor="#d99834" />
                <stop offset="45%"  stopColor="#ffe27f" />
                <stop offset="100%" stopColor="#c7652e" />
              </linearGradient>
            </defs>
            <path d="M 40 136 Q 250 44 500 32 Q 760 44 960 136"
              fill="none" stroke="url(#solarCurveMap)" strokeWidth="6" strokeLinecap="round" />
            <path d="M 40 136 Q 250 44 500 32 Q 760 44 960 136"
              fill="rgba(233,190,98,0.12)" stroke="none" />
          </svg>

          {/* Hour ticks */}
          <div className="panchang-cosmic-map__hours">
            {Array.from({ length: cosmicMap.dayEnd - cosmicMap.dayStart + 1 }).map((_, i) => {
              const h = cosmicMap.dayStart + i;
              return (
                <span key={h} style={{ left: `${(i / Math.max(cosmicMap.dayEnd - cosmicMap.dayStart, 1)) * 100}%` }}>
                  {h}
                </span>
              );
            })}
          </div>

          {/* Panchang limb tracks */}
          <div className="panchang-cosmic-map__rows">
            {cosmicMap.timeRows.map(row => (
              <div key={row.label} className="panchang-cosmic-map__row">
                <span className="panchang-cosmic-map__row-label">{row.label}</span>
                <div className="panchang-cosmic-map__track">
                  {row.segments.map(seg => (
                    <div
                      key={`${row.label}-${seg.name}-${seg.start}`}
                      className={`panchang-cosmic-map__segment panchang-cosmic-map__segment--${seg.tone}`}
                      style={{
                        left:  `${pct(seg.start, cosmicMap.dayStart, cosmicMap.dayEnd)}%`,
                        width: `${pct(seg.end, cosmicMap.dayStart, cosmicMap.dayEnd) - pct(seg.start, cosmicMap.dayStart, cosmicMap.dayEnd)}%`,
                      }}
                    >
                      <span>{seg.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Timing windows strip */}
          <div className="panchang-cosmic-map__windows">
            {cosmicMap.timeWindows.map(w => (
              <div
                key={`${w.label}-${w.start}`}
                className={`panchang-cosmic-map__window panchang-cosmic-map__window--${w.tone}`}
                style={{
                  left:  `${pct(w.start, cosmicMap.dayStart, cosmicMap.dayEnd)}%`,
                  width: `${pct(w.end, cosmicMap.dayStart, cosmicMap.dayEnd) - pct(w.start, cosmicMap.dayStart, cosmicMap.dayEnd)}%`,
                }}
              >
                <span>{w.label}</span>
              </div>
            ))}
          </div>

          {/* Pulsating cursor */}
          <div className="panchang-cosmic-map__cursor" style={{ left: `${focusLeft}%` }}>
            <div className="panchang-cosmic-map__cursor-ring" />
            <div className="panchang-cosmic-map__cursor-dot"  />
          </div>

          {/* Zoom-lens card */}
          <div className="panchang-cosmic-map__lens" style={{ left: `${clamp(focusLeft, 18, 82)}%` }}>
            <div className="panchang-cosmic-map__lens-glow" />
            <div className="panchang-cosmic-map__lens-card">
              <p className="panchang-cosmic-map__lens-time">{formatHour(focusHour)}</p>
              <h3>{activeWindow ? activeWindow.label : "Live Panchang balance"}</h3>
              <p>Solar intensity is at <strong>{Math.round(intensity * 100)}%</strong> of the day peak.</p>
              <div className="panchang-cosmic-map__lens-grid">
                {activeRows.map(row => (
                  <div key={row.label}>
                    <span>{row.label}</span>
                    <strong>{row.segment?.name || "—"}</strong>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
