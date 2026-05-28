# Process Doc 6 -- Correct JSON-LD Schema.org Types by Module
> EverydayHoroscope.in -- SEO Structured Data Reference
> Document Type: Platform-Wide Process Reference
> Version: 1.0
> Date: 2026-05-27
> Scope: All SEO modules -- correct @type assignment, validated against schema.org

---

## 1. Purpose

This document is the authoritative reference for which JSON-LD schema.org types to use per module. It exists because:

1. **GAI hallucination risk:** AI tools commonly propose non-existent schema.org types (e.g., `CommentaryAction`, `ScriptureVerse`, `TarotReading`). All types must be validated at schema.org before inclusion in any Codex commission brief.
2. **GSC warning prevention:** Invalid schema types generate Google Search Console structured data errors, which suppress rich result eligibility.
3. **YMYL E-E-A-T alignment:** Spiritual and religious content (Faith module) is YMYL -- structured data choice directly impacts trust signals.

**Rule:** Before including ANY `@type` in a Codex brief, verify it exists at: https://schema.org/{TypeName}

---

## 2. Verified Schema Types -- By Module

### 2.1 Panchang / Daily Horoscope Pages
```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Panchang for {City} -- {Date}",
  "datePublished": "{ISO date}",
  "about": {
    "@type": "Event",
    "name": "{Festival or Tithi name}",
    "startDate": "{ISO date}"
  }
}
```
**For Horoscope pages:** Use `Article` with `author` entity.

---

### 2.2 Festival × Region Pages (M3)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{Festival} in {Region} -- {Year} Guide",
  "about": {
    "@type": "Event",
    "name": "{Festival Name}",
    "location": {
      "@type": "Place",
      "name": "{Region}"
    }
  },
  "author": {
    "@type": "Organization",
    "name": "EverydayHoroscope"
  }
}
```

---

### 2.3 Tarot SEO Pages (TAR-SEO)
**Card Pages** (`/tarot/card/{slug}`):
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "The {Card Name} Tarot Card -- Meaning, Upright & Reversed",
  "about": {
    "@type": "Thing",
    "name": "{Card Name}",
    "description": "A card from the Rider-Waite Tarot deck"
  }
}
```

**Spread Pages** (`/tarot/spread/{slug}`):
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "{Spread Name} Tarot Spread",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Position 1 -- {Position Name}",
      "text": "{Position meaning}"
    }
  ]
}
```

**Combination Pages** (`/tarot/cards/{cardSlug}/{spreadSlug}`):
```json
[
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{Card Name} in the {Spread Name} -- Position {N} Meaning"
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "What does {Card Name} mean in position {N} of {Spread}?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "{Answer text}"
        }
      }
    ]
  }
]
```

---

### 2.4 Faith Pages -- Gita Verse × Life Situation

⚠️ **CRITICAL NOTE:** `CommentaryAction` is NOT a valid schema.org type. It does not exist. Do NOT use it. GAI incorrectly proposed this in the Faith-20K strategic brief. The correct types are below.

**Gita Verse Pages** (`/faith/gita/{verse-slug}/{situation-slug}`):
```json
[
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Bhagavad Gita {Chapter}:{Verse} for {Life Situation}",
    "about": {
      "@type": "Book",
      "name": "Bhagavad Gita",
      "author": {
        "@type": "Person",
        "name": "Vyasa"
      }
    },
    "author": {
      "@type": "Organization",
      "name": "EverydayHoroscope"
    },
    "inLanguage": "en"
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "What does Bhagavad Gita {Chapter}:{Verse} say about {situation}?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "{Answer}"
        }
      },
      {
        "@type": "Question",
        "name": "How can I apply Gita {Chapter}:{Verse} to {situation} in daily life?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "{Answer}"
        }
      }
    ]
  }
]
```

**Bible Promise × Life Transition Pages** (`/faith/bible/{topic-slug}/{transition-slug}`):
```json
[
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Bible Promises for {Life Transition} -- Scripture & Guidance",
    "about": {
      "@type": "Book",
      "name": "The Bible"
    },
    "author": {
      "@type": "Organization",
      "name": "EverydayHoroscope"
    },
    "inLanguage": "en"
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "What does the Bible say about {transition}?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "{Answer}"
        }
      }
    ]
  }
]
```

**Transit × Scripture Pages** (`/faith/transit/{planet-sign}/{tradition}`):
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{Planet} in {Sign} -- Gita & Bible Guidance for This Transit",
  "about": [
    {
      "@type": "Book",
      "name": "Bhagavad Gita"
    },
    {
      "@type": "Book",
      "name": "The Bible"
    }
  ],
  "author": {
    "@type": "Organization",
    "name": "EverydayHoroscope"
  }
}
```

**Daily Scripture Pages** (`/faith/daily/{sign}/{month}`):
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{Sign} Scripture Guide -- {Month}",
  "about": {
    "@type": "Thing",
    "name": "Daily spiritual practice for {sign} energy in {month}"
  }
}
```

---

### 2.5 Angel Numbers Pages
```json
[
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Angel Number {NNNN} -- Meaning, Significance & What To Do",
    "author": {
      "@type": "Organization",
      "name": "EverydayHoroscope"
    }
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "What does angel number {NNNN} mean?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "{Answer}"
        }
      }
    ]
  }
]
```

---

### 2.6 Crystal Healing Pages
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{Crystal Name} -- Properties, Uses & Healing Guide",
  "about": {
    "@type": "Thing",
    "name": "{Crystal Name}",
    "description": "A healing crystal used in metaphysical practice"
  }
}
```

---

### 2.7 Lo Shu Grid Pages
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Lo Shu Grid Number {N} -- Meaning & Life Guidance",
  "about": {
    "@type": "Thing",
    "name": "Lo Shu Grid",
    "description": "A numerological system based on the ancient Chinese Lo Shu magic square"
  }
}
```

---

### 2.8 Rudraksha Pages
```json
[
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{N} Mukhi Rudraksha -- Benefits, Ruling Planet & Who Should Wear",
    "about": {
      "@type": "Thing",
      "name": "Rudraksha",
      "description": "Sacred seed used in Hindu spiritual practice"
    }
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": []
  }
]
```

---

## 3. Types That Do NOT Exist -- Never Use

| Incorrect Type | Correct Replacement | Source of Error |
|---|---|---|
| `CommentaryAction` | `Article` with `about: {Book}` | GAI hallucination in Faith-20K brief |
| `ScriptureVerse` | `Article` with `about: {Book}` | Common AI error |
| `TarotReading` | `Article` or `HowTo` | Common AI error |
| `NumerologyReport` | `Article` | Common AI error |
| `AstrologicalChart` | `Article` | Common AI error |
| `VedicText` | `Book` | Common AI error |
| `HoroscopePrediction` | `Article` | Common AI error |

---

## 4. Schema Validation Process

Before any Codex commission goes live:
1. Validate all `@type` values at https://schema.org
2. Run Google's Rich Results Test: https://search.google.com/test/rich-results
3. Check GSC → Enhancements → structured data for errors after indexing

---

## 5. References

- `PROCESS_5_CONTENT_ANCHOR_FRAMEWORK.md` -- 3-anchor content structure
- `PROCESS_7_YMYL_CONTENT_QUALITY.md` -- YMYL E-E-A-T requirements
- `Faith_Hubs/CODEX_COMMISSION_FAITH_20K.md` -- Faith module commission (primary use case for this doc)
