# CD Confirmations -- The Strategist Phase 2
> Response to CD's three pre-build questions
> Issued by: Temple Team / CC
> Date: 2026-05-27

---

## Q1 -- Single file or file-per-component?

**File-per-component delivery.**

Revised from the earlier "one big file" suggestion. Reason: token budget.
A 7-component, 4-mode, A/B-toggle prototype in one file will exhaust CD's
context window before delivery is complete. This is worse than fragmented
review -- it means partial delivery with no clean pickup point.

**Revised delivery format:**

| Delivery | File | Contents |
|---|---|---|
| Pattern-setter | `STR-2F · ConquestScoreboard.html` | ConquestScoreboard only -- toggle A/B, all 3 modes. Sign off pattern before proceeding. |
| 2 | `STR-2E · LKGateSummaries.html` | LKGateSummaries -- toggle A/B, all 3 modes |
| 3 | `STR-2C · PreFlightBanners.html` | All 4 verdict states (YES/WAIT/NO/PRAY) as pill-selectable, all 3 modes |
| 4 | `STR-2D · ScoreGatedReEntry.html` | Score-gated loop -- toggle A/B, all 3 modes |
| 5 | `STR-2I · PRAYPath.html` | Surrender protocol -- toggle A/B, all 3 modes |
| 6 | `STR-2G · ActionPlanPage.html` | Full action plan page -- Command/Briefing toggle, all 3 modes |
| 7 | `STR-2B · Gate0Panel.html` | KP Gate 0 inline panel shell -- stub data, all 3 modes |

CC reviews and approves each file before the next is started.
No file should begin until the previous one is signed off.

---

## Q2 -- Theme modes in prototype

**3 modes, not 4.**

cr-ambient and cr-tactical have been merged into a single optimised
Control Room mode (`cr`). Reasoning:

| Attribute | cr-ambient | cr-tactical | cr (optimised -- USE THIS) |
|---|---|---|---|
| Grid spacing | 48px minor / 192px major | 48px minor / 192px major | **48px minor / 192px major** (same in both -- no change) |
| Grid line colour | `#4a9866` | `#45b060` | **`#45b060`** (cr-tactical -- darker green) |
| Minor grid opacity | 0.10 | 0.15 | **0.15** (cr-tactical -- darker) |
| Major grid opacity | 0.15 | 0.20 | **0.20** (cr-tactical -- darker) |
| Stroke width | 1px | 1.5px | **1.5px** (cr-tactical -- heavier) |
| Card/text tokens | light-mode | light-mode | **light-mode** (same) |

**The 3 modes for the prototype top-bar pill:**

```
[ light ]  [ dark ]  [ cr ]
```

Card/text token behaviour per mode:

| Mode | Background | Card surface | Text | Grid |
|---|---|---|---|---|
| `light` | warm off-white `#F9F5F0` + soft gold radial | `rgba(197,160,89,0.04)` | `#2D241E` | none |
| `dark` | navy `#0a0d14` + faint gold ember | `#161b27` | `#ECE6D6` | none |
| `cr` | white `#F9F5F0` + green matrix grid | `rgba(197,160,89,0.04)` | `#2D241E` | green matrix |

---

## Q3 -- Token source

**Use the live token file pasted below.** This supersedes the Step 3 append.
Key differences from what CD already has:

- `:root` global block adds `--card-deep`, conquest band colours + soft scrims,
  and 9 planet command colours. These are global (not scoped to `.strategist-module`).
- The merged `cr` mode CSS is new -- replace the old `cr-ambient` / `cr-tactical`
  split with the single `[data-mode="cr"]` block below.

---

## Full Token CSS for Prototype

Copy this entire block into the prototype `<style>` tag.

```css
/* ── Brand-fixed, mode-agnostic ─────────────────────────── */
.strategist-module {
  --strategist-gold:         #C5A059;
  --strategist-gold-mustard: #E3B341;
  --strategist-gold-hover:   #D4AF37;
  --strategist-emerald:      #3FAA7A;
  --strategist-amber:        #E3A341;
  --strategist-orange:       #E27A3F;
  --strategist-red:          #E25C4B;
  font-family: 'Playfair Display', Georgia, serif;
  min-height: 100vh;
  background: var(--strategist-bg);
  color: var(--strategist-fg);
}

/* ── Light ──────────────────────────────────────────────── */
.strategist-module[data-mode="light"] {
  --strategist-bg:                 #F9F5F0;
  --strategist-fg:                 #2D241E;
  --strategist-text-primary:       #2D241E;
  --strategist-text-muted:         #8C7E72;
  --strategist-card-bg:            rgba(197, 160, 89, 0.04);
  --strategist-card-elev:          rgba(197, 160, 89, 0.08);
  --strategist-card-border:        rgba(197, 160, 89, 0.20);
  --strategist-card-border-strong: rgba(197, 160, 89, 0.40);
  background:
    radial-gradient(ellipse at 80% -10%, rgba(197,160,89,0.10), transparent 55%),
    #F9F5F0;
}

/* ── Dark ───────────────────────────────────────────────── */
.strategist-module[data-mode="dark"] {
  --strategist-bg:                 #0a0d14;
  --strategist-fg:                 #ECE6D6;
  --strategist-text-primary:       #ECE6D6;
  --strategist-text-muted:         #8A8576;
  --strategist-card-bg:            #161b27;
  --strategist-card-elev:          #1c2230;
  --strategist-card-border:        rgba(197, 160, 89, 0.20);
  --strategist-card-border-strong: rgba(197, 160, 89, 0.40);
  background:
    radial-gradient(ellipse at 80% -10%, rgba(197,160,89,0.08), transparent 55%),
    #0a0d14;
}

/* ── CR (Control Room -- optimised merge of cr-ambient + cr-tactical) ── */
/* Darker green lines (cr-tactical values) + 48px/192px grid spacing     */
.strategist-module[data-mode="cr"] {
  --strategist-bg:                 #F9F5F0;
  --strategist-fg:                 #2D241E;
  --strategist-text-primary:       #2D241E;
  --strategist-text-muted:         #8C7E72;
  --strategist-card-bg:            rgba(197, 160, 89, 0.04);
  --strategist-card-elev:          rgba(197, 160, 89, 0.08);
  --strategist-card-border:        rgba(197, 160, 89, 0.20);
  --strategist-card-border-strong: rgba(197, 160, 89, 0.40);
  background:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='192' height='192'%3E%3Cpath d='M 192 0 L 0 0 0 192' fill='none' stroke='%2345b060' stroke-opacity='0.20' stroke-width='1.5'/%3E%3C/svg%3E") 0 0 / 192px 192px,
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='48' height='48'%3E%3Cpath d='M 48 0 L 0 0 0 48' fill='none' stroke='%2345b060' stroke-opacity='0.15' stroke-width='1.5'/%3E%3C/svg%3E") 0 0 / 48px 48px,
    #F9F5F0;
}

/* ── Type helpers ────────────────────────────────────────── */
.strategist-module .font-cinzel   { font-family: 'Cinzel', Georgia, serif; }
.strategist-module .font-playfair { font-family: 'Playfair Display', Georgia, serif; }
.strategist-module .font-mono     {
  font-family: ui-monospace, 'JetBrains Mono', 'SF Mono', Menlo, monospace;
}

/* ── Global band + planet tokens ─────────────────────────── */
:root {
  --card-deep:      #11151f;

  /* Conquest score bands */
  --emerald:        #3FAA7A;   --emerald-soft: rgba(63,  170, 122, 0.12);
  --amber:          #E3A341;   --amber-soft:   rgba(227, 163,  65, 0.12);
  --orange:         #E27A3F;   --orange-soft:  rgba(226, 122,  63, 0.12);
  --red:            #E25C4B;   --red-soft:     rgba(226,  92,  75, 0.12);

  /* Planet command colours */
  --planet-sun:     #F5A623;   --planet-moon:    #B8D4E8;
  --planet-mars:    #E05A5A;   --planet-mercury: #6FCF97;
  --planet-jupiter: #C5A059;   --planet-venus:   #F2C4D0;
  --planet-saturn:  #7E92AE;   --planet-rahu:    #9B59B6;
  --planet-ketu:    #E67E22;
}
```

---

## Summary of Changes vs Earlier Response

| Item | Earlier answer | This answer |
|---|---|---|
| Delivery format | One big HTML file with left rail | **One HTML file per component -- 7 files total** |
| Theme modes | 4 (light / dark / cr-ambient / cr-tactical) | **3 (light / dark / cr)** |
| CR mode | Two separate modes | **Single merged `cr` mode -- darker cr-tactical lines + shared 48px spacing** |
| Token source | Paste from CC | **Same -- live token file, updated with merged `cr` mode** |
| Build order | 2F first, rest in sequence | **Same -- 2F pattern-setter, no next file starts until current is signed off** |
