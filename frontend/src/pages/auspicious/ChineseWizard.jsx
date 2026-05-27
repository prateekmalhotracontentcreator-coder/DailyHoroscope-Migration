import React, { useEffect, useMemo, useState } from "react";
import { ArrowLeft, ShieldCheck, CalendarDays } from "lucide-react";
import { Switch } from "../../components/ui/switch";

const ANIMALS = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"];

function deriveAnimal(birthDate) {
  if (!birthDate) return null;
  const year = Number.parseInt(String(birthDate).slice(0, 4), 10);
  if (Number.isNaN(year)) return null;
  return ANIMALS[(year - 4) % 12];
}

const VECTOR_EMOJI = {
  build: "🏛️",
  contract: "✍️",
  release: "🌿",
  travel: "🧭",
};

export default function ChineseWizard({
  vectors,
  form,
  busy,
  categoryLabel,
  onBack,
  onSubmit,
  onSkip,
}) {
  const [draft, setDraft] = useState(form);

  useEffect(() => {
    setDraft(form);
  }, [form]);

  const userAnimal = useMemo(() => deriveAnimal(draft.birth_date), [draft.birth_date]);

  return (
    <section className="rounded-[2rem] border border-gold/20 bg-white/80 p-6 shadow-sm sm:p-8">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Module 2 · Chinese Tong Shu Wizard</p>
          <h2 className="mt-3 font-cinzel text-3xl text-stone-900">Add personal timing filters before the combined score</h2>
          <p className="mt-3 max-w-3xl text-sm leading-7 text-stone-600">
            This layer derives the zodiac animal from birth year, reads the 12 Day Officers, and optionally blocks
            personal clash dates.
          </p>
        </div>
        <div className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.22em] text-stone-700">
          {categoryLabel}
        </div>
      </div>

      <div className="mt-8 grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
        <div className="space-y-6 rounded-[1.75rem] border border-gold/15 bg-gradient-to-br from-white to-gold/10 p-5">
          <div>
            <div className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-full bg-gold text-sm font-semibold text-stone-950">1</span>
              <div>
                <p className="text-sm font-semibold text-stone-900">Birth date</p>
                <p className="text-xs text-stone-500">Used only for Chinese zodiac clash shielding in this phase.</p>
              </div>
            </div>

            <label className="mt-4 block text-xs font-semibold uppercase tracking-[0.22em] text-stone-500">Birth date</label>
            <div className="relative mt-2">
              <CalendarDays className="pointer-events-none absolute left-4 top-3.5 h-4 w-4 text-stone-400" />
              <input
                type="date"
                value={draft.birth_date || ""}
                onChange={(event) => setDraft((current) => ({ ...current, birth_date: event.target.value }))}
                className="w-full rounded-2xl border border-gold/20 bg-white/85 py-3 pl-11 pr-4 text-sm text-stone-900 outline-none transition focus:border-gold"
              />
            </div>

            <div className="mt-4 rounded-[1.4rem] border border-gold/15 bg-white/80 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Derived zodiac animal</p>
              <p className="mt-2 font-playfair text-2xl font-semibold text-stone-900">
                {userAnimal ? `${VECTOR_EMOJI[draft.activity_vector] || "🐲"} ${userAnimal}` : "Select your birth date"}
              </p>
            </div>
          </div>

          <div>
            <div className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-full bg-gold text-sm font-semibold text-stone-950">2</span>
              <div>
                <p className="text-sm font-semibold text-stone-900">Action vector</p>
                <p className="text-xs text-stone-500">This adjusts which Day Officers count as strong or weak for the intent.</p>
              </div>
            </div>

            <div className="mt-4 grid gap-3 sm:grid-cols-2">
              {vectors.map((vector) => {
                const active = draft.activity_vector === vector.slug;
                return (
                  <button
                    key={vector.slug}
                    type="button"
                    onClick={() => setDraft((current) => ({ ...current, activity_vector: vector.slug }))}
                    className={`rounded-[1.4rem] border p-4 text-left transition ${
                      active ? "border-gold bg-gold/15 shadow-sm" : "border-gold/15 bg-white/70 hover:border-gold/35"
                    }`}
                  >
                    <p className="text-sm font-semibold text-stone-900">
                      <span className="mr-2">{VECTOR_EMOJI[vector.slug] || "•"}</span>
                      {vector.display_name}
                    </p>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        <div className="rounded-[1.75rem] border border-gold/15 bg-white/85 p-5">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-full bg-gold text-sm font-semibold text-stone-950">3</span>
            <div>
              <p className="text-sm font-semibold text-stone-900">Clash shield</p>
              <p className="text-xs text-stone-500">Keeps personal clash days out of the final shortlist by default.</p>
            </div>
          </div>

          <div className="mt-5 rounded-[1.5rem] border border-gold/15 bg-gold/6 p-5">
            <label className="flex items-start justify-between gap-4">
              <span>
                <span className="flex items-center text-sm font-semibold text-stone-900">
                  <ShieldCheck className="mr-2 h-4 w-4 text-gold" />
                  Filter out my personal clash days
                </span>
                <span className="mt-1 block text-xs leading-6 text-stone-500">
                  When enabled, a clash between your zodiac animal and the day animal will hard-block that date.
                </span>
              </span>
              <Switch
                checked={draft.filter_personal_clash}
                onCheckedChange={(checked) => setDraft((current) => ({ ...current, filter_personal_clash: checked }))}
                className="data-[state=checked]:bg-gold data-[state=unchecked]:bg-stone-300"
              />
            </label>
          </div>

          <div className="mt-6 rounded-[1.5rem] border border-gold/15 bg-gradient-to-br from-white to-gold/10 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Combined system preview</p>
            <p className="mt-3 text-sm leading-7 text-stone-600">
              The final month score blends Vedic Muhurta at 55% with Chinese Tong Shu at 45%, then marks each day as
              excellent, good, neutral, or blocked.
            </p>
          </div>

          <div className="mt-8 flex flex-wrap gap-3">
            <button
              type="button"
              onClick={onBack}
              className="inline-flex items-center rounded-full border border-gold/20 bg-white px-5 py-3 text-sm font-semibold text-stone-700 transition hover:border-gold"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </button>
            <button
              type="button"
              disabled={busy}
              onClick={() => onSubmit(draft)}
              className="rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
            >
              Calculate Combined Auspicious Calendar →
            </button>
            <button
              type="button"
              disabled={busy}
              onClick={onSkip}
              className="rounded-full border border-gold/25 bg-white px-6 py-3 text-sm font-semibold text-stone-700 transition hover:border-gold disabled:cursor-not-allowed disabled:opacity-50"
            >
              Use Vedic system only
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
