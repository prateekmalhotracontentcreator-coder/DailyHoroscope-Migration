import React, { useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useLocation } from 'react-router-dom';
import { ArrowRight, LoaderCircle, Mail, Sparkles } from 'lucide-react';
import { API } from './faithShared';

const TRACKS = [
  { value: 'anxiety', label: 'Anxiety and calm' },
  { value: 'career', label: 'Career reset' },
  { value: 'relationship', label: 'Relationship healing' },
  { value: 'grief', label: 'Grief and comfort' },
  { value: 'fresh-start', label: 'Fresh start' },
  { value: 'mercury-retrograde', label: 'Mercury retrograde' },
];

const THEMES = {
  gold: {
    shell: 'border-[#d4af37]/18 bg-white/[0.05]',
    badge: 'border-[#d4af37]/25 bg-[#d4af37]/10 text-[#f3d27a]',
    title: 'text-stone-50',
    body: 'text-stone-300',
    input: 'border-[#d4af37]/16 bg-white/[0.04] text-stone-100 placeholder:text-stone-500',
    button: 'bg-[#d4af37] text-stone-950 hover:opacity-90',
    ghost: 'border-[#d4af37]/18 bg-white/[0.04] text-stone-100 hover:border-[#d4af37]/35 hover:bg-white/[0.07]',
    link: 'text-[#f6dda0]',
  },
  emerald: {
    shell: 'border-emerald-300/18 bg-white/[0.05]',
    badge: 'border-emerald-300/25 bg-emerald-400/10 text-emerald-200',
    title: 'text-stone-50',
    body: 'text-stone-300',
    input: 'border-emerald-300/16 bg-white/[0.04] text-stone-100 placeholder:text-stone-500',
    button: 'bg-emerald-300 text-slate-950 hover:opacity-90',
    ghost: 'border-emerald-300/18 bg-white/[0.04] text-stone-100 hover:border-emerald-300/35 hover:bg-white/[0.07]',
    link: 'text-emerald-200',
  },
  sky: {
    shell: 'border-sky-300/18 bg-white/[0.05]',
    badge: 'border-sky-300/25 bg-sky-400/10 text-sky-200',
    title: 'text-stone-50',
    body: 'text-stone-300',
    input: 'border-sky-300/16 bg-white/[0.04] text-stone-100 placeholder:text-stone-500',
    button: 'bg-sky-300 text-slate-950 hover:opacity-90',
    ghost: 'border-sky-300/18 bg-white/[0.04] text-stone-100 hover:border-sky-300/35 hover:bg-white/[0.07]',
    link: 'text-sky-200',
  },
};

export function FaithGrowthPanel({
  theme = 'gold',
  sourceTag = 'faith',
  title = 'Start a guided Faith journey',
  body = 'Join the Faith updates list to help us shape devotional follow-ups, guided pathways, and scripture plans around what readers need most.',
}) {
  const location = useLocation();
  const palette = THEMES[theme] || THEMES.gold;
  const [form, setForm] = useState({ name: '', email: '', track: 'anxiety' });
  const [status, setStatus] = useState({ type: '', message: '' });
  const [submitting, setSubmitting] = useState(false);
  const sourcePath = useMemo(() => location.pathname.replace(/^\/+/, '') || 'faith', [location.pathname]);

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    setStatus({ type: '', message: '' });

    try {
      const response = await axios.post(`${API}/subscribe`, {
        name: form.name,
        email: form.email,
        track: form.track,
        source_path: sourcePath,
        tags: [sourceTag, `page-${sourceTag}`],
      });
      setStatus({
        type: 'success',
        message: response.data?.message || 'You are on the Faith journey list.',
      });
      setForm((current) => ({ ...current, email: '' }));
    } catch (error) {
      setStatus({
        type: 'error',
        message: error?.response?.data?.detail || 'Unable to save your Faith signup right now.',
      });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className={`mt-8 rounded-[1.9rem] border p-7 ${palette.shell}`}>
      <div className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
        <div>
          <div className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] ${palette.badge}`}>
            <Mail className="h-3.5 w-3.5" />
            Growth Layer
          </div>
          <h2 className={`mt-4 font-playfair text-3xl font-semibold ${palette.title}`}>{title}</h2>
          <p className={`mt-4 max-w-2xl text-sm leading-8 ${palette.body}`}>{body}</p>
          <div className="mt-6 grid gap-3 sm:grid-cols-3">
            <Link to="/faith/pathways" className={`rounded-[1.2rem] border px-4 py-4 text-sm font-semibold transition ${palette.ghost}`}>
              Guided pathways
            </Link>
            <Link to="/lumina" className={`rounded-[1.2rem] border px-4 py-4 text-sm font-semibold transition ${palette.ghost}`}>
              Start in Lumina
            </Link>
            <Link to="/premium-reports" className={`rounded-[1.2rem] border px-4 py-4 text-sm font-semibold transition ${palette.ghost}`}>
              Premium reports
            </Link>
          </div>
          <p className={`mt-5 text-xs uppercase tracking-[0.18em] ${palette.link}`}>
            Phase A focus: capture intent, deepen sessions, and route readers into devotional journeys.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="rounded-[1.5rem] border border-white/10 bg-black/10 p-5">
          <div className="flex items-center gap-2 text-sm font-semibold text-stone-100">
            <Sparkles className="h-4 w-4" />
            Join the Faith updates list
          </div>
          <div className="mt-5 grid gap-3">
            <input
              type="text"
              value={form.name}
              onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))}
              placeholder="Your name"
              className={`rounded-[1rem] border px-4 py-3 text-sm outline-none transition focus:border-white/30 ${palette.input}`}
              required
            />
            <input
              type="email"
              value={form.email}
              onChange={(event) => setForm((current) => ({ ...current, email: event.target.value }))}
              placeholder="Email address"
              className={`rounded-[1rem] border px-4 py-3 text-sm outline-none transition focus:border-white/30 ${palette.input}`}
              required
            />
            <select
              value={form.track}
              onChange={(event) => setForm((current) => ({ ...current, track: event.target.value }))}
              className={`rounded-[1rem] border px-4 py-3 text-sm outline-none transition focus:border-white/30 ${palette.input}`}
            >
              {TRACKS.map((item) => (
                <option key={item.value} value={item.value} className="bg-slate-900 text-stone-100">
                  {item.label}
                </option>
              ))}
            </select>
          </div>
          <button
            type="submit"
            disabled={submitting}
            className={`mt-5 inline-flex w-full items-center justify-center rounded-full px-5 py-3 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-70 ${palette.button}`}
          >
            {submitting ? (
              <>
                <LoaderCircle className="mr-2 h-4 w-4 animate-spin" />
                Saving your path
              </>
            ) : (
              <>
                Join the Faith journey
                <ArrowRight className="ml-2 h-4 w-4" />
              </>
            )}
          </button>
          {status.message ? (
            <p className={`mt-4 text-sm leading-7 ${status.type === 'error' ? 'text-rose-200' : 'text-emerald-200'}`}>{status.message}</p>
          ) : null}
        </form>
      </div>
    </section>
  );
}
