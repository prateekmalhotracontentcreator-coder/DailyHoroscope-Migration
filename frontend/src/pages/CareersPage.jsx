import React, { useState } from 'react';
import { Briefcase, MapPin, Clock, ChevronDown, ChevronUp, Star, Zap, Heart } from 'lucide-react';
import { SEO } from '../components/SEO';

const OPEN_ROLES = [
  {
    id: 'fe-eng',
    title: 'Frontend Engineer (React)',
    team: 'Product',
    location: 'Remote — India',
    type: 'Full-time',
    level: 'Mid / Senior',
    description:
      "We're looking for a React engineer who loves crafting delightful, pixel-perfect UIs. You'll work across our Panchang, Palmistry, Lumina, and Horoscope modules — shipping features that reach millions of seekers.",
    responsibilities: [
      'Build and maintain React components with Tailwind CSS',
      'Collaborate with the design and backend teams on new features',
      'Improve performance, accessibility, and SEO across all pages',
      'Own the frontend build pipeline (CRA/CRACO/Vercel)',
    ],
    requirements: [
      '3+ years of production React experience',
      'Strong command of Tailwind CSS and responsive design',
      'Familiarity with REST APIs and async data patterns',
      'Bonus: Interest in Vedic astrology, spirituality, or wellness apps',
    ],
  },
  {
    id: 'python-backend',
    title: 'Python Backend Engineer (FastAPI)',
    team: 'Engineering',
    location: 'Remote — India',
    type: 'Full-time',
    level: 'Mid / Senior',
    description:
      'Help us power the Vedic computation engines behind Everyday Horoscope — Swiss Ephemeris astronomy, AI report generation, and scalable MongoDB pipelines.',
    responsibilities: [
      'Maintain and extend our FastAPI services on Render',
      'Work on pyswisseph-based Panchang and birth chart engines',
      'Integrate Claude / Gemini AI APIs for dynamic report generation',
      'Ensure reliability, monitoring, and performance of all backend services',
    ],
    requirements: [
      '3+ years Python; 1+ year FastAPI or similar async framework',
      'Experience with MongoDB (Motor async driver preferred)',
      'Comfortable with Docker-based deployments',
      'Bonus: Astronomy / astrology computation background',
    ],
  },
  {
    id: 'content-astrologer',
    title: 'Vedic Astrologer & Content Lead',
    team: 'Content',
    location: 'Remote — India / Global',
    type: 'Contract / Part-time',
    level: 'Expert',
    description:
      'We need a practicing Jyotishi to validate our AI-generated content, guide accuracy benchmarks, and author monthly deep-dive articles for our growing audience.',
    responsibilities: [
      'Review and validate horoscope, Panchang, and palmistry content',
      'Write 4–6 monthly articles covering transits, yogas, and festivals',
      'Define accuracy benchmarks for our computation engines',
      'Consult on new product features rooted in Vedic tradition',
    ],
    requirements: [
      'Formal training or certification in Jyotish / Vedic Astrology',
      'Strong written English (Hindi a bonus)',
      'Familiarity with Drik Panchang, KP System, or Parashari system',
      'Portfolio of published astrology content preferred',
    ],
  },
  {
    id: 'growth-marketer',
    title: 'Growth Marketer — Organic & SEO',
    team: 'Growth',
    location: 'Remote — India',
    type: 'Full-time',
    level: 'Mid',
    description:
      'Own our organic acquisition — SEO, content strategy, social media, and App Store optimisation — as we scale from 10k to 1M monthly users.',
    responsibilities: [
      'Drive keyword research and on-page SEO across 500+ pages',
      'Manage content calendar and coordinate blog / social output',
      'Track and improve GSC, GA4, and App Store metrics',
      'Run WhatsApp / email notification campaigns via our admin console',
    ],
    requirements: [
      '2+ years of SEO or content marketing in a product-led company',
      'Hands-on experience with Google Search Console and GA4',
      'Data-driven — comfortable with dashboards and weekly reporting',
      'Bonus: Passion for astrology, wellness, or spiritual apps',
    ],
  },
];

const WHY_US = [
  { icon: Star,      title: 'Purpose-driven product',    desc: 'Everyday Horoscope serves millions of seekers across India and the diaspora. Your work has real meaning.' },
  { icon: Zap,       title: 'Move fast, own big things',  desc: 'Small, focused team. No bureaucracy. Ship features in days, not quarters.' },
  { icon: Heart,     title: 'Remote-first, async-first',  desc: 'Work from anywhere in India (or the world). Flexible hours, results-driven culture.' },
  { icon: Briefcase, title: 'Competitive compensation',   desc: 'Market-rate salaries, equity for senior hires, and a performance bonus tied to product milestones.' },
];

export function CareersPage() {
  const [openRole, setOpenRole] = useState(null);

  return (
    <div className="min-h-screen bg-background">
      <SEO
        title="Careers — Everyday Horoscope"
        description="Join the team building India's premium Vedic astrology platform. Open roles in engineering, content, and growth."
        url="https://www.everydayhoroscope.in/careers"
      />

      <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">

        {/* Hero */}
        <div className="mb-12 text-center">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/5 px-4 py-1.5 text-xs font-semibold uppercase tracking-widest text-gold">
            <Briefcase className="h-3.5 w-3.5" /> We're hiring
          </div>
          <h1 className="mb-4 font-playfair text-4xl font-semibold sm:text-5xl">
            Build the future of <span className="text-gold">Vedic wisdom</span>
          </h1>
          <p className="mx-auto max-w-2xl text-base leading-7 text-muted-foreground">
            Everyday Horoscope is India's premium Vedic astrology platform — blending 5,000 years of ancient wisdom with modern AI. We're a small, mission-driven team and we'd love your help.
          </p>
        </div>

        {/* Why us */}
        <div className="mb-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {WHY_US.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="rounded-2xl border border-gold/20 bg-gold/[0.04] p-5">
              <div className="mb-3 inline-flex rounded-full border border-gold/25 bg-gold/10 p-2 text-gold">
                <Icon className="h-4 w-4" />
              </div>
              <p className="mb-1 font-semibold text-foreground">{title}</p>
              <p className="text-sm leading-6 text-muted-foreground">{desc}</p>
            </div>
          ))}
        </div>

        {/* Open roles */}
        <h2 className="mb-6 font-playfair text-2xl font-semibold text-foreground">Open Roles</h2>
        <div className="space-y-4">
          {OPEN_ROLES.map((role) => {
            const isOpen = openRole === role.id;
            return (
              <div key={role.id} className="overflow-hidden rounded-2xl border border-gold/20 bg-gold/[0.03]">
                {/* Role header — always visible */}
                <button
                  type="button"
                  onClick={() => setOpenRole(isOpen ? null : role.id)}
                  className="flex w-full items-start justify-between gap-4 p-5 text-left transition hover:bg-gold/[0.06]"
                >
                  <div className="space-y-1.5">
                    <p className="font-semibold text-foreground">{role.title}</p>
                    <div className="flex flex-wrap gap-2">
                      <span className="inline-flex items-center gap-1 rounded-full border border-gold/20 bg-background px-2.5 py-0.5 text-xs text-muted-foreground">
                        <MapPin className="h-3 w-3" /> {role.location}
                      </span>
                      <span className="inline-flex items-center gap-1 rounded-full border border-gold/20 bg-background px-2.5 py-0.5 text-xs text-muted-foreground">
                        <Clock className="h-3 w-3" /> {role.type}
                      </span>
                      <span className="rounded-full border border-gold/25 bg-gold/10 px-2.5 py-0.5 text-xs font-semibold text-gold">
                        {role.team}
                      </span>
                    </div>
                  </div>
                  {isOpen ? (
                    <ChevronUp className="mt-1 h-5 w-5 flex-shrink-0 text-gold" />
                  ) : (
                    <ChevronDown className="mt-1 h-5 w-5 flex-shrink-0 text-muted-foreground" />
                  )}
                </button>

                {/* Expanded detail */}
                {isOpen && (
                  <div className="border-t border-gold/15 px-5 pb-6 pt-5 space-y-5">
                    <p className="text-sm leading-7 text-muted-foreground">{role.description}</p>

                    <div className="grid gap-5 md:grid-cols-2">
                      <div>
                        <p className="mb-2 text-xs font-semibold uppercase tracking-[0.22em] text-gold">Responsibilities</p>
                        <ul className="space-y-1.5">
                          {role.responsibilities.map((r) => (
                            <li key={r} className="flex items-start gap-2 text-sm text-muted-foreground">
                              <span className="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-gold" />
                              {r}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <p className="mb-2 text-xs font-semibold uppercase tracking-[0.22em] text-gold">Requirements</p>
                        <ul className="space-y-1.5">
                          {role.requirements.map((r) => (
                            <li key={r} className="flex items-start gap-2 text-sm text-muted-foreground">
                              <span className="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-gold" />
                              {r}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    <a
                      href={`mailto:careers@everydayhoroscope.in?subject=Application: ${encodeURIComponent(role.title)}`}
                      className="inline-block rounded-full bg-gold px-6 py-2.5 text-sm font-semibold text-primary-foreground transition hover:bg-gold/90"
                    >
                      Apply for this role →
                    </a>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* General application */}
        <div className="mt-10 rounded-2xl border border-gold/20 bg-gold/[0.04] p-6 text-center">
          <p className="mb-1 font-semibold text-foreground">Don't see your role?</p>
          <p className="mb-4 text-sm text-muted-foreground">
            We're always interested in meeting talented people. Send us a note with what you do and why you love Vedic astrology.
          </p>
          <a
            href="mailto:careers@everydayhoroscope.in?subject=General Application"
            className="inline-block rounded-full border border-gold/30 bg-background px-6 py-2.5 text-sm font-semibold text-foreground transition hover:bg-gold/10"
          >
            Send a general application
          </a>
        </div>

      </div>
    </div>
  );
}

export default CareersPage;
