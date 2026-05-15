# Panchang Language Pages -- Traffic Strategy
> Based on Drik Panchang's multilingual SEO structure
> Target: Tamil, Telugu, Malayalam, Kannada, Hindi Panchang pages

---

## 1. Why These Pages Drive Traffic

Drik Panchang gets millions of visits from searches like:
- "today tamil panchangam" → 40K+ monthly searches
- "telugu panchangam today" → 35K+ monthly searches
- "malayalam panchangam today" → 28K+ monthly searches
- "kannada panchanga today" → 22K+ monthly searches
- "hindi panchang today" → 150K+ monthly searches

These are **intent-rich, regional searches** where users want the SAME astronomical data but presented in their language/script. This is exactly what we can build on top of our existing Swiss Ephemeris engine.

---

## 2. URL Structure (following Drik's pattern)

```
/panchang/tamil          → Tamil Panchangam today
/panchang/telugu         → Telugu Panchangam today
/panchang/malayalam      → Malayalam Panchangam today
/panchang/kannada        → Kannada Panchanga today
/panchang/hindi          → Hindi Panchang today
```

Each page shows the SAME computed data from the existing API (`/api/panchang/daily`) but with:
1. Regional script labels for all Panchang elements
2. Regional calendar year name + month name
3. Page title, meta description, and H1 in that language
4. Regional terminology where different (e.g. "Nalla Neram" in Tamil for auspicious time)

---

## 3. Regional Data Reference (26 March 2026, New Delhi)

### Tamil (தமிழ்)
| Element | English | Tamil |
|---|---|---|
| Page title | Tamil Panchangam | தமிழ் பஞ்சாங்கம் |
| Today | Today | இன்று |
| Tithi | Ashtami | அஷ்டமி |
| Nakshatra | Ardra | திருவாதிரை |
| Yoga | Shobhana | சோபன யோகம் |
| Karana | Bava | பவ கரணம் |
| Weekday | Thursday | வியாழக்கிழமை |
| Sunrise | Sunrise | சூரிய உதயம் |
| Sunset | Sunset | சூரிய அஸ்தமனம் |
| Moonrise | Moonrise | சந்திர உதயம் |
| Rahu Kaal | Rahu Kalam | ராகு காலம் |
| Auspicious | Nalla Neram | நல்ல நேரம் |
| Tamil Month | Panguni | பங்குனி |
| Tamil Year | Sarvari (2025-26) | சார்வரி |
| Paksha | Shukla | சுக்ல பக்ஷம் |
| Samvat | Vikram 2082 | விக்ரம் 2082 |

### Telugu (తెలుగు)
| Element | English | Telugu |
|---|---|---|
| Page title | Telugu Panchangam | తెలుగు పంచాంగం |
| Today | Today | నేడు |
| Tithi | Ashtami | అష్టమి |
| Nakshatra | Ardra | ఆర్ద్ర |
| Yoga | Shobhana | శోభన |
| Karana | Bava | బవ |
| Weekday | Thursday | గురువారం |
| Sunrise | Sunrise | సూర్యోదయం |
| Sunset | Sunset | సూర్యాస్తమయం |
| Rahu Kaal | Rahu Kalam | రాహు కాలం |
| Telugu Month | Phalguna | ఫాల్గుణ |
| Telugu Year | Sarvari | సర్వారి |
| Paksha | Shukla | శుక్ల పక్షం |

### Malayalam (മലയാളം)
| Element | English | Malayalam |
|---|---|---|
| Page title | Malayalam Panchangam | മലയാളം പഞ്ചാംഗം |
| Today | Today | ഇന്ന് |
| Tithi | Ashtami | അഷ്ടമി |
| Nakshatra | Ardra (Thiruvathira) | തിരുവാതിര |
| Yoga | Shobhana | ശോഭന |
| Weekday | Thursday | വ്യാഴം |
| Sunrise | Sunrise | സൂര്യോദയം |
| Sunset | Sunset | സൂര്യാസ്തമയം |
| Rahu Kaal | Rahu Kalam | രാഹു കാലം |
| Malayalam Month | Meenam | മീനം |
| Malayalam Era | Kollam Era 1201 | കൊല്ലവർഷം 1201 |

### Kannada (ಕನ್ನಡ)
| Element | English | Kannada |
|---|---|---|
| Page title | Kannada Panchanga | ಕನ್ನಡ ಪಂಚಾಂಗ |
| Today | Today | ಇಂದು |
| Tithi | Ashtami | ಅಷ್ಟಮಿ |
| Nakshatra | Ardra | ಆರ್ದ್ರ |
| Yoga | Shobhana | ಶೋಭನ |
| Weekday | Thursday | ಗುರುವಾರ |
| Sunrise | Sunrise | ಸೂರ್ಯೋದಯ |
| Rahu Kaal | Rahu Kala | ರಾಹು ಕಾಲ |
| Kannada Month | Phalguna | ಫಾಲ್ಗುಣ |
| Kannada Year | Sarvari | ಸರ್ವಾರಿ |

### Hindi (हिंदी)
| Element | English | Hindi |
|---|---|---|
| Page title | Hindi Panchang | हिंदी पंचांग |
| Today | Today | आज |
| Tithi | Ashtami | अष्टमी |
| Nakshatra | Ardra | आर्द्रा |
| Yoga | Shobhana | शोभन |
| Weekday | Thursday | गुरुवार |
| Sunrise | Sunrise | सूर्योदय |
| Sunset | Sunset | सूर्यास्त |
| Rahu Kaal | Rahu Kaal | राहु काल |
| Month | Phalguna | फाल्गुन |
| Samvat | Vikram Samvat 2082 | विक्रम संवत 2082 |
| Paksha | Shukla Paksha | शुक्ल पक्ष |

---

## 4. Page Structure (same for all 5 languages)

Each language page renders exactly the same layout as the English Panchang Today page, but:

1. **Labels** -- All field labels in regional script
2. **Calendar metadata** -- Regional year + month name shown prominently
3. **Page title** -- In regional script + English (bilingual for SEO)
4. **H1** -- "[Language] Panchangam -- [Date]" in regional script
5. **Meta description** -- In regional script + English
6. **Regional terminology** -- e.g. Tamil shows "நல்ல நேரம்" (Nalla Neram) instead of just "Auspicious"

Data values (times, nakshatra names in transliteration) come from the SAME backend API -- no new backend computation needed.

---

## 5. Implementation Plan

### Phase 1 -- Frontend only (Week 1)
Create `frontend/src/pages/PanchangLangPage.jsx` -- a thin wrapper that:
- Accepts a `lang` prop ('tamil' | 'telugu' | 'malayalam' | 'kannada' | 'hindi')
- Imports the same panchang data from the existing API
- Maps all labels through a `LANG_LABELS[lang]` dictionary
- Renders the same card layout as `PanchangPage.jsx`

Routes to add in `App.js`:
```jsx
<Route path="/panchang/tamil"    element={<PanchangLangPage lang="tamil" />} />
<Route path="/panchang/telugu"   element={<PanchangLangPage lang="telugu" />} />
<Route path="/panchang/malayalam" element={<PanchangLangPage lang="malayalam" />} />
<Route path="/panchang/kannada"  element={<PanchangLangPage lang="kannada" />} />
<Route path="/panchang/hindi"    element={<PanchangLangPage lang="hindi" />} />
```

### Phase 2 -- SEO optimization (Week 2)
- Unique SEO component per language with hreflang tags
- Sitemap entries for all 5 language routes
- JSON-LD in each language
- Canonical tags pointing to English as primary

### Phase 3 -- Regional calendar accuracy (Week 3)
- Add Tamil month computation to backend (Panguni, Chithirai, etc.)
- Add Malayalam month (Meenam, Medam, etc.)
- Add Telugu Samvatsara year name
- Add Kollam Era for Malayalam

---

## 6. SEO Title Formats (by language)

| Language | Title format |
|---|---|
| Tamil | "இன்றைய தமிழ் பஞ்சாங்கம் -- [Date] \| Everyday Horoscope" |
| Telugu | "నేటి తెలుగు పంచాంగం -- [Date] \| Everyday Horoscope" |
| Malayalam | "ഇന്നത്തെ മലയാളം പഞ്ചാംഗം -- [Date] \| Everyday Horoscope" |
| Kannada | "ಇಂದಿನ ಕನ್ನಡ ಪಂಚಾಂಗ -- [Date] \| Everyday Horoscope" |
| Hindi | "आज का हिंदी पंचांग -- [Date] \| Everyday Horoscope" |

---

## 7. Nakshatra Names in Regional Languages

### Tamil names for 27 Nakshatras
Ashwini=அஸ்வினி, Bharani=பரணி, Krittika=கார்த்திகை, Rohini=ரோகிணி,
Mrigashira=மிருகசீரிஷம், Ardra=திருவாதிரை, Punarvasu=புனர்பூசம்,
Pushya=பூசம், Ashlesha=ஆயில்யம், Magha=மகம், PurvaPhalguni=பூரம்,
UttaraPhalguni=உத்திரம், Hasta=அஸ்தம், Chitra=சித்திரை,
Swati=சுவாதி, Vishakha=விசாகம், Anuradha=அனுஷம், Jyeshtha=கேட்டை,
Mula=மூலம், PurvaAshadha=பூராடம், UttaraAshadha=உத்திராடம்,
Shravana=திருவோணம், Dhanishtha=அவிட்டம், Shatabhisha=சதயம்,
PurvaBhadrapada=பூரட்டாதி, UttaraBhadrapada=உத்திரட்டாதி, Revati=ரேவதி

### Telugu names for 27 Nakshatras
Ashwini=అశ్విని, Bharani=భరణి, Krittika=కృత్తిక, Rohini=రోహిణి,
Mrigashira=మృగశిర, Ardra=ఆర్ద్ర, Punarvasu=పునర్వసు,
Pushya=పుష్యమి, Ashlesha=ఆశ్లేష, Magha=మఘ, PurvaPhalguni=పూర్వఫల్గుణి,
UttaraPhalguni=ఉత్తరఫల్గుణి, Hasta=హస్త, Chitra=చిత్ర,
Swati=స్వాతి, Vishakha=విశాఖ, Anuradha=అనూరాధ, Jyeshtha=జ్యేష్ఠ,
Mula=మూల, PurvaAshadha=పూర్వాషాఢ, UttaraAshadha=ఉత్తరాషాఢ,
Shravana=శ్రవణ, Dhanishtha=ధనిష్ఠ, Shatabhisha=శతభిష,
PurvaBhadrapada=పూర్వభాద్ర, UttaraBhadrapada=ఉత్తరభాద్ర, Revati=రేవతి

---

## 8. Quick Start -- Minimal Implementation

To launch all 5 language pages in a single sprint, implement just:
1. `PanchangLangPage.jsx` with a `LABELS` dictionary for all 5 languages
2. 5 routes in `App.js`
3. SEO titles in regional script
4. Language bar in NavBar routes to these pages ← ALREADY WIRED

Estimated time: 1 day of development.

Full regional calendar computation (Tamil month, Malayalam era, etc.) can be Phase 2.
