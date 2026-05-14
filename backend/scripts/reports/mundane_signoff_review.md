# Mundane Astrology -- Co-Founder Sign-Off Review
**Generated:** 08 May 2026, 06:20 UTC
**Scope:** All `mundane_jyotish` rules requiring decision

---

## How to Use This File

| Section | Rules | Action needed |
|---|---|---|
| **Part A -- Auto-Approved** | 137 | Confirm → promote to `approved` (or flag any concern) |
| **Part B -- Pending Human Review** | 186 | Read PHR reason → approve / rewrite / discard |
| **Part C -- Flagged** | 1 | Source check needed before decision |

**Promotion command** (after co-founder confirms a rule_id):
```python
col.update_one({'rule_id': 'RULE_ID'}, {'$set': {'approval_status': 'approved'}})
```

---

# PART A -- Auto-Approved Rules
*137 rules passed all 3 validation stages without flags.*
*Co-founder confirms → promote to `approved` → live to users.*

## v10 -- Raphael western eclipse decanate

#### `mundane-raphael-ch28-benefic-transit-country-sign-benefits`
**Title:** Benefics Transiting a Country's Ruling Sign = Improvement of Trade, Beneficial Government Changes
**Source:** Raphael Ch 28, Part 3 p.9
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** A benefic planet (Jupiter, Venus, or well-aspected Mercury) passes through a zodiac sign. Identify the countries ruled by that sign (see raphael-ch28-countries-ruled-by-signs).
**Result:** Many benefits will fall on the different countries and places ruled by such sign: improvement of trade, advantageous changes in the Government, and general benefits to the country.
**Notes:** This is the positive counterpart to the Mars/Saturn/Uranus transit rules. Jupiter transit through a country's sign is particularly beneficial -- trade expansion, judicial improvements, religious harmon...

#### `mundane-raphael-ch28-saturn-transit-country-sign-troubles`
**Title:** Saturn Transiting a Country's Ruling Sign = Serious and Chronic Troubles in That Country
**Source:** Raphael Ch 28, Part 3 p.9
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Transit Saturn passes through a zodiac sign. Identify the countries and cities ruled by that sign (see raphael-ch28-countries-ruled-by-signs).
**Result:** Serious troubles are shown in those countries ruled by whatever sign Saturn is passing through. Saturn troubles are more prolonged and structural than Mars troubles -- long-term hardship, government difficulties, agricultural failures, economic depression. Cities governed by that sign are likely to b...
**Notes:** Saturn in a sign lasts ~2.5 years -- so the period of trouble for that country extends over the full transit. Compare Mars (acute, sudden: fires/insurrections) vs Saturn (chronic, structural). Cross-va...

#### `mundane-raphael-ch28-uranus-transit-country-sign-insurrection`
**Title:** Uranus Transiting a Country's Ruling Sign = Insurrections, Strikes, Rioting, Anarchist Outrages
**Source:** Raphael Ch 28, Part 3 p.9
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Transit Uranus passes through a zodiac sign. Identify the countries ruled by that sign (see raphael-ch28-countries-ruled-by-signs).
**Result:** Uranus passing through the sign ruling any particular country will cause: INSURRECTIONS, STRIKES, and RIOTING among the people; generally disposes to Anarchist or Nihilistic outrages. The element of reform -- whether by peaceful or violent means -- is resorted to.
**Notes:** VALIDATED CASE (c.1905-1910): Events occurring in India due to Uranus being in Capricorn (which rules India) -- the Indian independence/reform movement intensified during this period. Uranus spends ~7 ...

## v11 -- Historical validation / benchmark cases

#### `gaur-ch1-samvatsar-brahma-lord-rulers-pleased`
**Title:** Brahma as Samvatsar Lord = Rulers Pleased, Luxury Increases, Good Crops
**Source:** Gaur Ch 1, p. 5
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** The current Samvatsar has Brahma as its lord. Brahma-lord Samvatsars: #1 Prabhav, #21 Sarvjat, #41 Plavang.
**Result:** Rulers, cabinet ministers, and senior officers remain pleased. Increase in people's luxuries and comforts. Crop is good due to absence of disease or loss in plants. MONTHLY PATTERN: Chaitra and Baisakh are lucky with cheap things. Jyeshtha, Aashadh, Shravan: grains costly. Bhadrapad: lucky. Ashwin: ...
**Notes:** Brahma-lord years are generally auspicious for governance and agriculture. The mid-year (monsoon months) may see price rises despite good crops overall.

#### `gaur-ch1-samvatsar-mars-lord-plentiful-grains-wars`
**Title:** Mars as Samvatsar Lord = Plentiful Grains but Rulers in Conflicts, World Peace Breached
**Source:** Gaur Ch 1, p. 6
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** The current Samvatsar has Mars as its lord. Mars-lord Samvatsars: #6 Angira, #26 Nandan, #46 Paridhavi, #15 Vrish, #55 Durmati.
**Result:** Grains are plentiful. Rulers remain engaged in conflicts. The peace of world is breached by wars. MONTHLY PATTERN: Chaitra/Baisakh -- grains cheap. Jyeshtha -- storms. Aashadh -- heavy rains and floods. Shravan/Bhadrapad/Ashwin -- disease widespread. Kartik -- grains costly. Margsheersh/Paush/Magh/Phalgu...
**Notes:** Mars years show an interesting paradox: good grain production but political violence. Flood risk in Aashadh (Jul); disease peak in monsoon end (Shravan-Ashwin). Aligns with Mars as karaka for wars and...

#### `gaur-ch1-samvatsar-mercury-lord-harmony-good-produce`
**Title:** Mercury as Samvatsar Lord = Good Produce, Satisfactory Rains, Harmony, Diseases Removed
**Source:** Gaur Ch 1, p. 6
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** The current Samvatsar has Mercury as its lord. Mercury-lord Samvatsars: #7 Shree Mukh, #27 Vijai, #47 Pramadi, #16 Chitrabhanu, #56 Dundubhi.
**Result:** Produce of grains is good. Rains are satisfactory. Farmers get good returns for their crops. People have less conflicts and more harmony. Brahmins remain busy in religious practices; people inclined towards noble deeds. Diseases are removed. No specific adverse monthly pattern noted.
**Notes:** Mercury years are generally benefic across all domains: agriculture, health, social harmony. No monthly breakdown given -- the benefic quality is uniform throughout the year. The most straightforwardly...

#### `gaur-ch1-samvatsar-saturn-lord-war-atmosphere-fearful`
**Title:** Saturn as Samvatsar Lord = War Atmosphere, People Fearful, Good Crops but Flood Losses
**Source:** Gaur Ch 1, p. 7
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** The current Samvatsar has Saturn as its lord. Saturn-lord Samvatsars: #10 Dhata, #30 Durmukh, #50 Nal, #19 Parthiv, #59 Krodhan.
**Result:** Rulers create atmosphere for war due to their diplomatic actions. People remain fearful. Crops are good. Widespread rains also cause losses. MONTHLY PATTERN: Chaitra/Baisakh -- grains costlier. Jyeshtha -- normal. Aashadh -- rains less, oils and ghee costlier. Ashwin -- juicy materials and metals costly...
**Notes:** Saturn years create geopolitical tension even when agriculture is good. Fear and insecurity are the dominant social themes. Validates Saturn transit rules from Raphael (chronic troubles in countries r...

## v12 -- Saturn transit price matrix

#### `gaur-ch3-new-year-virgo-ascendant-democracy-dissolved`
**Title:** New Year Ascendant Virgo = 'Democracy Dissolved' Alert for Middle Provinces
**Source:** Gaur Ch 3
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** The Chaitra Shukla Pratipada (New Year) chart has Virgo (Kanya) as Lagna.
**Result:** People of the Middle Provinces are dissatisfied and democracy is dissolved. East: normal; Ghee is expensive. South: drought. West: riots and expensive grains. North-East: riots.
**Notes:** Virgo is the most politically turbulent New Year ascendant. The 'democracy dissolved' indicator is unique to this ascendant. In modern context: President's Rule, Emergency, or constitutional crisis.

#### `gaur-ch3-samvat-stambha-all-pillars-max-prosperity`
**Title:** All Four Samvat Stambha Pillars Present = Maximum Prosperity Year
**Source:** Gaur Ch 3
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** Calculate Samvat Stambha for the year. ALL FOUR pillars are present (strength > 0%): Jal (Revati on Chaitra Pratipada) + Trin (Bharani on Vaishakh Pratipada) + Vayu (Mrigshira on Jyeshtha Pratipada) + Anna (Punarvasu on Aashadh Pratipada).
**Result:** Maximum benefic results for the year. Good rainfall, healthy vegetation, clean air, and abundant grain production. Overall prosperity and national well-being.

#### `gaur-ch3-samvat-stambha-jal-absent-dry-harvest`
**Title:** Samvat Stambha -- Grains Present but Water Absent = Dry Harvest Alert (Medium Year)
**Source:** Gaur Ch 3
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Calculate Samvat Stambha. Trin (Grass) AND Anna (Grain) pillars are present (> 0%). BUT Jal (Water) AND Vayu (Air) pillars are absent (= 0%).
**Result:** DRY HARVEST ALERT -- Medium/partial prosperity year. Medicinal plants and grains will sprout, but lack of rain (Jal) and wind (Vayu) prevents full maturation. Financial benefit to the state is diluted -- results are only medium. SYNERGY VETO: Even if Anna = 100%, Jal = 0% means: 'Production targets me...
**Notes:** Validated: VS 2059 (2002 Indian drought) -- Jal Stambha = 9% (Revati = 142 min / 1562 min total = 9%). Result: Indian Drought of 2002 confirmed. Cross-verify low Jal with Gaur Ch 2 Cloud Engine for pos...

#### `gaur-ch3-samvat-stambha-no-pillars-destitution`
**Title:** No Samvat Stambha Pillars Present = Total Destitution -- Overrides All Benefic Aspects
**Source:** Gaur Ch 3
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Calculate Samvat Stambha for the year. NONE of the four pillars are present (all strength = 0%): Jal = 0%, Trin = 0%, Vayu = 0%, Anna = 0%.
**Result:** TOTAL DESTITUTION AND HARDSHIP for the year. This is the HIGHEST MALEFIC WARNING LEVEL -- it overrides all other benefic planetary aspects in the Universal Chart or transit analysis.

#### `mehta-ch2-commander-not-mars-military-disorder`
**Title:** If Commander-in-Chief Is Not Mars, Military Disorder = TRUE
**Source:** Mehta/Rao Ch 2
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** In the Hindu New Year horoscope, identify the planet holding the Commander-in-Chief (Senapati) portfolio. Condition: that planet is NOT Mars.
**Result:** Military disorder is predicted. Expect disciplinary failures in armed forces, border security lapses, or ineffective military command. Defense spending may be mismanaged.

#### `mehta-ch2-foundation-dasha-overrides-transits`
**Title:** Foundation Dasha Overrides All Transit Results -- The Primary Rule
**Source:** Mehta/Rao Ch 2
**Severity:** high | **Checkable:** False | **Weight:** 1.0
**Condition:** A transit result (Step 6) conflicts with the Foundation Horoscope's Dasha result (Step 1). Example: transit of Jupiter through 9th house suggests prosperity, but Foundation Chart is running Saturn Mahadasha in the 8th.
**Result:** The Foundation Dasha result OVERRIDES the transit. Treat nations as 'Natives' -- their natal Dasha is primary. All subsequent steps (2-9) modify, they do not replace, the Foundation signal. This is the single most important rule in the 9-Step Scheme.
**Notes:** This rule prevents the common error of over-weighting transits in mundane work. Foundation charts for key nations: India = Independence chart Aug 15, 1947, Taurus Lagna. USA = Leo 29° Lagna (superpowe...

#### `mehta-ch2-mars-lagna-new-year-turbulent`
**Title:** Mars in Lagna of New Year Chart + Aspects Sun/Moon/Mercury = Turbulent Year
**Source:** Mehta/Rao Ch 2
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** In the Chaitra Shukla Pratipada (New Year) chart: Mars occupies the Lagna AND Mars aspects Sun, Moon, or Mercury.
**Result:** Turbulent year predicted. Expect political upheaval, conflict, communal violence, or sudden reversal of national policy.

#### `mehta-ch2-sat-mars-6th-house-military-domestic`
**Title:** Saturn-Mars Conjunction in 6th House of National Chart = Military Operation Against Domestic Threats
**Source:** Mehta/Rao Ch 2
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn and Mars conjoin in the 6th house of a nation's Foundation Chart (or in the sign that falls in the 6th house from the national Lagna).
**Result:** Extreme violence and 'Black Days' in national history. Specifically: military action against domestic/internal enemies. 6th house = internal security, enemies, borders.
**Notes:** Historical validation: Operation Blue Star (1984) -- Saturn-Mars conjunction in the 6th house of India's Foundation Chart timed the military action against the Golden Temple. General Saturn-Mars conjun...

#### `mehta-ch2-saturn-rohini-famine-war-highest-alert`
**Title:** Saturn Transiting Rohini Nakshatra = Famine or Devastating War (Highest Alert)
**Source:** Mehta/Rao Ch 2
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Transit Saturn passes through Rohini Nakshatra (Taurus 10°00' to 23°20' sidereal).
**Result:** HIGHEST LEVEL WARNING in all of mundane astrology. This is the Rohini Shakata Bhedan Yoga. Predicts devastating war OR 12-year famine for the affected region/nation.
**Notes:** Rohini is the Moon's own nakshatra -- its affliction by Saturn represents the worst possible agricultural and security scenario. Historical validations of this rule exist across multiple Indian and glo...

#### `mehta-ch2-triple-conjunction-sat-mars-rahu-global-destruction`
**Title:** Saturn + Mars + Rahu Together in a Quadrant = Global Destruction Scheme
**Source:** Mehta/Rao Ch 2
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn, Mars, and Rahu simultaneously occupy the same quadrant (kendra house: 1st, 4th, 7th, or 10th from any national Lagna or within approximately 90° of each other in the zodiac).
**Result:** GLOBAL DESTRUCTION SCHEME = TRUE. This is the most severe conjunction alert. Expect coordinated large-scale destruction events at global level.
**Notes:** Apply the 1-degree orb rule for maximum precision: if Sun, Saturn, Moon, and Rahu are within 1° of each other, the alert level is 'Catastrophic Mundane Event.'

## v13 -- Koorma directional + Sanghatta Chakra + war gates

#### `gaur-ch11-eclipse-capricorn-vip-families-medicine`
**Title:** Eclipse in Capricorn = Families of VIPs and Medicine Manufacturers Suffer
**Source:** Gaur/AIFAS Ch 11
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A solar or lunar eclipse occurs in Capricorn (Makar rashi).
**Result:** Families of VIPs and ministers face personal tragedies or public scandals. Medicine manufacturers and pharma sector suffer losses or regulatory setbacks. Capricorn rules India overall -- so this is a particularly sensitive eclipse position for India.

#### `gaur-ch11-eclipse-chaitra-variable-rains`
**Title:** Eclipse in Chaitra Month = Variable Rains (Floods/Drought); Intellectuals Suffer
**Source:** Gaur/AIFAS Ch 11
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** A solar or lunar eclipse occurs in the Hindu month of Chaitra (March-April).
**Result:** Variable and erratic rainfall patterns -- simultaneous drought in some regions and floods in others. Suffering specifically for intellectuals, writers, and artists.

#### `gaur-ch11-eclipse-jyeshtha-govt-change`
**Title:** Eclipse in Jyeshtha Month = Change of State Governments; VIPs Suffer
**Source:** Gaur/AIFAS Ch 11
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A solar or lunar eclipse occurs in the Hindu month of Jyeshtha (May-June).
**Result:** Change of state governments -- ruling parties fall or key reshuffles occur. Suffering for VIPs and senior executives.
**Notes:** Combine with Gopal Ch 9 saturn-trika-transit rule for compounding signal: eclipse in Jyeshtha + Saturn in trika = near-certain government collapse.

#### `gaur-ch11-eclipse-leo-political-parties-suffer`
**Title:** Eclipse in Leo = Political Party Officials (Ruling and Opposition) Suffer
**Source:** Gaur/AIFAS Ch 11
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** A solar or lunar eclipse occurs in Leo (Simha rashi).
**Result:** Both ruling party and opposition party officials suffer personal setbacks, health issues, or political downfall. Leo = the sign of kings and power.

#### `gaur-ch4-koorma-back-malefic-heartland-unrest`
**Title:** Malefic in Koorma Back Constellations = Unrest in Central Provinces / Heartland
**Source:** Gaur/AIFAS Ch 4
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A malefic planet transits or afflicts the Koorma Back constellations: Krittika, Rohini, or Mrigshira.
**Result:** Inland Rebellion Monitor triggered. Unrest in the Heartland / Central Provinces of the mapped territory. Rohini specifically activates the global war threshold (see Rohini gate rule).
**Notes:** Rohini (Taurus 10°-23°20') is the single most critical nakshatra in all of mundane astrology. Affliction here by Saturn alone triggers the Rohini War Gate (AH-08). Krittika and Mrigshira affliction in...

#### `gaur-ch4-koorma-benefic-segment-progress`
**Title:** Benefic in Any Koorma Segment = Bliss and Progress for That Region
**Source:** Gaur/AIFAS Ch 4
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** A benefic planet (Jupiter, Venus, well-placed Mercury, waxing Moon) transits or positively aspects a constellation in any Koorma grid segment.
**Result:** The geographical direction/region corresponding to that Koorma segment enjoys Anand (bliss) and measurable progress: trade expansion, good harvests, political stability, social harmony.

#### `gaur-ch4-koorma-tail-malefic-west-calamity`
**Title:** Malefic in Koorma Tail Constellations = Critical Calamity Alert for West India
**Source:** Gaur/AIFAS Ch 4
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A malefic planet (Saturn, Rahu, Mars, Ketu) transits or creates Vedha on any of the Koorma Tail constellations: Jyeshtha, Mool, or Poorvashadh.
**Result:** Critical Vulnerability Alert for West India / Gujarat / Rajasthan. Predicted events: war, severe natural calamity, or major civil unrest. The western direction of the mapped landmass is most afflicted.
**Notes:** Saturn in Jyeshtha is particularly significant as Jyeshtha rules kings and power. Cross-validate: if Saturn is simultaneously creating Vedha via Sanghatta grid, the calamity weight doubles.

#### `gaur-ch4-koorma-vedha-synchronization`
**Title:** Regional Alert Requires BOTH Koorma Occupation AND Sarvatobhadra Vedha
**Source:** Gaur/AIFAS Ch 4 (Report 3: JSON Refinements)
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** A malefic occupies a Koorma constellation segment. Additionally verify: is that malefic ALSO creating Vedha on those constellations via the Sarvatobhadra Chakra (Ch 9) grid?
**Result:** A regional alert is valid ONLY when BOTH conditions are satisfied: (1) malefic transits the Koorma segment, AND (2) that malefic creates Vedha on the same constellations. Single-condition alerts are advisory; dual-condition alerts are actionable.
**Notes:** This is the validation gate that prevents false positives. Without Sarvatobhadra confirmation, the Koorma signal is 'background noise' only.

#### `mehta-ch8-rohini-gate-saturn-war-famine`
**Title:** Saturn Transiting Rohini = Devastating War or 12-Year Famine (Highest Alert)
**Source:** Mehta Ch 8
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** Transit Saturn enters Rohini Nakshatra (Taurus 10° to 23° 20'). Alert is upgraded to CRITICAL if Rahu is also present in or aspecting Rohini.
**Result:** Devastating war OR 12-year famine -- historically, one of the two always manifests. WWI (1914-18), WWII (1939-45), and the 1971 Indo-Pak War all began with Saturn in Rohini. If Rahu co-occupies or aspects: dual-threat confirmed -- both war AND famine risk.
**Notes:** This is the single highest-severity rule in the entire mundane astrology corpus. No other planetary configuration has been as consistently validated across world wars. Historical benchmarks: Saturn in...

#### `mehta-ch8-rohini-ketu-rahu-mars-aspect-massacre`
**Title:** Ketu or Rahu in Rohini + Mars Aspect = Critical War Risk / Massacre Alert
**Source:** Mehta Ch 8
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** Rahu or Ketu transits Rohini Nakshatra (Taurus 10°-23°20') AND Mars simultaneously aspects Rohini by any aspect.
**Result:** War Risk = CRITICAL. Internal rebellion and large-scale massacres are likely. Historical example: June 1984 Punjab crisis (Operation Blue Star) -- Ketu in Rohini with Mars aspect → massacre.
**Notes:** The Mars aspect acts as the 'ignition trigger' for the underlying Rahu/Ketu tension. Dramatic events rarely happen at the moment of conjunction -- they materialize when Mars conjoins or aspects the pre...

#### `mehta-ch8-sanghatta-seventh-house-war-ignition`
**Title:** Saturn + Mars Vedha on Nation's 7th House = War / International Conflict Ignition
**Source:** Mehta Ch 8
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** In a national horoscope (foundation chart), the 7th house lord or the 7th house sign is under simultaneous Sanghatta Vedha from both Saturn and Mars.
**Result:** War or international conflict ignition for that nation. The 7th house governs International Disputes, Rebellions, and Foreign Affairs. Vedha here from malefics overrides any benefic standard transits.
**Notes:** Chakra aspect primacy rule: treat Sanghatta Vedha as the primary ignition source. This rule is the formal diagnostic gate for all war predictions -- any war prediction MUST confirm Vedha on the 7th hou...

#### `mehta-ch8-triple-malefic-destruction-scheme`
**Title:** Saturn + Mars + Rahu in Quadrant or Mutual Sanghatta Vedha = Global Destruction Warning
**Source:** Mehta Ch 8
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn, Mars, and Rahu simultaneously meet on the Sanghatta grid -- either in the same quadrant, in mutual Vedha (Front/Left/Right vectors), or in a conjunction within 10° of each other.
**Result:** GLOBAL DESTRUCTION WARNING -- the Destruction Scheme is active. Predicted: major global conflict, mass casualties, collapse of established order. Trigger 'Global Destruction Warning' at the highest diagnostic level.
**Notes:** This is one of two 'critical severity' configurations in Mehta's system (the other being Saturn-Rahu in Capricorn for major global conflict). Cross-validate with Mehta Ch 2 Step 8: 'IF Saturn AND Mars...

## v14 -- Macro-conjunctions + transit timing

#### `gaur-ch10-drought-ingress-alert`
**Title:** Sun Ingress on Sun/Tue/Sat + 15-Muhurti Ingress = Critical Water Scarcity and Food Inflation
**Source:** Gaur/AIFAS Ch 10
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** The Sun enters (Sankranti) any zodiac sign on a Sunday, Tuesday, or Saturday AND the ingress occurs in a 15-Muhurti constellation (Bharani, Ardra, Ashlesha, Jyeshtha, or Shatbhisha).
**Result:** 'Critical Water Scarcity and Food Inflation Alert' for the month of that transit. Grains and juicy materials become expensive; rainfall is below normal.
**Notes:** Both conditions must be true simultaneously for maximum severity. Either condition alone is a medium alert; both together = critical. The 15-muhurti constellation list: Bharani, Ardra, Ashlesha, Jyesh...

#### `gaur-ch10-saturn-station-direct-oils-spices-spike`
**Title:** Saturn Turning Direct from Retrograde = Oils and Spices Expensive for 60 Days
**Source:** Gaur/AIFAS Ch 10
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn changes its motion state from Retrograde to Direct (Saturn goes Stationary-Direct).
**Result:** 'Price Spike Warning: Oils and Spices (Asafetida, Chillies) will remain expensive for the next 60 days.' This spike is independent of the sign Saturn occupies.
**Notes:** Retrograde-to-Direct station is a universal Saturn trigger regardless of sign position. The 60-day (2-month) window applies from the exact date of the station. Cross-validate with Saturn sign results ...

#### `mehta-ch10-mars-ignition-rule`
**Title:** Mars Ignition Rule -- Historical Events Materialize When Mars Triggers Conjunction Degree
**Source:** Mehta/Rao Ch 10
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A Saturn-Jupiter, Saturn-Rahu, or Saturn-Mars conjunction / opposition has occurred. Mars then transits to conjoin or aspect the exact degree of that prior conjunction.
**Result:** The actual historical event (war, revolution, massacre, economic collapse) materializes. Do NOT predict the event at the moment of the original conjunction -- Mars is the 'Minute Hand' that fires the trigger. Monitor the next Mars transit to the conjunction degree for the event window.
**Notes:** This is the single most important operational refinement in macro-temporal forecasting. Without Mars triggering, a conjunction creates 'background tension' only -- not an event. Apply 1-degree orb for ...

#### `mehta-ch10-saturn-jupiter-great-mutation-era-shift`
**Title:** Saturn-Jupiter Great Mutation (First Conjunction in New Triplicity) = Era-Level Turning Point
**Source:** Mehta/Rao Ch 10
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A Saturn-Jupiter conjunction occurs in a triplicity (Fire/Earth/Air/Water) for the FIRST time after a long period in the previous triplicity. This is the 'Great Mutation' -- the change of triplicity.
**Result:** Era-Level Turning Point with permanent impact for the next 200 years: Earthy triplicity = material growth and shifts in world financial dominance; Fiery triplicity = wars of ideology and rapid territorial expansion; Airy triplicity = technology revolutions and democratic movements; Watery triplicity...
**Notes:** The current Great Mutation in Aquarius (January 2020) marks the transition from Earthy triplicity (Capricorn dominance 1802-2020) to Airy triplicity -- signaling a century of technology, social upheava...

#### `mehta-ch10-saturn-mars-watery-sign-tsunami`
**Title:** Saturn-Mars Conjunction in Watery Sign = Critical Tsunami / Maritime Flood Risk
**Source:** Mehta/Rao Ch 10
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn and Mars conjoin in a Watery Sign: Cancer, Scorpio, or Pisces.
**Result:** Critical Tsunami / Maritime Flood Risk -- immediate 'Maritime Disaster or Flood-based Tragedy' alert. Large-scale loss of life by water-related catastrophe.
**Notes:** VALIDATED: 2004 Asian Tsunami -- Saturn and Mars in Cancer. This rule produces one of the highest historically-validated hit rates in the corpus. Cross-validate with Moon affliction in the same watery ...

#### `mehta-ch10-saturn-rahu-eighth-twelfth-house-humiliation`
**Title:** Saturn-Rahu Conjunction in Nation's 8th or 12th House = National Setback / Loss of Prestige
**Source:** Mehta/Rao Ch 10
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn and Rahu conjoin in the 8th or 12th house of a nation's foundation chart.
**Result:** National Setback and Loss of Prestige -- the nation suffers a humiliating defeat, territorial loss, economic collapse, or major institutional failure on the world stage.

## v15 -- Mars/Mercury/Jupiter/Venus/Rahu transits + Koorma kill-switch

#### `gaur-ch10-mars-retrograde-gold-silver-expensive`
**Title:** Retrograde Mars = Gold, Silver, Wheat, and Red Items Remain Expensive
**Source:** Gaur/AIFAS Ch 10
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Mars is in retrograde motion in any sign.
**Result:** Gold, silver, wheat, red things, and goods influenced by Mars's own signs remain expensive. This holds regardless of the sign Mars occupies.

#### `gaur-ch10-rahu-libra-drought-veto`
**Title:** Rahu in Libra = Drought Veto -- Agricultural Failure Even If Other Planets Promise Rain
**Source:** Gaur/AIFAS Ch 10
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Rahu transits Libra (Tula rashi). Duration: ~18 months.
**Result:** 'Drought Veto' activated -- agricultural failure and grain price inflation are predicted even if other planetary configurations suggest rainfall. Grains become expensive throughout this transit.
**Notes:** Libra rules Austria, Tibet, Kashmir, and parts of USA/Japan. This is a 1.5-year 'Vulnerability Window' for water scarcity in these regions. Cross-validate with Koorma Chakra for Anarta (Gujarat/Sauras...

#### `gaur-ch10-venus-direct-station-luxury-spike`
**Title:** Venus Turning Direct = Price Spike in Gold, Gems, and Fine Silks; Cotton Bearish
**Source:** Gaur/AIFAS Ch 10
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Venus changes motion from Retrograde to Direct (Venus Stationary-Direct).
**Result:** 'Luxury Market Inflation Alert': Gold, gems, silks, ghee, silver, and gur become expensive. Cotton sector enters bearish trend (cotton cheap).

#### `mehta-ch7-koorma-regime-collapse-kill-switch`
**Title:** Malefic Afflicting Koorma Star Cluster = Regime Collapse Risk for Corresponding Territory
**Source:** Mehta/Rao Ch 7
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A malefic planet (Saturn, Mars, Rahu, Ketu) occupies, aspects, or creates Vedha on any of the 9 Koorma directional star clusters. Use the Regime Collapse Kill-Switch table (spec: mehta-ch7-koorma-chakra-reconciled) to identify the at-risk territory.
**Result:** 'Regime Stability Crisis' alert for the mapped territory. The ruler or ruling party of that region faces high risk of collapse, removal, or defeat. Example: Malefic in Ardra/Punarvasu/Pushya cluster → 'Regime Crisis in Magadha (Bihar)'.
**Notes:** This is a BINARY logic gate -- the kill-switch fires regardless of standard yearly benefic trends. Retrograde malefic in the cluster = maximum severity. Cross-validate with national 10th house (Ruling ...

## v16 -- Gaur Ch5/6/7 monsoon + crop + Sarvatobhadra trade

#### `mundane-gaur-ch5-ardra-drought-riot`
**Title:** Ardra Entry Drought & Civil Unrest -- Triteeya + Vyaghat Yoga
**Source:** Gaur Ch 5 -- Ardra Entry & Rohini Chart
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** Ardra Entry Tithi = Triteeya AND Nitya Yoga at Entry = Vyaghat
**Result:** CRITICAL WARNING: Severe drought followed by civil unrest and high commodity prices. Grain production will fail; riots and public disorder expected during the rainy season.

#### `mundane-gaur-ch5-ardra-wednesday-prosperity`
**Title:** Ardra Entry Wednesday or Thursday -- National Prosperity Signal
**Source:** Gaur Ch 5 -- Ardra Entry Weekday
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Ardra Entry Weekday = Wednesday OR Thursday AND Nitya Yoga IN (Shubh, Sukarma, Vriddhi, Preeti)
**Result:** OPTIMAL MONSOON: Excellent crops and cheap prices (Wednesday) / Prosperous season (Thursday). When combined with auspicious Yoga, national food security is high and low inflation predicted for the year.

#### `mundane-gaur-ch5-rohini-mountain-drought`
**Title:** Rohini Mountain Residence -- Guaranteed Drought Signal
**Source:** Gaur Ch 5 -- Rohini Chart (Samudra Chakra)
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** Rohini Samudra Chakra Residence = Mountain (Parvat)
**Result:** DROUGHT CONFIRMED: Scanty rains; acute crop suffering. Potter's House residence indicates fragile agricultural economy for the year. Hydrological Stress flag active regardless of Ardra Entry weekday result.
**Notes:** Mountain residence overrides positive weekday/tithi signals -- it is the strongest standalone drought indicator in this system.

#### `mundane-gaur-ch6-saptnadi-dahan-fire`
**Title:** Saptnadi Dahan Nadi Vedha -- Fire on Earth Alert
**Source:** Gaur Ch 6 -- Saptnadi Chart
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Two or more planets concentrated in Dahan Nadi (Mrigshira, Chitra, Moola, Revti) -- Vedha triggered
**Result:** FIRE HAZARD: High risk of fires on earth -- forest fires, industrial fires, or military conflagration. Dahan (combustion) Nadi lord is Mars. Drought conditions likely to co-occur.

#### `mundane-gaur-ch6-saptnadi-jala-36hrs`
**Title:** Saptnadi Jala Nadi Vedha -- 36-72 Hour Sustained Rain
**Source:** Gaur Ch 6 -- Saptnadi Chart
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Gentle AND Cruel planets bundled in Jala Nadi (Pushya, Poorvaphalguni, Abhijit, Shatbhisha)
**Result:** METEOROLOGICAL ALERT: Continuous precipitation predicted for next 36 to 72 hours. Excessive rain; flood monitoring recommended for low-lying areas.

#### `mundane-gaur-ch7-bumper-harvest-yoga-i`
**Title:** Crop Yoga I -- Benefics in Quadrants = Bumper Harvest + Cheap Grains
**Source:** Gaur Ch 7 -- Sasya Jatak Crop Yogas
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Benefic planets (Jupiter, Venus, Mercury, Moon) occupy quadrant houses (1st, 4th, 7th, 10th) from the transiting Sun OR Sun is aspected by strong benefics in the seasonal ingress chart
**Result:** BUMPER HARVEST: Produce = High. Inverse Pricing Rule triggers Bearish trend for grain commodities. Grain prices to drop significantly. Trade module must flag 'Bearish/Low Price' for all grain categories.

#### `mundane-gaur-ch7-food-security-gate`
**Title:** Food Security Gate -- Strong Lagna + Jupiter Aspects 4th House
**Source:** Gaur Ch 7 -- Sasya Jatak Diagnostics
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Crop Horoscope Lagna = Strong (no malefic influence) AND Jupiter aspects the 4th House of the seasonal ingress chart
**Result:** BUMPER HARVEST: National food security high. Grain prices to drop significantly. Inverse Pricing: Trade module flags all grain/pulse categories as Bearish. Dairy (if Jupiter in 10th) also Abundant.

#### `mundane-gaur-ch7-malefic-interference-yoga-vii`
**Title:** Crop Yoga VII -- Sun Between Mars & Saturn = Crop Destroyed
**Source:** Gaur Ch 7 -- Sasya Jatak Crop Yogas
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Sun positioned between Mars AND Saturn (Mars one side, Saturn the other) OR Mars AND Saturn together in 7th house from Sun
**Result:** CROP DESTRUCTION: Produce = Destroyed/Poor. Grains = Expensive. Inverse Pricing Rule triggers Bullish trend for grain commodities. Extended period of elevated grain prices expected.

#### `mundane-gaur-ch7-sprouting-failure-yoga-viii`
**Title:** Crop Yoga VIII -- Malefic in 2nd from Sun = Sprouting Failure
**Source:** Gaur Ch 7 -- Sasya Jatak Crop Yogas
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** Malefic planet in 2nd house from the Sun in seasonal ingress chart AND Sun lacks any benefic aspect
**Result:** AGRICULTURAL CRISIS: Crop destroyed soon after sprouting. Reseeding required -- farmers must prepare for high-cost second sowing. Initial market supply will be severely disrupted; grain prices spike early in season.

#### `mundane-gaur-ch8-saturn-retrograde-industrial`
**Title:** Saturn Retrograde -- Steel & Industrial Production Slowdown
**Source:** Gaur Ch 8 -- Material Database (Saturn-Factory Veto)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn is Retrograde in any sign
**Result:** PRODUCTION SLOWDOWN ALERT: Steel mills and heavy factories face output reduction. Saturn governs Steel, Iron, Machinery, Chemicals, and Foreign Capital. Retrograde motion signals supply contraction → steel and iron prices rise.

## v17 -- Gopal Ch3 (leadership auth) + Gopal Ch14 (markets)

#### `mundane-gopal-ch14-4th-venus-car-buyers`
**Title:** Strong 4th House + Well-Placed Venus -- Record Car Buyers
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (4th house is strong -- Lord in own sign, exalted, or with benefics) AND (Venus is well-placed -- exalted, own sign, or in Kendra/Trikona)
**Result:** Market Forecast: 'Record level of first-time car buyers. Volume auto brands (entry-level and mid-segment) achieve all-time sales highs. Lower-end segments significantly outperform luxury segments due to first-time buyer demographics entering the market'. Validation: 2006 Maruti, Bajaj bull run confi...

#### `mundane-gopal-ch14-6th-lord-pharma-wealth`
**Title:** 6th Lord in 11th House or Dhana Yoga -- Pharma Dream Run
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (6th lord is placed in the 11th house) OR (6th lord participates in a Dhana Yoga -- combination with 2nd or 11th lord)
**Result:** Industry Alert: 'Pharmaceutical and Healthcare sectors will achieve exceptional profitability -- record exports and R&D breakthroughs. Hospital chains enter a growth phase. Medical stocks outperform the broader index'. Validation: 2006 India pharma dream run confirmed in source audit.

#### `mundane-gopal-ch14-cluster-boss-coalition-stability`
**Title:** 9th House Cluster in Oath Chart -- Coalition Stability via Compromise
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (3 or more planets occupy the 9th house of the oath-taking chart)
**Result:** Governance Pattern: 'Leader will recognise multiple bosses and lack full autonomy. Despite apparent weakness, government achieves surprising stability through compromise and coalition management. Do not forecast early collapse -- the multi-boss constraint IS the stabiliser'. Validation: Manmohan Sing...

#### `mundane-gopal-ch14-mars-upchayya-auto-exports`
**Title:** Mars in Upchayya from Lagna -- Auto Ancillary Export Boom
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Mars is transiting an Upchayya house -- 3rd, 6th, 10th, or 11th -- from the National Lagna in the Annual/Varsha Chart)
**Result:** Auto Sector Forecast: 'Auto ancillary companies become export-oriented profit centres. Manufacturing efficiency peaks -- electrical components, metal parts, and precision engineering sub-sectors lead the rally'. Note: Upchayya houses improve with time -- Mars here is progressively stronger.

#### `mundane-gopal-ch14-mercury-jupiter-banking`
**Title:** Mercury Bhukti + Jupiter in 2nd House -- Banking Computerisation
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Mercury Bhukti is active in national chart) AND (Jupiter is placed in or transiting the 2nd house)
**Result:** Banking Forecast: 'Massive computerisation of the banking sector and introduction of new revenue models (online banking, mobile wallets, investment products). Banking stocks enter a sustained bull run'. Validation: 2003-2006 Indian banking transformation confirmed.

#### `mundane-gopal-ch14-saturn-8th-defeat`
**Title:** Saturn 8th from Natal Moon or Lagna -- Defeat Predicted
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Transiting Saturn enters the sign 8th from the native's Natal Moon OR 8th from the native's Natal Lagna)
**Result:** Defeat Likely: 'The native enters a period of maximum obstruction, loss, and humiliation. Political leaders in this transit face electoral defeat or forced resignation. Businesses face insolvency risk. For nations: incumbent government at high risk of collapse'.

#### `mundane-gopal-ch3-10th-in-3rd-innovator`
**Title:** 10th Lord in 3rd House -- Author/Innovator/Technology Career
**Source:** Gopalakrishnan Ch 3 -- Celebrity Horoscope Analysis
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (10th lord is placed in the 3rd house of the native's chart)
**Result:** Career Signature: 'Native will dominate in communication-based fields -- Writing, Authorship, Information Technology, Software innovation, or Media. The 3rd house connection gives the career a distinctly intellectual and communication-driven flavour'. Validation: Bill Gates -- 10th lord in 3rd → softw...

#### `mundane-gopal-ch3-national-trika-lagna`
**Title:** Politician's Lagna in National Trika -- Limited Success Alert
**Source:** Gopalakrishnan Ch 3 -- Celebrity Horoscope Analysis
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Politician's Lagna falls in the 6th, 8th, or 12th house from the National Foundation Chart Lagna) -- e.g., for India (Taurus Lagna): Libra (6th), Sagittarius (8th), or Aries (12th)
**Result:** Limited Success Alert: 'Native will face systemic opposition from the national establishment. Career advancement in national politics is structurally obstructed by the nation's own astrological geometry'.

#### `mundane-gopal-ch3-struggle-to-success`
**Title:** Raja Yoga in 8th House -- Struggle-to-Success Career Pattern
**Source:** Gopalakrishnan Ch 3 -- Celebrity Horoscope Analysis
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Raja Yogas -- two or more Trikona/Kendra lords conjoined -- occur in the 8th House of the native's chart)
**Result:** Career Pattern Alert: 'Significant early struggle, breaks, and reversals followed by a phenomenal rise and eventual iconic status'. The obstacles ARE the path -- do not interpret 8th house placements as failure'. Validation: Amitabh Bachchan -- 10th lord in 8th, Saturn Dasha triggered iconic career.

#### `mundane-gopal-ch3-triple-check-fail`
**Title:** Celebrity Triple Check Failure -- Chart Rejected
**Source:** Gopalakrishnan Ch 3 -- Celebrity Horoscope Analysis
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (10th lord is NOT strong from at least 2 of: Lagna, Chandra Lagna, Karkamsha Lagna) -- i.e., Strength Coefficient < 0.60
**Result:** Chart Rejected: 'Data Unreliable -- perform birth rectification before processing any governance, election, or career query for this native'. Engine processing halted.

## v18 -- Gopal Ch5 (oath chart) + Mehta Ch18 (election lagna)

#### `mundane-gopal-ch5-11th-in-8th-market-rule`
**Title:** 11th Lord in 8th House -- Stock Market Below Prior Administration
**Source:** Gopal Ch 5 -- Oath Taking Charts
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the 11th lord (house of government gains, revenue, stock market) is placed in the 8th house (house of functional longevity, mass deaths, scams) in the oath taking chart
**Result:** Foreign reserves and stock market performance will be LOWER at the end of this administration's tenure than at its start, and lower than the preceding government's market performance. The 8th house placement of the income lord directs gains into the house of obstruction and hidden matters. Economic ...

#### `mundane-gopal-ch5-graha-yuddha-veto`
**Title:** Graha Yuddha in Oath Chart -- Terminal Stability Veto
**Source:** Gopal Ch 5 -- Oath Taking Charts
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF two planets (excluding Sun and Moon) are within 1° of each other (Graha Yuddha / Planetary War) in the oath taking chart → Graha Yuddha veto triggered
**Result:** Terminal stability veto: the government cannot rule peacefully regardless of its parliamentary majority or popular mandate. The losing planet in the war (lower degree = loser) represents a critical governance sector that is permanently compromised. Administration is marked by continuous internal con...

#### `mundane-gopal-ch5-jaimini-medium-tenure`
**Title:** Jaimini Ayurdaya: Medium Tenure Gate -- Dual + Dual Sign Types
**Source:** Gopal Ch 5 -- Oath Taking Charts
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Lagna Lord of oath chart is in a Dual/Dwiswabhava sign (Gemini/Virgo/Sagittarius/Pisces) AND 8th Lord of oath chart is in a Dual/Dwiswabhava sign → Jaimini Ayurdaya classification = Medium Life
**Result:** Government will likely complete its mandate but may face mid-term crises, reshuffles, or a significantly weakened second half. Dual-sign energy produces an administration that pivots policy direction at least once. Prognosis: term completed but not without significant internal transitions.

#### `mundane-mehta-ch18-chandrashekhar-collapse-pattern`
**Title:** Chandrashekhar 1990 -- Transitionary Collapse Pattern
**Source:** Mehta Ch 18 -- Leadership Autopsy Database
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF oath chart shows ALL of the following: (1) No independent parliamentary majority (externally verified), (2) 7th lord (opposition) stronger than 10th lord (executive), (3) 4th house (domestic stability / High Command support) afflicted or empty of benefics, (4) Moon in the last degrees (27°-29°) o...
**Result:** Chandrashekhar (oath: 10 November 1990) -- 5 adverse features. His government was entirely dependent on Congress (I) outside support. When that support was withdrawn (March 1991), the government fell with 7 months of tenure completed. Pattern indicates: the administration is structurally transitionar...

#### `mundane-mehta-ch18-papakatari-discord`
**Title:** Papakatari Yoga on Lagna -- Continuous Bickering Administration
**Source:** Mehta Ch 18 -- Importance of Muhurta in Oath Taking
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF both the 12th house AND the 2nd house from Lagna in the Muhurta chart are occupied by malefic planets (Saturn/Mars/Rahu/Ketu/Sun) → Papakatari Yoga on Lagna formed
**Result:** Papakatari Yoga on the Lagna hemmed between two malefics creates an administration characterised by: (1) Continuous bickering and infighting within the Cabinet; (2) Public perception of a fractious, uncoordinated government; (3) Communication failures -- government cannot deliver a clear message (2nd...

## v19 -- Gopal Ch4 (election engine) + Mehta Ch22/23 (cabinet)

#### `mundane-gopal-ch4-rasi-sandhi-10th-lord-spoiler`
**Title:** Rasi Sandhi Spoiler -- 10th Lord at 0°/29° Negates Apparent Strength
**Source:** Gopal Ch 4 -- How to Predict for Elections
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF a candidate's 10th lord is placed at 0° or 29° of any sign (Rasi Sandhi -- sign junction point) in ANY of the Tri-Lagna reference charts → Rasi Sandhi Spoiler veto triggered for that reference point
**Result:** The Rasi Sandhi placement NEGATES the house-based strength of the 10th lord. A 10th lord in the 11th house that is at 29° is treated as WEAK, not strong, for the purposes of the Tri-Lagna comparison. Even a candidate who appears to have a strong 10th lord position will fail to 'cross the finish line...

#### `mundane-gopal-ch4-saturn-transit-defeat-veto`
**Title:** Saturn Ashtama Transit -- 8th from Moon/Lagna = Defeat Likely
**Source:** Gopal Ch 4 -- How to Predict for Elections
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Saturn is transiting the 8th house from the candidate's natal Moon OR 8th house from the natal Lagna (Ashtama Shani) at the time of the election → Saturn Ashtama Transit defeat signal triggered
**Result:** Defeat Likely under Ashtama Shani. The 8th transit of Saturn from Moon or Lagna is the classical maximum-obstruction period -- exhaustion of vitality, cumulative burdens reaching a peak, and the inability to project forward momentum. In an election context: the candidate cannot sustain the campaign e...

#### `mundane-gopal-ch4-sixth-lord-nexus-defeat`
**Title:** 6th Lord Nexus -- 10th Lord Contaminated by Opposition = Defeat by Intrigue
**Source:** Gopal Ch 4 -- How to Predict for Elections
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF a candidate's 10th lord is conjunct the 6th lord OR receives a direct aspect from the 6th lord in the natal chart (from any of the three Tri-Lagna reference points) → 6th Lord Nexus defeat signal triggered
**Result:** The candidate's authority/career indicator (10th lord) is contaminated by the house of enemies, obstacles, and opposition (6th lord). This candidate will lose power through opposition manoeuvring, legal challenges, internal party betrayal, or engineered political scandal. The defeat is NOT a clean e...

#### `mundane-gopal-ch4-tri-lagna-sweep-winner`
**Title:** Tri-Lagna Sweep -- 10th Lord Strong in 2+ Reference Points = Victory
**Source:** Gopal Ch 4 -- How to Predict for Elections
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Candidate A's 10th lord is STRONG (in 11th, 9th, exalted, Vargottama, or Raja Yoga) in 2 or more of the three Tri-Lagna reference points (Lagna / Chandra Lagna / Karkamsha Lagna) AND Candidate B's 10th lord scores 0-1 strong reference points → Tri-Lagna Sweep triggered for Candidate A
**Result:** Prediction: Candidate A is the projected election winner. The higher the frequency of strong 10th lord placements, the higher the victory margin. A 3/3 sweep (all three reference points strong) indicates a landslide; a 2/3 score indicates a comfortable majority. Validated: Bush 2000 (3/3 sweep) vs. ...

#### `mundane-mehta-ch22-moon-raja-prosperity-affliction`
**Title:** Moon as Raja -- Prosperity or National Pain (Depends on Moon Condition)
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Moon is the Raja (King) for the year → check Moon's condition in the Hindu New Year chart: Unafflicted Moon = Prosperity gate; Afflicted Moon = National Pain gate
**Result:** UNAFFLICTED Moon Raja: Prosperity declared -- plenty of rain and food, joy and mirth, flourishing vegetation, prosperous and happy citizenry, healthcare measures succeed. Social harmony is the year's dominant tone. AFFLICTED Moon Raja (aspected by Saturn/Rahu/Mars, or combust, or in Grahayudha): Nati...

#### `mundane-mehta-ch22-saturn-raja-famine-misery`
**Title:** Saturn as Raja -- Famine, Scarcity, and Societal Misery Year
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Saturn is the Raja (King) for the year → Saturn governance tone year declared
**Result:** Difficult year declared. Classical outcomes: poor rainfall, robber and criminal activity elevated, sinful and corrupt acts normalized, destruction of crops, general societal misery. Modern calibration: mass strikes, austerity measures, food shortages, administrative frustration, heavy industry and l...

## v2n -- Gopal Ch2 + Mehta Ch6 + Raphael Ch3 (novel rules only)

#### `mundane-gopal-ch2-celebrity-authentication`
**Title:** Gopal Ch 2 -- Celebrity / Leader Chart Authentication Rule
**Source:** Gopal Ch 2 -- 10th House Verification
**Severity:** high | **Checkable:** False | **Weight:** 1.0
**Condition:** IF the 10th lord is NOT strong from at least 2 of [Lagna, Chandra Lagna, Karkamsha Lagna] THEN reject chart (Gate 1 failure); IF the 10th house is vacant AND unaspected by any planet THEN reject chart (Gate 2 failure); Apply Gate 1 then Gate 2 as the FIRST check before any analysis of any celebrity ...
**Result:** Chart passes authentication: proceed with full analysis. Chart fails Gate 1 or Gate 2: output 'Chart Rejected -- Potentially Inauthentic Birth Data' and halt. Do not apply any further planetary or dasha analysis until birth data is verified against public records.

#### `mundane-gopal-ch2-saturn-transit-regime-cycle`
**Title:** Gopal Ch 2 -- Saturn Transit Regime Cycle (4th/8th/12th House Trigger)
**Source:** Gopal Ch 2 -- Law of Karma in Office
**Severity:** high | **Checkable:** False | **Weight:** 1.0
**Condition:** IF Saturn transits through the 4th, 8th, or 12th house from a political leader's natal Moon THEN regime change, electoral defeat, or loss of power is triggered -- this is the 'Law of Karma in Office'; the veto applies even when the leader has strong administrative or technological achievements, as Sa...
**Result:** High probability of regime change, electoral defeat, or loss of power for the leader during Saturn's transit through 4th, 8th, or 12th from natal Moon. Case study: Chandra Babu Naidu's political downfall despite major IT and infrastructure achievements -- Saturn's transit through 4th/8th/12th overrod...

#### `mundane-mehta-ch6-eclipse-10th-overthrow`
**Title:** Mehta Ch 6 -- Eclipse / Malefic in 10th House: Government Overthrow Sign
**Source:** Mehta Ch 6 -- Houses and their Signification
**Severity:** critical | **Checkable:** False | **Weight:** 1.0
**Condition:** IF a solar or lunar eclipse falls on the 10th house of a national chart THEN direct sign of defeat or overthrow of the government; IF a malefic (Saturn, Rahu, Mars) is stationed or transiting the 10th house THEN disgrace, scandal, or illness/death among the head of state; IF a lunation (New Moon or ...
**Result:** Government Defeat / Overthrow / Disgrace of Head of State. Eclipse in 10th = highest-severity governance warning in the mundane chart. Nearest lunation in 10th marks the event timing window.

#### `mundane-raphael-ch3-angular-multiplier`
**Title:** Raphael Ch 3 -- Angular House Power Multiplier
**Source:** Raphael Ch 3 -- Twelve Mundane Houses
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** IF a diagnostic planet occupies an Angular house (1, 4, 7, 10) THEN apply FULL diagnostic weight (1.0×) to its effects; IF planet occupies a Succedent house (2, 5, 8, 11) THEN apply 0.7× weight; IF planet occupies a Cadent house (3, 6, 9, 12) THEN apply 0.4× weight; IF planet is within 5 degrees of ...
**Result:** All mundane diagnoses must weight planetary signals by house type before producing output. A critical malefic in the 4th house (Angular, 1.0×) carries far greater Calamity Warning weight than the same malefic in the 3rd house (Cadent, 0.4×). Accidentally Dignified planets override the base house wei...

## v20 -- Gopal Ch10 (sports predictions)

#### `mundane-gopal-ch10-sports-captain-lagna-boost`
**Title:** Gopal Ch10 -- Captain's Lagna Boost (+0.15 Victory Weight)
**Source:** Gopalakrishnan Ch 10 -- Predicting Sports Events (pp.743-745)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the captain's individual natal chart is strong during the match window -- specifically, the captain's Dasha and Antardasha planets are strong from both natal Lagna and natal Chandra Lagna during the match date -- THEN add +0.15 to that team's victory probability weight after the base 10th lord vs 4...
**Result:** Captain's natal strength confirmed during match window -- add +0.15 to the team's base victory probability. This modifier can tip close matches (equal-strength 10th/4th lords) toward the team with the stronger captain. Do not apply if captain's natal data is unavailable or unverified.

#### `mundane-gopal-ch10-sports-close-finish-trigger`
**Title:** Gopal Ch10 -- Close Finish Trigger (Equal Lords + 8th Lord in Dual Sign)
**Source:** Gopalakrishnan Ch 10 -- Predicting Sports Events (pp.744-745)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the 10th lord and the 4th lord are assessed as equal in strength (neither clearly dominant after full triage from Lagna, Chandra Lagna, and Karkamsha) AND the 8th lord of the match chart is placed in a Dual sign (Gemini, Virgo, Sagittarius, or Pisces) THEN the match will be extremely competitive ...
**Result:** Match Alert: Highly competitive finish -- result decided in final overs/last set/penalty shoot-out. No decisive winner predicted from chart alone. Monitor Reduced Vimshottari segments for the final phase to identify which team has planetary support in the closing stages.

#### `mundane-gopal-ch10-sports-rain-delay-monitor`
**Title:** Gopal Ch10 -- Rain Delay Monitor (Watery 4th House + 4th Lord in Watery Sign)
**Source:** Gopalakrishnan Ch 10 -- Predicting Sports Events (pp.744-745)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the 4th house of the match chart contains watery planets (Moon or Venus) AND the 4th lord is simultaneously placed in a watery sign (Cancer, Scorpio, or Pisces) THEN there is a high probability of match interruption or abandonment due to rain -- the 4th house governs atmospheric conditions; the du...
**Result:** Weather Warning: High probability of rain delay or match interruption. In limited-overs cricket, apply DLS method probability. In tennis, expect play suspension. In football, expect waterlogged pitch risk. The actual result remains pending until match is completed -- do not project a winner until int...

#### `mundane-gopal-ch10-sports-toss-winner-victory-gate`
**Title:** Gopal Ch10 -- Toss Winner Victory Gate (10th Lord vs 4th Lord)
**Source:** Gopalakrishnan Ch 10 -- Predicting Sports Events (pp.741-744)
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the 10th lord from the match Lagna is stronger than the 4th lord (assessed from Lagna, Chandra Lagna, and Karkamsha Lagna) -- where strength is ranked as: Exaltation > Own sign > Friendly sign > Neutral > Debilitation, and Retrograde reduces strength by one tier, Combust planet is treated as sever...
**Result:** Team A Victory (toss winner wins): 10th lord dominance confirmed -- the team assigned to Lagna/1st house will win the match. Team B Victory (toss loser wins): 4th lord dominance confirmed -- the team assigned to the 7th house will win the match. Validated: India vs West Indies 1st ODI (Jamaica, 18 May...

## v21 -- Gopal Ch11 (rainfall / monsoon forecast)

#### `mundane-gopal-ch11-rains-mars-4th-agri-stress`
**Title:** Mars in 4th of Ingress + 12th Lord in 1st -- Agricultural Stress & Famine Alert
**Source:** Gopal Ch 11 -- Tajika Ingress Chart Diagnostics (Agricultural Stress Trigger)
**Severity:** high | **Checkable:** True | **Weight:** 0.85
**Condition:** IF in the Sun ingress chart (SW or NE monsoon onset) Mars is placed in the 4th house AND the 12th lord is placed in the 1st house
**Result:** SOCIO-ECONOMIC ALERT: Mars in the 4th house burns agricultural land and groundwater reserves -- the 4th house signifies soil moisture and crop fields in mundane charts. The 12th lord in the 1st house brings 'loss to the nation's body' -- expenses and losses affect the national identity and visible pro...
**Notes:** Mars in 4th is a standalone malefic signal for the land. The additional condition (12th lord in 1st) confirms the loss manifests publicly. This trigger is most dangerous when Rahu is simultaneously in...

#### `mundane-gopal-ch11-rains-prasna-balance-negative`
**Title:** Prasna Marga Rainfall Balance -- Evaporation Exceeds Precipitation Gate
**Source:** Gopal Ch 11 -- Economic Analogy Technique (Technique 4, Prasna Marga)
**Severity:** medium | **Checkable:** True | **Weight:** 0.7
**Condition:** IF in the Sun ingress chart (SW or NE monsoon onset) the malefic strength in the 12th house (Evaporation/Loss/Expense) exceeds the benefic strength in the 2nd house (Rain Income/Cloud formation capacity)
**Result:** NEGATIVE RAINFALL BALANCE: Following Prasna Marga's income-vs-expense economic analogy, when the 'expense' of evaporation and moisture loss exceeds the 'income' of cloud formation, the seasonal rainfall budget is in deficit. Result: below-normal total precipitation even if rains arrive on schedule. ...
**Notes:** Strength comparison uses natural benefic/malefic classification: Benefics = Jupiter, Venus, unafflicted Mercury, waxing Moon. Malefics = Saturn, Mars, Rahu, Ketu, Sun, afflicted Mercury. A 12th house ...

#### `mundane-gopal-ch11-rains-rahu-leo-moderate`
**Title:** Rahu Transit Leo -- SW Monsoon Onset Delay Alert
**Source:** Gopal Ch 11 -- Rahu Transit Veto
**Severity:** medium | **Checkable:** True | **Weight:** 0.65
**Condition:** IF Rahu is transiting Leo (Simha)
**Result:** MODERATE RAINFALL ALERT: Leo is a fixed fire sign. Rahu's transit here generates excess heat in the planetary environment, reducing cloud formation capacity and potentially delaying the SW monsoon onset by 1-3 weeks. Overall seasonal total may be adequate but the delayed onset causes agricultural st...
**Notes:** Rank 3 of 4 in the Rahu Transit Veto. Leo is the natural 5th house (speculation, heat) -- Rahu amplifies the fire element. Monitor SW monsoon onset date vs. IMD climatological average (June 1 Kerala) d...

#### `mundane-gopal-ch11-rains-rahu-scorpio-severe`
**Title:** Rahu Transit Scorpio -- Severe NE Monsoon Disruption Alert
**Source:** Gopal Ch 11 -- Rahu Transit Veto
**Severity:** high | **Checkable:** True | **Weight:** 0.85
**Condition:** IF Rahu is transiting Scorpio (Vrichika)
**Result:** SEVERE RAINFALL ALERT: Scorpio is the mirror axis of Taurus in the Rahu Transit Veto system. High probability of NE monsoon disruption and drought risk in southern India (Tamil Nadu, coastal Andhra, Kerala). The SW monsoon may be adequate nationally while the NE monsoon fails. Run Tajika ingress aud...
**Notes:** Rank 2 of 4 in the Rahu Transit Veto. Scorpio is a fixed water sign -- Rahu's transit here disrupts the NE monsoon more than the SW. Rahu transits Taurus and Scorpio alternately every ~9 years.

#### `mundane-gopal-ch11-rains-rahu-taurus-critical`
**Title:** Rahu Transit Taurus -- Critical National Rainfall Alert (2002 Validated)
**Source:** Gopal Ch 11 -- Rahu Transit Veto & 2002 Drought Case Study
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Rahu is transiting Taurus (Rishabha)
**Result:** CRITICAL RAINFALL ALERT: High probability of hydrological drought. Taurus is the highest-priority disruptive sign for India's water cycle per Gopalakrishnan. Validated against the 2002 national drought: Rahu in Taurus + Saturn/Mercury in 10th of June 15 ingress chart → 29 of 35 meteorological subdiv...
**Notes:** Rank 1 of 4 in the Rahu Transit Veto. Rahu completes a nodal cycle every ~18 years; last Taurus transit was 2022-2023. Highest confidence drought signal in Gopal's modernized Vedic meteorology system....

## v22 -- Gopal Ch12 (India native profile)

#### `mundane-gopal-ch12-india-mars-7th-2nd-wealth-trade`
**Title:** India Mars (7th Lord) in 2nd -- Wealth Tied to Foreign Trade & Defense
**Source:** Gopal Ch 12 -- Wealth Architecture (Mars 7th Lord in 2nd House)
**Severity:** medium | **Checkable:** True | **Weight:** 0.75
**Condition:** IF the query context is India's national economic performance, trade balance, defense budget, or foreign investment climate
**Result:** STRUCTURAL WEALTH LOGIC -- EVERGREEN: Mars (7th lord = Foreign Relations, War, Partnerships) is placed in India's 2nd house (National Wealth, Revenue, Resources). This creates a permanent structural linkage: India's prosperity is tied to the health of its foreign relationships. When foreign relations...
**Notes:** Checkable: India's worst economic periods correlate with foreign relations crises. 1971 (Bangladesh war → economic strain), 1991 (Gulf War + BoP crisis → IMF bailout), 2016 (demonetization + US electi...

## v3  -- Gaur Ch2 (Celestial Council) + Mehta Ch13/20/26

#### `mundane-gaur-ch2-dhanesh-outcome-matrix`
**Title:** Dhanesh (Lord of Wealth and Treasure) Planet Outcome Matrix
**Source:** Gaur Ch 2 -- The Celestial Council
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** Identify the Dhanesh -- Lord of Wealth and Treasure planet as lord of weekday on Lord of the weekday on Virgo ingress (Kanya Sankranti) for the Wealth accumulation, trade profits, economic prosperity, treasury. Apply 7-planet outcome matrix: IF Sun → Businessmen earn good profits in trade. Traders of...
**Result:** Identify the lord of weekday on Virgo ingress. Mercury, Jupiter or Venus as Dhanesh → strong trade year. Mars or Saturn → trade disruption and economic stress. Cross-reference with King planet for overall economic picture.

#### `mundane-gaur-ch2-durgesh-outcome-matrix`
**Title:** Durgesh (Lord of Defence and Security) Planet Outcome Matrix
**Source:** Gaur Ch 2 -- The Celestial Council
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** Identify the Durgesh -- Lord of Security and Defence planet as lord of weekday on Lord of the weekday on Leo ingress (Simha Sankranti) for the Defence, military, law enforcement, national security. Apply 7-planet outcome matrix: IF Sun → Rulers improve legal system and general administration. Justice...
**Result:** Identify the lord of weekday on Leo ingress. Mars or Saturn as Durgesh → national security crises, oppressive administration. Jupiter or Mercury → strong defence with diplomacy. When both King and Durgesh are malefics -- war scenario heightened.

#### `mundane-gaur-ch2-king-outcome-matrix`
**Title:** King (Raja) Planet Outcome Matrix -- 7 Planets × Governance Domain
**Source:** Gaur Ch 2 -- The Celestial Council
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** Identify the King (Raja / Samvatsar King) planet as lord of weekday on Lord of the weekday on Chaitra Shukla Pratipada (first day of Vikram Samvat) for the Governance, war/peace, overall prosperity of the year. Apply 7-planet outcome matrix: IF Sun → Rains insufficient. Danger of diseases to people ...
**Result:** Identify the planetary lord (weekday ruler on Chaitra Shukla Pratipada). Look up that planet's outcome above. Cross-reference with Samvatsar lord for confirmation. Assess the planet's strength (exaltation/debilitation, combustion, retrograde, aspect) to calibrate outcome: strong planet → better vers...
**Notes:** The King role in Gaur Ch 2 and the Raja/Lord of Year in Mehta Ch 22 are the same concept -- cross-reference both books for synthesis.

#### `mundane-gaur-ch2-minister-outcome-matrix`
**Title:** Minister (Mantri) Planet Outcome Matrix -- 7 Planets × Administration Domain
**Source:** Gaur Ch 2 -- The Celestial Council
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** Identify the Minister (Mantri) planet as lord of weekday on Lord of the weekday on Aries ingress (Mesha Sankranti) for the Administration, law and order, ministerial conduct. Apply 7-planet outcome matrix: IF Sun → Bitterness amongst rulers increased. Fear due to disease and theft. Prosperity and fo...
**Result:** Identify the lord of the weekday on Aries ingress. Look up that planet's outcome above. Minister's affliction (combust, debilitated, with malefics) indicates administrative breakdown and cruelty.

#### `mundane-gaur-ch2-nava-megha-cloud-forecast`
**Title:** Nava Megha (Nine Clouds) -- Auxiliary Rainfall Forecast
**Source:** Gaur Ch 2 -- The Celestial Council
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** Apply formula: Multiply Shak Samvat by 8, divide by 9. Remainder = cloud type (1-9). Good-rain signal: Clouds 2, 4, 6, 7 → adequate to good rainfall. Poor-rain signal: Clouds 1, 3, 5, 8, 9 → below-average to poor rainfall.
**Result:** Use as auxiliary cross-check alongside Meghesh planet forecast. If both Meghesh and cloud type indicate poor rain -- drought signal confirmed. If both indicate good rain -- abundant monsoon signal.
**Notes:** Engine spec gaur-ch2-nine-clouds holds the full lookup table.

#### `mundane-gaur-ch2-neersesh-outcome-matrix`
**Title:** Neersesh (Lord of Metals and Trade) Planet Outcome Matrix
**Source:** Gaur Ch 2 -- The Celestial Council
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** Identify the Neersesh -- Lord of all trades such as metals planet as lord of weekday on Lord of the weekday on Capricorn ingress (Makara Sankranti) for the Metals, gemstones, trade, commerce, manufacturing. Apply 7-planet outcome matrix: IF Sun → Gold, copper, silver, ruby, pearl become expensive.; I...
**Result:** Use for commodity price forecasting. The Neersesh planet determines which category of metals/goods faces price pressure. Malefic aspects on the Neersesh planet intensify price rises.

#### `mundane-gaur-ch2-phalesh-outcome-matrix`
**Title:** Phalesh (Lord of Fruits and Flowers) Planet Outcome Matrix
**Source:** Gaur Ch 2 -- The Celestial Council
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** Identify the Phalesh -- Lord of Fruits and Flowers planet as lord of weekday on Lord of the weekday on Pisces ingress (Meena Sankranti) for the Horticulture: fruits, flowers, vegetables, ornamental plants. Apply 7-planet outcome matrix: IF Sun → Earth lush and decorated with fruits and flowers of all...
**Result:** Identify the lord of weekday on Pisces ingress. Mars or Saturn as Phalesh → horticultural loss. Jupiter or Venus as Phalesh → exceptional fruit and flower production.

#### `mundane-gaur-ch2-rasesh-outcome-matrix`
**Title:** Rasesh (Lord of Juicy Materials) Planet Outcome Matrix
**Source:** Gaur Ch 2 -- The Celestial Council
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** Identify the Rasesh -- Lord of Gur (Jaggery), Sugar and Juices planet as lord of weekday on Lord of the weekday on Libra ingress (Tula Sankranti) for the Sugar, jaggery, ghee, oils, dairy, juicy commodities. Apply 7-planet outcome matrix: IF Sun → Rains insufficient. Production of juicy materials lik...
**Result:** Identify the lord of weekday on Libra ingress. Look up planet outcome for sugar/jaggery/oil price and supply forecast. Combined with Neersesh (metals) for commodity market analysis.

#### `mundane-gaur-ch2-sasyesh-outcome-matrix`
**Title:** Sasyesh (Lord of 4-Month / Summer Crops) Planet Outcome Matrix
**Source:** Gaur Ch 2 -- The Celestial Council
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** Identify the Sasyesh -- Lord of Summer/4-Month Crops planet as lord of weekday on Lord of the weekday on Cancer ingress (Karka Sankranti) for the Summer crops: barley, wheat, rice, sugarcane (Kharif season). Apply 7-planet outcome matrix: IF Sun → Summer grains expensive. Increase in theft and robber...
**Result:** Identify the lord of the weekday on Cancer ingress. Look up that planet's outcome above. Combined with Meghesh (monsoon lord) -- if both are malefics the summer crop failure is severe.

#### `mundane-mehta-ch13-eclipse-airy-watery-signs`
**Title:** Eclipse in Airy and Watery Signs -- Social and Maritime Effects
**Source:** Mehta/Rao Ch 13 -- Eclipses
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Solar or lunar eclipse occurring in an airy or watery sign. Sign/context effects: gemini: High class women, kings and powerful ministers, persons proficient in arts, peop...; libra: People of Avanti and Apranta region (western borders near Sahya mountains), virt...; aquarius: Harm people living on mo...
**Result:** Airy sign eclipses → affect communication, trade routes, arts community, western borders. Watery sign eclipses → maritime disasters, fishing industry, coastal populations, epidemic risk. Eclipse in Satabhisha nakshatra (regardless of sign) → affects ministers, scientists, laboratories, stock exchang...

#### `mundane-mehta-ch13-eclipse-earthy-signs`
**Title:** Eclipse in Earthy Signs -- Agricultural and Economic Effects
**Source:** Mehta/Rao Ch 13 -- Eclipses
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Solar or lunar eclipse occurring in an earthy sign (Taurus, Virgo, Capricorn). Sign/context effects: taurus: Trouble to shepherds, cattle, owners of large herds; men who have risen to promi...; virgo: Afflict crops, poets, writers, musicians, people of Asmaka region as well as cou...; capricorn: Affe...
**Result:** Eclipse in Taurus → cattle/livestock crisis; India's lagna sign -- heightened national significance; established personalities lose prominence. Eclipse in Virgo → crop failure, public health crisis, labour unrest. Eclipse in Capricorn → drought, famine, earthquake, mining disaster; ministerial crisis...
**Notes:** Taurus eclipse has special significance for India as Taurus is India's traditional lagna.

#### `mundane-mehta-ch13-eclipse-fiery-signs`
**Title:** Eclipse in Fiery Signs -- Political and Military Effects
**Source:** Mehta/Rao Ch 13 -- Eclipses
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Solar or lunar eclipse occurring in a fiery sign (Aries, Leo, Sagittarius). Sign/context effects: aries: People of Panchala, Kalinga, Suraswna, Kambojas (modern Orissa), hunters, warrio...; leo: Destroys tribe of hunters, people inhabiting Mekala mountains, heroic persons, r...; sagittarius: Destroys...
**Result:** Eclipse in Aries → Orissa/North India military/civil conflict. Eclipse in Leo → rulers, forest regions, wildlife at risk; leadership crisis. Eclipse in Sagittarius → death or serious trouble to key leader/minister; fire disasters; food shortage.

## v4  -- Gaur Ch10 (price differentials) + Gaur Ch11 (eclipse)

#### `mundane-gaur-ch10-mars-motion-differentials`
**Title:** Mars Motion State Commodity Differentials
**Source:** Gaur Ch 10, pp.95-96
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** IF direct motion → Mars in direct motion causes fall in cotton prices after 3 days. Keeps oils and silver expensive. IF retrograde → Retrograde Mars keeps gold, silver, wheat, red things and goods influenced by own signs expensive. E... IF rising → When Mars rises: grains cheap, oils and oil materials...
**Result:** Use motion state to determine whether Mars's sign/nakshatra price signals are amplified (retrograde, combusted) or dampened (direct, benefic aspect).
**Notes:** Mars influence lasts 15 days to 1 month per sign. Retrograde Mars is more sinister for commodities.

#### `mundane-gaur-ch10-transit-synthesis-methodology`
**Title:** Transit Synthesis Methodology -- Multi-Planet Commodity Forecast
**Source:** Gaur Ch 10, pp.109-110
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** IF method: To forecast prices of grains, metals etc for a period: (1) Find the sign and nakshatra of each plane...; example: August 2002: Sun in Pushya/Ashlesha/Magha → grains expensive. Mars in Ashlesha/Magha → grains expens....
**Result:** Composite multi-planet transit signal: cross all 7-9 planet nakshatra/sign positions + motion states to derive net commodity price direction. Convergence of 5+ planets on expensive signal = strong bullish forecast for that commodity.
**Notes:** This is the core methodology of Gaur Ch 10. Not a single rule but the aggregation framework. Use lookup specs gaur-ch10-*-transit for individual planet signals.

#### `mundane-gaur-ch11-eclipse-aashadh-drought`
**Title:** Solar Eclipse in Aashadh -- Drought Signal
**Source:** Gaur Ch 11, p.111
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Solar eclipse occurs during Aashadh (Hindu month, ~June-July).
**Result:** Grains become expensive. Drought signal -- lack of sufficient rainfall in that agricultural season.
**Notes:** Scorpio sign eclipse also independently signals drought (see eclipse_by_sign table). Convergence of Aashadh solar eclipse + Scorpio placement = strong drought indicator.

#### `mundane-gaur-ch11-eclipse-severity-duration`
**Title:** Eclipse Coverage Percentage → Effect Duration
**Source:** Gaur Ch 11, p.113-114
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF 100 percent: Full eclipse (totality): commodity effects materialise within 20 days.; 75 percent: 75% coverage: effects felt within 1 month.; 50 percent: 50% coverage: effects felt within 2 months.; 33 percent: 33% coverage: effects felt within 3 months..
**Result:** Eclipse magnitude directly controls how quickly and strongly commodity price effects manifest. Full eclipse = immediate 20-day effect window. Partial eclipse = delayed effect by months.

#### `mundane-gaur-ch11-jupiter-aspect-eclipse-benefic`
**Title:** Jupiter Full Aspect on Eclipse -- Reduces Malefic Effects
**Source:** Gaur Ch 11, p.116
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Jupiter's full (7th house) aspect falls on the eclipse point (solar or lunar).
**Result:** Jupiter's full aspect on eclipse reduces the above undesired results; peace and prosperity prevail. This is the primary mitigating factor for eclipse maleficence.
**Notes:** Other planetary aspects on eclipse: Mars = red things expensive; Mercury = ghee/oils/maize/gold/brass expensive; Venus = silver/white clothes expensive; Saturn = black things/iron/urad/black grains ex...

#### `mundane-gaur-ch11-saturn-in-eclipse-sign`
**Title:** Saturn Residing in Eclipse Sign -- Metals Expensive
**Source:** Gaur Ch 11, p.113
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn is also transiting through the sign in which the solar or lunar eclipse occurs.
**Result:** When Saturn is in the eclipse sign: metals (gold, silver, iron) become expensive.
**Notes:** Compound signal: eclipse sign's commodity effects + Saturn's malefic amplification of metal prices.

## v5  -- Gopal Ch6 (mass death) + Gopal Ch7 (earthquakes)

#### `mundane-gopal-ch6-8th-house-death-zone`
**Title:** 8th House Death Zone -- Saturn+Rahu or Triple Malefic Confluence
**Source:** Gopalakrishnan Ch 6, pp.82-84
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF saturn rahu 8th: Saturn and Rahu (or Saturn and Ketu) both transiting the 8th house of the national chart simultaneou...; mars in 8th during eclipse: Mars transiting the 8th house during an eclipse period (within 30 days either side of eclipse date).; triple malefic 8th: Three or more malefic plane...
**Result:** Mass death signal of varying severity: Saturn+Rahu/Ketu = epidemic or slow-burning mass casualty event; Mars in 8th during eclipse = war-related mass death; Triple malefic 8th = severe multi-vector crisis (war + disease + disaster).
**Notes:** Cross-reference with Mehta Ch 19 triple-affliction rule (mundane-mehta-ch19-triple-affliction). The 8th lord's condition is equally important -- see mundane-gopal-ch6-8th-lord-affliction.

#### `mundane-gopal-ch6-8th-lord-affliction`
**Title:** 8th Lord Afflicted by Three Malefics -- Mass Casualty Risk
**Source:** Gopalakrishnan Ch 6, p.84
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** The lord of the 8th house of the national chart is afflicted by three or more malefic planets by conjunction, square (4th/8th/10th aspect), or opposition in the current transit chart.
**Result:** Mass casualty event. The nature of casualties is indicated by the sign/house placement of the 8th lord and the malefic planets afflicting it (Mars = war/fire/accidents; Saturn = disease/famine; Rahu = epidemic/poison/gas).
**Notes:** This rule operates independently of eclipse timing but is greatly amplified when an eclipse simultaneously activates the 8th house. The 8th lord in its own sign (debilitation) makes the affliction wor...

#### `mundane-gopal-ch6-eclipse-lagna-luminaries-leader`
**Title:** Eclipse Conjunct National Chart Ascendant or Luminaries -- Leader in Danger
**Source:** Gopalakrishnan Ch 6, p.80
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A solar or lunar eclipse falls within 5° of the national chart's Ascendant degree, natal Sun longitude, or natal Moon longitude. Also: on ascendant: Eclipse on Ascendant: national identity crisis; head of state in physical danger...; on natal sun: Eclipse conjunct natal Sun: extreme danger to the head...
**Result:** Serious threat to the incumbent national leader. May manifest as assassination attempt, death in office, or forced removal from power.
**Notes:** Cross-reference with Mehta Ch 18 lagna-lord-afflicted-death rule (mundane-mehta-ch18-lagna-lord-afflicted-death) and Mehta Ch 21 hazard rules. When eclipse hits both 8th house AND natal Sun/Moon simul...

#### `mundane-gopal-ch6-eclipse-trika-mass-death`
**Title:** Eclipse on Trika Houses of National Chart -- Mass Death
**Source:** Gopalakrishnan Ch 6, p.79
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A solar or lunar eclipse falls on the 4th, 8th, or 12th house of a country's national horoscope (or Aries Ingress chart for that year). Also: house 4: Eclipse on 4th house: mass suffering and death among the general population.; house 8: Eclipse on 8th house: mass death, war casualties, or epidemic....
**Result:** Mass death event in that country within the effect period of the eclipse (scale proportional to eclipse magnitude -- see Gaur Ch 11 severity-duration rule).
**Notes:** Cross-reference with Raphael Ch 25 eclipse-4th-8th rule (mundane-raphael-ch25-eclipse-4th-8th) for Western validation of the same principle. Severity escalates when Saturn or Mars also transits the ec...

#### `mundane-gopal-ch6-mars-gandanta-accidents`
**Title:** Mars in Gandanta Nakshatras -- Mass Accidents and Sudden Casualties
**Source:** Gopalakrishnan Ch 6, pp.86-87
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Mars transiting through any of the four gandanta (junction) nakshatras: Ardra (Gemini 6°40'-20°00'), Ashlesha (Cancer 16°40'-30°00'), Jyeshtha (Scorpio 16°40'-30°00'), or Mool (Sagittarius 0°00'-13°20'). Also: ardra: Mars in Ardra: mass accidents, sudden casualties from storms or transportation d...; ...
**Result:** Elevated risk of mass casualty events from sudden accidents, violence, or epidemics during Mars's transit through the specific gandanta nakshatra. Effect window: 7-14 days around Mars's stay in the nakshatra.
**Notes:** Gandanta nakshatras span the water-fire sign junctions: Pisces-Aries, Cancer-Leo, Scorpio-Sagittarius. All four are considered karmically unstable. Mars, as the natural significator of accidents and v...

#### `mundane-gopal-ch7-mars-eclipse-point-trigger`
**Title:** Mars Transiting Eclipse Point -- Seismic Trigger Within 3 Days
**Source:** Gopalakrishnan Ch 7, p.94
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Mars transiting over the exact longitude of a recent solar or lunar eclipse (within 1° orb) that occurred within the past 6 months. Also: trigger window: 3 days before to 3 days after Mars's exact conjunction with the eclipse longitud...; amplification: Effect is greatly amplified when Saturn's primar...
**Result:** Seismic event (earthquake) triggered in the geographic zone corresponding to the eclipse longitude. Mars acts as the igniter that activates the latent seismic energy stored at the eclipse point.
**Notes:** Cross-reference with Mehta Ch 11 forerunner-igniter rule (mundane-mehta-ch11-forerunner-igniter) which covers Mars/Sun/Venus triggering eclipse-point seismic events. Track the last 2-3 eclipse longitu...

#### `mundane-gopal-ch7-new-moon-fixed-sign-seismic`
**Title:** New Moon Conjunct Saturn or Mars in Fixed Sign -- Seismic Risk Window
**Source:** Gopalakrishnan Ch 7, p.97
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** A New Moon (Sun-Moon conjunction) occurs while Saturn or Mars is also in a fixed sign (Taurus, Leo, Scorpio, Aquarius), and the New Moon itself falls within 10° of Saturn or Mars. Also: new moon conjunct saturn fixed: New Moon conjunct Saturn in fixed sign: seismic risk window of 7-14 days.; new moo...
**Result:** Seismic risk window of 7-14 days centered on the New Moon date. Geographic zone indicated by the fixed sign involved.
**Notes:** New Moon amplifies the energy of any planet it conjoins. In fixed signs, this concentrates telluric (earth) energy. Strongest when Saturn's primary fixed-sign indicator is already active AND Mars is a...

#### `mundane-gopal-ch7-sandhi-clustering`
**Title:** Sandhi Degree Clustering -- Earthquake Signal from Sign-Boundary Planets
**Source:** Gopalakrishnan Ch 7, pp.97-98
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Two or more planets simultaneously within 2° of a sign boundary (sandhi degree: last 2° of any sign or first 2° of any sign = 0°-2° or 28°-30° in the sign). Also: gandanta boundaries: Most seismically sensitive sandhi points: Pisces-Aries (29°Pi - 2°Ar), Cancer-Le...; non gandanta: Other sign boundari...
**Result:** Earthquake signal. The sandhi zone represents instability -- planets at sign boundaries are between states, creating a 'fault line' in the cosmic structure that can manifest as geological fault lines activating. Effect window: 5-10 days.
**Notes:** Cross-reference with Mehta Ch 11 rasi-sandhi rule (mundane-mehta-ch11-rasi-sandhi). Both authors independently identify sign-boundary clustering as a seismic signal. When both are active simultaneousl...

#### `mundane-gopal-ch7-saturn-fixed-signs-primary`
**Title:** Saturn in Fixed Signs (Retrograde) -- Primary Earthquake Indicator
**Source:** Gopalakrishnan Ch 7, pp.91-93
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF saturn fixed direct: Saturn transiting a fixed sign (Taurus, Leo, Scorpio, Aquarius) in direct motion: elevated baseline ...; saturn fixed retrograde: Saturn retrograde in a fixed sign: strongest primary seismic indicator. Retrograde Saturn in fixed s...; most dangerous signs: Saturn in Scorpio or Aq...
**Result:** Primary seismic indicator active. Elevated earthquake probability globally in regions associated with the fixed sign Saturn occupies. Retrograde condition amplifies probability by ~2x.
**Notes:** Cross-reference with Mehta Ch 11 rules: mundane-mehta-ch11-scorpio-taurus-primary (Scorpio-Taurus axis), mundane-mehta-ch11-cardinal-clustering, mundane-gopal-ch8-seismic-triad. Saturn in fixed signs ...

## v6  -- Gopal Ch8 (war) + Gopal Ch9 (civil unrest)

#### `mundane-gopal-ch8-6th-lord-dasa-insurgency`
**Title:** 6th Lord Dasa -- Insurgency and Terrorist Conflict Activation
**Source:** Gopalakrishnan Ch 8, p.105
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A nation enters the Vimshottari dasa period of its 6th house lord (the planet that rules the 6th house from the national chart's Ascendant). Also: india application: India: 6th lord = Saturn (Libra Ascendant). When India runs Saturn dasa/bhukthi,...; sri lanka application: Sri Lanka ran Rahu Dasha fro...
**Result:** Insurgency, terrorism, border conflicts, war with enemy nations, and mass debt/disease conditions are activated during the 6th lord dasa period.
**Notes:** The 6th house in mundane astrology governs: sickness/epidemic, mass death, war with other countries, debt, medical industry, and enemy nations. The dasa of any planet placed in or ruling the 6th house...

#### `mundane-gopal-ch8-dasa-quality-war-duration`
**Title:** National Dasa Quality Determines War Duration and Outcome
**Source:** Gopalakrishnan Ch 8, pp.103-104
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF good dasa short war: Country running a benefic or raja yoga dasa/bhukthi at time of war: war will be short, country will ...; bad dasa prolonged war: Country running a malefic dasa (6th lord, 8th lord, Rahu dasa) at time of war: war will be prolonged...; war ends when: Wars end when a favorable raja ...
**Result:** Dasa quality is the primary determinant of war outcome and duration. Assess the dasa/bhukthi/antara of the national chart at time of conflict to determine probable war length and winner.
**Notes:** All India-Pakistan wars were short because India was running good overall dasa periods: 1947-48: Saturn/Saturn → Mercury bhukthi (favorable) ended it; 1965: Saturn/Jupiter/Rahu → Mercury dasa coming (...

#### `mundane-gopal-ch8-saturn-kataka-bloodshed`
**Title:** Saturn Entering Cancer (Kataka) -- Bloodshed Signal for Specific Nations
**Source:** Gopalakrishnan Ch 8, p.106
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn transits into Cancer (Kataka). For nations whose significant chart points (Ascendant, Moon sign, natal Saturn) are in or square to Cancer, Saturn's entry creates bloodshed conditions. Also: sri lanka specific: Saturn enters Kataka (Cancer): Sept 2004 to 2006. For Sri Lanka (Cancer rising o...; ...
**Result:** Bloodshed, civilian casualties, and leadership assassination risk for nations with Cancer prominent in the national chart during Saturn's transit through Cancer.
**Notes:** Saturn in Cancer = in its sign of debilitation (neecha). Debilitated Saturn in a nation's sensitive sign produces worst results. Cross-reference with Gopalakrishnan Ch 8 rule on Sri Lanka's LTTE confl...

#### `mundane-gopal-ch8-saturn-over-india-rahu-war`
**Title:** Saturn Transiting India's Natal Rahu -- War or Military Conflict Trigger
**Source:** Gopalakrishnan Ch 8, p.103
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn in transit conjuncts the natal Rahu longitude of India's independence chart (India Rahu = approx Taurus 3°-5°, chart-version dependent). Also: orb: Within 3° of exact conjunction.; source statement: 'Whenever Saturn has gone over India's Rahu there have been fights.' -- K. Gopala....
**Result:** Military conflict or war involving India. All confirmed India-Pakistan wars occurred during Saturn-Rahu transit activations.
**Notes:** This is an empirically validated rule across the 1947-48, 1965, 1971 and Kargil 1999 conflicts. Rahu's natal position in India's chart must be confirmed from a reliable India independence chart (Aug 1...

#### `mundane-gopal-ch9-abnormal-long-transit-amplification`
**Title:** Planet Staying Abnormally Long in a Sign -- Amplified Effects
**Source:** Gopalakrishnan Ch 9, p.147
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** A planet stays in a sign for significantly longer than its normal transit period, due to retrograde + direct motion cycles in the same sign. Also: examples: Mars in Aquarius (Kumbha) for more than 6 months (normal = ~....
**Result:** The themes governed by that sign (and the houses it rules in the national chart) are amplified and prolonged for the duration. Both positive and negative effects are extended.
**Notes:** This is Detail B in Gopalakrishnan's operational framework. Normal transit durations: Moon = 2.25 days per sign; Sun = 1 month; Mars = 6 weeks; Mercury = 3-4 weeks; Jupiter = 1 year; Saturn = 2.5 year...

#### `mundane-gopal-ch9-eclipse-trika-axis-negative`
**Title:** Eclipse in 6/8/12 Axis of National Chart -- Very Negative
**Source:** Gopalakrishnan Ch 9, p.148
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A solar or lunar eclipse falls within the 6th, 8th, or 12th house of the national chart, or aspects these houses by opposition (eclipse in 12th = also activates 6th by opposition, etc.).
**Result:** Very negative outcome for the nation. Eclipse in 6th: war, epidemic, debt crisis. Eclipse in 8th: leader death, mass casualties, government instability. Eclipse in 12th: financial ruin, foreign crisis, mass displacement.
**Notes:** This is Detail D in Gopalakrishnan's operational framework -- the final checkpoint in annual prediction analysis. Cross-reference with Gopalakrishnan Ch 6 eclipse-trika-mass-death rule (mundane-gopal-c...

#### `mundane-gopal-ch9-sandhi-malefics-confusion`
**Title:** Saturn/Rahu/Jupiter at Rasi Sandhi -- National Confusion and Instability
**Source:** Gopalakrishnan Ch 9, p.146
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn, Rahu, or Jupiter transiting at rasi sandhi -- the last 2° of any sign or the first 2° of any sign (the sign-change transition zone). Also: compounding: Two or more of these three planets simultaneously in rasi sandhi creates maximum....
**Result:** National confusion, policy paralysis, leadership indecision, and instability. Markets volatile. Events sudden and unexpected. Severity proportional to which planet is in sandhi and how long it remains there.
**Notes:** Cross-reference with Mehta Ch 11 rasi-sandhi rule (mundane-mehta-ch11-rasi-sandhi) which applies this to seismic events. Gopalakrishnan applies it more broadly to national governance and economic stab...

#### `mundane-gopal-ch9-saturn-10th-lord-leadership-change`
**Title:** Saturn Transiting Natal 10th Lord -- Leadership Change
**Source:** Gopalakrishnan Ch 9, p.147
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn in transit conjuncts the natal 10th lord's position in the national chart (i.e., transits over the natal degree of the planet that rules the 10th house). Orb: within 3°. Also: example: Saturn over India's natal Saturn (India's 10th lord from Ascendant perspective):....
**Result:** Changes in leadership at the national level. Prime minister may change, government may fall, or significant cabinet reshuffles occur.
**Notes:** Cross-reference with Mehta Ch 18 governance rules. Saturn transiting the 10th lord applies to any national chart. Identify the 10th lord from the national chart's Ascendant, find its natal position (d...

## v7  -- Gopal Ch10/13/15 (career/governance/economy)

#### `mundane-gopal-ch10-saturn-8th-dasa-lord-career-fall`
**Title:** Saturn Transiting 8th from Natal Dasa Lord -- Career Fall (Nadi Rule)
**Source:** Gopalakrishnan Ch 10, pp.163-170
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Transit Saturn occupies the 8th sign counted from the sign where the native's (or nation's) current Vimshottari Mahadasha planet is placed in the natal chart. Also: bhukthi amplification: If the Bhukthi lord is also unfavorably placed (12th house, 6/8 relationship), t....
**Result:** Fall in career, public standing, position, and performance for the duration of Saturn's transit through that sign (~2.5 years maximum). Applies to sportspersons, politicians, executives, actors -- any public figure.
**Notes:** This is a Nadi astrology rule validated on Sourav Ganguly and Sachin Tendulkar: Both running Jupiter Mahadasha. Saturn transiting 8th from Jupiter's natal sign = career fall for both simultaneously. F...

#### `mundane-gopal-ch13-saturn-trika-house-govt-change`
**Title:** Saturn Transiting Trika Houses of State Chart -- Government Power Change
**Source:** Gopalakrishnan Ch 13, pp.196-202
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Saturn in 4th house → Saturn transits 4th house of state/national chart: new party/challenger rises to power. IF Saturn in 6th house → Saturn transits 6th house: incumbent weakened; opposition wins. IF Saturn in 8th house → Saturn transits 8th house: major leadership transformation; sitting leade...
**Result:** Government change at the state or national level. The specific house determines the nature of change: 4th = new challenger; 6th = incumbent weakened; 8th = transformation + potential elimination; 12th = complete power change, new ruling party.
**Notes:** Validated empirically for Andhra Pradesh (Cancer lagna) over 4 election cycles: Saturn 4th → NTR first victory (1983); Saturn 6th → Congress returned (1989); Saturn 8th → NTR returned then eliminated ...

## v8  -- Eclipse severity/commodity rules

#### `mundane-raphael-ch11-lunation-4th-cusp-fixed-earthquake`
**Title:** Lunation in Fixed Sign on 4th House Cusp = Disastrous Earthquake
**Source:** Raphael Ch 11, Part 2 p.2
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A New Moon or Full Moon (Lunation) falls: (1) IN a fixed sign (Taurus, Leo, Scorpio, Aquarius), AND (2) EXACTLY ON the cusp of the fourth house of the mundane map.
**Result:** This is a sign of a DISASTROUS EARTHQUAKE in whatever part of the world this position may occur. The location is determined by which geographic area has this lunation falling exactly on their 4th house cusp.
**Notes:** Cross-validates with Gopalakrishnan's earthquake rules: both authors emphasize fixed signs as earthquake triggers (see gopal-ch7-saturn-fixed-signs-primary). Raphael's rule specifically combines fixed...

#### `mundane-raphael-ch11-saturn-4th-earthquakes-bad-weather`
**Title:** Saturn in 4th House = Earthquakes, Mining Disasters, Bad Weather, Crop Failure
**Source:** Raphael Ch 11, Part 2 p.2
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** At a Solar Ingress, Lunation, or in transit: Saturn is placed in the fourth house of the national mundane map.
**Result:** Obstacles and difficulties to the Government; national affairs will not proceed smoothly. Causes bad weather for crops; adversely affects agricultural matters. Denotes mining disasters, EARTHQUAKES, depreciates the value of land, disturbs property. If afflicted: evil very considerably increased. Gov...
**Notes:** Cross-validates Gopalakrishnan's earthquake rule: gopal-ch7-saturn-fixed-signs-primary specifies Saturn in FIXED signs as primary earthquake signal; Raphael's rule adds the 4th house placement as a ke...

#### `mundane-raphael-ch13-mars-6th-feverish-disease-warships`
**Title:** Mars in 6th House = Feverish Inflammatory Disease + Naval Fires and Accidents
**Source:** Raphael Ch 13, Part 2 p.5
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** At a Solar Ingress, Lunation, or in transit: Mars is placed in the sixth house of the national mundane map.
**Result:** Very evil position: feverish and inflammatory disease among the people, according to the nature of the sign in which Mars is placed. Also denotes fires and accidents on warships, and insubordination among sailors. If well aspected: effects are mitigated; may denote some naval demonstration or naval ...
**Notes:** Mars in 6th indicates inflammatory/fever-type disease (vs Saturn in 6th = chronic wasting). The dual effect (disease + naval accidents) follows from Mars's significations (soldiers, naval men, fire, i...

#### `mundane-raphael-ch13-saturn-6th-public-illness`
**Title:** Saturn in 6th House = Widespread Public Ill-Health of Nature Shown by Sign
**Source:** Raphael Ch 13, Part 2 pp.4-5
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** At a Solar Ingress, Lunation, or in transit: Saturn is placed in the sixth house of the national mundane map.
**Result:** Very evil position: much ill-health among the populace. The NATURE of the sickness is shown by the SIGN Saturn occupies -- e.g., Saturn in a water sign: lung/fluid conditions; Saturn in an earth sign: chronic/wasting diseases; Saturn in a fire sign: fevers with exhaustion. Also: discontent and dissat...
**Notes:** Cross-validates Gopalakrishnan's epidemic triad (see gopal-ch6-epidemic-triad): both sources emphasize Saturn in 6th-related positions as epidemic indicators. Raphael adds the refinement that the SIGN...

#### `mundane-raphael-ch6-ingress-rising-sign-duration`
**Title:** Ingress Rising Sign Determines Duration -- Cardinal 3mo / Fixed 12mo / Mutable 6mo
**Source:** Raphael Ch 6, p.7
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A Solar Ingress chart is cast for the moment the Sun enters Aries, Cancer, Libra, or Capricorn. Note the rising sign (Ascendant sign) of the ingress chart for the location in question.
**Result:** CARDINAL sign rising (Aries, Cancer, Libra, Capricorn): ingress figure has rule for THREE MONTHS only -- cast the next ingress immediately. FIXED sign rising (Taurus, Leo, Scorpio, Aquarius): ingress figure influences the WHOLE of the twelve months following. MUTABLE/COMMON sign rising (Gemini, Virgo...
**Notes:** This rule determines how many ingress charts need to be cast and consulted for a given year and location. A fixed sign rising at the Aries ingress means only ONE chart rules the entire year. A cardina...

#### `mundane-raphael-ch6-lunar-eclipse-duration-hours-months`
**Title:** Lunar Eclipse Duration Rule -- Hours of Eclipse = Months of Influence
**Source:** Raphael Ch 6, p.8
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** A Lunar eclipse (figure cast for the exact moment of Full Moon) occurs. Measure the duration of the eclipse in hours.
**Result:** The Lunar eclipse has a period of action extending over AS MANY MONTHS as the eclipse is HOURS IN DURATION. Example: a 2-hour lunar eclipse → 2 months of influence. Lunar eclipses are important but less powerful than Solar eclipses (years vs months). Effects chiefly where visible and in countries ru...
**Notes:** Pair with solar eclipse rule (AC-01). A total lunar eclipse can last ~1.5-3 hours in totality but partial phases can extend the duration to 3-4 hours. The figure is cast for the exact Full Moon moment...

#### `mundane-raphael-ch6-solar-eclipse-duration-hours-years`
**Title:** Solar Eclipse Duration Rule -- Hours of Eclipse = Years of Influence
**Source:** Raphael Ch 6, p.8
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A Solar eclipse (figure cast for the exact moment of New Moon) occurs. Measure the duration of the eclipse in hours.
**Result:** The Solar eclipse has a specific influence of its own lasting for AS MANY YEARS as the eclipse is HOURS IN LENGTH. Example: a 3-hour solar eclipse → 3 years of influence in affected countries. Effects are strongest: (1) where the eclipse is visible, (2) in countries and cities ruled by the zodiac si...
**Notes:** This is Raphael's unique duration formula for solar eclipses. A total solar eclipse can last up to ~7.5 minutes of totality but the entire umbral/partial event can last 2-4 hours. Partial solar eclips...

#### `mundane-raphael-ch9-mars-2nd-stock-panic`
**Title:** Mars in 2nd House = Stock Exchange Panic, Bank Failures, Military Expenditure
**Source:** Raphael Ch 9, p.13
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** At a Solar Ingress, Lunation, or in transit: Mars is placed in the second house of the national mundane map.
**Result:** Losses on the Stock Exchange, panics, bank failures. Enormous expenditure and waste of public money. Military affairs will require large amounts of money -- the revenue will be seriously affected by military/defence spending. Note: does not necessarily denote a diminution of national revenue per se, ...
**Notes:** Mars in 2nd is particularly negative for stock markets and banking. Different from Saturn in 2nd (stagnation/depression) -- Mars in 2nd indicates sudden violent financial events: panics, crashes, failu...

#### `mundane-raphael-ch9-saturn-2nd-financial-stagnation`
**Title:** Saturn in 2nd House = Financial Stagnation, Securities Depression, Revenue Decrease
**Source:** Raphael Ch 9, p.13
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** At a Solar Ingress, Lunation, or in transit: Saturn is placed in the second house of the national mundane map.
**Result:** Very evil for national finances: poor revenue, decrease of receipts, financial stagnation, depression in securities and financial circles, general want of activity in all money matters. If Saturn is afflicted: heavy depreciation of securities (market crash). If Saturn is well aspected: gives a stead...
**Notes:** Saturn in 2nd is the most consistently negative planetary position for national finance. Compare: Mars in 2nd = sudden panics/crashes; Saturn in 2nd = prolonged stagnation. Jupiter in 2nd well aspecte...

## v9  -- Sun/Moon transit + Solar ingress rules

#### `mundane-raphael-ch22-eclipse-airy-signs-famine-storm`
**Title:** Eclipse in Airy Signs = Famine, Sickness, Pestilence, Stormy Winds
**Source:** Raphael Ch 22, p.15 (Part 2)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** A Solar or Lunar eclipse falls in an Airy sign: Gemini, Libra, or Aquarius.
**Result:** Famine, sickness, pestilence, and tempests and stormy winds hurtful to mankind.
**Notes:** Aquarius eclipse may also correlate with public grief and sorrow (per decanate effects). Airy signs connect to intellectual unrest, media/communications disruption (3rd house link). Libra eclipse: pes...

#### `mundane-raphael-ch22-eclipse-earthy-signs-earthquakes-drought`
**Title:** Eclipse in Earthy Signs = Earthquakes, Mining Disasters, Drought, Agricultural Failure
**Source:** Raphael Ch 22, p.15 (Part 2)
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A Solar or Lunar eclipse falls in an Earthy sign: Taurus, Virgo, or Capricorn.
**Result:** Foreshadow a scarcity of corn and products of the earth by drought; cause earthquakes, mining disasters, and great agricultural depression.
**Notes:** Taurus and Capricorn are particularly earthquake-prone eclipse signs (Taurus-Scorpio axis = most seismically active per Raphael Ch 26 Rule 3). Cross-validates Gopalakrishnan's Ch7 earthquake rules. So...

#### `mundane-raphael-ch22-eclipse-fiery-signs-war-pestilence`
**Title:** Eclipse in Fiery Signs = War, Fires, Pestilence, Royal Exile or Murder
**Source:** Raphael Ch 22, p.15 (Part 2)
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A Solar or Lunar eclipse falls in a Fiery sign: Aries, Leo, or Sagittarius.
**Result:** Threaten the destruction of cattle and sheep; exile, imprisonment, or murder of some king, notable person, or great ruler; much discontent and dissension among the people; movements of armies, fighting, fires, fevers, pestilence, and scarcity of the fruits of the earth, especially in those regions a...
**Notes:** Effects most powerful in countries where eclipse is visible and in those ruled by the sign (see raphael-ch28-countries-ruled-by-signs). Solar eclipse in fiery sign = effects last years (per AC-01). Lu...

#### `mundane-raphael-ch22-eclipse-watery-signs-mortality`
**Title:** Eclipse in Watery Signs = Mass Mortality Among Common People, Maritime Destruction
**Source:** Raphael Ch 22, p.15 (Part 2)
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A Solar or Lunar eclipse falls in a Watery sign: Cancer, Scorpio, or Pisces.
**Result:** Much mortality among the common people; great destruction of fowls and fishes, and such things as live in or near the sea. Also: tidal waves, inundations (especially Pisces 2nd decanate = tidal waves).
**Notes:** Cancer eclipse: excites wars (Cancer 1st decanate lunar), weather changes, dries up rivers (Cancer 2nd solar). Scorpio eclipse: earthquakes and thunders (Scorpio 1st decanate lunar), fevers and pestil...

#### `mundane-raphael-ch22-ptolemy-eclipse-timing-horizon`
**Title:** Ptolemy Eclipse Timing -- Eastern Horizon = First 4 Months; Midheaven = 4-8 Months; Western = 8-12 Months
**Source:** Raphael Ch 22, p.16 (Part 2)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** An eclipse occurs. Note where in the mundane map the eclipse falls: near the Ascendant/eastern horizon (1st house), near the Midheaven (10th house), or near the Descendant/western horizon (7th house).
**Result:** EASTERN HORIZON (near 1st house): effects manifest in the NEXT FOUR MONTHS; most strongly in the FIRST THIRD of that period (months 1-2). MIDHEAVEN (near 10th house): events begin from FOURTH TO EIGHTH MONTH; chief effects in the SECOND OR MIDDLE PART (months 5-6). WESTERN HORIZON (near 7th house): ...
**Notes:** This rule determines WHEN eclipse effects will manifest, not WHAT the effects will be. Combine with sign element rule for 'what' and this rule for 'when'. The most reliable timing per Raphael: calcula...

#### `mundane-raphael-ch26-cardinal-points-stellium-earthquake`
**Title:** Many Planets at Cardinal Point Degrees (0° Aries/Cancer/Libra/Capricorn) = Earthquake
**Source:** Raphael Ch 26, Part 3 p.5
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Many planets are clustered on or near the FOUR CARDINAL POINTS -- the first degrees of Aries, Cancer, Libra, and Capricorn -- at an ingress, lunation, or eclipse.
**Result:** Earthquakes generally happen during this configuration. The cardinal points (0° of each cardinal sign) represent the four directional angles of the ecliptic and have particular seismic sensitivity.
**Notes:** Cross-validates Gopalakrishnan's cardinal stellium rule (gopal-ch7-cardinal-stellium-upheaval). Both Western (Raphael) and Indian (Gopalakrishnan) traditions independently identify cardinal point clus...

#### `mundane-raphael-ch26-malefics-taurus-scorpio-earthquakes`
**Title:** Uranus/Saturn/Jupiter/Mars in Taurus or Scorpio = Increased Earthquake Frequency
**Source:** Raphael Ch 26, Part 3 p.5
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Any combination of the planets Uranus, Saturn, Jupiter, or Mars are transiting through the signs TAURUS or SCORPIO.
**Result:** Earthquakes happen MORE FREQUENTLY during this period. Taurus-Scorpio is the most earthquake-prone axis in the zodiac. The more malefic planets clustered in these signs, the greater the seismic risk globally.
**Notes:** Cross-validates Gopalakrishnan's earthquake rule about Saturn in fixed signs. Raphael specifically names TAURUS and SCORPIO as most earthquake-prone. Aquarius and Leo (the other two fixed signs) are a...

---

# PART B -- Pending Human Review
*186 rules escalated for co-founder decision.*
*Each rule shows the PHR reason -- the specific concern that needs resolution.*

**Decision options per rule:**
- ✅ Approve as-is → `approved`
- ✏️  Rewrite condition/result → resubmit for validation
- ❌ Discard → `rejected`

## v10 -- Raphael western eclipse decanate

#### `mundane-raphael-ch28-mars-exact-city-degree-fire-accident`
**Title:** Mars Transiting Exact Meridian Degree of a City = Serious Fire or Accident in That City
**Source:** Raphael Ch 28, Part 3 p.10
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Transit Mars passes over the exact zodiacal degree that corresponds to the meridian (MC) of a specific city. The meridian degree for known cities: London = Aquarius 12°; Gemini 17°54' (alternative); Johannesburg = Libra 27°; Messina = Scorpio 18°; Copenhagen = Libra 1°; Milwaukee = Scorpio 7°.
**Result:** This transit has been frequently observed to coincide with a serious FIRE or ACCIDENT in that city. The effect is highly specific to the city and highly time-precise -- manifests on or very close to the day Mars exactly crosses that degree.
**Notes:** VALIDATED CASE: London Aquarius 12° meridian -- transits of Mars over this degree have been marked with serious fire or accident in the City. This rule enables precise day-level predictions for specifi...
**PHR Reason:** Specific city-degree mappings (London = Aquarius 12° vs Gemini 17°54') show conflicting data; requires verification against primary Raphael source to confirm which is authoritative.

#### `mundane-raphael-ch28-mars-transit-country-sign-fires`
**Title:** Mars Transiting a Country's Ruling Sign = Fires, Incendiarism, Insurrections in That Country
**Source:** Raphael Ch 28, Part 3 p.9
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Transit Mars passes through a zodiac sign. Identify the countries and cities ruled by that sign (see raphael-ch28-countries-ruled-by-signs).
**Result:** Serious troubles are shown in those countries ruled by whatever sign Mars is passing through. Mars specifically causes FIRES, INCENDIARISM, and INSURRECTIONS in those countries. Cities governed by the sign Mars is passing through are likely to be much disturbed. The effect is most precise when Mars ...
**Notes:** This is Raphael's primary transit rule for Mars. Combines with sign rulerships to pinpoint WHICH country. Example application: Mars entering Aries → troubles in England, Germany, Japan, Syria. Mars en...
**PHR Reason:** Result text is incomplete/truncated ('Johannesburg = L'); cannot assess full coherence without complete statement.

## v11 -- Historical validation / benchmark cases

#### `gaur-ch1-samvatsar-group-quality-modifier`
**Title:** Samvatsar Group (Brahma/Vishnu/Shiv) as Secondary Quality Modifier
**Source:** Gaur Ch 1, p. 4
**Severity:** low | **Checkable:** False | **Weight:** 1.0
**Condition:** Any Samvatsar is active. Identify its group: Brahma-group: #1-20 (Prabhav to Vyaya); Vishnu-group: #21-40 (Sarvjat to Parabhav); Shiv-group: #41-60 (Plavang to Kshaya).
**Result:** The group ownership provides a background quality modifying the lord's results: BRAHMA GROUP (1-20): Generally auspicious undertone -- creation and abundance energy. VISHNU GROUP (21-40): Preservation and order undertone -- maintenance of status quo. SHIV GROUP (41-60): Dissolution and transformation ...
**Notes:** This tripartite division mirrors the Hindu cosmic trinity (Brahma/Vishnu/Shiva) mapping onto the 60-year Jupiter cycle. In practice: a Shiv-group year with a benefic lord (e.g., Mercury) will still sh...
**PHR Reason:** Result text is truncated mid-sentence ('secondary b'); cannot verify completeness or coherence of the full rule.

#### `gaur-ch1-samvatsar-jupiter-lord-excessive-rains-disease`
**Title:** Jupiter as Samvatsar Lord = Excessive Rains, High Prices, Excessive Disease but People Feel Secure
**Source:** Gaur Ch 1, p. 6-7
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** The current Samvatsar has Jupiter as its lord. Jupiter-lord Samvatsars: #8 Bhav, #28 Jai, #48 Anand, #17 Subhanu, #57 Rudhirodgari.
**Result:** Diseases are excessive. Grain production is medium. Though rulers engage in wars, people have a feeling of security. Rains are excessive; cattle give more milk. All things are dear (high prices). MONTHLY PATTERN: Chaitra -- medium. Baisakh -- food materials costly. Aashadh/Shravan -- rains normal. Bhad...
**Notes:** Jupiter years show high prices and disease despite political security. The excessive rain pattern leads to flooding and crop damage despite high yield cattle. Year-end (Kartik onwards) corrects grain ...
**PHR Reason:** Monthly pattern is truncated ('Kartik -- beneficial. Margsheersh/Paush/Magh/Pha'); cannot verify full monthly cycle or internal consistency.

#### `gaur-ch1-samvatsar-ketu-lord-plentiful-rains-loose-morals`
**Title:** Ketu as Samvatsar Lord = Plentiful Rains, Abundant Grains, Loose Social Conduct
**Source:** Gaur Ch 1, p. 7
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** The current Samvatsar has Ketu as its lord. Ketu-lord Samvatsars: #12 Bahudhanya, #32 Vilambi, #52 Kaal Yukta, #40 Parabhav.
**Result:** Plentiful rains. Grains available abundantly. People have increased tendency of loose character and conduct. MONTHLY PATTERN: Chaitra/Baisakh/Jyeshtha -- grains expensive (pre-monsoon scarcity). Aashadh/Shravan/Bhadrapad -- sufficient rains, grains become cheap.
**Notes:** Ketu years combine agricultural abundance with social/moral deterioration. The pre-monsoon period sees high prices that sharply reverse once rains arrive. Ketu as a moksha karaka produces both spiritu...
**PHR Reason:** Ketu-lord Samvatsars list includes #40 Parabhav, but Parabhav is traditionally the 40th Samvatsar (Vishnu-group), not Ketu-group; this is a factual error in planetary lord assignment.

#### `gaur-ch1-samvatsar-moon-lord-all-months-excellent`
**Title:** Moon as Samvatsar Lord = All 12 Months Excellent, Plentiful Rains, Cheap Grains
**Source:** Gaur Ch 1, p. 6
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** The current Samvatsar has Moon as its lord. Moon-lord Samvatsars: #5 Prajapati, #25 Khar, #45 Virodhkrit, #14 Vikram, #54 Raudra.
**Result:** All people leave their rivalries. Rains are plentiful. Grains are cheap. All 12 months are excellent. Rains could be deficient at few places. MONTHLY PATTERN: Chaitra through Bhadrapad -- excellent. Ashwin -- diseases more prevalent, grains costlier. Kartik/Margsheersh -- things cheap. Paush/Magh/Phalg...
**Notes:** Moon years are the most broadly auspicious -- 'all 12 months excellent' is unique to Moon. The year-end (Paush-Phalgun) carries natural calamity risk despite overall prosperity.
**PHR Reason:** Result claims 'all 12 months are excellent' but then lists Ashwin with disease prevalence and Paush/Magh/Phalgun with natural calamities; this internal contradiction weakens coherence.

#### `gaur-ch1-samvatsar-rahu-lord-drought-north-floods-east`
**Title:** Rahu as Samvatsar Lord = Drought in North, Floods in East, War in West, Riots Year-End
**Source:** Gaur Ch 1, p. 7
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** The current Samvatsar has Rahu as its lord. Rahu-lord Samvatsars: #11 Eashwar, #31 Hamelambi, #51 Pingal, #20 Vyaya, #60 Kshaya.
**Result:** Superficially: all people live happily and fruits and grains are good. But GEOGRAPHIC EFFECTS are severe and directional: DROUGHT in the North; FLOODS in the East; WAR in the West. MONTHLY PATTERN: Chaitra/Baisakh -- things costly. Jyeshtha/Aashadh -- rains less. Shravan/Bhadrapad -- rains more. Kartik...
**Notes:** Rahu years show a deceptive surface calm ('all people live happily') masking severe regional imbalances. The directional specification (North/East/West) is a unique Jyotish mapping tool linking Rahu's...
**PHR Reason:** Monthly pattern is truncated ('lives lost to rio'); cannot verify full cycle. Rahu-lord Samvatsars list includes #60 Kshaya, but Kshaya is traditionally the 60th (Shiv-group); factual accuracy unclear.

#### `gaur-ch1-samvatsar-shiv-lord-rulers-overthrown`
**Title:** Shiv as Samvatsar Lord = Rulers Overthrown, President's Rule, Heavy Rains Mid-Year
**Source:** Gaur Ch 1, p. 5
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** The current Samvatsar has Shiv as its lord. Shiv-lord Samvatsars: #3 Shukla, #23 Virodhi, #43 Saumya.
**Result:** People live with relatives happily but there is friction between rulers and opposition parties. Rulers of many places lose their throne; president's or emergency rule may be imposed. MONTHLY PATTERN: Chaitra/Baisakh/Jyeshtha -- normal. Aashadh/Shravan/Bhadrapad -- heavy rains. Ashwin -- spread of disea...
**Notes:** Shiv years are politically turbulent. The year-end (Phalgun) is particularly difficult. Validates political instability indicators in national charts.
**PHR Reason:** Monthly pattern is truncated ('Phalgu'); cannot verify full 12-month cycle or internal consistency.

#### `gaur-ch1-samvatsar-sun-lord-less-rain-insurgency`
**Title:** Sun as Samvatsar Lord = Less Rain, Insurgencies, Violence, Throne Changes
**Source:** Gaur Ch 1, p. 5
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** The current Samvatsar has Sun as its lord. Sun-lord Samvatsars: #4 Pramod, #24 Vikriti, #44 Sadharan, #13 Pramathi, #53 Siddharthi.
**Result:** Rains are less. Insurgencies in the country encourage violence. Persons of lower class remain in anxiety. The throne is changed at few places. Conflict between rulers and businessmen. MONTHLY PATTERN: Chaitra/Baisakh -- goods become costlier. Jyeshtha -- diseases cause agony. Aashadh/Shravan/Bhadrapad...
**Notes:** Sun years are dry and politically unstable. Agriculture suffers due to scanty monsoon. Cross-reference: Raphael Mars transit rules for insurgency timing within the year.
**PHR Reason:** Monthly pattern is truncated ('Magh -- juicy materials dearer. '); cannot verify complete monthly cycle.

#### `gaur-ch1-samvatsar-venus-lord-natural-calamities`
**Title:** Venus as Samvatsar Lord = Earthquakes and Natural Calamities, Female Supremacy, Excessive Rains
**Source:** Gaur Ch 1, p. 7
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** The current Samvatsar has Venus as its lord. Venus-lord Samvatsars: #9 Yuva, #29 Manmath, #49 Rakshas, #18 Taran, #58 Raktaksha.
**Result:** Milk production is good. Rains are excessive. Ladies remain engaged in activities of all types. Young people want luxuries. All people live comfortably. Supremacy of females is established. EARTHQUAKE AND CALAMITY RISK throughout the year. MONTHLY PATTERN: Chaitra/Baisakh -- natural calamities. Jyesh...
**Notes:** Venus years have a dual character: social prosperity and luxury on one side, earthquake/calamity risk on the other. Cross-validate with Raphael Ch 26 earthquake rules (malefics in Taurus/Scorpio) to a...
**PHR Reason:** Monthly pattern is truncated ('Bhadrapad -- floods cause loss'); cannot verify full cycle. Also, Samvatsars list includes #37 Shobhan, which is not in the standard 60-year cycle.

#### `gaur-ch1-samvatsar-venus-year-earthquake-calamity-specific`
**Title:** Venus Samvatsar Year = Earthquakes and Natural Calamities Are Specifically Indicated
**Source:** Gaur Ch 1, p. 7
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** The current Samvatsar has Venus as its lord (Samvatsars: #9 Yuva, #18 Taran, #29 Manmath, #37 Shobhan, #49 Rakshas, #58 Raktaksha). This rule activates the FULL year, not just specific months.
**Result:** During a Venus Samvatsar, earthquakes and other natural calamities cause agony. This is a year-level risk -- not restricted to Chaitra/Baisakh alone. The Chaitra and Baisakh months specifically show natural calamity manifestation. Floods in Bhadrapad are also part of this pattern.
**Notes:** This rule provides the ANNUAL-LEVEL earthquake signal from the Samvatsar cycle. It should be combined with Raphael Ch 26 earthquake rules (eclipse on meridian/nadir, malefics in Taurus/Scorpio, great ...
**PHR Reason:** Samvatsars list includes #37 Shobhan, which does not exist in the standard 60-year Samvatsar cycle; this is a factual error.

#### `gaur-ch1-samvatsar-vishnu-lord-law-order-diseases`
**Title:** Vishnu as Samvatsar Lord = Law and Order Enforced, Many Diseases, Plentiful Rains
**Source:** Gaur Ch 1, p. 5
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** The current Samvatsar has Vishnu as its lord. Vishnu-lord Samvatsars: #2 Vibhav, #22 Sarvdhari, #42 Keelak.
**Result:** Rulers and senior officers take stern measures to maintain law and order. Common people forget differences and live with peace and happiness. Rains and crops are good. Many diseases are prevalent throughout the year. Hilly areas experience more difficulties and agonies. MONTHLY PATTERN: Chaitra/Bais...
**Notes:** Vishnu years balance political order with widespread disease. The second half of the year (Kartik onwards) is economically favourable.
**PHR Reason:** Monthly pattern is truncated ('Ashwin -- juices '); cannot verify full 12-month cycle.

## v12 -- Saturn transit price matrix

#### `gaur-ch3-universal-horoscope-malefics-7th-crop-damage`
**Title:** Malefics in 7th House of Aries Ingress Chart = Damage to Ripe Crops in Ashwin (Sep-Oct)
**Source:** Gaur Ch 3
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** In the Aries Ingress (Universal Horoscope) chart: Sun, Mars, Saturn, or Rahu occupies or strongly aspects the 7th house.
**Result:** Damage to ripe crops during Ashwin month (September-October). The 7th house of the Universal Horoscope maps to Ashwin -- malefic presence there destroys the harvest period specifically.
**Notes:** In the Universal Horoscope framework, each house = one Hindu month. 7th house = Ashwin (Sep-Oct) = peak harvest season for most of India. This is why malefics in the 7th of the Universal Chart are par...
**PHR Reason:** The mapping of 7th house to Ashwin month is specific but requires verification against Gaur's actual month-house correspondence table; the rule assumes a fixed Aries Ingress baseline.

#### `mehta-ch2-double-eclipse-14-days-destruction`
**Title:** Solar + Lunar Eclipse Within 14 Days = Terrible Destruction
**Source:** Mehta/Rao Ch 2
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A solar eclipse AND a lunar eclipse occur within 14 days of each other.
**Result:** TERRIBLE DESTRUCTION = TRUE. Highest alert in the eclipse module. Expect a major catastrophic national or global event within the period mapped by those two eclipses.
**Notes:** In the Universal Horoscope, identify which houses the two eclipses fall in to determine WHICH months carry the destruction energy. Cross-reference with Raphael's eclipse element rules (raphael-ch22-ec...
**PHR Reason:** Contradicts: gaur-ch11-eclipse-lunar-solar-sequence-religious-happiness

#### `mehta-ch2-king-of-year-sun-moon-governance`
**Title:** If King of Year Is Not Sun or Moon, Governance Instability = TRUE
**Source:** Mehta/Rao Ch 2
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** In the Hindu New Year horoscope (Chaitra Shukla Pratipada chart), identify the Lord of the Year (Varsha Lord). Condition: Varsha Lord is NOT Sun AND NOT Moon.
**Result:** Governance instability is predicted for the year. Royal authority is weakened -- expect challenges to central leadership, coalition friction, or executive paralysis.
**Notes:** Cross-reference with Gaur Ch 2 Celestial Council spec (gaur-ch2-celestial-council-outcomes) for the full cabinet analysis. Sun as King = strong decisive governance. Moon as King = popular leadership, ...
**PHR Reason:** Classical sources emphasize Sun/Moon as Varsha Lords, but the negation logic (NOT Sun AND NOT Moon → instability) requires verification against Mehta's exact phrasing; may conflate weak Varsha Lord with non-solar/lunar rulership.

#### `mehta-ch2-mars-retrograde-jyeshtha-anuradha-fall-of-kings`
**Title:** Mars Retrograde in Jyeshtha Nakshatra Then Enters Anuradha = Fall of Kings
**Source:** Mehta/Rao Ch 2
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Mars is retrograde while in Jyeshtha Nakshatra (Scorpio 16°40' to 30°00') and subsequently (after turning direct) enters Anuradha Nakshatra (Scorpio 3°20' to 16°40').
**Result:** Fall of Kings = TRUE. Rulers or heads of state lose power during this transit. This can manifest as electoral defeat, forced resignation, or regime change.
**PHR Reason:** The retrograde-to-direct transition across two nakshatras in reverse order (Jyeshtha → Anuradha backward) is geometrically incoherent; Jyeshtha is 16°40'-30°00' Scorpio, Anuradha is 3°20'-16°40' Scorpio, so retrograde Mars would exit Jyeshtha into Anuradha, not the reverse. Condition is internally contradictory.

#### `mehta-ch2-sat-jup-conjunction-us-president-mortality`
**Title:** Saturn-Jupiter Conjunction (Every 20 Years) = US President Elected Near That Date Faces Mortality Risk
**Source:** Mehta/Rao Ch 2
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A Saturn-Jupiter conjunction occurs (approximately every 20 years). A US President is elected in a year close to the conjunction date.
**Result:** That US President faces elevated mortality risk during their term. Historical pattern: Presidents elected in 1840, 1860, 1880, 1900, 1920, 1940, 1960 all died in office.
**Notes:** The Sat-Jup conjunction also marks Triplicity shifts -- when the conjunction moves to an Earthy triplicity (Virgo/Taurus/Capricorn), it signals a 200-year era of slow material world-order restructuring...
**PHR Reason:** The historical pattern cited (1840, 1860, 1880, 1900, 1920, 1940, 1960) is accurate for US presidential deaths in office, but attributing this to Saturn-Jupiter conjunction timing is not a classical Vedic mundane astrology rule; this appears to be a Western astrology observation (20-year cycle) retrofitted to Vedic sources. Not faithfully sourced to Mehta.

#### `mehta-ch2-sat-rahu-conjunction-imperialism-ends`
**Title:** Saturn-Rahu Conjunction = End of Imperialism, New Nations, or Mass Destruction via Advanced Weapons
**Source:** Mehta/Rao Ch 2
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Transit Saturn and Rahu conjoin in any sign. Special case: conjunction occurs in Capricorn.
**Result:** End of an imperial era, birth of new nations, OR mass destruction via atomic or advanced weaponry. IF conjunction in Capricorn: major global conflict = TRUE.
**Notes:** Historical validations: 1945 Sat-Rah conjunction → atomic bomb usage, end of British/Japanese imperialism. 1990 Sat-Rah conjunction in Capricorn → Gulf War.
**PHR Reason:** Saturn-Rahu conjunction is a recognized malefic signal, but the dual outcome (imperialism OR mass destruction) and the special Capricorn case require cross-reference to confirm Mehta's exact formulation; the rule as stated is somewhat disjunctive.

#### `mehta-ch2-three-saturdays-tuesdays-paksha-alert`
**Title:** Three Saturdays or Three Tuesdays in a Lunar Fortnight = High Inauspicious Alert
**Source:** Mehta/Rao Ch 2
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** In a Hindu lunar month (Paksha chart period -- 15 days), count occurrences of Saturday and Tuesday. Condition: >= 3 Saturdays OR >= 3 Tuesdays within the fortnight.
**Result:** High-alert inauspicious period. Elevated probability of: national tragedy, communal riots, financial crashes, or political violence within that 15-day window.
**Notes:** This must be audited against the Hindu lunar month (Paksha), NOT the Gregorian calendar. Combine with communal tension gate: if Paksha Lagna is also Leo or Scorpio, probability of communal crisis is H...
**PHR Reason:** Paksha-level day-of-week counting (Saturday/Tuesday) is not a standard classical Vedic mundane rule in major sources; this appears to be a modern interpolation. Requires verification against Mehta's actual methodology.

## v13 -- Koorma directional + Sanghatta Chakra + war gates

#### `gaur-ch11-eclipse-jupiter-aspect-neutralizes`
**Title:** Jupiter Aspecting an Eclipse Point Destroys / Neutralizes Its Bad Effects
**Source:** Gaur/AIFAS Ch 11
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** Jupiter aspects the sign or degree where a solar or lunar eclipse occurs.
**Result:** The malefic effects of the eclipse are significantly reduced or fully neutralized. Jupiter's expansive and benevolent nature acts as a protective shield.
**PHR Reason:** Jupiter aspect reducing eclipse malefic effects is sound in principle, but 'full neutralization' is overstated; classical texts indicate mitigation rather than complete cancellation.

#### `gaur-ch11-eclipse-lunar-solar-sequence-tyrant-rulers`
**Title:** Lunar Eclipse Followed by Solar Eclipse within 15 Days = Rulers Become Tyrants
**Source:** Gaur/AIFAS Ch 11
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A lunar eclipse is followed by a solar eclipse within 15 days (i.e., both eclipses occur in the same paksha or fortnight).
**Result:** National Authoritarianism Alert: rulers become tyrants. Emergency rule, suspension of democratic norms, or authoritarian crackdowns become likely.
**Notes:** VALIDATED via historical patterns of emergency rule announcements globally. Cross-validate with Mehta Ch 2 Step 5 (eclipse duration = impact duration: 1 hour solar = 1 year of impact). This is the 'Ty...
**PHR Reason:** Contradicts: gaur-ch11-eclipse-solar-lunar-sequence-religious-happiness

#### `gaur-ch11-eclipse-solar-lunar-sequence-religious-happiness`
**Title:** Solar Eclipse Followed by Lunar Eclipse within 15 Days = Religious Sentiments Increase
**Source:** Gaur/AIFAS Ch 11
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** A solar eclipse is followed by a lunar eclipse within 15 days.
**Result:** Religious sentiments and general happiness increase across the population. Spiritual movements gain momentum; charitable activities rise.
**PHR Reason:** Contradicts: gaur-ch11-eclipse-lunar-solar-sequence-tyrant-rulers

#### `gaur-ch4-koorma-northeast-enemy-attack`
**Title:** Mars in 7th House in NE Koorma Constellations = Enemy Attack from North-East
**Source:** Gaur/AIFAS Ch 4
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Mars occupies the 7th house of the national horoscope AND is transiting a North-East Koorma constellation (Revati, Ashwini, or Bharani).
**Result:** Enemy attack or armed aggression originates from the North-East direction. For India: this points specifically to the North-East frontier.
**Notes:** 7th house = International Disputes and Rebellions (Ministry mapping). Bharani is ruled by Venus but contains intense Mars energy (Yama's nakshatra). This rule enables directional specificity for milit...
**PHR Reason:** The dual condition (7th house Mars + NE Koorma transit) is coherent but the specific constellation assignment (Revati, Ashwini, Bharani as NE) requires cross-check against Gaur's directional grid.

#### `gaur-ch8-commodity-malefic-vedha-price-spike`
**Title:** Malefic Vedha on Planetary Lord = Price Spike for That Planet's Commodities
**Source:** Gaur Ch 8; Mehta Ch 8
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** A malefic planet (Saturn, Mars, Rahu, Ketu) creates Vedha on the sign or nakshatra ruling a specific commodity (use Commodity Ownership Dictionary -- spec: mehta-ch8-commodity-ownership-dictionary). Example: Saturn transits Swati → Vedha on Chillies, Mustard, Cotton (Swati's commodities).
**Result:** Critical Price Inflation Alert for all commodities owned by the afflicted sign/nakshatra. Prices rise sharply during the transit period.
**Notes:** Price Vector Logic: Malefic Vedha = Price INCREASE; Benefic Vedha = Price DECREASE. If a planet is in a sign ALSO under Vedha from another malefic simultaneously, the commodity price inflation weight ...
**PHR Reason:** The rule is logically sound but depends entirely on the accuracy and completeness of the Commodity Ownership Dictionary; without that reference, verification is incomplete.

#### `gaur-ch8-gold-reserve-banking-crisis-veto`
**Title:** Sun + Jupiter in Mutual Vedha + Saturn in Capricorn = State Gold & Banking Crisis
**Source:** Gaur Ch 8; Mehta Ch 8
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Sun and Jupiter (both Gold significators) are in mutual Vedha on the Sanghatta grid WHILE Saturn transits Capricorn (Makar rashi).
**Result:** State-level Gold Liquidity Crisis and Banking Instability. Gold reserves come under pressure; banks face solvency or trust issues.
**Notes:** Capricorn is the sign of India and also rules Gold, Iron, Coal, Steel (Gaur Ch 4 zodiac commodity map). Saturn in Capricorn = own sign, adding structural intensity. This is a compound rule requiring t...
**PHR Reason:** The condition 'mutual Vedha on Sanghatta grid' is vague and non-standard; Sanghatta is a rare conjunction type, not a grid. The triple condition (Sun-Jupiter Vedha + Saturn in Capricorn) lacks classical precedent in Mehta or Gaur.

## v14 -- Macro-conjunctions + transit timing

#### `gaur-ch10-45-muhurti-ingress-overrides-drought`
**Title:** Sun Ingress in 45-Muhurti Constellation Overrides All Drought/Dry-Sign Signals
**Source:** Gaur/AIFAS Ch 10
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** The Sun enters any zodiac sign while the Sun is in a 45-Muhurti constellation: Rohini, Punarvasu, Uttaraphalguni, Vishakha, Uttarashadh, or Uttarabhadrapad.
**Result:** Good rains are assured. Grains, ghee, oil, and cotton become cheap. This overrides all dry-season signals, malefic weekday ingress results, and any drought indications from sign or star placements.
**PHR Reason:** The claim that a 45-Muhurti ingress 'overrides all dry-season signals' and 'malefic weekday ingress results' is too absolute and not supported by classical mundane astrology; override rules are rare and require explicit textual authority.

#### `gaur-ch10-mars-ahead-sun-monsoon-failure`
**Title:** Mars Ahead of Sun During Rainy Season = Monsoon Failure
**Source:** Gaur/AIFAS Ch 10
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Mars is at a higher zodiacal degree than the Sun during the rainy season -- specifically when the Sun is in Gemini or Cancer.
**Result:** 'Monsoon Failure: Rains will be obstructed or delayed.' Agricultural crisis follows -- below-normal southwest monsoon for India.
**Notes:** The rainy season window is Sun in Gemini (approx. June 15 - July 15) and Sun in Cancer (approx. July 15 - Aug 15). Monitor Mars longitude vs Sun longitude in this window annually.
**PHR Reason:** The condition 'Mars at higher zodiacal degree than Sun' is clear, but restricting to Gemini/Cancer only is narrow; classical sources (Gopalakrishnan, Mehta) typically apply Mars-ahead-of-Sun to broader monsoon periods. Verify source specificity.

#### `gaur-ch10-saturn-28-degree-aries-market-correction`
**Title:** Saturn at 28-29° Aries = Bearish Market Correction for Hardware, Gems, and Metals
**Source:** Gaur/AIFAS Ch 10
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Transit Saturn reaches 28° to 29° in Aries (Mesha rashi).
**Result:** 'Bearish Market Correction Alert' for hardware, gems, and metals. Prices which were elevated throughout Saturn's transit of Aries undergo a sharp decline. This acts as a natural 'price circuit breaker' at this specific degree.
**Notes:** Throughout Saturn's stay in Aries, oils, gold, silver, copper, gems, and hardware are expensive. This correction rule fires ONLY at 28-29° and produces a temporary crash before Saturn ingresses into T...
**PHR Reason:** Saturn at 28-29° Aries triggering a specific 'circuit breaker' correction is plausible but the exact degree threshold and its universal application across hardware/gems/metals lacks explicit confirmation in primary Gaur sources.

#### `gaur-ch10-saturn-retrograde-uttarashadh-poorvashadh-famine`
**Title:** Saturn Retrograde Re-Entry from Uttarashadha into Poorvashadha = 12-Year Famine Protocol
**Source:** Gaur/AIFAS Ch 10
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn, while retrograde, crosses back from Uttarashadha nakshatra into Poorvashadha nakshatra (i.e., moves backwards from Sagittarius 26°40'+ into Sagittarius 13°20'-26°40').
**Result:** CRITICAL LONG-TERM FAMINE AND AGRICULTURAL COLLAPSE ALERT. Severe drought and grain crisis extending up to 12 years. Escalate to the highest diagnostic level -- this matches the Rohini Gate severity for agricultural destruction.
**Notes:** This rule is the specific transit-level famine trigger. The Rohini Gate (AH-13) is the constellation-level famine trigger. If BOTH activate simultaneously: famine severity is near-certain and prolonge...
**PHR Reason:** The 12-year famine duration and comparison to 'Rohini Gate severity' are not standard in Gaur/AIFAS texts; Saturn retrograde nakshatra transitions do trigger agricultural alerts, but this formulation appears speculative and over-dramatized.

#### `mehta-ch10-mars-ketu-fiery-sign-terrorism`
**Title:** Mars-Ketu Conjunction in Fiery Sign / Fiery Nakshatra = High-Intensity Terrorist Event
**Source:** Mehta/Rao Ch 10
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** Mars conjuncts Ketu in a Fiery Sign (Aries, Leo, Sagittarius) OR in a fiery/violent nakshatra (Moola, Jyeshtha, Bharani). 1-degree orb applies for maximum severity.
**Result:** Extreme_Terrorist_Event = TRUE. High-intensity suicide attacks, bombings, or mass-casualty events. Ketu provides secrecy and self-immolation energy; Mars provides the explosive force.
**Notes:** VALIDATED: 9/11 WTC (2001) -- Mars conjunct Ketu in Sagittarius/Moola, opposing Jupiter in Gemini (USA's sign). This is a 'template match' rule -- future dates with Mars-Ketu within 1° in Fiery Signs sh...
**PHR Reason:** The rule is coherent and sourced, but the claim of 'extreme terrorist event' as a deterministic outcome requires careful orb definition and historical validation; the 1-degree orb is reasonable but severity language is absolute.

#### `mehta-ch10-saturn-jupiter-us-president-mortality-veto`
**Title:** Saturn-Jupiter Conjunction Year + US Presidential Election = President Mortality Risk
**Source:** Mehta/Rao Ch 10
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A Saturn-Jupiter conjunction occurs in any sign. A US Presidential election takes place in the same year or within 1 year of the conjunction.
**Result:** Mortality Risk = CRITICAL for that US President. High probability that the President will not complete their full term in office (death in office, assassination, forced resignation, or severe incapacitation).
**Notes:** VALIDATED HISTORICAL CASES: Presidents elected in 1840, 1860, 1880, 1900, 1920, 1940, 1960 all died in office. (The 'Tecumseh's Curse' / 'Zero-Year Curse' pattern.) The 1980 conjunction produced the a...
**PHR Reason:** The rule conflates Saturn-Jupiter conjunction with US Presidential mortality risk without clear classical source; Mehta does not establish this specific nation-ruler linkage. The 1-year window is also arbitrary.

#### `mehta-ch10-saturn-mars-sixth-house-internal-military`
**Title:** Saturn-Mars Conjunction in Nation's 6th House = Internal Military Operation / Massacre
**Source:** Mehta/Rao Ch 10
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn and Mars conjoin in the 6th house of a national horoscope (foundation chart or annual Solar Ingress chart). Upgrade severity if conjunction is also in a Dual Sign.
**Result:** 'Black Day' Configuration: Internal military operation or large-scale massacre. Internal security forces are deployed against the civilian population. For Dual Sign + 6th-from-India: General Massacre confirmed.
**Notes:** VALIDATED: Operation Blue Star (June 1984) -- Saturn-Mars conjunction in the 6th house of India's national chart. Nadir Shah massacre (1739) -- Saturn-Mars in Dual Sign, 6th from Makar Lagna. This rule ...
**PHR Reason:** The 6th house + Dual Sign escalation is coherent, but the phrase 'General Massacre confirmed' for India-specific 6th house is overly deterministic and lacks explicit Mehta precedent.

#### `mehta-ch10-saturn-rahu-capricorn-regime-change`
**Title:** Saturn-Rahu Conjunction in Capricorn = Major Regime Change in Middle East
**Source:** Mehta/Rao Ch 10
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn and Rahu conjoin in Capricorn (Makar rashi).
**Result:** Major_Regime_Change_Middle_East = TRUE. Multi-planet concentration in Capricorn (especially within 1° orb) triggers 'Economic Paradigm Shift' AND 'Catastrophic Event' (3× weight when within 1°).
**Notes:** VALIDATED: 1991 Gulf War -- Sun, Saturn, Moon, Rahu all met within 1° in Capricorn. Capricorn also rules India, Afghanistan, Punjab -- so secondary alerts for the Indian subcontinent are always warrante...
**PHR Reason:** The rule is sourced but the Middle East specificity and the 3× weight multiplier for 1° orb require verification against Mehta's actual text; the condition is clear but the result scope may be overstated.

#### `mehta-ch10-saturn-rahu-gemini-nuclear-shift`
**Title:** Saturn-Rahu Conjunction in Gemini = Global Shift in Military Technology / Nuclear Escalation
**Source:** Mehta/Rao Ch 10
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn and Rahu conjoin in Gemini (Mithuna rashi).
**Result:** 'Atomic/Colonial Veto' triggered: Global Shift in Military Technology / Nuclear Escalation AND the Birth of New Sovereign States. Old empires collapse; new nation-states emerge.
**Notes:** VALIDATED: 1945 conjunction -- Hiroshima/Nagasaki + decolonization wave. Gemini = sign of USA and communications technology. Rahu = atomic/disruptive energy; Saturn = death of the old order. Next simil...
**PHR Reason:** The dual outcome (nuclear escalation + new sovereign states) is coherent but the Gemini-specific linkage to 'atomic/colonial' events requires historical validation; the rule is plausible but borderline on specificity.

## v15 -- Mars/Mercury/Jupiter/Venus/Rahu transits + Koorma kill-switch

#### `gaur-ch10-jupiter-cancer-sun-aspect-supremacy`
**Title:** Jupiter in Cancer (Exaltation) Aspected by Sun = Establishment of Global Supremacy
**Source:** Gaur/AIFAS Ch 10
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** Jupiter transits Cancer (its exaltation sign) AND the Sun aspects Jupiter by conjunction or trine.
**Result:** 'Establishment of Global Supremacy and victory in international treaties' for the relevant nation. Treaties are signed; international cooperation peaks; the nation's position on the world stage is elevated.
**PHR Reason:** The condition 'Sun aspects Jupiter by conjunction or trine' is vague (conjunction is not an aspect; trine is 120°); classical mundane astrology does not typically use 'trine' for Sun-Jupiter. Condition needs clarification.

#### `gaur-ch10-jupiter-capricorn-afflicted-banking-crisis`
**Title:** Jupiter Afflicted in Capricorn = Banking Scandal and Interest Rate Hikes
**Source:** Gaur/AIFAS Ch 10
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Jupiter transits Capricorn AND is afflicted by Saturn, Rahu, or Mars.
**Result:** 'Critical Alert: Instability in national treasury, banking scandals, and high-interest rate hikes.' Capricorn is Jupiter's sign of debilitation -- affliction here damages financial systems directly.
**PHR Reason:** Jupiter's debilitation in Capricorn is correct, but the rule's specificity to 'banking scandals and high-interest rate hikes' is modern economic language not typical of classical Vedic mundane sources; verify source attribution.

#### `gaur-ch10-mars-12th-lord-afflicted-military-insubordination`
**Title:** Mars = 12th House Lord and Afflicted in Transit = Risk of Military Insubordination / Coup
**Source:** Gaur/AIFAS Ch 10
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** In the national horoscope, Mars is the lord of the 12th house (house of foreign attack, secret enemies). Mars is simultaneously afflicted in transit by Saturn, Rahu, or Ketu.
**Result:** 'Risk of Military Insubordination or Coup' alert. Internal forces act against the established authority.
**PHR Reason:** The rule conflates natal chart (Mars as 12th lord) with transit affliction without clear methodology; classical mundane astrology typically uses either natal or transit analysis separately, not this hybrid approach.

#### `gaur-ch10-mars-gemini-sudden-price-volatility`
**Title:** Mars Transiting Gemini = Sudden Extreme Price Spike or Crash (Market Shock)
**Source:** Gaur/AIFAS Ch 10
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Transit Mars enters Gemini (Mithuna rashi).
**Result:** Materials become very costly or cheap suddenly -- market shock event. When Mars goes Direct in Gemini, this extreme volatility triggers immediately. When Mars enters Gemini Retrograde, goods become expensive or cheap gradually.
**Notes:** Gemini is the sign of USA and communications/trade. Mars in Gemini produces the most volatile price environment of all sign transits. Monitor for compounding effect: if Rahu or Saturn also aspect Gemi...
**PHR Reason:** Mars in Gemini is classically associated with volatility and trade disruption, but the distinction between direct-entry (immediate shock) vs retrograde-entry (gradual) lacks explicit sourcing in standard Gaur/AIFAS texts and appears over-specified.

#### `gaur-ch10-mercury-combust-leo-stock-market-crash`
**Title:** Mercury Combusted and Afflicted in Leo = Stock Market Decline and Textile Bearishness
**Source:** Gaur/AIFAS Ch 10
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Mercury is combusted (within 15° of the Sun) AND afflicted while transiting Leo.
**Result:** 'Sudden decline in Stock Market values and Textile/Jute sector bearishness' alert. Leo is the sign of rulers and the stock exchange. Combustion kills Mercury's trading function.
**PHR Reason:** Mercury combustion + Leo is sound (Leo = rulers/exchange), but the specific pairing of 'stock market crash' with 'textile/jute sector bearishness' as a unified result is overly prescriptive and may conflate separate sectoral rules.

#### `gaur-ch10-mercury-retrograde-gemini-education-scandal`
**Title:** Mercury Retrograde Entering Gemini = Vegetables Cheap + Education Scandal Risk
**Source:** Gaur/AIFAS Ch 10
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Mercury enters Gemini in Retrograde motion.
**Result:** Vegetables become cheap. Cross-reference with House 5 (Education Ministry) -- 'Potential scams and scandals in educational institutions' alert triggered.
**Notes:** Mercury retrograde in its own sign amplifies the House 5 effect. Mercury rules Gemini and Virgo -- retrograde here disrupts Mercurial functions: trade, communications, education, media.
**PHR Reason:** The rule conflates two unrelated outcomes (vegetables cheap + education scandal) without coherent logical connection; Mercury retrograde in Gemini does not classically trigger education ministry scandals in standard mundane texts.

#### `gaur-ch10-mercury-sign-ingress-weather-disturbance`
**Title:** Mercury Crossing Any Sign Boundary = Weather Disturbance Alert
**Source:** Gaur/AIFAS Ch 10
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** Mercury transits from one zodiac sign to another (any sign ingress).
**Result:** 'Weather Disturbance Alert' -- noticeable atmospheric changes occur. This includes sudden temperature shifts, unexpected rain or dry spells, or wind changes.
**PHR Reason:** Mercury ingress triggering weather disturbance is plausible (Mercury = air/communication), but the rule is too broad and non-specific; classical texts typically require additional affliction or aspect to predict weather events.

#### `mehta-ch7-koorma-northwest-affliction-tribal-insurgency`
**Title:** Malefic in NW Koorma Cluster = Tribal Unrest and Instability in Afghanistan / Oxus Corridor
**Source:** Mehta/Rao Ch 7
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A malefic planet transits or creates Vedha on the North-West Koorma constellations: Uttarashadh, Sravana, or Dhanishtha.
**Result:** 'Tribal unrest and instability in the Oxus Valley / Afghanistan corridor' alert. Specific regions: North Pakistan, Afghanistan, Northern Kashmir, Jodhpur. Ancient correlation: Madra (Sialkot/West Punjab) regime collapse risk.
**Notes:** Dhanishtha is particularly sensitive as it sits on the NW-North boundary. Saturn retrograde in Dhanishtha = maximum unrest signal for this corridor. Cross-validate with Capricorn sign afflictions (Cap...
**PHR Reason:** Koorma Chakra directional mapping is classical, but the specific regional correlation (Oxus Valley, Madra, Sialkot) and the 'tribal unrest' outcome require verification against Mehta Ch 7; the rule is coherent but the historical-geographic specificity may be over-determined.

#### `mehta-ch7-koorma-saturn-west-triple-amplifier`
**Title:** Saturn in Western Sign + Western Koorma Sector = Malefic Impact on Industry TRIPLED
**Source:** Mehta/Rao Ch 7
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn is transiting a Western zodiac sign (Libra or Capricorn) AND is occupying the Western Koorma sector constellations (Jyeshtha, Moola, Poorvashadh -- the Tail / West sector).
**Result:** The malefic impact on heavy industry and labor is TRIPLED. Severe industrial stagnation, labor strikes, and commodity shortages for the West direction. For India: impact concentrated on Western Maharashtra, Baluchistan, West Punjab.
**PHR Reason:** The 'triple amplifier' logic (Saturn in Western sign + Western Koorma sector = 3× impact) is coherent but the multiplication factor is not standard in classical sources; requires confirmation that Mehta explicitly endorses this amplification rule.

#### `mehta-ch7-koorma-triple-directional-audit`
**Title:** Triple Directional Audit (Koorma + Planet + 7th House) All Agree = Critical Conflict Confidence
**Source:** Mehta/Rao Ch 7
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** For a war or major conflict prediction, audit three directional signals: (1) Koorma Chakra: which direction is the afflicted nakshatra cluster mapped to? (2) Planet's Direction: which compass point does the afflicting planet rule (Sun=East, Moon=NW, Mars=South, Mercury=North, Jupiter=NE, Venus=SE, S...
**Result:** IF all three directional signals agree on the same direction: prediction confidence for conflict in that direction = CRITICAL. Example: Saturn (West) in Jyeshtha (West sector) with 7th house Mars in Libra (West) = Critical conflict alert for Baluchistan/West Punjab corridor.
**Notes:** This is the validation gate that transforms a single-signal alert into a confirmed prediction. Two signals agreeing = high confidence. All three agreeing = critical/confirmed.
**PHR Reason:** The condition is incomplete: it cuts off mid-sentence at '7th House Direction: Mars in Aries=East, Cancer=North, Libra=' without finishing the mapping. Cannot evaluate coherence or correctness of an incomplete rule.

## v16 -- Gaur Ch5/6/7 monsoon + crop + Sarvatobhadra trade

#### `mundane-gaur-ch5-ardra-afternoon-entry`
**Title:** Ardra Entry in Afternoon -- Grain Scarcity Override
**Source:** Gaur Ch 5 -- Ardra Entry Time Logic
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Time of Ardra Entry = Afternoon (between 12:00 and sunset)
**Result:** MARKET SCARCITY ALERT: Afternoon entry overrides all positive Tithi/Yoga signals. Poor crops expected; grain prices will rise. Agriculture sector under stress for the season.
**Notes:** Afternoon entry is a hard veto -- positive yogas cannot neutralize it.
**PHR Reason:** Ardra entry timing (morning/afternoon/evening) is a recognized Gaur monsoon signal, but the claim that afternoon entry 'overrides all positive Tithi/Yoga signals' is a strong assertion; requires verification that Gaur explicitly states this override hierarchy.

#### `mundane-gaur-ch5-ardra-bumper-harvest`
**Title:** Ardra Entry Bumper Harvest -- Triyodashi + Pushya + Sea Residence
**Source:** Gaur Ch 5 -- Ardra Entry & Rohini Chart
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Ardra Entry Tithi = Triyodashi AND Moon in Pushya at Entry AND Rohini Samudra Chakra Residence = Sea
**Result:** OPTIMAL MONSOON: Record grain production confirmed. Gardener's House residence signals a lush, prosperous year. Grain prices to drop significantly. National food security high.
**Notes:** Triple convergence of best Tithi + best Moon nakshatra + Sea residence. All three must be present for maximum confidence.
**PHR Reason:** Condition combines three independent indicators (Tithi, Moon nakshatra, Samudra Chakra) with AND logic; coherence of this specific triple conjunction in classical sources requires verification against Gaur Ch 5 primary text.

#### `mundane-gaur-ch5-ardra-krithika-fire`
**Title:** Moon in Krithika at Ardra Entry -- Fire Risk & Rain Deficiency
**Source:** Gaur Ch 5 -- Ardra Entry Moon Nakshatra
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Moon in Krithika at moment of Ardra Entry
**Result:** EMERGENCY ALERT: High risk of accidental fires and heatwaves. Moisture deficiency confirmed. Rain will be deficient for the season; fire hazard to crops and rural infrastructure elevated.
**PHR Reason:** Contradicts: mundane-gaur-ch5-rohini-sea-flash-flood

#### `mundane-gaur-ch5-ardra-saturday-disease`
**Title:** Ardra Entry Saturday + Midnight -- Epidemic & Civil Unrest
**Source:** Gaur Ch 5 -- Ardra Entry
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Ardra Entry Weekday = Saturday AND Time of Entry = Midnight
**Result:** PUBLIC HEALTH WARNING: High risk of widespread epidemics and civil unrest throughout the rainy season. Disease incidence at peak; social stability threatened.
**PHR Reason:** Midnight timing condition is highly specific; classical Gaur sources typically emphasize weekday + Tithi/Yoga combinations rather than precise time-of-day thresholds for disease forecasting.

#### `mundane-gaur-ch5-rohini-sea-flash-flood`
**Title:** Rohini Sea Residence + Watery 12th House -- Flash Flood Risk
**Source:** Gaur Ch 5 -- Ardra Entry Horoscope + Rohini Chart
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Rohini Samudra Chakra Residence = Sea AND Ardra Entry Horoscope Sun in 12th House AND Moon in Watery Sign
**Result:** REGIONAL RISK ALERT: Overall rains are sufficient (Sea residence confirms), but high probability of localized flood-related crop loss. Flood_Risk_Weight +0.4 applied. Infrastructure in low-lying areas at risk.
**PHR Reason:** Condition requires three independent chart placements (Samudra Chakra + Ardra Entry Sun + Moon sign); the specific combination and its flood-risk weighting (+0.4) needs source verification.

#### `mundane-gaur-ch6-mars-venus-jupiter-catastrophic`
**Title:** Mars 7th from Venus + Jupiter 7th from Saturn -- Annihilating Floods
**Source:** Gaur Ch 6 -- Planetary Rain Combinations
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** Mars in 7th house from Venus AND Jupiter in 7th house from Saturn
**Result:** CATASTROPHIC WEATHER ALERT: Annihilating floods imminent. Highest severity weather event in the Gaur rain combination system. National disaster-level flooding expected.
**PHR Reason:** Condition specifies two independent 7th-house relationships (Mars from Venus AND Jupiter from Saturn) with no logical connection stated; this appears to conflate two separate rain combination rules without coherent astrological justification.

#### `mundane-gaur-ch6-ownership-rain-confirm`
**Title:** Sun/Moon Cross-Ownership -- Rain Certainty Confirmation
**Source:** Gaur Ch 6 -- Constellation Ownership
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Sun occupies a Moon-owned star AND Moon occupies a Sun-owned star simultaneously (cross-ownership swap)
**Result:** RAIN CERTAINTY: Both planetary ownership indicators confirm precipitation. Combined with Female-Male gender interaction = Optimal Rainfall Forecast. High confidence for rainfall within 24-48 hours.
**PHR Reason:** Cross-ownership swap (Sun in Moon-star AND Moon in Sun-star simultaneously) is a rare configuration; the 24-48 hour precipitation window is precise but requires source validation for timing specificity.

#### `mundane-gaur-ch6-saptnadi-amrita-rain`
**Title:** Saptnadi Amrita Nadi Vedha -- Continuous 1-7 Day Rain
**Source:** Gaur Ch 6 -- Saptnadi Chart
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Gentle (benefic) AND Cruel (malefic) planets both present in Amrita Nadi (Ashlesha, Magha, Shravan, Dhanishtha) AND Moon also present
**Result:** METEOROLOGICAL ALERT: Continuous rainfall predicted for 1 to 7 days (may recur multiple times). Moon is lord of Amrita Nadi -- its presence is the primary rain trigger. High confidence forecast.
**PHR Reason:** Contradicts: mundane-gaur-ch6-trinadi-no-rain-veto

#### `mundane-gaur-ch6-trinadi-catastrophic-flood`
**Title:** All Male Planets in One Nadi -- Destructive Rain Alert
**Source:** Gaur Ch 6 -- Snake Trinadi Chart
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** All male planets (Sun, Mars, Saturn, Rahu, Ketu) occupy one Trinadi Nadi
**Result:** EMERGENCY ALERT: High probability of excessive and destructive rains. Flash flood risk elevated. Agricultural and infrastructure damage expected.
**PHR Reason:** Condition requires all five male planets in one Trinadi Nadi--an extremely rare configuration; the result 'excessive and destructive rains' is coherent but the specificity of this conjunction in classical Gaur sources needs verification.

#### `mundane-gaur-ch6-trinadi-hail-storm`
**Title:** Female + Eunuch Planets Bundled -- Hail Storm Hazard
**Source:** Gaur Ch 6 -- Snake Trinadi Chart
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Female planets (Moon, Venus) AND Eunuch planet (Mercury) all concentrated in one Trinadi Nadi
**Result:** AVIATION & AGRICULTURE WARNING: High probability of damaging hail storms. Severe hazard to standing crops and exposed infrastructure.
**PHR Reason:** Female + Eunuch planet concentration in one Trinadi is plausible, but hail-storm specificity (vs. general rain) requires source confirmation; gender-based weather differentiation is non-standard in most classical texts.

#### `mundane-gaur-ch6-trinadi-no-rain-veto`
**Title:** Trinadi Rule 8 -- Malefics in Patal + Benefics in Heaven = No Rain
**Source:** Gaur Ch 6 -- Snake Trinadi Chart
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** Malefic planets (Sun, Mars, Saturn, Rahu, Ketu) concentrated in Patal Nadi AND Benefic planets (Moon, Mercury, Jupiter, Venus) concentrated in Heaven Nadi
**Result:** CRITICAL RAINFALL FAILURE: Strict veto -- no rains whatsoever. Atmospheric Inversion confirmed. Moisture delivery completely blocked. Drought monitoring protocol activated.
**PHR Reason:** Condition specifies malefics in Patal Nadi AND benefics in Heaven Nadi (opposite Nadis); this appears to describe a separation/opposition rather than a unified rain-blocking mechanism, and 'Atmospheric Inversion' is modern meteorological language not found in classical Vedic texts.

#### `mundane-gaur-ch7-conspiracy-yoga-vi`
**Title:** Crop Yoga VI -- Jupiter Aquarius + Moon Taurus + Mars/Saturn Capricorn
**Source:** Gaur Ch 7 -- Sasya Jatak Crop Yogas
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Jupiter in Aquarius AND Moon in Taurus AND Saturn AND Mars both in Capricorn simultaneously
**Result:** COMPLEX HARVEST: Produce = Good (high yields) BUT Status = 'National Conspiracy and Disease Alert'. High yields will be overshadowed by national health crises and political plots. Markets disrupted despite good supply.
**PHR Reason:** Condition specifies exact sign placements (Jupiter Aquarius, Moon Taurus, Saturn+Mars Capricorn) with high rarity; the result conflates agricultural yield with political/health crises, which is coherent but requires source validation for this specific yoga definition.

#### `mundane-gaur-ch7-total-crop-failure-yoga-ix`
**Title:** Crop Yoga IX -- Malefics in 7th + 1st/4th/10th = Total Crop Failure
**Source:** Gaur Ch 7 -- Sasya Jatak Crop Yogas
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn OR Mars in 7th house from Sun AND another malefic in 1st, 4th, or 10th house from Sun in seasonal ingress chart AND no benefic aspects on these malefics
**Result:** TOTAL CROP FAILURE: Complete agricultural collapse predicted. Grain prices will spike to extreme highs. If benefics aspect the malefics → Partial/Localized destruction only. National food security critical.
**PHR Reason:** Condition is specific and logically coherent (malefic placement + lack of benefic aspect = crop failure), but 'no benefic aspects' is an absolute qualifier that may be overly rigid; classical texts typically use 'weak' or 'afflicted' rather than absolute negation. Verify Gaur Ch 7 exact phrasing.

#### `mundane-gaur-ch8-dual-mapping-volatility`
**Title:** Dual-Mapping Conflict -- Sign Bullish vs Nakshatra Bearish = Choppy Markets
**Source:** Gaur Ch 8 -- Material Database (Dual-Mapping Filter)
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** A commodity's governing Zodiac Sign indicates Bullish trend AND its governing Nakshatra indicates Bearish trend simultaneously (or vice versa) -- example: Gold via Aries = Bullish, Gold via Pushya = Bearish
**Result:** MARKET VOLATILITY: Choppy trading in the conflicted commodity. No clean directional trend -- price oscillates. Engine outputs 'Dual-Signal Conflict' flag; position sizing should be reduced.
**PHR Reason:** Contradicts: mundane-gaur-ch8-gold-silver-bullion-gate

#### `mundane-gaur-ch8-gold-silver-bullion-gate`
**Title:** Bullion Gate -- Jupiter transits Pushya + Sun in Aries
**Source:** Gaur Ch 8 -- Material Database / Ch 9 -- Sarvatobhadra
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Jupiter transiting Pushya nakshatra AND Sun in Aries sign simultaneously
**Result:** BULLISH PRECIOUS METALS: Massive price surge for Gold and Silver expected. Multi-vector pressure confirmed -- Pushya governs Gold/Silver (nakshatra ownership) and Aries governs them (planetary ownership via Sun). Gold/Silver at seasonal highs.
**PHR Reason:** The condition conflates two independent systems (nakshatra ownership and planetary ownership via Sun sign) without classical justification; Gaur's material database does not establish that simultaneous Sun-Aries + Jupiter-Pushya creates 'multi-vector pressure' or that both must align for bullish metals. This appears to be synthetic rule-stacking.

#### `mundane-gaur-ch8-saturn-mars-capricorn-chemical`
**Title:** Saturn + Mars in Capricorn -- Industrial Accident & Chemical Price Spike
**Source:** Gaur Ch 8 -- Material Database Diagnostics
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn aspected by Mars in Capricorn sign
**Result:** INDUSTRIAL WARNING: High risk of accidents in steel mills or chemical leaks. Heavy hardware prices to fluctuate sharply. Capricorn governs Iron, Coal, Steel, Glass -- malefic conjunction here amplifies risk.
**PHR Reason:** Saturn-Mars aspect in Capricorn is logically sound (malefic conjunction in industrial sign), but the result conflates two distinct outcomes (accidents vs. price fluctuation) without clear causal link. Verify whether Gaur treats these as separate or unified predictions.

#### `mundane-gaur-ch9-sarvatobhadra-currency-spike`
**Title:** Sarvatobhadra Dhanishtha Malefic Vedha -- Currency & Metal Spike
**Source:** Gaur Ch 9 -- Sarvatobhadra Trade Engine
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn OR Rahu transiting Dhanishtha nakshatra (malefic) OR Mars has Right Vedha on Krittika
**Result:** CRITICAL METAL ALERT: Rapid price increase for Gold, Silver, All Currencies, Ruby, and Pearl predicted. Dhanishtha governs all currencies -- malefic Vedha here signals financial market stress.
**PHR Reason:** Condition mixes three unrelated triggers (Saturn in Dhanishtha OR Rahu in Dhanishtha OR Mars Vedha on Krittika) with no logical unity; result claims all three produce identical outcome (currency/metal spike), which violates coherence. Sarvatobhadra Vedha rules are specific to constellation pairs, not aggregated across unrelated nakshatras.

#### `mundane-gaur-ch9-sarvatobhadra-market-sentiment`
**Title:** Sarvatobhadra Majority Vedha -- Overall Market Sentiment Signal
**Source:** Gaur Ch 9 -- Sarvatobhadra Trade Engine
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Count of Benefic Vedha points (Moon, Mercury, Jupiter, Venus active on constellation) > Count of Malefic Vedha points (Sun, Mars, Saturn, Rahu, Ketu active on constellation)
**Result:** BEARISH MARKET SENTIMENT: Prices are likely to soften as goods become easily available. Accumulation recommended as prices dip. Reverse (Malefic > Benefic) → Bullish overall market: prices rising across commodities.
**PHR Reason:** Vedha counting logic is sound, but the result reversal (Benefic > Malefic = Bearish, Malefic > Benefic = Bullish) is counterintuitive and requires explicit source validation from Gaur Ch 9. Classical Vedha typically treats benefic Vedha as supportive and malefic as obstructive.

#### `mundane-gaur-ch9-sarvatobhadra-textile-shortage`
**Title:** Sarvatobhadra Punarvasu Malefic Vedha -- Cotton & Textile Shortage
**Source:** Gaur Ch 9 -- Sarvatobhadra Trade Engine
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Mars transiting Punarvasu AND Mars has Front Vedha on Poorvashadh
**Result:** INDUSTRY WARNING: High volatility in cotton, jute, and silken goods. Supply chain disruption for textiles expected. Punarvasu governs cotton and millet -- malefic obstruction raises prices sharply.
**PHR Reason:** Mars in Punarvasu + Front Vedha on Poorvashadh is specific, but 'Front Vedha' terminology and its application to textile commodities requires verification against Gaur's exact Vedha definitions. Punarvasu-Poorvashadh Vedha relationship is plausible but needs source confirmation.

## v17 -- Gopal Ch3 (leadership auth) + Gopal Ch14 (markets)

#### `mundane-gopal-ch14-bpo-contrarian-gate`
**Title:** BPO/IT Contrarian Gate -- Ignore Media Collapse Predictions
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Media/analysts predict BPO or IT sector collapse or saturation) AND (Saturn is transiting the 3rd house of the National Independence Chart)
**Result:** Contrarian Alert: 'Override media skepticism entirely. BPO/IT sector will treble recruitment and set new export records. The Saturn-3rd-house transit structurally guarantees the knowledge-sector boom regardless of short-term noise. This is the single most reliable sectoral forecast from the 2006 aud...
**PHR Reason:** Rule is coherent and validated against 2004-2006 data, but the claim that 'Saturn-3rd-house transit structurally guarantees the knowledge-sector boom regardless of short-term noise' is an absolute assertion that may overstate determinism. Verify Gopalakrishnan's exact language on Saturn-3rd causality vs. correlation.

#### `mundane-gopal-ch14-decentralised-terror`
**Title:** Saturn in 12th of Coronation Chart -- Decentralised Terror Active
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Saturn transits the 12th house of a nation's Coronation/Oath-taking Chart)
**Result:** Security Alert: 'Decentralised terror doctrine is active. Security agencies must monitor cellular/autonomous threat cells -- not a conventional standing army. Disrupting the command head will NOT stop attacks. Each cell operates independently -- intelligence-based approach required'. Doctrine validate...
**PHR Reason:** Saturn-12th-house rule is classical (12th = hidden enemies, loss, confinement), but the leap from Saturn-12th to 'decentralised cellular terror doctrine' is interpretive and geopolitically specific. The validation (Bin Laden model) is post-hoc and does not establish causal mechanism. Verify Gopalakrishnan's exact wording.

#### `mundane-gopal-ch14-mall-culture-venus-rahu`
**Title:** Venus-Rahu Axis -- Mall Culture Explosion in Metropolis
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Venus as Lagna lord is in Rahu-Ketu axis -- i.e., Venus conjunct or opposite Rahu/Ketu in the national or annual chart)
**Result:** Retail Boom: 'Explosion of Malls, Hyper-marts, and new retail formats in major metropolis areas. Organised retail replaces traditional kirana stores at an accelerated pace. Mall construction stocks and retail chains in explosive growth phase'. Validation: 2006 India -- mall culture launched simultane...
**PHR Reason:** Venus-Rahu axis is classically associated with illusion, desire, and material expansion, which aligns with mall culture. However, the result (explosion of malls in 12+ metros simultaneously) is highly specific and may reflect 2006 India's economic cycle rather than pure astrological causation. Verify whether Gopalakrishnan treats this as deterministic or probabilistic.

#### `mundane-gopal-ch14-mars-perigee-manufacturing`
**Title:** Mars Perigee -- Manufacturing and Electrical Sector Efficiency Surge
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Mars is at perigee/closest to Earth)
**Result:** Manufacturing Boost: 'High efficiency in manufacturing units and electrical components. Automotive, medical equipment, and metal sectors achieve 1.5× normal growth. Auto ancillaries turn into export-oriented profit centres'. Note: Same transit also correlates with increased risk of fire accidents, b...
**PHR Reason:** Mars perigee correlating with manufacturing efficiency is plausible (Mars = energy, action, industry), but the rule conflates manufacturing boost with fire/accident risk without explaining the mechanism. The 1.5× growth multiplier is quantitatively specific but lacks source justification.

#### `mundane-gopal-ch14-mars-perigee-south-cm`
**Title:** Mars Perigee in Fixed Sign -- Multiple Regional Leaders Replaced
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Mars is at perigee -- closest point to Earth) AND (Mars occupies a Fixed Sign)
**Result:** Leadership Alert: 'High probability of multiple Chief Ministers or regional leaders being simultaneously replaced in the geographic direction represented by the sign Mars occupies (Mars = South direction). Incumbents in that region face structural electoral veto from the cosmos'. Validation: 2006 So...
**PHR Reason:** The rule assumes Mars perigee + Fixed Sign = directional leadership change in South India, but Mars perigee is a global phenomenon; the directional specificity (South) and the claim of 'structural electoral veto' are not standard mundane astrology principles. The 2006 validation (three CM losses) may be coincidental rather than causal.

#### `mundane-gopal-ch14-mars-proximity-children`
**Title:** Mars Proximity to Earth -- Mass Death Risk for Children
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Mars proximity to Earth is observed -- coming within 60 million km)
**Result:** Severe Warning: 'High risk of mass casualties among children via epidemic or violence. Surgical costs and paediatric healthcare costs surge. Simultaneously: manufacturing and fire incidents increase. One major mass-death event is expected during the Mars proximity window'. Validation: July 2003 Mars...
**PHR Reason:** Mars proximity (60M km threshold) predicting mass child casualties is an extraordinary claim without established classical precedent. The rule conflates three unrelated outcomes (child epidemics, surgical costs, manufacturing) and relies on a single 2003 validation. This violates coherence and appears speculative.

#### `mundane-gopal-ch14-mercury-bhukti-epidemic-recovery`
**Title:** Mercury Direct Motion in Bhukti -- Epidemic/Crisis Normalisation
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Current Bhukti Lord is Mercury) AND (Mercury resumes direct motion after a retrograde period)
**Result:** Crisis Normalisation: 'Agriculture and livestock industries will return to normalcy within 60 days of Mercury going direct. Food-related scares, poultry epidemics, and market panics will dissipate. Sector recovery is predictable and should be used as an entry point'. Validation: 2006 Bird Flu crisis...
**PHR Reason:** Mercury direct motion correlating with agricultural/livestock recovery is plausible (Mercury = commerce, communication, agriculture), but the 60-day window is quantitatively specific and the 2006 Bird Flu validation may reflect seasonal recovery rather than Mercury Bhukti causation. Verify Gopalakrishnan's exact timing claim.

#### `mundane-gopal-ch14-nadi-saturn-8th-from-jupiter`
**Title:** Saturn 8th from Natal Jupiter -- Elite Career Break (Nadi Rule)
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Transiting Saturn enters the sign that is 8th from the native's Natal Jupiter)
**Result:** Individual Performance Alert: 'Sudden and sustained poor form or career break for the elite native. The 8th house from Jupiter is the zone of maximum Jupiterian obstruction -- expansion is blocked, luck withdraws, and performance collapses despite apparent talent'. Validation: Sourav Ganguly 2006 -- S...
**PHR Reason:** Saturn 8th from Jupiter is a recognized obstruction principle, but the rule conflates nadi (timing) with career outcome without specifying Dasha/Bhukti context; Sourav Ganguly's 2006 exit requires birth time verification and Dasha confirmation.

#### `mundane-gopal-ch14-regional-direction-leadership`
**Title:** Malefic Transit in Directional Sign -- Regional Incumbency Failure
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Malefic planet -- Mars, Saturn, or Rahu -- transits a sign strongly associated with a geographic direction) AND (That malefic is afflicted or in close proximity to Earth)
**Result:** Regional Stability Alert: 'High probability of incumbency failure for leaders in the geographic direction associated with that sign/planet. Apply directional mapping: Sun→East, Venus→South-East, Mars→South, Saturn→West, Moon→North-West, Mercury→North'.
**PHR Reason:** The directional mapping (Sun→East, Venus→SE, Mars→South, Saturn→West, Moon→NW, Mercury→North) is non-standard in classical Vedic mundane astrology; 'proximity to Earth' is undefined; the condition lacks coherence.

#### `mundane-gopal-ch14-saturn-3rd-it-backbone`
**Title:** Saturn in 3rd from National Lagna -- IT/BPO National Backbone
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Saturn transits the 3rd house from the National Independence Chart Lagna)
**Result:** Contrarian IT Alert: 'Ignore media skepticism about BPO collapse. India becomes and remains the global backbone for information technology and back-office processing during this transit. BPO recruitment will treble. Internet penetration surges. IT/software exports reach record highs'. Validation: 20...
**PHR Reason:** Saturn in 3rd house typically indicates contraction, delay, and obstruction--not expansion of IT/BPO sectors; the result contradicts Saturn's classical malefic nature in the 3rd; validation conflates correlation with causation.

#### `mundane-gopal-ch14-saturn-kataka-bloodshed`
**Title:** Saturn in Cancer -- 3-Year Window of Conflict and Assassinations
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Saturn transits Kataka/Cancer) AND (Nation is in 6th or 8th lord Dasha)
**Result:** Conflict Escalation Alert: '3-year window of intensified hostilities, high-profile assassinations, and leadership-level casualties for nations with Cancer prominently placed in their Foundation Chart or Varsha chart'. Validation: Sri Lanka civil war escalated sharply during Saturn-in-Cancer transit.
**PHR Reason:** Saturn in Cancer + 6th/8th lord Dasha is a recognized conflict indicator, but the rule requires explicit Dasha/Bhukti timing and Foundation Chart placement verification; Sri Lanka validation needs precise chart and Dasha dates.

#### `mundane-gopal-ch14-saturn-ketu-leo-oil`
**Title:** Saturn-Ketu Conjunction in Leo -- Oil Price Spike
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Saturn and Ketu are conjunct in Leo/Simha)
**Result:** Commodity Alert: 'Oil prices likely to touch $70+/barrel due to proxy war pressures and energy sector disruptions. Simultaneously: gold prices peak, then correct, then establish new highs'. Validation: 2006 oil price spike to $70/barrel confirmed.
**PHR Reason:** Saturn-Ketu conjunction in Leo is a recognized malefic combination, but the specific $70/barrel oil price prediction and gold price pattern are overly precise without Dasha/transit context; 2006 validation is post-hoc.

#### `mundane-gopal-ch14-saturn-leo-real-estate`
**Title:** Saturn Enters Leo -- 100% Real Estate Growth Phase
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Saturn transits Simha/Leo)
**Result:** Real Estate Alert: 'Property prices and builder stocks will achieve 100% value gains during this transit. Middle-class obsession with home ownership peaks -- record mortgage demand despite rising interest rates. Engineering, construction, and builder stocks enter explosive growth phase'. Validation: ...
**PHR Reason:** Saturn in Leo (contraction, delay) predicting 100% property gains contradicts Saturn's classical nature; the result is internally incoherent with Saturn's malefic significations.

#### `mundane-gopal-ch14-saturn-pushya-bull-run`
**Title:** Saturn in Pushya Nakshatra -- Exceptional Stock Market Bull Run
**Source:** Gopalakrishnan Ch 14 -- Hits of 2006 Validation Audit
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Saturn transits Pushya Nakshatra, within Cancer/Kataka) AND (Nation in Raja Yoga Dasha/Bhukti -- Rahu/Mercury/Venus for India)
**Result:** Exceptional Bull Run: 'Expect 50-100% growth in national stock index values. Sector winners: Banking, FMCG, IT, and Telecom. Validation: 2006 India -- Sensex moved from 6,000 to 10,000+ (peak 12,000+)'. Ignore media correction warnings during this transit -- the bull run will persist.
**PHR Reason:** Saturn in Pushya (Cancer) is a restrictive transit; predicting 50-100% stock index growth contradicts Saturn's contraction principle; the rule lacks Dasha/Bhukti specificity and conflates planetary position with market direction.

#### `mundane-gopal-ch3-rasi-sandhi-spoiler`
**Title:** Rasi Sandhi 10th Lord -- Automatic Election Spoiler
**Source:** Gopalakrishnan Ch 3 -- Celebrity Horoscope Analysis
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (10th lord is in Rasi Sandhi: 0° or 29° of any sign) -- even if the candidate appears strong in polls or media analysis
**Result:** Margin Warning: 'Significant risk of losing a close race due to technicalities, sudden vote-splits, or administrative disqualification. Rasi Sandhi acts as an automatic Spoiler -- nullifying apparent strength'.
**PHR Reason:** Rasi Sandhi (0° or 29°) as a spoiler for 10th lord is a recognized principle, but the rule lacks specificity on orb tolerance and does not distinguish between sign boundaries; validation example needed.

#### `mundane-gopal-ch3-trikona-trikona-billionaire`
**Title:** Trikona-Trikona Raja Yoga -- Billionaire-Level Wealth
**Source:** Gopalakrishnan Ch 3 -- Celebrity Horoscope Analysis
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Two Trikona lords -- lords of 1st, 5th, and 9th houses -- combine in a Trikona house)
**Result:** Wealth Forecast: 'Native will achieve wealth at unheard-of levels -- Billionaire calibre. The high-order Trikona-Trikona Raja Yoga is the most powerful wealth combination in Vedic astrology'. Validation: Bill Gates -- 5th and 9th lords combined in 5th house.
**PHR Reason:** Trikona-Trikona Raja Yoga (two Trikona lords in a Trikona house) is a recognized wealth combination, but the rule overstates certainty ('billionaire calibre') without Dasha/transit context; Bill Gates validation requires chart verification.

#### `mundane-gopal-ch3-triple-check-pass`
**Title:** Celebrity Triple Check Pass -- Leadership Coefficient Established
**Source:** Gopalakrishnan Ch 3 -- Celebrity Horoscope Analysis
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (10th lord is strong from all 3 reference points: Lagna, Chandra Lagna, and Karkamsha Lagna)
**Result:** Destiny Alert: 'Native is mathematically marked for global greatness and pinnacle career success'. Leadership Coefficient set to 1.0. Proceed with full governance analysis.
**PHR Reason:** The rule assigns Leadership Coefficient = 1.0 based solely on 10th lord strength across three Lagnas; this oversimplifies destiny prediction and lacks Dasha/transit integration.

#### `mundane-gopal-ch3-widow-pm-multiplier`
**Title:** Widow/Unmarried Candidate -- Indian PM Longevity Multiplier
**Source:** Gopalakrishnan Ch 3 -- Celebrity Horoscope Analysis
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF (Saturn is the 10th lord in candidate's chart) AND (candidate is unmarried or widowed) AND (Query context is Indian Prime Minister seat)
**Result:** Longevity Bonus: +0.2 weight multiplier applied to this candidate's 'Duration of Government' forecast. Historical basis: Nehru, Indira Gandhi, Vajpayee, Modi -- all unmarried/widowed or ascetic by nature, all held PM seat for extended durations.
**PHR Reason:** The rule conflates marital status with astrological strength and applies a +0.2 multiplier without classical Vedic basis; the historical examples (Nehru, Indira Gandhi, Vajpayee, Modi) do not form a coherent astrological pattern.

## v18 -- Gopal Ch5 (oath chart) + Mehta Ch18 (election lagna)

#### `mundane-gopal-ch5-hora-lagna-fixed-veto`
**Title:** Hora Lagna Double-Fixed Veto -- Terminal Governance Signal
**Source:** Gopal Ch 5 -- Oath Taking Charts
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Lagna of oath chart is in a Fixed sign (Taurus/Leo/Scorpio/Aquarius) AND Hora Lagna of oath chart is also in a Fixed sign → Hora Lagna Double-Fixed Veto triggered
**Result:** Survival Probability coefficient = 0.10 (terminal). This is the most dangerous configuration in oath chart analysis -- the rigidity of both Lagna and Hora Lagna in Fixed signs signals near-certain premature collapse regardless of parliamentary majority. No amount of beneficial planetary support can o...
**PHR Reason:** The claim that double-fixed Lagna and Hora Lagna produces a 0.10 survival coefficient is extremely severe and lacks explicit source validation; the rule is internally coherent but the severity claim is not grounded in cited classical texts.

#### `mundane-gopal-ch5-jaimini-long-tenure`
**Title:** Jaimini Ayurdaya: Long Tenure Gate -- Moving + Moving Sign Types
**Source:** Gopal Ch 5 -- Oath Taking Charts
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Lagna Lord of oath chart is in a Moving/Chara sign (Aries/Cancer/Libra/Capricorn) AND 8th Lord of oath chart is in a Moving/Chara sign → Jaimini Ayurdaya classification = Long Life
**Result:** Government has HIGH probability of completing its full mandate. Administration projects energy and adaptability. Long governance tenure indicated. Prognosis: administration likely goes the full term without premature collapse.
**PHR Reason:** Contradicts: mundane-gopal-ch5-hora-lagna-fixed-veto, mundane-gopal-ch5-jaimini-short-tenure

#### `mundane-gopal-ch5-jaimini-short-tenure`
**Title:** Jaimini Ayurdaya: Short Tenure Gate -- Fixed + Fixed Sign Types
**Source:** Gopal Ch 5 -- Oath Taking Charts
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Lagna Lord of oath chart is in a Fixed/Sthira sign (Taurus/Leo/Scorpio/Aquarius) AND 8th Lord of oath chart is in a Fixed/Sthira sign → Jaimini Ayurdaya classification = Short Life
**Result:** Government has HIGH RISK of premature fall, collapse of coalition, or forced early exit before the full mandate is completed. Fixed-sign rigidity in the 8th house signals functional longevity problems. Prognosis: government unlikely to reach full term. Validate against Vajpayee 1996 (13-day governme...
**PHR Reason:** Contradicts: mundane-gopal-ch5-jaimini-long-tenure

#### `mundane-gopal-ch5-rasi-sandhi-veto`
**Title:** Rasi Sandhi Coefficient -- Effective Governance Collapse
**Source:** Gopal Ch 5 -- Oath Taking Charts
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF 4 or more planets in the oath chart are placed at 0° or 29° of their sign (Rasi Sandhi -- sign cusp / junction point) → Rasi Sandhi veto triggered
**Result:** Effective Governance coefficient = 0.20. Planets at Rasi Sandhi are in a 'between worlds' state -- they cannot express their natural significations reliably. An oath chart with 4+ planets at the cusp becomes structurally incapable of coherent governance. Administration will be marked by policy paraly...
**PHR Reason:** The threshold of 4+ planets at Rasi Sandhi and the 0.20 governance coefficient are specific but lack explicit source citation; the logic (between-worlds weakness) is sound but the quantitative threshold may be arbitrary.

#### `mundane-mehta-ch18-8th-house-vacancy-rule`
**Title:** 8th House Vacancy Requirement -- Core Longevity Gate
**Source:** Mehta Ch 18 -- Importance of Muhurta in Oath Taking
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the 8th house of the Muhurta chart contains any planet at time of oath taking → 8th house vacancy rule violated
**Result:** The 8th house MUST be empty of all planets in the oath-taking Muhurta chart. Any planet in the 8th house at the moment of oath taking directly compromises the functional longevity of the administration. Malefics (Saturn/Mars/Rahu/Ketu) in the 8th = severe threat to government survival. Even benefics...
**PHR Reason:** The rule states the 8th house MUST be empty, but then contradicts itself by discussing malefics vs. benefics in the 8th; this internal contradiction makes the rule incoherent and unusable.

#### `mundane-mehta-ch18-aadhaar-dependency-governance`
**Title:** Moon in Aadhaar Nakshatra -- Foundation-Level Governance (Weakest)
**Source:** Mehta Ch 18 -- Simhasan Chakra (Panch Nadi)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Moon in the oath chart is in an Aadhaar-level nakshatra (Ashwini/Ashlesha/Magha/Jyeshtha/Moola/Revati -- governed by Ketu and Mercury) → Moon occupies the Aadhaar (foundation) position -- lowest authority level
**Result:** Aadhaar (foundation) represents the weakest position in the Panch Nadi hierarchy. The leader governs from the ground floor -- the administration lacks the elevated authority to project power effectively. Governance is reactive rather than proactive. The government will be perceived as unstable, inexp...
**PHR Reason:** The Panch Nadi hierarchy and Aadhaar position are classical Simhasan Chakra concepts, but the attribution of specific nakshatras to Aadhaar level and the governance implications lack explicit source validation.

#### `mundane-mehta-ch18-ashtakvarga-8th-lord-stronger`
**Title:** Ashtakvarga 8th Lord Stronger Than Lagna Lord -- Collapse Indicator
**Source:** Mehta Ch 18 -- Leadership Autopsy Database
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF in the oath chart the Ashtakvarga bindus (benefic points) of the 8th Lord exceed the Ashtakvarga bindus of the Lagna Lord → Ashtakvarga 8th-lord-stronger collapse indicator triggered
**Result:** When the 8th lord (obstruction, longevity challenge, hidden destruction) is stronger than the Lagna lord (administration's fundamental vitality) in the Ashtakvarga point count, the destructive force within the administration exceeds its constructive capacity. This is Mulayam Singh Yadav's 1993 patte...
**PHR Reason:** The Ashtakvarga bindu comparison between 8th lord and Lagna lord is a valid technique, but the specific Mulayam Singh Yadav case (1993) requires verification and the causal logic could be more explicitly grounded.

#### `mundane-mehta-ch18-cancer-leo-partner-discord`
**Title:** Cancer/Leo Lagna -- Coalition Partner Discord in Oath Charts
**Source:** Mehta Ch 18 -- Importance of Muhurta in Oath Taking
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Muhurta chart for oath taking has Cancer or Leo as Lagna AND Saturn or Mars aspects the Lagna or Lagna Lord
**Result:** Cancer and Leo Lagnas in oath charts produce discord with coalition partners. Cancer (Moon-ruled) creates over-sensitivity and dependency on external support; Leo (Sun-ruled) creates ego conflicts within the ruling alliance. When additionally afflicted by Saturn or Mars, the administration will be c...
**PHR Reason:** The rule attributes specific governance problems to Cancer/Leo Lagnas with Saturn/Mars aspects, but the causal logic (Cancer = over-sensitivity, Leo = ego) is interpretive and lacks explicit source citation.

#### `mundane-mehta-ch18-capricorn-lagna-exclusion`
**Title:** Capricorn Lagna Exclusion -- Mehta's Governance Anti-Pattern
**Source:** Mehta Ch 18 -- Importance of Muhurta in Oath Taking
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** IF Muhurta chart for oath taking has Capricorn as Lagna → Mehta's Capricorn governance anti-pattern triggered
**Result:** Capricorn Lagna is specifically identified by Mehta as unsuitable for democratic oath-taking ceremonies. Saturn's cold, slow, obstructive nature as Lagna ruler creates an administration that is bureaucratically paralysed, slow to execute, and perceived by the public as cold or out-of-touch. Leadersh...
**PHR Reason:** The rule cites Mehta's exclusion of Capricorn for oath-taking, but the characterization (bureaucratic paralysis, cold leadership) is interpretive; the rule is usable but the source attribution should be verified.

#### `mundane-mehta-ch18-enemy-lord-coalition`
**Title:** Enemy Lord Coalition Rule -- Hostile Alliance Signs Imminent Collapse
**Source:** Mehta Ch 18 -- Leadership Autopsy Database
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF in the oath chart the Lagna lord and the 7th lord (natural enemies by sign) are conjunct OR in mutual aspect (paap-kartari between them) AND the 10th lord is simultaneously weak → Enemy Lord Coalition rule triggered
**Result:** A government formed from a coalition of natural political enemies -- parties or leaders whose fundamental agendas are opposed -- cannot sustain itself. The Lagna lord (administration's identity) in conflict with the 7th lord (the opposition) while the 10th lord (executive authority) is weak indicates ...
**PHR Reason:** Result text is truncated mid-sentence ('Adm'); condition is sound but result needs completion and clarification on what 'paap-kartari between them' means in this context.

#### `mundane-mehta-ch18-many-bosses-constraint`
**Title:** Many Bosses Constraint -- Multi-Lord Oath Chart Configuration
**Source:** Mehta Ch 18 -- Leadership Autopsy Database
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the oath chart shows 3+ of the following simultaneously: (1) Lagna Lord in the sign or nakshatra of another planet (parivartana or dependency), (2) 10th Lord under aspect of 3+ other planets, (3) Sun (natural karaka of leadership) conjunct or aspected by 2+ planets, (4) Moon in Aasan-level naksha...
**Result:** Manmohan Singh 2004 (oath: 22 May 2004) -- 15 features including multiple indicators of constrained authority. Manmohan Singh governed effectively but was publicly acknowledged as operating under the authority of the Congress High Command (Sonia Gandhi). Pattern indicates: the nominal leader does not...
**PHR Reason:** Result text truncated ('The leader is an i'); condition is coherent but result needs completion. Also, 'Aasan-level nakshatra' terminology should be verified against source.

#### `mundane-mehta-ch18-nakshatra-tithi-veto-combo`
**Title:** Rikta Tithi + Malefic Nakshatra Combo -- Double Muhurta Veto
**Source:** Mehta Ch 18 -- Importance of Muhurta in Oath Taking
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the oath is taken on a Rikta Tithi (4th/9th/14th lunar day) AND the Moon is in a malefic nakshatra (Ashlesha/Jyeshtha/Moola/Magha/Mrigshira/Ardra) → Double Muhurta veto triggered
**Result:** Rikta (empty/void) Tithis combined with a malefic Moon nakshatra create a double-veto in Muhurta analysis. Rikta Tithis signify emptiness and lack of fructification -- plans do not reach completion. Malefic Moon nakshatra adds emotional instability, public antipathy, and adversarial media coverage to...
**PHR Reason:** Result text truncated ('will fail to materialis'); Rikta Tithi definition (4th/9th/14th) is standard but the malefic nakshatra list (Ashlesha/Jyeshtha/Moola/Magha/Mrigshira/Ardra) needs verification--Magha and Mrigshira are not universally classified as malefic.

#### `mundane-mehta-ch18-narasimha-rao-liberalisation-dhana`
**Title:** Narasimha Rao 1991 -- Liberalisation Dhana Yoga Pattern
**Source:** Mehta Ch 18 -- Leadership Autopsy Database
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF oath chart shows 5+ of the following positive features: (1) Lagna Lord in Kendra or Trikona with no severe affliction, (2) 2nd and 11th lords connected by aspect or conjunction (Dhana Yoga), (3) Jupiter in angle or trine, (4) Moon waxing (Shukla Paksha) at time of oath, (5) 10th lord strong and u...
**Result:** P.V. Narasimha Rao (oath: 21 June 1991) -- 7 positive features including strong Dhana Yoga. His administration oversaw India's 1991 economic liberalisation (the most transformative economic shift in post-independence India). Pattern indicates: administration will preside over significant economic exp...
**PHR Reason:** Result text truncated ('The Dhana Yoga link between 2nd and'); condition is coherent and Dhana Yoga (2nd-11th connection) is classical, but result needs completion.

#### `mundane-mehta-ch18-raman-democratic-lagnas`
**Title:** Raman Democratic Lagna Rule -- Aquarius and Libra for Oath Taking
**Source:** Mehta Ch 18 -- Importance of Muhurta in Oath Taking
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Muhurta chart for oath taking has Aquarius or Libra as Lagna → Raman's preferred democratic governance Lagnas
**Result:** Aquarius (Saturn-ruled, democratic, people-oriented) and Libra (Venus-ruled, justice, balance) are B.V. Raman's recommended Lagnas for democratic oath-taking ceremonies. Both signs project an image of governance for the masses. Aquarius particularly favours long-term constitutional stability. Libra ...
**PHR Reason:** Result text truncated ('when free of afflict'); attribution to B.V. Raman is plausible but should be verified against his published works on Muhurta. Aquarius and Libra as democratic Lagnas is coherent.

#### `mundane-mehta-ch18-sandhi-bharani-lethality`
**Title:** Sandhi-Bharani Lethality Rule -- Bharani at Sign Junction = Maximum Death Signal
**Source:** Mehta Ch 18 -- Leadership Autopsy Database
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the Moon in the oath chart is in Bharani nakshatra (ruled by Venus, nakshatra of Yama/death) AND is simultaneously at a Rasi Sandhi (0° or 29° of a sign) -- placing it at the most vulnerable junction point → Sandhi-Bharani lethality configuration triggered
**Result:** Bharani is the nakshatra of Yama (god of death) -- it governs endings, transition, and irreversible finality. When placed at a Rasi Sandhi, the death-oriented quality of Bharani is amplified to its maximum. In an oath chart: the administration's end will be sudden, final, and marked by events of irre...
**PHR Reason:** Bharani is ruled by Venus, not Yama directly; Yama is associated with the 8th house and Saturn. The claim that Bharani is 'the nakshatra of Yama' is not standard Vedic astrology doctrine. The rule conflates mythological association with astrological function.

#### `mundane-mehta-ch18-shastri-terminal-leadership`
**Title:** Shastri 1964 Pattern -- Terminal Leadership (Death in Office)
**Source:** Mehta Ch 18 -- Leadership Autopsy Database
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF oath chart shows 5+ of the following adverse features simultaneously: (1) Lagna Lord in 8th house, (2) 8th Lord in Lagna or aspecting Lagna, (3) Saturn in the 1st or 8th house, (4) Moon in a Kendra (1/4/7/10) and afflicted by malefics, (5) Jupiter (karaka for life) debilitated or combust, (6) 5th...
**Result:** Lal Bahadur Shastri (oath: 9 June 1964) -- 9 adverse features present in his oath chart. He died in office on 11 January 1966 in Tashkent under mysterious circumstances just after signing the Tashkent Declaration. Pattern indicates: administration ends with the leader's death in office, not through e...
**PHR Reason:** Result text truncated ('greater the'); condition is coherent and Shastri's death in office is historical fact, but the rule mixes Jaimini Ayurdaya (personal longevity) with oath chart analysis (government longevity) without clear justification.

#### `mundane-mehta-ch18-simha-moon-rahu-dasha`
**Title:** Moon in Simha Nakshatra + Rahu Dasha -- Shadow Authority Pattern
**Source:** Mehta Ch 18 -- Simhasan Chakra (Panch Nadi)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Moon in the oath chart is in a Simha-level nakshatra (Rohini/Aridra/Hasta/Swati/Shravana/Shatbhisha -- governed by Moon and Rahu) AND the Dasha lord at oath time is Rahu → Simha-Rahu shadow authority configuration
**Result:** Simha (lion, seat of lions) is the second tier in the Panch Nadi hierarchy, just below the throne. When Rahu (the shadow) is also the Dasha lord, the Simhasan Chakra affinity rule (Dasha lord matching the Nadi level lord) fires: the administration operates with significant behind-the-scenes power bu...
**PHR Reason:** Nakshatras listed (Rohini/Aridra/Hasta/Swati/Shravana/Shatbhisha) are not all Moon and Rahu governed; Rohini is Moon, Hasta is Moon, Shravana is Moon, but Ardra is Rahu, Swati is Rahu, Shatbhisha is Rahu. The grouping is correct but the phrasing 'governed by Moon and Rahu' is ambiguous and potentially misleading.

#### `mundane-mehta-ch18-simhasan-aasan-saturn-terminal`
**Title:** Moon in Aasan Nakshatra -- Dependency Governance (Terminal if Saturn)
**Source:** Mehta Ch 18 -- Simhasan Chakra (Panch Nadi)
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Moon in the oath chart is in an Aasan-level nakshatra (Bharani/Pushya/P.Phalguni/Anuradha/P.Ashadha/U.Bhadrapada -- governed by Venus and Saturn) AND the Dasha lord at oath time is Saturn → Aasan-Saturn terminal configuration
**Result:** Moon in Aasan indicates the leader governs from a 'supported chair' -- dependent on coalition partners, allies, or a High Command for survival. When the Dasha lord is also Saturn (which governs half of the Aasan nakshatras): the dependency becomes acute and terminal -- the administration is entirely a...
**PHR Reason:** Result text truncated ('leader has n'); Aasan nakshatras listed (Bharani/Pushya/P.Phalguni/Anuradha/P.Ashadha/U.Bhadrapada) are Venus and Saturn governed, which is correct. However, the Simhasan Chakra (Panch Nadi) framework attribution to Mehta needs verification.

#### `mundane-mehta-ch18-simhasan-jupiter-protection`
**Title:** Moon in Patta Nakshatra -- Constitutional Protection and Judicial Shield
**Source:** Mehta Ch 18 -- Simhasan Chakra (Panch Nadi)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Moon in the oath chart is in a Patta-level nakshatra (Krittika/Punarvasu/U.Phalguni/Vishakha/U.Ashadha/P.Bhadrapada -- governed by Sun and Jupiter) → Moon occupies the Patta (canopy/umbrella) position in the Panch Nadi grid
**Result:** The leader is sheltered under the protective umbrella of constitutional and judicial authority. Sun/Jupiter's governance of this level indicates: strong Rajya Sabha support, legal victories when challenged, Supreme Court rulings in the government's favour, and the ability to withstand no-confidence ...
**PHR Reason:** Patta nakshatras listed (Krittika/Punarvasu/U.Phalguni/Vishakha/U.Ashadha/P.Bhadrapada) are Sun and Jupiter governed, which is correct. However, the Panch Nadi framework attribution and the specific outcomes (Rajya Sabha support, Supreme Court rulings) need source verification.

#### `mundane-mehta-ch18-simhasan-martial-king`
**Title:** Moon in Simhasan + Mars Dasha Lord -- Martial King Pattern
**Source:** Mehta Ch 18 -- Simhasan Chakra (Panch Nadi)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Moon in the oath chart is in a Simhasan nakshatra (Mrigshira/Chitra/Dhanishtha) AND the Dasha lord at the time of oath taking is Mars → Moon-Simhasan + Mars Dasha affinity confirmed (both Mars-governed)
**Result:** The Martial King Pattern: Simhasan nakshatras are Mars-governed, and when the Dasha lord is also Mars, the Simhasan Chakra affinity rule produces a doubled martial signal. Administration will be characterised by: decisive executive action, willingness to use state force when challenged, strong borde...
**PHR Reason:** Simhasan nakshatras are listed as Mrigshira/Chitra/Dhanishtha, but Mrigshira is Rahu-governed, Chitra is Mars-governed, and Dhanishtha is Mars-governed. The claim that all three are 'Mars-governed' is factually incorrect.

#### `mundane-mehta-ch18-simhasan-moon-absolute-power`
**Title:** Moon in Simhasan Nakshatra -- Absolute Political Authority
**Source:** Mehta Ch 18 -- Simhasan Chakra (Panch Nadi)
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Moon in the oath chart is in a Simhasan-level nakshatra (Mrigshira/Chitra/Dhanishtha -- the throne-level nakshatras governed by Mars) → Moon occupies the Simhasan (throne) position in the Panch Nadi grid
**Result:** The leader sits on the metaphorical throne -- occupying a position of absolute political authority and dominance. Administration projects unquestioned command. The leader's will is the government's direction. No effective political opposition can challenge the ruling position during this administrati...
**PHR Reason:** Simhasan nakshatras listed as Mrigshira/Chitra/Dhanishtha with claim all are 'Mars-governed' is factually incorrect (Mrigshira is Rahu). The rule also claims Moon placement 'overrides standard house analysis' which contradicts foundational Vedic astrology principles.

#### `mundane-mehta-ch18-vajpayee-balarishta-pattern`
**Title:** Vajpayee 1996 -- 13-Day Balarishta Government Pattern
**Source:** Mehta Ch 18 -- Leadership Autopsy Database
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF oath chart shows ALL of the following simultaneously: (1) Jaimini Ayurdaya = Short Life (Fixed + Fixed sign types for Lagna/8th lords), (2) 10th lord weak (debilitated, combust, or in 6th/8th/12th), (3) Lagna lord not aspecting Lagna, (4) Moon afflicted by 2+ malefics simultaneously, (5) No major...
**Result:** Atal Bihari Vajpayee (oath: 16 May 1996) -- 8 adverse features, including Jaimini Short Life configuration. Government lasted only 13 days before a floor test defeat. This is the fastest government collapse in Indian history. Pattern indicates: government will not last more than a few weeks. The term...
**PHR Reason:** Result text truncated ('administration'); Jaimini Ayurdaya application to oath charts (government longevity) rather than natal charts (personal longevity) is non-standard and needs source justification. The 13-day tenure is historically accurate.

## v19 -- Gopal Ch4 (election engine) + Mehta Ch22/23 (cabinet)

#### `mundane-gopal-ch4-destiny-anchor-karkamsha`
**Title:** Destiny Anchor -- Karkamsha 10th Lord + Trikona Lord = Marked for High Office
**Source:** Gopal Ch 4 -- How to Predict for Elections
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the 10th lord in the Karkamsha Lagna chart is conjunct or aspected by a Trikona lord (1st/5th/9th house lords) in the Karkamsha Lagna → Destiny Anchor triggered -- candidate is marked by fate for high office
**Result:** Destiny Alert: This candidate has a soul-level mandate for high political office. The Karkamsha represents the deepest destiny blueprint of the individual. A Trikona connection to the 10th lord here indicates that leadership is fated -- the divine mandate for governance is present regardless of immed...
**PHR Reason:** Karkamsha Lagna with 10th lord + Trikona lord conjunction is a recognized destiny indicator, but the rule assigns +0.30 weight modifier without Dasha/transit context; 'soul-level mandate' is metaphorical rather than astrologically precise.

#### `mundane-gopal-ch4-eighth-saturn-sudden-reversal`
**Title:** 8th House Saturn -- Sudden Unexpected Electoral Reversal
**Source:** Gopal Ch 4 -- How to Predict for Elections
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Saturn is natally placed in the 8th house of a candidate's chart OR Saturn is transiting the 8th house from the candidate's natal Lagna or Moon at the time of the election cycle → 8th house Saturn sudden-reversal signal triggered
**Result:** Indicates a sudden, unexpected reversal of electoral fortune. The fall arrives from an entirely unanticipated direction -- NOT from the visible political opponent or from standard electoral arithmetic. Can manifest as: health crisis, sudden scandal, forced withdrawal from candidacy, or an unforeseen ...
**PHR Reason:** Saturn in 8th house as a sudden-reversal signal is recognized, but the rule lacks Dasha/Bhukti specificity and does not distinguish between natal and transit Saturn; validation example (Vajpayee 2004) is incomplete.

#### `mundane-gopal-ch4-eleventh-house-dasha-surge`
**Title:** 11th House Dasha Surge -- Winning Momentum Coefficient 0.90
**Source:** Gopal Ch 4 -- How to Predict for Elections
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the candidate's active Dasha or Bhukti lord at the time of polling is placed in the 11th house (Labha/Gains) from the Lagna OR from the Moon → 11th House Dasha Surge winning momentum triggered
**Result:** Winning Momentum coefficient = 0.90. The 11th house is the house of gains, fulfillment of desires, and electoral victory. A Dasha/Bhukti whose period lord occupies the 11th house from either key Lagna provides the decisive timing push for electoral victory. This is the single most reliable Dasha-lev...
**PHR Reason:** 11th house Dasha/Bhukti lord as a winning indicator is recognized, but assigning Winning Momentum = 0.90 is overly precise without considering opposing transits or 8th/12th house factors; Bush 2000 validation is incomplete.

#### `mundane-gopal-ch4-incumbent-vulnerability-trigger`
**Title:** Incumbent Vulnerability -- 8th Lord Dasha + 10th Lord in 3rd = Regime Shift
**Source:** Gopal Ch 4 -- How to Predict for Elections
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the incumbent candidate/government is running a Dasha of the 8th lord (obstruction / hidden transformation period) AND the 10th lord (executive authority) is placed in the 3rd house (effort / valour -- fighting without structural executive backing) → Incumbent Vulnerability trigger fired
**Result:** Incumbency Warning: High risk of the incumbent being voted out by an emerging new political force or 'star' in the opposition. The 8th lord Dasha signals hidden upheaval approaching from beneath. The 10th lord in 3rd means the incumbent is fighting hard but lacks the structural elevation of a 10th-h...
**PHR Reason:** 8th lord Dasha + 10th lord in 3rd house as an incumbency vulnerability is coherent, but the rule lacks Dasha/Bhukti specificity and does not account for opposing candidate's chart strength; validation example is incomplete.

#### `mundane-gopal-ch4-indian-pm-lagna-bias`
**Title:** Indian PM Lagna Bias -- Cancer/Taurus/Scorpio/Leo Historical Pattern
**Source:** Gopal Ch 4 -- How to Predict for Elections
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** IF predicting the Indian national PM election AND a candidate has Lagna in Cancer, Taurus, Scorpio, or Leo → Indian PM Lagna Bias modifier applied
**Result:** Historical pattern: most successful Indian PMs with full terms and significant governance legacies have had Cancer, Taurus, Scorpio, or Leo as their Lagna. Apply +0.1 weight modifier to the overall Tri-Lagna strength coefficient for Indian national elections only. This is a contextual modifier, not ...
**PHR Reason:** The rule claims a historical pattern for Indian PMs with specific Lagnas but lacks citation of specific cases and the +0.1 modifier is arbitrary without source validation from Gopalakrishnan's text.

#### `mundane-gopal-ch4-indian-pm-widowhood-rule`
**Title:** Indian PM Widowhood Rule -- Saturn 10th Lord Favours Single/Widowed Candidates
**Source:** Gopal Ch 4 -- How to Predict for Elections
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** IF predicting the Indian national PM election AND Saturn is the candidate's 10th lord (from any Tri-Lagna reference point) AND the candidate is widowed, unmarried, or living apart from spouse → Indian PM Widowhood modifier applied
**Result:** Weight modifier: +0.2 to overall Tri-Lagna strength coefficient for this candidate in Indian PM contests specifically. Gopalakrishnan identifies that Saturn as 10th lord in Indian politics historically favours candidates without active marital partnerships. Saturn demands sacrifice of personal/domes...
**PHR Reason:** The rule conflates Saturn as 10th lord with marital status in a way that is not standard Vedic astrology doctrine; the +0.2 modifier lacks textual grounding and the causal logic (Saturn demands sacrifice) is interpretive rather than classical.

#### `mundane-gopal-ch4-sonia-dramatic-change-trigger`
**Title:** Sonia Gandhi Dramatic Change Trigger -- Saturn in Cancer + Cancer Lagna
**Source:** Gopal Ch 4 -- How to Predict for Elections
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Saturn is transiting Cancer AND the election frontrunner or incoming leader has Cancer as their natal Lagna → Sonia Gandhi Dramatic Change Alert triggered
**Result:** Dramatic Change Alert: The most powerful political office will see a dramatic transition before Saturn completes its transit through Cancer. This pattern -- Saturn in Cancer + Cancer-Lagna candidate -- signals a major regime shift that overturns pre-election expectations. Validated: 2004 Indian Genera...
**PHR Reason:** The rule cites the 2004 Indian election as validation, but the causal mechanism (Saturn in Cancer + Cancer Lagna candidate = regime shift) is overly specific and the rule may be retrofitted to a single historical case rather than a generalizable principle.

#### `mundane-gopal-ch4-volatile-nomination-chart`
**Title:** Volatile Nomination Chart -- 2+ Rasi Sandhi Planets = Candidacy Collapse Risk
**Source:** Gopal Ch 4 -- How to Predict for Elections
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the nomination filing time chart (the moment a candidate files their nomination papers) has 2 or more planets at 0° or 29° of any sign (Rasi Sandhi) → Volatile Nomination Chart flag triggered
**Result:** Volatile: This candidacy is prone to sudden collapse or technical disqualification. The nomination chart acts as the 'birth chart' of the individual candidate's electoral quest. With 2+ planets at Rasi Sandhi (between worlds), the campaign lacks structural grounding. Risk manifestations: nomination ...
**PHR Reason:** The nomination chart as a 'birth chart' for candidacy is a reasonable extension of Vedic principles, but the threshold of 2+ planets at Rasi Sandhi and the specific risk manifestations lack explicit source citation.

#### `mundane-mehta-ch22-anarchy-gate-sun-raja-saturn-mantri`
**Title:** Anarchy Gate -- Sun Raja + Saturn Mantri = High-Level Leadership Mortality
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Raja (King) for the year is Sun AND Mantri (Minister) for the year is Saturn → Anarchy Gate triggered
**Result:** Systemic Instability Warning: Cruel administrative behavior and high-level leader mortality predicted for this year. The Sun-Saturn combination at the Raja-Mantri level is the most dangerous executive configuration in the annual cabinet system. Sun represents the head of state; Saturn represents obs...
**PHR Reason:** Result text truncated ('i'); Sun-Saturn as Raja-Mantri is plausible as an adverse combination, but the specific claim of 'high-level leader mortality' needs source verification from Mehta Ch 22.

#### `mundane-mehta-ch22-combustion-veto-reversal`
**Title:** Combustion Veto -- Combust or Grahayudha-Lost Raja Reverses All Benefic Results
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the Raja (King) planet for the year is combust (within 8° of Sun for planets other than Sun itself) OR loses in Grahayudha (Planetary War -- within 1° of another planet, the losing planet has a lower degree) in the Hindu New Year chart → Combustion Veto triggered
**Result:** All beneficial results for this planet's Raja year are REVERSED to their calamitous opposites. Jupiter combust as Raja → banking failures instead of banking prosperity. Venus combust as Raja → luxury inflation instead of abundance. Mercury combust as Raja → media chaos and misinformation instead of ...
**PHR Reason:** Combustion definition (8° for non-Sun planets) is standard. The reversal principle is coherent, but the specific examples (Jupiter combust → banking failures) need verification against Mehta's actual text.

#### `mundane-mehta-ch22-golden-year-jupiter-venus`
**Title:** Jupiter Raja + Venus Mantri -- Golden Year National Prosperity
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Raja (King) for the year is Jupiter AND Mantri (Minister) for the year is Venus AND Jupiter is unafflicted in the Hindu New Year chart → Golden Year compound signal triggered
**Result:** Golden Year Forecast: Exceptional national wealth, bumper agricultural output, and societal peace predicted for the year. Jupiter-Venus is the most auspicious Raja-Mantri pairing in the Celestial Cabinet. Jupiter (prosperity, justice, religion) governs the year's destiny; Venus (abundance, culture, ...
**PHR Reason:** Contradicts: mundane-mehta-ch22-combustion-veto-reversal

#### `mundane-mehta-ch22-jupiter-raja-afflicted-banking-crisis`
**Title:** Afflicted Jupiter Raja -- Banking Crisis / Institutional Collapse Warning
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Jupiter is the Raja (King) for the year AND Jupiter is afflicted (combust / debilitated / losing in Grahayudha / aspected by Saturn or Mars without benefic protection) in the Hindu New Year chart → Afflicted Jupiter Raja veto triggered
**Result:** Fiscal Stability Warning: High probability of a banking crisis or collapse of a major financial institution during this year. Jupiter governs banks, judges, and the treasury in mundane analysis. When afflicted as the Raja, all beneficial Jupiter outcomes reverse: prosperity becomes financial distres...
**PHR Reason:** Contradicts: mundane-mehta-ch22-jupiter-raja-golden-year

#### `mundane-mehta-ch22-jupiter-raja-golden-year`
**Title:** Jupiter as Raja -- Golden Year (Prosperity / Banking / Legal Welfare)
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Mars is the Raja for the year (unafflicted, not combust, not in Grahayudha) → Jupiter prosperity activation IF Jupiter is also unafflicted in the Hindu New Year chart
**Result:** Golden Year declared for banking, agriculture, and national prosperity. Classical outcomes: excellent crops, religious rituals, universal prosperity, abundant milk and honey, legal welfare, effective judiciary. Modern calibration: Banking and financial systems strengthen; Jupiter is the Karaka for b...
**PHR Reason:** Condition states 'IF Mars is the Raja' but result discusses Jupiter prosperity; this is internally contradictory. The rule should either be Mars Raja or Jupiter Raja, not both.

#### `mundane-mehta-ch22-mars-raja-year-of-sword`
**Title:** Mars as Raja -- Year of the Sword (War / Fire / Terrorism)
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the weekday lord at Chaitra Shukla Pratipada (Hindu New Year) is Mars → Mars is the Raja (King) for the year OR IF the weekday lord at Solar Ingress into Aries is Mars → Mars is the Mantri (Minister) for the year
**Result:** Year of the Sword declared. Classical outcomes: fighting between rulers, forest and urban fires, robberies, widespread bilious diseases, military aggression elevated. Modern calibration: significant global terrorism incidents, property destruction by fire, military confrontations, and armed conflict...
**PHR Reason:** Rule is logically sound and well-grounded in classical Mars symbolism, but the result text is truncated mid-sentence ('gold and'), making it impossible to verify completeness and coherence of the full outcome statement.

#### `mundane-mehta-ch22-mercury-dhanesh-it-boom`
**Title:** Mercury as Dhanesh -- IT, BPO, and Publishing Sector Boom
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Mercury is the Dhanesh (Lord of Treasury/Commerce, appointed at Sun's entry into Virgo) AND Mercury is unafflicted in the Dhanesh appointment chart → Mercury Dhanesh IT boom signal triggered
**Result:** Information Technology and Publishing Sector Boom declared for this year. Classical Dhanesh-Mercury outcomes: farmers earn well, business rituals observed, financial markets stable. Modern 21st-century calibration (Mehta modernization override): Mercury as treasury lord maps to IT, BPO, communicatio...
**PHR Reason:** The modernization of Mercury Dhanesh to IT/BPO sectors is plausible but represents a significant departure from classical Dhanesh doctrine; the result text is truncated ('annual cyc'), preventing full assessment of coherence and validation examples.

#### `mundane-mehta-ch22-raja-mantri-enemy-deadlock`
**Title:** Raja-Mantri Enemy Pair -- Administrative Policy Deadlock
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the Raja (King) and Mantri (Minister) for the year are natural planetary enemies (Sun-Saturn, Moon-Rahu, Mars-Mercury, Jupiter-Mercury adversarial pairing, or Venus-Jupiter tension pair) → Raja-Mantri enemy configuration triggered
**Result:** Administrative Alert: High probability of policy deadlock and cabinet bickering throughout the year. The executive (Raja) and the implementation layer (Mantri) are working against each other at a fundamental level. Governance appears active on the surface but produces little durable output. Key bill...
**PHR Reason:** The planetary enemy pairings listed (Sun-Saturn, Moon-Rahu, Mars-Mercury, Jupiter-Mercury, Venus-Jupiter) are not uniformly established as 'natural enemies' in classical Vedic astrology; Jupiter-Mercury and Venus-Jupiter are particularly questionable as adversarial pairs.

#### `mundane-mehta-ch22-saturn-dhanesh-treasury-depletion`
**Title:** Saturn as Dhanesh + Mars Aspect -- National Treasury Depletion
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Saturn is the Dhanesh (Lord of Treasury, appointed at Sun's entry into Virgo) AND Mars aspects Saturn in the New Year chart (or within the Dhanesh appointment chart) → Treasury Depletion alert triggered
**Result:** Fiscal Stability Warning: Paucity of national funds predicted for the year. Scholars, accountants, and financial sector workers suffer. Saturn as treasury lord already produces conservative, restricted, slow-moving national finances. Mars's aspect adds aggressive expenditure pressure -- specifically ...
**PHR Reason:** The condition specifies Mars aspect to Saturn in 'New Year chart (or within Dhanesh appointment chart)' -- this dual-chart reference is ambiguous and could create conflicting interpretations; result text is truncated ('reser').

#### `mundane-mehta-ch22-saturn-durgesh-defense-humiliation`
**Title:** Saturn as Durgesh in 12th -- National Defense Humiliation / Territorial Loss
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Saturn is the Durgesh (Lord of Defense, appointed at Sun's entry into Leo) AND Saturn is placed in the 12th house of the Hindu New Year chart → Defense Vulnerability critical alert triggered
**Result:** Critical Defense Alert: Risk of national humiliation by enemies and potential loss of territorial integrity. Durgesh governs the national security apparatus -- army, navy, police, border security, and fortress defense. Saturn in the 12th house directs the defense portfolio toward 'loss, expenditure w...
**PHR Reason:** The rule is coherent and logically sound, but the assignment of Saturn in 12th house specifically to 'loss of territorial integrity' is a strong inference that would benefit from explicit classical or modern validation source citation.

#### `mundane-mehta-ch22-sun-raja-2001-validation`
**Title:** Sun as Raja -- Corruption Exposés / Fire Disaster / Institutional Failure
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Sun is the Raja (King) for the year → Sun governance tone year declared
**Result:** Mixed/hazardous year declared. Classical outcomes: mentally disturbed rulers, danger by fire and theft, unusual heat, scarce food, destructive wars, death of a senior leader. Modern calibration: high-level government corruption exposés, institutional/financial scheme collapses, major fire or heat di...
**PHR Reason:** The 2001 validation example cites Gujarat Earthquake and Tehelka (text truncated at 'Teh'), but the causal link between Sun Raja and these specific events requires stronger astrological justification; result text is incomplete.

#### `mundane-mehta-ch22-winter-prosperity-dhanyesh-meghesh`
**Title:** Jupiter Dhanyesh + Moon Meghesh -- Exceptional Winter Harvest and Rain
**Source:** Mehta Ch 22 -- Yearly Governance Engine
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Jupiter is the Dhanyesh (Lord of Winter Crops, appointed at Sun's entry into Sagittarius) AND Moon is the Meghesh (Lord of Rain/Clouds, appointed at Sun's entry into Ardra Nakshatra) AND both are unafflicted → Winter Prosperity compound signal triggered
**Result:** National Forecast: Exceptional winter harvest and abundant water resources predicted. Jupiter as Dhanyesh: wheat and rice plentiful, religious activities increase, winter grains freely available. Moon as Meghesh: copious and timely rain, social harmony, public amenities increase. Together: this is t...
**PHR Reason:** The compound signal (Jupiter Dhanyesh + Moon Meghesh both unafflicted) is logically coherent, but the claim that this is 'the strongest agricultural prosperity signal' is a superlative assertion that would require comparative validation against other prosperity configurations.

## v2n -- Gopal Ch2 + Mehta Ch6 + Raphael Ch3 (novel rules only)

#### `mundane-gopal-ch2-10th-lord-triage`
**Title:** Gopal Ch 2 -- 10th Lord Triage (Chart Authenticity Veto)
**Source:** Gopal Ch 2 -- How to Become a Very Good Mundane Astrologer
**Severity:** high | **Checkable:** False | **Weight:** 1.0
**Condition:** IF the 10th lord is NOT strong from at least 2 of [Lagna, Chandra Lagna, Karkamsha Lagna] THEN flag chart as 'Potentially Inauthentic -- verify birth data before analysis'; IF the 10th house is vacant AND unaspected THEN reinforce the flag regardless of other factors
**Result:** Chart flagged as 'Potentially Inauthentic' -- stop analysis and verify birth data. Apply as a mandatory first gate before any deep mundane analysis. Example: Advani chart with 10th lord weak in 12th → rejected as likely incorrect birth data.
**PHR Reason:** The three-Lagna strength test (Lagna, Chandra, Karkamsha) is sound Gopal methodology, but the 'at least 2 of 3' threshold and the vacant/unaspected 10th house veto lack explicit source citation; recommend verification against Gopal Ch 2 original text.

#### `mundane-gopal-ch2-election-comparative-audit`
**Title:** Gopal Ch 2 -- Election Winner Comparative Strength Audit
**Source:** Gopal Ch 2 -- Election Winner Logic
**Severity:** high | **Checkable:** False | **Weight:** 1.0
**Condition:** IF comparing two election candidates: Step 1 -- compare 10th lord strength from Lagna, Chandra Lagna, and Karkamsha for both candidates; Step 2 -- identify who is running a Raja Yoga Dasha period (Kendra/Trikona lord as Mahadasha or Antardasha lord); Step 3 -- veto any candidate currently running a 6th...
**Result:** Candidate with stronger 10th lord + active Raja Yoga Dasha + non-Dusthana period + favorable Lagna alignment wins. Any candidate failing Step 3 (active Dusthana Dasha) is near-certainly eliminated regardless of other chart strengths.
**PHR Reason:** The four-step logic is coherent and well-structured, but the 'India Alignment Lagna Filter' (Step 4) is introduced here without prior definition; cross-reference with mundane-gopal-ch2-india-lagna-filter rule to ensure consistency and verify Gopal source attribution.

#### `mundane-gopal-ch2-governance-longevity`
**Title:** Gopal Ch 2 -- Saturnine Longevity Rule for Indian PM
**Source:** Gopal Ch 2 -- Saturnine Power Gate
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** IF an Indian PM is unmarried or widowed AND Saturn is the 10th lord of India (Taurus Lagna chart) THEN long tenure predicted -- Saturn (asceticism, solitude) is naturally empowered by the leader's renunciation of domestic life; IF the Indian PM has a living spouse THEN shorter tenure predicted
**Result:** Long-tenure gate: Nehru (widower), Indira Gandhi (widow), Vajpayee (bachelor) all validated as long-tenure PMs under this rule. Short-tenure examples: Rajiv Gandhi, Lal Bahadur Shastri, V.P. Singh. This is the 'Law of Saturn as 10th Lord' -- domestic renunciation amplifies executive staying power for...
**PHR Reason:** False flag -- content_validity_dispute: validator applied a classical Vedic causal-logic frame to Gopalakrishnan's empirical observational heuristic. Rule is not presented as a classical derivation -- it is an observed pattern from Indian PM tenure data: Nehru (widower), Indira Gandhi (widow), Vajpayee (bachelor) → long tenures; Rajiv Gandhi, Shastri, VP Singh (all married) → short tenures. The Satu...

#### `mundane-gopal-ch2-india-lagna-filter`
**Title:** Gopal Ch 2 -- India Alignment Lagna Filter for National Leaders
**Source:** Gopal Ch 2 -- Indian Political Lagna Filter
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** IF Indian national leader's Lagna is Cancer or Taurus THEN Tier 1 success alignment (harmonious with India's Taurus Independence Lagna); IF Lagna is Scorpio or Leo THEN Tier 2 success alignment; IF Lagna is Libra (6th from Taurus), Sagittarius (8th from Taurus), or Aries (12th from Taurus) THEN veto...
**Result:** Tier 1 Lagnas (Cancer, Taurus) → highest probability of sustained national power in India. Tier 2 Lagnas (Scorpio, Leo) → moderate success probability. Veto Lagnas (Libra, Sagittarius, Aries) → significantly lower probability of sustained Indian national leadership -- apply as disqualification flag.
**PHR Reason:** The Tier 1/Tier 2/Veto classification by Lagna sign relative to India's Taurus Independence Lagna is logically coherent (using 6th/8th/12th veto positions), but the specific assignment of Cancer and Taurus as Tier 1 (Cancer is 11th from Taurus, not 1st or 4th/7th/10th) requires verification against Gopal source; the harmonic logic may be correct but needs source confirmation.

#### `mundane-mehta-ch6-5th-malefic-assassination`
**Title:** Mehta Ch 6 -- 5th House Malefics + 10th Lord Afflicted: Assassination / Danger to Ruler
**Source:** Mehta Ch 6 -- Houses and their Signification
**Severity:** critical | **Checkable:** False | **Weight:** 1.0
**Condition:** IF the 5th house (which is the 8th from the 10th -- the Danger to the Ruler position) contains one or more malefics (Saturn, Mars, Rahu) AND the 10th lord is simultaneously afflicted by malefic aspect, combustion, or debilitation THEN trigger 'Critical Danger to Ruler' -- the dual affliction of Ruler'...
**Result:** Critical Danger to Ruler: Assassination risk, terrorist attacks on officials, or sudden political elimination of the head of state. Both conditions (5th house malefic + 10th lord afflicted) must be present simultaneously -- single-factor affliction alone does not trigger this rule.
**PHR Reason:** The logic (5th as 8th from 10th = danger to ruler) is sound, but the requirement for BOTH conditions (5th malefic AND 10th lord afflicted) simultaneously is stated as mandatory; verify whether Mehta Ch 6 requires both or treats them as independent triggers, as this affects forecast sensitivity.

#### `mundane-mehta-ch6-sat-10th-democracy`
**Title:** Mehta Ch 6 -- Saturn in 10th House: Democracy vs. Dictator Diagnostic
**Source:** Mehta Ch 6 -- Houses and their Signification
**Severity:** high | **Checkable:** False | **Weight:** 1.0
**Condition:** IF Saturn is in the 10th house of a Republic or Democracy national chart THEN BENEFIC -- Saturn strengthens democratic institutions, rule of law, and long-term stable governance (Saturn as natural significator of the common people and labor is empowered in a democratically-elected government's 10th h...
**Result:** Democracy chart: Saturn in 10th → stable democratic governance, long-term institutional strengthening. Autocratic chart: Saturn in 10th → internal revolt, labor strikes, eventual regime collapse. Diagnosis requires first classifying the national chart as democratic vs. autocratic before applying the...
**PHR Reason:** The bifurcation (Saturn in 10th benefic for democracy, fatal for autocracy) is conceptually sound but requires prior classification of the national chart as democratic vs. autocratic; the rule lacks explicit guidance on how to make this classification and whether it is based on chart signature or historical regime type.

#### `mundane-mehta-ch6-sun-6th-border-war`
**Title:** Mehta Ch 6 -- Sun in 6th House with Malefic: Border Clash Alert
**Source:** Mehta Ch 6 -- Houses and their Signification
**Severity:** critical | **Checkable:** False | **Weight:** 1.0
**Condition:** IF the Sun is in the 6th house of a national chart (6th = Ministry of Defense, Armed Forces) AND is conjunct a malefic (Saturn, Mars, or Rahu) THEN trigger 'Serious Border Clash Alert' -- the 6th house governs territorial defense and military combativeness; Sun + malefic here energizes leadership wit...
**Result:** Serious Border Clash Alert: military escalation, territorial skirmishes, or armed conflict is imminent. Mars lords 6th + 7th simultaneously: Open War = CERTAIN -- escalate to Critical War Warning regardless of other chart factors.
**PHR Reason:** The Sun + malefic in 6th for border clash is coherent, but the secondary condition 'Mars lords both 6th AND 7th = Open War CERTAIN' is a strong claim; verify whether Mehta Ch 6 explicitly states this dual-lordship rule and whether it truly overrides all other chart factors as stated.

#### `mundane-raphael-ch3-intellectual-triad`
**Title:** Raphael Ch 3 -- Intellectual Triad (Houses 1+3+9): National Mind Synchrony
**Source:** Raphael Ch 3 -- Twelve Mundane Houses
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** IF a query concerns National Mood, Press Freedom, Propaganda, Religious Harmony, or Public Opinion THEN audit Houses 1, 3, and 9 together as the Intellectual Triad (House 1 = Collective mental state; House 3 = Press and newspapers; House 9 = Religious attitude and higher thought); IF benefics occupy...
**Result:** Benefic Triad (Houses 1+3+9 benefic): 'Nation entering period of intellectual growth, press freedom, and religious harmony.' Malefic Triad (all three afflicted): 'National intellectual crisis -- press censorship, misinformation campaigns, and religious conflict.' Isolated 9th house malefic: internati...
**PHR Reason:** The Intellectual Triad (Houses 1, 3, 9) is a coherent grouping, but the secondary flag 'malefic in 9th = international shipping disruption + scientific setbacks' appears disconnected from the primary intellectual/press/religion theme; verify whether Raphael Ch 3 explicitly links 9th house malefics to shipping and science, or if this is an inference.

#### `mundane-raphael-ch3-opposition-4th-trigger`
**Title:** Raphael Ch 3 -- 4th House Opposition Rise Trigger
**Source:** Raphael Ch 3 -- Twelve Mundane Houses
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** IF the 4th house lord is strong AND aspected by Jupiter AND the 10th house (Government seat) is simultaneously afflicted by malefics THEN trigger 'Opposition Party Rise Alert'; NOTE: the 4th house in mundane astrology governs both (a) the political Opposition party and (b) agriculture, weather, and ...
**Result:** Opposition Rise Alert: high probability of Opposition party gaining significant influence, electoral momentum, or winning public favor. Dual 4th house activation: the same transit that signals agricultural crop crisis simultaneously signals political opposition surge -- report both outcomes when the ...
**PHR Reason:** False flag -- non_standard_terminology: validator applied a single-signification Vedic frame to Raphael's western mundane system. Raphael's Ch3 explicitly assigns the 4th house BOTH significations -- the political Opposition party AND agriculture/weather -- as a published feature of his system. The dual activation (same transit triggers both agriculture and opposition surge) is Raphael's documented l...

## v20 -- Gopal Ch10 (sports predictions)

#### `mundane-gopal-ch10-sports-batting-first-winner-gate`
**Title:** Gopal Ch10 -- Batting First Winner Gate (10th Lord Trikona + Non-Retrograde)
**Source:** Gopalakrishnan Ch 10 -- Predicting Sports Events (pp.743-744)
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the 10th lord from the match Lagna is placed in a Trikona house (1st, 5th, or 9th house) AND is not Retrograde THEN the team batting first (Team A) has a high probability of winning -- Trikona placement amplifies the 10th lord's victory signal; Retrograde negates this advantage even if Trikona-pla...
**Result:** Team batting first (Team A) will dominate the match and defend their total. Trikona placement of the 10th lord is the strongest single indicator of a comfortable Team A batting-first victory. Validated: India vs WI 2006 series -- Mercury (10th lord) in 9th house (Trikona), non-Retrograde → India succ...
**PHR Reason:** Trikona placement of 10th lord for batting-first advantage is coherent, but the validation example (India vs WI 2006) requires verification against actual Gopalakrishnan text; retrograde negation is standard but the 'highest single indicator' claim may overstate the rule's weight relative to 10th/4th lord comparison hierarchy.

#### `mundane-gopal-ch10-sports-chasing-victory-trigger`
**Title:** Gopal Ch10 -- Chasing Victory Trigger (4th Lord Exalted or Vargottam)
**Source:** Gopalakrishnan Ch 10 -- Predicting Sports Events (pp.744-746)
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the 4th lord (Team B's victory significator -- the 10th from the 7th) is Exalted or Vargottam (same sign in Rasi and Navamsa) at match start, THEN Team B will successfully chase any target set by Team A -- this override applies even when the 10th lord appears moderately strong; the Exaltation/Vargo...
**Result:** Team B Chase Victory confirmed: the team batting second will successfully overhaul the target set by Team A. Even a strong Team A innings does not prevent this if the 4th lord is Exalted or Vargottam. Apply as a primary modifier before the standard Toss Winner Victory Gate.
**PHR Reason:** False flag -- internal_logic_misread: the validator treated the Chasing Victory Trigger as a mechanical override of the Toss Winner Victory Gate, but both rules describe the same underlying mechanism -- the stronger lord wins. An Exalted or Vargottam 4th lord occupies the highest tier of the Vedic planetary strength hierarchy and IS by definition stronger than a 'moderately strong' 10th lord. The Ch...

#### `mundane-gopal-ch10-sports-injury-scandal-alert`
**Title:** Gopal Ch10 -- Injury and Scandal Alert (Mars or Rahu in 6th House)
**Source:** Gopalakrishnan Ch 10 -- Predicting Sports Events (pp.743-744)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Mars or Rahu occupies the 6th house of the match chart (the 6th house governs fall of wickets, injuries, run-outs, and controversies) THEN output a Match Integrity Alert -- Mars in 6th = physical injury to a key player or aggressive confrontation; Rahu in 6th = match-fixing allegations, controvers...
**Result:** Match Alert: High risk of player injury (Mars) or match-fixing / controversial umpire decisions / disciplinary incident (Rahu). The match result may be disputed or overshadowed by off-field events. Mars + Rahu conjunct in 6th = highest-severity integrity alert -- flag for post-match investigation mon...
**PHR Reason:** Mars in 6th for injury and Rahu in 6th for match-fixing are coherent with 6th house significations, but the specific attribution of match-fixing to Rahu (rather than other fraud indicators like 12th lord or Ketu) requires source verification; severity assignment seems reasonable but needs Gopalakrishnan text confirmation.

#### `mundane-gopal-ch10-sports-match-longevity-gate`
**Title:** Gopal Ch10 -- Match Longevity Gate (8th Lord in Fixed Sign)
**Source:** Gopalakrishnan Ch 10 -- Predicting Sports Events (pp.744-746)
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the 8th lord of the match chart is placed in a Fixed sign (Taurus, Leo, Scorpio, or Aquarius) THEN the match will go to its full scheduled duration -- no early finish, no sudden collapse; in cricket: match goes to final over / all 10 wickets fall; in football: match goes to full 90 minutes / extra...
**Result:** Longevity Alert: Match goes to full duration -- no early finish. Cricket: expect close contest decided in final overs, all wickets used. Football: 90 minutes minimum, possible extra time or penalties. Tennis: full sets played, no retirement injury likely. Combine with Close Finish Trigger (equal lord...
**PHR Reason:** Fixed sign placement of 8th lord for full match duration is logically coherent (8th = longevity/duration, Fixed = rigidity/completion), but the distinction from Dual sign (Close Finish Trigger) may conflate two separate principles; requires verification that Gopalakrishnan explicitly uses 8th lord sign classification for match longevity prediction.

#### `mundane-gopal-ch10-sports-umpire-conflict-filter`
**Title:** Gopal Ch10 -- Umpire Conflict Filter (Mars or Rahu in 9th House)
**Source:** Gopalakrishnan Ch 10 -- Predicting Sports Events (pp.743-746)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Mars or Rahu occupies the 9th house of the match chart (the 9th house governs umpires, referees, third-umpire decisions, and the captain/vice-captain) THEN the match will be marred by officiating controversy -- Mars in 9th = aggressive captain behaviour or confrontation with officials; Rahu in 9th...
**Result:** Judgment Alert: Match likely marred by poor officiating, controversial third-umpire / VAR decisions, or captain-referee confrontation. The decisive moment of the match may hinge on an officiating call rather than pure play quality. Flag this match for referee conduct review regardless of final resul...
**PHR Reason:** Mars/Rahu in 9th for officiating controversy is coherent (9th = authority/judgment), but attribution of specific incident types (VAR/DRS, 'Hand of God') to Rahu alone may be over-specified; classical mundane texts typically use 9th lord strength or 9th house affliction more broadly without sport-specific sub-categorization.

## v21 -- Gopal Ch11 (rainfall / monsoon forecast)

#### `mundane-gopal-ch11-rains-rahu-capricorn-moderate`
**Title:** Rahu Transit Capricorn -- NE Monsoon / Himalayan Watershed Stress
**Source:** Gopal Ch 11 -- Rahu Transit Veto
**Severity:** medium | **Checkable:** True | **Weight:** 0.6
**Condition:** IF Rahu is transiting Capricorn (Makara)
**Result:** MODERATE RAINFALL ALERT: Capricorn is a fixed earth sign. Rahu's transit here creates cold disruption of the NE monsoon and stress on Himalayan watersheds. River flow in the Gangetic plain may reduce during the winter season. Snowfall patterns in J&K and Himachal may be erratic.
**Notes:** Rank 4 of 4 in the Rahu Transit Veto. Capricorn is Saturn's own sign -- Rahu + Saturn energy combines to produce cold/dry disruption. Most relevant for North India winter crop (Rabi) and Himalayan hydr...
**PHR Reason:** Rahu in Capricorn is a valid mundane indicator but the specificity of 'NE monsoon disruption' and 'Himalayan watershed stress' requires verification against Gopalakrishnan's actual Capricorn veto classification; Capricorn's role in the Rahu Transit Veto system may differ from Leo/Taurus/Scorpio priority rankings.

#### `mundane-gopal-ch11-rains-rahu-saturn-bhukti-monsoon-failure`
**Title:** Rahu in Taurus/Scorpio + Saturn Bhukti -- Critical SW Monsoon Failure Gate
**Source:** Gopal Ch 11 -- Rahu Transit Veto (Amplifier Rule)
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Rahu is transiting Taurus OR Scorpio AND the current India National Dasha/Bhukti lord is Saturn
**Result:** CRITICAL RAINFALL ALERT -- ELEVATED: Saturn is the amplifier of Rahu's disruptive effect on the water cycle. When both conditions converge, the probability of a severe South-West Monsoon failure rises to near-certain. This is the compound gate described by Gopalakrishnan as the signature of Pan-India...
**Notes:** This compound rule combines Rahu Transit Veto (T-01 or T-02) with the Saturn Bhukti amplifier. India's national Dasha sequence must be computed from the Independence chart (Aug 15, 1947). Do not apply...
**PHR Reason:** The compound gate (Rahu in Taurus/Scorpio + Saturn Bhukti) is a recognized amplifier rule, but the claim of 'near-certain' monsoon failure and 'Pan-India drought signature' is extremely strong; requires cross-validation against historical case studies beyond 2002 and clarification of whether this applies to both SW and NE monsoons equally.

#### `mundane-gopal-ch11-rains-tajika-4th-watery-positive`
**Title:** Tajika Ingress 4th House Watery -- Positive Seasonal Rainfall Forecast
**Source:** Gopal Ch 11 -- Tajika / Monthly Ingress Technique (Technique 3)
**Severity:** low | **Checkable:** True | **Weight:** 0.8
**Condition:** IF in the Sun ingress chart (Gemini for SW monsoon, Libra for NE monsoon) the 4th house contains Moon OR Venus, OR the 4th lord is placed in a watery sign (Cancer, Scorpio, or Pisces), OR an unafflicted Jupiter aspects the 4th house by trine or conjunction
**Result:** POSITIVE RAINFALL FORECAST: The 4th house is the house of moisture, agricultural land, and groundwater in mundane charts. Watery planets or watery lord placement confirms adequate seasonal rainfall. Jupiter's aspect adds the 'blessing of timely distribution' -- rains arrive when crops need them. Expe...
**Notes:** Cast ingress chart for New Delhi (national capital) for Indian forecasts. Check Moon and Venus -- both are watery planets in Vedic meteorology. Jupiter's unafflicted aspect overrides minor malefic plac...
**PHR Reason:** The rule correctly identifies 4th house significations and watery planet placement, but the phrase 'Jupiter's aspect adds the blessing of timely distribution' is interpretive language that may not directly correspond to classical Tajika methodology; the condition list is comprehensive but could benefit from clarification on aspect orbs and whether all conditions must be met or any single condition...

## v22 -- Gopal Ch12 (India native profile)

#### `mundane-gopal-ch12-india-bpo-destiny-3rd-house`
**Title:** India 3rd House Cluster -- BPO/IT Global Backbone Destiny
**Source:** Gopal Ch 12 -- Regional Economic Weights (BPO Destiny Modifier)
**Severity:** low | **Checkable:** False | **Weight:** 0.85
**Condition:** IF the query context is India's long-term economic trajectory, global competitiveness, or knowledge-economy forecasts
**Result:** STRUCTURAL DESTINY -- EVERGREEN: The cluster of Mercury (communication, trade, data) and Venus (services, aesthetics, relational skills) in the 3rd house of India's Independence chart creates a natal promise: India is structurally destined to remain the global backbone of IT, BPO, and back-office pro...
**Notes:** This rule applies a permanent positive modifier to India IT/BPO forecasts. It does NOT override short-term negative transit signals (e.g., Saturn in Cancer → sector stress), but it sets the recovery t...
**PHR Reason:** False flag (partial) -- content_validity_dispute: The core principle -- Mercury + Venus cluster in India's 3rd house creates a natal IT/BPO destiny -- is Gopalakrishnan's teaching from Ch12. The validator correctly identifies that the +0.50 quantified weight modifier is the analyst's calibration, not Gopal's sourced figure, and that 'immune to economic cycles' overstates the source claim. However, th...

#### `mundane-gopal-ch12-india-cancer-transit-south-it`
**Title:** Cancer Sign Transits -- South India IT Sector Economic Impact
**Source:** Gopal Ch 12 -- Regional Economic Weights (South India IT Boom)
**Severity:** medium | **Checkable:** True | **Weight:** 0.8
**Condition:** IF a major planet (Saturn, Jupiter, or Rahu/Ketu) transits Cancer (Kataka) AND the query context is India's IT, BPO, or knowledge-services sector
**Result:** REGIONAL SECTOR ALERT: Cancer is the 3rd house from India's Taurus Lagna and is associated with the southern direction. The planetary cluster in India's natal 3rd house (Mercury + Venus) creates a permanent IT/BPO destiny for southern India (Karnataka, Tamil Nadu, Telangana, Andhra, Kerala). When a ...
**Notes:** Checkable: verify against India IT sector performance during historical Cancer transits. Saturn in Cancer (2003-2005): India IT/BPO boom despite initial caution. Jupiter in Cancer (2014-2015): Start-u...
**PHR Reason:** The directional logic (Cancer = 3rd from Taurus = south) and planetary transit effects are coherent, but the claim that Cancer specifically governs South India IT requires verification against Gopalakrishnan's actual regional mapping methodology.

#### `mundane-gopal-ch12-india-jupiter-6th-judicial-corruption`
**Title:** India Jupiter in 6th -- Structural Judicial Corruption & Merit Bypass
**Source:** Gopal Ch 12 -- India Native Profile (Structural Governance Flaws)
**Severity:** medium | **Checkable:** False | **Weight:** 0.75
**Condition:** IF the query context is India governance, judiciary, or merit-based institutions AND the reference chart is the Independence chart (Aug 15, 1947, Taurus Lagna) AND Jupiter is natally in the 6th house
**Result:** STRUCTURAL GOVERNANCE FLAW -- EVERGREEN: Jupiter (planet of Dharma, wisdom, and justice) placed in the 6th house (service, debt, conflict, litigation) creates a permanent structural tension in India's judiciary and merit systems. Merit is consistently bypassed in favor of political influence, seniori...
**Notes:** This is a structural diagnostic -- use it when forecasting outcomes of judicial reforms, anti-corruption drives, or meritocracy debates in India. The base forecast is: reform efforts will face systemic...
**PHR Reason:** False flag -- content_validity_dispute: Jupiter in the 6th house of a national chart indicating institutional friction and displacement of the dharmic/priestly class is valid mundane astrology. The caste-reservation framing is Gopalakrishnan's own interpretation in Ch12 -- he explicitly connects Jupiter in 6th to the displacement of the Brahmin/intellectual class through reservation policies. The va...

#### `mundane-gopal-ch12-india-pakistan-2-12-friction-veto`
**Title:** India-Pakistan 2/12 Lagna Veto -- Permanent Structural Friction Gate
**Source:** Gopal Ch 12 -- Neighbor Friction Framework (2/12 Lagna Veto)
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF the query context is India-Pakistan relations, peace negotiations, or bilateral trade agreements
**Result:** STRUCTURAL WARNING -- PERMANENT: Pakistan's Lagna (Aries/Mesha) is the 12th sign from India's Lagna (Taurus/Rishabha). The 12th house represents loss, foreign enemies, hidden adversaries, and expenditure in mundane charts. Pakistan literally occupies India's house of loss in zodiacal geometry. This i...
**Notes:** Checkable: every India-Pakistan peace initiative since 1947 has broken down. Validated instances: 1966 Tashkent (failed after Shastri death), 1972 Simla (partial implementation), 1999 Lahore (Kargil w...
**PHR Reason:** False flag -- content_validity_dispute: The 2/12 Lagna relationship as a structural tension indicator between neighboring nations is established mundane astrology. Gopalakrishnan explicitly states in Ch12 that India and Pakistan cannot maintain lasting peace due to this geometric relationship -- this is his documented teaching, not the analyst's extrapolation or deterministic addition. The validator...

#### `mundane-gopal-ch12-india-rahu-lagna-western-imitation`
**Title:** India Rahu in Lagna -- Structural Western Imitation Tendency
**Source:** Gopal Ch 12 -- India Native Profile (National Psyche Markers)
**Severity:** medium | **Checkable:** False | **Weight:** 0.7
**Condition:** IF the query context is India AND the reference chart is the Independence chart (Aug 15, 1947, Taurus Lagna) AND Rahu is natally placed in the Lagna
**Result:** STRUCTURAL NATIONAL TRAIT -- EVERGREEN: Rahu in the Lagna of India's Independence chart creates a permanent national psyche oriented toward foreign cultures, Western systems, and external validation. India consistently adopts foreign frameworks (legal, academic, economic, technological) over indigeno...
**Notes:** Structural rule -- applies to every India-context forecast as a base modifier. Rahu's transit through the Lagna by progression does not change this; the natal placement is permanent. Use as a backgroun...
**PHR Reason:** False flag -- content_validity_dispute: 'Pseudo-secularism' and the Western-imitation characterization are Gopalakrishnan's own terms from Ch12, not an editorial overlay. Rahu in Lagna = orientation toward the foreign/external is standard Vedic mundane astrology (Rahu = foreign, boundary-crossing, imitative). The validator rejected the cultural characterization as ideologically loaded, but it is so...

#### `mundane-gopal-ch12-india-venus-moon-sports-obsession`
**Title:** India Venus + Moon Conjunction -- National Sports Obsession (Cricket)
**Source:** Gopal Ch 12 -- India Native Profile (National Psyche Markers)
**Severity:** low | **Checkable:** False | **Weight:** 0.6
**Condition:** IF the query context is India AND the reference chart is the Independence chart (Aug 15, 1947, Taurus Lagna) AND Venus (Lagna lord) and Moon (3rd lord) are natally combined
**Result:** STRUCTURAL NATIONAL TRAIT -- EVERGREEN: The conjunction of Venus (Lagna lord = national identity) and Moon (3rd lord = communication, sports, competitive activities) creates a mass-level emotional identification with competitive sports. Cricket is the primary manifestation. Any major cricket outcome ...
**Notes:** Combined with the v20 Ch10 Sports rules (mundane-interp-v20 batch), this rule provides the India-specific background weight for cricket match predictions. A sport prediction for India carries +0.20 na...
**PHR Reason:** The Venus-Moon conjunction logic for mass emotional identification is coherent, but the claim that cricket outcomes produce 'measurable socio-economic ripple effects' requires empirical validation and is not a standard mundane astrology principle in classical sources.

## v3  -- Gaur Ch2 (Celestial Council) + Mehta Ch13/20/26

#### `mundane-gaur-ch2-dhanyesh-outcome-matrix`
**Title:** Dhanyesh (Lord of Winter Crops) Planet Outcome Matrix
**Source:** Gaur Ch 2 -- The Celestial Council
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** Identify the Dhanyesh -- Lord of Winter Crops planet as lord of weekday on Lord of the weekday on Sagittarius ingress (Dhanu Sankranti) for the Winter crops (Rabi season): Moong, Moth/lentil, Millet, Mustard, Wheat. Apply 7-planet outcome matrix: IF Sun → Winter crops Moong, Moth (lentil), Millet des...
**Result:** Identify the lord of the weekday on Sagittarius ingress. Look up that planet's outcome. Venus and Saturn as Dhanyesh both indicate winter crop losses -- critical overlap signal.
**PHR Reason:** False flag -- content_validity_dispute: The Dhanyesh rule encodes Gaur's planet-outcome matrix for the Lord of Winter Crops official. The Mars outcome listing summer produce (Millet, Moong, Rice, Maize) reflects Gaur's source text -- Mars governs these crops as heat-demanding grains regardless of the seasonal office. The validator applied a seasonal-logic filter that is not part of Gaur Ch2's framew...

#### `mundane-gaur-ch2-dvadasha-sarpa-snake-forecast`
**Title:** Dvadasha Sarpa (Twelve Snakes) -- Auxiliary Rainfall and Security Forecast
**Source:** Gaur Ch 2 -- The Celestial Council
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** Apply formula: Add 2 to Shak Samvat, divide by 12. Remainder = snake type (1-12). Good-rain signal: [2, 5, 9, 10]. Poor-rain signal: [3, 4, 7, 8, 11, 12]. Notable signals: {'3_Kakotak': 'Rains less. Mourning due to death of a senior ruler -- leader mortality signal.', '6_Takshak': 'Rains medi....
**Result:** Use as third auxiliary check alongside Meghesh planet and Cloud type. Three-way convergence (Meghesh + Cloud + Snake all indicating poor rain) = strong drought alert. Kakotak (3) or Takshak (6) years need enhanced political monitoring.
**Notes:** Engine spec gaur-ch2-twelve-snakes holds the full lookup table.
**PHR Reason:** Snake type formula and signal assignments appear consistent with Gaur Ch 2 auxiliary rainfall methods, but Kakotak (3) linked to 'leader mortality' is a secondary inference not explicitly stated in most standard Gaur texts; requires verification against original source.

#### `mundane-gaur-ch2-meghesh-outcome-matrix`
**Title:** Meghesh (Lord of Weather and Rains) Planet Outcome Matrix
**Source:** Gaur Ch 2 -- The Celestial Council
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** Identify the Meghesh -- Lord of Weather and Rains planet as lord of weekday on Lord of the weekday when Sun enters Ardra nakshatra for the Monsoon quality, rainfall quantity, weather patterns for the year. Apply 7-planet outcome matrix: IF Sun → Rains less, prices high, politicians have differences. ...
**Result:** Meghesh is the primary rainfall forecaster. Identify the lord of the weekday when Sun enters Ardra nakshatra. Cross-reference with Gaur Ch 10 Saturn-in-Ardra rule and Rohini protection rule for monsoon synthesis. Sun or Saturn as Meghesh → drought alert.
**PHR Reason:** Cross-reference to 'Gaur Ch 10 Saturn-in-Ardra rule and Rohini protection rule' is plausible but those specific chapter/rule citations are not standard in widely available Gaur texts; requires source verification.

#### `mundane-mehta-ch13-eclipse-lord-placement`
**Title:** Eclipse Sign Lord Placement -- Amplification Rule
**Source:** Mehta/Rao Ch 13 -- Eclipses
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Saturn in 8th house placement → Eclipse sign lord in 8th house → serious deaths and accidents. IF Saturn in 6th house placement → Eclipse sign lord in 6th house → may cause diseases. IF Saturn in 3rd house placement → Eclipse sign lord in 3rd house → rail, road and air accidents or strikes in rai...
**Result:** After identifying eclipse sign, check its lord's natal house position in the national horoscope. 8th placement = death/accident signal. 3rd placement = transport crisis. Total eclipse + malefic aspect = national famine/pestilence trigger.
**PHR Reason:** Rule conflates Saturn's natal house with eclipse sign lord's house; classical sources typically examine eclipse sign lord's placement in the national chart, not Saturn's position as the determining factor.

#### `mundane-mehta-ch13-eclipse-national-validation`
**Title:** Eclipse National Impact -- India Empirical Validations (Mehta/Rao)
**Source:** Mehta/Rao Ch 13 -- Eclipses
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF india 1983 rule: Solar eclipse 11 June 1983 in Taurus sign with Mars in it -- eclipse falling on India's ruling Taurus...; india 1995 rule: Solar eclipse 24 Oct 1995 07:22 in Libra -- 10th house from Capricorn (India's traditional rashi). Re...; nepal 2001 rule: Lunar eclipse 10 Jan 2001 at 00:12 AM fe...
**Result:** Eclipse in India's lagna sign Taurus or 10th from traditional Capricorn rashi → major political disruption + agricultural crisis for India. Eclipse on 4/10 axis of any nation's horoscope with retrograde malefics → leadership assassination or violent regime change.
**PHR Reason:** False flag -- content_validity_dispute: Mehta and Rao explicitly use India's Independence chart (Aug 15, 1947) with Taurus Lagna as the reference chart for eclipse impact analysis -- not the traditional Capricorn national rashi. The 1983 solar eclipse in Taurus directly afflicted India's natal Lagna, which is the standard independence-chart method used throughout Ch13. The validator's concern about ...

#### `mundane-mehta-ch13-eclipse-ruler-royalty`
**Title:** Eclipse Effects on Rulers and Royalty -- Positive and Negative Outcomes
**Source:** Mehta/Rao Ch 13 -- Eclipses
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF timing: Events may happen within 4 months of solar eclipse and a week of lunar eclipse. Events may happen pr...; auspicious rule: Eclipse on or in opposition to natal Sun, Moon or ascendant of a ruler → mostly auspicious; elevatio...; auspicious examples: Duke of York: natal Sun fell on eclipse 13 De...
**Result:** For any ruling leader: check if current eclipse falls on/opposite natal Sun, Moon or ascendant. If ON these points AND aspected by both Mars and Saturn → assassination or death in office signal. If only in opposition with benefic involvement → elevation. Two eclipses in 15 days → war imminent.
**PHR Reason:** The Duke of York example (1936) and assassination rule are plausible but the condition mixing auspicious opposition with malefic conjunction needs clearer logical separation; timing windows (4 months solar, 1 week lunar) are standard but should be cross-referenced.

#### `mundane-mehta-ch20-delhi-bombs-national-affliction`
**Title:** Delhi Bomb Blasts (13.09.2008) -- India National Chart Affliction Pattern
**Source:** Mehta/Rao Ch 20 -- Terrorism
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF event: Serial bombing in Delhi 13.09.2008 18:10; observations -- Saturn afflicting Sun, Moon and Taurus lagna of independent India -- direct attac...; india signature: When Saturn simultaneously afflicts India's Taurus lagna + afflicts Sun and Moon in India's chart + ....
**Result:** India national attack trigger: Saturn on Taurus lagna AND Rahu on Capricorn rashi AND all benefics (Mercury, Venus, Jupiter) simultaneously afflicted by Mars in grah yudha = maximum national vulnerability window. Capital (Delhi) under direct attack risk when Simha rashi is in Papkartari yoga.
**PHR Reason:** False flag -- content_validity_dispute: The Delhi 2008 serial bombing analysis is Mehta/Rao's own empirical case from Ch20. The validator questions the Saturn + Rahu affliction hierarchy and Papkartari yoga applied to a rashi (not a planet), but these are Mehta's own observational notes -- they are not the analyst's extrapolations. The rule is source-faithful empirical documentation, not a normative...

#### `mundane-mehta-ch20-india-temple-attack-signature`
**Title:** India Temple/Religious Site Attack Signature (Ayodhya 5 July 2005)
**Source:** Mehta/Rao Ch 20 -- Terrorism
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF trigger pattern -- Planet of religion Jupiter under heavy affliction from Ketu (secret spies), Rahu...; navamsha protection: Answer in navamsha, if lagna is very strong with Jupiter in lagna and directional strength, with asp...; event: Ayodhya Ram Janam Bhoomi temple attack, 5 July 2005, 8:46 AM.
**Result:** Religious site attack signature: Jupiter heavily afflicted by all four malefics (Rahu, Ketu, Mars, Saturn) + 9th house Saturn affliction + Mars in 8th with nodes = high risk of temple/mosque/religious site attack. Saturn in 12th = foreign-origin terrorists infiltrated. Strong navamsha lagna may part...
**PHR Reason:** False flag -- content_validity_dispute: The Ayodhya 2005 temple attack analysis is Mehta/Rao's own empirical case from Ch20. The validator flags 'Jupiter afflicted by all four malefics' as imprecise, but Rahu and Ketu are explicitly treated as malefics in Mehta/Rao's framework throughout this chapter. The navamsha protection clause is Mehta's own qualifying language -- it is operationally vague but ...

#### `mundane-mehta-ch20-madrid-london-validation`
**Title:** Madrid (11.03.2004) and London (07.07.2005) -- Transport Terror Validation
**Source:** Mehta/Rao Ch 20 -- Terrorism
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF transport terror signature: Mars-Rahu/Ketu in or aspecting the 3rd house (communication/transport) or 4th lord afflicted by Rahu-Mars = transport attack indicator. Madrid 11.03.2004: Mars-Rahu conjunct in 3rd house (railways) + Venus (vehicles) with Rahu + Moon afflicted by Ketu + Jupiter retrogr...
**Result:** Transport terror signature: Mars + Rahu/Ketu in 3rd house or aspecting 3rd/4th lord of vehicles = train/bus/air vehicle attack. When Saturn also afflicts communication houses (3rd, 12th) simultaneously with Mars-Rahu = mass casualty transport attack. Both Madrid and London validated this parameter c...
**PHR Reason:** False flag (methodology class mismatch) -- this rule is intentionally a documentary empirical case study validating the transport terror signature across two historical events (Madrid 2004, London 2005). Sub_type 'terrorism_empirical_case' marks it as evidentiary, not a standalone predictive rule. The predictive mechanism is in mundane-mehta-ch20-terrorism-ten-parameters (auto_approved). The valida...

#### `mundane-mehta-ch20-nine-eleven-validation`
**Title:** 9/11 WTC New York -- Astrological Validation (11 Sept 2001, 9:00 AM)
**Source:** Mehta/Rao Ch 20 -- Terrorism
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF event: September 11, 2001 suicide planes attack on World Trade Centre and Pentagon, New York, 9:00 AM. Chart features confirming terrorism parameters: Saturn in Rohini Nakshatra -- evil position causing wars, riots and strife (Parameter 6 ✓). Mars and Ketu conjunct in Sagittarius 4th house (buildi...
**Result:** 6 of 10 terrorism parameters were active simultaneously. Saturn in Rohini + Mars-Ketu in Sagittarius 4th house + Rahu affliction of Moon + Jupiter in 6th with Rahu = full terrorism gate activated. Historical validation: 9/11 WTC attack confirmed this parameter set as catastrophic event trigger. Also...
**PHR Reason:** False flag (methodology class mismatch) -- this rule is intentionally a documentary empirical case study, not a standalone predictive rule. Sub_type 'terrorism_empirical_case' explicitly marks it as evidentiary, not operational. The predictive framework (10 parameters, weighting, methodology) is defined in the companion rule mundane-mehta-ch20-terrorism-ten-parameters -- which is auto_approved. This...

#### `mundane-mehta-ch20-terrorism-ten-parameters`
**Title:** Terrorism Astrological Gate -- 10 Parameters (K.N. Rao)
**Source:** Mehta/Rao Ch 20 -- Terrorism: An Astrological Explanation
**Severity:** critical | **Checkable:** True | **Weight:** 1.0
**Condition:** IF source article: K.N. Rao in Journal of Astrology, July-September 2002; parameter 1: Combination of Mars with Rahu/Ketu -- together, in opposition, or in kendras from each other.; parameter 2: Combination of Saturn-Rahu conjunction, opposition or in square. 'When Saturn and Rahu join together...; par...
**Result:** When 4+ parameters are simultaneously active in any national or world chart, increased terrorist activity is indicated. When 6+ parameters converge with an eclipse active within 4 months -- catastrophic multi-casualty event risk. Parameters 1+2+3+6 together constitute the core terror quartet. When pa...
**PHR Reason:** Parameters 1-3 are clearly stated but the rule cuts off before listing parameters 4-10; the threshold of '4+ parameters' for increased activity and '6+ for catastrophic event' is quantifiable but needs full parameter set and source verification from K.N. Rao's 2002 article.

#### `mundane-mehta-ch26-bjp-dasha-history`
**Title:** Bhartiya Janata Party (BJP) -- Dasha-Event Historical Validation
**Source:** Mehta/Rao Ch 26 -- Political Parties of India
**Severity:** high | **Checkable:** False | **Weight:** 1.0
**Condition:** IF party birth: BJP: 6 April 1980, 11:45, Delhi. Lagna 23°36'.; key correlations -- BJP obtained only 2 seats of 543 in 1984 elections. Mercury (lagna lord) in Rahu....
**Result:** BJP empirical model confirms: lagna lord in Rahu/Ketu axis with malefic aspect = minimal electoral performance. Ketu/Jupiter antardasha with 9th-10th lords = electoral breakthrough. Antardasha lord as 8th lord from Mahadasha = electoral loss. Rajayoga (malviya yoga from Moon + Saturn aspecting own 1...
**PHR Reason:** The empirical correlations (lagna lord in Rahu/Ketu axis, Ketu/Jupiter antardasha, 8th lord antardasha) are coherent but the condition cuts off mid-sentence; the 1984 election result (2 seats) is historically accurate and supports the rule's logic.

#### `mundane-mehta-ch26-congress-i-dasha-history`
**Title:** Indian National Congress-I -- Dasha-Event Historical Validation
**Source:** Mehta/Rao Ch 26 -- Political Parties of India
**Severity:** high | **Checkable:** False | **Weight:** 1.0
**Condition:** IF party birth: Congress-I (Indira Congress): 2 January 1978, Lagna 15°01'; key correlations -- Elections Jan 1980 -- won 351 of 524 seats (landslide). But tragedy too: Sanjay G....
**Result:** Congress-I empirical model confirms: retrograde malefic (Mars R) as Mahadasha lord = founder's violent assassination (Indira Gandhi 1984). Rahu chidra dasha = second leadership assassination (Rajiv Gandhi 1991). Saturn 12th from Mahadasha lord = loss of government power. Jupiter aspect on own 10th =...
**PHR Reason:** Retrograde Mars as Mahadasha lord causing assassination is a strong classical principle; the 1980 landslide (351/524) and 1984/1991 assassinations are historically accurate; however, the condition cuts off and navamsha details are missing.

#### `mundane-mehta-ch26-party-dasha-framework`
**Title:** Political Party Horoscope -- Vimshottari Dasha Analysis Framework
**Source:** Mehta/Rao Ch 26 -- Political Parties of India
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** IF method: Cast horoscope for exact founding date, time and place of the political party. Apply Vimshottari das...; key houses -- Power and governance -- strength here = ability to form government; dasha principles -- Debilitated planet as dasha lord brings setbacks in that house's domain; cross referenc...
**Result:** Apply full Vimshottari dasha analysis to party's founding chart. Dasha lord in 8th or marka role → leadership crisis or loss of power. Retrograde malefic dasha = internal party violence, leader assassination risk. Jupiter aspecting own 10th = party retains relevance even in opposition. Saturn 12th f...
**PHR Reason:** False flag -- content_validity_dispute: Mehta/Rao Ch26 is explicitly titled 'Political Parties of India' and covers the dasha framework for party horoscopes throughout the chapter. Political party chart analysis is Mehta's own documented methodology, not an extrapolation. The validator's concern about it being 'non-classical' misapplies the standards for classical Jyotish to a modern mundane applic...

#### `mundane-mehta-ch26-retrograde-malefic-dasha-crisis`
**Title:** Retrograde Malefic Dasha → Political Leader Assassination / Violent Death
**Source:** Mehta/Rao Ch 26 -- Political Parties of India
**Severity:** critical | **Checkable:** False | **Weight:** 1.0
**Condition:** IF primary rule: When a retrograde malefic planet (Mars R, Saturn R, Rahu -- always retrograde) is the active Mahadash...; mars retrograde rule: Mars retrograde as Mahadasha lord: Mars is planet of violence and lord of marka house. Being retrogr...; rahu chidra dasha rule: Rahu chidra dasha (Rahu/Rahu su...
**Result:** Monitor: (1) Is the current Mahadasha lord of the party chart a retrograde malefic? (2) Is the leader's personal chart also showing marka dasha? (3) Is India's national chart simultaneously showing 8th lord activation or Rahu-marka-house conjunction? Triple convergence = very high risk of leader ass...
**PHR Reason:** The triple convergence logic (retrograde malefic Mahadasha + leader's marka dasha + India's 8th lord activation) is coherent and follows classical principles; however, the condition is incomplete and the distinction between 'very high risk' and 'heightened vigilance' needs quantified thresholds.

## v4  -- Gaur Ch10 (price differentials) + Gaur Ch11 (eclipse)

#### `mundane-gaur-ch10-jupiter-motion-differentials`
**Title:** Jupiter Motion State Commodity Differentials
**Source:** Gaur Ch 10, p.101
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** IF direct motion → When Jupiter comes in direct motion: grains, metals and pulses are cheap. IF retrograde → Jupiter retrograde: brings down prices of grains, ELEVATES metals such as gold and silver. IF rising → When Jupiter rises: gold is cheap, silver is expensive. IF combusted → When Jupiter is c...
**Result:** Jupiter retrograde is the key signal for precious metals (gold, silver) price elevation. Direct Jupiter benefits all grains and pulses (prices fall). Combusted Jupiter depresses everything.
**Notes:** Jupiter's retrograde period is an important window for gold/silver price monitoring.
**PHR Reason:** False flag -- content_validity_dispute (conversion artefact): The validator identifies an apparent mismatch between the converted IF-chain condition (which covers both direct and retrograde Jupiter outcomes) and the result (which summarises the retrograde signal as the key actionable). This is an artefact of the dict-to-prose conversion: the full original condition dict contained both motion-state ...

#### `mundane-gaur-ch10-mercury-motion-differentials`
**Title:** Mercury Motion State Commodity Differentials
**Source:** Gaur Ch 10, pp.98
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** IF direct motion → Mercury direct: grains expensive. Silver and cotton undergo fluctuations initially, later expensive.... IF retrograde → Mercury retrograde: juicy materials (gur/khand) expensive. Grains cheap. IF rising → Mercury rises: wheat and gram expensive. IF combusted → Mercury combusted: whe...
**Result:** Mercury's motion state reverses grain vs gur price signals. Direct = grains up, gur/khand up. Retrograde = grains down, gur/khand up. Combusted = grains down.
**PHR Reason:** Result summary is coherent but condition text appears truncated ('silver and cotton undergo fluctuations initially, later expensive....'); verify full source text for completeness of motion-state reversals.

#### `mundane-gaur-ch10-rahu-drought-aries-libra`
**Title:** Rahu in Aries or Libra -- Drought Signal
**Source:** Gaur Ch 10, p.109
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Rahu transiting through Aries OR Libra (both axis signs of the Aries-Libra axis). Also: effect: Drought due to lack of rains. Grains expensive..
**Result:** Rahu in Aries or Libra is a recurring drought indicator. Grains become expensive. Cross-check with Meghesh planet and Nava Megha cloud type for convergence.
**Notes:** Ketu is simultaneously in the opposite sign (Libra or Aries). Both nodes on the Aries-Libra axis = dual drought indicator.
**PHR Reason:** Rule is logically sound but 'Aries-Libra axis' phrasing is non-standard in classical Vedic mundane texts; verify whether source explicitly treats both signs as equivalent drought triggers or if one is primary.

#### `mundane-gaur-ch10-saturn-motion-differentials`
**Title:** Saturn Motion State Commodity Differentials
**Source:** Gaur Ch 10, pp.107-108
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF rising → Saturn rises: mustard oil, peanuts and cotton cheap for 1 month; iron, gur, khand expensive. IF combusted → Saturn combusted: gold cheap, grains expensive. direct change: Saturn changes to direct motion: oil materials, chillies and asafoetida expensive for 2 months..
**Result:** Saturn retrograde periods signal grain and oil price increases. The specific nakshatra retrograde patterns (Uttarashadh→Poorvashadh; Magha→Ashlesha) are drought/price triggers.
**PHR Reason:** False flag -- content_validity_dispute (conversion artefact): The validator notes that the result references Saturn retrograde and specific nakshatra transition patterns (Uttarashadha→Poorvashadha, Magha→Ashlesha) not visible in the converted condition text. These nakshatra references are from Gaur Ch10's Saturn-motion table, which includes additional retrograde observations not captured by the Pat...

#### `mundane-gaur-ch10-venus-motion-differentials`
**Title:** Venus Motion State Commodity Differentials
**Source:** Gaur Ch 10, p.104
**Severity:** low | **Checkable:** True | **Weight:** 1.0
**Condition:** IF direct motion → Venus direct: grains, gur, ghee, gold, silver and gems expensive. Cotton cheap. IF retrograde → Venus retrograde: grains (wheat, gur, khand, ghee, oils) expensive. IF combusted → Venus combusted: gold and silver expensive. Grains expensive initially then cheap later on. IF rising ...
**Result:** Both direct and retrograde Venus tend to raise commodity prices (different categories). Rising Venus is the key signal for gold, silver, rice, and textile price elevation.
**PHR Reason:** False flag -- content_validity_dispute (conversion artefact): The validator flags an apparent contradiction between Venus direct/retrograde both elevating grain prices, with the cotton-cheap signal in direct motion not appearing in the result summary. This is an artefact of prose conversion from the original dict: the result summarises the net directional signal across all Venus motion states (gene...

#### `mundane-gaur-ch11-two-eclipses-fortnight-calamity`
**Title:** Two Eclipses Within 15 Days -- Turmoil and Grain Price Surge
**Source:** Gaur Ch 11, p.113
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF Two eclipses (solar + lunar) occurring within a 15-day fortnight.. Sign/context effects: sequence_note: If lunar eclipse 15 days AFTER solar eclipse: beneficial outcome.; inverse: If solar eclipse comes AFTER lunar eclipse: results undesired and detrimental..
**Result:** Two eclipses in a fortnight → turmoils or natural calamities in the world, resulting in loss of money and lives. Grains become expensive. The sequence (solar first vs lunar first) determines whether outcome is harmful or beneficial.
**Notes:** Cross-reference with Mehta Ch 13 rule: two eclipses in fortnight also signals war risk at geopolitical level.
**PHR Reason:** Sequence logic (lunar after solar = beneficial; solar after lunar = detrimental) is stated but result conflates this with 'turmoils or natural calamities' without clarifying which sequence produces which outcome; verify source for explicit outcome mapping.

## v5  -- Gopal Ch6 (mass death) + Gopal Ch7 (earthquakes)

#### `mundane-gopal-ch6-epidemic-triad`
**Title:** Epidemic Triad -- Saturn 6th from Country Moon, Rahu in Country Moon Sign, Venus-Saturn Conjunction
**Source:** Gopalakrishnan Ch 6, pp.88-90
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** IF saturn 6th from country moon: Saturn transiting the 6th sign counted from the country's natal Moon sign. E.g., India's Moon = Canc...; rahu in country natal moon sign: Rahu transiting through the same sign as the country's natal Moon. E.g., India's Moon = Cancer → Rah...; venus saturn conjunction: Ve...
**Result:** Epidemic or pandemic conditions in the country. Single condition = watch; two conditions active = elevated epidemic risk; all three active simultaneously = severe epidemic/pandemic imminent.
**Notes:** Gopalakrishnan validated this triad against the 1918 Spanish Flu (Saturn+Rahu positions + Venus-Saturn aspect active globally). The country-specific Moon sign anchor makes this rule nation-by-nation. ...
**PHR Reason:** Venus-Saturn conjunction in 6th/8th for epidemic is non-standard; typically Saturn-Rahu or Saturn-Ketu are primary epidemic indicators in classical sources; Venus involvement requires verification against Gopalakrishnan's exact wording.

#### `mundane-gopal-ch7-cardinal-stellium-upheaval`
**Title:** Cardinal Sign Stellium -- Geopolitical Upheaval and Large-Scale Sudden Events
**Source:** Gopalakrishnan Ch 7, p.96
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Three or more planets clustering in cardinal signs (Aries, Cancer, Libra, Capricorn) simultaneously. Also: pure cardinal: All 3+ planets in the same cardinal sign: maximum intensity.; spread cardinal: 3+ planets spread across 2-3 different cardinal signs: broad geopolitical instab....
**Result:** Geopolitical upheaval, leadership crises, sudden large-scale events. Not a direct earthquake indicator but frequently co-occurs with seismic events as part of a broader world-crisis configuration.
**Notes:** Cardinal signs = signs of initiation and action. Heavy planetary clustering = forced change. Cross-reference with Mehta Ch 11 cardinal-clustering rule (mundane-mehta-ch11-cardinal-clustering) and Gopa...
**PHR Reason:** Cardinal stellium is typically a geopolitical/governance indicator; attribution to seismic events is secondary and requires confirmation that Gopalakrishnan explicitly links cardinal clusters to seismic activity rather than only upheaval.

#### `mundane-gopal-ch7-rahu-ketu-ic-mc-axis`
**Title:** Rahu/Ketu Axis Aligned with IC/MC of Regional Chart -- Major Seismic Event
**Source:** Gopalakrishnan Ch 7, pp.95-96
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** The Rahu-Ketu nodal axis aligns within 5° of the IC (4th house cusp) and MC (10th house cusp) of the Aries Ingress chart cast for a specific territory, or of that territory's natal chart. Also: eclipse on ic: A solar or lunar eclipse occurs within 5° of the IC of the regional chart: seism....
**Result:** Major seismic event in the territory within 3-6 months of the nodal alignment. Eclipse on IC specifically indicates the earthquake's epicenter near the capital or geographic center of the country.
**Notes:** The IC (4th cusp) represents the earth itself / underground / foundations. Rahu/Ketu on this axis destabilizes the literal ground. Cross-reference with Mehta Ch 11 eclipse-nadir rule (mundane-mehta-ch...
**PHR Reason:** Nodal axis alignment with IC/MC is strong; however, the claim that eclipse on IC indicates epicenter near capital is overly specific and may exceed classical source precision; requires direct textual verification.

## v6  -- Gopal Ch8 (war) + Gopal Ch9 (civil unrest)

#### `mundane-gopal-ch8-india-pakistan-2-12-lagna`
**Title:** India-Pakistan 2/12 Lagna Relationship -- Structural Permanent Tension
**Source:** Gopalakrishnan Ch 8, p.104
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** India and Pakistan have their national chart Ascendants in a 2/12 relationship: one country's Ascendant falls in the 2nd sign from the other's, and vice versa. (India lagna = Taurus; Pakistan lagna = Cancer -- Cancer is 3rd from Taurus, but Gopalakrishnan cites 2/12 axis from his chart versions.) Als...
**Result:** India and Pakistan will always have recurring border tensions, infiltration, and periodic military skirmishes or wars. Peace agreements are temporary -- structural axis ensures conflict returns.
**Notes:** Cross-reference with Mehta Ch 19 India-Cancer-Capricorn axis rule (mundane-mehta-ch19-india-cancer-capricorn). Gopalakrishnan uses this structural 2/12 principle to explain why India-Pakistan relation...
**PHR Reason:** Condition states Cancer is 3rd from Taurus (correct), but then claims Gopalakrishnan cites 2/12 axis--this internal contradiction needs verification against actual source text to confirm whether the rule is based on 2/12 or 3/11 relationship.

#### `mundane-gopal-ch9-malefics-trika-entry`
**Title:** Saturn/Rahu/Jupiter Entering Trika Houses (6/8/12) -- Negative Events Triggered
**Source:** Gopalakrishnan Ch 9, p.146
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn, Rahu, or Jupiter transiting into the 6th, 8th, or 12th house of the national chart (or into the sign ruled by the 6th/8th/12th lord). Also: into 6th: Triggers war, epidemic, debt crisis, labor disputes.; into 8th: Triggers leadership crisis, mass deaths, government collapse.; into 12th: Trig...
**Result:** Negative events in the domain governed by that trika house are triggered when Saturn, Rahu, or Jupiter enter it. Effect begins at ingress and intensifies during the full transit period.
**Notes:** This rule uses the national chart's house structure (not generic zodiac houses). For India (Taurus Ascendant): 6th = Libra, 8th = Sagittarius, 12th = Aries. Saturn entering Libra = 6th house for India...
**PHR Reason:** Jupiter inclusion as malefic in trika house transits is borderline; classical sources often treat Jupiter as benefic even in 6th/8th/12th. Verify whether Gopalakrishnan explicitly groups Jupiter with Saturn/Rahu for trika malefic effects or treats it separately.

#### `mundane-gopal-ch9-planet-bundle-crisis`
**Title:** 5+ Planets Bundled Within 30° in Sensitive Houses -- National Crisis
**Source:** Gopalakrishnan Ch 9, p.148
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Five or more planets concentrated within a 30° arc simultaneously, especially when this concentration falls in the national chart's 6th, 8th, 12th, 10th, or 1st house. Also: threshold: Concentration of 5 or more planets within 30° = problem.; house sensitivity: 6th/8th/12th: maximum negative impact ...
**Result:** Major national or global crisis: mass deaths, market crashes, regime changes, wars, epidemics. The nature of crisis depends on which houses the bundle occupies and which planets are involved.
**Notes:** Case study May 2003: Saturn+Mars in Taurus (fixed sign), Ketu in Scorpio. Results: mass deaths globally, world markets depressed (bearish), Saddam regime overthrown, tensions in multiple countries. Si...
**PHR Reason:** The 30° arc threshold and 5-planet minimum are specific but lack explicit source citation; verify exact parameters from Gopalakrishnan Ch 9 p.148 to confirm these are his stated thresholds rather than interpolation.

## v7  -- Gopal Ch10/13/15 (career/governance/economy)

#### `mundane-gopal-ch10-mars-perigee-leadership-change`
**Title:** Mars at Perigee (Closest to Earth) -- Incumbent Leaders Replaced
**Source:** Gopalakrishnan Ch 10, pp.170-175
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Mars reaches its closest approach to Earth (Mars at opposition/perigee): occurs approximately every 26 months. Mars = Bhumi Karaka (significator of land and earth). Also: affected regions: Leaders in regions where Mars is the dominant planetary influence (states/nation....
**Result:** Incumbent leaders, chief ministers, and heads of government in affected regions are removed, defeated, or replaced within 12-24 months of Mars perigee. Accompanied by: mass death events (tsunami, floods, drought), war/military conflict, earthquakes, price rise in chemicals and red goods.
**Notes:** Validated in 2005-2006 Mars perigee: ALL south Indian CMs replaced -- Kerala (AK Anthony), Karnataka (SM Krishna), Andhra (CBN), MP (Uma Bharti), Sri Lanka (Chandrika). Gopalakrishnan predicted this be...
**PHR Reason:** False flag -- content_validity_dispute: Mars at opposition/perigee (closest approach) is a classical mundane astrology concept -- Gopal teaches this in Ch10 as the Mars Bhumi Yoga (Mars at maximum terrestrial influence). The validator's objection that astronomical events lack astrological basis is contradicted by the fact that planetary opposition IS an astrological configuration (Mars opposite Sun)...

#### `mundane-gopal-ch13-jupiter-6th-dasa-no-peace`
**Title:** Leader Running 6th House Lord Dasa -- No Peace in Tenure
**Source:** Gopalakrishnan Ch 13, pp.202-205
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** The head of government (president, prime minister) is running the Vimshottari dasa of the planet that rules the 6th house in their natal chart. Also: bush case: George W. Bush (2nd oath chart): running Jupiter dasa. Jupiter is in his 6th hou....
**Result:** Continued conflict, war, and insurgency throughout the leader's tenure. Little to no chance of genuine peace. Policy shifts possible when bhukthi changes, but base conflict continues.
**Notes:** Mirror rule to mundane-gopal-ch8-6th-lord-dasa-insurgency (national chart version). This applies to the individual leader's natal chart -- the 6th lord dasa activates enemies, war, conflict, and health...
**PHR Reason:** The rule is coherent (6th house = conflict; Jupiter dasa = expansion of that conflict), but the claim of 'little to no chance of genuine peace' is absolute and requires verification against Gopalakrishnan's actual text for nuance and exceptions.

#### `mundane-gopal-ch13-saturn-bhukthi-raja-yoga-stock-market`
**Title:** Nation Running Raja Yoga Bhukthi -- Stock Market Bull Run
**Source:** Gopalakrishnan Ch 9, pp.153-155 (Sensex case study)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** The national chart is running a Bhukthi period of a planet that forms a Raja Yoga in the natal chart (conjunction or mutual aspect between Kendra lord + Trikona lord, or the planet that is both 1st/4th/7th/10th AND 5th/9th lord). Also: india saturn bhukthi: India running Venus Dasa + Saturn Bhukthi ...
**Result:** Bull run in the national stock market for the duration of the Raja Yoga bhukthi. Economic growth, FII inflows, multiple sector booms.
**Notes:** Bull run ends when the bhukthi changes to a non-raja-yoga planet, or when Saturn finishes the sign it is transiting at the time. Gopalakrishnan: 'The bull run will last till Saturn is in Kataka (Cance...
**PHR Reason:** Raja Yoga definition is correct, but the rule assumes all Raja Yoga bhukthi periods produce bull runs; this oversimplifies--other transits (Saturn's own strength, aspect patterns, dasa lord strength) must be considered. The India case study needs verification.

#### `mundane-gopal-ch13-saturn-ketu-conjunction-civil-war`
**Title:** Saturn + Ketu Transit Conjunction -- Civil War Eruption Signal
**Source:** Gopalakrishnan Ch 13, p.205
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn and Ketu form a transit conjunction (within 5° orb) in the same sign simultaneously. Also: amplification: Effect is greatly amplified when the conjunction falls in the 6th, 8th, or 12th ....
**Result:** Very strong probability of civil war erupting or intensifying dramatically. Internal armed conflict reaches new heights. For nations already in insurgency: full-scale civil war breaks out.
**Notes:** Validated: Sri Lanka prediction for Saturn-Ketu conjunction 2007. 'With Saturn and Ketu conjunction in 2007 there will be very good chances of civil war erupting.' Historical record: Sri Lanka civil w...
**PHR Reason:** False flag -- content_validity_dispute: Saturn-Ketu conjunction is Gopal Ch13's own documented signal for civil war risk. The 'very strong probability' language is Gopal's own framing -- not the analyst's deterministic addition. The 5° orb is standard for conjunction rules in Gopal's framework. Historical instances (1882, 1942, 2019 Kashmir escalation) support the correlation directionally. The vali...

#### `mundane-gopal-ch15-jupiter-6th-national-dharma-down`
**Title:** Jupiter in 6th House of National Chart -- Dharma and Merit Compromised
**Source:** Gopalakrishnan Ch 15, p.228
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** Jupiter is placed in the 6th house of a nation's natal chart, OR Jupiter is severely afflicted (conjunct/aspected by 3+ malefics) in any house of the national chart. Also: india case: India natal chart: Jupiter in 6th house from Taurus Ascendant (in Libra)..
**Result:** Dharma (righteousness/merit-based decision-making) goes down in that nation. Merit will NOT be the source of decision-making in government and institutions. Caste-based, connection-based, or corruption-based systems dominate over merit. 'Whenever Jupiter is afflicted in a nation's horoscope, DHARMA ...
**Notes:** Gopalakrishnan uses this to explain India's reservation/caste-quota system persisting despite economic development. Jupiter in 6th = conflict between dharma (9th) and debt/disease/enemies (6th). In In...
**PHR Reason:** The principle (Jupiter 6th = dharma decline) is coherent, but the rule conflates Jupiter in 6th with Jupiter 'severely afflicted by 3+ malefics'--these are two different conditions with potentially different outcomes. Needs clarification on which applies when.

#### `mundane-gopal-ch15-rahu-11th-national-stock-boom`
**Title:** Rahu in 11th House of National Chart -- Stock Market Bull Run
**Source:** Gopalakrishnan Ch 9, pp.153-155 (case study)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Rahu transiting through the 11th house of the national chart (11th sign from the national Ascendant). Also: india specific: For India (Taurus Ascendant): 11th house = Pisces. When Rahu enters Pisces (coun....
**Result:** Stock market bull run and tech sector frenzy for the duration of Rahu's transit through the 11th house (~18 months). FII (foreign institutional investor) inflows surge.
**Notes:** 11th house = income, gains, trade of the country. Rahu in 11th = exaggerated and unexpected gains, speculative frenzy. Validated: India's Rahu-in-11th period corresponded to major Sensex bull runs (Se...
**PHR Reason:** Rahu in 11th (gains/networks) producing stock boom is logically coherent, but the ~18-month window is vague (Rahu transits a sign ~18 months, but effect onset/offset timing unclear). Requires case study verification.

#### `mundane-gopal-ch15-saturn-3rd-national-it-boom`
**Title:** Saturn Transiting 3rd House of National Chart -- IT/Communication/BPO Boom
**Source:** Gopalakrishnan Ch 15, pp.225-228
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Saturn transiting through the 3rd house of a nation's chart (the 3rd sign from the national chart's Ascendant). Also: india specific: For India (Taurus Ascendant): 3rd house = Cancer. When Saturn enters Cancer = IT....
**Result:** Massive boom in communication, information technology, transportation, and outsourcing/BPO sectors for that nation. Government and corporate investment in communication infrastructure surges.
**Notes:** Validated for India: Saturn entered Cancer (India's 3rd house) 2002 → India became global BPO backbone; telecom revolution; IT exports surged. Cross-reference with Gaur Ch 10 Saturn-3rd-India-IT rule ...
**PHR Reason:** False flag -- content_validity_dispute: Gopal Ch15 explicitly teaches that Saturn transiting the 3rd house (communication, technology, short-distance commerce) creates disciplined, systematic expansion in technology sectors -- not contraction. Saturn in 3rd generates structured IT/BPO infrastructure growth through rigour and process (Saturn's positive qualities in a Mercury/3rd-house domain). The va...

## v8  -- Eclipse severity/commodity rules

#### `mundane-raphael-ch14-mars-7th-war-direction`
**Title:** Mars in 7th House = War Danger + Cardinal Direction of Enemy
**Source:** Raphael Ch 14, Part 2 pp.5-6
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** At the time of a Solar Ingress, Lunation, or Eclipse: Mars is placed in the seventh house of the mundane map.
**Result:** Grave danger of international disputes, disagreement with other Powers, unsatisfactory condition of foreign relations, and DANGER OF WAR. DIRECTION OF ENEMY: the cardinal direction from which the enemy will come is shown by the sign Mars occupies -- Mars in Aries = enemy from EAST; Mars in Cancer = e...
**Notes:** Mars is the most powerful malefic in the 7th house. Next most malefic in foreign affairs: Saturn in 7th. This rule applies to ingress, lunation, and eclipse charts for any nation. The direction indica...
**PHR Reason:** The directional mapping (Aries=East, Cancer=North, Libra=West, Capricorn=South) is stated but the result text is truncated ('Signs betwee'), preventing verification of how intermediate signs are handled.

#### `mundane-raphael-ch8-malefic-1st-national-troubles`
**Title:** Malefic in 1st House of Mundane Map = National Troubles and Public Ill-Health
**Source:** Raphael Ch 8, p.11
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** At a Solar Ingress, Lunation, or Eclipse: a malefic planet (Mars, Saturn, Uranus, Neptune) is placed in the first house of the mundane map, especially if afflicted by other planets.
**Result:** Much trouble is shown in the country; things will be unsettled; health of the people bad. MARS in 1st: discontent, strikes, riots, fires, crime and ill-health. SATURN in 1st: distress, discontent, want of work, loss of trade, poverty, general ill-health. URANUS in 1st: strikes, rioting, violence, an...
**Notes:** The 1st house in mundane astrology represents the general population and national health. If no planet is in 1st, judge by the ruler of the rising sign and its aspects. Well-aspected malefics are some...
**PHR Reason:** Result text is incomplete/truncated ('NEPTUNE in 1st: agitation, secret propaganda, sociali'); cannot assess full coherence without complete statement.

## v9  -- Sun/Moon transit + Solar ingress rules

#### `mundane-raphael-ch22-eclipse-fixed-lasting-cardinal-brief`
**Title:** Eclipse in Fixed Signs = Very Lasting Effect; Cardinal = Brief; Mutable = Interrupted
**Source:** Raphael Ch 22, p.15 (Part 2)
**Severity:** medium | **Checkable:** True | **Weight:** 1.0
**Condition:** Assess the zodiac modality of the sign in which any Solar or Lunar eclipse falls.
**Result:** FIXED sign eclipse (Taurus, Leo, Scorpio, Aquarius): VERY LASTING EFFECT -- the most enduring and serious in mundane impact. CARDINAL sign eclipse (Aries, Cancer, Libra, Capricorn): BRIEF AND SOON OVER -- effects are intense but pass quickly. MUTABLE sign eclipse (Gemini, Virgo, Sagittarius, Pisces): ...
**Notes:** Combine with element rule for full assessment: Fixed + Earthy (Taurus) = most lasting earthquake/agricultural crisis. Fixed + Fiery (Leo) = most lasting war/royal crisis. Fixed + Watery (Scorpio) = mo...
**PHR Reason:** The modality framework (fixed=lasting, cardinal=brief, mutable=interrupted) is coherent, but the result text is truncated ('t'), preventing full assessment of the mutable sign outcome description.

#### `mundane-raphael-ch26-eclipse-on-meridian-nadir-earthquake`
**Title:** Eclipse on Meridian or Nadir = Earthquake in That Region; Fixed-Sign Planet at Eclipse = Quake Where Planet Rises/Sets
**Source:** Raphael Ch 26, Part 3 p.5
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A Solar or Lunar eclipse falls on or near the MERIDIAN (MC) or NADIR (IC) of a given location's mundane map. OR: at the moment of eclipse, a planet in a fixed sign is at a significant angle (rising, setting, culminating, or on the nadir) in a given location.
**Result:** Earthquakes generally follow close on the heels of such eclipses. If planets are in fixed signs at the eclipse moment: earthquakes will occur in those parts of the world where such planets are either RISING, SETTING, CULMINATING, or ON THE NADIR. Example: if at eclipse, Saturn is in a fixed sign and...
**Notes:** Validated by Syria 1822: Lunar eclipse → Saturn in exact square to eclipse degree on day of disaster. This rule requires calculating for each specific location whether the eclipse falls on or near the...
**PHR Reason:** Result text is incomplete/truncated mid-sentence ('45° from the meridian, earthquakes occur in that part of the world which is the same distance from'); cannot assess full coherence without complete statement.

#### `mundane-raphael-ch26-great-conjunction-4th-cusp-earthquake`
**Title:** Great Planetary Conjunction on 4th House Cusp (IC/Nadir) = Earthquake in That Locality
**Source:** Raphael Ch 26, Part 3 p.5
**Severity:** high | **Checkable:** True | **Weight:** 1.0
**Condition:** A great planetary conjunction (Mars-Jupiter, Mars-Saturn, Jupiter-Saturn, Saturn-Uranus, or Saturn-Neptune) falls exactly on or within orb of the cusp of the 4th house (IC/Nadir) of the mundane map for a given location.
**Result:** An earthquake is sure to occur in that locality. Cast a mundane map for the time of the great conjunction and check whether the conjunction falls on the Nadir or 4th house cusp for each location of interest.
**Notes:** Validated cases: Charlestown 1886: Mars-Jupiter conjunction on 4th house cusp → serious earthquake. Kuchan 1898: Mars-Saturn conjunction on 4th house cusp → 12,000 killed. Mont Pelée 1902: Jupiter-Sat...
**PHR Reason:** Rule is coherent but 'sure to occur' is an absolute claim; classical Raphael typically uses probabilistic language ('likely', 'generally'); verify exact wording in source.

#### `mundane-raphael-ch27-comet-sign-type-effects`
**Title:** Comet Effects by Sign Type -- Cardinal = Death of Great Men; Fixed = Foreign Wars; Mutable = Sedition/Pestilence
**Source:** Raphael Ch 27, Part 3 p.7
**Severity:** medium | **Checkable:** False | **Weight:** 1.0
**Condition:** A great comet appears or is at perihelion (nearest Sun or Earth). Note the zodiac sign in which the comet first appears.
**Result:** CARDINAL signs (Aries, Cancer, Libra, Capricorn): death of great men. FIXED signs (Taurus, Leo, Scorpio, Aquarius): foreign wars and invasion. COMMON/MUTABLE signs (Gemini, Virgo, Sagittarius, Pisces): sedition and pestilence. Position by horizon: East = rising of some eminent law-giver; Midheaven =...
**Notes:** Historical example: Halley's Comet 1910 return -- earthquakes and electrical storms were frequent for two years prior to its approach. Russo-Japanese War (1904): comet of 1903 appeared in Aquarius (= R...
**PHR Reason:** Result text is incomplete/truncated ('Countries ruled by the sign in which'); cannot assess full coherence and faithfulness without complete statement.

---

# PART C -- Flagged (Genuine Open Issues)
*1 rule(s) with unresolved content flags.*

#### `mehta-ch10-aries-1-degree-conjunction-paradigm-shift`
**Title:** Heavy Planet Conjunction in Aries 1° = Century-Level Paradigm Shift (Highest Signal)
**Source:** Mehta/Rao Ch 10
**Flag:** The claim that this applies 'equally to conjunctions, not only Saturn-Jupiter' contradicts classical Mehta doctrine, which reserves the 0°-1° Aries paradigm shift specifically for Saturn-Jupiter. Extending to Mars, Rahu, Ketu is not faithfully sourced.
**Condition:** Any conjunction of heavy planets (Saturn, Jupiter, Mars, Rahu, Ketu) commences in the first degree of Aries (0°-1° Aries). This applies equally to conjunctions, not only Saturn-Jupiter.
**Result:** 'Century-Level Paradigm Shift' alert -- the highest-level predictive signal in the engine. This is the rarest configuration in mundane astrology: known to have occurred only eight times in recorded history. Historical turning points of civilizational scale have always followed.

---

## Summary Counts

| Status | Count |
|---|---|
| auto_approved (ready to promote) | 137 |
| pending_human_review | 186 |
| flagged (open) | 1 |
| **Total under review** | **324** |

*No rules reach live users until explicitly set to `approval_status: approved` via co-founder sign-off.*