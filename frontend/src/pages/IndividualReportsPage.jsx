import React, { startTransition, useDeferredValue, useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Link, useLocation, useNavigate } from "react-router-dom";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const REPORTS = [
  {
    type: "karmic_debt",
    slug: "karmic-debt",
    name: "Karmic Debt & Past Life",
    eyebrow: "Patterns & karma",
    description: "Decode repeating life loops through Saturn, Rahu-Ketu, retrogrades, and the Atmakaraka.",
    accent: "#8d4f3d",
  },
  {
    type: "career_blueprint",
    slug: "career-blueprint",
    name: "Career & Success Blueprint",
    eyebrow: "Work & destiny",
    description: "Map public direction, career strengths, wealth signatures, and Dasha-backed peak periods.",
    accent: "#586b43",
  },
  {
    type: "shadow_self",
    slug: "shadow-self",
    name: "Shadow Self & Hidden Qualities",
    eyebrow: "Inner landscape",
    description: "Read Janma Nakshatra, hidden strengths, blind spots, and subtle inner pressure points.",
    accent: "#315665",
  },
  {
    type: "retrograde_survival",
    slug: "retrograde-survival",
    name: "Retrograde Survival Guide",
    eyebrow: "Current timing",
    description: "Understand Mercury, Venus, or Mars retrograde periods in general or through your natal houses.",
    accent: "#6a4b89",
  },
  {
    type: "life_cycles",
    slug: "life-cycles",
    name: "The Pattern of Life Cycles",
    eyebrow: "Dasha timeline",
    description: "See the current Maha and Antar Dasha, next transitions, and the larger chapter now unfolding.",
    accent: "#9a6a26",
  },
];

const CITY_OPTIONS = [
  { label: "New Delhi", city_name: "New Delhi", latitude: 28.6139, longitude: 77.209, timezone: "Asia/Kolkata" },
  { label: "Mumbai", city_name: "Mumbai", latitude: 19.076, longitude: 72.8777, timezone: "Asia/Kolkata" },
  { label: "Bengaluru", city_name: "Bengaluru", latitude: 12.9716, longitude: 77.5946, timezone: "Asia/Kolkata" },
  { label: "Kolkata", city_name: "Kolkata", latitude: 22.5726, longitude: 88.3639, timezone: "Asia/Kolkata" },
  { label: "Chennai", city_name: "Chennai", latitude: 13.0827, longitude: 80.2707, timezone: "Asia/Kolkata" },
  { label: "Hyderabad", city_name: "Hyderabad", latitude: 17.385, longitude: 78.4867, timezone: "Asia/Kolkata" },
  { label: "Pune", city_name: "Pune", latitude: 18.5204, longitude: 73.8567, timezone: "Asia/Kolkata" },
  { label: "Ahmedabad", city_name: "Ahmedabad", latitude: 23.0225, longitude: 72.5714, timezone: "Asia/Kolkata" },
  { label: "Jaipur", city_name: "Jaipur", latitude: 26.9124, longitude: 75.7873, timezone: "Asia/Kolkata" },
  { label: "Lucknow", city_name: "Lucknow", latitude: 26.8467, longitude: 80.9462, timezone: "Asia/Kolkata" },
  { label: "New York", city_name: "New York", latitude: 40.7128, longitude: -74.006, timezone: "America/New_York" },
  { label: "London", city_name: "London", latitude: 51.5072, longitude: -0.1276, timezone: "Europe/London" },
  { label: "Dubai", city_name: "Dubai", latitude: 25.2048, longitude: 55.2708, timezone: "Asia/Dubai" },
  { label: "Singapore", city_name: "Singapore", latitude: 1.3521, longitude: 103.8198, timezone: "Asia/Singapore" },
];

const HISTORY_CACHE_KEY = "individual_reports_full_cache_v1";

const pageStyle = {
  minHeight: "100vh",
  background:
    "radial-gradient(circle at top left, rgba(157,106,38,0.18), transparent 26%), radial-gradient(circle at top right, rgba(49,86,101,0.14), transparent 22%), linear-gradient(180deg, #faf6ef 0%, #f4ede2 100%)",
  color: "#2a2119",
  padding: "28px 18px 72px",
};

const shellStyle = {
  maxWidth: 1180,
  margin: "0 auto",
  display: "grid",
  gap: 18,
};

const cardStyle = {
  background: "rgba(255, 250, 244, 0.88)",
  border: "1px solid rgba(120,90,55,0.14)",
  borderRadius: 24,
  boxShadow: "0 18px 46px rgba(74, 50, 22, 0.09)",
  backdropFilter: "blur(10px)",
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
  const current = loadCachedReports();
  current[report.id] = report;
  window.localStorage.setItem(HISTORY_CACHE_KEY, JSON.stringify(current));
}

function useSeo(reportConfig, activeTab, currentReport) {
  useEffect(() => {
    const titleBase = reportConfig ? `${reportConfig.name} | Everyday Horoscope` : "Individual Reports | Everyday Horoscope";
    const title = currentReport ? `${reportConfig?.name || "Report"} Ready | Everyday Horoscope` : activeTab === "history" ? "My Individual Reports | Everyday Horoscope" : titleBase;
    document.title = title;
    const description =
      currentReport?.summary ||
      reportConfig?.description ||
      "Generate premium Vedic individual reports for karmic patterns, career, shadow work, retrogrades, and life cycles.";

    let meta = document.querySelector('meta[name="description"]');
    if (!meta) {
      meta = document.createElement("meta");
      meta.setAttribute("name", "description");
      document.head.appendChild(meta);
    }
    meta.setAttribute("content", description);
  }, [activeTab, currentReport, reportConfig]);
}

function queryParams(search) {
  return new URLSearchParams(search);
}

function defaultBirthState() {
  return {
    city_mode: "preset",
    city_code: CITY_OPTIONS[0].label,
    city_name: CITY_OPTIONS[0].city_name,
    latitude: CITY_OPTIONS[0].latitude,
    longitude: CITY_OPTIONS[0].longitude,
    timezone: CITY_OPTIONS[0].timezone,
    date: "",
    time: "",
    check_date: new Date().toISOString().slice(0, 10),
    retrograde_mode: "personal",
    retrograde_planet: "Mercury",
  };
}

function applyPreset(state, code) {
  const preset = CITY_OPTIONS.find((item) => item.label === code) || CITY_OPTIONS[0];
  return {
    ...state,
    city_code: preset.label,
    city_name: preset.city_name,
    latitude: preset.latitude,
    longitude: preset.longitude,
    timezone: preset.timezone,
  };
}

function toBirthPayload(form) {
  return {
    date: form.date,
    time: form.time,
    city_name: form.city_name,
    latitude: Number(form.latitude),
    longitude: Number(form.longitude),
    timezone: form.timezone,
  };
}

function SectionTabs({ activeTab, setActiveTab }) {
  const tabs = [
    ["select", "Select"],
    ["generate", "Generate"],
    ["report", "Report"],
    ["history", "History"],
  ];
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
      {tabs.map(([key, label]) => (
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

function ReportSelector({ selected, onSelect }) {
  return (
    <section style={{ ...cardStyle, padding: 24 }}>
      <div style={{ marginBottom: 18 }}>
        <p style={{ margin: "0 0 10px", fontSize: 12, letterSpacing: "0.2em", textTransform: "uppercase", color: "#8c6a39" }}>Individual Reports</p>
        <h1 style={{ margin: 0, fontSize: "clamp(2rem, 5vw, 3.6rem)", lineHeight: 0.94, fontFamily: "Georgia, Times New Roman, serif" }}>
          Choose the report that matches the question your soul keeps circling.
        </h1>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 16 }}>
        {REPORTS.map((item) => {
          const active = item.type === selected.type;
          return (
            <button
              key={item.type}
              type="button"
              onClick={() => onSelect(item)}
              style={{
                textAlign: "left",
                padding: 20,
                borderRadius: 22,
                border: active ? `1px solid ${item.accent}` : "1px solid rgba(120,90,55,0.14)",
                background: active ? `linear-gradient(180deg, ${item.accent}16, rgba(255,250,244,0.96))` : "rgba(255,255,255,0.76)",
                cursor: "pointer",
                boxShadow: active ? "0 14px 32px rgba(74, 50, 22, 0.12)" : "none",
              }}
            >
              <p style={{ margin: "0 0 8px", fontSize: 11, letterSpacing: "0.14em", textTransform: "uppercase", color: item.accent }}>{item.eyebrow}</p>
              <h2 style={{ margin: "0 0 10px", fontSize: 22, lineHeight: 1.05, color: "#2a2119", fontFamily: "Georgia, Times New Roman, serif" }}>{item.name}</h2>
              <p style={{ margin: 0, lineHeight: 1.62, color: "#64584c" }}>{item.description}</p>
            </button>
          );
        })}
      </div>
    </section>
  );
}

function BirthFields({ form, setForm, selected }) {
  const showRetroToggle = selected.type === "retrograde_survival";
  const personalMode = !showRetroToggle || form.retrograde_mode === "personal";

  return (
    <section style={{ ...cardStyle, padding: 24 }}>
      <div style={{ display: "grid", gap: 14 }}>
        <div>
          <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: selected.accent }}>{selected.eyebrow}</p>
          <h2 style={{ margin: "0 0 8px", fontSize: 30, fontFamily: "Georgia, Times New Roman, serif" }}>Generate {selected.name}</h2>
          <p style={{ margin: 0, color: "#62574a", lineHeight: 1.64 }}>{selected.description}</p>
        </div>

        {showRetroToggle ? (
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            {[
              ["personal", "Personal mode"],
              ["general", "General mode"],
            ].map(([value, label]) => (
              <button
                key={value}
                type="button"
                onClick={() => setForm((current) => ({ ...current, retrograde_mode: value }))}
                style={{
                  minHeight: 42,
                  padding: "10px 14px",
                  borderRadius: 999,
                  border: "1px solid rgba(120,90,55,0.16)",
                  background: form.retrograde_mode === value ? "linear-gradient(135deg, #b78646 0%, #d8af6a 100%)" : "rgba(255,255,255,0.7)",
                  cursor: "pointer",
                  fontWeight: 700,
                }}
              >
                {label}
              </button>
            ))}
          </div>
        ) : null}

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 14 }}>
          <label style={{ display: "grid", gap: 6 }}>
            <span style={{ fontWeight: 700 }}>Check date</span>
            <input type="date" value={form.check_date} onChange={(event) => setForm((current) => ({ ...current, check_date: event.target.value }))} style={inputStyle} />
          </label>

          {showRetroToggle ? (
            <label style={{ display: "grid", gap: 6 }}>
              <span style={{ fontWeight: 700 }}>Retrograde planet</span>
              <select value={form.retrograde_planet} onChange={(event) => setForm((current) => ({ ...current, retrograde_planet: event.target.value }))} style={inputStyle}>
                <option value="Mercury">Mercury</option>
                <option value="Venus">Venus</option>
                <option value="Mars">Mars</option>
              </select>
            </label>
          ) : null}
        </div>

        {personalMode ? (
          <>
            <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
              {[
                ["preset", "Use city picker"],
                ["manual", "Enter manually"],
              ].map(([value, label]) => (
                <button
                  key={value}
                  type="button"
                  onClick={() => setForm((current) => ({ ...current, city_mode: value }))}
                  style={{
                    minHeight: 42,
                    padding: "10px 14px",
                    borderRadius: 999,
                    border: "1px solid rgba(120,90,55,0.16)",
                    background: form.city_mode === value ? "rgba(184, 134, 70, 0.16)" : "rgba(255,255,255,0.7)",
                    cursor: "pointer",
                    fontWeight: 700,
                  }}
                >
                  {label}
                </button>
              ))}
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 14 }}>
              <label style={{ display: "grid", gap: 6 }}>
                <span style={{ fontWeight: 700 }}>Birth date</span>
                <input type="date" value={form.date} onChange={(event) => setForm((current) => ({ ...current, date: event.target.value }))} style={inputStyle} />
              </label>
              <label style={{ display: "grid", gap: 6 }}>
                <span style={{ fontWeight: 700 }}>Birth time</span>
                <input type="time" value={form.time} onChange={(event) => setForm((current) => ({ ...current, time: event.target.value }))} style={inputStyle} />
              </label>
            </div>

            {form.city_mode === "preset" ? (
              <label style={{ display: "grid", gap: 6 }}>
                <span style={{ fontWeight: 700 }}>City</span>
                <select
                  value={form.city_code}
                  onChange={(event) => setForm((current) => applyPreset(current, event.target.value))}
                  style={inputStyle}
                >
                  {CITY_OPTIONS.map((item) => (
                    <option key={item.label} value={item.label}>
                      {item.label}
                    </option>
                  ))}
                </select>
              </label>
            ) : null}

            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 14 }}>
              <label style={{ display: "grid", gap: 6 }}>
                <span style={{ fontWeight: 700 }}>City name</span>
                <input value={form.city_name} onChange={(event) => setForm((current) => ({ ...current, city_name: event.target.value }))} style={inputStyle} />
              </label>
              <label style={{ display: "grid", gap: 6 }}>
                <span style={{ fontWeight: 700 }}>Timezone</span>
                <input value={form.timezone} onChange={(event) => setForm((current) => ({ ...current, timezone: event.target.value }))} style={inputStyle} />
              </label>
              <label style={{ display: "grid", gap: 6 }}>
                <span style={{ fontWeight: 700 }}>Latitude</span>
                <input value={form.latitude} onChange={(event) => setForm((current) => ({ ...current, latitude: event.target.value }))} style={inputStyle} />
              </label>
              <label style={{ display: "grid", gap: 6 }}>
                <span style={{ fontWeight: 700 }}>Longitude</span>
                <input value={form.longitude} onChange={(event) => setForm((current) => ({ ...current, longitude: event.target.value }))} style={inputStyle} />
              </label>
            </div>
          </>
        ) : (
          <div style={{ padding: 18, borderRadius: 18, background: "rgba(106,75,137,0.08)", color: "#5c5066", lineHeight: 1.64 }}>
            General mode skips birth details and returns a broader retrograde guide for the selected planet and date.
          </div>
        )}
      </div>
    </section>
  );
}

const inputStyle = {
  minHeight: 46,
  borderRadius: 14,
  border: "1px solid rgba(120,90,55,0.16)",
  background: "rgba(255,255,255,0.88)",
  padding: "12px 14px",
  color: "#2a2119",
};

function ReportRenderer({ report, onReset }) {
  if (!report) {
    return (
      <section style={{ ...cardStyle, padding: 24 }}>
        <h2 style={{ marginTop: 0 }}>No report open yet</h2>
        <p style={{ color: "#63594d" }}>Generate a report or open one from your cached history on this device.</p>
      </section>
    );
  }

  const output = report.output_payload || {};
  const type = report.report_type;
  const archivedSummaryOnly = !output || !Object.keys(output).length;

  if (archivedSummaryOnly) {
    return (
      <section style={{ ...cardStyle, padding: 24 }}>
        <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.18em", textTransform: "uppercase", color: "#8c6a39" }}>Archived summary</p>
        <h2 style={{ marginTop: 0 }}>{report.report_slug?.replaceAll("-", " ") || "Saved report"}</h2>
        <p style={{ color: "#62574a", lineHeight: 1.64 }}>{report.summary}</p>
        <p style={{ color: "#7b6b5d", lineHeight: 1.64 }}>
          The history endpoint for this report family returns summary cards, not the full stored payload. If this report was generated on this device it will open fully from cache; otherwise the summary is shown here until a dedicated detail endpoint exists.
        </p>
        <button type="button" onClick={onReset} style={primaryButtonStyle}>
          Generate another report
        </button>
      </section>
    );
  }

  return (
    <section style={{ ...cardStyle, padding: 24, display: "grid", gap: 16 }}>
      <div>
        <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.18em", textTransform: "uppercase", color: "#8c6a39" }}>
          {report.report_slug?.replaceAll("-", " ")}
        </p>
        <h2 style={{ margin: "0 0 10px", fontSize: 34, fontFamily: "Georgia, Times New Roman, serif" }}>{report.summary}</h2>
      </div>

      {type === "karmic_debt" ? <KarmicDebtView output={output} /> : null}
      {type === "career_blueprint" ? <CareerBlueprintView output={output} /> : null}
      {type === "shadow_self" ? <ShadowSelfView output={output} /> : null}
      {type === "retrograde_survival" ? <RetrogradeView output={output} /> : null}
      {type === "life_cycles" ? <LifeCyclesView output={output} /> : null}

      <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
        <button type="button" onClick={onReset} style={primaryButtonStyle}>
          Generate more
        </button>
        <Link to="/my-reports" style={ghostLinkStyle}>
          Go to My Reports
        </Link>
      </div>
    </section>
  );
}

function InfoGrid({ items }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 12 }}>
      {items.map((item) => (
        <article key={item.label} style={{ ...cardStyle, padding: 18, borderRadius: 18 }}>
          <p style={{ margin: "0 0 6px", fontSize: 12, letterSpacing: "0.1em", textTransform: "uppercase", color: "#8a6d42" }}>{item.label}</p>
          <div style={{ fontSize: 18, lineHeight: 1.4 }}>{item.value}</div>
        </article>
      ))}
    </div>
  );
}

function TextSection({ title, body }) {
  if (!body) return null;
  return (
    <article style={{ ...cardStyle, padding: 20, borderRadius: 20 }}>
      <h3 style={{ marginTop: 0, fontSize: 24, fontFamily: "Georgia, Times New Roman, serif" }}>{title}</h3>
      <p style={{ margin: 0, color: "#60564b", lineHeight: 1.7 }}>{body}</p>
    </article>
  );
}

function RemedyPanel({ remedies }) {
  if (!remedies) return null;
  return (
    <section style={{ ...cardStyle, padding: 20, borderRadius: 20 }}>
      <h3 style={{ marginTop: 0, fontSize: 24, fontFamily: "Georgia, Times New Roman, serif" }}>Supportive remedies</h3>
      <div style={{ display: "grid", gap: 12 }}>
        {remedies.mantra ? (
          <div>
            <strong>Mantra:</strong> {remedies.mantra.text}
            <div style={{ color: "#74695d", marginTop: 4 }}>{remedies.mantra.practice}</div>
          </div>
        ) : null}
        {remedies.gemstone ? (
          <div>
            <strong>Gemstone:</strong> {remedies.gemstone.stone}
            <div style={{ color: "#74695d", marginTop: 4 }}>{remedies.gemstone.purpose}</div>
          </div>
        ) : null}
        {remedies.ritual ? (
          <div>
            <strong>Ritual:</strong> <span style={{ color: "#74695d" }}>{remedies.ritual}</span>
          </div>
        ) : null}
      </div>
    </section>
  );
}

function KarmicDebtView({ output }) {
  return (
    <>
      <InfoGrid
        items={[
          { label: "Saturn House", value: output.karmic_indicators?.saturn_house || "—" },
          { label: "Rahu House", value: output.karmic_indicators?.rahu_house || "—" },
          { label: "Ketu House", value: output.karmic_indicators?.ketu_house || "—" },
          { label: "Atmakaraka", value: output.karmic_indicators?.atmakaraka || "—" },
        ]}
      />
      <TextSection title={output.report?.headline || "Karmic theme"} body={output.report?.karmic_theme} />
      <TextSection title="Past life echo" body={output.report?.past_life_echo} />
      <TextSection title="Atmakaraka insight" body={output.report?.atmakaraka_insight} />
      {output.report?.retrograde_lessons?.length ? (
        <section style={{ ...cardStyle, padding: 20, borderRadius: 20 }}>
          <h3 style={{ marginTop: 0, fontSize: 24, fontFamily: "Georgia, Times New Roman, serif" }}>Retrograde lessons</h3>
          <div style={{ display: "grid", gap: 12 }}>
            {output.report.retrograde_lessons.map((item) => (
              <div key={item.planet}>
                <strong>{item.planet}</strong>
                <div style={{ color: "#6f6357", marginTop: 4 }}>{item.lesson}</div>
              </div>
            ))}
          </div>
        </section>
      ) : null}
      <TextSection title="Breaking the cycle" body={output.report?.breaking_the_cycle} />
      <RemedyPanel remedies={output.report?.remedies} />
    </>
  );
}

function CareerBlueprintView({ output }) {
  return (
    <>
      <TextSection title="Career archetype" body={output.career_archetype} />
      <TextSection title="Natural strengths" body={output.natural_strengths} />
      <TextSection title="Success formula" body={output.success_formula} />
      <TextSection title="Wealth signature" body={output.wealth_signature} />
      {output.peak_periods?.length ? (
        <section style={{ ...cardStyle, padding: 20, borderRadius: 20 }}>
          <h3 style={{ marginTop: 0, fontSize: 24, fontFamily: "Georgia, Times New Roman, serif" }}>Peak periods</h3>
          <div style={{ display: "grid", gap: 12 }}>
            {output.peak_periods.map((period) => (
              <div key={`${period.planet}-${period.start}`}>
                <strong>{period.planet}</strong> <span style={{ color: "#826a4a" }}>{period.start} to {period.end}</span>
                <div style={{ color: "#6c6054", marginTop: 4 }}>{period.description}</div>
              </div>
            ))}
          </div>
        </section>
      ) : null}
      <TextSection title="Action guidance" body={output.action_guidance} />
      <RemedyPanel remedies={output.remedies} />
    </>
  );
}

function ShadowSelfView({ output }) {
  return (
    <>
      <TextSection title="Janma Nakshatra" body={output.janma_nakshatra} />
      <TextSection title="Shadow Nakshatra" body={output.shadow_nakshatra} />
      <TextSection title="Hidden strengths" body={output.hidden_strengths} />
      <TextSection title="Blind spots" body={output.blind_spots} />
      <TextSection title="Psychological driver" body={output.psychological_driver} />
      <TextSection title="Integration path" body={output.integration_path} />
      <RemedyPanel remedies={output.remedies} />
    </>
  );
}

function RetrogradeView({ output }) {
  return (
    <>
      <InfoGrid
        items={[
          { label: "Mode", value: output.mode || "—" },
          { label: "Active retrogrades", value: output.active_retrogrades?.length || 0 },
        ]}
      />
      {output.active_retrogrades?.length ? (
        output.active_retrogrades.map((item) => (
          <section key={`${item.planet}-${item.start_date}`} style={{ ...cardStyle, padding: 20, borderRadius: 20, display: "grid", gap: 12 }}>
            <div>
              <h3 style={{ margin: "0 0 4px", fontSize: 24, fontFamily: "Georgia, Times New Roman, serif" }}>{item.planet} Retrograde</h3>
              <p style={{ margin: 0, color: "#76695b" }}>{item.start_date} to {item.end_date}</p>
            </div>
            <TextSection title="Life area" body={item.life_area} />
            <TextSection title="What to expect" body={item.what_to_expect} />
            <InfoGrid
              items={[
                { label: "Transit house", value: item.transit_house || "General mode" },
                { label: "Avoid", value: item.what_to_avoid?.join(", ") || "—" },
              ]}
            />
            {item.navigation_tips?.length ? <TextSection title="Navigation tips" body={item.navigation_tips.join(" • ")} /> : null}
            <RemedyPanel remedies={item.remedies} />
          </section>
        ))
      ) : (
        <section style={{ ...cardStyle, padding: 24 }}>
          <h3 style={{ marginTop: 0 }}>No active retrogrades found</h3>
          <p style={{ color: "#6d6256", lineHeight: 1.68 }}>For the selected date and planet filter, no active Mercury, Venus, or Mars retrograde window was detected.</p>
        </section>
      )}
    </>
  );
}

function LifeCyclesView({ output }) {
  return (
    <>
      <TextSection title="Current chapter" body={output.current_chapter} />
      <TextSection title="Current sub-chapter" body={output.current_sub_chapter} />
      <TextSection title="Chapter quality" body={output.chapter_quality} />
      {output.upcoming_transitions?.length ? (
        <section style={{ ...cardStyle, padding: 20, borderRadius: 20 }}>
          <h3 style={{ marginTop: 0, fontSize: 24, fontFamily: "Georgia, Times New Roman, serif" }}>Upcoming transitions</h3>
          <div style={{ display: "grid", gap: 12 }}>
            {output.upcoming_transitions.map((item) => (
              <div key={`${item.planet}-${item.date}`}>
                <strong>{item.planet}</strong> <span style={{ color: "#8a6b45" }}>{item.date}</span>
                <div style={{ color: "#6b6055", marginTop: 4 }}>{item.theme}</div>
              </div>
            ))}
          </div>
        </section>
      ) : null}
      <TextSection title="This decade arc" body={output.this_decade_arc} />
      <RemedyPanel remedies={output.remedies} />
    </>
  );
}

function HistoryPanel({ historyMap, loadingHistory, historyError, onOpen, selectedType }) {
  const merged = REPORTS.flatMap((item) =>
    (historyMap[item.type] || []).map((entry) => ({
      ...entry,
      type: item.type,
      name: item.name,
      slug: item.slug,
      accent: item.accent,
    }))
  ).sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());

  return (
    <section style={{ ...cardStyle, padding: 24 }}>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
        <div>
          <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: "#8c6a39" }}>Archive</p>
          <h2 style={{ margin: 0, fontSize: 30, fontFamily: "Georgia, Times New Roman, serif" }}>Your individual reports</h2>
        </div>
        <div style={{ color: "#76695b" }}>Parallel fetch across all 5 report families</div>
      </div>

      {loadingHistory ? <p style={{ color: "#6d6256" }}>Opening your archive...</p> : null}
      {historyError ? <p style={{ color: "#8c3b2e" }}>{historyError}</p> : null}

      {!loadingHistory && !merged.length ? (
        <div style={{ marginTop: 18, padding: 20, borderRadius: 18, background: "rgba(255,255,255,0.65)" }}>
          <h3 style={{ marginTop: 0 }}>No reports yet</h3>
          <p style={{ color: "#6b6054" }}>Generate your first report to start building a personal Vedic archive.</p>
        </div>
      ) : null}

      <div style={{ marginTop: 18, display: "grid", gap: 14 }}>
        {merged
          .filter((entry) => !selectedType || selectedType === entry.type)
          .map((entry) => (
            <article key={entry.id} style={{ padding: 18, borderRadius: 18, background: "rgba(255,255,255,0.74)", border: `1px solid ${entry.accent}22` }}>
              <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "flex-start" }}>
                <div>
                  <p style={{ margin: "0 0 6px", fontSize: 12, letterSpacing: "0.12em", textTransform: "uppercase", color: entry.accent }}>{entry.name}</p>
                  <h3 style={{ margin: "0 0 8px", fontSize: 22, fontFamily: "Georgia, Times New Roman, serif" }}>{new Date(entry.created_at).toLocaleDateString()}</h3>
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

const ghostLinkStyle = {
  ...primaryButtonStyle,
  background: "rgba(255,255,255,0.72)",
  border: "1px solid rgba(120,90,55,0.16)",
  color: "#2a2119",
};

function IndividualReportsPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [selected, setSelected] = useState(REPORTS[0]);
  const [activeTab, setActiveTab] = useState("select");
  const deferredTab = useDeferredValue(activeTab);
  const [form, setForm] = useState(defaultBirthState);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [currentReport, setCurrentReport] = useState(null);
  const [historyMap, setHistoryMap] = useState({});
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [historyError, setHistoryError] = useState("");

  useSeo(selected, activeTab, currentReport);

  useEffect(() => {
    startTransition(() => {
      if (deferredTab === "generate" && !selected) setSelected(REPORTS[0]);
    });
  }, [deferredTab, selected]);

  useEffect(() => {
    let active = true;
    async function loadHistory() {
      setLoadingHistory(true);
      setHistoryError("");
      try {
        const responses = await Promise.all(
          REPORTS.map((item) =>
            axios.get(`${API}/reports/${item.slug}/history`, {
              withCredentials: true,
            })
          )
        );
        if (!active) return;
        const next = {};
        REPORTS.forEach((item, index) => {
          next[item.type] = responses[index].data?.items || [];
        });
        setHistoryMap(next);
      } catch (err) {
        if (!active) return;
        setHistoryError(err?.response?.data?.detail || "Unable to load individual report history right now.");
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
    if (reportType) {
      const target = REPORTS.find((item) => item.type === reportType || item.slug === reportType);
      if (target) setSelected(target);
    }
    if (reportId) {
      const cached = loadCachedReports()[reportId];
      if (cached) setCurrentReport(cached);
      else {
        const found =
          Object.values(historyMap)
            .flat()
            .find((item) => item.id === reportId) || null;
        if (found) setCurrentReport(found);
      }
    }
  }, [location.search, historyMap]);

  const canSubmit = useMemo(() => {
    if (selected.type === "retrograde_survival" && form.retrograde_mode === "general") {
      return Boolean(form.check_date);
    }
    return Boolean(form.date && form.time && form.city_name && form.latitude && form.longitude && form.timezone);
  }, [form, selected.type]);

  async function handleGenerate() {
    setSubmitting(true);
    setError("");
    try {
      let payload;
      if (selected.type === "retrograde_survival") {
        payload = {
          check_date: form.check_date,
          planet: form.retrograde_planet,
          birth_data: form.retrograde_mode === "personal" ? toBirthPayload(form) : null,
        };
      } else {
        payload = toBirthPayload(form);
      }
      const response = await axios.post(`${API}/reports/${selected.slug}/generate`, payload, {
        withCredentials: true,
      });
      const generated = response.data?.report || null;
      if (generated) {
        saveCachedReport(generated);
        setCurrentReport(generated);
        setHistoryMap((current) => ({
          ...current,
          [selected.type]: [
            {
              id: generated.id,
              report_type: generated.report_type,
              report_slug: generated.report_slug,
              summary: generated.summary,
              created_at: generated.created_at,
            },
            ...(current[selected.type] || []),
          ],
        }));
        setActiveTab("report");
        navigate(`/individual-reports?reportType=${selected.type}&reportId=${generated.id}&tab=report`, { replace: true });
      }
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to generate this report right now.");
    } finally {
      setSubmitting(false);
    }
  }

  function openHistoryItem(item) {
    const cached = loadCachedReports()[item.id];
    setCurrentReport(cached || item);
    const target = REPORTS.find((entry) => entry.type === item.type || entry.slug === item.report_slug);
    if (target) setSelected(target);
    setActiveTab("report");
    navigate(`/individual-reports?reportType=${item.type || item.report_type}&reportId=${item.id}&tab=report`, { replace: true });
  }

  function resetForNew() {
    setCurrentReport(null);
    setError("");
    setActiveTab("generate");
    navigate(`/individual-reports?reportType=${selected.type}&tab=generate`, { replace: true });
  }

  return (
    <div style={pageStyle}>
      <div style={shellStyle}>
        <SectionTabs activeTab={activeTab} setActiveTab={setActiveTab} />

        {activeTab === "select" ? <ReportSelector selected={selected} onSelect={(item) => { setSelected(item); setActiveTab("generate"); }} /> : null}
        {activeTab === "generate" ? (
          <>
            <ReportSelector selected={selected} onSelect={setSelected} />
            <BirthFields form={form} setForm={setForm} selected={selected} />
            <section style={{ ...cardStyle, padding: 20, display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
              <p style={{ margin: 0, color: "#675b50" }}>
                {selected.type === "retrograde_survival" && form.retrograde_mode === "general"
                  ? "General mode uses current-date retrograde logic only."
                  : "Birth details stay local to this request and are sent only for report generation."}
              </p>
              <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
                <button type="button" onClick={() => setActiveTab("history")} style={ghostLinkStyle}>
                  Open history
                </button>
                <button type="button" onClick={handleGenerate} disabled={!canSubmit || submitting} style={{ ...primaryButtonStyle, opacity: !canSubmit || submitting ? 0.6 : 1 }}>
                  {submitting ? "Generating..." : "Generate Report"}
                </button>
              </div>
            </section>
            {error ? (
              <section style={{ ...cardStyle, padding: 18, color: "#8a3929" }}>
                {error}
              </section>
            ) : null}
          </>
        ) : null}
        {activeTab === "report" ? <ReportRenderer report={currentReport} onReset={resetForNew} /> : null}
        {activeTab === "history" ? <HistoryPanel historyMap={historyMap} loadingHistory={loadingHistory} historyError={historyError} onOpen={openHistoryItem} selectedType={selected.type} /> : null}
      </div>
    </div>
  );
}

export default IndividualReportsPage;
