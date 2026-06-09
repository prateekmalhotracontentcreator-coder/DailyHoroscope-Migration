import React, { useEffect, useMemo, useState } from "react";

const PLANET_ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"];

const THEMES = {
  longevity: {
    wrapper: "border-[#d5a14a]/20 bg-[#101423]/88 shadow-[0_30px_80px_rgba(2,6,23,0.24)]",
    eyebrow: "text-[#d5a14a]",
    title: "text-[#fbf6ef]",
    copy: "text-white/66",
    toggle: "border-[#d5a14a]/25 bg-[#d5a14a]/10 text-[#f6d79e] hover:bg-[#d5a14a]/18",
    card: "border-white/8 bg-white/[0.03]",
    tableHead: "text-white/42",
    tableRow: "border-white/6 text-white/78",
    value: "text-[#fbf6ef]",
    body: "text-white/72",
    pill: "border-white/15 bg-white/5 text-white/70",
  },
  oracle: {
    wrapper: "border-amber-200/20 bg-amber-500/[0.04] shadow-[0_18px_50px_rgba(0,0,0,0.18)]",
    eyebrow: "text-[#d9a84a]/80",
    title: "text-white",
    copy: "text-white/68",
    toggle: "border-[#d9a84a]/25 bg-[#d9a84a]/10 text-[#f5d189] hover:bg-[#d9a84a]/18",
    card: "border-white/10 bg-black/18",
    tableHead: "text-white/46",
    tableRow: "border-white/8 text-white/80",
    value: "text-[#fbf6ef]",
    body: "text-white/78",
    pill: "border-[#d9a84a]/20 bg-[#d9a84a]/10 text-[#f5d189]",
  },
};

function DataPill({ children, theme }) {
  return (
    <span className={`inline-flex items-center rounded-full border px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.22em] ${theme.pill}`}>
      {children}
    </span>
  );
}

function SummaryValue({ label, value, theme }) {
  return (
    <div className={`rounded-2xl border px-4 py-3 ${theme.card}`}>
      <p className={`mb-1 text-[11px] uppercase tracking-[0.24em] ${theme.tableHead}`}>{label}</p>
      <p className={`text-sm leading-6 ${theme.value}`}>{value}</p>
    </div>
  );
}

export default function KPChartPanel({
  kpChart,
  defaultOpen = false,
  title = "Your KP Chart",
  eyebrow = "Foundation Layer",
  theme = "longevity",
  description = "This panel shows the reusable KP foundation layer: Placidus cusps, Krishnamurti ayanamsha, sub-lords, and raw significator links.",
  className = "",
}) {
  const palette = THEMES[theme] || THEMES.longevity;
  const [open, setOpen] = useState(defaultOpen);

  useEffect(() => {
    setOpen(defaultOpen);
  }, [defaultOpen, kpChart]);

  const kpPlanets = useMemo(
    () => PLANET_ORDER.map((name) => [name, kpChart?.planets?.[name]]).filter(([, details]) => details),
    [kpChart],
  );
  const kpCusps = Array.isArray(kpChart?.cusps) ? kpChart.cusps : [];
  const kpSignificators = useMemo(
    () => PLANET_ORDER.map((name) => [name, kpChart?.significators?.[name] || []]).filter(([, houses]) => houses.length),
    [kpChart],
  );

  if (!kpChart) return null;

  return (
    <section className={`rounded-[28px] border p-5 backdrop-blur-xl sm:p-7 ${palette.wrapper} ${className}`}>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="max-w-3xl space-y-2">
          {eyebrow ? <p className={`m-0 text-[11px] uppercase tracking-[0.3em] ${palette.eyebrow}`}>{eyebrow}</p> : null}
          {title ? <h2 className={`m-0 font-serif text-2xl sm:text-[2rem] ${palette.title}`}>{title}</h2> : null}
          {description ? <p className={`m-0 text-sm leading-7 ${palette.copy}`}>{description}</p> : null}
        </div>
        <button
          type="button"
          onClick={() => setOpen((current) => !current)}
          className={`rounded-full border px-4 py-2 text-sm font-semibold transition ${palette.toggle}`}
        >
          {open ? "Hide KP Chart" : "Show KP Chart"}
        </button>
      </div>

      {open ? (
        <div className="mt-6 space-y-6">
          <div className="grid gap-3 md:grid-cols-3">
            <SummaryValue
              label="Ascendant"
              value={kpChart?.ascendant ? `${kpChart.ascendant.sign} ${kpChart.ascendant.degree_label}` : "Unavailable"}
              theme={palette}
            />
            <SummaryValue label="Ayanamsha" value={kpChart?.ayanamsha || "Krishnamurti"} theme={palette} />
            <SummaryValue label="Ascendant Sub-Lord" value={kpChart?.ascendant?.sub_lord || "Unavailable"} theme={palette} />
          </div>

          <div className={`rounded-[24px] border p-4 ${palette.card}`}>
            <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
              <h3 className={`m-0 text-lg font-semibold ${palette.value}`}>Planet Placements</h3>
              <DataPill theme={palette}>{`${kpPlanets.length} planets`}</DataPill>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full text-left text-sm">
                <thead className={`text-[11px] uppercase tracking-[0.24em] ${palette.tableHead}`}>
                  <tr className="border-b border-white/10">
                    <th className="px-3 py-3 font-medium">Planet</th>
                    <th className="px-3 py-3 font-medium">Sign</th>
                    <th className="px-3 py-3 font-medium">House</th>
                    <th className="px-3 py-3 font-medium">Nakshatra</th>
                    <th className="px-3 py-3 font-medium">Star Lord</th>
                    <th className="px-3 py-3 font-medium">Sub-Lord</th>
                  </tr>
                </thead>
                <tbody>
                  {kpPlanets.map(([planet, details]) => (
                    <tr key={planet} className={`border-b last:border-b-0 ${palette.tableRow}`}>
                      <td className={`px-3 py-3 font-semibold ${palette.value}`}>{planet}</td>
                      <td className="px-3 py-3">{details.sign}</td>
                      <td className="px-3 py-3">{details.house}</td>
                      <td className="px-3 py-3">{details.nakshatra}</td>
                      <td className="px-3 py-3">{details.star_lord}</td>
                      <td className="px-3 py-3">{details.sub_lord}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className={`rounded-[24px] border p-4 ${palette.card}`}>
            <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
              <h3 className={`m-0 text-lg font-semibold ${palette.value}`}>Placidus Cusp Table</h3>
              <DataPill theme={palette}>12 cusps</DataPill>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full text-left text-sm">
                <thead className={`text-[11px] uppercase tracking-[0.24em] ${palette.tableHead}`}>
                  <tr className="border-b border-white/10">
                    <th className="px-3 py-3 font-medium">House</th>
                    <th className="px-3 py-3 font-medium">Cusp Sign</th>
                    <th className="px-3 py-3 font-medium">Degree</th>
                    <th className="px-3 py-3 font-medium">Sub-Lord</th>
                  </tr>
                </thead>
                <tbody>
                  {kpCusps.map((cusp) => (
                    <tr key={cusp.house} className={`border-b last:border-b-0 ${palette.tableRow}`}>
                      <td className={`px-3 py-3 font-semibold ${palette.value}`}>{cusp.house}</td>
                      <td className="px-3 py-3">{cusp.sign}</td>
                      <td className="px-3 py-3">{cusp.degree_label}</td>
                      <td className="px-3 py-3">{cusp.sub_lord}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className={`rounded-[24px] border p-4 ${palette.card}`}>
            <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
              <h3 className={`m-0 text-lg font-semibold ${palette.value}`}>Ascendant Summary</h3>
              <DataPill theme={palette}>{kpChart?.ascendant?.nakshatra || "KP"}</DataPill>
            </div>
            <p className={`m-0 text-sm leading-7 ${palette.body}`}>
              {kpChart?.ascendant
                ? `${kpChart.ascendant.sign} ascendant at ${kpChart.ascendant.degree_label}, using ${kpChart.ayanamsha} ayanamsha, with ${kpChart.ascendant.sub_lord} as the ascendant cusp sub-lord.`
                : "Ascendant data is unavailable for this report."}
            </p>
          </div>

          {kpSignificators.length ? (
            <div className={`rounded-[24px] border p-4 ${palette.card}`}>
              <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
                <h3 className={`m-0 text-lg font-semibold ${palette.value}`}>House Significators</h3>
                <DataPill theme={palette}>Raw KP mapping</DataPill>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full text-left text-sm">
                  <thead className={`text-[11px] uppercase tracking-[0.24em] ${palette.tableHead}`}>
                    <tr className="border-b border-white/10">
                      <th className="px-3 py-3 font-medium">Planet</th>
                      <th className="px-3 py-3 font-medium">Houses Signified</th>
                    </tr>
                  </thead>
                  <tbody>
                    {kpSignificators.map(([planet, houses]) => (
                      <tr key={planet} className={`border-b last:border-b-0 ${palette.tableRow}`}>
                        <td className={`px-3 py-3 font-semibold ${palette.value}`}>{planet}</td>
                        <td className="px-3 py-3">{houses.join(", ")}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ) : null}
        </div>
      ) : null}
    </section>
  );
}
