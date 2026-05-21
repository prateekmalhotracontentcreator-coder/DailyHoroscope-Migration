# Lagna Kundali -- User Manual
> EverydayHoroscope · Vedic Birth Chart Workspace
> Version: KUN-1 · Updated 2026-05-22

---

## What is the Lagna Kundali?

The **Lagna Kundali** (also called the Rashi Chart or D1 Chart) is your primary Vedic birth chart. It is a snapshot of the sky at the exact moment of your birth -- showing which sign was rising on the eastern horizon (your **Lagna / Ascendant**) and where each of the nine Vedic planets was placed across the twelve houses.

This chart is the foundation of all Vedic astrological reading. Everything else -- Dasha periods, Vargas, Yogas, Shadbala strength -- is derived from or layered on top of your D1.

---

## How to Generate Your Chart

### Step 1 -- Enter Your Birth Details

| Field | What to enter |
|---|---|
| **Date of birth** | Your exact birth date (DD/MM/YYYY) |
| **Time of birth** | Your birth time in 24-hour format. The more precise, the more accurate the Lagna. |
| **Time precision** | Exact / Approximate / Unknown |
| **Birth Location** | Search for your birth city. The system uses the city's latitude, longitude, and timezone for all astronomical calculations. |

### Step 2 -- Unknown Birth Time

If you do not know your birth time, check the box:
> **"I don't know my exact birth time -- use 12:00 noon (chart will be marked as approximate)."**

When this is checked:
- Time is automatically set to **12:00 noon**
- Time precision is set to **Unknown**
- The Dasha and Shadbala tabs will be restricted, since accurate dasha calculation requires a reliable Moon longitude (which depends on the time of birth)
- All other tabs remain visible

**Tip:** Even with an approximate time, the D1 chart is meaningful for sign-level placements. Only house cusps and Lagna itself shift significantly with time.

### Step 3 -- Generate D1

Click **Generate D1** to compute your chart. The engine uses **pyswisseph** (Swiss Ephemeris) -- the same astronomical engine used by professional astrology software worldwide.

The system computes D1 first. All other Varga charts (D9, D10, etc.) are registered in the workspace and load only when you select them, so your initial load is always fast.

### Step 4 -- Save Chart

Click **Save Chart** to store your chart in your account. You can retrieve saved charts by navigating to `/kundali/view/{chart_id}` or from your account dashboard.

---

## The Dual Chart Workspace

The central panel shows **two charts side by side** -- called Left Panel and Right Panel. This dual-chart view is designed for direct comparison:

| Use case | Left Panel | Right Panel |
|---|---|---|
| Default | D1 (Rashi Chart) | D9 (Navamsa) |
| Transit study | D1 (natal) | D1 for a transit date |
| Career analysis | D1 | D10 (Dashamsha) |
| Relationship overlay | Your D1 | Partner's chart (saved) |
| Varga deep-dive | Any two divisional charts |

### Changing Charts in Either Panel

Use the two dropdowns above the dual chart panel to select which chart appears in the Left or Right slot. All Varga charts registered in the system appear in the selector. Charts that are currently enabled compute on demand when selected. Charts marked `(Registered)` are in the system but not yet computationally enabled -- they will load with a "Registered in the selector" message.

### Chart Style -- North / South / East Indian

Use the **North / South / East** toggle above the panels to switch the visual style of the chart diagram:

| Style | Layout | Common in |
|---|---|---|
| **North Indian** | Diamond-shaped houses with Lagna at top centre | North India, UP, Punjab, Rajasthan |
| **South Indian** | Square fixed-sign grid (Aries always top-left) | Tamil Nadu, Kerala, Karnataka, Andhra |
| **East Indian** | Square with corner triangles | Bengal, Odisha, Assam |

All three styles show the same planetary data -- only the visual layout differs. Your preference is saved automatically in your browser.

---

## Left Navigation Bar -- Layers

The **Layers** sidebar on the left is your workspace navigator. Each section loads a different analytical layer of your chart. Tabs that are restricted (due to unknown birth time or computational tier) are automatically hidden.

---

### Kundali (D1 Chart View)

The default tab. Shows:

**Dual Chart Panels** -- Your selected pair of charts rendered as SVG diagrams. Each house cell shows:
- House number
- Rashi (sign) number
- Sign name abbreviation
- Abbreviated planet names for planets placed in that house

**Graha Details Table** -- A row for each of the 9 Vedic planets (Sun through Ketu) showing:
- Graha name
- Rashi (sign)
- Degree within sign
- Nakshatra
- House in D1 (whole-sign)
- House in Bhav Chalit (house-offset chart)

**House Summary Table** -- A quick reference for all 12 houses showing:
- House number (1-12)
- Rashi occupying that house
- Lord of that house (the planet that rules the Rashi)

The House Lord is especially important in Vedic astrology -- the relationship between a house lord and its placement determines much of how that house's themes manifest in life.

---

### Graha (Planetary Layer)

A detailed table of all 9 Vedic planets with:
- Longitude (absolute ecliptic degree)
- Sign placement
- Retrograde status (Yes / No)
- Dignity (exalted / own / friendly / neutral / enemy / debilitated)

**How to read:** Dignity tells you the planet's comfort level in that sign. Exalted and own-sign planets tend to perform well; debilitated planets may need remediation. Retrograde planets are considered to have a more internalised, intensified quality in Vedic tradition.

---

### Upagraha (Secondary Planets)

Upagrahas are calculated shadow points -- they are not visible planets but mathematically derived positions used in advanced timing and muhurta. Includes Gulika, Mandi, Dhuma, Vyatipata, Parivesha, and Indrachapa.

`Supported: Yes` -- computationally enabled and verified.
`Supported: Pending` -- registered, enablement in a future tier.

---

### Yoga (Yoga Registry)

Lists all yogas detected in your chart. A **Yoga** is a specific planetary combination described in classical Vedic texts -- when certain planets occupy certain relationships (sign, house, aspect, or conjunction), a yoga is formed.

The table shows:
- Yoga code and name
- Category (raja yoga, dhana yoga, arishta yoga, etc.)
- Whether it is computationally supported in the current tier
- Whether it matched (triggered) in your chart

**How to read:** A matched yoga means the combination was found in your D1. Whether it manifests strongly depends on the dasha period, the strength of the participating planets (see Shadbala), and other modifying factors.

---

### Dasha (Vimshottari Mahadasha)

The **Vimshottari Dasha** system divides your life into planetary periods totalling 120 years. Each planet rules a main period (Mahadasha) of fixed duration, and within it, each sub-period (Antardasha or Bhukti) cycles through all 9 planets.

**Current Dasha Window panel** shows:
- Active **Maha Dasha** planet + start/end dates + time remaining
- Active **Antar Dasha** planet + start/end dates

**Vimshottari Mahadashas table** shows the full 9-period timeline from birth onward with each planet, start date, end date, and duration in years.

**How to read:** Events in life tend to align with the nature of the active Maha Dasha planet and Antar Dasha planet. A Jupiter Mahadasha generally brings expansion, wisdom, and opportunity. A Saturn Mahadasha brings hard work, discipline, and restructuring. The outcome is always filtered through the strength and placement of that planet in your D1 -- a strong exalted Jupiter in the 5th will manifest the Jupiter Mahadasha very differently from a debilitated Jupiter in the 8th.

> **Note:** This tab is restricted if birth time is unknown, since the Dasha start is computed from Moon's nakshatra longitude at the moment of birth.

---

### Ashtaka Varga

**Ashtaka Varga** is a classical system of numerically scoring each planet's strength in each of the 12 houses, based on contributions from all 7 planets + Lagna.

**Sarva Ashtaka Varga** -- Total bindus (points) per house across all contributing planets. Houses with higher bindus (typically 28+) are considered stronger and more productive for the matters of that house.

**Bhinna Ashtaka Varga** -- The individual contribution grid per planet. Shows how many bindus each of the 7 contributing planets adds to each of the 12 houses. This is used for transit timing -- when a planet transits a house where it has 5+ bindus in its own Bhinna table, the transit tends to be more positive.

**How to read:** Look at your Sarva Ashtaka totals. Houses with 30+ bindus are strong -- activities related to that house (career for 10th, marriage for 7th, etc.) tend to be more naturally supported. Houses below 22-25 may require more conscious effort or remediation.

---

### Shadbala (Planetary Strength)

**Shadbala** is the classical system for quantifying a planet's total functional strength in your chart. Six categories of strength are combined:

| Bala component | What it measures |
|---|---|
| **Sthana Bala** | Positional strength -- sign dignity, exaltation, own sign, etc. |
| **Dig Bala** | Directional strength -- each planet is strongest in a specific direction/quadrant |
| **Kala Bala** | Temporal strength -- time of birth (day/night), weekday, etc. |
| **Cheshta Bala** | Motional strength -- retrograde vs. direct motion |
| **Naisargika Bala** | Natural strength -- inherent luminosity hierarchy (Sun highest, Moon, Venus, Jupiter, Mercury, Mars, Saturn) |
| **Drik Bala** | Aspectual strength -- how much the planet is supported or afflicted by aspects |

**Strength Band** -- `Strong`, `Moderate`, or `Weak` based on total Shadbala relative to the Required Minimum for that planet.

**How to read:** A planet with strong Shadbala tends to deliver its significations clearly and powerfully -- for better or worse depending on its nature. A weak planet may need gemstone or mantra remediation to express its positive potential.

> **Note:** This tab is restricted if birth time is unknown, since Dig Bala and Kala Bala require the exact birth moment.

---

### Bhavabala (House Strength)

**Bhavabala** calculates the strength of each of the 12 houses (Bhavas) as a whole, not just the planet inside them. This determines how powerfully that house can deliver its results.

Strength components:
- **Bhavadhipati Bala** -- strength of the house lord
- **Bhava Dig Bala** -- directional strength of the house
- **Bhava Drushti Bala** -- aspects received by the house from benefic/malefic planets
- **Bhava Shubha-Ashubha Bala** -- auspicious vs. inauspicious influences on the house
- **Bhava Dina-Ratri Bala** -- day/night influence on the house
- **Karaka Strength** -- strength of the natural significator (karaka) of that house

**Rank** and **Strength Band** show how each house compares to others in your chart.

**How to read:** A high-Bhavabala house is generally more productive and delivers results clearly. A low-Bhavabala house may see delays or require more effort. Combine Bhavabala with Shadbala of the house lord for a full picture.

---

## Free Tier vs. Premium

| Feature | Free (`/kundali`) | Premium (`/lagna-kundali`) |
|---|---|---|
| D1 chart generation | ✅ | ✅ |
| Dual chart comparison workspace | ✅ | ✅ |
| House Summary + Graha Details | ✅ | ✅ |
| Yoga registry | ✅ | ✅ |
| Upagraha layer | ✅ | ✅ |
| Ashtaka Varga | ✅ | ✅ |
| Vimshottari Dasha | ✅ (requires exact birth time) | ✅ |
| Shadbala + Bhavabala | ✅ (requires exact birth time) | ✅ |
| Save chart to account | ✅ (login required) | ✅ |
| Share a generated Paid Report | ❌ | ✅ (premium paid reports only) |
| Brihat Kundali extended report | ❌ | ✅ |

---

## Tips for Best Results

1. **Use exact birth time when possible.** Even a 5-minute difference can change the Lagna (Ascendant) in some cases, and the Moon's Nakshatra determines which Dasha period you are born into.

2. **Birth records are the most reliable source.** Hospital records, birth certificates, or family registers are preferable to family memory.

3. **The D1 is always the anchor.** Before exploring D9, D10, or any Varga, fully understand your D1 placements. The Vargas refine and specialise -- they do not contradict D1.

4. **Dasha + Transit + Bhavabala together.** The richest readings come from combining the active Dasha planet, the current planetary transits, and the Bhavabala of the house being activated.

5. **Yoga matching requires Dasha to activate.** A raja yoga in your D1 does not necessarily produce results throughout life -- it tends to activate strongly during the Dasha/Antardasha of the yoga-forming planets.

---

## Glossary

| Term | Meaning |
|---|---|
| **Lagna** | Ascendant -- the rising sign at the moment of birth. Determines the house numbering for your chart. |
| **Rashi** | Zodiac sign (Aries through Pisces = Mesha through Meena) |
| **Graha** | Vedic planet (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu) |
| **Bhava** | House (1-12). The 1st Bhava = the Lagna house. |
| **Nakshatra** | Lunar mansion. The Moon's 27 (or 28) nakshatra divisions are central to Dasha calculations. |
| **Varga** | Divisional chart (D1 = Rashi, D9 = Navamsa, D10 = Dashamsha, etc.) |
| **Mahadasha** | Main planetary period in the Vimshottari Dasha system (7-20 years) |
| **Antardasha** | Sub-period within a Mahadasha (also called Bhukti) |
| **Yoga** | A specific planetary combination described in classical texts |
| **Shadbala** | Six-component planetary strength score |
| **Bhavabala** | Composite house strength score |
| **Ashtaka Varga** | Point-based planetary contribution system (bindus) |
| **Bhav Chalit** | A modified house chart that can shift planets between houses based on exact house cusps |
| **Dig Bala** | Directional strength -- each planet has a preferred directional house |
| **Upagraha** | Mathematical shadow points (Gulika, Mandi, etc.) used in advanced analysis |
