from __future__ import annotations

from functools import lru_cache
from math import ceil


SITE_URL = "https://www.everydayhoroscope.in"
PAGE_SIZE = 1000

INTENT_ORDER = [
    "love",
    "career",
    "twin-flame",
    "manifestation",
    "health",
    "spiritual-growth",
    "family",
    "protection",
    "new-beginnings",
]

INTENT_CONFIG = {
    "love": {
        "display": "Love & Relationships",
        "theme": "heart-led honesty, emotional safety, and soulful reciprocity",
        "cta": "Choose clarity over mixed signals.",
        "strong_numbers": ["222", "444", "666", "1212", "2222"],
    },
    "career": {
        "display": "Career & Money",
        "theme": "purpose-led work, timing, and grounded progress",
        "cta": "Make the next smart move, not just the loudest one.",
        "strong_numbers": ["111", "555", "888", "1234", "4444"],
    },
    "twin-flame": {
        "display": "Twin Flame",
        "theme": "mirroring, healing, reunion cycles, and soul recognition",
        "cta": "Focus on inner alignment before outer chasing.",
        "strong_numbers": ["1111", "1212", "222", "7171", "7777"],
    },
    "manifestation": {
        "display": "Manifestation",
        "theme": "thought hygiene, aligned action, and energetic momentum",
        "cta": "Anchor the vision with one practical step.",
        "strong_numbers": ["111", "333", "555", "888", "9999"],
    },
    "health": {
        "display": "Health & Wellbeing",
        "theme": "nervous-system balance, routine, rest, and embodied healing",
        "cta": "Support the body before pushing the schedule.",
        "strong_numbers": ["444", "666", "777", "1010", "2424"],
    },
    "spiritual-growth": {
        "display": "Spiritual Growth",
        "theme": "inner guidance, awakening, discernment, and trust",
        "cta": "Create enough quiet to hear the deeper message.",
        "strong_numbers": ["333", "777", "999", "1111", "3333"],
    },
    "family": {
        "display": "Family & Home",
        "theme": "roots, belonging, repair, and supportive structure",
        "cta": "Strengthen the home base one honest conversation at a time.",
        "strong_numbers": ["222", "444", "666", "1000", "2626"],
    },
    "protection": {
        "display": "Protection & Guidance",
        "theme": "boundaries, reassurance, timing, and divine cover",
        "cta": "Move steadily and let wisdom set the pace.",
        "strong_numbers": ["444", "777", "999", "1414", "4444"],
    },
    "new-beginnings": {
        "display": "New Beginnings",
        "theme": "fresh starts, courage, release, and forward momentum",
        "cta": "Honor the ending, then step into the opening.",
        "strong_numbers": ["111", "555", "999", "1000", "2020"],
    },
}

BASE_ARCHETYPES = {
    1: {
        "label": "Initiator",
        "essence": "initiative, self-trust, and the courage to begin",
        "gift": "clear direction",
        "lesson": "moving before doubt hardens into delay",
        "themes": ["new beginnings", "leadership", "focus", "self-belief", "momentum"],
        "actions": ["claim the first step", "simplify the priority", "act with conviction"],
        "affirmation": "I trust the beginning that is opening for me.",
    },
    2: {
        "label": "Bridge",
        "essence": "cooperation, patience, and emotional intelligence",
        "gift": "harmonising people and timing",
        "lesson": "staying receptive without becoming passive",
        "themes": ["partnership", "balance", "patience", "intuition", "trust"],
        "actions": ["slow the pace", "listen deeply", "choose mutuality"],
        "affirmation": "I let trust and timing work together in my favor.",
    },
    3: {
        "label": "Messenger",
        "essence": "expression, joy, and inspired expansion",
        "gift": "creative momentum",
        "lesson": "turning insight into voice and action",
        "themes": ["creativity", "joy", "communication", "growth", "inspiration"],
        "actions": ["say what matters", "create something tangible", "follow the spark"],
        "affirmation": "My voice carries wisdom, warmth, and direction.",
    },
    4: {
        "label": "Builder",
        "essence": "stability, order, and dependable structure",
        "gift": "making support feel practical",
        "lesson": "building foundations before chasing scale",
        "themes": ["stability", "discipline", "protection", "routine", "grounding"],
        "actions": ["strengthen the base", "stay consistent", "protect your energy"],
        "affirmation": "I build my path with steadiness, patience, and grace.",
    },
    5: {
        "label": "Catalyst",
        "essence": "change, freedom, and adaptive intelligence",
        "gift": "unlocking movement where life has stalled",
        "lesson": "choosing conscious change over restless escape",
        "themes": ["change", "freedom", "adaptability", "movement", "curiosity"],
        "actions": ["release rigidity", "welcome the pivot", "choose growth over fear"],
        "affirmation": "I move with change and let it refine me.",
    },
    6: {
        "label": "Caretaker",
        "essence": "care, harmony, and the healing power of presence",
        "gift": "restoring warmth and connection",
        "lesson": "nurturing others without abandoning yourself",
        "themes": ["healing", "home", "beauty", "care", "responsibility"],
        "actions": ["restore balance", "care for the home", "lead with compassion"],
        "affirmation": "I create harmony by honoring care, truth, and tenderness.",
    },
    7: {
        "label": "Mystic",
        "essence": "reflection, intuition, and soul-level discernment",
        "gift": "deep spiritual clarity",
        "lesson": "trusting the inner signal more than external noise",
        "themes": ["intuition", "awakening", "wisdom", "reflection", "faith"],
        "actions": ["seek stillness", "trust the deeper knowing", "study the pattern"],
        "affirmation": "I trust the wisdom that rises in stillness.",
    },
    8: {
        "label": "Steward",
        "essence": "abundance, mastery, and karmic return",
        "gift": "turning effort into visible result",
        "lesson": "receiving success without losing integrity",
        "themes": ["abundance", "authority", "results", "discipline", "karma"],
        "actions": ["own your value", "lead responsibly", "stabilize the flow"],
        "affirmation": "I receive and circulate abundance with integrity.",
    },
    9: {
        "label": "Closer",
        "essence": "completion, compassion, and release",
        "gift": "helping life close one chapter cleanly",
        "lesson": "letting go before the next cycle arrives",
        "themes": ["completion", "release", "compassion", "service", "transformation"],
        "actions": ["finish the chapter", "forgive what is complete", "make room for renewal"],
        "affirmation": "I release with grace and welcome the wiser next chapter.",
    },
}

PRIORITY_SPECIAL_NUMBERS = [
    "1000",
    "1001",
    "1010",
    "1011",
    "1100",
    "1101",
    "1110",
    "1111",
    "1112",
    "1122",
    "1144",
    "1155",
    "1166",
    "1177",
    "1188",
    "1199",
    "1200",
    "1212",
    "1221",
    "1234",
    "1313",
    "1414",
    "1515",
    "1616",
    "1717",
    "1818",
    "1919",
    "2020",
    "2121",
    "2222",
    "2323",
    "2424",
    "2525",
    "2626",
    "2727",
    "2828",
    "2929",
    "3030",
    "3131",
    "3232",
    "3333",
    "3434",
    "3535",
    "3636",
    "3737",
    "3838",
    "3939",
    "4040",
    "4141",
    "4242",
    "4343",
    "4444",
    "4545",
    "4646",
    "4747",
    "4848",
    "4949",
    "5050",
    "5151",
    "5252",
    "5353",
    "5454",
    "5555",
    "5656",
    "5757",
    "5858",
    "5959",
    "6060",
    "6161",
    "6262",
    "6363",
    "6464",
    "6565",
    "6666",
    "6767",
    "6868",
    "6969",
    "7070",
    "7171",
    "7272",
    "7777",
    "8888",
    "9999",
    "10000",
]

SPECIAL_NUMBER_OVERRIDES = {
    "111": {"vibe": "manifestation portal", "tagline": "alignment, fresh momentum, and fast-moving intention"},
    "222": {"vibe": "relationship harmoniser", "tagline": "balance, patience, and trusted timing"},
    "333": {"vibe": "creative amplifier", "tagline": "expression, joy, and spiritual encouragement"},
    "444": {"vibe": "protection code", "tagline": "stability, support, and grounded reassurance"},
    "555": {"vibe": "transition trigger", "tagline": "change, movement, and liberating redirection"},
    "666": {"vibe": "restoration signal", "tagline": "care, home, and emotional rebalancing"},
    "777": {"vibe": "awakening beacon", "tagline": "intuition, study, and sacred confirmation"},
    "888": {"vibe": "abundance current", "tagline": "results, karmic return, and material flow"},
    "999": {"vibe": "completion bell", "tagline": "release, closure, and compassionate endings"},
    "1111": {"vibe": "master portal", "tagline": "awakening, synchronicity, and amplified intention"},
    "1212": {"vibe": "alignment ladder", "tagline": "faith, progress, and balanced momentum"},
    "1234": {"vibe": "ordered ascent", "tagline": "stepwise progress, structure, and clean advancement"},
    "2222": {"vibe": "master balance code", "tagline": "lasting partnership, patience, and sturdy trust"},
    "3333": {"vibe": "expansion chorus", "tagline": "creative abundance and supported growth"},
    "4444": {"vibe": "guardian wall", "tagline": "protection, discipline, and sacred structure"},
    "5555": {"vibe": "destiny pivot", "tagline": "bold change and accelerated reinvention"},
    "6666": {"vibe": "hearth keeper", "tagline": "healing, beauty, and the return to what matters"},
    "7777": {"vibe": "mystic mirror", "tagline": "deep spiritual verification and inner mastery"},
    "8888": {"vibe": "legacy builder", "tagline": "power, prosperity, and sustainable achievement"},
    "9999": {"vibe": "threshold closer", "tagline": "final release before a major rebirth"},
    "1000": {"vibe": "reset gate", "tagline": "clean beginnings, divine order, and renewed trust"},
    "10000": {"vibe": "magnified reset gate", "tagline": "scale, stewardship, and long-horizon beginnings"},
}

PATTERN_DETAILS = {
    "pure amplification": {
        "label": "amplified echo",
        "descriptor": "repeated digits keep the same lesson ringing until it is answered cleanly",
        "tempo": "direct response",
        "outcome": "the message gets louder when you try to answer it halfway",
    },
    "stepwise progress": {
        "label": "ascending ladder",
        "descriptor": "the sequence climbs in order, so progress matters more than drama",
        "tempo": "sequenced progress",
        "outcome": "the blessing lives in respecting the order of events",
    },
    "mirrored reinforcement": {
        "label": "mirrored bridge",
        "descriptor": "the reflected layout turns inner truth and outer events toward each other",
        "tempo": "balanced adjustment",
        "outcome": "reflection works best when both sides of the pattern are honored",
    },
    "rhythmic alternation": {
        "label": "alternating rhythm",
        "descriptor": "the digits pulse back and forth, revealing where response patterns need refinement",
        "tempo": "measured recalibration",
        "outcome": "small corrections made consistently matter more than one dramatic swing",
    },
    "reset and recalibration": {
        "label": "reset corridor",
        "descriptor": "zero widens the field so the lesson can be heard without old static",
        "tempo": "intentional reset",
        "outcome": "space and timing become part of the medicine, not a delay tactic",
    },
    "layered guidance": {
        "label": "layered weave",
        "descriptor": "mixed digits stack several lessons together, so nuance matters",
        "tempo": "pattern reading",
        "outcome": "clarity comes from seeing how the parts of life interact, not from forcing one note",
    },
}

ROOT_VIBRATION_FRAGMENTS = {
    1: [
        "It strengthens decisive self-trust and clears space for an honest beginning.",
        "It sharpens your inner yes so hesitation stops dressing up as caution.",
    ],
    2: [
        "It softens force and teaches timing through relationship, rhythm, and receptive intelligence.",
        "It restores trust in pacing so connection can grow without being rushed.",
    ],
    3: [
        "It wakes up voice, expression, and the courage to let inspiration become visible.",
        "It rewards open communication and turns buried insight into useful movement.",
    ],
    4: [
        "It favors structure, steadiness, and the kind of discipline that makes protection practical.",
        "It brings order back to the situation so your next step can stand on something solid.",
    ],
    5: [
        "It turns change into usable momentum instead of letting transition become chaos.",
        "It loosens stale patterns so movement can happen without abandoning discernment.",
    ],
    6: [
        "It gathers scattered energy back into care, harmony, and responsible devotion.",
        "It restores warmth and asks whether your environment truly supports what you value.",
    ],
    7: [
        "It deepens spiritual listening and makes quiet discernment more valuable than noise.",
        "It asks for reflection strong enough to separate intuition from projection.",
    ],
    8: [
        "It concentrates authority, responsibility, and karmic return into visible results.",
        "It teaches mastery by making value, effort, and consequence easier to read.",
    ],
    9: [
        "It ripens closure and makes release feel purposeful instead of punishing.",
        "It helps endings become clean enough for the next cycle to arrive without residue.",
    ],
}

PATTERN_VIBRATION_FRAGMENTS = {
    "pure amplification": [
        "The amplified echo keeps pressing the exact same note until your response matches it.",
        "Because the digits repeat without dilution, the number does not support half-hearted participation.",
    ],
    "stepwise progress": [
        "The ascending ladder says the answer develops in sequence, with each stage earning the next.",
        "This climbing pattern rewards order, pacing, and respect for process over shortcuts.",
    ],
    "mirrored reinforcement": [
        "The mirrored bridge reflects your inner state back through outer events, which makes honesty essential.",
        "This mirrored pattern asks you to reconcile what you feel privately with what you are building publicly.",
    ],
    "rhythmic alternation": [
        "The alternating rhythm reveals where repeated responses are either healing the cycle or feeding it.",
        "This back-and-forth pattern makes calibration the real work, not dramatic speed.",
    ],
    "reset and recalibration": [
        "The reset corridor uses space, pause, and perspective as part of the guidance itself.",
        "Because zero is involved, the pattern wants a cleaner field before it asks for a louder move.",
    ],
    "layered guidance": [
        "The layered weave suggests several lessons are arriving together, so a single-track reading will miss the point.",
        "This mixed pattern behaves like a woven signal: one strand explains the next.",
    ],
}

VIBRATION_CADENCE = [
    "That is why this sequence tends to arrive right before a meaningful choice, not after one.",
    "That is what makes the number feel active rather than merely symbolic.",
    "That is where the sequence becomes guidance instead of decoration.",
    "That is why the message usually clarifies once you respond in a concrete way.",
]

ROOT_SEEING_FRAGMENTS = {
    1: [
        "Treat the sighting as permission to stop waiting for perfect certainty.",
        "Let the repetition remind you that a clean beginning is already available.",
    ],
    2: [
        "Read the sighting as a cue to trust rhythm, timing, and relational truth.",
        "Use the repetition to return to patience without slipping into passivity.",
    ],
    3: [
        "Take the sequence as a prompt to express what has been ripening inside you.",
        "Let the repetition pull hidden insight into conversation, art, prayer, or truth-telling.",
    ],
    4: [
        "Receive the sighting as a reminder to stabilize the foundation before demanding faster results.",
        "Take the repetition as support for consistency, boundaries, and practical next steps.",
    ],
    5: [
        "Treat the sighting as a nudge to work with change rather than negotiating against it.",
        "Read the repetition as proof that movement is already underway and needs your cooperation.",
    ],
    6: [
        "Use the sequence as a reminder to restore warmth where life has become overly functional.",
        "Take the sighting as a call to bring care, beauty, and responsibility back into alignment.",
    ],
    7: [
        "Treat the repetition as an invitation to trust the deeper signal before the louder one.",
        "Use the sighting to move closer to stillness, study, and clean discernment.",
    ],
    8: [
        "Read the sequence as a sign that consequence, value, and stewardship are coming into sharper view.",
        "Take the repetition seriously when money, leadership, or responsibility is asking for integrity.",
    ],
    9: [
        "Treat the sighting as confirmation that something is ready to complete without being dragged further.",
        "Use the repetition to release the chapter that already taught what it came to teach.",
    ],
}

PATTERN_SEEING_FRAGMENTS = {
    "pure amplification": [
        "The amplified echo keeps returning until the obvious move is answered with full participation.",
        "Repeated digits rarely settle for mixed signals, so clarity matters more than comforting delay.",
    ],
    "stepwise progress": [
        "The ascending ladder asks you to honor sequence, because the next step makes sense only after the present one is lived.",
        "Climbing numbers rarely ask for a leap; they ask for the courage to respect progression.",
    ],
    "mirrored reinforcement": [
        "The mirrored bridge usually appears when your inner truth and outer behavior need to match more closely.",
        "Reflected patterns often surface when life is showing you yourself through timing, people, and repetition.",
    ],
    "rhythmic alternation": [
        "The alternating rhythm points to habits, loops, and response cycles that are ready for refinement.",
        "Back-and-forth patterns are often less about prediction and more about correcting the way you keep answering the same lesson.",
    ],
    "reset and recalibration": [
        "The reset corridor suggests a pause, clearing, or clean restart is part of the answer, not avoidance of it.",
        "Zero-backed patterns usually appear when space itself is the medicine and timing needs to be reset.",
    ],
    "layered guidance": [
        "The layered weave means several areas of life are speaking at once, so the message opens through nuance.",
        "Mixed-digit sequences often arrive when you need to read the whole pattern rather than one isolated event.",
    ],
}

SEEING_CADENCE = [
    "That is usually the moment the message turns from curiosity into useful direction.",
    "That is where the number stops repeating as noise and starts acting like guidance.",
    "That is often where relief begins, because the lesson is finally being met directly.",
    "That is how the sighting becomes a turning point instead of a passing coincidence.",
    "That is when the pattern finally earns its name and becomes something you can work with.",
    "That is the window where noticing becomes deciding instead of just observing.",
    "That is how attention shifts from pattern-spotting into the question the pattern was asking.",
    "That is usually where the urgency softens and the deeper invitation becomes clearer.",
    "That is the moment the sequence graduates from background noise into a recognisable signal.",
    "That is where the repeated sighting earns its authority by matching something already known inside.",
    "That is often the point where the sign loses its mystery and gains its usefulness.",
    "That is how the number becomes a verb instead of a noun -- something to act on, not just observe.",
    "That is the interval where the visible pattern and the internal question finally land on the same page.",
    "That is how external repetition eventually translates into interior clarity.",
    "That is when the message stops accumulating and starts delivering what it was building toward.",
    "That is usually when seeing it again stops feeling like coincidence and starts feeling like information.",
    "That is where the sighting converts from something noticed to something used.",
    "That is how a number earns meaning rather than borrows it from elsewhere.",
    "That is the point where the signal has done its job and the next move belongs to you.",
    "That is when the repeated pattern becomes a compass rather than a curiosity.",
    "That is how the sequence moves from background frequency into a question worth answering directly.",
    "That is the moment the accumulation tips from interesting into actionable.",
    "That is usually where the resistance softens enough to let the actual message through.",
    "That is how consistent sightings eventually do what a single sighting never could.",
    "That is the crossing point where wonder turns into discernment and the number does its real work.",
    "That is when the frequency becomes familiar enough to feel instructive instead of strange.",
    "That is how a sequence that began as noise quietly becomes the clearest signal in the room.",
    "That is the threshold where repetition stops being a coincidence and starts being a curriculum.",
    "That is when the sighting finally earns the attention it was asking for all along.",
    "That is how the number moves from being seen to being understood, which is always the point.",
    "That is usually when the meaning stops hiding in the pattern and starts showing up in the choices.",
    "That is how a sequence that felt random gradually becomes the most coherent voice in a noisy moment.",
    "That is where the pattern hands the work back to you, because the seeing was always preparation.",
    "That is when the number finishes its loop and the response belongs entirely to the person watching.",
    "That is how repetition that once felt like background static becomes the signal worth following.",
]

INTENT_STYLES = {
    "love": {
        "focus": "emotional honesty, reciprocity, and the courage to say what the heart actually needs",
        "challenge": "mixed signals, protective silence, or attachment habits that blur the truth",
        "closing": [
            "Let the heart move with honesty, because this sequence favors connection that can survive the truth.",
            "Use the number as permission to choose reciprocity over guessing games and emotional over-editing.",
        ],
    },
    "career": {
        "focus": "timing, earned opportunity, professional courage, and clearer money decisions",
        "challenge": "scattered effort, underpricing, or fear of being seen at your real level",
        "closing": [
            "Treat the signal like a timing note from life: act where momentum is real and stop feeding what keeps leaking energy.",
            "Use the sequence to tighten your standards, because career progress rarely improves through vagueness.",
        ],
    },
    "twin-flame": {
        "focus": "mirroring, soul recognition, reunion-separation lessons, and nervous-system steadiness",
        "challenge": "confusing obsession with guidance or reading every emotional spike as destiny",
        "closing": [
            "Let the number point you back to inner regulation first, because twin-flame lessons sharpen when self-abandonment stops.",
            "Read the sign as guidance toward mirroring and healing, not as a license to chase intensity without discernment.",
        ],
    },
    "manifestation": {
        "focus": "alignment, attention, energetic congruence, and co-creation with clear intent",
        "challenge": "contradictory focus, emotional static, or trying to manifest from urgency rather than resonance",
        "closing": [
            "Use the sequence to match thought, feeling, and behavior, because manifestation responds to coherence more than wishful repetition.",
            "Let the number refine your signal until desire, action, and timing are finally speaking the same language.",
        ],
    },
    "health": {
        "focus": "body signals, energy rhythm, rest, regulation, and the lifestyle patterns that either support or drain you",
        "challenge": "ignoring fatigue, forcing pace, or living in a way your body keeps protesting",
        "closing": [
            "Treat the number like a body-level nudge, because wellbeing improves when signals are answered early instead of endured late.",
            "Let the sequence restore rhythm before you demand output, because health is often the foundation beneath every other answer.",
        ],
    },
    "spiritual-growth": {
        "focus": "inner work, awareness, discernment, and the relationship between wisdom and lived practice",
        "challenge": "spiritual bypassing, noisy intuition, or collecting insight without embodiment",
        "closing": [
            "Use the sign to move from spiritual theory into lived practice, because clarity matures through embodiment.",
            "Let the sequence deepen awareness rather than decorate it, because genuine growth changes behavior as well as belief.",
        ],
    },
    "family": {
        "focus": "roots, home dynamics, forgiveness, roles, and generational patterns asking for repair",
        "challenge": "old scripts, avoidance, or carrying responsibilities that no longer belong to you",
        "closing": [
            "Treat the number as a prompt to heal the atmosphere, not just the argument, because families often change through tone before words.",
            "Let the sequence guide you toward steadier roots, cleaner roles, and conversations that stop recycling old pain.",
        ],
    },
    "protection": {
        "focus": "boundaries, discernment, energetic safety, and the wisdom to separate guidance from pressure",
        "challenge": "porous boundaries, overexposure, or mistaking intensity for truth",
        "closing": [
            "Use the number to strengthen discernment, because protection often looks like clear boundaries before it looks like rescue.",
            "Let the sequence remind you that safety grows when your yes and no become equally trustworthy.",
        ],
    },
    "new-beginnings": {
        "focus": "thresholds, release, starting conditions, and the emotional readiness required for a fresh chapter",
        "challenge": "dragging expired stories into a doorway that needs cleaner energy",
        "closing": [
            "Treat the sign as a threshold marker, because beginnings work best when endings are actually honored.",
            "Let the number help you clear the runway so the next chapter begins from intention rather than leftover momentum.",
        ],
    },
}


def reduce_to_root(number: str) -> int:
    total = sum(int(ch) for ch in number)
    while total > 9:
        total = sum(int(ch) for ch in str(total))
    return total


def is_repeating(number: str) -> bool:
    return len(set(number)) == 1


def is_mirrored(number: str) -> bool:
    return len(number) >= 4 and number[: len(number) // 2] == number[len(number) // 2 :]


def is_ascending(number: str) -> bool:
    digits = [int(ch) for ch in number]
    return all(digits[index] + 1 == digits[index + 1] for index in range(len(digits) - 1))


def is_alternating(number: str) -> bool:
    return len(number) >= 4 and len(set(number[::2])) == 1 and len(set(number[1::2])) == 1


def number_pattern(number: str) -> str:
    if is_repeating(number):
        return "pure amplification"
    if is_ascending(number):
        return "stepwise progress"
    if is_mirrored(number):
        return "mirrored reinforcement"
    if is_alternating(number):
        return "rhythmic alternation"
    if "0" in number:
        return "reset and recalibration"
    return "layered guidance"


def variation_seed(number: str, salt: int = 0) -> int:
    return sum((index + 1 + salt) * int(ch) for index, ch in enumerate(number)) + len(number) * 13 + salt * 17


def choose_variant(options: list[str], number: str, salt: int = 0) -> str:
    return options[variation_seed(number, salt) % len(options)]


def number_digits(number: str) -> list[int]:
    return [int(ch) for ch in number]


def number_structure_note(number: str, pattern: str) -> str:
    digits = number_digits(number)
    leading = digits[0]
    trailing = digits[-1]
    zero_count = number.count("0")
    if pattern == "pure amplification":
        return f"Because every digit repeats the same note, {number} behaves like a concentrated signal rather than a subtle hint."
    if pattern == "stepwise progress":
        return f"Because the digits rise from {leading} to {trailing}, {number} favors order, pacing, and one honest step at a time."
    if pattern == "mirrored reinforcement":
        return f"Because the sequence mirrors itself around its midpoint, {number} often reflects inner reality back through outer timing."
    if pattern == "rhythmic alternation":
        return f"The alternating movement between {leading} and {trailing} gives {number} a rhythmic quality that exposes repeated response habits."
    if pattern == "reset and recalibration":
        return f"With {zero_count} zero{'s' if zero_count != 1 else ''} in the sequence, {number} creates more space around the lesson and slows the reaction cycle down."
    return f"The mixed-digit structure of {number} layers the opening force of {leading} with the closing lesson of {trailing}, so the guidance lands through nuance."


def build_vibration_closer(number: str, root: int, pattern: str) -> str:
    root_fragment = choose_variant(ROOT_VIBRATION_FRAGMENTS[root], number, salt=1).rstrip(".")
    pattern_fragment = choose_variant(PATTERN_VIBRATION_FRAGMENTS[pattern], number, salt=2).rstrip(".").lower()
    cadence = choose_variant(VIBRATION_CADENCE, number, salt=3).rstrip(".").lower()
    return f"{root_fragment} while {pattern_fragment}, and {cadence}."


def build_seeing_closer(number: str, root: int, pattern: str) -> str:
    root_fragment = choose_variant(ROOT_SEEING_FRAGMENTS[root], number, salt=4).rstrip(".")
    pattern_fragment = choose_variant(PATTERN_SEEING_FRAGMENTS[pattern], number, salt=5).rstrip(".").lower()
    cadence = choose_variant(SEEING_CADENCE, number, salt=6).rstrip(".").lower()
    return f"{root_fragment} because {pattern_fragment}, and {cadence}."


def build_intent_message_closer(number: str, intent: str, root: int, pattern: str) -> str:
    style = INTENT_STYLES[intent]
    archetype = BASE_ARCHETYPES[root]
    pattern_detail = PATTERN_DETAILS[pattern]
    intent_close = choose_variant(style["closing"], number, salt=7)
    cadence = [
        f"The root-{root} lesson is to let {archetype['gift']} shape the choice instead of letting pressure set the tone.",
        f"The healthiest move is the one that honors {archetype['gift']} while respecting the {pattern_detail['tempo']} this pattern is asking for.",
        f"That is how {number} turns {pattern_detail['label']} energy into a practical next step rather than a passing spiritual mood.",
    ]
    return f"{intent_close} {choose_variant(cadence, number, salt=8)}"


@lru_cache(maxsize=1)
def get_core_numbers() -> tuple[str, ...]:
    numbers: list[str] = [str(value) for value in range(1, 10)]
    numbers.extend(str(value) for value in range(11, 100, 11))
    numbers.extend(str(value) for value in range(100, 1000))

    seen = set(numbers)
    reserved_tail = ["7777", "8888", "9999", "10000"]
    specials = [value for value in PRIORITY_SPECIAL_NUMBERS if value not in reserved_tail][:78]
    specials.extend(reserved_tail)

    for value in specials:
        if value not in seen:
            numbers.append(value)
            seen.add(value)
        if len(numbers) == 1000:
            break

    if len(numbers) != 1000:
        raise ValueError(f"Expected 1000 angel numbers, found {len(numbers)}")
    return tuple(numbers)


@lru_cache(maxsize=1)
def get_number_index() -> dict[str, int]:
    return {number: index for index, number in enumerate(get_core_numbers())}


def normalize_number(raw_number: str) -> str | None:
    digits = "".join(ch for ch in raw_number if ch.isdigit())
    if not digits:
        return None
    normalized = str(int(digits))
    return normalized if normalized in get_number_index() else None


def number_family_members(root: int) -> list[str]:
    return [number for number in get_core_numbers() if reduce_to_root(number) == root]


def related_numbers(number: str, root: int) -> list[str]:
    index = get_number_index()[number]
    matches: list[str] = []

    for candidate in number_family_members(root):
        if candidate != number:
            matches.append(candidate)
        if len(matches) == 2:
            break

    for offset in (-1, 1, -2, 2):
        if 0 <= index + offset < len(get_core_numbers()):
            candidate = get_core_numbers()[index + offset]
            if candidate != number and candidate not in matches:
                matches.append(candidate)
        if len(matches) == 4:
            break

    return matches[:4]


def number_label(number: str, root: int) -> str:
    override = SPECIAL_NUMBER_OVERRIDES.get(number)
    if override:
        return override["tagline"]
    base = BASE_ARCHETYPES[root]
    return f"{base['label'].lower()} energy with {number_pattern(number)}"


def build_key_themes(number: str, root: int) -> list[str]:
    base = list(BASE_ARCHETYPES[root]["themes"])
    extras = []
    if is_repeating(number):
        extras.extend(["amplification", "clarity"])
    if is_ascending(number):
        extras.extend(["progress", "momentum"])
    if is_mirrored(number):
        extras.extend(["balance", "echoed support"])
    if is_alternating(number):
        extras.extend(["rhythm", "course correction"])
    if "0" in number:
        extras.extend(["reset", "trust"])

    unique = []
    for value in base + extras:
        if value not in unique:
            unique.append(value)
    return unique[:6]


def build_vibration(number: str, root: int) -> str:
    archetype = BASE_ARCHETYPES[root]
    pattern = number_pattern(number)
    override = SPECIAL_NUMBER_OVERRIDES.get(number)
    if override:
        return (
            f"{number} carries a {override['vibe']} wrapped in the root-{root} current of "
            f"{archetype['essence']}. {build_vibration_closer(number, root, pattern)}"
        )
    return (
        f"Angel number {number} carries the root-{root} current of {archetype['essence']}, expressed through "
        f"a pattern of {pattern}. {build_vibration_closer(number, root, pattern)}"
    )


def build_summary(number: str, root: int) -> str:
    archetype = BASE_ARCHETYPES[root]
    return (
        f"Angel number {number} highlights {archetype['essence']}. When this sequence keeps repeating, "
        f"it usually means your next step becomes easier once you respond with {archetype['gift']}."
    )


def build_seeing_it_means(number: str, root: int) -> str:
    archetype = BASE_ARCHETYPES[root]
    pattern = number_pattern(number)
    return (
        f"Seeing {number} repeatedly is often a timing signal rather than random coincidence. "
        f"It draws your attention back to {archetype['essence']} and asks where life is inviting you into "
        f"{archetype['lesson']}. {number_structure_note(number, pattern)} "
        f"If the number appears during stress, it is a reminder to regulate first and respond second. "
        f"{build_seeing_closer(number, root, pattern)}"
    )


def build_core_actions(number: str, root: int) -> list[str]:
    archetype = BASE_ARCHETYPES[root]
    pattern = number_pattern(number)
    return [
        f"Name the one situation where {number} is asking for {archetype['gift']}.",
        f"Use this {pattern} phase to {archetype['actions'][0]} before the window passes.",
        f"End the day by choosing one concrete way to {archetype['actions'][2]}.",
    ]


def build_core_affirmation(number: str, root: int) -> str:
    override = SPECIAL_NUMBER_OVERRIDES.get(number)
    if override:
        return f"I receive the {override['vibe']} of {number} and act in alignment with it."
    return BASE_ARCHETYPES[root]["affirmation"]


@lru_cache(maxsize=1)
def build_intent_base_matrix() -> dict[str, dict[int, dict[str, object]]]:
    matrix: dict[str, dict[int, dict[str, object]]] = {}
    for intent, config in INTENT_CONFIG.items():
        style = INTENT_STYLES[intent]
        matrix[intent] = {}
        for root, archetype in BASE_ARCHETYPES.items():
            matrix[intent][root] = {
                "opening": (
                    f"In {config['display'].lower()}, the root-{root} {archetype['label'].lower()} current emphasizes "
                    f"{config['theme']} and asks for {style['focus']}."
                ),
                "focus_line": (
                    f"It is strongest when {archetype['gift']} guides the way you handle {style['focus']}."
                ),
                "challenge_line": (
                    f"The friction usually shows up through {style['challenge']}, so the lesson is less about forcing the answer and more about {archetype['lesson']}."
                ),
                "actions": [
                    f"{config['cta']} Let {archetype['gift']} set the tone instead of urgency.",
                    f"Use this area of life to {archetype['actions'][0]} with more honesty than performance.",
                    f"Let {archetype['actions'][1]} guide the next concrete move you make here.",
                ],
            }
    return matrix


def build_intent_message(number: str, intent: str, root: int) -> str:
    pattern = number_pattern(number)
    template = build_intent_base_matrix()[intent][root]
    pattern_detail = PATTERN_DETAILS[pattern]
    return (
        f"Angel number {number} brings {template['focus_line'].lower()} "
        f"{template['challenge_line']} {number_structure_note(number, pattern)} "
        f"This {pattern_detail['label']} pattern matters here because {pattern_detail['descriptor']}. "
        f"{build_intent_message_closer(number, intent, root, pattern)}"
    )


def build_intent_action_steps(number: str, intent: str, root: int) -> list[str]:
    archetype = BASE_ARCHETYPES[root]
    pattern = number_pattern(number)
    pattern_detail = PATTERN_DETAILS[pattern]

    if intent == "love":
        return [
            f"Say the feeling you have been editing down, because {number} favors emotional clarity over protective guessing.",
            f"Use {archetype['gift']} to reset one relationship pattern this week, especially where the current dynamic feels stuck in {pattern_detail['tempo']}.",
            f"Ask whether this connection is growing through reciprocity, firmer boundaries, or a cleaner goodbye, and act on the honest answer.",
        ]
    if intent == "career":
        return [
            f"List the next work or money decision that needs a cleaner timeline, because {number} rarely appears just to inspire without asking for structure.",
            f"Apply {archetype['gift']} to one measurable move today, whether that means pitching, pricing, delegating, or closing a distraction.",
            f"Cut one obligation that keeps your professional energy scattered so the {pattern_detail['label']} of this number can become momentum.",
        ]
    if intent == "twin-flame":
        return [
            f"Regulate your body before interpreting the bond, because {number} is more useful when your nervous system is steady than when it is flooded.",
            f"Journal what this connection is mirroring back to you and let {archetype['gift']} guide the part that is yours to heal.",
            f"Choose one action that honors sacred timing instead of chase energy, especially if the current cycle already feels shaped by {pattern_detail['tempo']}.",
        ]
    if intent == "manifestation":
        return [
            f"Write the desire behind this sighting in one clean sentence, then remove any goal that conflicts with it.",
            f"Use {archetype['gift']} to align one behavior with the future you say you want, because {number} responds to coherence more than intensity.",
            f"Treat the {pattern_detail['label']} in this number as a cue to refine your signal until thought, feeling, and action are moving together.",
        ]
    if intent == "health":
        return [
            f"Notice the body signal you have been normalizing, because {number} often arrives before depletion becomes harder to ignore.",
            f"Let {archetype['gift']} shape one supportive rhythm today around sleep, food, movement, breath, or screen boundaries.",
            f"Respond to the {pattern_detail['label']} of this number by making one calm, repeatable change instead of promising a dramatic overhaul.",
        ]
    if intent == "spiritual-growth":
        return [
            f"Take one spiritual insight you already know and practice it in behavior today, because {number} rewards embodiment over collection.",
            f"Use {archetype['gift']} to choose a quieter channel for guidance, whether that means prayer, study, meditation, or a more honest journal entry.",
            f"Let the {pattern_detail['label']} in this number show you where awareness needs repetition, pacing, or deeper trust before it becomes wisdom.",
        ]
    if intent == "family":
        return [
            f"Name the family pattern that keeps replaying, because {number} often appears when inherited roles need to be seen clearly.",
            f"Use {archetype['gift']} to steady the tone of one home conversation instead of trying to control the entire outcome.",
            f"Choose one repair action that fits the {pattern_detail['tempo']} of this pattern, whether that means apology, boundary, presence, or release.",
        ]
    if intent == "protection":
        return [
            f"Identify where your yes and no have become muddy, because {number} sharpens protection through discernment before anything else.",
            f"Let {archetype['gift']} guide one boundary decision around access, attention, oversharing, or energy leakage.",
            f"Use the {pattern_detail['label']} in this number to check what keeps repeating because the boundary is still being negotiated instead of held.",
        ]
    return [
        f"Name what is ending so the next chapter is not forced to carry old momentum into a new doorway.",
        f"Use {archetype['gift']} to prepare one cleaner starting condition today, especially where the current transition already needs {pattern_detail['tempo']}.",
        f"Treat {number} as a threshold marker and release one attachment that would make this beginning heavier than it needs to be.",
    ]


def build_intent_subtitle(number: str, intent: str, root: int) -> str:
    config = INTENT_CONFIG[intent]
    base = BASE_ARCHETYPES[root]
    if is_repeating(number):
        return f"a magnified message about {config['display'].lower()} and {base['gift']}"
    if is_ascending(number):
        return f"step-by-step guidance for {config['display'].lower()}"
    if is_mirrored(number):
        return f"a balance check for {config['display'].lower()}"
    return f"what this sequence is pointing out in {config['display'].lower()}"


def build_intent_teaser(number: str, intent: str, root: int) -> str:
    config = INTENT_CONFIG[intent]
    base = BASE_ARCHETYPES[root]
    return (
        f"{number} brings the root-{root} energy of {base['essence']} into {config['display'].lower()}, "
        f"highlighting {config['theme']}."
    )


def build_intent_affirmation(number: str, intent: str, root: int) -> str:
    config = INTENT_CONFIG[intent]
    base = BASE_ARCHETYPES[root]
    return (
        f"I welcome the guidance of {number} and allow {base['gift']} to shape my "
        f"{config['display'].lower()} journey."
    )


def build_intent_related_numbers(intent: str, number: str, root: int) -> list[str]:
    preferred = [candidate for candidate in INTENT_CONFIG[intent]["strong_numbers"] if candidate != number]
    family = [candidate for candidate in related_numbers(number, root) if candidate not in preferred]
    return (preferred + family)[:3]


def build_core_faq(number: str, root: int) -> list[dict[str, str]]:
    base = BASE_ARCHETYPES[root]
    return [
        {
            "q": f"What does angel number {number} mean?",
            "a": f"{number} points to {base['essence']}. Its message is usually about responding with {base['gift']} instead of staying stuck in hesitation.",
        },
        {
            "q": f"Why do I keep seeing {number} everywhere?",
            "a": f"Repeating contact with {number} usually shows up when one life lesson is trying to get your full attention. It is a cue to notice the pattern, the timing, and your emotional state in the moment.",
        },
        {
            "q": f"Is {number} a good sign?",
            "a": f"Yes. Even when {number} arrives during pressure, it is still a supportive sign because it helps you recognize the wiser response before the situation hardens.",
        },
        {
            "q": f"What should I do when I see {number}?",
            "a": f"Pause, ground yourself, and take one action that honors {base['gift']}. Angel numbers work best as prompts for aligned movement, not passive superstition.",
        },
        {
            "q": f"Which numbers are related to {number}?",
            "a": f"Numbers that reduce to {root} often carry a similar lesson. Neighboring sequences can also matter because they show how the message is evolving around you.",
        },
    ]


def build_intent_faq(number: str, intent: str, root: int) -> list[dict[str, str]]:
    config = INTENT_CONFIG[intent]
    base = BASE_ARCHETYPES[root]
    return [
        {
            "q": f"What does {number} mean for {config['display'].lower()}?",
            "a": f"In {config['display'].lower()}, {number} emphasizes {config['theme']}. The healthiest response is to meet that area with {base['gift']}.",
        },
        {
            "q": f"Is {number} a strong {intent.replace('-', ' ')} angel number?",
            "a": f"Yes. The root-{root} current naturally supports {config['display'].lower()} through {base['essence']}, which is why the sequence tends to feel personally relevant in this domain.",
        },
        {
            "q": f"What should I do after seeing {number} for {config['display'].lower()}?",
            "a": f"Use the sighting as a prompt to make one honest, grounded move. Angel number guidance becomes clearer when insight is paired with action.",
        },
        {
            "q": f"Does {number} promise an outcome in {config['display'].lower()}?",
            "a": f"No angel number bypasses free will. {number} is better understood as guidance about the energy available to you and the lesson asking for participation.",
        },
        {
            "q": f"Which other numbers support this same message?",
            "a": f"Sequences with a similar root number or intent emphasis often echo this lesson. Related numbers can show whether the message is deepening, widening, or preparing for closure.",
        },
    ]


def build_core_record(number: str) -> dict[str, object]:
    root = reduce_to_root(number)
    display = number
    headline = f"{display} Angel Number - Meaning, Message & What To Do"
    record = {
        "number": number,
        "display": display,
        "headline": headline,
        "summary": build_summary(number, root),
        "numerology_base": str(root),
        "key_themes": build_key_themes(number, root),
        "vibration": build_vibration(number, root),
        "seeing_it_means": build_seeing_it_means(number, root),
        "what_to_do": build_core_actions(number, root),
        "affirmation": build_core_affirmation(number, root),
        "meta_title": f"{display} Angel Number Meaning - Signs, Love, Career & More | EverydayHoroscope",
        "meta_description": (
            f"Seeing {display} everywhere? Discover the meaning of angel number {display} and what it signals for love, career, manifestation, and spiritual growth."
        ),
        "faq": build_core_faq(number, root),
        "related_numbers": related_numbers(number, root),
        "canonical_url": f"{SITE_URL}/angel-numbers/{display}",
        "tagline": number_label(number, root),
    }
    record["intent_summaries"] = [build_intent_summary(number, intent) for intent in INTENT_ORDER]
    return record


def build_intent_summary(number: str, intent: str) -> dict[str, object]:
    root = reduce_to_root(number)
    config = INTENT_CONFIG[intent]
    return {
        "intent": intent,
        "display_name": config["display"],
        "headline": f"{number} Angel Number {config['display']} - {build_intent_subtitle(number, intent, root).capitalize()}",
        "teaser": build_intent_teaser(number, intent, root),
        "url": f"/angel-numbers/{number}/{intent}",
    }


def build_intent_record(number: str, intent: str) -> dict[str, object]:
    root = reduce_to_root(number)
    config = INTENT_CONFIG[intent]
    template = build_intent_base_matrix()[intent][root]
    subtitle = build_intent_subtitle(number, intent, root)
    return {
        "number": number,
        "intent": intent,
        "display_name": config["display"],
        "headline": f"{number} Angel Number {config['display']} - {subtitle.capitalize()}",
        "subtitle": subtitle,
        "opening": (
            f"{number} often appears when {config['display'].lower()} needs a clearer rhythm. "
            f"{template['opening']}"
        ),
        "message": build_intent_message(number, intent, root),
        "action_steps": build_intent_action_steps(number, intent, root),
        "affirmation": build_intent_affirmation(number, intent, root),
        "faq": build_intent_faq(number, intent, root),
        "related_numbers": build_intent_related_numbers(intent, number, root),
        "meta_title": f"{number} Angel Number {config['display']} Meaning | EverydayHoroscope",
        "meta_description": (
            f"Discover what angel number {number} means for {config['display'].lower()}. "
            f"Read the message, action steps, affirmation, and related signs."
        ),
        "canonical_url": f"{SITE_URL}/angel-numbers/{number}/{intent}",
        "all_intents": [{"slug": slug, "display_name": INTENT_CONFIG[slug]["display"]} for slug in INTENT_ORDER],
    }


def build_hub_intro() -> str:
    return (
        "Angel numbers are repeating or symbolically charged number sequences that many people notice during turning points, decisions, and seasons of growth. "
        "This hub brings together 1,000 angel number meanings, from the classic repeating patterns to deeper mirrored and sequence-based codes. "
        "Each number can also be explored through nine life intents so the message feels practical, not abstract. "
        "Use the search, popular numbers grid, and numerology families below to follow the number that keeps finding you."
    )


@lru_cache(maxsize=1)
def build_hub_payload() -> dict[str, object]:
    popular_numbers = [
        {"number": "111", "display": "111", "theme": "Manifestation gate"},
        {"number": "222", "display": "222", "theme": "Trust the timing"},
        {"number": "333", "display": "333", "theme": "Creative support"},
        {"number": "444", "display": "444", "theme": "Protected and grounded"},
        {"number": "555", "display": "555", "theme": "Change is here"},
        {"number": "666", "display": "666", "theme": "Return to balance"},
        {"number": "777", "display": "777", "theme": "Awakening signal"},
        {"number": "888", "display": "888", "theme": "Abundance current"},
        {"number": "999", "display": "999", "theme": "Cycle closing"},
        {"number": "1111", "display": "1111", "theme": "Portal energy"},
        {"number": "1212", "display": "1212", "theme": "Aligned progress"},
        {"number": "2222", "display": "2222", "theme": "Master partnership"},
        {"number": "3333", "display": "3333", "theme": "Expansion chorus"},
        {"number": "4444", "display": "4444", "theme": "Guardian support"},
        {"number": "5555", "display": "5555", "theme": "Destiny pivot"},
        {"number": "6666", "display": "6666", "theme": "Healing the home"},
        {"number": "7777", "display": "7777", "theme": "Mystic confirmation"},
        {"number": "8888", "display": "8888", "theme": "Legacy abundance"},
        {"number": "9999", "display": "9999", "theme": "Final release"},
        {"number": "1000", "display": "000", "theme": "Zero-point reset"},
    ]

    families = []
    for root in range(1, 10):
        members = number_family_members(root)
        families.append(
            {
                "root": root,
                "label": f"Base {root} - {BASE_ARCHETYPES[root]['label']}",
                "theme": BASE_ARCHETYPES[root]["essence"],
                "numbers": members,
                "preview": members[:18],
            }
        )

    faq = [
        {
            "q": "What are angel numbers?",
            "a": "Angel numbers are number patterns people interpret as meaningful timing cues or spiritual nudges. They are less about superstition and more about noticing where life is asking for awareness.",
        },
        {
            "q": "Do angel numbers have different meanings in love and career?",
            "a": "Yes. The same number can point to different applications depending on the area of life in focus, which is why this module includes intent-specific pages for each core number.",
        },
        {
            "q": "How do I find my angel number meaning fast?",
            "a": "Use the search bar if you already know the sequence, or browse popular numbers and numerology families if you want to understand the wider pattern behind it.",
        },
        {
            "q": "What is a numerology root?",
            "a": "A numerology root is the single-digit sum of a number. It helps group numbers into energetic families so patterns like 111, 444, and 777 can be understood at both the sequence and base-vibration level.",
        },
        {
            "q": "Should I act every time I see an angel number?",
            "a": "You do not need to overreact to every sighting. The healthiest approach is to notice the repeating context, reflect honestly, and then take one grounded action if the message feels relevant.",
        },
    ]

    return {
        "headline": "Angel Numbers - Meanings, Messages & What They Mean for You",
        "intro": build_hub_intro(),
        "popular_numbers": popular_numbers,
        "intent_categories": [
            {
                "slug": slug,
                "display_name": config["display"],
                "theme": config["theme"],
                "strong_numbers": config["strong_numbers"],
            }
            for slug, config in INTENT_CONFIG.items()
        ],
        "numerology_families": families,
        "how_to_work_with_angel_numbers": [
            "Notice the exact number, the time, and the life situation around the sighting.",
            "Read both the core meaning and the intent page that matches your current concern.",
            "Look for the practical invitation in the message rather than treating it like a fixed prediction.",
            "Repeat the affirmation and follow through with one concrete action the same day.",
        ],
        "faq": faq,
        "counts": {"core_numbers": 1000, "intent_pages": 9000, "total_pages": 10001},
    }


def get_core_record(number: str) -> dict[str, object]:
    return build_core_record(number)


def get_intent_record(number: str, intent: str) -> dict[str, object]:
    return build_intent_record(number, intent)


def iter_core_records() -> list[dict[str, object]]:
    return [get_core_record(number) for number in get_core_numbers()]


def iter_intent_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for number in get_core_numbers():
        for intent in INTENT_ORDER:
            records.append(get_intent_record(number, intent))
    return records


def build_sitemap_paths() -> list[str]:
    paths = ["/angel-numbers"]
    for number in get_core_numbers():
        paths.append(f"/angel-numbers/{number}")
        for intent in INTENT_ORDER:
            paths.append(f"/angel-numbers/{number}/{intent}")
    return paths


def sitemap_page_count() -> int:
    return ceil(len(build_sitemap_paths()) / PAGE_SIZE)


def get_sitemap_page(page: int) -> dict[str, object]:
    paths = build_sitemap_paths()
    page_count = sitemap_page_count()
    if page < 1 or page > page_count:
        raise ValueError(f"page must be between 1 and {page_count}")
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    return {
        "page": page,
        "page_count": page_count,
        "urls": [f"{SITE_URL}{path}" for path in paths[start:end]],
    }
