import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ArrowLeft, Copy, Check, Gem, Sparkles, AlertTriangle, CheckCircle, Loader2 } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Card } from '../../components/ui/card';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import SharedBirthCityPicker from '../../components/SharedBirthCityPicker';

const API_BASE = `${process.env.REACT_APP_BACKEND_URL}/api/remedies/gemstones`;

const PLANET_COLORS = {
  Sun:     '#e11d48', Moon:    '#94a3b8', Mars:   '#f97316',
  Mercury: '#22c55e', Jupiter: '#eab308', Venus:  '#e879f9',
  Saturn:  '#6366f1', Rahu:    '#a16207', Ketu:   '#71717a',
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

function ChartPanel({ lagna, chartSummary, highlight }) {
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
              <tr key={p.planet} className={`border-t border-gold/10 ${p.planet === highlight ? 'text-gold' : ''}`}>
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

function GemstoneCard({ rule }) {
  const r = rule.remedy || {};
  const sev = r.severity || '';
  const synergy = r.synergy_conflict?.synergy || [];
  const conflict = r.synergy_conflict?.conflict || [];
  const activation = r.activation || {};

  return (
    <Card className="rounded-2xl border-gold/20 bg-gold/[0.03] p-5 shadow-none flex flex-col gap-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-widest text-gold/60 mb-0.5">Gemstone Remedy</p>
          <h3 className="font-playfair text-xl font-semibold">{r.remedy_area || r.primary_gemstone}</h3>
          {r.primary_gemstone && r.remedy_area && (
            <p className="text-sm text-muted-foreground mt-0.5">{r.primary_gemstone}</p>
          )}
        </div>
        {sev && (
          <span className={`text-xs font-semibold px-2.5 py-1 rounded-full shrink-0 ${SEVERITY_BADGE[sev] || 'bg-gold/10 text-gold border border-gold/20'}`}>
            {sev}
          </span>
        )}
      </div>

      {r.metal_finger && (
        <div className="rounded-xl border border-gold/15 bg-background/60 px-4 py-2.5">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground mb-0.5">Metal & Finger</p>
          <p className="text-sm font-semibold">{r.metal_finger}</p>
        </div>
      )}

      {r.wearing_mantra && (
        <div className="rounded-xl border border-gold/20 bg-gold/[0.06] px-4 py-3">
          <p className="text-[10px] uppercase tracking-wider text-gold/70 mb-1">Wearing Mantra</p>
          <div className="flex items-center">
            <p className="text-sm font-medium italic flex-1">{r.wearing_mantra}</p>
            <CopyBtn text={r.wearing_mantra} />
          </div>
        </div>
      )}

      {Object.keys(activation).length > 0 && (
        <div>
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground mb-2">Activation Protocol</p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
            {[
              { label: 'Paksha',  value: activation.paksha },
              { label: 'Day',     value: activation.day },
              { label: 'Tithi',   value: activation.tithi },
              { label: 'Muhurta', value: activation.muhurta },
            ].filter(f => f.value).map(f => (
              <div key={f.label} className="rounded-lg border border-gold/10 bg-background/50 px-2.5 py-2">
                <p className="text-[9px] uppercase tracking-wider text-muted-foreground mb-0.5">{f.label}</p>
                <p className="font-medium text-foreground">{f.value}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {r.purification_process && (
        <div className="rounded-xl border border-blue-400/15 bg-blue-400/[0.04] px-4 py-3">
          <p className="text-[10px] uppercase tracking-wider text-blue-400/70 mb-1">Purification</p>
          <p className="text-sm text-muted-foreground">{r.purification_process}</p>
        </div>
      )}

      {(synergy.length > 0 || conflict.length > 0) && (
        <div className="grid grid-cols-2 gap-3">
          {synergy.length > 0 && (
            <div className="rounded-xl border border-emerald-400/20 bg-emerald-400/[0.04] px-3 py-2.5">
              <div className="flex items-center gap-1 mb-2">
                <CheckCircle className="h-3 w-3 text-emerald-400" />
                <p className="text-[10px] uppercase tracking-wider text-emerald-400/80">Synergy</p>
              </div>
              {synergy.map(s => (
                <span key={s} className="inline-block text-xs bg-emerald-400/10 text-emerald-400 rounded-full px-2 py-0.5 mr-1 mb-1">{s}</span>
              ))}
            </div>
          )}
          {conflict.length > 0 && (
            <div className="rounded-xl border border-red-400/20 bg-red-400/[0.04] px-3 py-2.5">
              <div className="flex items-center gap-1 mb-2">
                <AlertTriangle className="h-3 w-3 text-red-400" />
                <p className="text-[10px] uppercase tracking-wider text-red-400/80">Avoid with</p>
              </div>
              {conflict.map(c => (
                <span key={c} className="inline-block text-xs bg-red-400/10 text-red-400 rounded-full px-2 py-0.5 mr-1 mb-1">{c}</span>
              ))}
            </div>
          )}
        </div>
      )}

      {r.rituals_care && (
        <div className="text-sm text-muted-foreground leading-relaxed border-l-2 border-gold/20 pl-3">
          {r.rituals_care}
        </div>
      )}

      {r.dos_donts && (
        <div className="flex items-start gap-2 text-xs text-muted-foreground/80">
          <Sparkles className="h-3.5 w-3.5 text-gold/50 mt-0.5 shrink-0" />
          <span>{r.dos_donts}</span>
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

export default function GemstoneRemediesPage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [view, setView]             = useState('tiles');
  const [tiles, setTiles]           = useState([]);
  const [tilesLoading, setTilesLoading] = useState(true);
  const [focus, setFocus]           = useState(null); // planet tile object
  const [form, setForm]             = useState({ date_of_birth: '', time_of_birth: '', city_name: 'New Delhi', city_slug: 'new-delhi', timezone_offset: '+05:30' });
  const [report, setReport]         = useState(null);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    axios.get(`${API_BASE}/tiles`)
      .then(r => setTiles(r.data.tiles || []))
      .catch(() => toast.error('Could not load planets'))
      .finally(() => setTilesLoading(false));
  }, []);

  const selectPlanet = (tile) => {
    if (!user) { navigate('/login'); return; }
    setFocus(tile);
    setView('form');
  };

  const handleGenerate = async () => {
    if (!form.date_of_birth) { toast.error('Date of birth is required'); return; }
    setGenerating(true);
    try {
      const res = await axios.post(`${API_BASE}/generate-report`, {
        focus_area: focus.planet,
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
        title="Gemstone Remedy Report — Vedic Ratna Shastra | EverydayHoroscope"
        description="Get a personalised Vedic gemstone remedy report based on your birth chart. Wearing mantra, activation protocol, and full prescription."
        url="https://www.everydayhoroscope.in/gemstone-remedies"
      />

      {/* Header */}
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6 mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-3 py-1.5 rounded-full mb-4">
          <Gem className="h-3 w-3" /> Ratna Shastra
        </div>
        <h1 className="font-playfair text-3xl font-semibold mb-2">Gemstone Remedy Report</h1>
        <p className="text-muted-foreground text-sm max-w-xl">
          Select your planetary ruler, enter birth details, and receive a chart-specific gemstone prescription with full activation protocol.
        </p>
      </div>

      {/* ── TILES VIEW ── */}
      {view === 'tiles' && (
        <div>
          <p className="text-xs uppercase tracking-widest text-muted-foreground mb-4">Select Planetary Ruler</p>
          {tilesLoading ? (
            <div className="grid grid-cols-3 gap-3">
              {Array.from({ length: 9 }).map((_, i) => (
                <div key={i} className="h-24 rounded-xl border border-gold/10 bg-gold/[0.03] animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-3 gap-3">
              {tiles.map(tile => {
                const color = PLANET_COLORS[tile.planet] || '#c5a059';
                return (
                  <button
                    key={tile.planet}
                    onClick={() => selectPlanet(tile)}
                    className="rounded-xl border border-gold/20 bg-gold/[0.03] hover:bg-gold/[0.08] hover:border-gold/40 transition-all p-4 text-left"
                  >
                    <div
                      className="h-8 w-8 rounded-full mb-3 flex items-center justify-center"
                      style={{ backgroundColor: color + '33', border: `1.5px solid ${color}66` }}
                    >
                      <span className="text-sm font-bold" style={{ color }}>{tile.planet[0]}</span>
                    </div>
                    <p className="text-sm font-semibold text-foreground">{tile.planet}</p>
                    <p className="text-xs text-muted-foreground mt-0.5">{tile.gemstone}</p>
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
            <ArrowLeft className="h-4 w-4" /> All planets
          </button>

          <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5 mb-6">
            <div className="flex items-center gap-3">
              <div
                className="h-10 w-10 rounded-full flex items-center justify-center"
                style={{ backgroundColor: (PLANET_COLORS[focus.planet] || '#c5a059') + '33', border: `1.5px solid ${(PLANET_COLORS[focus.planet] || '#c5a059')}66` }}
              >
                <span className="text-base font-bold" style={{ color: PLANET_COLORS[focus.planet] || '#c5a059' }}>{focus.planet[0]}</span>
              </div>
              <div>
                <p className="font-playfair text-xl font-semibold">{focus.planet}</p>
                <p className="text-sm text-muted-foreground">{focus.gemstone}</p>
              </div>
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
              inputId="gem-birth-city"
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
                : <><Sparkles className="h-4 w-4" /> Generate Gemstone Report</>
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
            <div>
              <h2 className="font-playfair text-2xl font-semibold">{focus.planet} — Gemstone Report</h2>
              <p className="text-sm text-muted-foreground">{focus.gemstone}</p>
            </div>
            <span className="text-xs text-muted-foreground">{report.count} prescriptions</span>
          </div>

          <ChartPanel lagna={report.lagna} chartSummary={report.chart_summary || []} highlight={focus.planet} />

          {report.count === 0 ? (
            <div className="text-center py-16 text-muted-foreground">No gemstone prescriptions found for {focus.planet}.</div>
          ) : (
            <div className="grid gap-5">
              {report.rules.map((rule, i) => <GemstoneCard key={rule.rule_id || i} rule={rule} />)}
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
          <h2 className="mb-2 text-base font-semibold text-foreground">What is Vedic Gemstone Therapy?</h2>
          <p className="leading-7">Vedic Gemstone Therapy (Ratna Shastra) is the science of using natural gemstones to amplify, balance, or redirect planetary energies in your birth chart. Each gemstone is the primary stone of a specific planet — Ruby for the Sun, Pearl for Moon, Red Coral for Mars, Emerald for Mercury, Yellow Sapphire for Jupiter, Diamond for Venus, Blue Sapphire for Saturn, Hessonite for Rahu, Cat's Eye for Ketu. When worn correctly, the stone acts as a resonance amplifier for that planet's frequencies.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">How Gemstones Work — Planetary Resonance</h2>
          <p className="leading-7">Vedic astrology understands each planet as emitting a specific spectrum of cosmic light. Gemstones filter and concentrate that spectrum through their crystalline structure — natural gems act as piezoelectric transmitters that, when worn against the skin, interact with the body's bioelectric field. The principle is not metaphorical — it is the same physics underlying quartz oscillators in electronics. The prescribed stone must be natural (not synthetic), flawless, and of sufficient weight (typically 3–5 carats minimum).</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Choosing the Right Gemstone — Critical Rules</h2>
          <p className="leading-7">Never wear a gemstone without proper Vedic analysis. The wrong stone amplifies a malefic planet's harmful influence. The prescription depends on: (1) your Lagna lord and its strength, (2) the planet's functional nature in your specific chart (benefic or malefic), (3) your active Dasha period, and (4) any contraindications between proposed stones. Blue Sapphire (Saturn), for example, produces dramatic results — positive or negative — within days of wearing, making it the most dangerous stone to wear without a proper prescription.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Wearing Protocols — Metal, Finger & Timing</h2>
          <p className="leading-7">Each planetary gemstone has a prescribed metal setting, finger, and activation timing. Ruby: gold, ring finger, Sunday sunrise. Pearl: silver, little finger, Monday. Red Coral: copper or gold, ring finger, Tuesday. Emerald: gold, little finger, Wednesday. Yellow Sapphire: gold, index finger, Thursday. Diamond: platinum or silver, middle or little finger, Friday. Blue Sapphire: silver or panchdhatu, middle finger, Saturday. The stone should be activated (abhishek and mantra) before first wearing.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Primary Stones vs Substitute Stones (Uparatna)</h2>
          <p className="leading-7">Each primary gemstone has less expensive substitutes (Uparatna) that carry similar but gentler energies. Ruby → Red Spinel or Red Garnet. Pearl → Moonstone. Red Coral → Red Jasper. Emerald → Green Tourmaline or Peridot. Yellow Sapphire → Yellow Topaz or Citrine. Diamond → White Zircon or White Sapphire. Blue Sapphire → Amethyst or Blue Spinel. Substitutes are appropriate when the primary stone is unaffordable or when a gentler influence is needed — but they are not equivalent in strength.</p>
        </div>
      </div>
    </div>
  );
}
