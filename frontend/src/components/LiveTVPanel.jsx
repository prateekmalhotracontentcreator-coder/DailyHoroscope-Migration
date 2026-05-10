import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ExternalLink, Volume2, VolumeX, X } from 'lucide-react';

import { useLiveTv } from '../hooks/useLiveTv';

const DISMISS_KEY = 'temple-live-tv-dismissed';

export function LiveTVPlayer({
  title,
  videoUrl,
  posterUrl,
  compact = false,
}) {
  const videoRef = useRef(null);
  const [muted, setMuted] = useState(true);

  useEffect(() => {
    if (!videoRef.current) return;
    videoRef.current.muted = muted;
    const playPromise = videoRef.current.play();
    if (playPromise && typeof playPromise.catch === 'function') {
      playPromise.catch(() => {});
    }
  }, [muted, videoUrl]);

  return (
    <div className="overflow-hidden rounded-xl border border-gold/20 bg-black">
      <div className={`relative ${compact ? 'aspect-video' : 'aspect-video md:aspect-[16/8.5]'}`}>
        <video
          ref={videoRef}
          key={videoUrl}
          src={videoUrl}
          poster={posterUrl}
          className="h-full w-full object-cover"
          autoPlay
          loop
          muted={muted}
          playsInline
          controls={!compact}
        />
      </div>
      <div className="flex items-center justify-between gap-3 border-t border-gold/10 bg-card/95 px-3 py-2">
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold text-foreground">{title}</p>
          <p className="text-xs text-muted-foreground">
            Continuous loop with muted autoplay for smooth browser playback.
          </p>
        </div>
        <button
          type="button"
          onClick={() => setMuted((value) => !value)}
          className="inline-flex items-center gap-1 rounded-full border border-gold/30 px-3 py-1.5 text-xs font-medium text-gold transition-colors hover:bg-gold/10"
        >
          {muted ? <VolumeX className="h-3.5 w-3.5" /> : <Volume2 className="h-3.5 w-3.5" />}
          {muted ? 'Unmute' : 'Mute'}
        </button>
      </div>
    </div>
  );
}

export function LiveTVPanel() {
  const navigate = useNavigate();
  const { data, loading } = useLiveTv();
  const [dismissed, setDismissed] = useState(false);

  useEffect(() => {
    setDismissed(window.localStorage.getItem(DISMISS_KEY) === '1');
  }, []);

  if (loading || !data?.website_video_url) {
    return null;
  }

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
        <span className="inline-block h-2 w-2 rounded-full bg-red-500" />
        Live TV
      </button>
    );
  }

  return (
    <aside className="fixed right-2 top-20 z-40 w-[min(320px,calc(100vw-1rem))] sm:right-4 sm:w-[320px]">
      <div className="overflow-hidden rounded-2xl border border-gold/25 bg-background/90 shadow-[0_18px_50px_-18px_rgba(197,160,89,0.45)] backdrop-blur">
        <div className="flex items-center justify-between gap-3 border-b border-gold/10 px-4 py-3">
          <div className="min-w-0">
            <p className="flex items-center gap-2 text-[11px] font-semibold uppercase tracking-[0.22em] text-gold">
              <span className="inline-block h-2 w-2 rounded-full bg-red-500" />
              Live
            </p>
            <p className="truncate text-sm font-semibold text-foreground">{data.title || 'Sai Baba Arti'}</p>
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

        <div className="p-3">
          <LiveTVPlayer
            title={data.title || 'Live Sai Baba Arti'}
            videoUrl={data.website_video_url}
            posterUrl={data.thumbnail_url}
            compact
          />
        </div>

        <div className="flex items-center justify-between gap-2 border-t border-gold/10 px-4 py-3">
          <p className="text-xs text-muted-foreground">Top-right on the public landing page (/) only, with full page immersion one tap away.</p>
          <button
            type="button"
            onClick={() => navigate('/live-sai-baba-arti')}
            className="inline-flex items-center gap-1 rounded-full bg-gold px-3 py-1.5 text-xs font-semibold text-primary-foreground transition-colors hover:bg-gold/90"
          >
            Full Page
            <ExternalLink className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
    </aside>
  );
}
