import React, { startTransition, useDeferredValue, useEffect, useState } from "react";
import axios from "axios";
import { Link, useLocation, useNavigate } from "react-router-dom";
import SharedBirthCityPicker from "../../components/SharedBirthCityPicker";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const HISTORY_CACHE_KEY = "love_reports_cache_v1";

const LOVE_REPORTS = [
  { type: "love_weather", slug: "love-weather", label: "Love Weather", description: "90-day romantic forecast with best and caution dates", accent: "#b73c64", tint: "rgba(183, 60, 100, 0.12)", icon: "☁" },
  { type: "encounter_window", slug: "encounter-window", label: "Encounter Window", description: "Upcoming transit windows most likely to spark new meetings", accent: "#b73c64", tint: "rgba(183, 60, 100, 0.12)", icon: "✦" },
  { type: "date_night_score", slug: "date-night", label: "Date Night", description: "Daily Love Battery score and timing note for connection", accent: "#8b1e3c", tint: "rgba(139, 30, 60, 0.12)", icon: "☾" },
  { type: "digital_dating_strategy", slug: "digital-dating", label: "Digital Dating", description: "Optimise your profile, tone, and message timing with your chart", accent: "#8b1e3c", tint: "rgba(139, 30, 60, 0.12)", icon: "✉" },
  { type: "intimacy_vitality_forecast", slug: "intimacy-vitality", label: "Intimacy & Vitality", description: "Mars-Venus windows for depth, confidence, and romantic momentum", accent: "#8b1e3c", tint: "rgba(139, 30, 60, 0.12)", icon: "✧" },
  { type: "venus_retrograde_personal_impact", slug: "venus-retrograde", label: "Venus Retrograde", description: "How the current retrograde is reshaping your relationship themes", accent: "#9a6a26", tint: "rgba(215, 175, 106, 0.14)", icon: "♀" },
  { type: "soulmate_timing", slug: "soulmate-timing", label: "Soulmate Timing", description: "Jupiter and Dasha windows for long-term partnership", accent: "#9a6a26", tint: "rgba(215, 175, 106, 0.14)", icon: "⌛" },
  { type: "deep_synastry_soul_connection", slug: "soul-connection", label: "Soul Connection", description: "Karmic and evolutionary patterns in your relationships", accent: "#6a4b89", tint: "rgba(100, 60, 160, 0.12)", icon: "∞" },
];

const EMPTY_CITY = {
  slug: "",
  city_name: "",
  latitude: "",
  longitude: "",
  timezone: "",
};

const pageStyle = {
  minHeight: "100vh",
  background:
    "radial-gradient(circle at top left, rgba(183,60,100,0.16), transparent 24%), radial-gradient(circle at top right, rgba(100,60,160,0.12), transparent 18%), linear-gradient(180deg, #faf6ef 0%, #f4ede2 100%)",
  color: "#2a2119",
  padding: "28px 18px 72px",
};

const cardStyle = {
  background: "rgba(255,251,245,0.88)",
  border: "1px solid rgba(120,90,55,0.14)",
  borderRadius: 22,
  boxShadow: "0 18px 46px rgba(74,50,22,0.09)",
  backdropFilter: "blur(10px)",
};

const inputStyle = {
  minHeight: 46,
  borderRadius: 14,
  border: "1px solid rgba(120,90,55,0.16)",
  background: "rgba(255,255,255,0.88)",
  padding: "12px 14px",
  color: "#2a2119",
};

const primaryButtonStyle = {
  minHeight: 46,
  padding: "10px 16px",
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
  background: "rgba(255,255,255,0.72)",
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

function useProtectedSeo() {
  useEffect(() => {
    document.title = "Love Reports | Everyday Horoscope";
    ensureMeta('meta[name="robots"]', { name: "robots" }).setAttribute("content", "noindex, nofollow");
  }, []);
}

function queryParams(search) {
  return new URLSearchParams(search);
}

function loadCachedReports() {
  try {
    return JSON.parse(window.localStorage.getItem(HISTORY_CACHE_KEY) || "{}");
  } catch {
    return {};
  }
}

function saveCachedReport(report) {
  if (!report?.id) return;
  const current = loadCachedReports();
  current[report.id] = report;
  window.localStorage.setItem(HISTORY_CACHE_KEY, JSON.stringify(current));
}

function defaultPersonForm() {
  return {
    city_slug: EMPTY_CITY.slug,
    city_name: EMPTY_CITY.city_name,
    latitude: EMPTY_CITY.latitude,
    longitude: EMPTY_CITY.longitude,
    timezone: EMPTY_CITY.timezone,
    date_of_birth: "",
    time_of_birth: "",
  };
}

function defaultMetaForm() {
  return {
    lookahead_days: 90,
  };
}

function reportByQuery(value) {
  return LOVE_REPORTS.find((item) => item.slug === value || item.type === value) || LOVE_REPORTS[0];
}

function personPayload(form) {
  return {
    date_of_birth: form.date_of_birth,
    time_of_birth: form.time_of_birth,
    city_name: form.city_name || undefined,
    latitude: form.latitude === "" || form.latitude == null ? undefined : Number(form.latitude),
    longitude: form.longitude === "" || form.longitude == null ? undefined : Number(form.longitude),
    timezone: form.timezone || undefined,
  };
}

function buildPayload(selected, primaryForm, secondaryForm, metaForm) {
  if (selected.slug === "soul-connection") {
    return {
      person_a: personPayload(primaryForm),
      person_b: personPayload(secondaryForm),
    };
  }
  const base = personPayload(primaryForm);
  if (selected.slug === "love-weather") {
    return { ...base, lookahead_days: Number(metaForm.lookahead_days || 90) };
  }
  return base;
}

function prettifyDate(value) {
  if (!value) return "-";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleDateString();
}

function toList(value) {
  if (Array.isArray(value)) return value;
  if (!value) return [];
  return [value];
}

function TabBar({ activeTab, setActiveTab }) {
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
      {[
        ["select", "Select"],
        ["generate", "Generate"],
        ["report", "Report"],
        ["history", "History"],
      ].map(([key, label]) => (
        <button
          key={key}
          type="button"
          onClick={() => setActiveTab(key)}
          style={{
            minHeight: 44,
            padding: "10px 16px",
            borderRadius: 999,
            border: "1px solid rgba(120,90,55,0.16)",
            background: activeTab === key ? "linear-gradient(135deg, #b78646 0%, #d8af6a 100%)" : "rgba(255,255,255,0.78)",
            color: "#2b2118",
            fontWeight: 700,
            cursor: "pointer",
          }}
        >
          {label}
        </button>
      ))}
    </div>
  );
}

function Selector({ selected, setSelected, continueToGenerate = true }) {
  return (
    <section style={{ ...cardStyle, padding: 24 }}>
      <div style={{ marginBottom: 18 }}>
        <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.18em", textTransform: "uppercase", color: "#8c6a39" }}>Love Reports</p>
        <h1 style={{ margin: 0, fontSize: "clamp(2.2rem, 5vw, 3.7rem)", lineHeight: 0.95, fontFamily: "Georgia, Times New Roman, serif" }}>
          Choose the report that matches the relationship question you want answered.
        </h1>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 16 }}>
        {LOVE_REPORTS.map((report) => {
          const active = selected.slug === report.slug;
          return (
            <button
              key={report.slug}
              type="button"
              onClick={() => setSelected(report, continueToGenerate)}
              style={{
                textAlign: "left",
                padding: 18,
                borderRadius: 22,
                border: active ? `1px solid ${report.accent}` : "1px solid rgba(120,90,55,0.14)",
                background: active ? `linear-gradient(180deg, ${report.accent}16, rgba(255,250,244,0.96))` : "rgba(255,255,255,0.78)",
                cursor: "pointer",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", gap: 10, alignItems: "center" }}>
                <span style={{ fontSize: 24 }}>{report.icon}</span>
                <span
                  style={{
                    width: 18,
                    height: 18,
                    borderRadius: "50%",
                    border: `2px solid ${report.accent}`,
                    background: active ? report.accent : "transparent",
                    display: "inline-block",
                  }}
                />
              </div>
              <p style={{ margin: "10px 0 8px", fontSize: 11, letterSpacing: "0.14em", textTransform: "uppercase", color: report.accent }}>
                {active ? "Selected" : "Love report"}
              </p>
              <h2 style={{ margin: "0 0 8px", fontSize: 22, lineHeight: 1.08, fontFamily: "Georgia, Times New Roman, serif" }}>{report.label}</h2>
              <p style={{ margin: 0, color: "#64584c", lineHeight: 1.6 }}>{report.description}</p>
            </button>
          );
        })}
      </div>
    </section>
  );
}

function BirthFormBlock({ title, form, setForm }) {
  return (
    <section style={{ ...cardStyle, padding: 20, background: "rgba(255,251,245,0.78)" }}>
      <div style={{ display: "grid", gap: 14 }}>
        <div>
          <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: "#8c6a39" }}>{title}</p>
          <p style={{ margin: 0, color: "#6f6253", lineHeight: 1.6 }}>
            Choose the birth city to auto-populate timezone and coordinates for the report payload.
          </p>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 14 }}>
          <label style={{ display: "grid", gap: 6 }}>
            <span style={{ fontWeight: 700 }}>Date of Birth</span>
            <input type="date" value={form.date_of_birth} onChange={(event) => setForm((current) => ({ ...current, date_of_birth: event.target.value }))} style={inputStyle} />
          </label>
          <label style={{ display: "grid", gap: 6 }}>
            <span style={{ fontWeight: 700 }}>Time of Birth</span>
            <input type="time" value={form.time_of_birth} onChange={(event) => setForm((current) => ({ ...current, time_of_birth: event.target.value }))} style={inputStyle} />
          </label>
        </div>

        <SharedBirthCityPicker
          inputId={`${title.toLowerCase().replace(/\s+/g, "-")}-birth-city`}
          label="Birth City"
          value={form.city_slug}
          required
          helpText="Search by city, country, or timezone abbreviation."
          wrapperStyle={{ display: "grid", gap: 6 }}
          labelStyle={{ fontWeight: 700 }}
          inputStyle={inputStyle}
          selectStyle={inputStyle}
          onChange={(city) =>
            setForm((current) => ({
              ...current,
              city_slug: city.slug,
              city_name: city.city_name,
              latitude: city.latitude,
              longitude: city.longitude,
              timezone: city.timezone,
            }))
          }
        />
      </div>
    </section>
  );
}

function GenerateForm({ selected, primaryForm, setPrimaryForm, secondaryForm, setSecondaryForm, metaForm, setMetaForm, onSubmit, submitting, error }) {
  return (
    <>
      <section style={{ ...cardStyle, padding: 24 }}>
        <div style={{ display: "grid", gap: 14 }}>
          <div>
            <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: selected.accent }}>{selected.label}</p>
            <h2 style={{ margin: "0 0 8px", fontSize: 30, fontFamily: "Georgia, Times New Roman, serif" }}>Generate {selected.label}</h2>
            <p style={{ margin: 0, color: "#62574a", lineHeight: 1.64 }}>{selected.description}</p>
          </div>

          <BirthFormBlock title={selected.slug === "soul-connection" ? "Person A" : "Birth data"} form={primaryForm} setForm={setPrimaryForm} />

          {selected.slug === "soul-connection" ? <BirthFormBlock title="Person B" form={secondaryForm} setForm={setSecondaryForm} /> : null}

          {selected.slug === "love-weather" ? (
            <section style={{ ...cardStyle, padding: 20, background: "rgba(255,251,245,0.78)", maxWidth: 320 }}>
              <label style={{ display: "grid", gap: 6 }}>
                <span style={{ fontWeight: 700 }}>Lookahead Days</span>
                <input
                  type="number"
                  min={30}
                  max={180}
                  value={metaForm.lookahead_days}
                  onChange={(event) => setMetaForm((current) => ({ ...current, lookahead_days: event.target.value }))}
                  style={inputStyle}
                />
              </label>
            </section>
          ) : null}
        </div>
      </section>

      <section style={{ ...cardStyle, padding: 20, display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
        <p style={{ margin: 0, color: "#675b50" }}>Requests are sent to the live Love Bundle backend with authenticated session credentials.</p>
        <button type="button" onClick={onSubmit} disabled={submitting} style={{ ...primaryButtonStyle, opacity: submitting ? 0.65 : 1 }}>
          {submitting ? `Calculating your ${selected.label}...` : "Generate Report"}
        </button>
      </section>

      {error ? <section style={{ ...cardStyle, padding: 18, color: "#8a3929" }}>{error}</section> : null}
    </>
  );
}

function renderBar(value, tint) {
  return (
    <div style={{ width: "100%", height: 10, borderRadius: 999, background: "rgba(120,90,55,0.12)", overflow: "hidden" }}>
      <div style={{ width: `${Math.max(4, Math.min(100, Number(value) || 0))}%`, height: "100%", background: tint || "linear-gradient(135deg, #b78646 0%, #d8af6a 100%)" }} />
    </div>
  );
}

function StackCard({ title, children }) {
  return (
    <section style={{ ...cardStyle, padding: 20 }}>
      <h3 style={{ margin: "0 0 10px", fontSize: 24, fontFamily: "Georgia, Times New Roman, serif" }}>{title}</h3>
      {children}
    </section>
  );
}

function ListBlock({ items }) {
  const list = toList(items).filter(Boolean);
  if (!list.length) return null;
  return (
    <ul style={{ margin: 0, paddingLeft: 18, color: "#62574a", lineHeight: 1.8 }}>
      {list.map((item, index) => (
        <li key={`${index}-${String(item)}`}>{item}</li>
      ))}
    </ul>
  );
}

function LoveWeatherRenderer({ output }) {
  return (
    <>
      <StackCard title="Arc Summary">
        <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.arc_summary || output.summary}</p>
      </StackCard>
      {!!output.monthly_ratings?.length && (
        <StackCard title="Monthly Ratings">
          <div style={{ display: "grid", gap: 12 }}>
            {output.monthly_ratings.map((item, index) => (
              <div key={`${item.month}-${index}`} style={{ padding: 14, borderRadius: 18, background: "rgba(183, 60, 100, 0.08)" }}>
                <div style={{ display: "flex", justifyContent: "space-between", gap: 10, flexWrap: "wrap" }}>
                  <strong>{item.month}</strong>
                  <span style={{ textTransform: "capitalize" }}>{item.rating}</span>
                </div>
                <div style={{ margin: "8px 0" }}>{renderBar(item.average_score, "linear-gradient(135deg, #b73c64 0%, #d8af6a 100%)")}</div>
                <p style={{ margin: "0 0 8px", color: "#64584c" }}>{item.theme}</p>
                <p style={{ margin: 0, color: "#7a6d60" }}>Best: {item.best_date || "-"} · Caution: {item.caution_date || "-"}</p>
              </div>
            ))}
          </div>
        </StackCard>
      )}
      {!!output.key_dates?.length && (
        <StackCard title="Key Dates">
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 12 }}>
            {output.key_dates.map((item, index) => (
              <div key={`${item.date}-${index}`} style={{ padding: 14, borderRadius: 18, background: "rgba(255,255,255,0.76)" }}>
                <strong>{item.date}</strong>
                <div style={{ margin: "8px 0" }}>{renderBar(item.score || 50, "linear-gradient(135deg, #b73c64 0%, #d8af6a 100%)")}</div>
                <p style={{ margin: 0, color: "#64584c", lineHeight: 1.58 }}>{item.theme || item.description}</p>
              </div>
            ))}
          </div>
        </StackCard>
      )}
      {output.action_guidance ? (
        <StackCard title="Action Guidance">
          <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.action_guidance}</p>
        </StackCard>
      ) : null}
      {!!toList(output.remedies).length && (
        <StackCard title="Remedies">
          <ListBlock items={output.remedies} />
        </StackCard>
      )}
    </>
  );
}

function EncounterRenderer({ output }) {
  const windows = output.windows || output.peak_windows || [];
  return (
    <>
      <StackCard title="Current Window Status">
        <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.summary || output.current_status?.headline || output.personalized_context}</p>
      </StackCard>
      <StackCard title="Windows">
        <div style={{ display: "grid", gap: 12 }}>
          {windows.map((item, index) => (
            <div key={`${item.start_date || item.peak_date || item.date}-${index}`} style={{ padding: 14, borderRadius: 18, background: "rgba(183,60,100,0.08)" }}>
              <strong>{item.trigger_type || item.trigger_basis || "Encounter Window"}</strong>
              <p style={{ margin: "8px 0", color: "#64584c" }}>
                {(item.start_date || item.date || "-")} to {(item.end_date || item.peak_date || item.date || "-")}
              </p>
              <p style={{ margin: "0 0 6px", color: "#62574a", lineHeight: 1.62 }}>{item.description || item.note || item.peak_description}</p>
              {item.ritual_suggestion ? <p style={{ margin: 0, color: "#7c6e61" }}>{item.ritual_suggestion}</p> : null}
            </div>
          ))}
        </div>
      </StackCard>
      {(output.action_note || output.personalized_context) ? (
        <StackCard title="Action Note">
          <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.action_note || output.personalized_context}</p>
        </StackCard>
      ) : null}
    </>
  );
}

function DateNightRenderer({ output }) {
  const bestDates = output.best_dates || (output.check_date ? [{ date: output.check_date, score: output.love_battery_percent, theme: output.alignment_description, suggested_activity: output.action_note }] : []);
  return (
    <>
      <StackCard title="Summary">
        <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.summary || `Love Battery ${output.love_battery_percent || 0}% with a ${output.score_category || "steady"} tone.`}</p>
      </StackCard>
      <StackCard title="Best Dates">
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 12 }}>
          {bestDates.map((item, index) => (
            <div key={`${item.date || "today"}-${index}`} style={{ padding: 14, borderRadius: 18, background: "rgba(139,30,60,0.08)" }}>
              <strong>{item.date || "Today"}</strong>
              <div style={{ margin: "8px 0" }}>{renderBar(item.score || output.love_battery_percent || 50, "linear-gradient(135deg, #8b1e3c 0%, #d8af6a 100%)")}</div>
              <p style={{ margin: "0 0 6px", color: "#62574a", lineHeight: 1.58 }}>{item.theme || output.alignment_description}</p>
              <p style={{ margin: 0, color: "#7b6d61" }}>{item.suggested_activity || output.action_note}</p>
            </div>
          ))}
        </div>
      </StackCard>
      <StackCard title="Ritual Note">
        <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.ritual_note || output.venus_mars_amplifier?.note || "Use the score as a tone guide rather than a rigid yes-or-no signal."}</p>
      </StackCard>
    </>
  );
}

function DigitalDatingRenderer({ output }) {
  return (
    <>
      <StackCard title="Profile Insight">
        <p style={{ margin: "0 0 10px", color: "#62574a", lineHeight: 1.7 }}>{output.profile_insight || output.attraction_signature}</p>
        {output.dating_style ? <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.dating_style}</p> : null}
      </StackCard>
      <StackCard title="Best Times">
        <div style={{ display: "grid", gap: 10 }}>
          {(output.best_times || output.sections || []).map((item, index) => (
            <div key={item.section_id || index} style={{ padding: 12, borderRadius: 16, background: "rgba(255,255,255,0.76)" }}>
              <strong>{item.day_of_week || item.title || "Timing note"}</strong>
              <p style={{ margin: "6px 0 0", color: "#62574a", lineHeight: 1.62 }}>{item.reason || item.summary || item.body}</p>
            </div>
          ))}
        </div>
      </StackCard>
      <StackCard title="Message Timing">
        <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.message_timing || output.first_date_lead || output.ideal_partner_profile}</p>
      </StackCard>
      <StackCard title="Aura Note">
        <p style={{ margin: "0 0 10px", color: "#62574a", lineHeight: 1.7 }}>{output.aura_note || output.ideal_partner_profile || output.self_red_flags}</p>
        <ListBlock items={output.remedies} />
      </StackCard>
    </>
  );
}

function IntimacyRenderer({ output }) {
  const windows = output.windows || output.peak_windows || [];
  const vitalityScore = output.vitality_score || Math.min(95, Math.max(40, 50 + windows.length * 10));
  return (
    <>
      <StackCard title="Current Vitality Phase">
        <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.phase || output.current_vitality_phase}</p>
      </StackCard>
      <StackCard title="Vitality Score">
        <div style={{ marginBottom: 10 }}>{renderBar(vitalityScore, "linear-gradient(135deg, #8b1e3c 0%, #d8af6a 100%)")}</div>
        <p style={{ margin: 0, color: "#62574a" }}>{vitalityScore}% energetic intensity</p>
      </StackCard>
      <StackCard title="Peak Windows">
        <div style={{ display: "grid", gap: 12 }}>
          {windows.map((item, index) => (
            <div key={`${item.start_date || item.date}-${index}`} style={{ padding: 14, borderRadius: 18, background: "rgba(139,30,60,0.08)" }}>
              <strong>{item.intensity || item.trigger_basis || "Vitality Window"}</strong>
              <p style={{ margin: "8px 0", color: "#62574a" }}>{item.start_date || "-"} to {item.end_date || "-"}</p>
              <p style={{ margin: 0, color: "#62574a", lineHeight: 1.62 }}>{item.description || item.note}</p>
            </div>
          ))}
        </div>
      </StackCard>
      <StackCard title="Lunar Note">
        <p style={{ margin: "0 0 10px", color: "#62574a", lineHeight: 1.7 }}>{output.lunar_note || output.natal_intimacy_signature}</p>
        <ListBlock items={output.remedies} />
      </StackCard>
    </>
  );
}

function VenusRetrogradeRenderer({ output }) {
  const active = output.retrograde_active ?? output.transiting_venus_retrograde ?? false;
  return (
    <>
      <StackCard title="Retrograde Status">
        <div style={{ display: "inline-flex", padding: "8px 12px", borderRadius: 999, background: active ? "rgba(183, 60, 100, 0.12)" : "rgba(120,145,78,0.12)", fontWeight: 700 }}>
          {active ? "Active" : "Dormant"}
        </div>
      </StackCard>
      <StackCard title="Personal Impact">
        <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.personal_impact}</p>
      </StackCard>
      <StackCard title="Shadow Themes">
        <ListBlock items={output.shadow_themes || output.retrograde_house_signs} />
      </StackCard>
      <StackCard title="Reframe">
        <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.reframe || output.healing_focus || output.best_practice}</p>
      </StackCard>
      {!!toList(output.remedies).length && (
        <StackCard title="Remedies">
          <ListBlock items={output.remedies} />
        </StackCard>
      )}
    </>
  );
}

function SoulmateTimingRenderer({ output }) {
  const primaryWindow = output.jupiter_window || output.peak_windows?.[0];
  const readiness = output.readiness_score || Math.min(95, 55 + (output.peak_windows?.length || 0) * 8);
  return (
    <>
      <StackCard title="Jupiter Window">
        <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>
          {primaryWindow
            ? `${primaryWindow.start || primaryWindow.start_date || "-"} to ${primaryWindow.end || primaryWindow.end_date || "-"}: ${primaryWindow.note || primaryWindow.planet || primaryWindow.description || "Supportive relationship timing"}`
            : "No single window dominates yet; timing is distributed across the next supportive dasha periods."}
        </p>
      </StackCard>
      <StackCard title="Dasha Summary">
        <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.dasha_summary || output.timing_note}</p>
      </StackCard>
      <StackCard title="Readiness Score">
        <div style={{ marginBottom: 10 }}>{renderBar(readiness, "linear-gradient(135deg, #b78646 0%, #d8af6a 100%)")}</div>
        <p style={{ margin: 0, color: "#62574a" }}>{readiness}% long-term partnership readiness</p>
      </StackCard>
      <StackCard title="Composite Note">
        <p style={{ margin: "0 0 10px", color: "#62574a", lineHeight: 1.7 }}>{output.composite_note || output.summary || output.birth_nakshatra}</p>
        <ListBlock items={output.remedies} />
      </StackCard>
    </>
  );
}

function SoulConnectionRenderer({ output, report }) {
  const sections = output.sections || [];
  const overlays = output.overlays || {};
  return (
    <>
      <StackCard title="Connection Archetype">
        <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.karmic_theme || output.connection_archetype || report.summary}</p>
      </StackCard>
      <StackCard title="Emotional Resonance">
        <div style={{ marginBottom: 10 }}>{renderBar(output.emotional_resonance_score || 50, "linear-gradient(135deg, #6a4b89 0%, #d8af6a 100%)")}</div>
        <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.evolutionary_north || output.attraction_dynamic}</p>
      </StackCard>
      <StackCard title="Long-Term Compatibility">
        <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{output.relational_pattern || output.long_term_compatibility}</p>
      </StackCard>
      {(output.shadow_invitation || toList(output.growth_areas).length) ? (
        <StackCard title="Growth Areas">
          {output.shadow_invitation ? <p style={{ margin: "0 0 10px", color: "#62574a", lineHeight: 1.7 }}>{output.shadow_invitation}</p> : null}
          <ListBlock items={output.growth_areas} />
        </StackCard>
      ) : null}
      {(output.integration_path || toList(output.remedies || output.remedies_for_both).length) ? (
        <StackCard title="Integration Path">
          {output.integration_path ? <p style={{ margin: "0 0 10px", color: "#62574a", lineHeight: 1.7 }}>{output.integration_path}</p> : null}
          <ListBlock items={output.remedies || output.remedies_for_both} />
        </StackCard>
      ) : null}
      {!!sections.length && (
        <StackCard title="Detailed Sections">
          <div style={{ display: "grid", gap: 12 }}>
            {sections.map((section, index) => (
              <div key={section.section_id || index} style={{ padding: 14, borderRadius: 18, background: "rgba(100,60,160,0.08)" }}>
                <strong>{section.title}</strong>
                <p style={{ margin: "8px 0 6px", color: "#62574a", lineHeight: 1.62 }}>{section.summary}</p>
                <p style={{ margin: 0, color: "#6d5e74", lineHeight: 1.62 }}>{section.body}</p>
              </div>
            ))}
          </div>
        </StackCard>
      )}
      {!!Object.keys(overlays).length && (
        <StackCard title="Synastry Overlays">
          <div style={{ display: "grid", gap: 12 }}>
            {Object.entries(overlays).map(([title, items]) => (
              <div key={title} style={{ padding: 14, borderRadius: 18, background: "rgba(255,255,255,0.76)" }}>
                <strong>{title}</strong>
                <div style={{ marginTop: 8 }}>
                  <ListBlock items={items} />
                </div>
              </div>
            ))}
          </div>
        </StackCard>
      )}
    </>
  );
}

function ReportRenderer({ report, selected, onGenerateAgain }) {
  if (!report) {
    return (
      <section style={{ ...cardStyle, padding: 24 }}>
        <h2 style={{ marginTop: 0 }}>No report open yet</h2>
        <p style={{ color: "#63594d" }}>Generate a Love report or open one from your cached history on this device.</p>
      </section>
    );
  }

  const output = report.output_payload || {};
  const type = report.report_type || selected.type;
  const archivedSummaryOnly = !output || !Object.keys(output).length;

  if (archivedSummaryOnly) {
    return (
      <section style={{ ...cardStyle, padding: 24 }}>
        <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.18em", textTransform: "uppercase", color: "#8c6a39" }}>Archived summary</p>
        <h2 style={{ marginTop: 0 }}>{report.report_slug?.replaceAll("-", " ") || selected.label}</h2>
        <p style={{ color: "#62574a", lineHeight: 1.7 }}>{report.summary}</p>
        <p style={{ color: "#7b6b5d", lineHeight: 1.66 }}>
          Full detail is available if this report has been generated on this device and saved into the Love reports cache. Otherwise, the archive view stays summary-only until a detail fetch exists.
        </p>
        <button type="button" onClick={onGenerateAgain} style={primaryButtonStyle}>
          Generate Again
        </button>
      </section>
    );
  }

  return (
    <section style={{ ...cardStyle, padding: 24, display: "grid", gap: 16 }}>
      <div>
        <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.18em", textTransform: "uppercase", color: selected.accent }}>{selected.label}</p>
        <h2 style={{ margin: "0 0 10px", fontSize: 34, fontFamily: "Georgia, Times New Roman, serif" }}>{report.summary}</h2>
        <p style={{ margin: 0, color: "#7a6d60" }}>Generated {prettifyDate(report.created_at)}</p>
      </div>

      {type === "love_weather" ? <LoveWeatherRenderer output={output} /> : null}
      {type === "encounter_window" ? <EncounterRenderer output={output} /> : null}
      {type === "date_night_score" ? <DateNightRenderer output={output} /> : null}
      {type === "digital_dating_strategy" ? <DigitalDatingRenderer output={output} /> : null}
      {type === "intimacy_vitality_forecast" ? <IntimacyRenderer output={output} /> : null}
      {type === "venus_retrograde_personal_impact" ? <VenusRetrogradeRenderer output={output} /> : null}
      {type === "soulmate_timing" ? <SoulmateTimingRenderer output={output} /> : null}
      {type === "deep_synastry_soul_connection" ? <SoulConnectionRenderer output={output} report={report} /> : null}

      <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
        <button type="button" onClick={onGenerateAgain} style={primaryButtonStyle}>
          Generate another report
        </button>
        <Link to="/ritual-engine" style={secondaryButtonStyle}>
          Open Ritual Engine
        </Link>
      </div>
    </section>
  );
}

function HistoryPanel({ historyRows, loadingHistory, historyError, onOpen }) {
  return (
    <section style={{ ...cardStyle, padding: 24 }}>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
        <div>
          <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: "#8c6a39" }}>Archive</p>
          <h2 style={{ margin: 0, fontSize: 30, fontFamily: "Georgia, Times New Roman, serif" }}>Your Love reports</h2>
        </div>
        <div style={{ color: "#76695b" }}>Parallel fetch across all 8 Love report families</div>
      </div>

      {loadingHistory ? <p style={{ color: "#6d6256" }}>Opening your Love archive...</p> : null}
      {historyError ? <p style={{ color: "#8c3b2e" }}>{historyError}</p> : null}

      {!loadingHistory && !historyRows.length ? (
        <div style={{ marginTop: 18, padding: 20, borderRadius: 18, background: "rgba(255,255,255,0.65)" }}>
          <h3 style={{ marginTop: 0 }}>No Love reports yet</h3>
          <p style={{ color: "#6b6054" }}>Generate your first Love report to start building a personal relationship archive.</p>
        </div>
      ) : null}

      <div style={{ marginTop: 18, display: "grid", gap: 14 }}>
        {historyRows.map((entry) => (
          <article key={entry.id} style={{ padding: 18, borderRadius: 18, background: "rgba(255,255,255,0.74)", border: `1px solid ${entry.accent}22` }}>
            <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "flex-start" }}>
              <div>
                <p style={{ margin: "0 0 6px", fontSize: 12, letterSpacing: "0.12em", textTransform: "uppercase", color: entry.accent }}>{entry.label}</p>
                <h3 style={{ margin: "0 0 8px", fontSize: 22, fontFamily: "Georgia, Times New Roman, serif" }}>{prettifyDate(entry.created_at)}</h3>
                <p style={{ margin: 0, color: "#64594e", lineHeight: 1.64 }}>{entry.summary}</p>
              </div>
              <button type="button" onClick={() => onOpen(entry)} style={primaryButtonStyle}>
                View Report
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function LoveReportsPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [selected, setSelectedState] = useState(LOVE_REPORTS[0]);
  const [activeTab, setActiveTab] = useState("select");
  const deferredTab = useDeferredValue(activeTab);
  const [primaryForm, setPrimaryForm] = useState(defaultPersonForm);
  const [secondaryForm, setSecondaryForm] = useState(defaultPersonForm);
  const [metaForm, setMetaForm] = useState(defaultMetaForm);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [currentReport, setCurrentReport] = useState(null);
  const [historyRows, setHistoryRows] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [historyError, setHistoryError] = useState("");

  useProtectedSeo();

  useEffect(() => {
    startTransition(() => {
      if (deferredTab === "generate" && !selected) setSelectedState(LOVE_REPORTS[0]);
    });
  }, [deferredTab, selected]);

  useEffect(() => {
    let active = true;
    async function loadHistory() {
      setLoadingHistory(true);
      setHistoryError("");
      try {
        const responses = await Promise.all(
          LOVE_REPORTS.map((report) =>
            axios.get(`${API}/reports/${report.slug}/history`, { withCredentials: true }).catch(() => ({ data: { items: [] } }))
          )
        );
        if (!active) return;
        const merged = LOVE_REPORTS.flatMap((report, index) =>
          (responses[index].data?.items || []).map((entry) => ({
            ...entry,
            label: report.label,
            accent: report.accent,
            slug: report.slug,
            type: report.type,
          }))
        ).sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
        setHistoryRows(merged);
      } catch (requestError) {
        if (!active) return;
        setHistoryError(requestError?.response?.data?.detail || "Unable to load Love report history right now.");
      } finally {
        if (active) setLoadingHistory(false);
      }
    }
    loadHistory();
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    const params = queryParams(location.search);
    const reportType = params.get("reportType");
    const reportId = params.get("reportId");
    const tab = params.get("tab");
    if (tab) setActiveTab(tab);
    if (reportType) setSelectedState(reportByQuery(reportType));
    if (reportId) {
      const cached = loadCachedReports()[reportId];
      if (cached) setCurrentReport(cached);
      else {
        const fallback = historyRows.find((item) => item.id === reportId);
        if (fallback) setCurrentReport(fallback);
      }
    }
  }, [location.search, historyRows]);

  function setSelected(report, autoAdvance = false) {
    setSelectedState(report);
    if (autoAdvance) {
      setActiveTab("generate");
      navigate(`/love-reports?reportType=${report.slug}&tab=generate`, { replace: true });
    }
  }

  async function handleGenerate() {
    setSubmitting(true);
    setError("");
    try {
      const response = await axios.post(`${API}/reports/${selected.slug}/generate`, buildPayload(selected, primaryForm, secondaryForm, metaForm), {
        withCredentials: true,
      });
      const generated = response.data?.report || null;
      if (generated) {
        saveCachedReport(generated);
        setCurrentReport(generated);
        setHistoryRows((current) =>
          [
            {
              id: generated.id,
              report_type: generated.report_type,
              report_slug: generated.report_slug,
              summary: generated.summary,
              created_at: generated.created_at,
              label: selected.label,
              accent: selected.accent,
              slug: selected.slug,
              type: selected.type,
            },
            ...current,
          ].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        );
        setActiveTab("report");
        navigate(`/love-reports?reportType=${selected.slug}&reportId=${generated.id}&tab=report`, { replace: true });
      }
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || `Unable to generate your ${selected.label} right now.`);
    } finally {
      setSubmitting(false);
    }
  }

  function openHistoryItem(item) {
    const cached = loadCachedReports()[item.id];
    setCurrentReport(cached || item);
    setSelectedState(reportByQuery(item.slug || item.type || item.report_slug));
    setActiveTab("report");
    navigate(`/love-reports?reportType=${item.slug || item.type}&reportId=${item.id}&tab=report`, { replace: true });
  }

  function resetForNew() {
    setCurrentReport(null);
    setError("");
    setActiveTab("generate");
    navigate(`/love-reports?reportType=${selected.slug}&tab=generate`, { replace: true });
  }

  return (
    <div style={pageStyle}>
      <div style={{ maxWidth: 1180, margin: "0 auto", display: "grid", gap: 18 }}>
        <TabBar activeTab={activeTab} setActiveTab={setActiveTab} />
        {activeTab === "select" ? <Selector selected={selected} setSelected={setSelected} continueToGenerate /> : null}
        {activeTab === "generate" ? (
          <>
            <Selector selected={selected} setSelected={setSelected} continueToGenerate={false} />
            <GenerateForm
              selected={selected}
              primaryForm={primaryForm}
              setPrimaryForm={setPrimaryForm}
              secondaryForm={secondaryForm}
              setSecondaryForm={setSecondaryForm}
              metaForm={metaForm}
              setMetaForm={setMetaForm}
              onSubmit={handleGenerate}
              submitting={submitting}
              error={error}
            />
          </>
        ) : null}
        {activeTab === "report" ? <ReportRenderer report={currentReport} selected={selected} onGenerateAgain={resetForNew} /> : null}
        {activeTab === "history" ? <HistoryPanel historyRows={historyRows} loadingHistory={loadingHistory} historyError={historyError} onOpen={openHistoryItem} /> : null}
      </div>
    </div>
  );
}

export default LoveReportsPage;
