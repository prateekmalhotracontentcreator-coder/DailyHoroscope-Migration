import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { ArrowLeft, Copy, Check, Zap, Sparkles, CheckCircle } from 'lucide-react';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { toast } from 'sonner';

const API = `${process.env.REACT_APP_BACKEND_URL}/api/remedies/crystals`;

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

function CrystalCard({ rule }) {
  const r = rule.remedy || {};
  const sev = r.severity || '';
  const synergy = r.synergy_grid || [];

  return (
    <Card className="rounded-2xl border-gold/20 bg-gold/[0.03] p-5 shadow-none flex flex-col gap-4">
      {/* Header */}
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

      {/* Crystal details grid */}
      <div className="grid grid-cols-2 gap-2 text-xs">
        {[
          { label: 'Form',         value: r.form },
          { label: 'Chakra',       value: r.primary_chakra },
          { label: 'Start Day',    value: r.start_day },
          { label: 'Recharge',     value: r.recharge_freq },
          { label: 'Placement',    value: r.placement },
          { label: 'Tattva',       value: r.tattva_imbalance },
        ].filter(f => f.value).map(f => (
          <div key={f.label} className="rounded-lg border border-gold/10 bg-background/50 px-2.5 py-2">
            <p className="text-[9px] uppercase tracking-wider text-muted-foreground mb-0.5">{f.label}</p>
            <p className="font-medium text-foreground leading-tight">{f.value}</p>
          </div>
        ))}
      </div>

      {/* Programming Mantra */}
      {r.programming_mantra && (
        <div className="rounded-xl border border-gold/20 bg-gold/[0.06] px-4 py-3">
          <p className="text-[10px] uppercase tracking-wider text-gold/70 mb-1">Programming Mantra</p>
          <div className="flex items-center">
            <p className="text-sm font-medium italic flex-1">{r.programming_mantra}</p>
            <CopyBtn text={r.programming_mantra} />
          </div>
        </div>
      )}

      {/* Cleansing */}
      {r.cleansing && (
        <div className="rounded-xl border border-blue-400/15 bg-blue-400/[0.04] px-4 py-3">
          <p className="text-[10px] uppercase tracking-wider text-blue-400/70 mb-1">Cleansing</p>
          <p className="text-sm text-muted-foreground">{r.cleansing}</p>
        </div>
      )}

      {/* Synergy grid */}
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

      {/* Care */}
      {r.care && (
        <div className="text-sm text-muted-foreground leading-relaxed border-l-2 border-gold/20 pl-3">{r.care}</div>
      )}

      {/* Dos & Don'ts */}
      {r.dos_donts && (
        <div className="flex items-start gap-2 text-xs text-muted-foreground/80">
          <Sparkles className="h-3.5 w-3.5 text-gold/50 mt-0.5 shrink-0" />
          <span>{r.dos_donts}</span>
        </div>
      )}

      {/* Guidance */}
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
  const [tiles, setTiles]       = useState([]);
  const [selected, setSelected] = useState(null);
  const [rules, setRules]       = useState([]);
  const [loading, setLoading]   = useState(false);
  const [tilesLoading, setTilesLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API}/tiles`)
      .then(r => setTiles(r.data.tiles || []))
      .catch(() => toast.error('Could not load focus areas'))
      .finally(() => setTilesLoading(false));
  }, []);

  const selectFocus = useCallback(async (focus) => {
    setSelected(focus);
    setLoading(true);
    setRules([]);
    try {
      const res = await axios.get(`${API}/query`, { params: { focus } });
      setRules(res.data.rules || []);
    } catch {
      toast.error('Could not load crystal remedies');
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <SEO
        title="Crystal Therapy — Vedic Crystal Remedies | EverydayHoroscope"
        description="Vedic crystal healing remedies with programming mantras, synergy grids, placement guidance, and cleansing protocols."
        url="https://www.everydayhoroscope.in/crystal-therapy"
      />

      {/* Header */}
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6 mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-3 py-1.5 rounded-full mb-4">
          <Zap className="h-3 w-3" /> Crystal Therapy
        </div>
        <h1 className="font-playfair text-3xl font-semibold mb-2">Crystal Therapy</h1>
        <p className="text-muted-foreground text-sm max-w-xl">
          Select your healing intention. Each crystal prescription includes the programming mantra, placement, cleansing protocol, synergy grid, and recharge frequency.
        </p>
      </div>

      {/* Tile Grid */}
      {!selected && (
        <div>
          <p className="text-xs uppercase tracking-widest text-muted-foreground mb-4">Select Healing Intention</p>
          {tilesLoading ? (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {Array.from({length: 9}).map((_, i) => (
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
                    onClick={() => selectFocus(tile.focus)}
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
        </div>
      )}

      {/* Results */}
      {selected && (
        <div>
          <button
            onClick={() => { setSelected(null); setRules([]); }}
            className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition mb-5"
          >
            <ArrowLeft className="h-4 w-4" /> All intentions
          </button>

          <div className="flex items-center justify-between mb-6">
            <h2 className="font-playfair text-2xl font-semibold">{selected}</h2>
            {rules.length > 0 && (
              <span className="text-xs text-muted-foreground">{rules.length} crystal{rules.length > 1 ? 's' : ''}</span>
            )}
          </div>

          {loading ? (
            <div className="grid gap-4">
              {Array.from({length: 2}).map((_, i) => (
                <div key={i} className="h-64 rounded-2xl border border-gold/10 bg-gold/[0.03] animate-pulse" />
              ))}
            </div>
          ) : rules.length === 0 ? (
            <div className="text-center py-16 text-muted-foreground">No crystal remedies found for this focus.</div>
          ) : (
            <div className="grid gap-5">
              {rules.map((rule, i) => <CrystalCard key={rule.rule_id || i} rule={rule} />)}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
