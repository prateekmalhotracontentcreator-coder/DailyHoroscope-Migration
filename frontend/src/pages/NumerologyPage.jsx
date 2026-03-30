import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import {
  Hash, Sparkles, ChevronRight, BookOpen, Clock, Heart,
  Briefcase, Home, Baby, Phone, Building2, Star, Bookmark,
  BookmarkCheck, ArrowLeft, AlertCircle, Loader2
} from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const TILE_META = {
  life_path_soul_mission:         { icon: Star,      label: 'Life Path & Soul Mission',             color: 'text-gold' },
  name_correction_energy_alignment: { icon: Sparkles, label: 'Name Correction & Energy Alignment',   color: 'text-purple-400' },
  favorable_timing:               { icon: Clock,     label: 'Favorable Timing',                     color: 'text-blue-400' },
  karmic_debt_loshu:              { icon: AlertCircle,label: 'Karmic Debt & Lo Shu Grid',           color: 'text-red-400' },
  relationship_compatibility:     { icon: Heart,     label: 'Relationship Compatibility',           color: 'text-pink-400' },
  career_guidance:                { icon: Briefcase, label: 'Career Guidance',                      color: 'text-emerald-400' },
  lucky_digital_vibrations:       { icon: Phone,     label: 'Lucky Digital Vibrations',             color: 'text-cyan-400' },
  residential_compatibility:      { icon: Home,      label: 'Residential Compatibility',            color: 'text-orange-400' },
  business_brand_optimization:    { icon: Building2, label: 'Business & Brand Optimization',       color: 'text-yellow-400' },
  baby_name_selection:            { icon: Baby,      label: 'Auspicious Baby Name',                 color: 'text-rose-400' },
  premium_ankjyotish_report:      { icon: Star,      label: 'Premium Ankjyotish Report',            color: 'text-amber-400' },
};


const schema = {
  '@context': 'https://schema.org',
  '@type': 'WebPage',
  name: 'Vedic Numerology Reports — Life Path, Name, Timing & More',
  description: 'Generate personalised Vedic numerology reports. Life Path, Name Correction, Karmic Debt, Relationship Compatibility, Career Guidance and more.',
  url: 'https://everydayhoroscope.in/numerology',
  publisher: { '@type': 'Organization', name: 'Everyday Horoscope', url: 'https://everydayhoroscope.in' },
};

export const NumerologyPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('tiles'); // tiles | generate | report | history
  const [tiles, setTiles] = useState([]);
  const [selectedTile, setSelectedTile] = useState(null);
  const [form, setForm] = useState({
    full_birth_name: '',
    date_of_birth: '',
    current_popular_name: '',
    partner_full_birth_name: '',
    partner_date_of_birth: '',
    digital_identifier: '',
    residential_number: '',
    business_name: '',
    candidate_name: '',
    target_year: new Date().getFullYear(),
    focus_area: 'general',
    numerology_system: 'pythagorean',
    // Ankjyotish premium fields (lagna/moon/nakshatra auto-computed on backend)
    time_of_birth: '',
    place_of_birth: '',
  });
  const [report, setReport] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);

  useEffect(() => {
    fetchTiles();
  }, []);

  useEffect(() => {
    if (activeTab === 'history' && user) fetchHistory();
  }, [activeTab, user]);

  const fetchTiles = async () => {
    try {
      const res = await axios.get(`${API}/numerology/tiles`);
      setTiles(res.data.tiles || []);
    } catch {
      // tiles fallback — use TILE_META keys
      setTiles(Object.keys(TILE_META).map(k => ({ tile_code: k, name: TILE_META[k].label, description: '', is_premium: true })));
    }
  };

  const fetchHistory = async () => {
    setHistoryLoading(true);
    try {
      const res = await axios.get(`${API}/numerology/history`, { withCredentials: true });
      setHistory(res.data.items || []);
    } catch {
      toast.error('Could not load history');
    } finally {
      setHistoryLoading(false);
    }
  };

  const selectTile = (tile) => {
    if (!user) { navigate('/login'); return; }
    setSelectedTile(tile);
    setReport(null);
    setActiveTab('generate');
  };

  const handleGenerate = async () => {
    if (!form.full_birth_name || !form.date_of_birth) {
      toast.error('Full birth name and date of birth are required');
      return;
    }
    setLoading(true);
    try {
      const payload = {
        tile_code: selectedTile.tile_code,
        full_birth_name: form.full_birth_name,
        date_of_birth: form.date_of_birth,
        focus_area: form.focus_area,
        numerology_system: form.numerology_system,
        reduction_method: 'grouping',
        y_mode: 'auto',
      };
      if (form.current_popular_name) payload.current_popular_name = form.current_popular_name;
      if (form.partner_full_birth_name) payload.partner_full_birth_name = form.partner_full_birth_name;
      if (form.partner_date_of_birth) payload.partner_date_of_birth = form.partner_date_of_birth;
      if (form.digital_identifier) payload.digital_identifier = form.digital_identifier;
      if (form.residential_number) payload.residential_number = form.residential_number;
      if (form.business_name) payload.business_name = form.business_name;
      if (form.candidate_name) payload.candidate_name = form.candidate_name;
      if (selectedTile.tile_code === 'favorable_timing') payload.target_year = parseInt(form.target_year);
      // Ankjyotish premium fields — lagna/moon/nakshatra are auto-computed on the backend
      if (form.time_of_birth)  payload.time_of_birth  = form.time_of_birth;
      if (form.place_of_birth) payload.place_of_birth = form.place_of_birth;

      const res = await axios.post(`${API}/numerology/report/generate`, payload, { withCredentials: true });
      setReport(res.data.report);
      setActiveTab('report');
      toast.success('Report generated!');
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Generation failed');
    } finally {
      setLoading(false);
    }
  };

  const toggleBookmark = async (reportId, current) => {
    try {
      await axios.post(`${API}/numerology/history/${reportId}/bookmark`, { bookmarked: !current }, { withCredentials: true });
      if (report?.id === reportId) setReport(r => ({ ...r, bookmarked: !current }));
      setHistory(h => h.map(i => i.id === reportId ? { ...i, bookmarked: !current } : i));
      toast.success(!current ? 'Bookmarked' : 'Removed bookmark');
    } catch {
      toast.error('Could not update bookmark');
    }
  };

  const openHistoryReport = async (id) => {
    try {
      const res = await axios.get(`${API}/numerology/report/${id}`, { withCredentials: true });
      setReport(res.data.report);
      setActiveTab('report');
    } catch {
      toast.error('Could not load report');
    }
  };

  const TileIcon = ({ code }) => {
    const meta = TILE_META[code];
    if (!meta) return <Hash className="h-5 w-5 text-gold" />;
    const I = meta.icon;
    return <I className={`h-5 w-5 ${meta.color}`} />;
  };

  const needsField = (field) => {
    const tc = selectedTile?.tile_code;
    const map = {
      current_popular_name: ['name_correction_energy_alignment'],
      partner_full_birth_name: ['relationship_compatibility'],
      partner_date_of_birth: ['relationship_compatibility'],
      digital_identifier: ['lucky_digital_vibrations'],
      residential_number: ['residential_compatibility'],
      business_name: ['business_brand_optimization'],
      candidate_name: ['baby_name_selection'],
      target_year: ['favorable_timing'],
      time_of_birth:  ['premium_ankjyotish_report'],
      place_of_birth: ['premium_ankjyotish_report'],
    };
    return map[field]?.includes(tc);
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <SEO
        title="Vedic Numerology — Life Path, Name & Timing Reports"
        description="Generate personalised Vedic numerology reports. Life Path, Name Correction, Karmic Debt, Compatibility, Career, and more."
        url="https://everydayhoroscope.in/numerology"
        schema={schema}
      />

      {/* Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
          <Hash className="h-3 w-3" /> Vedic Numerology
        </div>
        <h1 className="text-3xl font-playfair font-semibold mb-2">Numerology Reports</h1>
        <p className="text-muted-foreground">Select a tile, enter your details, and get a personalised numerology reading.</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-border mb-8">
        {[
          { key: 'tiles', label: 'Select Report' },
          { key: 'generate', label: 'Generate', disabled: !selectedTile },
          { key: 'report', label: 'Report', disabled: !report },
          { key: 'history', label: 'History', disabled: !user },
        ].map(t => (
          <button
            key={t.key}
            onClick={() => !t.disabled && setActiveTab(t.key)}
            disabled={t.disabled}
            className={`px-4 py-2.5 text-sm font-medium transition-colors ${
              activeTab === t.key
                ? 'border-b-2 border-gold text-gold'
                : t.disabled
                ? 'text-muted-foreground/40 cursor-not-allowed'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* TILES TAB */}
      {activeTab === 'tiles' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {tiles.map(tile => (
            <Card
              key={tile.tile_code}
              onClick={() => selectTile(tile)}
              className="p-5 border border-border hover:border-gold/50 cursor-pointer transition-all hover:-translate-y-0.5 hover:shadow-md"
            >
              <div className="flex items-start gap-3">
                <div className="w-9 h-9 rounded-sm bg-muted flex items-center justify-center flex-shrink-0 mt-0.5">
                  <TileIcon code={tile.tile_code} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-sm mb-1">{tile.name}</p>
                  <p className="text-xs text-muted-foreground line-clamp-2">{tile.description}</p>
                </div>
                <ChevronRight className="h-4 w-4 text-muted-foreground flex-shrink-0 mt-1" />
              </div>
            </Card>
          ))}
          {!user && (
            <div className="col-span-2 text-center py-4">
              <p className="text-sm text-muted-foreground mb-3">Sign in to generate reports</p>
              <Button onClick={() => navigate('/login')} variant="outline" size="sm">Sign in</Button>
            </div>
          )}
        </div>
      )}

      {/* GENERATE TAB */}
      {activeTab === 'generate' && selectedTile && (
        <div className="space-y-5">
          <button onClick={() => setActiveTab('tiles')} className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors">
            <ArrowLeft className="h-4 w-4" /> Back to tiles
          </button>
          <Card className="p-5 border border-gold/20 bg-gold/5">
            <div className="flex items-center gap-3">
              <TileIcon code={selectedTile.tile_code} />
              <p className="font-playfair font-semibold text-lg">{selectedTile.name}</p>
            </div>
          </Card>

          <Card className="p-6 border border-border space-y-4">
            {/* Core fields — always shown */}
            <div>
              <label className="block text-sm font-medium mb-1.5">Full Birth Name <span className="text-red-400">*</span></label>
              <input
                type="text"
                value={form.full_birth_name}
                onChange={e => setForm(f => ({ ...f, full_birth_name: e.target.value }))}
                placeholder="As on birth certificate"
                className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1.5">Date of Birth <span className="text-red-400">*</span></label>
              <input
                type="date"
                value={form.date_of_birth}
                onChange={e => setForm(f => ({ ...f, date_of_birth: e.target.value }))}
                className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40"
              />
            </div>

            {/* Conditional fields */}
            {needsField('current_popular_name') && (
              <div>
                <label className="block text-sm font-medium mb-1.5">Current Popular Name</label>
                <input type="text" value={form.current_popular_name} onChange={e => setForm(f => ({ ...f, current_popular_name: e.target.value }))} placeholder="Name commonly used today" className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40" />
              </div>
            )}
            {needsField('partner_full_birth_name') && (
              <div>
                <label className="block text-sm font-medium mb-1.5">Partner's Full Birth Name</label>
                <input type="text" value={form.partner_full_birth_name} onChange={e => setForm(f => ({ ...f, partner_full_birth_name: e.target.value }))} placeholder="Partner's name as on birth certificate" className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40" />
              </div>
            )}
            {needsField('partner_date_of_birth') && (
              <div>
                <label className="block text-sm font-medium mb-1.5">Partner's Date of Birth</label>
                <input type="date" value={form.partner_date_of_birth} onChange={e => setForm(f => ({ ...f, partner_date_of_birth: e.target.value }))} className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40" />
              </div>
            )}
            {needsField('digital_identifier') && (
              <div>
                <label className="block text-sm font-medium mb-1.5">Mobile / Vehicle / Important Number</label>
                <input type="text" value={form.digital_identifier} onChange={e => setForm(f => ({ ...f, digital_identifier: e.target.value }))} placeholder="e.g. 9876543210" className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40" />
              </div>
            )}
            {needsField('residential_number') && (
              <div>
                <label className="block text-sm font-medium mb-1.5">House / Flat Number</label>
                <input type="text" value={form.residential_number} onChange={e => setForm(f => ({ ...f, residential_number: e.target.value }))} placeholder="e.g. 42 or B-7" className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40" />
              </div>
            )}
            {needsField('business_name') && (
              <div>
                <label className="block text-sm font-medium mb-1.5">Business / Brand Name</label>
                <input type="text" value={form.business_name} onChange={e => setForm(f => ({ ...f, business_name: e.target.value }))} placeholder="Full business name" className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40" />
              </div>
            )}
            {needsField('candidate_name') && (
              <div>
                <label className="block text-sm font-medium mb-1.5">Candidate Baby Name</label>
                <input type="text" value={form.candidate_name} onChange={e => setForm(f => ({ ...f, candidate_name: e.target.value }))} placeholder="Proposed name" className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40" />
              </div>
            )}
            {needsField('target_year') && (
              <div>
                <label className="block text-sm font-medium mb-1.5">Target Year</label>
                <input type="number" min="2024" max="2040" value={form.target_year} onChange={e => setForm(f => ({ ...f, target_year: e.target.value }))} className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40" />
              </div>
            )}

            {/* Ankjyotish premium fields */}
            {needsField('time_of_birth') && (
              <div>
                <label className="block text-sm font-medium mb-1.5">Time of Birth <span className="text-red-400">*</span></label>
                <input type="time" value={form.time_of_birth} onChange={e => setForm(f => ({ ...f, time_of_birth: e.target.value }))} className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40" />
              </div>
            )}
            {needsField('place_of_birth') && (
              <div>
                <label className="block text-sm font-medium mb-1.5">Place of Birth <span className="text-red-400">*</span></label>
                <input type="text" value={form.place_of_birth} onChange={e => setForm(f => ({ ...f, place_of_birth: e.target.value }))} placeholder="e.g. Mumbai, India" className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40" />
              </div>
            )}
            {/* System selector */}
            <div className="flex gap-3">
              <div className="flex-1">
                <label className="block text-xs text-muted-foreground mb-1.5">System</label>
                <select value={form.numerology_system} onChange={e => setForm(f => ({ ...f, numerology_system: e.target.value }))} className="w-full px-3 py-2 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40">
                  <option value="pythagorean">Pythagorean</option>
                  <option value="chaldean">Chaldean</option>
                </select>
              </div>
              <div className="flex-1">
                <label className="block text-xs text-muted-foreground mb-1.5">Focus Area</label>
                <select value={form.focus_area} onChange={e => setForm(f => ({ ...f, focus_area: e.target.value }))} className="w-full px-3 py-2 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40">
                  {['general','career','love','health','wealth','purpose'].map(o => (
                    <option key={o} value={o}>{o.charAt(0).toUpperCase() + o.slice(1)}</option>
                  ))}
                </select>
              </div>
            </div>

            <Button onClick={handleGenerate} disabled={loading} className="w-full bg-gold hover:bg-gold/90 text-primary-foreground font-semibold gap-2">
              {loading ? <><Loader2 className="h-4 w-4 animate-spin" /> Generating...</> : <><Sparkles className="h-4 w-4" /> Generate Report</>}
            </Button>
          </Card>
        </div>
      )}

      {/* REPORT TAB */}
      {activeTab === 'report' && report && (
        <div className="space-y-5">
          <div className="flex items-center justify-between">
            <button onClick={() => setActiveTab('generate')} className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors">
              <ArrowLeft className="h-4 w-4" /> Back
            </button>
            <button
              onClick={() => toggleBookmark(report.id, report.bookmarked)}
              className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-gold transition-colors"
            >
              {report.bookmarked
                ? <><BookmarkCheck className="h-4 w-4 text-gold" /> Bookmarked</>
                : <><Bookmark className="h-4 w-4" /> Bookmark</>
              }
            </button>
          </div>

          {/* Summary card */}
          <Card className="p-6 border border-gold/30 bg-gold/5">
            <div className="flex items-start gap-3 mb-4">
              <TileIcon code={report.tile_code} />
              <div>
                <p className="font-playfair font-semibold text-lg">{TILE_META[report.tile_code]?.label || report.report_type}</p>
                <p className="text-xs text-muted-foreground">{report.full_birth_name} · {report.numerology_system}</p>
              </div>
            </div>
            <p className="text-sm text-foreground leading-relaxed">{report.summary}</p>
          </Card>

          {/* Computed numbers */}
          {report.computed_values && Object.keys(report.computed_values).length > 0 && (
            <Card className="p-5 border border-border">
              <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-4">Calculated Numbers</p>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {Object.entries(report.computed_values).map(([key, val]) => (
                  <div key={key} className="text-center p-3 rounded-sm bg-muted/30 border border-border">
                    <p className="text-2xl font-playfair font-bold text-gold">{val.reduced}</p>
                    {val.master_number && <p className="text-xs text-gold/70">Master {val.master_number}</p>}
                    <p className="text-xs text-muted-foreground mt-1 capitalize">{key.replace(/_/g, ' ')}</p>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Report sections */}
          {report.report_sections?.map(section => (
            <Card key={section.section_id} className="p-5 border border-border">
              <p className="font-semibold mb-2">{section.title}</p>
              <p className="text-sm text-gold mb-2">{section.summary}</p>
              <p className="text-sm text-muted-foreground leading-relaxed">{section.body}</p>
            </Card>
          ))}

          {/* Guidance */}
          <Card className="p-5 border border-gold/20 bg-gold/5">
            <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-2">Guidance</p>
            <p className="text-sm text-foreground leading-relaxed">{report.guidance}</p>
            {report.remedy_note && (
              <p className="text-sm text-muted-foreground mt-3 pt-3 border-t border-gold/20">{report.remedy_note}</p>
            )}
          </Card>

          <Button onClick={() => { setSelectedTile(null); setActiveTab('tiles'); }} variant="outline" className="w-full border-border">
            Generate Another Report
          </Button>
        </div>
      )}

      {/* HISTORY TAB */}
      {activeTab === 'history' && (
        <div className="space-y-3">
          {historyLoading && (
            <div className="text-center py-12"><Loader2 className="h-6 w-6 animate-spin text-gold mx-auto" /></div>
          )}
          {!historyLoading && history.length === 0 && (
            <div className="text-center py-12">
              <Hash className="h-10 w-10 text-muted-foreground/30 mx-auto mb-3" />
              <p className="text-muted-foreground">No reports yet. Generate your first reading.</p>
              <Button onClick={() => setActiveTab('tiles')} className="mt-4 bg-gold hover:bg-gold/90 text-primary-foreground" size="sm">Get Started</Button>
            </div>
          )}
          {history.map(item => (
            <Card key={item.id} className="p-4 border border-border hover:border-gold/30 transition-colors">
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-sm bg-muted flex items-center justify-center flex-shrink-0">
                  <TileIcon code={item.tile_code} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm">{TILE_META[item.tile_code]?.label || item.report_type}</p>
                  <p className="text-xs text-muted-foreground line-clamp-1 mt-0.5">{item.summary}</p>
                  <p className="text-xs text-muted-foreground mt-1">{new Date(item.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}</p>
                </div>
                <div className="flex items-center gap-2">
                  <button onClick={() => toggleBookmark(item.id, item.bookmarked)} className="text-muted-foreground hover:text-gold transition-colors">
                    {item.bookmarked ? <BookmarkCheck className="h-4 w-4 text-gold" /> : <Bookmark className="h-4 w-4" />}
                  </button>
                  <button onClick={() => openHistoryReport(item.id)} className="text-muted-foreground hover:text-foreground transition-colors">
                    <BookOpen className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
