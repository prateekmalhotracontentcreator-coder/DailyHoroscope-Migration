import React, { startTransition, useDeferredValue, useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Link, useLocation, useNavigate } from "react-router-dom";
import SharedBirthCityPicker from "../../components/SharedBirthCityPicker";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
const API_BASE = `${BACKEND_URL}/api`;
const CANONICAL_URL = "https://www.everydayhoroscope.in/reports";
const HISTORY_CACHE_KEY = "individual_reports_full_cache_v2";

const REPORT_CONFIGS = [
  {
    type: "karmic_debt",
    slug: "karmic-debt",
    name: "Karmic Debt & Past Life",
    shortName: "Karmic Debt",
    color: "#7f4be0",
    icon: "◎",
    hook: "Decode the spiritual loop you keep meeting in different disguises.",
    description: "A premium Vedic reading for karmic themes, past-life echoes, soul lessons, and release practices.",
  },
  {
    type: "career_blueprint",
    slug: "career-blueprint",
    name: "Career & Success Blueprint",
    shortName: "Career Blueprint",
    color: "#c9961f",
    icon: "▲",
    hook: "See the work pattern, public calling, and success rhythm written into your chart.",
    description: "A Vedic career reading for strengths, wealth signals, career timing, and practical next moves.",
  },
  {
    type: "shadow_self",
    slug: "shadow-self",
    name: "Shadow Self & Hidden Qualities",
    shortName: "Shadow Self",
    color: "#3f7ae0",
    icon: "◐",
    hook: "Name the hidden pressure shaping your reactions before it chooses for you.",
    description: "A deep self-knowledge report for hidden strengths, blind spots, emotional drivers, and integration guidance.",
  },
  {
    type: "retrograde_survival",
    slug: "retrograde-survival",
    name: "Retrograde Survival Guide",
    shortName: "Retrograde Survival",
    color: "#e27c33",
    icon: "↺",
    hook: "Track the retrograde weather around you and move through it with less chaos.",
    description: "A timing-led guidance report for Mercury, Venus, and Mars retrogrades with clean, grounded remedies.",
  },
  {
    type: "life_cycles",
    slug: "life-cycles",
    name: "Pattern of Life Cycles",
    shortName: "Life Cycles",
    color: "#3fa56a",
    icon: "◌",
    hook: "Understand the chapter you are in now and the one already rising behind it.",
    description: "A Vimshottari Dasha report for current chapter, sub-cycle, decade arc, and upcoming transitions.",
  },
  {
    type: "wealth_blueprint",
    slug: "wealth-blueprint",
    name: "Wealth & Abundance Blueprint",
    shortName: "Wealth Blueprint",
    color: "#c8930a",
    icon: "◈",
    hook: "See the wealth signals, abundance timing, and Dhana yogas written into your Vedic chart.",
    description: "A Vedic wealth reading for Dhana yogas, 2nd house strength, Jupiter/Venus influence, and key abundance windows.",
  },
  {
    type: "romance_creative",
    slug: "romance-creative",
    name: "Romance & Creative Intelligence",
    shortName: "Romance & Creativity",
    color: "#d4538a",
    icon: "✦",
    hook: "Unlock the romantic and creative intelligence wired into your 5th house.",
    description: "A Vedic reading for romantic timing, creative gifts, 5th lord strength, and the windows where both peak together.",
  },
  {
    type: "vitality_health",
    slug: "vitality-health",
    name: "Vitality & Health Report",
    shortName: "Vitality & Health",
    color: "#2a9d6f",
    icon: "⬡",
    hook: "Read the health rhythm your chart encodes and the periods that need the most care.",
    description: "A Vedic health reading for 6th house analysis, Mars/Saturn influence, vulnerable patterns, and daily rhythm guidance.",
  },
  {
    type: "partnership_window",
    slug: "partnership-window",
    name: "Partnership & Marriage Window",
    shortName: "Partnership Window",
    color: "#6b4fbd",
    icon: "◇",
    hook: "Find the Vedic marriage timing and see the partnership pattern your 7th house reveals.",
    description: "A Vedic partnership reading for Darakaraka, 7th lord, Upapada Lagna, and marriage/commitment dasha windows.",
  },
  {
    type: "dharma_purpose",
    slug: "dharma-purpose",
    name: "Dharma & Soul Purpose Report",
    shortName: "Dharma & Purpose",
    color: "#1e5fa8",
    icon: "☉",
    hook: "Trace the dharmic thread running through your chart to the purpose this life is asking you to fulfill.",
    description: "A Vedic dharma reading for 9th lord, Jupiter strength, Atmakaraka path, and the soul-level direction already written in your chart.",
  },
  {
    type: "gains_network",
    slug: "gains-network",
    name: "Gains & Network Activator",
    shortName: "Gains & Network",
    color: "#d46f22",
    icon: "◆",
    hook: "See the aspiration fulfillment windows and the social leverage points your 11th house encodes.",
    description: "A Vedic gains reading for 11th lord strength, Saturn's role in aspiration, key gains dasha windows, and network activation timing.",
  },
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
  padding: "28px 18px 88px",
  background:
    "radial-gradient(circle at top left, rgba(127,75,224,0.16), transparent 24%), radial-gradient(circle at top right, rgba(201,150,31,0.14), transparent 26%), linear-gradient(180deg, #f9f3ea 0%, #efe4d2 100%)",
  color: "#221c17",
};

const surfaceStyle = {
  background: "rgba(255, 251, 246, 0.9)",
  border: "1px solid rgba(92, 66, 32, 0.12)",
  borderRadius: 26,
  boxShadow: "0 24px 64px rgba(67, 43, 15, 0.08)",
  backdropFilter: "blur(10px)",
};

const buttonBase = {
  minHeight: 46,
  borderRadius: 999,
  border: "1px solid transparent",
  padding: "11px 18px",
  fontSize: 15,
  fontWeight: 700,
  cursor: "pointer",
};

function loadCachedReports() {
  try {
    return JSON.parse(window.localStorage.getItem(HISTORY_CACHE_KEY) || "{}");
  } catch {
    return {};
  }
}

function saveCachedReport(report) {
  if (!report?.id) return;
  const cache = loadCachedReports();
  cache[report.id] = report;
  window.localStorage.setItem(HISTORY_CACHE_KEY, JSON.stringify(cache));
}

function findCachedReport(reportId) {
  return loadCachedReports()[reportId] || null;
}

function defaultFormState(selectedType) {
  return {
    date: "",
    time: "",
    check_date: new Date().toISOString().slice(0, 10),
    retrograde_mode: selectedType === "retrograde_survival" ? "general" : "personal",
    retrograde_planet: "",
    city_slug: EMPTY_CITY.slug,
    city_name: EMPTY_CITY.city_name,
    latitude: EMPTY_CITY.latitude,
    longitude: EMPTY_CITY.longitude,
    timezone: EMPTY_CITY.timezone,
  };
}

function buildBirthPayload(form) {
  return {
    date: form.date,
    time: form.time,
    city_name: form.city_name,
    latitude: form.latitude === "" || form.latitude == null ? undefined : Number(form.latitude),
    longitude: form.longitude === "" || form.longitude == null ? undefined : Number(form.longitude),
    timezone: form.timezone || undefined,
  };
}

function humanDate(value) {
  if (!value) return "Unknown";
  try {
    return new Date(value).toLocaleString(undefined, {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit",
    });
  } catch {
    return value;
  }
}

function sentenceCase(key) {
  return key.replace(/_/g, " ").replace(/\b\w/g, (character) => character.toUpperCase());
}

function normalizeHistoryEntry(item, config) {
  return {
    ...item,
    kind: "individual_report",
    report_type: config.type,
    report_slug: config.slug,
    label: config.name,
    accent: config.color,
  };
}

function useSeo(selectedReport, activeTab, currentReport) {
  useEffect(() => {
    const baseTitle = selectedReport ? `${selectedReport.name} | Everyday Horoscope` : "Individual Reports | Everyday Horoscope";
    const title =
      activeTab === "history"
        ? "My Individual Reports | Everyday Horoscope"
        : currentReport
          ? `${selectedReport?.name || "Individual Report"} Ready | Everyday Horoscope`
          : baseTitle;
    const description =
      activeTab === "history"
        ? "Review your saved Individual Reports inside the Everyday Horoscope archive."
        : selectedReport?.description || "Generate premium AI-enriched Vedic reports for karma, career, shadow work, retrogrades, life cycles, wealth, romance, vitality, partnership, dharma, and gains.";
    document.title = title;

    let metaDescription = document.querySelector('meta[name="description"]');
    if (!metaDescription) {
      metaDescription = document.createElement("meta");
      metaDescription.setAttribute("name", "description");
      document.head.appendChild(metaDescription);
    }
    metaDescription.setAttribute("content", description);

    let robots = document.querySelector('meta[name="robots"]');
    if (!robots) {
      robots = document.createElement("meta");
      robots.setAttribute("name", "robots");
      document.head.appendChild(robots);
    }
    robots.setAttribute("content", "noindex, nofollow");

    let canonical = document.querySelector('link[rel="canonical"]');
    if (!canonical) {
      canonical = document.createElement("link");
      canonical.setAttribute("rel", "canonical");
      document.head.appendChild(canonical);
    }
    canonical.setAttribute("href", CANONICAL_URL);
  }, [activeTab, currentReport, selectedReport]);
}

function SectionTabs({ activeTab, onChange }) {
  const tabs = [
    ["select", "Select"],
    ["generate", "Generate"],
    ["report", "Report"],
    ["history", "History"],
  ];
  return (
    <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
      {tabs.map(([value, label]) => {
        const active = activeTab === value;
        return (
          <button
            key={value}
            type="button"
            onClick={() => onChange(value)}
            style={{
              ...buttonBase,
              background: active ? "#241b13" : "rgba(255,255,255,0.74)",
              color: active ? "#fff8ee" : "#3d3022",
              borderColor: active ? "#241b13" : "rgba(92, 66, 32, 0.12)",
            }}
          >
            {label}
          </button>
        );
      })}
    </div>
  );
}

function ReportCards({ selectedReport, onSelect, onGenerate }) {
  return (
    <section style={{ ...surfaceStyle, padding: 28 }}>
      <div style={{ display: "grid", gap: 12, marginBottom: 20 }}>
        <p style={{ margin: 0, fontSize: 12, letterSpacing: "0.22em", textTransform: "uppercase", color: "#94734c" }}>Individual Reports</p>
        <h1 style={{ margin: 0, fontSize: "clamp(2rem, 5vw, 4rem)", lineHeight: 0.94, fontFamily: "Georgia, Times New Roman, serif" }}>
          Premium chart readings for the questions that keep returning.
        </h1>
        <p style={{ margin: 0, maxWidth: 760, color: "#675548", lineHeight: 1.72 }}>
          Each report blends deterministic Vedic logic with the live enrichment layer already active on Temple's backend, then returns a polished reading with structure, guidance, and remedies.
        </p>
      </div>

      <div style={{ display: "grid", gap: 16, gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))" }}>
        {REPORT_CONFIGS.map((report) => {
          const active = report.type === selectedReport.type;
          return (
            <article
              key={report.type}
              style={{
                borderRadius: 24,
                padding: 20,
                border: `1px solid ${active ? report.color : "rgba(92, 66, 32, 0.12)"}`,
                background: active
                  ? `linear-gradient(180deg, ${report.color}1e 0%, rgba(255,255,255,0.92) 100%)`
                  : "linear-gradient(180deg, rgba(255,255,255,0.92) 0%, rgba(246,239,229,0.78) 100%)",
                display: "grid",
                gap: 14,
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 10 }}>
                <div
                  style={{
                    width: 44,
                    height: 44,
                    borderRadius: 14,
                    display: "grid",
                    placeItems: "center",
                    background: report.color,
                    color: "#fff8ee",
                    fontSize: 24,
                    fontWeight: 700,
                  }}
                >
                  {report.icon}
                </div>
                <span style={{ fontSize: 11, letterSpacing: "0.16em", textTransform: "uppercase", color: report.color }}>
                  {active ? "Selected" : "Premium"}
                </span>
              </div>
              <div style={{ display: "grid", gap: 8 }}>
                <h2 style={{ margin: 0, fontSize: 24, lineHeight: 1.03, fontFamily: "Georgia, Times New Roman, serif" }}>{report.name}</h2>
                <p style={{ margin: 0, color: "#3d3128", lineHeight: 1.6 }}>{report.hook}</p>
                <p style={{ margin: 0, color: "#706154", lineHeight: 1.64 }}>{report.description}</p>
              </div>
              <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
                <button
                  type="button"
                  onClick={() => onSelect(report)}
                  style={{
                    ...buttonBase,
                    background: active ? "#241b13" : "rgba(255,255,255,0.72)",
                    color: active ? "#fff8ee" : "#2f241b",
                    borderColor: active ? "#241b13" : "rgba(92, 66, 32, 0.12)",
                  }}
                >
                  {active ? "Selected" : "Choose Report"}
                </button>
                <button
                  type="button"
                  onClick={() => onGenerate(report)}
                  style={{ ...buttonBase, background: report.color, color: "#fffaf2" }}
                >
                  Generate
                </button>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}

function FormField({ label, children, note }) {
  return (
    <label style={{ display: "grid", gap: 8 }}>
      <span style={{ fontSize: 13, fontWeight: 700, color: "#3a2e24" }}>{label}</span>
      {children}
      {note ? <span style={{ fontSize: 12, color: "#7b6a5c" }}>{note}</span> : null}
    </label>
  );
}

function FieldInput(props) {
  return (
    <input
      {...props}
      style={{
        minHeight: 48,
        borderRadius: 16,
        border: "1px solid rgba(92, 66, 32, 0.14)",
        background: "rgba(255,255,255,0.9)",
        padding: "12px 14px",
        fontSize: 15,
        color: "#291f18",
      }}
    />
  );
}

function FieldSelect({ children, ...props }) {
  return (
    <select
      {...props}
      style={{
        minHeight: 48,
        borderRadius: 16,
        border: "1px solid rgba(92, 66, 32, 0.14)",
        background: "rgba(255,255,255,0.9)",
        padding: "12px 14px",
        fontSize: 15,
        color: "#291f18",
      }}
    >
      {children}
    </select>
  );
}

function GeneratePanel({ selectedReport, form, onFormChange, onSubmit, submitting, error }) {
  const isRetrograde = selectedReport.type === "retrograde_survival";
  const retrogradeGeneral = isRetrograde && form.retrograde_mode === "general";

  return (
    <section style={{ ...surfaceStyle, padding: 28, display: "grid", gap: 20 }}>
      <div style={{ display: "grid", gap: 10 }}>
        <p style={{ margin: 0, fontSize: 12, letterSpacing: "0.18em", textTransform: "uppercase", color: selectedReport.color }}>
          {selectedReport.shortName}
        </p>
        <h2 style={{ margin: 0, fontSize: 32, fontFamily: "Georgia, Times New Roman, serif" }}>Generate your report</h2>
        <p style={{ margin: 0, color: "#665548", lineHeight: 1.68 }}>
          The input flow stays consistent across all five reports. Retrograde Survival includes a faster general mode with no birth time required.
        </p>
      </div>

      {isRetrograde ? (
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          {[
            ["general", "General mode"],
            ["personal", "Personal mode"],
          ].map(([value, label]) => {
            const active = form.retrograde_mode === value;
            return (
              <button
                key={value}
                type="button"
                onClick={() => onFormChange("retrograde_mode", value)}
                style={{
                  ...buttonBase,
                  background: active ? selectedReport.color : "rgba(255,255,255,0.74)",
                  color: active ? "#fffaf2" : "#33271e",
                  borderColor: active ? selectedReport.color : "rgba(92, 66, 32, 0.12)",
                }}
              >
                {label}
              </button>
            );
          })}
        </div>
      ) : null}

      <form onSubmit={onSubmit} style={{ display: "grid", gap: 16 }}>
        <div style={{ display: "grid", gap: 16, gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))" }}>
          {!isRetrograde || !retrogradeGeneral ? (
            <>
              <FormField label="Birth date">
                <FieldInput type="date" value={form.date} onChange={(event) => onFormChange("date", event.target.value)} required />
              </FormField>

              <FormField
                label="Birth time"
                note={isRetrograde ? "General mode hides this field. Personal mode uses it for house-level retrograde context." : null}
              >
                <FieldInput type="time" value={form.time} onChange={(event) => onFormChange("time", event.target.value)} required />
              </FormField>

              <FormField label="Birth city">
                <SharedBirthCityPicker
                  inputId={`individual-report-city-${selectedReport.slug}`}
                  label=""
                  value={form.city_slug}
                  required
                  helpText="Select the birth city to populate timezone and coordinates for this report."
                  wrapperStyle={{ display: "grid" }}
                  labelStyle={{ display: "none" }}
                  inputStyle={{
                    minHeight: 48,
                    borderRadius: 16,
                    border: "1px solid rgba(92, 66, 32, 0.14)",
                    background: "rgba(255,255,255,0.9)",
                    padding: "12px 14px",
                    fontSize: 15,
                    color: "#291f18",
                  }}
                  selectStyle={{
                    minHeight: 48,
                    borderRadius: 16,
                    border: "1px solid rgba(92, 66, 32, 0.14)",
                    background: "rgba(255,255,255,0.9)",
                    padding: "12px 14px",
                    fontSize: 15,
                    color: "#291f18",
                  }}
                  onChange={(city) => onFormChange("city_slug", city)}
                />
              </FormField>
            </>
          ) : null}

          {isRetrograde ? (
            <>
              <FormField label="Check date" note="Leave today's date for the current retrograde weather, or choose another date to inspect.">
                <FieldInput type="date" value={form.check_date} onChange={(event) => onFormChange("check_date", event.target.value)} />
              </FormField>

              <FormField label="Planet focus" note="Blank checks Mercury, Venus, and Mars together.">
                <FieldSelect value={form.retrograde_planet} onChange={(event) => onFormChange("retrograde_planet", event.target.value)}>
                  <option value="">All active retrogrades</option>
                  <option value="Mercury">Mercury</option>
                  <option value="Venus">Venus</option>
                  <option value="Mars">Mars</option>
                </FieldSelect>
              </FormField>
            </>
          ) : null}
        </div>

        {error ? (
          <div style={{ borderRadius: 18, padding: 14, background: "rgba(163, 60, 39, 0.08)", color: "#8f3423" }}>{error}</div>
        ) : null}

        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          <button type="submit" disabled={submitting} style={{ ...buttonBase, background: selectedReport.color, color: "#fffaf2", opacity: submitting ? 0.7 : 1 }}>
            {submitting ? "Generating..." : `Generate ${selectedReport.shortName}`}
          </button>
          <Link to="/my-reports" style={{ ...buttonBase, display: "inline-flex", alignItems: "center", justifyContent: "center", background: "rgba(255,255,255,0.72)", color: "#30251c", borderColor: "rgba(92, 66, 32, 0.12)", textDecoration: "none" }}>
            Open My Reports
          </Link>
        </div>
      </form>
    </section>
  );
}

function ReportSection({ title, accent, children }) {
  return (
    <section style={{ ...surfaceStyle, padding: 24, borderTop: `4px solid ${accent}` }}>
      <h3 style={{ margin: "0 0 14px", fontSize: 24, fontFamily: "Georgia, Times New Roman, serif" }}>{title}</h3>
      <div style={{ display: "grid", gap: 12, color: "#3a2d22", lineHeight: 1.72 }}>{children}</div>
    </section>
  );
}

function LabelValueGrid({ items }) {
  return (
    <div style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(auto-fit, minmax(170px, 1fr))" }}>
      {items.map((item) => (
        <div key={item.label} style={{ borderRadius: 18, padding: 16, background: "rgba(244, 236, 225, 0.78)" }}>
          <div style={{ fontSize: 12, letterSpacing: "0.12em", textTransform: "uppercase", color: "#87694a", marginBottom: 8 }}>{item.label}</div>
          <div style={{ color: "#2d221a", lineHeight: 1.6 }}>{item.value}</div>
        </div>
      ))}
    </div>
  );
}

function RemediesGrid({ remedies }) {
  if (!remedies) return null;
  return (
    <div style={{ display: "grid", gap: 14, gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))" }}>
      <div style={{ borderRadius: 18, padding: 18, background: "rgba(244, 236, 225, 0.78)" }}>
        <div style={{ marginBottom: 10, fontSize: 12, letterSpacing: "0.14em", textTransform: "uppercase", color: "#8c6f4e" }}>Mantra</div>
        <div style={{ fontWeight: 700, marginBottom: 6 }}>{remedies.mantra?.text}</div>
        <div style={{ fontStyle: "italic", marginBottom: 8, color: "#6c5d50" }}>{remedies.mantra?.transliteration}</div>
        <div style={{ lineHeight: 1.65 }}>{remedies.mantra?.practice}</div>
      </div>
      <div style={{ borderRadius: 18, padding: 18, background: "rgba(244, 236, 225, 0.78)" }}>
        <div style={{ marginBottom: 10, fontSize: 12, letterSpacing: "0.14em", textTransform: "uppercase", color: "#8c6f4e" }}>Gemstone</div>
        <div style={{ fontWeight: 700, marginBottom: 6 }}>{remedies.gemstone?.stone}</div>
        <div style={{ lineHeight: 1.65 }}>{remedies.gemstone?.purpose}</div>
      </div>
      <div style={{ borderRadius: 18, padding: 18, background: "rgba(244, 236, 225, 0.78)" }}>
        <div style={{ marginBottom: 10, fontSize: 12, letterSpacing: "0.14em", textTransform: "uppercase", color: "#8c6f4e" }}>Ritual</div>
        <div style={{ lineHeight: 1.65 }}>{remedies.ritual}</div>
      </div>
    </div>
  );
}

function KarmicDebtRenderer({ report, config }) {
  const output = report.output_payload;
  const body = output.report;
  const indicators = output.karmic_indicators;
  return (
    <div style={{ display: "grid", gap: 18 }}>
      <ReportSection title={body.headline} accent={config.color}>
        <p style={{ margin: 0 }}>{body.karmic_theme}</p>
        <p style={{ margin: 0 }}>{body.past_life_echo}</p>
        <p style={{ margin: 0 }}>{body.atmakaraka_insight}</p>
        <p style={{ margin: 0 }}>{body.breaking_the_cycle}</p>
      </ReportSection>
      <ReportSection title="Karmic indicators" accent={config.color}>
        <LabelValueGrid
          items={[
            { label: "Atmakaraka", value: `${indicators.atmakaraka} (${indicators.atmakaraka_degree}°)` },
            { label: "Saturn House", value: indicators.saturn_house },
            { label: "Rahu House", value: indicators.rahu_house },
            { label: "Ketu House", value: indicators.ketu_house },
            { label: "Debt Activated", value: indicators.debt_activated ? "Yes" : "No" },
            { label: "Retrogrades", value: indicators.retrograde_planets.length ? indicators.retrograde_planets.join(", ") : "None active in natal snapshot" },
          ]}
        />
      </ReportSection>
      <ReportSection title="Retrograde lessons" accent={config.color}>
        {body.retrograde_lessons?.length ? (
          body.retrograde_lessons.map((lesson) => (
            <div key={lesson.planet} style={{ borderRadius: 18, padding: 16, background: "rgba(244, 236, 225, 0.78)" }}>
              <strong>{lesson.planet}</strong>
              <p style={{ margin: "8px 0 0" }}>{lesson.lesson}</p>
            </div>
          ))
        ) : (
          <p style={{ margin: 0 }}>No natal retrograde lesson was surfaced in this chart snapshot.</p>
        )}
      </ReportSection>
      <ReportSection title="Supportive remedies" accent={config.color}>
        <RemediesGrid remedies={body.remedies} />
      </ReportSection>
    </div>
  );
}

function CareerRenderer({ report, config }) {
  const output = report.output_payload;
  return (
    <div style={{ display: "grid", gap: 18 }}>
      <ReportSection title="Career archetype" accent={config.color}>
        <p style={{ margin: 0 }}>{output.career_archetype}</p>
        <p style={{ margin: 0 }}>{output.natural_strengths}</p>
        <p style={{ margin: 0 }}>{output.success_formula}</p>
        <p style={{ margin: 0 }}>{output.wealth_signature}</p>
        <p style={{ margin: 0 }}>{output.action_guidance}</p>
      </ReportSection>
      <ReportSection title="Peak periods" accent={config.color}>
        {output.peak_periods?.map((period) => (
          <div key={`${period.planet}-${period.start}`} style={{ borderRadius: 18, padding: 16, background: "rgba(244, 236, 225, 0.78)" }}>
            <strong>{period.planet}</strong>
            <p style={{ margin: "6px 0" }}>
              {period.start} to {period.end}
            </p>
            <p style={{ margin: 0 }}>{period.description}</p>
          </div>
        ))}
      </ReportSection>
      <ReportSection title="Supportive remedies" accent={config.color}>
        <RemediesGrid remedies={output.remedies} />
      </ReportSection>
    </div>
  );
}

function ShadowRenderer({ report, config }) {
  const output = report.output_payload;
  return (
    <div style={{ display: "grid", gap: 18 }}>
      <ReportSection title="Your inner pattern" accent={config.color}>
        <p style={{ margin: 0 }}>{output.janma_nakshatra}</p>
        <p style={{ margin: 0 }}>{output.shadow_nakshatra}</p>
      </ReportSection>
      <ReportSection title="What lives underneath" accent={config.color}>
        <p style={{ margin: 0 }}>{output.hidden_strengths}</p>
        <p style={{ margin: 0 }}>{output.blind_spots}</p>
        <p style={{ margin: 0 }}>{output.psychological_driver}</p>
        <p style={{ margin: 0 }}>{output.integration_path}</p>
      </ReportSection>
      <ReportSection title="Supportive remedies" accent={config.color}>
        <RemediesGrid remedies={output.remedies} />
      </ReportSection>
    </div>
  );
}

function RetrogradeRenderer({ report, config }) {
  const output = report.output_payload;
  return (
    <div style={{ display: "grid", gap: 18 }}>
      <ReportSection title={`Retrograde mode: ${sentenceCase(output.mode)}`} accent={config.color}>
        <p style={{ margin: 0 }}>
          This report checks current or selected-date retrograde weather for Mercury, Venus, and Mars, then adds personal house context when birth data is supplied.
        </p>
      </ReportSection>
      <ReportSection title="Active retrogrades" accent={config.color}>
        {output.active_retrogrades?.length ? (
          output.active_retrogrades.map((item) => (
            <div key={`${item.planet}-${item.start_date}`} style={{ ...surfaceStyle, padding: 20, boxShadow: "none" }}>
              <div style={{ display: "grid", gap: 12 }}>
                <div>
                  <h4 style={{ margin: "0 0 8px", fontSize: 22, fontFamily: "Georgia, Times New Roman, serif" }}>{item.planet}</h4>
                  <p style={{ margin: 0, color: "#665548" }}>
                    {item.start_date} to {item.end_date}
                    {item.transit_house ? ` • House ${item.transit_house}` : ""}
                  </p>
                </div>
                <p style={{ margin: 0 }}>{item.what_to_expect}</p>
                <LabelValueGrid items={[{ label: "Life Area", value: item.life_area }]} />
                <div style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))" }}>
                  <div style={{ borderRadius: 18, padding: 16, background: "rgba(244, 236, 225, 0.78)" }}>
                    <div style={{ marginBottom: 8, fontSize: 12, letterSpacing: "0.14em", textTransform: "uppercase", color: "#8c6f4e" }}>Navigation Tips</div>
                    <ul style={{ margin: 0, paddingLeft: 18, lineHeight: 1.7 }}>
                      {item.navigation_tips?.map((tip) => (
                        <li key={tip}>{tip}</li>
                      ))}
                    </ul>
                  </div>
                  <div style={{ borderRadius: 18, padding: 16, background: "rgba(244, 236, 225, 0.78)" }}>
                    <div style={{ marginBottom: 8, fontSize: 12, letterSpacing: "0.14em", textTransform: "uppercase", color: "#8c6f4e" }}>What To Avoid</div>
                    <ul style={{ margin: 0, paddingLeft: 18, lineHeight: 1.7 }}>
                      {item.what_to_avoid?.map((avoid) => (
                        <li key={avoid}>{avoid}</li>
                      ))}
                    </ul>
                  </div>
                </div>
                <RemediesGrid remedies={item.remedies} />
              </div>
            </div>
          ))
        ) : (
          <p style={{ margin: 0 }}>No active retrograde was returned for the selected date and planet filter.</p>
        )}
      </ReportSection>
    </div>
  );
}

function LifeCyclesRenderer({ report, config }) {
  const output = report.output_payload;
  return (
    <div style={{ display: "grid", gap: 18 }}>
      <ReportSection title="Current chapter" accent={config.color}>
        <p style={{ margin: 0 }}>{output.current_chapter}</p>
        <p style={{ margin: 0 }}>{output.current_sub_chapter}</p>
        <p style={{ margin: 0 }}>{output.chapter_quality}</p>
        <p style={{ margin: 0 }}>{output.this_decade_arc}</p>
      </ReportSection>
      <ReportSection title="Upcoming transitions" accent={config.color}>
        {output.upcoming_transitions?.map((transition) => (
          <div key={`${transition.planet}-${transition.date}`} style={{ borderRadius: 18, padding: 16, background: "rgba(244, 236, 225, 0.78)" }}>
            <strong>{transition.planet}</strong>
            <p style={{ margin: "6px 0" }}>{transition.date}</p>
            <p style={{ margin: 0 }}>{transition.theme}</p>
          </div>
        ))}
      </ReportSection>
      <ReportSection title="Supportive remedies" accent={config.color}>
        <RemediesGrid remedies={output.remedies} />
      </ReportSection>
    </div>
  );
}

function WealthRenderer({ report, config }) {
  const output = report.output_payload;
  const indicators = output.wealth_indicators;
  return (
    <div style={{ display: "grid", gap: 18 }}>
      <ReportSection title="Wealth signature" accent={config.color}>
        <p style={{ margin: 0 }}>{output.wealth_signature}</p>
        <p style={{ margin: 0 }}>{output.dhanayoga_profile}</p>
        <p style={{ margin: 0 }}>{output.abundance_blocks}</p>
        <p style={{ margin: 0 }}>{output.prosperity_path}</p>
      </ReportSection>
      <ReportSection title="Abundance indicators" accent={config.color}>
        <LabelValueGrid
          items={[
            { label: "2nd Lord", value: `${indicators.second_lord} • House ${indicators.second_lord_house}` },
            { label: "11th Lord", value: `${indicators.eleventh_lord} • House ${indicators.eleventh_lord_house}` },
            { label: "Jupiter", value: `House ${indicators.jupiter_house}` },
            { label: "Venus", value: `House ${indicators.venus_house}` },
            { label: "Dhana Links", value: indicators.dhana_yoga_count },
            { label: "Planets In 2nd", value: indicators.planets_in_second?.length ? indicators.planets_in_second.join(", ") : "None" },
          ]}
        />
      </ReportSection>
      <ReportSection title="Wealth windows" accent={config.color}>
        {output.wealth_windows?.map((period) => (
          <div key={`${period.planet}-${period.start}`} style={{ borderRadius: 18, padding: 16, background: "rgba(244, 236, 225, 0.78)" }}>
            <strong>{period.planet}</strong>
            <p style={{ margin: "6px 0" }}>
              {period.start} to {period.end}
            </p>
            <p style={{ margin: 0 }}>{period.description}</p>
          </div>
        ))}
      </ReportSection>
      <ReportSection title="Supportive remedies" accent={config.color}>
        <RemediesGrid remedies={output.remedies} />
      </ReportSection>
    </div>
  );
}

function RomanceCreativeRenderer({ report, config }) {
  const output = report.output_payload;
  const indicators = output.romance_indicators;
  return (
    <div style={{ display: "grid", gap: 18 }}>
      <ReportSection title="Romantic and creative signature" accent={config.color}>
        <p style={{ margin: 0 }}>{output.romantic_signature}</p>
        <p style={{ margin: 0 }}>{output.creative_intelligence}</p>
        <p style={{ margin: 0 }}>{output.heart_blocks}</p>
        <p style={{ margin: 0 }}>{output.expression_path}</p>
      </ReportSection>
      <ReportSection title="5th house indicators" accent={config.color}>
        <LabelValueGrid
          items={[
            { label: "5th Lord", value: `${indicators.fifth_lord} • House ${indicators.fifth_lord_house}` },
            { label: "Putrakaraka", value: indicators.putrakaraka },
            { label: "Venus", value: `House ${indicators.venus_house}` },
            { label: "Sun", value: `House ${indicators.sun_house}` },
            { label: "Moon Nakshatra", value: indicators.moon_nakshatra },
            { label: "Planets In 5th", value: indicators.planets_in_fifth?.length ? indicators.planets_in_fifth.join(", ") : "None" },
          ]}
        />
      </ReportSection>
      <ReportSection title="Opening windows" accent={config.color}>
        {output.opening_windows?.map((period) => (
          <div key={`${period.planet}-${period.start}`} style={{ borderRadius: 18, padding: 16, background: "rgba(244, 236, 225, 0.78)" }}>
            <strong>{period.planet}</strong>
            <p style={{ margin: "6px 0" }}>
              {period.start} to {period.end}
            </p>
            <p style={{ margin: 0 }}>{period.description}</p>
          </div>
        ))}
      </ReportSection>
      <ReportSection title="Supportive remedies" accent={config.color}>
        <RemediesGrid remedies={output.remedies} />
      </ReportSection>
    </div>
  );
}

function VitalityHealthRenderer({ report, config }) {
  const output = report.output_payload;
  const indicators = output.vitality_indicators;
  return (
    <div style={{ display: "grid", gap: 18 }}>
      <ReportSection title="Vitality signature" accent={config.color}>
        <p style={{ margin: 0 }}>{output.vitality_signature}</p>
        <p style={{ margin: 0 }}>{output.pressure_pattern}</p>
        <p style={{ margin: 0 }}>{output.recovery_path}</p>
        <p style={{ margin: 0 }}>{output.daily_rhythm_guidance}</p>
      </ReportSection>
      <ReportSection title="Health indicators" accent={config.color}>
        <LabelValueGrid
          items={[
            { label: "Lagna", value: indicators.lagna_sign },
            { label: "6th Lord", value: `${indicators.sixth_lord} • House ${indicators.sixth_lord_house}` },
            { label: "Mars", value: `House ${indicators.mars_house}` },
            { label: "Saturn", value: `House ${indicators.saturn_house}` },
            { label: "Sun", value: `House ${indicators.sun_house}` },
            { label: "Moon", value: `House ${indicators.moon_house}` },
          ]}
        />
        <div style={{ marginTop: 14, color: "#665548" }}>
          <strong>Planets in 6th:</strong> {indicators.planets_in_sixth?.length ? indicators.planets_in_sixth.join(", ") : "None"}
        </div>
      </ReportSection>
      <ReportSection title="Care windows" accent={config.color}>
        {output.care_windows?.map((period) => (
          <div key={`${period.planet}-${period.start}`} style={{ borderRadius: 18, padding: 16, background: "rgba(244, 236, 225, 0.78)" }}>
            <strong>{period.planet}</strong>
            <p style={{ margin: "6px 0" }}>
              {period.start} to {period.end}
            </p>
            <p style={{ margin: 0 }}>{period.description}</p>
          </div>
        ))}
      </ReportSection>
      <ReportSection title="Supportive remedies" accent={config.color}>
        <RemediesGrid remedies={output.remedies} />
      </ReportSection>
    </div>
  );
}

function PartnershipRenderer({ report, config }) {
  const output = report.output_payload;
  const indicators = output.partnership_indicators;
  return (
    <div style={{ display: "grid", gap: 18 }}>
      <ReportSection title="Partnership signature" accent={config.color}>
        <p style={{ margin: 0 }}>{output.partnership_signature}</p>
        <p style={{ margin: 0 }}>{output.commitment_pattern}</p>
        <p style={{ margin: 0 }}>{output.relationship_blocks}</p>
        <p style={{ margin: 0 }}>{output.readiness_path}</p>
      </ReportSection>
      <ReportSection title="7th house indicators" accent={config.color}>
        <LabelValueGrid
          items={[
            { label: "7th Lord", value: `${indicators.seventh_lord} • House ${indicators.seventh_lord_house}` },
            { label: "Darakaraka", value: indicators.darakaraka },
            { label: "Venus", value: `House ${indicators.venus_house}` },
            { label: "Upapada", value: indicators.upapada_sign },
            { label: "Planets In 7th", value: indicators.planets_in_seventh?.length ? indicators.planets_in_seventh.join(", ") : "None" },
          ]}
        />
      </ReportSection>
      <ReportSection title="Partnership windows" accent={config.color}>
        {output.partnership_windows?.map((period) => (
          <div key={`${period.planet}-${period.start}`} style={{ borderRadius: 18, padding: 16, background: "rgba(244, 236, 225, 0.78)" }}>
            <strong>{period.planet}</strong>
            <p style={{ margin: "6px 0" }}>
              {period.start} to {period.end}
            </p>
            <p style={{ margin: 0 }}>{period.description}</p>
          </div>
        ))}
      </ReportSection>
      <ReportSection title="Supportive remedies" accent={config.color}>
        <RemediesGrid remedies={output.remedies} />
      </ReportSection>
    </div>
  );
}

function DharmaPurposeRenderer({ report, config }) {
  const output = report.output_payload;
  const indicators = output.dharma_indicators;
  return (
    <div style={{ display: "grid", gap: 18 }}>
      <ReportSection title="Dharma signature" accent={config.color}>
        <p style={{ margin: 0 }}>{output.dharma_signature}</p>
        <p style={{ margin: 0 }}>{output.soul_calling}</p>
        <p style={{ margin: 0 }}>{output.faith_tests}</p>
        <p style={{ margin: 0 }}>{output.alignment_path}</p>
      </ReportSection>
      <ReportSection title="9th house indicators" accent={config.color}>
        <LabelValueGrid
          items={[
            { label: "9th Lord", value: `${indicators.ninth_lord} • House ${indicators.ninth_lord_house}` },
            { label: "Jupiter", value: `House ${indicators.jupiter_house}` },
            { label: "Atmakaraka", value: `${indicators.atmakaraka} (${indicators.atmakaraka_degree}°)` },
            { label: "Moon Nakshatra Lord", value: indicators.moon_nakshatra_lord },
            { label: "Planets In 9th", value: indicators.planets_in_ninth?.length ? indicators.planets_in_ninth.join(", ") : "None" },
          ]}
        />
      </ReportSection>
      <ReportSection title="Purpose windows" accent={config.color}>
        {output.purpose_windows?.map((period) => (
          <div key={`${period.planet}-${period.start}`} style={{ borderRadius: 18, padding: 16, background: "rgba(244, 236, 225, 0.78)" }}>
            <strong>{period.planet}</strong>
            <p style={{ margin: "6px 0" }}>
              {period.start} to {period.end}
            </p>
            <p style={{ margin: 0 }}>{period.description}</p>
          </div>
        ))}
      </ReportSection>
      <ReportSection title="Supportive remedies" accent={config.color}>
        <RemediesGrid remedies={output.remedies} />
      </ReportSection>
    </div>
  );
}

function GainsNetworkRenderer({ report, config }) {
  const output = report.output_payload;
  const indicators = output.gains_indicators;
  return (
    <div style={{ display: "grid", gap: 18 }}>
      <ReportSection title="Gains signature" accent={config.color}>
        <p style={{ margin: 0 }}>{output.gains_signature}</p>
        <p style={{ margin: 0 }}>{output.network_style}</p>
        <p style={{ margin: 0 }}>{output.aspiration_blocks}</p>
        <p style={{ margin: 0 }}>{output.activation_path}</p>
      </ReportSection>
      <ReportSection title="11th house indicators" accent={config.color}>
        <LabelValueGrid
          items={[
            { label: "11th Lord", value: `${indicators.eleventh_lord} • House ${indicators.eleventh_lord_house}` },
            { label: "Saturn", value: `House ${indicators.saturn_house}` },
            { label: "Lagna Lord", value: `${indicators.lagna_lord} • House ${indicators.lagna_lord_house}` },
            { label: "Planets In 11th", value: indicators.planets_in_eleventh?.length ? indicators.planets_in_eleventh.join(", ") : "None" },
          ]}
        />
      </ReportSection>
      <ReportSection title="Gains windows" accent={config.color}>
        {output.gains_windows?.map((period) => (
          <div key={`${period.planet}-${period.start}`} style={{ borderRadius: 18, padding: 16, background: "rgba(244, 236, 225, 0.78)" }}>
            <strong>{period.planet}</strong>
            <p style={{ margin: "6px 0" }}>
              {period.start} to {period.end}
            </p>
            <p style={{ margin: 0 }}>{period.description}</p>
          </div>
        ))}
      </ReportSection>
      <ReportSection title="Supportive remedies" accent={config.color}>
        <RemediesGrid remedies={output.remedies} />
      </ReportSection>
    </div>
  );
}

function ArchivedSummary({ item, config }) {
  return (
    <div style={{ display: "grid", gap: 18 }}>
      <ReportSection title="Archived summary" accent={config.color}>
        <p style={{ margin: 0 }}>{item.summary}</p>
        <p style={{ margin: 0, color: "#6d5b4d" }}>
          Temple's Phase 3 backend does not expose a report detail endpoint yet, so history can always show the stored summary and can show the full renderer when this device has the generated payload cached locally.
        </p>
      </ReportSection>
    </div>
  );
}

function renderFullReport(report, config) {
  switch (report.report_type) {
    case "karmic_debt":
      return <KarmicDebtRenderer report={report} config={config} />;
    case "career_blueprint":
      return <CareerRenderer report={report} config={config} />;
    case "shadow_self":
      return <ShadowRenderer report={report} config={config} />;
    case "retrograde_survival":
      return <RetrogradeRenderer report={report} config={config} />;
    case "life_cycles":
      return <LifeCyclesRenderer report={report} config={config} />;
    case "wealth_blueprint":
      return <WealthRenderer report={report} config={config} />;
    case "romance_creative":
      return <RomanceCreativeRenderer report={report} config={config} />;
    case "vitality_health":
      return <VitalityHealthRenderer report={report} config={config} />;
    case "partnership_window":
      return <PartnershipRenderer report={report} config={config} />;
    case "dharma_purpose":
      return <DharmaPurposeRenderer report={report} config={config} />;
    case "gains_network":
      return <GainsNetworkRenderer report={report} config={config} />;
    default:
      return <ArchivedSummary item={report} config={config} />;
  }
}

function ReportPanel({ selectedReport, currentReport, archivedSummary, onGenerateMore }) {
  const content = currentReport ? renderFullReport(currentReport, selectedReport) : archivedSummary ? <ArchivedSummary item={archivedSummary} config={selectedReport} /> : null;

  return (
    <section style={{ display: "grid", gap: 18 }}>
      <section style={{ ...surfaceStyle, padding: 24 }}>
        <p style={{ margin: "0 0 10px", fontSize: 12, letterSpacing: "0.18em", textTransform: "uppercase", color: selectedReport.color }}>
          {selectedReport.shortName}
        </p>
        <h2 style={{ margin: "0 0 8px", fontSize: 34, fontFamily: "Georgia, Times New Roman, serif" }}>Your report</h2>
        <p style={{ margin: 0, color: "#665548", lineHeight: 1.7 }}>
          Generated reports render in full on this page. Archived history entries can always reopen their summary, and reopen the complete report when the full payload is available on this device.
        </p>
      </section>
      {content || (
        <section style={{ ...surfaceStyle, padding: 24 }}>
          <h3 style={{ marginTop: 0 }}>Nothing generated yet</h3>
          <p style={{ color: "#6c5c4f", lineHeight: 1.68 }}>
            Select a report, complete the input form, and generate to see the AI-enriched output here.
          </p>
          <button type="button" onClick={onGenerateMore} style={{ ...buttonBase, background: selectedReport.color, color: "#fffaf2" }}>
            Generate {selectedReport.shortName}
          </button>
        </section>
      )}
    </section>
  );
}

function HistoryPanel({ items, loading, error, onOpenReport, onGenerate }) {
  const deferredItems = useDeferredValue(items);
  return (
    <section style={{ display: "grid", gap: 16 }}>
      <section style={{ ...surfaceStyle, padding: 24 }}>
        <p style={{ margin: "0 0 10px", fontSize: 12, letterSpacing: "0.18em", textTransform: "uppercase", color: "#94734c" }}>History</p>
        <h2 style={{ margin: "0 0 8px", fontSize: 32, fontFamily: "Georgia, Times New Roman, serif" }}>All individual reports in one timeline</h2>
        <p style={{ margin: 0, color: "#675548", lineHeight: 1.68 }}>
          The page fetches all individual report history endpoints in parallel, merges the results, and sorts them by creation time so the most recent reading stays on top.
        </p>
      </section>

      {loading ? <section style={{ ...surfaceStyle, padding: 20 }}>Loading report history...</section> : null}
      {error ? <section style={{ ...surfaceStyle, padding: 20, color: "#8d392b" }}>{error}</section> : null}

      {!loading && !deferredItems.length ? (
        <section style={{ ...surfaceStyle, padding: 24 }}>
          <h3 style={{ marginTop: 0 }}>No report history yet</h3>
          <p style={{ color: "#6d5b4d", lineHeight: 1.68 }}>Your archive will appear here after your first generated Individual Report.</p>
        </section>
      ) : null}

      {deferredItems.map((item) => (
        <article key={item.id} style={{ ...surfaceStyle, padding: 20, borderLeft: `5px solid ${item.accent}` }}>
          <div style={{ display: "flex", justifyContent: "space-between", gap: 14, flexWrap: "wrap", alignItems: "flex-start" }}>
            <div style={{ display: "grid", gap: 8 }}>
              <div style={{ fontSize: 12, letterSpacing: "0.14em", textTransform: "uppercase", color: item.accent }}>{item.label}</div>
              <h3 style={{ margin: 0, fontSize: 24, fontFamily: "Georgia, Times New Roman, serif" }}>{humanDate(item.created_at)}</h3>
              <p style={{ margin: 0, color: "#675548", lineHeight: 1.66 }}>{item.summary}</p>
            </div>
            <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
              <button type="button" onClick={() => onOpenReport(item)} style={{ ...buttonBase, background: item.accent, color: "#fffaf2" }}>
                View Report
              </button>
              <button
                type="button"
                onClick={() => onGenerate(item.report_type)}
                style={{ ...buttonBase, background: "rgba(255,255,255,0.72)", color: "#31261d", borderColor: "rgba(92, 66, 32, 0.12)" }}
              >
                Generate More
              </button>
            </div>
          </div>
        </article>
      ))}
    </section>
  );
}

function IndividualReportsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const query = useMemo(() => new URLSearchParams(location.search), [location.search]);

  const initialReport = REPORT_CONFIGS.find((item) => item.type === query.get("reportType")) || REPORT_CONFIGS[0];
  const initialTab = ["select", "generate", "report", "history"].includes(query.get("tab")) ? query.get("tab") : "select";

  const [selectedReport, setSelectedReport] = useState(initialReport);
  const [activeTab, setActiveTab] = useState(initialTab);
  const [form, setForm] = useState(defaultFormState(initialReport.type));
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState("");
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState("");
  const [historyItems, setHistoryItems] = useState([]);
  const [currentReport, setCurrentReport] = useState(null);
  const [archivedSummary, setArchivedSummary] = useState(null);

  useSeo(selectedReport, activeTab, currentReport || archivedSummary);

  useEffect(() => {
    const reportId = query.get("reportId");
    const reportType = query.get("reportType");
    if (!reportId || !reportType) return;
    const config = REPORT_CONFIGS.find((item) => item.type === reportType);
    if (!config) return;
    setSelectedReport(config);
    const cached = findCachedReport(reportId);
    if (cached) {
      setCurrentReport(cached);
      setArchivedSummary(null);
      setActiveTab("report");
      return;
    }
    const historyMatch = historyItems.find((item) => item.id === reportId);
    if (historyMatch) {
      setCurrentReport(null);
      setArchivedSummary(historyMatch);
      setActiveTab("report");
    }
  }, [historyItems, query]);

  useEffect(() => {
    let active = true;
    async function loadHistory() {
      setHistoryLoading(true);
      setHistoryError("");
      try {
        const responses = await Promise.allSettled(
          REPORT_CONFIGS.map((config) => axios.get(`${API_BASE}/reports/${config.slug}/history`, { withCredentials: true }))
        );
        if (!active) return;
        const merged = REPORT_CONFIGS.flatMap((config, index) =>
          (responses[index].status === "fulfilled" ? (responses[index].value.data?.items || []) : []).map((item) => normalizeHistoryEntry(item, config))
        ).sort((left, right) => new Date(right.created_at).getTime() - new Date(left.created_at).getTime());
        setHistoryItems(merged);
      } catch (error) {
        if (!active) return;
        setHistoryError(error?.response?.data?.detail || "Unable to load your report history right now.");
      } finally {
        if (active) setHistoryLoading(false);
      }
    }
    loadHistory();
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    setForm((previous) => {
      const next = { ...defaultFormState(selectedReport.type), ...previous };
      if (selectedReport.type !== "retrograde_survival") {
        next.retrograde_mode = "personal";
      }
      return next;
    });
  }, [selectedReport.type]);

  function syncQuery(nextReport, nextTab, reportId) {
    const params = new URLSearchParams();
    params.set("reportType", nextReport.type);
    params.set("tab", nextTab);
    if (reportId) params.set("reportId", reportId);
    navigate({ pathname: "/reports", search: params.toString() }, { replace: true });
  }

  function handleSelectReport(report) {
    setSelectedReport(report);
    setForm(defaultFormState(report.type));
    setFormError("");
    syncQuery(report, activeTab === "report" ? "select" : activeTab);
  }

  function handleGeneratePath(reportOrType) {
    const nextReport = typeof reportOrType === "string" ? REPORT_CONFIGS.find((item) => item.type === reportOrType) || selectedReport : reportOrType;
    setSelectedReport(nextReport);
    setActiveTab("generate");
    setForm(defaultFormState(nextReport.type));
    setFormError("");
    syncQuery(nextReport, "generate");
  }

  function handleFormChange(field, value) {
    setForm((previous) => {
      if (field === "city_slug") {
        const city = value || EMPTY_CITY;
        return {
          ...previous,
          city_slug: city.slug,
          city_name: city.city_name,
          latitude: city.latitude,
          longitude: city.longitude,
          timezone: city.timezone,
        };
      }
      return { ...previous, [field]: value };
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setFormError("");

    // Guard: city picker must be selected (latitude + longitude are required by all backends)
    const needsBirth = selectedReport.type !== "retrograde_survival" || form.retrograde_mode === "personal";
    if (needsBirth && (!form.latitude || !form.longitude)) {
      setFormError("Please select a birth city from the dropdown -- start typing and choose a result.");
      return;
    }

    setSubmitting(true);
    try {
      let payload;
      if (selectedReport.type === "retrograde_survival") {
        payload = {
          check_date: form.check_date || undefined,
          planet: form.retrograde_planet || undefined,
        };
        if (form.retrograde_mode === "personal") {
          payload.birth_data = buildBirthPayload(form);
        }
      } else {
        payload = buildBirthPayload(form);
      }

      const response = await axios.post(`${API_BASE}/reports/${selectedReport.slug}/generate`, payload, { withCredentials: true });
      const generated = response.data?.report;
      if (!generated) throw new Error("No report returned.");
      saveCachedReport(generated);
      startTransition(() => {
        setCurrentReport(generated);
        setArchivedSummary(null);
        setActiveTab("report");
        syncQuery(selectedReport, "report", generated.id);
        setHistoryItems((previous) => {
          const normalized = normalizeHistoryEntry(
            {
              id: generated.id,
              report_type: generated.report_type,
              report_slug: generated.report_slug,
              summary: generated.summary,
              created_at: generated.created_at,
            },
            selectedReport
          );
          const filtered = previous.filter((item) => item.id !== normalized.id);
          return [normalized, ...filtered].sort((left, right) => new Date(right.created_at).getTime() - new Date(left.created_at).getTime());
        });
      });
    } catch (error) {
      setFormError(error?.response?.data?.detail || "The report could not be generated right now. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  function handleOpenHistoryItem(item) {
    const config = REPORT_CONFIGS.find((entry) => entry.type === item.report_type) || selectedReport;
    setSelectedReport(config);
    const cached = findCachedReport(item.id);
    if (cached) {
      setCurrentReport(cached);
      setArchivedSummary(null);
    } else {
      setCurrentReport(null);
      setArchivedSummary(item);
    }
    setActiveTab("report");
    syncQuery(config, "report", item.id);
  }

  return (
    <div style={pageStyle}>
      <div style={{ maxWidth: 1200, margin: "0 auto", display: "grid", gap: 18 }}>
        <SectionTabs
          activeTab={activeTab}
          onChange={(nextTab) => {
            setActiveTab(nextTab);
            syncQuery(selectedReport, nextTab, nextTab === "report" && currentReport ? currentReport.id : undefined);
          }}
        />

        {activeTab === "select" ? <ReportCards selectedReport={selectedReport} onSelect={handleSelectReport} onGenerate={handleGeneratePath} /> : null}

        {activeTab === "generate" ? (
          <GeneratePanel
            selectedReport={selectedReport}
            form={form}
            onFormChange={handleFormChange}
            onSubmit={handleSubmit}
            submitting={submitting}
            error={formError}
          />
        ) : null}

        {activeTab === "report" ? (
          <ReportPanel
            selectedReport={selectedReport}
            currentReport={currentReport}
            archivedSummary={archivedSummary}
            onGenerateMore={() => handleGeneratePath(selectedReport)}
          />
        ) : null}

        {activeTab === "history" ? (
          <HistoryPanel
            items={historyItems}
            loading={historyLoading}
            error={historyError}
            onOpenReport={handleOpenHistoryItem}
            onGenerate={handleGeneratePath}
          />
        ) : null}
      </div>
    </div>
  );
}

export default IndividualReportsPage;
