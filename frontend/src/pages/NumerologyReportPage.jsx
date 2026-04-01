import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

import ContinueJourney from '../components/ContinueJourney';
import LoShuGrid from '../components/LoShuGrid';
import LuckyElementsTable from '../components/LuckyElementsTable';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CTA_MAP = {
  life_path_soul_mission: {
    label: "Open Your Brihat Kundali",
    route: "/brihat-kundli",
    bridge:
      "Your core numbers reveal the pattern. Brihat Kundali shows how that pattern unfolds across life, career, relationships, health, and wealth.",
    precisionNote:
      "For the deepest predictive precision, Birth Chart and Lagna-based analysis are both part of that next layer.",
  },
  name_correction_energy_alignment: {
    label: "Explore Your Remedies",
    route: "/remedies",
    bridge:
      "If your name vibration feels mixed, the next question is how to strengthen alignment in practical life through corrective and supportive remedies.",
  },
  favorable_timing: {
    label: "Open Your Brihat Kundali",
    route: "/brihat-kundli",
    bridge:
      "Numerology timing shows the cycle. Brihat Kundali deepens that with dasha-driven timing and a fuller life-context view of when to act.",
    precisionNote:
      "Precise timing decisions are strongest when both Birth Chart and Lagna-based analysis are considered together.",
  },
  karmic_debt_loshu: {
    label: "Draw A Tarot Clarifier",
    route: "/tarot",
    bridge:
      "When karmic patterns and inner imbalances surface, Tarot helps translate them into an immediate reflective message you can work with emotionally and intuitively.",
  },
  relationship_compatibility: {
    label: "Explore Kundali Milan",
    route: "/kundali-milan",
    bridge:
      "Numerology reveals the emotional and symbolic rhythm between two people. Kundali Milan adds the Vedic compatibility layer for deeper relationship matching.",
    precisionNote:
      "Where users want fuller precision beyond Numerology, chart-based compatibility becomes the next natural lens.",
  },
  career_guidance: {
    label: "Open Your Brihat Kundali",
    route: "/brihat-kundli",
    bridge:
      "Your numbers show work style and direction. Brihat Kundali reveals the fuller career arc through houses, dashas, strengths, pressures, and karmic themes.",
    precisionNote:
      "Career prediction becomes more precise when Birth Chart and Lagna-based analysis are both accounted for.",
  },
  lucky_digital_vibrations: {
    label: "Open Your Birth Chart",
    route: "/birth-chart",
    bridge:
      "A supportive number is only one surface signal. Your Birth Chart shows the deeper natal blueprint behind what truly strengthens or drains you.",
    precisionNote:
      "If the user later wants finer predictive precision, Lagna Kundali becomes the next complementary layer after Birth Chart.",
  },
  residential_compatibility: {
    label: "Explore Vedic Remedies",
    route: "/remedies",
    bridge:
      "If your home vibration feels supportive or mixed, Remedies is the next step to understand how to balance the environment through practical corrective tools.",
  },
  business_brand_optimization: {
    label: "Explore Brihat Kundali",
    route: "/brihat-kundli",
    bridge:
      "Your brand name may align symbolically, but Brihat Kundali shows the deeper career and business promises shaping how success can actually manifest.",
    precisionNote:
      "For serious business timing and direction, Birth Chart and Lagna-based analysis together add the precision Numerology alone cannot provide.",
  },
  baby_name_selection: {
    label: "Explore Your Child's Birth Chart",
    route: "/birth-chart",
    bridge:
      "Once a name feels aligned, the next layer is the child's natal blueprint — the chart that shows the deeper life pattern the name will accompany.",
    precisionNote:
      "If Temple later wants a more advanced child-focused flow, Lagna context can become the follow-on precision layer after Birth Chart.",
  },
  premium_ankjyotish_report: {
    label: "Explore Your Brihat Kundali",
    route: "/brihat-kundli",
    bridge:
      "You have reached the deepest Numerology layer. Brihat Kundali is the natural next step when you want the fullest Vedic synthesis across timing, karma, life direction, and manifestation.",
    precisionNote:
      "This is the clearest place to acknowledge that precise prediction depends on both Birth Chart and Lagna-based analysis working together.",
  },
};

function NumberCards({ computedValues }) {
  const entries = Object.entries(computedValues || {});
  if (!entries.length) return null;

  return (
    <section className="numerology-report-page__numbers">
      {entries.map(([key, value]) => (
        <article key={key} className="numerology-number-card">
          <p>{key.replaceAll("_", " ")}</p>
          <h2>{value?.reduced ?? "-"}</h2>
          <span>Raw {value?.raw ?? "-"}</span>
          {value?.master_number ? <span>Master {value.master_number}</span> : null}
        </article>
      ))}
    </section>
  );
}

function SectionCards({ sections }) {
  return (
    <section className="numerology-report-page__sections">
      {(sections || []).map((section) => (
        <article key={section.section_id} className="numerology-report-section">
          <h2>{section.title}</h2>
          <p className="numerology-report-section__summary">{section.summary}</p>
          <p>{section.body}</p>
        </article>
      ))}
    </section>
  );
}

function RemediationPlan({ items }) {
  if (!Array.isArray(items) || !items.length) return null;

  return (
    <section className="numerology-structured-card numerology-remediation-plan">
      <div className="numerology-structured-card__header">
        <p className="numerology-structured-card__eyebrow">7-Day Remediation</p>
        <h3>Daily Alignment Plan</h3>
      </div>

      <div className="numerology-remediation-plan__grid">
        {items.map((item, index) => (
          <article key={item.day || index} className="numerology-remediation-plan__card">
            <p className="numerology-remediation-plan__day">{item.day || `Day ${index + 1}`}</p>
            <h4>{item.focus || "Alignment Focus"}</h4>
            <p>{item.practice || item.note || "Use this day to reinforce steadier alignment and intention."}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function VedicCrossReference({ payload }) {
  if (!payload) return null;

  const items = [
    { label: "Lagna", value: payload.lagna_sign },
    { label: "Moon Sign", value: payload.moon_sign },
    { label: "Nakshatra", value: payload.nakshatra_name },
  ].filter((item) => item.value);

  if (!items.length) return null;

  return (
    <section className="numerology-structured-card numerology-vedic-crossref">
      <div className="numerology-structured-card__header">
        <p className="numerology-structured-card__eyebrow">Vedic Cross-Reference</p>
        <h3>Temple-Computed Context Layer</h3>
      </div>

      <div className="numerology-chip-group">
        {items.map((item) => (
          <span key={item.label} className="numerology-chip numerology-chip--soft">
            {item.label}: {item.value}
          </span>
        ))}
      </div>

      {payload.cross_reference_note ? <p>{payload.cross_reference_note}</p> : null}
    </section>
  );
}

function PremiumStructuredBlocks({ report }) {
  const trace = report?.calculation_trace || {};
  const showLoShu = Boolean(trace.lo_shu_grid_payload) && (
    report.tile_code === "karmic_debt_loshu" || report.tile_code === "premium_ankjyotish_report"
  );
  const showLuckyElements = Boolean(trace.lucky_elements_table);
  const showPlan = Array.isArray(trace.remediation_plan) && trace.remediation_plan.length > 0;
  const showVedic = Boolean(trace.vedic_cross_reference) && report.tile_code === "premium_ankjyotish_report";

  if (!showLoShu && !showLuckyElements && !showPlan && !showVedic) {
    return null;
  }

  return (
    <section className="numerology-report-page__structured">
      {showLoShu ? <LoShuGrid payload={trace.lo_shu_grid_payload} /> : null}
      {showLuckyElements ? <LuckyElementsTable payload={trace.lucky_elements_table} /> : null}
      {showVedic ? <VedicCrossReference payload={trace.vedic_cross_reference} /> : null}
      {showPlan ? <RemediationPlan items={trace.remediation_plan} /> : null}
    </section>
  );
}

function nextStepForTile(tileCode) {
  return CTA_MAP[tileCode] || {
    label: "Open Your Brihat Kundali",
    route: "/brihat-kundli",
    bridge:
      "This report can be deepened further through a fuller Vedic synthesis layer that connects life themes, timing, and manifestation.",
  };
}

function NumerologyReportPage() {
  const params = useParams();
  const reportId = params.reportId || params.id || "";
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [report, setReport] = useState(null);

  useEffect(() => {
    let active = true;

    async function loadReport() {
      try {
        const res = await axios.get(`${API}/numerology/report/${reportId}`, {
          withCredentials: true,
        });
        if (!active) return;
        setReport(res.data?.report || null);
      } catch (err) {
        if (!active) return;
        setError(err?.response?.data?.detail || "Unable to load this numerology report.");
      } finally {
        if (active) setLoading(false);
      }
    }

    loadReport();
    return () => {
      active = false;
    };
  }, [reportId]);

  const reportTitle = useMemo(() => {
    if (!report?.report_slug) return "Numerology Report";
    return report.report_slug.replaceAll("-", " ");
  }, [report?.report_slug]);

  const nextStep = useMemo(() => nextStepForTile(report?.tile_code), [report?.tile_code]);

  if (loading) {
    return <div className="numerology-report-page numerology-report-page--loading">Opening your report...</div>;
  }

  if (error) {
    return <div className="numerology-report-page__error">{error}</div>;
  }

  if (!report) {
    return <div className="numerology-report-page__empty">No report found.</div>;
  }

  return (
    <div className="numerology-report-page">
      <section className="numerology-report-page__hero">
        <p className="numerology-report-page__eyebrow">Numerology Report</p>
        <h1>{reportTitle}</h1>
        <p>{report.summary}</p>
      </section>

      <NumberCards computedValues={report.computed_values} />
      <SectionCards sections={report.report_sections} />
      <PremiumStructuredBlocks report={report} />

      <section className="numerology-report-page__guidance">
        <h2>Guidance</h2>
        <p>{report.guidance}</p>
        {report.remedy_note ? <p>{report.remedy_note}</p> : null}
      </section>

      <ContinueJourney bridge={nextStep.bridge} cta={nextStep} precisionNote={nextStep.precisionNote} />
    </div>
  );
}

export default NumerologyReportPage;
