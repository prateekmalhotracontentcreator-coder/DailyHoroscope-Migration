# TAR-DESIGN-1 Commission Brief -- Tarot Module UI/UX Upgrade
> Commission ID: TAR-DESIGN-1
> Thread: Claude Design (dedicated design thread)
> Date: 2026-06-18
> Status: READY TO ISSUE
> Depends on: TAR-SEO-1 ✅ · TAR-SEO-2 ✅ · TAR-v4 ✅ · SVG deck (78 cards -- pending TT delivery)

---

## 1. Objective

Upgrade the Tarot module across all surfaces -- the interactive draw tool, the SEO content pages, and the incoming combination pages -- into a cohesive, premium, temple-aesthetic experience that can receive a custom SVG card deck (78 cards).

This is a **design-only commission.** No backend changes. No new routes. No data model changes. The upgrade touches only JSX, CSS-in-JS, and Tailwind class structure within existing files.

---

## 2. Scope -- Files You Will Touch

### Interactive Draw Tool (primary surface)
```
frontend/src/pages/tarot/TarotPage.jsx
```

### SEO Content Pages (secondary surface)
```
frontend/src/pages/tarot-seo/TarotSeoHubPage.jsx
frontend/src/pages/tarot-seo/TarotSpreadPage.jsx
frontend/src/pages/tarot-seo/TarotCardPage.jsx
frontend/src/pages/tarot-seo/TarotIntentionPage.jsx
```

### Phase 2 Pages (design scaffold -- content wired by TAR-SEO-3)
```
frontend/src/pages/tarot-seo/TarotCardHubPage.jsx      (new, not yet built)
frontend/src/pages/tarot-seo/TarotCombinationPage.jsx  (new, not yet built)
```

### Do NOT touch
```
backend/tarot_router.py
backend/tarot_seo_router.py
backend/tarot_seo_data.py
frontend/public/tarot_cards.json
frontend/src/App.js      (routes only -- no design changes needed)
```

---

## 3. Design System -- Temple App Tokens (MANDATORY)

All UI must use these tokens. Do not introduce arbitrary hex values or inline colours.

```
Background:         bg-background
Card surface:       bg-card
Primary text:       text-foreground
Secondary text:     text-muted-foreground
Gold accent:        text-gold / border-gold / bg-gold   →  #c5a059
GlassCard:          rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm
Premium border:     border-gold/30
Glow:               box-shadow: 0 0 32px rgba(197,160,89,0.65)
```

Typography: system fonts only (`font-family: Georgia, 'Times New Roman', serif` for display headings; sans-serif for body via Tailwind default).

Iconography: Lucide React only. No new icon libraries.

---

## 4. SVG Card Deck Integration

Temple Team will deliver 78 SVG files -- one per tarot card -- in one consistent visual style (either Classic parchment or Celestial Neon). The files will follow a naming pattern like `major_02_high_priestess_classic.svg`.

**Your task for card rendering:**

The existing `CardFace` component in `TarotPage.jsx` (line ~147) already renders SVG card data as a base64 data URL:

```jsx
function CardFace({ svgData, cardName, orientation, className = '' }) {
  const svgUrl = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svgData)}`;
  return (
    <div className={`aspect-[2/3] rounded-xl overflow-hidden ...`}>
      <img src={svgUrl} alt={cardName} className="w-full h-full object-cover" />
    </div>
  );
}
```

This pipeline is correct. Design upgrade requirements for card display:

1. **Card reveal animation** -- the existing `FlippingCard` component (line ~163) has a 3D flip and gold particle burst. Preserve both. Upgrade: add a subtle shimmer pass across the card face on reveal completion (CSS `@keyframes` only -- no JS timers).
2. **Reversed card treatment** -- reversed cards currently apply `rotate-180`. Upgrade: add a faint red-tinted overlay (`bg-red-900/10`) on reversed card faces to visually signal the orientation without obscuring the artwork.
3. **Card modal / drawer** -- currently uses Vaul drawer. Keep Vaul. Upgrade the drawer interior:
   - Card image: larger, centred, max-height 60vh
   - Card name: display serif font, gold colour
   - Meaning text: readable body size (text-base), muted foreground, generous line-height
   - Keywords: gold pill chips
   - Close button: top-right, subtle
4. **Card back design** -- current `CardBack` (line ~137) is minimal (dark gradient + star icon). Upgrade with a proper mandala/yantra SVG pattern inline -- parchment or deep-space tone depending on which deck style TT delivers. Must work as a pure SVG `<g>` embedded in the JSX.

---

## 5. Interactive Draw Tool -- Tab-by-Tab Upgrade (`TarotPage.jsx`)

The tool has 5 tabs: **Daily Draw · Spreads · Favorable Periods · Journal · History**

### Tab 1 -- Daily Draw

Current state: card flip, focus area pills, reading guidance text.

Upgrade requirements:
- **Hero section** -- above the card: a thin decorative rule with `✦ Your Daily Draw ✦` centred in gold. Replace the current plain heading.
- **Focus area pills** -- currently plain buttons. Upgrade: active pill gets gold border + subtle bg-gold/10 fill + glow. Inactive: muted border, ghost.
- **Card flip zone** -- preserve all animation. Add: after flip, the card name fades in below the card with a tarot-fade-up animation (already defined in `TarotV4Styles`).
- **Reading guidance block** -- currently plain text in a card. Upgrade to a GlassCard with a left gold border accent (`border-l-4 border-gold`). Guidance text in italic serif for the main paragraph.
- **Share button** -- currently a plain `Share2` icon button. Upgrade: add a pill label "Share Reading" next to the icon.

### Tab 2 -- Spreads

Current state: spread cards listing.

Upgrade requirements:
- **Spread cards** -- each spread in the list should be a GlassCard with: spread title (bold), category badge (gold pill), and a one-line purpose excerpt. Currently this may be plain list items -- elevate to card grid (2-col on mobile, 3-col on desktop).
- **Celtic Cross layout** (if rendered visually): position markers should use gold circle nodes with position numbers, connected by thin hairlines.

### Tab 3 -- Favorable Periods

No design changes required -- data-driven, keep as-is.

### Tab 4 -- Journal

Current state: text input + entries list.

Upgrade requirements:
- **Journal entry cards** -- give each entry a GlassCard wrapper with date in muted foreground, card name in gold, entry text in body.
- **Input area** -- textarea with gold focus ring (`focus:border-gold focus:ring-gold/20`).

### Tab 5 -- History

Current state: grouped reading history.

Upgrade requirements:
- **Month group headers** -- style as thin gold ruled dividers with month label centred.
- **History item cards** -- GlassCard. Card image thumbnail (small, 48×72px), card name bold, date muted, focus area as a coloured dot.
- **Streak widget** -- already exists. Upgrade: filled week-day dots should pulse gently with a CSS animation. XP progress bar should use gold fill.

---

## 6. SEO Content Pages -- Shared Design System

All four existing SEO pages (`TarotSeoHubPage`, `TarotSpreadPage`, `TarotCardPage`, `TarotIntentionPage`) follow a similar layout. Apply these upgrades consistently across all four.

### 6a. Page Header / Hero Section

Each page currently opens with a plain H1 and subtitle. Upgrade:

```
┌──────────────────────────────────────────────────────┐
│  ✦ decorative rule                                   │
│  [Breadcrumb: Home › Tarot › Spreads]  (muted, sm)  │
│                                                       │
│  H1 -- large serif, text-foreground                  │
│  Subtitle -- muted-foreground, max-width prose       │
│  ✦ decorative rule                                   │
└──────────────────────────────────────────────────────┘
```

- Breadcrumb: muted text-sm, `›` separator, last item in text-foreground
- H1: `text-3xl md:text-4xl font-bold` -- serif weight
- Decorative rules: `<div className="flex items-center gap-3"><div className="flex-1 h-px bg-gold/20"/><span className="text-gold/60 text-xs">✦</span><div className="flex-1 h-px bg-gold/20"/></div>`

### 6b. Spread Hub (`TarotSeoHubPage.jsx`)

- **Featured spreads grid**: GlassCard per spread -- title bold, category pill, purpose text truncated to 2 lines, arrow CTA in gold
- **Category filter tabs**: horizontal scroll pill tabs -- active = gold fill, inactive = ghost
- **Card section grid**: 4-col on desktop, 2-col on mobile, uniform aspect ratio
- **Intention section**: 3-col pill grid with icon + label

### 6c. Spread Detail Page (`TarotSpreadPage.jsx`)

- **Spread overview block**: GlassCard with left gold accent border
- **Position accordion**: each position item -- position number in a gold circle, label bold, guidance text body. Accordion trigger uses ChevronDown Lucide icon.
- **How-to steps**: numbered list with gold circle step numbers
- **FAQ accordion**: consistent styling with spread positions

### 6d. Card Detail Page (`TarotCardPage.jsx`)

- **Card image block**: centred, max-width 280px, gold border frame (`border-2 border-gold/40 rounded-xl`), subtle shadow
- **Arcana / suit badge**: gold pill top-right of image
- **Meaning tabs**: Upright · Reversed · Love · Career · Health -- horizontal tab bar, active tab underlined in gold
- **Keywords block**: gold pill chips, wrapping
- **Best spreads section**: 3-col pill grid linking to spread pages -- gold text, border-gold/20

### 6e. Intention Page (`TarotIntentionPage.jsx`)

- **Intention hero**: full-width GlassCard with intention icon (large, gold), title, description
- **Best cards grid**: 3-col, each card as GlassCard with card name and 1-line upright meaning

---

## 7. Phase 2 Design Scaffolds (TAR-SEO-3 pages -- build the shells)

These two pages do not exist yet. Build the JSX shells with design-complete layouts. Content data will be wired by the TAR-SEO-3 commission separately. Use loading skeleton states where live data would appear.

### 7a. Card Hub Page (`TarotCardHubPage.jsx`)
Route: `/tarot/cards`

```
Header: "All 78 Tarot Cards Explained"
Filter tabs: All · Major Arcana · Wands · Cups · Swords · Pentacles
Card grid: 6-col desktop / 3-col tablet / 2-col mobile
  Per card: arcana/suit badge (colour-coded), card name, 1-line keyword
  Click: navigates to /tarot/card/:slug
```

Suit colour coding:
- Major Arcana: gold
- Wands: amber/fire (`text-amber-500`)
- Cups: blue (`text-blue-400`)
- Swords: slate (`text-slate-300`)
- Pentacles: emerald (`text-emerald-400`)

### 7b. Combination Page (`TarotCombinationPage.jsx`)
Route: `/tarot/card/:cardSlug/:spreadSlug`

```
Breadcrumb: Tarot › [Card Name] › [Spread Title]
H1: "[Card Name] in a [Spread Title]"
Synthesis block: GlassCard, left gold accent border
Position accordion: same style as spread page
Action step strip: full-width gold-tinted banner (bg-gold/10, border-gold/30)
  "Your next step:" label + action text
Related combos: 3-col GlassCard grid
CTA strip: 3 buttons -- "Full card meaning" | "Learn the spread" | "Draw live"
```

---

## 8. Responsive Breakpoints

All grids must be mobile-first. Reference breakpoints:
- `sm`: 640px (2-col grids start)
- `md`: 768px (3-col grids start)
- `lg`: 1024px (full desktop layouts)

The app is primarily used on mobile (Indian audience). Prioritise mobile layout quality over desktop.

---

## 9. Animation Budget

Keep animations minimal and performant (CSS only, no JS-timer-based animations):

| Animation | Where | Duration |
|---|---|---|
| `tarotFadeUp` | Card name reveal, tab transitions | 420ms ease-out |
| `tarotGlow` | Card face on flip completion | 1100ms ease-out |
| `tarotBurst` | Gold particle burst on flip | 650ms ease-out |
| Shimmer pass | Card face reveal (new) | 800ms ease-in-out |
| Streak dot pulse | History tab week dots | 2s ease-in-out infinite |

No `framer-motion` -- this project does not use it. CSS `@keyframes` only.

---

## 10. Accessibility Requirements

- All interactive elements must have `aria-label` or visible label text
- Card images: `alt={cardName}` (already present in `CardFace` -- preserve)
- Accordion items: use the existing Radix UI `Accordion` component (already imported) -- do not replace with custom divs
- Colour contrast: all text on gold backgrounds must pass WCAG AA (use dark text `text-neutral-900` on gold fills)
- Focus rings: `focus-visible:ring-2 focus-visible:ring-gold/50` on all interactive elements

---

## 11. Architecture Rules (MANDATORY)

1. **Do NOT touch `tarot_router.py`, `tarot_seo_router.py`, or `tarot_seo_data.py`** -- backend is locked
2. **Do NOT modify `tarot_cards.json`** -- deck swap handled separately by TT
3. **Preserve all Punya Rewards hooks** -- `safeClaimPunyaAction('tarot_daily_draw')`, `tarot_spread_complete`, `tarot_bookmark` -- fire-and-forget, must not be removed or blocked
4. **Preserve all Vaul Drawer usage** -- do not replace with a custom modal
5. **Preserve all existing SEO/schema JSON-LD** -- do not remove or alter `buildSchema()` calls
6. **Do NOT add new npm packages** -- Lucide React, Tailwind, Radix UI, Vaul are all already available

---

## 12. Build Verification

After delivery, CC will run:

```bash
cd frontend && CI=true DISABLE_ESLINT_PLUGIN=true npx craco build
```

Zero errors required. Warnings are acceptable if they are pre-existing.

---

## 13. Acceptance Checklist

- [ ] `TarotPage.jsx` -- card reveal shimmer, reversed overlay, upgraded drawer interior, upgraded card back, all 5 tab designs upgraded
- [ ] `TarotSeoHubPage.jsx` -- hero section, GlassCard spread grid, category pills, FAQ
- [ ] `TarotSpreadPage.jsx` -- hero section, position accordion, how-to steps, FAQ
- [ ] `TarotCardPage.jsx` -- card image frame, meaning tabs, keywords, best spreads pills
- [ ] `TarotIntentionPage.jsx` -- hero GlassCard, best cards grid
- [ ] `TarotCardHubPage.jsx` -- shell built: filter tabs, 6-col grid, suit colour coding
- [ ] `TarotCombinationPage.jsx` -- shell built: breadcrumb, synthesis block, position accordion, action step strip, related combos, CTA strip
- [ ] All gold token usage -- no arbitrary hex colours introduced
- [ ] Mobile layouts verified (all grids collapse correctly at sm/md)
- [ ] All Punya hooks preserved
- [ ] Build passes: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`

---

## 14. Reference Files

| File | Purpose |
|---|---|
| `frontend/src/pages/tarot/TarotPage.jsx` | Current interactive tool -- all 5 tabs |
| `frontend/src/pages/tarot-seo/TarotSeoHubPage.jsx` | Current spread hub |
| `frontend/src/pages/tarot-seo/TarotSpreadPage.jsx` | Current spread detail |
| `frontend/src/pages/tarot-seo/TarotCardPage.jsx` | Current card detail |
| `frontend/src/pages/tarot-seo/TarotIntentionPage.jsx` | Current intention page |
| `Codex_Deliveries/Tarot/CODEX_COMMISSION_TAR_SEO_3_COMBINATIONS.md` | Phase 2 content spec (for combination page shell) |
| `CLAUDE.md` | Temple theme tokens, architecture rules, commit protocol |
