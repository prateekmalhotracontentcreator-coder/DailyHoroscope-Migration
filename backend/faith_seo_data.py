from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from zoneinfo import ZoneInfo

from faith_bible_data import (
    get_bible_hub_payload as get_live_bible_hub_payload,
    get_bible_page_count,
    get_bible_sitemap_urls,
)
from faith_gita_data import (
    get_gita_hub_payload as get_live_gita_hub_payload,
    get_gita_page_count,
    get_gita_sitemap_urls,
)
from lumina_prompt_service import DAILY_SCRIPTURES

SITE_URL = "https://www.everydayhoroscope.in"
INDIA_TZ = ZoneInfo("Asia/Kolkata")
DEFAULT_PANCHANG_CITY = "new-delhi-india"
FAITH_PATHWAY_SLUGS = [
    "anxiety-reset",
    "career-reset",
    "relationship-healing",
    "grief-and-comfort",
    "fresh-start",
    "mercury-retrograde-faith",
    "financial-rebuild",
    "healing-and-illness",
    "parenting-under-pressure",
    "wisdom-at-the-crossroads",
]

SIGNS = [
    {
        "slug": "aries",
        "name": "Aries",
        "element": "Fire",
        "modality": "Cardinal",
        "ruler": "Mars",
        "seasonal_focus": "courage without emotional overreaction",
        "growth_edge": "act from conviction instead of pressure",
        "daily_practice": "Begin the day with a spoken intention before you reach for urgency.",
    },
    {
        "slug": "taurus",
        "name": "Taurus",
        "element": "Earth",
        "modality": "Fixed",
        "ruler": "Venus",
        "seasonal_focus": "steady devotion and patient rebuilding",
        "growth_edge": "release comfort that has become stagnation",
        "daily_practice": "Give ten uninterrupted minutes to prayer, chanting, or breath before the world enters your nervous system.",
    },
    {
        "slug": "gemini",
        "name": "Gemini",
        "element": "Air",
        "modality": "Mutable",
        "ruler": "Mercury",
        "seasonal_focus": "clear speech and disciplined thought",
        "growth_edge": "stop scattering attention across too many voices",
        "daily_practice": "Write one grounding sentence you will return to whenever the mind starts splitting into too many directions.",
    },
    {
        "slug": "cancer",
        "name": "Cancer",
        "element": "Water",
        "modality": "Cardinal",
        "ruler": "Moon",
        "seasonal_focus": "emotional shelter and spiritual nourishment",
        "growth_edge": "care without disappearing into everyone else's weather",
        "daily_practice": "Create one protective ritual around your home, altar, or evening wind-down.",
    },
    {
        "slug": "leo",
        "name": "Leo",
        "element": "Fire",
        "modality": "Fixed",
        "ruler": "Sun",
        "seasonal_focus": "purpose, dignity, and heart-led leadership",
        "growth_edge": "lead without making every challenge about pride",
        "daily_practice": "Offer one act of visible generosity that strengthens someone else instead of feeding performance.",
    },
    {
        "slug": "virgo",
        "name": "Virgo",
        "element": "Earth",
        "modality": "Mutable",
        "ruler": "Mercury",
        "seasonal_focus": "clean habits and practical service",
        "growth_edge": "exchange perfectionism for faithful completion",
        "daily_practice": "Choose one neglected task and finish it with devotion instead of criticism.",
    },
    {
        "slug": "libra",
        "name": "Libra",
        "element": "Air",
        "modality": "Cardinal",
        "ruler": "Venus",
        "seasonal_focus": "relational balance and wise peacemaking",
        "growth_edge": "tell the truth before harmony becomes avoidance",
        "daily_practice": "Name one conversation that needs grace and honesty at the same time.",
    },
    {
        "slug": "scorpio",
        "name": "Scorpio",
        "element": "Water",
        "modality": "Fixed",
        "ruler": "Mars",
        "seasonal_focus": "deep release, truth, and sacred restraint",
        "growth_edge": "transform intensity into devotion instead of control",
        "daily_practice": "Journal one fear honestly, then choose one grounded action that reduces secrecy around it.",
    },
    {
        "slug": "sagittarius",
        "name": "Sagittarius",
        "element": "Fire",
        "modality": "Mutable",
        "ruler": "Jupiter",
        "seasonal_focus": "meaning, study, and long-view faith",
        "growth_edge": "anchor vision in discipline, not just inspiration",
        "daily_practice": "Study one short passage slowly and carry its question with you all day.",
    },
    {
        "slug": "capricorn",
        "name": "Capricorn",
        "element": "Earth",
        "modality": "Cardinal",
        "ruler": "Saturn",
        "seasonal_focus": "endurance, responsibility, and inner authority",
        "growth_edge": "stop equating worth with relentless output",
        "daily_practice": "Set a boundary that protects your energy for what is truly essential.",
    },
    {
        "slug": "aquarius",
        "name": "Aquarius",
        "element": "Air",
        "modality": "Fixed",
        "ruler": "Saturn",
        "seasonal_focus": "clarity, conviction, and community purpose",
        "growth_edge": "turn ideals into one lived contribution",
        "daily_practice": "Choose one service-oriented act that puts your values into visible motion.",
    },
    {
        "slug": "pisces",
        "name": "Pisces",
        "element": "Water",
        "modality": "Mutable",
        "ruler": "Jupiter",
        "seasonal_focus": "surrender, imagination, and spiritual trust",
        "growth_edge": "stay porous to grace without drifting from structure",
        "daily_practice": "Pair devotion with a simple timetable so inspiration has a container.",
    },
]

SIGN_INDEX = {item["slug"]: item for item in SIGNS}

MONTHS = [
    {"slug": "january", "name": "January", "seasonal_note": "clean starts and sober priorities", "month_energy": "a reset month that asks for honest ordering"},
    {"slug": "february", "name": "February", "seasonal_note": "heart work and relational honesty", "month_energy": "a relational month that exposes what still needs softening"},
    {"slug": "march", "name": "March", "seasonal_note": "threshold energy and movement", "month_energy": "a turning month that asks for brave but thoughtful action"},
    {"slug": "april", "name": "April", "seasonal_note": "new fire and visible motion", "month_energy": "an activating month that rewards clean initiative"},
    {"slug": "may", "name": "May", "seasonal_note": "stability and nourishment", "month_energy": "a grounding month that matures effort through consistency"},
    {"slug": "june", "name": "June", "seasonal_note": "conversation and adaptability", "month_energy": "a fast-moving month that tests mental flexibility"},
    {"slug": "july", "name": "July", "seasonal_note": "home, memory, and emotional weather", "month_energy": "a feeling-rich month that calls for gentler boundaries"},
    {"slug": "august", "name": "August", "seasonal_note": "visibility and courage", "month_energy": "a bright month that asks what leadership looks like with humility"},
    {"slug": "september", "name": "September", "seasonal_note": "refinement and discernment", "month_energy": "an editing month that sharpens habits and standards"},
    {"slug": "october", "name": "October", "seasonal_note": "equilibrium and recalibration", "month_energy": "a balancing month that reveals what must be renegotiated"},
    {"slug": "november", "name": "November", "seasonal_note": "depth, endings, and inward work", "month_energy": "an intense month that rewards honesty over performance"},
    {"slug": "december", "name": "December", "seasonal_note": "meaning, gratitude, and long-view reflection", "month_energy": "a reflective month that helps faith and wisdom mature together"},
]

MONTH_INDEX = {item["slug"]: item for item in MONTHS}

TRANSIT_FAMILIES = [
    {
        "planet_slug": "sun",
        "planet_name": "Sun",
        "core": "identity, leadership, confidence, and visible responsibility",
        "watch_for": "ego strain, approval hunger, and pride-driven timing",
        "practice": "Practice offering service freely.",
    },
    {
        "planet_slug": "mercury",
        "planet_name": "Mercury",
        "core": "speech, thought, planning, learning, and timing decisions",
        "watch_for": "restless thinking, mixed messages, and rushed conclusions",
        "practice": "Practice deliberate, truthful speech.",
    },
    {
        "planet_slug": "venus",
        "planet_name": "Venus",
        "core": "relationship repair, beauty, receptivity, and value alignment",
        "watch_for": "avoidance, indulgence, and calling comfort the same thing as peace",
        "practice": "Practice genuine, restorative gestures.",
    },
    {
        "planet_slug": "mars",
        "planet_name": "Mars",
        "core": "action, courage, conflict, and disciplined use of force",
        "watch_for": "reactivity, impatience, and battles you pick to relieve tension rather than serve truth",
        "practice": "Practice steady, constructive exertion.",
    },
    {
        "planet_slug": "jupiter",
        "planet_name": "Jupiter",
        "core": "growth, meaning, faith, blessing, and larger perspective",
        "watch_for": "overconfidence, excess, and assuming expansion removes the need for structure",
        "practice": "Practice deep, patient study.",
    },
    {
        "planet_slug": "saturn",
        "planet_name": "Saturn",
        "core": "structure, endurance, accountability, and time-tested maturity",
        "watch_for": "heaviness, fear, withdrawal, and mistaking delay for rejection",
        "practice": "Practice slow, disciplined repetition.",
    },
]

TRANSIT_SPECIALS = [
    {
        "slug": "mercury-retrograde",
        "label": "Mercury Retrograde",
        "planet_slug": "mercury",
        "planet_name": "Mercury",
        "sign_slug": None,
        "sign_name": None,
        "core": "review, revision, and wiser speech under slowed timing",
        "watch_for": "mixed signals, paperwork drift, and impulsive replies",
        "practice": "Edit before sending, pray before answering, and review before agreeing.",
    },
    {
        "slug": "venus-retrograde",
        "label": "Venus Retrograde",
        "planet_slug": "venus",
        "planet_name": "Venus",
        "sign_slug": None,
        "sign_name": None,
        "core": "relationship reflection, value revision, and heart-level honesty",
        "watch_for": "nostalgia, blurry standards, and beauty without truth",
        "practice": "Return to the relationships and promises that still need mature clarity.",
    },
    {
        "slug": "mars-retrograde",
        "label": "Mars Retrograde",
        "planet_slug": "mars",
        "planet_name": "Mars",
        "sign_slug": None,
        "sign_name": None,
        "core": "paused assertion, redirected effort, and a deeper audit of motivation",
        "watch_for": "frustrated anger and force without strategy",
        "practice": "Turn intensity into training, planning, and honest self-observation.",
    },
    {
        "slug": "jupiter-retrograde",
        "label": "Jupiter Retrograde",
        "planet_slug": "jupiter",
        "planet_name": "Jupiter",
        "sign_slug": None,
        "sign_name": None,
        "core": "inner teaching, belief review, and a quieter form of expansion",
        "watch_for": "inflated certainty or waiting for wisdom without practicing it",
        "practice": "Return to the teachings you already know but have not embodied yet.",
    },
    {
        "slug": "saturn-retrograde",
        "label": "Saturn Retrograde",
        "planet_slug": "saturn",
        "planet_name": "Saturn",
        "sign_slug": None,
        "sign_name": None,
        "core": "inner accountability, karmic review, and disciplined restructuring",
        "watch_for": "discouragement, paralysis, and harsh self-judgment",
        "practice": "Repair one neglected responsibility instead of trying to fix your whole life in one move.",
    },
    {
        "slug": "eclipse-season",
        "label": "Eclipse Season",
        "planet_slug": "sun",
        "planet_name": "Sun and Moon",
        "sign_slug": None,
        "sign_name": None,
        "core": "sudden clarity, emotional volatility, and accelerated turning points",
        "watch_for": "drama, projection, and decisions made inside temporary turbulence",
        "practice": "Stay observant, keep rituals simple, and resist forcing certainty too early.",
    },
]

TRANSIT_SLUGS: list[dict[str, str | None]] = []
for family in TRANSIT_FAMILIES:
    for sign in SIGNS:
        TRANSIT_SLUGS.append(
            {
                "slug": f"{family['planet_slug']}-in-{sign['slug']}",
                "label": f"{family['planet_name']} in {sign['name']}",
                "planet_slug": family["planet_slug"],
                "planet_name": family["planet_name"],
                "sign_slug": sign["slug"],
                "sign_name": sign["name"],
                "core": family["core"],
                "watch_for": family["watch_for"],
                "practice": family["practice"],
            }
        )
TRANSIT_SLUGS.extend(TRANSIT_SPECIALS)
TRANSIT_INDEX = {item["slug"]: item for item in TRANSIT_SLUGS}

GITA_REFERENCES = DAILY_SCRIPTURES["GITA"]
BIBLE_REFERENCES = DAILY_SCRIPTURES["BIBLE"]
TRADITION_META = {
    "gita": {
        "label": "Bhagavad Gita",
        "intro": "Gita guidance reads the transit as a training ground for dharma, disciplined effort, and inner steadiness.",
        "verses": GITA_REFERENCES,
        "prayer_prefix": "Transit mantra",
    },
    "bible": {
        "label": "Bible",
        "intro": "Bible guidance reads the transit as a season for faithful response, wise surrender, and scripture-led courage.",
        "verses": BIBLE_REFERENCES,
        "prayer_prefix": "Transit prayer",
    },
}


def _today_iso() -> str:
    return datetime.now(INDIA_TZ).date().isoformat()


def _chapter_verse_from_reference(reference: str) -> tuple[int, int] | tuple[None, None]:
    try:
        value = reference.rsplit(" ", 1)[-1]
        chapter_str, verse_str = value.split(":")
        return int(chapter_str), int(verse_str)
    except Exception:
        return None, None


def _hash_index(*values: str, modulus: int) -> int:
    total = 0
    for value in values:
        for char in value:
            total += ord(char)
    return total % modulus


def _title_case_slug(value: str) -> str:
    return " ".join(part.capitalize() for part in value.split("-"))


def _month_position(month_slug: str) -> int:
    for index, month in enumerate(MONTHS, start=1):
        if month["slug"] == month_slug:
            return index
    return 1


def _modality_style(modality: str) -> str:
    styles = {
        "Cardinal": "begins movement quickly and benefits from clean starts",
        "Fixed": "holds the line strongly and needs conscious flexibility",
        "Mutable": "adapts fluidly and needs structure so openness does not become drift",
    }
    return styles.get(modality, "responds best to steady, conscious practice")


def _transit_sign_frame(sign: dict, transit: dict, tradition: str) -> str:
    watch_phrase = _transit_watch_phrase(transit, sign)
    core_phrase = _transit_core_phrase(transit, sign)
    tradition_lens = (
        "Gita language emphasizes disciplined action, dharma, and clean effort."
        if tradition == "gita"
        else "Bible language emphasizes faithful response, surrender, and trust under pressure."
    )
    return (
        f"{sign['name']} receives this transit through {sign['element'].lower()} instinct and {sign['modality'].lower()} pacing. "
        f"{sign['element']} signs tend to process {transit['core']} by leaning into {sign['seasonal_focus']}, while a {sign['modality'].lower()} sign style "
        f"{_modality_style(sign['modality'])}. That means {transit['label'].lower()} is less about abstract astrology and more about how {sign['name']} can "
        f"{sign['growth_edge']} while {watch_phrase} is in the atmosphere. {tradition_lens}"
    )


def _transit_integration_steps(sign: dict, transit: dict, tradition: str) -> list[str]:
    openings = {
        "Cardinal": f"Start with one deliberate reset that helps {sign['name']} stop reacting to the transit on autopilot.",
        "Fixed": f"Loosen one rigid habit so {sign['name']} can work with the transit instead of defending against it.",
        "Mutable": f"Choose one container for the day so {sign['name']} does not let the transit scatter attention.",
    }
    middle = {
        "Fire": f"Channel the heat into one courageous act that serves truth rather than performance during {transit['label'].lower()}.",
        "Earth": f"Turn the transit into one measurable routine that keeps effort grounded and visible during {transit['label'].lower()}.",
        "Air": f"Name the clearest sentence you need to remember so the transit does not multiply unnecessary voices.",
        "Water": f"Protect the emotional field with one ritual that keeps feeling from becoming the only authority today.",
    }
    closings = {
        "gita": f"Close with a duty check: ask whether today's choices honored {transit['core']} with steadiness instead of noise.",
        "bible": f"Close with a prayer check: ask where trust, mercy, or obedience needs to become more concrete before sleep.",
    }
    return [
        openings.get(sign["modality"], f"Begin with one small reset that fits {sign['name']}'s present pace."),
        middle.get(sign["element"], f"Use the transit to practice one steadier response around {transit['core']}."),
        closings.get(tradition, "Close by naming one faithful response you want to repeat tomorrow."),
    ]


def _transit_watch_phrase(transit: dict, sign: dict | None) -> str:
    if sign is None:
        options = [
            f"the transit's drift toward {transit['watch_for'].split(',')[0]}",
            f"pressure turning into {transit['watch_for'].split(',')[0]} before wisdom catches up",
            f"{transit['watch_for'].split(',')[0]} becoming the atmosphere instead of the warning",
            f"timing noise around {transit['watch_for'].split(',')[0]}",
        ]
        return options[_hash_index(transit["slug"], "collective-watch", modulus=len(options))]

    tendency = transit["watch_for"].split(",")[0].strip()
    seed = _hash_index(transit["slug"], sign["slug"], modulus=6)
    options = [
        f"{sign['name']}'s drift toward {tendency}",
        f"the {sign['element'].lower()} reflex in {sign['name']} reaching for {tendency}",
        f"{sign['name']}'s {sign['modality'].lower()} habit of answering strain with {tendency}",
        f"{transit['planet_name'].lower()} pressure exaggerating {sign['name']}'s pull toward {tendency}",
        f"{tendency} taking over {sign['name']}'s timing before reflection arrives",
        f"{sign['name']}'s urge to manage the season through {tendency}",
    ]
    return options[seed]


def _transit_core_phrase(transit: dict, sign: dict | None) -> str:
    if sign is None:
        return transit["core"]
    return (
        f"{transit['planet_name']} themes landing in {sign['name']}'s {sign['element'].lower()} and {sign['modality'].lower()} style"
    )


def _transit_type(transit: dict) -> str:
    slug = transit["slug"]
    if "retrograde" in slug:
        return "retrograde"
    if "eclipse" in slug:
        return "eclipse"
    return "ingress"


def _transit_seed(transit_slug: str, tradition: str, modulus: int) -> int:
    return _hash_index(transit_slug, tradition, modulus=modulus)


def _transit_summary_text(transit: dict, sign: dict | None, tradition: str) -> str:
    core_phrase = _transit_core_phrase(transit, sign)
    transit_type = _transit_type(transit)
    seed = _hash_index(transit["slug"], tradition, "summ", modulus=12)
    if tradition == "gita":
        options = [
            f"{transit['label']} puts {core_phrase} under direct pressure. The Gita layer here is not prediction but discipline: how to act with steadier motive when timing amplifies the demand.",
            f"A {transit_type} season is not a pause. For {core_phrase}, it is an intensification - the kind that forces review, correction, and realignment. This page approaches it through karma-yoga practice, not through avoidance.",
            f"What does dharma require when {core_phrase} is under transit pressure? This page answers that through action-discipline, not consolation.",
            f"The instinct during {transit['label'].lower()} is often to manage external outcomes. The Gita layer inverts that: manage motive and effort first, and let outcomes belong to the timing.",
            f"Without a disciplined frame, {transit['label'].lower()} makes {core_phrase} reactive. This Gita page provides that frame.",
            f"If {transit['label'].lower()} is in the current sky, {core_phrase} is live for you right now. This page uses Gita language to give that pressure a useful shape.",
            f"The reactive read of {transit['label'].lower()} is pressure. The Gita read is opportunity: {core_phrase} becomes a training field when steady action governs motive.",
            f"What changes when {core_phrase} is under {transit_type} pressure? This Gita page answers with a discipline frame rather than a narrative one.",
            f"Left without a framework, {transit['label'].lower()} turns {core_phrase} into anxiety. This Gita reading converts the same pressure into a karma-yoga drill.",
            f"If {transit_type} energy is active now, {core_phrase} is where it lands first. The Gita route gives that landing a usable shape.",
            f"Every {transit_type} brings something into relief. For {core_phrase}, {transit['label'].lower()} brings the demand for cleaner motive to the surface.",
            f"When {core_phrase} is already unstable, {transit['label'].lower()} amplifies the instability. The Gita layer here is a stabilizer, not an explanation.",
        ]
    else:
        options = [
            f"{transit['label']} presses directly on {core_phrase}. The Bible route answers that pressure through trust, speech, and obedience rather than through speculation.",
            f"When a {transit_type} season arrives, the question is not merely what changes outside. It is whether {core_phrase} can be carried with prayerful steadiness inside the change.",
            f"What does scripture ask for when {core_phrase} comes under timing strain? This page answers with repentance, trust, and faithful response.",
            f"The reflex during {transit['label'].lower()} is often to predict outcomes and then panic. The Bible layer reverses that order: pray first, obey next, and let the season unfold under God.",
            f"Without a pastoral frame, {transit['label'].lower()} turns {core_phrase} into inner noise. This Bible page gives the reader a cleaner response pattern.",
            f"If this transit is active now, {core_phrase} is where the spiritual work is happening. The Bible route gives that work a prayer-shaped vocabulary.",
            f"The reactive read of {transit['label'].lower()} is fear. The Bible read is trust: {core_phrase} becomes a place for prayer when the season intensifies.",
            f"What changes when {core_phrase} is under {transit_type} pressure? This Bible page answers with surrender and obedience rather than speculation.",
            f"Left without a pastoral frame, {transit['label'].lower()} turns {core_phrase} into spiritual noise. This scripture reading converts the same strain into a prayerful response.",
            f"If {transit_type} energy is active now, {core_phrase} is where it lands first. The Bible route gives that landing a trust-shaped vocabulary.",
            f"Every {transit_type} brings something into relief. For {core_phrase}, {transit['label'].lower()} brings the call to cleaner faith to the surface.",
            f"When {core_phrase} is already vulnerable, {transit['label'].lower()} amplifies that vulnerability. The Bible layer here is a shepherding frame, not a panic script.",
        ]
    return options[seed]


def _transit_energy_text(transit: dict, sign: dict | None, tradition: str, watch_phrase: str) -> str:
    core_phrase = _transit_core_phrase(transit, sign)
    transit_type = _transit_type(transit)
    seed = _hash_index(transit["slug"], tradition, "enrg", modulus=12)
    if tradition == "gita":
        options = [
            f"In Gita terms, the question is whether {core_phrase} can be carried without surrendering to {watch_phrase}. That is the real pressure of this {transit_type} season.",
            f"Do not read {transit['label'].lower()} first as fate. Read it as a correction cycle around {core_phrase}, especially where {watch_phrase} keeps trying to take the steering wheel.",
            f"{core_phrase.capitalize()} becomes the training field here. The real opponent is not the calendar but {watch_phrase}, which is why steadier motive matters more than stronger emotion.",
            f"This timing window exposes conduct before it explains events. Where {core_phrase} is concerned, {watch_phrase} has to be noticed early or it becomes the hidden author of choice.",
            f"Without self-mastery, a {transit_type} phase turns {core_phrase} into reaction. With self-mastery, the same phase becomes usable discipline - precisely where {watch_phrase} wants the opposite.",
            f"If you want the Gita reading in one line, it is this: let {core_phrase} be shaped by duty while {watch_phrase} is kept under observation.",
            f"The season becomes spiritually expensive when {watch_phrase} starts deciding how {core_phrase} will be handled. The Gita concern is to interrupt that takeover early.",
            f"What looks like timing pressure is often motive pressure in disguise. Around {core_phrase}, {watch_phrase} reveals whether discipline or impulse is actually leading.",
            f"Not every transit exposes behavior so directly, but this {transit_type} one does. {core_phrase.capitalize()} is where {watch_phrase} tries to become normal.",
            f"If the atmosphere feels louder than the facts, notice what {watch_phrase} is doing to {core_phrase}. That observation is already part of the discipline.",
            f"A seeker usually loses the thread here not through events but through identification with {watch_phrase}. {core_phrase.capitalize()} is where that identification must break.",
            f"When the calendar tightens, {watch_phrase} tries to pass itself off as wisdom. The Gita page keeps {core_phrase} from being governed by that substitution.",
        ]
    else:
        options = [
            f"In Bible terms, this {transit_type} season asks whether {core_phrase} can be carried with cleaner trust while {watch_phrase} keeps crowding the heart.",
            f"Treat {transit['label'].lower()} as a pastoral threshold, not a panic trigger. {core_phrase.capitalize()} comes forward here, and {watch_phrase} has to be answered with prayerful steadiness.",
            f"{core_phrase.capitalize()} is where the test lands. The deeper issue is whether {watch_phrase} will narrate the season before scripture does.",
            f"This timing window presses on trust before it explains events. Around {core_phrase}, the soul has to resist {watch_phrase} or the whole season becomes spiritually distorted.",
            f"Without faithful response, a {transit_type} phase turns {core_phrase} into turmoil. With faithful response, the same phase becomes a place for surrender and cleaner speech.",
            f"If the Bible reading is reduced to one sentence, it is this: guard {core_phrase} with prayer while {watch_phrase} is still trying to grow roots.",
            f"The season becomes spiritually costly when {watch_phrase} starts deciding how {core_phrase} will be interpreted. The Bible concern is to interrupt that reading early.",
            f"What looks like timing pressure is often trust pressure in disguise. Around {core_phrase}, {watch_phrase} reveals whether fear or surrender is actually speaking.",
            f"Not every transit exposes the heart so directly, but this {transit_type} one does. {core_phrase.capitalize()} is where {watch_phrase} tries to become normal.",
            f"If the atmosphere feels louder than the facts, notice what {watch_phrase} is doing to {core_phrase}. That discernment is already part of the pastoral work.",
            f"A soul usually loses clarity here not through events but through agreement with {watch_phrase}. {core_phrase.capitalize()} is where that agreement must be broken.",
            f"When the calendar tightens, {watch_phrase} tries to sound reasonable. The Bible page keeps {core_phrase} from being narrated by that false reason.",
        ]
    return options[seed]


def _transit_application_text(transit: dict, sign: dict | None, tradition: str) -> str:
    core_phrase = _transit_core_phrase(transit, sign)
    transit_type = _transit_type(transit)
    seed = _hash_index(transit["slug"], tradition, "appl", modulus=12)
    if tradition == "gita":
        options = [
            f"Use this {transit_type} phase as a karma-yoga drill. {transit['practice']} Keep the action small enough to repeat, and let {core_phrase} become something practiced rather than merely analyzed.",
            f"Start where {core_phrase} is already being tested. Then apply {transit['practice'].lower()} with cleaner motive until repetition becomes steadier than mood.",
            f"Not a dramatic overhaul - a disciplined loop. Treat {core_phrase} as today's duty field and let {transit['practice'].lower()} convert atmosphere into habit.",
            f"What should be done with this transit? Begin where {core_phrase} feels unstable and let {transit['practice'].lower()} rebuild sequence and restraint.",
            f"Practice must become stronger than reaction here. Use {transit['practice'].lower()} at the precise point where {core_phrase} is under strain, and let relief arrive second.",
            f"If you need one instruction for the Gita route, keep it simple: meet {core_phrase} through repeated duty and let {transit['practice'].lower()} teach steadiness.",
            f"The first useful move is smaller than the atmosphere suggests. Apply {transit['practice'].lower()} where {core_phrase} is fraying, then repeat it until the season loses some of its authority.",
            f"If motive is the hidden battlefield, action is still the visible medicine. Use {transit['practice'].lower()} so {core_phrase} is trained instead of merely discussed.",
            f"Do not try to solve the whole transit. Take the one stretch of {core_phrase} that feels most unstable and answer it with {transit['practice'].lower()}.",
            f"When this {transit_type} phase starts tightening, let repetition outrun interpretation. {core_phrase.capitalize()} becomes steadier when {transit['practice'].lower()} keeps returning.",
            f"One disciplined act now is worth more than a full theory of the season. Bring {transit['practice'].lower()} directly to {core_phrase} and let behavior teach the mind.",
            f"The clean Gita application is not intensity but sequence: identify the unstable zone in {core_phrase}, then let {transit['practice'].lower()} become the next honest duty.",
        ]
    else:
        options = [
            f"Use this {transit_type} phase as a prayer-and-obedience rhythm. {transit['practice']} Keep the response concrete, and let {core_phrase} be met through trust rather than frantic control.",
            f"Begin where {core_phrase} is already exposed. Practice {transit['practice'].lower()}, then let the next step stay prayerfully honest instead of theatrically certain.",
            f"Not prediction first but response first. Meet {core_phrase} with scripture, confession, or prayerful action, and let {transit['practice'].lower()} anchor the day.",
            f"What does the Bible route ask for here? Start where {core_phrase} feels most vulnerable and let {transit['practice'].lower()} become the next faithful response.",
            f"Trust must outrun panic in this season. Use {transit['practice'].lower()} at the exact place where {core_phrase} is being tested, and keep the step spiritually clean.",
            f"If one pastoral move has to carry the whole transit, let it be this: turn {core_phrase} into a prayer field and keep repeating {transit['practice'].lower()}.",
            f"The first useful move is smaller than the atmosphere suggests. Apply {transit['practice'].lower()} where {core_phrase} feels thin, then repeat it until the season loses some of its power to alarm.",
            f"If trust is the hidden battlefield, obedience is still the visible medicine. Use {transit['practice'].lower()} so {core_phrase} is shepherded instead of merely analyzed.",
            f"Do not try to solve the whole transit. Take the one exposed part of {core_phrase} and answer it with {transit['practice'].lower()} before the story grows louder.",
            f"When this {transit_type} phase tightens, let faithful repetition outrun interpretation. {core_phrase.capitalize()} becomes steadier when {transit['practice'].lower()} keeps returning.",
            f"One obedient act now is worth more than a full theory of the season. Bring {transit['practice'].lower()} directly to {core_phrase} and let response teach the heart.",
            f"The clean Bible application is not intensity but faithfulness: identify the vulnerable zone in {core_phrase}, then let {transit['practice'].lower()} become the next honest response.",
        ]
    return options[seed]


def _transit_faq(transit: dict, sign_name: str | None, tradition_meta: dict, tradition: str, watch_phrase: str) -> list[dict]:
    selector = _transit_seed(transit["slug"], tradition, modulus=8)
    label = transit["label"]
    if selector == 0:
        return [
            {
                "q": f"What kind of inner work does {label} expose?",
                "a": f"It exposes the part of life where {transit['core']} must mature before {watch_phrase} turns into the season's dominant reflex.",
            },
            {
                "q": f"Why does this page use {tradition_meta['label']} for {label}?",
                "a": f"Because this tradition gives a workable spiritual vocabulary for the exact pressure pattern this transit tends to surface.",
            },
            {
                "q": f"How should {sign_name or 'a reader'} practice during {label}?",
                "a": f"Keep one repeatable discipline that is small enough to survive mood swings and clear enough to become training.",
            },
        ]
    if selector == 1:
        return [
            {
                "q": f"Why can {label} feel louder than the external facts?",
                "a": f"Because the transit often intensifies inner weather around {transit['core']} before the outer story has finished changing shape.",
            },
            {
                "q": f"Which spiritual habit protects clarity during {label}?",
                "a": f"A short repeated practice works better than intensity bursts, especially once {watch_phrase} starts building in the background.",
            },
            {
                "q": f"How does {tradition_meta['label']} reinterpret this transit?",
                "a": f"It asks the reader to move inward rather than wait for events to resolve, which is what this tradition does with pressure cycles.",
            },
        ]
    if selector == 2:
        return [
            {
                "q": f"How should {sign_name or 'a reader'} read {label} spiritually?",
                "a": f"Read it as a season where {transit['core']} becomes impossible to ignore. The healthiest response is thoughtful practice that matches this {tradition_meta['label'].lower()} route instead of dramatic overreaction.",
            },
            {
                "q": f"Why does this {tradition_meta['label']} page fit {label}?",
                "a": f"It delivers a reading of {label.lower()} built to stay usable once {watch_phrase} starts narrowing the picture.",
            },
            {
                "q": f"What daily practice best supports {sign_name or label} timing?",
                "a": f"Use one modest ritual that suits {label.lower()} - a prayer pause, a short reading, or a panchang check - because consistency will teach more than intensity spikes.",
            },
        ]
    if selector == 3:
        return [
            {
                "q": f"What does {label} usually put pressure on first?",
                "a": f"It usually presses first on the area of life where {transit['core']} has already been unstable, especially once {watch_phrase} starts rising.",
            },
            {
                "q": f"How can someone avoid making this transit theatrical?",
                "a": f"Treat it as a discipline cycle instead of a drama cycle: narrow the response, repeat the practice, and keep timing cleaner than mood.",
            },
            {
                "q": f"Why pair transit language with {tradition_meta['label']} here?",
                "a": f"Because scripture gives the transit an ethical response pattern instead of leaving it as atmosphere description alone.",
            },
        ]
    if selector == 4:
        return [
            {
                "q": f"What is the most useful spiritual posture during {label}?",
                "a": f"The most useful posture is steadier repetition: notice where {watch_phrase} is growing louder and answer it with a smaller, more faithful action.",
            },
            {
                "q": f"How should {sign_name or 'the reader'} use timing information without overreacting?",
                "a": f"Use timing to pace the response, not to surrender agency. The goal is cleaner rhythm, not dependence on agitation.",
            },
            {
                "q": f"What makes this transit page different from a generic forecast?",
                "a": f"It is built as a practice page: the transit names the pressure, and the scripture tradition names the right kind of response.",
            },
        ]
    if selector == 5:
        return [
            {
                "q": f"When is {label} spiritually most demanding?",
                "a": f"It is most demanding when the atmosphere around {transit['core']} is already strained and {watch_phrase} begins turning pressure into reflex.",
            },
            {
                "q": f"What response helps keep this transit from wasting energy?",
                "a": f"A measured repeatable response helps most. The aim is to keep the season teachable instead of letting it become a cycle of overcorrection.",
            },
            {
                "q": f"Why does this page focus on response more than prediction?",
                "a": f"Because the spiritual value of transit work lies in how the reader answers the season, not in claiming certainty about every event within it.",
            },
        ]
    if selector == 6:
        return [
            {
                "q": f"How does {tradition_meta['label']} keep {label} from becoming fatalistic?",
                "a": f"It insists that the reader's quality of attention matters more than the transit's duration. {transit['core'].capitalize()} can be trained regardless of how {watch_phrase} resolves.",
            },
            {
                "q": f"What is the smallest useful practice for navigating {label}?",
                "a": f"One honest, repeated act that does not depend on the transit cooperating. That kind of practice outlasts the season.",
            },
            {
                "q": f"Why is {sign_name or 'this reader'} better served by a tradition-rooted reading of {label}?",
                "a": f"Because a tradition gives the transit an ethical shape instead of leaving it as ambient pressure with no clear call to action.",
            },
        ]
    return [
        {
            "q": f"What does {label} reveal about how {transit['core']} matures over time?",
            "a": f"It reveals that maturity requires sustained attention rather than peak effort. Each return to practice during {label} builds what a single intense response never could.",
        },
        {
            "q": f"How can {sign_name or 'this reader'} use this tradition framework without losing independence?",
            "a": f"Use it as a reference, not a verdict. The tradition names the pattern; {sign_name or 'the reader'} decides the response. That distinction keeps the work personal.",
        },
        {
            "q": f"Why does {label} matter spiritually even when the external effects feel small?",
            "a": f"Because the interior work it initiates around {transit['core']} can outlast the transit itself. What is built during the season is more durable than what the season resolves.",
        },
    ]


def _daily_seed(sign_slug: str, month_slug: str, modulus: int) -> int:
    return _hash_index(sign_slug, month_slug, modulus=modulus)


def _daily_summary(sign: dict, month: dict) -> str:
    seed = _daily_seed(sign["slug"], month["slug"], modulus=5)
    options = [
        f"{month['name']} is approached here as an evergreen training month for {sign['name']}, where {sign['element'].lower()} instinct and scripture-shaped practice meet.",
        f"For {sign['name']}, this {month['name']} page is less a forecast than a timing discipline built inside {month['month_energy']}.",
        f"Not a forecast but a recurring field: the {sign['name']} {month['name']} guide meets {month['month_energy']} with repeated practice rather than prediction.",
        f"Under this Faith reading, {month['name']} becomes a spiritual season for {sign['name']} rather than a one-time prediction window.",
        f"Imagine {month['name']} as a recurring practice field for {sign['name']}. That is the premise behind this sign-and-scripture guide.",
    ]
    return options[seed]


def _daily_month_focus(sign: dict, month: dict) -> str:
    month_position = _month_position(month["slug"])
    element_bucket_leads = {
        ("Fire", 0): f"Early-year {month['name']} asks {sign['name']} to channel ignition before it scatters into impulsive starts.",
        ("Fire", 1): f"Mid-cycle {month['name']} asks {sign['name']} to sustain the fire rather than keep relighting it.",
        ("Fire", 2): f"Late-cycle {month['name']} asks {sign['name']} to reflect on what the year's heat actually built.",
        ("Earth", 0): f"Early-year {month['name']} asks {sign['name']} to build structure before momentum pressures shortcuts.",
        ("Earth", 1): f"Mid-cycle {month['name']} asks {sign['name']} to keep effort grounded while everything else speeds up.",
        ("Earth", 2): f"Late-cycle {month['name']} asks {sign['name']} to consolidate what was grown rather than starting fresh.",
        ("Air", 0): f"Early-year {month['name']} asks {sign['name']} to clarify direction before mental energy turns into noise.",
        ("Air", 1): f"Mid-cycle {month['name']} asks {sign['name']} to keep communication precise while the year's pace peaks.",
        ("Air", 2): f"Late-cycle {month['name']} asks {sign['name']} to distinguish insight earned from ideas still unproven.",
        ("Water", 0): f"Early-year {month['name']} asks {sign['name']} to channel emotional depth into early decisions rather than deferring them.",
        ("Water", 1): f"Mid-cycle {month['name']} asks {sign['name']} to protect the emotional field while external demands accelerate.",
        ("Water", 2): f"Late-cycle {month['name']} asks {sign['name']} to integrate what the year's feeling-states have been teaching.",
    }
    bucket = 0 if month_position <= 4 else (1 if month_position <= 8 else 2)
    lead = element_bucket_leads.get(
        (sign["element"], bucket),
        f"{month['name']} asks {sign['name']} to work wisely with the season's demands.",
    )
    selector = _daily_seed(sign["slug"], month["slug"], modulus=8)
    close = [
        f"instead of holding {sign['growth_edge']} only as an intention.",
        f"rather than filing {month['seasonal_note']} away as insight.",
        f"instead of leaving {sign['growth_edge']} as an unreached resolution.",
        f"rather than admiring {month['month_energy']} without applying it.",
        f"instead of letting {month['month_energy']} remain a private idea.",
        f"rather than turning {sign['growth_edge']} into a promise with no embodiment.",
        f"instead of keeping {month['seasonal_note']} trapped in reflection.",
        f"rather than studying {month['month_energy']} without practicing it.",
    ][selector]
    variants = [
        f"{lead} The training edge is {sign['growth_edge']} inside {month['month_energy']}, {close}",
        f"{lead} This season tests whether {sign['growth_edge']} can survive {month['month_energy']}, {close}",
        f"{lead} {month['month_energy'].capitalize()} becomes useful only when {sign['growth_edge']} is practiced, {close}",
        f"{lead} The month matures when {sign['growth_edge']} moves from reflection into behavior within {month['month_energy']}, {close}",
        f"{lead} The work of {month['month_energy']} is to make {sign['growth_edge']} visible in ordinary choices, {close}",
        f"{lead} If {month['month_energy']} is handled well, {sign['growth_edge']} stops sounding aspirational and starts sounding necessary, {close}",
        f"{lead} The season is asking {sign['name']} to translate {month['month_energy']} through {sign['growth_edge']}, {close}",
        f"{lead} {month['month_energy'].capitalize()} presses the month toward embodiment, which is why {sign['growth_edge']} has to become active, {close}",
    ]
    return variants[selector]


def _daily_gita_application(sign: dict, month: dict, gita: dict) -> str:
    month_position = _month_position(month["slug"])
    if sign["modality"] == "Cardinal":
        lead = "The verse is strongest when it helps the reader begin cleanly instead of beginning noisily."
    elif sign["modality"] == "Fixed":
        lead = "The verse is strongest when it softens stubborn momentum without draining conviction."
    else:
        lead = "The verse is strongest when it gives movement a container so flexibility does not become diffusion."

    if month_position <= 4:
        month_move = "Use it to shape the start of the month before the pace hardens."
    elif month_position <= 8:
        month_move = "Use it midstream, when the month is already moving and steadiness matters more than enthusiasm."
    else:
        month_move = "Use it as an end-of-cycle correction that gathers the month back into wisdom."
    outcomes = {
        1: f"For {month['name']}, that means turning first movement into a cleaner vow.",
        2: f"For {month['name']}, that means turning visible momentum into something that can actually be sustained.",
        0: f"For {month['name']}, that means turning spiritual insight into a repeatable rhythm before the month scatters it.",
    }

    selector = _daily_seed(sign["slug"], month["slug"], modulus=8)
    gita_close = [
        f"That is how {month['seasonal_note']} becomes a practice for {sign['name']} rather than a theme.",
        f"The verse is most useful when it converts {month['seasonal_note']} into a specific {sign['modality'].lower()} next step.",
        f"One repeated act that honors {sign['growth_edge']} is worth more than a month of intention without behavior.",
        f"{month['seasonal_note']} becomes real for {sign['name']} when it shows up in a decision, not just in a reflection.",
        f"That is the point where {month['month_energy']} stops being ambient and starts becoming directional.",
        f"Used well, the verse makes {month['month_energy']} feel trainable rather than chaotic.",
        f"This is where {month['seasonal_note']} turns into a lived response instead of a passing impression.",
        f"The month changes most when {month['month_energy']} is answered through repeated action.",
    ][selector]
    variants = [
        f"{gita['reference']} meets {sign['name']} through {month['month_energy']} this month. {lead} {month_move} {outcomes[month_position % 3]} {gita_close}",
        f"When {sign['name']} enters {month['name']}, {gita['reference']} becomes useful inside {month['month_energy']}. {month_move} {gita_close}",
        f"Do not start with the whole month; start with the verse. {gita['reference']} meets {month['month_energy']} for {sign['name']} before the rest of the schedule fills in. {outcomes[month_position % 3]} {gita_close}",
        f"The Gita route for {sign['name']} in {month['name']} is practical, not decorative. Use {gita['reference']} where {month['month_energy']} needs cleaner handling most. {gita_close}",
        f"In {month['name']}, {month['month_energy']} is the reason this Gita verse matters. {lead} Let the next decision carry the teaching rather than only admiring it. {gita_close}",
        f"{gita['reference']} belongs in this month because {month['month_energy']} is asking for steadier action from {sign['name']}. {month_move} {gita_close}",
        f"If {month['month_energy']} is the atmosphere, {gita['reference']} is the training line. Use it in {month['name']} with one clear action and let the momentum follow. {gita_close}",
        f"The month becomes more usable when {gita['reference']} interprets {month['month_energy']} before mood does. For {sign['name']}, that means one repeatable act. {gita_close}",
    ]
    return variants[selector]


def _daily_bible_application(sign: dict, month: dict, bible: dict) -> str:
    selector = _daily_seed(sign["slug"], month["slug"], modulus=8)
    variants = [
        f"{bible['reference']} meets {month['name']} by naming the hidden fear inside {month['month_energy']}. For {sign['name']}, read it as a call to practice trust in a way that matches {sign['daily_practice'].lower()}.",
        f"When {month['month_energy']} starts crowding the heart, {bible['reference']} becomes the Bible anchor for {sign['name']}. Let the promise move toward {sign['daily_practice'].lower()}.",
        f"The Bible side of this month begins with {bible['reference']}, because {month['name']} often tests trust before it tests outcomes. Use the verse in the same rhythm as {sign['daily_practice'].lower()}.",
        f"Not every month needs more information; some months need a steadier promise. For {sign['name']}, {bible['reference']} answers {month['month_energy']} from that place. Practice it through {sign['daily_practice'].lower()}.",
        f"In {month['name']}, {bible['reference']} keeps {month['month_energy']} from becoming spiritually shapeless. Carry it through {sign['daily_practice'].lower()}.",
        f"The promise matters this month because {month['month_energy']} can distort trust if it goes uninterpreted. {bible['reference']} gives {sign['name']} a steadier response. Let that response shape {sign['daily_practice'].lower()}.",
        f"{bible['reference']} belongs in {month['name']} where {month['month_energy']} is already pressing the heart. Practice the promise through {sign['daily_practice'].lower()}.",
        f"When {month['month_energy']} begins deciding the emotional weather, answer it with {bible['reference']}. For {sign['name']}, let the verse travel through {sign['daily_practice'].lower()}.",
    ]
    return variants[selector]


def _daily_faq(sign: dict, month: dict, gita: dict, bible: dict) -> list[dict]:
    selector = _daily_seed(sign["slug"], month["slug"], modulus=8)
    if selector == 0:
        return [
            {
                "q": f"Why does {month['name']} ask {sign['name']} for these two scriptures?",
                "a": f"{gita['reference']} and {bible['reference']} were paired because {month['month_energy']} tends to expose {sign['name']}'s need for {sign['seasonal_focus']}.",
            },
            {
                "q": f"What practice keeps {sign['name']} grounded first in {month['name']}?",
                "a": f"Start with one repeatable action that supports {sign['growth_edge']} inside {month['month_energy']}, then let the rest of the month build around that steadier center.",
            },
            {
                "q": f"How does {sign['modality'].lower()} pacing help during {month['name']}?",
                "a": f"{sign['modality']} energy works best in {month['month_energy']} when it {_modality_style(sign['modality'])} rather than reacting to every shift in mood or timing.",
            },
        ]
    if selector == 1:
        return [
            {
                "q": f"What is the main spiritual tension for {sign['name']} in {month['name']}?",
                "a": f"The main tension is how to move through {month['month_energy']} without losing {sign['seasonal_focus']}.",
            },
            {
                "q": f"Why pair a Gita verse with a Bible promise for {sign['name']} this month?",
                "a": f"Because {gita['reference']} disciplines {month['month_energy']} through effort while {bible['reference']} disciplines it through faithfulness -- each addresses the same pressure from a different foundation.",
            },
            {
                "q": f"How should a {sign['element'].lower()} sign pace prayer in {month['name']}?",
                "a": f"Use a practice rhythm that respects {sign['element'].lower()} sensitivity while still giving {month['month_energy']} enough structure to mature into action.",
            },
        ]
    if selector == 2:
        return [
            {
                "q": f"Which month pattern is most important for {sign['name']} to notice in {month['name']}?",
                "a": f"It is the pattern where {month['seasonal_note']} starts pulling this sign away from {sign['growth_edge']}.",
            },
            {
                "q": f"What should a {sign['element'].lower()} {sign['name']} practice first in {month['name']}?",
                "a": f"Return first to {sign['daily_practice'].lower()} and let that small act regulate the rest of the day inside {month['month_energy']}.",
            },
            {
                "q": f"Why is this guide evergreen instead of date-specific for {month['name']}?",
                "a": f"Because it is built around the repeatable interaction between sign nature, {month['month_energy']}, and scripture-backed practice rather than around a one-time forecast.",
            },
        ]
    if selector == 3:
        return [
            {
                "q": f"What does {month['name']} usually test first in {sign['name']}?",
                "a": f"It usually tests whether {sign['seasonal_focus']} can survive the first wave of {month['month_energy']}.",
            },
            {
                "q": f"How can this sign keep the month from becoming scattered?",
                "a": f"Give {sign['daily_practice'].lower()} a fixed time and let the rest of {month['month_energy']} organize itself around that anchor.",
            },
            {
                "q": f"What makes the scripture pair practical instead of decorative?",
                "a": f"The Gita text trains effort, the Bible text trains trust, and both are tied to one concrete rhythm for meeting {month['month_energy']}.",
            },
        ]
    if selector == 4:
        return [
            {
                "q": f"When does {month['name']} become spiritually noisy for {sign['name']}?",
                "a": f"When {month['seasonal_note']} stops being interpreted and starts being obeyed without reflection.",
            },
            {
                "q": f"How should {sign['name']} use the paired scriptures before a busy day?",
                "a": f"Read the shorter one first, carry one phrase from it into the day, and let the second text deepen that phrase later while {month['month_energy']} is still manageable.",
            },
            {
                "q": f"Why keep the month tied to sign temperament at all?",
                "a": f"Because the same scripture lands differently in fire, earth, air, and water lives, especially once {month['month_energy']} enters the picture.",
            },
        ]
    if selector == 5:
        return [
            {
                "q": f"What is the cleanest spiritual starting point for {sign['name']} in {month['name']}?",
                "a": f"Start where {sign['growth_edge']} already feels most resisted, because that is where this month is asking for practice instead of theory.",
            },
            {
                "q": f"How can {sign['name']} keep prayer connected to action this month?",
                "a": f"Let one prayer lead directly into one small behavior, so {month['month_energy']} never has to choose between inspiration and embodiment.",
            },
            {
                "q": f"Why does this page avoid prediction-style language for {month['name']}?",
                "a": f"Because the goal is repeatable formation through sign nature, {month['month_energy']}, and scripture, not dependence on a dated emotional forecast.",
            },
        ]
    if selector == 6:
        return [
            {
                "q": f"What is {sign['name']} most likely to neglect when {month['name']} gets busy?",
                "a": f"The {sign['growth_edge']} practice usually shrinks first. Protecting a small daily form of it is what keeps {month['month_energy']} from becoming drift.",
            },
            {
                "q": f"How should these two scriptures be read when {sign['name']} is already stretched thin?",
                "a": f"Read the shorter verse first, carry one word from it, and let the second text wait until the day offers a quieter moment.",
            },
            {
                "q": f"Why does this guide pair sign nature with scripture for {month['name']}?",
                "a": f"Because the month lands differently in different temperaments. What {sign['element'].lower()} attentiveness brings to {month['month_energy']} is not incidental - it is the whole point of a sign-rooted reading.",
            },
        ]
    return [
        {
            "q": f"Why approach {month['name']} as a recurring practice field rather than a new forecast?",
            "a": f"Because {sign['name']} returns to {month['name']} every year. A field that teaches {sign['growth_edge']} more clearly each cycle is more valuable than a prediction that expires in thirty days.",
        },
        {
            "q": f"How can {sign['name']} carry just one thing from these scriptures this month?",
            "a": f"Take the single phrase that feels most resistant right now -- from {gita['reference']} or {bible['reference']} -- and let it become the measure of one daily choice.",
        },
        {
            "q": f"What changes when {sign['name']} treats {month['month_energy']} as training material?",
            "a": f"The month stops being an obstacle to manage and starts being a teacher to use. {sign['growth_edge'].capitalize()} becomes more visible when pressure is accepted as instruction.",
        },
    ]


def _select_gita_pair(seed: str) -> list[dict[str, str]]:
    index = _hash_index(seed, modulus=len(GITA_REFERENCES))
    second = (index + 3) % len(GITA_REFERENCES)
    return [deepcopy(GITA_REFERENCES[index]), deepcopy(GITA_REFERENCES[second])]


def _select_bible_pair(seed: str) -> list[dict[str, str]]:
    index = _hash_index(seed, modulus=len(BIBLE_REFERENCES))
    second = (index + 2) % len(BIBLE_REFERENCES)
    return [deepcopy(BIBLE_REFERENCES[index]), deepcopy(BIBLE_REFERENCES[second])]


def _transit_seed_content(transit_slug: str, tradition: str) -> dict:
    transit = TRANSIT_INDEX[transit_slug]
    tradition_meta = TRADITION_META[tradition]
    sign_name = transit["sign_name"]
    sign = SIGN_INDEX.get(transit["sign_slug"] or "")
    label = transit["label"]
    transit_type = _transit_type(transit).capitalize()
    is_special = sign_name is None
    route_label = "Dharma Compass" if tradition == "gita" else "Pastoral Prayerfield"
    heading = (
        f"{label} - {transit_type} {route_label}"
        if is_special
        else f"{transit['planet_name']} in {sign_name} - {transit_type} {route_label}"
    )
    verse_items = _select_gita_pair(transit_slug) if tradition == "gita" else _select_bible_pair(transit_slug)
    article_slug = transit_slug
    today = _today_iso()
    transit_href = f"/transits/{article_slug}"
    panchang_href = f"/panchang/{DEFAULT_PANCHANG_CITY}/{today}"
    traits_href = f"/traits/{(transit['sign_slug'] or 'aries')}/sun/1st-house"
    watch_phrase = _transit_watch_phrase(transit, sign)
    core_phrase = _transit_core_phrase(transit, sign)
    summary = _transit_summary_text(transit, sign, tradition)
    energy_intro = _transit_energy_text(transit, sign, tradition, watch_phrase)
    practice_body = _transit_application_text(transit, sign, tradition)

    scripture_cards = []
    for offset, verse in enumerate(verse_items, start=1):
        scripture_cards.append(
            {
                "reference": verse["reference"],
                "text": verse["text"],
                "why_it_fits": (
                    f"Verse {offset} is used here because {label.lower()} places pressure on {core_phrase}. "
                    f"This teaching keeps the seeker focused on disciplined response instead of getting lost in {_transit_watch_phrase(transit, sign)}."
                ),
            }
        )

    prayer_body = (
        f"{tradition_meta['prayer_prefix']}: During {label.lower()}, keep my motives clean, my speech measured, "
        f"and my effort aligned with what is true. Teach {sign_name or 'me'} to meet {core_phrase} without giving in to {watch_phrase}."
    )
    page_path = f"/faith/transit/{transit_slug}/{tradition}"
    sign_frame = (
        _transit_sign_frame(sign, transit, tradition)
        if sign is not None
        else (
            f"{label} works less like a sign filter and more like a collective timing reset around {transit['core']}. "
            f"In these special windows, the spiritual task is to slow reaction, notice {watch_phrase}, and respond with cleaner timing than the atmosphere invites."
        )
    )
    integration_steps = (
        _transit_integration_steps(sign, transit, tradition)
        if sign is not None
        else [
            f"Name the one area where {label.lower()} is already changing your inner weather.",
            f"Use {transit['practice'].lower()} so the transit becomes a review process rather than a drama engine.",
            "End the day by noting what became clearer once you stopped forcing an answer too early.",
        ]
    )
    practice_title = (
        f"{sign_name} practice rhythm during {label}"
        if sign_name
        else f"Practice rhythm during {label}"
    )
    prayer_title = (
        f"{tradition_meta['prayer_prefix']} for {sign_name}"
        if sign_name
        else f"{tradition_meta['prayer_prefix']} for this transit season"
    )
    faq = _transit_faq(transit, sign_name, tradition_meta, tradition, watch_phrase)

    return {
        "id": f"faith-transit-{transit_slug}-{tradition}",
        "route": page_path,
        "title": heading,
        "meta_title": heading[:60],
        "meta_description": (
            f"Spiritual guidance for {label.lower()} with {tradition_meta['label']} references, practice ideas, and panchang timing."
        )[:155],
        "tradition": tradition,
        "tradition_label": tradition_meta["label"],
        "transit_slug": transit_slug,
        "transit_label": label,
        "planet_name": transit["planet_name"],
        "sign_name": sign_name,
        "summary": summary,
        "energy_intro": energy_intro,
        "guidance": energy_intro,
        "sign_frame_title": (
            f"{sign_name} {sign['element']} {sign['modality']} frame"
            if sign_name
            else f"Collective frame for {label}"
        ),
        "sign_frame": sign_frame,
        "scripture_cards": scripture_cards,
        "practice_title": practice_title,
        "practice_body": practice_body,
        "application": practice_body,
        "integration_title": (
            f"{sign_name} {sign['modality']} integration steps"
            if sign_name
            else "Three-step integration"
        ),
        "integration_steps": integration_steps,
        "prayer_title": prayer_title,
        "prayer_body": prayer_body,
        "faq": faq,
        "links": {
            "transit_href": transit_href,
            "panchang_href": panchang_href,
            "traits_href": traits_href,
            "faith_hub_href": "/faith",
            "tradition_hub_href": "/faith/transit",
        },
    }


def _daily_seed_content(sign_slug: str, month_slug: str) -> dict:
    sign = SIGN_INDEX[sign_slug]
    month = MONTH_INDEX[month_slug]
    month_number = _month_position(month_slug)
    gita = deepcopy(GITA_REFERENCES[(month_number + len(sign_slug)) % len(GITA_REFERENCES)])
    bible = deepcopy(BIBLE_REFERENCES[(month_number + len(month_slug)) % len(BIBLE_REFERENCES)])
    chapter, verse = _chapter_verse_from_reference(gita["reference"])
    gita_cross_link = f"/faith/gita/{chapter}-{verse}/{sign_slug}-season" if chapter and verse else "/faith/gita"
    transit_choice = TRANSIT_SLUGS[_hash_index(sign_slug, month_slug, modulus=len(TRANSIT_SLUGS))]
    title = f"{sign['name']} Spiritual Guide - {month['name']} for {month['month_energy']}"
    today = _today_iso()

    practices = [
        f"Begin {month['name']} by naming the one emotional pattern {sign['name']} needs to stop negotiating with.",
        f"In {month['name']}, give {sign['ruler']}-ruled discipline a concrete form: {sign['daily_practice']} Do it in a way that matches {month['seasonal_note']}.",
        f"Read one short scripture passage before the busiest part of the day so {month['month_energy']} becomes prayerfully interpreted instead of purely reactive.",
        f"Use the panchang before a major decision when {month['name']} starts amplifying {sign['modality'].lower()} pressure or {sign['element'].lower()} overstimulation.",
        f"Close the evening by writing one line about where {sign['growth_edge']} became visible inside {month['month_energy']}.",
    ]
    month_focus = _daily_month_focus(sign, month)
    gita_application = _daily_gita_application(sign, month, gita)
    bible_application = _daily_bible_application(sign, month, bible)
    faq = _daily_faq(sign, month, gita, bible)
    summary = _daily_summary(sign, month)

    return {
        "id": f"faith-daily-{sign_slug}-{month_slug}",
        "route": f"/faith/daily/{sign_slug}/{month_slug}",
        "sign_slug": sign_slug,
        "sign_name": sign["name"],
        "month_slug": month_slug,
        "month_name": month["name"],
        "title": title,
        "meta_title": title[:60],
        "meta_description": (
            f"{sign['name']} spiritual guidance for {month['name']} with a Gita verse, a Bible promise, and practical daily steps."
        )[:155],
        "summary": summary,
        "month_focus_title": f"{sign['name']} {sign['element']} focus for {month['name']}",
        "month_focus": month_focus,
        "energy_intro": (
            f"For {sign['name']}, {month['name']} tends to emphasize {sign['seasonal_focus']}. The month carries {month['seasonal_note']}, "
            f"so the deeper question is not what will happen next, but how this sign can live {month['month_energy']} without abandoning its center. "
            f"This is not a horoscope prediction. It is a spiritual guide for how {sign['element'].lower()} energy, {sign['modality'].lower()} pacing, and {sign['ruler']}-ruled instincts interact during {month['name']}."
        ),
        "message": month_focus,
        "guidance": f"{gita_application} {bible_application}",
        "gita_reference": gita["reference"],
        "gita_text": gita["text"],
        "scripture_blend_title": f"{sign['name']} {sign['element']} scripture blend for {month['name']}",
        "gita_application": gita_application,
        "bible_reference": bible["reference"],
        "bible_text": bible["text"],
        "bible_application": bible_application,
        "daily_practice_title": f"{month['name']} {sign['modality']} practice rhythm for {sign['name']}",
        "daily_practices": practices,
        "faq": faq,
        "cta": {
            "label": "Receive a personalized 21-day scripture plan matched to your Vedic birth chart.",
            "href": "/birth-chart",
        },
        "links": {
            "faith_hub_href": "/faith",
            "daily_hub_href": "/faith/daily",
            "sign_hub_href": f"/faith/daily/{sign_slug}",
            "transit_href": f"/faith/transit/{transit_choice['slug']}/gita",
            "panchang_href": f"/panchang/{DEFAULT_PANCHANG_CITY}/{today}",
            "gita_cross_link": gita_cross_link,
        },
    }


def build_daily_pages() -> list[dict]:
    pages = []
    for sign in SIGNS:
        for month in MONTHS:
            pages.append(_daily_seed_content(sign["slug"], month["slug"]))
    return pages


def build_transit_pages() -> list[dict]:
    pages = []
    for transit in TRANSIT_SLUGS:
        for tradition in ("gita", "bible"):
            pages.append(_transit_seed_content(transit["slug"], tradition))
    return pages


def get_daily_page(sign_slug: str, month_slug: str) -> dict | None:
    if sign_slug not in SIGN_INDEX or month_slug not in MONTH_INDEX:
        return None
    return _daily_seed_content(sign_slug, month_slug)


def get_transit_page(transit_slug: str, tradition: str) -> dict | None:
    if transit_slug not in TRANSIT_INDEX or tradition not in TRADITION_META:
        return None
    return _transit_seed_content(transit_slug, tradition)


def get_faith_hub_payload() -> dict:
    gita_pages = get_gita_page_count()
    bible_pages = get_bible_page_count()
    return {
        "title": "Faith Hubs - Gita, Bible, Transit and Daily Scripture",
        "meta_title": "Faith Hubs - Gita, Bible and Daily Scripture",
        "meta_description": "Explore Faith Hubs for daily scripture, transit guidance, the live Bhagavad Gita verse library, and Bible promise pathways by transition.",
        "hero_title": "Faith Hubs for Scripture, Transit Wisdom and Daily Practice",
        "hero_body": (
            "Faith Hubs is EverydayHoroscope's public scripture layer. It connects spiritual practice with the rhythms people actually live through: "
            "monthly emotional seasons, planetary pressure, and daily choices that need steadier guidance than generic inspiration."
        ),
        "counts": {
            "transit_pages": len(TRANSIT_SLUGS) * 2,
            "daily_pages": len(SIGNS) * len(MONTHS),
            "gita_pages": gita_pages,
            "bible_pages": bible_pages,
            "phase_total": len(TRANSIT_SLUGS) * 2 + len(SIGNS) * len(MONTHS) + gita_pages + bible_pages,
        },
        "collections": [
            {
                "slug": "transit",
                "title": "Transit and Scripture",
                "href": "/faith/transit",
                "count_label": f"{len(TRANSIT_SLUGS) * 2} pages",
                "description": "Planetary seasons paired with Gita and Bible guidance, plus practice suggestions rooted in timing and discipline.",
            },
            {
                "slug": "daily",
                "title": "Daily Scripture by Sign and Month",
                "href": "/faith/daily",
                "count_label": f"{len(SIGNS) * len(MONTHS)} pages",
                "description": "Evergreen monthly spiritual guides for every zodiac sign, designed as practice pages rather than prediction pages.",
            },
            {
                "slug": "gita",
                "title": "Gita Verse Hubs",
                "href": "/faith/gita",
                "count_label": f"{gita_pages} pages",
                "description": "All 700 Bhagavad Gita verses mapped across 15 life situations, with chapter hubs and verse-specific guidance.",
            },
            {
                "slug": "bible",
                "title": "Bible Promise Hubs",
                "href": "/faith/bible",
                "count_label": f"{bible_pages} pages",
                "description": "A Bible promise library organized by 120 themes and 50 real-life transitions, with parallel Gita bridges.",
            },
        ],
        "featured_transits": [deepcopy(item) for item in TRANSIT_SLUGS[:6]],
        "featured_signs": [deepcopy(item) for item in SIGNS[:6]],
        "faq": [
            {
                "q": "What are Faith Hubs on Everyday Horoscope?",
                "a": "Faith Hubs is the scripture-led layer that connects Gita, Bible, transit, and evergreen daily practice pages inside one public structure.",
            },
            {
                "q": "Are these pages predictions or spiritual guidance?",
                "a": "They are spiritual guidance pages. Transit and sign language are used as reflective timing frameworks, not as guarantees about what will happen.",
            },
            {
                "q": "How should a reader start if the library feels large?",
                "a": "Start from the main hub, a guided pathway, or the concern that feels most immediate, then move deeper into Gita, Bible, transit, or daily pages from there.",
            },
        ],
    }


def get_transit_hub_payload() -> dict:
    return {
        "title": "Faith Transit Hub",
        "meta_title": "Faith Transit Hub - Gita and Bible Guidance",
        "meta_description": "Explore transit-based scripture guidance across 78 transit themes and 2 faith traditions.",
        "hero_title": "Transit and Scripture Guidance",
        "hero_body": (
            "These pages are built for the moments when a transit changes the emotional weather before you can explain why. "
            "Each transit entry pairs a planetary pattern with either Bhagavad Gita or Bible guidance so the season becomes actionable instead of abstract."
        ),
        "traditions": [
            {"slug": "gita", "label": "Bhagavad Gita", "description": TRADITION_META["gita"]["intro"]},
            {"slug": "bible", "label": "Bible", "description": TRADITION_META["bible"]["intro"]},
        ],
        "transits": [deepcopy(item) for item in TRANSIT_SLUGS],
    }


def get_daily_hub_payload() -> dict:
    return {
        "title": "Faith Daily Hub",
        "meta_title": "Daily Scripture by Sign and Month",
        "meta_description": "Browse evergreen daily scripture guides by zodiac sign and month across all 144 sign-month combinations.",
        "hero_title": "Daily Scripture by Sign and Month",
        "hero_body": (
            "This daily layer is evergreen on purpose. Instead of expiring with a date stamp, each guide answers the deeper pattern a sign meets in a given month "
            "and offers scripture-backed practices that can be returned to year after year."
        ),
        "signs": [deepcopy(item) for item in SIGNS],
        "months": [deepcopy(item) for item in MONTHS],
    }


def get_daily_sign_payload(sign_slug: str) -> dict | None:
    sign = SIGN_INDEX.get(sign_slug)
    if sign is None:
        return None
    items = []
    for month in MONTHS:
        page = _daily_seed_content(sign_slug, month["slug"])
        items.append(
            {
                "month_slug": month["slug"],
                "month_name": month["name"],
                "href": page["route"],
                "summary": page["summary"],
            }
        )
    return {
        "title": f"{sign['name']} Daily Scripture Hub",
        "meta_title": f"{sign['name']} Spiritual Guides by Month",
        "meta_description": f"Browse all 12 evergreen monthly spiritual guides for {sign['name']} with Gita and Bible references.",
        "hero_title": f"{sign['name']} Spiritual Guides by Month",
        "hero_body": (
            f"This sign hub gathers every {sign['name']} monthly guide in one place. Use it when you want the spiritual rhythm of the month without reading a generic forecast."
        ),
        "sign": deepcopy(sign),
        "months": items,
    }


def get_gita_hub_payload() -> dict:
    return get_live_gita_hub_payload()


def get_bible_hub_payload() -> dict:
    return get_live_bible_hub_payload()


def get_faith_sitemap_urls() -> list[str]:
    urls = [
        f"{SITE_URL}/faith",
        f"{SITE_URL}/faith/pathways",
        f"{SITE_URL}/faith/transit",
        f"{SITE_URL}/faith/daily",
    ]
    urls.extend(f"{SITE_URL}/faith/pathways/{slug}" for slug in FAITH_PATHWAY_SLUGS)
    urls.extend(get_gita_sitemap_urls())
    urls.extend(get_bible_sitemap_urls())
    urls.extend(f"{SITE_URL}/faith/daily/{sign['slug']}" for sign in SIGNS)
    urls.extend(f"{SITE_URL}{page['route']}" for page in build_daily_pages())
    urls.extend(f"{SITE_URL}{page['route']}" for page in build_transit_pages())
    return urls
