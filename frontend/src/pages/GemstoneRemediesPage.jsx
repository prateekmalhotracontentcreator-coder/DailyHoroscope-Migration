import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { ArrowLeft, Copy, Check, Gem, Sparkles, AlertTriangle, CheckCircle } from 'lucide-react';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { toast } from 'sonner';

const API = `${process.env.REACT_APP_BACKEND_URL}/api/remedies/gemstones`;

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

function GemstoneCard({ rule }) {
  const r = rule.remedy || {};
  const sev = r.severity || '';
  const synergy = r.synergy_conflict?.synergy || [];
  const conflict = r.synergy_conflict?.conflict || [];
  const activation = r.activation || {};

  return (
    <Card className="rounded-2xl border-gold/20 bg-gold/[0.03] p-5 shadow-none flex flex-col gap-4">
      {/* Header */}
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

      {/* Metal + Finger */}
      {r.metal_finger && (
        <div className="rounded-xl border border-gold/15 bg-background/60 px-4 py-2.5">
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground mb-0.5">Metal & Finger</p>
          <p className="text-sm font-semibold">{r.metal_finger}</p>
        </div>
      )}

      {/* Wearing Mantra */}
      {r.wearing_mantra && (
        <div className="rounded-xl border border-gold/20 bg-gold/[0.06] px-4 py-3">
          <p className="text-[10px] uppercase tracking-wider text-gold/70 mb-1">Wearing Mantra</p>
          <div className="flex items-center">
            <p className="text-sm font-medium italic flex-1">{r.wearing_mantra}</p>
            <CopyBtn text={r.wearing_mantra} />
          </div>
        </div>
      )}

      {/* Activation */}
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

      {/* Purification */}
      {r.purification_process && (
        <div className="rounded-xl border border-blue-400/15 bg-blue-400/[0.04] px-4 py-3">
          <p className="text-[10px] uppercase tracking-wider text-blue-400/70 mb-1">Purification</p>
          <p className="text-sm text-muted-foreground">{r.purification_process}</p>
        </div>
      )}

      {/* Synergy / Conflict */}
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

      {/* Rituals */}
      {r.rituals_care && (
        <div className="text-sm text-muted-foreground leading-relaxed border-l-2 border-gold/20 pl-3">
          {r.rituals_care}
        </div>
      )}

      {/* Dos & Don'ts */}
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
  const [tiles, setTiles]       = useState([]);
  const [selected, setSelected] = useState(null);
  const [rules, setRules]       = useState([]);
  const [loading, setLoading]   = useState(false);
  const [tilesLoading, setTilesLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API}/tiles`)
      .then(r => setTiles(r.data.tiles || []))
      .catch(() => toast.error('Could not load planets'))
      .finally(() => setTilesLoading(false));
  }, []);

  const selectPlanet = useCallback(async (planet) => {
    setSelected(planet);
    setLoading(true);
    setRules([]);
    try {
      const res = await axios.get(`${API}/query`, { params: { focus: planet } });
      setRules(res.data.rules || []);
    } catch {
      toast.error('Could not load gemstone remedies');
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <SEO
        title="Gemstone Remedies — Vedic Ratna Shastra | EverydayHoroscope"
        description="Discover your personalised Vedic gemstone remedy. Ruby, Pearl, Emerald, and more — with wearing mantra, activation protocol, and synergy guide."
        url="https://www.everydayhoroscope.in/gemstone-remedies"
      />

      {/* Header */}
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6 mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-3 py-1.5 rounded-full mb-4">
          <Gem className="h-3 w-3" /> Ratna Shastra
        </div>
        <h1 className="font-playfair text-3xl font-semibold mb-2">Gemstone Remedies</h1>
        <p className="text-muted-foreground text-sm max-w-xl">
          Select your planetary ruler. Each gemstone prescription includes the wearing mantra, metal, finger placement, activation muhurta, purification protocol, and synergy/conflict guide.
        </p>
      </div>

      {/* Planet Tiles */}
      {!selected && (
        <div>
          <p className="text-xs uppercase tracking-widest text-muted-foreground mb-4">Select Planetary Ruler</p>
          {tilesLoading ? (
            <div className="grid grid-cols-3 sm:grid-cols-3 gap-3">
              {Array.from({length: 9}).map((_, i) => (
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
                    onClick={() => selectPlanet(tile.planet)}
                    className="rounded-xl border border-gold/20 bg-gold/[0.03] hover:bg-gold/[0.08] hover:border-gold/40 transition-all p-4 text-left"
                  >
                    <div
                      className="h-8 w-8 rounded-full mb-3 flex items-center justify-center text-sm font-bold text-white"
                      style={{ backgroundColor: color + '33', border: `1.5px solid ${color}66` }}
                    >
                      <span style={{ color }}>{tile.planet[0]}</span>
                    </div>
                    <p className="text-sm font-semibold text-foreground">{tile.planet}</p>
                    <p className="text-xs text-muted-foreground mt-0.5">{tile.gemstone}</p>
                  </button>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* Results */}
      {selected && (
        <div>
          <button
            onClick={() => { setSelected(null); setRules([]); }}
            className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition mb-5"
          >
            <ArrowLeft className="h-4 w-4" /> All planets
          </button>

          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="font-playfair text-2xl font-semibold">{selected}</h2>
              {tiles.find(t => t.planet === selected)?.gemstone && (
                <p className="text-sm text-muted-foreground">{tiles.find(t => t.planet === selected).gemstone}</p>
              )}
            </div>
            {rules.length > 0 && (
              <span className="text-xs text-muted-foreground">{rules.length} rule{rules.length > 1 ? 's' : ''}</span>
            )}
          </div>

          {loading ? (
            <div className="grid gap-4">
              {Array.from({length: 2}).map((_, i) => (
                <div key={i} className="h-64 rounded-2xl border border-gold/10 bg-gold/[0.03] animate-pulse" />
              ))}
            </div>
          ) : rules.length === 0 ? (
            <div className="text-center py-16 text-muted-foreground">No gemstone remedies found for {selected}.</div>
          ) : (
            <div className="grid gap-5">
              {rules.map((rule, i) => <GemstoneCard key={rule.rule_id || i} rule={rule} />)}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
