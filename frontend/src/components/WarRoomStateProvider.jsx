import React, { createContext, useContext, useEffect, useState } from 'react';

const SUNSET_BUFFER_MINS = 30;
const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

const WarRoomContext = createContext({
  state: 'OFFENSIVE_GOLD',
  sunset: null,
  countdown: null,
  panchangData: null,
});

export function WarRoomStateProvider({ children, locationSlug = 'new-delhi' }) {
  const [warState, setWarState] = useState('OFFENSIVE_GOLD');
  const [sunset, setSunset] = useState(null);
  const [countdown, setCountdown] = useState(null);
  const [panchangData, setPanchangData] = useState(null);

  useEffect(() => {
    const today = new Date().toISOString().slice(0, 10);
    fetch(`${BACKEND}/api/panchang/daily?date=${today}&location_slug=${locationSlug}`)
      .then(r => r.json())
      .then(data => {
        setPanchangData(data);
        const sunsetStr = data?.sunset || data?.sun?.sunset;
        if (sunsetStr) setSunset(sunsetStr);
      })
      .catch(() => {});
  }, [locationSlug]);

  useEffect(() => {
    if (!sunset) return;

    const tick = () => {
      const now = Date.now();
      const sunsetMs = new Date(sunset).getTime();
      const buffer = SUNSET_BUFFER_MINS * 60 * 1000;

      if (now < sunsetMs - buffer) {
        setWarState('OFFENSIVE_GOLD');
        setCountdown(null);
      } else if (now >= sunsetMs - buffer && now <= sunsetMs) {
        setWarState('GOLDEN_HOUR');
        const remaining = Math.floor((sunsetMs - now) / 1000);
        const m = Math.floor(remaining / 60);
        const s = remaining % 60;
        setCountdown(`${m}:${String(s).padStart(2, '0')}`);
      } else {
        setWarState('DEFENSIVE_MIDNIGHT');
        setCountdown(null);
      }
    };

    tick();
    const id = setInterval(tick, 5000);
    return () => clearInterval(id);
  }, [sunset]);

  return (
    <WarRoomContext.Provider value={{ state: warState, sunset, countdown, panchangData }}>
      {children}
    </WarRoomContext.Provider>
  );
}

export function useWarRoom() {
  return useContext(WarRoomContext);
}
