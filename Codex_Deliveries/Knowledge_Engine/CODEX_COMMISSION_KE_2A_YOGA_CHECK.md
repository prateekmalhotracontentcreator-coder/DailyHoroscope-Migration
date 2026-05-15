# Commission KE-2A -- Knowledge Engine: Yoga Check Evaluation Engine

> EverydayHoroscope · Stack: FastAPI, Python 3.12, MongoDB
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Date issued: 2026-05-15

---

CODEX COMMISSION BRIEF -- KE Phase 2A  
Knowledge Engine -- Yoga Check Evaluation Engine  
New file:    backend/ke_yoga_evaluator.py  
Integration: backend/knowledge_engine.py  (_condition_matches -- one line addition)  
────────────────────────────────────────────────────────────────────────────────

CONTEXT  
-------  
The EverydayHoroscope Knowledge Engine (knowledge_engine.py) is a MongoDB-backed  
rules library. Collection: horoscope_db.interpretation_rules. It holds 6,000+  
ingested rules covering BPHS Chapters 35-41, Lal Kitab Ch 19, and Dasha chapters.

The engine infrastructure is complete: rule fetching, scoring, narrative generation.  
The missing layer is yoga evaluation -- determining whether a combination is present  
in a native's birth chart before the rule fires.

Every rule stores its conditions with:  
  condition.type = "yoga_combination"  
  condition.sub_conditions = []   (always empty)  
  condition.yoga_check.type = "\<one of 16 evaluator types>"  
  condition.yoga_check.checkable = true | false

The existing _condition_matches() in knowledge_engine.py has no handler for  
"yoga_combination" -- it falls through to return False. Zero rules are evaluated  
against any birth chart today.

────────────────────────────────────────────────────────────────────────────────  
EXISTING INFRASTRUCTURE -- DO NOT DUPLICATE  
────────────────────────────────────────────────────────────────────────────────

All of the following already exist in knowledge_engine.py. Read them. Reuse them.  
Do not rewrite them.

ChartFacts dataclass (lines 281-291 of knowledge_engine.py):  
  planet_positions : dict  -- planet name -> {house, sign, dignity, retrograde}  
  house_lords      : dict  -- house number (int) -> planet name  
  aspect_targets   : dict  -- planet name -> set of house numbers it aspects  
  aspected_by      : dict  -- house number -> set of planet names aspecting it  
  house_planets    : dict  -- house number -> list of planet names in it  
  yogas            : set   -- matched yoga names (strings)  
  dasha_levels     : dict  -- planet name -> dasha level

extract_chart_facts(chart: dict) -> ChartFacts  
  Call this to build ChartFacts from a raw chart dict. Already implemented.

_vedic_aspect_targets(planet: str, house: int) -> set[int]  
  Returns houses that planet (in house) aspects. Already implemented.  
  Mars   : {4, 7, 8} relative offsets applied to house position  
  Jupiter: {5, 7, 9}  
  Saturn : {3, 7, 10}  
  Rahu   : {5, 7, 9}  
  Ketu   : {5, 7, 9}  
  Others : {7}  
  (All inclusive, 1-indexed house numbers.)

_condition_matches(condition: dict, facts: ChartFacts) -> bool  
  Already handles: planet_in_house, planet_in_sign, planet_aspect,  
  planet_conjunction, planet_dignity, planet_retrograde, house_lord_in_house,  
  yoga, dasha_period, composite (AND/OR of sub_conditions).  
  DO NOT modify any existing case. Only ADD the yoga_combination dispatch below.

Reference constants in vedic_calculator.py:  
  SIGN_ORDER = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra',  
                'Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']  
  SIGN_LORDS = {'Aries':'Mars','Taurus':'Venus','Gemini':'Mercury',  
                'Cancer':'Moon','Leo':'Sun','Virgo':'Mercury','Libra':'Venus',  
                'Scorpio':'Mars','Sagittarius':'Jupiter','Capricorn':'Saturn',  
                'Aquarius':'Saturn','Pisces':'Jupiter'}

Reference constants in kundali_router.py:  
  EXALTATION_SIGNS = {Sun:'Aries', Moon:'Taurus', Mars:'Capricorn',  
                      Mercury:'Virgo', Jupiter:'Cancer', Venus:'Pisces',  
                      Saturn:'Libra'}  
  _dignity(planet_name, sign) -> str  ('own_sign','exalted','debilitated','')

────────────────────────────────────────────────────────────────────────────────  
DELIVERABLE  
────────────────────────────────────────────────────────────────────────────────

New file: backend/ke_yoga_evaluator.py

Entry function:  
  def evaluate_yoga_check(condition: dict, facts: ChartFacts) -> YogaCheckResult

Result dataclass (define in ke_yoga_evaluator.py):  
  @dataclass  
  class YogaCheckResult:  
      matched       : bool  
      confidence    : float        # 0.0 to 1.0  
      evidence      : list[str]    # human-readable reasons  
      yoga_check_type: str         # which evaluator was used  
      checkable     : bool = True  # False when yoga_check.checkable is False

Guard clause -- apply before any evaluation:  
  If condition["yoga_check"].get("checkable") is False:  
    return YogaCheckResult(  
        matched=False, confidence=0.0,  
        evidence=["Rule not yet checkable"],  
        yoga_check_type=condition["yoga_check"]["type"],  
        checkable=False  
    )

────────────────────────────────────────────────────────────────────────────────  
INTEGRATION POINT IN knowledge_engine.py  
────────────────────────────────────────────────────────────────────────────────

Add exactly ONE new case inside _condition_matches(). Do not change anything else.

  elif condition_type == "yoga_combination":  
      from ke_yoga_evaluator import evaluate_yoga_check  
      return evaluate_yoga_check(condition, facts).matched

────────────────────────────────────────────────────────────────────────────────  
MODULE-LEVEL CONSTANTS  (define once at top of ke_yoga_evaluator.py)  
────────────────────────────────────────────────────────────────────────────────

NATURAL_BENEFICS  = {"Moon", "Mercury", "Venus", "Jupiter"}  
NATURAL_MALEFICS  = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}  
ANGULAR_HOUSES    = {1, 4, 7, 10}  
TRINAL_HOUSES     = {1, 5, 9}  
SEVEN_PLANETS     = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]

SIGN_QUALITY = {  
    "movable": {"Aries","Cancer","Libra","Capricorn"},  
    "fixed"  : {"Taurus","Leo","Scorpio","Aquarius"},  
    "dual"   : {"Gemini","Virgo","Sagittarius","Pisces"},  
}  
ODD_SIGNS  = {"Aries","Gemini","Leo","Libra","Sagittarius","Aquarius"}  
EVEN_SIGNS = {"Taurus","Cancer","Virgo","Scorpio","Capricorn","Pisces"}

────────────────────────────────────────────────────────────────────────────────  
THE 16 EVALUATOR TYPES  
────────────────────────────────────────────────────────────────────────────────

Dispatch from evaluate_yoga_check() via:

  EVALUATOR_DISPATCH = {  
      "planetary_combination"     : _eval_planetary_combination,  
      "planet_in_house"           : _eval_planet_in_house,  
      "multi_house_requirements"  : _eval_multi_house_requirements,  
      "benefics_in_houses"        : _eval_benefics_in_houses,  
      "malefics_in_houses"        : _eval_malefics_in_houses,  
      "benefic_only_in_house"     : _eval_benefic_only_in_house,  
      "planet_in_kendra_from"     : _eval_planet_in_kendra_from,  
      "sign_quality_all"          : _eval_sign_quality_all,  
      "angles_by_planet_type"     : _eval_angles_by_planet_type,  
      "planets_in_n_signs"        : _eval_planets_in_n_signs,  
      "all_planets_in_alt_signs"  : _eval_all_planets_in_alt_signs,  
      "all_planets_in_houses"     : _eval_all_planets_in_houses,  
      "planet_in_house_from_moon" : _eval_planet_in_house_from_moon,  
      "kemadruma_check"           : _eval_kemadruma_check,  
      "moon_from_sun_position"    : _eval_moon_from_sun_position,  
      "dosha"                     : _eval_dosha,  
  }

────────────────────────────────────────────────────────────────────────────────  
TYPE 1: planetary_combination  
Source rules: BPHS Ch 41 rules 001-014 (Wealth Axis \+ Own-Sign Lagna yogas)  
────────────────────────────────────────────────────────────────────────────────

Used when: a set of planets must occupy specified houses, with optional ascendant  
filter and optional activation (conjunction or aspect by a list of planets).

Parameters format (structured, for future rules):  
  {  
    "type": "planetary_combination",  
    "planets_in_houses": [{"planet": "Venus", "house": 5}, {"planet": "Mars", "house": 11}],  
    "ascendant_filter": ["Capricorn","Gemini"],  
    "activation_planets": ["Mars","Jupiter"],  
    "activation_mode": "conjunction_or_aspect"  
  }

Evaluation logic:  
  1. If ascendant_filter present:  
       lagna_sign = facts.planet_positions.get("Lagna",{}).get("sign")  
       If lagna_sign not in ascendant_filter -> matched=False  
  2. For each {planet, house} pair:  
       facts.planet_positions.get(planet,{}).get("house") == house  
       All pairs must pass (AND logic)  
  3. If activation_planets present (activation_mode = "conjunction_or_aspect"):  
       primary_house = house of the first planet in planets_in_houses  
       Each activation planet must EITHER:  
         a. Be in the same house as primary planet (conjunction):  
              facts.planet_positions.get(act_planet,{}).get("house") == primary_house  
         b. Aspect the primary_house:  
              primary_house in facts.aspect_targets.get(act_planet, set())  
       ALL activation planets must satisfy (a) or (b).

Ch 41 rules 001-014 do not carry structured parameters -- use this lookup table:

  CH41_COMBINATIONS = {  
    "Venus-Mars Wealth Axis -- 5th/11th Own-Sign": {  
        "ascendant_filter": ["Capricorn","Gemini"],  
        "planets_in_houses": [("Venus",5),("Mars",11)]},  
    "Mercury-Jupiter-Moon-Mars Wealth Axis -- 5th/11th Own-Sign": {  
        "ascendant_filter": ["Aquarius","Taurus"],  
        "planets_in_houses": [("Mercury",5),("Moon",11),("Mars",11),("Jupiter",11)]},  
    "Sun-Saturn-Moon-Jupiter Wealth Axis -- 5th/11th Own-Sign": {  
        "ascendant_filter": ["Aries"],  
        "planets_in_houses": [("Sun",5),("Saturn",11),("Moon",11),("Jupiter",11)]},  
    "Saturn-Sun-Moon Wealth Axis -- 5th/11th Own-Sign": {  
        "ascendant_filter": ["Virgo","Libra"],  
        "planets_in_houses": [("Saturn",5),("Sun",11),("Moon",11)]},  
    "Jupiter-Mercury Wealth Axis -- 5th/11th Own-Sign": {  
        "ascendant_filter": ["Leo","Scorpio"],  
        "planets_in_houses": [("Jupiter",5),("Mercury",11)]},  
    "Mars-Venus Wealth Axis -- 5th/11th Own-Sign": {  
        "ascendant_filter": ["Cancer","Sagittarius"],  
        "planets_in_houses": [("Mars",5),("Venus",11)]},  
    "Moon-Saturn Wealth Axis -- 5th/11th Own-Sign": {  
        "ascendant_filter": ["Pisces"],  
        "planets_in_houses": [("Moon",5),("Saturn",11)]},  
    "Sun Wealth Engine -- Leo Ascendant Own-Sign": {  
        "ascendant_filter": ["Leo"],  
        "planets_in_houses": [("Sun",1)],  
        "activation_planets": ["Mars","Jupiter"],  
        "activation_mode": "conjunction_or_aspect"},  
    "Moon Wealth Engine -- Cancer Ascendant Own-Sign": {  
        "ascendant_filter": ["Cancer"],  
        "planets_in_houses": [("Moon",1)],  
        "activation_planets": ["Mercury","Jupiter"],  
        "activation_mode": "conjunction_or_aspect"},  
    "Mars Wealth Engine -- Aries/Scorpio Ascendant Own-Sign": {  
        "ascendant_filter": ["Aries","Scorpio"],  
        "planets_in_houses": [("Mars",1)],  
        "activation_planets": ["Mercury","Venus","Saturn"],  
        "activation_mode": "conjunction_or_aspect"},  
    "Mercury Wealth Engine -- Gemini/Virgo Ascendant Own-Sign": {  
        "ascendant_filter": ["Gemini","Virgo"],  
        "planets_in_houses": [("Mercury",1)],  
        "activation_planets": ["Saturn","Jupiter"],  
        "activation_mode": "conjunction_or_aspect"},  
    "Jupiter Wealth Engine -- Sagittarius/Pisces Ascendant Own-Sign": {  
        "ascendant_filter": ["Sagittarius","Pisces"],  
        "planets_in_houses": [("Jupiter",1)],  
        "activation_planets": ["Mercury","Mars"],  
        "activation_mode": "conjunction_or_aspect"},  
    "Venus Wealth Engine -- Taurus/Libra Ascendant Own-Sign": {  
        "ascendant_filter": ["Taurus","Libra"],  
        "planets_in_houses": [("Venus",1)],  
        "activation_planets": ["Saturn","Mercury"],  
        "activation_mode": "conjunction_or_aspect"},  
    "Saturn Wealth Engine -- Capricorn/Aquarius Ascendant Own-Sign": {  
        "ascendant_filter": ["Capricorn","Aquarius"],  
        "planets_in_houses": [("Saturn",1)],  
        "activation_planets": ["Mars","Jupiter"],  
        "activation_mode": "conjunction_or_aspect"},  
  }

If yoga_name not found in table and no structured parameters:  
  return matched=False, confidence=0.0,  
         evidence=["Parameters not yet structured for this yoga_name"]

────────────────────────────────────────────────────────────────────────────────  
TYPE 2: planet_in_house  
Source rules: BPHS Ch 36, Lal Kitab Ch 19  
────────────────────────────────────────────────────────────────────────────────

Parameters: {"planet": "Jupiter", "house": 7}  
Logic:      facts.planet_positions.get(planet, {}).get("house") == house

────────────────────────────────────────────────────────────────────────────────  
TYPE 3: multi_house_requirements  
Source rules: BPHS Ch 36, Ch 38, Lal Kitab Ch 19  
────────────────────────────────────────────────────────────────────────────────

Parameters:  
  {"requirements": [{"planet": "Venus", "house": 2}, {"planet": "Jupiter", "house": 5}]}  
Logic: ALL requirements must pass (AND). Each:  
  facts.planet_positions.get(planet, {}).get("house") == house

────────────────────────────────────────────────────────────────────────────────  
TYPE 4: benefics_in_houses  
Source rules: BPHS Ch 36, Ch 37  
────────────────────────────────────────────────────────────────────────────────

Parameters: {"houses": [1,4,7,10]}  or  {"houses": [1,4,7,10], "min_count": 3}  
Logic:  
  For each planet in NATURAL_BENEFICS:  
    house = facts.planet_positions.get(planet, {}).get("house")  
  If min_count absent: ALL benefics must be in the house set.  
  If min_count present: at least min_count benefics in the house set.

────────────────────────────────────────────────────────────────────────────────  
TYPE 5: malefics_in_houses  
Source rules: BPHS Ch 36 (Asubha Yoga)  
────────────────────────────────────────────────────────────────────────────────

Parameters: {"houses": [1,4,7,10]}  
Logic: same pattern as Type 4 but for NATURAL_MALEFICS.

────────────────────────────────────────────────────────────────────────────────  
TYPE 6: benefic_only_in_house  
Source rules: BPHS Ch 36 (Amala Yoga)  
────────────────────────────────────────────────────────────────────────────────

Parameters: {"house": 10}  
Logic:  
  house_planets = facts.house_planets.get(house, [])  
  has_benefic   = any(p in NATURAL_BENEFICS for p in house_planets)  
  has_malefic   = any(p in NATURAL_MALEFICS for p in house_planets)  
  matched = has_benefic and not has_malefic

────────────────────────────────────────────────────────────────────────────────  
TYPE 7: planet_in_kendra_from  
Source rules: BPHS Ch 36 (Gajakesari, Hamsa yoga)  
────────────────────────────────────────────────────────────────────────────────

Parameters:  
  {"planet": "Jupiter", "reference": "Moon", "positions": [1,4,7,10]}  
  reference may be a planet name or "Lagna".

Logic:  
  planet_house = facts.planet_positions.get(planet, {}).get("house")  
  if reference == "Lagna": ref_house = 1  
  else: ref_house = facts.planet_positions.get(reference, {}).get("house")  
  dist = ((planet_house - ref_house \+ 12) % 12) \+ 1  
  matched = dist in positions

────────────────────────────────────────────────────────────────────────────────  
TYPE 8: sign_quality_all  
Source rules: BPHS Ch 35 (Rajju, Musala, Nala -- Nabhasa yogas)  
────────────────────────────────────────────────────────────────────────────────

Parameters: {"quality": "movable"}   # "movable" | "fixed" | "dual"  
Logic: for each planet in SEVEN_PLANETS:  
  sign = facts.planet_positions.get(planet, {}).get("sign")  
  sign must be in SIGN_QUALITY[quality]  
All 7 must pass.

NABHASA_QUALITY_MAP (for lookup by yoga_name if parameters absent):  
  "Rajju Yoga" -> "movable"  
  "Musala Yoga" -> "fixed"  
  "Nala Yoga"  -> "dual"

────────────────────────────────────────────────────────────────────────────────  
TYPE 9: angles_by_planet_type  
Source rules: BPHS Ch 35 (Maala Yoga, Sarpa Yoga)  
────────────────────────────────────────────────────────────────────────────────

Parameters:  
  {"planet_type": "benefic", "required_houses": [1,4,7,10], "requires_all": true}  
Logic:  
  If planet_type == "benefic": check_planets = NATURAL_BENEFICS  
  If planet_type == "malefic": check_planets = NATURAL_MALEFICS  
  If requires_all: ALL check_planets must have house in required_houses.  
  Else: ANY check_planet in required_houses.

────────────────────────────────────────────────────────────────────────────────  
TYPE 10: planets_in_n_signs  
Source rules: BPHS Ch 35 (Kedara, Parvata -- Nabhasa yogas)  
────────────────────────────────────────────────────────────────────────────────

Parameters: {"n": 4}  
Logic:  
  occupied = set(facts.planet_positions[p]["sign"]  
                 for p in SEVEN_PLANETS  
                 if facts.planet_positions.get(p, {}).get("sign"))  
  matched = len(occupied) == n

────────────────────────────────────────────────────────────────────────────────  
TYPE 11: all_planets_in_alt_signs  
Source rules: BPHS Ch 35 (Nabhasa yogas with odd/even sign constraint)  
────────────────────────────────────────────────────────────────────────────────

Parameters: {"sign_parity": "odd"}   # "odd" | "even"  
Logic:  
  target = ODD_SIGNS if sign_parity == "odd" else EVEN_SIGNS  
  For each planet in SEVEN_PLANETS:  
    facts.planet_positions.get(planet, {}).get("sign") must be in target.

────────────────────────────────────────────────────────────────────────────────  
TYPE 12: all_planets_in_houses  
Source rules: BPHS Ch 35 (Yuga, Shoola -- Nabhasa yogas)  
────────────────────────────────────────────────────────────────────────────────

Parameters: {"houses": [1,2,3,4,5,6]}  
Logic: for each planet in SEVEN_PLANETS:  
  facts.planet_positions.get(planet, {}).get("house") must be in houses.

────────────────────────────────────────────────────────────────────────────────  
TYPE 13: planet_in_house_from_moon  
Source rules: BPHS Ch 37 (Sunapha, Anapha, Vesi, Vasi yogas)  
────────────────────────────────────────────────────────────────────────────────

Parameters:  
  {"planet": "any_except_sun", "distance_from_moon": 2}  
  planet may be: a specific planet name | "any_except_sun" | "any_benefic"

Logic:  
  moon_house = facts.planet_positions["Moon"]["house"]  
  For each candidate planet (resolved from planet parameter):  
    dist = ((candidate_house - moon_house \+ 12) % 12) \+ 1  
    If dist == distance_from_moon -> matched = True (any match suffices)

Resolve "any_except_sun":  
  candidates = [p for p in facts.planet_positions  
                if p not in ("Sun","Lagna","Moon")]  
Resolve "any_benefic": candidates = list(NATURAL_BENEFICS)

────────────────────────────────────────────────────────────────────────────────  
TYPE 14: kemadruma_check  
Source rules: BPHS Ch 37 (Kemadruma Yoga)  
────────────────────────────────────────────────────────────────────────────────

Parameters: {"strict": false}  
Logic:  
  moon_house        = facts.planet_positions["Moon"]["house"]  
  second_from_moon  = (moon_house % 12) \+ 1  
  twelfth_from_moon = ((moon_house - 2) % 12) \+ 1  
  planets_in_2nd  = facts.house_planets.get(second_from_moon, [])  
  planets_in_12th = facts.house_planets.get(twelfth_from_moon, [])  
  Kemadruma = both lists are empty (no planets in 2nd or 12th from Moon).  
  If strict == True: additionally Moon's house must NOT be in ANGULAR_HOUSES.

────────────────────────────────────────────────────────────────────────────────  
TYPE 15: moon_from_sun_position  
Source rules: BPHS Ch 37 (Vesi, Vasi, Ubhayachari yogas)  
────────────────────────────────────────────────────────────────────────────────

Parameters:  
  {"reference": "Sun", "target_distances": [2], "requires_benefic": true}  
Logic:  
  sun_house = facts.planet_positions["Sun"]["house"]  
  For each target_distance:  
    target_house = ((sun_house \+ target_distance - 2) % 12) \+ 1  
    planets_there = facts.house_planets.get(target_house, [])  
    If requires_benefic:  
      matched = any(p in NATURAL_BENEFICS for p in planets_there)  
    Else:  
      matched = len([p for p in planets_there if p not in ("Sun","Lagna")]) > 0

────────────────────────────────────────────────────────────────────────────────  
TYPE 16: dosha  
Source rules: Lal Kitab Ch 19  
────────────────────────────────────────────────────────────────────────────────

Parameters: {"planet": "Saturn", "house": 1, "dosha_type": "negative_placement"}  
Logic: facts.planet_positions.get(planet, {}).get("house") == house  
Note: dosha_type is a label only -- does not affect the boolean check.

────────────────────────────────────────────────────────────────────────────────  
REFERENCE FILES  (share all of these with Codex before starting)  
────────────────────────────────────────────────────────────────────────────────

• backend/knowledge_engine.py  
    Read: ChartFacts (lines 281-291), extract_chart_facts signature,  
          _condition_matches structure, _vedic_aspect_targets implementation  
• backend/kundali_router.py  
    Read: EXALTATION_SIGNS, _dignity() function  
• backend/vedic_calculator.py  
    Read: SIGN_ORDER, SIGN_LORDS definitions  
• backend/scripts/bphs_ch35_rules.json  
    Sample rules: sign_quality_all, angles_by_planet_type, planets_in_n_signs  
• backend/scripts/bphs_ch36_rules.json  
    Sample rules: benefics_in_houses, planet_in_kendra_from, benefic_only_in_house  
• backend/scripts/bphs_ch37_rules.json  
    Sample rules: kemadruma_check, planet_in_house_from_moon, moon_from_sun_position  
• backend/scripts/bphs_ch41_rules.json  
    Sample rules: planetary_combination (Ch 41 wealth and lagna yogas)  
• backend/scripts/lalkitab_ch19_rules.json  
    Sample rules: dosha, multi_house_requirements

────────────────────────────────────────────────────────────────────────────────  
CONSTRAINTS  (never violate)  
────────────────────────────────────────────────────────────────────────────────

• DO NOT modify vedic_calculator.py -- astronomical layer, immutable  
• DO NOT modify any existing case in _condition_matches() -- add only one new case  
• DO NOT import from knowledge_engine.py inside ke_yoga_evaluator.py  
    (circular import risk -- import ChartFacts via TYPE_CHECKING guard or  
     accept it as a plain dict parameter)  
• DO NOT call any AI/LLM API -- all logic must be pure deterministic Python  
• DO NOT change MongoDB document structure -- evaluate rules as stored  
• All planet name strings must match normalize_planet_name() output exactly:  
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",  
    "Saturn", "Rahu", "Ketu"

────────────────────────────────────────────────────────────────────────────────  
STYLE REQUIREMENTS  
────────────────────────────────────────────────────────────────────────────────

• Straight ASCII quotes throughout -- no curly/smart quotes  
• Python 3.10+ -- use match/case or dict dispatch, not long if/elif chains  
• Type hints on all public functions  
• No external dependencies -- standard library \+ existing project imports only  
• Each private evaluator function (_eval_*) must be under 30 lines

────────────────────────────────────────────────────────────────────────────────  
ACCEPTANCE CRITERIA  
────────────────────────────────────────────────────────────────────────────────

1.  ke_yoga_evaluator.py exists and imports cleanly with no circular import errors  
2.  evaluate_yoga_check() dispatches correctly to all 16 evaluator types  
3.  Guard clause returns checkable=False for rules where yoga_check.checkable=False  
4.  Type 1 (planetary_combination) evaluates all 14 Ch 41 yoga names via lookup table  
5.  Type 7 (planet_in_kendra_from) correctly handles both planet and "Lagna" reference  
6.  Type 14 (kemadruma_check) correctly identifies empty 2nd and 12th from Moon  
7.  All 16 evaluators return YogaCheckResult with populated evidence list  
8.  The one-line addition to knowledge_engine.py _condition_matches() dispatches  
    yoga_combination to evaluate_yoga_check and returns result.matched  
9.  tests/test_ke_yoga_evaluator.py -- minimum 32 tests (positive \+ negative per type)  
    All tests pass: pytest tests/test_ke_yoga_evaluator.py  
10. No changes to any file other than ke_yoga_evaluator.py, knowledge_engine.py  
    (_condition_matches one line), and tests/test_ke_yoga_evaluator.py  
────────────────────────────────────────────────────────────────────────────────  
