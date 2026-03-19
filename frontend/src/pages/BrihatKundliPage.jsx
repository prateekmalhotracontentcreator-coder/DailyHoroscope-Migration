import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

import { Footer } from '../components/Footer';
import { PaymentModal } from '../components/PaymentModal';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { toast } from 'sonner';
import axios from 'axios';
import {
  Crown, Sparkles, Star, ArrowLeft, Download, Share2,
  ChevronDown, ChevronUp, BookOpen, Heart, TrendingUp,
  Shield, Gem, Sun, Moon, AlertTriangle, Check
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ─── Section Accordion ───────────────────────────────────────────────────────
const Section = ({ icon: Icon, title, color, children, defaultOpen = false }) => {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <Card className="border border-border overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-6 py-4 hover:bg-muted/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className={`w-8 h-8 rounded-sm flex items-center justify-center ${color}`}>
            <Icon className="h-4 w-4" />
          </div>
          <span className="font-playfair font-semibold text-lg">{title}</span>
        </div>
        {open ? <ChevronUp className="h-4 w-4 text-muted-foreground" /> : <ChevronDown className="h-4 w-4 text-muted-foreground" />}
      </button>
      {open && <div className="px-6 pb-6 border-t border-border pt-4">{children}</div>}
    </Card>
  );
};

// ─── Helper components ────────────────────────────────────────────────────────
const Tag = ({ children, color = 'bg-gold/10 text-gold' }) => (
  <span className={`inline-block text-xs font-medium px-2.5 py-1 rounded-full ${color}`}>{children}</span>
);

const BulletList = ({ items = [] }) => (
  <ul className="space-y-1.5 mt-2">
    {items.map((item, i) => (
      <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
        <Check className="h-3.5 w-3.5 text-gold flex-shrink-0 mt-0.5" />
        <span>{item}</span>
      </li>
    ))}
  </ul>
);

const RatingBadge = ({ rating }) => {
  const color = {
    Excellent: 'bg-green-500/10 text-green-600 dark:text-green-400',
    Good: 'bg-blue-500/10 text-blue-500',
    Average: 'bg-amber-500/10 text-amber-600',
    Challenging: 'bg-red-500/10 text-red-500',
    Strong: 'bg-green-500/10 text-green-600 dark:text-green-400',
    'Needs Attention': 'bg-red-500/10 text-red-500',
    Moderate: 'bg-amber-500/10 text-amber-600',
  }[rating] || 'bg-muted text-muted-foreground';
  return <Tag color={color}>{rating}</Tag>;
};

// ─── Report Display ───────────────────────────────────────────────────────────
const ReportDisplay = ({ report, onShare }) => {
  const planetStrengthColor = (strength) => ({
    Strong: 'text-green-500', Medium: 'text-amber-500', Weak: 'text-red-500'
  }[strength] || 'text-muted-foreground');

  return (
    <div className="space-y-4">
      {/* Header card */}
      <Card className="p-6 border border-gold/30 bg-gold/5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Crown className="h-5 w-5 text-gold" />
              <span className="text-xs font-semibold uppercase tracking-widest text-gold">Brihat Kundli Pro</span>
            </div>
            <h2 className="font-playfair text-2xl font-semibold">{report.full_name}</h2>
            <p className="text-sm text-muted-foreground mt-1">
              {report.date_of_birth} · {report.time_of_birth} · {report.place_of_birth}
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" className="gap-2 border-gold/40 hover:border-gold" onClick={onShare}>
              <Share2 className="h-4 w-4" /> Share
            </Button>
          </div>
        </div>
      </Card>

      {/* Core trinity */}
      {(report.ascendant || report.moon_sign || report.sun_sign) && (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            { label: 'Ascendant (Lagna)', data: report.ascendant, icon: '⬆', key: 'sign' },
            { label: 'Moon Sign (Rashi)', data: report.moon_sign, icon: '🌙', key: 'sign' },
            { label: 'Sun Sign', data: report.sun_sign, icon: '☀', key: 'sign' },
          ].map(({ label, data, icon, key }) => data && (
            <Card key={label} className="p-4 border border-border text-center">
              <div className="text-2xl mb-1">{icon}</div>
              <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">{label}</p>
              <p className="font-playfair font-semibold text-lg">{data[key]}</p>
              {data.nakshatra && <p className="text-xs text-gold mt-1">{data.nakshatra} Nakshatra</p>}
              {data.lord && <p className="text-xs text-muted-foreground mt-1">Lord: {data.lord}</p>}
            </Card>
          ))}
        </div>
      )}

      {/* Planetary positions */}
      {report.planetary_positions?.length > 0 && (
        <Section icon={Sun} title="Planetary Positions" color="bg-amber-500/10 text-amber-500" defaultOpen={true}>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  {['Planet', 'Sign', 'House', 'Status', 'Strength', 'Effects'].map(h => (
                    <th key={h} className="text-left py-2 pr-4 text-xs text-muted-foreground font-semibold uppercase tracking-wider">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {report.planetary_positions.map((p, i) => (
                  <tr key={i} className="hover:bg-muted/20 transition-colors">
                    <td className="py-3 pr-4 font-semibold">{p.planet}</td>
                    <td className="py-3 pr-4 text-muted-foreground">{p.sign}</td>
                    <td className="py-3 pr-4 text-muted-foreground">House {p.house}</td>
                    <td className="py-3 pr-4"><Tag>{p.status}</Tag></td>
                    <td className={`py-3 pr-4 font-semibold ${planetStrengthColor(p.strength)}`}>{p.strength}</td>
                    <td className="py-3 text-muted-foreground text-xs">{p.effects?.slice(0, 2).join(' · ')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>
      )}

      {/* Career */}
      {report.career_prediction && (
        <Section icon={TrendingUp} title="Career & Profession" color="bg-blue-500/10 text-blue-500">
          <div className="space-y-4">
            <div className="flex items-center gap-3 flex-wrap">
              <RatingBadge rating={report.career_prediction.overall_rating} />
              <span className="text-sm text-muted-foreground">Business potential: <strong>{report.career_prediction.business_potential}</strong></span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Best Career Fields</p>
                <BulletList items={report.career_prediction.best_career_fields} />
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Strengths at Work</p>
                <BulletList items={report.career_prediction.strengths_at_work} />
              </div>
            </div>
            {report.career_prediction.career_timeline?.length > 0 && (
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">Career Timeline</p>
                <div className="space-y-2">
                  {report.career_prediction.career_timeline.map((t, i) => (
                    <div key={i} className="flex gap-3 p-3 rounded-sm bg-muted/30 border border-border">
                      <div className="text-xs font-bold text-gold whitespace-nowrap">{t.period}</div>
                      <div>
                        <p className="text-sm">{t.prediction}</p>
                        <p className="text-xs text-muted-foreground mt-0.5">💡 {t.advice}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Section>
      )}

      {/* Love & Relationships */}
      {report.love_prediction && (
        <Section icon={Heart} title="Love & Relationships" color="bg-pink-500/10 text-pink-500">
          <div className="space-y-4">
            <RatingBadge rating={report.love_prediction.overall_rating} />
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Ideal Partner Traits</p>
                <BulletList items={report.love_prediction.ideal_partner_traits} />
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Compatible Signs</p>
                <div className="flex flex-wrap gap-2 mt-2">
                  {report.love_prediction.compatibility_signs?.map(s => <Tag key={s} color="bg-green-500/10 text-green-600 dark:text-green-400">{s}</Tag>)}
                </div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2 mt-3">Challenging Signs</p>
                <div className="flex flex-wrap gap-2">
                  {report.love_prediction.challenging_signs?.map(s => <Tag key={s} color="bg-red-500/10 text-red-500">{s}</Tag>)}
                </div>
              </div>
            </div>
            {report.love_prediction.marriage_timing && (
              <div className="p-3 rounded-sm bg-gold/5 border border-gold/20">
                <p className="text-xs font-semibold text-gold uppercase tracking-wider mb-2">Favorable Marriage Years</p>
                <div className="flex flex-wrap gap-2">
                  {report.love_prediction.marriage_timing.favorable_years?.map(y => (
                    <Tag key={y} color="bg-gold/15 text-gold">{y}</Tag>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Section>
      )}

      {/* Health */}
      {report.health_prediction && (
        <Section icon={Shield} title="Health & Wellbeing" color="bg-green-500/10 text-green-500">
          <div className="space-y-4">
            <div className="flex items-center gap-3 flex-wrap">
              <RatingBadge rating={report.health_prediction.overall_vitality} />
              {report.health_prediction.body_constitution && (
                <Tag color="bg-purple-500/10 text-purple-500">{report.health_prediction.body_constitution}</Tag>
              )}
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Vulnerable Areas</p>
                <BulletList items={report.health_prediction.vulnerable_areas} />
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Preventive Measures</p>
                <BulletList items={report.health_prediction.preventive_measures} />
              </div>
            </div>
            {report.health_prediction.dietary_recommendations?.length > 0 && (
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Dietary Recommendations</p>
                <div className="flex flex-wrap gap-2">
                  {report.health_prediction.dietary_recommendations.map(d => <Tag key={d}>{d}</Tag>)}
                </div>
              </div>
            )}
          </div>
        </Section>
      )}

      {/* Wealth */}
      {report.wealth_prediction && (
        <Section icon={Star} title="Wealth & Finance" color="bg-gold/10 text-gold">
          <div className="space-y-4">
            <RatingBadge rating={report.wealth_prediction.overall_rating} />
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Primary Income Sources</p>
                <BulletList items={report.wealth_prediction.primary_income_sources} />
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Good Investments</p>
                <BulletList items={report.wealth_prediction.investment_aptitude} />
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2 mt-3">Avoid</p>
                <BulletList items={report.wealth_prediction.avoid_investments} />
              </div>
            </div>
          </div>
        </Section>
      )}

      {/* Dasha */}
      {report.current_dasha && (
        <Section icon={Moon} title="Dasha Periods" color="bg-purple-500/10 text-purple-500">
          <div className="space-y-4">
            <div className="p-4 rounded-sm bg-purple-500/5 border border-purple-500/20">
              <p className="text-xs font-semibold uppercase tracking-wider text-purple-500 mb-2">Current Mahadasha</p>
              <p className="font-playfair font-semibold text-lg">{report.current_dasha.mahadasha} Dasha</p>
              {report.current_dasha.end_year && (
                <p className="text-sm text-muted-foreground">Until {report.current_dasha.end_year}</p>
              )}
              {report.current_dasha.effects && <BulletList items={report.current_dasha.effects} />}
            </div>
            {report.dasha_timeline?.length > 0 && (
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">Upcoming Dashas</p>
                <div className="space-y-2">
                  {report.dasha_timeline.map((d, i) => (
                    <div key={i} className="flex items-center justify-between p-3 rounded-sm border border-border bg-muted/20">
                      <div>
                        <span className="font-semibold text-sm">{d.planet} Dasha</span>
                        <p className="text-xs text-muted-foreground">{d.start_year} – {d.end_year}</p>
                      </div>
                      {d.key_theme && <Tag>{d.key_theme}</Tag>}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Section>
      )}

      {/* Doshas */}
      {(report.mangal_dosha || report.kalsarp_dosha) && (
        <Section icon={AlertTriangle} title="Doshas & Yogas" color="bg-red-500/10 text-red-500">
          <div className="space-y-4">
            {report.mangal_dosha && (
              <div className="p-3 rounded-sm border border-border">
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-1">Mangal Dosha</p>
                <p className="text-sm font-semibold">{report.mangal_dosha.present ? '⚠ Present' : '✓ Not Present'}</p>
                {report.mangal_dosha.severity && <p className="text-xs text-muted-foreground mt-1">Severity: {report.mangal_dosha.severity}</p>}
                {report.mangal_dosha.remedies && <BulletList items={report.mangal_dosha.remedies} />}
              </div>
            )}
            {report.benefic_yogas?.length > 0 && (
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-green-500 mb-2">Benefic Yogas</p>
                <div className="flex flex-wrap gap-2">
                  {report.benefic_yogas.map((y, i) => (
                    <Tag key={i} color="bg-green-500/10 text-green-600 dark:text-green-400">{y.name || y}</Tag>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Section>
      )}

      {/* Remedies */}
      {(report.gemstone_remedies?.length > 0 || report.mantra_remedies?.length > 0 || report.lifestyle_remedies?.length > 0) && (
        <Section icon={Gem} title="Remedies & Recommendations" color="bg-teal-500/10 text-teal-500">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {report.gemstone_remedies?.length > 0 && (
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Gemstones</p>
                <div className="space-y-2">
                  {report.gemstone_remedies.map((g, i) => (
                    <div key={i} className="p-2.5 rounded-sm border border-border bg-muted/20">
                      <p className="text-sm font-semibold">{g.stone || g}</p>
                      {g.finger && <p className="text-xs text-muted-foreground">Wear on: {g.finger}</p>}
                      {g.weight && <p className="text-xs text-muted-foreground">Weight: {g.weight}</p>}
                    </div>
                  ))}
                </div>
              </div>
            )}
            {report.mantra_remedies?.length > 0 && (
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Mantras</p>
                <BulletList items={report.mantra_remedies.map(m => m.mantra || m)} />
              </div>
            )}
            {report.lifestyle_remedies?.length > 0 && (
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Lifestyle</p>
                <BulletList items={report.lifestyle_remedies} />
              </div>
            )}
            {report.lucky_numbers?.length > 0 && (
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Lucky Numbers & Colours</p>
                <div className="flex flex-wrap gap-2 mb-2">
                  {report.lucky_numbers.map(n => <Tag key={n} color="bg-gold/10 text-gold">{n}</Tag>)}
                </div>
                <div className="flex flex-wrap gap-2">
                  {report.lucky_colors?.map(c => <Tag key={c}>{c}</Tag>)}
                </div>
              </div>
            )}
          </div>
        </Section>
      )}

      {/* Numerology */}
      {report.numerology && Object.keys(report.numerology).length > 0 && (
        <Section icon={BookOpen} title="Numerology" color="bg-indigo-500/10 text-indigo-500">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { label: 'Life Path', value: report.numerology.life_path_number },
              { label: 'Destiny', value: report.numerology.destiny_number },
              { label: 'Soul Urge', value: report.numerology.soul_urge_number },
              { label: 'Personality', value: report.numerology.personality_number },
            ].filter(i => i.value).map(({ label, value }) => (
              <div key={label} className="text-center p-3 rounded-sm border border-border">
                <p className="text-2xl font-bold font-playfair text-gold">{value}</p>
                <p className="text-xs text-muted-foreground mt-1">{label}</p>
              </div>
            ))}
          </div>
          {report.numerology.interpretation && (
            <p className="text-sm text-muted-foreground mt-4">{report.numerology.interpretation}</p>
          )}
        </Section>
      )}
    </div>
  );
};

// ─── Main Page ────────────────────────────────────────────────────────────────
export const BrihatKundliPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [form, setForm] = useState({
    full_name: user?.name || '',
    date_of_birth: '',
    time_of_birth: '',
    place_of_birth: '',
    gender: 'male',
    current_city: '',
    marital_status: '',
  });

  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showPayment, setShowPayment] = useState(false);
  const [hasPaid, setHasPaid] = useState(false);
  const [reportId, setReportId] = useState(null);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.full_name || !form.date_of_birth || !form.time_of_birth || !form.place_of_birth) {
      toast.error('Please fill in all required fields');
      return;
    }
    if (!hasPaid) {
      setShowPayment(true);
      return;
    }
    await generateReport();
  };

  const generateReport = async () => {
    setLoading(true);
    try {
      const res = await axios.post(
        `${API}/brihat-kundli/generate?user_email=${encodeURIComponent(user?.email || '')}`,
        form,
        { withCredentials: true }
      );
      setReport(res.data.report);
      setReportId(res.data.report_id);
      toast.success('Your Brihat Kundli Pro report is ready!');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      toast.error('Failed to generate report. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handlePaymentSuccess = async () => {
    setShowPayment(false);
    setHasPaid(true);
    toast.success('Payment successful! Generating your report...');
    await generateReport();
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({ title: 'My Brihat Kundli Pro Report', url: window.location.href });
    } else {
      navigator.clipboard.writeText(window.location.href);
      toast.success('Link copied to clipboard!');
    }
  };

  return (
    <div className="min-h-screen flex flex-col">


      <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-10">

        {/* Page header */}
        <div className="mb-8">
          <button onClick={() => navigate('/home')} className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors mb-5">
            <ArrowLeft className="h-4 w-4" /> Back to Home
          </button>
          <div className="flex items-center gap-3 mb-2">
            <div className="bg-gold/10 p-2 rounded-sm">
              <Crown className="h-6 w-6 text-gold" />
            </div>
            <div>
              <h1 className="text-3xl font-playfair font-semibold">Brihat Kundli Pro</h1>
              <p className="text-sm text-muted-foreground">Comprehensive Vedic Astrology Life Report · ₹1,499</p>
            </div>
          </div>
        </div>

        {/* What's included banner */}
        {!report && (
          <Card className="p-5 border border-gold/20 bg-gold/5 mb-8">
            <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">What's included in your report</p>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {[
                'Full planetary positions (9 planets)',
                'Career timeline & peak years',
                'Love & marriage predictions',
                'Health & dietary guidance',
                'Wealth & investment insights',
                'Current & future Dasha periods',
                'Mangal & Kalsarp Dosha analysis',
                'Benefic Yogas in your chart',
                'Gemstone & mantra remedies',
                'Lucky numbers, colours & days',
                'Numerology analysis',
                'PDF download included',
              ].map((item) => (
                <div key={item} className="flex items-start gap-2 text-xs text-muted-foreground">
                  <Check className="h-3 w-3 text-gold flex-shrink-0 mt-0.5" />
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </Card>
        )}

        {/* Report display */}
        {report ? (
          <ReportDisplay report={report} onShare={handleShare} />
        ) : (
          /* Input form */
          <Card className="p-6 border border-border">
            <div className="flex items-center gap-2 mb-6">
              <Sparkles className="h-5 w-5 text-gold" />
              <h2 className="text-xl font-playfair font-semibold">Enter Your Birth Details</h2>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Full name */}
              <div>
                <label className="block text-sm font-medium mb-1.5">Full Name <span className="text-red-500">*</span></label>
                <input
                  name="full_name"
                  value={form.full_name}
                  onChange={handleChange}
                  placeholder="As per birth records"
                  required
                  className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 focus:border-gold transition-all"
                />
              </div>

              {/* Date + Time */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1.5">Date of Birth <span className="text-red-500">*</span></label>
                  <input
                    type="date"
                    name="date_of_birth"
                    value={form.date_of_birth}
                    onChange={handleChange}
                    required
                    className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 focus:border-gold transition-all"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5">Time of Birth <span className="text-red-500">*</span></label>
                  <input
                    type="time"
                    name="time_of_birth"
                    value={form.time_of_birth}
                    onChange={handleChange}
                    required
                    className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 focus:border-gold transition-all"
                  />
                  <p className="text-xs text-muted-foreground mt-1">24-hour format — be as accurate as possible</p>
                </div>
              </div>

              {/* Place + Gender */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1.5">Place of Birth <span className="text-red-500">*</span></label>
                  <input
                    name="place_of_birth"
                    value={form.place_of_birth}
                    onChange={handleChange}
                    placeholder="City, State, Country"
                    required
                    className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 focus:border-gold transition-all"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5">Gender <span className="text-red-500">*</span></label>
                  <select
                    name="gender"
                    value={form.gender}
                    onChange={handleChange}
                    className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 focus:border-gold transition-all"
                  >
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>

              {/* Optional fields */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1.5">Current City <span className="text-xs text-muted-foreground font-normal">(optional)</span></label>
                  <input
                    name="current_city"
                    value={form.current_city}
                    onChange={handleChange}
                    placeholder="Where you live now"
                    className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 focus:border-gold transition-all"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5">Marital Status <span className="text-xs text-muted-foreground font-normal">(optional)</span></label>
                  <select
                    name="marital_status"
                    value={form.marital_status}
                    onChange={handleChange}
                    className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 focus:border-gold transition-all"
                  >
                    <option value="">Select...</option>
                    <option value="single">Single</option>
                    <option value="married">Married</option>
                    <option value="divorced">Divorced</option>
                    <option value="widowed">Widowed</option>
                  </select>
                </div>
              </div>

              <div className="pt-2">
                <Button
                  type="submit"
                  disabled={loading}
                  className="w-full h-12 bg-gold hover:bg-gold/90 text-primary-foreground font-semibold text-base gap-2 hover:shadow-[0_8px_20px_-5px_rgba(197,160,89,0.4)] transition-all"
                >
                  {loading ? (
                    <><Sparkles className="h-4 w-4 animate-pulse" /> Generating your report...</>
                  ) : (
                    <><Crown className="h-4 w-4" /> Generate Report · ₹1,499</>
                  )}
                </Button>
                <p className="text-xs text-center text-muted-foreground mt-2">
                  One-time payment · Report generated in ~60 seconds · Secure payment via Razorpay
                </p>
              </div>
            </form>
          </Card>
        )}
      </main>

      <Footer />

      {/* Payment modal */}
      <PaymentModal
        isOpen={showPayment}
        onClose={() => setShowPayment(false)}
        reportType="brihat_kundli"
        reportId={reportId || 'new'}
        onSuccess={handlePaymentSuccess}
      />
    </div>
  );
};
