import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { Calendar, Sun, Moon, Star, Shield, Zap, Sparkles, ChevronLeft, ChevronRight, ExternalLink } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/panchang`;

const QUALITY_STYLES = {
  good:    { bg: 'bg-green-50 border-green-200', label: 'text-green-700', badge: 'bg-green-100 text-green-800' },
  neutral: { bg: 'bg-amber-50 border-amber-200', label: 'text-amber-700', badge: 'bg-amber-100 text-amber-800' },
  caution: { bg: 'bg-red-50 border-red-200',    label: 'text-red-700',   badge: 'bg-red-100 text-red-800' },
};

const TYPE_META = {
  daily:    { title: "Today's Panchang",    icon: Sun,      desc: 'Complete Vedic almanac — Tithi, Nakshatra, Yoga, Karana, Sunrise & Sunset' },
  calendar: { title: 'Panchang Calendar',   icon: Calendar, desc: 'Monthly Hindu calendar with Tithi and observances' },
  festivals:{ title: 'Festivals & Vrats',   icon: Sparkles, desc: 'Upcoming Hindu festivals and vrat dates' },
};

function formatTime(isoString) {
  if (!isoString) return '--';
  try {
    return new Date(isoString).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true, timeZone: 'Asia/Kolkata' });
  } catch { return isoString.slice(11, 16); }
}

function formatDate(isoString) {
  if (!isoString) return '';
  try {
    return new Date(isoString).toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Asia/Kolkata' });
  } catch { return isoString; }
}

function PanchangDailyView() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${API}/daily`)
      .then(r => setData(r.data))
      .catch(() => setError('Failed to load Panchang data'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div className="space-y-4">
      {[...Array(5)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}
    </div>
  );

  if (error) return <p className="text-center text-muted-foreground py-12">{error}</p>;
  if (!data) return null;

  const { summary, panchang, day_quality_windows, observances } = data;

  return (
    <div className="space-y-6">
      {/* Date header */}
      <div className="flex items-center justify-between px-6 py-4 bg-gold/5 border border-gold/20 rounded-xl">
        <div className="flex items-center gap-3">
          <Sun className="h-5 w-5 text-gold" />
          <span className="font-playfair font-semibold text-lg">{formatDate(data.date + 'T00:00:00')}</span>
        </div>
        <span className="text-xs text-muted-foreground">{data.location.label}</span>
      </div>

      {/* Core 5 limbs */}
      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">Panch Anga — Five Limbs</p>
        </div>
        <div className="divide-y divide-border">
          {[
            { label: 'Tithi', value: panchang.tithi.name, sub: panchang.paksha + ' Paksha' + (panchang.tithi.end ? ' · until ' + formatTime(panchang.tithi.end) : '') },
            { label: 'Nakshatra', value: panchang.nakshatra.name, sub: 'Moon in ' + panchang.moon_sign + (panchang.nakshatra.end ? ' · until ' + formatTime(panchang.nakshatra.end) : '') },
            { label: 'Yoga', value: panchang.yoga.name, sub: panchang.yoga.end ? 'Until ' + formatTime(panchang.yoga.end) : '' },
            { label: 'Karana', value: panchang.karana.name, sub: panchang.karana.end ? 'Until ' + formatTime(panchang.karana.end) : '' },
            { label: 'Vara (Day)', value: summary.weekday, sub: panchang.samvat },
          ].map(item => (
            <div key={item.label} className="flex items-center justify-between px-5 py-4">
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-wide mb-0.5">{item.label}</p>
                <p className="font-medium text-sm">{item.value}</p>
              </div>
              {item.sub && <p className="text-xs text-muted-foreground text-right max-w-[180px]">{item.sub}</p>}
            </div>
          ))}
        </div>
      </Card>

      {/* Sun times + Signs */}
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

      {/* Day quality windows */}
      {day_quality_windows.length > 0 && (
        <Card className="border border-gold/20 overflow-hidden">
          <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
            <p className="text-xs font-semibold uppercase tracking-widest text-gold">Timing Windows</p>
          </div>
          <div className="divide-y divide-border">
            {day_quality_windows.map(w => {
              const style = QUALITY_STYLES[w.quality] || QUALITY_STYLES.neutral;
              return (
                <div key={w.label} className="flex items-center justify-between px-5 py-3">
                  <div className="flex items-center gap-3">
                    <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${style.badge}`}>{w.quality}</span>
                    <span className="text-sm font-medium">{w.label}</span>
                  </div>
                  <span className="text-xs text-muted-foreground">{formatTime(w.start)} — {formatTime(w.end)}</span>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {/* Observances */}
      {observances.length > 0 && (
        <Card className="border border-gold/20 p-5">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">Today’s Observances</p>
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

      {/* Nav links */}
      <div className="flex gap-3">
        <Link to={`/panchang/calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}`}
          className="flex-1 flex items-center justify-center gap-2 py-3 border border-gold/30 rounded-xl text-sm font-medium text-gold hover:bg-gold/5 transition-colors">
          <Calendar className="h-4 w-4" /> Monthly Calendar
        </Link>
        <Link to="/panchang/festivals"
          className="flex-1 flex items-center justify-center gap-2 py-3 border border-gold/30 rounded-xl text-sm font-medium text-gold hover:bg-gold/5 transition-colors">
          <Sparkles className="h-4 w-4" /> Festivals & Vrats
        </Link>
      </div>
    </div>
  );
}

function PanchangCalendarView() {
  const { year: yearParam, month: monthParam } = useParams();
  const navigate = useNavigate();
  const today = new Date();
  const year = parseInt(yearParam) || today.getFullYear();
  const month = parseInt(monthParam) || (today.getMonth() + 1);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    axios.get(`${API}/calendar/${year}/${month}`)
      .then(r => setData(r.data))
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [year, month]);

  const prevMonth = month === 1 ? { y: year - 1, m: 12 } : { y: year, m: month - 1 };
  const nextMonth = month === 12 ? { y: year + 1, m: 1 } : { y: year, m: month + 1 };

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <button onClick={() => navigate(`/panchang/calendar/${prevMonth.y}/${prevMonth.m}`)} className="p-2 hover:bg-gold/10 rounded-lg transition-colors">
          <ChevronLeft className="h-5 w-5 text-gold" />
        </button>
        <h2 className="font-playfair font-semibold text-xl">{data?.month_label || `${year}`}</h2>
        <button onClick={() => navigate(`/panchang/calendar/${nextMonth.y}/${nextMonth.m}`)} className="p-2 hover:bg-gold/10 rounded-lg transition-colors">
          <ChevronRight className="h-5 w-5 text-gold" />
        </button>
      </div>

      {loading ? (
        <div className="grid grid-cols-7 gap-1">
          {[...Array(35)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}
        </div>
      ) : data ? (
        <div className="space-y-1">
          <div className="grid grid-cols-7 gap-1 mb-2">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(d => (
              <div key={d} className="text-center text-xs font-semibold text-muted-foreground py-1">{d}</div>
            ))}
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
                  const isToday = day.date === today.toISOString().slice(0, 10);
                  const hasObservance = day.observances.length > 0;
                  return (
                    <div key={day.date} className={`p-1.5 rounded-lg border text-center cursor-pointer hover:border-gold/40 transition-colors ${ isToday ? 'border-gold bg-gold/10' : 'border-border' }`}>
                      <p className={`text-sm font-semibold ${isToday ? 'text-gold' : ''}`}>{day.day}</p>
                      <p className="text-[9px] text-muted-foreground leading-tight mt-0.5 truncate">{day.tithi.split(' ')[1] || day.tithi}</p>
                      {hasObservance && <div className="w-1 h-1 bg-gold rounded-full mx-auto mt-1" />}
                    </div>
                  );
                })}
              </div>
            ));
          })()}
        </div>
      ) : <p className="text-center text-muted-foreground py-12">Failed to load calendar</p>}
    </div>
  );
}

function PanchangFestivalsView() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const year = new Date().getFullYear();

  useEffect(() => {
    axios.get(`${API}/festivals?year=${year}`)
      .then(r => setData(r.data))
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [year]);

  if (loading) return <div className="space-y-3">{[...Array(8)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (!data?.items?.length) return <p className="text-center text-muted-foreground py-12">No festivals found</p>;

  const grouped = data.items.reduce((acc, item) => {
    const month = item.date.slice(0, 7);
    if (!acc[month]) acc[month] = [];
    acc[month].push(item);
    return acc;
  }, {});

  return (
    <div className="space-y-6">
      {Object.entries(grouped).map(([month, items]) => (
        <div key={month}>
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">
            {new Date(month + '-01').toLocaleDateString('en-IN', { month: 'long', year: 'numeric' })}
          </p>
          <div className="space-y-2">
            {items.map(item => (
              <div key={item.slug + item.date} className="flex items-start gap-4 p-4 border border-gold/20 rounded-xl bg-gold/5">
                <div className="text-center min-w-[40px]">
                  <p className="text-xl font-playfair font-bold text-gold">{new Date(item.date + 'T00:00:00').getDate()}</p>
                  <p className="text-[10px] text-muted-foreground uppercase">{new Date(item.date + 'T00:00:00').toLocaleDateString('en-IN', { weekday: 'short' })}</p>
                </div>
                <div>
                  <span className={`text-[10px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full ${ item.observance_type === 'festival' ? 'bg-amber-100 text-amber-800' : item.observance_type === 'vrat' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800' }`}>{item.observance_type}</span>
                  <p className="font-semibold text-sm mt-1">{item.name}</p>
                  <p className="text-xs text-muted-foreground">{item.summary}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export const PanchangPage = () => {
  const { type = 'daily' } = useParams();
  const config = TYPE_META[type] || TYPE_META.daily;
  const Icon = config.icon;

  const getSchema = () => ({
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: config.title + ' \u2014 Everyday Horoscope',
    description: config.desc + ' Powered by Vedic astronomy for New Delhi, India.',
    url: 'https://everydayhoroscope.in/panchang/' + type,
    publisher: { '@type': 'Organization', name: 'Everyday Horoscope', url: 'https://everydayhoroscope.in' },
    about: { '@type': 'Thing', name: 'Panchang', description: 'Vedic almanac used in Hindu astrology.' },
  });

  return (
    <div className="max-w-3xl mx-auto px-4 py-10 pb-24 lg:pb-10">
      <SEO
        title={config.title + ' \u2014 Everyday Horoscope'}
        description={config.desc + ' Powered by Vedic astronomy for New Delhi, India.'}
        url={'https://everydayhoroscope.in/panchang/' + type}
        schema={getSchema()}
      />

      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
          <Calendar className="h-3 w-3" /> Vedic Panchang
        </div>
        <h1 className="text-3xl font-playfair font-semibold mb-2">{config.title}</h1>
        <p className="text-muted-foreground">{config.desc}</p>
      </div>

      {/* Sub-nav */}
      <div className="flex gap-2 mb-8 border-b border-border pb-4">
        {Object.entries(TYPE_META).map(([key, meta]) => (
          <Link
            key={key}
            to={key === 'calendar' ? `/panchang/calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}` : `/panchang/${key}`}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-colors ${ (type === key || (type === 'calendar' && key === 'calendar')) ? 'bg-gold text-white' : 'border border-border text-muted-foreground hover:border-gold/50 hover:text-gold' }`}
          >
            {key === 'daily' && <Sun className="h-3 w-3" />}
            {key === 'calendar' && <Calendar className="h-3 w-3" />}
            {key === 'festivals' && <Sparkles className="h-3 w-3" />}
            {meta.title.split("'s")[0].replace('Panchang ', '').replace(' & Vrats', '')}
          </Link>
        ))}
      </div>

      {type === 'daily' && <PanchangDailyView />}
      {type === 'calendar' && <PanchangCalendarView />}
      {type === 'festivals' && <PanchangFestivalsView />}
    </div>
  );
};
