import { useEffect, useState } from 'react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API = `${BACKEND_URL}/api/live-tv/active`;

// Video and thumbnail are served from Vercel's CDN (frontend/public/live_tv/).
// This avoids Render cold-start delays, mixed-content (http vs https) blocks,
// and any streaming issues with the backend FileResponse endpoint.
const STATIC_VIDEO_URL = '/live_tv/active_live_tv.mp4';
const STATIC_THUMB_URL = '/live_tv/active_live_tv.jpg';

export function useLiveTv() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      setLoading(true);
      try {
        const response = await fetch(API);
        if (!response.ok) {
          throw new Error(
            response.status === 404
              ? 'Live TV is not configured yet.'
              : 'Failed to load Live TV.',
          );
        }
        const payload = await response.json();

        // Override the backend-constructed URLs with Vercel static files.
        // The backend URL may use http:// (Render proxy strips SSL) which
        // browsers silently block as mixed-content on the https:// site.
        payload.website_video_url = STATIC_VIDEO_URL;
        if (!payload.thumbnail_url) {
          payload.thumbnail_url = STATIC_THUMB_URL;
        }

        if (!cancelled) {
          setData(payload);
          setError('');
        }
      } catch (err) {
        // API unavailable -- still activate the player with static assets
        // so the video plays even when Render is cold or unreachable.
        if (!cancelled) {
          setData({
            title: 'LIVE Sai Baba Arti | Om Sai Ram | EverydayHoroscope',
            website_video_url: STATIC_VIDEO_URL,
            thumbnail_url: STATIC_THUMB_URL,
            is_active: true,
          });
          setError(err.message || 'Failed to load Live TV metadata.');
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  return { data, loading, error };
}
