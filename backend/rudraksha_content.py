from __future__ import annotations

from copy import deepcopy


SITE_NAME = "EverydayHoroscope"
NUMBER_WORDS = {
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
    10: "Ten",
    11: "Eleven",
    12: "Twelve",
    13: "Thirteen",
    14: "Fourteen",
    15: "Fifteen",
    16: "Sixteen",
    17: "Seventeen",
    18: "Eighteen",
    19: "Nineteen",
    20: "Twenty",
    21: "Twenty One",
}

_MUKHI_CORE = [
    {
        "mukhi": 1,
        "ruling_deity": "Lord Shiva",
        "ruling_planet": "Sun",
        "overview": "A rare bead for inner authority, concentration, and a more settled spiritual practice.",
        "benefits": ["clarity", "leadership", "meditation depth", "confidence", "solar vitality"],
        "best_for": ["deep meditation", "leadership roles", "public responsibility", "self-mastery"],
        "cautions": [
            "Best approached with sincerity rather than as a status object.",
            "If you are already working with strong solar remedies, combine it only with guidance.",
        ],
        "wearing_instructions": {
            "day": "Sunday",
            "metal": "Gold or copper",
            "mantra": "Om Hreem Namah",
            "how_to_wear": "Wear as a pendant close to the heart after morning prayer.",
        },
        "rarity": "Extremely rare",
        "price_range": "Very high",
        "related_mukhis": [12, 5, 14],
    },
    {
        "mukhi": 2,
        "ruling_deity": "Ardhanarishvara",
        "ruling_planet": "Moon",
        "overview": "A harmonising bead used for emotional balance, softer communication, and relationship healing.",
        "benefits": ["emotional steadiness", "relationship harmony", "receptivity", "calmness", "heart-centred listening"],
        "best_for": ["marital harmony", "family healing", "mood balance", "partnership work"],
        "cautions": [
            "Works best when worn consistently rather than only during stressful periods.",
            "Use gentle expectations if emotional instability comes from medical causes.",
        ],
        "wearing_instructions": {
            "day": "Monday",
            "metal": "Silver",
            "mantra": "Om Namah",
            "how_to_wear": "Wear as a pendant or bracelet after offering water or milk in prayer.",
        },
        "rarity": "Rare",
        "price_range": "High",
        "related_mukhis": [5, 6, 16],
    },
    {
        "mukhi": 3,
        "ruling_deity": "Agni",
        "ruling_planet": "Mars",
        "overview": "A fiery cleansing bead linked with courage, momentum, and releasing old emotional residue.",
        "benefits": ["courage", "action", "release from guilt", "motivation", "digestive fire"],
        "best_for": ["confidence rebuilding", "students under pressure", "athletic drive", "moving past setbacks"],
        "cautions": [
            "Strong Mars types may prefer to balance it with grounding practices.",
            "Avoid treating it as a substitute for anger management or therapy.",
        ],
        "wearing_instructions": {
            "day": "Tuesday",
            "metal": "Copper",
            "mantra": "Om Kleem Namah",
            "how_to_wear": "Wear after sunrise once the bead has been cleansed and energised with mantra.",
        },
        "rarity": "Moderately available",
        "price_range": "Medium",
        "related_mukhis": [6, 9, 14],
    },
    {
        "mukhi": 4,
        "ruling_deity": "Lord Brahma",
        "ruling_planet": "Mercury",
        "overview": "A knowledge-oriented bead associated with speech, memory, organisation, and learning flow.",
        "benefits": ["memory", "communication", "creativity", "analytical clarity", "learning ease"],
        "best_for": ["students", "writers", "teachers", "speakers"],
        "cautions": [
            "Helps focus, but still needs disciplined study habits.",
            "If worn for career ambition alone, keep expectations practical and gradual.",
        ],
        "wearing_instructions": {
            "day": "Wednesday",
            "metal": "Silver or panchdhatu",
            "mantra": "Om Hreem Namah",
            "how_to_wear": "Wear as a pendant or on the right wrist after reciting the mantra mindfully.",
        },
        "rarity": "Common to moderate",
        "price_range": "Medium",
        "related_mukhis": [5, 6, 20],
    },
    {
        "mukhi": 5,
        "ruling_deity": "Kalagni Rudra",
        "ruling_planet": "Jupiter",
        "overview": "The universal Rudraksha for steadiness, grounded spirituality, and everyday wellbeing.",
        "benefits": ["peace", "discipline", "spiritual grounding", "health support", "wisdom"],
        "best_for": ["daily japa", "stress reduction", "students of scripture", "general wellbeing"],
        "cautions": [
            "The bead is gentle, but respectful handling is still recommended.",
            "It supports wellbeing practices; it does not replace medical care.",
        ],
        "wearing_instructions": {
            "day": "Thursday",
            "metal": "Thread, silver, or panchdhatu",
            "mantra": "Om Hreem Namah",
            "how_to_wear": "Wear as a mala or bracelet after a simple prayer and clean water rinse.",
        },
        "rarity": "Very common",
        "price_range": "Accessible",
        "related_mukhis": [1, 4, 12],
    },
    {
        "mukhi": 6,
        "ruling_deity": "Lord Kartikeya",
        "ruling_planet": "Venus",
        "overview": "A bead for refined discipline, self-respect, healthy attraction, and practical focus.",
        "benefits": ["self-control", "charisma", "clarity in relationships", "discipline", "creative steadiness"],
        "best_for": ["artists", "students", "relationship maturity", "habit correction"],
        "cautions": [
            "Best used to support restraint, not indulgence.",
            "If relationship patterns are severe, combine spiritual work with real behavioural change.",
        ],
        "wearing_instructions": {
            "day": "Friday",
            "metal": "Silver",
            "mantra": "Om Hreem Hum Namah",
            "how_to_wear": "After morning prayer, place it as a bracelet or pendant.",
        },
        "rarity": "Common",
        "price_range": "Accessible to medium",
        "related_mukhis": [2, 4, 13],
    },
    {
        "mukhi": 7,
        "ruling_deity": "Mahalakshmi and the Sapta Rishis",
        "ruling_planet": "Saturn",
        "overview": "A grounding bead used for financial steadiness, patience, and carrying karmic weight more gracefully.",
        "benefits": ["financial patience", "endurance", "protection during delays", "stability", "humility"],
        "best_for": ["debt pressure", "slow-moving careers", "business stability", "Saturn discipline"],
        "cautions": [
            "Works gradually and suits people prepared for steady effort.",
            "Do not expect quick gains without practical planning.",
        ],
        "wearing_instructions": {
            "day": "Saturday",
            "metal": "Silver or panchdhatu",
            "mantra": "Om Hum Namah",
            "how_to_wear": "Wear after a calm Saturday prayer, ideally with a disciplined routine.",
        },
        "rarity": "Moderately available",
        "price_range": "Medium to high",
        "related_mukhis": [8, 14, 17],
    },
    {
        "mukhi": 8,
        "ruling_deity": "Lord Ganesha",
        "ruling_planet": "Ketu",
        "overview": "An obstacle-clearing bead used when life feels blocked, scattered, or repeatedly derailed.",
        "benefits": ["obstacle removal", "clarity under confusion", "safer transitions", "focus", "karmic untangling"],
        "best_for": ["new beginnings", "legal or career hurdles", "sudden disruptions", "travel uncertainty"],
        "cautions": [
            "Useful for clearing a path, but it does not remove the need for wise decisions.",
            "Pair with grounding habits if you already feel mentally overstimulated.",
        ],
        "wearing_instructions": {
            "day": "Wednesday or Saturday",
            "metal": "Silver",
            "mantra": "Om Ganeshaya Namah",
            "how_to_wear": "Wear after invoking Ganesha before important new starts or transitions.",
        },
        "rarity": "Rare",
        "price_range": "High",
        "related_mukhis": [7, 9, 10],
    },
    {
        "mukhi": 9,
        "ruling_deity": "Goddess Durga",
        "ruling_planet": "Rahu",
        "overview": "A protective bead for fierce resolve, spiritual courage, and moving through shadowy periods with strength.",
        "benefits": ["protection", "fearlessness", "drive", "resilience", "energetic shielding"],
        "best_for": ["people in high-pressure roles", "times of uncertainty", "self-protection", "deep spiritual practice"],
        "cautions": [
            "Can feel intense for very sensitive people; introduce it gradually.",
            "Works best when paired with disciplined prayer rather than impulse.",
        ],
        "wearing_instructions": {
            "day": "Friday or Tuesday",
            "metal": "Silver or red thread",
            "mantra": "Om Hreem Hum Namah",
            "how_to_wear": "After Durga mantra or quiet prayer, place it for strength and protection.",
        },
        "rarity": "Rare",
        "price_range": "High",
        "related_mukhis": [3, 8, 10],
    },
    {
        "mukhi": 10,
        "ruling_deity": "Lord Vishnu",
        "ruling_planet": "All Planets",
        "overview": "A broad protective bead chosen when someone wants stabilising support across many moving parts at once.",
        "benefits": ["protection", "energetic balance", "calmness", "stability", "resilience under pressure"],
        "best_for": ["general protection", "travel", "family peace", "times of mixed transits"],
        "cautions": [
            "Helpful as a stabiliser, but not a shortcut around deeper chart work.",
            "If your need is very specific, a planet-linked bead may still be more precise.",
        ],
        "wearing_instructions": {
            "day": "Thursday",
            "metal": "Silver or panchdhatu",
            "mantra": "Om Hreem Namah",
            "how_to_wear": "Wear as a pendant after a prayer for protection and steadiness.",
        },
        "rarity": "Rare",
        "price_range": "High",
        "related_mukhis": [8, 9, 11],
    },
    {
        "mukhi": 11,
        "ruling_deity": "Ekadasha Rudra",
        "ruling_planet": "None",
        "overview": "A bead for courage, disciplined action, and speaking or acting from inner conviction.",
        "benefits": ["courage", "decision-making", "discipline", "inner strength", "clear expression"],
        "best_for": ["leaders", "entrepreneurs", "spiritual practitioners", "public speaking"],
        "cautions": [
            "Its force is best channelled through restraint and ethics.",
            "Do not use it to justify impulsive behaviour or domination.",
        ],
        "wearing_instructions": {
            "day": "Monday",
            "metal": "Silver or thread",
            "mantra": "Om Hreem Hum Namah",
            "how_to_wear": "After a focused prayer, place it when you need steadiness in speech and action.",
        },
        "rarity": "Rare",
        "price_range": "High",
        "related_mukhis": [10, 12, 14],
    },
    {
        "mukhi": 12,
        "ruling_deity": "Lord Surya",
        "ruling_planet": "Sun",
        "overview": "A bright, forceful bead associated with stature, vitality, and healthy self-command.",
        "benefits": ["authority", "radiance", "confidence", "career visibility", "vitality"],
        "best_for": ["administrators", "public roles", "confidence rebuilding", "leadership presence"],
        "cautions": [
            "Strong personalities should balance it with humility and rest.",
            "If heat, ego, or overexertion are already high, introduce it carefully.",
        ],
        "wearing_instructions": {
            "day": "Sunday",
            "metal": "Gold or copper",
            "mantra": "Om Kraum Sraum Raum Namah",
            "how_to_wear": "Wear after sunrise prayer, especially when seeking clean authority and vitality.",
        },
        "rarity": "Rare",
        "price_range": "High",
        "related_mukhis": [1, 5, 19],
    },
    {
        "mukhi": 13,
        "ruling_deity": "Lord Indra and Kamadeva",
        "ruling_planet": "Venus",
        "overview": "A refinement bead for attraction, presentation, creative magnetism, and tasteful expansion.",
        "benefits": ["charisma", "creativity", "relationship magnetism", "luxury consciousness", "artistic flow"],
        "best_for": ["artists", "performers", "brand builders", "relationship confidence"],
        "cautions": [
            "Best used for refinement, not manipulation.",
            "Ground it with values if vanity or restlessness are already high.",
        ],
        "wearing_instructions": {
            "day": "Friday",
            "metal": "Silver or gold",
            "mantra": "Om Hreem Namah",
            "how_to_wear": "Wear after Friday prayer when seeking grace, beauty, or creative flow.",
        },
        "rarity": "Very rare",
        "price_range": "Very high",
        "related_mukhis": [6, 12, 19],
    },
    {
        "mukhi": 14,
        "ruling_deity": "Mahadeva",
        "ruling_planet": "Saturn",
        "overview": "A high-potency protection bead associated with intuition, karmic steadiness, and major life turning points.",
        "benefits": ["protection", "foresight", "stability in upheaval", "intuition", "deep grounding"],
        "best_for": ["major transitions", "risk management", "spiritual discipline", "serious karmic phases"],
        "cautions": [
            "Traditionally considered a powerful bead and best worn with reverence.",
            "If you are new to Rudraksha, many people begin with gentler beads first.",
        ],
        "wearing_instructions": {
            "day": "Monday or Saturday",
            "metal": "Silver or panchdhatu",
            "mantra": "Om Namah",
            "how_to_wear": "Wear after cleansing and energising it during a quiet prayerful setting.",
        },
        "rarity": "Extremely rare",
        "price_range": "Very high",
        "related_mukhis": [7, 11, 21],
    },
    {
        "mukhi": 15,
        "ruling_deity": "Lord Pashupatinath",
        "ruling_planet": "Mercury",
        "overview": "A heart-mind balancing bead used for emotional repair, trust, and gentler self-relationship.",
        "benefits": ["emotional healing", "self-acceptance", "relief from isolation", "mental softness", "compassion"],
        "best_for": ["heartbreak recovery", "inner work", "relationship reflection", "quiet healing phases"],
        "cautions": [
            "It can support healing, but not replace counselling or mental healthcare.",
            "Works best when worn with honesty about the patterns you are trying to change.",
        ],
        "wearing_instructions": {
            "day": "Wednesday or Monday",
            "metal": "Silver",
            "mantra": "Om Namah Shivaya",
            "how_to_wear": "Wear after a calm prayer, especially when working through emotional strain.",
        },
        "rarity": "Very rare",
        "price_range": "Very high",
        "related_mukhis": [2, 4, 16],
    },
    {
        "mukhi": 16,
        "ruling_deity": "Mahamrityunjaya Shiva",
        "ruling_planet": "Moon",
        "overview": "A deeply protective bead for fear release, emotional fortitude, and inner steadiness during crisis.",
        "benefits": ["fear release", "mental peace", "protection during difficult phases", "emotional resilience", "restfulness"],
        "best_for": ["health anxiety", "high-stress periods", "nighttime fear", "spiritual resilience"],
        "cautions": [
            "Supportive during crisis, but should not delay urgent medical or legal action.",
            "Sensitive wearers may prefer to acclimatise gradually.",
        ],
        "wearing_instructions": {
            "day": "Monday",
            "metal": "Silver",
            "mantra": "Om Hreem Hum Namah",
            "how_to_wear": "After reciting a Mahamrityunjaya prayer or sitting quietly in devotion, place it gently.",
        },
        "rarity": "Very rare",
        "price_range": "Very high",
        "related_mukhis": [2, 9, 15],
    },
    {
        "mukhi": 17,
        "ruling_deity": "Goddess Katyayani",
        "ruling_planet": "Saturn",
        "overview": "A rare bead linked with graceful expansion, visibility, and gains earned through persistence.",
        "benefits": ["prosperity", "recognition", "growth opportunities", "business expansion", "confidence"],
        "best_for": ["entrepreneurs", "investors", "brand growth", "measured ambition"],
        "cautions": [
            "Useful for expansion, but strong financial choices still matter more than symbolism.",
            "Avoid wearing it from pure greed or without a stable plan.",
        ],
        "wearing_instructions": {
            "day": "Saturday or Friday",
            "metal": "Gold or silver",
            "mantra": "Om Hreem Hum Namah",
            "how_to_wear": "Approach it prayerfully when seeking responsible growth rather than reckless gain.",
        },
        "rarity": "Extremely rare",
        "price_range": "Very high",
        "related_mukhis": [7, 13, 21],
    },
    {
        "mukhi": 18,
        "ruling_deity": "Bhumi Devi",
        "ruling_planet": "Earth / Mars",
        "overview": "A stabilising bead for grounding, land matters, and restoring a sense of safety and rootedness.",
        "benefits": ["grounding", "property support", "stability", "nourishment", "material steadiness"],
        "best_for": ["real-estate matters", "family security", "grounding after upheaval", "practical stability"],
        "cautions": [
            "Helpful for stability themes, but it will not resolve disputes without real action.",
            "Best used with patience when life feels materially unsettled.",
        ],
        "wearing_instructions": {
            "day": "Tuesday or Friday",
            "metal": "Copper or silver",
            "mantra": "Om Hreem Shreem Vasudhaye Namah",
            "how_to_wear": "Wear after a brief prayer for stability, safety, and grounded progress.",
        },
        "rarity": "Extremely rare",
        "price_range": "Very high",
        "related_mukhis": [3, 7, 19],
    },
    {
        "mukhi": 19,
        "ruling_deity": "Lord Narayana",
        "ruling_planet": "Sun",
        "overview": "A blessing bead associated with fuller success, alignment, and a more generous life current.",
        "benefits": ["prosperity", "fulfilment", "grace", "confidence", "purpose alignment"],
        "best_for": ["balanced ambition", "householders", "career success", "spiritual material balance"],
        "cautions": [
            "Can amplify desire, so it is best worn with clarity about values.",
            "It supports opportunity, not entitlement.",
        ],
        "wearing_instructions": {
            "day": "Sunday or Thursday",
            "metal": "Gold",
            "mantra": "Om Vam Vishnave Namah",
            "how_to_wear": "Wear after prayer when seeking both protection and prosperous alignment.",
        },
        "rarity": "Extremely rare",
        "price_range": "Very high",
        "related_mukhis": [12, 13, 21],
    },
    {
        "mukhi": 20,
        "ruling_deity": "Lord Brahma",
        "ruling_planet": "Moon and Venus",
        "overview": "A rare contemplative bead linked with higher insight, wise decisions, and a more spacious intellect.",
        "benefits": ["clarity", "higher wisdom", "protective insight", "creative intelligence", "discernment"],
        "best_for": ["researchers", "teachers", "spiritual study", "big-picture decision-making"],
        "cautions": [
            "Its benefits are subtle and tend to reward sincere reflective practice.",
            "Do not expect intellectual growth without actual study or contemplation.",
        ],
        "wearing_instructions": {
            "day": "Thursday or Friday",
            "metal": "Gold or silver",
            "mantra": "Om Hreem Brahmane Namah",
            "how_to_wear": "Wear after study, prayer, or meditation when cultivating insight and discrimination.",
        },
        "rarity": "Extremely rare",
        "price_range": "Very high",
        "related_mukhis": [4, 5, 21],
    },
    {
        "mukhi": 21,
        "ruling_deity": "Lord Kubera",
        "ruling_planet": "All Planets",
        "overview": "A culmination bead connected with abundance, protection of assets, and expansive stewardship.",
        "benefits": ["abundance", "asset protection", "expansion", "authority", "benefic support"],
        "best_for": ["major wealth stewardship", "founders", "philanthropic leaders", "legacy building"],
        "cautions": [
            "Traditionally treated as a high-order bead and not worn casually.",
            "Best suited to mature spiritual or financial responsibility rather than display.",
        ],
        "wearing_instructions": {
            "day": "Thursday",
            "metal": "Gold",
            "mantra": "Om Hreem Kuberaya Namah",
            "how_to_wear": "Wear after formal energising and prayer, usually as a pendant rather than an everyday bracelet.",
        },
        "rarity": "One of the rarest",
        "price_range": "Exceptional",
        "related_mukhis": [14, 17, 19],
    },
]

def _hash_index(*values: str, modulus: int) -> int:
    total = 0
    for value in values:
        for char in value:
            total += ord(char)
    return total % modulus


def _variant_text(page_key: str, answer_index: int, variants: list[str], **kwargs: str) -> str:
    template = variants[_hash_index(page_key, str(answer_index), modulus=5)]
    return template.format(**kwargs)


def _comma_phrase(items: list[str], limit: int = 3) -> str:
    return ", ".join(items[:limit])


def _word_mukhi_label(mukhi: int) -> str:
    return f"{NUMBER_WORDS[mukhi]} Mukhi Rudraksha"


def _faq_bead_label(reference: dict) -> str:
    return f"{NUMBER_WORDS[int(reference['mukhi'])]} Mukhi"


def _mukhi_meta_title(payload: dict) -> str:
    word_label = _word_mukhi_label(int(payload["mukhi"]))
    benefit_one = str(payload["benefits"][0]).title()
    benefit_two = str(payload["benefits"][1]).title()
    planet = str(payload["ruling_planet"])
    return f"{word_label} for {benefit_one}, {benefit_two} and {planet} Support | {SITE_NAME}"


def _faq_items(page_key: str, name: str, overview: str, benefits: list[str], instructions: dict[str, str]) -> list[dict[str, str]]:
    answer_name = f"{NUMBER_WORDS[int(str(page_key).split('-')[0])]} Mukhi"
    benefit_text = _comma_phrase(benefits, limit=3)
    benefit_four = _comma_phrase(benefits, limit=4)
    benefit_one = str(benefits[0])
    benefit_two = str(benefits[1] if len(benefits) > 1 else benefits[0])
    benefit_three = str(benefits[2] if len(benefits) > 2 else benefit_two)
    overview_lower = overview.lower()
    wearing_lower = instructions["how_to_wear"].lower()
    answers = [
        _variant_text(
            page_key,
            0,
            [
                "Best for {benefit_one}, {benefit_two}, and {benefit_three}.",
                "{answer_name} fits {benefit_one} with {benefit_two}.",
                "Think {benefit_three} plus {benefit_one}; that is where {answer_name} fits.",
                "Choose {answer_name} for {benefit_two} and {benefit_three}.",
                "{answer_name} often clusters with {benefit_one} and {benefit_three}.",
            ],
            answer_name=answer_name,
            benefit_one=benefit_one,
            benefit_two=benefit_two,
            benefit_three=benefit_three,
        ),
        _variant_text(
            page_key,
            1,
            [
                "Profile: {overview_lower} Main themes: {benefit_one}, {benefit_two}, {benefit_three}.",
                "{overview_lower} Focus words: {benefit_one}, {benefit_two}, {benefit_three}.",
                "{answer_name} links {benefit_one}, {benefit_two}, and {benefit_three} to {overview_lower}.",
                "{benefit_one}, {benefit_two}, and {benefit_three} form the short reading of {answer_name}.",
                "{overview_lower} That profile usually shows up through {benefit_one}, {benefit_two}, and {benefit_three}.",
            ],
            answer_name=answer_name,
            overview_lower=overview_lower,
            benefit_one=benefit_one,
            benefit_two=benefit_two,
            benefit_three=benefit_three,
        ),
        _variant_text(
            page_key,
            2,
            [
                "{day}; {mantra}; the {answer_name} rule is {wearing_lower}.",
                "Start on {day}; {mantra} belongs to {answer_name}; {wearing_lower}.",
                "{answer_name}: {day}; {mantra}; the rule is {wearing_lower}.",
                "{mantra} guides {answer_name} on {day}; the rule is {wearing_lower}.",
                "{day} with {mantra} keeps {answer_name} aligned with {wearing_lower}.",
            ],
            answer_name=answer_name,
            mantra=instructions["mantra"],
            day=instructions["day"],
            wearing_lower=wearing_lower,
        ),
        _variant_text(
            page_key,
            3,
            [
                "Use only when {benefit_one} or {benefit_two} is real.",
                "{benefit_three} and {benefit_one} should be genuine before choosing {answer_name}.",
                "{answer_name} suits genuine {benefit_two} needs, not impulse.",
                "Choose {answer_name} only if {benefit_one} and {benefit_three} truly fit.",
                "{benefit_two} with {benefit_three} is the right signal for {answer_name}.",
            ],
            answer_name=answer_name,
            benefit_one=benefit_one,
            benefit_two=benefit_two,
            benefit_three=benefit_three,
        ),
        _variant_text(
            page_key,
            4,
            [
                "{metal}; {how_to_wear}.",
                "Wear through {metal}, then keep to {how_to_wear}.",
                "{answer_name} usually goes in {metal}; after that, {how_to_wear}.",
                "{metal} is standard for {answer_name}; the practice is {how_to_wear}.",
                "For {answer_name}, use {metal} and keep to {how_to_wear}.",
            ],
            answer_name=answer_name,
            metal=instructions["metal"],
            how_to_wear=instructions["how_to_wear"].lower(),
        ),
    ]
    return [
        {"q": f"Who should wear {name}?", "a": answers[0]},
        {"q": f"What are the benefits of {name}?", "a": answers[1]},
        {"q": f"How do I activate {name}?", "a": answers[2]},
        {"q": f"Can anyone wear {name}?", "a": answers[3]},
        {"q": f"How should {name} be worn?", "a": answers[4]},
    ]


def _build_document(payload: dict) -> dict:
    mukhi = int(payload["mukhi"])
    title = f"{mukhi} Mukhi Rudraksha"
    slug = f"{mukhi}-mukhi"
    meta_title = _mukhi_meta_title(payload)
    meta_description = (
        f"{mukhi} Mukhi Rudraksha is traditionally associated with {payload['ruling_planet']}. "
        f"Discover its benefits, who may wear it, the activation mantra, and step-by-step wearing guidance."
    )
    return {
        "mukhi": mukhi,
        "name": title,
        "slug": slug,
        "overview": payload["overview"],
        "ruling_deity": payload["ruling_deity"],
        "ruling_planet": payload["ruling_planet"],
        "benefits": list(payload["benefits"]),
        "wearing_instructions": dict(payload["wearing_instructions"]),
        "cautions": list(payload["cautions"]),
        "best_for": list(payload["best_for"]),
        "rarity": payload["rarity"],
        "price_range": payload["price_range"],
        "related_mukhis": list(payload["related_mukhis"]),
        "faq": _faq_items(slug, title, payload["overview"], list(payload["benefits"]), dict(payload["wearing_instructions"])),
        "meta_title": meta_title,
        "meta_description": meta_description,
    }


RUDRAKSHA_MUKHIS = [_build_document(item) for item in _MUKHI_CORE]
RUDRAKSHA_MUKHIS_BY_NUMBER = {item["mukhi"]: item for item in RUDRAKSHA_MUKHIS}


def get_rudraksha_documents() -> list[dict]:
    return deepcopy(RUDRAKSHA_MUKHIS)


def get_rudraksha_document(mukhi: int) -> dict | None:
    payload = RUDRAKSHA_MUKHIS_BY_NUMBER.get(int(mukhi))
    return deepcopy(payload) if payload else None


PLANET_TO_PRIMARY_MUKHI = {
    "Sun": 1,
    "Moon": 2,
    "Mars": 3,
    "Mercury": 4,
    "Jupiter": 5,
    "Venus": 6,
    "Saturn": 7,
    "Rahu": 8,
    "Ketu": 9,
}


def _mukhi_reference(mukhi: int, *, fit_reason: str | None = None) -> dict:
    payload = get_rudraksha_document(mukhi)
    if not payload:
        raise KeyError(f"Unknown mukhi: {mukhi}")
    reference = {
        "mukhi": payload["mukhi"],
        "name": payload["name"],
        "slug": payload["slug"],
        "overview": payload["overview"],
        "ruling_deity": payload["ruling_deity"],
        "ruling_planet": payload["ruling_planet"],
        "benefits": list(payload["benefits"]),
        "wearing_instructions": dict(payload["wearing_instructions"]),
        "rarity": payload["rarity"],
        "price_range": payload["price_range"],
    }
    if fit_reason:
        reference["fit_reason"] = fit_reason
    return reference


def _faq_from_pairs(items: list[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"q": question, "a": answer} for question, answer in items]


def _planet_meta_title(planet: str, primary: dict, secondary: dict | None) -> str:
    benefit_one = str(primary["benefits"][0]).title()
    benefit_two = str(primary["benefits"][1]).title()
    if secondary:
        return f"{planet} Rudraksha with {primary['name']} and {secondary['name']} for {benefit_one} and {benefit_two} | {SITE_NAME}"
    return f"{planet} Rudraksha with {primary['name']} for {benefit_one} and {benefit_two} | {SITE_NAME}"


def _problem_meta_title(problem: str, primary: dict, supporting: list[dict]) -> str:
    support_phrase = _faq_bead_label(supporting[0]) if supporting else "single-bead support"
    fit_phrase = str(primary.get("fit_reason") or primary["overview"]).replace("Rudraksha", "bead")
    return f"{problem} Rudraksha for {fit_phrase} with {support_phrase} | {SITE_NAME}"


def _sign_meta_title(sign: str, primary: dict, payload: dict) -> str:
    challenge_one = str(payload["typical_challenges"][0]).title()
    challenge_two = str(payload["typical_challenges"][1]).title()
    return f"{sign} Rudraksha with {primary['name']} for {challenge_one} Balance and {challenge_two} Relief | {SITE_NAME}"


_PLANET_META_DESCS: dict[str, str] = {
    "sun": "Which Rudraksha bead strengthens Sun -- its effect on vitality, authority, and self-respect, and the correct mukhi, mantra, and wearing day.",
    "moon": "Which Rudraksha supports the Moon -- its role in emotional balance, intuition, and mental steadiness, with mukhi guidance and activation mantra.",
    "mars": "Which Rudraksha works with Mars energy -- channelling courage and drive productively, with the right mukhi, mantra, and cautions for intensity.",
    "mercury": "Which Rudraksha enhances Mercury -- its benefits for communication, intelligence, and decision timing, with mukhi selection and wearing method.",
    "jupiter": "Which Rudraksha amplifies Jupiter's blessings -- its effect on wisdom, growth, and spiritual progress, with correct mukhi and activation guidance.",
    "venus": "Which Rudraksha aligns with Venus -- its influence on harmony, creativity, and relationship quality, with mukhi guidance and traditional wearing rules.",
    "saturn": "Which Rudraksha eases Saturn's lessons -- its role in building discipline, endurance, and karmic clarity, with the right mukhi and mantra.",
    "rahu": "Which Rudraksha balances Rahu -- its effect on obsession, ambition, and non-traditional drives, with traditional mukhi choices and wearing guidance.",
    "ketu": "Which Rudraksha supports Ketu's detachment -- its role in spiritual clarity and letting go, with suitable mukhi, mantra, and wearing method.",
}

_SIGN_META_DESCS: dict[str, str] = {
    "aries": "Best Rudraksha for Aries -- the Mars-ruled mukhi for leadership and fire, plus a grounding bead to steady impulsive energy and protect stamina.",
    "taurus": "Best Rudraksha for Taurus -- the Venus-ruled mukhi for beauty and stability, with a supporting bead for patience and material groundedness.",
    "gemini": "Best Rudraksha for Gemini -- the Mercury-ruled mukhi for communication and adaptability, plus a secondary bead for mental focus and consistency.",
    "cancer": "Best Rudraksha for Cancer -- the Moon-ruled mukhi for emotional nurturing and intuition, with a supporting bead for security and inner calm.",
    "leo": "Best Rudraksha for Leo -- the Sun-ruled mukhi for confidence and vitality, plus a grounding bead for ego balance and heart-centred leadership.",
    "virgo": "Best Rudraksha for Virgo -- the Mercury-ruled mukhi for precision and health awareness, with a secondary bead for reducing over-analysis.",
    "libra": "Best Rudraksha for Libra -- the Venus-ruled mukhi for balance and relationship harmony, plus a supporting bead for decisiveness and inner clarity.",
    "scorpio": "Best Rudraksha for Scorpio -- the Mars and Ketu-aligned mukhi for transformation, with a secondary bead for grounding intensity and emotional depth.",
    "sagittarius": "Best Rudraksha for Sagittarius -- the Jupiter-ruled mukhi for expansion and wisdom, with a supporting bead for follow-through and practical focus.",
    "capricorn": "Best Rudraksha for Capricorn -- the Saturn-ruled mukhi for discipline and long-term structure, plus a secondary bead for easing karmic pressure.",
    "aquarius": "Best Rudraksha for Aquarius -- the Saturn and Rahu-aligned mukhi for innovation and detachment, with a grounding bead for social connection.",
    "pisces": "Best Rudraksha for Pisces -- the Jupiter and Ketu-aligned mukhi for spirituality and compassion, with a supporting bead for boundaries and clarity.",
}

_PLANET_CORE = [
    {
        "slug": "sun",
        "planet": "Sun",
        "primary": 1,
        "secondary": 12,
        "intro": "The Sun in Vedic astrology governs vitality, self-respect, visibility, and the ability to act from a clear centre. A Rudraksha chosen for the Sun is traditionally used to stabilise confidence, authority, and disciplined life force.",
        "wearing_guidance": {
            "metal": "Gold or copper",
            "thread_color": "Red or saffron",
            "mantra": "Om Hreem Namah",
            "day_to_energise": "Sunday sunrise",
            "finger": "Right hand ring finger or as a pendant",
        },
        "who_needs_this": [
            "Low confidence despite ability",
            "Difficulty being recognised or taking leadership responsibility",
            "Fatigue, low drive, or a scattered sense of purpose",
            "A weak or afflicted Sun in chart interpretation",
        ],
        "contraindications": [
            "Approach carefully if you already run very hot, ego-driven, or over-aggressive in your solar expression.",
            "If your chart work already includes a strong Sun remedy stack, add this only with guidance.",
        ],
    },
    {
        "slug": "moon",
        "planet": "Moon",
        "primary": 2,
        "secondary": None,
        "intro": "The Moon governs emotional steadiness, receptivity, sleep quality, and the way you process nourishment and relationships. Rudraksha for the Moon is traditionally chosen to soften mental turbulence and restore inner calm.",
        "wearing_guidance": {
            "metal": "Silver",
            "thread_color": "White",
            "mantra": "Om Namah",
            "day_to_energise": "Monday morning",
            "finger": "Little finger or pendant near the heart",
        },
        "who_needs_this": [
            "Emotional fluctuation or oversensitivity",
            "Difficulty feeling settled in relationships or at home",
            "Sleep disruption linked with mental overactivity",
            "A weakened Moon in chart guidance",
        ],
        "contraindications": [
            "Very passive personalities should combine Moon support with grounded routines so softness does not become inertia.",
            "It supports emotional balance, but it does not replace mental-health care when that is needed.",
        ],
    },
    {
        "slug": "mars",
        "planet": "Mars",
        "primary": 3,
        "secondary": None,
        "intro": "Mars represents courage, heat, assertion, immune fire, and the ability to move through obstacles decisively. Rudraksha for Mars is used when strength must be steadied rather than allowed to become rage or exhaustion.",
        "wearing_guidance": {
            "metal": "Copper",
            "thread_color": "Red",
            "mantra": "Om Kleem Namah",
            "day_to_energise": "Tuesday sunrise",
            "finger": "Right hand ring finger or bracelet",
        },
        "who_needs_this": [
            "Low courage or trouble acting when action is needed",
            "Stored anger, irritability, or frustration",
            "Recovery from guilt, shame, or discouragement",
            "A weak Mars in traditional chart reading",
        ],
        "contraindications": [
            "If you already react impulsively or aggressively, wear it with deliberate restraint practices.",
            "Strong Mars personalities may need balancing rather than more raw heat.",
        ],
    },
    {
        "slug": "mercury",
        "planet": "Mercury",
        "primary": 4,
        "secondary": None,
        "intro": "Mercury governs memory, speech, learning agility, trade, and the nervous system's processing rhythm. Rudraksha for Mercury is traditionally chosen to bring order, focus, and cleaner expression to an overloaded mind.",
        "wearing_guidance": {
            "metal": "Silver or panchdhatu",
            "thread_color": "Green",
            "mantra": "Om Hreem Namah",
            "day_to_energise": "Wednesday morning",
            "finger": "Little finger or pendant",
        },
        "who_needs_this": [
            "Memory drift or poor concentration",
            "Speech hesitation or unclear communication",
            "Restless mental energy that scatters focus",
            "A weak Mercury in chart interpretation",
        ],
        "contraindications": [
            "Helpful for focus, but still needs disciplined study habits and sleep hygiene.",
            "If overthinking is your main issue, use it with grounding rather than more mental stimulation.",
        ],
    },
    {
        "slug": "jupiter",
        "planet": "Jupiter",
        "primary": 5,
        "secondary": None,
        "intro": "Jupiter governs wisdom, teachers, ethics, expansion, blessings, and the stabilising force of spiritual intelligence. Rudraksha for Jupiter is chosen when guidance, peace, and principled growth need reinforcement.",
        "wearing_guidance": {
            "metal": "Thread, silver, or panchdhatu",
            "thread_color": "Yellow",
            "mantra": "Om Hreem Namah",
            "day_to_energise": "Thursday morning",
            "finger": "Index finger or mala",
        },
        "who_needs_this": [
            "Loss of faith, direction, or disciplined spiritual routine",
            "Difficulty learning from mentors or life lessons",
            "Stress-driven overreaction instead of wise response",
            "A weakened Jupiter in chart guidance",
        ],
        "contraindications": [
            "Because 5 Mukhi is gentle, the main caution is complacency: wear it with sincere practice, not superstition.",
            "It supports health and calm, but not as a substitute for treatment.",
        ],
    },
    {
        "slug": "venus",
        "planet": "Venus",
        "primary": 6,
        "secondary": 13,
        "intro": "Venus governs harmony, attraction, relationships, artistry, refinement, and the ability to enjoy life without losing balance. Rudraksha for Venus is used to steady desire, improve grace, and mature relationship energy.",
        "wearing_guidance": {
            "metal": "Silver",
            "thread_color": "White or pastel pink",
            "mantra": "Om Hreem Hum Namah",
            "day_to_energise": "Friday morning",
            "finger": "Right hand ring finger or pendant",
        },
        "who_needs_this": [
            "Relationship immaturity or repeated attraction drama",
            "Creative blockage or low aesthetic confidence",
            "Poor self-worth showing up in love or luxury choices",
            "A weak Venus in chart interpretation",
        ],
        "contraindications": [
            "Use carefully if you are already overly indulgent, vain, or pulled by addictive pleasure patterns.",
            "It supports graceful attraction, not manipulation or obsession.",
        ],
    },
    {
        "slug": "saturn",
        "planet": "Saturn",
        "primary": 7,
        "secondary": 14,
        "intro": "Saturn governs discipline, karmic maturity, endurance, delays, duty, and long-form resilience. Rudraksha for Saturn is chosen when life feels heavy, slow, or burdened and steadiness matters more than speed.",
        "wearing_guidance": {
            "metal": "Silver or panchdhatu",
            "thread_color": "Black or deep blue",
            "mantra": "Om Hum Namah",
            "day_to_energise": "Saturday morning",
            "finger": "Middle finger or pendant",
        },
        "who_needs_this": [
            "Long delays, debt pressure, or career stagnation",
            "Fear around responsibility or sustained effort",
            "Periods of isolation, karmic heaviness, or slow results",
            "A weak or harsh Saturn pattern in chart work",
        ],
        "contraindications": [
            "Saturn remedies work slowly, so avoid wearing them while expecting instant relief.",
            "Very new seekers may begin with the gentler 7 Mukhi before stronger Saturn-linked beads.",
        ],
    },
    {
        "slug": "rahu",
        "planet": "Rahu",
        "primary": 8,
        "secondary": 18,
        "intro": "Rahu governs obsession, ambition, disruption, unfamiliar territory, and the pressure to move through shadow without losing judgment. Rudraksha for Rahu is traditionally chosen for obstacle-clearing, grounding, and protection during confusing phases.",
        "wearing_guidance": {
            "metal": "Silver",
            "thread_color": "Smoky grey or black",
            "mantra": "Om Ganeshaya Namah",
            "day_to_energise": "Saturday or Wednesday",
            "finger": "Middle finger or pendant",
        },
        "who_needs_this": [
            "Confusion, obsession, or repeated derailment",
            "Sudden instability in career, travel, or reputation",
            "Fear of unseen obstacles or heavy external pressure",
            "Rahu Mahadasha or Rahu affliction in chart guidance",
        ],
        "contraindications": [
            "If you already feel mentally fragmented, wear Rahu support with grounding routines and simplified lifestyle rhythms.",
            "Use discernment so the remedy does not become another object of obsession.",
        ],
    },
    {
        "slug": "ketu",
        "planet": "Ketu",
        "primary": 9,
        "secondary": None,
        "intro": "Ketu governs detachment, spiritual intensity, past-life residue, and the sharp cutting away of false identities. Rudraksha for Ketu is traditionally used for courage, protection, and steadier spiritual focus when detachment turns into instability.",
        "wearing_guidance": {
            "metal": "Silver or red thread",
            "thread_color": "Red or saffron",
            "mantra": "Om Hreem Hum Namah",
            "day_to_energise": "Tuesday or Friday",
            "finger": "Pendant or bracelet",
        },
        "who_needs_this": [
            "Intense detachment, spiritual restlessness, or inner fear",
            "Loss of grounding during transformative periods",
            "Trouble converting spiritual force into stable action",
            "Ketu Mahadasha or Ketu affliction in chart guidance",
        ],
        "contraindications": [
            "If you are already very withdrawn, combine Ketu support with embodied daily routines.",
            "It supports spiritual courage, not escapism from worldly duties.",
        ],
    },
]


def _build_planet_document(payload: dict) -> dict:
    planet = payload["planet"]
    slug = payload["slug"]
    primary = _mukhi_reference(
        payload["primary"],
        fit_reason=f"{_mukhi_reference(payload['primary'])['name']} is traditionally linked with {planet} and is chosen when {planet.lower()} themes need steadier support.",
    )
    secondary_mukhi = None
    if payload.get("secondary"):
        secondary_number = int(payload["secondary"])
        secondary_mukhi = _mukhi_reference(
            secondary_number,
            fit_reason=f"{_mukhi_reference(secondary_number)['name']} is used as an alternative or companion when a stronger or more specialised {planet.lower()} remedy is desired.",
        )
    primary_label = _faq_bead_label(primary)
    support_role = _faq_bead_label(secondary_mukhi) if secondary_mukhi else f"no second {planet.lower()} bead"
    focus_one = str(payload["who_needs_this"][0]).lower()
    focus_two = str(payload["who_needs_this"][1]).lower()
    faq = _faq_from_pairs([
        (
            f"Which Rudraksha is best for {planet}?",
            _variant_text(
                slug,
                0,
                [
                    "{planet}: start with {primary_label}; keep {support_role} in backup.",
                    "{primary_label} leads {planet}; {support_role} only supports.",
                    "For {planet}, {primary_label} comes first; {support_role} stays secondary.",
                    "{planet} guidance begins with {primary_label}; backup is {support_role}.",
                    "{support_role} is secondary; {primary_label} carries the main {planet} role.",
                ],
                planet=planet,
                primary_label=primary_label,
                support_role=support_role,
                focus_one=focus_one,
                focus_two=focus_two,
            ),
        ),
        (
            f"Who should wear Rudraksha for {planet}?",
            _variant_text(
                slug,
                1,
                [
                    "{focus_one} and {focus_two} are the classic {planet} triggers.",
                    "{planet} support usually points to {focus_one} with {focus_two}.",
                    "{focus_one}; {focus_two}; that is this {planet} page.",
                    "Look at {planet} support when {focus_one} meets {focus_two}.",
                    "This {planet} guide speaks to {focus_one} and {focus_two}.",
                ],
                planet=planet,
                focus_one=focus_one,
                focus_two=focus_two,
            ),
        ),
        (
            f"When should Rudraksha for {planet} be energised?",
            _variant_text(
                slug,
                2,
                [
                    "{day}; {mantra}; {planet} activation.",
                    "Activate on {day} with {mantra}.",
                    "{planet} timing here is {day}, with {mantra}.",
                    "{mantra} plus {day} is the key {planet} ritual.",
                    "Use {day} and {mantra} for this {planet} bead.",
                ],
                planet=planet,
                day=payload["wearing_guidance"]["day_to_energise"],
                mantra=payload["wearing_guidance"]["mantra"],
            ),
        ),
        (
            f"Can I wear Rudraksha for {planet} with other beads?",
            _variant_text(
                slug,
                3,
                [
                    "Pair only if {focus_one} overlaps another real need.",
                    "{planet} layering works when {focus_two} meets a second need.",
                    "{primary_label} can pair, but only around {focus_one}.",
                    "Combine cautiously; {focus_two} should remain distinct.",
                    "A second bead is fine only if {focus_one} remains the reason.",
                ],
                planet=planet,
                primary_label=primary_label,
                focus_one=focus_one,
                focus_two=focus_two,
            ),
        ),
        (
            f"Should everyone wear Rudraksha for {planet}?",
            _variant_text(
                slug,
                4,
                [
                    "Not universal; use only when {focus_one} or {focus_two} is real.",
                    "Treat {planet} as optional unless {focus_two} is active.",
                    "Only choose {primary_label} when {focus_one} or {focus_two} is active.",
                    "Skip this {planet} remedy unless {focus_one} clearly fits.",
                    "Choose {planet} only when {focus_two} or close patterns are present.",
                ],
                planet=planet,
                primary_label=primary_label,
                focus_one=focus_one,
                focus_two=focus_two,
            ),
        ),
    ])
    return {
        "page_type": "planet",
        "slug": slug,
        "planet": planet,
        "title": f"Rudraksha for {planet} - Best Mukhi & How to Wear It",
        "intro": payload["intro"],
        "primary_mukhi": primary,
        "secondary_mukhi": secondary_mukhi,
        "wearing_guidance": dict(payload["wearing_guidance"]),
        "who_needs_this": list(payload["who_needs_this"]),
        "contraindications": list(payload["contraindications"]),
        "faq": faq,
        "meta_title": _planet_meta_title(planet, primary, secondary_mukhi),
        "meta_description": _PLANET_META_DESCS.get(payload["slug"], f"Discover the best Rudraksha for {planet}, including mukhi guidance, mantra, and traditional wearing rules."),
    }


PLANET_RUDRAKSHA_DATA = {
    item["slug"]: _build_planet_document(item)
    for item in _PLANET_CORE
}
PLANET_RUDRAKSHA_SLUGS = list(PLANET_RUDRAKSHA_DATA.keys())


_PROBLEM_CORE = [
    {
        "slug": "depression",
        "problem": "Depression / Low Mood",
        "key_mukhis": [1, 7],
        "intro": "This page addresses low mood from an energetic and devotional perspective: when heaviness, hopelessness, or inner dimness make it hard to feel purposeful. In tradition, Rudraksha is used here to support steadiness, not to replace mental-health care.",
        "mukhi_notes": {
            1: "1 Mukhi is chosen to rekindle clarity, inner dignity, and the sense that life still has a centre.",
            7: "7 Mukhi is used when mood drops under karmic heaviness, financial strain, or long periods of pressure.",
        },
        "combination_suggestion": "A gentle pairing of 7 Mukhi for grounding with 1 Mukhi for clarity may be used when low mood comes with fatigue and loss of direction, but strong combinations should still be approached carefully.",
        "wearing_method": {
            "thread": "Red or black thread depending on whether clarity or grounding is the main need",
            "metal": "Silver or copper",
            "mantra": "Om Hreem Namah",
            "activation_ritual": "Cleanse the bead, sit quietly at sunrise, and wear it after a short grounding prayer rather than during panic.",
        },
        "lifestyle_tips": [
            "Keep a simple sunrise routine, even if short.",
            "Reduce overstimulation and avoid late-night mental spirals.",
            "Pair spiritual remedies with real emotional support and treatment when needed.",
        ],
    },
    {
        "slug": "financial-stress",
        "problem": "Debt / Financial Stress",
        "key_mukhis": [7, 8],
        "intro": "Financial stress is traditionally treated as both a practical and karmic strain: pressure, fear, blocked movement, and difficulty seeing stable next steps. Rudraksha here is used for grounding, obstacle-clearing, and steadier decision-making.",
        "mukhi_notes": {
            7: "7 Mukhi is linked with Saturn-like endurance, patience, and carrying pressure without collapse.",
            8: "8 Mukhi is chosen when money problems are tangled with repeated obstacles, confusion, or blocked openings.",
        },
        "combination_suggestion": "7 and 8 Mukhi can be worn together when debt pressure is mixed with delays, business obstacles, or repeated setbacks.",
        "wearing_method": {
            "thread": "Black thread",
            "metal": "Silver",
            "mantra": "Om Hum Namah",
            "activation_ritual": "Energise on Saturday morning and wear only after setting one concrete financial action for the day.",
        },
        "lifestyle_tips": [
            "Track expenses honestly instead of avoiding them.",
            "Prioritise one debt or pressure point at a time.",
            "Avoid panic decisions during stress spikes.",
        ],
    },
    {
        "slug": "career-block",
        "problem": "Career Block",
        "key_mukhis": [6, 11],
        "intro": "A career block often shows up as stalled momentum, weak visibility, hesitation, or repeated near-misses. Rudraksha for this area is traditionally chosen to restore disciplined action and cleaner professional presence.",
        "mukhi_notes": {
            6: "6 Mukhi helps refine discipline, self-presentation, and practical focus in work environments.",
            11: "11 Mukhi supports courage, decisive movement, and the will to act instead of delaying.",
        },
        "combination_suggestion": "6 and 11 Mukhi can complement each other when the block is part confidence, part lack of disciplined action.",
        "wearing_method": {
            "thread": "Red or white thread",
            "metal": "Silver or panchdhatu",
            "mantra": "Om Hreem Hum Namah",
            "activation_ritual": "Wear after a morning prayer and before focused work rather than as a passive symbol.",
        },
        "lifestyle_tips": [
            "Set one visible output goal each week.",
            "Refine communication, not just effort.",
            "Avoid mixing career ambition with scattered priorities.",
        ],
    },
    {
        "slug": "relationship-problems",
        "problem": "Relationship Problems",
        "key_mukhis": [2, 14],
        "intro": "Relationship strain is often described in tradition as a problem of imbalance between softness and steadiness. Rudraksha for this area is used to support harmony, listening, and protection from repeated emotional shocks.",
        "mukhi_notes": {
            2: "2 Mukhi is chosen for emotional balance, cooperation, and restoring relational softness.",
            14: "14 Mukhi is used when relationship strain is tied to deep karmic patterns, instability, or repeated rupture.",
        },
        "combination_suggestion": "2 Mukhi is the gentler base. 14 Mukhi is better treated as a serious support bead rather than a casual addition.",
        "wearing_method": {
            "thread": "White or red thread",
            "metal": "Silver",
            "mantra": "Om Namah",
            "activation_ritual": "Wear after a calm Monday or Saturday prayer with a clear intention around truth and harmony.",
        },
        "lifestyle_tips": [
            "Slow down conflict conversations.",
            "Name patterns instead of only blaming events.",
            "Avoid wearing a relationship remedy while ignoring harmful behaviour.",
        ],
    },
    {
        "slug": "fear-anxiety",
        "problem": "Fear and Anxiety",
        "key_mukhis": [5, 9],
        "intro": "Fear and anxiety are traditionally approached as disturbances of grounding, trust, and inner protection. Rudraksha for this area is chosen to create steadier breath, calmer thought, and more courageous response.",
        "mukhi_notes": {
            5: "5 Mukhi offers broad calming and spiritual grounding when the system is overstimulated.",
            9: "9 Mukhi is chosen when fear is mixed with vulnerability, pressure, or the need for protective strength.",
        },
        "combination_suggestion": "5 Mukhi can serve as a daily baseline, while 9 Mukhi is added when protection and courage are equally needed.",
        "wearing_method": {
            "thread": "Yellow or red thread",
            "metal": "Silver",
            "mantra": "Om Hreem Hum Namah",
            "activation_ritual": "Chant before wearing, then take several slow breaths so the remedy begins in the body, not only the mind.",
        },
        "lifestyle_tips": [
            "Reduce doom-scrolling and nervous overstimulation.",
            "Use short grounding breath practices daily.",
            "Seek clinical support when anxiety becomes persistent or disabling.",
        ],
    },
    {
        "slug": "anger",
        "problem": "Anger Management",
        "key_mukhis": [3, 12],
        "intro": "Anger in the Rudraksha tradition is often treated as misdirected fire: force without clarity, heat without containment, or hurt turning into reaction. The right bead is chosen to purify and then steady that fire.",
        "mukhi_notes": {
            3: "3 Mukhi helps release stored heat, guilt, and frustrated internal pressure.",
            12: "12 Mukhi is used when anger is tied to pride, authority clashes, or an overheated solar temperament.",
        },
        "combination_suggestion": "Start with 3 Mukhi when anger feels reactive. Add 12 Mukhi only if the issue also involves wounded authority or misused personal power.",
        "wearing_method": {
            "thread": "Red thread",
            "metal": "Copper",
            "mantra": "Om Kleem Namah",
            "activation_ritual": "Energise on Tuesday or Sunday, then wear only with a conscious commitment to restraint.",
        },
        "lifestyle_tips": [
            "Do not speak at peak heat if it can be delayed.",
            "Move physical fire through exercise instead of argument.",
            "Notice the hurt beneath the anger.",
        ],
    },
    {
        "slug": "low-immunity",
        "problem": "Low Immunity / Frequent Illness",
        "key_mukhis": [5, 6],
        "intro": "Low immunity is described traditionally as a sign that the system needs steadier protection, routine, and vitality support. Rudraksha for this area is chosen to reinforce daily balance rather than create a dramatic short-term shift.",
        "mukhi_notes": {
            5: "5 Mukhi is the broad health and steadiness bead used for daily support.",
            6: "6 Mukhi is chosen when health dips are tied to exhaustion, depletion, or poor self-management.",
        },
        "combination_suggestion": "5 and 6 Mukhi can be worn together as a calm daily pair for routine-based vitality support.",
        "wearing_method": {
            "thread": "Yellow or white thread",
            "metal": "Silver",
            "mantra": "Om Hreem Namah",
            "activation_ritual": "Cleanse, chant, and wear after committing to one concrete health-supportive habit.",
        },
        "lifestyle_tips": [
            "Protect sleep as seriously as medicine.",
            "Eat at more regular times.",
            "Use Rudraksha as support, not as a reason to avoid medical evaluation.",
        ],
    },
    {
        "slug": "heart-blood-pressure",
        "problem": "Blood Pressure / Heart Issues",
        "key_mukhis": [12],
        "intro": "This page reflects a traditional devotional approach to pressure, circulation, and overstressed solar energy. It is supportive in a spiritual sense and never a replacement for medical care.",
        "mukhi_notes": {
            12: "12 Mukhi is associated with the Sun and is traditionally chosen when vitality, circulation, and overstrained authority-like pressure need harmonising support.",
        },
        "combination_suggestion": "Because this is a strong and specific bead, many people keep it as a single focused support rather than mixing it casually.",
        "wearing_method": {
            "thread": "Red thread",
            "metal": "Gold or copper",
            "mantra": "Om Kraum Sraum Raum Namah",
            "activation_ritual": "Wear after sunrise prayer with a calm pace rather than in a rushed state.",
        },
        "lifestyle_tips": [
            "Reduce overstimulation and reaction speed.",
            "Do not ignore prescribed treatment.",
            "Create more rhythm in food, sleep, and work timing.",
        ],
    },
    {
        "slug": "memory-concentration",
        "problem": "Memory and Concentration",
        "key_mukhis": [4],
        "intro": "Memory drift and poor concentration are often described as a scattered Mercury pattern: information enters, but does not settle. Rudraksha for this area is chosen to support order, recall, and cleaner mental processing.",
        "mukhi_notes": {
            4: "4 Mukhi is the traditional Mercury-linked bead for memory, speech, learning, and concentration.",
        },
        "combination_suggestion": "4 Mukhi is usually enough as the lead bead here, especially when the main problem is mental organisation rather than emotional strain.",
        "wearing_method": {
            "thread": "Green thread",
            "metal": "Silver or panchdhatu",
            "mantra": "Om Hreem Namah",
            "activation_ritual": "Wear on Wednesday after a few quiet minutes of study, prayer, or focused intention.",
        },
        "lifestyle_tips": [
            "Single-task more often.",
            "Write down important information instead of trusting overload.",
            "Protect sleep so memory consolidation can happen.",
        ],
    },
    {
        "slug": "negative-energy",
        "problem": "Negative Energy / Black Magic",
        "key_mukhis": [8, 10],
        "intro": "This page reflects a traditional protective use of Rudraksha when someone feels psychically burdened, obstructed, or repeatedly disturbed by unseen pressure. The emphasis is on protection, grounding, and obstacle-clearing.",
        "mukhi_notes": {
            8: "8 Mukhi is chosen to clear blockages and break repeating obstructive patterns.",
            10: "10 Mukhi is used as a broad protective field when the disturbance feels diffuse or difficult to name.",
        },
        "combination_suggestion": "8 and 10 Mukhi can be paired when the issue feels both obstructive and intrusive.",
        "wearing_method": {
            "thread": "Black thread",
            "metal": "Silver",
            "mantra": "Om Ganeshaya Namah",
            "activation_ritual": "Cleanse the bead, light a lamp, and wear it only after the mind is settled rather than frightened.",
        },
        "lifestyle_tips": [
            "Keep your living space orderly and ventilated.",
            "Reduce fear-based ritual excess.",
            "Seek grounded guidance rather than panic.",
        ],
    },
    {
        "slug": "evil-eye",
        "problem": "Evil Eye Protection",
        "key_mukhis": [10, 11],
        "intro": "In traditional remedy logic, the evil eye is handled through stronger personal protection, steadier will, and less energetic leakage. Rudraksha is used here as a protective devotional anchor.",
        "mukhi_notes": {
            10: "10 Mukhi is the broad shield bead traditionally chosen for external negativity and subtle protection.",
            11: "11 Mukhi reinforces inner strength and prevents fear from widening the opening to negative suggestion.",
        },
        "combination_suggestion": "10 Mukhi forms the main shield, while 11 Mukhi is added if the person also needs stronger inner resolve.",
        "wearing_method": {
            "thread": "Black or red thread",
            "metal": "Silver",
            "mantra": "Om Hreem Hum Namah",
            "activation_ritual": "Energise prayerfully and wear it with a focus on calm strength rather than superstition.",
        },
        "lifestyle_tips": [
            "Share less when energy feels exposed.",
            "Avoid feeding fear with constant checking.",
            "Strengthen daily prayer or centring practice.",
        ],
    },
    {
        "slug": "legal-issues",
        "problem": "Legal / Court Case Issues",
        "key_mukhis": [14, 17],
        "intro": "Legal pressure is traditionally treated as a mix of karmic weight, timing, protection, and disciplined persistence. Rudraksha for this area is chosen to support stability, foresight, and sustained confidence.",
        "mukhi_notes": {
            14: "14 Mukhi is used for protection, foresight, and grounded intuition in complex, high-stakes phases.",
            17: "17 Mukhi is chosen when the matter also concerns gains, reputation, or a long-haul success outcome.",
        },
        "combination_suggestion": "14 Mukhi is the heavier stabiliser, while 17 Mukhi can be supportive when the legal issue is strongly tied to business or financial outcomes.",
        "wearing_method": {
            "thread": "Black or yellow thread",
            "metal": "Silver or gold",
            "mantra": "Om Namah",
            "activation_ritual": "Wear after Saturday prayer and after committing to practical legal preparation.",
        },
        "lifestyle_tips": [
            "Do not let spiritual remedies replace professional legal action.",
            "Keep records organised.",
            "Prioritise patience over emotional escalation.",
        ],
    },
    {
        "slug": "marriage-delay",
        "problem": "Marriage Delays",
        "key_mukhis": [2, 13],
        "intro": "Marriage delay is traditionally approached through harmony, receptivity, timing, and refinement of relationship karma. Rudraksha here is chosen to soften blockages while strengthening attraction and readiness.",
        "mukhi_notes": {
            2: "2 Mukhi supports partnership harmony and emotional readiness for union.",
            13: "13 Mukhi is used when attraction, grace, or marital magnetism need reinforcement.",
        },
        "combination_suggestion": "2 Mukhi is the softer base. 13 Mukhi is more specialised and is best added when timing has opened but attraction patterns still feel blocked.",
        "wearing_method": {
            "thread": "White or pink thread",
            "metal": "Silver",
            "mantra": "Om Namah",
            "activation_ritual": "Wear after Monday or Friday prayer with a clear intention for mature partnership rather than urgency.",
        },
        "lifestyle_tips": [
            "Work on emotional availability, not only timing.",
            "Drop rigid or fear-based partner criteria.",
            "Address repeated relational patterns honestly.",
        ],
    },
    {
        "slug": "fertility",
        "problem": "Childlessness / Fertility",
        "key_mukhis": [9],
        "intro": "This page reflects a traditional spiritual support approach to fertility challenges and the desire for healthy reproductive blessings. It is devotional guidance and not a medical replacement.",
        "mukhi_notes": {
            9: "9 Mukhi is linked with Shakti, protection, and reproductive courage in traditional remedy logic.",
        },
        "combination_suggestion": "Because 9 Mukhi is already a focused Shakti bead, many people keep it as the central remedy rather than layering many others.",
        "wearing_method": {
            "thread": "Red thread",
            "metal": "Silver",
            "mantra": "Om Hreem Hum Namah",
            "activation_ritual": "Wear after Friday or Tuesday prayer with quiet devotion rather than anxious force.",
        },
        "lifestyle_tips": [
            "Do not delay medical evaluation.",
            "Reduce stress cycles that keep the body braced.",
            "Use spiritual support to strengthen patience and hope, not denial.",
        ],
    },
    {
        "slug": "addiction",
        "problem": "Addiction",
        "key_mukhis": [1, 3],
        "intro": "Addiction is traditionally approached as a problem of lost centre, unresolved pain, and misdirected fire. Rudraksha for this area is chosen to restore dignity, release burden, and support disciplined self-return.",
        "mukhi_notes": {
            1: "1 Mukhi is used to reconnect a person with inner dignity, centre, and higher intention.",
            3: "3 Mukhi helps burn through stored guilt, frustration, and compulsive emotional heat.",
        },
        "combination_suggestion": "3 Mukhi is often the more accessible starting point, while 1 Mukhi is approached as a deeper clarity bead when the person is ready for serious discipline.",
        "wearing_method": {
            "thread": "Red thread",
            "metal": "Copper or silver",
            "mantra": "Om Hreem Namah",
            "activation_ritual": "Wear after a sober, intentional prayer and alongside a real recovery plan.",
        },
        "lifestyle_tips": [
            "Use treatment and accountability, not symbolism alone.",
            "Remove triggers where possible.",
            "Replace secrecy with support.",
        ],
    },
    {
        "slug": "insomnia",
        "problem": "Insomnia",
        "key_mukhis": [2, 5],
        "intro": "Insomnia is often described in traditional terms as a Moon imbalance mixed with overstimulation or poor grounding. Rudraksha here is chosen to support calmness, softness, and routine-based rest.",
        "mukhi_notes": {
            2: "2 Mukhi supports emotional softness and settling before sleep.",
            5: "5 Mukhi provides broad calming and daily grounding when the system feels overactive.",
        },
        "combination_suggestion": "2 Mukhi can be paired with 5 Mukhi when sleeplessness comes from both emotional agitation and general overstimulation.",
        "wearing_method": {
            "thread": "White thread",
            "metal": "Silver",
            "mantra": "Om Namah",
            "activation_ritual": "Wear after an evening wind-down prayer rather than during active stress.",
        },
        "lifestyle_tips": [
            "Protect a consistent sleep window.",
            "Reduce screens late at night.",
            "Create a calmer pre-sleep ritual.",
        ],
    },
    {
        "slug": "digestive-issues",
        "problem": "Digestive / Stomach Issues",
        "key_mukhis": [3],
        "intro": "Digestive difficulty is often treated traditionally as a fire-regulation issue: either too low, too erratic, or too aggravated. Rudraksha here is chosen to steady and purify the Martian fire principle.",
        "mukhi_notes": {
            3: "3 Mukhi is associated with digestive fire, cleaner energy release, and better use of internal heat.",
        },
        "combination_suggestion": "3 Mukhi usually remains the central bead in this category unless another issue is also dominant.",
        "wearing_method": {
            "thread": "Red thread",
            "metal": "Copper",
            "mantra": "Om Kleem Namah",
            "activation_ritual": "Wear after sunrise and pair it with calmer eating habits.",
        },
        "lifestyle_tips": [
            "Eat with less rush.",
            "Notice which foods aggravate heat or instability.",
            "Do not use spiritual support to delay medical diagnosis.",
        ],
    },
    {
        "slug": "skin-issues",
        "problem": "Skin Problems",
        "key_mukhis": [4],
        "intro": "Traditional remedy logic sometimes links skin strain with nervous overload, speech/mental imbalance, or internal irritation that needs clearer regulation. Rudraksha here is used as a steadying Mercury support.",
        "mukhi_notes": {
            4: "4 Mukhi is chosen here for cleaner regulation, nervous steadiness, and better balance of internal processing.",
        },
        "combination_suggestion": "4 Mukhi is typically kept simple and consistent rather than heavily layered.",
        "wearing_method": {
            "thread": "Green thread",
            "metal": "Silver",
            "mantra": "Om Hreem Namah",
            "activation_ritual": "Wear on Wednesday with a focus on consistency rather than expectation of instant change.",
        },
        "lifestyle_tips": [
            "Reduce inflammatory lifestyle triggers where possible.",
            "Track stress alongside physical flare-ups.",
            "Seek medical care for persistent skin conditions.",
        ],
    },
    {
        "slug": "spiritual-growth",
        "problem": "Spiritual Growth",
        "key_mukhis": [1, 21],
        "intro": "Spiritual growth in this tradition is not only mystical intensity but cleaner centre, disciplined devotion, and expansive but grounded awareness. Rudraksha here is chosen for deepening practice and alignment.",
        "mukhi_notes": {
            1: "1 Mukhi is the clarity-and-unity bead traditionally linked with higher inward focus.",
            21: "21 Mukhi represents expansive blessing, stewardship, and the mature side of spiritual abundance.",
        },
        "combination_suggestion": "For most seekers, 1 Mukhi is the more direct contemplative support. 21 Mukhi is a rarer, more mature expansion bead.",
        "wearing_method": {
            "thread": "Saffron thread",
            "metal": "Gold",
            "mantra": "Om Hreem Namah",
            "activation_ritual": "Wear after prayer, meditation, or scripture study instead of treating it as a status marker.",
        },
        "lifestyle_tips": [
            "Choose consistency over intensity.",
            "Let practice change conduct, not only mood.",
            "Stay grounded in service and ethics.",
        ],
    },
    {
        "slug": "business-success",
        "problem": "Business Success",
        "key_mukhis": [7, 8, 11],
        "intro": "Business success is traditionally approached through stamina, obstacle-clearing, and decisive action. Rudraksha in this area is chosen to help a person stay grounded under pressure while moving with courage and timing.",
        "mukhi_notes": {
            7: "7 Mukhi supports financial steadiness, discipline, and the long-haul patience needed in business.",
            8: "8 Mukhi helps remove recurring blocks, delays, and tangled openings.",
            11: "11 Mukhi supports decisive courage, negotiation strength, and the will to move.",
        },
        "combination_suggestion": "7, 8, and 11 Mukhi can form a practical business trio when the challenge includes pressure, delays, and the need for stronger execution.",
        "wearing_method": {
            "thread": "Black or red thread",
            "metal": "Silver or panchdhatu",
            "mantra": "Om Hum Namah",
            "activation_ritual": "Wear after prayer and pair it with clear planning, clean accounts, and disciplined decision-making.",
        },
        "lifestyle_tips": [
            "Separate ambition from impulsiveness.",
            "Review cash flow regularly.",
            "Act on bottlenecks instead of only hoping for luck.",
        ],
    },
]


def _build_problem_document(payload: dict) -> dict:
    primary_number = int(payload["key_mukhis"][0])
    primary = _mukhi_reference(primary_number, fit_reason=payload["mukhi_notes"][primary_number])
    supporting = [
        _mukhi_reference(number, fit_reason=payload["mukhi_notes"][number])
        for number in payload["key_mukhis"][1:]
    ]
    problem = payload["problem"]
    primary_label = _faq_bead_label(primary)
    support_names = ", ".join(_faq_bead_label(item) for item in supporting) if supporting else f"no backup beyond the {primary_label}"
    lifestyle_pair = ", ".join(payload["lifestyle_tips"][:2]).lower()
    lifestyle_one = str(payload["lifestyle_tips"][0]).lower()
    faq = _faq_from_pairs([
        (
            f"Which Rudraksha is best for {problem}?",
            _variant_text(
                payload["slug"],
                0,
                [
                    "For {problem}, start with {primary_label}; {support_names} are only the supporting beads.",
                    "{primary_label} leads this {problem} page, while {support_names} stay in the second line.",
                    "The first bead named for {problem} is {primary_label}, followed by {support_names}.",
                    "This {problem} guide centres {primary_label} and adds {support_names} only as support.",
                    "When {problem} is the concern, {primary_label} comes first and {support_names} come after.",
                ],
                problem=problem,
                primary_label=primary_label,
                support_names=support_names,
            ),
        ),
        (
            f"Can these Rudraksha beads for {problem} be worn together?",
            _variant_text(
                payload["slug"],
                1,
                [
                    "{problem}: {combination}.",
                    "The {problem} stack on this page is {combination}.",
                    "For {problem}, the combined route is {combination}.",
                    "{combination} That is the shared pattern for {problem}.",
                    "{combination} That is the allowed combination on this {problem} page.",
                ],
                problem=problem,
                combination=payload["combination_suggestion"],
            ),
        ),
        (
            f"How should Rudraksha for {problem} be worn?",
            _variant_text(
                payload["slug"],
                2,
                [
                    "{problem}: {mantra}, with {metal} on {thread}.",
                    "{metal}, {thread}; chant {mantra} for {problem}.",
                    "For {problem}, use {metal}; keep {thread}; chant {mantra}.",
                    "{problem} uses {mantra}, plus {metal} and {thread}.",
                    "When {problem} needs a bead, choose {thread} with {metal}; the chant is {mantra}.",
                ],
                problem=problem,
                metal=payload["wearing_method"]["metal"],
                thread=payload["wearing_method"]["thread"],
                mantra=payload["wearing_method"]["mantra"],
            ),
        ),
        (
            f"Will Rudraksha alone solve {problem}?",
            _variant_text(
                payload["slug"],
                3,
                [
                    "Start with {lifestyle_one}; the bead is support for {problem}.",
                    "Without {lifestyle_one}, Rudraksha alone will not resolve {problem}.",
                    "{problem} still needs {lifestyle_one} beside the bead.",
                    "For {problem}, keep {lifestyle_one} active with Rudraksha.",
                    "No bead replaces the practical work of {lifestyle_one} for {problem}.",
                ],
                problem=problem,
                lifestyle_one=lifestyle_one,
            ),
        ),
        (
            f"What should I do alongside Rudraksha for {problem}?",
            _variant_text(
                payload["slug"],
                4,
                [
                    "{lifestyle_pair} should sit beside the bead.",
                    "For {problem}, pair the bead with {lifestyle_pair}.",
                    "{problem} also needs {lifestyle_pair}.",
                    "Support this Rudraksha through {lifestyle_pair}.",
                    "{lifestyle_pair} should accompany this bead.",
                ],
                problem=problem,
                lifestyle_pair=lifestyle_pair,
            ),
        ),
    ])
    return {
        "page_type": "problem",
        "slug": payload["slug"],
        "problem": problem,
        "title": f"Rudraksha for {problem} - Which Mukhi Bead Helps & How to Use It",
        "intro": payload["intro"],
        "primary_mukhi": primary,
        "supporting_mukhis": supporting,
        "combination_suggestion": payload["combination_suggestion"],
        "wearing_method": dict(payload["wearing_method"]),
        "lifestyle_tips": list(payload["lifestyle_tips"]),
        "faq": faq,
        "meta_title": _problem_meta_title(problem, primary, supporting),
        "meta_description": f"Explore the traditional Rudraksha guidance for {problem.lower()}, including primary mukhi beads, supporting combinations, mantra, and wearing method.",
    }


PROBLEM_RUDRAKSHA_DATA = {
    item["slug"]: _build_problem_document(item)
    for item in _PROBLEM_CORE
}
PROBLEM_RUDRAKSHA_SLUGS = list(PROBLEM_RUDRAKSHA_DATA.keys())


_SIGN_CORE = [
    {
        "slug": "aries",
        "sign": "Aries",
        "ruling_planet": "Mars",
        "primary": 3,
        "secondary": 5,
        "nature": "Bold, fast, initiating, and heat-driven.",
        "typical_challenges": ["impatience", "reactive anger", "burnout from speed"],
        "intro": "Aries energy moves quickly, acts boldly, and often learns by impact. The best Rudraksha for Aries is usually chosen to strengthen healthy courage while cooling impulsive fire and protecting long-term stamina.",
        "avoid": [
            {"mukhi": 12, "reason": "12 Mukhi can intensify heat and authority themes if Aries is already overly sharp or combustible."},
        ],
    },
    {
        "slug": "taurus",
        "sign": "Taurus",
        "ruling_planet": "Venus",
        "primary": 6,
        "secondary": 2,
        "nature": "Steady, sensual, comfort-seeking, and materially grounded.",
        "typical_challenges": ["stubborn attachment", "emotional bottling", "comfort inertia"],
        "intro": "Taurus seeks stability, beauty, and dependable rhythms. The right Rudraksha for Taurus is chosen to protect self-worth and refinement while loosening over-attachment and emotional heaviness.",
        "avoid": [
            {"mukhi": 13, "reason": "13 Mukhi may feel too indulgence-amplifying if Taurus is already pulled toward excess or attachment."},
        ],
    },
    {
        "slug": "gemini",
        "sign": "Gemini",
        "ruling_planet": "Mercury",
        "primary": 4,
        "secondary": 5,
        "nature": "Curious, verbal, adaptable, and mentally quick.",
        "typical_challenges": ["scattered focus", "overthinking", "inconsistent follow-through"],
        "intro": "Gemini energy thrives on movement, language, and fresh input. Rudraksha for Gemini is traditionally chosen to improve concentration, cleaner speech, and a calmer, more directed mind.",
        "avoid": [
            {"mukhi": 8, "reason": "8 Mukhi can feel too destabilising if Gemini is already scattered and overstimulated."},
        ],
    },
    {
        "slug": "cancer",
        "sign": "Cancer",
        "ruling_planet": "Moon",
        "primary": 2,
        "secondary": 5,
        "nature": "Protective, feeling-led, memory-rich, and inwardly tidal.",
        "typical_challenges": ["mood swings", "overprotection", "holding old hurt"],
        "intro": "Cancer moves through emotion, belonging, and subtle sensitivity. Rudraksha for Cancer is traditionally chosen to bring emotional steadiness, softness without fragility, and a more secure inner tide.",
        "avoid": [
            {"mukhi": 9, "reason": "9 Mukhi can feel too intense if Cancer is already emotionally overwhelmed or highly reactive."},
        ],
    },
    {
        "slug": "leo",
        "sign": "Leo",
        "ruling_planet": "Sun",
        "primary": 1,
        "secondary": 12,
        "nature": "Radiant, expressive, proud, and dignity-driven.",
        "typical_challenges": ["ego strain", "hurt pride", "overexertion"],
        "intro": "Leo energy wants to shine with heart, purpose, and clean authority. The right Rudraksha for Leo supports leadership and vitality while helping strong solar energy stay generous rather than domineering.",
        "avoid": [
            {"mukhi": 11, "reason": "11 Mukhi may further intensify force and command if Leo already pushes too hard."},
        ],
    },
    {
        "slug": "virgo",
        "sign": "Virgo",
        "ruling_planet": "Mercury",
        "primary": 4,
        "secondary": 6,
        "nature": "Precise, analytical, service-oriented, and improvement-focused.",
        "typical_challenges": ["perfectionism", "nervous strain", "self-criticism"],
        "intro": "Virgo seeks order, usefulness, and clear systems. Rudraksha for Virgo is chosen to steady the mind, improve discrimination, and prevent analysis from turning into anxiety or depletion.",
        "avoid": [
            {"mukhi": 3, "reason": "3 Mukhi can feel too heat-driven if Virgo's stress already shows up as internal agitation."},
        ],
    },
    {
        "slug": "libra",
        "sign": "Libra",
        "ruling_planet": "Venus",
        "primary": 6,
        "secondary": 2,
        "nature": "Relational, balanced, aesthetically tuned, and harmony-seeking.",
        "typical_challenges": ["people-pleasing", "indecision", "avoidance of necessary conflict"],
        "intro": "Libra looks for fairness, beauty, and relational ease. Rudraksha for Libra is chosen to mature attraction, strengthen boundaries, and preserve harmony without loss of self-respect.",
        "avoid": [
            {"mukhi": 13, "reason": "13 Mukhi can amplify charm and desire too much if Libra is already ungrounded in relationship choices."},
        ],
    },
    {
        "slug": "scorpio",
        "sign": "Scorpio",
        "ruling_planet": "Mars",
        "primary": 3,
        "secondary": 9,
        "nature": "Intense, private, transformative, and emotionally deep.",
        "typical_challenges": ["control", "resentment", "all-or-nothing reactions"],
        "intro": "Scorpio carries depth, endurance, and a powerful inner furnace. Rudraksha for Scorpio is chosen to channel intensity into courage, protection, and cleaner transformation rather than secrecy or implosion.",
        "avoid": [
            {"mukhi": 8, "reason": "8 Mukhi can feel too destabilising if Scorpio is already moving through intense inner upheaval."},
        ],
    },
    {
        "slug": "sagittarius",
        "sign": "Sagittarius",
        "ruling_planet": "Jupiter",
        "primary": 5,
        "secondary": 12,
        "nature": "Expansive, idealistic, forward-looking, and meaning-driven.",
        "typical_challenges": ["restlessness", "preaching without grounding", "overextension"],
        "intro": "Sagittarius seeks truth, freedom, and a horizon worth moving toward. Rudraksha for Sagittarius is traditionally chosen to support wisdom, ethical action, and clean vitality without scattering conviction.",
        "avoid": [
            {"mukhi": 13, "reason": "13 Mukhi can pull Sagittarius toward glamour or excess when grounded wisdom is the real need."},
        ],
    },
    {
        "slug": "capricorn",
        "sign": "Capricorn",
        "ruling_planet": "Saturn",
        "primary": 7,
        "secondary": 14,
        "nature": "Structured, serious, strategic, and responsibility-led.",
        "typical_challenges": ["heaviness", "work overload", "fear of failure"],
        "intro": "Capricorn is built for structure, responsibility, and slow-earned results. Rudraksha for Capricorn is chosen to support endurance, karmic steadiness, and protection from the emotional weight of pressure.",
        "avoid": [
            {"mukhi": 1, "reason": "1 Mukhi may feel too solar and pressure-building if Capricorn is already carrying excessive performance strain."},
        ],
    },
    {
        "slug": "aquarius",
        "sign": "Aquarius",
        "ruling_planet": "Saturn",
        "primary": 7,
        "secondary": 8,
        "nature": "Independent, idea-led, unconventional, and socially wide-angled.",
        "typical_challenges": ["detachment", "erratic focus", "living too much in the head"],
        "intro": "Aquarius brings vision, difference, and a willingness to move outside familiar lanes. Rudraksha for Aquarius is chosen to anchor Saturn's discipline while giving Rahu-like disruptions a steadier channel.",
        "avoid": [
            {"mukhi": 9, "reason": "9 Mukhi can feel too fiery if Aquarius is already restless, detached, or difficult to ground."},
        ],
    },
    {
        "slug": "pisces",
        "sign": "Pisces",
        "ruling_planet": "Jupiter",
        "primary": 5,
        "secondary": 2,
        "nature": "Intuitive, porous, imaginative, and spiritually receptive.",
        "typical_challenges": ["escapism", "boundary confusion", "emotional flooding"],
        "intro": "Pisces is guided by feeling, faith, and subtle inner currents. Rudraksha for Pisces is chosen to strengthen spiritual grounding, emotional steadiness, and healthy boundaries around compassion.",
        "avoid": [
            {"mukhi": 21, "reason": "21 Mukhi may feel too expansive if Pisces is already diffuse, unbounded, or spiritually ungrounded."},
        ],
    },
]


def _build_sign_document(payload: dict) -> dict:
    sign = payload["sign"]
    primary = _mukhi_reference(
        payload["primary"],
        fit_reason=f"{_mukhi_reference(payload['primary'])['name']} follows the ruling-planet logic for {sign} and supports the sign's core energy in a cleaner, steadier way.",
    )
    secondary = _mukhi_reference(
        payload["secondary"],
        fit_reason=f"{_mukhi_reference(payload['secondary'])['name']} is chosen for the shadow side of {sign}: {', '.join(payload['typical_challenges'][:2])}.",
    )
    primary_instructions = primary["wearing_instructions"]
    avoid_mukhis = [
        {
            **_mukhi_reference(item["mukhi"]),
            "fit_reason": item["reason"],
        }
        for item in payload["avoid"]
    ]
    primary_label = _faq_bead_label(primary)
    secondary_label = _faq_bead_label(secondary)
    challenge_pair = ", ".join(payload["typical_challenges"][:2])
    ruling_planet = payload["ruling_planet"]
    avoid_name = _faq_bead_label(avoid_mukhis[0])
    avoid_reason = avoid_mukhis[0]["fit_reason"].lower()
    avoid_reason_parts = avoid_reason.split(" ", 2)
    if len(avoid_reason_parts) == 3 and avoid_reason_parts[1] == "mukhi":
        avoid_reason_brief = avoid_reason_parts[2]
    else:
        avoid_reason_brief = avoid_reason
    faq = _faq_from_pairs([
        (
            f"Which Rudraksha is best for {sign}?",
            _variant_text(
                payload["slug"],
                0,
                [
                    "{sign}: {primary_label} first; for {sign}, {secondary_label} helps {challenge_pair}.",
                    "{primary_label} leads {sign}; for {sign}, {secondary_label} answers {challenge_pair}.",
                    "Start {sign} with {primary_label}; add {secondary_label} if {challenge_pair} rises.",
                    "For {sign}, {challenge_pair} keeps support reserved.",
                    "{primary_label} stays first for {sign}, even when {challenge_pair} suggests backup support.",
                ],
                sign=sign,
                primary_label=primary_label,
                secondary_label=secondary_label,
                challenge_pair=challenge_pair,
            ),
        ),
        (
            f"Why does {sign} use this Rudraksha?",
            _variant_text(
                payload["slug"],
                1,
                [
                    "{ruling_planet} rules {sign}; {challenge_pair} explains {primary_label}.",
                    "{sign} meets this remedy through {ruling_planet} and {challenge_pair}.",
                    "{challenge_pair} turns the {ruling_planet}-{sign} match toward this remedy.",
                    "{ruling_planet} gives the base; {challenge_pair} gives the correction for {sign}.",
                    "{primary_label} fits {sign} because {ruling_planet} plus {challenge_pair} line up.",
                ],
                sign=sign,
                ruling_planet=ruling_planet,
                primary_label=primary_label,
                challenge_pair=challenge_pair,
            ),
        ),
        (
            f"Can {sign} wear more than one Rudraksha?",
            _variant_text(
                payload["slug"],
                2,
                [
                    "For {challenge_pair}, {sign} may use both {primary_label} and {secondary_label}.",
                    "For {sign}, split {challenge_pair}: give one side to {primary_label} and the other to {secondary_label}.",
                    "Use two beads for {sign} only when {challenge_pair} outgrows one layer in {sign}.",
                    "{primary_label} plus {secondary_label} works for {sign} when one layer is not enough for {challenge_pair}.",
                    "{challenge_pair} may justify both {primary_label} and {secondary_label} for {sign}.",
                ],
                sign=sign,
                primary_label=primary_label,
                secondary_label=secondary_label,
                challenge_pair=challenge_pair,
            ),
        ),
        (
            f"Which Rudraksha should {sign} approach carefully?",
            _variant_text(
                payload["slug"],
                3,
                [
                    "For {sign}, caution starts here: {avoid_reason}.",
                    "{sign} caution note: {avoid_reason_brief}.",
                    "{sign} should question {avoid_name}: {avoid_reason}.",
                    "{avoid_reason} That is why {sign} treats {avoid_name} carefully.",
                    "For {sign}, caution starts here: {avoid_reason}.",
                ],
                sign=sign,
                avoid_name=avoid_name,
                avoid_reason=avoid_reason,
                avoid_reason_brief=avoid_reason_brief,
            ),
        ),
    ])
    return {
        "page_type": "sign",
        "slug": payload["slug"],
        "sign": sign,
        "title": f"Best Rudraksha for {sign} - Mukhi Beads for {sign} Energy",
        "intro": payload["intro"],
        "ruling_planet": payload["ruling_planet"],
        "nature": payload["nature"],
        "typical_challenges": list(payload["typical_challenges"]),
        "primary_mukhi": primary,
        "secondary_mukhi": secondary,
        "avoid_mukhis": avoid_mukhis,
        "wearing_guidance": {
            "best_day": primary_instructions["day"],
            "best_metal": primary_instructions["metal"],
            "activation_mantra": primary_instructions["mantra"],
        },
        "faq": faq,
        "meta_title": _sign_meta_title(sign, primary, payload),
        "meta_description": _SIGN_META_DESCS.get(payload["slug"], f"Find the best Rudraksha for {sign}, including the ruling-planet mukhi and practical wearing guidance."),
    }


SIGN_RUDRAKSHA_DATA = {
    item["slug"]: _build_sign_document(item)
    for item in _SIGN_CORE
}
SIGN_RUDRAKSHA_SLUGS = list(SIGN_RUDRAKSHA_DATA.keys())


def get_planet_rudraksha_document(slug: str) -> dict | None:
    payload = PLANET_RUDRAKSHA_DATA.get(str(slug))
    return deepcopy(payload) if payload else None


def get_problem_rudraksha_document(slug: str) -> dict | None:
    payload = PROBLEM_RUDRAKSHA_DATA.get(str(slug))
    return deepcopy(payload) if payload else None


def get_sign_rudraksha_document(slug: str) -> dict | None:
    payload = SIGN_RUDRAKSHA_DATA.get(str(slug))
    return deepcopy(payload) if payload else None


def get_planet_rudraksha_documents() -> list[dict]:
    return [deepcopy(PLANET_RUDRAKSHA_DATA[slug]) for slug in PLANET_RUDRAKSHA_SLUGS]


def get_problem_rudraksha_documents() -> list[dict]:
    return [deepcopy(PROBLEM_RUDRAKSHA_DATA[slug]) for slug in PROBLEM_RUDRAKSHA_SLUGS]


def get_sign_rudraksha_documents() -> list[dict]:
    return [deepcopy(SIGN_RUDRAKSHA_DATA[slug]) for slug in SIGN_RUDRAKSHA_SLUGS]
