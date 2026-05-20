// ─────────────────────────────────────────────────────────────────────────────
// GlassCard.jsx
// STR-R2-A · Visual Foundation
//
// Formal export of the Strategist card primitive -- extracted from the
// existing QuestionnaireWidget.jsx pattern, extended with four variants.
//
// Variants
// ─────────
//   default    · base card surface
//   highlight  · active mission / current Dasha · gold/40 border
//   muted      · completed / inactive items     · reduced opacity
//   warning    · streak-at-risk / Pitru-Rin     · red/30 border
//
// Usage
// ─────
//   <GlassCard>...</GlassCard>
//   <GlassCard variant="highlight">...</GlassCard>
//   <GlassCard as="section" variant="warning" className="p-6">...</GlassCard>
// ─────────────────────────────────────────────────────────────────────────────

import React from 'react';
import { cn } from '../../lib/utils';
import { useStrategistTheme } from './StrategistThemeProvider';

const LIGHT_VARIANTS = {
  default:   'border-gold/20 bg-gold/[0.04]',
  highlight: 'border-gold/40 bg-gold/[0.08]',
  muted:     'border-gold/10 bg-gold/[0.02]',
  warning:   'border-red-500/30 bg-red-500/[0.04]',
};

const DARK_VARIANTS = {
  default:   'border-gold/20 bg-[#161b27]',
  highlight: 'border-gold/40 bg-[#1c2230]',
  muted:     'border-gold/10 bg-[#161b27]/60',
  warning:   'border-red-500/30 bg-[#1c2230]',
};

export function GlassCard({
  variant = 'default',
  as: Tag = 'div',
  className,
  children,
  ...rest
}) {
  const ctx = useStrategistTheme();
  const mode = ctx?.mode ?? 'light';
  const isDark = mode !== 'light';

  const variants = isDark ? DARK_VARIANTS : LIGHT_VARIANTS;
  const surface  = variants[variant] || variants.default;

  return (
    <Tag
      className={cn(
        'rounded-xl border shadow-sm',
        surface,
        className,
      )}
      data-variant={variant}
      data-mode={mode}
      {...rest}
    >
      {children}
    </Tag>
  );
}

export default GlassCard;
