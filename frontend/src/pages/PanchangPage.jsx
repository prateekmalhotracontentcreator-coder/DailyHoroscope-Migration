import React, { useState, useEffect, useMemo } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { Calendar, Sun, Moon, Star, Sparkles, ChevronLeft, ChevronRight, Zap } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/panchang`;
const SITE = 'https://everydayhoroscope.in';
const OG_IMAGE = `${SITE}/og-image.png`;

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
};

const ALIAS = {
  today:      'daily',
  tomorrow:   'tomorrow',
  tithi:      'tithi',
  choghadiya: 'choghadiya',
  muhurat:    'daily',
  nakshatra:  'daily',
  rahukaal:   'daily',
};

// ─── date helpers ──────────────────────────────────────────────────────────

function formatTime(iso) {
  if (!iso) return '--';
  try { return new Date(iso).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true, timeZone: 'Asia/Kolkata' }); }
  catch { return iso.slice(11, 16); }
}

function formatDate(iso) {
  if (!iso) return '';
  try { return new Date(iso).toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Asia/Kolkata' }); }
  catch { return iso; }
}

function getTodayIST() {
  const now = new Date();
  const ist = new Date(now.getTime() + 5.5 * 60 * 60 * 1000);
  const y = ist.getUTCFullYear();
  const m = String(ist.getUTCMonth() + 1).padStart(2, '0');
  const d = String(ist.getUTCDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function getTomorrowIST() {
  const now = new Date();
  const ist = new Date(now.getTime() + 5.5 * 60 * 60 * 1000);
  ist.setUTCDate(ist.getUTCDate() + 1);
  const y = ist.getUTCFullYear();
  const m = String(ist.getUTCMonth() + 1).padStart(2, '0');
  const d = String(ist.getUTCDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

const MONTH_NAMES = ['January','February','March','April','May','June','July','August','September','October','November','December'];

function humanDate(isoDate) {
  if (!isoDate) return '';
  const [y, m, d] = isoDate.split('-');
  const weekday = new Date(`${isoDate}T12:00:00+05:30`).toLocaleDateString('en-IN', { weekday: 'long', timeZone: 'Asia/Kolkata' });
  return `${weekday}, ${parseInt(d)} ${MONTH_NAMES[parseInt(m) - 1]} ${y}`;
}

// ─── SEO helpers ───────────────────────────────────────────────────────────

function webPageSchema({ name, description, url, datePublished }) {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name,
    description,
    url,
    inLanguage: 'en-IN',
    ...(datePublished ? { datePublished } : {}),
    isPartOf: { '@type': 'WebSite', name: 'Everyday Horoscope', url: SITE },
    provider: { '@type': 'Organization', name: 'Everyday Horoscope', url: SITE },
  };
}

function buildPanchangSEO({ view, calYear, calMonth, dateValue, festivalData, panchangData }) {
  const todayISO    = getTodayIST();
  const tomorrowISO = getTomorrowIST();
  switch (view) {
    case 'daily': {
      const humanToday = humanDate(todayISO);
      const title = `Today's Panchang — ${humanToday}`;
      const description = `Free daily Panchang for ${humanToday}. Get today's Tithi, Nakshatra, Yoga, Karana, Rahu Kaal, Gulika Kaal, Abhijit Muhurta, Sunrise & Sunset — powered by Vedic astronomy.`;
      const url = `${SITE}/panchang/today`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    case 'tomorrow': {
      const humanTomorrow = humanDate(tomorrowISO);
      const title = `Tomorrow's Panchang — ${humanTomorrow}`;
      const description = `Panchang for ${humanTomorrow}. Plan your day with tomorrow's Tithi, Nakshatra, Yoga, Karana, Rahu Kaal, Gulika Kaal, Abhijit Muhurta, and Sunrise & Sunset.`;
      const url = `${SITE}/panchang/tomorrow`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: tomorrowISO }) };
    }
    case 'tithi': {
      const humanToday = humanDate(todayISO);
      const title = `Today's Tithi (Lunar Day) — ${humanToday}`;
      const description = `What is today's Tithi? Find the current Tithi (lunar day), Paksha phase, Nakshatra, and Moon sign for ${humanToday} — accurate Vedic Panchang data.`;
      const url = `${SITE}/panchang/tithi`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    case 'choghadiya': {
      const humanToday = humanDate(todayISO);
      const title = `Choghadiya Today — ${humanToday}`;
      const description = `Today's Choghadiya table for ${humanToday}. Find auspicious (Amrit, Shubh, Labh, Char) and inauspicious time slots for starting new work, travel, and muhurat planning.`;
      const url = `${SITE}/panchang/choghadiya`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    case 'festivals': {
      const year = new Date().getFullYear();
      const title = `Hindu Festivals & Vrats ${year} — Complete Calendar`;
      const description = `Full list of Hindu festivals, vrats, and religious observances for ${year}. Includes Ekadashi, Purnima, Amavasya, and major festivals with exact dates.`;
      const url = `${SITE}/panchang/festivals`;
      let schema;
      if (festivalData?.items?.length) {
        schema = { '@context': 'https://schema.org', '@type': 'ItemList', name: title, description, url, numberOfItems: festivalData.items.length,
          itemListElement: festivalData.items.slice(0, 20).map((item, idx) => ({ '@type': 'ListItem', position: idx + 1, name: item.name, description: item.summary || item.name, url: `${SITE}/panchang/date/${item.date}` })) };
      } else {
        schema = webPageSchema({ name: title, description, url });
      }
      return { title, description, url, schema };
    }
    case 'calendar': {
      const y = calYear || new Date().getFullYear();
      const mo = calMonth || (new Date().getMonth() + 1);
      const monthLabel = `${MONTH_NAMES[mo - 1]} ${y}`;
      const title = `Panchang Calendar — ${monthLabel}`;
      const description = `Hindu Panchang calendar for ${monthLabel}. View daily Tithi, Nakshatra, festivals, and Vedic observances for every day of ${monthLabel}.`;
      const url = `${SITE}/panchang/calendar/${y}/${mo}`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: `${y}-${String(mo).padStart(2,'0')}-01` }) };
    }
    case 'date': {
      if (!dateValue) return null;
      const humanDay = humanDate(dateValue);
      let title, description;
      if (panchangData?.panchang) {
        const { tithi, nakshatra, yoga } = panchangData.panchang;
        title = `Panchang ${humanDay} — ${tithi.name}, ${nakshatra.name} Nakshatra`;
        description = `Panchang for ${humanDay}: Tithi — ${tithi.name} (${panchangData.panchang.paksha} Paksha), Nakshatra — ${nakshatra.name}, Yoga — ${yoga.name}. Includes Rahu Kaal, Gulika Kaal, Sunrise & Sunset timings.`;
      } else {
        title = `Panchang — ${humanDay}`;
        description = `Complete Vedic Panchang for ${humanDay}. Tithi, Nakshatra, Yoga, Karana, Rahu Kaal, Gulika Kaal, Abhijit Muhurta, Sunrise & Sunset.`;
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
    default: return null;
  }
}

function PanchangSEO({ view, calYear, calMonth, dateValue, festivalData, panchangData }) {
  const seo = useMemo(
    () => buildPanchangSEO({ view, calYear, calMonth, dateValue, festivalData, panchangData }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [view, calYear, calMonth, dateValue, festivalData?.items?.length, panchangData?.panchang?.tithi?.name]
  );
  if (!seo) return null;
  const schemas = Array.isArray(seo.schema) ? seo.schema : seo.schema ? [seo.schema] : [];
  return <SEO title={seo.title} description={seo.description} url={seo.url} image={OG_IMAGE} type="website" schema={schemas.length === 1 ? schemas[0] : schemas.length > 1 ? schemas : null} />;
}

// ─── SEO body-copy blocks ──────────────────────────────────────────────────
// Static, crawlable explanatory content rendered below the live data.
// These are what Google actually ranks — descriptive H2/H3 + paragraph copy.

function PanchangDailySEOContent() {
  return (
    <div className="mt-12 space-y-8 text-sm text-muted-foreground border-t border-border pt-8">
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">What is Panchang?</h2>
        <p>Panchang (also written as Panchangam or Panchāṅga) is the traditional Hindu almanac used across India for over 1,800 years. The word means "five limbs" — referring to Tithi (lunar day), Vara (weekday), Nakshatra (lunar mansion), Yoga, and Karana. Together these five elements describe the quality and character of each day according to Vedic astronomy.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">What is Rahu Kaal?</h2>
        <p>Rahu Kaal is an inauspicious 90-minute period each day governed by Rahu, the shadow planet. The traditional Vedic system divides daylight into 8 equal Kaals. Rahu Kaal occupies one of these slots, with the exact slot shifting each day of the week — Monday through Sunday each have a different Rahu Kaal position. Important activities like travel, business deals, or ceremonies are generally avoided during this window.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">What is Abhijit Muhurta?</h2>
        <p>Abhijit Muhurta is the most auspicious 48-minute window of the day, centred on solar noon. It is considered so powerful in Vedic tradition that it overrides most negative planetary influences. Starting any new work, signing agreements, or making important decisions during Abhijit Muhurta is highly recommended — except on Wednesdays.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Tithi, Nakshatra, Yoga and Karana explained</h2>
        <p><strong className="text-foreground">Tithi</strong> is the lunar day — calculated from the angular distance between the Sun and Moon. There are 30 Tithis in a lunar month, 15 in Shukla Paksha (waxing) and 15 in Krishna Paksha (waning). <strong className="text-foreground">Nakshatra</strong> is the lunar mansion — the position of the Moon among the 27 asterisms of the zodiac. <strong className="text-foreground">Yoga</strong> is computed from the sum of Sun and Moon longitudes and indicates the combined planetary quality of the day. <strong className="text-foreground">Karana</strong> is half a Tithi and changes twice daily.</p>
      </div>
    </div>
  );
}

function PanchangTithiSEOContent() {
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Understanding Tithi — the Vedic Lunar Day</h2>
        <p>In Vedic astrology, a Tithi is not a solar calendar day — it is a lunar day defined by the Moon moving 12° away from the Sun. This means a Tithi can begin and end at any time of the solar day, and two Tithis can even fall within one solar day. There are 30 Tithis in a complete lunar cycle (Paksha), numbered 1 (Pratipada) through 15 (Purnima or Amavasya).</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Shukla Paksha and Krishna Paksha</h2>
        <p>The lunar month is split into two fortnights. Shukla Paksha is the bright fortnight from Amavasya (new moon) to Purnima (full moon) — associated with growth and auspicious beginnings. Krishna Paksha is the dark fortnight from Purnima to Amavasya — associated with completion, letting go, and ancestral rites. Many Vedic rituals and festivals are specifically tied to Tithis within each Paksha.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Important Tithis and their significance</h2>
        <p>Ekadashi (11th Tithi) is observed as a fast day dedicated to Lord Vishnu in both Pakshas. Chaturdashi (14th) in Krishna Paksha is Shivaratri — auspicious for Shiva worship. Purnima (15th Shukla) is the full moon, ideal for spiritual practices and charity. Amavasya (15th Krishna) is the new moon, observed for ancestral rites (Pitru Tarpan). Pradosh (13th Tithi) is sacred to Lord Shiva.</p>
      </div>
    </div>
  );
}

function PanchangChoghadiyaSEOContent() {
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">What is Choghadiya?</h2>
        <p>Choghadiya (also Chaughadia) is a traditional Vedic time-keeping system that divides the day and night into eight equal segments called Choghadiyas. Each Choghadiya is approximately 90 minutes long and is classified by its ruling planet, giving it one of seven qualities: Amrit (excellent), Shubh (auspicious), Labh (profitable), Char (neutral — good for travel), Udveg (inauspicious — Sun rules), Kaal (inauspicious — Saturn rules), and Rog (inauspicious — Mars rules).</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">How to use Choghadiya for muhurat planning</h2>
        <p>For starting a new business, signing a contract, travelling, or beginning any important activity, look for an Amrit or Shubh Choghadiya window. Labh and Char are good for routine tasks and travel respectively. Udveg, Kaal, and Rog periods are traditionally avoided for new beginnings — though Kaal Choghadiya is sometimes considered good for government-related work. The times shift daily based on the weekday and the length of the day.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Choghadiya vs Rahu Kaal — what's the difference?</h2>
        <p>Rahu Kaal is a single fixed inauspicious window each day determined by the weekday, whereas Choghadiya provides a full table of all eight time segments with their qualities. Choghadiya gives you a more granular picture — you can see not just when to avoid activity but also which specific windows in the day are especially powerful for different types of work.</p>
      </div>
    </div>
  );
}

function PanchangFestivalsSEOContent() {
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Hindu Festivals and the Vedic Calendar</h2>
        <p>Hindu festivals are not fixed to the Gregorian calendar — they are computed from Tithi, Nakshatra, and planetary positions each year. This is why Holi, Diwali, Janmashtami, and Rama Navami fall on different Gregorian dates every year. Our festival dates are calculated directly from Vedic astronomy using the Swiss Ephemeris for maximum accuracy.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Vrats (fasting days) in the Hindu calendar</h2>
        <p>Vrats are days of fasting or observance tied to specific Tithis. Ekadashi Vrat (11th Tithi of each fortnight, 24 times per year) is the most widely observed. Pradosh Vrat falls on the 13th Tithi and is dedicated to Shiva. Satyanarayan Vrat is typically observed on Purnima or Ekadashi. Mondays (Somvar Vrat) are sacred to Shiva. Observing these days with intention is said to accelerate spiritual progress and remove karmic obstacles.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Major Hindu festivals and their Panchang basis</h2>
        <p><strong className="text-foreground">Diwali</strong> falls on Amavasya of Kartika month. <strong className="text-foreground">Holi</strong> is celebrated on Purnima of Phalguna. <strong className="text-foreground">Janmashtami</strong> occurs on Ashtami Krishna Paksha of Shravana. <strong className="text-foreground">Rama Navami</strong> is on Navami Shukla Paksha of Chaitra. <strong className="text-foreground">Maha Shivaratri</strong> falls on Chaturdashi Krishna Paksha of Magha or Phalguna.</p>
      </div>
    </div>
  );
}

function PanchangCalendarSEOContent({ calYear, calMonth }) {
  const monthName = MONTH_NAMES[(calMonth || 1) - 1];
  const year = calYear || new Date().getFullYear();
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Hindu Panchang Calendar — {monthName} {year}</h2>
        <p>This month view shows the Tithi for every day of {monthName} {year}, along with festivals and Vedic observances. Each date is a direct link to the full Panchang for that day — including Nakshatra, Yoga, Karana, Rahu Kaal, and all timing windows. Tap any date to access its complete Panchang details.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">How to read the Panchang Calendar</h2>
        <p>Each cell shows the Tithi name for that day (calculated at sunrise). A gold dot indicates a festival or Vrat observance. Dates shown in gold are today. The calendar follows the Amanta lunar month system (month ends on Amavasya), which is the standard used across most of India outside Bengal and some northern states.</p>
      </div>
    </div>
  );
}

function PanchangDateSEOContent({ panchangData }) {
  if (!panchangData?.panchang) return null;
  const { tithi, nakshatra, yoga, karana, paksha, lunar_month, sun_sign, moon_sign } = panchangData.panchang;
  const { sunrise, sunset } = panchangData.summary || {};
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Full Panchang Details</h2>
        <p>On this day, the Tithi is <strong className="text-foreground">{tithi.name}</strong> in <strong className="text-foreground">{paksha} Paksha</strong> of <strong className="text-foreground">{lunar_month}</strong> month. The Moon is transiting <strong className="text-foreground">{nakshatra.name}</strong> Nakshatra in <strong className="text-foreground">{moon_sign}</strong> Rashi, while the Sun is placed in <strong className="text-foreground">{sun_sign}</strong>. Yoga for the day is <strong className="text-foreground">{yoga.name}</strong>, and Karana is <strong className="text-foreground">{karana.name}</strong>.</p>
        {sunrise && sunset && <p className="mt-2">Sunrise: <strong className="text-foreground">{sunrise}</strong> &nbsp;·&nbsp; Sunset: <strong className="text-foreground">{sunset}</strong> (IST, New Delhi).</p>}
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">About {tithi.name} Tithi</h2>
        <p>{tithi.name} is a {paksha === 'Shukla' ? 'waxing (Shukla Paksha)' : 'waning (Krishna Paksha)'} Tithi. {paksha === 'Shukla' ? 'Shukla Paksha Tithis are generally considered auspicious for new beginnings, ceremonies, and growth-oriented activities.' : 'Krishna Paksha Tithis are associated with completion, reflection, and ancestral rites.'} The quality of activities undertaken aligns with the energy of this Tithi according to Vedic tradition.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">About {nakshatra.name} Nakshatra</h2>
        <p>The Moon in {nakshatra.name} shapes the emotional quality of this day. Each of the 27 Nakshatras carries a distinct deity, symbol, and set of qualities that influence the nature of any activity begun under them. Checking the Nakshatra before muhurat selection is a fundamental step in Vedic Panchang.</p>
      </div>
    </div>
  );
}

// ─── views ─────────────────────────────────────────────────────────────────

function PanchangDailyView({ dayOffset = 0, onDataLoad }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true); setError(null); setData(null);
    const params = dayOffset === 1 ? { date: getTomorrowIST() } : {};
    axios.get(`${API}/daily`, { params })
      .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
      .catch(() => setError('Failed to load Panchang data. Please try again.'))
      .finally(() => setLoading(false));
  }, [dayOffset]); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) return <div className="space-y-4">{[...Array(5)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (error) return <p className="text-center text-muted-foreground py-12">{error}</p>;
  if (!data) return null;

  const { summary, panchang, day_quality_windows, observances } = data;
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between px-6 py-4 bg-gold/5 border border-gold/20 rounded-xl">
        <div className="flex items-center gap-3">
          <Sun className="h-5 w-5 text-gold" />
          <span className="font-playfair font-semibold text-lg">{formatDate(data.date + 'T00:00:00')}</span>
        </div>
        <span className="text-xs text-muted-foreground">{data.location?.label || 'New Delhi, India'}</span>
      </div>
      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">Panch Anga — Five Limbs</p>
        </div>
        <div className="divide-y divide-border">
          {[
            { label: 'Tithi',      value: panchang.tithi.name,     sub: panchang.paksha + ' Paksha' + (panchang.tithi.end ? ' · until ' + formatTime(panchang.tithi.end) : '') },
            { label: 'Nakshatra',  value: panchang.nakshatra.name, sub: 'Moon in ' + panchang.moon_sign + (panchang.nakshatra.end ? ' · until ' + formatTime(panchang.nakshatra.end) : '') },
            { label: 'Yoga',       value: panchang.yoga.name,      sub: panchang.yoga.end ? 'Until ' + formatTime(panchang.yoga.end) : '' },
            { label: 'Karana',     value: panchang.karana.name,    sub: panchang.karana.end ? 'Until ' + formatTime(panchang.karana.end) : '' },
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
      <div className="grid grid-cols-2 gap-3">
        <Card className="p-4 border border-gold/20 text-center">
          <Sun className="h-5 w-5 text-amber-500 mx-auto mb-2" />
          <p className="text-xs text-muted-foreground uppercase tracking-wide">Sunrise</p>
          <p className="font-semibold text-lg">{summary.sunrise}</p>
          <p className="text-xs text-muted-foreground mt-1">Sun in {panchang.sun_sign}</p>
        </Card>
        <Card className="p-4 border border-gold/20 text-center">
          <Moon className="h-5 w-5 text-blue-400 mx-auto mb-2" />
          <p className="text-xs text-muted-foreground uppercase tracking-wide">Sunset</p>
          <p className="font-semibold text-lg">{summary.sunset}</p>
          <p className="text-xs text-muted-foreground mt-1">Moon in {panchang.moon_sign}</p>
        </Card>
      </div>
      {day_quality_windows?.length > 0 && (
        <Card className="border border-gold/20 overflow-hidden">
          <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
            <p className="text-xs font-semibold uppercase tracking-widest text-gold">Timing Windows</p>
          </div>
          <div className="divide-y divide-border">
            {day_quality_windows.map(w => (
              <div key={w.label} className="flex items-center justify-between px-5 py-3">
                <div className="flex items-center gap-3">
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${(QUALITY_STYLES[w.quality] || QUALITY_STYLES.neutral).badge}`}>{w.quality}</span>
                  <span className="text-sm font-medium">{w.label}</span>
                </div>
                <span className="text-xs text-muted-foreground">{formatTime(w.start)} — {formatTime(w.end)}</span>
              </div>
            ))}
          </div>
        </Card>
      )}
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

function PanchangTithiView() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    axios.get(`${API}/daily`).then(r => setData(r.data)).catch(() => setData(null)).finally(() => setLoading(false));
  }, []);
  if (loading) return <div className="space-y-4">{[...Array(3)].map((_, i) => <div key={i} className="h-20 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (!data) return <p className="text-center text-muted-foreground py-12">Failed to load Tithi data</p>;
  const { panchang, summary } = data;
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
            <p className="text-sm text-muted-foreground border-t border-border pt-3">
              Ends at <span className="font-semibold text-foreground">{formatTime(panchang.tithi.end)}</span>
            </p>
          )}
        </div>
      </Card>
      <Card className="border border-gold/20 p-5">
        <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">Moon Position</p>
        <div className="grid grid-cols-2 gap-4">
          <div><p className="text-xs text-muted-foreground">Moon Sign</p><p className="font-semibold">{panchang.moon_sign}</p></div>
          <div><p className="text-xs text-muted-foreground">Nakshatra</p><p className="font-semibold">{panchang.nakshatra.name}</p></div>
          <div><p className="text-xs text-muted-foreground">Weekday</p><p className="font-semibold">{summary.weekday}</p></div>
          <div><p className="text-xs text-muted-foreground">Samvat</p><p className="font-semibold text-xs">{panchang.samvat}</p></div>
        </div>
      </Card>
      <PanchangTithiSEOContent />
    </div>
  );
}

function PanchangChoghadiyaView() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    axios.get(`${API}/daily`).then(r => setData(r.data)).catch(() => setData(null)).finally(() => setLoading(false));
  }, []);
  if (loading) return <div className="space-y-3">{[...Array(8)].map((_, i) => <div key={i} className="h-12 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (!data) return <p className="text-center text-muted-foreground py-12">Failed to load Choghadiya data</p>;
  const windows = data.day_quality_windows || [];
  const now = new Date();
  return (
    <div className="space-y-4">
      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">Today's Choghadiya</p>
        </div>
        {windows.length === 0
          ? <p className="text-center text-muted-foreground py-8">No timing data available for today</p>
          : <div className="divide-y divide-border">
              {windows.map((w, i) => {
                const isCurrent = now >= new Date(w.start) && now <= new Date(w.end);
                return (
                  <div key={i} className={`flex items-center justify-between px-5 py-3 ${isCurrent ? 'bg-gold/5' : ''}`}>
                    <div className="flex items-center gap-3">
                      {isCurrent && <span className="w-2 h-2 rounded-full bg-green-500 flex-shrink-0" />}
                      <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${(QUALITY_STYLES[w.quality] || QUALITY_STYLES.neutral).badge}`}>{w.quality}</span>
                      <span className="text-sm font-medium">{w.label}</span>
                      {isCurrent && <span className="text-xs text-green-600 font-semibold">Current</span>}
                    </div>
                    <span className="text-xs text-muted-foreground">{formatTime(w.start)} — {formatTime(w.end)}</span>
                  </div>
                );
              })}
            </div>
        }
      </Card>
      <p className="text-xs text-muted-foreground text-center">Times shown in IST (Indian Standard Time)</p>
      <PanchangChoghadiyaSEOContent />
    </div>
  );
}

function PanchangCalendarView({ year, month }) {
  const navigate = useNavigate();
  const today = new Date();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    setLoading(true); setData(null);
    axios.get(`${API}/calendar/${year}/${month}`).then(r => setData(r.data)).catch(() => setData(null)).finally(() => setLoading(false));
  }, [year, month]);
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

function PanchangFestivalsView({ onDataLoad }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const year = new Date().getFullYear();
  useEffect(() => {
    axios.get(`${API}/festivals?year=${year}`)
      .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [year]); // eslint-disable-line react-hooks/exhaustive-deps
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

function PanchangDateView({ dateStr, onDataLoad }) {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    setLoading(true); setError(null); setData(null);
    // Use the dedicated /date/{date} endpoint (CODEX requirement)
    axios.get(`${API}/date/${dateStr}`)
      .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
      .catch(() => {
        // Fallback to /daily?date= if dedicated endpoint not yet deployed
        axios.get(`${API}/daily`, { params: { date: dateStr } })
          .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
          .catch(() => setError('Failed to load Panchang data.'))
          .finally(() => setLoading(false));
      })
      .finally(() => setLoading(false));
  }, [dateStr]); // eslint-disable-line react-hooks/exhaustive-deps
  if (loading) return <div className="space-y-4">{[...Array(5)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (error) return <p className="text-center text-muted-foreground py-12">{error}</p>;
  if (!data) return null;
  const { summary, panchang, day_quality_windows, observances } = data;
  const [y, mo] = dateStr.split('-');
  return (
    <div className="space-y-6">
      <button onClick={() => navigate(`/panchang/calendar/${y}/${parseInt(mo)}`)} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-gold transition-colors">
        <ChevronLeft className="h-4 w-4" /> Back to Calendar
      </button>
      <div className="flex items-center justify-between px-6 py-4 bg-gold/5 border border-gold/20 rounded-xl">
        <div className="flex items-center gap-3">
          <Sun className="h-5 w-5 text-gold" />
          <span className="font-playfair font-semibold text-lg">{formatDate(data.date + 'T00:00:00')}</span>
        </div>
        <span className="text-xs text-muted-foreground">{data.location?.label || 'New Delhi, India'}</span>
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
      <div className="grid grid-cols-2 gap-3">
        <Card className="p-4 border border-gold/20 text-center">
          <Sun className="h-5 w-5 text-amber-500 mx-auto mb-2" />
          <p className="text-xs text-muted-foreground uppercase tracking-wide">Sunrise</p>
          <p className="font-semibold text-lg">{summary.sunrise}</p>
        </Card>
        <Card className="p-4 border border-gold/20 text-center">
          <Moon className="h-5 w-5 text-blue-400 mx-auto mb-2" />
          <p className="text-xs text-muted-foreground uppercase tracking-wide">Sunset</p>
          <p className="font-semibold text-lg">{summary.sunset}</p>
        </Card>
      </div>
      {day_quality_windows?.length > 0 && (
        <Card className="border border-gold/20 overflow-hidden">
          <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
            <p className="text-xs font-semibold uppercase tracking-widest text-gold">Timing Windows</p>
          </div>
          <div className="divide-y divide-border">
            {day_quality_windows.map(w => (
              <div key={w.label} className="flex items-center justify-between px-5 py-3">
                <div className="flex items-center gap-3">
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${(QUALITY_STYLES[w.quality] || QUALITY_STYLES.neutral).badge}`}>{w.quality}</span>
                  <span className="text-sm font-medium">{w.label}</span>
                </div>
                <span className="text-xs text-muted-foreground">{formatTime(w.start)} — {formatTime(w.end)}</span>
              </div>
            ))}
          </div>
        </Card>
      )}
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
      <PanchangDateSEOContent panchangData={data} />
    </div>
  );
}

// ─── main page ─────────────────────────────────────────────────────────────

export const PanchangPage = () => {
  const { type: rawType = 'daily', year: yearParam, month: monthParam, dateValue } = useParams();
  const resolvedType = ALIAS[rawType] || rawType;
  const isCalendar = resolvedType === 'calendar' || (yearParam && monthParam && !dateValue);
  const isDateView = !!dateValue;
  const activeView = isDateView ? 'date' : isCalendar ? 'calendar' : (resolvedType || 'daily');
  const today = new Date();
  const calYear  = parseInt(yearParam)  || today.getFullYear();
  const calMonth = parseInt(monthParam) || (today.getMonth() + 1);

  const [festivalData, setFestivalData] = useState(null);
  const [panchangData, setPanchangData] = useState(null);

  useEffect(() => {
    setFestivalData(null);
    setPanchangData(null);
  }, [activeView, dateValue, calYear, calMonth]);

  const config = isDateView
    ? { title: 'Panchang Details', icon: Calendar, desc: 'Complete Vedic almanac for the selected date' }
    : (TYPE_META[activeView] || TYPE_META.daily);

  const subNavItems = [
    { key: 'daily',       label: 'Today',      icon: Sun,      path: '/panchang/today' },
    { key: 'tomorrow',    label: 'Tomorrow',   icon: Sun,      path: '/panchang/tomorrow' },
    { key: 'tithi',       label: 'Tithi',      icon: Moon,     path: '/panchang/tithi' },
    { key: 'choghadiya',  label: 'Choghadiya', icon: Zap,      path: '/panchang/choghadiya' },
    { key: 'calendar',    label: 'Calendar',   icon: Calendar, path: `/panchang/calendar/${today.getFullYear()}/${today.getMonth() + 1}` },
    { key: 'festivals',   label: 'Festivals',  icon: Sparkles, path: '/panchang/festivals' },
  ];

  const subNavActive = activeView === 'date' ? 'calendar' : activeView;

  return (
    <div className="max-w-3xl mx-auto px-4 py-10 pb-24 lg:pb-10">
      <PanchangSEO
        view={activeView}
        calYear={calYear}
        calMonth={calMonth}
        dateValue={dateValue}
        festivalData={festivalData}
        panchangData={panchangData}
      />
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
          <Calendar className="h-3 w-3" /> Vedic Panchang
        </div>
        <h1 className="text-3xl font-playfair font-semibold mb-2">{config.title}</h1>
        <p className="text-muted-foreground">{config.desc}</p>
      </div>
      <div className="flex flex-wrap gap-2 mb-8 border-b border-border pb-4">
        {subNavItems.map(({ key, label, icon: Icon, path }) => (
          <Link key={key} to={path} className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-colors ${subNavActive === key ? 'bg-gold text-white' : 'border border-border text-muted-foreground hover:border-gold/50 hover:text-gold'}`}>
            <Icon className="h-3 w-3" />{label}
          </Link>
        ))}
      </div>
      {isDateView                                 && <PanchangDateView     dateStr={dateValue}                  onDataLoad={setPanchangData} />}
      {!isDateView && activeView === 'daily'      && <PanchangDailyView    dayOffset={0}                        onDataLoad={setPanchangData} />}
      {!isDateView && activeView === 'tomorrow'   && <PanchangDailyView    dayOffset={1}                        onDataLoad={setPanchangData} />}
      {!isDateView && activeView === 'tithi'      && <PanchangTithiView />}
      {!isDateView && activeView === 'choghadiya' && <PanchangChoghadiyaView />}
      {!isDateView && activeView === 'calendar'   && <PanchangCalendarView year={calYear} month={calMonth} />}
      {!isDateView && activeView === 'festivals'  && <PanchangFestivalsView                                    onDataLoad={setFestivalData} />}
    </div>
  );
};
