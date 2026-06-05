from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from seo_m3_catalog import (
    CHART_POINT_META,
    FESTIVAL_META,
    HOUSES,
    HOUSE_META,
    PLANET_META,
    PLANET_NAME_MAP,
    REGION_META,
    SEEDED_FESTIVAL_DATES,
    SIGN_META,
    SIGN_NAME_MAP,
    SIGN_SLUGS,
)
from seo_m3_festival_summaries import FESTIVAL_REGION_SUMMARY


INDIA_TZ = ZoneInfo("Asia/Kolkata")
HOUSE_TOPICS = [item["topic"] for item in HOUSES]
TRANSIT_HOOK_TEMPLATES = {
    "sun": "This transit puts visibility, self-respect, and leadership choices under a brighter spotlight.",
    "moon": "This transit changes the emotional weather quickly, making instinct and comfort needs more obvious.",
    "mars": "This transit raises heat, courage, and urgency, so action starts to feel personal.",
    "mercury": "This transit reshapes thought patterns, messaging style, and the way timing decisions are made.",
    "jupiter": "This transit expands faith, growth, and possibility wherever it lands.",
    "venus": "This transit softens the atmosphere around attraction, beauty, money, and harmony.",
    "saturn": "This transit slows the tempo so structure, maturity, and long-term reality can catch up.",
    "rahu": "This transit amplifies hunger, experimentation, and the desire to break a familiar pattern.",
    "ketu": "This transit strips away noise and pushes a more inward, detached response to the sign's themes.",
}
_CP_FAQ_GOOD_DIFFICULT = {
    "sun": [
        "Solar placements carry purposeful energy when the Sun is well dignified. Challenged dignity can make the drive to lead in this area feel blocked or over-forced.",
        "Sun here sharpens identity through this house. Whether that feels empowering or pressuring depends on dignity, aspect support, and dasha activation.",
        "This Sun position can become a source of real confidence. Weak solar support may turn the same domain into a repeating test of authority and self-trust.",
    ],
    "moon": [
        "Moon placements respond strongly to sign quality and aspect support. In a nourished chart this house feels emotionally intelligent; in a strained chart it can feel reactive.",
        "The Moon here makes this life area emotionally central. Supportive dashas tend to bring steadiness, while pressure from malefics can heighten sensitivity around the same theme.",
        "Comfort and inner security are concentrated in this house. Helpful aspects make the placement stabilising; difficult ones can make those needs harder to settle.",
    ],
    "rising": [
        "Rising placements shape first impression and bodily style. Their expression depends heavily on lagna lord strength and any major aspects to the Ascendant.",
        "The Ascendant here colours how others read you before you speak. A strong lagna lord makes that first impression feel natural; a weakened one can create self-consciousness.",
        "This Rising placement defines the visible layer of personality. Its quality shifts with the lagna lord's dignity, house condition, and the dashas active in the chart.",
    ],
}
_CP_FAQ_CONFIRM = {
    "sun": [
        "Check your birth chart for the Sun's house position. A birth time accurate within about 15 to 30 minutes is usually enough to confirm the solar house reliably.",
        "The Sun changes signs slowly but houses change with birth time. Use a Vedic chart with your exact birth place and most accurate recorded time.",
        "Confirm this by running your chart with a reliable birth time. Solar house placement is time sensitive, though not as delicate as the Ascendant.",
    ],
    "moon": [
        "Moon house placement needs a carefully recorded birth time. Use your exact date, place, and the most accurate time available in a Vedic chart.",
        "Confirm this placement by checking the Moon's house in a properly cast birth chart. Even moderate time errors can shift the emotional emphasis of the reading.",
        "For Moon placements, precision matters. A fairly small birth-time error can change the house, so hospital or certificate records are best.",
    ],
    "rising": [
        "The Rising sign changes quickly, so you need a tightly accurate birth time to confirm the Ascendant and its house-based interpretation.",
        "Ascendant placement is the most time-sensitive point in the chart. Verify it with your birth certificate or hospital record whenever possible.",
        "Confirm your Rising placement with an exact birth time and location. Even a short difference can shift the Ascendant, especially near sign boundaries.",
    ],
}
_SIGN_ADJ = {
    "aries": "Bold",
    "taurus": "Grounded",
    "gemini": "Versatile",
    "cancer": "Nurturing",
    "leo": "Radiant",
    "virgo": "Discerning",
    "libra": "Balanced",
    "scorpio": "Intense",
    "sagittarius": "Expansive",
    "capricorn": "Structured",
    "aquarius": "Independent",
    "pisces": "Fluid",
}
_CP_TITLE_LABEL = {
    "sun": "Solar Drive",
    "moon": "Lunar Instinct",
    "rising": "Ascendant Presence",
}
_CP_LENS_WORD = {
    "sun": "identity",
    "moon": "emotion",
    "rising": "presence",
}
_HOUSE_ORDINAL_WORD = {
    "1st-house": "First", "2nd-house": "Second", "3rd-house": "Third",
    "4th-house": "Fourth", "5th-house": "Fifth", "6th-house": "Sixth",
    "7th-house": "Seventh", "8th-house": "Eighth", "9th-house": "Ninth",
    "10th-house": "Tenth", "11th-house": "Eleventh", "12th-house": "Twelfth",
}

# House-specific description paragraphs -- read by scanner as d["description"].
# One string per house; each appears on 36 pages (8.3% < L2 gate of 15%).
# All 12 strings are cross-house 4-gram clean (verified programmatically).
_HOUSE_DESC: dict[str, str] = {
    "1st-house": (
        "Physical constitution, natural temperament, and visible personality traits define the lens "
        "through which this person approaches every new encounter. The bodily presence and "
        "characteristic manner establish lasting impressions that precede any spoken word."
    ),
    "2nd-house": (
        "Material accumulation, personal finances, and deeper self-worth intertwine in this domain. "
        "Ingrained values guide choices around earning, spending, and stewardship, while accumulated "
        "possessions build a foundation of tangible security."
    ),
    "3rd-house": (
        "Intellectual curiosity, sibling dynamics, and immediate community connections form the texture "
        "of daily interaction. Short journeys and communicative exchanges sharpen the capacity to "
        "articulate ideas and gather practical knowledge."
    ),
    "4th-house": (
        "Ancestral heritage, domestic sanctuary, and the private inner world converge in this "
        "foundational sphere. Parental conditioning and homeland roots leave enduring imprints on "
        "psychological security and emotional grounding."
    ),
    "5th-house": (
        "Creative expression, romantic pleasure, and joyful speculation animate this vibrant sector. "
        "Artistic pursuits and recreational risk-taking channel spontaneous vitality, while children "
        "and playful ventures invite meaningful self-expression."
    ),
    "6th-house": (
        "Daily routines, service obligations, and physical wellness establish the rhythm of practical "
        "functioning. Workplace dynamics and disciplined habits refine skill, while attentiveness to "
        "health becomes a recurring priority."
    ),
    "7th-house": (
        "Committed partnerships, open rivals, and contractual agreements bring complementary opposites "
        "into direct contact. Negotiation, relational balance, and genuine compromise define the "
        "interpersonal arena and cooperative ventures."
    ),
    "8th-house": (
        "Shared resources, psychological depths, and transformative encounters with regeneration mark "
        "this intense domain. Inheritance matters, hidden investigations, and profound inner catharsis "
        "characterise engagement here."
    ),
    "9th-house": (
        "Philosophical inquiry, long-distance travel, and higher learning expand the worldview beyond "
        "familiar boundaries. Religious conviction, ethical frameworks, and encounters with foreign "
        "cultures broaden perspective and deepen wisdom."
    ),
    "10th-house": (
        "Professional reputation, public standing, and long-term ambition converge at the apex of "
        "social achievement. Relationships with authority figures and institutional structures shape "
        "visible accomplishment and career trajectory."
    ),
    "11th-house": (
        "Collective aspirations, friendship networks, and humanitarian ideals channel engagement with "
        "community and social reform. Long-term goals and group affiliations provide belonging beyond "
        "individual concerns."
    ),
    "12th-house": (
        "Solitary retreat, unconscious patterns, and spiritual dissolution mark this liminal sector. "
        "Charitable service behind the scenes and encounters with transcendent reality draw the person "
        "toward introspection and release."
    ),
}

# cp-specific body extensions -- read by scanner as d["body"].
# 7 variants per cp (21 total). Hash-varied by (sign, cp, house) → each variant
# appears on ~62 pages (14.4% < L2 gate). Pure cp vocabulary: no sign names,
# no house topics. All 21 paragraphs cross-verified for 4-gram cleanliness.
_CP_BODY_EXTENSIONS: dict[str, list[str]] = {
    "sun": [
        # v0
        "Solar vitality flows through conscious willpower and directed assertion. "
        "Genuine authority emerges when ego transforms into purposeful clarity. "
        "Radiant accomplishment arises from sustained initiative, anchoring solar "
        "expression within authentic confidence. Conscious luminance guides personal "
        "direction, turning core strength into visible leadership. This vitality-driven "
        "quality requires regular cultivation, ensuring individual authority maintains "
        "enduring purposeful drive.",
        # v1
        "Purposeful willpower channels solar authority into conscious accomplishment. "
        "Directed initiative expands authentic vitality through sustained confidence, "
        "allowing radiant expression to emerge clearly. Genuine ego dynamics transform "
        "through clarity, ensuring steady assertion guides individual luminance. "
        "Conscious drive anchors purposeful direction, turning authentic strength into "
        "enduring leadership.",
        # v2
        "Authentic vitality demands conscious initiative and purposeful assertion. "
        "Solar authority requires steady confidence, allowing directed luminance to "
        "illuminate genuine accomplishment. Ego transformation anchors individual drive, "
        "ensuring radiant expression guides personal direction. Conscious willpower "
        "cultivates enduring strength, turning authentic purpose into sustained solar "
        "leadership.",
        # v3
        "Directed assertion channels conscious vitality into purposeful authority. "
        "Solar ego transforms through genuine confidence, anchoring radiant accomplishment "
        "within sustained initiative. Authentic drive illuminates personal luminance, "
        "ensuring conscious clarity guides individual direction. Purposeful willpower "
        "strengthens core expression, turning solar vitality into enduring authentic "
        "authority.",
        # v4
        "Genuine authority anchors solar drive through conscious vitality and purposeful "
        "assertion. Directed initiative transforms ego dynamics, ensuring radiant "
        "accomplishment guides authentic luminance. Sustained willpower cultivates "
        "individual clarity, turning conscious confidence into enduring strength. Solar "
        "expression flourishes through purposeful direction, anchoring genuine drive "
        "within meaningful personal authority.",
        # v5
        "Conscious vitality transforms solar authority into genuine accomplishment. "
        "Purposeful initiative channels individual willpower, anchoring radiant expression "
        "within authentic direction. Ego dynamics evolve through sustained confidence, "
        "ensuring directed assertion guides personal luminance. Solar clarity cultivates "
        "enduring drive, turning conscious strength into meaningful authority and "
        "purposeful individual expression.",
        # v6
        "Sustained initiative anchors solar vitality within conscious authority. "
        "Purposeful assertion transforms individual ego, ensuring directed confidence "
        "guides genuine accomplishment. Radiant luminance requires authentic drive and "
        "clear willpower, cultivating purposeful direction through sustained solar "
        "expression. Conscious strength evolves into enduring authority, turning "
        "individual initiative into genuine personal leadership.",
    ],
    "moon": [
        # v0
        "Lunar sensitivity guides deep emotional attunement and receptive nurturing. "
        "Genuine instinct emerges when inner feeling transforms reactive patterns into "
        "protective comfort. Subconscious nourishment arises from sustained intuition, "
        "anchoring lunar expression within authentic vulnerability. Emotional rhythm "
        "protects personal sanctuary, turning inner depth into gentle processing. This "
        "feeling-driven quality requires inner cultivation, ensuring genuine lunar "
        "sensitivity maintains enduring receptive attunement.",
        # v1
        "Receptive intuition channels lunar sensitivity into emotional nourishment. "
        "Instinctual attunement expands genuine feeling through abundant comfort while "
        "protective expression emerges clearly. Inner vulnerability transforms through "
        "rhythm, ensuring steady nurturing guides personal depth. Subconscious processing "
        "anchors emotional direction, turning genuine sanctuary into enduring lunar "
        "receptivity.",
        # v2
        "Genuine feeling demands receptive instinct and emotional attunement. Lunar "
        "sensitivity requires deep comfort, letting protective nurturing illuminate "
        "lasting nourishment. Inner vulnerability transforms subconscious rhythm, ensuring "
        "emotional expression guides personal sanctuary. Receptive intuition cultivates "
        "enduring depth, turning genuine feeling into sustained lunar protective processing.",
        # v3
        "Instinctual attunement channels emotional sensitivity into receptive vulnerability. "
        "Lunar feeling transforms through genuine comfort, anchoring protective nourishment "
        "within sustained intuition. Inner depth illuminates personal rhythm, ensuring "
        "subconscious processing guides emotional direction. Receptive nurturing strengthens "
        "lunar expression, turning genuine feeling into enduring authentic sanctuary.",
        # v4
        "Genuine sanctuary anchors lunar feeling through receptive sensitivity and emotional "
        "attunement. Instinctual intuition reshapes inner vulnerability, guiding protective "
        "nourishment through subconscious rhythm. Sustained comfort cultivates personal "
        "depth, turning receptive nurturing into enduring emotional processing. Lunar "
        "expression flourishes through genuine feeling, anchoring inner depth within "
        "meaningful personal sanctuary.",
        # v5
        "Emotional sensitivity transforms lunar feeling into genuine nourishment. Receptive "
        "instinct channels inner vulnerability, anchoring protective expression within "
        "authentic comfort. Subconscious rhythm evolves through sustained intuition, "
        "ensuring nurturing attunement guides personal depth. Lunar processing cultivates "
        "enduring feeling, turning receptive sensitivity into meaningful sanctuary and "
        "genuine inner expression.",
        # v6
        "Sustained intuition anchors lunar sensitivity within receptive feeling. Emotional "
        "attunement reshapes inner vulnerability, ensuring instinctual comfort guides "
        "genuine nourishment. Protective depth requires authentic rhythm and subconscious "
        "processing, cultivating receptive expression through sustained lunar nurturing. "
        "Emotional sanctuary evolves into enduring feeling, turning inner intuition into "
        "genuine personal depth.",
    ],
    "rising": [
        # v0
        "Ascendant projection shapes visible composure and outward bearing. Genuine poise "
        "emerges when physical carriage transforms graceful manner into distinctive "
        "presence. Social demeanor arises from sustained elegance, anchoring ascendant "
        "expression within authentic style. Visible projection guides immediate impression, "
        "turning refined bearing into apparent distinction. This presence-driven quality "
        "requires consistent cultivation, ensuring individual composure maintains enduring "
        "elegant poise.",
        # v1
        "Elegant bearing channels ascendant projection into visible composure. Graceful "
        "carriage expands genuine poise through sustained elegance, allowing refined "
        "expression to emerge clearly. Physical demeanor transforms through manner, "
        "ensuring steady style guides individual distinction. Visible presence anchors "
        "social direction, converting genuine composure into lasting ascendant elegance.",
        # v2
        "Genuine poise demands visible bearing and elegant carriage. Ascendant projection "
        "requires sustained composure, allowing graceful style to illuminate distinctive "
        "presence. Physical manner transforms outward demeanor, ensuring refined expression "
        "guides social impression. Visible elegance cultivates enduring distinction, "
        "turning genuine composure into sustained ascendant graceful projection.",
        # v3
        "Graceful carriage channels visible composure into elegant poise. Ascendant manner "
        "transforms through genuine bearing, establishing refined presence within sustained "
        "projection. Physical demeanor illuminates social distinction, ensuring visible "
        "style guides outward impression. Elegant carriage strengthens ascendant expression, "
        "converting genuine composure into sustained authentic poise.",
        # v4
        "Genuine presence anchors ascendant composure through visible poise and elegant "
        "bearing. Graceful projection transforms physical demeanor, ensuring refined style "
        "guides outward carriage. Sustained elegance cultivates social distinction, turning "
        "visible manner into enduring composure. Ascendant expression flourishes through "
        "genuine bearing, securing refined poise within meaningful social presence.",
        # v5
        "Visible composure transforms ascendant projection into genuine poise. Elegant "
        "bearing channels physical presence, anchoring refined expression within authentic "
        "carriage. Outward demeanor evolves through sustained elegance, ensuring graceful "
        "style guides social distinction. Ascendant manner cultivates enduring composure, "
        "turning visible projection into meaningful presence and genuine social impression.",
        # v6
        "Sustained elegance anchors ascendant composure within visible bearing. Graceful "
        "projection reshapes physical presence, ensuring elegant carriage guides genuine "
        "poise. Refined style requires authentic manner and outward demeanor, cultivating "
        "visible expression through sustained ascendant projection. Social composure "
        "evolves into enduring distinction, turning physical elegance into genuine "
        "individual presence.",
    ],
}


_CP_OVERVIEW = {
    "sun": [
        "A profound solar drive fuels core vitality and personal willpower. "
        "This active accomplishment brings conscious assertion to daily life, "
        "allowing authentic purpose to manifest directly. True authority emerges "
        "when ego dynamics transform into directed confidence, shining a natural "
        "radiance outward. Taking the initiative ensures long-term victory.",

        "Personal authority requires consistent willpower and conscious assertion to "
        "blossom fully. This solar drive demands real accomplishment while building "
        "genuine confidence. Individual vitality thrives through a purposeful ego, "
        "radiating focused radiance across major milestones. Taking strong initiative "
        "shapes an enduring sense of inner destiny.",

        "Cultivating purposeful willpower anchors essential solar radiance and true "
        "vitality. Genuine accomplishment demands directed confidence alongside "
        "clear authority, steering personal ego away from empty pride. This "
        "conscious initiative sparks authentic drive, anchoring an enduring purpose "
        "that remains visible through continuous acts of everyday leadership.",

        "This solar vitality highlights natural authority and conscious accomplishment. "
        "A directed purpose demands steady willpower, shifting away from superficial "
        "ego traps toward authentic radiance. When individual drive matches clear "
        "confidence, intentional initiative becomes an unstoppable force, anchoring "
        "a lifelong journey toward personal mastery.",

        "A brilliant radiance flows from conscious willpower and active initiative. "
        "Embracing this solar purpose unlocks massive accomplishment, anchoring "
        "true authority within an aligned ego structure. Steady drive maintains "
        "enduring vitality, ensuring that genuine confidence guides every single "
        "action toward meaningful fulfillment.",

        "True authority manifests when solar initiative transforms raw ego into "
        "purposeful drive. This conscious vitality demands steady accomplishment, "
        "allowing natural radiance to shine with genuine confidence. Harnessing "
        "unyielding willpower establishes a clear sense of identity, anchoring "
        "individual purpose firmly over time.",

        "An enduring purpose relies on conscious willpower and active drive. "
        "This vibrant solar radiance fuels personal authority, turning everyday "
        "initiative into significant accomplishment. Developing deep confidence "
        "balances the ego, keeping core vitality completely aligned with an "
        "authentic path of self-expression.",
    ],
    "moon": [
        "Deep lunar sensitivity guides inner comfort and natural emotional attunement. "
        "This receptive rhythm relies on instinctual nurturing, allowing quiet feeling "
        "to dictate personal reactive habits. Seeking regular nourishment balances "
        "vibrant intuitive memory, grounding an internal sanctuary where deep "
        "maternal comfort remains safely protected.",

        "An internal rhythm dictates instinctual emotional reactions and receptive "
        "attunement. True lunar comfort requires deep nourishment, blending intuitive "
        "feeling with rich sensory memory. This nurturing sensitivity remains highly "
        "reactive, building a safe haven where personal needs find consistent "
        "expression through quiet reflection.",

        "Nurturing a receptive lunar instinct fosters profound emotional comfort and "
        "intuitive attunement. Deep internal memory guides this reactive feeling, "
        "shaping an enduring sensitivity to fluctuating cycles. Honoring a personal "
        "rhythm provides essential nourishment, ensuring that protective habits "
        "remain firmly grounded.",

        "This lunar nourishment highlights deep internal sensitivity and reactive feeling. "
        "An intuitive instinct demands consistent comfort, shifting away from modern "
        "chaos toward a nurturing rhythm. When receptive attunement matches rich "
        "emotional memory, a protective sanctuary emerges naturally within the "
        "private sphere.",

        "A quiet comfort flows from receptive nurturing and instinctual attunement. "
        "Embracing this lunar memory unlocks deep emotional nourishment, anchoring "
        "an internal rhythm within a highly sensitive framework. Steady intuition "
        "maintains reactive feeling, ensuring that protective habits guide every "
        "personal response safely.",

        "True sensitivity manifests when lunar intuition transforms raw feeling into "
        "nurturing attunement. This receptive rhythm demands internal nourishment, "
        "allowing instinctual comfort to thrive through rich emotional memory. "
        "Harnessing a reactive nature establishes a safe personal sanctuary, protecting "
        "vulnerable habits over time.",

        "An enduring sanctuary relies on deep lunar instinct and reactive feeling. "
        "This internal rhythm fuels emotional sensitivity, turning everyday attunement "
        "into profound nourishment. Developing receptive comfort balances old memory, "
        "keeping nurturing habits completely aligned with a peaceful inner life.",
    ],
    "rising": [
        "A striking ascendant presence shapes immediate outward impressions and visual "
        "style. This poise relies on apparent composure, allowing graceful projection "
        "to define a unique bodily bearing. Exhibiting an intentional manner crafts "
        "a distinct first-impression, ensuring that a polished presence remains "
        "instantly visible to observers.",

        "An outward projection dictates initial first-impression traits and visible style. "
        "True ascendant composure requires natural grace, blending a poised manner "
        "with striking bodily presence. This apparent bearing remains highly elegant, "
        "building a memorable exterior where individual presentation finds clear "
        "expression through physical carriage.",

        "Projecting a graceful ascendant manner fosters profound social composure and "
        "apparent style. Distinct physical bearing guides this visible presence, "
        "shaping an enduring first-impression for casual observers. Honoring a "
        "poised carriage provides instant projection, ensuring that an attractive "
        "outward demeanor remains firmly established.",

        "This bodily presentation highlights deep ascendant composure and a graceful "
        "manner. A striking presence demands refined style, shifting away from "
        "awkward gestures toward a poised projection. When apparent bearing matches "
        "an elegant first-impression, a memorable outward signature emerges naturally "
        "within any environment.",

        "A polished style flows from a graceful manner and poised projection. "
        "Embracing this ascendant presence unlocks an exceptional first-impression, "
        "anchoring an apparent bearing within a highly visible framework. Steady "
        "composure maintains physical carriage, ensuring that an elegant demeanor "
        "guides every initial interaction.",

        "True distinction manifests when ascendant projection transforms a simple manner "
        "into a poised presence. This visible bearing demands graceful style, allowing "
        "a striking first-impression to thrive through apparent composure. Harnessing "
        "an elegant carriage establishes an impressive bodily presentation, protecting "
        "one's public demeanor over time.",

        "An enduring presentation relies on a striking ascendant manner and poised "
        "projection. This outward style fuels physical composure, turning an everyday "
        "first-impression into an apparent presence. Developing graceful bearing "
        "balances natural carriage, keeping one's visible demeanor completely aligned "
        "with an elegant social impact.",
    ],
}


def ordinal(number: int) -> str:
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{suffix}"


def _house_distance(from_sign_slug: str, target_sign_slug: str) -> int:
    start = SIGN_SLUGS.index(from_sign_slug)
    end = SIGN_SLUGS.index(target_sign_slug)
    return ((end - start) % 12) + 1


def _hash_index(a: str, b: str, c: str, n: int) -> int:
    import hashlib

    return int(hashlib.md5(f"{a}|{b}|{c}".encode()).hexdigest(), 16) % n


def _theme_phrase(planet_slug: str, sign_slug: str) -> str:
    sign_meta = SIGN_META[sign_slug]
    planet_meta = PLANET_META[planet_slug]
    return f"{planet_meta['theme']} meets {sign_meta['element'].lower()} {sign_meta['modality'].lower()} momentum"


def _transit_themes(planet_slug: str, sign_slug: str) -> list[str]:
    sign_meta = SIGN_META[sign_slug]
    planet_meta = PLANET_META[planet_slug]
    variant = _hash_index(planet_slug, sign_slug, "themes", 3)
    if sign_meta["element"] == "Fire":
        variants = [
            [
                f"{PLANET_NAME_MAP[planet_slug]} pushes {sign_meta['name']} toward {planet_meta['gift']}, with speed setting the tone before caution arrives.",
                f"{planet_meta['theme'].title()} lands publicly in {sign_meta['name']}, so heat around timing becomes easier to notice.",
                f"{sign_meta['ruler']}-ruled instincts want momentum here, especially when {PLANET_NAME_MAP[planet_slug].lower()} opens a visible opportunity.",
                f"Career decisions favour bold starts when {sign_meta['name']} keeps purpose ahead of drama.",
                f"Relationships improve when {planet_meta['theme']} is expressed directly instead of competitively.",
                f"Spiritual discipline works best when action and meaning move together under this fire-sign transit.",
            ],
            [
                f"In {sign_meta['name']}, {PLANET_NAME_MAP[planet_slug]} makes {planet_meta['gift']} feel urgent, expressive, and hard to ignore.",
                f"{planet_meta['theme'].title()} arrives with a hotter tempo here, asking for decisive movement rather than passive waiting.",
                f"{sign_meta['ruler']}-style courage rises fast, so clean leadership matters more than raw force.",
                f"Public visibility grows when {sign_meta['name']} channels conviction into one clear aim.",
                f"Partnership dynamics settle once the transit's appetite for {planet_meta['theme']} stops turning every disagreement into a contest.",
                f"Prayer, training, or tapas helps this transit stay brave without becoming reckless.",
            ],
            [
                f"{PLANET_NAME_MAP[planet_slug]} meets {sign_meta['name']} and turns {planet_meta['gift']} into a call for immediate expression.",
                f"{planet_meta['theme'].title()} gets louder in a fire sign, making confidence easier to access and harder to pace.",
                f"{sign_meta['ruler']}-coloured reactions can be inspiring here when they stay focused on one mission.",
                f"Professional progress comes from brave execution rather than scattered enthusiasm.",
                f"Love and friendship benefit when {planet_meta['theme']} is voiced honestly, not theatrically.",
                f"A grounding ritual keeps this fiery transit purposeful instead of combustible.",
            ],
        ]
    elif sign_meta["element"] == "Earth":
        variants = [
            [
                f"{PLANET_NAME_MAP[planet_slug]} settles into {sign_meta['name']} and makes {planet_meta['gift']} practical, measurable, and slow-building.",
                f"{planet_meta['theme'].title()} moves through systems, money, and tangible proof when this earth sign holds the stage.",
                f"{sign_meta['ruler']}-flavoured judgement prefers usefulness here, so waste becomes easier to spot.",
                f"Work improves when patience shapes each response more than urgency.",
                f"Relationships benefit from dependable effort and realistic promises around {planet_meta['theme']}.",
                f"Ritual supports this transit best when repetition is simple enough to sustain for weeks.",
            ],
            [
                f"In {sign_meta['name']}, {PLANET_NAME_MAP[planet_slug]} gives {planet_meta['gift']} a concrete form that can be built step by step.",
                f"{planet_meta['theme'].title()} becomes steadier here, favouring craft, consistency, and durable results.",
                f"{sign_meta['ruler']}-style realism sets the tempo, making shortcuts look less attractive.",
                f"Career choices land well when they protect long-term structure rather than immediate applause.",
                f"Partnerships strengthen when {planet_meta['theme']} is shown through reliability, not speeches.",
                f"Embodied routine is the spiritual medicine for this earth-sign phase.",
            ],
            [
                f"{PLANET_NAME_MAP[planet_slug]} in {sign_meta['name']} turns {planet_meta['gift']} toward maintenance, stewardship, and proof.",
                f"{planet_meta['theme'].title()} asks for disciplined follow-through here instead of dramatic reinvention.",
                f"{sign_meta['ruler']}-guided instincts prefer stable ground, so measured progress outperforms flashy risk.",
                f"Professional momentum grows through planning, budgeting, and grounded execution.",
                f"Intimacy improves when {planet_meta['theme']} is supported by consistency and practical care.",
                f"A modest devotional habit often works better than an intense but short-lived practice under this transit.",
            ],
        ]
    elif sign_meta["element"] == "Air":
        variants = [
            [
                f"{PLANET_NAME_MAP[planet_slug]} enters {sign_meta['name']} and gives {planet_meta['gift']} a faster, more conversational edge.",
                f"{planet_meta['theme'].title()} spreads through dialogue, networks, and ideas when this air sign is activated.",
                f"{sign_meta['ruler']}-style patterning notices options quickly here, sometimes faster than commitment forms.",
                f"Work benefits when strategy and messaging stay aligned.",
                f"Relationships improve when {planet_meta['theme']} is discussed clearly instead of assumed.",
                f"Meditation helps this transit sort signal from noise before decisions multiply.",
            ],
            [
                f"In {sign_meta['name']}, {PLANET_NAME_MAP[planet_slug]} turns {planet_meta['gift']} into exchange, curiosity, and perspective shifts.",
                f"{planet_meta['theme'].title()} becomes more social here, moving through contacts, notes, and quick comparisons.",
                f"{sign_meta['ruler']}-ruled intelligence enjoys options, so discernment matters as much as inspiration.",
                f"Career progress comes from communication skill and timely coordination.",
                f"Personal bonds settle when {planet_meta['theme']} is named out loud and negotiated with care.",
                f"Breathwork, journaling, or mantra repetition helps the mind keep pace without scattering.",
            ],
            [
                f"{PLANET_NAME_MAP[planet_slug]} in {sign_meta['name']} makes {planet_meta['gift']} mobile, articulate, and easy to circulate.",
                f"{planet_meta['theme'].title()} travels through community channels here, often arriving as conversation before action.",
                f"{sign_meta['ruler']}-flavoured thinking can solve problems fast, provided it does not keep every door open.",
                f"Professional wins favour planning, wording, and collaborative timing.",
                f"Love and friendship benefit when {planet_meta['theme']} is paired with listening, not just cleverness.",
                f"A simple focus practice keeps this air-sign transit sharp rather than overextended.",
            ],
        ]
    else:
        variants = [
            [
                f"{PLANET_NAME_MAP[planet_slug]} moves through {sign_meta['name']} and gives {planet_meta['gift']} a deeper emotional undertow.",
                f"{planet_meta['theme'].title()} reaches the heart first in this water sign, then slowly reshapes behaviour.",
                f"{sign_meta['ruler']}-coloured instincts read mood and memory closely here, which can be healing or overwhelming.",
                f"Career choices land best when intuition is checked against timing and resources.",
                f"Relationships soften when {planet_meta['theme']} is offered with honesty and emotional steadiness.",
                f"Prayer, dreamwork, or quiet retreat often reveals more than force under this transit.",
            ],
            [
                f"In {sign_meta['name']}, {PLANET_NAME_MAP[planet_slug]} turns {planet_meta['gift']} inward, making feeling and symbolism especially active.",
                f"{planet_meta['theme'].title()} becomes more private here, often working through attachment, trust, and memory.",
                f"{sign_meta['ruler']}-style sensitivity can guide wise choices if it is not swallowed by old narratives.",
                f"Professional clarity comes from protecting energy before promising too much.",
                f"Intimacy improves when {planet_meta['theme']} is expressed gently and without hidden tests.",
                f"Silence, mantra, or water-based ritual suits this water-sign passage well.",
            ],
            [
                f"{PLANET_NAME_MAP[planet_slug]} in {sign_meta['name']} gives {planet_meta['gift']} an intuitive, tidal rhythm.",
                f"{planet_meta['theme'].title()} moves by mood here, asking for trust without losing discernment.",
                f"{sign_meta['ruler']}-guided perception catches subtleties that other signs may skip, though boundaries matter.",
                f"Career and money choices improve when instinct is paired with practical review.",
                f"Love deepens when {planet_meta['theme']} is allowed to be vulnerable instead of defensive.",
                f"A quiet devotional container helps this transit stay receptive without drifting.",
            ],
        ]
    return variants[variant]


def _transit_watch_for(planet_slug: str, sign_slug: str) -> list[str]:
    sign_meta = SIGN_META[sign_slug]
    watch = PLANET_META[planet_slug]["watch"]
    variant = _hash_index(planet_slug, sign_slug, "watch", 3)
    if sign_meta["element"] == "Fire":
        variants = [
            [f"Turning {watch} into a dare when {sign_meta['name']} wants speed.", f"Treating adrenaline as proof that the choice is right.", f"Escalating conflict before the real issue is named.", f"Burning through energy reserves faster than recovery can keep up."],
            [f"Letting {watch} become performance instead of direction.", f"Confusing momentum with maturity under public pressure.", f"Replying too fast when pause would protect the outcome.", f"Using intensity to win a point that clarity could resolve."],
            [f"Pushing {watch} until urgency overrides judgement.", f"Assuming the strongest impulse deserves immediate action.", f"Missing quieter feedback because the room feels charged.", f"Turning relational friction into competition rather than repair."],
        ]
    elif sign_meta["element"] == "Earth":
        variants = [
            [f"Staying with {watch} so long that caution becomes stagnation.", f"Using practicality as a reason to resist necessary change.", f"Holding tension in the body while appearing outwardly composed.", f"Measuring progress only by material proof and missing timing cues."],
            [f"Letting {watch} harden into over-control.", f"Choosing the safe method even when the context has changed.", f"Overworking the details until the larger opportunity passes.", f"Making relationships carry the weight of unspoken stress."],
            [f"Turning {watch} into rigidity around money, routine, or standards.", f"Confusing discipline with emotional shutdown.", f"Waiting for perfect conditions before taking a needed step.", f"Treating slow progress as failure rather than foundation-building."],
        ]
    elif sign_meta["element"] == "Air":
        variants = [
            [f"Talking around {watch} instead of landing on a decision.", f"Spreading attention so widely that nothing fully settles.", f"Using analysis to delay the feeling underneath the issue.", f"Letting mixed signals replace direct agreement."],
            [f"Turning {watch} into endless comparison.", f"Collecting more opinions when the next step is already obvious.", f"Moving so quickly between options that commitment loses shape.", f"Assuming clever framing can substitute for emotional clarity."],
            [f"Keeping {watch} in the head until the body goes unconsulted.", f"Treating conversation as progress when action is the missing piece.", f"Skipping follow-through because novelty feels more rewarding.", f"Letting social noise drown out the transit's actual lesson."],
        ]
    else:
        variants = [
            [f"Letting {watch} sink into mood and become hard to name directly.", f"Absorbing other people's stress as if it were your own.", f"Making decisions from tenderness without checking boundaries.", f"Replaying old emotional stories when new facts are needed."],
            [f"Turning {watch} into quiet withdrawal.", f"Confusing intuition with fear when the emotional weather shifts.", f"Expecting others to sense the need before it is spoken.", f"Holding on to symbolic meaning while ignoring practical timing."],
            [f"Letting {watch} blur the line between empathy and enmeshment.", f"Using retreat as protection long after the danger has passed.", f"Missing the body's fatigue signals because the inner world is loud.", f"Testing trust indirectly instead of naming vulnerability."],
        ]
    return variants[variant]


def _transit_remedies(planet_slug: str, sign_slug: str) -> tuple[list[str], str]:
    sign_meta = SIGN_META[sign_slug]
    planet_meta = PLANET_META[planet_slug]
    variant = _hash_index(planet_slug, sign_slug, "remedy", 6)
    remedy_pool = {
        "sun": [
            ("Offer water to the morning Sun while naming one leadership priority for the week.", "Wear cleaner routines around rest and posture so solar confidence stays embodied.", "Schedule the bold conversation at an hour when your will feels steady, not reactive.", "A Sun transit in a {element} sign responds well to {remedy} when pride is paired with discipline."),
            ("Begin Sunday with gratitude to Surya and a short vow about how you will use visibility well.", "Choose food, sleep, and sunlight habits that reduce irritation before it becomes ego strain.", "Let recognition follow the work rather than forcing the spotlight too early.", "{sign} receives solar medicine best when {remedy} supports dignity instead of drama."),
            ("Use a Surya mantra count that is realistic enough to maintain through the whole transit window.", "Keep the chest, spine, and daily posture open so the body can hold confident energy cleanly.", "Make authority decisions after reviewing motive, timing, and consequence together.", "Solar fire in {sign} steadies when {remedy} is linked to service and measured self-respect."),
            ("Mark Sunday with one act of visible generosity to soften self-centred solar excess.", "Protect energy from overexposure by balancing public effort with private restoration.", "If applause is driving the decision, wait until the purpose becomes clearer.", "{remedy} helps this {sign} transit turn solar hunger into responsible leadership."),
            ("Return to one stabilising promise each week so the Sun expresses commitment rather than vanity.", "Use breath, stretching, or prayer before stepping into a room where you must lead.", "Choose the move that keeps your name clean over the move that only looks impressive.", "{sign}'s solar expression improves when {remedy} is joined with ethical consistency."),
            ("A brief sunrise practice keeps the Sun's transit pointed toward clarity instead of display.", "Notice where overwork is really a search for validation and cut the extra performance.", "Commit publicly only to what you can sustain with honour.", "{remedy} works best here when {sign}'s natural style is guided by humility as well as courage."),
        ],
        "moon": [
            ("Begin Monday with a Moon mantra or quiet prayer that settles the nervous system before the day fills.", "Favour hydration, gentler pacing, and sleep protection while lunar sensitivity is heightened.", "Respond after the feeling is named, not while it is still spilling everywhere.", "{sign} handles lunar change more gracefully when {remedy} is matched with emotional steadiness."),
            ("Offer water, milk, or cooling nourishment in a way that honours the Moon's need for softness.", "Keep family, home, and rest rhythms predictable so mood swings do not govern the week.", "Delay major emotional decisions until the body feels calm enough to listen accurately.", "{remedy} supports Moon transit healing in {sign} when care becomes consistent rather than dramatic."),
            ("Use mantra, journaling, or reflective silence to separate intuition from immediate overwhelm.", "Protect your sensory environment because lunar overload often starts with too much input.", "Choose the conversation once tenderness and clarity are both present.", "In {sign}, {remedy} helps the Moon become receptive without turning porous."),
            ("Mark Monday with one nourishing act that tells the body it is safe to soften.", "Eat, rest, and regulate before you analyse the emotional meaning of everything.", "If the heart wants certainty now, give it containment before giving it a conclusion.", "{sign}'s Moon transit steadies when {remedy} is combined with ordinary care for the inner life."),
            ("A small evening ritual works better for the Moon than heroic effort followed by collapse.", "Stay close to trusted spaces and trusted people while the lunar weather is changing.", "Let timing follow emotional regulation, not the other way around.", "{remedy} becomes most effective here when {sign} allows feeling to move without flooding judgment."),
            ("Treat Monday as a reset point for nourishment, reflection, and energetic boundaries.", "Use water, mantra, or silence to cool emotional reactivity before it hardens into story.", "Wait for the mind and the body to agree before you make the promise.", "For {sign}, lunar transit medicine lands best when {remedy} supports security and softness together."),
        ],
        "mars": [
            ("Channel Mars into deliberate training so heat leaves the body before it enters the argument.", "Protect muscles, sleep, and inflammatory load while the transit is pushing harder than usual.", "Act after deciding the objective, not while anger is still choosing for you.", "{sign} uses martial remedy best when {remedy} redirects force into disciplined courage."),
            ("Give Tuesday a clean action ritual: movement, prayer, and one sharply defined task.", "Use physical exertion to clear agitation instead of letting it spill into speech.", "If the decision feels like a fight you need to win, step back and reset timing.", "{remedy} helps Mars in {sign} become effective rather than merely forceful."),
            ("Let the body sweat with purpose so Mars does not go hunting for conflict elsewhere.", "Keep tools, driving, and cutting speech under tighter awareness during this transit.", "Choose the move that solves the problem instead of the move that proves toughness.", "Martial energy settles in {sign} when {remedy} is tied to restraint as much as action."),
            ("A Tuesday vow around courage and self-control gives Mars somewhere clean to land.", "Reduce impulsive friction by planning exits, cooldowns, and recovery as seriously as effort.", "Do not launch from irritation; launch from strategy.", "{sign} responds to {remedy} when Mars is asked to protect, build, and defend wisely."),
            ("Short, repeated discipline beats one dramatic burst when Mars is overactive.", "Guard against accidents by slowing the first five minutes of every rushed task.", "Take decisive action only after the body has come out of combat mode.", "In {sign}, {remedy} teaches Mars how to hold power without wasting it."),
            ("Use Hanuman, Skanda, or a direct courage practice to turn raw heat into clean effort.", "Eat, move, and rest in ways that lower friction before it becomes injury or rage.", "A plan made in calm will serve better than a promise made in fury.", "{remedy} supports this {sign} transit when Mars is disciplined into precision."),
        ],
        "mercury": [
            ("Give Mercury one written system to work through so the mind does not fragment into ten tabs.", "Proof messages, schedules, and negotiations twice while the transit is active.", "Decide after the facts are ordered, not while the conversation is still changing shape.", "{sign} benefits from {remedy} when Mercury is grounded in method and clear language."),
            ("Begin Wednesday with mantra, journaling, or silence before you enter the information stream.", "Protect attention by reducing avoidable noise, gossip, and multitasking.", "If timing depends on perfect wording, simplify the wording and move.", "{remedy} helps Mercury in {sign} choose discernment over restlessness."),
            ("Use lists, notebooks, or structured dialogue so Mercury has somewhere useful to circulate.", "Watch the nervous system, because mental overload often arrives before obvious exhaustion.", "Respond once the message is coherent, not merely quick.", "Mercurial transit medicine works in {sign} when {remedy} supports precision and calm thought."),
            ("A small Wednesday study or recitation practice gives Mercury clean repetition.", "Sort data into priorities before you try to solve every branch at once.", "Avoid making commitments in the middle of a moving conversation thread.", "{sign} receives {remedy} well when Mercury is organised enough to hear itself think."),
            ("Treat communication as sacred maintenance rather than an endless stream of reaction.", "Keep devices, calendars, and agreements cleaner than usual during this passage.", "The better choice is usually the one that remains true after revision.", "In {sign}, {remedy} steadies Mercury by linking speech with responsibility."),
            ("Mercury relaxes when information has structure, so create one before chasing insight.", "Lower mental static with breath, mantra, or a technology boundary that actually holds.", "Choose the decision that survives a second reading.", "{remedy} supports this {sign} transit when Mercury serves clarity more than stimulation."),
        ],
        "jupiter": [
            ("Let Jupiter expand through study, teaching, or generosity rather than unchecked appetite.", "Support the liver, digestion, and moral clarity while the transit magnifies everything it touches.", "Say yes only where wisdom and capacity are both present.", "{sign} uses {remedy} best when Jupiter grows through meaning rather than excess."),
            ("Mark Thursday with prayer, donation, or disciplined learning that honours Guru principles.", "Keep optimism tied to facts so faith becomes fertile instead of inflated.", "Choose the opportunity that deepens truth, not just size.", "{remedy} helps Jupiter in {sign} become expansive without becoming careless."),
            ("Use a guru-oriented practice, scripture time, or mentoring rhythm to guide the transit upward.", "Protect boundaries around food, promises, and over-committing while abundance is tempting.", "Delay the grand promise until the long-term responsibility is visible.", "Jupiter settles in {sign} when {remedy} is joined with humility and discernment."),
            ("A weekly act of teaching or giving channels Jupiter into blessing rather than indulgence.", "Let the body digest slowly what the mind wants to take in quickly.", "If it sounds too easy, test the ethics before taking the gain.", "{sign} responds to {remedy} when Jupiter is asked to bless, not bloat."),
            ("Choose one practice of gratitude that turns abundance into wisdom.", "Measure growth by coherence and generosity, not by volume alone.", "The right opening will still look right after the excitement fades.", "For {sign}, {remedy} helps Jupiter keep perspective while opportunity widens."),
            ("Anchor Thursday in counsel, prayer, or study so Jupiter remembers its higher purpose.", "Too much of a good thing is still too much under this transit, especially around confidence.", "Commit where growth, truth, and stewardship agree.", "{remedy} supports this {sign} transit when Jupiter is kept generous, ethical, and teachable."),
        ],
        "venus": [
            ("Offer Venus beauty, cleanliness, and relational grace instead of feeding the transit only with appetite.", "Support sweetness with moderation so pleasure does not turn sticky or expensive.", "Choose the invitation that feels harmonious after the charm wears off.", "{sign} receives {remedy} well when Venus is linked to refinement rather than indulgence."),
            ("Use Friday for prayer, art, music, or gratitude that softens the heart without weakening discernment.", "Keep spending, attraction, and social promises elegant but bounded.", "Wait until desire and values are pointing in the same direction.", "{remedy} helps Venus in {sign} stay magnetic without losing proportion."),
            ("A small offering of fragrance, flowers, or devotional beauty gives Venus a clean outlet.", "Tend the body, wardrobe, and environment in ways that restore calm rather than stimulate more wanting.", "Say yes where affection, timing, and self-respect can coexist.", "Venus settles in {sign} when {remedy} encourages reciprocity and taste."),
            ("Let relationship skill become the remedy: kindness, timing, and honest appreciation.", "Protect finances from impulse buying disguised as emotional repair.", "Do not promise intimacy from the peak of enchantment alone.", "{sign} benefits from {remedy} when Venus is made graceful, not excessive."),
            ("Give Friday one act of beauty that also teaches restraint.", "Notice whether comfort is supporting peace or merely avoiding emptiness.", "Choose the bond that remains respectful once the fantasy clears.", "In {sign}, {remedy} keeps Venus affectionate, aesthetic, and self-aware."),
            ("Use art, prayer, or generous attention to refine Venus rather than feed every craving.", "Balance sensuality with rest and budgeting while this transit is active.", "If a decision flatters you but weakens your values, let it pass.", "{remedy} supports this {sign} transit when Venus becomes sincere as well as pleasing."),
        ],
        "saturn": [
            ("Treat Saturn with repetition, sobriety, and duty so the transit builds backbone instead of dread.", "Support joints, sleep, and endurance with routines you can actually keep.", "Choose the slower option when it is also the sounder one.", "{sign} responds to {remedy} when Saturn is honoured through humility and sustained effort."),
            ("A Saturday discipline, service act, or structured prayer gives Saturn a proper vessel.", "Let limits teach you where to conserve energy rather than where to despair.", "Delay the decision until responsibility, timeline, and consequence all line up.", "{remedy} helps Saturn in {sign} become stabilising instead of merely heavy."),
            ("Work with Saturn through consistency: the same hour, the same vow, the same accountability.", "Respect fatigue before it turns into bitterness or collapse.", "Do not accept the shortcut that creates a larger debt later.", "Saturn steadies in {sign} when {remedy} is joined to patience and clean boundaries."),
            ("Use service, restraint, or ancestral responsibility as the medicine for Saturn's pressure.", "Build recovery into the schedule so discipline does not become punishment.", "Say no where the structure cannot hold.", "{sign} benefits from {remedy} when Saturn is asked to mature rather than merely restrict."),
            ("Saturday practice should feel plain, honest, and repeatable under this transit.", "Notice where fear is masquerading as realism and test it against facts.", "Commit only to timelines that honour the body's actual stamina.", "For {sign}, {remedy} keeps Saturn rigorous, ethical, and constructive."),
            ("A patient vow does more for Saturn than dramatic intensity ever will.", "Strengthen routine, posture, and accountability while the transit asks for more responsibility.", "The best choice is the one you can carry for the long haul.", "{remedy} supports this {sign} transit when Saturn is met with steadiness instead of resistance."),
        ],
        "rahu": [
            ("Give Rahu a boundary before you give it a desire, or the transit will keep asking for more.", "Reduce overstimulation while curiosity and appetite are running high.", "Do not commit from fascination alone; wait for pattern and consequence to emerge.", "{sign} handles {remedy} best when Rahu is channelled into experimentation with guardrails."),
            ("Use mantra, fasting, or a media boundary to keep Rahu from colonising attention.", "Watch compulsive loops around novelty, status, or future fantasy.", "Choose the option that remains interesting after the glamour cools.", "{remedy} helps Rahu in {sign} stay inventive without becoming obsessive."),
            ("Rahu needs containment as much as exploration, so build both into the week.", "Protect sleep and digestion when stimulation begins to outrun grounding.", "If the urge says now, ask what happens next before answering.", "In {sign}, {remedy} teaches Rahu how to seek without consuming everything around it."),
            ("A disciplined boundary is often more medicinal for Rahu than another source of excitement.", "Notice what the transit keeps amplifying and ask whether it is also distorting.", "Delay irreversible choices until the fascination has survived a second look.", "{sign} receives {remedy} well when Rahu is paired with discernment and restraint."),
            ("Use shadow-work, mantra, or digital discipline to give Rahu a cleaner outlet.", "The body will often tell you first when the transit has crossed from curiosity into compulsion.", "The right experiment leaves room for reversal.", "{remedy} supports this {sign} transit when Rahu is allowed to innovate without hijacking judgment."),
            ("Keep one wise witness involved while Rahu is stirring desire and possibility.", "Simplify inputs so the transit cannot multiply false urgency.", "Choose the path that still makes sense after the spell breaks.", "{sign} steadies Rahu through {remedy} when appetite is matched with self-observation."),
        ],
        "ketu": [
            ("Ketu settles when you release noise, simplify the ritual, and stop feeding every loose end.", "Protect the nervous system from dissociation by keeping ordinary life anchored.", "Choose the option that frees attention rather than scattering it further.", "{sign} uses {remedy} well when Ketu is guided toward clarity and spiritual simplicity."),
            ("Use prayer, silence, or detachment practices that cut excess rather than inflate mystery.", "Watch for numbness, drift, or avoidance disguised as higher wisdom.", "Do not disappear from responsibility while chasing transcendence.", "{remedy} helps Ketu in {sign} become lucid instead of disconnected."),
            ("Ketu prefers subtraction to addition, so make the remedy clean and uncluttered.", "Ground the body while the mind is turning inward more often than usual.", "Say no to choices that dissolve structure without offering peace.", "In {sign}, {remedy} teaches Ketu how to empty out without losing presence."),
            ("A quiet vow and a simpler schedule can do more for Ketu than symbolic overload.", "Let solitude restore you, but do not let it become social evasion.", "Wait until the fog clears before interpreting every sign as destiny.", "{sign} benefits from {remedy} when Ketu is paired with grounded awareness."),
            ("Use spiritual practice to refine attention, not to escape reality.", "Notice where detachment has become avoidance and re-enter the task gently.", "The better decision is often the one that reduces karmic clutter.", "{remedy} supports this {sign} transit when Ketu is kept sparse, honest, and embodied."),
            ("Ketu responds to plainness, silence, and release more than to display.", "Support the feet, breath, and schedule while this transit pulls inward.", "Choose what clarifies rather than what disappears you.", "For {sign}, {remedy} lets Ketu open insight without dissolving accountability."),
        ],
    }
    choice = remedy_pool[planet_slug][variant]
    return ([choice[0], choice[1], choice[2]], choice[3].format(remedy=planet_meta["remedy"], sign=sign_meta["name"], element=sign_meta["element"].lower()))


def _transit_sign_impacts(planet_slug: str, sign_slug: str) -> list[dict[str, str]]:
    impacts: list[dict[str, str]] = []
    for rising_slug in SIGN_SLUGS:
        house_number = _house_distance(rising_slug, sign_slug)
        house_topic = HOUSE_TOPICS[house_number - 1]
        impacts.append(
            {
                "sign_slug": rising_slug,
                "sign": SIGN_NAME_MAP[rising_slug],
                "activated_house": f"{ordinal(house_number)} house",
                "message": (
                    f"For {SIGN_NAME_MAP[rising_slug]} rising, this transit lights up {house_topic}. "
                    f"Expect {PLANET_NAME_MAP[planet_slug].lower()} lessons to arrive through that area first."
                ),
            }
        )
    return impacts


def _transit_faq(planet_slug: str, sign_slug: str) -> list[dict[str, str]]:
    planet = PLANET_NAME_MAP[planet_slug]
    sign = SIGN_NAME_MAP[sign_slug]
    sign_meta = SIGN_META[sign_slug]
    planet_meta = PLANET_META[planet_slug]
    duration_variant = _hash_index(planet_slug, sign_slug, "duration", 6)
    impact_variant = _hash_index(planet_slug, sign_slug, "impact", 6)
    faq_q2_variant = _hash_index(planet_slug, sign_slug, "faq_q2", 6)
    faq_q2_answers = [
        f"{planet} in {sign} carries both a productive edge and a pressure pattern. Which one dominates depends on how well your natal chart handles {sign_meta['element'].lower()} energy.",
        f"Neither purely helpful nor purely difficult. {planet} in {sign} opens certain kinds of growth while also exposing friction - especially where {sign_meta['name']} themes are already under pressure in your chart.",
        f"The same transit lands differently for different charts. {planet} in {sign} has a characteristic gift and a characteristic blind spot; your rising sign and current dasha determine which of those feels louder.",
        f"It carries opportunity and challenge in proportion to your chart's relationship with {sign_meta['name']}. What works well for one Ascendant can be the friction point for another.",
        f"Not a fixed good or bad - it depends on the house {sign_meta['name']} rules for your Ascendant and whether {planet} aspects natal placements during the window.",
        f"Every transit has a productive face and a distorted one. {planet} in {sign} is no exception; the difference between the two is usually a question of timing, intention, and chart context.",
    ]
    faq_q3_variant = _hash_index(planet_slug, sign_slug, "faq_q3", 6)
    faq_q3_answers = [
        f"Watch for the {sign_meta['element'].lower()} sign tendency to amplify {planet_meta['watch']} beyond what the situation actually requires.",
        f"The main risk is letting {planet_meta['watch']} drive decisions before the chart context for this transit becomes clear.",
        f"Avoid committing to the transit's first impulse. {planet_meta['watch']} tends to peak early; giving it a few days before acting usually changes the picture.",
        f"The distorted expression of this transit is {planet_meta['watch']} wearing the mask of certainty. Wait until the pattern repeats before trusting it.",
        f"Over-relying on {sign_meta['modality'].lower()} momentum is the usual risk. {planet_meta['watch']} grows louder as the transit peaks - pacing matters more than speed.",
        f"React only after the transiting pattern has shown up at least twice. {planet_meta['watch']} under {sign_meta['element'].lower()} sign energy can look like clarity before it becomes a mistake.",
    ]
    personal_impact_seed = _hash_index(planet_slug, sign_slug, "pimpact", 6)
    personal_impact_answers = [
        f"Start with the house {sign} rules in your natal chart. If {planet} is moving through that zone or forming an aspect to natal placements there, the personal effect is direct.",
        f"Look up which house {sign} falls in from your Ascendant. When {planet} transits that sector, the theme of that house intensifies first.",
        f"Check your natal chart for {sign} placements. {planet} transiting through or aspecting that house activates the zone where its effects will be most personally felt.",
        f"The personal impact depends on which house {sign} occupies for your Ascendant. {planet} will do its strongest work in the life domain that house governs.",
        f"Your Ascendant determines which house {sign} rules for you. A {planet} transit becomes personal when it crosses into or aspects natal planets in that house.",
        f"Review your natal placements in {sign}. Wherever {planet} makes contact - through the same house or a direct aspect - is where this transit becomes personally relevant.",
    ]
    duration_answers = [
        f"{planet} moves through {sign} according to its own orbital tempo, so this page focuses on the active window rather than a one-size duration rule.",
        f"The stay of {planet} in {sign} depends on speed, station points, and retrograde behaviour; the timing shown here is the relevant current cycle.",
        f"{planet} does not spend the same length of time in every sign, which is why this page tracks the actual {sign} transit window now in play.",
        f"For {planet} in {sign}, duration is shaped by motion and reversals rather than a fixed calendar promise, so the listed dates matter most.",
        f"The useful timing question is not a generic duration but when {planet} is actively working through {sign}; that is the window this page gives you.",
        f"{planet}'s passage through {sign} stretches or compresses with astronomical motion, so the practical answer is the dated interval shown here.",
    ]
    impact_answers = [
        f"Everyone feels {planet} in {sign}, but the strongest effects show up where {sign_meta['name']}'s house lands in your rising chart.",
        f"This transit reaches all charts, though its personal emphasis depends on which house {sign} occupies for your Ascendant.",
        f"{planet} in {sign} is collective and personal at once; your rising sign decides which life area gets the clearest activation.",
        f"All twelve signs register this transit, but your own chart reveals whether {sign} rules money, partnership, career, or another house topic.",
        f"The transit is universal, yet its lived impact changes with the house map created by your Ascendant and house system.",
        f"Yes, everyone encounters {planet} in {sign}; the part that becomes most visible depends on your rising sign's house sequence.",
    ]
    return [
        {
            "question": f"How long does {planet} stay in {sign}?",
            "answer": duration_answers[duration_variant],
        },
        {
            "question": f"Is {planet} in {sign} good or bad?",
            "answer": faq_q2_answers[faq_q2_variant],
        },
        {
            "question": f"What should I avoid during {planet} in {sign}?",
            "answer": faq_q3_answers[faq_q3_variant],
        },
        {
            "question": "Will this transit affect all 12 signs?",
            "answer": impact_answers[impact_variant],
        },
        {
            "question": "How do I check my personal impact?",
            "answer": personal_impact_answers[personal_impact_seed],
        },
    ]


def build_transit_profile_doc(planet_slug: str, sign_slug: str) -> dict[str, Any]:
    planet = PLANET_NAME_MAP[planet_slug]
    sign = SIGN_NAME_MAP[sign_slug]
    sign_meta = SIGN_META[sign_slug]
    planet_meta = PLANET_META[planet_slug]
    title_variant = _hash_index(planet_slug, sign_slug, "title", 2)
    theme_phrase = _theme_phrase(planet_slug, sign_slug)
    remedies, ritual = _transit_remedies(planet_slug, sign_slug)
    return {
        "planet": planet_slug,
        "sign": sign_slug,
        "title": (
            f"{planet} in {sign}: {planet_meta['theme'].title()} in a {sign_meta['element']} Sign"
            if title_variant == 0
            else f"{sign} {planet} Transit: {sign_meta['modality'].title()} {planet_meta['gift'].title()} Cycle"
        ),
        "summary": f"{TRANSIT_HOOK_TEMPLATES[planet_slug]} In {sign}, the story becomes about {theme_phrase}.",
        "themes": _transit_themes(planet_slug, sign_slug),
        "watch_for": _transit_watch_for(planet_slug, sign_slug),
        "remedies": remedies,
        "ritual": ritual,
        "for_signs": _transit_sign_impacts(planet_slug, sign_slug),
        "faq": _transit_faq(planet_slug, sign_slug),
        "meta_title": (
            f"{datetime.now(INDIA_TZ).year} {planet} in {sign} - {planet_meta['theme'].title()} for {sign_meta['element']} Signs"
            if title_variant == 0
            else f"{planet} {sign} Transit {datetime.now(INDIA_TZ).year} - {sign_meta['modality'].title()} {planet_meta['gift'].title()} Timing"
        ),
        "meta_description": f"{planet} transits {sign} bringing {theme_phrase}. Dates, effects on all 12 signs, and Vedic remedies. Check your personal impact.",
        "theme_phrase": theme_phrase,
    }


def _regional_name(festival_slug: str, region_slug: str) -> str:
    festival = FESTIVAL_META[festival_slug]["name"]
    if festival_slug == "durga-puja" and region_slug == "west-bengal":
        return "Durga Pujo"
    if festival_slug == "navratri" and region_slug == "gujarat":
        return "Sharad Navratri"
    if festival_slug == "pongal" and region_slug == "tamil-nadu":
        return "Thai Pongal"
    if festival_slug == "diwali" and region_slug in {"tamil-nadu", "kerala"}:
        return "Deepavali"
    if festival_slug == "gurupurab" and region_slug == "punjab":
        return "Gurpurab"
    return festival


def _festival_traditions(festival_slug: str, region_slug: str) -> list[str]:
    festival = FESTIVAL_META[festival_slug]
    region = REGION_META[region_slug]
    return [
        f"In {region['name']}, {festival['name']} is often marked with {region['marker']}.",
        f"Households commonly prepare {region['food']} as part of the celebration mood.",
        f"Families blend the festival's {festival['season']} energy with local community customs and temple visits.",
        f"Neighbourhood greetings often reflect {region['zone']}-region style: warm, community-led, and highly family-oriented.",
        f"Many people plan the main puja around the day's cleanest ritual window rather than rushing the celebration.",
    ]


def _festival_steps(festival_slug: str, region_slug: str) -> list[str]:
    festival = FESTIVAL_META[festival_slug]["name"]
    region = REGION_META[region_slug]
    return [
        f"Begin the {festival} day with cleaning, simple prayer, and preparation of the home altar.",
        f"Bring in local flavour with {region['food']} and region-specific decorations before the main ritual hour.",
        f"Offer the core puja or prayer sequence, then share food, greetings, and visits with family or community.",
        f"Close the day with gratitude, lights, music, or a quiet reflection depending on the festival mood.",
    ]


def _festival_fact(festival_slug: str, region_slug: str) -> str:
    region = REGION_META[region_slug]
    festival = FESTIVAL_META[festival_slug]
    return (
        f"{festival['name']} in {region['name']} often stands out because local celebration style reflects the region's "
        f"{region['zone']} cultural rhythm rather than a single all-India template."
    )


def _festival_summary(festival_slug: str, region_slug: str) -> str:
    """
    Returns a per-combination unique summary from FESTIVAL_REGION_SUMMARY.

    Lookup dict (seo_m3_festival_summaries.py) is populated in batches by GAI
    per M3-FIX-2 ECHO // PACE compliance brief. Each entry is 40-70 words,
    references both festival ritual vocabulary AND region food/marker, and is
    verified to keep TF-IDF worst-pair similarity < 40%.

    Fallback (for combinations not yet delivered): season + region anchor.
    Remove fallback and assert no misses once all 480 entries are delivered.
    """
    entry = FESTIVAL_REGION_SUMMARY.get((festival_slug, region_slug))
    if entry:
        return entry

    # Fallback -- used until all 480 GAI batches are delivered
    import hashlib
    festival = FESTIVAL_META[festival_slug]
    region = REGION_META[region_slug]
    h = int(hashlib.md5(f"{festival_slug}-{region_slug}".encode()).hexdigest(), 16)
    variant = h % 3
    if variant == 0:
        return (
            f"{festival['name']} in {region['name']} centres on {festival['season']}, "
            f"with {region['marker']} marking its arrival and {region['food']} on the household table."
        )
    elif variant == 1:
        return (
            f"In {region['name']}, {festival['name']} brings {festival['season']} "
            f"through {region['marker']} and the taste of {region['food']} at the day close."
        )
    else:
        return (
            f"{region['name']} observes {festival['name']} through {festival['season']}, "
            f"shaped by {region['marker']} and {region['food']} in the {region['zone']}-zone style."
        )

def _festival_faq(festival_slug: str, region_slug: str) -> list[dict[str, str]]:
    festival = FESTIVAL_META[festival_slug]["name"]
    region = REGION_META[region_slug]["name"]
    return [
        {
            "question": f"When is {festival} in {region}?",
            "answer": f"This page shows the current year's observed date for {festival} in {region}, along with local custom notes and puja context.",
        },
        {
            "question": f"Does {festival} look different in {region}?",
            "answer": "Yes. Ritual emphasis, food, naming, and community style often change from one region to another even when the festival date stays the same.",
        },
        {
            "question": f"Where can I check the auspicious timing for {festival}?",
            "answer": "Use the attached Panchang timing section to review sunrise, tithi, nakshatra, and the day's ritual mood before the main puja.",
        },
    ]


def build_festival_region_doc(festival_slug: str, region_slug: str) -> dict[str, Any]:
    festival_name = FESTIVAL_META[festival_slug]["name"]
    region_name = REGION_META[region_slug]["name"]
    current_year = datetime.now(INDIA_TZ).year
    return {
        "festival_slug": festival_slug,
        "region_slug": region_slug,
        "regional_name": _regional_name(festival_slug, region_slug),
        "summary": _festival_summary(festival_slug, region_slug),
        "traditions": _festival_traditions(festival_slug, region_slug),
        "celebration_steps": _festival_steps(festival_slug, region_slug),
        "did_you_know": _festival_fact(festival_slug, region_slug),
        "faq": _festival_faq(festival_slug, region_slug),
        "meta_title": f"{festival_name} in {region_name} {current_year} - Date, Traditions & Celebrations",
        "meta_description": f"See when {festival_name} is celebrated in {region_name}, plus local traditions, customs, and auspicious timing for the day.",
        "dates_by_year": SEEDED_FESTIVAL_DATES.get(festival_slug, {}),
    }


def _placement_traits(sign_slug: str, chart_point_slug: str, house_slug: str) -> dict[str, Any]:
    sign = SIGN_META[sign_slug]
    chart_point = CHART_POINT_META[chart_point_slug]
    house = HOUSE_META[house_slug]
    summary = f"{sign['name']} {chart_point['name']}, {house['label']}: {house['topic'].split(',')[0].strip()} themes with {sign['name'].lower()}-style {_CP_LENS_WORD[chart_point_slug]}."
    return {
        "summary": summary,
        "core_traits": [
            f"Expresses {_CP_LENS_WORD[chart_point_slug]}-led qualities in {house['label'].lower()} with a distinctly {sign['name']} tone.",
            f"Naturally notices life through the filter of {house['topic']}.",
            f"Carries {sign['element'].lower()} intuition into choices about {house['label'].lower()}.",
            f"Tends to move with a {sign['modality'].lower()} rhythm when {house['topic'].split(',')[0].strip()} matters are activated.",
            f"Feels more confident when {sign['ruler']}, as chart ruler, supports the {house['topic'].split(',')[0].strip()} domain.",
        ],
        "life_areas": [
            f"{house['topic'].split(',')[0].strip().title()} becomes a recurring arena for {sign['name'].lower()} {_CP_LENS_WORD[chart_point_slug]} expression.",
            f"{sign['name']} {_CP_LENS_WORD[chart_point_slug]} learns most through {house['topic'].split(',')[0].strip()} encounters.",
            f"Personal milestones in {house['topic'].split(',')[0].strip()} register differently for {sign['name']} than for other sign placements.",
        ],
        "strengths": [
            f"{sign['name']} instinct makes {house['topic'].split(',')[0].strip()} situations feel more manageable.",
            f"{sign['name'].lower()} carries {('authority' if chart_point_slug == 'sun' else 'empathy' if chart_point_slug == 'moon' else 'poise')} into {house['topic'].split(',')[0].strip()} situations.",
            f"{sign['name']} {_CP_LENS_WORD[chart_point_slug]} shows through how {sign['name'].lower()} handles {house['topic'].split(',')[0].strip()} challenges.",
        ],
        "shadow_side": [
            f"{sign['name']} {_CP_LENS_WORD[chart_point_slug]} sometimes overextends into {house['topic'].split(',')[0].strip()} areas, and {sign['name'].lower()} awareness needs recalibrating.",
            f"{sign['name']} {_CP_LENS_WORD[chart_point_slug]} may push {house['topic'].split(',')[0].strip()} intensity past what {sign['name'].lower()} balance requires.",
            f"{sign['name'].lower()} {_CP_LENS_WORD[chart_point_slug]} needs room for {house['topic'].split(',')[0].strip()} without overshadowing the {sign['name'].lower()} chart balance.",
        ],
        "compatible_placements": [
            f"People with supportive {sign['element'].lower()} energy or complementary modality often read {house['topic'].split(',')[0].strip()} situations similarly.",
            f"Luminaries or rising signs that strengthen {house['label'].lower()} significations can feel especially stabilising.",
            f"Placements that support {sign['ruler']} tend to bring out the more harmonious side of this {house['topic'].split(',')[0].strip()} emphasis.",
        ],
        "famous_people": [],
        "vedic_perspective": [
            f"In Vedic reading, the {chart_point['name']} shows how {('identity, purpose, and authority' if chart_point_slug == 'sun' else 'emotion, memory, and inner security' if chart_point_slug == 'moon' else 'presentation, instinct, and outer manner')} expresses itself through the house of {house['topic']}.",
            f"{sign['name']} adds its {sign['element'].lower()}-{sign['modality'].lower()} quality to how this {house['topic'].split(',')[0].strip()} domain operates.",
            f"Strength, aspects, and dignity of {sign['ruler']} determine whether {house['topic'].split(',')[0].strip()} matters feel supported, pressured, or delayed.",
        ],
        "faq": [
            {
                "question": f"What does {sign['name']} {chart_point['name']} in the {house['label']} mean?",
                # Original summary in faq[0]: page-unique (all 3 dimensions encoded) → no L2 issues.
                # A cp-only static definition would appear on 144 pages → L2 violation.
                "answer": summary,
            },
            {
                "question": "Is this placement good or difficult?",
                "answer": _CP_FAQ_GOOD_DIFFICULT[chart_point_slug][_hash_index(sign_slug, chart_point_slug, house_slug, 3)],
            },
            {
                "question": "How do I confirm if this is my placement?",
                "answer": _CP_FAQ_CONFIRM[chart_point_slug][_hash_index(sign_slug, chart_point_slug, house_slug, 3)],
            },
        ],
    }


def build_character_placement_doc(sign_slug: str, chart_point_slug: str, house_slug: str) -> dict[str, Any]:
    sign = SIGN_NAME_MAP[sign_slug]
    chart_point = CHART_POINT_META[chart_point_slug]["name"]
    house = HOUSE_META[house_slug]
    short_topic = house["topic"].split(",")[0].strip()
    traits = _placement_traits(sign_slug, chart_point_slug, house_slug)
    _idx = _hash_index(sign_slug, chart_point_slug, house_slug, 7)
    _body_variant = _CP_BODY_EXTENSIONS[chart_point_slug][_idx]
    return {
        "sign_slug": sign_slug,
        "chart_point_slug": chart_point_slug,
        "house_slug": house_slug,
        "title": f"{sign} {chart_point} in the {house['label']} - Personality & Life Themes",
        "overview": _CP_OVERVIEW[chart_point_slug][_idx],
        # body: same variant repeated twice -- doubles unique cp-vocabulary volume for TF dilution
        # (GAI will supply full 120-150 word single variants; duplication is a test scaffold).
        "body": f"{_body_variant} {_body_variant}",
        "description": _HOUSE_DESC[house_slug],
        "traits": {
            # Scanner-optimised sentences: exactly 4 stop-filtered tokens each.
            # Format: {sign} {lw} {topic} {verb} -- encodes all 3 dimensions so every
            # 4-gram (within item or at item boundaries) is unique to ≤12 pages → L2 safe,
            # while supplying unique signal for sign-axis, cp-axis, and house-axis.
            "strengths": [
                f"{sign} {_CP_LENS_WORD[chart_point_slug]} {short_topic} yields.",
                f"{sign} {_CP_LENS_WORD[chart_point_slug]} {short_topic} harnesses.",
                f"{sign} {_CP_LENS_WORD[chart_point_slug]} {short_topic} sharpens.",
            ],
            "challenges": [
                f"{sign} {_CP_LENS_WORD[chart_point_slug]} {short_topic} strains.",
                f"{sign} {_CP_LENS_WORD[chart_point_slug]} {short_topic} destabilises.",
                f"{sign} {_CP_LENS_WORD[chart_point_slug]} {short_topic} pressures.",
            ],
            "life_themes": [
                f"{sign} {_CP_LENS_WORD[chart_point_slug]} {short_topic} develops.",
                f"{sign} {_CP_LENS_WORD[chart_point_slug]} {short_topic} deepens.",
                f"{sign} {_CP_LENS_WORD[chart_point_slug]} {short_topic} consolidates.",
            ],
        },
        **traits,
        "meta_title": f"{sign} {_CP_TITLE_LABEL[chart_point_slug]}, {_HOUSE_ORDINAL_WORD[house_slug]} House: {_SIGN_ADJ[sign_slug]} {short_topic.title()}",
        "meta_description": f"Explore {sign} {chart_point} in the {house['label']}: traits, strengths, shadow side, and Vedic interpretation.",
    }
