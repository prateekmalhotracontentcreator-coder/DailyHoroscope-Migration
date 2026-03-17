import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Footer } from '../components/Footer';
import { SEO } from '../components/SEO';
import {
  Sparkles, Star, Sun, Calendar, TrendingUp, Heart,
  Crown, ArrowRight, Check, Moon
} from 'lucide-react';

const ZODIAC_SIGNS = [
  { id: 'aries',       symbol: '♈', name: 'Aries',       dates: 'Mar 21 – Apr 19', element: 'Fire'  },
  { id: 'taurus',      symbol: '♉', name: 'Taurus',      dates: 'Apr 20 – May 20', element: 'Earth' },
  { id: 'gemini',      symbol: '♊', name: 'Gemini',      dates: 'May 21 – Jun 20', element: 'Air'   },
  { id: 'cancer',      symbol: '♋', name: 'Cancer',      dates: 'Jun 21 – Jul 22', element: 'Water' },
  { id: 'leo',         symbol: '♌', name: 'Leo',         dates: 'Jul 23 – Aug 22', element: 'Fire'  },
  { id: 'virgo',       symbol: '♍', name: 'Virgo',       dates: 'Aug 23 – Sep 22', element: 'Earth' },
  { id: 'libra',       symbol: '♎', name: 'Libra',       dates: 'Sep 23 – Oct 22', element: 'Air'   },
  { id: 'scorpio',     symbol: '♏', name: 'Scorpio',     dates: 'Oct 23 – Nov 21', element: 'Water' },
  { id: 'sagittarius', symbol: '♐', name: 'Sagittarius', dates: 'Nov 22 – Dec 21', element: 'Fire'  },
  { id: 'capricorn',   symbol: '♑', name: 'Capricorn',   dates: 'Dec 22 – Jan 19', element: 'Earth' },
  { id: 'aquarius',    symbol: '♒', name: 'Aquarius',    dates: 'Jan 20 – Feb 18', element: 'Air'   },
  { id: 'pisces',      symbol: '♓', name: 'Pisces',      dates: 'Feb 19 – Mar 20', element: 'Water' },
];

const FEATURES = [
  { icon: Sun,       title: 'Daily Horoscope',     description: 'Start every morning with personalised cosmic guidance. Your stars, refreshed at midnight.',                        free: true,  color: 'text-amber-500', bg: 'bg-amber-500/10' },
  { icon: Calendar,  title: 'Weekly Forecast',      description: 'Plan ahead with a full week of astrological insights covering love, career, and wellness.',                        free: true,  color: 'text-blue-500',  bg: 'bg-blue-500/10'  },
  { icon: TrendingUp,title: 'Monthly Outlook',      description: 'See the big picture. Navigate major planetary transits and seize the month\'s best moments.',                      free: true,  color: 'text-green-500', bg: 'bg-green-500/10' },
  { icon: Star,      title: 'Birth Chart Analysis', description: 'A deep Vedic astrology report built from your exact birth time, date, and location.',                             free: false, color: 'text-gold',      bg: 'bg-gold/10'      },
  { icon: Heart,     title: 'Kundali Milan',         description: 'Compatibility scoring for couples. Guna matching, doshas, and full relationship analysis.',                        free: false, color: 'text-pink-500',  bg: 'bg-pink-500/10'  },
  { icon: Crown,     title: 'Brihat Kundli Pro',    description: 'The most comprehensive Vedic report — 40+ pages covering every aspect of your destiny.',                          free: false, color: 'text-purple-500',bg: 'bg-purple-500/10'},
];

const TESTIMONIALS = [
  { name: 'Ananya S.', sign: '♏', signName: 'Scorpio',     text: 'The daily horoscope is uncannily accurate. It\'s the first thing I check every morning before work.', stars: 5 },
  { name: 'Rohan M.',  sign: '♌', signName: 'Leo',         text: 'My birth chart report gave me chills. Details about my personality I\'ve never seen described so precisely.', stars: 5 },
  { name: 'Priya K.',  sign: '♎', signName: 'Libra',       text: 'Used Kundali Milan before our engagement. It matched our horoscopes and gave us real peace of mind.', stars: 5 },
  { name: 'Vikram T.', sign: '♐', signName: 'Sagittarius', text: 'Beautifully designed and genuinely insightful. The weekly forecast helps me plan my week ahead.', stars: 5 },
];

const PLANS = [
  {
    name: 'Free', price: '₹0', period: 'forever', description: 'Start your cosmic journey', highlight: false, cta: 'Get Started Free',
    features: ['Daily horoscope for your sign', 'Weekly forecast', 'Monthly outlook', 'Cosmic Blog access'],
  },
  {
    name: 'Premium', price: '₹1,599', period: 'per month', description: 'Unlock your full cosmic potential', highlight: true, cta: 'Start Premium',
    features: ['Everything in Free', 'Unlimited Birth Chart reports', 'Unlimited Kundali Milan', 'PDF downloads', 'Priority report generation', 'Social sharing'],
  },
  {
    name: 'Brihat Kundli Pro', price: '₹1,499', period: 'one-time', description: 'The ultimate Vedic life report', highlight: false, cta: 'Get Your Report',
    features: ['40+ page comprehensive report', 'Full planetary dasha analysis', 'Career, love & wealth insights', 'Remedies & gemstone guidance', 'PDF download included'],
  },
];

const StarField = () => {
  const canvasRef = useRef(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animFrame;
    const resize = () => { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; };
    resize();
    window.addEventListener('resize', resize);
    const stars = Array.from({ length: 120 }, () => ({
      x: Math.random(), y: Math.random(),
      r: Math.random() * 1.4 + 0.2,
      speed: Math.random() * 0.008 + 0.002,
      phase: Math.random() * Math.PI * 2,
    }));
    const draw = (t) => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      stars.forEach((s) => {
        const a = 0.3 + 0.7 * Math.abs(Math.sin(t * s.speed + s.phase));
        ctx.beginPath();
        ctx.arc(s.x * canvas.width, s.y * canvas.height, s.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(197,160,89,${a * 0.85})`;
        ctx.fill();
      });
      animFrame = requestAnimationFrame(draw);
    };
    animFrame = requestAnimationFrame(draw);
    return () => { cancelAnimationFrame(animFrame); window.removeEventListener('resize', resize); };
  }, []);
  return <canvas ref={canvasRef} className="absolute inset-0 w-full h-full pointer-events-none" style={{ opacity: 0.6 }} />;
};

export const Landing = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [selectedSign, setSelectedSign] = useState(null);
  const [visible, setVisible] = useState(new Set());
  const refs = useRef({});

  useEffect(() => { if (user) navigate('/home', { replace: true }); }, [user, navigate]);

  useEffect(() => {
    const saved = localStorage.getItem('selected-sign');
    if (saved) setSelectedSign(saved);
  }, []);

  useEffect(() => {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) setVisible((p) => new Set([...p, e.target.dataset.sec])); });
    }, { threshold: 0.1 });
    Object.values(refs.current).forEach((el) => { if (el) obs.observe(el); });
    return () => obs.disconnect();
  }, []);

  const ref = (key) => (el) => { refs.current[key] = el; if (el) el.dataset.sec = key; };
  const vis = (k) => visible.has(k);

  const anim = (key, delay = 0) => ({
    opacity: vis(key) ? 1 : 0,
    transform: vis(key) ? 'translateY(0)' : 'translateY(28px)',
    transition: `opacity 0.7s ease ${delay}ms, transform 0.7s ease ${delay}ms`,
  });

  const elementColor = (el) => ({
    Fire: 'text-amber-500', Earth: 'text-green-600', Air: 'text-blue-400', Water: 'text-cyan-500'
  }[el] || 'text-muted-foreground');

  return (
    <div className="min-h-screen overflow-x-hidden">
      <SEO
        title="Free Daily Horoscope & Vedic Astrology"
        description="Get your free daily, weekly, and monthly horoscope predictions. AI-powered Birth Chart, Kundali Milan, and Brihat Kundli Pro reports based on Vedic astrology."
        url="https://everydayhoroscope.in"
        schema={{
          "@context": "https://schema.org",
          "@type": "Organization",
          "name": "Everyday Horoscope",
          "url": "https://everydayhoroscope.in",
          "logo": "https://everydayhoroscope.in/og-image.png",
          "description": "AI-powered Vedic astrology platform offering daily horoscopes, birth charts, and Kundali Milan.",
          "founder": { "@type": "Organization", "name": "SkyHound Studios" },
          "contactPoint": { "@type": "ContactPoint", "email": "prateekmalhotra.contentcreator@gmail.com", "contactType": "customer support" }
        }}
      />

      {/* NAV */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-border/40 bg-background/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
            <Sparkles className="h-5 w-5 text-gold" />
            <span className="font-cinzel font-bold text-lg tracking-wide">Everyday Horoscope</span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm text-muted-foreground">
            {[['Features', 'features'], ['Pricing', null], ['Blog', null]].map(([label, id]) => (
              <button key={label} onClick={() => {
                if (label === 'Pricing') navigate('/pricing');
                else if (id) document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
                else navigate('/blog');
              }} className="hover:text-foreground transition-colors">{label}</button>
            ))}
          </div>
          <div className="flex items-center gap-3">
            <button onClick={() => navigate('/login')} className="text-sm text-muted-foreground hover:text-foreground transition-colors px-3 py-1.5">Sign in</button>
            <button onClick={() => navigate('/register')} className="text-sm bg-gold hover:bg-gold/90 text-primary-foreground px-4 py-1.5 rounded-sm font-medium transition-all">Get Started</button>
          </div>
        </div>
      </nav>

      {/* HERO */}
      <section className="relative min-h-screen flex flex-col items-center justify-center pt-16 pb-12 px-4 overflow-hidden">
        <StarField />
        <div className="absolute inset-0 pointer-events-none" style={{ background: 'radial-gradient(ellipse 70% 50% at 50% 40%, rgba(197,160,89,0.07) 0%, transparent 70%)' }} />
        <div className="relative z-10 text-center max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-[0.2em] px-4 py-2 rounded-full mb-8">
            <Moon className="h-3 w-3" /> Ancient Vedic Astrology
          </div>
          <h1 className="font-cinzel font-bold leading-none mb-6" style={{ fontSize: 'clamp(2.8rem, 8vw, 6rem)' }}>
            Your Stars.<br /><span className="text-gold">Your Story.</span>
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed font-playfair">
            Personalised daily horoscopes, birth charts, and Vedic reports — rooted in 5,000 years of ancient wisdom, interpreted for you.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <button onClick={() => document.getElementById('sign-picker')?.scrollIntoView({ behavior: 'smooth' })} className="group inline-flex items-center gap-2 bg-gold hover:bg-gold/90 text-primary-foreground px-8 py-4 rounded-sm font-semibold text-base transition-all hover:shadow-[0_8px_30px_-5px_rgba(197,160,89,0.5)] hover:-translate-y-0.5">
              Begin Your Journey <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </button>
            <button onClick={() => document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })} className="inline-flex items-center gap-2 border border-border hover:border-gold/50 text-foreground px-8 py-4 rounded-sm font-medium text-base transition-all hover:-translate-y-0.5">
              Explore Features
            </button>
          </div>
          <div className="flex flex-wrap items-center justify-center gap-4 sm:gap-6 text-sm text-muted-foreground">
            <div className="flex items-center gap-1.5"><span className="text-gold text-xs">★★★★★</span><span>4.9 / 5</span></div>
            <div className="h-4 w-px bg-border" />
            <span>10,000+ readings generated</span>
            <div className="h-4 w-px bg-border hidden sm:block" />
            <span className="hidden sm:block">12 zodiac signs covered daily</span>
          </div>
        </div>
      </section>

      {/* SIGN PICKER */}
      <section id="sign-picker" ref={ref('signs')} className="py-20 px-4" style={anim('signs')}>
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="font-playfair text-3xl md:text-4xl font-semibold mb-3">What's your sign?</h2>
            <p className="text-muted-foreground">Select your zodiac to personalise your experience</p>
          </div>
          <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3 mb-10">
            {ZODIAC_SIGNS.map((sign) => (
              <button key={sign.id} onClick={() => { setSelectedSign(sign.id); localStorage.setItem('selected-sign', sign.id); }}
                className={`group flex flex-col items-center gap-1.5 p-4 rounded-sm border transition-all duration-300 hover:-translate-y-1 ${selectedSign === sign.id ? 'border-gold bg-gold/10 shadow-[0_0_20px_-5px_rgba(197,160,89,0.4)]' : 'border-border bg-card hover:border-gold/40'}`}>
                <span className="text-3xl leading-none group-hover:scale-110 transition-transform duration-200">{sign.symbol}</span>
                <span className="text-xs font-semibold font-playfair">{sign.name}</span>
                <span className={`text-[10px] uppercase tracking-wider ${elementColor(sign.element)}`}>{sign.element}</span>
              </button>
            ))}
          </div>
          {selectedSign && (
            <div className="text-center">
              <button onClick={() => navigate('/register')} className="group inline-flex items-center gap-2 bg-gold hover:bg-gold/90 text-primary-foreground px-10 py-4 rounded-sm font-semibold text-base transition-all hover:shadow-[0_8px_30px_-5px_rgba(197,160,89,0.4)] hover:-translate-y-0.5">
                <Sparkles className="h-4 w-4" />
                Read My {ZODIAC_SIGNS.find(s => s.id === selectedSign)?.name} Horoscope
                <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
          )}
        </div>
      </section>

      {/* FEATURES */}
      <section id="features" ref={ref('features')} className="py-20 px-4 border-t border-border/50" style={anim('features', 100)}>
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <div className="inline-flex items-center gap-2 text-gold text-xs font-semibold uppercase tracking-[0.2em] mb-4"><Star className="h-3 w-3" /> Everything you need</div>
            <h2 className="font-playfair text-3xl md:text-4xl font-semibold mb-4">Cosmic tools for every seeker</h2>
            <p className="text-muted-foreground max-w-xl mx-auto">From free daily readings to in-depth Vedic reports — insights for every stage of your journey.</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {FEATURES.map((f, i) => {
              const Icon = f.icon;
              return (
                <div key={f.title} onClick={() => navigate('/register')} className="group relative p-6 rounded-sm border border-border bg-card hover:border-gold/40 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_8px_30px_-5px_rgba(197,160,89,0.15)] cursor-pointer">
                  {!f.free && <div className="absolute top-4 right-4 flex items-center gap-1 bg-gold/15 text-gold text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full"><Crown className="h-2.5 w-2.5" /> Premium</div>}
                  <div className={`${f.bg} ${f.color} w-11 h-11 rounded-sm flex items-center justify-center mb-4`}><Icon className="h-5 w-5" /></div>
                  <h3 className="font-playfair text-lg font-semibold mb-2 group-hover:text-gold transition-colors">{f.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{f.description}</p>
                  {f.free && <div className="mt-4 text-xs text-green-500 font-semibold uppercase tracking-wider flex items-center gap-1"><Check className="h-3 w-3" /> Free forever</div>}
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* TESTIMONIALS */}
      <section ref={ref('testimonials')} className="py-20 px-4 border-t border-border/50" style={anim('testimonials', 100)}>
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <div className="inline-flex items-center gap-2 text-gold text-xs font-semibold uppercase tracking-[0.2em] mb-4"><Heart className="h-3 w-3" /> Loved by seekers</div>
            <h2 className="font-playfair text-3xl md:text-4xl font-semibold">What our community says</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {TESTIMONIALS.map((t, i) => (
              <div key={i} className="p-6 rounded-sm border border-border bg-card flex flex-col gap-4">
                <div className="flex gap-0.5">{[...Array(t.stars)].map((_, j) => <span key={j} className="text-gold text-sm">★</span>)}</div>
                <p className="text-sm text-muted-foreground leading-relaxed flex-1 font-playfair italic">"{t.text}"</p>
                <div className="flex items-center gap-3 pt-2 border-t border-border">
                  <div className="w-9 h-9 rounded-full bg-gold/15 flex items-center justify-center text-lg leading-none">{t.sign}</div>
                  <div><p className="text-sm font-semibold">{t.name}</p><p className="text-xs text-muted-foreground">{t.signName}</p></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* PRICING */}
      <section id="pricing" ref={ref('pricing')} className="py-20 px-4 border-t border-border/50" style={anim('pricing', 100)}>
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-14">
            <div className="inline-flex items-center gap-2 text-gold text-xs font-semibold uppercase tracking-[0.2em] mb-4"><Crown className="h-3 w-3" /> Simple pricing</div>
            <h2 className="font-playfair text-3xl md:text-4xl font-semibold mb-4">Start free. Go deeper when ready.</h2>
            <p className="text-muted-foreground max-w-lg mx-auto">No hidden fees. Cancel anytime. Your cosmic journey begins for free.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {PLANS.map((plan) => (
              <div key={plan.name} className={`relative p-6 rounded-sm border flex flex-col gap-5 transition-all ${plan.highlight ? 'border-gold bg-gold/5 shadow-[0_0_40px_-10px_rgba(197,160,89,0.3)]' : 'border-border bg-card'}`}>
                {plan.highlight && <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gold text-primary-foreground text-[10px] font-bold uppercase tracking-widest px-4 py-1 rounded-full whitespace-nowrap">Most Popular</div>}
                <div>
                  <h3 className="font-cinzel font-bold text-lg mb-1">{plan.name}</h3>
                  <p className="text-xs text-muted-foreground">{plan.description}</p>
                </div>
                <div className="flex items-end gap-1">
                  <span className="text-3xl font-bold font-playfair">{plan.price}</span>
                  <span className="text-sm text-muted-foreground mb-1">/ {plan.period}</span>
                </div>
                <ul className="space-y-2.5 flex-1">
                  {plan.features.map((f) => (
                    <li key={f} className="flex items-start gap-2.5 text-sm">
                      <Check className="h-4 w-4 text-gold flex-shrink-0 mt-0.5" />
                      <span className="text-muted-foreground">{f}</span>
                    </li>
                  ))}
                </ul>
                <button onClick={() => navigate('/register')} className={`w-full py-3 rounded-sm font-semibold text-sm transition-all hover:-translate-y-0.5 ${plan.highlight ? 'bg-gold hover:bg-gold/90 text-primary-foreground hover:shadow-[0_8px_20px_-5px_rgba(197,160,89,0.4)]' : 'border border-border hover:border-gold/50 text-foreground'}`}>
                  {plan.cta}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FINAL CTA */}
      <section ref={ref('cta')} className="py-24 px-4 border-t border-border/50 relative overflow-hidden" style={anim('cta')}>
        <div className="absolute inset-0 pointer-events-none" style={{ background: 'radial-gradient(ellipse 60% 60% at 50% 50%, rgba(197,160,89,0.06) 0%, transparent 70%)' }} />
        <div className="relative z-10 max-w-2xl mx-auto text-center">
          <Sparkles className="h-10 w-10 text-gold mx-auto mb-6 opacity-80" />
          <h2 className="font-cinzel font-bold text-3xl md:text-4xl mb-5 leading-snug">The stars are ready.<br />Are you?</h2>
          <p className="text-muted-foreground mb-8 text-lg font-playfair">Join thousands of seekers discovering their cosmic path every day.</p>
          <button onClick={() => navigate('/register')} className="group inline-flex items-center gap-2 bg-gold hover:bg-gold/90 text-primary-foreground px-10 py-4 rounded-sm font-semibold text-base transition-all hover:shadow-[0_8px_30px_-5px_rgba(197,160,89,0.5)] hover:-translate-y-0.5">
            Create Free Account <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
          </button>
          <p className="mt-4 text-xs text-muted-foreground">No credit card required · Free forever plan available</p>
        </div>
      </section>

      <Footer />
    </div>
  );
};
