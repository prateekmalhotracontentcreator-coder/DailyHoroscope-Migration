from __future__ import annotations

import json
import os
import re
from typing import Any


FAST_MODEL = "claude-3-5-haiku-20241022"

_CODE_FENCE_PATTERN = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)

HAND_ARCHETYPES: dict[str, dict[str, str]] = {
    "Earth": {
        "summary": "steady, practical, and materially grounded",
        "personality": "an earthy temperament that values stability, reliability, and direct effort",
        "career": "patient building, operational strength, and results earned through consistency",
        "love": "loyal affection expressed through presence, duty, and tangible care",
        "spiritual": "embodied discipline rather than abstract mysticism",
    },
    "Air": {
        "summary": "mental, observant, and idea-driven",
        "personality": "an airy temperament that processes life through thought, pattern, and communication",
        "career": "strategy, analysis, teaching, advising, and systems thinking",
        "love": "connection through conversation, mental rapport, and emotional clarity",
        "spiritual": "study, reflection, and insight-led growth",
    },
    "Fire": {
        "summary": "dynamic, expressive, and action-led",
        "personality": "a fiery temperament that acts with conviction, momentum, and visible presence",
        "career": "leadership, initiative, courageous risk-taking, and visible achievement",
        "love": "warmth, directness, and passionate emotional expression",
        "spiritual": "willpower, tapas, and disciplined assertion",
    },
    "Water": {
        "summary": "sensitive, intuitive, and impressionable",
        "personality": "a watery temperament that absorbs atmosphere deeply and responds through feeling and intuition",
        "career": "creative, caring, healing, and people-sensitive work",
        "love": "emotional devotion, receptivity, and strong inner bonds",
        "spiritual": "bhakti, imagination, and inner-symbolic awareness",
    },
}

MOUNT_GUIDANCE: dict[str, dict[str, str]] = {
    "Base of index finger (Jupiter)": {
        "planet": "Jupiter",
        "quality": "ambition, dignity, guidance, and dharmic expansion",
        "career": "teaching, leadership, advising, management, and roles where judgment matters",
        "love": "high standards, protective affection, and a desire for respect in partnership",
        "wealth": "growth through wisdom, reputation, and principled decision-making",
        "gemstone": "Yellow sapphire for Jupiter, worn in gold on the index finger after suitability guidance.",
        "mantra": "Om Brim Brihaspataye Namah for Jupiter, 108 repetitions on Thursdays.",
        "colour": "Yellow or saffron, reflecting Jupiter's expansive and sattvic current.",
        "practice": "Offer guidance, teach, or donate something useful on Thursdays to strengthen benefic Jupiter.",
    },
    "Base of middle finger (Saturn)": {
        "planet": "Saturn",
        "quality": "discipline, realism, endurance, and karmic seriousness",
        "career": "structured work, research, engineering, persistence-heavy callings, and long-cycle mastery",
        "love": "reserved loyalty, caution in trust, and maturity through tested bonds",
        "wealth": "slow but durable accumulation through discipline, order, and patience",
        "gemstone": "Blue sapphire for Saturn, worn only after proper suitability checking, traditionally in steel or silver.",
        "mantra": "Om Sham Shanicharaya Namah for Saturn, 108 repetitions on Saturdays.",
        "colour": "Indigo, navy, or deep blue, reflecting Saturn's sober and karmic field.",
        "practice": "Keep one non-negotiable daily discipline and serve the elderly, poor, or burdened to harmonize Saturn.",
    },
    "Base of ring finger (Sun)": {
        "planet": "Sun",
        "quality": "visibility, confidence, recognition, and radiance",
        "career": "public-facing work, authority, creative recognition, and reputation-led advancement",
        "love": "warm-hearted expression, pride, and the need to feel seen and appreciated",
        "wealth": "prosperity linked to visibility, self-belief, and strong personal presence",
        "gemstone": "Ruby for the Sun, worn in gold on the ring finger on a Sunday morning.",
        "mantra": "Om Hram Hreem Hraum Suryaya Namah for the Sun, 108 repetitions at sunrise.",
        "colour": "Gold, saffron, or deep orange, reflecting Surya's radiant current.",
        "practice": "Offer water to the rising Sun each morning to stabilize confidence and clear inner dullness.",
    },
    "Base of pinky (Mercury)": {
        "planet": "Mercury",
        "quality": "intelligence, language, adaptability, and trade skill",
        "career": "communication, commerce, writing, negotiation, consulting, and agile problem-solving",
        "love": "needs wit, dialogue, and quick understanding in close bonds",
        "wealth": "prosperity through skill, business sense, networking, and timing",
        "gemstone": "Emerald for Mercury, worn in gold or silver on the little finger on a Wednesday.",
        "mantra": "Om Bum Budhaya Namah for Mercury, 108 repetitions on Wednesdays.",
        "colour": "Green, reflecting Budha's clarity, learning, and commercial intelligence.",
        "practice": "Write, study, or refine communication daily so Mercury's gifts become disciplined rather than scattered.",
    },
    "Base of thumb (Venus)": {
        "planet": "Venus",
        "quality": "affection, pleasure, magnetism, and relational warmth",
        "career": "beauty, hospitality, design, care, diplomacy, and attraction-based success",
        "love": "strong attachment, romance, sensuality, and a desire for harmony",
        "wealth": "comfort, enjoyment, and gains through taste, refinement, and social ease",
        "gemstone": "White opal for Venus, worn in silver on a Friday after purification.",
        "mantra": "Om Shum Shukraya Namah for Venus, 108 repetitions on Fridays.",
        "colour": "White, pastel pink, or soft cream, reflecting Venusian harmony and refinement.",
        "practice": "Keep one daily act of beauty, cleanliness, or relationship repair to keep Venus balanced and gracious.",
    },
    "Lower palm opposite thumb (Moon)": {
        "planet": "Moon",
        "quality": "imagination, receptivity, intuition, and emotional tides",
        "career": "healing, writing, travel, care work, psychology, and imaginative vocations",
        "love": "deep feeling, tenderness, and emotional fluctuation that needs safety",
        "wealth": "flow-based prosperity influenced by mood, timing, and relational trust",
        "gemstone": "Pearl for the Moon, worn in silver on the little finger or ring finger on a Monday.",
        "mantra": "Om Som Somaya Namah for the Moon, 108 repetitions on Mondays.",
        "colour": "White or silver, reflecting Chandra's cooling and receptive current.",
        "practice": "Create a calming evening ritual with water, moonlight, or quiet reflection to steady the lunar mind.",
    },
    "Centre of palm (Plain of Mars)": {
        "planet": "Mars",
        "quality": "courage, resilience, response under pressure, and battlefield stamina",
        "career": "initiative, defense, competition, crisis handling, and roles that reward nerve",
        "love": "direct intensity, protectiveness, and occasional friction if energy is unmanaged",
        "wealth": "gains through decisive action, courage, and disciplined use of force",
        "gemstone": "Red coral for Mars, worn in gold or copper on the ring finger on a Tuesday.",
        "mantra": "Om Kraam Kreem Kraum Sah Bhaumaya Namah for Mars, 108 repetitions on Tuesdays.",
        "colour": "Red or rust, reflecting Mars' heat, drive, and protective force.",
        "practice": "Channel Mars through daily disciplined movement so assertion stays constructive rather than reactive.",
    },
}

LIFE_LINE_GUIDANCE = {
    "Long & deep": "strong reserves, stamina, and the ability to recover after strain",
    "Short or faint": "energy that must be managed consciously, with rhythm mattering more than brute force",
    "Broken or chained": "phases of fluctuating vitality, restlessness, or marked life transitions",
    "Forked at the end": "later-life changes, travel signatures, or a split in life direction over time",
}

HEART_LINE_GUIDANCE = {
    "Long & curved upward": "warm feeling, expressive affection, and emotional generosity",
    "Straight across": "self-control in feeling, loyalty, and a more measured style of attachment",
    "Short": "selective emotional expression and a guarded heart that opens carefully",
    "Broken or chained": "emotional sensitivity, relationship lessons, and fluctuating feelings",
}

HEAD_LINE_GUIDANCE = {
    "Straight & horizontal": "practical logic, realism, and linear thinking",
    "Sloping downward": "imagination, intuition, and symbolic or creative thinking",
    "Short & straight": "quick decisions, direct thought, and a concise mental style",
    "Forked at the end": "dual perspective, adaptability, and the ability to bridge logic with intuition",
}

FATE_LINE_GUIDANCE = {
    "Strong & clear": "a defined vocational thread and a clearer sense of worldly direction",
    "Faint or partial": "a self-made path with changes, experimentation, or non-linear timing",
    "Not visible": "freedom from a fixed outer script, with destiny shaped through choice more than institution",
}

THUMB_GUIDANCE = {
    "Long & flexible": "strong will joined with adaptability and social intelligence",
    "Long & stiff": "strong will, firmness, and a tendency toward rigidity once decided",
    "Short": "responsive instinct, softer assertion, and motivation that rises through encouragement",
    "Waisted (narrowed at middle)": "diplomacy, tact, and fluctuating resolve between desire and judgment",
}

FINGER_STYLE_GUIDANCE = {
    "Smooth (no prominent knots at joints)": "intuitive action, spontaneous judgment, and feeling-led response",
    "Knotty (prominent joints)": "analysis, method, and the need to understand before committing",
    "Tapering toward tips": "aesthetic sensitivity, impressionability, and refined taste",
    "Spatulate (wider at tips)": "inventive energy, experimentation, and practical originality",
}

HAND_TEXTURE_GUIDANCE = {
    "Soft & fine": "receptivity, sensitivity, and a refined nervous system",
    "Firm & elastic": "balanced vitality, resilience, and practical responsiveness",
    "Rough or coarse": "physical endurance, blunt realism, and direct engagement with the world",
}

SPECIAL_MARK_GUIDANCE = {
    "Star or asterisk on a mount": "a sudden intensification of the planetary influence of the marked area",
    "Triangle on a mount": "focused intelligence and constructive use of the planet linked to that area",
    "Cross or X": "a karmic lesson, obstacle, or testing pattern around the marked field",
    "Ring around a finger base": "pressure, fixation, or over-concentration around that planet's domain",
    "None visible": "the reading rests more on the major lines, shape, and mount balance than on special signs",
}


def _clean_json_text(text: str) -> str:
    stripped = text.strip()
    stripped = _CODE_FENCE_PATTERN.sub("", stripped)
    return stripped.strip()


def _extract_text_from_claude_response(response: Any) -> str | None:
    content = getattr(response, "content", None)
    if not content:
        return None
    text_parts: list[str] = []
    for item in content:
        text_value = getattr(item, "text", None)
        if text_value:
            text_parts.append(text_value)
    text = "\n".join(text_parts).strip()
    return text or None


async def _anthropic_client():
    try:
        from anthropic import AsyncAnthropic  # type: ignore
    except Exception:
        return None

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    return AsyncAnthropic(api_key=api_key)


async def _call_json(prompt: str, *, model: str, max_tokens: int, temperature: float = 0.35) -> Any:
    client = await _anthropic_client()
    if client is None:
        return None

    try:
        response = await client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        )
    except Exception:
        return None

    text = _extract_text_from_claude_response(response)
    if not text:
        return None

    try:
        return json.loads(_clean_json_text(text))
    except Exception:
        return None


def _clean_value(value: str | None, fallback: str) -> str:
    cleaned = str(value or "").strip()
    return cleaned or fallback


def _mount_payload(dominant_mount: str) -> dict[str, str]:
    return MOUNT_GUIDANCE.get(dominant_mount, MOUNT_GUIDANCE["Centre of palm (Plain of Mars)"])


def _archetype_payload(hand_shape: str) -> dict[str, str]:
    return HAND_ARCHETYPES.get(hand_shape, HAND_ARCHETYPES["Earth"])


def _context(
    *,
    user_name: str | None,
    dominant_hand: str,
    palm_shape: str | None,
    hand_shape: str,
    finger_length: str,
    life_line: str,
    heart_line: str,
    head_line: str,
    fate_line: str,
    dominant_mount: str,
    thumb_type: str,
    finger_style: str,
    hand_texture: str,
    special_marks: str,
    scripture_mode: str | None,
) -> dict[str, Any]:
    mount = _mount_payload(dominant_mount)
    archetype = _archetype_payload(hand_shape)
    name = _clean_value(user_name, "The native")
    return {
        "user_name": name,
        "dominant_hand": dominant_hand,
        "palm_shape": _clean_value(palm_shape, "Not specified"),
        "hand_shape": hand_shape,
        "finger_length": finger_length,
        "life_line": life_line,
        "heart_line": heart_line,
        "head_line": head_line,
        "fate_line": fate_line,
        "dominant_mount": dominant_mount,
        "thumb_type": thumb_type,
        "finger_style": finger_style,
        "hand_texture": hand_texture,
        "special_marks": special_marks,
        "scripture_mode": _clean_value(scripture_mode, "VEDIC"),
        "mount_planet": mount["planet"],
        "mount_quality": mount["quality"],
        "mount_career": mount["career"],
        "mount_love": mount["love"],
        "mount_wealth": mount["wealth"],
        "hand_summary": archetype["summary"],
        "hand_personality": archetype["personality"],
        "hand_career": archetype["career"],
        "hand_love": archetype["love"],
        "hand_spiritual": archetype["spiritual"],
        "life_line_reading": LIFE_LINE_GUIDANCE.get(life_line, LIFE_LINE_GUIDANCE["Long & deep"]),
        "heart_line_reading": HEART_LINE_GUIDANCE.get(heart_line, HEART_LINE_GUIDANCE["Long & curved upward"]),
        "head_line_reading": HEAD_LINE_GUIDANCE.get(head_line, HEAD_LINE_GUIDANCE["Straight & horizontal"]),
        "fate_line_reading": FATE_LINE_GUIDANCE.get(fate_line, FATE_LINE_GUIDANCE["Strong & clear"]),
        "thumb_reading": THUMB_GUIDANCE.get(thumb_type, THUMB_GUIDANCE["Long & flexible"]),
        "finger_style_reading": FINGER_STYLE_GUIDANCE.get(finger_style, FINGER_STYLE_GUIDANCE["Smooth (no prominent knots at joints)"]),
        "hand_texture_reading": HAND_TEXTURE_GUIDANCE.get(hand_texture, HAND_TEXTURE_GUIDANCE["Firm & elastic"]),
        "special_marks_reading": SPECIAL_MARK_GUIDANCE.get(special_marks, SPECIAL_MARK_GUIDANCE["None visible"]),
        "mount": mount,
    }


def _fallback_report(context: dict[str, Any]) -> dict[str, Any]:
    mount = context["mount"]
    overview = (
        f"This {context['hand_shape'].lower()} hand shows a clear {context['mount_planet']} emphasis through the prominence of the "
        f"{context['dominant_mount'].lower()}. The palm combines {context['hand_summary']} qualities with a Life Line that suggests "
        f"{context['life_line_reading']} and a Head Line that points to {context['head_line_reading']}."
    )
    personality = (
        f"In Samudrika Shastra, this hand reads as {context['hand_personality']}. The raised {context['dominant_mount'].lower()} adds "
        f"{context['mount_quality']} to the temperament. A {context['thumb_type'].lower()} thumb shows {context['thumb_reading']}, "
        f"while {context['finger_style'].lower()} fingers add {context['finger_style_reading']}. The {context['hand_texture'].lower()} texture "
        f"further suggests {context['hand_texture_reading']} in day-to-day response."
    )
    career_purpose = (
        f"The Fate Line appears {context['fate_line'].lower()}, which points to {context['fate_line_reading']}. The Head Line is "
        f"{context['head_line'].lower()}, so work decisions are shaped by {context['head_line_reading']}. Because the dominant mount is linked "
        f"to {context['mount_planet']}, career fulfillment grows through {mount['career']}. This gives the life path a tone of "
        f"{context['hand_career']} rather than random movement."
    )
    love_relationships = (
        f"The Heart Line is {context['heart_line'].lower()}, showing {context['heart_line_reading']}. The hand type itself favors "
        f"{context['hand_love']}, while the prominence of {context['mount']['planet']} adds {mount['love']}. This combination suggests that "
        f"relationship karma deepens when affection is matched with steadiness and emotional honesty."
    )
    health_vitality = (
        f"The Life Line indicates {context['life_line_reading']}, so vitality is best protected through rhythm rather than excess. "
        f"The {context['hand_texture'].lower()} texture and {context['thumb_type'].lower()} thumb show {context['hand_texture_reading']} and "
        f"{context['thumb_reading']}. In Vedic terms, this hand benefits when personal energy is used deliberately and not scattered."
    )
    wealth_prosperity = (
        f"The wealth pattern rests on a Fate Line that is {context['fate_line'].lower()}, pointing to {context['fate_line_reading']}. "
        f"Since {context['mount_planet']} is strongest, prosperity is supported through {mount['wealth']}. Financial growth looks better when "
        f"skill and planetary discipline are allowed to mature gradually."
    )
    spiritual_karmic = (
        f"Spiritually, the hand carries {context['hand_spiritual']} as its deeper path. The special mark pattern reads as "
        f"{context['special_marks_reading']}, and the dominant mount shows that karmic lessons are especially colored by {context['mount_planet']}. "
        f"This is a hand that matures through conscious self-observation rather than superficial luck-seeking."
    )
    remedies = {
        "gemstone": mount["gemstone"],
        "mantra": mount["mantra"],
        "colour": mount["colour"],
        "practice": mount["practice"],
    }
    return {
        "overview": overview,
        "personality": personality,
        "career_purpose": career_purpose,
        "love_relationships": love_relationships,
        "health_vitality": health_vitality,
        "wealth_prosperity": wealth_prosperity,
        "spiritual_karmic": spiritual_karmic,
        "remedies": remedies,
    }


def _coerce_report(content: Any, fallback: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(content, dict):
        return fallback

    remedies = content.get("remedies")
    fallback_remedies = fallback["remedies"]
    remedy_values = remedies if isinstance(remedies, dict) else {}
    return {
        "overview": str(content.get("overview") or fallback["overview"]),
        "personality": str(content.get("personality") or fallback["personality"]),
        "career_purpose": str(content.get("career_purpose") or fallback["career_purpose"]),
        "love_relationships": str(content.get("love_relationships") or fallback["love_relationships"]),
        "health_vitality": str(content.get("health_vitality") or fallback["health_vitality"]),
        "wealth_prosperity": str(content.get("wealth_prosperity") or fallback["wealth_prosperity"]),
        "spiritual_karmic": str(content.get("spiritual_karmic") or fallback["spiritual_karmic"]),
        "remedies": {
            "gemstone": str(remedy_values.get("gemstone") or fallback_remedies["gemstone"]),
            "mantra": str(remedy_values.get("mantra") or fallback_remedies["mantra"]),
            "colour": str(remedy_values.get("colour") or fallback_remedies["colour"]),
            "practice": str(remedy_values.get("practice") or fallback_remedies["practice"]),
        },
    }


def _prompt(context: dict[str, Any]) -> str:
    evidence = {
        "user_name": context["user_name"],
        "dominant_hand": context["dominant_hand"],
        "palm_shape": context["palm_shape"],
        "derived_hand_shape": context["hand_shape"],
        "finger_length": context["finger_length"],
        "life_line": context["life_line"],
        "heart_line": context["heart_line"],
        "head_line": context["head_line"],
        "fate_line": context["fate_line"],
        "dominant_mount": context["dominant_mount"],
        "thumb_type": context["thumb_type"],
        "finger_style": context["finger_style"],
        "hand_texture": context["hand_texture"],
        "special_marks": context["special_marks"],
        "interpretive_notes": {
            "hand_shape": context["hand_summary"],
            "mount_planet": context["mount_planet"],
            "mount_quality": context["mount_quality"],
            "life_line": context["life_line_reading"],
            "heart_line": context["heart_line_reading"],
            "head_line": context["head_line_reading"],
            "fate_line": context["fate_line_reading"],
            "thumb": context["thumb_reading"],
            "finger_style": context["finger_style_reading"],
            "texture": context["hand_texture_reading"],
            "special_marks": context["special_marks_reading"],
        },
    }

    return f"""
You are the Samudrika Shastra palm reader for Everyday Horoscope.

This is explicitly Vedic palmistry, not Western palmistry.

Core rules:
- Return valid JSON only. No markdown, no code fences, no preamble.
- Use only the evidence provided. Every section must be directly anchored in the questionnaire answers.
- Never use generic horoscope filler, vague fate language, or stock personality fluff.
- Mention the derived hand type and dominant planetary influence clearly.
- Read mounts through Jyotish planets:
  Jupiter = base of index finger
  Saturn = base of middle finger
  Sun/Apollo = base of ring finger
  Mercury = base of little finger
  Venus = base of thumb
  Mars = plain/central martial field
  Moon = lower palm opposite thumb
- Read lines in their planetary context:
  Heart Line = Venus/Moon
  Head Line = Mercury/Jupiter
  Life Line = Mars/Venus
  Fate Line = Saturn
- Remedies must remain planetary and Jyotish-consistent: gemstone, mantra, colour, practice.
- Avoid fatalism and avoid medical diagnosis.

Write in a premium, spiritually precise, grounded tone for a modern user.

Evidence:
{json.dumps(evidence, ensure_ascii=True, indent=2)}

Return this exact JSON structure:
{{
  "overview": "2-3 sentences",
  "personality": "3-4 sentences",
  "career_purpose": "3-4 sentences",
  "love_relationships": "3-4 sentences",
  "health_vitality": "2-3 sentences",
  "wealth_prosperity": "2-3 sentences",
  "spiritual_karmic": "2-3 sentences",
  "remedies": {{
    "gemstone": "primary stone + planet + how to wear",
    "mantra": "mantra + planet + repetitions",
    "colour": "lucky colour + planetary basis",
    "practice": "one practical daily recommendation"
  }}
}}
""".strip()


async def generate_hasta_rekha_report(
    *,
    user_name: str | None,
    dominant_hand: str,
    palm_shape: str | None,
    hand_shape: str,
    life_line: str,
    heart_line: str,
    head_line: str,
    fate_line: str,
    dominant_mount: str,
    thumb_type: str,
    finger_length: str,
    finger_style: str,
    hand_texture: str,
    special_marks: str,
    scripture_mode: str | None = None,
) -> dict[str, Any]:
    context = _context(
        user_name=user_name,
        dominant_hand=dominant_hand,
        palm_shape=palm_shape,
        hand_shape=hand_shape,
        finger_length=finger_length,
        life_line=life_line,
        heart_line=heart_line,
        head_line=head_line,
        fate_line=fate_line,
        dominant_mount=dominant_mount,
        thumb_type=thumb_type,
        finger_style=finger_style,
        hand_texture=hand_texture,
        special_marks=special_marks,
        scripture_mode=scripture_mode,
    )
    fallback = _fallback_report(context)
    content = await _call_json(_prompt(context), model=FAST_MODEL, max_tokens=1400, temperature=0.35)
    return _coerce_report(content, fallback)
