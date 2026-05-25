from __future__ import annotations

from copy import deepcopy


SITE_NAME = "EverydayHoroscope"

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
            "how_to_wear": "Wear after morning prayer as a bracelet or pendant.",
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
            "how_to_wear": "Wear after Durga mantra or quiet prayer for strength and protection.",
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
            "how_to_wear": "Wear after a focused prayer when you need steadiness in speech and action.",
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
            "how_to_wear": "Wear after reciting a Mahamrityunjaya prayer or sitting quietly in devotion.",
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
            "how_to_wear": "Wear prayerfully when seeking responsible growth rather than reckless gain.",
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


def _faq_items(name: str, overview: str, benefits: list[str], instructions: dict[str, str]) -> list[dict[str, str]]:
    benefit_text = ", ".join(benefits[:3])
    return [
        {
            "q": f"Who should wear {name}?",
            "a": f"{name} is generally chosen by people seeking {benefit_text}, along with the life themes described in its traditional profile.",
        },
        {
            "q": f"What are the benefits of {name}?",
            "a": f"{overview} In practice, people usually look to it for support around {', '.join(benefits[:4])}.",
        },
        {
            "q": f"How do I activate {name}?",
            "a": f"Cleanse the bead, sit quietly, chant {instructions['mantra']}, and wear it with a clear intention on {instructions['day']}.",
        },
        {
            "q": f"Can anyone wear {name}?",
            "a": "Most people approach Rudraksha with devotion and simplicity, but strong or very rare beads are often worn after personal guidance.",
        },
        {
            "q": f"How should {name} be worn?",
            "a": f"It is commonly worn using {instructions['metal']} and is traditionally {instructions['how_to_wear'].lower()}",
        },
    ]


def _build_document(payload: dict) -> dict:
    mukhi = int(payload["mukhi"])
    title = f"{mukhi} Mukhi Rudraksha"
    slug = f"{mukhi}-mukhi"
    meta_title = f"{mukhi} Mukhi Rudraksha - Benefits, Mantra & Who Should Wear | {SITE_NAME}"
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
        "faq": _faq_items(title, payload["overview"], list(payload["benefits"]), dict(payload["wearing_instructions"])),
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
