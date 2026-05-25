from __future__ import annotations

from typing import Any


SIGNS: list[dict[str, Any]] = [
    {"slug": "aries", "name": "Aries", "element": "Fire", "modality": "Cardinal", "ruler": "Mars"},
    {"slug": "taurus", "name": "Taurus", "element": "Earth", "modality": "Fixed", "ruler": "Venus"},
    {"slug": "gemini", "name": "Gemini", "element": "Air", "modality": "Mutable", "ruler": "Mercury"},
    {"slug": "cancer", "name": "Cancer", "element": "Water", "modality": "Cardinal", "ruler": "Moon"},
    {"slug": "leo", "name": "Leo", "element": "Fire", "modality": "Fixed", "ruler": "Sun"},
    {"slug": "virgo", "name": "Virgo", "element": "Earth", "modality": "Mutable", "ruler": "Mercury"},
    {"slug": "libra", "name": "Libra", "element": "Air", "modality": "Cardinal", "ruler": "Venus"},
    {"slug": "scorpio", "name": "Scorpio", "element": "Water", "modality": "Fixed", "ruler": "Mars"},
    {"slug": "sagittarius", "name": "Sagittarius", "element": "Fire", "modality": "Mutable", "ruler": "Jupiter"},
    {"slug": "capricorn", "name": "Capricorn", "element": "Earth", "modality": "Cardinal", "ruler": "Saturn"},
    {"slug": "aquarius", "name": "Aquarius", "element": "Air", "modality": "Fixed", "ruler": "Saturn"},
    {"slug": "pisces", "name": "Pisces", "element": "Water", "modality": "Mutable", "ruler": "Jupiter"},
]

SIGN_SLUGS = [item["slug"] for item in SIGNS]
SIGN_NAME_MAP = {item["slug"]: item["name"] for item in SIGNS}
SIGN_META = {item["slug"]: item for item in SIGNS}

PLANETS: list[dict[str, Any]] = [
    {
        "slug": "sun",
        "name": "Sun",
        "theme": "identity and visibility",
        "gift": "confidence and leadership",
        "watch": "ego clashes and burnout",
        "remedy": "sunrise prayers, Surya mantra, and clean discipline",
    },
    {
        "slug": "moon",
        "name": "Moon",
        "theme": "emotions and belonging",
        "gift": "intuition and care",
        "watch": "mood swings and over-absorption",
        "remedy": "rest, lunar fasting rhythm, and gentle grounding rituals",
    },
    {
        "slug": "mars",
        "name": "Mars",
        "theme": "action and courage",
        "gift": "drive and decisive movement",
        "watch": "impatience, conflict, and heat",
        "remedy": "Hanuman practice, structured movement, and anger hygiene",
    },
    {
        "slug": "mercury",
        "name": "Mercury",
        "theme": "thinking and communication",
        "gift": "adaptability and clever timing",
        "watch": "overthinking, mixed signals, and scattered effort",
        "remedy": "Budha mantra, journaling, and cleaner information boundaries",
    },
    {
        "slug": "jupiter",
        "name": "Jupiter",
        "theme": "growth and wisdom",
        "gift": "faith and expansion",
        "watch": "over-promising, excess, and blind optimism",
        "remedy": "guru seva, Thursday simplicity, and dharmic study",
    },
    {
        "slug": "venus",
        "name": "Venus",
        "theme": "love and attraction",
        "gift": "harmony and refinement",
        "watch": "indulgence, avoidance, and blurred values",
        "remedy": "Friday beauty rituals, gratitude, and Venus mantra practice",
    },
    {
        "slug": "saturn",
        "name": "Saturn",
        "theme": "responsibility and structure",
        "gift": "endurance and realism",
        "watch": "delay, heaviness, and fear-based thinking",
        "remedy": "service, Saturn mantra, and disciplined pacing",
    },
    {
        "slug": "rahu",
        "name": "Rahu",
        "theme": "ambition and disruption",
        "gift": "innovation and appetite for change",
        "watch": "obsession, confusion, and shortcuts",
        "remedy": "clarity rituals, breath regulation, and avoiding impulsive leaps",
    },
    {
        "slug": "ketu",
        "name": "Ketu",
        "theme": "detachment and inner release",
        "gift": "insight and spiritual refinement",
        "watch": "disconnection, drift, and sudden withdrawal",
        "remedy": "silence, spiritual study, and clean energetic boundaries",
    },
]

PLANET_SLUGS = [item["slug"] for item in PLANETS]
PLANET_NAME_MAP = {item["slug"]: item["name"] for item in PLANETS}
PLANET_META = {item["slug"]: item for item in PLANETS}

CHART_POINTS: list[dict[str, str]] = [
    {"slug": "sun", "name": "Sun", "lens": "identity, pride, and purpose"},
    {"slug": "moon", "name": "Moon", "lens": "emotions, memory, and instinct"},
    {"slug": "rising", "name": "Rising", "lens": "outer style, approach, and first impact"},
]

CHART_POINT_META = {item["slug"]: item for item in CHART_POINTS}

HOUSES: list[dict[str, Any]] = [
    {"slug": "1st-house", "number": 1, "label": "1st House", "topic": "identity, body, and self-direction"},
    {"slug": "2nd-house", "number": 2, "label": "2nd House", "topic": "income, family, and voice"},
    {"slug": "3rd-house", "number": 3, "label": "3rd House", "topic": "communication, courage, and siblings"},
    {"slug": "4th-house", "number": 4, "label": "4th House", "topic": "home, roots, and emotional security"},
    {"slug": "5th-house", "number": 5, "label": "5th House", "topic": "creativity, romance, and self-expression"},
    {"slug": "6th-house", "number": 6, "label": "6th House", "topic": "work, health, and pressure management"},
    {"slug": "7th-house", "number": 7, "label": "7th House", "topic": "partnership, contracts, and one-to-one dynamics"},
    {"slug": "8th-house", "number": 8, "label": "8th House", "topic": "intimacy, power, and transformation"},
    {"slug": "9th-house", "number": 9, "label": "9th House", "topic": "belief, teachers, and higher meaning"},
    {"slug": "10th-house", "number": 10, "label": "10th House", "topic": "career, status, and public life"},
    {"slug": "11th-house", "number": 11, "label": "11th House", "topic": "community, gains, and future goals"},
    {"slug": "12th-house", "number": 12, "label": "12th House", "topic": "retreat, release, and the unseen inner life"},
]

HOUSE_META = {item["slug"]: item for item in HOUSES}

REGIONS: list[dict[str, str]] = [
    {"slug": "andhra-pradesh", "name": "Andhra Pradesh", "zone": "south", "location_slug": "visakhapatnam-india", "food": "pulihora and laddus", "marker": "temple processions and decorated entrances"},
    {"slug": "arunachal-pradesh", "name": "Arunachal Pradesh", "zone": "northeast", "location_slug": "kolkata-india", "food": "community sweets and festive rice dishes", "marker": "community halls and family gatherings"},
    {"slug": "assam", "name": "Assam", "zone": "east", "location_slug": "kolkata-india", "food": "pitha, payas, and festive rice offerings", "marker": "music, prayer, and neighbourhood visits"},
    {"slug": "bihar", "name": "Bihar", "zone": "north", "location_slug": "patna-india", "food": "thekua, kheer, and seasonal savouries", "marker": "ghat visits and family puja routines"},
    {"slug": "chhattisgarh", "name": "Chhattisgarh", "zone": "central", "location_slug": "nagpur-india", "food": "rice sweets and home-style prasad", "marker": "community puja and local fairs"},
    {"slug": "goa", "name": "Goa", "zone": "west", "location_slug": "mumbai-india", "food": "coconut sweets and festive savouries", "marker": "home altars and neighbourhood celebration routes"},
    {"slug": "gujarat", "name": "Gujarat", "zone": "west", "location_slug": "ahmedabad-india", "food": "fafda, jalebi, and festive thalis", "marker": "garba grounds and bright rangoli work"},
    {"slug": "haryana", "name": "Haryana", "zone": "north", "location_slug": "new-delhi-india", "food": "halwa, puri, and farm-style festive meals", "marker": "family courtyards and temple offerings"},
    {"slug": "himachal-pradesh", "name": "Himachal Pradesh", "zone": "north", "location_slug": "new-delhi-india", "food": "sweet rice, prasad, and mountain-style meals", "marker": "village temples and hillside processions"},
    {"slug": "jharkhand", "name": "Jharkhand", "zone": "east", "location_slug": "kolkata-india", "food": "seasonal sweets and simple ceremonial meals", "marker": "community grounds and family prayer circles"},
    {"slug": "karnataka", "name": "Karnataka", "zone": "south", "location_slug": "bengaluru-india", "food": "kosambari, payasa, and temple-style prasada", "marker": "flower decorations and early-morning puja"},
    {"slug": "kerala", "name": "Kerala", "zone": "south", "location_slug": "chennai-india", "food": "payasam, banana chips, and elaborate festive spreads", "marker": "floral designs and household lamp lighting"},
    {"slug": "madhya-pradesh", "name": "Madhya Pradesh", "zone": "central", "location_slug": "indore-india", "food": "poha-style snacks, sweets, and prasad", "marker": "mandir visits and old-city processions"},
    {"slug": "maharashtra", "name": "Maharashtra", "zone": "west", "location_slug": "mumbai-india", "food": "modak, puran poli, and festive snacks", "marker": "society pandals and family aarti gatherings"},
    {"slug": "manipur", "name": "Manipur", "zone": "northeast", "location_slug": "kolkata-india", "food": "community feasts and seasonal sweets", "marker": "cultural performance and temple participation"},
    {"slug": "meghalaya", "name": "Meghalaya", "zone": "northeast", "location_slug": "kolkata-india", "food": "festive rice dishes and local sweets", "marker": "church halls, homes, and community spaces"},
    {"slug": "mizoram", "name": "Mizoram", "zone": "northeast", "location_slug": "kolkata-india", "food": "shared festive meals and sweet offerings", "marker": "community halls and neighbourhood visits"},
    {"slug": "nagaland", "name": "Nagaland", "zone": "northeast", "location_slug": "kolkata-india", "food": "community meals and celebratory desserts", "marker": "collective singing and family hosting"},
    {"slug": "odisha", "name": "Odisha", "zone": "east", "location_slug": "kolkata-india", "food": "khaja, pitha, and temple mahaprasad", "marker": "alpona art and neighbourhood mandaps"},
    {"slug": "punjab", "name": "Punjab", "zone": "north", "location_slug": "new-delhi-india", "food": "kada prasad, festive rotis, and sweets", "marker": "gurdwara seva and community langar"},
    {"slug": "rajasthan", "name": "Rajasthan", "zone": "west", "location_slug": "jaipur-india", "food": "ghevar, dal-baati spreads, and festive mithai", "marker": "courtyard lamps and royal-colour decoration"},
    {"slug": "sikkim", "name": "Sikkim", "zone": "northeast", "location_slug": "kolkata-india", "food": "shared sweets and festive rice dishes", "marker": "community prayer and hillside celebrations"},
    {"slug": "tamil-nadu", "name": "Tamil Nadu", "zone": "south", "location_slug": "chennai-india", "food": "sweet pongal, sundal, and temple prasadam", "marker": "kolam art, brass lamps, and dawn rituals"},
    {"slug": "telangana", "name": "Telangana", "zone": "south", "location_slug": "hyderabad-india", "food": "paramannam, laddus, and festive savouries", "marker": "Bonalu-style community devotion and floral decor"},
    {"slug": "tripura", "name": "Tripura", "zone": "east", "location_slug": "kolkata-india", "food": "festive rice offerings and sweets", "marker": "family courtyards and community pandals"},
    {"slug": "uttar-pradesh", "name": "Uttar Pradesh", "zone": "north", "location_slug": "lucknow-india", "food": "peda, kachori, and traditional prasad", "marker": "ghat rituals and temple crowds"},
    {"slug": "uttarakhand", "name": "Uttarakhand", "zone": "north", "location_slug": "new-delhi-india", "food": "singori, halwa, and temple offerings", "marker": "hill temples and family vrat observance"},
    {"slug": "west-bengal", "name": "West Bengal", "zone": "east", "location_slug": "kolkata-india", "food": "sandesh, khichuri bhog, and festive sweets", "marker": "pandals, dhaak rhythms, and artistic decorations"},
    {"slug": "nri-london", "name": "NRI London", "zone": "diaspora", "location_slug": "london-uk", "food": "potluck sweets and temple prasada", "marker": "weekend community events and cultural centres"},
    {"slug": "nri-new-york", "name": "NRI New York", "zone": "diaspora", "location_slug": "new-york-usa", "food": "shared festive meals and mandir prasad", "marker": "temple halls, family Zooms, and community gatherings"},
]

REGION_META = {item["slug"]: item for item in REGIONS}
REGION_SLUGS = [item["slug"] for item in REGIONS]

FESTIVALS: list[dict[str, str]] = [
    {"slug": "diwali", "name": "Diwali", "source": "engine", "season": "light, prosperity, and renewal"},
    {"slug": "holi", "name": "Holi", "source": "engine", "season": "colour, play, and spring release"},
    {"slug": "navratri", "name": "Navratri", "source": "seeded", "season": "devotion, dance, and Shakti worship"},
    {"slug": "durga-puja", "name": "Durga Puja", "source": "seeded", "season": "goddess celebration, artistry, and community worship"},
    {"slug": "ganesh-chaturthi", "name": "Ganesh Chaturthi", "source": "seeded", "season": "auspicious beginnings and Ganapati devotion"},
    {"slug": "janmashtami", "name": "Janmashtami", "source": "engine", "season": "bhakti, midnight worship, and Krishna leela"},
    {"slug": "maha-shivaratri", "name": "Maha Shivaratri", "source": "engine", "season": "night vigil, mantra, and inward stillness"},
    {"slug": "makar-sankranti", "name": "Makar Sankranti", "source": "seeded", "season": "harvest, sunlight, and transition"},
    {"slug": "pongal", "name": "Pongal", "source": "seeded", "season": "harvest gratitude and household abundance"},
    {"slug": "onam", "name": "Onam", "source": "seeded", "season": "harvest joy, floral beauty, and family reunion"},
    {"slug": "baisakhi", "name": "Baisakhi", "source": "seeded", "season": "harvest thanksgiving and collective celebration"},
    {"slug": "eid-ul-fitr", "name": "Eid-ul-Fitr", "source": "seeded", "season": "gratitude, prayer, and family feasting"},
    {"slug": "christmas", "name": "Christmas", "source": "seeded", "season": "joy, prayer, and generous gathering"},
    {"slug": "gurupurab", "name": "Gurupurab", "source": "seeded", "season": "guru remembrance, kirtan, and seva"},
    {"slug": "ram-navami", "name": "Ram Navami", "source": "engine", "season": "dharma, maryada, and devotional celebration"},
    {"slug": "hanuman-jayanti", "name": "Hanuman Jayanti", "source": "seeded", "season": "strength, devotion, and protection"},
]

FESTIVAL_META = {item["slug"]: item for item in FESTIVALS}
FESTIVAL_SLUGS = [item["slug"] for item in FESTIVALS]

ENGINE_FESTIVAL_SLUGS = {
    "diwali",
    "holi",
    "janmashtami",
    "maha-shivaratri",
    "ram-navami",
}

ENGINE_FESTIVAL_ALIASES = {
    "ram-navami": "rama-navami",
}

SEEDED_FESTIVAL_DATES: dict[str, dict[str, str]] = {
    "navratri": {
        "2026": "2026-10-12",
        "2027": "2027-10-02",
        "2028": "2028-09-21",
    },
    "durga-puja": {
        "2026": "2026-10-20",
        "2027": "2027-10-11",
        "2028": "2028-09-30",
    },
    "ganesh-chaturthi": {
        "2026": "2026-09-12",
        "2027": "2027-09-01",
        "2028": "2028-08-21",
    },
    "makar-sankranti": {
        "2026": "2026-01-14",
        "2027": "2027-01-14",
        "2028": "2028-01-14",
    },
    "pongal": {
        "2026": "2026-01-15",
        "2027": "2027-01-15",
        "2028": "2028-01-15",
    },
    "onam": {
        "2026": "2026-08-28",
        "2027": "2027-09-16",
        "2028": "2028-09-04",
    },
    "baisakhi": {
        "2026": "2026-04-14",
        "2027": "2027-04-14",
        "2028": "2028-04-13",
    },
    "eid-ul-fitr": {
        "2026": "2026-03-20",
        "2027": "2027-03-10",
        "2028": "2028-02-27",
    },
    "christmas": {
        "2026": "2026-12-25",
        "2027": "2027-12-25",
        "2028": "2028-12-25",
    },
    "gurupurab": {
        "2026": "2026-11-24",
        "2027": "2027-11-13",
        "2028": "2028-11-01",
    },
    "hanuman-jayanti": {
        "2026": "2026-04-01",
        "2027": "2027-04-20",
        "2028": "2028-04-09",
    },
}


def ordinal(number: int) -> str:
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{suffix}"
