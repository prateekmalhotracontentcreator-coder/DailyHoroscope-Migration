// ─────────────────────────────────────────────────────────────────────────────
// StrategistThemeToggle.jsx
// STR-R2-A · Visual Foundation
//
// Four-state segmented pill toggle: Light · Dark · CR-A · CR-B.
// ─────────────────────────────────────────────────────────────────────────────

import React, { useCallback, useRef } from 'react';
import { Sun, Moon, Grid3x3, LayoutGrid } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useStrategistTheme, STRATEGIST_MODES } from '@/components/strategist/StrategistThemeProvider';

const OPTIONS = [
  { id: 'light',       label: 'Light',  short: 'Light', Icon: Sun,        description: 'Default · matches the rest of the web app' },
  { id: 'dark',        label: 'Dark',   short: 'Dark',  Icon: Moon,       description: 'Navy + gold · reduces glare in long War Room sessions' },
  { id: 'cr-ambient',  label: 'CR · A', short: 'CR-A',  Icon: LayoutGrid, description: 'Control Room · Ambient grid' },
  { id: 'cr-tactical', label: 'CR · B', short: 'CR-B',  Icon: Grid3x3,    description: 'Control Room · Tactical grid' },
];

export function StrategistThemeToggle({ size = 'md', className, showLabels = false }) {
  const { mode, setMode } = useStrategistTheme();
  const groupRef = useRef(null);

  const onKeyDown = useCallback((e) => {
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    e.preventDefault();
    const idx = STRATEGIST_MODES.indexOf(mode);
    if (idx === -1) return;
    const delta = e.key === 'ArrowRight' ? 1 : -1;
    const next = STRATEGIST_MODES[(idx + delta + STRATEGIST_MODES.length) % STRATEGIST_MODES.length];
    setMode(next);
    requestAnimationFrame(() => {
      const el = groupRef.current?.querySelector(`[data-mode-id="${next}"]`);
      if (el) el.focus();
    });
  }, [mode, setMode]);

  const dims = size === 'lg'
    ? { btn: 'h-9 w-9', icon: 16, gap: 'gap-1', pad: 'p-1' }
    : { btn: 'h-7 w-7', icon: 13, gap: 'gap-0.5', pad: 'p-[3px]' };

  return (
    <div
      ref={groupRef}
      role="radiogroup"
      aria-label="Strategist theme mode"
      onKeyDown={onKeyDown}
      className={cn(
        'inline-flex items-center rounded-full',
        'border border-[color:var(--strategist-card-border)]',
        'bg-[color:var(--strategist-card-bg)]',
        dims.gap, dims.pad,
        className,
      )}
    >
      {OPTIONS.map((opt) => {
        const active = mode === opt.id;
        const Icon = opt.Icon;
        return (
          <button
            key={opt.id}
            type="button"
            role="radio"
            data-mode-id={opt.id}
            aria-checked={active}
            aria-label={opt.label}
            title={opt.description}
            tabIndex={active ? 0 : -1}
            onClick={() => setMode(opt.id)}
            className={cn(
              'inline-flex items-center justify-center rounded-full',
              'transition-colors duration-150 ease-out',
              'focus:outline-none focus-visible:ring-2 focus-visible:ring-[color:var(--strategist-gold)]/60',
              dims.btn,
              active
                ? 'bg-[color:var(--strategist-gold)]/15 text-[color:var(--strategist-gold)]'
                : 'text-[color:var(--strategist-text-muted)] hover:text-[color:var(--strategist-gold)]',
            )}
          >
            <Icon size={dims.icon} strokeWidth={1.75} />
            {showLabels && (
              <span className="font-cinzel ml-1.5 text-[10px] font-semibold uppercase tracking-[0.18em]">
                {opt.short}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}

export default StrategistThemeToggle;
