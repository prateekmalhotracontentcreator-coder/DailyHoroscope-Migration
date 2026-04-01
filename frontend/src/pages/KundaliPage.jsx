import React, { startTransition, useDeferredValue, useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const TAB_LABELS = [
  ["kundali", "Kundali"],
  ["graha", "Graha"],
  ["upagraha", "Upagraha"],
  ["yoga", "Yoga"],
  ["vimshottari_dasha", "Dasha"],
  ["ashtaka_varga", "Ashtaka Varga"],
  ["shadbala", "Shadbala"],
  ["bhavabala", "Bhavabala"],
];

const chartPanelStyle = {
  background:
    "linear-gradient(180deg, rgba(254,252,247,0.98) 0%, rgba(247,239,221,0.98) 100%)",
  border: "1px solid rgba(197,160,89,0.5)",
  borderRadius: "20px",
  boxShadow: "0 18px 45px rgba(91,66,20,0.1)",
};

const chartLayout = {
  12: { x: 70, y: 30 },
  1: { x: 200, y: 30 },
  2: { x: 330, y: 30 },
  11: { x: 30, y: 120 },
  5: { x: 120, y: 120 },
  6: { x: 280, y: 120 },
  3: { x: 370, y: 120 },
  10: { x: 30, y: 280 },
  8: { x: 120, y: 280 },
  7: { x: 280, y: 280 },
  4: { x: 370, y: 280 },
  9: { x: 200, y: 370 },
};

function NorthIndianChart({ chart, title }) {
  const houseMap = {};
  const planetsByHouse = {};
  (chart?.houses || []).forEach((house) => {
    houseMap[house.house_num] = house;
  });
  (chart?.grahas || []).forEach((graha) => {
    const house = graha.house_whole_sign || 1;
    planetsByHouse[house] = planetsByHouse[house] || [];
    planetsByHouse[house].push(graha);
  });

  return (
    <div style={{ ...chartPanelStyle, padding: 18 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 12 }}>
        <div>
          <div style={{ fontSize: 12, letterSpacing: "0.18em", textTransform: "uppercase", color: "#8B6A30" }}>{title}</div>
          <h3 style={{ margin: "4px 0 0", fontSize: 22, color: "#3E2C14" }}>{chart?.name || "Chart"}</h3>
        </div>
        <div style={{ color: "#8B6A30", fontSize: 13 }}>
          Lagna: <strong>{chart?.lagna?.sign || "--"}</strong>
        </div>
      </div>

      <svg viewBox="0 0 400 400" width="100%" role="img" aria-label={title}>
        <rect x="4" y="4" width="392" height="392" rx="18" fill="#FEFCF7" stroke="#C5A059" strokeWidth="2" />
        <line x1="200" y1="16" x2="16" y2="200" stroke="#C5A059" strokeWidth="1.5" />
        <line x1="200" y1="16" x2="384" y2="200" stroke="#C5A059" strokeWidth="1.5" />
        <line x1="16" y1="200" x2="200" y2="384" stroke="#C5A059" strokeWidth="1.5" />
        <line x1="384" y1="200" x2="200" y2="384" stroke="#C5A059" strokeWidth="1.5" />
        <line x1="16" y1="16" x2="200" y2="200" stroke="#C5A059" strokeWidth="1" />
        <line x1="384" y1="16" x2="200" y2="200" stroke="#C5A059" strokeWidth="1" />
        <line x1="16" y1="384" x2="200" y2="200" stroke="#C5A059" strokeWidth="1" />
        <line x1="384" y1="384" x2="200" y2="200" stroke="#C5A059" strokeWidth="1" />

        {Object.entries(chartLayout).map(([houseNumber, coords]) => {
          const house = houseMap[Number(houseNumber)];
          const grahas = planetsByHouse[Number(houseNumber)] || [];
          return (
            <g key={houseNumber}>
              <text x={coords.x} y={coords.y} textAnchor="middle" fontSize="12" fill="#A98445" fontWeight="700">
                {houseNumber}
              </text>
              <text x={coords.x} y={coords.y + 18} textAnchor="middle" fontSize="15" fill="#2B2111" fontWeight="700">
                {house?.sign_num || ""}
              </text>
              <text x={coords.x} y={coords.y + 34} textAnchor="middle" fontSize="10" fill="#6F5730">
                {house?.sign || ""}
              </text>
              {grahas.slice(0, 4).map((graha, index) => (
                <text key={`${houseNumber}-${graha.code}`} x={coords.x} y={coords.y + 52 + index * 13} textAnchor="middle" fontSize="10" fill="#864E1B">
                  {graha.abbr}
                </text>
              ))}
            </g>
          );
        })}
      </svg>
      <div style={{ marginTop: 12, fontSize: 13, color: "#5E4724" }}>{chart?.focus_area}</div>
    </div>
  );
}

function DataTable({ title, rows, columns }) {
  return (
    <section style={{ ...chartPanelStyle, padding: 18 }}>
      <h3 style={{ marginTop: 0, color: "#3E2C14" }}>{title}</h3>
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  style={{
                    textAlign: "left",
                    padding: "10px 8px",
                    fontSize: 12,
                    letterSpacing: "0.08em",
                    textTransform: "uppercase",
                    color: "#8B6A30",
                    borderBottom: "1px solid rgba(197,160,89,0.35)",
                  }}
                >
                  {column.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, rowIndex) => (
              <tr key={row.id || row.code || row.house_num || rowIndex}>
                {columns.map((column) => (
                  <td key={column.key} style={{ padding: "11px 8px", borderBottom: "1px solid rgba(197,160,89,0.18)", color: "#402F18" }}>
                    {column.render ? column.render(row) : row[column.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function PendingLayer({ title, message }) {
  return (
    <section style={{ ...chartPanelStyle, padding: 18 }}>
      <h3 style={{ marginTop: 0, color: "#3E2C14" }}>{title}</h3>
      <p style={{ marginBottom: 0, color: "#5A4321" }}>{message}</p>
    </section>
  );
}

function KundaliPage() {
  const params = useParams();
  const routeChartId = params.chartId || params.id || "";
  const [form, setForm] = useState({
    date: "",
    time: "14:30",
    time_precision: "exact",
    place_label: "Mumbai, Maharashtra, India",
    latitude: "",
    longitude: "",
    timezone: "Asia/Kolkata",
  });
  const [chart, setChart] = useState(null);
  const [definitions, setDefinitions] = useState([]);
  const [rightChartData, setRightChartData] = useState(null);
  const [leftChart, setLeftChart] = useState("D1");
  const [rightChart, setRightChart] = useState("D9");
  const [activeTab, setActiveTab] = useState("kundali");
  const [loading, setLoading] = useState(false);
  const [loadingVariant, setLoadingVariant] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const deferredRightChart = useDeferredValue(rightChart);

  useEffect(() => {
    let active = true;
    async function loadDefinitions() {
      try {
        const response = await axios.get(`${API}/lagna-kundali/chart-definitions`);
        if (!active) return;
        setDefinitions(response.data?.charts || []);
      } catch (_err) {
        if (!active) return;
        setDefinitions([]);
      }
    }
    loadDefinitions();
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!routeChartId) return;
    let active = true;
    async function loadChart() {
      setLoading(true);
      try {
        const response = await axios.get(`${API}/lagna-kundali/chart/${routeChartId}`, { withCredentials: true });
        if (!active) return;
        startTransition(() => {
          setChart(response.data || null);
        });
      } catch (err) {
        if (!active) return;
        setError(err?.response?.data?.detail || "Unable to open this chart.");
      } finally {
        if (active) setLoading(false);
      }
    }
    loadChart();
    return () => {
      active = false;
    };
  }, [routeChartId]);

  useEffect(() => {
    if (!chart?.chart_id) return;
    if (!deferredRightChart || deferredRightChart === "D1") {
      setRightChartData(chart?.charts?.D1 || null);
      return;
    }
    if (chart?.charts?.[deferredRightChart]) {
      setRightChartData(chart.charts[deferredRightChart]);
      return;
    }
    const definition = definitions.find((item) => item.code === deferredRightChart);
    if (definition && !definition.enabled) {
      setRightChartData({
        name: deferredRightChart,
        focus_area: definition.short_meaning,
        pending_verification: "Registered in the selector. Computational enablement is pending a later tier.",
      });
      return;
    }

    let active = true;
    async function loadVariant() {
      setLoadingVariant(true);
      try {
        const response = await axios.get(`${API}/lagna-kundali/chart/${chart.chart_id}/charts/${deferredRightChart}`, {
          withCredentials: true,
        });
        if (!active) return;
        startTransition(() => {
          setRightChartData(response.data || null);
          setChart((current) => {
            if (!current) return current;
            return {
              ...current,
              charts: {
                ...(current.charts || {}),
                [deferredRightChart]: response.data,
              },
            };
          });
        });
      } catch (err) {
        if (!active) return;
        setError(err?.response?.data?.detail || `Unable to load ${deferredRightChart}.`);
      } finally {
        if (active) setLoadingVariant(false);
      }
    }
    loadVariant();
    return () => {
      active = false;
    };
  }, [chart, deferredRightChart, definitions]);

  async function handleCompute() {
    setLoading(true);
    setError("");
    try {
      const payload = {
        ...form,
        latitude: form.latitude ? Number(form.latitude) : undefined,
        longitude: form.longitude ? Number(form.longitude) : undefined,
        requested_chart_codes: ["D1"],
      };
      const response = await axios.post(`${API}/lagna-kundali/compute`, payload, { withCredentials: true });
      startTransition(() => {
        setChart(response.data || null);
        setLeftChart("D1");
        setRightChart("D9");
        setRightChartData(null);
      });
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to compute the Lagna Kundali right now.");
    } finally {
      setLoading(false);
    }
  }

  async function handleSave() {
    setSaving(true);
    setError("");
    try {
      const payload = {
        ...form,
        latitude: form.latitude ? Number(form.latitude) : undefined,
        longitude: form.longitude ? Number(form.longitude) : undefined,
        requested_chart_codes: ["D1"],
      };
      const response = await axios.post(`${API}/lagna-kundali/save`, payload, { withCredentials: true });
      if (chart) {
        setChart((current) => ({ ...current, chart_id: response.data?.chart_id || current.chart_id }));
      }
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to save this chart.");
    } finally {
      setSaving(false);
    }
  }

  const leftDefinition = definitions.find((item) => item.code === leftChart);
  const leftChartData =
    chart?.charts?.[leftChart] ||
    (leftDefinition && !leftDefinition.enabled
      ? {
          name: leftChart,
          focus_area: leftDefinition.short_meaning,
          pending_verification: "Registered in the selector. Computational enablement is pending a later tier.",
        }
      : chart?.charts?.D1 || null);
  const reliabilityNotes = chart?.meta?.reliability?.notes || [];
  const yogaRows = chart?.layers?.yoga?.items?.slice(0, 18) || [];

  return (
    <div
      style={{
        minHeight: "100vh",
        background:
          "radial-gradient(circle at top left, rgba(241,216,163,0.55), transparent 32%), linear-gradient(180deg, #F5E7C7 0%, #F0D5A3 44%, #E5C081 100%)",
        padding: "28px 18px 56px",
      }}
    >
      <div style={{ maxWidth: 1380, margin: "0 auto" }}>
        <section style={{ marginBottom: 24 }}>
          <div style={{ color: "#8B6A30", letterSpacing: "0.2em", textTransform: "uppercase", fontSize: 12 }}>Lagna Kundali</div>
          <h1 style={{ margin: "8px 0 10px", fontSize: "clamp(2.2rem, 4vw, 4.2rem)", color: "#37240D", lineHeight: 0.95 }}>
            Lagna Kundali Workspace
          </h1>
          <p style={{ maxWidth: 860, fontSize: 17, lineHeight: 1.6, color: "#523B18" }}>
            D1 computes first for a fast and trustworthy entry point. D9, D10, and the rest of the Varga registry stay visible
            from day one and load only when the user asks for them.
          </p>
        </section>

        <section style={{ ...chartPanelStyle, padding: 20, marginBottom: 24 }}>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
              gap: 14,
              alignItems: "end",
            }}
          >
            <label style={{ display: "grid", gap: 6 }}>
              <span style={{ color: "#6D542A", fontSize: 13 }}>Date of birth</span>
              <input type="date" value={form.date} onChange={(event) => setForm((current) => ({ ...current, date: event.target.value }))} />
            </label>
            <label style={{ display: "grid", gap: 6 }}>
              <span style={{ color: "#6D542A", fontSize: 13 }}>Time of birth</span>
              <input type="time" value={form.time} onChange={(event) => setForm((current) => ({ ...current, time: event.target.value }))} />
            </label>
            <label style={{ display: "grid", gap: 6 }}>
              <span style={{ color: "#6D542A", fontSize: 13 }}>Time precision</span>
              <select value={form.time_precision} onChange={(event) => setForm((current) => ({ ...current, time_precision: event.target.value }))}>
                <option value="exact">Exact</option>
                <option value="approximate">Approximate</option>
                <option value="unknown">Unknown</option>
              </select>
            </label>
            <label style={{ display: "grid", gap: 6 }}>
              <span style={{ color: "#6D542A", fontSize: 13 }}>Place</span>
              <input value={form.place_label} onChange={(event) => setForm((current) => ({ ...current, place_label: event.target.value }))} />
            </label>
            <label style={{ display: "grid", gap: 6 }}>
              <span style={{ color: "#6D542A", fontSize: 13 }}>Timezone</span>
              <input value={form.timezone} onChange={(event) => setForm((current) => ({ ...current, timezone: event.target.value }))} />
            </label>
          </div>
          <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginTop: 18 }}>
            <button onClick={handleCompute} disabled={loading} style={{ padding: "12px 18px", borderRadius: 999, border: "none", background: "#6E4C18", color: "#FFF8EA", fontWeight: 700 }}>
              {loading ? "Computing..." : "Generate D1"}
            </button>
            <button onClick={handleSave} disabled={saving || !chart} style={{ padding: "12px 18px", borderRadius: 999, border: "1px solid #8B6A30", background: "transparent", color: "#6E4C18", fontWeight: 700 }}>
              {saving ? "Saving..." : "Save Chart"}
            </button>
          </div>
          {error ? <p style={{ color: "#8D241A", marginTop: 14 }}>{error}</p> : null}
          {reliabilityNotes.length ? (
            <div style={{ marginTop: 16, padding: 14, background: "rgba(115,89,38,0.08)", borderRadius: 14 }}>
              {reliabilityNotes.map((note) => (
                <p key={note} style={{ margin: 0, color: "#5A4321" }}>
                  {note}
                </p>
              ))}
            </div>
          ) : null}
        </section>

        <section style={{ display: "grid", gridTemplateColumns: "240px 1fr", gap: 20, alignItems: "start" }}>
          <aside style={{ ...chartPanelStyle, padding: 14, position: "sticky", top: 18 }}>
            <div style={{ padding: "10px 12px", marginBottom: 8, borderRadius: 14, background: "rgba(110,76,24,0.09)" }}>
              <div style={{ fontSize: 12, color: "#8B6A30", letterSpacing: "0.14em", textTransform: "uppercase" }}>Workspace</div>
              <div style={{ marginTop: 5, fontSize: 18, color: "#3E2C14", fontWeight: 700 }}>Layers</div>
            </div>
            <nav style={{ display: "grid", gap: 6 }}>
              {TAB_LABELS.map(([key, label]) => (
                <button
                  key={key}
                  onClick={() => setActiveTab(key)}
                  style={{
                    textAlign: "left",
                    padding: "12px 14px",
                    borderRadius: 14,
                    border: "none",
                    background: activeTab === key ? "#6E4C18" : "rgba(255,255,255,0.38)",
                    color: activeTab === key ? "#FFF8EA" : "#5A4321",
                    fontWeight: 600,
                  }}
                >
                  {label}
                </button>
              ))}
            </nav>
          </aside>

          <main style={{ display: "grid", gap: 18 }}>
            <section style={{ ...chartPanelStyle, padding: 18 }}>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 12, alignItems: "center", justifyContent: "space-between" }}>
                <div>
                  <div style={{ fontSize: 12, color: "#8B6A30", letterSpacing: "0.18em", textTransform: "uppercase" }}>Comparison</div>
                  <h2 style={{ margin: "4px 0 0", color: "#3E2C14" }}>Chart Workspace</h2>
                </div>
                <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
                  <select value={leftChart} onChange={(event) => setLeftChart(event.target.value)}>
                    {definitions.map((definition) => (
                      <option key={`left-${definition.code}`} value={definition.code}>
                        {definition.code}{definition.enabled ? "" : " (Registered)"}
                      </option>
                    ))}
                  </select>
                  <select value={rightChart} onChange={(event) => setRightChart(event.target.value)}>
                    {definitions.map((definition) => (
                      <option key={definition.code} value={definition.code}>
                        {definition.code}{definition.enabled ? "" : " (Registered)"}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </section>

            {activeTab === "kundali" ? (
              <>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: 18 }}>
                  {leftChartData?.pending_verification ? (
                    <PendingLayer title={leftChart} message={leftChartData.pending_verification} />
                  ) : (
                    <NorthIndianChart chart={leftChartData} title="Left Panel" />
                  )}
                  {loadingVariant ? (
                    <PendingLayer title={`Loading ${rightChart}`} message="Fetching the selected Varga on demand." />
                  ) : rightChartData?.pending_verification ? (
                    <PendingLayer title={rightChart} message={rightChartData.pending_verification} />
                  ) : (
                    <NorthIndianChart chart={rightChartData} title="Right Panel" />
                  )}
                </div>

                <DataTable
                  title="Graha Details"
                  rows={chart?.layers?.graha?.items || []}
                  columns={[
                    { key: "name", label: "Graha" },
                    { key: "sign", label: "Rashi" },
                    { key: "degree_in_sign", label: "Degree" },
                    { key: "nakshatra", label: "Nakshatra" },
                    { key: "house_d1", label: "D1 House" },
                    { key: "house_bhav_chalit", label: "Bhav Chalit" },
                  ]}
                />
              </>
            ) : null}

            {activeTab === "graha" ? (
              <DataTable
                title="Graha Layer"
                rows={chart?.layers?.graha?.items || []}
                columns={[
                  { key: "name", label: "Graha" },
                  { key: "longitude", label: "Longitude" },
                  { key: "sign", label: "Sign" },
                  { key: "retrograde", label: "Retro", render: (row) => (row.retrograde ? "Yes" : "No") },
                  { key: "dignity", label: "Dignity" },
                ]}
              />
            ) : null}

            {activeTab === "upagraha" ? (
              <DataTable
                title="Upagraha Layer"
                rows={chart?.layers?.upagraha?.items || []}
                columns={[
                  { key: "name", label: "Upagraha" },
                  { key: "sign", label: "Sign" },
                  { key: "degree_in_sign", label: "Degree" },
                  { key: "house", label: "House" },
                  { key: "supported", label: "Supported", render: (row) => (row.supported ? "Yes" : "Pending") },
                ]}
              />
            ) : null}

            {activeTab === "yoga" ? (
              <DataTable
                title="Yoga Registry"
                rows={yogaRows}
                columns={[
                  { key: "code", label: "Code" },
                  { key: "name", label: "Yoga" },
                  { key: "category", label: "Category" },
                  { key: "supported", label: "Supported", render: (row) => (row.supported ? "Yes" : "Pending") },
                  { key: "matched", label: "Matched", render: (row) => (row.matched ? "Yes" : "No") },
                ]}
              />
            ) : null}

            {activeTab === "vimshottari_dasha" ? (
              <DataTable
                title="Vimshottari Mahadashas"
                rows={chart?.layers?.vimshottari_dasha?.maha_dashas || []}
                columns={[
                  { key: "planet", label: "Planet" },
                  { key: "start", label: "Start" },
                  { key: "end", label: "End" },
                  { key: "years", label: "Years" },
                ]}
              />
            ) : null}

            {activeTab === "ashtaka_varga" ? (
              <PendingLayer title="Ashtaka Varga" message={chart?.layers?.ashtaka_varga?.pending_verification || "Layer not loaded yet."} />
            ) : null}

            {activeTab === "shadbala" ? (
              <PendingLayer title="Shadbala" message={chart?.layers?.shadbala?.pending_verification || "Layer not loaded yet."} />
            ) : null}

            {activeTab === "bhavabala" ? (
              <PendingLayer title="Bhavabala" message={chart?.layers?.bhavabala?.pending_verification || "Layer not loaded yet."} />
            ) : null}
          </main>
        </section>
      </div>
    </div>
  );
}

export default KundaliPage;
