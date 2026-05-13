import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Sun, Coins, Heart, Baby, Activity, Briefcase, Home,
  Shield, Clock, Sparkles, BookOpen, Globe, Star, Wind,
  Gem, ArrowLeft, Copy, Check, Loader2,
} from 'lucide-react';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import SharedBirthCityPicker from '../components/SharedBirthCityPicker';

const API_BASE = `${process.env.REACT_APP_BACKEND_URL}/api/remedies/dana`;

const TILE_ICONS = {
  sun: Sun, coins: Coins, heart: Heart, baby: Baby,
  activity: Activity, briefcase: Briefcase, home: Home,
  shield: Shield, clock: Clock, sparkles: Sparkles,
  book: BookOpen, globe: Globe, star: Star, wind: Wind, gem: Gem,
};

const SEVERITY_BADGE = {
  High:   'bg-red-500/15 text-red-400 border border-red-400/30',
  Medium: 'bg-amber-500/15 text-amber-400 border border-amber-400/30',
  Low:    'bg-emerald-500/15 text-emerald-400 border border-emerald-400/30',
};

function CopyBtn({ text }) {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    });
  };
  return (
    <button onClick={copy} className="ml-2 text-gold/60 hover:text-gold transition">
      {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
    </button>
  );
}

function ChartPanel({ lagna, chartSummary }) {
  return (
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 mb-6">
      <p className="text-[10px] uppercase tracking-widest text-gold/60 mb-3">
        Birth Chart · Ascendant: {lagna}
      </p>
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr className="text-muted-foreground/60">
              <th className="text-left pb-2 font-medium pr-4">Planet</th>
              <th className="text-left pb-2 font-medium pr-4">Sign</th>
              <th className="text-left pb-2 font-medium pr-4">House</th>
              <th className="text-left pb-2 font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            {chartSummary.map(p => (
              <tr key={p.planet} className="border-t border-gold/10">
                <td className="py-1.5 font-medium pr-4">{p.planet}</td>
                <td className="py-1.5 text-muted-foreground pr-4">{p.sign}</td>
                <td className="py-1.5 text-muted-foreground pr-4">H{p.house}</td>
                <td className="py-1.5 text-muted-foreground/70">
                  {p.retrograde && <span className="text-amber-400 mr-1">℞</span>}
                  {p.dignity && <span className="text-[9px]">{p.dignity}</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function DanaCard({ rule }) {
  const r = rule.remedy || {};
  const sev = r.severity || '';
  return (
    <Card className="rounded-2xl border-gold/20 bg-gold/[0.03] p-5 shadow-none flex flex-col gap-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-widest text-gold/60 mb-0.5">Dana Remedy</p>
          <h3 className="font-playfair text-xl font-semibold text-foreground">{r.remedy_area}</h3>
        </div>
        {sev && (
          <span className={`text-xs font-semibold px-2.5 py-1 rounded-full shrink-0 ${SEVERITY_BADGE[sev] || 'bg-gold/10 text-gold border border-gold/20'}`}>
            {sev}
          </span>
        )}
      </div>

      <div className="grid grid-cols-2 gap-3">
        {r.deity && (
          <div className="rounded-xl border border-gold/15 bg-background/60 px-3 py-2.5">
            <p className="text-[10px] uppercase tracking-wider text-muted-foreground mb-0.5">Deity</p>
            <p className="text-sm font-semibold text-foreground">{r.deity}</p>
          </div>
        )}
        {r.yantra && (
          <div className="rounded-xl border border-gold/15 bg-background/60 px-3 py-2.5">
            <p className="text-[10px] uppercase tracking-wider text-muted-foreground mb-0.5">Yantra</p>
            <p className="text-sm font-semibold text-foreground">{r.yantra}</p>
          </div>
        )}
      </div>

      {r.mantra && (
        <div className="rounded-xl border border-gold/20 bg-gold/[0.06] px-4 py-3">
          <p className="text-[10px] uppercase tracking-wider text-gold/70 mb-1">Mantra</p>
          <div className="flex items-center">
            <p className="text-sm font-medium text-foreground italic flex-1">{r.mantra}</p>
            <CopyBtn text={r.mantra} />
          </div>
        </div>
      )}

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
        {[
          { label: 'Paksha',   value: r.paksha },
          { label: 'Timing',   value: r.tithi_day || r.muhurta },
          { label: 'Season',   value: r.season },
          { label: 'Duration', value: r.frequency },
          { label: 'Attire',   value: r.attire_color },
          { label: 'Muhurta',  value: r.muhurta },
        ].filter(f => f.value).map(f => (
          <div key={f.label} className="rounded-lg border border-gold/10 bg-background/50 px-2.5 py-2">
            <p className="text-[9px] uppercase tracking-wider text-muted-foreground mb-0.5">{f.label}</p>
            <p className="text-foreground font-medium leading-tight">{f.value}</p>
          </div>
        ))}
      </div>

      {r.donation_item && (
        <div className="rounded-xl border border-amber-400/20 bg-amber-400/[0.05] px-4 py-3">
          <p className="text-[10px] uppercase tracking-wider text-amber-400/80 mb-1">Donation Item</p>
          <p className="text-sm text-foreground">{r.donation_item}</p>
        </div>
      )}

      {r.process_direction && (
        <div className="text-sm text-muted-foreground leading-relaxed border-l-2 border-gold/20 pl-3">
          {r.process_direction}
        </div>
      )}

      {r.guidance && (
        <div className="flex items-start gap-2 text-xs text-muted-foreground/80">
          <Sparkles className="h-3.5 w-3.5 text-gold/50 mt-0.5 shrink-0" />
          <span>{r.guidance}</span>
        </div>
      )}

      {r.trigger_birth_chart && (
        <div className="text-[11px] text-muted-foreground/60 border-t border-gold/10 pt-3">
          <span className="text-gold/50">Trigger: </span>{r.trigger_birth_chart}
        </div>
      )}
    </Card>
  );
}

export default function DanaRemediesPage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [view, setView]           = useState('tiles');   // tiles | form | report
  const [tiles, setTiles]         = useState([]);
  const [tilesLoading, setTilesLoading] = useState(true);
  const [focus, setFocus]         = useState(null);
  const [form, setForm]           = useState({ date_of_birth: '', time_of_birth: '', city_name: 'New Delhi', city_slug: 'new-delhi', timezone_offset: '+05:30' });
  const [report, setReport]       = useState(null);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    axios.get(`${API_BASE}/tiles`)
      .then(r => setTiles(r.data.tiles || []))
      .catch(() => toast.error('Could not load focus areas'))
      .finally(() => setTilesLoading(false));
  }, []);

  const selectFocus = (tile) => {
    if (!user) { navigate('/login'); return; }
    setFocus(tile);
    setView('form');
  };

  const handleGenerate = async () => {
    if (!form.date_of_birth) { toast.error('Date of birth is required'); return; }
    setGenerating(true);
    try {
      const res = await axios.post(`${API_BASE}/generate-report`, {
        focus_area: focus.focus,
        date_of_birth: form.date_of_birth,
        time_of_birth: form.time_of_birth || '12:00',
        place_of_birth: form.city_name,
        timezone_offset: form.timezone_offset,
      });
      setReport(res.data);
      setView('report');
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Report generation failed');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <SEO
        title="Dana Remedies Report — Vedic Charity Remedies | EverydayHoroscope"
        description="Get a personalised Dana (charity) remedy report based on your birth chart. Deity, mantra, yantra, timing and donation guidance."
        url="https://www.everydayhoroscope.in/dana-remedies"
      />

      {/* Header */}
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6 mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-3 py-1.5 rounded-full mb-4">
          <Gem className="h-3 w-3" /> Dana Remedies
        </div>
        <h1 className="font-playfair text-3xl font-semibold mb-2">Dana (Charity) Remedy Report</h1>
        <p className="text-muted-foreground text-sm max-w-xl">
          Select your concern area, enter your birth details, and receive a personalised chart-based Dana remedy prescription.
        </p>
      </div>

      {/* ── TILES VIEW ── */}
      {view === 'tiles' && (
        <div>
          <p className="text-xs uppercase tracking-widest text-muted-foreground mb-4">Select Focus Area</p>
          {tilesLoading ? (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {Array.from({ length: 9 }).map((_, i) => (
                <div key={i} className="h-20 rounded-xl border border-gold/10 bg-gold/[0.03] animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {tiles.map(tile => {
                const Icon = TILE_ICONS[tile.icon] || Gem;
                return (
                  <button
                    key={tile.focus}
                    onClick={() => selectFocus(tile)}
                    className="rounded-xl border border-gold/20 bg-gold/[0.03] hover:bg-gold/[0.08] hover:border-gold/40 transition-all p-4 text-left group"
                  >
                    <Icon className="h-5 w-5 text-gold mb-2" />
                    <p className="text-sm font-medium text-foreground leading-tight">{tile.focus}</p>
                    {tile.count > 0 && (
                      <p className="text-[11px] text-muted-foreground/60 mt-1">{tile.count} remedy{tile.count > 1 ? 'ies' : ''}</p>
                    )}
                  </button>
                );
              })}
            </div>
          )}
          {!user && (
            <p className="text-center text-sm text-muted-foreground mt-6">
              <button onClick={() => navigate('/login')} className="text-gold underline">Sign in</button> to generate your report
            </p>
          )}
        </div>
      )}

      {/* ── FORM VIEW ── */}
      {view === 'form' && focus && (
        <div>
          <button onClick={() => setView('tiles')} className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition mb-5">
            <ArrowLeft className="h-4 w-4" /> All focus areas
          </button>

          <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5 mb-6">
            <p className="text-xs uppercase tracking-widest text-gold/60 mb-0.5">Selected Focus</p>
            <p className="font-playfair text-xl font-semibold">{focus.focus}</p>
          </div>

          <div className="rounded-xl border border-border p-6 space-y-5">
            <h2 className="font-semibold">Enter Your Birth Details</h2>

            <div>
              <label className="block text-sm font-medium mb-1.5">Date of Birth <span className="text-red-400">*</span></label>
              <input
                type="date"
                value={form.date_of_birth}
                onChange={e => setForm(f => ({ ...f, date_of_birth: e.target.value }))}
                className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1.5">
                Time of Birth <span className="text-muted-foreground text-xs font-normal">(improves accuracy)</span>
              </label>
              <input
                type="time"
                value={form.time_of_birth}
                onChange={e => setForm(f => ({ ...f, time_of_birth: e.target.value }))}
                className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40"
              />
            </div>

            <SharedBirthCityPicker
              inputId="dana-birth-city"
              label="Place of Birth"
              value={form.city_slug}
              onChange={city => setForm(f => ({
                ...f,
                city_name: city.city_name,
                city_slug: city.slug,
                timezone_offset: city.timezone_offset || '+05:30',
              }))}
            />

            <button
              onClick={handleGenerate}
              disabled={!form.date_of_birth || generating}
              className="w-full bg-gold text-background font-semibold rounded-lg px-4 py-3 flex items-center justify-center gap-2 disabled:opacity-40 transition"
            >
              {generating
                ? <><Loader2 className="h-4 w-4 animate-spin" /> Generating Report...</>
                : <><Sparkles className="h-4 w-4" /> Generate Remedy Report</>
              }
            </button>
          </div>
        </div>
      )}

      {/* ── REPORT VIEW ── */}
      {view === 'report' && report && (
        <div>
          <button onClick={() => setView('form')} className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition mb-5">
            <ArrowLeft className="h-4 w-4" /> Edit Details
          </button>

          <div className="flex items-center justify-between mb-6">
            <h2 className="font-playfair text-2xl font-semibold">{report.focus} — Remedy Report</h2>
            <span className="text-xs text-muted-foreground">{report.count} prescriptions</span>
          </div>

          <ChartPanel lagna={report.lagna} chartSummary={report.chart_summary || []} />

          {report.count === 0 ? (
            <div className="text-center py-16 text-muted-foreground">No remedies found for this focus area.</div>
          ) : (
            <div className="grid gap-5">
              {report.rules.map((rule, i) => <DanaCard key={rule.rule_id || i} rule={rule} />)}
            </div>
          )}

          <button
            onClick={() => { setFocus(null); setReport(null); setView('tiles'); }}
            className="mt-8 w-full border border-gold/30 text-gold rounded-lg px-4 py-2.5 text-sm hover:bg-gold/5 transition"
          >
            Generate Another Report
          </button>
        </div>
      )}

      {/* ── On-page SEO content ──────────────────────────────────────────── */}
      <div className="mt-12 space-y-8 border-t border-border pt-10 text-sm text-muted-foreground">
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">What is Dana in Vedic Astrology?</h2>
          <p className="leading-7">Dana (दान — charitable giving) is one of the most powerful karmic remedies in Vedic astrology. The principle is rooted in the law of karma: planets afflicting specific houses indicate a karmic debt in that domain, and targeted charitable acts toward the significations of that planet discharge the debt. Dana is not random generosity — it is precise, planet-specific giving, prescribed based on the exact nature and placement of the afflicting planet in your birth chart.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Planetary Dana Prescriptions</h2>
          <p className="leading-7">Each planet has specific items, colours, metals, grains, and recipients associated with it. Sun Dana: wheat, jaggery, copper — offered on Sundays. Moon Dana: rice, milk, silver — on Mondays. Mars: red lentils, copper, land — Tuesdays. Mercury: green dal, books — Wednesdays. Jupiter: yellow items, gold, education — Thursdays. Venus: white sweets, silk, cows — Fridays. Saturn: black sesame, iron, oil — Saturdays. Rahu: blue or black items — Saturdays. Ketu: multi-coloured items, blankets.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">How Dana Works Karmically</h2>
          <p className="leading-7">Dana neutralises planetary afflictions by enacting the opposite of the karma that created the debt. A debilitated Saturn (indicating past neglect of the poor or elderly) is pacified by consistent giving to labourers or the underprivileged. An afflicted Jupiter (indicating past disrespect of teachers or scripture) is softened by supporting education or brahmins. The key is sincerity and consistency — mechanical giving without awareness produces minimal effect.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Timing Your Dana</h2>
          <p className="leading-7">The most effective Dana is given on the planet's ruling weekday, during the planet's hora (planetary hour), and during the planet's Dasha or Antardasha period. Giving Saturn Dana during a Saturn Mahadasha, on a Saturday, during Saturn's hora compounds the remedial power significantly. EverydayHoroscope's Dana reports factor in your current Dasha period when prioritising which planetary Danas to prescribe.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Dana vs Ritual Remedies</h2>
          <p className="leading-7">Dana (charity) works at the karmic/social level — it discharges debt through giving to others. Ritual remedies (puja, homa) work at the energetic/devotional level — they propitiate the planetary deity directly. Mantra works at the vibrational level — it aligns the mind with the planet's frequency. Gemstones work at the electromagnetic level — amplifying the planet's energy field. All four types are complementary; Dana is often prescribed alongside one other modality for maximum effect.</p>
        </div>
      </div>
    </div>
  );
}
