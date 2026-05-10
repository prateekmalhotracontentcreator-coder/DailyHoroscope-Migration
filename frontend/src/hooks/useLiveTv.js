import { useEffect, useState } from 'react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API = `${BACKEND_URL}/api/live-tv/active`;

export function useLiveTv() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      setLoading(true);
      try {
        const response = await fetch(API, { credentials: 'include' });
        if (!response.ok) {
          throw new Error(response.status === 404 ? 'Live TV is not configured yet.' : 'Failed to load Live TV.');
        }
        const payload = await response.json();
        if (!cancelled) {
          setData(payload);
          setError('');
        }
      } catch (err) {
        if (!cancelled) {
          setData(null);
          setError(err.message || 'Failed to load Live TV.');
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  return { data, loading, error };
}
