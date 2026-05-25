from __future__ import annotations

from datetime import date
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, field_validator


router = APIRouter(prefix="/api/lo-shu", tags=["lo-shu"])

GRID_ROWS: tuple[tuple[int, int, int], ...] = (
    (4, 9, 2),
    (3, 5, 7),
    (8, 1, 6),
)

PYTHAGOREAN_MAP = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "O": 6, "P": 7, "Q": 8, "R": 9,
    "S": 1, "T": 2, "U": 3, "V": 4, "W": 5, "X": 6, "Y": 7, "Z": 8,
}

NUMBER_REFERENCE: dict[int, dict[str, str]] = {
    1: {"planet": "Sun", "day": "Sunday", "archetype": "King"},
    2: {"planet": "Moon", "day": "Monday", "archetype": "Queen"},
    3: {"planet": "Jupiter", "day": "Thursday", "archetype": "Devguru"},
    4: {"planet": "Rahu", "day": "Saturday", "archetype": "Path Breaker"},
    5: {"planet": "Mercury", "day": "Wednesday", "archetype": "Prince"},
    6: {"planet": "Venus", "day": "Friday", "archetype": "Harmoniser"},
    7: {"planet": "Ketu", "day": "Tuesday", "archetype": "Mystic"},
    8: {"planet": "Saturn", "day": "Saturday", "archetype": "Judge"},
    9: {"planet": "Mars", "day": "Tuesday", "archetype": "Warrior"},
}

NUMBER_CLASSICAL_ASSOCIATIONS: dict[int, dict[str, Any]] = {
    1: {
        "element": "Water",
        "direction": "North",
        "colours": ["black", "dark blue"],
        "body_area": "kidneys and ears",
        "family_role": "middle son",
        "life_theme": "career, communication, and initiative",
    },
    2: {
        "element": "Earth",
        "direction": "South-West",
        "colours": ["pink", "red", "white"],
        "body_area": "abdomen",
        "family_role": "mother",
        "life_theme": "love, marriage, intuition, and partnership",
    },
    3: {
        "element": "Wood",
        "direction": "East",
        "colours": ["green", "blue"],
        "body_area": "feet, ankles, and knees",
        "family_role": "eldest son",
        "life_theme": "planning, memory, study, and growth",
    },
    4: {
        "element": "Soft Wood",
        "direction": "South-East",
        "colours": ["red", "green", "blue", "purple", "gold"],
        "body_area": "thighs and liver",
        "family_role": "eldest daughter",
        "life_theme": "wealth, structure, discipline, and practical effort",
    },
    5: {
        "element": "Earth",
        "direction": "Center",
        "colours": ["yellow", "brown", "orange"],
        "body_area": "internal organs",
        "family_role": "whole family",
        "life_theme": "balance, stability, speech, and adaptability",
    },
    6: {
        "element": "Hard Metal",
        "direction": "North-West",
        "colours": ["black", "white"],
        "body_area": "head",
        "family_role": "father",
        "life_theme": "home, responsibility, contracts, and support",
    },
    7: {
        "element": "Soft Metal",
        "direction": "West",
        "colours": ["white", "silver", "gray", "copper"],
        "body_area": "mouth and lungs",
        "family_role": "youngest daughter",
        "life_theme": "creativity, reflection, and lessons through experience",
    },
    8: {
        "element": "Earth",
        "direction": "North-East",
        "colours": ["blue", "black", "green"],
        "body_area": "hands and body weight",
        "family_role": "youngest son",
        "life_theme": "knowledge, endurance, discipline, and education",
    },
    9: {
        "element": "Fire",
        "direction": "South",
        "colours": ["red"],
        "body_area": "heart, blood, and eyes",
        "family_role": "middle daughter",
        "life_theme": "fame, courage, energy, and visibility",
    },
}

NUMBER_DEEP_DIVE_BLUEPRINTS: dict[int, dict[str, Any]] = {
    1: {
        "intro": "Lo Shu number 1 carries the charge of initiative, self-definition, and the urge to move first. In the source material it is tied to communication, confidence, and career movement.",
        "present_once": "A single 1 usually gives healthy independence, a clear personal spark, and the courage to begin new things. It often strengthens direct communication and the need to stand on your own feet.",
        "repeat_guidance": "When 1 repeats, confidence and self-assertion amplify. Two 1s often improve articulation and initiative, while three or more can swing toward stubbornness, dominance, or difficulty relaxing enough to truly listen.",
        "balancing_tips": [
            "Use sunlight, early starts, and visible goals to channel the number instead of forcing outcomes.",
            "Practice speaking clearly without over-talking; strong 1 energy matures through clean self-expression.",
            "Balance independence with collaboration so leadership does not harden into isolation.",
        ],
        "famous_personalities": [],
    },
    2: {
        "intro": "Lo Shu number 2 is the field of sensitivity, partnership, and emotional intelligence. The classical references link it with love, marriage, intuition, and the Moon's reflective quality.",
        "present_once": "A single 2 usually supports empathy, cooperation, and the ability to read emotional tone. It can strengthen relationship awareness and make someone easier to work with.",
        "repeat_guidance": "When 2 repeats, intuition becomes sharper but emotional permeability rises too. Two 2s can feel gifted and perceptive, while three or more may create hypersensitivity, self-doubt, or withdrawal after emotional hurt.",
        "balancing_tips": [
            "Protect your emotional rhythm with clear boundaries instead of absorbing every room you enter.",
            "Choose collaboration intentionally; not every partnership deserves full emotional access.",
            "Calm Moon rituals like journaling, hydration, or slower evenings help 2 stay steady.",
        ],
        "famous_personalities": [],
    },
    3: {
        "intro": "Lo Shu number 3 is linked with memory, planning, expression, and intellectual growth. Source material also ties it to education, creative thinking, and the expanding wisdom of Jupiter.",
        "present_once": "A single 3 often gives good mental recall, curiosity, and a natural ability to learn by connecting ideas. It strengthens planning, teaching, and expressive intelligence.",
        "repeat_guidance": "When 3 repeats, imagination and mental activity intensify. Two 3s often boost creativity and writing ability, while three or more can drift into over-thinking, fantasy loops, or brilliance that is not always grounded in action.",
        "balancing_tips": [
            "Pair every idea with one practical next step so imagination has somewhere to land.",
            "Use study, teaching, or writing as a structured outlet for excess mental energy.",
            "If you feel mentally scattered, come back to body movement before doing more thinking.",
        ],
        "famous_personalities": [],
    },
    4: {
        "intro": "Lo Shu number 4 represents structure, detail, wealth-building discipline, and the capacity to work with systems. In the source texts it is practical, hands-on, and strongly tied to organised effort.",
        "present_once": "A single 4 usually supports order, follow-through, and a fact-based relationship with work. It can strengthen planning, craft, and the ability to build something tangible over time.",
        "repeat_guidance": "When 4 repeats, discipline becomes a major life signature. Two 4s often create strong organisational power, while three or more can turn into overwork, rigidity, or an overly physical approach that leaves little room for flexibility.",
        "balancing_tips": [
            "Keep structure supportive, not punitive; routines should create momentum, not fear.",
            "Work with your hands or environment to stabilise 4 without becoming harsh or mechanical.",
            "Introduce creative or relational softness if duty starts replacing joy.",
        ],
        "famous_personalities": [],
    },
    5: {
        "intro": "Lo Shu number 5 sits at the center of the grid and is the balancing force. It is connected with communication, emotional steadiness, freedom, and the capacity to move between life's demands without losing center.",
        "present_once": "A single 5 usually gives emotional balance, social flexibility, and the ability to steady others. It often helps with speech, adaptability, and keeping different parts of life in conversation with each other.",
        "repeat_guidance": "When 5 repeats, freedom and intensity increase together. Two 5s can make someone magnetic and driven, while three or more may become reactive, impulsive in speech, or too restless to stay with one path for long.",
        "balancing_tips": [
            "Use movement, sunlight, and varied-but-clear routines to keep 5 alive without becoming chaotic.",
            "Pause before speaking when emotions are high; overactive 5 can cut before it clarifies.",
            "Give yourself healthy novelty instead of creating drama just to feel movement.",
        ],
        "famous_personalities": [],
    },
    6: {
        "intro": "Lo Shu number 6 governs home, family care, responsibility, and the desire to create beauty or protection around loved ones. In the source set it also touches contracts, friendship, and supportive relational roles.",
        "present_once": "A single 6 often gives a caring domestic instinct, creative warmth, and the ability to hold responsibility with heart. It commonly strengthens family loyalty and the wish to make life feel more harmonious.",
        "repeat_guidance": "When 6 repeats, love and care become stronger, but so can worry. Two 6s often heighten creativity and protectiveness, while three or more may become possessive, overly anxious, or emotionally over-involved in everyone else's life.",
        "balancing_tips": [
            "Care for others without making yourself responsible for every outcome.",
            "Keep beauty and order restorative, not perfectionistic.",
            "Schedule real rest; heavy 6 energy tires itself through concern before the body admits it.",
        ],
        "famous_personalities": [],
    },
    7: {
        "intro": "Lo Shu number 7 is the reflective, spiritual, and experience-tested number. The source material repeatedly frames it as learning through disappointment, sensitivity, and a deeper inward intelligence that grows through life lessons.",
        "present_once": "A single 7 usually gives introspection, emotional depth, and a quiet instinct for learning from experience. It can strengthen spiritual curiosity and a preference for meaningful rather than noisy living.",
        "repeat_guidance": "When 7 repeats, the inner life deepens dramatically. Two 7s can sharpen analysis and intuition, while three or more may intensify disappointment patterns, emotional heaviness, or a life path that grows mainly through hard-earned wisdom.",
        "balancing_tips": [
            "Let solitude nourish you, but do not turn every wound into a permanent identity.",
            "Ground intuition in routine, sleep, and reflection instead of waiting for crisis to teach everything.",
            "Channel deep feeling into prayer, study, or healing work so 7 becomes wisdom rather than withdrawal.",
        ],
        "famous_personalities": [
            {"name": "Mahendra Singh Dhoni", "note": "One source uses him as an example of the cool, composed quality linked with strong 7 energy."},
        ],
    },
    8: {
        "intro": "Lo Shu number 8 is linked with endurance, knowledge, regulation, money realism, and the discipline required for long-range outcomes. The source texts also connect it with education, detail, and ethical responsibility.",
        "present_once": "A single 8 often gives method, seriousness, and problem-solving patience. It strengthens attention to detail, disciplined learning, and the ability to build slowly instead of chasing quick proof.",
        "repeat_guidance": "When 8 repeats, ambition and restlessness both increase. Two 8s can make someone highly conscientious, while three or more may become materially fixated, mentally over-busy, or trapped in constant motion without inner ease.",
        "balancing_tips": [
            "Respect the long game; 8 works best when it stops negotiating with shortcuts.",
            "Keep ethics visible in money decisions, because strong 8 magnifies consequence as well as reward.",
            "If restlessness rises, return to one clear priority instead of opening five new fronts.",
        ],
        "famous_personalities": [],
    },
    9: {
        "intro": "Lo Shu number 9 is the number of visibility, humanitarian fire, ambition, and the desire to leave impact. The source texts connect it with fame, recognition, valor, and the energy to finish what one begins.",
        "present_once": "A single 9 usually brings courage, idealism, and a stronger sense of mission. It can support public visibility, protective strength, and the urge to improve life beyond personal comfort alone.",
        "repeat_guidance": "When 9 repeats, drive and emotional intensity increase together. Two 9s can sharpen intelligence and influence, while three or more may become combative, over-heated, or too identified with being right, heroic, or always in motion.",
        "balancing_tips": [
            "Use purpose to guide action; raw force without direction burns through energy too quickly.",
            "Serve something larger than ego so 9 stays noble instead of reactive.",
            "Balance action with cooling practices when anger, impatience, or competitiveness spike.",
        ],
        "famous_personalities": [],
    },
}

MISSING_NUMBER_BLUEPRINTS: dict[int, dict[str, Any]] = {
    1: {
        "effect_summary": "Missing 1 usually points to a softer sense of self-direction. People may hesitate before taking the lead or may wait for outside validation before acting.",
        "traits_affected": ["leadership", "self-confidence", "decision-making", "personal identity"],
        "life_areas_impacted": ["career direction", "self-expression", "public presence"],
        "remedies": [
            "Start Sundays with a clear personal intention instead of reacting to the day.",
            "Spend time in early sunlight or offer a simple gratitude practice at sunrise.",
            "Choose one independent decision each week and follow through without over-seeking approval.",
            "Use warm gold, copper, or saffron accents when you need confidence and visibility.",
        ],
        "affirmation": "I trust my voice, my timing, and my ability to lead my own life.",
        "related_missing": [4, 9],
        "focus_trait": "confidence and leadership",
    },
    2: {
        "effect_summary": "Missing 2 can show up as emotional over-sensitivity on some days and emotional distance on others. Cooperation, patience, and intuition may need conscious nurturing.",
        "traits_affected": ["emotional balance", "intuition", "cooperation", "patience"],
        "life_areas_impacted": ["relationships", "teamwork", "inner calm"],
        "remedies": [
            "Use Mondays for softer pacing, hydration, and emotional check-ins.",
            "Wear white, pearl, or silver tones when you want more calm and receptivity.",
            "Pause before responding in charged situations so instinct can settle into clarity.",
            "Keep a moon journal or evening reflection habit to strengthen emotional awareness.",
        ],
        "affirmation": "I respond with calm, softness, and emotional wisdom.",
        "related_missing": [5, 8],
        "focus_trait": "emotional steadiness",
    },
    3: {
        "effect_summary": "Missing 3 often reduces optimism and expressive warmth. The person may know a lot internally but struggle to share insight with confidence or joy.",
        "traits_affected": ["optimism", "communication", "creative expression", "faith"],
        "life_areas_impacted": ["learning", "mentorship", "public speaking"],
        "remedies": [
            "Reserve Thursdays for study, teaching, or sharing one idea clearly.",
            "Wear yellow or gold when you want to feel brighter and more expressive.",
            "Practice speaking one honest thought instead of editing yourself too early.",
            "Create something small each week so inspiration turns into a visible habit.",
        ],
        "affirmation": "My voice carries wisdom, warmth, and generous expression.",
        "related_missing": [4, 8],
        "focus_trait": "expression and optimism",
    },
    4: {
        "effect_summary": "Missing 4 can make life feel less structured than it needs to be. Discipline, consistency, and the ability to build steady systems may require extra attention.",
        "traits_affected": ["discipline", "structure", "consistency", "practical planning"],
        "life_areas_impacted": ["work routines", "planning", "long-term stability"],
        "remedies": [
            "Break big goals into repeatable weekly systems instead of depending on mood.",
            "Use Saturdays for decluttering, grounding, and catching up on unfinished tasks.",
            "Add earthy greens or muted neutrals to workspaces that need focus and steadiness.",
            "Track one habit for 40 days to build rhythm instead of chasing quick results.",
        ],
        "affirmation": "I create stability through steady action and clear structure.",
        "related_missing": [3, 8],
        "focus_trait": "discipline and order",
    },
    5: {
        "effect_summary": "Missing 5 may create mental restlessness, inconsistent communication, or difficulty adapting smoothly to change. Flexibility improves when the mind is grounded first.",
        "traits_affected": ["adaptability", "communication", "mental balance", "versatility"],
        "life_areas_impacted": ["decision-making", "travel", "daily coordination"],
        "remedies": [
            "Use Wednesdays for planning, writing, and finishing open loops.",
            "Keep your schedule simple when too many choices begin to scatter your energy.",
            "Wear fresh green or light mercurial tones when you need clarity and adaptability.",
            "Practice one-minute pauses before speaking so communication becomes cleaner and calmer.",
        ],
        "affirmation": "My mind is flexible, clear, and balanced under change.",
        "related_missing": [2, 6],
        "focus_trait": "adaptability and communication",
    },
    6: {
        "effect_summary": "Missing 6 can show as uneven relationship harmony or discomfort around responsibility, beauty, and emotional reciprocity. Balance grows when care becomes intentional.",
        "traits_affected": ["harmony", "responsibility", "relationship care", "aesthetic balance"],
        "life_areas_impacted": ["love life", "family duties", "home environment"],
        "remedies": [
            "Use Fridays to restore your environment and make one relationship gesture with care.",
            "Bring more softness into daily routines through music, fragrance, or visual order.",
            "Wear cream, rose, or gentle pastel tones when you want relational ease.",
            "Choose one responsibility to complete beautifully rather than many things halfway.",
        ],
        "affirmation": "I give and receive care with grace, steadiness, and love.",
        "related_missing": [5, 9],
        "focus_trait": "harmony and responsibility",
    },
    7: {
        "effect_summary": "Missing 7 may reduce trust in inner guidance. The person can become overly practical, impatient with reflection, or disconnected from the quieter meaning behind events.",
        "traits_affected": ["intuition", "inner reflection", "faith", "spiritual depth"],
        "life_areas_impacted": ["inner life", "healing", "long-term perspective"],
        "remedies": [
            "Protect time for silence, prayer, journaling, or reflective walking every week.",
            "Use Tuesdays for disciplined spiritual practice rather than scattered effort.",
            "Notice repeated patterns in life instead of dismissing every nudge as coincidence.",
            "Choose indigo, sea green, or muted spiritual tones when you want deeper calm.",
        ],
        "affirmation": "I trust the quiet wisdom rising from within me.",
        "related_missing": [2, 3],
        "focus_trait": "intuition and reflection",
    },
    8: {
        "effect_summary": "Missing 8 often weakens endurance, patience, and strategic realism. Opportunities may be present, but long-range discipline can be harder to sustain.",
        "traits_affected": ["endurance", "patience", "material discipline", "strategic maturity"],
        "life_areas_impacted": ["finances", "career growth", "long-term commitments"],
        "remedies": [
            "Treat Saturdays as a reset for budgeting, planning, and reality-checking priorities.",
            "Avoid fast-money temptations and reward yourself for slow, consistent progress.",
            "Use dark blue, charcoal, or grounding tones when you need restraint and seriousness.",
            "Commit to one long game instead of restarting every time results feel delayed.",
        ],
        "affirmation": "I build success through patience, integrity, and steady endurance.",
        "related_missing": [4, 2],
        "focus_trait": "endurance and discipline",
    },
    9: {
        "effect_summary": "Missing 9 can show up as reduced courage, weak follow-through under pressure, or discomfort with direct action. Energy improves when purpose becomes emotionally meaningful.",
        "traits_affected": ["courage", "drive", "assertiveness", "protective strength"],
        "life_areas_impacted": ["conflict handling", "leadership under pressure", "execution"],
        "remedies": [
            "Use Tuesdays for action-oriented tasks you have been postponing.",
            "Move the body regularly so stored frustration turns into healthy momentum.",
            "Wear maroon, red, or copper accents when you need bravery and momentum.",
            "Define the reason behind your action first so courage connects to purpose, not impulse.",
        ],
        "affirmation": "I act with courage, purpose, and clean inner strength.",
        "related_missing": [1, 6],
        "focus_trait": "courage and initiative",
    },
}

ARROW_BLUEPRINTS: dict[str, dict[str, Any]] = {
    "intellect": {
        "name": "Arrow of Intellect",
        "numbers": [4, 9, 2],
        "theme": "Mind plane",
        "effect_present": "A complete 4-9-2 line suggests sharp thinking, strong recall, and the ability to study patterns quickly. This arrow usually supports analysis, mental stamina, and clear situational reading.",
        "effect_missing": "When 4, 9, and 2 are all absent, mental steadiness can feel inconsistent. Focus, retention, and confident analysis usually improve only after deliberate practice and routine.",
        "real_life_traits": ["strong memory", "analytical thinking", "quick pattern recognition", "clear mental framing"],
        "shadow_trait": "Can become mentally rigid or quietly superior when intellect is over-identified with self-worth.",
        "strength_band": "high",
        "aliases": ["mind", "thought-mind", "arrow-of-intellect"],
    },
    "spirituality": {
        "name": "Arrow of Spirituality",
        "numbers": [3, 5, 7],
        "theme": "Soul plane",
        "effect_present": "A complete 3-5-7 line brings emotional depth, intuition, and a stronger pull toward meaning. It often supports empathy, reflection, creativity, and a quieter spiritual intelligence.",
        "effect_missing": "If 3, 5, and 7 are all absent, emotional isolation can build over time. Joy, empathy, and inner connection may need to be developed intentionally rather than arriving naturally.",
        "real_life_traits": ["intuition", "compassion", "emotional sensitivity", "creative depth"],
        "shadow_trait": "Can feel too porous or idealistic if emotional boundaries are weak.",
        "strength_band": "high",
        "aliases": ["spiritual", "soul", "willpower", "body-soul", "arrow-of-spirituality"],
    },
    "prosperity": {
        "name": "Arrow of Prosperity",
        "numbers": [8, 1, 6],
        "theme": "Practical plane",
        "effect_present": "A complete 8-1-6 line supports work ethic, completion energy, and stronger material execution. It often appears in people who can organise effort and build visible results over time.",
        "effect_missing": "When 8, 1, and 6 are all absent, ambition may fade or scatter. Financial decisions can become reactive, and shortcuts may look more attractive than patient progress.",
        "real_life_traits": ["practical effort", "business instinct", "task completion", "material organisation"],
        "shadow_trait": "Can become overly status-driven or too focused on outcomes over inner balance.",
        "strength_band": "high",
        "aliases": ["activity", "physical", "prosperity-plane", "arrow-of-prosperity"],
    },
    "planner": {
        "name": "Arrow of Planner",
        "numbers": [4, 3, 8],
        "theme": "Thought column",
        "effect_present": "A full 4-3-8 column is excellent for systems thinking, preparation, and planning ahead. It gives a strategic mindset that prefers structure, sequencing, and long-range positioning.",
        "effect_missing": "If 4, 3, and 8 are missing together, life can feel disorganised or directionless. Ideas may appear, but the system required to hold them is usually underdeveloped.",
        "real_life_traits": ["discipline", "strategic planning", "organisation", "future focus"],
        "shadow_trait": "Can turn shrewd, overly controlling, or politically calculating when balance is lost.",
        "strength_band": "high",
        "aliases": ["thought", "thought-plane", "arrow-of-planner"],
    },
    "will-power": {
        "name": "Arrow of Will Power",
        "numbers": [9, 5, 1],
        "theme": "Will column",
        "effect_present": "A complete 9-5-1 line is one of the clearest markers of determination. It supports persistence, expressive clarity, and the ability to keep moving until the work is finished.",
        "effect_missing": "When 9, 5, and 1 are all absent, decisions can be delayed for too long. People-pleasing, hesitation, and difficulty voicing a firm position tend to increase.",
        "real_life_traits": ["persistence", "goal focus", "communication strength", "inner authority"],
        "shadow_trait": "Can become stubborn, inflexible, or too attached to winning the argument.",
        "strength_band": "high",
        "aliases": ["will", "willpower", "arrow-of-will", "arrow-of-will-power"],
    },
    "action": {
        "name": "Arrow of Action",
        "numbers": [2, 7, 6],
        "theme": "Action column",
        "effect_present": "A full 2-7-6 line helps ideas move into lived action. This arrow supports practical execution, embodied learning, and a hands-on style that prefers doing over endless theorising.",
        "effect_missing": "When the 2-7-6 action column is empty, motivation can feel uneven and opportunities may be missed through delay. Momentum improves when action is broken into immediate, tangible steps.",
        "real_life_traits": ["execution", "hands-on learning", "active effort", "practical follow-through"],
        "shadow_trait": "Can act too quickly or stay busy without enough reflection if the line becomes overactive.",
        "strength_band": "high",
        "aliases": ["activity-column", "planner-action", "arrow-of-action"],
    },
    "emotional-balance": {
        "name": "Arrow of Emotional Balance",
        "numbers": [4, 5, 6],
        "theme": "Rajayoga diagonal",
        "effect_present": "The 4-5-6 diagonal is treated as a Rajayoga indicator in the decoded source. It suggests strong inner balance between sensitivity, communication, and worldly functioning, which can translate into visible life success.",
        "effect_missing": "When 4, 5, and 6 are all absent, suspicion and mental negativity can color relationships and choices. Trust, emotional regulation, and grounded interpretation of events become central growth areas.",
        "real_life_traits": ["balanced responses", "social ease", "measured judgment", "stable success drive"],
        "shadow_trait": "Can become image-conscious or over-managing when success and composure become identity armor.",
        "strength_band": "extreme",
        "rajayoga": True,
        "aliases": ["rajayoga-1", "suspicion", "arrow-of-emotional-balance"],
    },
    "determination": {
        "name": "Arrow of Determination",
        "numbers": [2, 5, 8],
        "theme": "Rajayoga diagonal",
        "effect_present": "The 2-5-8 diagonal is the second Rajayoga pattern in this system. It points to disciplined resolve, honest effort, and the ability to keep sight of a goal even when conditions are slow or demanding.",
        "effect_missing": "If 2, 5, and 8 are all absent, frustration and instability can repeat until patience and foresight are strengthened. Reactive choices usually create more losses than direct obstacles do.",
        "real_life_traits": ["resolve", "honesty", "long-range focus", "steadiness under pressure"],
        "shadow_trait": "Can become severe, overly self-pressured, or emotionally tight when determination loses softness.",
        "strength_band": "extreme",
        "rajayoga": True,
        "aliases": ["rajayoga-2", "frustration", "instability", "compassion", "arrow-of-determination"],
    },
}

# The decoded source labels the missing action arrow as 8-7-6 in one place, but
# the Lo Shu grid geometry and the commission's own calculation logic make the
# inverse action column 2-7-6. Runtime logic follows the grid geometry.
MISSING_ARROW_LABELS = {
    "intellect": "Arrow of Poor Memory",
    "spirituality": "Arrow of Loneliness",
    "prosperity": "Arrow of Losses",
    "planner": "Arrow of Confusion",
    "will-power": "Arrow of Indecision",
    "action": "Arrow of Apathy",
    "emotional-balance": "Arrow of Suspicion",
    "determination": "Arrow of Frustration",
}

ARROW_DISPLAY_ORDER = [
    "intellect",
    "spirituality",
    "prosperity",
    "planner",
    "will-power",
    "action",
    "emotional-balance",
    "determination",
]

PROBLEM_PAGE_ORDER = [
    "career-growth",
    "financial-instability",
    "relationship-difficulties",
    "marriage-delays",
    "health-issues",
    "lack-of-confidence",
    "communication-problems",
    "stress-anxiety",
    "poor-decisions",
    "loneliness",
    "academic-struggles",
    "business-partnerships",
    "family-conflicts",
    "property-issues",
    "travel-relocation",
    "creativity-block",
    "spiritual-disconnection",
    "legal-problems",
    "fertility",
    "leadership",
]

PROBLEM_AREA_BLUEPRINTS: dict[str, dict[str, Any]] = {
    "career-growth": {
        "problem_name": "Career Growth Block",
        "intro": "Career stagnation in Lo Shu often shows up when initiative, structure, and long-range discipline are not reinforcing each other. The source material repeatedly ties numbers 1, 4, and 8 to career direction, prosperity, and progress.",
        "diagnostic_missing_numbers": [1, 4, 8],
        "diagnostic_overrepresented_numbers": [5],
        "primary_fix_number": 1,
        "grid_diagnostic": "Look first for weak 1, 4, or 8 energy, because these numbers support communication, disciplined effort, and gradual material growth. A scattered 5 can add movement without enough stability to turn effort into advancement.",
        "missing_number_fix": "Start with number 1 if your career feels invisible or directionless. A steadier voice, stronger self-trust, and cleaner initiative usually create the first opening before wealth or status numbers can do their job.",
        "arrow_slugs": ["planner", "will-power", "prosperity"],
        "remedies": [
            "Strengthen the North zone with cleaner work goals, simpler communication, and fewer delayed decisions.",
            "Build a repeatable weekly routine so 4-style discipline becomes visible in your work rhythm.",
            "Use North-East study or planning time to sharpen skill, memory, and long-range credibility.",
            "Choose one high-value task every day and finish it before chasing new opportunities.",
            "Avoid saying yes to everything when growth actually requires clearer positioning.",
        ],
        "affirmation": "My effort is focused, visible, and moving toward meaningful growth.",
    },
    "financial-instability": {
        "problem_name": "Financial Instability",
        "intro": "The Lo Shu sources connect money flow with discipline, balance, and steady prosperity patterns rather than luck alone. Weak 4, 5, or 8 energy often shows why income comes in but stability does not remain.",
        "diagnostic_missing_numbers": [4, 5, 8],
        "diagnostic_overrepresented_numbers": [9],
        "primary_fix_number": 4,
        "grid_diagnostic": "Missing 4 can weaken wealth structure, missing 5 can reduce balance, and missing 8 can reduce financial realism and patience. Overheated 9 energy may then push reactive spending or pressure-driven decisions.",
        "missing_number_fix": "Address number 4 first when money feels inconsistent. Lo Shu texts repeatedly connect 4 with practical wealth-building, disciplined effort, and material order.",
        "arrow_slugs": ["emotional-balance", "determination", "prosperity"],
        "remedies": [
            "Create a visible budget and return to it on the same day each week.",
            "Reduce speculative or fast-money behavior until stability is stronger than urgency.",
            "Use grounding colors and calmer workspaces so spending decisions are less emotional.",
            "Strengthen South-East and North-East habits through savings, study, and slower planning.",
            "Finish pending financial paperwork before opening new commitments.",
        ],
        "affirmation": "I build stable wealth through order, patience, and disciplined choices.",
    },
    "relationship-difficulties": {
        "problem_name": "Relationship Difficulties",
        "intro": "Relationship strain often appears when emotional sensitivity, balance, and care are unevenly distributed in the grid. Lo Shu sources place special weight on 2, 5, and 6 for partnership, emotional balance, and home energy.",
        "diagnostic_missing_numbers": [2, 5, 6],
        "diagnostic_overrepresented_numbers": [1, 9],
        "primary_fix_number": 2,
        "grid_diagnostic": "Missing 2 can reduce empathy, missing 5 can reduce emotional regulation, and missing 6 can weaken relational responsibility. Heavy 1 or 9 may then push the dynamic into ego clashes or hard speech.",
        "missing_number_fix": "Begin with number 2 when closeness feels difficult. Lo Shu gives 2 the role of love, marriage, intuition, and the emotional bridge between people.",
        "arrow_slugs": ["spirituality", "emotional-balance", "determination"],
        "remedies": [
            "Slow down reactive conversations and speak after emotions have cooled, not during their peak.",
            "Use Friday or Monday rituals for repair, appreciation, and emotional check-ins.",
            "Bring more softness into the home through order, fragrance, music, or calm shared space.",
            "Strengthen listening before persuasion when relationship tension keeps repeating.",
            "Spend less time diagnosing each other and more time restoring trust in small ways.",
        ],
        "affirmation": "I create relationships through presence, care, and emotional honesty.",
    },
    "marriage-delays": {
        "problem_name": "Marriage Delays",
        "intro": "Marriage delays in a Lo Shu reading often point less to denial and more to imbalance in partnership, emotional readiness, and home-supportive patterns. Numbers 2 and 6 are especially important in the source set for these themes.",
        "diagnostic_missing_numbers": [2, 6, 4],
        "diagnostic_overrepresented_numbers": [7],
        "primary_fix_number": 2,
        "grid_diagnostic": "Missing 2 may slow bonding, missing 6 may weaken domestic commitment energy, and missing 4 can reduce the practical structure required to stabilise a long-term union. Excess 7 can deepen solitude or inward withdrawal.",
        "missing_number_fix": "Start with number 2 if the issue feels relational rather than circumstantial. It governs marriage, compatibility, and the emotional receptivity needed to actually welcome partnership.",
        "arrow_slugs": ["emotional-balance", "determination", "action"],
        "remedies": [
            "Strengthen South-West themes: steadier commitment language, softer emotional habits, and fewer mixed signals.",
            "Treat home and self-presentation as ready-for-partnership spaces, not temporary holding zones.",
            "Resolve lingering resentment from old bonds before inviting a new one.",
            "On Fridays and Mondays, do one act that aligns you with care rather than fear.",
            "Avoid letting spiritual detachment become a reason to avoid emotional availability.",
        ],
        "affirmation": "I welcome committed love with clarity, steadiness, and readiness.",
    },
    "health-issues": {
        "problem_name": "Health Issues",
        "intro": "The Lo Shu texts explicitly connect health with the three horizontal planes: mental, emotional, and practical. When 3, 5, 7 or 4, 9, 2 or 8, 1, 6 are weak together, wellbeing often feels fragmented instead of supported.",
        "diagnostic_missing_numbers": [3, 5, 7],
        "diagnostic_overrepresented_numbers": [9],
        "primary_fix_number": 5,
        "grid_diagnostic": "Poor balance in the emotional row can weaken stress handling, while missing practical or mental supports can reduce consistency in healing. Heavy 9 can add inflammation, impatience, or forceful habits that ignore recovery timing.",
        "missing_number_fix": "Address number 5 first when the system feels overtaxed. It sits in the center of the grid and acts like the stabiliser between body, mind, and lifestyle demands.",
        "arrow_slugs": ["spirituality", "intellect", "prosperity"],
        "remedies": [
            "Prioritise sleep, meal rhythm, and repeatable self-care before adding more complicated remedies.",
            "Reduce overstimulation so emotional and mental arrows can settle instead of staying activated.",
            "Use simple grounding practices like walking, breathwork, and sunlight rather than only crisis responses.",
            "Track health patterns weekly to bring planner energy into the healing process.",
            "Choose steadiness over heroic bursts of discipline followed by collapse.",
        ],
        "affirmation": "My body responds to rhythm, balance, and patient care.",
    },
    "lack-of-confidence": {
        "problem_name": "Lack of Confidence",
        "intro": "Confidence issues in Lo Shu usually show up when self-expression, courage, and structure are not supporting one another. The key numbers here are 1 for voice, 9 for force, and 4 for practical grounding.",
        "diagnostic_missing_numbers": [1, 4, 9],
        "diagnostic_overrepresented_numbers": [2],
        "primary_fix_number": 1,
        "grid_diagnostic": "Missing 1 can weaken voice, missing 9 can reduce assertive fire, and missing 4 can remove the steady structure that helps confidence feel earned. Excess 2 can make approval-seeking louder than self-trust.",
        "missing_number_fix": "Number 1 is the first corrective focus because confidence often improves when the person starts hearing their own voice clearly again.",
        "arrow_slugs": ["will-power", "intellect", "planner"],
        "remedies": [
            "Speak one direct truth a day instead of practicing your opinion only in private.",
            "Use body posture, clean routines, and task completion to build evidence-based confidence.",
            "Return to the North and South directions symbolically through visibility and courage cues.",
            "Do not confuse gentleness with self-erasure in high-stakes spaces.",
            "Keep a written record of completed actions so self-belief is anchored in proof.",
        ],
        "affirmation": "I trust my voice and act with steady self-respect.",
    },
    "communication-problems": {
        "problem_name": "Communication Problems",
        "intro": "Communication strain in Lo Shu often reflects imbalance between number 1's directness, number 3's articulation, and number 5's balance. Without those supports, speech can become hesitant, rushed, or emotionally imprecise.",
        "diagnostic_missing_numbers": [1, 3, 5],
        "diagnostic_overrepresented_numbers": [2, 9],
        "primary_fix_number": 1,
        "grid_diagnostic": "Weak 1 reduces clear self-expression, weak 3 can reduce verbal coherence, and weak 5 weakens timing and balance. Too much 2 or 9 may then turn communication into hurt reactivity or aggressive bluntness.",
        "missing_number_fix": "Begin with number 1 when communication itself is the bottleneck. A cleaner sense of self-expression usually makes the rest of the conversation easier to repair.",
        "arrow_slugs": ["will-power", "intellect", "spirituality"],
        "remedies": [
            "Write before difficult conversations so your real point is clear to you first.",
            "Lower the speed of speech when emotion is high; balance matters more than volume.",
            "Strengthen Mercury-like habits: simple wording, clearer intent, fewer mixed messages.",
            "Practice repeating what you heard before answering with what you want.",
            "Build confidence through consistency, not by forcing dramatic conversations.",
        ],
        "affirmation": "I communicate with clarity, timing, and respect.",
    },
    "stress-anxiety": {
        "problem_name": "Chronic Stress and Anxiety",
        "intro": "Stress patterns in Lo Shu often intensify when the calming, balancing, and reflective numbers are thin or unstable. The most relevant corrective numbers are usually 2, 5, and 7.",
        "diagnostic_missing_numbers": [2, 5, 7],
        "diagnostic_overrepresented_numbers": [4, 9],
        "primary_fix_number": 5,
        "grid_diagnostic": "Missing 5 can reduce inner balance, missing 2 can weaken emotional softness, and missing 7 can reduce reflection or spiritual buffering. Too much 4 or 9 can then turn the mind into a constant pressure chamber.",
        "missing_number_fix": "Start with number 5 when everything feels overstimulating. The center number acts like the grid's balancing axis and often settles multiple symptoms at once.",
        "arrow_slugs": ["spirituality", "determination", "will-power"],
        "remedies": [
            "Reduce over-scheduling and create predictable daily anchors for sleep, food, and transition time.",
            "Use quiet evening practices to lower nervous-system speed before bedtime.",
            "Avoid making every concern a decision problem; some stress resolves through rhythm, not analysis.",
            "Bring softer colors, slower pacing, and emotional check-ins into the environments where tension spikes.",
            "If your mind is loud, let your body do something repetitive and calming before trying to solve it.",
        ],
        "affirmation": "I return to center through calm rhythm and grounded presence.",
    },
    "poor-decisions": {
        "problem_name": "Poor Decision Making",
        "intro": "Poor decisions in Lo Shu often come from a weak center or weak will rather than from lack of intelligence alone. Numbers 1, 5, and 9 are especially important when choices must be clear, timely, and lived out.",
        "diagnostic_missing_numbers": [1, 5, 9],
        "diagnostic_overrepresented_numbers": [2],
        "primary_fix_number": 5,
        "grid_diagnostic": "Missing 5 makes balance harder, missing 1 weakens self-positioning, and missing 9 can reduce decisive force. Excess 2 may then keep someone over-reading everyone else's feelings before acting for themselves.",
        "missing_number_fix": "Address number 5 first because decisions usually improve when the mind stops swinging between extremes and returns to center.",
        "arrow_slugs": ["will-power", "planner", "intellect"],
        "remedies": [
            "Make fewer decisions in emotional peaks; decide after the body has settled.",
            "Use written criteria for important choices instead of pure mood or pressure.",
            "Strengthen will through small daily follow-through, not only big promises.",
            "Ask whether a choice is truly yours before optimizing it for other people.",
            "Set time limits for decisions that habitually drag past their useful window.",
        ],
        "affirmation": "I decide from balance, clarity, and inner authority.",
    },
    "loneliness": {
        "problem_name": "Loneliness and Social Isolation",
        "intro": "Loneliness has one of the clearest signatures in the Lo Shu source set: the missing 3-5-7 emotional or spiritual row. When this line is weak, joy, empathy, and social warmth often need deliberate rebuilding.",
        "diagnostic_missing_numbers": [3, 5, 7],
        "diagnostic_overrepresented_numbers": [1],
        "primary_fix_number": 3,
        "grid_diagnostic": "Weak 3 can reduce open expression, weak 5 can reduce balance, and weak 7 can reduce inner trust. Heavy 1 can then turn independence into social distance instead of healthy individuality.",
        "missing_number_fix": "Begin with number 3 when loneliness feels emotional rather than circumstantial. Expression and creative warmth often reopen connection faster than forcing more social contact alone.",
        "arrow_slugs": ["spirituality"],
        "remedies": [
            "Make room for joy, play, and shared activity instead of only serious connection attempts.",
            "Use creativity or learning spaces to meet people through meaning, not performance.",
            "Strengthen the emotional row through gentler speech, shared meals, or regular check-ins.",
            "Let connection build through consistency instead of waiting for instant depth.",
            "If isolation has become a habit, start with one warm relational gesture each week.",
        ],
        "affirmation": "I create connection through warmth, openness, and shared humanity.",
    },
    "academic-struggles": {
        "problem_name": "Academic Struggles",
        "intro": "Academic difficulty in Lo Shu usually reflects strain in memory, planning, or disciplined study energy. The key numbers here are 3 for learning, 8 for knowledge and structure, and 9 for mental drive.",
        "diagnostic_missing_numbers": [3, 8, 9],
        "diagnostic_overrepresented_numbers": [2, 5],
        "primary_fix_number": 8,
        "grid_diagnostic": "Missing 3 can weaken memory and expression, missing 8 can reduce educational discipline, and missing 9 can lower force under pressure. Too much 2 or 5 may create sensitivity or distraction without enough sustained structure.",
        "missing_number_fix": "Start with number 8 when studies feel inconsistent. The source texts directly connect 8 with education, memory power, and disciplined learning.",
        "arrow_slugs": ["intellect", "planner"],
        "remedies": [
            "Use fixed study blocks in the North-East so learning becomes rhythmic instead of negotiable.",
            "Write summaries by hand to strengthen memory and attention to detail together.",
            "Break complex subjects into planned repetition rather than intensity-driven cramming.",
            "Reduce emotional clutter before study sessions so cognition is not carrying everything else too.",
            "Choose fewer study goals and finish them fully instead of multitasking your focus away.",
        ],
        "affirmation": "My mind learns steadily, remembers clearly, and grows through discipline.",
    },
    "business-partnerships": {
        "problem_name": "Business Partnership Problems",
        "intro": "Business partnerships in Lo Shu need a clean blend of relationship intelligence, balanced communication, and responsibility. Weak 2, 5, or 6 can make even promising collaborations unstable.",
        "diagnostic_missing_numbers": [2, 5, 6],
        "diagnostic_overrepresented_numbers": [1, 8],
        "primary_fix_number": 2,
        "grid_diagnostic": "Missing 2 weakens diplomacy, missing 5 weakens coordination, and missing 6 weakens trustworthy responsibility. Excess 1 or 8 may then create control battles, rigidity, or financially driven mistrust.",
        "missing_number_fix": "Start with number 2 if a partnership keeps turning into friction. Relational intelligence is the first thing that keeps shared work from becoming a silent power contest.",
        "arrow_slugs": ["determination", "emotional-balance", "action"],
        "remedies": [
            "Put expectations, money splits, and responsibilities in writing before emotion fills the gaps.",
            "Restore diplomacy before strategy when trust has weakened.",
            "Use regular review meetings to keep small resentments from becoming structural problems.",
            "Strengthen Friday care and Wednesday clarity instead of waiting for conflict to force honesty.",
            "If one partner dominates every decision, rebalance the communication structure first.",
        ],
        "affirmation": "I build partnerships through fairness, clarity, and shared responsibility.",
    },
    "family-conflicts": {
        "problem_name": "Family Conflicts",
        "intro": "Family conflict often reflects imbalance in the relational and central home numbers. Lo Shu repeatedly points to 2, 5, and 6 as stabilisers of emotional harmony, understanding, and domestic responsibility.",
        "diagnostic_missing_numbers": [2, 5, 6],
        "diagnostic_overrepresented_numbers": [4, 9],
        "primary_fix_number": 6,
        "grid_diagnostic": "Missing 6 weakens home harmony, missing 2 weakens softness, and missing 5 weakens balance. Heavy 4 or 9 can then make family spaces feel rule-heavy, reactive, or emotionally overheated.",
        "missing_number_fix": "Address number 6 first when home life feels strained. In the source material, 6 carries family care, support, and the relational duty that holds a household together.",
        "arrow_slugs": ["spirituality", "emotional-balance"],
        "remedies": [
            "Rebuild calm routines at home before trying to solve every old issue at once.",
            "Bring beauty, order, and gentler shared spaces into areas where conflict keeps reigniting.",
            "Use appreciation language more often than corrective language for one full week.",
            "Resolve practical responsibility imbalances instead of calling everything an emotional problem.",
            "If family members are overwhelmed, slow the household pace before demanding better behavior.",
        ],
        "affirmation": "My home becomes steadier through care, clarity, and mutual respect.",
    },
    "property-issues": {
        "problem_name": "Property and Home Issues",
        "intro": "Property matters in the Lo Shu system are strongly connected with stability, wealth structure, and the Rajayoga-style material diagonals. Weak 4, 8, or 2 often shows why home or property plans keep stalling.",
        "diagnostic_missing_numbers": [4, 8, 2],
        "diagnostic_overrepresented_numbers": [7],
        "primary_fix_number": 8,
        "grid_diagnostic": "Missing 4 weakens prosperity structure, missing 8 weakens property-minded patience, and missing 2 reduces supportive relational timing. Excess 7 can make the person hesitant, detached, or stuck in reflection instead of action.",
        "missing_number_fix": "Start with number 8 if property matters keep delaying. The source material connects 8 with education, planning maturity, and the kind of realistic patience property decisions need.",
        "arrow_slugs": ["determination", "planner", "prosperity"],
        "remedies": [
            "Treat property decisions as long-range structure, not emotional rescue.",
            "Strengthen the North-East with clean planning, fewer delays, and practical documentation.",
            "Avoid rushing a home decision to end uncertainty; unstable choices cost more later.",
            "Use the 2-5-8 material stability pattern as a reminder that property thrives on patience and balance.",
            "Clear old clutter or unfinished repairs if the home itself feels energetically stalled.",
        ],
        "affirmation": "I create stable foundations through patient and grounded choices.",
    },
    "travel-relocation": {
        "problem_name": "Travel and Relocation",
        "intro": "Travel and relocation in Lo Shu ask for mobility, opportunity support, and stable adjustment. Numbers 6, 5, and 1 often explain whether movement becomes an opening or a source of disorientation.",
        "diagnostic_missing_numbers": [6, 5, 1],
        "diagnostic_overrepresented_numbers": [4],
        "primary_fix_number": 6,
        "grid_diagnostic": "Missing 6 can weaken support systems and beneficial movement, missing 5 reduces adaptability, and missing 1 weakens decisiveness. Excess 4 may keep someone over-attached to routine even when change is necessary.",
        "missing_number_fix": "Begin with number 6 if relocation keeps feeling blocked or unsupported. The source texts associate 6 with new opportunities, friendship support, and movement tied to practical life.",
        "arrow_slugs": ["action", "prosperity"],
        "remedies": [
            "Clarify why you are moving before obsessing over every possible route.",
            "Create support structures in the new place early, not after stress peaks.",
            "Travel light in both logistics and emotional baggage when relocation is already demanding.",
            "Use Wednesday planning and Friday settling rituals to make movement feel safer.",
            "If every move feels chaotic, strengthen adaptability before blaming the destination.",
        ],
        "affirmation": "I move with clarity, support, and grounded adaptability.",
    },
    "creativity-block": {
        "problem_name": "Lack of Creativity",
        "intro": "Creativity blocks in Lo Shu usually reflect weak imagination, emotional flow, or playful life-force. The most useful corrective numbers are 3, 6, and 7.",
        "diagnostic_missing_numbers": [3, 6, 7],
        "diagnostic_overrepresented_numbers": [4, 8],
        "primary_fix_number": 3,
        "grid_diagnostic": "Missing 3 reduces expressive imagination, missing 6 reduces warm creative care, and missing 7 can disconnect intuition from art. Heavy 4 or 8 may over-structure life until there is no room left for experimentation.",
        "missing_number_fix": "Address number 3 first when ideas feel dry. In the source material, 3 repeatedly carries memory, creative intelligence, and planning imagination.",
        "arrow_slugs": ["spirituality", "prosperity"],
        "remedies": [
            "Return to unfinished creative outlets rather than waiting for the perfect new idea.",
            "Give imagination a time container so it is invited, not postponed forever.",
            "Reduce hyper-practical pressure if every idea is being judged before it can breathe.",
            "Create visual, musical, or writing rituals that reconnect you with play.",
            "Let creative output be imperfect long before it is impressive.",
        ],
        "affirmation": "My creativity returns when I give it space, warmth, and movement.",
    },
    "spiritual-disconnection": {
        "problem_name": "Spiritual Disconnection",
        "intro": "When someone feels cut off from meaning, faith, or inner guidance, the Lo Shu grid often shows weakness in the reflective and balancing numbers. The most important corrective pattern here is 7, supported by 5 and 2.",
        "diagnostic_missing_numbers": [7, 5, 2],
        "diagnostic_overrepresented_numbers": [8, 9],
        "primary_fix_number": 7,
        "grid_diagnostic": "Missing 7 reduces contemplative depth, missing 5 weakens inner balance, and missing 2 can reduce receptivity. Heavy 8 or 9 may then push life toward output, pressure, or ambition without enough inward listening.",
        "missing_number_fix": "Start with number 7 when the problem is spiritual dryness. The source texts place 7 close to learning through experience, inner wisdom, and the quieter side of life.",
        "arrow_slugs": ["spirituality", "action"],
        "remedies": [
            "Make silence deliberate again instead of waiting for insight to arrive inside constant noise.",
            "Choose one regular practice and stay with it long enough for depth to form.",
            "Spend time in nature, reflection, or sacred reading without trying to optimise the experience.",
            "Release the idea that spirituality should feel intense every day to be real.",
            "If you feel spiritually numb, soften the body first; the inner life often reopens through stillness.",
        ],
        "affirmation": "I reconnect with meaning through stillness, sincerity, and inner trust.",
    },
    "legal-problems": {
        "problem_name": "Legal Problems",
        "intro": "Legal strain in Lo Shu often points toward weak discipline, weak regulatory awareness, or reactive choices around power and money. Numbers 8, 9, and 4 are especially important here.",
        "diagnostic_missing_numbers": [8, 9, 4],
        "diagnostic_overrepresented_numbers": [5],
        "primary_fix_number": 8,
        "grid_diagnostic": "Missing 8 can weaken respect for structure and consequence, missing 9 can reduce clear protective action, and missing 4 can weaken practical order. An unstable 5 may then create fast choices without sufficient review.",
        "missing_number_fix": "Begin with number 8 when legal pressure is the issue. The source material directly associates 8 with law, regulation, discipline, and the outcome of actions.",
        "arrow_slugs": ["determination", "planner", "will-power"],
        "remedies": [
            "Bring all documentation, deadlines, and responsibilities into one visible system immediately.",
            "Choose restraint over escalation when emotions are high; legal matters punish impulsive reactions.",
            "Strengthen Saturn-style discipline through timelines, records, and procedural patience.",
            "Ask for expert help early instead of waiting until the situation becomes more expensive.",
            "Do not confuse optimism with preparedness in binding matters.",
        ],
        "affirmation": "I handle serious matters with discipline, truth, and steady judgment.",
    },
    "fertility": {
        "problem_name": "Childbirth and Fertility",
        "intro": "The Lo Shu texts connect family, marriage, children, and emotional harmony across numbers 2, 6, and 7. When these are weak together, fertility or childbirth anxiety may feel more energetically pronounced.",
        "diagnostic_missing_numbers": [2, 6, 7],
        "diagnostic_overrepresented_numbers": [9],
        "primary_fix_number": 6,
        "grid_diagnostic": "Missing 2 can weaken receptive partnership energy, missing 6 can weaken home-and-family support, and missing 7 can strain emotional calm. Heavy 9 may add stress, pressure, or impatience around timing.",
        "missing_number_fix": "Start with number 6 when the issue centers on family readiness, care, and the emotional container of home life.",
        "arrow_slugs": ["spirituality", "action"],
        "remedies": [
            "Prioritise nervous-system calm and household steadiness instead of making every month a crisis test.",
            "Use Friday care rituals and gentler domestic environments to support 6 energy.",
            "Reduce comparison and timeline pressure when the body already feels watched.",
            "Treat emotional rest as part of preparation, not as a distraction from it.",
            "Bring partnership softness and mutual support back to the center of the process.",
        ],
        "affirmation": "My home and heart are open to life in calm and trusting ways.",
    },
    "leadership": {
        "problem_name": "Leadership Challenges",
        "intro": "Leadership difficulty in Lo Shu usually reflects weak initiative, weak power under pressure, or poor structural follow-through. Numbers 1, 8, and 9 are central when authority needs to feel both credible and grounded.",
        "diagnostic_missing_numbers": [1, 8, 9],
        "diagnostic_overrepresented_numbers": [2],
        "primary_fix_number": 1,
        "grid_diagnostic": "Missing 1 weakens self-definition, missing 8 weakens authority through discipline, and missing 9 weakens visible force. Too much 2 may then make someone so accommodating that leadership becomes diluted.",
        "missing_number_fix": "Begin with number 1 if leadership feels shaky. The ability to own direction is usually the first thing that makes responsibility easier to carry.",
        "arrow_slugs": ["will-power", "prosperity", "intellect"],
        "remedies": [
            "Lead from clear priorities instead of trying to satisfy every voice at once.",
            "Strengthen visible accountability so confidence is backed by structure.",
            "Use challenge as a proving ground for steadiness, not just for intensity.",
            "Build leadership through decision quality and follow-through, not image alone.",
            "Do one thing daily that reinforces authority without aggression.",
        ],
        "affirmation": "I lead with clarity, courage, and disciplined responsibility.",
    },
}

PERSONAL_YEAR_BLUEPRINTS: dict[int, dict[str, Any]] = {
    1: {
        "intro": "Personal Year 1 marks a fresh cycle in Lo Shu-style yearly reading. It is the year of initiative, self-definition, and beginning again with cleaner intent.",
        "year_theme": "New starts, personal courage, independence, and setting the tone for the next cycle.",
        "opportunities": ["launching projects", "career repositioning", "self-confidence", "personal branding", "acting on long-delayed ideas"],
        "cautions": ["forcing things too quickly", "ego clashes", "starting too much without structure"],
        "monthly_note": "The year tends to feel strongest when each month is used to build momentum rather than to seek immediate proof. Small decisive actions matter more than dramatic gestures.",
        "remedies": [
            "Begin visible goals early in the year instead of waiting for certainty.",
            "Use direct communication and cleaner boundaries to support new beginnings.",
            "Protect your energy from people or routines that flatten initiative.",
        ],
    },
    2: {
        "intro": "Personal Year 2 slows the pace after a forceful beginning and asks for emotional intelligence. It is a year of partnership, patience, adjustment, and learning how timing works through relationship.",
        "year_theme": "Cooperation, emotional sensitivity, diplomacy, and quiet preparation.",
        "opportunities": ["deepening relationships", "teamwork", "healing conflicts", "intuition", "refining plans patiently"],
        "cautions": ["taking things personally", "indecision", "depending too much on other people's mood"],
        "monthly_note": "The energy of this year often rises through subtler progress. Some months may look slow on the outside while trust, emotional repair, or inner clarity is building underneath.",
        "remedies": [
            "Use listening and timing as strategic strengths instead of signs of weakness.",
            "Keep emotional routines steady so sensitivity does not become instability.",
            "Nurture one important partnership rather than spreading attention too thin.",
        ],
    },
    3: {
        "intro": "Personal Year 3 is described in the source material as a social, bright, and creatively expansive year. It often increases visibility, expression, old-friend reconnection, and the urge to live more fully.",
        "year_theme": "Creative expansion, social circulation, optimism, and expressive confidence.",
        "opportunities": ["creative work", "networking", "romance", "public expression", "recognition through talent or voice"],
        "cautions": ["scattering energy", "frivolous financial decisions", "enjoyment that loses sight of the larger goal"],
        "monthly_note": "This year tends to move in waves of enthusiasm. The key is to enjoy the social lift without abandoning the discipline needed to make the growth durable.",
        "remedies": [
            "Create, speak, publish, or perform instead of keeping ideas trapped inside drafts.",
            "Reconnect with old friends selectively and build new circles through shared interest.",
            "Keep money and deadlines in view so pleasure does not sabotage progress.",
        ],
    },
    4: {
        "intro": "Personal Year 4 is where life asks for structure, repetition, and practical rebuilding. It is rarely glamorous, but it is the year that turns vague intention into something durable.",
        "year_theme": "Discipline, foundations, consistent work, and long-range order.",
        "opportunities": ["system-building", "steady savings", "health routines", "work ethic", "finishing neglected practical tasks"],
        "cautions": ["rigidity", "burnout from overwork", "discouragement when results arrive slowly"],
        "monthly_note": "Month by month, this year usually rewards consistency more than inspiration. Progress can feel plain at first, but it compounds if the structure holds.",
        "remedies": [
            "Make one repeatable routine non-negotiable before adding bigger ambitions.",
            "Treat slow progress as proof that the year is working, not that it is failing.",
            "Leave room for recovery so discipline does not become self-punishment.",
        ],
    },
    5: {
        "intro": "Personal Year 5 increases movement, change, novelty, and demand for flexibility. In Lo Shu terms it resembles a center shift year where life stops responding well to stale patterns.",
        "year_theme": "Change, freedom, experimentation, movement, and rapid adjustment.",
        "opportunities": ["travel", "new experiences", "communication", "reinvention", "breaking out of stale environments"],
        "cautions": ["impulsiveness", "restlessness", "too many unfinished directions at once"],
        "monthly_note": "The months in a 5 year often feel uneven by design. The skill is not to freeze the movement, but to keep it from becoming chaos.",
        "remedies": [
            "Choose flexible plans with a clear spine rather than rigid systems that will snap.",
            "Let healthy novelty replace destructive disruption.",
            "Pause before major commitments so freedom does not become confusion.",
        ],
    },
    6: {
        "intro": "Personal Year 6 turns attention toward home, relationships, responsibility, and emotional maturity. It often highlights family, care, beauty, and the duties that cannot be outsourced forever.",
        "year_theme": "Love, family, obligation, harmony, and relational responsibility.",
        "opportunities": ["commitment", "healing family ties", "home improvements", "creative nurturing", "service through care"],
        "cautions": ["over-responsibility", "relationship pressure", "worrying about everyone else before yourself"],
        "monthly_note": "Through the months, the year may ask for repeated emotional repairs and practical care. Small acts of responsibility create disproportionate peace in a 6 year.",
        "remedies": [
            "Restore your environment as if it were part of your emotional body.",
            "Choose mature care over rescuing behavior.",
            "Make beauty, rest, and relational honesty part of the year's structure.",
        ],
    },
    7: {
        "intro": "Personal Year 7 is slower, deeper, and more inward than the years around it. It often emphasizes study, healing, spiritual inquiry, solitude, and lessons that cannot be rushed by external action alone.",
        "year_theme": "Reflection, inner work, wisdom, healing, and spiritual recalibration.",
        "opportunities": ["study", "therapy or healing", "research", "meditation", "clarifying what truly matters"],
        "cautions": ["withdrawal", "over-isolation", "treating every delay as a failure instead of a refinement"],
        "monthly_note": "Many months in a 7 year look quieter from the outside than they feel from within. Use that slower pace to deepen insight instead of demanding visible speed.",
        "remedies": [
            "Protect time for silence, reading, and reflective practices.",
            "Let depth become the goal instead of external applause.",
            "Take care with sleep and nervous-system load so insight is not drowned by exhaustion.",
        ],
    },
    8: {
        "intro": "Personal Year 8 is the year of material consequence, executive force, and tangible results. It tends to spotlight money, power, authority, contracts, and the visible reward or cost of prior effort.",
        "year_theme": "Achievement, finance, power, accountability, and strategic execution.",
        "opportunities": ["career advancement", "business growth", "financial rebuilding", "leadership", "serious goal completion"],
        "cautions": ["power struggles", "ethical shortcuts", "work swallowing the rest of life"],
        "monthly_note": "Month to month, an 8 year tends to respond best to focused execution and clean accountability. The faster you face reality, the more usable the year becomes.",
        "remedies": [
            "Track numbers, commitments, and agreements more carefully than usual.",
            "Use ambition in service of substance, not image alone.",
            "Keep your ethics clear because 8 magnifies consequence as much as reward.",
        ],
    },
    9: {
        "intro": "Personal Year 9 closes the cycle and asks for release, completion, and a larger perspective. It often brings endings, emotional clearing, service, and the need to let some things finish with dignity.",
        "year_theme": "Completion, release, humanitarian perspective, and emotional clearing.",
        "opportunities": ["finishing old cycles", "forgiveness", "service", "creative culmination", "making meaning from the past"],
        "cautions": ["clinging to what is ending", "drama around closure", "trying to force a fresh cycle before the old one is complete"],
        "monthly_note": "In a 9 year, the months often reveal what is ripe to conclude. The less you resist endings that are clearly mature, the more gracefully the next cycle begins.",
        "remedies": [
            "Clear obligations, clutter, and emotional residue before chasing the next beginning.",
            "Offer energy to service, compassion, or meaningful completion work.",
            "Release with discernment rather than burning everything down out of impatience.",
        ],
    },
}

ARROW_ALIAS_TO_SLUG: dict[str, str] = {}
for _slug, _payload in ARROW_BLUEPRINTS.items():
    ARROW_ALIAS_TO_SLUG[_slug] = _slug
    for _alias in _payload.get("aliases", []):
        ARROW_ALIAS_TO_SLUG[_alias] = _slug


class LoShuCalculateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    full_name: str
    dob: date
    gender: Literal["male", "female"]

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("full_name is required")
        if not any(char.isalpha() for char in value):
            raise ValueError("full_name must contain alphabetic characters")
        return value

    @field_validator("gender", mode="before")
    @classmethod
    def normalize_gender(cls, value: Any) -> str:
        if isinstance(value, str):
            return value.strip().lower()
        return value


def reduce_to_single(value: int) -> int:
    if value <= 0:
        return 0
    while value > 9:
        value = sum(int(char) for char in str(value))
    return value


def build_name_number(full_name: str) -> int:
    total = sum(PYTHAGOREAN_MAP[char.upper()] for char in full_name if char.isalpha())
    return reduce_to_single(total)


def build_kua_number(birth_date: date, gender: Literal["male", "female"]) -> int:
    year_sum = reduce_to_single(sum(int(char) for char in str(birth_date.year)))
    if gender == "female":
        return reduce_to_single(year_sum + 10)
    return reduce_to_single(11 - year_sum)


def build_number_counts(full_name: str, birth_date: date, gender: Literal["male", "female"]) -> tuple[dict[int, int], dict[str, int]]:
    dob_digits = [int(char) for char in birth_date.strftime("%d%m%Y") if char != "0"]
    day_digits = [int(char) for char in str(birth_date.day)] if birth_date.day > 9 else []
    basic_number = reduce_to_single(birth_date.day)
    destiny_number = reduce_to_single(sum(int(char) for char in birth_date.strftime("%d%m%Y") if char != "0"))
    kua_number = build_kua_number(birth_date, gender)
    name_number = build_name_number(full_name)

    digits = [*dob_digits, *day_digits, destiny_number, kua_number, name_number]
    counts = {number: 0 for number in range(1, 10)}
    for digit in digits:
        if 1 <= digit <= 9:
            counts[digit] += 1

    return counts, {
        "basic_number": basic_number,
        "destiny_number": destiny_number,
        "kua_number": kua_number,
        "name_number": name_number,
    }


def build_grid_rows(counts: dict[int, int]) -> list[list[dict[str, Any]]]:
    return [
        [{"number": number, "count": counts.get(number, 0), "present": counts.get(number, 0) > 0} for number in row]
        for row in GRID_ROWS
    ]


def build_missing_number_document(number: int) -> dict[str, Any]:
    if number not in MISSING_NUMBER_BLUEPRINTS:
        raise HTTPException(status_code=404, detail="Missing number not found")

    ref = NUMBER_REFERENCE[number]
    blueprint = MISSING_NUMBER_BLUEPRINTS[number]
    faq_items = [
        {
            "question": f"What does missing number {number} mean in Lo Shu Grid?",
            "answer": blueprint["effect_summary"],
        },
        {
            "question": f"Which planet rules number {number} in Lo Shu Grid?",
            "answer": f"Number {number} is linked with {ref['planet']} and is traditionally supported through {ref['day']} routines and symbolic balancing practices.",
        },
        {
            "question": f"Is missing {number} always bad?",
            "answer": f"Missing {number} does not mean failure. It usually points to an area that develops through practice rather than arriving as a natural default.",
        },
        {
            "question": f"How can I balance missing number {number}?",
            "answer": "Start with consistent habits, symbolic color or day alignment, and practical behavior shifts that strengthen the missing trait in daily life.",
        },
        {
            "question": f"What life area is most affected by missing number {number}?",
            "answer": f"The strongest impact is usually felt around {blueprint['focus_trait']}, with ripple effects in {', '.join(blueprint['life_areas_impacted'][:2])}.",
        },
    ]
    related_missing = blueprint["related_missing"]
    return {
        "number": number,
        "slug": f"missing-{number}",
        "title": f"Missing Number {number} in Lo Shu Grid - What It Means and How to Balance It",
        "ruling_planet": ref["planet"],
        "ruling_day": ref["day"],
        "archetype": ref["archetype"],
        "effect_summary": blueprint["effect_summary"],
        "traits_affected": blueprint["traits_affected"],
        "life_areas_impacted": blueprint["life_areas_impacted"],
        "remedies": blueprint["remedies"],
        "affirmation": blueprint["affirmation"],
        "faq": faq_items,
        "related_missing": related_missing,
        "related_pages": [
            {
                "number": related,
                "slug": f"missing-{related}",
                "title": f"Missing Number {related}",
            }
            for related in related_missing
        ],
        "meta_title": f"Missing Number {number} in Lo Shu Grid - {ref['planet']} Energy and Remedies",
        "meta_description": f"Number {number} missing from your Lo Shu Grid may affect {blueprint['focus_trait']}. Discover its meaning, practical remedies, and the life areas it influences.",
    }


def build_arrow_document(slug: str) -> dict[str, Any]:
    canonical_slug = ARROW_ALIAS_TO_SLUG.get(slug)
    if not canonical_slug:
        raise HTTPException(status_code=404, detail="Arrow not found")

    payload = ARROW_BLUEPRINTS[canonical_slug]
    faq_items = [
        {
            "question": f"What is the {payload['name']} in Lo Shu Grid?",
            "answer": f"It is the {payload['theme'].lower()} formed by numbers {', '.join(str(number) for number in payload['numbers'])} appearing together in the chart.",
        },
        {
            "question": f"What happens when the {payload['name']} is present?",
            "answer": payload["effect_present"],
        },
        {
            "question": f"What happens when the {payload['name']} is missing?",
            "answer": payload["effect_missing"],
        },
        {
            "question": f"Which traits are linked with the {payload['name']}?",
            "answer": f"It is most often linked with {', '.join(payload['real_life_traits'][:3])}.",
        },
        {
            "question": f"Is the {payload['name']} a Rajayoga?",
            "answer": "Yes. This arrow is treated as a Rajayoga pattern in the decoded Lo Shu source and is associated with heightened success potential." if payload.get("rajayoga") else "No. This arrow is important, but it is not one of the two Rajayoga diagonals.",
        },
    ]
    one_word_theme = payload["theme"].split()[0]
    return {
        "slug": canonical_slug,
        "name": payload["name"],
        "title": f"{payload['name']} - What This Lo Shu Arrow Reveals About You",
        "numbers": payload["numbers"],
        "theme": payload["theme"],
        "effect_present": payload["effect_present"],
        "effect_missing": payload["effect_missing"],
        "real_life_traits": payload["real_life_traits"],
        "shadow_trait": payload["shadow_trait"],
        "strength_band": payload["strength_band"],
        "rajayoga": bool(payload.get("rajayoga")),
        "faq": faq_items,
        "meta_title": f"{payload['name']} in Lo Shu Grid - {one_word_theme} Energy",
        "meta_description": f"Discover what the {payload['name']} means in Lo Shu Grid, what numbers {', '.join(str(number) for number in payload['numbers'])} reveal, and how this pattern shapes personality and action.",
    }


def build_number_deep_dive_document(number: int) -> dict[str, Any]:
    if number not in NUMBER_DEEP_DIVE_BLUEPRINTS:
        raise HTTPException(status_code=404, detail="Lo Shu number not found")

    ref = NUMBER_REFERENCE[number]
    assoc = NUMBER_CLASSICAL_ASSOCIATIONS[number]
    blueprint = NUMBER_DEEP_DIVE_BLUEPRINTS[number]
    faq_items = [
        {
            "question": f"What does Lo Shu number {number} mean when it is present?",
            "answer": blueprint["present_once"],
        },
        {
            "question": f"What happens when number {number} repeats in the Lo Shu Grid?",
            "answer": blueprint["repeat_guidance"],
        },
        {
            "question": f"What if number {number} is missing from the grid?",
            "answer": f"If number {number} is absent, the same energy usually develops through deliberate practice instead of natural ease. The dedicated missing number page explains the deeper effects and remedies.",
        },
        {
            "question": f"Which planet and direction are linked with number {number}?",
            "answer": f"Number {number} is linked with {ref['planet']}, the {assoc['element']} element, and the {assoc['direction']} direction in the decoded Lo Shu source set.",
        },
    ]
    return {
        "number": number,
        "slug": str(number),
        "title": f"Lo Shu Number {number} - Meaning, Energy & Influence in Your Grid",
        "intro": blueprint["intro"],
        "when_present": blueprint["present_once"],
        "when_repeated": blueprint["repeat_guidance"],
        "when_missing_summary": f"If number {number} is missing, the themes of {assoc['life_theme']} usually need more conscious cultivation through routine, confidence, and practical balancing work.",
        "missing_page": {
            "number": number,
            "href": f"/lo-shu-grid/missing-{number}",
            "title": f"Missing Number {number} in Lo Shu Grid",
        },
        "associations": {
            "planet": ref["planet"],
            "day": ref["day"],
            "archetype": ref["archetype"],
            "element": assoc["element"],
            "direction": assoc["direction"],
            "colours": assoc["colours"],
            "body_area": assoc["body_area"],
            "family_role": assoc["family_role"],
            "life_theme": assoc["life_theme"],
        },
        "balancing_tips": blueprint["balancing_tips"],
        "famous_personalities": blueprint["famous_personalities"],
        "faq": faq_items,
        "cta_href": "/lo-shu-grid/calculator",
        "meta_title": f"Lo Shu Number {number} - Meaning & Grid Influence | EverydayHoroscope",
        "meta_description": f"Discover what Lo Shu number {number} means when it is present, repeated, or missing from your grid, plus the classical associations and balancing tips linked with this number.",
    }


def build_problem_area_document(slug: str) -> dict[str, Any]:
    if slug not in PROBLEM_AREA_BLUEPRINTS:
        raise HTTPException(status_code=404, detail="Lo Shu problem page not found")

    payload = PROBLEM_AREA_BLUEPRINTS[slug]
    arrow_patterns = [
        {
            "slug": arrow_slug,
            "name": ARROW_BLUEPRINTS[arrow_slug]["name"],
            "href": f"/lo-shu-grid/arrow/{arrow_slug}",
            "theme": ARROW_BLUEPRINTS[arrow_slug]["theme"],
            "numbers": ARROW_BLUEPRINTS[arrow_slug]["numbers"],
        }
        for arrow_slug in payload["arrow_slugs"]
    ]
    faq_items = [
        {
            "question": f"What does Lo Shu Grid say about {payload['problem_name'].lower()}?",
            "answer": payload["grid_diagnostic"],
        },
        {
            "question": "Which missing number should I address first?",
            "answer": payload["missing_number_fix"],
        },
        {
            "question": "Do arrow patterns matter for this problem?",
            "answer": f"Yes. The most relevant arrows here are {', '.join(pattern['name'] for pattern in arrow_patterns)}, because they describe how thought, emotion, and action combine around this life area.",
        },
        {
            "question": "Can Lo Shu remedies replace practical help?",
            "answer": "No. Lo Shu remedies are best treated as reflective and supportive. They work alongside grounded action, clear communication, and professional support when the situation requires it.",
        },
    ]
    return {
        "slug": slug,
        "problem_name": payload["problem_name"],
        "title": f"Lo Shu Grid for {payload['problem_name']} - What Your Grid Reveals & How to Fix It",
        "intro": payload["intro"],
        "grid_diagnostic": payload["grid_diagnostic"],
        "diagnostic_missing_numbers": payload["diagnostic_missing_numbers"],
        "diagnostic_overrepresented_numbers": payload["diagnostic_overrepresented_numbers"],
        "primary_fix_number": payload["primary_fix_number"],
        "missing_number_fix": payload["missing_number_fix"],
        "primary_fix_page": {
            "number": payload["primary_fix_number"],
            "href": f"/lo-shu-grid/missing-{payload['primary_fix_number']}",
            "title": f"Missing Number {payload['primary_fix_number']}",
        },
        "arrow_patterns": arrow_patterns,
        "remedies": payload["remedies"],
        "affirmation": payload["affirmation"],
        "faq": faq_items,
        "cta_href": "/lo-shu-grid/calculator",
        "meta_title": f"Lo Shu Grid for {payload['problem_name']} - Analysis & Remedies | EverydayHoroscope",
        "meta_description": f"Explore how Lo Shu Grid patterns relate to {payload['problem_name'].lower()}, which missing numbers matter most, and which remedies can help restore balance.",
    }


def build_personal_year_document(number: int) -> dict[str, Any]:
    if number not in PERSONAL_YEAR_BLUEPRINTS:
        raise HTTPException(status_code=404, detail="Lo Shu personal year not found")

    current_year = date.today().year
    year_digit = reduce_to_single(sum(int(char) for char in str(current_year)))
    payload = PERSONAL_YEAR_BLUEPRINTS[number]
    formula_steps = [
        "Reduce your birth day to a single digit if needed.",
        "Reduce your birth month to a single digit if needed.",
        f"Reduce the current calendar year {current_year} to a single digit ({year_digit}).",
        "Add those three values together and reduce again to reach your Personal Year number.",
    ]
    faq_items = [
        {
            "question": f"What does Lo Shu Personal Year {number} mean?",
            "answer": payload["year_theme"],
        },
        {
            "question": f"How do I calculate my Personal Year for {current_year}?",
            "answer": f"Reduce your birth day, your birth month, and the current year {current_year}, then add the three values together and reduce the total to a single digit.",
        },
        {
            "question": "Does Personal Year replace the full Lo Shu Grid reading?",
            "answer": "No. Personal Year shows the annual theme, while the full Lo Shu Grid shows your deeper baseline pattern, missing numbers, and arrow dynamics.",
        },
        {
            "question": f"Can Personal Year {number} feel difficult even if it has opportunities?",
            "answer": f"Yes. Every Personal Year carries growth openings and caution zones, which is why the balance between opportunities and remedies matters as much as the headline theme.",
        },
    ]
    return {
        "number": number,
        "slug": str(number),
        "title": f"Lo Shu Personal Year {number} - What This Year Means for You",
        "intro": payload["intro"],
        "year_theme": payload["year_theme"],
        "opportunities": payload["opportunities"],
        "cautions": payload["cautions"],
        "monthly_note": payload["monthly_note"],
        "remedies": payload["remedies"],
        "current_year": current_year,
        "calculation_method": {
            "formula": "Personal Year = reduce(birth day) + reduce(birth month) + reduce(current year), then reduce the total",
            "steps": formula_steps,
        },
        "who_is_in_this_year_now": f"If your reduced birth day + reduced birth month + reduced year value for {current_year} adds up to {number} after reduction, you are in Personal Year {number} right now.",
        "faq": faq_items,
        "cta_href": "/lo-shu-grid/calculator",
        "meta_title": f"Lo Shu Personal Year {number} - What to Expect This Year | EverydayHoroscope",
        "meta_description": f"Understand the themes, opportunities, cautions, and remedies of Lo Shu Personal Year {number}, including how to calculate whether you are in this yearly cycle now.",
    }


def build_active_arrow_result(slug: str) -> dict[str, Any]:
    doc = build_arrow_document(slug)
    return {
        "slug": doc["slug"],
        "name": doc["name"],
        "numbers": doc["numbers"],
        "theme": doc["theme"],
        "effect_summary": doc["effect_present"],
        "strength_band": doc["strength_band"],
        "rajayoga": doc["rajayoga"],
    }


def build_missing_arrow_result(slug: str) -> dict[str, Any]:
    doc = build_arrow_document(slug)
    return {
        "slug": doc["slug"],
        "name": MISSING_ARROW_LABELS[doc["slug"]],
        "base_arrow_name": doc["name"],
        "numbers": doc["numbers"],
        "theme": doc["theme"],
        "effect_summary": doc["effect_missing"],
        "strength_band": "high" if doc["strength_band"] == "extreme" else doc["strength_band"],
    }


async def resolve_missing_number_document(request: Request, number: int) -> dict[str, Any]:
    db = getattr(request.app.state, "db", None)
    if db is not None:
        doc = await db.lo_shu_missing_numbers.find_one({"number": number}, {"_id": 0})
        if doc:
            return doc
    return build_missing_number_document(number)


async def resolve_arrow_document(request: Request, slug: str) -> dict[str, Any]:
    canonical_slug = ARROW_ALIAS_TO_SLUG.get(slug)
    if not canonical_slug:
        raise HTTPException(status_code=404, detail="Arrow not found")

    db = getattr(request.app.state, "db", None)
    if db is not None:
        doc = await db.lo_shu_arrows.find_one({"slug": canonical_slug}, {"_id": 0})
        if doc:
            return doc
    return build_arrow_document(canonical_slug)


async def resolve_number_deep_dive_document(request: Request, number: int) -> dict[str, Any]:
    db = getattr(request.app.state, "db", None)
    if db is not None:
        doc = await db.lo_shu_numbers.find_one({"number": number}, {"_id": 0})
        if doc:
            return doc
    return build_number_deep_dive_document(number)


async def resolve_problem_area_document(request: Request, slug: str) -> dict[str, Any]:
    db = getattr(request.app.state, "db", None)
    if db is not None:
        doc = await db.lo_shu_problems.find_one({"slug": slug}, {"_id": 0})
        if doc:
            return doc
    return build_problem_area_document(slug)


async def resolve_personal_year_document(request: Request, number: int) -> dict[str, Any]:
    db = getattr(request.app.state, "db", None)
    if db is not None:
        doc = await db.lo_shu_personal_years.find_one({"number": number}, {"_id": 0})
        if doc:
            return doc
    return build_personal_year_document(number)


@router.post("/calculate")
async def calculate_lo_shu(payload: LoShuCalculateRequest) -> dict[str, Any]:
    counts, core_numbers = build_number_counts(payload.full_name, payload.dob, payload.gender)
    present_numbers = [number for number in range(1, 10) if counts[number] > 0]
    missing_numbers = [number for number in range(1, 10) if counts[number] == 0]
    present_set = set(present_numbers)
    missing_set = set(missing_numbers)

    active_arrows = [
        build_active_arrow_result(slug)
        for slug in ARROW_DISPLAY_ORDER
        if all(number in present_set for number in ARROW_BLUEPRINTS[slug]["numbers"])
    ]
    missing_arrows = [
        build_missing_arrow_result(slug)
        for slug in ARROW_DISPLAY_ORDER
        if all(number in missing_set for number in ARROW_BLUEPRINTS[slug]["numbers"])
    ]
    rajayoga_present = [arrow for arrow in active_arrows if arrow["rajayoga"]]

    return {
        "grid": {str(number): counts[number] > 0 for number in range(1, 10)},
        "grid_rows": build_grid_rows(counts),
        "number_counts": {str(number): counts[number] for number in range(1, 10)},
        "missing_numbers": missing_numbers,
        "present_numbers": present_numbers,
        "active_arrows": active_arrows,
        "missing_arrows": missing_arrows,
        "basic_number": core_numbers["basic_number"],
        "destiny_number": core_numbers["destiny_number"],
        "kua_number": core_numbers["kua_number"],
        "name_number": core_numbers["name_number"],
        "missing_number_details": [build_missing_number_document(number) for number in missing_numbers],
        "rajayoga_present": rajayoga_present,
        "rajayoga_level": "dual" if len(rajayoga_present) == 2 else ("single" if len(rajayoga_present) == 1 else "none"),
    }


@router.get("/missing/{number}")
async def get_missing_number_page(number: int, request: Request) -> dict[str, Any]:
    if number < 1 or number > 9:
        raise HTTPException(status_code=404, detail="Missing number not found")
    return await resolve_missing_number_document(request, number)


@router.get("/arrow/{slug}")
async def get_arrow_page(slug: str, request: Request) -> dict[str, Any]:
    return await resolve_arrow_document(request, slug)


@router.get("/number/{number}")
async def get_number_page(number: int, request: Request) -> dict[str, Any]:
    if number < 1 or number > 9:
        raise HTTPException(status_code=404, detail="Lo Shu number not found")
    return await resolve_number_deep_dive_document(request, number)


@router.get("/problem/{slug}")
async def get_problem_page(slug: str, request: Request) -> dict[str, Any]:
    return await resolve_problem_area_document(request, slug)


@router.get("/personal-year/{number}")
async def get_personal_year_page(number: int, request: Request) -> dict[str, Any]:
    if number < 1 or number > 9:
        raise HTTPException(status_code=404, detail="Lo Shu personal year not found")
    return await resolve_personal_year_document(request, number)


LO_SHU_SITEMAP_URLS = [
    "https://www.everydayhoroscope.in/lo-shu-grid",
    "https://www.everydayhoroscope.in/lo-shu-grid/calculator",
    *[f"https://www.everydayhoroscope.in/lo-shu-grid/missing-{number}" for number in range(1, 10)],
    *[f"https://www.everydayhoroscope.in/lo-shu-grid/arrow/{slug}" for slug in ARROW_DISPLAY_ORDER],
    *[f"https://www.everydayhoroscope.in/lo-shu-grid/number/{number}" for number in range(1, 10)],
    *[f"https://www.everydayhoroscope.in/lo-shu-grid/for/{slug}" for slug in PROBLEM_PAGE_ORDER],
    *[f"https://www.everydayhoroscope.in/lo-shu-grid/personal-year/{number}" for number in range(1, 10)],
]

MISSING_NUMBER_DOCUMENTS = [build_missing_number_document(number) for number in range(1, 10)]
ARROW_DOCUMENTS = [build_arrow_document(slug) for slug in ARROW_DISPLAY_ORDER]
NUMBER_DEEP_DIVE_DOCUMENTS = [build_number_deep_dive_document(number) for number in range(1, 10)]
PROBLEM_AREA_DOCUMENTS = [build_problem_area_document(slug) for slug in PROBLEM_PAGE_ORDER]
PERSONAL_YEAR_DOCUMENTS = [build_personal_year_document(number) for number in range(1, 10)]
