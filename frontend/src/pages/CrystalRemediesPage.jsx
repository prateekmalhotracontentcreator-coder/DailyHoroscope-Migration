import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ArrowLeft, Copy, Check, Zap, Sparkles, CheckCircle, Loader2 } from 'lucide-react';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import SharedBirthCityPicker from '../components/SharedBirthCityPicker';

const API_BASE = `${process.env.REACT_APP_BACKEND_URL}/api/remedies/crystals`;

const TILE_ICONS_MAP = {
  'Psychic Shield': '🛡️', 'Clarity': '💎', 'Love': '💗',
  'Protection': '🔮', 'Abundance': '✨', 'Healing': '🌿',
  'Grounding': '🪨', 'Intuition': '👁️', 'Calm': '🌊',
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

function CrystalCard({ rule }) {
  const r = rule.remedy || {};
  const sev = r.severity || '';
  const synergy = r.synergy_grid || [];

  return (
    <Card className="rounded-2xl border-gold/20 bg-gold/[0.03] p-5 shadow-none flex flex-col gap-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-widest text-gold/60 mb-0.5">Crystal Remedy</p>
          <h3 className="font-playfair text-xl font-semibold">{r.remedy_area || r.crystal_name}</h3>
          {r.crystal_name && r.remedy_area && (
            <p className="text-sm text-muted-foreground mt-0.5">{r.crystal_name}</p>
          )}
        </div>
        {sev && (
          <span className={`text-xs font-semibold px-2.5 py-1 rounded-full shrink-0 ${SEVERITY_BADGE[sev] || 'bg-gold/10 text-gold border border-gold/20'}`}>
            {sev}
          </span>
        )}
      </div>

      <div className="grid grid-cols-2 gap-2 text-xs">
        {[
          { label: 'Form',      value: r.form },
          { label: 'Chakra',    value: r.primary_chakra },
          { label: 'Start Day', value: r.start_day },
          { label: 'Recharge',  value: r.recharge_freq },
          { label: 'Placement', value: r.placement },
          { label: 'Tattva',    value: r.tattva_imbalance },
        ].filter(f => f.value).map(f => (
          <div key={f.label} className="rounded-lg border border-gold/10 bg-background/50 px-2.5 py-2">
            <p className="text-[9px] uppercase tracking-wider text-muted-foreground mb-0.5">{f.label}</p>
            <p className="font-medium text-foreground leading-tight">{f.value}</p>
          </div>
        ))}
      </div>

      {r.programming_mantra && (
        <div className="rounded-xl border border-gold/20 bg-gold/[0.06] px-4 py-3">
          <p className="text-[10px] uppercase tracking-wider text-gold/70 mb-1">Programming Mantra</p>
          <div className="flex items-center">
            <p className="text-sm font-medium italic flex-1">{r.programming_mantra}</p>
            <CopyBtn text={r.programming_mantra} />
          </div>
        </div>
      )}

      {r.cleansing && (
        <div className="rounded-xl border border-blue-400/15 bg-blue-400/[0.04] px-4 py-3">
          <p className="text-[10px] uppercase tracking-wider text-blue-400/70 mb-1">Cleansing</p>
          <p className="text-sm text-muted-foreground">{r.cleansing}</p>
        </div>
      )}

      {synergy.length > 0 && (
        <div className="rounded-xl border border-emerald-400/20 bg-emerald-400/[0.04] px-3 py-2.5">
          <div className="flex items-center gap-1 mb-2">
            <CheckCircle className="h-3 w-3 text-emerald-400" />
            <p className="text-[10px] uppercase tracking-wider text-emerald-400/80">Synergy Crystals</p>
          </div>
          {synergy.map(s => (
            <span key={s} className="inline-block text-xs bg-emerald-400/10 text-emerald-400 rounded-full px-2 py-0.5 mr-1 mb-1">{s}</span>
          ))}
        </div>
      )}

      {r.care && (
        <div className="text-sm text-muted-foreground leading-relaxed border-l-2 border-gold/20 pl-3">{r.care}</div>
      )}

      {r.dos_donts && (
        <div className="flex items-start gap-2 text-xs text-muted-foreground/80">
          <Sparkles className="h-3.5 w-3.5 text-gold/50 mt-0.5 shrink-0" />
          <span>{r.dos_donts}</span>
        </div>
      )}

      {r.guidance && (
        <div className="flex items-start gap-2 text-xs text-muted-foreground/80">
          <Zap className="h-3.5 w-3.5 text-gold/50 mt-0.5 shrink-0" />
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

export default function CrystalRemediesPage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [view, setView]             = useState('tiles');
  const [tiles, setTiles]           = useState([]);
  const [tilesLoading, setTilesLoading] = useState(true);
  const [focus, setFocus]           = useState(null);
  const [form, setForm]             = useState({ date_of_birth: '', time_of_birth: '', city_name: 'New Delhi', city_slug: 'new-delhi', timezone_offset: '+05:30' });
  const [report, setReport]         = useState(null);
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
        title="Crystal Therapy Report — Vedic Crystal Remedies | EverydayHoroscope"
        description="Get a personalised crystal therapy report based on your birth chart. Programming mantras, placement, cleansing protocols and synergy guide."
        url="https://www.everydayhoroscope.in/crystal-therapy"
      />

      {/* Header */}
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6 mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-3 py-1.5 rounded-full mb-4">
          <Zap className="h-3 w-3" /> Crystal Therapy
        </div>
        <h1 className="font-playfair text-3xl font-semibold mb-2">Crystal Therapy Report</h1>
        <p className="text-muted-foreground text-sm max-w-xl">
          Select your healing intention, enter birth details, and receive a chart-based crystal prescription with programming mantra, placement, and synergy guide.
        </p>
      </div>

      {/* ── TILES VIEW ── */}
      {view === 'tiles' && (
        <div>
          <p className="text-xs uppercase tracking-widest text-muted-foreground mb-4">Select Healing Intention</p>
          {tilesLoading ? (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {Array.from({ length: 9 }).map((_, i) => (
                <div key={i} className="h-20 rounded-xl border border-gold/10 bg-gold/[0.03] animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {tiles.map(tile => {
                const emoji = TILE_ICONS_MAP[tile.focus] || '💎';
                return (
                  <button
                    key={tile.focus}
                    onClick={() => selectFocus(tile)}
                    className="rounded-xl border border-gold/20 bg-gold/[0.03] hover:bg-gold/[0.08] hover:border-gold/40 transition-all p-4 text-left"
                  >
                    <span className="text-2xl mb-2 block">{emoji}</span>
                    <p className="text-sm font-medium text-foreground leading-tight">{tile.focus}</p>
                    {tile.count > 0 && (
                      <p className="text-[11px] text-muted-foreground/60 mt-1">{tile.count} crystal{tile.count > 1 ? 's' : ''}</p>
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
            <ArrowLeft className="h-4 w-4" /> All intentions
          </button>

          <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5 mb-6">
            <div className="flex items-center gap-3">
              <span className="text-3xl">{TILE_ICONS_MAP[focus.focus] || '💎'}</span>
              <p className="font-playfair text-xl font-semibold">{focus.focus}</p>
            </div>
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
              inputId="crystal-birth-city"
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
                : <><Sparkles className="h-4 w-4" /> Generate Crystal Report</>
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
            <h2 className="font-playfair text-2xl font-semibold">{focus.focus} — Crystal Report</h2>
            <span className="text-xs text-muted-foreground">{report.count} crystals</span>
          </div>

          <ChartPanel lagna={report.lagna} chartSummary={report.chart_summary || []} />

          {report.count === 0 ? (
            <div className="text-center py-16 text-muted-foreground">No crystal remedies found for this focus.</div>
          ) : (
            <div className="grid gap-5">
              {report.rules.map((rule, i) => <CrystalCard key={rule.rule_id || i} rule={rule} />)}
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
          <h2 className="mb-2 text-base font-semibold text-foreground">What is Crystal Therapy?</h2>
          <p className="leading-7">Crystal therapy uses the natural vibrational frequency of mineral crystals to harmonise the body's energy field. Unlike Vedic gemstones (which amplify specific planetary energies through direct skin contact), crystals work more broadly on the auric field — they absorb, transmit, and modulate subtle electromagnetic energies. In the Vedic context, crystals are used alongside classical remedies as an accessible, lower-intensity energy tool — particularly effective for emotional clearing, environmental harmony, and chakra balancing.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Crystals vs Vedic Gemstones</h2>
          <p className="leading-7">The key distinction: Vedic gemstones (ruby, sapphire, emerald) are prescribed by Jyotish for specific planetary amplification — their effect is potent, targeted, and can be adverse if wrongly prescribed. Crystals are gentler, work on the auric/emotional field, and carry far less risk. Crystals are appropriate for everyone regardless of chart; gemstones require individual Vedic prescription. Many practitioners use crystals for daily energy maintenance and Jyotish gemstones for long-term planetary correction simultaneously.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Common Crystal Prescriptions by Planet</h2>
          <p className="leading-7">Sun: Sunstone, Citrine, Amber — vitality and clarity. Moon: Moonstone, Selenite, Pearl — emotional balance. Mars: Red Jasper, Carnelian — courage and energy. Mercury: Green Aventurine, Fluorite — clarity and communication. Jupiter: Amethyst, Lapis Lazuli — wisdom and abundance. Venus: Rose Quartz, Rhodonite — love and harmony. Saturn: Black Tourmaline, Obsidian — grounding and protection. Rahu: Labradorite, Smoky Quartz — intuition and shadow work. Ketu: Charoite, Lepidolite — spiritual insight and detachment.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Cleansing & Charging Crystals</h2>
          <p className="leading-7">Crystals absorb environmental energy and require regular cleansing — especially after emotional sessions, illness in the home, or high-stress periods. Cleansing methods: running water (for non-water-soluble stones), sunlight or moonlight (full moon light is particularly effective), burying in earth overnight, smudging with sage or frankincense, or sound cleansing with a singing bowl. After cleansing, set a clear intention to charge the crystal. Never cleanse selenite, malachite, or halite in water — they dissolve.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Using Crystals for Planetary Balance</h2>
          <p className="leading-7">EverydayHoroscope prescribes crystals based on your active Dasha lord and the planets most in need of support in your current chart cycle. During a Saturn Mahadasha, Black Tourmaline and Obsidian help ground and protect against Saturn's tendency toward isolation and depression. During a Rahu period, Labradorite and Smoky Quartz assist with the confusion and illusion Rahu can create. Crystal prescriptions are updated each time you generate a new report, reflecting your evolving planetary weather.</p>
        </div>
      </div>
    </div>
  );
}
