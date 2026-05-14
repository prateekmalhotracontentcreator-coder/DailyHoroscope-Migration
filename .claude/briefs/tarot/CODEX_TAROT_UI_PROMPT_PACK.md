# CODEX Prompt Pack — Tarot UI Enhancement
> EverydayHoroscope · Sprint: Tarot Frontend v2
> Stack: React 18, Tailwind CSS, Lucide Icons, Framer Motion (add if not present)
> Live backend: https://everydayhoroscope-api.onrender.com/api/tarot
> Frontend repo: github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration

---

## Context

The Tarot module has a working v1 UI (`frontend/src/pages/TarotPage.jsx`). The backend is fully live with:
- `POST /api/tarot/daily/draw` — single card daily draw with narrative scenes
- `POST /api/tarot/spread/generate` — 3-card premium spreads
- `GET /api/tarot/spreads` — available spread types
- `GET /api/tarot/history` — user reading history
- `POST /api/tarot/bookmark` — bookmark a reading
- SVG card bundle at `/tarot_cards.json` (78 cards, all Major + Minor Arcana)

Current v1 has: card flip animation, scene narrative player, spread grid, history tab, bookmark.

---

## Prompt 1 — Mystical Landing Hero

**Goal:** Replace the plain header with an immersive hero section.

Build a `TarotHero` component:
- Full-width gradient background: `from-neutral-950 via-purple-950/20 to-neutral-950`
- Animated starfield: 40-60 small white dots (`w-0.5 h-0.5 rounded-full`) scattered randomly, with a slow pulse animation (`animate-pulse` with staggered delays via inline style)
- Centered content:
  - Gold badge: `✦ VEDIC TAROT ✦` in small caps
  - Heading: "The Cards Know" in large Playfair Display font
  - Subtext: "Draw your card. Receive your message. Trust the cosmos."
- Three face-down cards fanned out at the bottom of the hero (CSS transform: left card `rotate(-8deg) translateX(-30px)`, center card upright, right card `rotate(8deg) translateX(30px)`)
- On hover over the card fan, cards spread out slightly (CSS transition)
- CTA button below cards: "Draw Today's Card →" in gold

---

## Prompt 2 — Enhanced Card Flip with Particle Burst

**Goal:** Make the card reveal moment feel magical.

Enhance `FlippingCard`:
- When `flipped` transitions from false→true, trigger a particle burst effect
- Particles: 12-16 small gold/yellow dots (`w-1.5 h-1.5 rounded-full bg-gold`) that burst outward from card center using CSS keyframe animation (`@keyframes burst`) and then fade out over 600ms
- Add a brief golden glow ring around the card on reveal (`box-shadow: 0 0 30px rgba(197,160,89,0.6)`) that fades after 1s
- Card flip should use `perspective: 1200px` for a more dramatic 3D effect
- Add subtle haptic-like timing: flip starts after 200ms delay once scene sequence ends

---

## Prompt 3 — Reading Detail Modal

**Goal:** Full-screen modal for deep reading details.

Create a `ReadingModal` component triggered by clicking the card after flip:
- Full-screen overlay with dark backdrop (`bg-black/80 backdrop-blur-sm`)
- Slides up from bottom (`translate-y-full → translate-y-0` with 300ms ease)
- Content:
  - Large card image (40% of modal width) on left
  - Right side: card name, orientation badge, full meaning (not snippet), keywords (3-5 pills), Vedic cross-reference note
  - Affirmation in a gold italic blockquote
  - "How to apply this today" section (from backend `reading.guidance`)
  - Share button (copy link or native share API)
  - Close (X) button top-right
- On mobile: card at top, content below (single column)

---

## Prompt 4 — Celtic Cross Spread UI (Premium)

**Goal:** Visual layout for the 10-card Celtic Cross spread.

Build `CelticCrossLayout`:
- Classic Celtic Cross position layout (hardcoded CSS grid):
  ```
  Position layout (pixel-based relative positioning):
    1 = center (the issue)
    2 = center overlaid rotated 90° (the cross / obstacle)
    3 = below center (the foundation)
    4 = left of center (the past)
    5 = above center (the crown / potential)
    6 = right of center (the near future)
    7-10 = vertical column on the right (staff positions)
  ```
- Each position shows: card face (or back if not yet revealed), position number, position label on hover
- Animated reveal: cards flip one by one with 300ms intervals
- Position labels appear in a table below the layout
- Gated behind "Premium" badge — shows locked state if user is not premium

---

## Prompt 5 — Focus Area with Vedic Icons

**Goal:** Replace plain text focus area buttons with icon+text cards.

Replace the current `FOCUS_AREAS` pill buttons with visual cards:
```
Guidance  🔮  — Vedic: Rahu/Ketu insight
Love      ❤️  — Vedic: Venus (Shukra) energy
Career    ⭐  — Vedic: Saturn (Shani) karma
Healing   🌿  — Vedic: Moon (Chandra) nourishment
Clarity   ✨  — Vedic: Mercury (Budha) wisdom
```
- Each card: `w-full md:w-auto`, icon large (32px), label bold, Vedic planet in small muted text
- Selected state: gold border + `bg-gold/10`
- Hover: subtle scale transform `scale(1.02)`
- Arranged in a responsive grid: 5 columns on desktop, 2-3 on mobile

---

## Prompt 6 — History Timeline View

**Goal:** Make the History tab visual and engaging.

Replace the flat card list with a timeline:
- Left border line (`border-l-2 border-gold/20`) running down the list
- Each entry has a gold dot (`w-3 h-3 rounded-full bg-gold/40`) on the left border line
- Entry card: date on top-left, card thumbnail (small, 40px wide), card name + orientation badge, affirmation snippet in italic
- Group entries by month: "March 2026", "February 2026" as section headers with `text-xs uppercase tracking-widest text-gold/60`
- Smooth scroll + fade-in animation as entries come into view (`IntersectionObserver`)
- If no history: illustration placeholder (use Lucide `BookOpen` large, muted, with "Your story begins with your first draw" text)

---

## Prompt 7 — Daily Card Streak & XP Widget

**Goal:** Gamification element to encourage daily draws.

Build `StreakWidget` component:
- Shows current daily draw streak (count of consecutive days drawn)
- Visual: row of 7 day circles (Mon-Sun), filled gold for days drawn, empty for not
- XP bar: small progress bar showing XP toward next level
- "🔥 3-day streak!" badge if streak >= 3
- Subtle animation on new streak increment (bounce)
- Data: derive from reading history (consecutive days) — compute on frontend from `/api/tarot/history` response
- Position: below the hero, above the focus area selector

---

## Prompt 8 — Card Detail Drawer (Mobile-First)

**Goal:** Swipeable bottom sheet for card details on mobile.

Build `CardDrawer` using Vaul (already in dependencies as `vaul`):
- Trigger: tap on revealed card
- Bottom sheet with drag handle
- Content: card name, large artwork (full width), meaning, keywords, Vedic note
- Swipe down to dismiss
- On desktop: renders as a right-side panel instead of bottom sheet

---

## General Code Requirements

- All new components in `frontend/src/pages/TarotPage.jsx` (single file, no new files needed unless very large)
- Use existing Tailwind classes + gold color system (`text-gold`, `bg-gold`, `border-gold`)
- Gold = `#C5A059`, light gold = `#E8C97A`
- All animations: prefer CSS transitions/keyframes over JS animation libraries
- Framer Motion: only use if truly needed (avoid bundle size increase)
- Vaul is already installed for the drawer
- No breaking changes to existing API calls
- Mobile-first: all layouts must work on 375px width

---

## Deliverable

Updated `frontend/src/pages/TarotPage.jsx` with all 8 prompts implemented.
Commit message: `feat(tarot): UI v2 — mystical hero, particle reveal, modals, timeline history, streak widget`
