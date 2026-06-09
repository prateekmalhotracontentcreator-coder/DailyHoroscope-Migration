# Commission KE-OP-18 -- KP Condition Handlers + Lookup Library

> EverydayHoroscope · Stack: FastAPI, Python 3.12, MongoDB Motor async
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Date issued: 2026-06-09

---

CODEX COMMISSION BRIEF -- KE-OP-18
Knowledge Engine -- KP Condition Type Handlers + Comprehensive Lookup Library
─────────────────────────────────────────────────────────────────────────────

New file:     backend/kp_sublord_table.py          (T05 lookup module, baked-in)
Modified:     backend/knowledge_engine.py           (ChartFacts + _condition_matches)
Modified:     backend/knowledge_schema.py           (secondary_axis field)
Modified:     backend/ke_schema_constants.py        (VALID_CLAIM_AXES update)

─────────────────────────────────────────────────────────────────────────────
CONTEXT
─────────────────────────────────────────────────────────────────────────────

The KE rule corpus includes ~10,234 evaluable rules (approved + auto_approved +
pending_human_review). Approximately 4,000+ rules sourced from KP Jyotish
textbooks (300 Notable Horoscopes, 300 Combinations, Longevity Unnatural,
Longevity 58 Chapters, KP Vol 3) use KP-specific condition types:

  kp_planet_signification   -- Does planet X signify house Y?
  kp_star_lord              -- Is planet X's nakshatra lord planet Y?
  kp_csl                    -- Is house H's cuspal sub-lord planet Y?
  kp_signification_chain    -- Composite: planet signifies ALL of houses [H1, H2, ...]

Currently, _condition_matches() in knowledge_engine.py has NO handler for any of
these types. They fall through to `return False` unconditionally. This means every
KP-flavoured rule returns False regardless of the chart -- the entire KP corpus
contributes zero signal to any chart evaluation.

This is a critical engine gap (KE-OP-18). The fix is NOT to rewrite the KP logic --
it already exists fully in kp_engine.py. The fix is to:
  1. Extend ChartFacts with KP-specific fields populated from the chart
  2. Add KP condition dispatch branches to _condition_matches
  3. Build kp_sublord_table.py as a baked-in lookup module (T05 data, 249 entries)
  4. Add secondary_axis to the rule schema

─────────────────────────────────────────────────────────────────────────────
EXISTING INFRASTRUCTURE -- READ FIRST, DO NOT DUPLICATE
─────────────────────────────────────────────────────────────────────────────

backend/kp_engine.py -- THE KP COMPUTATION ENGINE. Already fully built. Use it.

  kp_chain(longitude: float) -> dict
    Given a planet's sidereal longitude, returns:
      { "nakshatra": str, "nakshatra_lord": str, "star_lord": str,
        "pada": int, "sub_lord": str, "sub_sub_lord": str,
        "sub_lord_span_degrees": float, "sub_sub_lord_span_degrees": float }
    Implements the full KP sub-division lookup. This is the star_lord/sub_lord
    engine. DO NOT reimplement -- import and call this.

  house_relevance_for_planet(snapshot: dict, planet_name: str) -> dict[str, int]
    Given a full KP snapshot and a planet name, returns a dict mapping
    house number strings ("1"-"12") to integer relevance scores:
      +3 if planet is in that whole-sign house directly
      +2 if planet is lord of that house
      +1 for each of (nakshatra_lord, sub_lord, sub_sub_lord):
           if linked planet occupies that house (+1)
           if linked planet lords that house (+1)
    This is the complete KP signification scoring function.

  planet_significator_map(snapshot: dict) -> dict[str, list[int]]
    Returns { planet_name: [list of houses it signifies (score > 0)] }
    This is exactly what kp_planet_signification conditions need.

  placidus_sidereal_cusps(jd_ut: float, lat: float, lon: float)
      -> tuple[list[float], dict[str, float]]
    Returns (cusp_longitudes_list, extra_angles_dict).
    cusp_longitudes_list[0] = Ascendant (House 1 cusp)
    cusp_longitudes_list[1] = House 2 cusp
    ...
    cusp_longitudes_list[11] = House 12 cusp
    For each cusp longitude, call kp_chain(cusp_lon) to get the sub_lord.

  NOTE: house_relevance_for_planet() takes a "snapshot" dict (the full KP chart
  object from build_birth_snapshot()). The _condition_matches path works from
  ChartFacts, which is a lighter structure. See PART 1 below for how to bridge
  this -- you will implement the signification logic directly using ChartFacts
  fields rather than calling house_relevance_for_planet() with a snapshot.

backend/knowledge_engine.py -- THE KE ENGINE.

  ChartFacts (dataclass, lines ~378-388):
    keys            : set[str]
    planet_positions: dict[str, dict]  -- planet → {house, sign, nakshatra,
                                          dignity, retrograde, combust}
    house_planets   : dict[int, list[str]]
    house_lords     : dict[int, str]
    yogas           : set[str]
    dasha_levels    : dict[str, set[str]]
    aspect_targets  : dict[str, set[int]]
    aspected_by     : dict[int, set[str]]
    varga_dignities : dict[str, dict]
    CURRENTLY: no KP fields. You will add three (see PART 1).

  extract_chart_facts(chart: dict) -> ChartFacts
    Call this to build ChartFacts. You will add _populate_kp_facts() inside it.
    The chart dict has:
      chart["planets"]  -- dict keyed by planet name with "longitude" field
      chart["lagna"]    -- {"sign": str, "degree": float}
      chart["houses"]   -- dict {1: sign_name, 2: sign_name, ...}  (whole-sign)
    NOTE: Chart built by phase4_layer_b.py includes "longitude" in each planet.
    The live app chart from calculate_vedic_chart() also includes it.

  _condition_matches(condition: dict, facts: ChartFacts) -> bool
    Dispatch on condition.get("type"). Currently handles:
      planet_in_house, planet_in_sign, planet_in_nakshatra, planet_aspect,
      planet_conjunction, planet_dignity, planet_retrograde, planet_combust,
      house_lord_in_house, yoga, dasha_period, yoga_combination, kp_sublord,
      transit, composite.
    You will ADD handlers for four new types (see PART 2).
    DO NOT modify any existing handler.

backend/ke_schema_constants.py

  VALID_CLAIM_AXES (line 46): List of valid claim_axis strings.
    Current values: general, general_trend, career_growth, career_timing,
    career_trend, wealth, wealth_trend, financial_security, marriage_timing,
    relationship_quality, relationships_trend, partnership_stability, children,
    education_trend, health_vitality, health_trend, spiritual_growth,
    spirituality_trend, enemies_adversaries, past_lives, travel_pattern,
    learning_outcome, longevity, longevity_trend.

backend/knowledge_schema.py

  InterpretationRuleDocument (Pydantic model):
    claim_axis: str -- already present, validated against VALID_CLAIM_AXES
    secondary_axis: does not exist yet -- you will add it.

─────────────────────────────────────────────────────────────────────────────
PART 0 -- kp_sublord_table.py (NEW FILE)
─────────────────────────────────────────────────────────────────────────────

Create: backend/kp_sublord_table.py

This module bakes the T05 Master Sub-Significance table (249 entries) into a
Python constant. No file I/O at runtime -- the data is inline.

Source: /Users/apple/Documents/Knowledge Engine_eBooks/KP_CC_Decode/
        KP_T05_Master_Sub_Significance.json
Structure (schema of each entry):
  {
    "no":         int,        # sequential 1-249
    "sign":       str,        # zodiac sign name
    "sign_lord":  str,        # sign ruler planet
    "nakshatra":  str,        # nakshatra name (may include _a/_b suffix for split)
    "nak_lord":   str,        # nakshatra lord (= star_lord in KP chain)
    "sub_lord":   str,        # sub-lord planet
    "span":       str,        # degree span string (informational only)
    "body_parts": str,        # body parts governed
    "health":     str,        # health conditions indicated
    "vocations":  str,        # professions and trades indicated
    "mental":     str,        # mental/psychological tendencies
    "node_dep":   bool        # True = interpretation depends on Rahu/Ketu position
  }

Build TWO lookups:

  T05_BY_NUMBER: dict[int, dict]
    Key: entry "no" (1-249)
    Value: full entry dict

  T05_BY_CHAIN: dict[tuple[str, str], list[dict]]
    Key: (nak_lord, sub_lord)  -- both normalised to Title Case
    Value: list of matching entries (a chain pair can appear in multiple signs)

  Example:
    T05_BY_CHAIN[("Ketu", "Ketu")]   → entries where nak_lord=Ketu, sub_lord=Ketu
    T05_BY_CHAIN[("Ketu", "Rahu")]   → entries where nak_lord=Ketu, sub_lord=Rahu

Expose a lookup function:

  def get_sub_entries(star_lord: str, sub_lord: str) -> list[dict]:
      """Return all T05 entries matching (star_lord, sub_lord) chain.
      Returns empty list if no match (e.g. node_dep entries where Rahu/Ketu
      interpretation is position-dependent and incomplete in the table).
      """

  def get_sub_entry_for_sign(star_lord: str, sub_lord: str, sign: str) -> dict | None:
      """Return the single T05 entry matching (star_lord, sub_lord, sign).
      Returns None if not found.
      """

Important: node_dep=True entries (91 of 249) have partial or incomplete
interpretation text. Flag them but still return the entry -- the caller decides
whether to use or skip node_dep entries.

─────────────────────────────────────────────────────────────────────────────
PART 1 -- ChartFacts KP Extension (knowledge_engine.py)
─────────────────────────────────────────────────────────────────────────────

Add THREE new fields to the ChartFacts dataclass:

  kp_chains: dict[str, dict[str, str]]
    Per planet: { "star_lord": str, "sub_lord": str, "sub_sub_lord": str }
    Empty dict for planets whose longitude is not available.

  kp_significations: dict[str, list[int]]
    Per planet: sorted list of house numbers (1-12) that the planet signifies
    via the KP signification algorithm.
    Signification score > 0 → planet appears in the list.

  cuspal_sub_lords: dict[int, str]
    House number (1-12) → sub_lord planet name for that house's Placidus cusp.
    Populated ONLY when chart dict contains cusp longitude data.
    If cusp data is absent (chart built from whole-sign only), leave empty.

Add _populate_kp_facts(chart: dict, facts: ChartFacts) -> None inside
extract_chart_facts(), called after _populate_varga_dignity_facts().

Implementation of _populate_kp_facts:

  Step 1 -- Import kp_chain from kp_engine:
    from kp_engine import kp_chain

  Step 2 -- For each planet in facts.planet_positions:
    longitude = chart["planets"][planet_name].get("longitude")
    if longitude is None:
        continue
    chain = kp_chain(float(longitude))
    facts.kp_chains[planet_name] = {
        "star_lord":    chain["star_lord"],
        "sub_lord":     chain["sub_lord"],
        "sub_sub_lord": chain["sub_sub_lord"],
    }

  Step 3 -- Compute KP significations for each planet using ChartFacts:
    The signification algorithm uses ONLY ChartFacts (no external snapshot needed).
    For planet P, house H gets a signification score from:
      a. P is directly in house H (from facts.house_planets):            +3
      b. P is lord of house H (from facts.house_lords):                  +2
      c. For each linked_planet in (star_lord, sub_lord, sub_sub_lord):
           if linked_planet is in house H:                               +1
           if linked_planet is lord of house H:                          +1
    House lords: facts.house_lords is {house_num: lord_planet_name}.
    Reverse it to {lord_planet: [houses it lords]}.
    Collect all houses where score > 0 → facts.kp_significations[planet].
    Ketu and Rahu: treat their chain identically; they have no lordship
    (shadow planets), so skip lordship contribution for them.

  Step 4 -- Cuspal sub-lords (only if cusp data present in chart):
    chart may contain chart["cusps"] as a list of cusp longitude floats,
    OR chart["kp_cusps"] as a dict {house_num: longitude_float}.
    If either is present:
      for house in range(1, 13):
          cusp_lon = get cusp longitude for house
          cusp_chain = kp_chain(cusp_lon)
          facts.cuspal_sub_lords[house] = cusp_chain["sub_lord"]
    If cusp data is absent, skip silently (facts.cuspal_sub_lords stays empty).
    Layer B test vectors do NOT include cusp data -- that is expected and fine.
    The live app's calculate_vedic_chart does NOT currently compute Placidus
    cusps -- this is a future enhancement. Build the field now, populate when
    data is available.

─────────────────────────────────────────────────────────────────────────────
PART 2 -- _condition_matches New Handlers (knowledge_engine.py)
─────────────────────────────────────────────────────────────────────────────

Add FOUR new dispatch branches to _condition_matches(). Insert them BEFORE the
final `return False` line (currently line 717). Add in this order:

──── Handler 1: kp_planet_signification ────

  if condition_type == "kp_planet_signification":
      planet    = normalize_planet_name(condition.get("planet"))
      house     = condition.get("house")       # int, e.g. 10
      min_score = condition.get("min_score")   # optional int threshold (default: any > 0)
      if not planet or house is None:
          return False
      sig_houses = facts.kp_significations.get(planet, [])
      if int(house) not in sig_houses:
          return False
      return True

  Schema for this condition type in rules:
    { "type": "kp_planet_signification",
      "planet": "Saturn",
      "house": 10,
      "min_score": 2          # optional -- require at least this raw score
    }

  Use case: "Saturn signifies the 10th house" (career, profession).
  A planet signifies a house if it has ANY connection to it via the KP chain
  (occupying, lording, or its sub-chain lording/occupying that house).

──── Handler 2: kp_star_lord ────

  if condition_type == "kp_star_lord":
      planet     = normalize_planet_name(condition.get("planet"))
      star_lord  = normalize_planet_name(condition.get("star_lord"))
      if not planet or not star_lord:
          return False
      chain = facts.kp_chains.get(planet, {})
      return chain.get("star_lord") == star_lord

  Schema:
    { "type": "kp_star_lord", "planet": "Moon", "star_lord": "Saturn" }

  Use case: "Moon is in Saturn's nakshatra" (e.g. Pushya, Anuradha, Uttara Bhadra).

──── Handler 3: kp_csl ────

  if condition_type == "kp_csl":
      house     = condition.get("house")         # int, house cusp number
      sub_lord  = normalize_planet_name(condition.get("sub_lord"))
      if house is None or not sub_lord:
          return False
      if not facts.cuspal_sub_lords:
          # Cusp data not available in this chart (whole-sign chart)
          # Return False -- cannot evaluate without Placidus cusps.
          return False
      actual = normalize_planet_name(facts.cuspal_sub_lords.get(int(house), ""))
      return actual == sub_lord

  Schema:
    { "type": "kp_csl", "house": 8, "sub_lord": "Saturn" }

  Use case: "8th house cuspal sub-lord is Saturn" (longevity significator).

──── Handler 4: kp_signification_chain ────

  This is a composite: planet must signify ALL listed houses simultaneously.

  if condition_type == "kp_signification_chain":
      planet = normalize_planet_name(condition.get("planet"))
      houses = condition.get("houses", [])      # list of ints
      if not planet or not houses:
          return False
      sig_houses = set(facts.kp_significations.get(planet, []))
      return all(int(h) in sig_houses for h in houses)

  Schema:
    { "type": "kp_signification_chain",
      "planet": "Saturn",
      "houses": [8, 12]      # Saturn must signify BOTH house 8 AND house 12
    }

  Use case: "Saturn signifies both the 8th (longevity) and 12th (loss/exit)
            houses simultaneously" -- a compound KP observation requiring all
            houses to be signified in one rule (exact match, no tolerance).

─────────────────────────────────────────────────────────────────────────────
PART 3 -- Composite Condition Standard (knowledge_engine.py)
─────────────────────────────────────────────────────────────────────────────

The existing `composite` condition handler (dispatched at the `composite` branch
in _condition_matches) must support two operators: "AND" and "OR".

Verify the existing composite handler supports:
  { "type": "composite",
    "operator": "AND",      # or "OR"
    "conditions": [ <condition>, <condition>, ... ]
  }

If it does not, extend it so:
  AND: returns True only if ALL sub-conditions match
  OR:  returns True if ANY sub-condition matches

The multi-factor observation encoding standard (locked 2026-06-09):
  If an author observation requires N simultaneous conditions, encode as:
    { "type": "composite",
      "operator": "AND",
      "conditions": [
        { "type": "kp_planet_signification", "planet": "Saturn", "house": 8 },
        { "type": "kp_planet_signification", "planet": "Saturn", "house": 12 },
        { "type": "dasha_period", "dasha_active": "Saturn" }
      ]
    }
  No tolerance -- all N conditions must be True for the rule to fire.
  Do NOT split into N separate single-condition rules.

─────────────────────────────────────────────────────────────────────────────
PART 4 -- secondary_axis Schema Addition
─────────────────────────────────────────────────────────────────────────────

In backend/knowledge_schema.py, add to InterpretationRuleDocument:

  secondary_axis: Optional[str] = None

Add validator (same pattern as claim_axis):
  @field_validator("secondary_axis")
  @classmethod
  def validate_secondary_axis(cls, value: str | None) -> str | None:
      if value is None:
          return value
      lowered = _lower_or_none(value)
      if lowered not in VALID_CLAIM_AXES:
          raise ValueError(f"Unsupported secondary_axis: {value}")
      return lowered or value

In backend/ke_schema_constants.py, add these to VALID_CLAIM_AXES (they are
observation vocabulary currently used in test vectors but not in the list):
  "career"          -- coarse alias for career_growth/timing/trend combined
  "longevity"       -- already present ✅
  "wealth"          -- already present ✅  
  "health"          -- add (currently health_vitality/trend are separate)
  "marriage"        -- add (alias for marriage_timing/relationship_quality)
  "timing"          -- add (dasha timing observations)
  "death_timing"    -- add (longevity sub-axis)
  "death_mode"      -- add (longevity sub-axis, cause of death)
  "spouse_longevity"-- add (used in test vector observations)

  Note: Do NOT remove existing granular axes (career_growth etc.) -- they remain
  valid for rules that need fine-grained axis declaration. The coarse aliases are
  additive, for rules where the author's observation was at the coarse level.

─────────────────────────────────────────────────────────────────────────────
PART 5 -- T05 Sub-Lord Enrichment in Knowledge Engine (Optional Enhancement)
─────────────────────────────────────────────────────────────────────────────

NOTE: Parts 0-4 are mandatory. Part 5 is an enhancement -- implement only after
Parts 0-4 are complete and tested.

The kp_sublord_table module enables a new optional enrichment layer: when a KP
rule fires, the engine can look up the T05 entry for the planet's sub-lord to
add vocational/health flavour to the interpretation.

In knowledge_engine.py, add a helper:

  def get_t05_enrichment(planet: str, facts: ChartFacts) -> dict | None:
      """
      For a given planet, return the T05 sub-significance entry for its
      (star_lord, sub_lord, sign) combination.
      Returns None if chain data not available or entry not found.
      """
      from kp_sublord_table import get_sub_entry_for_sign
      chain  = facts.kp_chains.get(planet, {})
      sl     = chain.get("star_lord")
      sub    = chain.get("sub_lord")
      sign   = (facts.planet_positions.get(planet) or {}).get("sign", "")
      if not sl or not sub or not sign:
          return None
      return get_sub_entry_for_sign(sl, sub, sign)

This enrichment is NOT used in _condition_matches (condition matching stays
binary True/False). It is available to the interpretation layer (scan_chart
narrative builder) to add T05-derived contextual detail (vocations, body_parts,
health) to the rule's interpretation output.

Do NOT call this from _condition_matches. Keep condition evaluation pure.

─────────────────────────────────────────────────────────────────────────────
LOOKUP TABLE INVENTORY -- ALL 60+ DATATABLE FILES
─────────────────────────────────────────────────────────────────────────────

During book decoding, 105 DataTable .md files were produced. Their role:

  BPHS Vol 1 (38 files -- BPHS_Ch03 through BPHS_Ch45):
    Content: Planetary characters, sign properties, divisional charts,
    aspect rules, yoga structural data, house effects, avastha tables.
    Status: Reference data. Most corresponding chapters are already ingested
    as rules. The DataTables were the structural backbone for rule encoding.
    Action required: NONE from this commission. They are informational archives.
    Future use: Dasha-gate audit (KE-OP-19) may reference BPHS Ch43/44 tables
    for maraka and longevity combinations.

  300 Combinations (21 files -- Combo_Y001 through Combo_Y288):
    Content: Yoga identification tables -- which planets in which house
    combinations constitute each yoga. Already ingested as 329 rules.
    Action required: NONE from this commission. Used during encoding.

  Numerology (24 files -- Numerology_Ch05 through Numerology_Ch27):
    Content: Number→attribute lookup tables (Lo Shu grids, 81 combinations,
    compound numbers, alphabet values, etc.).
    Status: These ARE lookup engines (not rule ingest targets).
    Future action: Build backend/numerology_lookup_table.py parallel to
    kp_sublord_table.py -- a baked-in module for the numerology engine.
    NOT part of this commission.

  Medical Astrology (11 files -- MedAstro_Ch01 through MedAstro_Ch11):
    Content: Planet→disease maps, house→body-part maps, drekkana charts,
    three humours tables (Vata/Pitta/Kapha), duration/duration tables.
    Status: Disease/body-part tables are lookup reference, not rules.
    Future action: Build backend/medical_astrology_lookup.py.
    NOT part of this commission.

  Longevity Unnatural (7 files -- LU_S01 through LU_S04 + benchmarks):
    Content: House signification tables, node signification tables,
    badhaka/maraka tables. Already used to encode longevity rules.
    Action required: NONE.

  KP T05 (1 file -- KP_T05_Master_Sub_Significance.json):
    THIS IS PART 0 OF THIS COMMISSION. Build kp_sublord_table.py from this.

  KP P27 Profession Dictionary (1 file -- KP_P27_Profession_Dictionary.json):
    229 profession entries mapping vocations to planetary indicators.
    Status: Lookup reference for the KP profession-inference engine (765H).
    Action: In this commission, load P27 into kp_sublord_table.py as a
    secondary lookup (P27_BY_VOCATION: dict[str, dict]). Expose:
      def get_profession_entry(vocation: str) -> dict | None
    The 765H profession library (G3) uses this.

─────────────────────────────────────────────────────────────────────────────
ACCEPTANCE CRITERIA
─────────────────────────────────────────────────────────────────────────────

AC-1: kp_sublord_table.py imports without error and exports:
  - T05_BY_NUMBER: dict with 249 entries (keys 1-249)
  - T05_BY_CHAIN: dict; get_sub_entries("Ketu","Ketu") returns at least 1 entry
  - get_sub_entry_for_sign("Ketu","Venus","Aries") returns a non-None dict
  - P27 lookup: get_profession_entry("Military") returns non-None dict

AC-2: ChartFacts has three new fields: kp_chains, kp_significations, cuspal_sub_lords.
  extract_chart_facts(chart) populates kp_chains and kp_significations for all
  planets that have a "longitude" key in chart["planets"].
  cuspal_sub_lords is an empty dict when no cusp data is in chart.

AC-3: _condition_matches handles all four new condition types:
  Given a chart where Moon is in Pushya (Saturn's nakshatra, house 4,
  lording house 4, sub_lord = Jupiter):
    {"type":"kp_star_lord","planet":"Moon","star_lord":"Saturn"}   → True
    {"type":"kp_star_lord","planet":"Moon","star_lord":"Jupiter"}  → False
    {"type":"kp_planet_signification","planet":"Moon","house":4}   → True
    {"type":"kp_planet_signification","planet":"Moon","house":10}  → False (unless chain)

  Given a chart where Saturn is in house 10, lords houses 7 and 8:
    {"type":"kp_signification_chain","planet":"Saturn","houses":[8,10]}  → True
    {"type":"kp_signification_chain","planet":"Saturn","houses":[8,5]}   → False

  kp_csl with empty cuspal_sub_lords → returns False (not an error).

AC-4: composite handler supports AND and OR operators explicitly.
  {"type":"composite","operator":"AND","conditions":[
    {"type":"kp_planet_signification","planet":"Saturn","house":8},
    {"type":"kp_star_lord","planet":"Saturn","star_lord":"Ketu"}
  ]} evaluates correctly (True only when both sub-conditions pass).

AC-5: knowledge_schema.py accepts secondary_axis in rule documents.
  Rule with secondary_axis="longevity" and claim_axis="career" passes validation.
  Rule with secondary_axis="invalid_axis" raises a validation error.

AC-6: ke_schema_constants.py VALID_CLAIM_AXES includes all axes listed in Part 4.

AC-7: All existing _condition_matches handlers are unchanged. No regression.
  Run: python3 -m pytest tests/test_ke_*.py -- all existing tests must pass.
  Run: python3 -m pytest tests/test_ke_yoga_evaluator.py -- 52+ tests green.

AC-8: No circular import. kp_sublord_table.py has zero imports from knowledge_engine.py.
  knowledge_engine.py imports from kp_engine.py only inside _populate_kp_facts
  (local import to avoid circular dependency if needed).

─────────────────────────────────────────────────────────────────────────────
FILES TO READ BEFORE STARTING
─────────────────────────────────────────────────────────────────────────────

Read these in full before writing any code:

  backend/knowledge_engine.py        -- ChartFacts, extract_chart_facts,
                                       _condition_matches, _populate_* helpers
  backend/kp_engine.py               -- kp_chain(), house_relevance_for_planet(),
                                       planet_significator_map(), kp_sublord handler
  backend/knowledge_schema.py        -- InterpretationRuleDocument, validators
  backend/ke_schema_constants.py     -- VALID_CLAIM_AXES, STANDARD_PLANETS
  tests/test_ke_yoga_evaluator.py    -- existing test suite (must stay green)

Read the T05 source:
  /Users/apple/Documents/Knowledge Engine_eBooks/KP_CC_Decode/
    KP_T05_Master_Sub_Significance.json   (249 entries, bake ALL of them inline)
    KP_P27_Profession_Dictionary.json     (229 entries, bake ALL of them inline)

─────────────────────────────────────────────────────────────────────────────
CONSTRAINTS
─────────────────────────────────────────────────────────────────────────────

1. Do NOT modify any existing _condition_matches handler. Add only.
2. Do NOT create new MongoDB collections. kp_sublord_table.py is a pure Python
   module with baked-in data -- no DB queries, no file I/O at runtime.
3. Do NOT import kp_engine at module level in knowledge_engine.py if it creates
   a circular import. Use a local import inside _populate_kp_facts if needed.
4. The kp_signification algorithm in _populate_kp_facts uses ChartFacts.house_lords
   and ChartFacts.house_planets ONLY -- do not call build_birth_snapshot() or
   any other kp_engine function that requires jd/lat/lon at this stage.
5. Rahu and Ketu have no house lordship. Skip the lordship contribution (+2 and +1)
   for these two planets in the signification scoring.
6. smart-quote sanitisation: run scripts/sanitise-smart-quotes.sh on all new .py
   files before commit.
7. ENGINE_VERSION in panchang_router.py must be bumped before committing backend changes.

─────────────────────────────────────────────────────────────────────────────
DELIVERY FORMAT
─────────────────────────────────────────────────────────────────────────────

Deliver as a single diff or individual file patches for:
  backend/kp_sublord_table.py    (new -- complete file)
  backend/knowledge_engine.py    (patch -- ChartFacts + extract_chart_facts +
                                   _condition_matches additions only)
  backend/knowledge_schema.py    (patch -- secondary_axis field + validator)
  backend/ke_schema_constants.py (patch -- VALID_CLAIM_AXES additions)

Include test cases for AC-1 through AC-8 in:
  tests/test_ke_kp_conditions.py  (new test file)

Do NOT include a migration/backfill script for secondary_axis -- existing rules
have secondary_axis=None by default (Optional field). No DB migration needed.
