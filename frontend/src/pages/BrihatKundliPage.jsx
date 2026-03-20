import React, { useState, useEffect } from 'react';
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
const ReportDisplay = ({ report, onShare, onDownload }) => {
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
            <Button variant="outline" size="sm" className="gap-2 border-gold/40 hover:border-gold hover:bg-gold/10" onClick={onDownload}>
              <Download className="h-4 w-4" /> Generate PDF
            </Button>
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

      {/* North Indian Kundali Chart */}
      {report.chart_svg && (
        <Card className="p-4 border border-gold/30">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xs font-semibold uppercase tracking-widest text-gold">Janma Kundali — North Indian Chart</span>
          </div>
          <div className="flex justify-center"
            dangerouslySetInnerHTML={{ __html: report.chart_svg }}
          />
        </Card>
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
                <BulletList items={report.wealth_prediction.good_investments} />
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2 mt-3">Avoid</p>
                <BulletList items={report.wealth_prediction.avoid} />
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
              <p className="font-playfair font-semibold text-lg">{report.current_dasha.mahadasha} Mahadasha</p>
              {(report.current_dasha.end_year || report.current_dasha.period) && (
                <p className="text-sm text-muted-foreground">
                  {report.current_dasha.period || `Until ${report.current_dasha.end_year}`}
                </p>
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
                        <span className="font-semibold text-sm">{(d.planet || '').replace(' Mahadasha','').replace(' Dasha','')} Mahadasha</span>
                        <p className="text-xs text-muted-foreground">
                          {d.period || (d.start_year && d.end_year ? `${d.start_year} – ${d.end_year}` : '–')}
                        </p>
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
  const [checkingPremium, setCheckingPremium] = useState(true);

  // Check premium access + auto-populate form from saved birth profile
  useEffect(() => {
    const init = async () => {
      if (!user?.email) { setCheckingPremium(false); return; }
      try {
        // Premium check
        const premRes = await axios.get(`${API}/premium/check`, {
          params: { user_email: user.email, report_type: 'brihat_kundli', report_id: 'new' }
        });
        if (premRes.data.has_premium_access) setHasPaid(true);

        // Auto-populate from saved birth profile
        const profileRes = await axios.get(`${API}/profile/birth`);
        const profiles = profileRes.data;
        // Find profile matching current user name, or use most recent
        const userProfile = profiles?.find(p => 
          p.name?.toLowerCase().includes(user.name?.split(' ')[0]?.toLowerCase() || '')
        ) || profiles?.[0];
        if (userProfile) {
          const p = userProfile;
          setForm(prev => ({
            ...prev,
            full_name: p.name || prev.full_name,
            date_of_birth: p.date_of_birth || prev.date_of_birth,
            time_of_birth: p.time_of_birth || prev.time_of_birth,
            place_of_birth: p.location || p.place_of_birth || prev.place_of_birth,
          }));
        }
      } catch (err) {
        console.error('Init failed:', err);
      } finally {
        setCheckingPremium(false);
      }
    };
    init();
  }, [user]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.full_name || !form.date_of_birth || !form.time_of_birth || !form.place_of_birth) {
      toast.error('Please fill in all required fields');
      return;
    }
    if (checkingPremium) {
      toast.info('Verifying your access, please wait...');
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

  const handleDownload = async () => {
    if (!reportId) { toast.error('Report not found. Please generate first.'); return; }
    try {
      toast.info('Preparing your PDF...');
      const res = await axios.get(`${API}/brihat-kundli/${reportId}/pdf`, {
        responseType: 'blob',
        withCredentials: true,
      });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      const name = report?.full_name?.replace(/\s+/g, '_') || 'report';
      link.setAttribute('download', `brihat_kundli_${name}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      // Show password hint
      const pwd = res.headers['x-pdf-password'];
      if (pwd) {
        toast.success(`PDF downloaded! Password: ${pwd}`, { duration: 10000 });
      } else {
        toast.success('PDF downloaded!');
      }
    } catch (err) {
      console.error('PDF download error:', err);
      toast.error('Failed to download PDF. Please try again.');
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
          <ReportDisplay report={report} onShare={handleShare} onDownload={handleDownload} />
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

      {/* ── SEO Content Section ──────────────────────────────────────────── */}
      <section className="bg-muted/30 border-t border-border mt-12 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto space-y-12">

          {/* What is Brihat Kundli */}
          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-4">What is Brihat Kundli Pro?</h2>
            <p className="text-muted-foreground leading-relaxed mb-3">
              Brihat Kundli Pro is the most comprehensive Vedic astrology life report available online — equivalent to a 40-page professional consultation with a senior Jyotishi. The word <em>Brihat</em> means "vast" or "extensive" in Sanskrit, and this report lives up to its name by covering every major dimension of your life through the lens of your unique birth chart.
            </p>
            <p className="text-muted-foreground leading-relaxed">
              Unlike a basic horoscope or a simple birth chart reading, the Brihat Kundli Pro uses a two-layer system: Layer 1 performs precise mathematical calculations using your exact birth data — computing planetary positions, house lords, nakshatra placements, and Dasha periods with the same accuracy as professional astrology software. Layer 2 then applies deep Jyotish interpretation to these calculations, producing a personalised report that is both astrologically accurate and meaningfully written.
            </p>
          </div>

          {/* What's included */}
          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-4">What's Included in Your Brihat Kundli Report</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {[
                { title: 'North Indian Birth Chart', desc: 'Janma Kundali rendered in traditional North Indian diamond grid format with all 9 planets placed in their correct houses.' },
                { title: '12-House Complete Analysis', desc: 'Every house from Lagna (self) to Vyaya (liberation) receives a detailed interpretation covering its sign, lord, planets, and meaning for your life.' },
                { title: 'Ascendant & Personality', desc: 'Deep analysis of your Lagna sign, its ruling planet, and what it means for your personality, appearance, and approach to life.' },
                { title: 'Moon Sign & Emotional Nature', desc: 'Your Rashi (Moon sign) and Nakshatra reveal your emotional patterns, subconscious tendencies, and relationship with your inner world.' },
                { title: 'Planetary Positions & Yogas', desc: 'All 9 planets analysed in their houses — their strength, status, and effects on your life. Benefic yogas and their specific manifestations identified.' },
                { title: 'Career & Dharma', desc: 'Best career fields, professional strengths, and a career timeline covering your current Mahadasha through the next 20 years.' },
                { title: 'Love, Marriage & Partnerships', desc: 'Ideal partner traits, compatible signs, favourable marriage years, and spouse characteristics from 7th house analysis.' },
                { title: 'Health & Wellbeing', desc: 'Constitutional analysis, vulnerable body areas, preventive measures, and dietary recommendations based on your planetary positions.' },
                { title: 'Wealth & Finance', desc: 'Wealth potential, primary income sources, best investments, and periods of peak financial growth.' },
                { title: 'Mangal Dosha Analysis', desc: 'Precise Mangal Dosha assessment from Mars house position, severity level, cancellation rules, and specific remedies.' },
                { title: 'Dasha Period Analysis', desc: 'Current Mahadasha in depth plus the next two upcoming Mahadashas — what each period brings and how to navigate it.' },
                { title: 'Gemstones, Mantras & Remedies', desc: 'Personalised remedies including gemstone prescriptions with wearing instructions, planet-specific mantras, and lifestyle practices.' },
              ].map(({ title, desc }) => (
                <div key={title} className="flex gap-3 p-4 rounded-sm border border-border bg-card">
                  <span className="text-gold mt-0.5">✦</span>
                  <div>
                    <p className="font-semibold text-sm mb-1">{title}</p>
                    <p className="text-xs text-muted-foreground leading-relaxed">{desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Vedic Science */}
          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-4">How Our Vedic Calculations Work</h2>
            <p className="text-muted-foreground leading-relaxed mb-3">
              Your Brihat Kundli Pro is powered by the same Parashari Jyotish principles used by professional Vedic astrologers for thousands of years. Every result in your report is mathematically deterministic — the same birth details will always produce the same chart. There is no randomness in planetary positions, nakshatra placements, or Dasha calculations.
            </p>
            <p className="text-muted-foreground leading-relaxed mb-3">
              We use the Swiss Ephemeris — the most accurate planetary calculation system available — combined with the traditional Lahiri ayanamsha for Vedic sidereal calculations. Your Ascendant is calculated to the exact degree based on your birth time and location coordinates. Nakshatra Pada is determined from the Moon's precise longitude at your moment of birth.
            </p>
            <p className="text-muted-foreground leading-relaxed">
              The Vimshottari Dasha system calculates your planetary periods from the Moon's Nakshatra position, giving accurate start and end years for every major life period from birth to age 120. All doshas — Mangal Dosha, Kalsarp Dosha — are assessed using classical Parashari rules, not generalised assumptions.
            </p>
          </div>

          {/* FAQ */}
          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-6">Frequently Asked Questions</h2>
            <div className="space-y-5">
              {[
                {
                  q: 'What is the difference between a basic Birth Chart and Brihat Kundli Pro?',
                  a: 'A basic Birth Chart gives you planetary positions and a general interpretation. Brihat Kundli Pro goes significantly deeper — it includes full 12-house analysis with 4-5 sentences per house, detailed Dasha period analysis for the next 40 years, personalised gemstone prescriptions with wearing instructions, family and progeny analysis, numerology integration, and a downloadable 40-page PDF report. It is designed for people who want a comprehensive, lasting reference document rather than a quick overview.'
                },
                {
                  q: 'How accurate is the Vedic calculation in your report?',
                  a: 'Our calculations use the Swiss Ephemeris with Lahiri ayanamsha — the same system used by professional Vedic astrology software. Planetary positions, house lords, nakshatra placements, and Dasha timings are mathematically precise. The same birth details will always produce identical calculations. Interpretation quality depends on the accuracy of your birth time — even a difference of a few minutes can shift the Ascendant and Dasha start dates, so we recommend using your official birth record for best results.'
                },
                {
                  q: 'What is Mangal Dosha and should I be concerned?',
                  a: 'Mangal Dosha occurs when Mars is placed in the 1st, 2nd, 4th, 7th, 8th, or 12th house of the birth chart. It is associated with potential challenges in marriage and relationships. However, Mangal Dosha has multiple cancellation rules — if both partners have it, it cancels out. Many other planetary combinations also reduce its effect. Our report accurately identifies whether Mangal Dosha is present, its severity, applicable cancellation rules, and specific remedies. It is important context, not a cause for alarm.'
                },
                {
                  q: 'Can I download my Brihat Kundli report as a PDF?',
                  a: 'Yes — once your report is generated, click the "Generate PDF" button to download a fully formatted PDF version. The PDF includes your North Indian Kundali chart, planetary positions table, all analysis sections, and remedies. The PDF is password-protected for your privacy using a personalised formula based on your birth details. Your password hint is shown when the download completes.'
                },
                {
                  q: 'What birth details do I need to provide?',
                  a: 'You need your full name, date of birth (day/month/year), time of birth (as accurate as possible — check your birth certificate), place of birth (city), and gender. The time of birth is particularly important as it determines your Ascendant and house placements. If you do not know your exact birth time, the report will use a default time and note the limitation in the output.'
                },
                {
                  q: 'How is Brihat Kundli Pro different from what AstroSage or Astrotalk offers?',
                  a: 'Most platforms generate template-based reports with pre-written paragraphs filled with your name. Our Brihat Kundli Pro generates each report fresh using AI interpretation of your specific chart data — every sentence is written specifically for your planetary configuration. The gemstone prescriptions include how-to-wear instructions. The Dasha analysis addresses your specific current period, not a generic template. And unlike most competitors, our calculations are powered by the same Swiss Ephemeris used by professional software, ensuring mathematical accuracy.'
                },
              ].map(({ q, a }) => (
                <div key={q} className="border border-border rounded-sm p-5">
                  <h3 className="font-semibold mb-2 text-sm">{q}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{a}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Why Vedic */}
          <div>
            <h2 className="text-2xl font-playfair font-semibold mb-4">Why Vedic Astrology for Life Guidance?</h2>
            <p className="text-muted-foreground leading-relaxed mb-3">
              Vedic astrology (Jyotisha) is one of the six Vedangas — ancillary disciplines of the Vedas — with a continuous tradition spanning more than 5,000 years. Unlike Western astrology which uses the tropical zodiac, Vedic astrology uses the sidereal zodiac, aligning zodiac signs with actual star constellations. This means your Vedic chart may show a different sign placement than your Western chart — and is considered by millions of practitioners to be more accurate for life events and timing.
            </p>
            <p className="text-muted-foreground leading-relaxed mb-3">
              The Parashari system used in our reports — named after the sage Parashara, author of Brihat Parashara Hora Shastra — is the most widely practised school of Vedic astrology. It uses the Ascendant (Lagna) as the primary lens, the Nakshatra (lunar mansion) system for detailed personality and timing analysis, and the Vimshottari Dasha for period-by-period life forecasting. These three pillars together produce a remarkably precise and actionable framework for understanding your life.
            </p>
            <p className="text-muted-foreground leading-relaxed">
              The Brihat Kundli Pro incorporates Parashari principles throughout — from house analysis and yoga identification to Dasha timing and remedial prescriptions — giving you access to the depth of this ancient tradition in a format designed for the modern world.
            </p>
          </div>

        </div>
      </section>

      {/* JSON-LD Structured Data */}
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "Brihat Kundli Pro — Comprehensive Vedic Astrology Life Report",
        "description": "40-page comprehensive Vedic astrology life report including 12-house analysis, planetary positions, career, love, health, wealth, Dasha periods, Mangal Dosha, yogas, gemstone remedies, and downloadable PDF.",
        "provider": { "@type": "Organization", "name": "Everyday Horoscope", "url": "https://everydayhoroscope.in" },
        "serviceType": "Vedic Astrology Report",
        "url": "https://everydayhoroscope.in/brihat-kundli",
        "offers": { "@type": "Offer", "price": "1499", "priceCurrency": "INR" },
        "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "1200" },
        "faqPage": {
          "@type": "FAQPage",
          "mainEntity": [
            { "@type": "Question", "name": "What is Brihat Kundli Pro?", "acceptedAnswer": { "@type": "Answer", "text": "Brihat Kundli Pro is a comprehensive 40-page Vedic astrology life report covering all 12 houses, planetary positions, Dasha analysis, Mangal Dosha, yogas, and personalised remedies." } },
            { "@type": "Question", "name": "Is Mangal Dosha serious?", "acceptedAnswer": { "@type": "Answer", "text": "Mangal Dosha has multiple cancellation rules and is not automatically harmful. Our report accurately identifies severity and applicable remedies." } },
          ]
        }
      })}} />

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
