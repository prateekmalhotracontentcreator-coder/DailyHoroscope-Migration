import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ExternalLink, Play, Volume2, VolumeX, X } from 'lucide-react';

import { useLiveTv } from '../hooks/useLiveTv';

const DISMISS_KEY = 'temple-live-tv-dismissed';

// ─── Shared video player ──────────────────────────────────────────────────────
// Uses a callback ref to set elem.muted=true SYNCHRONOUSLY before the browser
// makes its autoplay policy decision -- the React `muted` JSX prop is known to
// not reflect to the DOM property in time, causing silent autoplay block.
export function LiveTVPlayer({ title, videoUrl, posterUrl, compact = false }) {
  const videoRef = useRef(null);
  const [muted, setMuted] = useState(true);
  const [playing, setPlaying] = useState(false);

  // Callback ref: fires synchronously when the element mounts.
  // Must set .muted before calling .play() so the browser sees the element
  // as muted when it evaluates the autoplay policy.
  const attachRef = useCallback(
    (el) => {
      if (!el) return;
      el.muted = true; // synchronous -- before autoplay decision
      el.defaultMuted = true;
      videoRef.current = el;
      el.play()
        .then(() => setPlaying(true))
        .catch(() => setPlaying(false));
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [videoUrl],
  );

  // Keep muted state in sync after user toggles
  const toggleMute = () => {
    const next = !muted;
    setMuted(next);
    if (videoRef.current) videoRef.current.muted = next;
  };

  // Manual play -- shown when autoplay was blocked
  const handleManualPlay = () => {
    if (!videoRef.current) return;
    videoRef.current.play()
      .then(() => setPlaying(true))
      .catch(() => {});
  };

  return (
    <div className="overflow-hidden rounded-xl border border-gold/20 bg-black">
      <div className={`relative ${compact ? 'aspect-video' : 'aspect-video md:aspect-[16/8.5]'}`}>
        <video
          ref={attachRef}
          key={videoUrl}
          src={videoUrl}
          poster={posterUrl}
          autoPlay
          loop
          playsInline
          preload="auto"
          className="h-full w-full object-cover"
        />

        {/* Manual play overlay -- visible only if autoplay was blocked */}
        {!playing && (
          <button
            type="button"
            onClick={handleManualPlay}
            className="absolute inset-0 flex items-center justify-center bg-black/40 transition hover:bg-black/50"
            aria-label="Play"
          >
            <div className="grid h-14 w-14 place-items-center rounded-full bg-gold/90 text-black shadow-[0_8px_24px_rgba(197,160,89,0.5)]">
              <Play className="h-6 w-6 translate-x-0.5" />
            </div>
          </button>
        )}
      </div>

      {/* Control bar */}
      <div className="flex items-center justify-between gap-3 border-t border-gold/10 bg-card/95 px-3 py-2">
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold text-foreground">{title}</p>
          <p className="text-xs text-muted-foreground">
            {playing ? 'Playing · loops continuously' : 'Tap ▶ to begin playback'}
          </p>
        </div>
        <button
          type="button"
          onClick={toggleMute}
          className="inline-flex shrink-0 items-center gap-1 rounded-full border border-gold/30 px-3 py-1.5 text-xs font-medium text-gold transition-colors hover:bg-gold/10"
        >
          {muted ? <VolumeX className="h-3.5 w-3.5" /> : <Volume2 className="h-3.5 w-3.5" />}
          {muted ? 'Unmute' : 'Mute'}
        </button>
      </div>
    </div>
  );
}

// ─── Fixed floating panel (homepage + panchang) ───────────────────────────────
export function LiveTVPanel() {
  const navigate = useNavigate();
  const { data, loading } = useLiveTv();
  const [dismissed, setDismissed] = useState(false);

  useEffect(() => {
    setDismissed(window.localStorage.getItem(DISMISS_KEY) === '1');
  }, []);

  // Still fetching -- show a subtle loading pill so the user knows it's coming
  if (loading) {
    return (
      <div className="fixed right-3 top-20 z-40 inline-flex items-center gap-2 rounded-full border border-gold/20 bg-background/80 px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-gold/50 shadow-lg backdrop-blur sm:right-4">
        <span className="h-2 w-2 animate-pulse rounded-full bg-gold/40" />
        Live TV
      </div>
    );
  }

  // No active video configured
  if (!data?.website_video_url) return null;

  // Dismissed -- show a restore pill
  if (dismissed) {
    return (
      <button
        type="button"
        onClick={() => {
          window.localStorage.removeItem(DISMISS_KEY);
          setDismissed(false);
        }}
        className="fixed right-3 top-20 z-40 inline-flex items-center gap-2 rounded-full border border-gold/30 bg-background/90 px-4 py-2 text-xs font-semibold uppercase tracking-[0.22em] text-gold shadow-lg backdrop-blur sm:right-4"
      >
        <span className="relative flex h-2.5 w-2.5">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-500 opacity-75" />
          <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-red-500" />
        </span>
        Live TV
      </button>
    );
  }

  // Full panel
  return (
    <aside className="fixed right-2 top-20 z-40 w-[min(320px,calc(100vw-1rem))] sm:right-4 sm:w-[320px]">
      <div className="overflow-hidden rounded-2xl border border-gold/25 bg-background/90 shadow-[0_18px_50px_-18px_rgba(197,160,89,0.45)] backdrop-blur">
        {/* Panel header */}
        <div className="flex items-center justify-between gap-3 border-b border-gold/10 px-4 py-3">
          <div className="min-w-0">
            <p className="flex items-center gap-2 text-[11px] font-semibold uppercase tracking-[0.22em] text-gold">
              <span className="relative flex h-2.5 w-2.5">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-500 opacity-75" />
                <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-red-500" />
              </span>
              Live
            </p>
            <p className="truncate text-sm font-semibold text-foreground">
              {data.title || 'Sai Baba Arti'}
            </p>
          </div>
          <button
            type="button"
            onClick={() => {
              window.localStorage.setItem(DISMISS_KEY, '1');
              setDismissed(true);
            }}
            className="rounded-full p-1.5 text-muted-foreground transition-colors hover:bg-gold/10 hover:text-foreground"
            aria-label="Hide Live TV panel"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Player */}
        <div className="p-3">
          <LiveTVPlayer
            title={data.title || 'Live Sai Baba Arti'}
            videoUrl={data.website_video_url}
            posterUrl={data.thumbnail_url}
            compact
          />
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between gap-2 border-t border-gold/10 px-4 py-3">
          <p className="text-xs text-muted-foreground">
            Devotional stream · tap for full immersion
          </p>
          <button
            type="button"
            onClick={() => navigate('/live-sai-baba-arti')}
            className="inline-flex shrink-0 items-center gap-1 rounded-full bg-gold px-3 py-1.5 text-xs font-semibold text-primary-foreground transition-colors hover:bg-gold/90"
          >
            Full Page
            <ExternalLink className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
    </aside>
  );
}
