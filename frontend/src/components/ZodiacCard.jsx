import React from 'react';
import { Sparkles, Star } from 'lucide-react';

export const ZodiacCard = ({ sign, onClick, selected, isFavourite, onToggleFavourite }) => {
  return (
    <button
      type="button"
      data-testid={`sign-${sign.id}`}
      onClick={() => onClick(sign)}
      className={`group relative p-4 sm:p-8 rounded-sm border transition-all duration-500 hover:scale-105 hover:-translate-y-2 cursor-pointer ${
        selected
          ? 'border-gold bg-card shadow-[0_0_30px_-5px_rgba(197,160,89,0.4)]'
          : 'border-border bg-card hover:border-gold/50 hover:shadow-[0_4px_20px_-2px_rgba(0,0,0,0.15)]'
      }`}
      style={{ pointerEvents: 'auto' }}
    >
      <div className="flex flex-col items-center space-y-3">
        <span className="text-5xl sm:text-7xl font-playfair leading-none group-hover:scale-110 transition-transform duration-300">
          {sign.symbol}
        </span>
        <h3 className="text-base sm:text-xl font-playfair font-semibold tracking-wide">
          {sign.name}
        </h3>
        <p className="text-xs text-muted-foreground uppercase tracking-[0.2em] font-semibold hidden sm:block">
          {sign.dates}
        </p>
        <span className="text-xs text-gold uppercase tracking-wider">
          {sign.element}
        </span>
      </div>

      {/* Selected badge */}
      {selected && (
        <div className="absolute -top-2 -right-2 bg-gold rounded-full p-1.5">
          <Sparkles className="h-4 w-4 text-primary-foreground" />
        </div>
      )}

      {/* Favourite star button */}
      {onToggleFavourite && (
        <button
          type="button"
          onClick={(e) => { e.stopPropagation(); onToggleFavourite(sign.id); }}
          className={`absolute top-2 left-2 p-1 rounded-full transition-all ${
            isFavourite
              ? 'text-gold bg-gold/10'
              : 'text-muted-foreground/40 hover:text-gold hover:bg-gold/10 opacity-0 group-hover:opacity-100'
          }`}
          aria-label={isFavourite ? 'Remove from favourites' : 'Add to favourites'}
        >
          <Star className={`h-3.5 w-3.5 ${isFavourite ? 'fill-gold' : ''}`} />
        </button>
      )}
    </button>
  );
};
