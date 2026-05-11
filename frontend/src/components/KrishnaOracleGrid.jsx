import React, { useEffect, useMemo, useState } from "react";

import { extractChaupaiIndices } from "../utils/chaupaiExtractor";

const GRID_SIZE = 18;
const GLOW_DURATION_MS = 500;

function cellClasses(isActive, isSelected, isPast) {
  const base =
    "flex aspect-square items-center justify-center rounded-lg border text-sm font-semibold transition-all duration-300 select-none";
  if (isSelected) {
    return `${base} border-amber-500 bg-amber-500 text-stone-950 shadow-[0_0_28px_rgba(245,158,11,0.35)] scale-[1.06]`;
  }
  if (isActive) {
    return `${base} border-amber-300 bg-gradient-to-br from-amber-200 to-amber-400 text-stone-950 shadow-[0_0_22px_rgba(251,191,36,0.5)] scale-[1.05]`;
  }
  if (isPast) {
    return `${base} border-amber-300 bg-amber-100/90 text-amber-900 dark:border-amber-700/50 dark:bg-amber-950/40 dark:text-amber-100`;
  }
  return `${base} border-amber-300 bg-white/90 text-amber-900 hover:border-amber-500 hover:bg-amber-50 dark:border-amber-900/60 dark:bg-stone-950/60 dark:text-amber-50 dark:hover:border-amber-500/60 dark:hover:bg-stone-900`;
}

export default function KrishnaOracleGrid({
  gridMatrix,
  selectedIndex,
  disabled = false,
  revealEnabled = false,
  onSelect,
}) {
  const derivedIndices = useMemo(() => {
    if (selectedIndex == null) return [];
    return extractChaupaiIndices(selectedIndex);
  }, [selectedIndex]);

  const [activeIndex, setActiveIndex] = useState(-1);
  const [completedIndices, setCompletedIndices] = useState([]);

  useEffect(() => {
    if (!revealEnabled || selectedIndex == null) {
      setActiveIndex(-1);
      setCompletedIndices([]);
      return undefined;
    }

    setActiveIndex(-1);
    setCompletedIndices([]);

    const timers = derivedIndices.map((index, step) =>
      window.setTimeout(() => {
        setActiveIndex(index);
        setCompletedIndices((current) => {
          const next = current.filter((value) => value !== index);
          next.push(index);
          return next;
        });
      }, step * GLOW_DURATION_MS)
    );

    const cleanupTimer = window.setTimeout(() => {
      setActiveIndex(-1);
    }, derivedIndices.length * GLOW_DURATION_MS);

    return () => {
      timers.forEach((timer) => window.clearTimeout(timer));
      window.clearTimeout(cleanupTimer);
    };
  }, [derivedIndices, revealEnabled, selectedIndex]);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="m-0 text-xs font-semibold uppercase tracking-[0.28em] text-amber-700/80 dark:text-amber-300/80">Krishna Grid</p>
          <h3 className="m-0 mt-1 text-xl font-semibold text-stone-900 dark:text-amber-50">18 × 18 Deterministic Selection Matrix</h3>
        </div>
        <div className="rounded-full border border-amber-300 bg-white/80 px-3 py-1 text-xs text-stone-700 dark:border-amber-700/60 dark:bg-stone-950/50 dark:text-amber-100">
          {selectedIndex == null ? "Choose one akshara" : `Selected index ${selectedIndex}`}
        </div>
      </div>

      <div
        className="grid gap-1.5 rounded-[1.75rem] border border-amber-200/80 bg-[#fff8ec] p-3 md:gap-2 md:p-4 dark:border-amber-900/60 dark:bg-[#160f09]"
        style={{ gridTemplateColumns: `repeat(${GRID_SIZE}, minmax(0, 1fr))` }}
      >
        {gridMatrix.map((glyph, index) => {
          const isSelected = index === selectedIndex;
          const isActive = index === activeIndex;
          const isPast = completedIndices.includes(index);
          const row = Math.floor(index / GRID_SIZE);
          const col = index % GRID_SIZE;
          return (
            <button
              key={`${index}-${glyph}`}
              type="button"
              disabled={disabled}
              onClick={() => onSelect?.({ row, col, index })}
              title={`[${row}][${col}]`}
              className={cellClasses(isActive, isSelected, isPast)}
            >
              <span className="text-[12px] md:text-[13px]">{glyph}</span>
            </button>
          );
        })}
      </div>

      <p className="m-0 text-sm leading-6 text-stone-700 dark:text-amber-100/75">
        The clicked cell becomes position 0 of the Krishna sequence. Each next reveal advances by 12, modulo 324.
      </p>
    </div>
  );
}
