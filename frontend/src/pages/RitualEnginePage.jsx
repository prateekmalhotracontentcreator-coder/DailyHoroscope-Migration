import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CITY_OPTIONS = [
  { label: "New Delhi", city_name: "New Delhi", latitude: 28.6139, longitude: 77.209, timezone: "Asia/Kolkata" },
  { label: "Mumbai", city_name: "Mumbai", latitude: 19.076, longitude: 72.8777, timezone: "Asia/Kolkata" },
  { label: "Bengaluru", city_name: "Bengaluru", latitude: 12.9716, longitude: 77.5946, timezone: "Asia/Kolkata" },
  { label: "Kolkata", city_name: "Kolkata", latitude: 22.5726, longitude: 88.3639, timezone: "Asia/Kolkata" },
  { label: "Chennai", city_name: "Chennai", latitude: 13.0827, longitude: 80.2707, timezone: "Asia/Kolkata" },
  { label: "Hyderabad", city_name: "Hyderabad", latitude: 17.385, longitude: 78.4867, timezone: "Asia/Kolkata" },
  { label: "New York", city_name: "New York", latitude: 40.7128, longitude: -74.006, timezone: "America/New_York" },
  { label: "London", city_name: "London", latitude: 51.5072, longitude: -0.1276, timezone: "Europe/London" },
];

const TRIGGER_OPTIONS = [
  { key: "first_date_magnet", label: "First Date Magnet" },
  { key: "steamy_encounter", label: "Steamy Encounter" },
  { key: "ex_recovery", label: "Ex-Recovery Window" },
  { key: "long_term_love", label: "Long-Term Love Portal" },
  { key: "lunar_daily_score", label: "Love Battery Score" },
];

const TRIGGER_STYLES = {
  first_date_magnet: { background: "rgba(183, 60, 100, 0.12)", color: "#8c3051" },
  steamy_encounter: { background: "rgba(139, 30, 60, 0.12)", color: "#7d1d3c" },
  ex_recovery: { background: "rgba(100, 60, 160, 0.12)", color: "#644399" },
  long_term_love: { background: "rgba(120, 145, 78, 0.14)", color: "#587142" },
  lunar_daily_score: { background: "rgba(215, 175, 106, 0.16)", color: "#8a6a39" },
};

const pageStyle = {
  minHeight: "100vh",
  background:
    "radial-gradient(circle at top left, rgba(215,175,106,0.16), transparent 24%), radial-gradient(circle at 85% 8%, rgba(183,60,100,0.14), transparent 20%), linear-gradient(180deg, #faf6ef 0%, #f4ede2 100%)",
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
    document.title = "Ritual Engine Dashboard | Everyday Horoscope";
    ensureMeta('meta[name="robots"]', { name: "robots" }).setAttribute("content", "noindex, nofollow");
  }, []);
}

function defaultForm() {
  return {
    city_mode: "preset",
    city_code: CITY_OPTIONS[0].label,
    date: "",
    time: "",
    city_name: CITY_OPTIONS[0].city_name,
    latitude: CITY_OPTIONS[0].latitude,
    longitude: CITY_OPTIONS[0].longitude,
    timezone: CITY_OPTIONS[0].timezone,
    triggers_opted_in: TRIGGER_OPTIONS.map((item) => item.key),
  };
}

function applyPreset(current, code) {
  const preset = CITY_OPTIONS.find((item) => item.label === code) || CITY_OPTIONS[0];
  return {
    ...current,
    city_code: preset.label,
    city_name: preset.city_name,
    latitude: preset.latitude,
    longitude: preset.longitude,
    timezone: preset.timezone,
  };
}

function prettyTriggerName(key) {
  return TRIGGER_OPTIONS.find((item) => item.key === key)?.label || key.replaceAll("_", " ");
}

function scoreBadge(score) {
  if (score >= 85) return "Magnetic";
  if (score >= 70) return "Building";
  if (score >= 50) return "Quiet";
  return "Reflective";
}

function progressColor(score) {
  if (score >= 85) return "#b73c64";
  if (score >= 70) return "#b78646";
  if (score >= 50) return "#7a8f4d";
  return "#7a5b9a";
}

function RitualEnginePage() {
  const [dashboard, setDashboard] = useState(null);
  const [historyItems, setHistoryItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [subscriptionMissing, setSubscriptionMissing] = useState(false);
  const [enrolling, setEnrolling] = useState(false);
  const [unenrolling, setUnenrolling] = useState(false);
  const [form, setForm] = useState(defaultForm);
  const [historyOpen, setHistoryOpen] = useState(false);

  useProtectedSeo();

  async function loadDashboard() {
    setLoading(true);
    setError("");
    try {
      const [dashboardResponse, historyResponse] = await Promise.all([
        axios.get(`${API}/ritual-engine/dashboard`, { withCredentials: true }),
        axios.get(`${API}/ritual-engine/history`, { withCredentials: true }).catch(() => ({ data: { items: [] } })),
      ]);
      setDashboard(dashboardResponse.data);
      setHistoryItems(dashboardResponse.data?.recent_history || historyResponse.data?.items || []);
      setSubscriptionMissing(false);
    } catch (requestError) {
      if (requestError?.response?.status === 404) {
        setSubscriptionMissing(true);
        setDashboard(null);
      } else {
        setError(requestError?.response?.data?.detail || "Unable to open the Ritual Engine right now.");
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  const loveBattery = dashboard?.love_battery;
  const gaugeStyle = useMemo(() => {
    const score = loveBattery?.love_battery_percent || 0;
    const color = progressColor(score);
    return {
      width: 220,
      height: 220,
      borderRadius: "50%",
      display: "grid",
      placeItems: "center",
      background: `conic-gradient(${color} 0 ${score}%, rgba(120,90,55,0.12) ${score}% 100%)`,
      padding: 18,
      margin: "0 auto",
    };
  }, [loveBattery]);

  async function handleEnroll() {
    setEnrolling(true);
    setError("");
    try {
      await axios.post(
        `${API}/ritual-engine/enroll`,
        {
          natal_data: {
            date: form.date,
            time: form.time,
            latitude: Number(form.latitude),
            longitude: Number(form.longitude),
            timezone: form.timezone,
            city_name: form.city_name || undefined,
          },
          triggers_opted_in: form.triggers_opted_in,
        },
        { withCredentials: true }
      );
      await loadDashboard();
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Unable to activate your Ritual Engine right now.");
    } finally {
      setEnrolling(false);
    }
  }

  async function handleUnenroll() {
    const confirmed = window.confirm("Are you sure you want to unenroll from the Ritual Engine?");
    if (!confirmed) return;
    setUnenrolling(true);
    setError("");
    try {
      await axios.delete(`${API}/ritual-engine/unenroll`, { withCredentials: true });
      setDashboard(null);
      setSubscriptionMissing(true);
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Unable to unenroll right now.");
    } finally {
      setUnenrolling(false);
    }
  }

  return (
    <div style={pageStyle}>
      <div style={{ maxWidth: 1180, margin: "0 auto", display: "grid", gap: 18 }}>
        <section style={{ ...cardStyle, padding: 24 }}>
          <p style={{ margin: "0 0 10px", fontSize: 12, letterSpacing: "0.18em", textTransform: "uppercase", color: "#8c6a39" }}>Ritual Engine</p>
          <h1 style={{ margin: "0 0 12px", fontSize: "clamp(2.2rem, 5vw, 3.8rem)", lineHeight: 0.95, fontFamily: "Georgia, Times New Roman, serif" }}>
            Your daily love intelligence feed.
          </h1>
          <p style={{ margin: 0, color: "#64584c", lineHeight: 1.7 }}>
            The Ritual Engine evaluates your active love triggers once per day and turns the result into one dashboard snapshot: battery, triggers, next timing, and recent history.
          </p>
        </section>

        {loading ? <section style={{ ...cardStyle, padding: 24 }}>Loading your Ritual Engine snapshot...</section> : null}
        {error ? <section style={{ ...cardStyle, padding: 20, color: "#8a3929" }}>{error}</section> : null}

        {!loading && subscriptionMissing ? (
          <section style={{ ...cardStyle, padding: 24 }}>
            <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: "#8c6a39" }}>Activate</p>
            <h2 style={{ margin: "0 0 12px", fontSize: 32, fontFamily: "Georgia, Times New Roman, serif" }}>Activate Your Ritual Engine</h2>
            <div style={{ display: "grid", gap: 14 }}>
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
                  <select value={form.city_code} onChange={(event) => setForm((current) => applyPreset(current, event.target.value))} style={inputStyle}>
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
                  <span style={{ fontWeight: 700 }}>City Name</span>
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

              <div style={{ display: "grid", gap: 10 }}>
                <strong>Trigger selector</strong>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 10 }}>
                  {TRIGGER_OPTIONS.map((item) => {
                    const checked = form.triggers_opted_in.includes(item.key);
                    return (
                      <label key={item.key} style={{ padding: 12, borderRadius: 16, background: checked ? "rgba(215,175,106,0.16)" : "rgba(255,255,255,0.76)", display: "flex", gap: 10, alignItems: "center" }}>
                        <input
                          type="checkbox"
                          checked={checked}
                          onChange={() =>
                            setForm((current) => ({
                              ...current,
                              triggers_opted_in: checked
                                ? current.triggers_opted_in.filter((value) => value !== item.key)
                                : [...current.triggers_opted_in, item.key],
                            }))
                          }
                        />
                        <span>{item.label}</span>
                      </label>
                    );
                  })}
                </div>
              </div>

              <button type="button" onClick={handleEnroll} disabled={enrolling} style={{ ...primaryButtonStyle, justifySelf: "start", opacity: enrolling ? 0.65 : 1 }}>
                {enrolling ? "Activating..." : "Activate"}
              </button>
            </div>
          </section>
        ) : null}

        {!loading && dashboard ? (
          <>
            <section style={{ ...cardStyle, padding: 24 }}>
              <div style={{ display: "grid", gridTemplateColumns: "minmax(260px, 320px) minmax(0, 1fr)", gap: 24, alignItems: "center" }}>
                <div style={gaugeStyle}>
                  <div style={{ width: "100%", height: "100%", borderRadius: "50%", background: "rgba(255,251,245,0.95)", display: "grid", placeItems: "center", textAlign: "center", padding: 18 }}>
                    <div>
                      <div style={{ fontSize: 44, fontWeight: 700 }}>{loveBattery?.love_battery_percent || 0}%</div>
                      <div style={{ marginTop: 8, padding: "6px 10px", borderRadius: 999, background: "rgba(215,175,106,0.16)", display: "inline-flex", fontWeight: 700 }}>
                        {scoreBadge(loveBattery?.love_battery_percent || 0)}
                      </div>
                    </div>
                  </div>
                </div>
                <div style={{ display: "grid", gap: 12 }}>
                  <div>
                    <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.18em", textTransform: "uppercase", color: "#8c6a39" }}>Love Battery</p>
                    <h2 style={{ margin: 0, fontSize: 34, fontFamily: "Georgia, Times New Roman, serif" }}>Today’s battery snapshot</h2>
                  </div>
                  <p style={{ margin: 0, color: "#62574a", lineHeight: 1.7 }}>{loveBattery?.alignment_description}</p>
                  <div style={{ display: "grid", gap: 8 }}>
                    <div>Moon-Venus angle: <strong>{loveBattery?.moon_natal_venus_angle ?? "—"}°</strong></div>
                    <div>Action note: <strong>{loveBattery?.action_note || "—"}</strong></div>
                    <div>Updated daily: <strong>{loveBattery?.check_date || "Today"}</strong></div>
                  </div>
                </div>
              </div>
            </section>

            <section style={{ ...cardStyle, padding: 24 }}>
              <div style={{ marginBottom: 14 }}>
                <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: "#8c6a39" }}>Active Triggers</p>
                <h2 style={{ margin: 0, fontSize: 30, fontFamily: "Georgia, Times New Roman, serif" }}>What is astrologically active for you today.</h2>
              </div>
              {!dashboard.active_triggers?.length ? (
                <div style={{ padding: 16, borderRadius: 18, background: "rgba(255,255,255,0.76)", color: "#62574a" }}>
                  No planetary triggers active today - your Love Battery is running on baseline lunar current.
                </div>
              ) : (
                <div style={{ display: "grid", gap: 12 }}>
                  {dashboard.active_triggers.map((trigger) => {
                    const tint = TRIGGER_STYLES[trigger.trigger_type] || TRIGGER_STYLES.lunar_daily_score;
                    return (
                      <article key={`${trigger.trigger_type}-${trigger.check_date}`} style={{ padding: 18, borderRadius: 18, background: tint.background }}>
                        <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center", marginBottom: 10 }}>
                          <span style={{ padding: "6px 10px", borderRadius: 999, background: "rgba(255,255,255,0.76)", color: tint.color, fontWeight: 700 }}>
                            {prettyTriggerName(trigger.trigger_type)}
                          </span>
                          {trigger.intensity ? (
                            <span style={{ padding: "6px 10px", borderRadius: 999, background: "rgba(255,255,255,0.76)", fontWeight: 700, textTransform: "capitalize" }}>
                              {trigger.intensity}
                            </span>
                          ) : null}
                          {trigger.orb_degrees !== null && trigger.orb_degrees !== undefined ? <span>{trigger.orb_degrees}° orb</span> : null}
                        </div>
                        <p style={{ margin: "0 0 8px", color: "#62574a", lineHeight: 1.7 }}>{trigger.alignment_description}</p>
                        {trigger.ritual_suggestion ? <p style={{ margin: "0 0 8px", color: "#62574a", lineHeight: 1.7 }}>{trigger.ritual_suggestion}</p> : null}
                        <p style={{ margin: 0, color: "#7a6d60" }}>
                          Active from {trigger.active_from || trigger.check_date} until {trigger.active_until || trigger.check_date}
                        </p>
                      </article>
                    );
                  })}
                </div>
              )}
            </section>

            {dashboard.next_upcoming_trigger ? (
              <section style={{ ...cardStyle, padding: 24 }}>
                <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: "#8c6a39" }}>Coming next</p>
                <h2 style={{ margin: "0 0 10px", fontSize: 28, fontFamily: "Georgia, Times New Roman, serif" }}>{prettyTriggerName(dashboard.next_upcoming_trigger.trigger_type)}</h2>
                <p style={{ margin: "0 0 8px", color: "#62574a", lineHeight: 1.7 }}>{dashboard.next_upcoming_trigger.preview}</p>
                <p style={{ margin: 0, color: "#7a6d60" }}>Starts in approximately {dashboard.next_upcoming_trigger.starts_in_days} days.</p>
              </section>
            ) : null}

            <section style={{ ...cardStyle, padding: 24 }}>
              <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
                <div>
                  <p style={{ margin: "0 0 8px", fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: "#8c6a39" }}>Recent History</p>
                  <h2 style={{ margin: 0, fontSize: 28, fontFamily: "Georgia, Times New Roman, serif" }}>Last 7 ritual log entries</h2>
                </div>
                <button type="button" onClick={() => setHistoryOpen((current) => !current)} style={secondaryButtonStyle}>
                  {historyOpen ? "Hide History" : "Show History"}
                </button>
              </div>
              {historyOpen ? (
                <div style={{ marginTop: 16, display: "grid", gap: 12 }}>
                  {historyItems.slice(0, 7).map((item, index) => (
                    <div key={`${item.id || item.trigger_type}-${index}`} style={{ padding: 14, borderRadius: 18, background: "rgba(255,255,255,0.76)" }}>
                      <strong>{item.check_date || item.fired_at?.slice?.(0, 10) || "Recent"}</strong>
                      <p style={{ margin: "6px 0", color: "#62574a" }}>
                        {prettyTriggerName(item.trigger_type)} {item.love_battery_percent ? `· ${item.love_battery_percent}%` : ""}
                      </p>
                      <p style={{ margin: 0, color: "#62574a", lineHeight: 1.62 }}>{item.alignment_description}</p>
                    </div>
                  ))}
                </div>
              ) : null}
            </section>

            <section style={{ ...cardStyle, padding: 24, display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
              <div>
                <p style={{ margin: "0 0 6px", fontSize: 12, letterSpacing: "0.16em", textTransform: "uppercase", color: "#8c6a39" }}>Manage subscription</p>
                <h2 style={{ margin: 0, fontSize: 28, fontFamily: "Georgia, Times New Roman, serif" }}>Need to pause the engine?</h2>
              </div>
              <button type="button" onClick={handleUnenroll} disabled={unenrolling} style={{ ...secondaryButtonStyle, opacity: unenrolling ? 0.65 : 1 }}>
                {unenrolling ? "Unenrolling..." : "Unenroll"}
              </button>
            </section>
          </>
        ) : null}
      </div>
    </div>
  );
}

export default RitualEnginePage;
