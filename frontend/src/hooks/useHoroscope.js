import { useState, useEffect } from 'react';

// ─── Zodiac sign data ─────────────────────────────────────────────────────────
export const ZODIAC_SIGNS_FULL = [
  { id: 'aries',       name: 'Aries',       symbol: '\u2648', dates: 'Mar 21 \u2013 Apr 19', element: 'Fire',  dobRange: { start: { m:3,  d:21 }, end: { m:4,  d:19 } } },
  { id: 'taurus',      name: 'Taurus',      symbol: '\u2649', dates: 'Apr 20 \u2013 May 20', element: 'Earth', dobRange: { start: { m:4,  d:20 }, end: { m:5,  d:20 } } },
  { id: 'gemini',      name: 'Gemini',      symbol: '\u264a', dates: 'May 21 \u2013 Jun 20', element: 'Air',   dobRange: { start: { m:5,  d:21 }, end: { m:6,  d:20 } } },
  { id: 'cancer',      name: 'Cancer',      symbol: '\u264b', dates: 'Jun 21 \u2013 Jul 22', element: 'Water', dobRange: { start: { m:6,  d:21 }, end: { m:7,  d:22 } } },
  { id: 'leo',         name: 'Leo',         symbol: '\u264c', dates: 'Jul 23 \u2013 Aug 22', element: 'Fire',  dobRange: { start: { m:7,  d:23 }, end: { m:8,  d:22 } } },
  { id: 'virgo',       name: 'Virgo',       symbol: '\u264d', dates: 'Aug 23 \u2013 Sep 22', element: 'Earth', dobRange: { start: { m:8,  d:23 }, end: { m:9,  d:22 } } },
  { id: 'libra',       name: 'Libra',       symbol: '\u264e', dates: 'Sep 23 \u2013 Oct 22', element: 'Air',   dobRange: { start: { m:9,  d:23 }, end: { m:10, d:22 } } },
  { id: 'scorpio',     name: 'Scorpio',     symbol: '\u264f', dates: 'Oct 23 \u2013 Nov 21', element: 'Water', dobRange: { start: { m:10, d:23 }, end: { m:11, d:21 } } },
  { id: 'sagittarius', name: 'Sagittarius', symbol: '\u2650', dates: 'Nov 22 \u2013 Dec 21', element: 'Fire',  dobRange: { start: { m:11, d:22 }, end: { m:12, d:21 } } },
  { id: 'capricorn',   name: 'Capricorn',   symbol: '\u2651', dates: 'Dec 22 \u2013 Jan 19', element: 'Earth', dobRange: { start: { m:12, d:22 }, end: { m:1,  d:19 } } },
  { id: 'aquarius',    name: 'Aquarius',    symbol: '\u2652', dates: 'Jan 20 \u2013 Feb 18', element: 'Air',   dobRange: { start: { m:1,  d:20 }, end: { m:2,  d:18 } } },
  { id: 'pisces',      name: 'Pisces',      symbol: '\u2653', dates: 'Feb 19 \u2013 Mar 20', element: 'Water', dobRange: { start: { m:2,  d:19 }, end: { m:3,  d:20 } } },
];

export const ZODIAC_MAP = Object.fromEntries(ZODIAC_SIGNS_FULL.map(s => [s.id, s]));

// Derive zodiac sign from a date string (YYYY-MM-DD or Date object)
export const getSignFromDOB = (dob) => {
  if (!dob) return null;
  const d = new Date(dob);
  if (isNaN(d)) return null;
  const m = d.getUTCMonth() + 1; // 1-12
  const day = d.getUTCDate();
  for (const sign of ZODIAC_SIGNS_FULL) {
    const { start, end } = sign.dobRange;
    // Handle Capricorn which spans year boundary (Dec 22 - Jan 19)
    if (start.m > end.m) {
      if ((m === start.m && day >= start.d) || (m === end.m && day <= end.d)) return sign;
    } else {
      if ((m === start.m && day >= start.d) || (m === end.m && day <= end.d) ||
          (m > start.m && m < end.m)) return sign;
    }
  }
  return null;
};

// ─── localStorage keys ────────────────────────────────────────────────────────
const KEY_SIGN      = 'selected-sign';
const KEY_DOB       = 'user-dob';
const KEY_FAVS      = 'favourite-signs';
const KEY_DOB_DONE  = 'dob-prompt-done';

// ─── Hook ─────────────────────────────────────────────────────────────────────
export const useHoroscope = () => {
  const [primarySign, setPrimarySignState]   = useState(null);
  const [favourites,  setFavouritesState]    = useState([]);
  const [dobDone,     setDobDone]            = useState(false);

  // Hydrate from localStorage on mount
  useEffect(() => {
    const sign  = localStorage.getItem(KEY_SIGN);
    const favs  = JSON.parse(localStorage.getItem(KEY_FAVS) || '[]');
    const done  = localStorage.getItem(KEY_DOB_DONE) === 'true';
    if (sign) setPrimarySignState(sign);
    setFavouritesState(favs);
    setDobDone(done);
  }, []);

  // Save DOB + auto-detect sign
  const saveDOB = (dob) => {
    localStorage.setItem(KEY_DOB, dob);
    localStorage.setItem(KEY_DOB_DONE, 'true');
    setDobDone(true);
    const sign = getSignFromDOB(dob);
    if (sign) {
      localStorage.setItem(KEY_SIGN, sign.id);
      setPrimarySignState(sign.id);
      // Auto-add primary sign to favourites if not already there
      setFavouritesState(prev => {
        if (prev.includes(sign.id)) return prev;
        const next = [sign.id, ...prev];
        localStorage.setItem(KEY_FAVS, JSON.stringify(next));
        return next;
      });
    }
    return sign;
  };

  // Toggle favourite
  const toggleFavourite = (signId) => {
    setFavouritesState(prev => {
      const next = prev.includes(signId)
        ? prev.filter(s => s !== signId)
        : [...prev, signId];
      localStorage.setItem(KEY_FAVS, JSON.stringify(next));
      return next;
    });
  };

  // Dismiss prompt without entering DOB
  const dismissDOBPrompt = () => {
    localStorage.setItem(KEY_DOB_DONE, 'true');
    setDobDone(true);
  };

  const isFavourite = (signId) => favourites.includes(signId);

  return {
    primarySign,
    primarySignMeta: primarySign ? ZODIAC_MAP[primarySign] : null,
    favourites,
    favouritesMeta: favourites.map(id => ZODIAC_MAP[id]).filter(Boolean),
    dobDone,
    saveDOB,
    toggleFavourite,
    dismissDOBPrompt,
    isFavourite,
  };
};
