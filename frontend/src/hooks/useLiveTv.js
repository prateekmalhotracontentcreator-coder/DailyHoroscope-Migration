import { useEffect, useState } from 'react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API = `${BACKEND_URL}/api/live-tv/active`;

// Video and thumbnail are served from Vercel's CDN (frontend/public/live_tv/).
// This avoids Render cold-start delays, mixed-content (http vs https) blocks,
// and any streaming issues with the backend FileResponse endpoint.
const STATIC_VIDEO_URL = '/live_tv/active_live_tv.mp4';
const STATIC_THUMB_URL = '/live_tv/active_live_tv.jpg';

const FALLBACK_DATA = {
  title: 'LIVE Sai Baba Arti | Om Sai Ram | EverydayHoroscope',
  website_video_url: STATIC_VIDEO_URL,
  thumbnail_url: STATIC_THUMB_URL,
  is_active: true,
};

export function useLiveTv() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      setLoading(true);

      // Abort the API call after 5 s so Render cold-starts never block the
      // panel from appearing. The fallback below activates immediately on abort.
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 5000);

      try {
        const response = await fetch(API, { signal: controller.signal });
        clearTimeout(timeout);

        if (!response.ok) {
          throw new Error(
            response.status === 404
              ? 'Live TV is not configured yet.'
              : 'Failed to load Live TV.',
          );
        }

        const payload = await response.json();

        // Always override video/thumbnail with Vercel-hosted static files.
        // The backend constructs http:// URLs (Render proxy strips SSL) which
        // browsers block as mixed-content on the https:// production site.
        payload.website_video_url = STATIC_VIDEO_URL;
        payload.thumbnail_url = STATIC_THUMB_URL;

        if (!cancelled) {
          setData(payload);
          setError('');
        }
      } catch (err) {
        clearTimeout(timeout);
        // API unreachable or timed out -- use static assets so the panel and
        // player always activate, even during Render cold-starts.
        if (!cancelled) {
          setData(FALLBACK_DATA);
          setError('');
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    load();
    return () => { cancelled = true; };
  }, []);

  return { data, loading, error };
}
