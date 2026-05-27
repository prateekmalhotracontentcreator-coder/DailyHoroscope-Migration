import React, { useEffect, useMemo, useState } from "react";
import { ChevronLeft, ChevronRight, RotateCcw, Crown } from "lucide-react";

const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

const TIER_STYLES = {
  excellent: "border-gold bg-gradient-to-br from-white to-gold/20 shadow-[0_18px_40px_rgba(197,160,89,0.18)]",
  good: "border-emerald-300 bg-emerald-50",
  neutral: "border-amber-300 bg-amber-50",
  blocked: "border-red-200 bg-red-50",
};

const TIER_LABELS = {
  excellent: "Excellent",
  good: "Good",
  neutral: "Neutral",
  blocked: "Blocked",
};

function buildMonthLabel(days) {
  if (!days.length) return "";
  const target = new Date(`${days[0].date}T12:00:00`);
  return target.toLocaleDateString("en-IN", { month: "long", year: "numeric" });
}

function buildCalendarCells(days) {
  if (!days.length) return [];
  const firstIndex = new Date(`${days[0].date}T12:00:00`).getDay();
  const prefix = Array.from({ length: firstIndex }, (_, index) => ({ key: `blank-${index}`, empty: true }));
  const content = days.map((day) => ({ key: day.date, empty: false, day }));
  const cells = [...prefix, ...content];
  while (cells.length % 7 !== 0) {
    cells.push({ key: `tail-${cells.length}`, empty: true });
  }
  return cells;
}

function scoreSort(a, b) {
  if (a.is_blocked !== b.is_blocked) return a.is_blocked ? 1 : -1;
  if (a.unified_score !== b.unified_score) return b.unified_score - a.unified_score;
  if (a.vedic_score !== b.vedic_score) return b.vedic_score - a.vedic_score;
  return a.date.localeCompare(b.date);
}

function DayBadge({ tier }) {
  if (tier === "excellent") {
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-gold px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.2em] text-stone-950">
        <Crown className="h-3 w-3" />
        Excellent
      </span>
    );
  }
  return (
    <span
      className={`inline-flex rounded-full px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.2em] ${
        tier === "good"
          ? "bg-emerald-100 text-emerald-700"
          : tier === "neutral"
            ? "bg-amber-100 text-amber-700"
            : "bg-red-100 text-red-700"
      }`}
    >
      {TIER_LABELS[tier]}
    </span>
  );
}

export default function AuspiciousCalendarGrid({
  days,
  categoryLabel,
  cityLabel,
  system,
  loading,
  onPreviousMonth,
  onNextMonth,
  onRecalculate,
}) {
  const cells = useMemo(() => buildCalendarCells(days), [days]);
  const topPicks = useMemo(() => [...days].sort(scoreSort).slice(0, 3), [days]);
  const [selectedDay, setSelectedDay] = useState(topPicks[0] || days[0] || null);

  useEffect(() => {
    setSelectedDay(topPicks[0] || days[0] || null);
  }, [days, topPicks]);

  if (!days.length) return null;

  return (
    <section className="rounded-[2rem] border border-gold/20 bg-white/80 p-6 shadow-sm sm:p-8">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Module 3 · Auspicious Calendar</p>
          <h2 className="mt-3 font-cinzel text-3xl text-stone-900">{buildMonthLabel(days)}</h2>
          <div className="mt-3 flex flex-wrap gap-2">
            <span className="rounded-full border border-gold/20 bg-gold/10 px-3 py-1 text-xs font-semibold text-stone-700">{categoryLabel}</span>
            <span className="rounded-full border border-gold/20 bg-white px-3 py-1 text-xs font-semibold text-stone-700">{cityLabel}</span>
            <span className="rounded-full border border-gold/20 bg-white px-3 py-1 text-xs font-semibold uppercase text-stone-700">{system}</span>
          </div>
        </div>

        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            disabled={loading}
            onClick={onPreviousMonth}
            className="inline-flex items-center rounded-full border border-gold/20 bg-white px-4 py-2 text-sm font-semibold text-stone-700 transition hover:border-gold disabled:opacity-50"
          >
            <ChevronLeft className="mr-1 h-4 w-4" />
            Previous
          </button>
          <button
            type="button"
            disabled={loading}
            onClick={onNextMonth}
            className="inline-flex items-center rounded-full border border-gold/20 bg-white px-4 py-2 text-sm font-semibold text-stone-700 transition hover:border-gold disabled:opacity-50"
          >
            Next
            <ChevronRight className="ml-1 h-4 w-4" />
          </button>
          <button
            type="button"
            onClick={onRecalculate}
            className="inline-flex items-center rounded-full bg-gold px-5 py-2 text-sm font-semibold text-stone-950 transition hover:opacity-90"
          >
            <RotateCcw className="mr-2 h-4 w-4" />
            Recalculate
          </button>
        </div>
      </div>

      <div className="mt-8">
        <div className="mb-4 flex items-end justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Top Picks</p>
            <h3 className="mt-2 font-playfair text-2xl font-semibold text-stone-900">Best dates in this month</h3>
          </div>
          <p className="text-sm text-stone-500">Ordered by unified score with blocked days pushed down.</p>
        </div>

        <div className="grid gap-4 lg:grid-cols-3">
          {topPicks.map((day) => (
            <article key={day.date} className="rounded-[1.6rem] border border-gold bg-gradient-to-br from-white to-gold/15 p-5 shadow-sm">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">{day.day_name}</p>
                  <p className="mt-3 font-cinzel text-5xl text-stone-900">{new Date(`${day.date}T12:00:00`).getDate()}</p>
                </div>
                <DayBadge tier={day.tier} />
              </div>
              <p className="mt-4 text-sm font-semibold text-stone-900">
                {day.vedic_details.tithi_name} · {day.vedic_details.nakshatra_name}
              </p>
              <p className="mt-2 inline-flex rounded-full bg-white/85 px-3 py-1 text-sm font-semibold text-stone-800">
                {day.unified_score}/100
              </p>
              <details className="mt-4 rounded-[1.2rem] border border-gold/15 bg-white/80 p-4">
                <summary className="cursor-pointer text-sm font-semibold text-stone-900">Why this day?</summary>
                <p className="mt-3 text-sm leading-7 text-stone-600">{day.recommendation}</p>
              </details>
            </article>
          ))}
        </div>
      </div>

      <div className="mt-8 overflow-hidden rounded-[1.75rem] border border-gold/15 bg-white/85">
        <div className="grid grid-cols-7 border-b border-gold/10 bg-gold/8">
          {WEEKDAYS.map((weekday) => (
            <div key={weekday} className="px-3 py-3 text-center text-xs font-semibold uppercase tracking-[0.2em] text-stone-500">
              {weekday}
            </div>
          ))}
        </div>

        <div className="grid grid-cols-7">
          {cells.map((cell) =>
            cell.empty ? (
              <div key={cell.key} className="min-h-[132px] border-b border-r border-gold/10 bg-white/45" />
            ) : (
              <button
                key={cell.key}
                type="button"
                onClick={() => setSelectedDay(cell.day)}
                title={`${cell.day.vedic_details.tithi_name} · ${cell.day.vedic_details.nakshatra_name} · ${cell.day.chinese_details.day_officer}`}
                className={`min-h-[132px] border-b border-r border-gold/10 p-3 text-left transition hover:bg-gold/8 ${
                  selectedDay?.date === cell.day.date ? "bg-gold/10" : "bg-white/65"
                }`}
              >
                <div className={`rounded-[1.15rem] border p-3 ${TIER_STYLES[cell.day.tier]}`}>
                  <div className="flex items-start justify-between gap-2">
                    <p className="font-cinzel text-3xl text-stone-900">{new Date(`${cell.day.date}T12:00:00`).getDate()}</p>
                    <span className="text-xs font-semibold text-stone-600">{cell.day.unified_score}</span>
                  </div>
                  <p className="mt-3 text-xs font-semibold uppercase tracking-[0.16em] text-stone-500">{TIER_LABELS[cell.day.tier]}</p>
                  <p className="mt-2 line-clamp-2 text-xs leading-5 text-stone-600">{cell.day.chinese_details.day_officer}</p>
                </div>
              </button>
            ),
          )}
        </div>
      </div>

      {selectedDay ? (
        <div className="mt-8 grid gap-5 lg:grid-cols-[0.95fr_1.05fr]">
          <article className="rounded-[1.75rem] border border-gold/15 bg-gold/6 p-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Selected day</p>
                <h3 className="mt-2 font-playfair text-2xl font-semibold text-stone-900">
                  {selectedDay.day_name}, {new Date(`${selectedDay.date}T12:00:00`).toLocaleDateString("en-IN", { day: "numeric", month: "long" })}
                </h3>
              </div>
              <DayBadge tier={selectedDay.tier} />
            </div>

            <div className="mt-5 grid grid-cols-3 gap-3">
              <div className="rounded-[1.2rem] border border-gold/15 bg-white/80 p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-stone-500">Vedic</p>
                <p className="mt-2 text-2xl font-semibold text-stone-900">{selectedDay.vedic_score}</p>
              </div>
              <div className="rounded-[1.2rem] border border-gold/15 bg-white/80 p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-stone-500">Chinese</p>
                <p className="mt-2 text-2xl font-semibold text-stone-900">{selectedDay.chinese_score}</p>
              </div>
              <div className="rounded-[1.2rem] border border-gold/15 bg-white/80 p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-stone-500">Unified</p>
                <p className="mt-2 text-2xl font-semibold text-stone-900">{selectedDay.unified_score}</p>
              </div>
            </div>

            <p className="mt-5 text-sm leading-7 text-stone-700">{selectedDay.recommendation}</p>

            <div className="mt-5 rounded-[1.2rem] border border-gold/15 bg-white/80 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">Blockers</p>
              {selectedDay.blockers.length ? (
                <ul className="mt-3 space-y-2 text-sm leading-6 text-stone-600">
                  {selectedDay.blockers.map((blocker) => (
                    <li key={blocker}>• {blocker}</li>
                  ))}
                </ul>
              ) : (
                <p className="mt-3 text-sm text-stone-600">No hard blockers surfaced for this date.</p>
              )}
            </div>
          </article>

          <article className="rounded-[1.75rem] border border-gold/15 bg-white/85 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Expanded details</p>
            <div className="mt-4 grid gap-4 sm:grid-cols-2">
              <div className="rounded-[1.2rem] border border-gold/15 bg-gold/6 p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-stone-500">Vedic layer</p>
                <p className="mt-3 text-sm font-semibold text-stone-900">{selectedDay.vedic_details.tithi_name}</p>
                <p className="mt-1 text-sm text-stone-600">{selectedDay.vedic_details.nakshatra_name}</p>
                <p className="mt-1 text-sm text-stone-600">{selectedDay.vedic_details.yoga_name}</p>
                <p className="mt-1 text-sm text-stone-600">{selectedDay.vedic_details.karana_name}</p>
                <p className="mt-4 text-xs uppercase tracking-[0.18em] text-stone-500">Timing windows</p>
                <p className="mt-2 text-sm text-stone-700">
                  Abhijit Muhurta: {selectedDay.vedic_details.abhijit_muhurta?.start || "--"} - {selectedDay.vedic_details.abhijit_muhurta?.end || "--"}
                </p>
                <p className="mt-1 text-sm text-red-600">
                  Rahu Kalam: {selectedDay.vedic_details.rahu_kalam?.start || "--"} - {selectedDay.vedic_details.rahu_kalam?.end || "--"}
                </p>
              </div>

              <div className="rounded-[1.2rem] border border-gold/15 bg-gold/6 p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-stone-500">Chinese layer</p>
                <p className="mt-3 text-sm font-semibold text-stone-900">{selectedDay.chinese_details.day_officer}</p>
                <p className="mt-1 text-sm text-stone-600">Day animal: {selectedDay.chinese_details.day_animal}</p>
                <p className="mt-1 text-sm text-stone-600">
                  User animal: {selectedDay.chinese_details.user_animal || "Not supplied"}
                </p>
                <p className="mt-1 text-sm text-stone-600">
                  Personal clash: {selectedDay.chinese_details.is_personal_clash ? "Yes" : "No"}
                </p>
                <p className="mt-1 text-sm text-stone-600">Lunar mansion: {selectedDay.chinese_details.lunar_mansion}</p>
              </div>
            </div>
          </article>
        </div>
      ) : null}

      <div className="mt-8 flex flex-wrap gap-3 rounded-[1.5rem] border border-gold/15 bg-gold/6 p-4 text-sm text-stone-700">
        <span>👑 Excellent (≥80)</span>
        <span>🟢 Good (60-79)</span>
        <span>🟡 Neutral (40-59)</span>
        <span>🔴 Blocked (&lt;40 or hard blocker)</span>
      </div>
    </section>
  );
}
