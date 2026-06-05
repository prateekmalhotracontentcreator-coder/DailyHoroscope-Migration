import React, { useEffect, useMemo, useRef, useState, useCallback } from "react";
import axios from "axios";

const BACKEND_URL  = process.env.REACT_APP_BACKEND_URL;
const PUBLIC_URL   = process.env.PUBLIC_URL || "";
const API = `${BACKEND_URL}/api`;

// ── Day axis: computed dynamically from location sunrise/sunset ───────────────
// No hardcoded constants -- every city uses its own local day range.

// ── Panchang name tables (same as PanchangCosmicMap) ─────────────────────────
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

// ── Pure helpers ───────────────────────────────────────────────────────────────
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

// Extract city-local hour directly from the ISO string's time portion.
// The backend generates timestamps in the queried city's local timezone
// (e.g. "2026-06-05T07:38:00+02:00" for Zurich). Reading new Date(iso).getHours()
// would re-interpret that in the USER's browser timezone -- wrong for every
// non-local visitor. We extract the T-prefixed time portion instead, which
// is always the correct city-local hour.
function hourFromISO(iso) {
  const match = iso && iso.match(/T(\d{2}):(\d{2}):(\d{2})/);
  if (match) {
    return parseInt(match[1], 10) + parseInt(match[2], 10) / 60 + parseInt(match[3], 10) / 3600;
  }
  // Fallback: should not be reached with well-formed API responses
  const d = new Date(iso);
  return d.getUTCHours() + d.getUTCMinutes() / 60;
}

// Clock strings like "05:23" from day.summary are already city-local -- just parse numbers.
function hourFromClock(clock) {
  const parts = clock.replace(/[^\d:]/g, "").split(":");
  return parseInt(parts[0], 10) + (parseInt(parts[1], 10) || 0) / 60;
}

// Converts decimal hour to % on a given axis (clamped 0-100)
function pct(hour, axisStart, axisEnd) {
  return clamp((hour - axisStart) / Math.max(axisEnd - axisStart, 1) * 100, 0, 100);
}

// Build city-appropriate hour ticks from axisStart to axisEnd
function buildHourTicks(axisStart, axisEnd) {
  const hours = Math.round(axisEnd - axisStart);
  return Array.from({ length: hours + 1 }, (_, i) => {
    const h = axisStart + i;
    const p = hours > 0 ? (i / hours) * 100 : 0;
    // Label every even hour; force label on first, last, noon, midnight
    const isKey = h === axisStart || h === axisEnd || h === 12 || h === 0;
    const showLabel = isKey || i % 2 === 0;
    let label = "";
    if (showLabel) {
      if (h === 0 || h === 24) label = "12am";
      else if (h === 12)       label = "12pm";
      else if (h < 12)         label = `${h}am`;
      else                     label = `${h - 12}pm`;
    }
    return { hour: h, pct: p, label };
  });
}

function solarIntensity(hour, rise, set) {
  const n = (hour - rise) / Math.max(set - rise, 0.1);
  if (n <= 0 || n >= 1) return 0;
  return Math.sin(n * Math.PI);
}

function nextName(names, idx) { return names[idx % names.length]; }

function buildRowSegments(segment, names, axisStart, axisEnd) {
  if (!segment) return [];
  const startH = segment.start ? hourFromISO(segment.start) : axisStart;
  const endH   = segment.end   ? hourFromISO(segment.end)   : axisEnd;
  const vs = clamp(startH, axisStart, axisEnd);
  const ve = clamp(endH,   axisStart, axisEnd);
  const segs = [];
  if (ve > vs) segs.push({ start: vs, end: ve, name: segment.name });
  if (segment.end && endH < axisEnd)
    segs.push({ start: clamp(endH, axisStart, axisEnd), end: axisEnd, name: nextName(names, segment.index) });
  if (!segs.length)
    segs.push({ start: axisStart, end: axisEnd, name: segment.name });
  return segs;
}

// Quality mapping from API tone → pill quality
const TONE_QUALITY = {
  alert: "caution", sage: "good", gold: "good", warm: "neutral",
};
function windowQuality(w) {
  if (w.quality === "good")    return "good";
  if (w.quality === "caution") return "caution";
  return TONE_QUALITY[w.tone] || "neutral";
}

// Greedy lane-packing by percent ranges (no DOM measurement needed)
function packWindowsIntoLanes(windows) {
  const lanes = [];
  windows.forEach(w => {
    const lo = w.leftPct;
    const hi = w.leftPct + w.widthPct;
    let placed = false;
    for (const lane of lanes) {
      const last = lane[lane.length - 1];
      if (lo >= last.leftPct + last.widthPct + 1) {
        lane.push(w);
        placed = true;
        break;
      }
    }
    if (!placed) lanes.push([w]);
  });
  return lanes;
}

// Hour ticks are built dynamically per location in the ptmData memo.

function formatLongDate(iso) {
  try {
    // Parse as noon UTC to avoid date rollover for any timezone
    const d = new Date(`${iso}T12:00:00Z`);
    return d.toLocaleDateString("en-IN", { weekday: "long", day: "numeric", month: "long", year: "numeric", timeZone: "UTC" });
  } catch { return iso; }
}

// ── Date helpers ───────────────────────────────────────────────────────────────
function getDateISO(dayOffset = 0) {
  const d = new Date(Date.now() + dayOffset * 86400000);
  try {
    const parts = new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Kolkata", year: "numeric", month: "2-digit", day: "2-digit",
    }).formatToParts(d);
    const map = Object.fromEntries(parts.map(p => [p.type, p.value]));
    return `${map.year}-${map.month}-${map.day}`;
  } catch { return d.toISOString().slice(0, 10); }
}

// ── State derivation from focusPct ────────────────────────────────────────────
function subline(quality) {
  if (quality === "good")    return "Safe Start Window";
  if (quality === "caution") return "Avoid";
  return "Neutral";
}

function getStateAtPct(focusPct, windows, sunrisePct, sunsetPct, axisStart, axisEnd) {
  const inside = windows.filter(w => focusPct >= w.leftPct && focusPct <= w.leftPct + w.widthPct);
  inside.sort((a, b) => {
    if (a.quality === "good" && b.quality !== "good") return -1;
    if (b.quality === "good" && a.quality !== "good") return 1;
    return a.widthPct - b.widthPct;
  });
  const w = inside[0] || null;

  // Interpolate city-local decimal hour from focusPct using the location's axis
  const span = axisEnd - axisStart;
  const decimalHour = axisStart + (focusPct / 100) * span;
  const rise = axisStart + (sunrisePct / 100) * span;
  const set  = axisStart + (sunsetPct  / 100) * span;
  const sol  = solarIntensity(decimalHour, rise, set);

  return {
    timeLabel: formatHour(decimalHour),
    activeWindow: w ? { label: w.label, quality: w.quality, timeRange: w.timeRange, subline: subline(w.quality) } : null,
    solarIntensity: sol,
    glassTint: w ? (w.quality === "neutral" ? null : w.quality) : null,
  };
}

// ── Clock SVG (inline) ────────────────────────────────────────────────────────
const ClockSVG = () => (
  <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
    <circle cx="8" cy="8" r="6.5" stroke="rgba(255,255,255,0.85)" strokeWidth="1.3"/>
    <line x1="8" y1="8" x2="8" y2="3.8" stroke="rgba(255,255,255,0.9)" strokeWidth="1.4" strokeLinecap="round"/>
    <line x1="8" y1="8" x2="11" y2="9.6" stroke="rgba(255,255,255,0.9)" strokeWidth="1.4" strokeLinecap="round"/>
  </svg>
);

const SunSVG = ({ color }) => (
  <svg width="15" height="15" viewBox="0 0 16 16" fill="none">
    <circle cx="8" cy="8" r="3.4" fill={color}/>
    <g stroke={color} strokeWidth="1.2" strokeLinecap="round">
      <line x1="8" y1="1" x2="8" y2="2.8"/><line x1="8" y1="13.2" x2="8" y2="15"/>
      <line x1="1" y1="8" x2="2.8" y2="8"/><line x1="13.2" y1="8" x2="15" y2="8"/>
      <line x1="3" y1="3" x2="4.3" y2="4.3"/><line x1="11.7" y1="11.7" x2="13" y2="13"/>
      <line x1="13" y1="3" x2="11.7" y2="4.3"/><line x1="4.3" y1="11.7" x2="3" y2="13"/>
    </g>
  </svg>
);

const MoonSVG = () => (
  <svg width="15" height="15" viewBox="0 0 16 16" fill="none">
    <path d="M11 2.2a6 6 0 1 0 2.8 7.4A4.7 4.7 0 0 1 11 2.2Z" fill="#7E92AE"/>
  </svg>
);

// ── Component ─────────────────────────────────────────────────────────────────
export default function PanchangCosmicMapV2({ locationSlug = "new-delhi-india", dayOffset = 0 }) {
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState("");
  const [day,      setDay]      = useState(null);
  const [focusPct, setFocusPct] = useState(50);

  const consoleRef = useRef(null);

  // ── Fetch ──────────────────────────────────────────────────────────────────
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

  // ── Shape the live data into the ptm data contract ─────────────────────────
  const ptmData = useMemo(() => {
    if (!day) return null;

    // City-local hours -- parse clock strings directly (already local time from API)
    const sunriseH = hourFromClock(day.summary.sunrise);
    const sunsetH  = hourFromClock(day.summary.sunset);

    // Dynamic day axis: 1h before sunrise, 2h after sunset, clamped 0-24.
    // This ensures all cities (London midsummer sunset 21:20, etc.) show all windows.
    const axisStart = Math.max(Math.floor(sunriseH) - 1, 0);
    const axisEnd   = Math.min(Math.ceil(sunsetH)   + 2, 24);

    const sunrisePct = pct(sunriseH, axisStart, axisEnd);
    const sunsetPct  = pct(sunsetH,  axisStart, axisEnd);

    // Build windows -- hourFromISO extracts city-local time from the ISO offset string,
    // so "07:38:00+02:00" (Zurich) and "07:38:00+05:30" (Delhi) both yield 7.633h correctly
    // regardless of what timezone the user's browser is in.
    const rawWindows = [...(day.day_quality_windows || []), ...(day.special_timing_windows || [])];
    const windows = rawWindows
      .map(w => {
        const startH = hourFromISO(w.start);
        const endH   = hourFromISO(w.end);
        const lp = pct(startH, axisStart, axisEnd);
        const wp = pct(endH,   axisStart, axisEnd) - lp;
        if (wp <= 0) return null;
        return {
          label:     w.label,
          quality:   windowQuality(w),
          leftPct:   lp,
          widthPct:  wp,
          timeRange: `${formatHour(startH)} - ${formatHour(endH)}`,
        };
      })
      .filter(Boolean);

    // Build limb rows (Tithi / Nakshatra / Yoga / Karana)
    const limbDefs = [
      { label: "Tithi",     segment: day.panchang?.tithi,     names: TITHI_NAMES     },
      { label: "Nakshatra", segment: day.panchang?.nakshatra, names: NAKSHATRA_NAMES  },
      { label: "Yoga",      segment: day.panchang?.yoga,      names: YOGA_NAMES      },
      { label: "Karana",    segment: day.panchang?.karana,    names: KARANA_NAMES    },
    ];
    const limbRows = limbDefs.map(def => ({
      label: def.label,
      tone:  def.label.toLowerCase(),
      segments: buildRowSegments(def.segment, def.names, axisStart, axisEnd).map(s => ({
        name:     s.name,
        leftPct:  pct(s.start, axisStart, axisEnd),
        widthPct: pct(s.end,   axisStart, axisEnd) - pct(s.start, axisStart, axisEnd),
      })),
    }));

    // Build hour ticks for this city's actual day span
    const hourTicks = buildHourTicks(axisStart, axisEnd);

    // Suggested focus: Abhijit Muhurta midpoint, else Amrit Kalam, else midday
    const focus = windows.find(w => w.label === "Abhijit Muhurta")
               || windows.find(w => w.label === "Amrit Kalam")
               || { leftPct: pct(12, axisStart, axisEnd), widthPct: 0 };
    const suggestedFocusPct = focus.leftPct + focus.widthPct / 2;

    return {
      locationLabel: day.location?.label ?? locationSlug,
      dateLabel:     formatLongDate(day.date),
      sunriseLabel:  day.summary.sunrise,
      sunsetLabel:   day.summary.sunset,
      moonriseLabel: day.summary.moonrise ?? "-",
      pakshaLabel:   day.panchang?.paksha ?? "",
      sunrisePct,
      sunsetPct,
      axisStart,
      axisEnd,
      windows,
      limbRows,
      hourTicks,
      suggestedFocusPct,
    };
  }, [day, locationSlug]);

  // ── Set initial focus when data arrives ────────────────────────────────────
  useEffect(() => {
    if (ptmData) setFocusPct(ptmData.suggestedFocusPct);
  }, [ptmData]);

  // ── Current state at focusPct ──────────────────────────────────────────────
  const focusState = useMemo(() => {
    if (!ptmData) return null;
    return getStateAtPct(focusPct, ptmData.windows, ptmData.sunrisePct, ptmData.sunsetPct, ptmData.axisStart, ptmData.axisEnd);
  }, [focusPct, ptmData]);

  // ── Active window / limb segment highlights ────────────────────────────────
  const activeWindowLabel = focusState?.activeWindow?.label ?? null;
  const activeLimbMap = useMemo(() => {
    if (!ptmData || !focusState) return {};
    const map = {};
    ptmData.limbRows.forEach(row => {
      const seg = row.segments.find(
        s => focusPct >= s.leftPct && focusPct < s.leftPct + s.widthPct
      ) || row.segments[row.segments.length - 1];
      if (seg) map[row.tone] = seg.name;
    });
    return map;
  }, [ptmData, focusPct, focusState]);

  // ── Packed lanes for window pills ─────────────────────────────────────────
  const windowLanes = useMemo(() => {
    if (!ptmData) return [];
    return packWindowsIntoLanes([...ptmData.windows].sort((a, b) => a.leftPct - b.leftPct));
  }, [ptmData]);

  // ── Interaction ────────────────────────────────────────────────────────────
  const updateFocus = useCallback((clientX) => {
    if (!consoleRef.current || !ptmData) return;
    const rect = consoleRef.current.getBoundingClientRect();
    // The track span is inset --tl (13.6%) from left and --tr (13.3%) from right
    const TL = 0.136, TR = 0.133;
    const L  = rect.left + TL * rect.width;
    const W  = (1 - TL - TR) * rect.width;
    const raw = (clientX - L) / W;
    setFocusPct(clamp(raw, 0, 1) * 100);
  }, [ptmData]);

  const handleMouseMove = useCallback((e) => updateFocus(e.clientX), [updateFocus]);
  const handleTouchMove = useCallback((e) => {
    e.preventDefault();
    if (e.touches[0]) updateFocus(e.touches[0].clientX);
  }, [updateFocus]);

  // ── Guidance tier ──────────────────────────────────────────────────────────
  const guidance = useMemo(() => {
    if (!focusState) return { tier: "default", icon: "◉", text: "Loading..." };
    const w = focusState.activeWindow;
    if (w && w.quality === "good") return {
      tier: "auspicious", icon: "✦",
      text: `${w.label} is active now (${w.timeRange}) -- a safe window to initiate critical ventures. Act with precision while it holds.`,
    };
    if (w && w.quality === "caution") return {
      tier: "inauspicious", icon: "⚠",
      text: `Critical: ${w.label} is active (${w.timeRange}). Avoid starting new ventures or signing contracts until it passes.`,
    };
    return {
      tier: "default", icon: "◉",
      text: `Open sky at ${focusState.timeLabel} -- no special timing window is active. Proceed with ordinary care.`,
    };
  }, [focusState]);

  // ── Cursor + lens position ─────────────────────────────────────────────────
  const TL = 13.6, TR = 13.3;
  const cursorLeft = `calc(${TL}% + ${(1 - (TL + TR) / 100) * 100}% * ${focusPct / 100})`;
  const lensRaw    = clamp(focusPct / 100, 0.06, 0.94);
  const lensLeft   = `calc(${TL}% + ${(1 - (TL + TR) / 100) * 100}% * ${lensRaw})`;

  // ── Render ─────────────────────────────────────────────────────────────────
  return (
    <section className="ptm-shell">
      {/* Header */}
      <header className="ptm-header">
        <p className="ptm-eyebrow">Time Map · The Cosmic Clock</p>
        <h2 className="ptm-title">
          {ptmData ? `${ptmData.locationLabel} -- ${ptmData.dateLabel}` : "The Cosmic Clock"}
        </h2>
        <p className="ptm-subtitle">Move across the scroll to inspect any moment of the day.</p>
      </header>

      {loading && <div className="ptm-status">Loading live Panchang time map...</div>}
      {error   && <div className="ptm-status ptm-status--error">{error}</div>}

      {ptmData && (
        <>
          {/* Parchment console */}
          <div
            className="ptm-console"
            ref={consoleRef}
            onMouseMove={handleMouseMove}
            onTouchMove={handleTouchMove}
            style={{ backgroundImage: `url(${PUBLIC_URL}/panchang/time-banner.png)`, backgroundRepeat: "no-repeat", backgroundPosition: "center", backgroundSize: "100% 100%" }}
          >
            <div className="ptm-stage">
              {/* Magnifying lens */}
              <div className="ptm-lens" style={{ left: lensLeft }}>
                <div className="ptm-lens__art" style={{ backgroundImage: `url(${PUBLIC_URL}/panchang/zoom-lens-cut.png)`, backgroundRepeat: "no-repeat", backgroundPosition: "center", backgroundSize: "contain" }} />
                <div className="ptm-lens__glass" data-tint={focusState?.glassTint || ""}>
                  <div className="ptm-lens__content">
                    <p className="ptm-lens__time">
                      {focusState?.timeLabel} · Solar {Math.round((focusState?.solarIntensity || 0) * 100)}%
                    </p>
                    {focusState?.activeWindow ? (
                      <>
                        <h3 className="ptm-lens__name">{focusState.activeWindow.label}</h3>
                        <p className={`ptm-lens__subline ptm-lens__subline--${focusState.activeWindow.quality}`}>
                          {focusState.activeWindow.subline}
                        </p>
                        <p className="ptm-lens__range">{focusState.activeWindow.timeRange}</p>
                      </>
                    ) : (
                      <>
                        <h3 className="ptm-lens__name">Open Sky</h3>
                        <p className="ptm-lens__subline ptm-lens__subline--good">No restrictions active</p>
                      </>
                    )}
                  </div>
                </div>
              </div>

              <div className="ptm-chart">
                {/* Almanac strip */}
                <div className="ptm-almanac">
                  <div className="ptm-alm">
                    <SunSVG color="#E0922A" />
                    <span>Sunrise</span>
                    <b>{ptmData.sunriseLabel}</b>
                  </div>
                  <div className="ptm-alm">
                    <SunSVG color="#B5642A" />
                    <span>Sunset</span>
                    <b>{ptmData.sunsetLabel}</b>
                  </div>
                  {ptmData.moonriseLabel && ptmData.moonriseLabel !== "--" && (
                    <div className="ptm-alm">
                      <MoonSVG />
                      <span>Moonrise</span>
                      <b>{ptmData.moonriseLabel}</b>
                    </div>
                  )}
                  {ptmData.pakshaLabel && (
                    <div className="ptm-alm">
                      <span>Paksha</span>
                      <b>{ptmData.pakshaLabel}</b>
                    </div>
                  )}
                </div>

                {/* Time-bar spine (art) */}
                <div className="ptm-bar" style={{ backgroundImage: `url(${PUBLIC_URL}/panchang/time-bar-spine.png)`, backgroundRepeat: "no-repeat", backgroundPosition: "center", backgroundSize: "100% 100%" }} />

                {/* Hour labels -- city-local, built from dynamic axis */}
                <div className="ptm-ticks">
                  {ptmData.hourTicks.map(tick => (
                    <span key={tick.hour} style={{ left: `${tick.pct}%` }}>
                      {tick.label}
                    </span>
                  ))}
                </div>

                {/* Window lanes */}
                <div className="ptm-lanes">
                  {windowLanes.map((lane, li) => (
                    <div key={li} className="ptm-lane">
                      {lane.map(w => (
                        <div
                          key={w.label}
                          className={`ptm-window ptm-window--${w.quality}${activeWindowLabel === w.label ? " is-active" : ""}`}
                          style={{ left: `${w.leftPct + w.widthPct / 2}%`, transform: "translateX(-50%)", minWidth: `${w.widthPct}%` }}
                          title={`${w.label} · ${w.timeRange}`}
                          onClick={() => setFocusPct(w.leftPct + w.widthPct / 2)}
                        >
                          {w.widthPct >= 16 && <ClockSVG />}
                          <span>{w.label}</span>
                        </div>
                      ))}
                    </div>
                  ))}
                </div>

                {/* Limb rows */}
                <div className="ptm-limbs">
                  {ptmData.limbRows.map(row => (
                    <div key={row.label} className="ptm-limb">
                      <span className="ptm-row-label">{row.label}</span>
                      <div className="ptm-limb__track">
                        {row.segments.map(seg => (
                          <div
                            key={`${row.tone}-${seg.name}-${seg.leftPct}`}
                            className={`ptm-seg ptm-seg--${row.tone}${seg.widthPct < 9 ? " ptm-seg--hide-label" : ""}${activeLimbMap[row.tone] === seg.name ? " is-active" : ""}`}
                            data-row={row.tone}
                            data-name={seg.name}
                            style={{ left: `${seg.leftPct}%`, width: `${seg.widthPct}%` }}
                          >
                            {seg.name}
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Cursor */}
                <div className="ptm-cursor" style={{ left: cursorLeft }}>
                  <div className="ptm-cursor__ring" />
                  <div className="ptm-cursor__dot" />
                </div>
              </div>
            </div>
          </div>

          {/* Critical guidance bar */}
          <div className={`ptm-guidance ptm-guidance--${guidance.tier}`}>
            <span className="ptm-guidance__icon">{guidance.icon}</span>
            <span>{guidance.text}</span>
          </div>
        </>
      )}
    </section>
  );
}
