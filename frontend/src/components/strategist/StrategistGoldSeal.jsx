// ─────────────────────────────────────────────────────────────────────────────
// StrategistGoldSeal.jsx
// STR-R2-A · Visual Foundation
//
// The Strategist's emblem mark. Compass + yantra geometry on a diamond
// chassis, mono-line. One SVG, scales infinitely.
//
// Props
// ─────
//   size       · number  · pixel dimension (default 80)
//   tone       · string  · 'gold' (default) or any CSS colour string
//   rotating   · boolean · runs the 6s ±2° gentle rotation loop
//   className  · string  · applied to the wrapping <span>
// ─────────────────────────────────────────────────────────────────────────────

import React, { useId } from 'react';
import { cn } from '@/lib/utils';

const GOLD = '#C5A059';

export function StrategistGoldSeal({
  size = 80,
  tone = 'gold',
  rotating = false,
  className,
  title = 'The Strategist',
  ...rest
}) {
  const id = useId();
  const colour = tone === 'gold' ? GOLD : tone;
  const stroke = Math.max(0.8, size / 80);

  return (
    <span
      role="img"
      aria-label={title}
      className={cn('inline-block leading-none', className)}
      style={{
        width: size,
        height: size,
        animation: rotating ? 'strategist-seal-rot 14s ease-in-out infinite' : 'none',
        transformOrigin: '50% 50%',
      }}
      {...rest}
    >
      <svg
        viewBox="0 0 80 80"
        width={size}
        height={size}
        fill="none"
        style={{ display: 'block', overflow: 'visible' }}
      >
        <defs>
          <radialGradient id={`sg-${id}`} cx="50%" cy="50%" r="50%">
            <stop offset="0%"   stopColor={colour} stopOpacity="0.18" />
            <stop offset="60%"  stopColor={colour} stopOpacity="0.04" />
            <stop offset="100%" stopColor={colour} stopOpacity="0" />
          </radialGradient>
        </defs>

        {/* radial wash */}
        <circle cx="40" cy="40" r="38" fill={`url(#sg-${id})`} />

        {/* concentric rings */}
        <circle cx="40" cy="40" r="36" stroke={colour} strokeOpacity="0.45" strokeWidth={stroke} />
        <circle cx="40" cy="40" r="28" stroke={colour} strokeOpacity="0.75" strokeWidth={stroke} />

        {/* cardinal compass ticks */}
        {[0, 90, 180, 270].map((deg) => (
          <line key={`c-${deg}`}
            x1="40" y1="2" x2="40" y2="8"
            stroke={colour} strokeWidth={stroke * 1.2} strokeLinecap="round"
            transform={`rotate(${deg} 40 40)`} />
        ))}
        {/* intercardinal short ticks */}
        {[45, 135, 225, 315].map((deg) => (
          <line key={`i-${deg}`}
            x1="40" y1="3" x2="40" y2="6"
            stroke={colour} strokeOpacity="0.55" strokeWidth={stroke} strokeLinecap="round"
            transform={`rotate(${deg} 40 40)`} />
        ))}

        {/* enclosing diamond -- yantra chassis */}
        <path d="M40 8 L72 40 L40 72 L8 40 Z"
          stroke={colour} strokeOpacity="0.9"
          strokeWidth={stroke * 1.1} strokeLinejoin="miter" />

        {/* inner rotated square -- depth layer */}
        <path d="M40 18 L62 40 L40 62 L18 40 Z"
          stroke={colour} strokeOpacity="0.35"
          strokeWidth={stroke} strokeLinejoin="miter" />

        {/* four-petal crosshair */}
        <path d="M40 22 L42.6 37.4 L58 40 L42.6 42.6 L40 58 L37.4 42.6 L22 40 L37.4 37.4 Z"
          fill={colour} fillOpacity="0.18"
          stroke={colour} strokeWidth={stroke * 0.8} strokeLinejoin="miter" />

        {/* centre diamond glyph -- matches BirthChartDisplay */}
        <path d="M40 35 L45 40 L40 45 L35 40 Z" fill={colour} />
      </svg>
    </span>
  );
}

export default StrategistGoldSeal;
