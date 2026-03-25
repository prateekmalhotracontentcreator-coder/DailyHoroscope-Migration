import { useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const PING_INTERVAL_MS = 10 * 60 * 1000; // 10 minutes

/**
 * useKeepAlive - pings /api/health every 10 minutes and on window focus
 * to prevent Render free-tier cold starts. Silent - never surfaces errors.
 */
export const useKeepAlive = () => {
  useEffect(() => {
    const ping = async () => {
      try {
        await axios.get(`${BACKEND_URL}/api/health`, { timeout: 5000 });
      } catch (_) {
        // Silent
      }
    };

    ping();

    const interval = setInterval(ping, PING_INTERVAL_MS);

    window.addEventListener('focus', ping);

    return () => {
      clearInterval(interval);
      window.removeEventListener('focus', ping);
    };
  }, []);
};
