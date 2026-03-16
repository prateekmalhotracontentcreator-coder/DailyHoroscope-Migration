import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';
import { PaymentModal } from '../components/PaymentModal';
import { Card } from '../components/ui/card';
import {
  Crown, Check, X, Sparkles, Star, Heart, Sun,
  Calendar, TrendingUp, ArrowRight, Shield
} from 'lucide-react';

const PLANS = [
  {
    id: 'free',
    name: 'Free',
    price: '₹0',
    period: 'forever',
    description: 'Start your cosmic journey',
    highlight: false,
    cta: 'Get Started Free',
    ctaAction: 'register',
    color: 'border-border',
    icon: Sun,
    features: [
      { text: 'Daily horoscope for your sign', included: true },
      { text: 'Weekly forecast', included: true },
      { text: 'Monthly outlook', included: true },
      { text: 'Cosmic Blog access', included: true },
      { text: 'Birth Chart Analysis', included: false },
      { text: 'Kundali Milan', included: false },
      { text: 'Brihat Kundli Pro', included: false },
      { text: 'PDF downloads', included: false },
    ],
  },
  {
    id: 'premium_monthly',
    name: 'Premium',
    price: '₹1,599',
    period: 'per month',
    description: 'Unlimited cosmic access',
    highlight: true,
    cta: 'Start Premium',
    ctaAction: 'pay',
    color: 'border-gold',
    icon: Crown,
    features: [
      { text: 'Daily horoscope for your sign', included: true },
      { text: 'Weekly forecast', included: true },
      { text: 'Monthly outlook', included: true },
      { text: 'Cosmic Blog access', included: true },
      { text: 'Unlimited Birth Chart reports', included: true },
      { text: 'Unlimited Kundali Milan', included: true },
      { text: 'PDF downloads', included: true },
      { text: 'Priority AI generation', included: true },
    ],
  },
  {
    id: 'birth_chart',
    name: 'Birth Chart',
    price: '₹799',
    period: 'one-time',
    description: 'Your Vedic birth chart',
    highlight: false,
    cta: 'Get Birth Chart',
    ctaAction: 'pay',
    color: 'border-border',
    icon: Star,
    features: [
      { text: 'Full Vedic birth chart', included: true },
      { text: 'Planetary positions & houses', included: true },
      { text: 'Personality & life path', included: true },
      { text: 'Career & wealth insights', included: true },
      { text: 'PDF download', included: true },
      { text: 'Unlimited regeneration', included: false },
      { text: 'Dasha timeline', included: false },
      { text: 'Remedies & gemstones', included: false },
    ],
  },
  {
    id: 'kundali_milan',
    name: 'Kundali Milan',
    price: '₹1,199',
    period: 'one-time',
    description: 'Marriage compatibility report',
    highlight: false,
    cta: 'Get Compatibility',
    ctaAction: 'pay',
    color: 'border-border',
    icon: Heart,
    features: [
      { text: 'Guna Milan (36 points)', included: true },
      { text: 'Mangal Dosha analysis', included: true },
      { text: 'Compatibility score & verdict', included: true },
      { text: 'Relationship strengths', included: true },
      { text: 'PDF download', included: true },
      { text: 'Auspicious wedding dates', included: true },
      { text: 'Remedies for doshas', included: true },
      { text: 'Unlimited reports', included: false },
    ],
  },
  {
    id: 'brihat_kundli',
    name: 'Brihat Kundli Pro',
    price: '₹1,499',
    period: 'one-time',
    description: 'The ultimate Vedic life report',
    highlight: false,
    cta: 'Get Full Report',
    ctaAction: 'navigate',
    navigateTo: '/brihat-kundli',
    color: 'border-purple-500/40',
    icon: Crown,
    features: [
      { text: '40+ page comprehensive report', included: true },
      { text: 'All 9 planetary positions', included: true },
      { text: 'Full dasha timeline', included: true },
      { text: 'Career, love, wealth & health', included: true },
      { text: 'Dosha & yoga analysis', included: true },
      { text: 'Gemstone & mantra remedies', included: true },
      { text: 'Numerology reading', included: true },
      { text: 'PDF download', included: true },
    ],
  },
];

const FAQ = [
  {
    q: 'Can I cancel my Premium subscription anytime?',
    a: 'Yes. Cancel any time from Account Settings. You keep access until the end of your billing period — no mid-cycle refunds.',
  },
  {
    q: 'Are the one-time reports really one-time?',
    a: 'Yes. Birth Chart, Kundali Milan, and Brihat Kundli Pro are single purchases. You can view your generated report any time from your account.',
  },
  {
    q: 'How accurate are the AI-generated reports?',
    a: 'Reports are generated using Claude Sonnet, our most capable AI, trained on Vedic astrology principles. They are for reflective and informational purposes — not a substitute for professional consultation.',
  },
  {
    q: 'What payment methods are accepted?',
    a: 'All major cards, UPI, net banking, and wallets via Razorpay — India\'s most trusted payment gateway.',
  },
  {
    q: 'Is my birth data safe?',
    a: 'Yes. Your data is stored securely and never shared with third parties. See our Privacy Policy for full details.',
  },
];

export const PricingPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [paymentPlan, setPaymentPlan] = useState(null);
  const [openFaq, setOpenFaq] = useState(null);

  const handleCta = (plan) => {
    if (plan.ctaAction === 'register') {
      navigate(user ? '/home' : '/register');
    } else if (plan.ctaAction === 'navigate') {
      navigate(user ? plan.navigateTo : '/register');
    } else if (plan.ctaAction === 'pay') {
      if (!user) {
        navigate('/register', { state: { from: { pathname: '/pricing' } } });
        return;
      }
      setPaymentPlan(plan);
    }
  };

  const handlePaymentSuccess = (plan) => {
    setPaymentPlan(null);
    // Navigate to the relevant page after payment
    const destinations = {
      premium_monthly: '/home',
      birth_chart: '/birth-chart',
      kundali_milan: '/kundali-milan',
      brihat_kundli: '/brihat-kundli',
    };
    navigate(destinations[plan.id] || '/home');
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1">
        {/* Hero */}
        <div className="text-center py-16 px-4">
          <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-[0.2em] px-4 py-2 rounded-full mb-6">
            <Sparkles className="h-3 w-3" /> Simple, transparent pricing
          </div>
          <h1 className="font-playfair text-4xl md:text-5xl font-semibold mb-4">
            Choose your cosmic plan
          </h1>
          <p className="text-muted-foreground max-w-xl mx-auto text-lg">
            Start free. Upgrade when you're ready. All plans secured by Razorpay.
          </p>
        </div>

        {/* Plans grid */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-5">
            {PLANS.map((plan) => {
              const Icon = plan.icon;
              return (
                <div
                  key={plan.id}
                  className={`relative flex flex-col rounded-sm border bg-card transition-all hover:-translate-y-1 hover:shadow-[0_8px_30px_-5px_rgba(0,0,0,0.1)] ${plan.color} ${plan.highlight ? 'shadow-[0_0_40px_-10px_rgba(197,160,89,0.3)] bg-gold/5' : ''}`}
                >
                  {plan.highlight && (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gold text-primary-foreground text-[10px] font-bold uppercase tracking-widest px-4 py-1 rounded-full whitespace-nowrap">
                      Most Popular
                    </div>
                  )}

                  <div className="p-5 flex flex-col gap-4 flex-1">
                    {/* Header */}
                    <div>
                      <div className={`w-9 h-9 rounded-sm flex items-center justify-center mb-3 ${plan.highlight ? 'bg-gold/20 text-gold' : 'bg-muted text-muted-foreground'}`}>
                        <Icon className="h-4 w-4" />
                      </div>
                      <h3 className="font-cinzel font-bold text-base">{plan.name}</h3>
                      <p className="text-xs text-muted-foreground mt-0.5">{plan.description}</p>
                    </div>

                    {/* Price */}
                    <div className="flex items-end gap-1">
                      <span className={`text-2xl font-bold font-playfair ${plan.highlight ? 'text-gold' : ''}`}>{plan.price}</span>
                      <span className="text-xs text-muted-foreground mb-1">/ {plan.period}</span>
                    </div>

                    {/* Features */}
                    <ul className="space-y-2 flex-1">
                      {plan.features.map((f, i) => (
                        <li key={i} className="flex items-start gap-2 text-xs">
                          {f.included
                            ? <Check className="h-3.5 w-3.5 text-gold flex-shrink-0 mt-0.5" />
                            : <X className="h-3.5 w-3.5 text-muted-foreground/40 flex-shrink-0 mt-0.5" />
                          }
                          <span className={f.included ? 'text-foreground' : 'text-muted-foreground/60'}>{f.text}</span>
                        </li>
                      ))}
                    </ul>

                    {/* CTA */}
                    <button
                      onClick={() => handleCta(plan)}
                      className={`w-full py-2.5 rounded-sm text-sm font-semibold transition-all hover:-translate-y-0.5 flex items-center justify-center gap-1.5 mt-2 ${
                        plan.highlight
                          ? 'bg-gold hover:bg-gold/90 text-primary-foreground hover:shadow-[0_6px_20px_-5px_rgba(197,160,89,0.5)]'
                          : 'border border-border hover:border-gold/50 text-foreground'
                      }`}
                    >
                      {plan.cta}
                      <ArrowRight className="h-3.5 w-3.5" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Trust bar */}
          <div className="flex flex-wrap items-center justify-center gap-6 mt-12 text-sm text-muted-foreground">
            {[
              { icon: Shield, text: 'Secured by Razorpay' },
              { icon: Check, text: 'Cancel anytime' },
              { icon: Sparkles, text: 'Powered by Claude AI' },
              { icon: Star, text: '10,000+ reports generated' },
            ].map(({ icon: Icon, text }) => (
              <div key={text} className="flex items-center gap-2">
                <Icon className="h-4 w-4 text-gold" />
                <span>{text}</span>
              </div>
            ))}
          </div>

          {/* Comparison note */}
          <Card className="mt-12 p-6 border border-gold/20 bg-gold/5 max-w-2xl mx-auto text-center">
            <Crown className="h-6 w-6 text-gold mx-auto mb-3" />
            <h3 className="font-playfair font-semibold text-lg mb-2">Not sure which to choose?</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Start with the free plan — no card needed. Upgrade to Premium for unlimited Birth Charts and Kundali Milan. Or pick a one-time report if you just need one deep analysis.
            </p>
            <button
              onClick={() => navigate(user ? '/home' : '/register')}
              className="inline-flex items-center gap-2 bg-gold hover:bg-gold/90 text-primary-foreground px-6 py-2.5 rounded-sm text-sm font-semibold transition-all"
            >
              Start for free <ArrowRight className="h-4 w-4" />
            </button>
          </Card>

          {/* FAQ */}
          <div className="max-w-2xl mx-auto mt-16">
            <h2 className="font-playfair text-2xl font-semibold text-center mb-8">Frequently asked questions</h2>
            <div className="space-y-3">
              {FAQ.map((faq, i) => (
                <div key={i} className="border border-border rounded-sm overflow-hidden">
                  <button
                    onClick={() => setOpenFaq(openFaq === i ? null : i)}
                    className="w-full flex items-center justify-between px-5 py-4 text-left hover:bg-muted/30 transition-colors"
                  >
                    <span className="text-sm font-medium pr-4">{faq.q}</span>
                    <span className="text-muted-foreground text-lg flex-shrink-0">{openFaq === i ? '−' : '+'}</span>
                  </button>
                  {openFaq === i && (
                    <div className="px-5 pb-4 text-sm text-muted-foreground border-t border-border pt-3">
                      {faq.a}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>

      <Footer />

      {/* Payment modal */}
      {paymentPlan && (
        <PaymentModal
          isOpen={!!paymentPlan}
          onClose={() => setPaymentPlan(null)}
          reportType={paymentPlan.id}
          reportId="new"
          onSuccess={() => handlePaymentSuccess(paymentPlan)}
        />
      )}
    </div>
  );
};
