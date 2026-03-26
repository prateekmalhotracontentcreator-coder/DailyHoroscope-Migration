import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { Calendar, Sun, Moon, Star, Sparkles, ChevronLeft, ChevronRight, Zap, MapPin, Globe, ChevronDown, Clock } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/panchang`;
const SITE = 'https://everydayhoroscope.in';
const OG_IMAGE = `${SITE}/og-image.png`;
const LOC_STORAGE_KEY = 'panchang_location_slug';
const DEFAULT_SLUG = 'new-delhi-india';

const QUALITY_STYLES = {
  good:    { badge: 'bg-green-100 text-green-800' },
  neutral: { badge: 'bg-amber-100 text-amber-800' },
  caution: { badge: 'bg-red-100 text-red-800' },
};

const TYPE_META = {
  daily:      { title: "Today's Panchang",      icon: Sun,      desc: 'Complete Vedic almanac — Tithi, Nakshatra, Yoga, Karana, Sunrise & Sunset' },
  tomorrow:   { title: "Tomorrow's Panchang",   icon: Sun,      desc: 'Complete Vedic almanac for tomorrow — Tithi, Nakshatra, Yoga, Karana' },
  tithi:      { title: 'Tithi — Lunar Day',      icon: Moon,     desc: "Today's Tithi (lunar day) with Paksha phase and timing" },
  choghadiya: { title: 'Choghadiya',             icon: Zap,      desc: 'Auspicious and inauspicious time periods of the day' },
  calendar:   { title: 'Panchang Calendar',      icon: Calendar, desc: 'Monthly Hindu calendar with Tithi and observances' },
  festivals:  { title: 'Festivals & Vrats',      icon: Sparkles, desc: 'Upcoming Hindu festivals and vrat dates' },
  muhurat:    { title: 'Shubh Muhurat Today',    icon: Star,     desc: 'Auspicious timings today — all 15 Vedic muhurtas with quality and exact times' },
};

const ALIAS = {
  today:      'daily',
  tomorrow:   'tomorrow',
  tithi:      'tithi',
  choghadiya: 'choghadiya',
  muhurat:    'muhurat',
  nakshatra:  'daily',
  rahukaal:   'daily',
};

// ─── Timezone abbreviation helper ──────────────────────────────────────────
const TZ_OVERRIDE = {
  'Asia/Kolkata':         'IST',
  'Asia/Kathmandu':       'NPT',
  'Asia/Dubai':           'GST',
  'Asia/Singapore':       'SGT',
  'Asia/Kuala_Lumpur':    'MYT',
  'Asia/Jakarta':         'WIB',
  'Asia/Makassar':        'WITA',
  'Asia/Bangkok':         'ICT',
  'Asia/Shanghai':        'CST',
  'Pacific/Auckland':     'NZST',
  'Australia/Brisbane':   'AEST',
  'Australia/Sydney':     'AEDT',
  'Australia/Melbourne':  'AEDT',
  'America/Toronto':      'EST',
  'America/Vancouver':    'PST',
};

function getTZAbbr(ianaTimezone) {
  if (!ianaTimezone) return 'IST';
  if (TZ_OVERRIDE[ianaTimezone]) return TZ_OVERRIDE[ianaTimezone];
  try {
    const parts = new Intl.DateTimeFormat('en-US', {
      timeZone: ianaTimezone,
      timeZoneName: 'short',
    }).formatToParts(new Date());
    const tzPart = parts.find(p => p.type === 'timeZoneName');
    if (tzPart?.value) return tzPart.value;
  } catch { /* fall through */ }
  return ianaTimezone.split('/').pop().replace('_', ' ');
}

// ─── Time formatting — with seconds ────────────────────────────────────────
function makeFormatTime(tz) {
  return function formatTime(iso) {
    if (!iso) return '--';
    try {
      return new Date(iso).toLocaleTimeString('en-IN', {
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true,
        timeZone: tz || 'Asia/Kolkata',
      });
    } catch { return iso.slice(11, 19); }
  };
}

function formatDate(iso, tz) {
  if (!iso) return '';
  try {
    return new Date(iso).toLocaleDateString('en-IN', {
      weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
      timeZone: tz || 'Asia/Kolkata',
    });
  } catch { return iso; }
}

function getTodayInTZ(tz) {
  try {
    const now = new Date();
    const parts = new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(now);
    const map = Object.fromEntries(parts.map(p => [p.type, p.value]));
    return `${map.year}-${map.month}-${map.day}`;
  } catch {
    const ist = new Date(new Date().getTime() + 5.5 * 60 * 60 * 1000);
    return ist.toISOString().slice(0, 10);
  }
}

function getTomorrowInTZ(tz) {
  try {
    const tomorrow = new Date(new Date().getTime() + 86400000);
    const parts = new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(tomorrow);
    const map = Object.fromEntries(parts.map(p => [p.type, p.value]));
    return `${map.year}-${map.month}-${map.day}`;
  } catch {
    const ist = new Date(new Date().getTime() + 5.5 * 60 * 60 * 1000);
    ist.setDate(ist.getDate() + 1);
    return ist.toISOString().slice(0, 10);
  }
}

const MONTH_NAMES = ['January','February','March','April','May','June','July','August','September','October','November','December'];

function humanDate(isoDate, tz) {
  if (!isoDate) return '';
  const [y, m, d] = isoDate.split('-');
  try {
    const weekday = new Date(`${isoDate}T12:00:00Z`).toLocaleDateString('en-IN', { weekday: 'long', timeZone: tz || 'Asia/Kolkata' });
    return `${weekday}, ${parseInt(d)} ${MONTH_NAMES[parseInt(m) - 1]} ${y}`;
  } catch {
    return `${parseInt(d)} ${MONTH_NAMES[parseInt(m) - 1]} ${y}`;
  }
}

// ─── Sun & Moon 2×2 grid ────────────────────────────────────────────────────
function SunMoonCards({ summary, panchang, tzAbbr }) {
  const cards = [
    { icon: <Sun className="h-5 w-5 text-amber-500 mx-auto mb-1" />,   label: 'Sunrise',  value: summary.sunrise  || '--', sub: `Sun in ${panchang.sun_sign}` },
    { icon: <Moon className="h-5 w-5 text-slate-400 mx-auto mb-1" />,  label: 'Sunset',   value: summary.sunset   || '--', sub: `Moon in ${panchang.moon_sign}` },
    { icon: <Moon className="h-5 w-5 text-blue-300 mx-auto mb-1" />,   label: 'Moonrise', value: summary.moonrise || '--', sub: panchang.nakshatra?.name ? `${panchang.nakshatra.name} Nakshatra` : '' },
    { icon: <Moon className="h-5 w-5 text-indigo-400 mx-auto mb-1" />, label: 'Moonset',  value: summary.moonset  || '--', sub: panchang.paksha ? `${panchang.paksha} Paksha` : '' },
  ];
  return (
    <div className="grid grid-cols-2 gap-3">
      {cards.map(c => (
        <Card key={c.label} className="p-4 border border-gold/20 text-center">
          {c.icon}
          <p className="text-xs text-muted-foreground uppercase tracking-wide">{c.label}</p>
          <p className="font-semibold text-base tabular-nums">{c.value}</p>
          {c.sub && <p className="text-xs text-muted-foreground mt-0.5 truncate">{c.sub}</p>}
          <p className="text-[10px] text-gold/70 font-bold mt-0.5">{tzAbbr}</p>
        </Card>
      ))}
    </div>
  );
}

// ─── Timing Windows grouped card ────────────────────────────────────────────
// Splits windows by quality into Auspicious / Inauspicious sub-headers.
const AUSPICIOUS_LABELS = new Set(['Brahma Muhurta', 'Abhijit Muhurta', 'Vijaya Muhurta']);

function TimingWindowsCard({ windows, fmtTime, tzAbbr }) {
  if (!windows?.length) return null;
  const now = new Date();
  const auspicious   = windows.filter(w => w.quality === 'good');
  const inauspicious = windows.filter(w => w.quality !== 'good');

  const renderRow = (w, i) => {
    const isCurrent = now >= new Date(w.start) && now <= new Date(w.end);
    return (
      <div key={w.label} className={`flex items-center justify-between px-5 py-3 ${isCurrent ? 'bg-gold/5' : ''}`}>
        <div className="flex items-center gap-3">
          {isCurrent && <span className="w-2 h-2 rounded-full bg-green-500 flex-shrink-0" />}
          <span className="text-sm font-medium">{w.label}</span>
          {isCurrent && <span className="text-xs text-green-600 font-semibold">Now</span>}
        </div>
        <span className="text-xs text-muted-foreground tabular-nums">{fmtTime(w.start)} — {fmtTime(w.end)}</span>
      </div>
    );
  };

  return (
    <Card className="border border-gold/20 overflow-hidden">
      <div className="px-5 py-3 bg-gold/5 border-b border-gold/20 flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-widest text-gold">Timing Windows</p>
        <span className="text-[10px] text-muted-foreground font-semibold">{tzAbbr}</span>
      </div>

      {/* ── Auspicious ───────────────────────────────────────────────────── */}
      {auspicious.length > 0 && (
        <>
          <div className="flex items-center gap-2 px-5 py-2 bg-green-50 border-b border-green-100">
            <span className="text-green-600 text-sm">✦</span>
            <p className="text-[11px] font-bold uppercase tracking-widest text-green-700">Auspicious</p>
          </div>
          <div className="divide-y divide-border">
            {auspicious.map(renderRow)}
          </div>
        </>
      )}

      {/* ── Inauspicious ─────────────────────────────────────────────────── */}
      {inauspicious.length > 0 && (
        <>
          <div className="flex items-center gap-2 px-5 py-2 bg-red-50 border-y border-red-100">
            <span className="text-red-500 text-sm">⚠</span>
            <p className="text-[11px] font-bold uppercase tracking-widest text-red-700">Inauspicious</p>
          </div>
          <div className="divide-y divide-border">
            {inauspicious.map(renderRow)}
          </div>
        </>
      )}
    </Card>
  );
}

// ─── Location picker ────────────────────────────────────────────────────────
function LocationPicker({ selectedSlug, onSelect }) {
  const [locations, setLocations] = useState([]);
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const ref = useRef(null);

  useEffect(() => {
    axios.get(`${API}/locations`).then(r => setLocations(r.data)).catch(() => {});
  }, []);

  useEffect(() => {
    function handleClick(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const selected = locations.find(l => l.slug === selectedSlug);
  const selectedTZAbbr = selected ? getTZAbbr(selected.timezone) : 'IST';
  const countries = [...new Set(locations.map(l => l.country))];

  const filtered = search.trim()
    ? locations.filter(l =>
        l.label.toLowerCase().includes(search.toLowerCase()) ||
        l.country.toLowerCase().includes(search.toLowerCase()) ||
        getTZAbbr(l.timezone).toLowerCase().includes(search.toLowerCase())
      )
    : locations;

  const grouped = countries.reduce((acc, c) => {
    const locs = filtered.filter(l => l.country === c);
    if (locs.length) acc[c] = locs;
    return acc;
  }, {});

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-gold/30 bg-gold/5 text-xs font-semibold text-gold hover:bg-gold/10 transition-colors"
      >
        <MapPin className="h-3 w-3 flex-shrink-0" />
        <span>{selected ? `${selected.label}, ${selected.country}` : 'Select location'}</span>
        <span className="px-1.5 py-0.5 rounded bg-gold/20 text-[10px] font-bold tracking-wide">{selectedTZAbbr}</span>
        <ChevronDown className={`h-3 w-3 flex-shrink-0 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-80 max-h-80 overflow-hidden rounded-xl border border-border bg-background shadow-xl z-50 flex flex-col">
          <div className="p-2 border-b border-border">
            <input
              autoFocus
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search city, country or timezone…"
              className="w-full px-3 py-1.5 text-xs rounded-lg border border-border bg-muted/30 focus:outline-none focus:border-gold/50"
            />
          </div>
          <div className="overflow-y-auto flex-1">
            {Object.entries(grouped).map(([country, locs]) => (
              <div key={country}>
                <div className="flex items-center gap-1.5 px-3 py-1.5 bg-muted/30 sticky top-0">
                  <Globe className="h-3 w-3 text-muted-foreground" />
                  <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">{country}</p>
                </div>
                {locs.map(loc => {
                  const tzAbbr = getTZAbbr(loc.timezone);
                  const isSelected = loc.slug === selectedSlug;
                  return (
                    <button
                      key={loc.slug}
                      onClick={() => { onSelect(loc.slug); setOpen(false); setSearch(''); }}
                      className={`w-full text-left px-4 py-2.5 text-xs hover:bg-gold/10 transition-colors flex items-center justify-between gap-3 ${
                        isSelected ? 'text-gold font-semibold bg-gold/5' : 'text-foreground'
                      }`}
                    >
                      <span className="flex-1">{loc.label}</span>
                      <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold tracking-wide flex-shrink-0 ${
                        isSelected ? 'bg-gold/30 text-gold' : 'bg-muted text-muted-foreground'
                      }`}>{tzAbbr}</span>
                      {isSelected && <span className="text-gold flex-shrink-0">✓</span>}
                    </button>
                  );
                })}
              </div>
            ))}
            {Object.keys(grouped).length === 0 && (
              <p className="text-xs text-muted-foreground text-center py-6">No locations found</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── SEO helpers ────────────────────────────────────────────────────────────
function webPageSchema({ name, description, url, datePublished }) {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name, description, url,
    inLanguage: 'en-IN',
    ...(datePublished ? { datePublished } : {}),
    isPartOf: { '@type': 'WebSite', name: 'Everyday Horoscope', url: SITE },
    provider: { '@type': 'Organization', name: 'Everyday Horoscope', url: SITE },
  };
}

function buildPanchangSEO({ view, calYear, calMonth, dateValue, festivalData, panchangData, locationTZ }) {
  const tz = locationTZ || 'Asia/Kolkata';
  const todayISO    = getTodayInTZ(tz);
  const tomorrowISO = getTomorrowInTZ(tz);
  switch (view) {
    case 'daily': {
      const humanToday = humanDate(todayISO, tz);
      const title = `Today's Panchang — ${humanToday}`;
      const description = `Free daily Panchang for ${humanToday}. Tithi, Nakshatra, Yoga, Karana, Brahma Muhurta, Rahu Kaal, Abhijit Muhurta, Vijaya Muhurta, Sunrise & Moonrise with seconds.`;
      const url = `${SITE}/panchang/today`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    case 'tomorrow': {
      const humanTomorrow = humanDate(tomorrowISO, tz);
      const title = `Tomorrow's Panchang — ${humanTomorrow}`;
      const description = `Panchang for ${humanTomorrow}. Tithi, Nakshatra, Yoga, Karana, all timing windows with exact seconds.`;
      const url = `${SITE}/panchang/tomorrow`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: tomorrowISO }) };
    }
    case 'tithi': {
      const humanToday = humanDate(todayISO, tz);
      const title = `Today's Tithi (Lunar Day) — ${humanToday}`;
      const description = `Today's Tithi, Paksha phase, Nakshatra, Moonrise & Moonset for ${humanToday}.`;
      const url = `${SITE}/panchang/tithi`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    case 'choghadiya': {
      const humanToday = humanDate(todayISO, tz);
      const title = `Choghadiya Today — ${humanToday}`;
      const description = `Auspicious and inauspicious time windows for ${humanToday} — Brahma Muhurta, Abhijit, Vijaya Muhurta, Rahu Kaal, Dur Muhurta with exact times.`;
      const url = `${SITE}/panchang/choghadiya`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    case 'festivals': {
      const year = new Date().getFullYear();
      const title = `Hindu Festivals & Vrats ${year} — Complete Calendar`;
      const description = `Full list of Hindu festivals, vrats, and observances for ${year}.`;
      const url = `${SITE}/panchang/festivals`;
      let schema;
      if (festivalData?.items?.length) {
        schema = { '@context': 'https://schema.org', '@type': 'ItemList', name: title, description, url, numberOfItems: festivalData.items.length,
          itemListElement: festivalData.items.slice(0, 20).map((item, idx) => ({ '@type': 'ListItem', position: idx + 1, name: item.name, description: item.summary || item.name, url: `${SITE}/panchang/date/${item.date}` })) };
      } else { schema = webPageSchema({ name: title, description, url }); }
      return { title, description, url, schema };
    }
    case 'calendar': {
      const y = calYear || new Date().getFullYear();
      const mo = calMonth || (new Date().getMonth() + 1);
      const monthLabel = `${MONTH_NAMES[mo - 1]} ${y}`;
      const title = `Panchang Calendar — ${monthLabel}`;
      const description = `Hindu Panchang calendar for ${monthLabel}. Daily Tithi, Nakshatra, festivals, and Vedic observances.`;
      const url = `${SITE}/panchang/calendar/${y}/${mo}`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: `${y}-${String(mo).padStart(2,'0')}-01` }) };
    }
    case 'date': {
      if (!dateValue) return null;
      const humanDay = humanDate(dateValue, tz);
      let title, description;
      if (panchangData?.panchang) {
        const { tithi, nakshatra, yoga } = panchangData.panchang;
        title = `Panchang ${humanDay} — ${tithi.name}, ${nakshatra.name} Nakshatra`;
        description = `Panchang for ${humanDay}: ${tithi.name} (${panchangData.panchang.paksha} Paksha), ${nakshatra.name}, Yoga: ${yoga.name}.`;
      } else {
        title = `Panchang — ${humanDay}`;
        description = `Complete Vedic Panchang for ${humanDay}. All timing windows with exact seconds.`;
      }
      const url = `${SITE}/panchang/date/${dateValue}`;
      const [y, mo] = dateValue.split('-');
      const breadcrumb = { '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Panchang', item: `${SITE}/panchang/today` },
        { '@type': 'ListItem', position: 2, name: `${MONTH_NAMES[parseInt(mo)-1]} ${y}`, item: `${SITE}/panchang/calendar/${y}/${parseInt(mo)}` },
        { '@type': 'ListItem', position: 3, name: humanDay, item: url },
      ]};
      return { title, description, url, schema: [breadcrumb, webPageSchema({ name: title, description, url, datePublished: dateValue })] };
    }
    case 'muhurat': {
      const humanToday = humanDate(todayISO, tz);
      const title = `Shubh Muhurat Today | Auspicious Timings ${humanToday} | Everyday Horoscope`;
      const description = `Shubh muhurat today for ${humanToday}. All 15 Vedic muhurtas with auspicious time today, muhurta timings, Rahu Kaal, Abhijit & Vijaya Muhurta with exact seconds.`;
      const url = `${SITE}/panchang/muhurat`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    default: return null;
  }
}

function PanchangSEO({ view, calYear, calMonth, dateValue, festivalData, panchangData, locationTZ }) {
  const seo = useMemo(
    () => buildPanchangSEO({ view, calYear, calMonth, dateValue, festivalData, panchangData, locationTZ }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [view, calYear, calMonth, dateValue, festivalData?.items?.length, panchangData?.panchang?.tithi?.name, locationTZ]
  );
  if (!seo) return null;
  const schemas = Array.isArray(seo.schema) ? seo.schema : seo.schema ? [seo.schema] : [];
  return <SEO title={seo.title} description={seo.description} url={seo.url} image={OG_IMAGE} type="website" schema={schemas.length === 1 ? schemas[0] : schemas.length > 1 ? schemas : null} />;
}

// ─── TZ footer note ─────────────────────────────────────────────────────────
function TZNote({ timezone, locationLabel }) {
  if (!timezone) return null;
  return (
    <p className="flex items-center justify-center gap-1.5 text-xs text-muted-foreground">
      <Clock className="h-3 w-3" />
      All times in <span className="font-semibold text-foreground">{getTZAbbr(timezone)}</span>
      {locationLabel ? ` · ${locationLabel}` : ''}
    </p>
  );
}

// ─── SEO body-copy blocks ───────────────────────────────────────────────────
function PanchangDailySEOContent() {
  return (
    <div className="mt-12 space-y-8 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">What is Panchang?</h2><p>Panchang is the traditional Hindu almanac — the word means "five limbs": Tithi, Vara, Nakshatra, Yoga, and Karana. Together they describe the quality of each day according to Vedic astronomy.</p></div>
      <div><h2 className="text-base font-semibold text-foreground mb-2">Auspicious Muhurtas — Brahma, Abhijit, Vijaya</h2><p><strong className="text-foreground">Brahma Muhurta</strong> (96 min before sunrise) is the Creator's Hour — ideal for meditation and new beginnings. <strong className="text-foreground">Abhijit Muhurta</strong> (solar noon ± 24 min) is the most powerful muhurat of the day. <strong className="text-foreground">Vijaya Muhurta</strong> (Victory Hour) is favoured for journeys and ventures — exact timing shifts by weekday.</p></div>
      <div><h2 className="text-base font-semibold text-foreground mb-2">Inauspicious Windows — Rahu Kaal, Yamaganda, Gulika, Dur Muhurta</h2><p>These four windows are traditionally avoided for new activities. Rahu Kaal is the most widely observed — its slot shifts each day of the week. Yamaganda and Gulika Kaal follow their own rotation. Dur Muhurta occurs twice daily at weekday-specific Muhurta positions.</p></div>
    </div>
  );
}

function PanchangTithiSEOContent() {
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">Understanding Tithi</h2><p>A Tithi is a lunar day — the Moon moving 12° from the Sun. There are 30 Tithis per lunar cycle: 15 in Shukla Paksha (waxing) and 15 in Krishna Paksha (waning).</p></div>
    </div>
  );
}

function PanchangChoghadiyaSEOContent() {
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">What is Choghadiya?</h2><p>Choghadiya (चौघड़िया) divides each day into 8 equal time slots from sunrise to sunset, and 8 night slots from sunset to next sunrise. Each slot is ruled by a planet and carries a quality — Amrit (Moon, best), Shubh (Jupiter, good), Labh (Mercury, good), Char (Venus, neutral/travel), Udveg (Sun, avoid), Kaal (Saturn, avoid), Rog (Mars, avoid). Use Choghadiya for quick muhurat decisions like starting travel, business dealings, or auspicious activities.</p></div>
    </div>
  );
}

function PanchangFestivalsSEOContent() {
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">Hindu Festivals and the Vedic Calendar</h2><p>Hindu festivals are computed from Tithi, Nakshatra, and planetary positions — not fixed to the Gregorian calendar. Our dates use the Swiss Ephemeris for maximum accuracy.</p></div>
    </div>
  );
}

// ─── 15-Muhurta data ─────────────────────────────────────────────────────────
const MUHURTA_LIST = [
  { n: 1,  name: 'Rudra',                  quality: 'caution' },
  { n: 2,  name: 'Ahi (Sarpa)',             quality: 'caution' },
  { n: 3,  name: 'Mitra',                   quality: 'good'    },
  { n: 4,  name: 'Pitru (Pitri)',           quality: 'caution' },
  { n: 5,  name: 'Vasu',                    quality: 'good'    },
  { n: 6,  name: 'Vara (Varah)',            quality: 'good'    },
  { n: 7,  name: 'Vishvedeva',              quality: 'good'    },
  { n: 8,  name: 'Vidhi (Brahma)',          quality: 'neutral' },
  { n: 9,  name: 'Satamukhi (Sutamukhi)',   quality: 'good'    },
  { n: 10, name: 'Puruhuta (Indra)',        quality: 'good'    },
  { n: 11, name: 'Vahini',                  quality: 'neutral' },
  { n: 12, name: 'Naktanakara',             quality: 'caution' },
  { n: 13, name: 'Varuna',                  quality: 'good'    },
  { n: 14, name: 'Aryaman',                 quality: 'good'    },
  { n: 15, name: 'Bhaga',                   quality: 'good'    },
];

const MUHURTA_QUALITY_LABEL = { good: 'Auspicious', neutral: 'Neutral', caution: 'Inauspicious' };
const MUHURTA_QUALITY_BADGE = {
  good:    'bg-green-100 text-green-800',
  neutral: 'bg-amber-100 text-amber-800',
  caution: 'bg-red-100 text-red-800',
};

function MuhuratSEOContent() {
  return (
    <div className="mt-12 space-y-8 text-sm text-muted-foreground border-t border-border pt-8">
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">What is Shubh Muhurat?</h2>
        <p>A <strong className="text-foreground">Muhurat</strong> (also spelled Muhurta) is an auspicious time window calculated from the Vedic Panchang — the ancient Hindu almanac. The word literally means "a moment of good omen." In Vedic astrology, not all moments are equal: planetary positions, the lunar day (Tithi), Nakshatra, and the day of the week together determine whether a span of time is favourable, neutral, or to be avoided.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">The 15 Vedic Muhurtas</h2>
        <p>The traditional Vedic system divides each day (sunrise to sunset) into <strong className="text-foreground">15 equal time slots</strong>, each called a Muhurta. The duration of one Muhurta therefore varies by season — roughly 48 minutes on an equinox day. Each slot carries a Sanskrit name and a fixed quality inherited from the presiding deity and planetary ruler. Knowing which Muhurta is active helps practitioners choose the best moment for weddings, business launches, travel, puja, and other significant activities.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Key Auspicious Muhurtas</h2>
        <p><strong className="text-foreground">Abhijit Muhurta</strong> — the solar noon window (±24 min around local solar noon) — is considered the most universally auspicious muhurat and overrides most negative influences. <strong className="text-foreground">Brahma Muhurta</strong> (96 minutes before sunrise) is ideal for study, meditation, and spiritual practice. <strong className="text-foreground">Vijaya Muhurta</strong> (Victory Hour) — weekday-specific — is recommended for journeys and competitive endeavours.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Inauspicious Windows to Avoid</h2>
        <p><strong className="text-foreground">Rahu Kaal</strong> is the most widely observed inauspicious period — its 90-minute slot shifts each day of the week. <strong className="text-foreground">Yamaganda</strong> and <strong className="text-foreground">Gulika Kaal</strong> follow their own weekly rotation. <strong className="text-foreground">Dur Muhurta</strong> occurs twice daily at Rudra and Ahi Muhurta positions. All times shown on this page use the Swiss Ephemeris (pyswisseph) for maximum precision, verified against Drik Panchang.</p>
      </div>
    </div>
  );
}

function MuhuratView({ locationSlug, locationTZ }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true); setError(null); setData(null);
    const tz = locationTZ || 'Asia/Kolkata';
    const dateStr = getTodayInTZ(tz);
    axios.get(`${API}/daily`, { params: { location_slug: locationSlug, date: dateStr } })
      .then(r => setData(r.data))
      .catch(() => setError('Failed to load Muhurat data. Please try again.'))
      .finally(() => setLoading(false));
  }, [locationSlug]); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) return <div className="space-y-4">{[...Array(6)].map((_, i) => <div key={i} className="h-14 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (error)   return <p className="text-center text-muted-foreground py-12">{error}</p>;
  if (!data)   return null;

  const { summary, day_quality_windows } = data;
  const locTZ   = data.location?.timezone || locationTZ || 'Asia/Kolkata';
  const fmtTime = makeFormatTime(locTZ);
  const tzAbbr  = getTZAbbr(locTZ);

  // Derive ISO sunrise/sunset from Brahma Muhurta window (end = sunrise) or time strings + date
  const brahmaWindow = (day_quality_windows || []).find(w => w.label === 'Brahma Muhurta');
  const abhijitWindow = (day_quality_windows || []).find(w => w.label === 'Abhijit Muhurta');
  let sunriseMs = null;
  let sunsetMs  = null;
  if (brahmaWindow?.end) {
    // Brahma Muhurta end is sunrise
    sunriseMs = new Date(brahmaWindow.end).getTime();
  } else if (data.date && summary.sunrise) {
    // Fallback: combine date + time string in location tz
    const [hh, mm, ss] = summary.sunrise.split(':').map(Number);
    const d = new Date(`${data.date}T00:00:00`);
    sunriseMs = d.getTime() + (hh * 3600 + mm * 60 + (ss || 0)) * 1000;
  }
  if (abhijitWindow?.start && abhijitWindow?.end && sunriseMs) {
    // Abhijit = noon ± 24 min; midpoint = solar noon = sunrise + daylight/2
    const noonMs = (new Date(abhijitWindow.start).getTime() + new Date(abhijitWindow.end).getTime()) / 2;
    sunsetMs = sunriseMs + (noonMs - sunriseMs) * 2;
  } else if (data.date && summary.sunset) {
    const [hh, mm, ss] = summary.sunset.split(':').map(Number);
    const d = new Date(`${data.date}T00:00:00`);
    sunsetMs = d.getTime() + (hh * 3600 + mm * 60 + (ss || 0)) * 1000;
  }
  const muhurtaSlots = (sunriseMs && sunsetMs) ? MUHURTA_LIST.map((m, i) => {
    const slotMs = (sunsetMs - sunriseMs) / 15;
    const start  = new Date(sunriseMs + i * slotMs);
    const end    = new Date(sunriseMs + (i + 1) * slotMs);
    return { ...m, start, end };
  }) : null;

  const auspicious   = (day_quality_windows || []).filter(w => w.quality === 'good');
  const inauspicious = (day_quality_windows || []).filter(w => w.quality !== 'good');
  const now = new Date();

  return (
    <div className="space-y-6">
      {/* Hero */}
      <div className="flex items-center justify-between px-6 py-4 bg-gold/5 border border-gold/20 rounded-xl">
        <div className="flex items-center gap-3">
          <Star className="h-5 w-5 text-gold" />
          <span className="font-playfair font-semibold text-lg">
            Shubh Muhurat — {formatDate(data.date + 'T00:00:00', locTZ)}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted-foreground">{data.location?.label}, {data.location?.country}</span>
          <span className="px-1.5 py-0.5 rounded bg-gold/20 text-[10px] font-bold text-gold">{tzAbbr}</span>
        </div>
      </div>

      {/* Auspicious windows */}
      {auspicious.length > 0 && (
        <Card className="border border-green-200 overflow-hidden">
          <div className="px-5 py-3 bg-green-50 border-b border-green-100 flex items-center gap-2">
            <span className="text-green-600">✦</span>
            <p className="text-xs font-semibold uppercase tracking-widest text-green-700">Auspicious Windows</p>
          </div>
          <div className="divide-y divide-border">
            {auspicious.map(w => {
              const isCurrent = now >= new Date(w.start) && now <= new Date(w.end);
              return (
                <div key={w.label} className={`flex items-center justify-between px-5 py-3 ${isCurrent ? 'bg-green-50/60' : ''}`}>
                  <div className="flex items-center gap-3">
                    {isCurrent && <span className="w-2 h-2 rounded-full bg-green-500 flex-shrink-0" />}
                    <span className="text-sm font-medium">{w.label}</span>
                    {isCurrent && <span className="text-xs text-green-600 font-semibold">Now</span>}
                  </div>
                  <span className="text-xs text-muted-foreground tabular-nums">{fmtTime(w.start)} — {fmtTime(w.end)}</span>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {/* 15-Muhurta table */}
      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20 flex items-center justify-between">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">15 Vedic Muhurtas — Sunrise to Sunset</p>
          <span className="text-[10px] text-muted-foreground font-semibold">{tzAbbr}</span>
        </div>
        {muhurtaSlots ? (
          <div className="divide-y divide-border">
            {muhurtaSlots.map(m => {
              const isCurrent = now >= m.start && now < m.end;
              return (
                <div key={m.n} className={`flex items-center gap-3 px-5 py-3 ${isCurrent ? 'bg-gold/5 ring-inset ring-1 ring-gold/20' : ''}`}>
                  <span className="w-6 text-center text-xs font-bold text-muted-foreground flex-shrink-0">{m.n}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-sm font-medium">{m.name}</span>
                      {isCurrent && <span className="text-[10px] font-bold text-gold bg-gold/10 px-1.5 py-0.5 rounded">NOW</span>}
                    </div>
                  </div>
                  <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded flex-shrink-0 ${MUHURTA_QUALITY_BADGE[m.quality]}`}>
                    {MUHURTA_QUALITY_LABEL[m.quality]}
                  </span>
                  <span className="text-xs text-muted-foreground tabular-nums whitespace-nowrap flex-shrink-0">
                    {fmtTime(m.start.toISOString())} — {fmtTime(m.end.toISOString())}
                  </span>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground text-center py-8">Muhurta times require sunrise/sunset data</p>
        )}
      </Card>

      {/* Inauspicious windows */}
      {inauspicious.length > 0 && (
        <Card className="border border-red-200 overflow-hidden">
          <div className="px-5 py-3 bg-red-50 border-b border-red-100 flex items-center gap-2">
            <span className="text-red-500">⚠</span>
            <p className="text-xs font-semibold uppercase tracking-widest text-red-700">Inauspicious Windows — Avoid</p>
          </div>
          <div className="divide-y divide-border">
            {inauspicious.map(w => {
              const isCurrent = now >= new Date(w.start) && now <= new Date(w.end);
              return (
                <div key={w.label} className={`flex items-center justify-between px-5 py-3 ${isCurrent ? 'bg-red-50/40' : ''}`}>
                  <div className="flex items-center gap-3">
                    {isCurrent && <span className="w-2 h-2 rounded-full bg-red-500 flex-shrink-0" />}
                    <span className="text-sm font-medium">{w.label}</span>
                    {isCurrent && <span className="text-xs text-red-600 font-semibold">Now</span>}
                  </div>
                  <span className="text-xs text-muted-foreground tabular-nums">{fmtTime(w.start)} — {fmtTime(w.end)}</span>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      <TZNote timezone={locTZ} locationLabel={data.location?.label} />
      <MuhuratSEOContent />
    </div>
  );
}

function PanchangCalendarSEOContent({ calYear, calMonth }) {
  const monthName = MONTH_NAMES[(calMonth || 1) - 1];
  const year = calYear || new Date().getFullYear();
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">Panchang Calendar — {monthName} {year}</h2><p>Tap any date to see the full Panchang — all five limbs, auspicious & inauspicious windows, Moonrise/Moonset with exact seconds.</p></div>
    </div>
  );
}

function PanchangDateSEOContent({ panchangData }) {
  if (!panchangData?.panchang) return null;
  const { tithi, nakshatra, yoga, karana, paksha, lunar_month, sun_sign, moon_sign } = panchangData.panchang;
  const { sunrise, sunset, moonrise, moonset } = panchangData.summary || {};
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Full Panchang Details</h2>
        <p>Tithi: <strong className="text-foreground">{tithi.name}</strong> ({paksha} Paksha, {lunar_month}). Moon: <strong className="text-foreground">{nakshatra.name}</strong> in {moon_sign}. Sun in {sun_sign}. Yoga: <strong className="text-foreground">{yoga.name}</strong>. Karana: <strong className="text-foreground">{karana.name}</strong>.</p>
        <p className="mt-2 tabular-nums">
          Sunrise: <strong className="text-foreground">{sunrise}</strong>
          {sunset   && <> · Sunset: <strong className="text-foreground">{sunset}</strong></>}
          {moonrise && <> · Moonrise: <strong className="text-foreground">{moonrise}</strong></>}
          {moonset  && <> · Moonset: <strong className="text-foreground">{moonset}</strong></>}
        </p>
      </div>
    </div>
  );
}

// ─── Views ──────────────────────────────────────────────────────────────────

function PanchangDailyView({ dayOffset = 0, locationSlug, locationTZ, onDataLoad }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showWarmup, setShowWarmup] = useState(false);

  // Show warming-up banner if the API call takes more than 4 seconds
  useEffect(() => {
    if (!loading) { setShowWarmup(false); return; }
    const timer = setTimeout(() => { if (loading) setShowWarmup(true); }, 4000);
    return () => clearTimeout(timer);
  }, [loading]);

  useEffect(() => {
    setLoading(true); setError(null); setData(null);
    const tz = locationTZ || 'Asia/Kolkata';
    const dateStr = dayOffset === 1 ? getTomorrowInTZ(tz) : getTodayInTZ(tz);
    axios.get(`${API}/daily`, { params: { location_slug: locationSlug, date: dateStr } })
      .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
      .catch(() => setError('Failed to load Panchang data. Please try again.'))
      .finally(() => setLoading(false));
  }, [dayOffset, locationSlug]); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) return (
    <div className="space-y-4">
      {showWarmup && (
        <div className="warming-up-banner flex items-center gap-3 px-4 py-3 rounded-xl border border-amber-300/60 bg-amber-50 text-amber-800 text-sm font-medium shadow-sm">
          <span className="text-lg leading-none">☀️</span>
          <span>Warming up the astrology engine… (first load takes ~10s)</span>
        </div>
      )}
      {[...Array(5)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}
    </div>
  );
  if (error)   return <p className="text-center text-muted-foreground py-12">{error}</p>;
  if (!data)   return null;

  const { summary, panchang, day_quality_windows, observances } = data;
  const locTZ  = data.location?.timezone || locationTZ || 'Asia/Kolkata';
  const fmtTime = makeFormatTime(locTZ);
  const tzAbbr  = getTZAbbr(locTZ);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between px-6 py-4 bg-gold/5 border border-gold/20 rounded-xl">
        <div className="flex items-center gap-3">
          <Sun className="h-5 w-5 text-gold" />
          <span className="font-playfair font-semibold text-lg">{formatDate(data.date + 'T00:00:00', locTZ)}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted-foreground">{data.location?.label}, {data.location?.country}</span>
          <span className="px-1.5 py-0.5 rounded bg-gold/20 text-[10px] font-bold text-gold">{tzAbbr}</span>
        </div>
      </div>

      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">Panch Anga — Five Limbs</p>
        </div>
        <div className="divide-y divide-border">
          {[
            { label: 'Tithi',      value: panchang.tithi.name,     sub: panchang.paksha + ' Paksha' + (panchang.tithi.end ? ' · until ' + fmtTime(panchang.tithi.end) : '') },
            { label: 'Nakshatra',  value: panchang.nakshatra.name, sub: 'Moon in ' + panchang.moon_sign + (panchang.nakshatra.end ? ' · until ' + fmtTime(panchang.nakshatra.end) : '') },
            { label: 'Yoga',       value: panchang.yoga.name,      sub: panchang.yoga.end ? 'Until ' + fmtTime(panchang.yoga.end) : '' },
            { label: 'Karana',     value: panchang.karana.name,    sub: panchang.karana.end ? 'Until ' + fmtTime(panchang.karana.end) : '' },
            { label: 'Vara (Day)', value: summary.weekday,          sub: panchang.samvat },
          ].map(item => (
            <div key={item.label} className="flex items-center justify-between px-5 py-4">
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-wide mb-0.5">{item.label}</p>
                <p className="font-medium text-sm">{item.value}</p>
              </div>
              {item.sub && <p className="text-xs text-muted-foreground text-right max-w-[220px] tabular-nums">{item.sub}</p>}
            </div>
          ))}
        </div>
      </Card>

      <SunMoonCards summary={summary} panchang={panchang} tzAbbr={tzAbbr} />
      <TimingWindowsCard windows={day_quality_windows} fmtTime={fmtTime} tzAbbr={tzAbbr} />

      {observances?.length > 0 && (
        <Card className="border border-gold/20 p-5">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">Today's Observances</p>
          <div className="space-y-2">
            {observances.map(o => (
              <div key={o.slug} className="flex items-start gap-3">
                <Star className="h-4 w-4 text-gold mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm font-medium">{o.name}</p>
                  <p className="text-xs text-muted-foreground">{o.summary}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
      <TZNote timezone={locTZ} locationLabel={data.location?.label} />
      <div className="flex gap-3">
        <Link to={`/panchang/calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}`}
          className="flex-1 flex items-center justify-center gap-2 py-3 border border-gold/30 rounded-xl text-sm font-medium text-gold hover:bg-gold/5 transition-colors">
          <Calendar className="h-4 w-4" /> Monthly Calendar
        </Link>
        <Link to="/panchang/festivals"
          className="flex-1 flex items-center justify-center gap-2 py-3 border border-gold/30 rounded-xl text-sm font-medium text-gold hover:bg-gold/5 transition-colors">
          <Sparkles className="h-4 w-4" /> Festivals &amp; Vrats
        </Link>
      </div>
      <PanchangDailySEOContent />
    </div>
  );
}

function PanchangTithiView({ locationSlug }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    axios.get(`${API}/daily`, { params: { location_slug: locationSlug } })
      .then(r => setData(r.data)).catch(() => setData(null)).finally(() => setLoading(false));
  }, [locationSlug]);
  if (loading) return <div className="space-y-4">{[...Array(3)].map((_, i) => <div key={i} className="h-20 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (!data)   return <p className="text-center text-muted-foreground py-12">Failed to load Tithi data</p>;
  const { panchang, summary } = data;
  const locTZ  = data.location?.timezone;
  const fmtTime = makeFormatTime(locTZ);
  return (
    <div className="space-y-6">
      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">Today's Tithi</p>
        </div>
        <div className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-3xl font-playfair font-bold">{panchang.tithi.name}</p>
              <p className="text-muted-foreground">{panchang.paksha} Paksha</p>
            </div>
            <Moon className="h-10 w-10 text-gold/60" />
          </div>
          {panchang.tithi.end && (
            <p className="text-sm text-muted-foreground border-t border-border pt-3 tabular-nums">
              Ends at <span className="font-semibold text-foreground">{fmtTime(panchang.tithi.end)}</span>
              {' '}<span className="text-[10px] font-bold text-gold">{getTZAbbr(locTZ)}</span>
            </p>
          )}
        </div>
      </Card>
      <Card className="border border-gold/20 p-5">
        <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">Moon Position</p>
        <div className="grid grid-cols-2 gap-4">
          <div><p className="text-xs text-muted-foreground">Moon Sign</p><p className="font-semibold">{panchang.moon_sign}</p></div>
          <div><p className="text-xs text-muted-foreground">Nakshatra</p><p className="font-semibold">{panchang.nakshatra.name}</p></div>
          <div><p className="text-xs text-muted-foreground">Moonrise</p><p className="font-semibold tabular-nums">{summary.moonrise || '--'}</p></div>
          <div><p className="text-xs text-muted-foreground">Moonset</p><p className="font-semibold tabular-nums">{summary.moonset || '--'}</p></div>
          <div><p className="text-xs text-muted-foreground">Weekday</p><p className="font-semibold">{summary.weekday}</p></div>
          <div><p className="text-xs text-muted-foreground">Samvat</p><p className="font-semibold text-xs">{panchang.samvat}</p></div>
        </div>
      </Card>
      <TZNote timezone={locTZ} locationLabel={data.location?.label} />
      <PanchangTithiSEOContent />
    </div>
  );
}

const CHOG_QUALITY_STYLES = {
  good:    { row: 'border-green-200 bg-green-50/40', badge: 'bg-green-100 text-green-800', dot: 'bg-green-500' },
  neutral: { row: 'border-amber-200 bg-amber-50/40', badge: 'bg-amber-100 text-amber-800', dot: 'bg-amber-500' },
  caution: { row: 'border-red-200 bg-red-50/20',    badge: 'bg-red-100 text-red-800',     dot: 'bg-red-400' },
};

function ChoghadiyaSlotRow({ slot, fmtTime, now }) {
  const isNow = now >= new Date(slot.start) && now < new Date(slot.end);
  const s = CHOG_QUALITY_STYLES[slot.quality] || CHOG_QUALITY_STYLES.neutral;
  return (
    <div className={`flex items-center justify-between px-3 py-2.5 rounded-lg border ${s.row} ${isNow ? 'ring-2 ring-gold/60' : ''}`}>
      <div className="flex items-center gap-2.5 min-w-0">
        <span className={`w-2 h-2 rounded-full flex-shrink-0 ${s.dot}`} />
        <div className="min-w-0">
          <span className="font-semibold text-sm text-foreground">{slot.name}</span>
          <span className="text-xs text-muted-foreground ml-1.5">{slot.ruler}</span>
        </div>
        {isNow && <span className="text-[10px] font-bold text-gold bg-gold/10 px-1.5 py-0.5 rounded">NOW</span>}
      </div>
      <div className="flex items-center gap-2 flex-shrink-0">
        <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded ${s.badge}`}>{slot.quality === 'good' ? 'Auspicious' : slot.quality === 'caution' ? 'Inauspicious' : 'Neutral'}</span>
        <span className="text-xs text-muted-foreground whitespace-nowrap">{fmtTime(slot.start)}–{fmtTime(slot.end)}</span>
      </div>
    </div>
  );
}

function PanchangChoghadiyaView({ locationSlug }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [now, setNow] = useState(new Date());
  useEffect(() => {
    axios.get(`${API}/choghadiya`, { params: { location_slug: locationSlug } })
      .then(r => setData(r.data)).catch(() => setData(null)).finally(() => setLoading(false));
  }, [locationSlug]);
  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 60000);
    return () => clearInterval(t);
  }, []);
  if (loading) return <div className="space-y-2">{[...Array(8)].map((_, i) => <div key={i} className="h-11 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (!data)   return <p className="text-center text-muted-foreground py-12">Failed to load Choghadiya</p>;
  const locTZ   = data.location?.timezone;
  const fmtTime = makeFormatTime(locTZ);
  const tzAbbr  = getTZAbbr(locTZ);
  return (
    <div className="space-y-5">
      {/* Day Choghadiya */}
      <div className="rounded-xl border border-border bg-card p-4 space-y-3">
        <div className="flex items-center gap-2">
          <Sun className="h-4 w-4 text-gold" />
          <h3 className="font-playfair font-semibold text-base">Day Choghadiya</h3>
          <span className="text-xs text-muted-foreground ml-auto">{fmtTime(data.sunrise)} – {fmtTime(data.sunset)}</span>
        </div>
        <div className="space-y-1.5">
          {data.day_choghadiya.map(slot => (
            <ChoghadiyaSlotRow key={slot.index} slot={slot} fmtTime={fmtTime} now={now} />
          ))}
        </div>
      </div>
      {/* Night Choghadiya */}
      <div className="rounded-xl border border-border bg-card p-4 space-y-3">
        <div className="flex items-center gap-2">
          <Moon className="h-4 w-4 text-gold" />
          <h3 className="font-playfair font-semibold text-base">Night Choghadiya</h3>
          <span className="text-xs text-muted-foreground ml-auto">{fmtTime(data.sunset)} – {fmtTime(data.next_sunrise)}</span>
        </div>
        <div className="space-y-1.5">
          {data.night_choghadiya.map(slot => (
            <ChoghadiyaSlotRow key={slot.index} slot={slot} fmtTime={fmtTime} now={now} />
          ))}
        </div>
      </div>
      <TZNote timezone={locTZ} locationLabel={data.location?.label} />
      <PanchangChoghadiyaSEOContent />
    </div>
  );
}

function PanchangCalendarView({ year, month, locationSlug }) {
  const navigate = useNavigate();
  const today = new Date();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    setLoading(true); setData(null);
    axios.get(`${API}/calendar/${year}/${month}`, { params: { location_slug: locationSlug } })
      .then(r => setData(r.data)).catch(() => setData(null)).finally(() => setLoading(false));
  }, [year, month, locationSlug]);
  const prevMonth = month === 1 ? { y: year - 1, m: 12 } : { y: year, m: month - 1 };
  const nextMonth = month === 12 ? { y: year + 1, m: 1 } : { y: year, m: month + 1 };
  const todayISO = today.toISOString().slice(0, 10);
  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <button onClick={() => navigate(`/panchang/calendar/${prevMonth.y}/${prevMonth.m}`)} className="p-2 hover:bg-gold/10 rounded-lg transition-colors"><ChevronLeft className="h-5 w-5 text-gold" /></button>
        <h2 className="font-playfair font-semibold text-xl">{data?.month_label || `${month}/${year}`}</h2>
        <button onClick={() => navigate(`/panchang/calendar/${nextMonth.y}/${nextMonth.m}`)} className="p-2 hover:bg-gold/10 rounded-lg transition-colors"><ChevronRight className="h-5 w-5 text-gold" /></button>
      </div>
      {loading ? (
        <div className="grid grid-cols-7 gap-1">{[...Array(35)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}</div>
      ) : data ? (
        <div className="space-y-1">
          <div className="grid grid-cols-7 gap-1 mb-2">
            {['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].map(d => <div key={d} className="text-center text-xs font-semibold text-muted-foreground py-1">{d}</div>)}
          </div>
          {(() => {
            const firstDay = new Date(year, month - 1, 1).getDay();
            const cells = [...Array(firstDay).fill(null), ...data.days];
            const rows = [];
            for (let i = 0; i < cells.length; i += 7) rows.push(cells.slice(i, i + 7));
            return rows.map((row, ri) => (
              <div key={ri} className="grid grid-cols-7 gap-1">
                {row.map((day, ci) => {
                  if (!day) return <div key={ci} />;
                  const isToday = day.date === todayISO;
                  const hasFestival = day.observances?.length > 0;
                  return (
                    <button key={day.date} onClick={() => navigate(`/panchang/date/${day.date}`)}
                      className={`p-1.5 rounded-lg border text-center w-full transition-all hover:border-gold hover:bg-gold/10 hover:shadow-sm ${isToday ? 'border-gold bg-gold/10' : 'border-border'}`}>
                      <p className={`text-sm font-semibold ${isToday ? 'text-gold' : ''}`}>{day.day}</p>
                      <p className="text-[9px] text-muted-foreground leading-tight mt-0.5 truncate">{day.tithi.split(' ')[1] || day.tithi}</p>
                      {hasFestival && <div className="w-1 h-1 bg-gold rounded-full mx-auto mt-1" />}
                    </button>
                  );
                })}
              </div>
            ));
          })()}
        </div>
      ) : <p className="text-center text-muted-foreground py-12">Failed to load calendar</p>}
      <p className="text-xs text-center text-muted-foreground">Tap any date to view full Panchang details</p>
      <PanchangCalendarSEOContent calYear={year} calMonth={month} />
    </div>
  );
}

function PanchangFestivalsView({ locationSlug, onDataLoad }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const year = new Date().getFullYear();
  useEffect(() => {
    axios.get(`${API}/festivals`, { params: { year, location_slug: locationSlug } })
      .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
      .catch(() => setData(null)).finally(() => setLoading(false));
  }, [locationSlug]); // eslint-disable-line react-hooks/exhaustive-deps
  if (loading) return <div className="space-y-3">{[...Array(8)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (!data?.items?.length) return <p className="text-center text-muted-foreground py-12">No festivals found</p>;
  const grouped = data.items.reduce((acc, item) => { const m = item.date.slice(0,7); if (!acc[m]) acc[m]=[]; acc[m].push(item); return acc; }, {});
  return (
    <div className="space-y-6">
      {Object.entries(grouped).map(([m, items]) => (
        <div key={m}>
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">
            {new Date(m + '-01').toLocaleDateString('en-IN', { month: 'long', year: 'numeric' })}
          </p>
          <div className="space-y-2">
            {items.map(item => (
              <div key={item.slug + item.date} className="flex items-start gap-4 p-4 border border-gold/20 rounded-xl bg-gold/5">
                <div className="text-center min-w-[40px]">
                  <p className="text-xl font-playfair font-bold text-gold">{new Date(item.date + 'T00:00:00').getDate()}</p>
                  <p className="text-[10px] text-muted-foreground uppercase">{new Date(item.date + 'T00:00:00').toLocaleDateString('en-IN', { weekday: 'short' })}</p>
                </div>
                <div>
                  <span className={`text-[10px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full ${item.observance_type === 'festival' ? 'bg-amber-100 text-amber-800' : item.observance_type === 'vrat' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}`}>{item.observance_type}</span>
                  <p className="font-semibold text-sm mt-1">{item.name}</p>
                  <p className="text-xs text-muted-foreground">{item.summary}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
      <PanchangFestivalsSEOContent />
    </div>
  );
}

function PanchangDateView({ dateStr, locationSlug, onDataLoad }) {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    setLoading(true); setError(null); setData(null);
    axios.get(`${API}/date/${dateStr}`, { params: { location_slug: locationSlug } })
      .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
      .catch(() => {
        axios.get(`${API}/daily`, { params: { date: dateStr, location_slug: locationSlug } })
          .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
          .catch(() => setError('Failed to load Panchang data.'))
          .finally(() => setLoading(false));
      })
      .finally(() => setLoading(false));
  }, [dateStr, locationSlug]); // eslint-disable-line react-hooks/exhaustive-deps
  if (loading) return <div className="space-y-4">{[...Array(5)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (error)   return <p className="text-center text-muted-foreground py-12">{error}</p>;
  if (!data)   return null;
  const { summary, panchang, day_quality_windows, observances } = data;
  const locTZ  = data.location?.timezone || 'Asia/Kolkata';
  const fmtTime = makeFormatTime(locTZ);
  const tzAbbr  = getTZAbbr(locTZ);
  const [y, mo] = dateStr.split('-');
  return (
    <div className="space-y-6">
      <button onClick={() => navigate(`/panchang/calendar/${y}/${parseInt(mo)}`)} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-gold transition-colors">
        <ChevronLeft className="h-4 w-4" /> Back to Calendar
      </button>
      <div className="flex items-center justify-between px-6 py-4 bg-gold/5 border border-gold/20 rounded-xl">
        <div className="flex items-center gap-3">
          <Sun className="h-5 w-5 text-gold" />
          <span className="font-playfair font-semibold text-lg">{formatDate(data.date + 'T00:00:00', locTZ)}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted-foreground">{data.location?.label}, {data.location?.country}</span>
          <span className="px-1.5 py-0.5 rounded bg-gold/20 text-[10px] font-bold text-gold">{tzAbbr}</span>
        </div>
      </div>
      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">Panch Anga — Five Limbs</p>
        </div>
        <div className="divide-y divide-border">
          {[
            { label: 'Tithi',      value: panchang.tithi.name,     sub: panchang.paksha + ' Paksha' },
            { label: 'Nakshatra',  value: panchang.nakshatra.name, sub: 'Moon in ' + panchang.moon_sign },
            { label: 'Yoga',       value: panchang.yoga.name,      sub: '' },
            { label: 'Karana',     value: panchang.karana.name,    sub: '' },
            { label: 'Vara (Day)', value: summary.weekday,          sub: panchang.samvat },
          ].map(item => (
            <div key={item.label} className="flex items-center justify-between px-5 py-4">
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-wide mb-0.5">{item.label}</p>
                <p className="font-medium text-sm">{item.value}</p>
              </div>
              {item.sub && <p className="text-xs text-muted-foreground text-right max-w-[200px]">{item.sub}</p>}
            </div>
          ))}
        </div>
      </Card>
      <SunMoonCards summary={summary} panchang={panchang} tzAbbr={tzAbbr} />
      <TimingWindowsCard windows={day_quality_windows} fmtTime={fmtTime} tzAbbr={tzAbbr} />
      {observances?.length > 0 && (
        <Card className="border border-gold/20 p-5">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">Observances</p>
          <div className="space-y-2">
            {observances.map(o => (
              <div key={o.slug} className="flex items-start gap-3">
                <Star className="h-4 w-4 text-gold mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm font-medium">{o.name}</p>
                  <p className="text-xs text-muted-foreground">{o.summary}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
      <TZNote timezone={locTZ} locationLabel={data.location?.label} />
      <PanchangDateSEOContent panchangData={data} />
    </div>
  );
}

// ─── Main page ──────────────────────────────────────────────────────────────
export const PanchangPage = () => {
  const { type: rawType = 'daily', year: yearParam, month: monthParam, dateValue } = useParams();
  const resolvedType = ALIAS[rawType] || rawType;
  const isCalendar = resolvedType === 'calendar' || (yearParam && monthParam && !dateValue);
  const isDateView = !!dateValue;
  const activeView = isDateView ? 'date' : isCalendar ? 'calendar' : (resolvedType || 'daily');
  const today = new Date();
  const calYear  = parseInt(yearParam)  || today.getFullYear();
  const calMonth = parseInt(monthParam) || (today.getMonth() + 1);

  const [locationSlug, setLocationSlug] = useState(() => localStorage.getItem(LOC_STORAGE_KEY) || DEFAULT_SLUG);
  const [locationTZ,   setLocationTZ]   = useState('Asia/Kolkata');

  const handleLocationSelect = useCallback((slug) => {
    setLocationSlug(slug);
    localStorage.setItem(LOC_STORAGE_KEY, slug);
  }, []);

  useEffect(() => {
    axios.get(`${API}/locations`)
      .then(r => {
        const loc = r.data.find(l => l.slug === locationSlug);
        if (loc?.timezone) setLocationTZ(loc.timezone);
      })
      .catch(() => {});
  }, [locationSlug]);

  const [festivalData, setFestivalData] = useState(null);
  const [panchangData, setPanchangData] = useState(null);

  useEffect(() => {
    setFestivalData(null);
    setPanchangData(null);
  }, [activeView, dateValue, calYear, calMonth, locationSlug]);

  const config = isDateView
    ? { title: 'Panchang Details', icon: Calendar, desc: 'Complete Vedic almanac for the selected date' }
    : (TYPE_META[activeView] || TYPE_META.daily);

  const subNavItems = [
    { key: 'daily',       label: 'Today',      icon: Sun,      path: '/panchang/today' },
    { key: 'tomorrow',    label: 'Tomorrow',   icon: Sun,      path: '/panchang/tomorrow' },
    { key: 'tithi',       label: 'Tithi',      icon: Moon,     path: '/panchang/tithi' },
    { key: 'muhurat',     label: 'Muhurat',    icon: Star,     path: '/panchang/muhurat' },
    { key: 'choghadiya',  label: 'Choghadiya', icon: Zap,      path: '/panchang/choghadiya' },
    { key: 'calendar',    label: 'Calendar',   icon: Calendar, path: `/panchang/calendar/${today.getFullYear()}/${today.getMonth() + 1}` },
    { key: 'festivals',   label: 'Festivals',  icon: Sparkles, path: '/panchang/festivals' },
  ];

  const subNavActive = activeView === 'date' ? 'calendar' : activeView;

  return (
    <div className="max-w-3xl mx-auto px-4 py-10 pb-24 lg:pb-10">
      <PanchangSEO
        view={activeView} calYear={calYear} calMonth={calMonth}
        dateValue={dateValue} festivalData={festivalData}
        panchangData={panchangData} locationTZ={locationTZ}
      />
      <div className="text-center mb-6">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
          <Calendar className="h-3 w-3" /> Vedic Panchang
        </div>
        <h1 className="text-3xl font-playfair font-semibold mb-2">{config.title}</h1>
        <p className="text-muted-foreground">{config.desc}</p>
      </div>
      <div className="flex justify-end mb-4">
        <LocationPicker selectedSlug={locationSlug} onSelect={handleLocationSelect} />
      </div>
      <div className="flex flex-wrap gap-2 mb-8 border-b border-border pb-4">
        {subNavItems.map(({ key, label, icon: Icon, path }) => (
          <Link key={key} to={path} className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-colors ${subNavActive === key ? 'bg-gold text-white' : 'border border-border text-muted-foreground hover:border-gold/50 hover:text-gold'}`}>
            <Icon className="h-3 w-3" />{label}
          </Link>
        ))}
      </div>
      {isDateView                                 && <PanchangDateView     dateStr={dateValue}           locationSlug={locationSlug} onDataLoad={setPanchangData} />}
      {!isDateView && activeView === 'daily'      && <PanchangDailyView    dayOffset={0}                 locationSlug={locationSlug} locationTZ={locationTZ} onDataLoad={setPanchangData} />}
      {!isDateView && activeView === 'tomorrow'   && <PanchangDailyView    dayOffset={1}                 locationSlug={locationSlug} locationTZ={locationTZ} onDataLoad={setPanchangData} />}
      {!isDateView && activeView === 'tithi'      && <PanchangTithiView                                  locationSlug={locationSlug} />}
      {!isDateView && activeView === 'muhurat'    && <MuhuratView                                        locationSlug={locationSlug} locationTZ={locationTZ} />}
      {!isDateView && activeView === 'choghadiya' && <PanchangChoghadiyaView                             locationSlug={locationSlug} />}
      {!isDateView && activeView === 'calendar'   && <PanchangCalendarView year={calYear} month={calMonth} locationSlug={locationSlug} />}
      {!isDateView && activeView === 'festivals'  && <PanchangFestivalsView                              locationSlug={locationSlug} onDataLoad={setFestivalData} />}
    </div>
  );
};
