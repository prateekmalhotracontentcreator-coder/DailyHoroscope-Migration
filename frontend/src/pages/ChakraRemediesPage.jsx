import React, { useState } from 'react';
import axios from 'axios';
import { Copy, Check, Sparkles, ArrowLeft, Loader2 } from 'lucide-react';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import SharedBirthCityPicker from '../components/SharedBirthCityPicker';

const API_BASE = `${process.env.REACT_APP_BACKEND_URL}/api/remedies/chakra`;

const CHAKRA_META = [
  { name: 'Root (Muladhara)',       color: '#ef4444', num: 1 },
  { name: 'Sacral (Svadhisthana)',  color: '#f97316', num: 2 },
  { name: 'Solar Plexus (Manipura)', color: '#eab308', num: 3 },
  { name: 'Heart (Anahata)',        color: '#22c55e', num: 4 },
  { name: 'Throat (Vishuddha)',     color: '#3b82f6', num: 5 },
  { name: 'Third Eye (Ajna)',       color: '#6366f1', num: 6 },
  { name: 'Crown (Sahasrara)',      color: '#a855f7', num: 7 },
];

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

function ChakraCard({ rule, meta }) {
  const r = rule.remedy || {};
  const color = meta?.color || '#c5a059';

  return (
    <Card className="rounded-2xl border-gold/20 bg-gold/[0.03] p-5 shadow-none flex flex-col gap-4">
      <div className="flex items-center gap-4">
        <div
          className="h-14 w-14 rounded-full flex items-center justify-center shrink-0 font-bold text-lg"
          style={{ backgroundColor: color + '22', border: `2px solid ${color}55` }}
        >
          <span style={{ color }}>{meta?.num || ''}</span>
        </div>
        <div>
          <p className="text-xs uppercase tracking-widest text-gold/60 mb-0.5">Chakra Healing</p>
          <h3 className="font-playfair text-xl font-semibold" style={{ color }}>{r.chakra || rule.condition?.yoga_name}</h3>
          {r.planet && <p className="text-xs text-muted-foreground mt-0.5">Planetary ruler: {r.planet}</p>}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {r.primary_crystal && (
          <div className="rounded-xl border border-gold/15 bg-background/60 px-3 py-2.5">
            <p className="text-[10px] uppercase tracking-wider text-muted-foreground mb-0.5">Primary Crystal</p>
            <p className="text-sm font-semibold">{r.primary_crystal}</p>
          </div>
        )}
        {r.tattva && (
          <div className="rounded-xl border border-gold/15 bg-background/60 px-3 py-2.5">
            <p className="text-[10px] uppercase tracking-wider text-muted-foreground mb-0.5">Tattva</p>
            <p className="text-sm font-semibold">{r.tattva}</p>
          </div>
        )}
      </div>

      {r.bija_mantra && (
        <div
          className="rounded-xl px-4 py-4 text-center"
          style={{ backgroundColor: color + '11', border: `1px solid ${color}33` }}
        >
          <p className="text-[10px] uppercase tracking-wider mb-1" style={{ color: color + 'aa' }}>Bija Mantra</p>
          <div className="flex items-center justify-center">
            <p className="font-playfair text-3xl font-bold" style={{ color }}>{r.bija_mantra}</p>
            <CopyBtn text={r.bija_mantra} />
          </div>
        </div>
      )}

      {r.process && (
        <div className="rounded-xl border border-gold/15 bg-background/50 px-4 py-3">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground mb-2">Healing Process</p>
          <p className="text-sm text-muted-foreground leading-relaxed">{r.process}</p>
        </div>
      )}

      {r.chs_threshold !== undefined && (
        <div className="flex items-start gap-2 text-xs text-muted-foreground/80">
          <Sparkles className="h-3.5 w-3.5 text-gold/50 mt-0.5 shrink-0" />
          <span>Alignment threshold: {r.chs_threshold}% · {r.chs_formula}</span>
        </div>
      )}

      {r.trigger_condition && (
        <div className="text-[11px] text-muted-foreground/60 border-t border-gold/10 pt-3">
          <span className="text-gold/50">Trigger: </span>{r.trigger_condition}
        </div>
      )}
    </Card>
  );
}

export default function ChakraRemediesPage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [view, setView]             = useState('tiles');
  const [focus, setFocus]           = useState(null); // CHAKRA_META item
  const [form, setForm]             = useState({ date_of_birth: '', time_of_birth: '', city_name: 'New Delhi', city_slug: 'new-delhi', timezone_offset: '+05:30' });
  const [report, setReport]         = useState(null);
  const [generating, setGenerating] = useState(false);

  const selectChakra = (meta) => {
    if (!user) { navigate('/login'); return; }
    setFocus(meta);
    setView('form');
  };

  const handleGenerate = async () => {
    if (!form.date_of_birth) { toast.error('Date of birth is required'); return; }
    setGenerating(true);
    try {
      const focusArea = focus.name.split('(')[0].trim(); // e.g. "Root"
      const res = await axios.post(`${API_BASE}/generate-report`, {
        focus_area: focusArea,
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
        title="Chakra Healing Report — 7 Chakra Vedic Remedies | EverydayHoroscope"
        description="Get a personalised 7-chakra healing report based on your birth chart. Bija mantras, crystals, Tattva elements, and complete healing protocol."
        url="https://www.everydayhoroscope.in/chakra-healing"
      />

      {/* Header */}
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6 mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-3 py-1.5 rounded-full mb-4">
          <Sparkles className="h-3 w-3" /> Chakra Healing
        </div>
        <h1 className="font-playfair text-3xl font-semibold mb-2">Chakra Healing Report</h1>
        <p className="text-muted-foreground text-sm max-w-xl">
          Select a chakra, enter your birth details, and receive a chart-based healing prescription with bija mantra, crystal, and process.
        </p>
      </div>

      {/* ── TILES VIEW ── */}
      {view === 'tiles' && (
        <div>
          <p className="text-xs uppercase tracking-widest text-muted-foreground mb-4">Select Chakra</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {CHAKRA_META.map(meta => (
              <button
                key={meta.name}
                onClick={() => selectChakra(meta)}
                className="rounded-xl border border-gold/20 bg-gold/[0.03] hover:bg-gold/[0.08] hover:border-gold/40 transition-all p-4 text-left flex items-center gap-4"
              >
                <div
                  className="h-10 w-10 rounded-full flex items-center justify-center shrink-0 font-bold text-sm"
                  style={{ backgroundColor: meta.color + '33', border: `1.5px solid ${meta.color}66` }}
                >
                  <span style={{ color: meta.color }}>{meta.num}</span>
                </div>
                <p className="text-sm font-medium text-foreground">{meta.name}</p>
              </button>
            ))}
          </div>
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
            <ArrowLeft className="h-4 w-4" /> All chakras
          </button>

          <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5 mb-6 flex items-center gap-4">
            <div
              className="h-12 w-12 rounded-full flex items-center justify-center shrink-0 font-bold text-lg"
              style={{ backgroundColor: focus.color + '33', border: `2px solid ${focus.color}66` }}
            >
              <span style={{ color: focus.color }}>{focus.num}</span>
            </div>
            <div>
              <p className="font-playfair text-xl font-semibold" style={{ color: focus.color }}>{focus.name}</p>
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
              inputId="chakra-birth-city"
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
                : <><Sparkles className="h-4 w-4" /> Generate Chakra Report</>
              }
            </button>
          </div>
        </div>
      )}

      {/* ── REPORT VIEW ── */}
      {view === 'report' && report && focus && (
        <div>
          <button onClick={() => setView('form')} className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition mb-5">
            <ArrowLeft className="h-4 w-4" /> Edit Details
          </button>

          <div className="flex items-center justify-between mb-6">
            <h2 className="font-playfair text-2xl font-semibold" style={{ color: focus.color }}>{focus.name}</h2>
            <span className="text-xs text-muted-foreground">{report.count} prescription{report.count !== 1 ? 's' : ''}</span>
          </div>

          <ChartPanel lagna={report.lagna} chartSummary={report.chart_summary || []} />

          {report.count === 0 ? (
            <div className="text-center py-16 text-muted-foreground">Healing protocol for this chakra is being prepared.</div>
          ) : (
            <div className="grid gap-5">
              {report.rules.map((rule, i) => (
                <ChakraCard
                  key={rule.rule_id || i}
                  rule={rule}
                  meta={focus}
                />
              ))}
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
          <h2 className="mb-2 text-base font-semibold text-foreground">What are the 7 Chakras?</h2>
          <p className="leading-7">Chakras (चक्र — "wheels") are the seven primary energy centres of the subtle body in the Vedic and Tantric tradition, arranged along the spinal axis from the base to the crown. They are: Muladhara (Root — base of spine), Svadhisthana (Sacral — lower abdomen), Manipura (Solar Plexus — navel), Anahata (Heart — centre of chest), Vishuddha (Throat — neck), Ajna (Third Eye — between brows), Sahasrara (Crown — top of head). Each governs specific physical organs, emotional states, and domains of consciousness.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Chakras & Their Vedic Planetary Rulers</h2>
          <p className="leading-7">In Jyotish, each chakra maps to a planetary ruler: Muladhara → Saturn (survival, structure), Svadhisthana → Jupiter (expansion, pleasure), Manipura → Mars (will, power), Anahata → Venus (love, connection), Vishuddha → Mercury (communication, expression), Ajna → Sun/Moon (intuition, perception), Sahasrara → Ketu/all planets (liberation, cosmic consciousness). Planetary afflictions in your birth chart often manifest as blockages in the corresponding chakra — making Jyotish and chakra healing naturally complementary systems.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">How EverydayHoroscope Diagnoses Chakra Imbalance</h2>
          <p className="leading-7">Our system identifies chakra imbalances by cross-referencing your birth chart's planetary afflictions with the chakra-planet mapping. A debilitated or heavily aspected Saturn indicates a likely Root Chakra blockage — manifesting as financial insecurity, fear, and lack of groundedness. An afflicted Venus or Moon points to Heart Chakra deficiency — difficulty with love, self-worth, and emotional intimacy. Each report surfaces the specific chakras requiring attention and the practices most aligned with your current Dasha period.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Chakra Healing Practices</h2>
          <p className="leading-7">Each chakra responds to a specific combination of practices: colour visualisation (each chakra has an associated colour — red for Root through violet for Crown), bija mantras (seed syllables — LAM, VAM, RAM, YAM, HAM, OM, AUM), yoga asanas (poses that activate the associated spinal region), pranayama (breath work for energy movement), and crystal placement on the chakra point during meditation. EverydayHoroscope prescribes the specific combination most relevant to your chart imbalances.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Chakra Healing & Your Dasha Period</h2>
          <p className="leading-7">Chakra blockages intensify during the Dasha of the ruling planet. During a Saturn Mahadasha, Root Chakra work becomes especially critical — grounding practices, earthing, and Muladhara activation can significantly reduce Saturnine anxiety and stagnation. During a Venus Antardasha, Heart Chakra practices (loving-kindness meditation, rose quartz work, anahata pranayama) support the flowering of Venus's gifts. EverydayHoroscope's prescriptions update with your evolving planetary periods.</p>
        </div>
      </div>
    </div>
  );
}
