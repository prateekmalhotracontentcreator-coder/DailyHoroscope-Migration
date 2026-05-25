import React from 'react';
import { cn } from '../../lib/utils';
import { GRID_CELL_DETAILS, GRID_LAYOUT } from '../../pages/lo_shu_grid/loShuContent';

function renderCount(number, count) {
  if (!count) return 'Missing';
  if (count <= 3) return String(number).repeat(count);
  return `${number}x${count}`;
}

export default function LoShuGridBoard({
  counts = {},
  interactive = false,
  onCellClick,
  className = '',
  caption = '',
}) {
  return (
    <div className={className}>
      <div className="grid grid-cols-3 gap-3">
        {GRID_LAYOUT.flat().map((number) => {
          const count = Number(counts[number] ?? counts[String(number)] ?? 0);
          const present = count > 0;
          const cell = GRID_CELL_DETAILS[number];
          const Wrapper = interactive ? 'button' : 'div';

          return (
            <Wrapper
              key={number}
              type={interactive ? 'button' : undefined}
              onClick={interactive ? () => onCellClick?.(number, present) : undefined}
              className={cn(
                'rounded-3xl border p-4 text-left transition',
                'min-h-[122px] shadow-sm backdrop-blur',
                present
                  ? 'border-gold/30 bg-gradient-to-br from-gold/20 via-gold/10 to-card'
                  : 'border-border bg-card/60',
                interactive ? 'hover:-translate-y-0.5 hover:border-gold/40 hover:shadow-md' : '',
              )}
            >
              <div className="flex items-start justify-between gap-3">
                <span className={cn('text-3xl font-playfair font-semibold', present ? 'text-gold' : 'text-muted-foreground')}>
                  {number}
                </span>
                <span className={cn('rounded-full px-2.5 py-1 text-[11px] font-semibold uppercase tracking-[0.18em]', present ? 'bg-gold/15 text-gold' : 'bg-muted text-muted-foreground')}>
                  {present ? 'Present' : 'Missing'}
                </span>
              </div>
              <p className="mt-4 text-sm font-semibold text-foreground">{cell.label}</p>
              <p className="mt-1 text-xs leading-5 text-muted-foreground">{cell.note}</p>
              <p className={cn('mt-4 text-sm font-medium', present ? 'text-foreground' : 'text-muted-foreground')}>
                {renderCount(number, count)}
              </p>
            </Wrapper>
          );
        })}
      </div>
      {caption ? <p className="mt-4 text-sm text-muted-foreground">{caption}</p> : null}
    </div>
  );
}
