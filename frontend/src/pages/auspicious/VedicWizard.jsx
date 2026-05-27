import React, { useEffect, useMemo, useState } from "react";
import { Search, MapPin, CalendarDays, Sparkles } from "lucide-react";
import { Switch } from "../../components/ui/switch";

function toMonthInputValue(value) {
  return `${value || ""}`.slice(0, 7);
}

export default function VedicWizard({
  categories,
  locations,
  form,
  busy,
  loadingCatalogs,
  onSubmit,
}) {
  const [draft, setDraft] = useState(form);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    setDraft(form);
  }, [form]);

  useEffect(() => {
    const selected = locations.find((location) => location.slug === form.city_id);
    setSearchTerm(selected ? selected.label : "");
  }, [form.city_id, locations]);

  const filteredLocations = useMemo(() => {
    const needle = searchTerm.trim().toLowerCase();
    if (!needle) return locations.slice(0, 8);
    return locations
      .filter((location) => {
        const haystack = `${location.label} ${location.city_name || ""} ${location.country || ""}`.toLowerCase();
        return haystack.includes(needle);
      })
      .slice(0, 8);
  }, [locations, searchTerm]);

  const selectedCategory = categories.find((item) => item.slug === draft.activity_category);
  const canContinue = Boolean(draft.activity_category && draft.city_id && draft.target_month);

  return (
    <section className="rounded-[2rem] border border-gold/20 bg-white/80 p-6 shadow-sm sm:p-8">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Module 1 · Vedic Wizard</p>
          <h2 className="mt-3 font-cinzel text-3xl text-stone-900">Set the intent, city, and timing filters</h2>
          <p className="mt-3 max-w-3xl text-sm leading-7 text-stone-600">
            This layer uses the live Panchang city catalogue plus the commission scoring matrix for all 10 activity
            categories.
          </p>
        </div>
        <div className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.22em] text-stone-700">
          {loadingCatalogs ? "Loading catalogue..." : `${locations.length} supported cities`}
        </div>
      </div>

      <div className="mt-8 grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
        <div>
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-full bg-gold text-sm font-semibold text-stone-950">1</span>
            <div>
              <p className="text-sm font-semibold text-stone-900">Intent selector</p>
              <p className="text-xs text-stone-500">Choose the real-world action you want to time well.</p>
            </div>
          </div>

          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            {categories.map((category) => {
              const active = draft.activity_category === category.slug;
              return (
                <button
                  key={category.slug}
                  type="button"
                  onClick={() => setDraft((current) => ({ ...current, activity_category: category.slug }))}
                  className={`rounded-[1.4rem] border p-4 text-left transition ${
                    active
                      ? "border-gold bg-gold/15 shadow-sm"
                      : "border-gold/15 bg-white/70 hover:-translate-y-0.5 hover:border-gold/35"
                  }`}
                >
                  <p className="text-sm font-semibold text-stone-900">{category.display_name}</p>
                  <p className="mt-2 text-xs leading-6 text-stone-600">
                    {category.chinese?.default_activity_vector_label || category.default_activity_vector_label}
                  </p>
                </button>
              );
            })}
          </div>
        </div>

        <div className="space-y-6 rounded-[1.75rem] border border-gold/15 bg-gradient-to-br from-white to-gold/10 p-5">
          <div>
            <div className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-full bg-gold text-sm font-semibold text-stone-950">2</span>
              <div>
                <p className="text-sm font-semibold text-stone-900">City search</p>
                <p className="text-xs text-stone-500">
                  Uses <code className="rounded bg-gold/10 px-1 py-0.5 text-[11px] text-stone-700">GET /api/panchang/locations</code> from the live Panchang catalogue.
                </p>
              </div>
            </div>

            <label className="mt-4 block text-xs font-semibold uppercase tracking-[0.22em] text-stone-500">City</label>
            <div className="relative mt-2">
              <Search className="pointer-events-none absolute left-4 top-3.5 h-4 w-4 text-stone-400" />
              <input
                value={searchTerm}
                onChange={(event) => {
                  setSearchTerm(event.target.value);
                  setDraft((current) => ({ ...current, city_id: "" }));
                }}
                placeholder="Search New Delhi, Mumbai, London..."
                className="w-full rounded-2xl border border-gold/20 bg-white/85 py-3 pl-11 pr-4 text-sm text-stone-900 outline-none transition focus:border-gold"
              />
            </div>

            <div className="mt-3 max-h-56 overflow-auto rounded-2xl border border-gold/15 bg-white/75">
              {filteredLocations.map((location) => {
                const active = draft.city_id === location.slug;
                return (
                  <button
                    key={location.slug}
                    type="button"
                    onClick={() => {
                      setDraft((current) => ({ ...current, city_id: location.slug }));
                      setSearchTerm(location.label);
                    }}
                    className={`flex w-full items-center justify-between gap-3 border-b border-gold/10 px-4 py-3 text-left last:border-b-0 ${
                      active ? "bg-gold/12" : "hover:bg-gold/6"
                    }`}
                  >
                    <span>
                      <span className="block text-sm font-medium text-stone-900">{location.label}</span>
                      <span className="block text-xs text-stone-500">{location.timezone}</span>
                    </span>
                    <MapPin className={`h-4 w-4 ${active ? "text-gold" : "text-stone-300"}`} />
                  </button>
                );
              })}
              {!filteredLocations.length ? (
                <div className="px-4 py-6 text-sm text-stone-500">No matching city found in the Panchang catalogue.</div>
              ) : null}
            </div>
          </div>

          <div>
            <div className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-full bg-gold text-sm font-semibold text-stone-950">3</span>
              <div>
                <p className="text-sm font-semibold text-stone-900">Target month and risk toggles</p>
                <p className="text-xs text-stone-500">Fine-tune how strict the Vedic layer should be.</p>
              </div>
            </div>

            <label className="mt-4 block text-xs font-semibold uppercase tracking-[0.22em] text-stone-500">Target month</label>
            <div className="relative mt-2">
              <CalendarDays className="pointer-events-none absolute left-4 top-3.5 h-4 w-4 text-stone-400" />
              <input
                type="month"
                value={toMonthInputValue(draft.target_month)}
                onChange={(event) =>
                  setDraft((current) => ({
                    ...current,
                    target_month: `${event.target.value || ""}-01`,
                  }))
                }
                className="w-full rounded-2xl border border-gold/20 bg-white/85 py-3 pl-11 pr-4 text-sm text-stone-900 outline-none transition focus:border-gold"
              />
            </div>

            <div className="mt-5 space-y-4 rounded-[1.5rem] border border-gold/15 bg-white/80 p-4">
              <label className="flex items-start justify-between gap-4">
                <span>
                  <span className="block text-sm font-semibold text-stone-900">Filter Mercury Retrograde periods</span>
                  <span className="block text-xs leading-6 text-stone-500">
                    Best for job entries, launches, and travel-heavy timing windows.
                  </span>
                </span>
                <Switch
                  checked={draft.avoid_retrogrades}
                  onCheckedChange={(checked) => setDraft((current) => ({ ...current, avoid_retrogrades: checked }))}
                  className="data-[state=checked]:bg-gold data-[state=unchecked]:bg-stone-300"
                />
              </label>

              <label className="flex items-start justify-between gap-4">
                <span>
                  <span className="block text-sm font-semibold text-stone-900">Exclude Rahu Kalam conflicts</span>
                  <span className="block text-xs leading-6 text-stone-500">
                    Softens recommendations when the premium timing window collides with Rahu Kaal.
                  </span>
                </span>
                <Switch
                  checked={draft.exclude_rahu_kalam}
                  onCheckedChange={(checked) => setDraft((current) => ({ ...current, exclude_rahu_kalam: checked }))}
                  className="data-[state=checked]:bg-gold data-[state=unchecked]:bg-stone-300"
                />
              </label>
            </div>

            <div className="mt-6 flex flex-wrap gap-3">
              <button
                type="button"
                disabled={!canContinue || busy}
                onClick={() => onSubmit(draft, "dual")}
                className="inline-flex items-center rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <Sparkles className="mr-2 h-4 w-4" />
                Calculate Vedic Auspicious Days →
              </button>
              <button
                type="button"
                disabled={!canContinue || busy}
                onClick={() => onSubmit(draft, "vedic")}
                className="rounded-full border border-gold/25 bg-white px-6 py-3 text-sm font-semibold text-stone-700 transition hover:border-gold disabled:cursor-not-allowed disabled:opacity-50"
              >
                Use Vedic system only
              </button>
            </div>
          </div>
        </div>
      </div>

      {selectedCategory ? (
        <div className="mt-6 rounded-[1.5rem] border border-gold/15 bg-gold/6 p-4 text-sm leading-7 text-stone-700">
          <span className="font-semibold text-stone-900">Selected intent:</span> {selectedCategory.display_name}
        </div>
      ) : null}
    </section>
  );
}
