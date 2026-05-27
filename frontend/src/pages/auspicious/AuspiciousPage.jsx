import React, { useEffect, useMemo, useState } from "react";
import { AlertCircle } from "lucide-react";
import { Footer } from "../../components/Footer";
import { SEO } from "../../components/SEO";
import AuspiciousCalendarGrid from "./AuspiciousCalendarGrid";
import ChineseWizard from "./ChineseWizard";
import VedicWizard from "./VedicWizard";
import { calculateMonth, fetchCategories } from "./auspiciousApi";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
const SITE = "https://www.everydayhoroscope.in";

function todayMonthStart() {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-01`;
}

function shiftMonth(monthIso, delta) {
  const pivot = new Date(`${monthIso}T12:00:00`);
  pivot.setMonth(pivot.getMonth() + delta);
  return `${pivot.getFullYear()}-${String(pivot.getMonth() + 1).padStart(2, "0")}-01`;
}

function buildSchema() {
  const faqs = [
    {
      q: "What does the Auspicious Day Calculator measure?",
      a: "It combines Vedic Muhurta signals like Tithi, Nakshatra, Vara, and Yoga with Chinese Tong Shu Day Officer logic to rank each date in a target month.",
    },
    {
      q: "Does this calculator use my birth chart?",
      a: "Phase 1 only uses birth date for Chinese zodiac clash filtering. It does not read your full natal chart in this commission.",
    },
    {
      q: "Why can a day be blocked even with a high score?",
      a: "Hard blockers like a category-forbidden Tithi, Po or Bi officer rejection, or a personal zodiac clash can force a blocked tier even when some other signals look strong.",
    },
    {
      q: "Can I use only the Vedic system?",
      a: "Yes. The page supports a Vedic-only path if you want Panchang-based scoring without the Chinese layer.",
    },
    {
      q: "What are the risk toggles for?",
      a: "They tighten the shortlist by filtering Mercury retrograde-sensitive windows and by soft-penalizing days where the premium window overlaps Rahu Kaal.",
    },
  ];

  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "FAQPage",
        mainEntity: faqs.map((item) => ({
          "@type": "Question",
          name: item.q,
          acceptedAnswer: { "@type": "Answer", text: item.a },
        })),
      },
    ],
  };
}

async function fetchPanchangLocations(signal) {
  const response = await fetch(`${BACKEND_URL}/api/panchang/locations`, { signal });
  if (!response.ok) {
    throw new Error("Unable to load Panchang cities.");
  }
  return response.json();
}

export default function AuspiciousPage() {
  const [categories, setCategories] = useState([]);
  const [vectors, setVectors] = useState([]);
  const [locations, setLocations] = useState([]);
  const [activeStep, setActiveStep] = useState("vedic");
  const [loadingCatalogs, setLoadingCatalogs] = useState(true);
  const [loadingResults, setLoadingResults] = useState(false);
  const [catalogError, setCatalogError] = useState("");
  const [resultError, setResultError] = useState("");
  const [system, setSystem] = useState("dual");
  const [days, setDays] = useState([]);

  const [vedicForm, setVedicForm] = useState({
    city_id: "new-delhi-india",
    activity_category: "job_start",
    target_month: todayMonthStart(),
    avoid_retrogrades: false,
    exclude_rahu_kalam: false,
  });

  const [chineseForm, setChineseForm] = useState({
    birth_date: "",
    activity_vector: "contract",
    filter_personal_clash: true,
  });

  useEffect(() => {
    const controller = new AbortController();
    setLoadingCatalogs(true);
    Promise.all([fetchCategories(controller.signal), fetchPanchangLocations(controller.signal)])
      .then(([categoryPayload, locationPayload]) => {
        setCategories(categoryPayload.categories || []);
        setVectors(categoryPayload.activity_vectors || []);
        setLocations(locationPayload || []);
      })
      .catch((error) => {
        setCatalogError(error.message || "Unable to load auspicious calculator references.");
      })
      .finally(() => setLoadingCatalogs(false));

    return () => controller.abort();
  }, []);

  const selectedCategory = useMemo(
    () => categories.find((item) => item.slug === vedicForm.activity_category),
    [categories, vedicForm.activity_category],
  );
  const selectedLocation = useMemo(
    () => locations.find((item) => item.slug === vedicForm.city_id),
    [locations, vedicForm.city_id],
  );

  const runCalculation = async (nextSystem, nextVedicForm = vedicForm, nextChineseForm = chineseForm) => {
    setLoadingResults(true);
    setResultError("");
    setSystem(nextSystem);

    try {
      const result = await calculateMonth({
        city_id: nextVedicForm.city_id,
        activity_category: nextVedicForm.activity_category,
        target_month: nextVedicForm.target_month,
        avoid_retrogrades: nextVedicForm.avoid_retrogrades,
        exclude_rahu_kalam: nextVedicForm.exclude_rahu_kalam,
        birth_date: nextChineseForm.birth_date || undefined,
        activity_vector: nextChineseForm.activity_vector,
        filter_personal_clash: nextChineseForm.filter_personal_clash,
        system: nextSystem,
      });
      setDays(result || []);
      setActiveStep("results");
    } catch (error) {
      setResultError(error.message || "Unable to calculate the auspicious calendar.");
    } finally {
      setLoadingResults(false);
    }
  };

  const handleVedicSubmit = async (nextForm, nextSystem) => {
    setVedicForm(nextForm);
    if (nextSystem === "vedic") {
      await runCalculation("vedic", nextForm, chineseForm);
      return;
    }

    const category = categories.find((item) => item.slug === nextForm.activity_category);
    if (category) {
      setChineseForm((current) => ({
        ...current,
        activity_vector: category.default_activity_vector || current.activity_vector,
      }));
    }
    setSystem("dual");
    setActiveStep("chinese");
  };

  const handleChineseSubmit = async (nextForm) => {
    setChineseForm(nextForm);
    await runCalculation("dual", vedicForm, nextForm);
  };

  const handleMonthShift = async (delta) => {
    const nextForm = {
      ...vedicForm,
      target_month: shiftMonth(vedicForm.target_month, delta),
    };
    setVedicForm(nextForm);
    await runCalculation(system, nextForm, chineseForm);
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.18),transparent_28%),linear-gradient(180deg,#fffaf0_0%,#f6eddc_52%,#efe3cd_100%)] text-stone-900">
      <SEO
        title="Auspicious Day Calculator - Vedic & Chinese Muhurta | EverydayHoroscope"
        description="Find the most auspicious days for career moves, marriage, property purchase, travel and more. Combines Vedic Muhurta with Chinese Tong Shu for dual-system guidance."
        url={`${SITE}/auspicious-calculator`}
        schema={buildSchema()}
      />

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <section className="overflow-hidden rounded-[2rem] border border-gold/20 bg-white/75 p-8 shadow-sm backdrop-blur sm:p-10">
          <div className="grid gap-8 lg:grid-cols-[1.05fr_0.95fr]">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">AUSPICIOUS-1 · Dual-System Engine</p>
              <h1 className="mt-4 font-cinzel text-4xl font-semibold tracking-tight text-stone-900 sm:text-5xl">
                Auspicious Day Calculator
              </h1>
              <p className="mt-5 max-w-3xl text-sm leading-8 text-stone-600">
                Score every day in a month across Vedic Muhurta and Chinese Tong Shu, then surface the best timing for
                career moves, marriage, property, travel, creative launches, and more.
              </p>
            </div>

            <div className="rounded-[1.75rem] border border-gold/20 bg-gradient-to-br from-white/90 to-gold/10 p-6 shadow-sm">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">How this works</p>
              <ol className="mt-4 grid gap-4">
                <li className="rounded-[1.4rem] border border-gold/15 bg-white/85 p-4 text-sm leading-7 text-stone-700">
                  <span className="font-semibold text-stone-900">1. Pick the intent and city.</span> The Vedic layer reads the live Panchang city catalogue.
                </li>
                <li className="rounded-[1.4rem] border border-gold/15 bg-white/85 p-4 text-sm leading-7 text-stone-700">
                  <span className="font-semibold text-stone-900">2. Add Chinese filters if you want them.</span> Birth date becomes zodiac shielding, not a full chart read.
                </li>
                <li className="rounded-[1.4rem] border border-gold/15 bg-white/85 p-4 text-sm leading-7 text-stone-700">
                  <span className="font-semibold text-stone-900">3. Review the month view.</span> Each day lands in an excellent, good, neutral, or blocked tier.
                </li>
              </ol>
            </div>
          </div>
        </section>

        {catalogError ? (
          <section className="mt-8 rounded-[1.75rem] border border-red-200 bg-red-50 p-5 text-sm text-red-700">
            <div className="flex items-start gap-3">
              <AlertCircle className="mt-0.5 h-5 w-5" />
              <p>{catalogError}</p>
            </div>
          </section>
        ) : null}

        <div className="mt-8">
          {activeStep === "vedic" ? (
            <VedicWizard
              categories={categories}
              locations={locations}
              form={vedicForm}
              busy={loadingResults}
              loadingCatalogs={loadingCatalogs}
              onSubmit={handleVedicSubmit}
            />
          ) : null}

          {activeStep === "chinese" ? (
            <ChineseWizard
              vectors={vectors}
              form={chineseForm}
              busy={loadingResults}
              categoryLabel={selectedCategory?.display_name || "Selected category"}
              onBack={() => setActiveStep("vedic")}
              onSubmit={handleChineseSubmit}
              onSkip={() => runCalculation("vedic", vedicForm, chineseForm)}
            />
          ) : null}

          {resultError ? (
            <section className="mt-8 rounded-[1.75rem] border border-red-200 bg-red-50 p-5 text-sm text-red-700">
              <div className="flex items-start gap-3">
                <AlertCircle className="mt-0.5 h-5 w-5" />
                <p>{resultError}</p>
              </div>
            </section>
          ) : null}

          {activeStep === "results" ? (
            <div className="mt-8">
              <AuspiciousCalendarGrid
                days={days}
                categoryLabel={selectedCategory?.display_name || "Selected category"}
                cityLabel={selectedLocation?.label || vedicForm.city_id}
                system={system}
                loading={loadingResults}
                onPreviousMonth={() => handleMonthShift(-1)}
                onNextMonth={() => handleMonthShift(1)}
                onRecalculate={() => setActiveStep("vedic")}
              />
            </div>
          ) : null}
        </div>
      </main>

      <Footer />
    </div>
  );
}
