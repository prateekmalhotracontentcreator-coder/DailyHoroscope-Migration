import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Copy, Check, Sparkles } from 'lucide-react';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { toast } from 'sonner';

const API = `${process.env.REACT_APP_BACKEND_URL}/api/remedies/chakra`;

const CHAKRA_META = [
  { name: 'Root (Muladhara)',       color: '#ef4444', num: 1 },
  { name: 'Sacral (Svadhisthana)',  color: '#f97316', num: 2 },
  { name: 'Solar Plexus (Manipura)','color': '#eab308', num: 3 },
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

function ChakraCard({ rule, meta }) {
  const r = rule.remedy || {};
  const color = meta?.color || '#c5a059';

  return (
    <Card className="rounded-2xl border-gold/20 bg-gold/[0.03] p-5 shadow-none flex flex-col gap-4">
      {/* Chakra circle + name */}
      <div className="flex items-center gap-4">
        <div
          className="h-14 w-14 rounded-full flex items-center justify-center shrink-0 font-bold text-white text-lg"
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

      {/* Primary Crystal + Tattva */}
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

      {/* Bija Mantra */}
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

      {/* Process */}
      {r.process && (
        <div className="rounded-xl border border-gold/15 bg-background/50 px-4 py-3">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground mb-2">Healing Process</p>
          <p className="text-sm text-muted-foreground leading-relaxed">{r.process}</p>
        </div>
      )}

      {/* CHS Threshold */}
      {r.chs_threshold !== undefined && (
        <div className="flex items-start gap-2 text-xs text-muted-foreground/80">
          <Sparkles className="h-3.5 w-3.5 text-gold/50 mt-0.5 shrink-0" />
          <span>Alignment threshold: {r.chs_threshold}% · {r.chs_formula}</span>
        </div>
      )}

      {/* Trigger */}
      {r.trigger_condition && (
        <div className="text-[11px] text-muted-foreground/60 border-t border-gold/10 pt-3">
          <span className="text-gold/50">Trigger: </span>{r.trigger_condition}
        </div>
      )}
    </Card>
  );
}

export default function ChakraRemediesPage() {
  const [allRules, setAllRules] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading]   = useState(true);

  useEffect(() => {
    axios.get(`${API}/all`)
      .then(r => setAllRules(r.data.rules || []))
      .catch(() => toast.error('Could not load chakra remedies'))
      .finally(() => setLoading(false));
  }, []);

  const selectedRule = selected
    ? allRules.find(r => {
        const chakraName = r.remedy?.chakra || r.condition?.yoga_name || '';
        return chakraName.toLowerCase().includes(selected.split('(')[0].trim().toLowerCase());
      })
    : null;

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <SEO
        title="Chakra Healing — 7 Chakra Vedic Remedies | EverydayHoroscope"
        description="7-chakra Vedic healing system with bija mantras, primary crystals, Tattva elements, and alignment protocols."
        url="https://www.everydayhoroscope.in/chakra-healing"
      />

      {/* Header */}
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6 mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-3 py-1.5 rounded-full mb-4">
          <Sparkles className="h-3 w-3" /> Chakra Healing
        </div>
        <h1 className="font-playfair text-3xl font-semibold mb-2">7 Chakra Healing System</h1>
        <p className="text-muted-foreground text-sm max-w-xl">
          Select a chakra to reveal its bija mantra, primary crystal, Tattva element, planetary ruler, and complete healing protocol.
        </p>
      </div>

      {/* Chakra Spine */}
      <div className="flex flex-col sm:flex-row gap-6">
        {/* Left: Chakra selector */}
        <div className="sm:w-56 shrink-0">
          {loading ? (
            <div className="flex flex-col gap-2">
              {Array.from({length: 7}).map((_, i) => (
                <div key={i} className="h-12 rounded-xl border border-gold/10 bg-gold/[0.03] animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="flex flex-col gap-2">
              {CHAKRA_META.map(meta => (
                <button
                  key={meta.name}
                  onClick={() => setSelected(selected === meta.name ? null : meta.name)}
                  className={`rounded-xl border transition-all px-3 py-2.5 text-left flex items-center gap-3 ${
                    selected === meta.name
                      ? 'border-gold/40 bg-gold/[0.08]'
                      : 'border-gold/15 bg-gold/[0.02] hover:bg-gold/[0.06] hover:border-gold/30'
                  }`}
                >
                  <div
                    className="h-5 w-5 rounded-full shrink-0"
                    style={{ backgroundColor: meta.color + '55', border: `1.5px solid ${meta.color}` }}
                  />
                  <span className="text-sm font-medium text-foreground leading-tight">{meta.name.split('(')[0].trim()}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Right: Detail card */}
        <div className="flex-1">
          {!selected && !loading && (
            <div className="flex flex-col items-center justify-center h-full py-16 text-center text-muted-foreground">
              <Sparkles className="h-8 w-8 text-gold/30 mb-3" />
              <p className="text-sm">Select a chakra to view its healing protocol</p>
            </div>
          )}

          {selected && selectedRule && (
            <ChakraCard
              rule={selectedRule}
              meta={CHAKRA_META.find(m => m.name === selected)}
            />
          )}

          {selected && !selectedRule && !loading && (
            <div className="text-center py-16 text-muted-foreground text-sm">
              Healing data for this chakra is being prepared.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
