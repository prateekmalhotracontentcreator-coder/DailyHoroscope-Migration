import { useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const PING_INTERVAL_MS = 4 * 60 * 1000; // 4 minutes

/**
 * useKeepAlive - pings /api/health every 4 minutes and on window focus
 * to prevent Render free-tier cold starts. Silent - never surfaces errors.
 * On first load, fires a 'warmup' custom event so components can show
 * a warming-up banner while the backend is cold-starting.
 */
export const useKeepAlive = () => {
  useEffect(() => {
    let warmupFired = false;

    const ping = async (isInitial = false) => {
      if (isInitial) {
        // Fire warmup event immediately so UI can show banner before awaiting
        warmupFired = true;
        window.dispatchEvent(new CustomEvent('warmup', { detail: { status: 'pending' } }));
      }
      try {
        await axios.get(`${BACKEND_URL}/api/health`, { timeout: 15000 });
        if (isInitial && warmupFired) {
          window.dispatchEvent(new CustomEvent('warmup', { detail: { status: 'ready' } }));
        }
      } catch (_) {
        // Silent
        if (isInitial && warmupFired) {
          window.dispatchEvent(new CustomEvent('warmup', { detail: { status: 'ready' } }));
        }
      }
    };

    ping(true);

    const interval = setInterval(() => ping(false), PING_INTERVAL_MS);

    window.addEventListener('focus', () => ping(false));

    return () => {
      clearInterval(interval);
      window.removeEventListener('focus', () => ping(false));
    };
  }, []);
};
