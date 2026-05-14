import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ArrowLeft, Copy, Check, BookOpen, Sparkles, Loader2 } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Card } from '../../components/ui/card';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import SharedBirthCityPicker from '../../components/SharedBirthCityPicker';

const API_BASE = `${process.env.REACT_APP_BACKEND_URL}/api/remedies/mantras`;

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
    <button onClick={copy} className="ml-2 text-gold/60 hover:text-gold transition" title="Copy">
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

function MantraCard({ rule }) {
  const r = rule.remedy || {};
  const sev = r.severity || '';

  return (
    <Card className="rounded-2xl border-gold/20 bg-gold/[0.03] p-5 shadow-none flex flex-col gap-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-widest text-gold/60 mb-0.5">Mantra Remedy</p>
          <h3 className="font-playfair text-xl font-semibold">{r.remedy_area}</h3>
          {r.deity && <p className="text-sm text-muted-foreground mt-0.5">Deity: {r.deity}</p>}
        </div>
        {sev && (
          <span className={`text-xs font-semibold px-2.5 py-1 rounded-full shrink-0 ${SEVERITY_BADGE[sev] || 'bg-gold/10 text-gold border border-gold/20'}`}>
            {sev}
          </span>
        )}
      </div>

      {r.mantra_devanagari && (
        <div className="rounded-xl border border-gold/25 bg-gold/[0.07] px-4 py-4 text-center">
          <p className="text-[10px] uppercase tracking-wider text-gold/60 mb-2">Mantra (Sanskrit)</p>
          <div className="flex items-center justify-center">
            <p className="font-playfair text-lg leading-relaxed text-foreground">{r.mantra_devanagari}</p>
            <CopyBtn text={r.mantra_devanagari} />
          </div>
        </div>
      )}

      {r.mantra_transliteration && (
        <div className="rounded-xl border border-gold/15 bg-background/50 px-4 py-3">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground mb-1">Transliteration</p>
          <div className="flex items-center">
            <p className="text-sm italic text-muted-foreground flex-1">{r.mantra_transliteration}</p>
            <CopyBtn text={r.mantra_transliteration} />
          </div>
        </div>
      )}

      {r.yantra && (
        <div className="rounded-xl border border-gold/15 bg-background/60 px-3 py-2.5">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground mb-0.5">Yantra</p>
          <p className="text-sm font-semibold">{r.yantra}</p>
        </div>
      )}

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
        {[
          { label: 'Paksha',   value: r.paksha },
          { label: 'Timing',   value: r.tithi_day || r.muhurta },
          { label: 'Season',   value: r.season },
          { label: 'Duration', value: r.frequency },
          { label: 'Attire',   value: r.attire_color },
          { label: 'Count',    value: r.japa_count },
        ].filter(f => f.value).map(f => (
          <div key={f.label} className="rounded-lg border border-gold/10 bg-background/50 px-2.5 py-2">
            <p className="text-[9px] uppercase tracking-wider text-muted-foreground mb-0.5">{f.label}</p>
            <p className="font-medium text-foreground leading-tight">{f.value}</p>
          </div>
        ))}
      </div>

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

export default function MantraRemediesPage() {
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
      .catch(() => toast.error('Could not load mantra categories'))
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
        title="Mantra Remedy Report — Vedic Mantras & Yantras | EverydayHoroscope"
        description="Get a personalised Vedic mantra remedy report based on your birth chart. Sanskrit text, transliteration, yantra, and complete japa protocol."
        url="https://www.everydayhoroscope.in/mantra-remedies"
      />

      {/* Header */}
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6 mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-3 py-1.5 rounded-full mb-4">
          <BookOpen className="h-3 w-3" /> Mantra Remedies
        </div>
        <h1 className="font-playfair text-3xl font-semibold mb-2">Mantra & Yantra Remedy Report</h1>
        <p className="text-muted-foreground text-sm max-w-xl">
          Select your planetary concern, enter birth details, and receive a chart-based mantra prescription with Sanskrit text, yantra, and complete japa protocol.
        </p>
      </div>

      {/* ── TILES VIEW ── */}
      {view === 'tiles' && (
        <div>
          <p className="text-xs uppercase tracking-widest text-muted-foreground mb-4">Select Concern Area</p>
          {tilesLoading ? (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {Array.from({ length: 9 }).map((_, i) => (
                <div key={i} className="h-20 rounded-xl border border-gold/10 bg-gold/[0.03] animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {tiles.map(tile => (
                <button
                  key={tile.focus}
                  onClick={() => selectFocus(tile)}
                  className="rounded-xl border border-gold/20 bg-gold/[0.03] hover:bg-gold/[0.08] hover:border-gold/40 transition-all p-4 text-left"
                >
                  <BookOpen className="h-5 w-5 text-gold mb-2" />
                  <p className="text-sm font-medium text-foreground leading-tight">{tile.focus}</p>
                  {tile.count > 0 && (
                    <p className="text-[11px] text-muted-foreground/60 mt-1">{tile.count} mantra{tile.count > 1 ? 's' : ''}</p>
                  )}
                </button>
              ))}
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
            <ArrowLeft className="h-4 w-4" /> All categories
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
              inputId="mantra-birth-city"
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
                : <><Sparkles className="h-4 w-4" /> Generate Mantra Report</>
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
            <h2 className="font-playfair text-2xl font-semibold">{report.focus} — Mantra Report</h2>
            <span className="text-xs text-muted-foreground">{report.count} mantra{report.count !== 1 ? 's' : ''}</span>
          </div>

          <ChartPanel lagna={report.lagna} chartSummary={report.chart_summary || []} />

          {report.count === 0 ? (
            <div className="text-center py-16 text-muted-foreground">No mantras found for this category.</div>
          ) : (
            <div className="grid gap-5">
              {report.rules.map((rule, i) => <MantraCard key={rule.rule_id || i} rule={rule} />)}
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
          <h2 className="mb-2 text-base font-semibold text-foreground">What is Mantra in Vedic Tradition?</h2>
          <p className="leading-7">Mantra (मंत्र) is Sanskrit sound — a precisely structured syllabic formula whose vibration, when correctly articulated and repeated, produces measurable effects on consciousness, the subtle body, and the environment. The word derives from "manas" (mind) + "tra" (instrument/protection) — a mantra is literally a tool of the mind. In Vedic astrology, planetary mantras are prescribed to propitiate a specific planet, align the mind with that planet's highest frequency, and gradually dissolve the karmic patterns encoded in its placement in your birth chart.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">How Mantra Works — Sound & Vibration</h2>
          <p className="leading-7">Sanskrit is a phonetically precise language designed so that the sound of the syllable mirrors the thing it names. Planetary mantras work through three mechanisms: (1) vibrational resonance — the mantra's frequency matches the planet's cosmic signature; (2) neurological imprinting — repetition creates new neural pathways that override habitual reactive patterns; (3) devotional intent — the practitioner's sincerity activates the mantra beyond its mechanical sound. All three must be present; mechanical repetition without awareness produces minimal effect.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">108 Repetitions — Why 108?</h2>
          <p className="leading-7">108 is the sacred number of Vedic tradition: the ratio of the Sun's diameter to its distance from Earth is approximately 108; the ratio of the Moon's distance to its diameter is also approximately 108. There are 108 Upanishads, 108 names of major deities, and 108 beads on a japa mala (rosary). Neurologically, 108 repetitions of a mantra at a steady pace takes approximately 10–15 minutes — long enough to shift brainwave state from beta to alpha and engage the parasympathetic system. The number is not arbitrary; it is mathematically embedded in the cosmos.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Planetary Mantras — the Nine</h2>
          <p className="leading-7">The nine planetary Beej (seed) mantras: Sun — "Om Hraam Hreem Hraum Sah Suryaya Namah"; Moon — "Om Shraam Shreem Shraum Sah Chandraaya Namah"; Mars — "Om Kraam Kreem Kraum Sah Bhaumaaya Namah"; Mercury — "Om Braam Breem Braum Sah Budhaaya Namah"; Jupiter — "Om Graam Greem Graum Sah Gurave Namah"; Venus — "Om Draam Dreem Draum Sah Shukraaya Namah"; Saturn — "Om Praam Preem Praum Sah Shanaischaraaya Namah"; Rahu — "Om Bhraam Bhreem Bhraum Sah Raahave Namah"; Ketu — "Om Straam Streem Straum Sah Ketave Namah".</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Building a Daily Japa Practice</h2>
          <p className="leading-7">Begin with one planetary mantra prescribed for your chart — the Dasha lord or the most afflicted planet. Use a japa mala (108 beads) and chant at Brahma Muhurta (pre-dawn) or at sunrise. Start with 1 mala (108 repetitions) daily; build to 3 malas (324) for deeper effect; 11 malas daily for 40 days is considered a full mantra purashcharana (completion ritual). Maintain a clean body and space, sit facing east, and keep the intent one-pointed. EverydayHoroscope's Mantra library includes pronunciation guides, meaning, and recommended count for each planetary mantra.</p>
        </div>
      </div>
    </div>
  );
}
