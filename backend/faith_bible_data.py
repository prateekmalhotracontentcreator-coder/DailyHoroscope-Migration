from __future__ import annotations

import json
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from zoneinfo import ZoneInfo

from faith_gita_data import GITA_SITUATIONS


SITE_URL = "https://www.everydayhoroscope.in"
INDIA_TZ = ZoneInfo("Asia/Kolkata")
BIBLE_SOURCE_ASSET_PATH = Path(__file__).resolve().parent / "assets" / "faith" / "bible_promises_source.json"
SUPPORTING_REFS_ASSET_PATH = Path(__file__).resolve().parent / "assets" / "faith" / "bible_supporting_references.json"
BIBLE_MEANINGS_ASSET_PATH = Path(__file__).resolve().parent / "assets" / "faith" / "bible_meanings_lexicon.json"
GITA_ASSET_PATH = Path(__file__).resolve().parent / "assets" / "faith" / "gita_verses.json"


def _hash_index(*values: str, modulus: int) -> int:
    total = 0
    for value in values:
        for char in value:
            total += ord(char)
    return total % modulus


def _title_case_slug(value: str) -> str:
    return " ".join(part.capitalize() for part in value.split("-"))


def _slugify(value: str) -> str:
    return "-".join(part for part in "".join(char.lower() if char.isalnum() else "-" for char in value).split("-") if part)


def _today_iso() -> str:
    return datetime.now(INDIA_TZ).date().isoformat()


TOPIC_GROUPS = [
    {
        "default_source_slug": "worry",
        "term": "merimna",
        "term_note": "anxious care that keeps splitting attention into too many imagined futures",
        "items": [
            ("anxiety", "Anxiety", "steadying a mind that keeps running ahead of the present moment"),
            ("worry", "Worry", "interrupting low-grade fear before it becomes a ruling habit"),
            ("panic", "Panic", "bringing breathing space back into a body that feels cornered"),
            ("overwhelm", "Overwhelm", "restoring proportion when too many demands are landing at once"),
            ("calm", "Calm", "teaching the heart to settle without pretending nothing hurts"),
            ("sound-mind", "Sound Mind", "recovering composure and disciplined thought under pressure"),
            ("stress", "Stress", "reducing the inner strain caused by unrelenting mental load"),
            ("mental-clarity", "Mental Clarity", "bringing clean thought back when nervousness has become fog"),
            ("emotional-safety", "Emotional Safety", "helping the reader feel held enough to think honestly again"),
            ("inner-rest", "Inner Rest", "moving from agitation into steadier inward stillness"),
        ],
    },
    {
        "default_source_slug": "fear",
        "term": "chazaq",
        "term_note": "strengthened courage that stays upright even when the surrounding facts are hard",
        "items": [
            ("fear", "Fear", "meeting threats without letting dread define the whole atmosphere"),
            ("courage", "Courage", "choosing faithful action while the outcome is still unclear"),
            ("protection", "Protection", "remembering that divine care does not disappear in exposed seasons"),
            ("deliverance", "Deliverance", "holding space for rescue without becoming passive"),
            ("confidence", "Confidence", "recovering holy steadiness after intimidation or repeated setbacks"),
            ("assurance", "Assurance", "grounding the heart when it keeps second-guessing every step"),
            ("boldness", "Boldness", "finding clean speech and action when fear has narrowed the voice"),
            ("refuge", "Refuge", "turning toward shelter instead of living in constant bracing"),
            ("uncertain-future", "Uncertain Future", "facing what is unknown without handing it all to dread"),
            ("crisis-faith", "Crisis Faith", "keeping trust alive when circumstances have become acute"),
        ],
    },
    {
        "default_source_slug": "hope",
        "term": "elpis",
        "term_note": "confident expectation rooted in God's character rather than in a fast emotional lift",
        "items": [
            ("hope", "Hope", "keeping expectation alive when the story still feels unfinished"),
            ("patience", "Patience", "remaining open and steady while outcomes take longer than hoped"),
            ("perseverance", "Perseverance", "staying in the work of faith past the first wave of fatigue"),
            ("waiting", "Waiting", "honoring delay without calling delay abandonment"),
            ("pressing-on", "Pressing On", "continuing after disappointment without pretending the loss was small"),
            ("endurance", "Endurance", "lasting through a long season without emotional collapse"),
            ("restoration", "Restoration", "trusting that repair can happen even after real damage"),
            ("renewal", "Renewal", "receiving fresh strength when inner resources feel depleted"),
            ("resilience", "Resilience", "bending without breaking under repeated strain"),
            ("not-giving-up", "Not Giving Up", "resisting the temptation to quit simply because it is taking time"),
        ],
    },
    {
        "default_source_slug": "guidance",
        "term": "hokmah",
        "term_note": "wisdom that teaches fitting action, not just abstract information",
        "items": [
            ("guidance", "Guidance", "seeking direction when the next step is not obvious"),
            ("wisdom", "Wisdom", "learning how to act well in situations that are emotionally noisy"),
            ("purpose", "Purpose", "recovering meaning when ordinary effort feels disconnected"),
            ("identity", "Identity", "remembering who you are when roles have shifted or blurred"),
            ("discernment", "Discernment", "separating what is true from what is only loud"),
            ("direction", "Direction", "moving from confusion into a more trustworthy path"),
            ("calling", "Calling", "listening for vocation beneath pressure and comparison"),
            ("decision-making", "Decision Making", "making a clean choice without worshiping certainty"),
            ("clarity", "Clarity", "bringing focus back when competing voices have multiplied"),
            ("obedience", "Obedience", "responding faithfully to what has already become clear"),
        ],
    },
    {
        "default_source_slug": "financial-need",
        "term": "daily-bread",
        "term_note": "God's provision understood as enough for faithful obedience, not permission for excess",
        "items": [
            ("provision", "Provision", "trusting God for real needs without shrinking from responsibility"),
            ("prosperity", "Prosperity", "reframing blessing as stewardship instead of vanity"),
            ("financial-pressure", "Financial Pressure", "bringing steadiness into seasons marked by money strain"),
            ("debt", "Debt", "facing obligation honestly without surrendering to shame"),
            ("work", "Work", "asking for both livelihood and integrity in the labor itself"),
            ("stewardship", "Stewardship", "ordering resources in a way that reflects trust and wisdom"),
            ("open-doors", "Open Doors", "recognizing opportunity without confusing it with impulse"),
            ("daily-bread", "Daily Bread", "receiving enough for today while larger answers unfold"),
            ("generosity", "Generosity", "staying open-handed even when resources need careful handling"),
            ("gods-providence", "God's Providence", "seeing care and timing working beneath visible uncertainty"),
        ],
    },
    {
        "default_source_slug": "forgiveness",
        "term": "hesed",
        "term_note": "steadfast covenant mercy that keeps moving toward repair rather than toward scorekeeping",
        "items": [
            ("forgiveness", "Forgiveness", "loosening the grip of offense without calling evil good"),
            ("grace", "Grace", "receiving unearned help when self-effort has run out"),
            ("mercy", "Mercy", "meeting failure with compassion serious enough to heal it"),
            ("redemption", "Redemption", "believing that even damaged stories can be reworked"),
            ("reconciliation", "Reconciliation", "pursuing repair where trust can responsibly be rebuilt"),
            ("guilt", "Guilt", "coming into honest confession without staying trapped in accusation"),
            ("shame", "Shame", "refusing the lie that failure has become your permanent identity"),
            ("cleansing", "Cleansing", "letting grace wash what self-punishment never can"),
            ("second-chances", "Second Chances", "opening to a new faithful path after collapse or regret"),
            ("repentance", "Repentance", "turning fully instead of bargaining around what needs change"),
        ],
    },
    {
        "default_source_slug": "peace",
        "term": "shalom",
        "term_note": "peace as wholeness, settledness, and rightly ordered life rather than mere quiet feelings",
        "items": [
            ("peace", "Peace", "receiving inner steadiness when life is outwardly unsettled"),
            ("comfort", "Comfort", "meeting pain with nearness instead of polished spiritual slogans"),
            ("rest", "Rest", "allowing the soul to stop living in continuous emergency mode"),
            ("loneliness", "Loneliness", "bringing companionship into seasons of emotional isolation"),
            ("sleeplessness", "Sleeplessness", "quieting the night mind when it refuses to release the day"),
            ("grief-comfort", "Grief Comfort", "finding gentle presence when sorrow has become ambient"),
            ("contentment", "Contentment", "receiving enoughness without needing life to be perfect first"),
            ("quietness", "Quietness", "making room for silence that restores instead of threatens"),
            ("security", "Security", "settling the heart in something stronger than circumstance"),
            ("safe-harbor", "Safe Harbor", "finding a place of emotional shelter in unstable seasons"),
        ],
    },
    {
        "default_source_slug": "suffering",
        "term": "dunamis",
        "term_note": "strength that arrives from God and can hold weakness without denial",
        "items": [
            ("healing", "Healing", "bringing restoration where the body, mind, or spirit has been wounded"),
            ("strength", "Strength", "receiving power for the next faithful step when your own feels thin"),
            ("recovery", "Recovery", "walking a slow path of repair with honesty and hope"),
            ("illness", "Illness", "holding physical vulnerability inside a larger story of care"),
            ("suffering", "Suffering", "finding companionship with God in pain that has not yet lifted"),
            ("trials", "Trials", "letting hardship mature trust rather than hollow it out"),
            ("trouble", "Trouble", "meeting disruptive seasons without spiritual panic"),
            ("weariness", "Weariness", "being sustained when tiredness has reached the soul"),
            ("backslider-healing", "Backslider Healing", "returning after spiritual drift without self-protection"),
            ("weakness", "Weakness", "allowing limitation to become a place of grace rather than embarrassment"),
        ],
    },
    {
        "default_source_slug": "marriage",
        "term": "agape",
        "term_note": "covenant love that seeks faithfulness, repair, and the good of another with maturity",
        "items": [
            ("marriage", "Marriage", "strengthening covenant love through truth and devotion"),
            ("relationships", "Relationships", "healing attachment patterns without abandoning discernment"),
            ("family", "Family", "bringing grace and stability into the home system itself"),
            ("parenting", "Parenting", "leading children with both tenderness and steadiness"),
            ("friendship", "Friendship", "building trustworthy companionship rather than shallow contact"),
            ("unity", "Unity", "pursuing peace without suppressing what must still be said"),
            ("estrangement-healing", "Estrangement Healing", "opening to repair where connection has gone cold"),
            ("prodigal-child", "Prodigal Child", "praying with hope when someone you love has wandered far"),
            ("singleness", "Singleness", "living whole-heartedly without treating this season as less than"),
            ("covenant-love", "Covenant Love", "anchoring affection in endurance rather than in volatility"),
        ],
    },
    {
        "default_source_slug": "faith",
        "term": "pistis",
        "term_note": "trusting reliance that expresses itself through prayer, seeking, and abiding action",
        "items": [
            ("faith", "Faith", "believing God in a way that changes how you move today"),
            ("trust", "Trust", "relying on God's character when your own certainty is low"),
            ("prayer", "Prayer", "bringing specific need before God instead of only rehearsing it internally"),
            ("answered-prayer", "Answered Prayer", "holding expectation without turning prayer into control"),
            ("seeking-god", "Seeking God", "returning desire and attention toward God in a focused way"),
            ("holy-spirit", "Holy Spirit", "welcoming divine help, conviction, and comfort in the present tense"),
            ("fruitfulness", "Fruitfulness", "abiding deeply enough that life begins to bear real evidence"),
            ("worship", "Worship", "reordering the heart around adoration instead of anxiety"),
            ("revival", "Revival", "asking for renewal that becomes visible in holy response"),
            ("abiding", "Abiding", "remaining connected to God when attention wants to scatter"),
        ],
    },
    {
        "default_source_slug": "salvation",
        "term": "hagios",
        "term_note": "holy set-apart life that grows from grace rather than from fear-driven performance",
        "items": [
            ("salvation", "Salvation", "resting in rescue that comes from God and not from self-merit"),
            ("freedom-from-sin", "Freedom from Sin", "believing that entrenched patterns do not have final ownership"),
            ("temptation", "Temptation", "resisting the pull that looks urgent but corrodes the soul"),
            ("holiness", "Holiness", "choosing consecration in ordinary habits and decisions"),
            ("purity", "Purity", "guarding the inner life rather than merely polishing the image"),
            ("self-control", "Self Control", "creating boundaries strong enough to protect what matters"),
            ("righteousness", "Righteousness", "walking in what is right even when compromise is easier"),
            ("discipleship", "Discipleship", "following Christ with practices that shape real loyalty"),
            ("transformation", "Transformation", "letting character be changed rather than merely managed"),
            ("spiritual-war", "Spiritual War", "recognizing that some battles are won by vigilance and truth"),
        ],
    },
    {
        "default_source_slug": "joy",
        "term": "chara",
        "term_note": "deep gladness that can coexist with difficulty because it is rooted in God, not in ease",
        "items": [
            ("joy", "Joy", "receiving delight that survives beyond immediate circumstances"),
            ("gratitude", "Gratitude", "learning to notice grace before the whole situation resolves"),
            ("celebration", "Celebration", "responding to goodness with visible thanksgiving"),
            ("praise", "Praise", "retraining the heart to lift its attention toward God"),
            ("thanksgiving", "Thanksgiving", "naming gifts clearly instead of rushing past them"),
            ("breakthrough", "Breakthrough", "asking for decisive movement without abandoning patient trust"),
            ("my-god-is-able", "My God Is Able", "bringing impossible situations under the language of divine capability"),
            ("impossible-situations", "Impossible Situations", "remembering that God's reach exceeds your visible options"),
            ("promise-keeping", "Promise Keeping", "leaning on God's faithfulness when waiting has become long"),
            ("confidence-in-god", "Confidence in God", "placing confidence in the One who can carry what you cannot"),
        ],
    },
]


def _build_topics() -> list[dict]:
    topics: list[dict] = []
    for group in TOPIC_GROUPS:
        for item in group["items"]:
            slug, label, promise_angle = item
            topics.append(
                {
                    "slug": slug,
                    "label": label,
                    "source_slug": group["default_source_slug"],
                    "promise_angle": promise_angle,
                    "term": group["term"],
                    "term_note": group["term_note"],
                }
            )
    if len(topics) != 120:
        raise ValueError(f"Expected 120 Bible topics, found {len(topics)}")
    return topics


BIBLE_TOPICS = _build_topics()
TOPIC_INDEX = {item["slug"]: item for item in BIBLE_TOPICS}
TOPIC_ORDINAL = {item["slug"]: index for index, item in enumerate(BIBLE_TOPICS)}

SOURCE_SUPPORT_TOPIC_MAP = {
    "worry": ["Anxiety", "Comfort", "Peace", "Uncertainty"],
    "fear": ["Fear", "Protection", "Comfort", "Anxiety"],
    "hope": ["Encouragement", "Discouragement", "Strength", "Uncertainty"],
    "guidance": ["Guidance", "Confusion", "Doubt"],
    "financial-need": ["Care", "Need", "Provision", "Blessings"],
    "forgiveness": ["Forgiveness", "Guilt", "Shame"],
    "peace": ["Peace", "Comfort", "Anxiety"],
    "suffering": ["Sickness", "Suffering", "Weakness", "Strength", "Grief"],
    "marriage": ["Family", "Love", "Forgiveness", "Comfort"],
    "faith": ["Prayer", "Guidance", "Doubt", "Encouragement"],
    "salvation": ["Salvation", "Temptation", "Obedience", "Discipline", "Holiness"],
    "joy": ["Joy", "Praise", "Encouragement", "Blessings"],
}

SOURCE_PRIMARY_BUCKET_MAP = {
    "worry": ["worry", "trouble", "the-promises-of-god"],
    "fear": ["fear", "confidence", "assurance", "the-promises-of-god"],
    "hope": ["hope", "perseverance", "pressing-on", "waiting-on-god"],
    "guidance": ["guidance", "wisdom", "the-promises-of-god"],
    "financial-need": ["financial-need", "providence", "the-promises-of-god"],
    "forgiveness": ["forgiveness", "reconciliation", "the-promises-of-god"],
    "peace": ["peace", "weariness", "the-promises-of-god"],
    "suffering": ["suffering", "trials", "trouble", "weariness"],
    "marriage": ["marriage", "reconciliation", "the-promises-of-god"],
    "faith": ["faith", "answered-prayer", "seeking-god", "the-holy-spirit"],
    "salvation": ["salvation", "victory-over-sin", "the-holy-spirit"],
    "joy": ["joy", "hope", "the-promises-of-god"],
}

SOURCE_MEANING_TAG_MAP = {
    "worry": ["rest", "shepherd", "water"],
    "fear": ["fortress", "deliverance", "light"],
    "hope": ["covenant", "light", "path"],
    "guidance": ["path", "light", "wilderness"],
    "financial-need": ["bread", "shepherd", "water"],
    "forgiveness": ["covenant", "water", "temple"],
    "peace": ["rest", "water", "shepherd"],
    "suffering": ["wilderness", "water", "deliverance"],
    "marriage": ["covenant", "temple", "water"],
    "faith": ["light", "path", "temple"],
    "salvation": ["deliverance", "covenant", "light"],
    "joy": ["light", "bread", "water"],
}

TRANSITIONS = [
    {
        "slug": "divorce",
        "label": "Divorce",
        "core_pain": "divides home, memory, finances, and identity at the same time",
        "faith_need": "grace for truth-telling without becoming consumed by retaliation",
        "practice": "keep decisions slow, documented, and emotionally clean",
        "transit_slug": "venus-retrograde",
        "transit_label": "Venus Retrograde",
        "sign_slug": "libra",
        "chart_point": "venus",
        "house": "7th-house",
        "gita_situation_slug": "divorce",
    },
    {
        "slug": "job-loss",
        "label": "Job Loss",
        "core_pain": "shakes security and can make self-worth feel suddenly negotiable",
        "faith_need": "provision without panic and work without humiliation",
        "practice": "keep structure, applications, and support conversations alive",
        "transit_slug": "saturn-in-capricorn",
        "transit_label": "Saturn in Capricorn",
        "sign_slug": "capricorn",
        "chart_point": "saturn",
        "house": "10th-house",
        "gita_situation_slug": "career-failure",
    },
    {
        "slug": "grief",
        "label": "Grief",
        "core_pain": "changes the shape of daily life long before the heart can explain it",
        "faith_need": "comfort that can hold sorrow without rushing it",
        "practice": "build simple rituals of remembrance and support",
        "transit_slug": "saturn-retrograde",
        "transit_label": "Saturn Retrograde",
        "sign_slug": "scorpio",
        "chart_point": "moon",
        "house": "8th-house",
        "gita_situation_slug": "grief-and-loss",
    },
    {
        "slug": "new-city",
        "label": "New City",
        "core_pain": "unsettles belonging, routine, and familiar support all at once",
        "faith_need": "guidance while everything still feels provisional",
        "practice": "create one stabilizing rhythm before chasing full certainty",
        "transit_slug": "sun-in-aries",
        "transit_label": "Sun in Aries",
        "sign_slug": "aries",
        "chart_point": "sun",
        "house": "4th-house",
        "gita_situation_slug": "new-beginning",
    },
    {
        "slug": "illness",
        "label": "Illness",
        "core_pain": "puts the body at the center of every plan and emotion",
        "faith_need": "steady hope that can coexist with medical reality",
        "practice": "follow care faithfully and ask for concrete help",
        "transit_slug": "mars-in-virgo",
        "transit_label": "Mars in Virgo",
        "sign_slug": "virgo",
        "chart_point": "mars",
        "house": "6th-house",
        "gita_situation_slug": "health-crisis",
    },
    {
        "slug": "retirement",
        "label": "Retirement",
        "core_pain": "can blur identity after years of being anchored by role and schedule",
        "faith_need": "renewed purpose beyond productivity alone",
        "practice": "design a weekly rhythm around service, rest, and meaning",
        "transit_slug": "jupiter-in-taurus",
        "transit_label": "Jupiter in Taurus",
        "sign_slug": "taurus",
        "chart_point": "jupiter",
        "house": "2nd-house",
        "gita_situation_slug": "identity-crisis",
    },
    {
        "slug": "new-baby",
        "label": "New Baby",
        "core_pain": "brings joy and exhaustion in the same breath",
        "faith_need": "strength for caregiving and peace inside disrupted routines",
        "practice": "receive help early and protect simple spiritual anchors",
        "transit_slug": "jupiter-in-cancer",
        "transit_label": "Jupiter in Cancer",
        "sign_slug": "cancer",
        "chart_point": "moon",
        "house": "5th-house",
        "gita_situation_slug": "parenting-challenges",
    },
    {
        "slug": "financial-crisis",
        "label": "Financial Crisis",
        "core_pain": "compresses options and can make tomorrow feel threatening",
        "faith_need": "provision with sober stewardship and courage",
        "practice": "clarify the numbers and reduce confusion before guessing",
        "transit_slug": "jupiter-in-taurus",
        "transit_label": "Jupiter in Taurus",
        "sign_slug": "taurus",
        "chart_point": "jupiter",
        "house": "2nd-house",
        "gita_situation_slug": "financial-pressure",
    },
    {
        "slug": "relationship-end",
        "label": "Relationship End",
        "core_pain": "leaves the future emotionally uninhabitable for a while",
        "faith_need": "healing strong enough to tell the truth and still stay soft-hearted",
        "practice": "name what ended and stop bargaining with mixed signals",
        "transit_slug": "venus-in-libra",
        "transit_label": "Venus in Libra",
        "sign_slug": "libra",
        "chart_point": "venus",
        "house": "7th-house",
        "gita_situation_slug": "relationship-breakdown",
    },
    {
        "slug": "starting-over",
        "label": "Starting Over",
        "core_pain": "asks for courage before a new structure has proven itself",
        "faith_need": "fresh hope with disciplined first steps",
        "practice": "build the first faithful routine before chasing scale",
        "transit_slug": "sun-in-aries",
        "transit_label": "Sun in Aries",
        "sign_slug": "aries",
        "chart_point": "sun",
        "house": "1st-house",
        "gita_situation_slug": "new-beginning",
    },
    {
        "slug": "addiction-recovery",
        "label": "Addiction Recovery",
        "core_pain": "forces honesty about both craving and the cost of secrecy",
        "faith_need": "grace that strengthens accountability instead of excusing relapse",
        "practice": "keep confession, support, and structure close together",
        "transit_slug": "mars-retrograde",
        "transit_label": "Mars Retrograde",
        "sign_slug": "scorpio",
        "chart_point": "mars",
        "house": "8th-house",
        "gita_situation_slug": "betrayal",
    },
    {
        "slug": "empty-nest",
        "label": "Empty Nest",
        "core_pain": "reshapes the home and exposes quiet spaces that used to stay full",
        "faith_need": "comfort with a renewed sense of purpose",
        "practice": "honor grief while rebuilding identity beyond constant caregiving",
        "transit_slug": "jupiter-in-cancer",
        "transit_label": "Jupiter in Cancer",
        "sign_slug": "cancer",
        "chart_point": "moon",
        "house": "4th-house",
        "gita_situation_slug": "loneliness",
    },
    {
        "slug": "career-change",
        "label": "Career Change",
        "core_pain": "creates tension between security, calling, and timing",
        "faith_need": "direction that is brave without being impulsive",
        "practice": "test the new path with structured next steps",
        "transit_slug": "mercury-in-virgo",
        "transit_label": "Mercury in Virgo",
        "sign_slug": "virgo",
        "chart_point": "mercury",
        "house": "10th-house",
        "gita_situation_slug": "major-decision",
    },
    {
        "slug": "marriage",
        "label": "Marriage",
        "core_pain": "raises the stakes of love, communication, and covenant responsibility",
        "faith_need": "wisdom that keeps romance grounded in mature devotion",
        "practice": "build habits of truth, prayer, and repair before tension spikes",
        "transit_slug": "venus-in-libra",
        "transit_label": "Venus in Libra",
        "sign_slug": "libra",
        "chart_point": "venus",
        "house": "7th-house",
        "gita_situation_slug": "relationship-breakdown",
    },
    {
        "slug": "pregnancy-loss",
        "label": "Pregnancy Loss",
        "core_pain": "creates grief that is intimate, bodily, and often hard to explain outwardly",
        "faith_need": "tender comfort that does not minimize the ache",
        "practice": "mark the loss, receive support, and let sorrow be named",
        "transit_slug": "saturn-in-pisces",
        "transit_label": "Saturn in Pisces",
        "sign_slug": "pisces",
        "chart_point": "moon",
        "house": "5th-house",
        "gita_situation_slug": "grief-and-loss",
    },
    {
        "slug": "aging-parent",
        "label": "Aging Parent",
        "core_pain": "mixes love, duty, anticipatory grief, and practical fatigue",
        "faith_need": "strength for care that does not harden into resentment",
        "practice": "share the load and name limits before burnout sets in",
        "transit_slug": "saturn-in-capricorn",
        "transit_label": "Saturn in Capricorn",
        "sign_slug": "capricorn",
        "chart_point": "saturn",
        "house": "4th-house",
        "gita_situation_slug": "parenting-challenges",
    },
    {
        "slug": "graduation",
        "label": "Graduation",
        "core_pain": "closes one chapter before the next has become secure",
        "faith_need": "purpose and courage for the threshold that follows achievement",
        "practice": "turn celebration into a clean first plan",
        "transit_slug": "sun-in-aries",
        "transit_label": "Sun in Aries",
        "sign_slug": "aries",
        "chart_point": "sun",
        "house": "9th-house",
        "gita_situation_slug": "new-beginning",
    },
    {
        "slug": "immigration",
        "label": "Immigration",
        "core_pain": "pulls identity, belonging, paperwork, and longing into one demanding season",
        "faith_need": "protection and endurance in a long bureaucratic threshold",
        "practice": "keep documents, support, and emotional care aligned",
        "transit_slug": "mercury-retrograde",
        "transit_label": "Mercury Retrograde",
        "sign_slug": "gemini",
        "chart_point": "mercury",
        "house": "9th-house",
        "gita_situation_slug": "major-decision",
    },
    {
        "slug": "business-failure",
        "label": "Business Failure",
        "core_pain": "makes public effort and private responsibility collapse into the same wound",
        "faith_need": "redemption that speaks to both loss and next steps",
        "practice": "review the numbers, tell the truth, and rebuild smaller",
        "transit_slug": "saturn-in-capricorn",
        "transit_label": "Saturn in Capricorn",
        "sign_slug": "capricorn",
        "chart_point": "saturn",
        "house": "10th-house",
        "gita_situation_slug": "career-failure",
    },
    {
        "slug": "natural-disaster",
        "label": "Natural Disaster",
        "core_pain": "can destroy stability so suddenly that the nervous system stays in survival mode",
        "faith_need": "shelter, provision, and collective courage",
        "practice": "prioritize safety, community, and small controllable actions",
        "transit_slug": "eclipse-season",
        "transit_label": "Eclipse Season",
        "sign_slug": "cancer",
        "chart_point": "moon",
        "house": "4th-house",
        "gita_situation_slug": "anxiety",
    },
    {
        "slug": "chronic-illness",
        "label": "Chronic Illness",
        "core_pain": "stretches vulnerability across months or years instead of one acute event",
        "faith_need": "endurance, honest lament, and practical hope",
        "practice": "pace life around reality rather than around shame",
        "transit_slug": "saturn-in-pisces",
        "transit_label": "Saturn in Pisces",
        "sign_slug": "pisces",
        "chart_point": "saturn",
        "house": "6th-house",
        "gita_situation_slug": "health-crisis",
    },
    {
        "slug": "mental-health-crisis",
        "label": "Mental Health Crisis",
        "core_pain": "can make the mind feel unsafe to inhabit",
        "faith_need": "mercy, treatment, and a steadier internal atmosphere",
        "practice": "seek clinical care and spiritual support together",
        "transit_slug": "mercury-retrograde",
        "transit_label": "Mercury Retrograde",
        "sign_slug": "gemini",
        "chart_point": "mercury",
        "house": "1st-house",
        "gita_situation_slug": "anxiety",
    },
    {
        "slug": "estrangement",
        "label": "Estrangement",
        "core_pain": "creates relational distance that is both grief and unresolved story",
        "faith_need": "wisdom for boundaries and openness without fantasy",
        "practice": "grieve what is gone and repair only what is honest to repair",
        "transit_slug": "saturn-in-aquarius",
        "transit_label": "Saturn in Aquarius",
        "sign_slug": "aquarius",
        "chart_point": "saturn",
        "house": "11th-house",
        "gita_situation_slug": "betrayal",
    },
    {
        "slug": "betrayal-by-friend",
        "label": "Betrayal by Friend",
        "core_pain": "breaks trust in a place that once felt relationally safe",
        "faith_need": "discernment that protects the heart without freezing it",
        "practice": "slow trust down and stop excusing what was false",
        "transit_slug": "eclipse-season",
        "transit_label": "Eclipse Season",
        "sign_slug": "scorpio",
        "chart_point": "moon",
        "house": "11th-house",
        "gita_situation_slug": "betrayal",
    },
    {
        "slug": "major-surgery",
        "label": "Major Surgery",
        "core_pain": "asks the body and mind to move through fear, waiting, and recovery together",
        "faith_need": "peace for the threshold and strength for healing afterward",
        "practice": "let others carry logistics while you conserve emotional energy",
        "transit_slug": "mars-in-virgo",
        "transit_label": "Mars in Virgo",
        "sign_slug": "virgo",
        "chart_point": "mars",
        "house": "6th-house",
        "gita_situation_slug": "health-crisis",
    },
    {
        "slug": "infertility-journey",
        "label": "Infertility Journey",
        "core_pain": "can mix longing, disappointment, and physical strain month after month",
        "faith_need": "hope that does not erase grief and grief that does not kill hope",
        "practice": "protect the heart with truthful expectations and support",
        "transit_slug": "venus-retrograde",
        "transit_label": "Venus Retrograde",
        "sign_slug": "libra",
        "chart_point": "venus",
        "house": "5th-house",
        "gita_situation_slug": "grief-and-loss",
    },
    {
        "slug": "caregiving-burden",
        "label": "Caregiving Burden",
        "core_pain": "turns love into relentless responsibility without much margin",
        "faith_need": "strength that can serve without disappearing",
        "practice": "set real limits and keep receiving help",
        "transit_slug": "saturn-in-capricorn",
        "transit_label": "Saturn in Capricorn",
        "sign_slug": "capricorn",
        "chart_point": "saturn",
        "house": "6th-house",
        "gita_situation_slug": "parenting-challenges",
    },
    {
        "slug": "burnout",
        "label": "Burnout",
        "core_pain": "makes even meaningful work feel emotionally unsustainable",
        "faith_need": "rest, limits, and clarity about what is not yours to carry",
        "practice": "reduce the load before demanding more willpower",
        "transit_slug": "saturn-in-capricorn",
        "transit_label": "Saturn in Capricorn",
        "sign_slug": "capricorn",
        "chart_point": "saturn",
        "house": "10th-house",
        "gita_situation_slug": "depression",
    },
    {
        "slug": "court-case",
        "label": "Court Case",
        "core_pain": "keeps life suspended inside evidence, waiting, and outcomes you cannot fully control",
        "faith_need": "wisdom and clean conscience under pressure",
        "practice": "stay factual, prepared, and emotionally measured",
        "transit_slug": "mercury-in-virgo",
        "transit_label": "Mercury in Virgo",
        "sign_slug": "virgo",
        "chart_point": "mercury",
        "house": "7th-house",
        "gita_situation_slug": "major-decision",
    },
    {
        "slug": "relocation",
        "label": "Relocation",
        "core_pain": "disrupts habit, belonging, and orientation even when the move is chosen",
        "faith_need": "peace in transition and guidance for new footing",
        "practice": "rebuild the basics before demanding deep certainty",
        "transit_slug": "sun-in-aries",
        "transit_label": "Sun in Aries",
        "sign_slug": "aries",
        "chart_point": "sun",
        "house": "4th-house",
        "gita_situation_slug": "new-beginning",
    },
    {
        "slug": "unemployment",
        "label": "Unemployment",
        "core_pain": "can slowly erode morale when days lose visible direction",
        "faith_need": "hope with enough structure to keep dignity intact",
        "practice": "treat the search itself as a disciplined assignment",
        "transit_slug": "saturn-in-capricorn",
        "transit_label": "Saturn in Capricorn",
        "sign_slug": "capricorn",
        "chart_point": "saturn",
        "house": "10th-house",
        "gita_situation_slug": "career-failure",
    },
    {
        "slug": "single-parenthood",
        "label": "Single Parenthood",
        "core_pain": "compresses emotional and practical responsibility into one set of hands",
        "faith_need": "strength, support, and wisdom for sustainable care",
        "practice": "build support systems instead of heroic isolation",
        "transit_slug": "jupiter-in-cancer",
        "transit_label": "Jupiter in Cancer",
        "sign_slug": "cancer",
        "chart_point": "moon",
        "house": "5th-house",
        "gita_situation_slug": "parenting-challenges",
    },
    {
        "slug": "widowhood",
        "label": "Widowhood",
        "core_pain": "makes absence tangible in both the practical and intimate parts of life",
        "faith_need": "comfort that stays present after the first wave of support fades",
        "practice": "honor grief, accept help, and simplify what can be simplified",
        "transit_slug": "saturn-retrograde",
        "transit_label": "Saturn Retrograde",
        "sign_slug": "scorpio",
        "chart_point": "moon",
        "house": "8th-house",
        "gita_situation_slug": "grief-and-loss",
    },
    {
        "slug": "public-failure",
        "label": "Public Failure",
        "core_pain": "adds shame and visibility to the ordinary pain of a setback",
        "faith_need": "identity rooted deeper than reputation",
        "practice": "name the mistake, repair what can be repaired, and keep moving",
        "transit_slug": "sun-in-leo",
        "transit_label": "Sun in Leo",
        "sign_slug": "leo",
        "chart_point": "sun",
        "house": "10th-house",
        "gita_situation_slug": "identity-crisis",
    },
    {
        "slug": "ministry-disappointment",
        "label": "Ministry Disappointment",
        "core_pain": "wounds deeply because the place that promised meaning became a place of strain",
        "faith_need": "renewed trust in God without naive denial about people",
        "practice": "separate God from the failure of human structures",
        "transit_slug": "jupiter-retrograde",
        "transit_label": "Jupiter Retrograde",
        "sign_slug": "sagittarius",
        "chart_point": "jupiter",
        "house": "9th-house",
        "gita_situation_slug": "betrayal",
    },
    {
        "slug": "academic-failure",
        "label": "Academic Failure",
        "core_pain": "can make effort feel invisible and the future suddenly unstable",
        "faith_need": "confidence that one result does not define the whole calling",
        "practice": "review honestly, ask for help, and rebuild your plan",
        "transit_slug": "mercury-in-gemini",
        "transit_label": "Mercury in Gemini",
        "sign_slug": "gemini",
        "chart_point": "mercury",
        "house": "9th-house",
        "gita_situation_slug": "career-failure",
    },
    {
        "slug": "prodigal-child",
        "label": "Prodigal Child",
        "core_pain": "holds parental love inside long uncertainty and little control",
        "faith_need": "hope without delusion and prayer without manipulation",
        "practice": "keep your heart open while holding wise boundaries",
        "transit_slug": "jupiter-in-cancer",
        "transit_label": "Jupiter in Cancer",
        "sign_slug": "cancer",
        "chart_point": "moon",
        "house": "5th-house",
        "gita_situation_slug": "parenting-challenges",
    },
    {
        "slug": "bankruptcy",
        "label": "Bankruptcy",
        "core_pain": "turns financial collapse into a public and emotional reset",
        "faith_need": "mercy strong enough to rebuild integrity after loss",
        "practice": "treat the process as a sober reordering, not as annihilation",
        "transit_slug": "jupiter-in-taurus",
        "transit_label": "Jupiter in Taurus",
        "sign_slug": "taurus",
        "chart_point": "jupiter",
        "house": "2nd-house",
        "gita_situation_slug": "financial-pressure",
    },
    {
        "slug": "diagnosis-waiting",
        "label": "Diagnosis Waiting",
        "core_pain": "keeps the body and imagination in suspense at the same time",
        "faith_need": "peace for the waiting room and courage for the answer",
        "practice": "limit speculation and stay rooted in what is actually known",
        "transit_slug": "mercury-retrograde",
        "transit_label": "Mercury Retrograde",
        "sign_slug": "gemini",
        "chart_point": "mercury",
        "house": "6th-house",
        "gita_situation_slug": "anxiety",
    },
    {
        "slug": "foster-care",
        "label": "Foster Care",
        "core_pain": "brings love, instability, attachment, and bureaucracy together",
        "faith_need": "wisdom for care that stays tender but realistic",
        "practice": "protect routine, ask for support, and honor the child's pace",
        "transit_slug": "jupiter-in-cancer",
        "transit_label": "Jupiter in Cancer",
        "sign_slug": "cancer",
        "chart_point": "moon",
        "house": "4th-house",
        "gita_situation_slug": "parenting-challenges",
    },
    {
        "slug": "military-deployment",
        "label": "Military Deployment",
        "core_pain": "stretches family life across distance, uncertainty, and risk",
        "faith_need": "protection and steadiness for both the one sent and the one waiting",
        "practice": "keep communication rhythms and practical support clear",
        "transit_slug": "mars-in-virgo",
        "transit_label": "Mars in Virgo",
        "sign_slug": "virgo",
        "chart_point": "mars",
        "house": "9th-house",
        "gita_situation_slug": "relationship-breakdown",
    },
    {
        "slug": "legal-separation",
        "label": "Legal Separation",
        "core_pain": "suspends a relationship between attachment and ending",
        "faith_need": "wisdom for process, boundaries, and honest motives",
        "practice": "keep paperwork and emotions from contaminating each other",
        "transit_slug": "venus-retrograde",
        "transit_label": "Venus Retrograde",
        "sign_slug": "libra",
        "chart_point": "venus",
        "house": "7th-house",
        "gita_situation_slug": "divorce",
    },
    {
        "slug": "hospice-care",
        "label": "Hospice Care",
        "core_pain": "places love inside anticipatory grief and final tenderness",
        "faith_need": "presence strong enough to stay soft in the face of loss",
        "practice": "keep the room simple, truthful, and gentle",
        "transit_slug": "saturn-retrograde",
        "transit_label": "Saturn Retrograde",
        "sign_slug": "scorpio",
        "chart_point": "moon",
        "house": "8th-house",
        "gita_situation_slug": "grief-and-loss",
    },
    {
        "slug": "layoff-season",
        "label": "Layoff Season",
        "core_pain": "creates communal instability even before the final outcome is known",
        "faith_need": "calm that protects both strategy and dignity",
        "practice": "prepare practically while refusing rumor-driven panic",
        "transit_slug": "saturn-in-capricorn",
        "transit_label": "Saturn in Capricorn",
        "sign_slug": "capricorn",
        "chart_point": "saturn",
        "house": "10th-house",
        "gita_situation_slug": "anxiety",
    },
    {
        "slug": "first-home",
        "label": "First Home",
        "core_pain": "mixes gratitude with debt, responsibility, and new pressure",
        "faith_need": "wisdom for stewardship and peace inside the commitment",
        "practice": "treat the home as a stable rhythm, not as a status project",
        "transit_slug": "jupiter-in-taurus",
        "transit_label": "Jupiter in Taurus",
        "sign_slug": "taurus",
        "chart_point": "venus",
        "house": "4th-house",
        "gita_situation_slug": "major-decision",
    },
    {
        "slug": "startup-collapse",
        "label": "Startup Collapse",
        "core_pain": "combines vision loss with financial and reputational pressure",
        "faith_need": "redemption for a dream that did not survive its first form",
        "practice": "grieve the idea, close the books, and keep learning",
        "transit_slug": "mercury-in-gemini",
        "transit_label": "Mercury in Gemini",
        "sign_slug": "gemini",
        "chart_point": "mercury",
        "house": "10th-house",
        "gita_situation_slug": "creative-block",
    },
    {
        "slug": "midlife-reset",
        "label": "Midlife Reset",
        "core_pain": "raises hard questions about identity, purpose, and the shape of the second half of life",
        "faith_need": "clarity that goes deeper than restlessness",
        "practice": "trim the noise and re-evaluate from values rather than panic",
        "transit_slug": "sun-in-leo",
        "transit_label": "Sun in Leo",
        "sign_slug": "leo",
        "chart_point": "sun",
        "house": "1st-house",
        "gita_situation_slug": "identity-crisis",
    },
    {
        "slug": "reconciliation-attempt",
        "label": "Reconciliation Attempt",
        "core_pain": "reopens a wound while hope and caution wrestle with each other",
        "faith_need": "truth, mercy, and discernment in the same room",
        "practice": "repair slowly enough that trust can be tested honestly",
        "transit_slug": "venus-in-libra",
        "transit_label": "Venus in Libra",
        "sign_slug": "libra",
        "chart_point": "venus",
        "house": "7th-house",
        "gita_situation_slug": "betrayal",
    },
    {
        "slug": "loss-of-faith-community",
        "label": "Loss of Faith Community",
        "core_pain": "can make spiritual language itself feel loaded or unsafe",
        "faith_need": "healing that distinguishes God from disappointed people",
        "practice": "rebuild trust slowly, with room for lament and boundaries",
        "transit_slug": "saturn-in-aquarius",
        "transit_label": "Saturn in Aquarius",
        "sign_slug": "aquarius",
        "chart_point": "saturn",
        "house": "11th-house",
        "gita_situation_slug": "betrayal",
    },
    {
        "slug": "postpartum-recovery",
        "label": "Postpartum Recovery",
        "core_pain": "brings healing, sleep disruption, and emotional adjustment into one demanding season",
        "faith_need": "gentleness, strength, and non-performative support",
        "practice": "lower expectations and protect small rhythms of care",
        "transit_slug": "jupiter-in-cancer",
        "transit_label": "Jupiter in Cancer",
        "sign_slug": "cancer",
        "chart_point": "moon",
        "house": "5th-house",
        "gita_situation_slug": "health-crisis",
    },
]

if len(TRANSITIONS) != 50:
    raise ValueError(f"Expected 50 Bible transitions, found {len(TRANSITIONS)}")

TRANSITION_INDEX = {item["slug"]: item for item in TRANSITIONS}
GITA_SITUATION_INDEX = {item["slug"]: item for item in GITA_SITUATIONS}


@lru_cache(maxsize=1)
def _load_bible_source() -> list[dict]:
    return json.loads(BIBLE_SOURCE_ASSET_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _source_index() -> dict[str, dict]:
    return {item["slug"]: item for item in _load_bible_source()}


@lru_cache(maxsize=1)
def _load_supporting_references() -> list[dict]:
    return json.loads(SUPPORTING_REFS_ASSET_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _supporting_reference_index() -> dict[str, dict]:
    return {item["slug"]: item for item in _load_supporting_references()}


@lru_cache(maxsize=1)
def _load_bible_meanings() -> list[dict]:
    return json.loads(BIBLE_MEANINGS_ASSET_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _meaning_index() -> dict[str, dict]:
    return {item["key"]: item for item in _load_bible_meanings()}


@lru_cache(maxsize=1)
def _load_gita_verses() -> list[dict]:
    return json.loads(GITA_ASSET_PATH.read_text(encoding="utf-8"))


def _select_bible_verse(topic_slug: str, transition_slug: str) -> dict:
    topic = TOPIC_INDEX[topic_slug]
    candidate_slugs = SOURCE_PRIMARY_BUCKET_MAP.get(topic["source_slug"], [topic["source_slug"], "the-promises-of-god"])
    candidate_buckets = [item for item in (_source_index().get(slug) for slug in candidate_slugs) if item]
    bucket = candidate_buckets[0] if candidate_buckets else {"verses": []}
    verses = []
    seen_pairs: set[tuple[str, str]] = set()
    for candidate_bucket in candidate_buckets:
        for verse in candidate_bucket.get("verses", []):
            pair = (verse.get("reference", ""), verse.get("text", ""))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            enriched = dict(verse)
            enriched.setdefault("source_label", candidate_bucket.get("source_label", "The Book of Bible Promises"))
            enriched.setdefault("source_pdf", candidate_bucket.get("source_pdf", "the_book_of_bible_promises.pdf"))
            enriched.setdefault("source_section_slug", candidate_bucket.get("slug", "the-promises-of-god"))
            enriched.setdefault("source_section_title", candidate_bucket.get("title", "The Promises of God"))
            verses.append(enriched)
    short_verses = [item for item in verses if len(item.get("text", "")) <= 260] or verses
    if not short_verses:
        return {
            "reference": "Psalm 23:1",
            "text": "The Lord is my shepherd; I shall not want.",
            "source_label": "The Book of Bible Promises",
            "source_pdf": "the_book_of_bible_promises.pdf",
            "source_section_slug": "the-promises-of-god",
            "source_section_title": "The Promises of God",
        }
    return dict(short_verses[_hash_index(topic_slug, transition_slug, modulus=len(short_verses))])


def _support_topic_labels_for_topic(topic_slug: str) -> list[str]:
    topic = TOPIC_INDEX[topic_slug]
    labels = SOURCE_SUPPORT_TOPIC_MAP.get(topic["source_slug"], [])
    if not labels:
        labels = [topic["label"]]
    return labels


def _select_supporting_references(topic_slug: str, transition_slug: str, limit: int = 6) -> list[dict]:
    refs: list[dict] = []
    seen: set[str] = set()
    for label in _support_topic_labels_for_topic(topic_slug):
        bucket = _supporting_reference_index().get(_slugify(label))
        if not bucket:
            continue
        for reference in bucket.get("references", []):
            if reference in seen:
                continue
            seen.add(reference)
            refs.append(
                {
                    "reference": reference,
                    "source_topic": bucket["title"],
                    "source_slug": bucket["slug"],
                }
            )

    if not refs:
        return []

    start = _hash_index(topic_slug, transition_slug, modulus=len(refs))
    selected = [refs[(start + offset) % len(refs)] for offset in range(min(limit, len(refs)))]
    return selected


def _meaning_tags_for_topic(topic_slug: str) -> list[dict]:
    topic = TOPIC_INDEX[topic_slug]
    tags = []
    for key in SOURCE_MEANING_TAG_MAP.get(topic["source_slug"], []):
        item = _meaning_index().get(key)
        if item:
            tags.append(item)
    return tags


def _word_study_for_topic(topic_slug: str, transition: dict | None = None) -> dict:
    topic = TOPIC_INDEX[topic_slug]
    title = f"Word study: {topic['term']}"
    if transition is not None:
        title = f"Word study for {transition['label']} {transition['chart_point']}: {topic['term']}"
    meaning = topic["term_note"]
    if transition is not None:
        meaning = (
            f"For {transition['label'].lower()}, {topic['term']} names the kind of inner movement where {topic['term_note']}."
        )
    transition_tail = (
        f" In {transition['label'].lower()}, it keeps the emphasis on {transition['faith_need']} while filtering out the panic story this season likes to generate."
        if transition is not None
        else ""
    )
    return {
        "term": topic["term"],
        "title": title,
        "meaning": meaning,
        "application": (
            f"For the {topic['label'].lower()} theme, this word keeps the reading close to {topic['promise_angle']}.{transition_tail} "
            f"It stops the page from floating above the real pressure of the transition and keeps the interpretation close to lived obedience."
        ),
        "source_pdf": "Bible Meanings.pdf",
    }


def _symbolic_note_for_topic(topic_slug: str, featured_meaning: dict | None, transition: dict | None = None) -> dict | None:
    if TOPIC_ORDINAL[topic_slug] % 10 not in {0, 3, 6} or featured_meaning is None:
        return None
    topic = TOPIC_INDEX[topic_slug]
    transition_tail = (
        f" In {transition['label'].lower()}, that picture helps the reader hold {transition['practice']} with more steadiness."
        if transition is not None
        else ""
    )
    return {
        "title": (
            f"Symbolic note for {transition['label']} {transition['house'].replace('-', ' ')}: {featured_meaning['label']}"
            if transition is not None
            else f"Symbolic note: {featured_meaning['label']}"
        ),
        "label": featured_meaning["label"],
        "note": (
            f"In the {topic['label'].lower()} cluster, {featured_meaning['label'].lower()} works as a controlled symbolic cue. "
            f"It helps the reader picture {featured_meaning['note'][0].lower() + featured_meaning['note'][1:]} without copying devotional source prose.{transition_tail}"
        ),
        "source_pdf": "Bible Meanings.pdf",
    }


def _bible_faq(topic: dict, transition: dict, gita_situation: dict) -> list[dict]:
    selector = _hash_index(topic["slug"], transition["slug"], modulus=8)
    if selector == 0:
        return [
            {
                "q": f"When {transition['label'].lower()} feels sharp, why start with {topic['label'].lower()}?",
                "a": f"Because {topic['label'].lower()} gives {transition['faith_need']} a scriptural name before the mind reduces the transition to urgency alone.",
            },
            {
                "q": f"What prayer language fits {transition['label'].lower()} under this promise?",
                "a": f"Start where {transition['label'].lower()} is pressing hardest. Ask for the {topic['term'].lower()} this passage offers. Close with one concrete act before the day ends.",
            },
            {
                "q": f"How does the paired Gita route sharpen {transition['label'].lower()}?",
                "a": f"It describes the same pressure through {gita_situation['label'].lower()}, which helps the reader compare pastoral comfort with disciplined action.",
            },
        ]
    if selector == 1:
        return [
            {
                "q": f"Which part of {transition['label'].lower()} does the {topic['label'].lower()} theme actually steady?",
                "a": f"It steadies the inner place where urgency starts narrating the whole day and {transition['faith_need']} becomes hardest to keep in view.",
            },
            {
                "q": f"How should someone pray about {transition['chart_point']} pressure during {transition['label'].lower()}?",
                "a": f"Name the pressure around {transition['chart_point']} plainly, ask for the grace this page highlights, then turn that prayer into one clean next step.",
            },
            {
                "q": f"Why is there a Gita bridge for {transition['house'].replace('-', ' ')} themes here?",
                "a": f"Because the Gita cross-link translates the same life area into duty language, not just reassurance language.",
            },
        ]
    if selector == 2:
        return [
            {
                "q": f"How does {topic['label'].lower()} steady {transition['label'].lower()}?",
                "a": f"It steadies the transition by giving {transition['faith_need']} a promise-shaped center before fear turns the moment into a verdict.",
            },
            {
                "q": f"What kind of prayer fits {transition['label'].lower()} when the theme is {topic['label'].lower()}?",
                "a": f"Use a prayer that tells the truth about the strain, asks for the exact mercy this page names, and closes with one act of obedience.",
            },
            {
                "q": f"Why pair this page with the Gita situation of {gita_situation['label'].lower()}?",
                "a": f"Because that situation names a parallel pressure pattern and offers a second spiritual grammar for the same season.",
            },
        ]
    if selector == 3:
        return [
            {
                "q": f"What should be noticed first inside {transition['label'].lower()} on this page?",
                "a": f"Notice where the threshold is rewriting your inner speech, because that is usually where {topic['label'].lower()} is most needed.",
            },
            {
                "q": f"How can prayer stay concrete during {transition['label'].lower()}?",
                "a": f"Anchor prayer to one named burden, one named grace, and one named response so the heart does not drift into vagueness.",
            },
            {
                "q": f"What does the Gita comparison add that the promise page does not?",
                "a": f"It adds a discipline lens, showing how the same burden behaves when read through duty, timing, and steadier motive.",
            },
        ]
    if selector == 4:
        return [
            {
                "q": f"Why is {topic['label'].lower()} stronger here than a generic comfort verse?",
                "a": f"Because it reaches the exact need for {transition['faith_need']} instead of offering comfort that could belong anywhere.",
            },
            {
                "q": f"When praying through {transition['label'].lower()}, what should come after honesty?",
                "a": f"After honesty, ask for the grace this text names and let it direct one concrete act before the day closes.",
            },
            {
                "q": f"How should the Gita bridge be used without diluting the Bible reading?",
                "a": f"Use it as a companion lens after the promise is clear, not before. Let scripture comfort first, then let the Gita sharpen practice.",
            },
        ]
    if selector == 5:
        return [
            {
                "q": f"When does this promise page become most useful in {transition['label'].lower()}?",
                "a": f"When the transition starts collapsing meaning into panic, because {topic['label'].lower()} restores a truer center for the next response.",
            },
            {
                "q": f"What is the cleanest way to pray this promise today?",
                "a": f"Tell the truth about the burden, receive the grace the passage offers, and let that grace govern one concrete action before the day closes.",
            },
            {
                "q": f"Why does the page point toward {gita_situation['label'].lower()} on the Gita side?",
                "a": f"Because the same season can be understood through promise and through discipline, and seeing both keeps the page richer than a single tradition silo.",
            },
        ]
    if selector == 6:
        return [
            {
                "q": f"What does {topic['label'].lower()} offer that advice alone cannot in {transition['label'].lower()}?",
                "a": f"It offers {transition['faith_need']} a named foundation rather than a strategy. Advice changes with circumstances; a promise holds the same ground.",
            },
            {
                "q": f"How should prayer move differently when {transition['label'].lower()} is the dominant pressure?",
                "a": f"Let it name what is true, ask for the specific help this text points to, and close with the smallest act that reflects {topic['label'].lower()} rather than fear.",
            },
            {
                "q": f"What does the Gita connection add that the Bible page cannot carry alone?",
                "a": f"It adds the language of duty and action to a page that already carries promise. Together they address both what to trust and what to do.",
            },
        ]
    return [
        {
            "q": f"How does {topic['label'].lower()} reframe what {transition['label'].lower()} is demanding?",
            "a": f"It shifts the question from survival to faithfulness: what is {transition['faith_need']} asking to be trusted with right now? A named promise makes that question answerable.",
        },
        {
            "q": f"What is the most important use of this page during {transition['label'].lower()}?",
            "a": f"Use it to name the grace available before urgency narrows what feels possible. {topic['label'].capitalize()} gives {transition['faith_need']} a shape, which steadies the next decision.",
        },
        {
            "q": f"How should the Gita path deepen this Bible reading without replacing it?",
            "a": f"Read the Bible promise first to establish what is true. Then use the Gita crosslink to convert that truth into a discipline -- a way of acting that reflects what you have just received.",
        },
    ]


def _bible_seed(topic_slug: str, transition_slug: str, modulus: int) -> int:
    return _hash_index(topic_slug, transition_slug, modulus=modulus)


def _first_content_token(text: str) -> str:
    """Returns the first non-trivial word (>4 chars, not a stop connector) from a phrase."""
    skip = {
        "which", "their", "about", "being", "those", "these", "where", "while",
        "there", "every", "often", "since", "until", "under", "might", "would",
        "could", "shall", "feels", "makes", "turns", "keeps", "gives",
    }
    for raw in text.split():
        word = raw.strip(".,;:!?").lower()
        if len(word) > 4 and word not in skip:
            return word
    return text.split()[0].lower() if text.strip() else "steadiness"


def _bible_verse_keywords(verse: dict, limit: int = 3) -> list[str]:
    words: list[str] = []
    for raw in verse.get("text", "").replace("-", " ").split():
        word = raw.strip(" ,.;:!?()[]'\"").lower()
        word = "".join(char for char in word if char.isalpha())
        if len(word) < 5 or word in {"shall", "thee", "unto", "therefore", "whatsoever", "through", "because", "which"} or word in words:
            continue
        words.append(word)
        if len(words) == limit:
            break
    if not words:
        words = ["mercy", "strength", "steadiness"][:limit]
    while len(words) < limit:
        words.append(words[-1])
    return words


def _bible_summary(topic: dict, transition: dict, verse: dict) -> str:
    words = _bible_verse_keywords(verse, limit=2)
    seed = _bible_seed(topic["slug"], transition["slug"], modulus=8)
    options = [
        f"{words[0].capitalize()} is the entry word on this page. {verse['reference']} brings that word into {transition['label'].lower()} so {topic['label'].lower()} is read as a precise promise rather than a generic comfort.",
        f"When {transition['label'].lower()} is the threshold, this page lets {verse['reference']} lead with {words[0]} and {words[1]} before any commentary widens the frame.",
        f"Not a broad reassurance page but a {words[0]} page: that is how {topic['label'].lower()} is handled here for {transition['label'].lower()}.",
        f"What allows {topic['label'].lower()} to speak freshly to {transition['label'].lower()} is the vocabulary of {verse['reference']}, especially {words[0]} beside {words[1]}.",
        f"{verse['reference']} enters this page through two terms - {words[0]} and {words[1]} - and those terms keep the promise attached to the real transition.",
        f"Read the page from the verse outward: {words[0]} first, {words[1]} next, and only then the larger topic of {topic['label'].lower()} for {transition['label'].lower()}.",
        f"For this page, {topic['label'].lower()} is not the headline so much as the destination. {words[0]} in {verse['reference']} is what gets the reader there.",
        f"Here the promise begins at word level. {words[0].capitalize()} and {words[1]} do the opening work, so {transition['label'].lower()} is interpreted by scripture rather than by mood.",
    ]
    return options[seed]


def _bible_emotional_frame(topic: dict, transition: dict, verse: dict) -> str:
    words = _bible_verse_keywords(verse, limit=3)
    seed = _bible_seed(topic["slug"], transition["slug"], modulus=8)
    options = [
        f"{transition['label']} often {transition['core_pain']}. Into that atmosphere, {verse['reference']} brings {words[0]} and {words[1]}, reminding the reader that the deeper need is still {transition['faith_need']}.",
        f"When identity or energy is being pressed by {transition['label'].lower()}, the words {words[0]} and {words[1]} keep the page from collapsing into vague reassurance.",
        f"{transition['label']} can send a person toward urgency. This page interrupts that motion with {words[0]}, {words[1]}, and {words[2]}, because {transition['faith_need']} is the real pressure underneath.",
        f"Decisions made during {transition['label'].lower()} easily borrow their tone from fear. {verse['reference']} resists that borrowing by foregrounding {words[0]} and {words[1]}.",
        f"{topic['label']} matters here because {transition['label'].lower()} has its own emotional weather. The verse language of {words[0]} and {words[1]} gives that weather a truthful spiritual frame.",
        f"If the heart is thinning out under {transition['label'].lower()}, start with the verse's own vocabulary. {words[0].capitalize()} and {words[1]} keep the page close to scripture and close to need at the same time.",
        f"Before this page becomes guidance, it becomes naming. {words[0].capitalize()}, {words[1]}, and {words[2]} tell the truth about what {transition['label'].lower()} is stirring.",
        f"The transition is not only external; it also alters inner tone. That is why {verse['reference']} leans on {words[0]} and {words[1]} instead of offering a slogan-sized comfort.",
    ]
    return options[seed]


def _bible_application(topic: dict, transition: dict, verse: dict, support_lead: dict | None, application_tail: str) -> str:
    words = _bible_verse_keywords(verse, limit=3)
    seed = _bible_seed(topic["slug"], transition["slug"], modulus=8)
    support_phrase = support_lead["reference"] if support_lead else "Psalm 23:1"
    tail = application_tail or "let the next step stay concrete and obedient."
    options = [
        f"Let {verse['reference']} become practical through one disciplined decision. Use {words[0]} to guide {transition['practice']}, then {tail} Pair it with {support_phrase} so the movement is reinforced from a second angle.",
        f"Today the page is applied by taking {topic['label'].lower()} out of abstraction. Start with {transition['practice']}, let {words[0]} and {words[1]} shape the choice, and keep {support_phrase} nearby if urgency returns.",
        f"The next wise move in {transition['label'].lower()} is usually smaller and cleaner than the mind expects. Make {words[0]} the rule for action, practice {transition['practice']}, and let {support_phrase} steady the same line of response.",
        f"Carry the verse into behavior before interpretation grows larger. Choose {transition['practice']}, let {words[1]} interrupt emotional overreach, and use {support_phrase} if the promise needs a second witness.",
        f"This promise becomes real when it governs the next obedient act. Build around {transition['practice']}, keep {words[0]} and {words[2]} visible, and let {support_phrase} reinforce the same response without extra noise.",
        f"What should happen after reading? {transition['practice'].capitalize()} should happen. Let {words[0]} set the tone, let {words[1]} narrow the step, and let {support_phrase} confirm the direction.",
        f"Not the whole life plan - just the next faithful move. Through {words[0]}, this page turns {transition['practice']} into something concrete, while {support_phrase} keeps the heart from drifting.",
        f"Begin with one obedient action and let theology catch up afterward. {words[0].capitalize()} belongs in the next decision, {words[2]} belongs in the inner posture, and {support_phrase} belongs close at hand.",
    ]
    return options[seed]


def _bible_hermeneutical(
    topic: dict,
    transition: dict,
    verse: dict,
    verse_excerpt: str,
    symbolic_note: str,
    support_lead: dict | None,
    transition_frame: str,
    featured_meaning: dict | None,
) -> str:
    seed = _bible_seed(topic["slug"], transition["slug"], modulus=8)
    sym_label = featured_meaning["label"].lower() if featured_meaning else "steadiness"
    support_ref = support_lead["reference"] if support_lead else "Psalm 23:1"
    support_topic = support_lead["source_topic"].lower() if support_lead else "steady prayer"
    frame_clause = transition_frame + " " if transition_frame else ""
    faith_token = _first_content_token(transition["faith_need"])
    pain_token = _first_content_token(transition["core_pain"])
    symbolic_clause = (
        f"{sym_label} here becomes a cue for {faith_token} while {transition['label'].lower()} is active"
    )

    options = [
        (
            f"The line '{verse_excerpt}...' from {verse['reference']} is what anchors this page to {transition['label'].lower()}. "
            f"{frame_clause}"
            f"It speaks to the need for {faith_token} - not as a guarantee that {transition['label'].lower()} will pass quickly, but as a truthful frame for living inside it. "
            f"{symbolic_clause}, which is why this verse stays usable when {pain_token} tightens. "
            f"A supporting thread, {support_ref}, keeps the same promise from a second scriptural angle without adding noise."
        ),
        (
            f"In {transition['label'].lower()}, {pain_token} rises quickly. {frame_clause}"
            f"That is the pressure this page is meant to meet, using {topic['promise_angle']} as its pastoral entry. "
            f"{verse['reference']} is not here generically; it approaches {faith_token} from the exact angle this threshold exposes. "
            f"{symbolic_clause}, and {support_ref} extends the response into a second verse bank."
        ),
        (
            f"The deeper need in {transition['label'].lower()} is {faith_token}, and {verse['reference']} addresses it through {topic['promise_angle']} rather than through comfort alone. "
            f"{frame_clause}"
            f"The line '{verse_excerpt}...' is chosen because it does not bypass the emotional difficulty - it names the need and then gives the reader a truthful anchor. "
            f"In the symbolic lexicon, {symbolic_clause}. {support_ref} reinforces the same pastoral movement from a different scriptural starting point."
        ),
        (
            f"This page approaches {transition['label'].lower()} through the lens of {topic['promise_angle']}, using {verse['reference']} as the primary scriptural voice. "
            f"{frame_clause}"
            f"'{verse_excerpt}...' lands directly on {faith_token} - the grace this threshold is actually asking for. "
            f"{symbolic_clause}. "
            f"The nearby thread in {support_ref} grounds the promise in a second passage so the page does not rest on a single verse alone."
        ),
        (
            f"The symbolic current running through {transition['label'].lower()} often surfaces as {symbolic_clause}. "
            f"{frame_clause}"
            f"{verse['reference']} meets this current through {topic['promise_angle']}, especially in the line '{verse_excerpt}...' where the promise is most direct. "
            f"That is why {faith_token} can be met here without bypassing the real weight of {pain_token}. "
            f"The supporting reference, {support_ref}, reinforces the same response from the {support_topic} thread in the Scripture for Every Moment bank."
        ),
        (
            f"{support_ref} is not the anchor on this page; {verse['reference']} is. "
            f"{frame_clause}"
            f"The anchor matters because {transition['label'].lower()} is asking for {faith_token}, and the phrase '{verse_excerpt}...' names that need without softening the threshold. "
            f"Then {symbolic_clause}, while the supporting verse keeps the same promise from standing alone."
        ),
        (
            f"{verse['reference']} is positioned here not for comfort alone but for clarity about {faith_token} while {transition['label'].lower()} reshapes the inner landscape. "
            f"{frame_clause}"
            f"The line '{verse_excerpt}...' names that reshaping from a scriptural angle, and {sym_label} becomes the symbolic thread that keeps it grounded. "
            f"A supporting passage, {support_ref}, carries the same promise into a second register without adding noise."
        ),
        (
            f"What {transition['label'].lower()} exposes is the need for {faith_token}, and {verse['reference']} addresses that need before urgency can collapse it. "
            f"{frame_clause}"
            f"'{verse_excerpt}...' carries the weight of {pain_token} without minimising it, which is why this page holds as a stable anchor under pressure. "
            f"{symbolic_clause.capitalize()}, and {support_ref} reinforces the same promise from a second doctrinal source."
        ),
    ]
    return options[seed]


def _topic_specific_transition_frame(topic_slug: str, transition: dict) -> str:
    topic = TOPIC_INDEX[topic_slug]
    if topic["source_slug"] != "financial-need":
        return ""

    slug = transition["slug"]
    if slug == "financial-crisis":
        return "In this case, provision is about stabilizing immediate cash pressure without letting urgency rewrite your values."
    if slug == "bankruptcy":
        return "In this case, provision is about rebuilding structure and dignity after a public financial reset."
    if slug == "job-loss":
        return "In this case, provision is tied to sudden interruption, shaken dignity, and the need to respond before fear hardens into humiliation."
    if slug == "unemployment":
        return "In this case, provision is tied to long uncertainty, shrinking routine, and the quiet erosion of morale over time."
    if slug == "layoff-season":
        return "In this case, provision is tied to anticipatory instability, rumor, and the strain of preparing before the outcome is final."
    if slug == "business-failure":
        return "In this case, provision has to speak to visible loss, stakeholder pressure, and the discipline of facing what the books now say."
    if slug == "startup-collapse":
        return "In this case, provision has to speak to founder grief, broken momentum, and the ache of a vision that did not survive its first form."
    if slug == "first-home":
        return "In this case, provision has to stay larger than status so stewardship can remain calmer than the monthly obligation."
    return ""


def _topic_specific_application_tail(topic_slug: str, transition: dict) -> str:
    topic = TOPIC_INDEX[topic_slug]
    if topic["source_slug"] != "financial-need":
        return ""

    slug = transition["slug"]
    if slug == "financial-crisis":
        return "Start with triage: clarify due dates, stop avoidable leakage, and make one honest decision before panic builds a story for you."
    if slug == "bankruptcy":
        return "Treat the process as structural cleanup, not as a verdict on your worth. Gather records, ask clean questions, and let shame lose its exaggerating voice."
    if slug == "job-loss":
        return "Protect dignity early by separating the event from your worth, then move quickly into concrete planning before shock becomes paralysis."
    if slug == "unemployment":
        return "Build structure into the week so the search does not dissolve into formless discouragement and self-doubt."
    if slug == "layoff-season":
        return "Prepare quietly and practically so rumor does not become your inner manager before the facts arrive."
    if slug == "business-failure":
        return "Tell the truth to every stakeholder you owe, then separate the failed model from the whole self so the lesson can stay concrete instead of shaming."
    if slug == "startup-collapse":
        return "Let the dream be grieved before you force a lesson from it, or you will carry panic into the next idea under the name of urgency."
    if slug == "first-home":
        return "Let the home become a stewardship rhythm before it becomes a status performance."
    return ""


def _topic_specific_bridge_tail(topic_slug: str, transition: dict) -> str:
    topic = TOPIC_INDEX[topic_slug]
    if topic["source_slug"] != "financial-need":
        return ""

    slug = transition["slug"]
    if slug == "financial-crisis":
        return "That matters here because the pressure is immediate and liquid: the mind keeps scanning for rescue before it can think clearly."
    if slug == "bankruptcy":
        return "That matters here because the pressure is structural and public: the soul is dealing with collapse, paperwork, and the fear of being reduced to one failed chapter."
    if slug == "job-loss":
        return "That matters here because the pressure is abrupt and identity-charged: income stops while self-worth tries to collapse with it."
    if slug == "unemployment":
        return "That matters here because the pressure is slower and more ambient: routine disappears, confidence thins, and time itself starts to feel accusatory."
    if slug == "layoff-season":
        return "That matters here because the pressure is anticipatory: the body starts bracing before the event has even fully happened."
    if slug == "business-failure":
        return "That matters here because the pressure mixes money loss with responsibility to others, visible fallout, and the need to restore integrity in public."
    if slug == "startup-collapse":
        return "That matters here because the pressure mixes money loss with authorship, momentum, and the grief of a vision that failed in front of other people."
    return ""


def _select_gita_cross_link(topic_slug: str, transition_slug: str, situation_slug: str) -> dict:
    verses = _load_gita_verses()
    selected = verses[_hash_index(topic_slug, transition_slug, modulus=len(verses))]
    return {
        "reference": selected["reference"],
        "translation": selected["translation"],
        "href": f"/faith/gita/{selected['chapter']}-{selected['verse']}/{situation_slug}",
    }


def _top_transitions_for_topic(topic_slug: str, limit: int = 10) -> list[dict]:
    start = _hash_index(topic_slug, modulus=len(TRANSITIONS))
    items = []
    for offset in range(limit):
        transition = TRANSITIONS[(start + offset) % len(TRANSITIONS)]
        items.append(
            {
                "slug": transition["slug"],
                "label": transition["label"],
                "href": f"/faith/bible/{topic_slug}/{transition['slug']}",
            }
        )
    return items


def get_bible_page(topic_slug: str, transition_slug: str) -> dict | None:
    topic = TOPIC_INDEX.get(topic_slug)
    transition = TRANSITION_INDEX.get(transition_slug)
    if topic is None or transition is None:
        return None

    verse = _select_bible_verse(topic_slug, transition_slug)
    gita_cross = _select_gita_cross_link(topic_slug, transition_slug, transition["gita_situation_slug"])
    gita_situation = GITA_SITUATION_INDEX[transition["gita_situation_slug"]]
    supporting_references = _select_supporting_references(topic_slug, transition_slug, limit=6)
    meaning_tags = _meaning_tags_for_topic(topic_slug)
    route = f"/faith/bible/{topic_slug}/{transition_slug}"
    verse_excerpt = " ".join(verse["text"].split()[:10]).rstrip(" ,.;:")
    featured_meaning = meaning_tags[_hash_index(topic_slug, transition_slug, modulus=len(meaning_tags))] if meaning_tags else None
    symbolic_note = featured_meaning["note"] if featured_meaning else "a steadier symbolic frame for this promise"
    support_lead = supporting_references[0] if supporting_references else None
    transition_frame = _topic_specific_transition_frame(topic_slug, transition)
    application_tail = _topic_specific_application_tail(topic_slug, transition)
    bridge_tail = _topic_specific_bridge_tail(topic_slug, transition)
    word_study = _word_study_for_topic(topic_slug, transition)
    symbolic_note_data = _symbolic_note_for_topic(topic_slug, featured_meaning, transition)
    faq = _bible_faq(topic, transition, gita_situation)
    summary = _bible_summary(topic, transition, verse)
    emotional_frame = _bible_emotional_frame(topic, transition, verse)
    application = _bible_application(topic, transition, verse, support_lead, application_tail)
    title_word = _bible_verse_keywords(verse, limit=1)[0].capitalize()
    title = f"Bible Promises for {transition['label']} - {topic['label']} on {title_word}"

    return {
        "id": f"faith-bible-{topic_slug}-{transition_slug}",
        "route": route,
        "title": title,
        "meta_title": title[:60],
        "meta_description": (
            f"Bible promises for {transition['label'].lower()} on {topic['label'].lower()} with pastoral guidance and a parallel Gita bridge."
        )[:155],
        "topic_slug": topic_slug,
        "topic_label": topic["label"],
        "transition_slug": transition_slug,
        "transition_label": transition["label"],
        "reference": verse["reference"],
        "verse_text": verse["text"],
        "source": f"{verse['source_label']} - {verse['source_section_title']}",
        "summary": summary,
        "emotional_frame": emotional_frame,
        "hermeneutical": _bible_hermeneutical(
            topic, transition, verse, verse_excerpt, symbolic_note,
            support_lead, transition_frame, featured_meaning
        ),
        "word_study_title": word_study["title"],
        "word_study": word_study,
        "symbolic_note_title": symbolic_note_data["title"] if symbolic_note_data else "",
        "symbolic_note": symbolic_note_data,
        "application": application,
        "vedic_bridge": (
            f"Vedic tradition would often read this same pressure through the lens of {gita_situation['label'].lower()}, especially during {transition['transit_label'].lower()}. "
            f"The linked Gita page uses {gita_cross['reference']} and places the strain near {transition['chart_point']} themes and the {transition['house'].replace('-', ' ')}. "
            f"{bridge_tail + ' ' if bridge_tail else ''}"
            f"The Gita counterpart names the same human tension with a different spiritual grammar around {transition['chart_point']} and {transition['house'].replace('-', ' ')} concerns. "
            f"That makes the cross-link useful when {transition['label'].lower()} needs both pastoral reassurance and a second disciplined lens."
        ),
        "faq": faq,
        "supporting_references": supporting_references,
        "meaning_tags": meaning_tags,
        "featured_meaning_tag": featured_meaning,
        "provenance": {
            "primary_source": {
                "label": verse["source_label"],
                "pdf": verse["source_pdf"],
                "section_slug": verse["source_section_slug"],
                "section_title": verse["source_section_title"],
                "usage": "primary_topic_spine_and_verse_text",
            },
            "supporting_sources": [
                {
                    "label": "Scripture for Every Moment",
                    "pdf": "Scripture_for_Every_Moment.pdf",
                    "usage": "supporting_reference_bank",
                    "topic_labels": _support_topic_labels_for_topic(topic_slug),
                },
                {
                    "label": "Bible Meanings.pdf",
                    "pdf": "Bible Meanings.pdf",
                    "usage": "controlled_symbolic_lexicon",
                    "meaning_keys": [item["key"] for item in meaning_tags],
                },
            ],
        },
        "top_transitions": [item for item in _top_transitions_for_topic(topic_slug, limit=6) if item["slug"] != transition_slug][:5],
        "links": {
            "faith_hub_href": "/faith",
            "bible_hub_href": "/faith/bible",
            "topic_hub_href": f"/faith/bible/topic/{topic_slug}",
            "gita_cross_href": gita_cross["href"],
            "gita_cross_reference": gita_cross["reference"],
            "gita_cross_translation": gita_cross["translation"],
            "faith_transit_href": f"/faith/transit/{transition['transit_slug']}/bible",
            "traits_href": f"/traits/{transition['sign_slug']}/{transition['chart_point']}/{transition['house']}",
        },
    }


def get_bible_topic_payload(topic_slug: str) -> dict | None:
    topic = TOPIC_INDEX.get(topic_slug)
    if topic is None:
        return None

    verse = _select_bible_verse(topic_slug, "topic-preview")
    transitions = _top_transitions_for_topic(topic_slug, limit=10)
    supporting_references = _select_supporting_references(topic_slug, "topic-preview", limit=8)
    meaning_tags = _meaning_tags_for_topic(topic_slug)
    featured_meaning = meaning_tags[_hash_index(topic_slug, "topic-preview", modulus=len(meaning_tags))] if meaning_tags else None
    word_study = _word_study_for_topic(topic_slug)
    symbolic_note = _symbolic_note_for_topic(topic_slug, featured_meaning)
    return {
        "title": f"{topic['label']} Bible Promise Hub",
        "meta_title": f"{topic['label']} Bible Promises by Transition",
        "meta_description": (
            f"Browse Bible promise pages for {topic['label'].lower()} across ten featured life transitions."
        )[:155],
        "hero_title": f"{topic['label']} Bible Promises by Transition",
        "hero_body": (
            f"This topic hub gathers the Bible theme of {topic['label'].lower()} across multiple life transitions. "
            f"It is designed for readers who know the theme they need but want the application tailored to the transition they are actually walking through."
        ),
        "topic_slug": topic_slug,
        "topic_label": topic["label"],
        "theme_term": topic["term"],
        "theme_term_note": topic["term_note"],
        "word_study_title": word_study["title"],
        "word_study": word_study,
        "symbolic_note_title": symbolic_note["title"] if symbolic_note else "",
        "symbolic_note": symbolic_note,
        "sample_reference": verse["reference"],
        "sample_text": verse["text"],
        "sample_source": f"{verse['source_label']} - {verse['source_section_title']}",
        "supporting_references": supporting_references,
        "meaning_tags": meaning_tags,
        "provenance": {
            "primary_source": {
                "label": verse["source_label"],
                "pdf": verse["source_pdf"],
                "section_slug": verse["source_section_slug"],
                "section_title": verse["source_section_title"],
                "usage": "primary_topic_spine_and_verse_text",
            },
            "supporting_sources": [
                {
                    "label": "Scripture for Every Moment",
                    "pdf": "Scripture_for_Every_Moment.pdf",
                    "usage": "supporting_reference_bank",
                    "topic_labels": _support_topic_labels_for_topic(topic_slug),
                },
                {
                    "label": "Bible Meanings.pdf",
                    "pdf": "Bible Meanings.pdf",
                    "usage": "controlled_symbolic_lexicon",
                    "meaning_keys": [item["key"] for item in meaning_tags],
                },
            ],
        },
        "transitions": transitions,
    }


def get_bible_hub_payload() -> dict:
    topic_cards = []
    for topic in BIBLE_TOPICS:
        sample_transition = _top_transitions_for_topic(topic["slug"], limit=1)[0]
        topic_cards.append(
            {
                "slug": topic["slug"],
                "label": topic["label"],
                "href": f"/faith/bible/topic/{topic['slug']}",
                "sample_href": sample_transition["href"],
            }
        )

    featured_topics = []
    for slug in ("anxiety", "hope", "healing", "guidance", "forgiveness", "peace"):
        topic = TOPIC_INDEX[slug]
        verse = _select_bible_verse(slug, "featured")
        featured_topics.append(
            {
                "slug": slug,
                "label": topic["label"],
                "reference": verse["reference"],
                "text": verse["text"],
                "href": f"/faith/bible/topic/{slug}",
            }
        )

    return {
        "title": "Faith Bible Hub",
        "meta_title": "Bible Promise Library by Topic and Transition",
        "meta_description": "Explore 120 Bible promise topics across 50 real-life transitions with a parallel Gita bridge and transition-based guidance.",
        "hero_title": "Bible Promise Library for Real-Life Transitions",
        "hero_body": (
            "This hub turns the Bible promise layer into a real library. Readers can now enter through a topic such as peace, provision, or forgiveness, "
            "then move into the life transition they are actually navigating without losing emotional specificity."
        ),
        "counts": {
            "topics": len(BIBLE_TOPICS),
            "transitions": len(TRANSITIONS),
            "pages": len(BIBLE_TOPICS) * len(TRANSITIONS),
        },
        "topics": topic_cards,
        "transition_index": [{"slug": item["slug"], "label": item["label"]} for item in TRANSITIONS],
        "featured_topics": featured_topics,
        "phase_note": "Phase 3 is live for the Bible promise layer. Faith Hubs now includes transit, daily, Gita, and Bible public paths.",
    }


def build_bible_pages() -> list[dict]:
    pages = []
    for topic in BIBLE_TOPICS:
        for transition in TRANSITIONS:
            pages.append(get_bible_page(topic["slug"], transition["slug"]))
    return [page for page in pages if page is not None]


def get_bible_page_count() -> int:
    return len(BIBLE_TOPICS) * len(TRANSITIONS)


def get_bible_sitemap_urls() -> list[str]:
    urls = [f"{SITE_URL}/faith/bible"]
    urls.extend(f"{SITE_URL}/faith/bible/topic/{topic['slug']}" for topic in BIBLE_TOPICS)
    for topic in BIBLE_TOPICS:
        for transition in TRANSITIONS:
            urls.append(f"{SITE_URL}/faith/bible/{topic['slug']}/{transition['slug']}")
    return urls
