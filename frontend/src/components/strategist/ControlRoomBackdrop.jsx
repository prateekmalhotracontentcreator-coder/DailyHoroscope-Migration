// ─────────────────────────────────────────────────────────────────────────────
// ControlRoomBackdrop.jsx
// STR-R2-A · Visual Foundation
//
// Renders the Strategist's signature Control Room canvas -- a green Square
// Matrix Grid over the dark navy base. Two variants:
//   ambient  · Variant A · muted green, 10% opacity, 1px lines
//   tactical · Variant B · brighter green, 15% opacity, 1.5px lines
//
// Drop it anywhere a Control Room surface is needed, including inside a
// Light-mode page (Section 6 preview band on the public landing).
// ─────────────────────────────────────────────────────────────────────────────

import React, { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';

const GREEN = {
  ambient:  'oklch(0.65 0.15 145)',
  tactical: 'oklch(0.72 0.18 145)',
};
const GOLD = '#C5A059';

function useIsMobile(breakpoint = 768) {
  const [mobile, setMobile] = useState(() =>
    typeof window === 'undefined' ? false : window.innerWidth < breakpoint
  );
  useEffect(() => {
    const onResize = () => setMobile(window.innerWidth < breakpoint);
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, [breakpoint]);
  return mobile;
}

function gridDataUri({ cell, color, opacity, weight }) {
  const svg =
    `<svg xmlns='http://www.w3.org/2000/svg' width='${cell}' height='${cell}'>` +
      `<path d='M ${cell} 0 L 0 0 0 ${cell}' fill='none' ` +
        `stroke='${color}' stroke-opacity='${opacity}' stroke-width='${weight}'/>` +
    `</svg>`;
  return `url("data:image/svg+xml;utf8,${encodeURIComponent(svg)}")`;
}

export function ControlRoomBackdrop({
  variant = 'ambient',
  tactical,
  children,
  className,
  showCrosshairs = true,
  style,
  ...rest
}) {
  const v = tactical ? 'tactical' : variant;
  const isTactical = v === 'tactical';

  const mobile = useIsMobile();
  const cell = mobile ? 32 : 48;
  const colour = GREEN[v] || GREEN.ambient;
  const opacity = isTactical ? 0.15 : 0.10;
  const weight  = isTactical ? 1.5  : 1;

  const majorCell = cell * 4;
  const majorOp = opacity + 0.05;

  const gridLayer  = gridDataUri({ cell,      color: colour, opacity,  weight });
  const majorLayer = gridDataUri({ cell: majorCell, color: colour, opacity: majorOp, weight });

  return (
    <div
      className={cn('relative', className)}
      data-cr-variant={v}
      style={{
        backgroundColor: 'var(--background-dark-strategist, #0a0d14)',
        backgroundImage: `${majorLayer}, ${gridLayer}`,
        backgroundSize: `${majorCell}px ${majorCell}px, ${cell}px ${cell}px`,
        backgroundPosition: '0 0, 0 0',
        color: '#ECE6D6',
        ...style,
      }}
      {...rest}
    >
      {/* Vignette */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.45) 100%)',
        }}
      />

      {showCrosshairs && <CornerCrosshairs gold={GOLD} />}

      <div className="relative z-[1]">{children}</div>
    </div>
  );
}

function CornerCrosshairs({ gold }) {
  const base = {
    position: 'absolute',
    width: 14,
    height: 14,
    borderColor: gold,
    borderStyle: 'solid',
    opacity: 0.35,
    pointerEvents: 'none',
  };
  return (
    <>
      <span aria-hidden style={{ ...base, top: 12,    left: 12,    borderWidth: '1px 0 0 1px' }} />
      <span aria-hidden style={{ ...base, top: 12,    right: 12,   borderWidth: '1px 1px 0 0' }} />
      <span aria-hidden style={{ ...base, bottom: 12, left: 12,    borderWidth: '0 0 1px 1px' }} />
      <span aria-hidden style={{ ...base, bottom: 12, right: 12,   borderWidth: '0 1px 1px 0' }} />
    </>
  );
}

export default ControlRoomBackdrop;
