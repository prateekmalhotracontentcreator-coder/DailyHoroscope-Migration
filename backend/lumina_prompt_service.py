from __future__ import annotations

import json
import os
import re
from datetime import date
from typing import Any, Literal
from urllib.parse import quote_plus


ScriptureMode = Literal["BIBLE", "GITA"]

FAST_MODEL = "claude-3-5-haiku-20241022"
QUALITY_MODEL = "claude-sonnet-4-5"

_CODE_FENCE_PATTERN = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)
_GITA_REF_PATTERN = re.compile(r"(\d+):(\d+)")

DAILY_SCRIPTURES: dict[ScriptureMode, list[dict[str, str]]] = {
    "BIBLE": [
        # Week 1
        {"reference": "Joshua 1:8",       "text": "This book of the law shall not depart out of thy mouth; but thou shalt meditate therein day and night."},
        {"reference": "Isaiah 41:10",      "text": "Fear thou not; for I am with thee: be not dismayed; for I am thy God."},
        {"reference": "Psalm 23:1",        "text": "The Lord is my shepherd; I shall not want."},
        {"reference": "Romans 8:28",       "text": "And we know that all things work together for good to them that love God."},
        {"reference": "Philippians 4:6",   "text": "Be careful for nothing; but in every thing by prayer and supplication with thanksgiving let your requests be made known unto God."},
        {"reference": "2 Timothy 1:7",     "text": "For God hath not given us the spirit of fear; but of power, and of love, and of a sound mind."},
        {"reference": "John 15:5",         "text": "I am the vine, ye are the branches: He that abideth in me, and I in him, the same bringeth forth much fruit."},
        # Week 2
        {"reference": "Psalm 27:1",        "text": "The Lord is my light and my salvation; whom shall I fear? the Lord is the strength of my life; of whom shall I be afraid?"},
        {"reference": "Psalm 37:4",        "text": "Delight thyself also in the Lord; and he shall give thee the desires of thine heart."},
        {"reference": "Psalm 46:1",        "text": "God is our refuge and strength, a very present help in trouble."},
        {"reference": "Psalm 91:1",        "text": "He that dwelleth in the secret place of the most High shall abide under the shadow of the Almighty."},
        {"reference": "Psalm 119:105",     "text": "Thy word is a lamp unto my feet, and a light unto my path."},
        {"reference": "Psalm 139:14",      "text": "I will praise thee; for I am fearfully and wonderfully made: marvellous are thy works."},
        {"reference": "Proverbs 3:5-6",    "text": "Trust in the Lord with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths."},
        # Week 3
        {"reference": "Proverbs 4:7",      "text": "Wisdom is the principal thing; therefore get wisdom: and with all thy getting get understanding."},
        {"reference": "Proverbs 16:3",     "text": "Commit thy works unto the Lord, and thy thoughts shall be established."},
        {"reference": "Isaiah 26:3",       "text": "Thou wilt keep him in perfect peace, whose mind is stayed on thee: because he trusteth in thee."},
        {"reference": "Isaiah 40:31",      "text": "But they that wait upon the Lord shall renew their strength; they shall mount up with wings as eagles."},
        {"reference": "Isaiah 43:2",       "text": "When thou passest through the waters, I will be with thee; and through the rivers, they shall not overflow thee."},
        {"reference": "Isaiah 55:8-9",     "text": "For my thoughts are not your thoughts, neither are your ways my ways, saith the Lord. For as the heavens are higher than the earth, so are my ways higher than your ways."},
        {"reference": "Jeremiah 29:11",    "text": "For I know the thoughts that I think toward you, saith the Lord, thoughts of peace, and not of evil, to give you an expected end."},
        # Week 4
        {"reference": "Lamentations 3:22-23", "text": "It is of the Lord's mercies that we are not consumed, because his compassions fail not. They are new every morning: great is thy faithfulness."},
        {"reference": "Micah 6:8",         "text": "He hath shewed thee, O man, what is good; and what doth the Lord require of thee, but to do justly, and to love mercy, and to walk humbly with thy God?"},
        {"reference": "Zephaniah 3:17",    "text": "The Lord thy God in the midst of thee is mighty; he will save, he will rejoice over thee with joy; he will rest in his love."},
        {"reference": "Deuteronomy 31:6",  "text": "Be strong and of a good courage, fear not, nor be afraid of them: for the Lord thy God, he it is that doth go with thee; he will not fail thee, nor forsake thee."},
        {"reference": "Numbers 6:24-26",   "text": "The Lord bless thee, and keep thee: the Lord make his face shine upon thee, and be gracious unto thee: the Lord lift up his countenance upon thee, and give thee peace."},
        {"reference": "Ecclesiastes 3:1",  "text": "To every thing there is a season, and a time to every purpose under the heaven."},
        {"reference": "Genesis 1:27",      "text": "So God created man in his own image, in the image of God created he him; male and female created he them."},
        # Week 5
        {"reference": "Matthew 5:3",       "text": "Blessed are the poor in spirit: for theirs is the kingdom of heaven."},
        {"reference": "Matthew 5:8",       "text": "Blessed are the pure in heart: for they shall see God."},
        {"reference": "Matthew 5:9",       "text": "Blessed are the peacemakers: for they shall be called the children of God."},
        {"reference": "Matthew 6:33",      "text": "But seek ye first the kingdom of God, and his righteousness; and all these things shall be added unto you."},
        {"reference": "Matthew 11:28",     "text": "Come unto me, all ye that labour and are heavy laden, and I will give you rest."},
        {"reference": "John 8:32",         "text": "And ye shall know the truth, and the truth shall make you free."},
        {"reference": "John 14:27",        "text": "Peace I leave with you, my peace I give unto you: not as the world giveth, give I unto you."},
        # Week 6
        {"reference": "Romans 5:3-4",      "text": "We glory in tribulations also: knowing that tribulation worketh patience; and patience, experience; and experience, hope."},
        {"reference": "Romans 12:2",       "text": "Be not conformed to this world: but be ye transformed by the renewing of your mind, that ye may prove what is that good, and acceptable, and perfect, will of God."},
        {"reference": "1 Corinthians 13:13","text": "And now abideth faith, hope, charity, these three; but the greatest of these is charity."},
        {"reference": "2 Corinthians 5:7", "text": "For we walk by faith, not by sight."},
        {"reference": "Galatians 5:22-23", "text": "The fruit of the Spirit is love, joy, peace, longsuffering, gentleness, goodness, faith, meekness, temperance: against such there is no law."},
        {"reference": "Ephesians 2:8",     "text": "For by grace are ye saved through faith; and that not of yourselves: it is the gift of God."},
        {"reference": "Ephesians 6:10",    "text": "Finally, my brethren, be strong in the Lord, and in the power of his might."},
        # Week 7
        {"reference": "Philippians 4:7",   "text": "The peace of God, which passeth all understanding, shall keep your hearts and minds through Christ Jesus."},
        {"reference": "Philippians 4:13",  "text": "I can do all things through Christ which strengtheneth me."},
        {"reference": "Colossians 3:23",   "text": "Whatsoever ye do, do it heartily, as to the Lord, and not unto men."},
        {"reference": "Hebrews 11:1",      "text": "Now faith is the substance of things hoped for, the evidence of things not seen."},
        {"reference": "Hebrews 12:1",      "text": "Let us lay aside every weight, and the sin which doth so easily beset us, and let us run with patience the race that is set before us."},
        {"reference": "James 1:5",         "text": "If any of you lack wisdom, let him ask of God, that giveth to all men liberally, and upbraideth not; and it shall be given him."},
        {"reference": "1 Peter 5:7",       "text": "Casting all your care upon him; for he careth for you."},
        # Week 8
        {"reference": "1 John 4:18",       "text": "There is no fear in love; but perfect love casteth out fear."},
        {"reference": "Revelation 21:4",   "text": "And God shall wipe away all tears from their eyes; and there shall be no more death, neither sorrow, nor crying, neither shall there be any more pain."},
        {"reference": "Song of Solomon 2:4","text": "He brought me to the banqueting house, and his banner over me was love."},
        {"reference": "Psalm 34:18",       "text": "The Lord is nigh unto them that are of a broken heart; and saveth such as be of a contrite spirit."},
    ],
    "GITA": [
        # Week 1
        {"reference": "Bhagavad Gita 2:47",  "text": "You have a right to perform your prescribed duty, but you are not entitled to the fruits of action."},
        {"reference": "Bhagavad Gita 4:7",   "text": "Whenever righteousness declines and unrighteousness rises, I manifest Myself."},
        {"reference": "Bhagavad Gita 6:5",   "text": "One must elevate, not degrade, oneself by the mind. The mind alone is the friend of the self, and the mind alone is the enemy of the self."},
        {"reference": "Bhagavad Gita 9:22",  "text": "To those who are constantly devoted and who worship Me with love, I give what they lack and preserve what they have."},
        {"reference": "Bhagavad Gita 10:10", "text": "To those who are constantly devoted and serve Me with love, I give the understanding by which they can come to Me."},
        {"reference": "Bhagavad Gita 12:15", "text": "One by whom the world is not disturbed and who is not disturbed by the world is dear to Me."},
        {"reference": "Bhagavad Gita 18:66", "text": "Abandon all varieties of duty and simply surrender unto Me. I shall deliver you from all sinful reactions; do not fear."},
        # Week 2
        {"reference": "Bhagavad Gita 2:14",  "text": "O son of Kunti, the non-permanent appearance of happiness and distress, and their disappearance in due course, are like the appearance and disappearance of winter and summer seasons. One must learn to tolerate them without being disturbed."},
        {"reference": "Bhagavad Gita 2:20",  "text": "For the soul there is never birth nor death at any time. It has not come into being, does not come into being, and will not come into being. It is unborn, eternal, ever-existing, and primeval."},
        {"reference": "Bhagavad Gita 2:22",  "text": "As a person puts on new garments, giving up old ones, the soul accepts new material bodies, giving up the old and useless ones."},
        {"reference": "Bhagavad Gita 2:48",  "text": "Perform your duty equipoised, O Arjuna, abandoning all attachment to success or failure. Such equanimity is called yoga."},
        {"reference": "Bhagavad Gita 2:50",  "text": "By rendering devotional service unto the Supreme, one is freed from the reactions of all activities. Therefore strive for yoga, which is the art of all work."},
        {"reference": "Bhagavad Gita 2:55",  "text": "When a man gives up all varieties of desire for sense gratification and when his mind, thus purified, finds satisfaction in the self alone, then he is said to be in pure transcendental consciousness."},
        {"reference": "Bhagavad Gita 3:19",  "text": "Therefore, without being attached to the fruits of activities, one should act as a matter of duty, for by working without attachment one attains the Supreme."},
        # Week 3
        {"reference": "Bhagavad Gita 3:21",  "text": "Whatever action a great man performs, common men follow. And whatever standards he sets by exemplary acts, all the world pursues."},
        {"reference": "Bhagavad Gita 3:27",  "text": "The bewildered spirit soul thinks himself the doer of activities that are in actuality carried out by the three modes of material nature."},
        {"reference": "Bhagavad Gita 3:42",  "text": "The working senses are superior to dull matter; mind is higher than the senses; intelligence is still higher than the mind; and the soul is even higher than the intelligence."},
        {"reference": "Bhagavad Gita 4:11",  "text": "As all surrender unto Me, I reward them accordingly. Everyone follows My path in all respects, O son of Prtha."},
        {"reference": "Bhagavad Gita 4:38",  "text": "In this world, there is nothing so sublime and pure as transcendental knowledge. Such knowledge is the mature fruit of all mysticism, and one who is accomplished in devotional service enjoys this knowledge within himself."},
        {"reference": "Bhagavad Gita 4:39",  "text": "A faithful person dedicated to transcendental knowledge, who subdues his senses, quickly attains the supreme spiritual peace."},
        {"reference": "Bhagavad Gita 5:7",   "text": "One who works in devotion, who is a pure soul, and who controls his mind and senses is dear to everyone, and everyone is dear to him. Though always working, such a man is never entangled."},
        # Week 4
        {"reference": "Bhagavad Gita 5:18",  "text": "The humble sage, by virtue of true knowledge, sees with equal vision a learned brahmin, a cow, an elephant, a dog and a dog-eater."},
        {"reference": "Bhagavad Gita 5:29",  "text": "A person in full consciousness of Me, knowing Me to be the ultimate beneficiary of all sacrifices and the Supreme Lord of all planets and demigods, attains peace from the pangs of material miseries."},
        {"reference": "Bhagavad Gita 6:17",  "text": "He who is regulated in his habits of eating, sleeping, recreation and work can mitigate all material pains by practicing the yoga system."},
        {"reference": "Bhagavad Gita 6:19",  "text": "As a lamp in a windless place does not waver, so the transcendentalist whose mind is controlled remains always steady in his meditation on the transcendent Self."},
        {"reference": "Bhagavad Gita 6:26",  "text": "From wherever the mind wanders due to its flickering and unsteady nature, one must certainly withdraw it and bring it back under the control of the Self."},
        {"reference": "Bhagavad Gita 6:35",  "text": "The mind is restless and difficult to restrain, but it is possible to subdue it by suitable practice and by detachment, O son of Kunti."},
        {"reference": "Bhagavad Gita 7:8",   "text": "O son of Kunti, I am the taste of water, the light of the sun and the moon, the syllable om in the Vedic mantras; I am the sound in ether and ability in man."},
        # Week 5
        {"reference": "Bhagavad Gita 7:14",  "text": "This divine energy of Mine, consisting of the three modes of material nature, is difficult to overcome. But those who have surrendered unto Me can easily cross beyond it."},
        {"reference": "Bhagavad Gita 7:19",  "text": "After many births and deaths, he who is actually in knowledge surrenders unto Me, knowing Me to be the cause of all causes and all that is. Such a great soul is very rare."},
        {"reference": "Bhagavad Gita 8:7",   "text": "Always think of Me and carry out your prescribed duty. With your activities dedicated to Me and your mind and intelligence fixed on Me, you will attain Me without doubt."},
        {"reference": "Bhagavad Gita 9:26",  "text": "If one offers Me with love and devotion a leaf, a flower, fruit or water, I will accept it."},
        {"reference": "Bhagavad Gita 9:27",  "text": "Whatever you do, whatever you eat, whatever you offer or give away, and whatever austerities you perform -- do that as an offering to Me."},
        {"reference": "Bhagavad Gita 10:8",  "text": "I am the source of all spiritual and material worlds. Everything emanates from Me. The wise who know this engage in My devotional service and worship Me with all their hearts."},
        {"reference": "Bhagavad Gita 12:6-7","text": "For those who worship Me with devotion, meditating on My transcendental form and carrying their oblations to Me -- I swiftly rescue them from the ocean of birth and death."},
        # Week 6
        {"reference": "Bhagavad Gita 12:13-14","text": "One who is not envious but is a kind friend to all living entities, free from false ego, equal in happiness and distress, tolerant, always satisfied, self-controlled, and engaged in devotional service -- such a devotee is very dear to Me."},
        {"reference": "Bhagavad Gita 13:8",  "text": "Humbleness, pridelessness, nonviolence, tolerance, simplicity, approaching a bona fide spiritual master, cleanliness, steadiness and self-control -- these are declared to be knowledge."},
        {"reference": "Bhagavad Gita 14:6",  "text": "The mode of goodness, being purer than the others, is illuminating, and it frees one from all sinful reactions. Those situated in that mode become conditioned by a sense of happiness and knowledge."},
        {"reference": "Bhagavad Gita 15:15", "text": "I am seated in everyone's heart, and from Me come remembrance, knowledge and forgetfulness. By all the Vedas I am to be known."},
        {"reference": "Bhagavad Gita 16:1-3","text": "Fearlessness, purification of one's existence, cultivation of spiritual knowledge, charity, self-control, nonviolence, truthfulness, freedom from anger -- these transcendental qualities belong to godly men."},
        {"reference": "Bhagavad Gita 17:3",  "text": "According to one's existence under the various modes of nature, one evolves a particular kind of faith. The living being is said to be of a particular faith according to the modes he has acquired."},
        {"reference": "Bhagavad Gita 18:20", "text": "That knowledge by which one undivided spiritual nature is seen in all living entities, though they are divided into innumerable forms, is knowledge in the mode of goodness."},
        # Week 7
        {"reference": "Bhagavad Gita 18:37", "text": "That which in the beginning may be just like poison but at the end is just like nectar, and which awakens one to self-realization, is said to be happiness in the mode of goodness."},
        {"reference": "Bhagavad Gita 18:45", "text": "By following his qualities of work, every man can become perfect. Now hear from Me how this can be done."},
        {"reference": "Bhagavad Gita 18:55", "text": "One can understand the Supreme Personality of Godhead as He is only by devotional service. And when one is in full consciousness by such devotion, one can enter into the kingdom of God."},
        {"reference": "Bhagavad Gita 18:63", "text": "Thus I have explained to you knowledge still more confidential. Deliberate on this fully, and then do what you wish to do."},
        {"reference": "Bhagavad Gita 18:65", "text": "Always think of Me, become My devotee, worship Me and offer your homage unto Me. Thus you will come to Me without fail. I promise you this because you are My very dear friend."},
        {"reference": "Bhagavad Gita 18:78", "text": "Wherever there is Krishna, the master of all mystics, and wherever there is Arjuna, the supreme archer, there will also certainly be opulence, victory, extraordinary power, and morality."},
        {"reference": "Bhagavad Gita 5:22",  "text": "An intelligent person does not take part in the sources of misery arising from contact with the material senses. Such pleasures have a beginning and an end, and the wise man does not delight in them."},
        # Week 8
        {"reference": "Bhagavad Gita 2:62-63","text": "While contemplating the objects of the senses, a person develops attachment; from attachment lust develops; from lust anger arises; from anger comes delusion, then loss of memory, then loss of intelligence, and then one falls down."},
        {"reference": "Bhagavad Gita 6:40",  "text": "A transcendentalist engaged in auspicious activities does not meet with destruction either in this world or in the spiritual world; one who does good is never overcome by evil."},
        {"reference": "Bhagavad Gita 13:22", "text": "The living entity in material nature follows the ways of life, enjoying the three modes of nature. This is due to his association with that material nature, and thus he meets with good and evil."},
        {"reference": "Bhagavad Gita 3:16",  "text": "One who does not follow in human life the cycle of sacrifice thus established by the Vedas certainly leads a life full of sin. Living only for the satisfaction of the senses, such a person lives in vain."},
        {"reference": "Bhagavad Gita 4:24",  "text": "A person who is fully absorbed in Krishna consciousness is sure to attain the spiritual kingdom, for his full contribution to spiritual activities makes the consummation absolute."},
    ],
}


def normalize_scripture_mode(scripture_mode: str | None) -> ScriptureMode:
    value = str(scripture_mode or "BIBLE").strip().upper()
    return "GITA" if value == "GITA" else "BIBLE"


def get_daily_scripture(scripture_mode: str | None) -> dict[str, str]:
    normalized = normalize_scripture_mode(scripture_mode)
    options = DAILY_SCRIPTURES[normalized]
    index = date.today().toordinal() % len(options)
    return options[index]


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


def _clean_json_text(text: str) -> str:
    stripped = text.strip()
    stripped = _CODE_FENCE_PATTERN.sub("", stripped)
    return stripped.strip()


def _scripture_frame(scripture_mode: ScriptureMode) -> str:
    if scripture_mode == "GITA":
        return (
            "Use Bhagavad Gita chapter and verse references. Frame guidance around dharma, disciplined action, devotion, inner steadiness, "
            "and Krishna-centered wisdom. Keep the tone warm, reverent, and spiritually precise without importing Christian terminology."
        )
    return (
        "Use Bible verse references. Frame guidance in a pastoral, scripture-grounded Christian voice that is warm, reverent, and theologically careful."
    )


def _daily_fallback(scripture_mode: ScriptureMode) -> dict[str, str]:
    verse = get_daily_scripture(scripture_mode)
    if scripture_mode == "GITA":
        return {
            "verse_reference": verse["reference"],
            "verse_text": verse["text"],
            "revelation_context": "This passage calls you back to sacred duty without anxious attachment. It invites disciplined action rooted in trust, clarity, and devotion.",
            "speak_it": "I will act with steadiness, offer my effort sincerely, and release anxiety over outcomes.",
            "think_it": "Where can I return to faithful effort instead of over-focusing on results?",
            "do_it": "Complete one important responsibility today with calm attention and no inner bargaining.",
            "prophets_promise": "Steady devotion matures into clarity. What is offered faithfully is never wasted in the divine economy.",
            "daily_application": "Choose one duty you have delayed, begin it with prayerful focus, and finish your next step before seeking reassurance.",
        }
    return {
        "verse_reference": verse["reference"],
        "verse_text": verse["text"],
        "revelation_context": "This word calls you to keep scripture close in speech, thought, and practice. Daily meditation is presented as the path to courage, wisdom, and stable fruitfulness.",
        "speak_it": "God's word lives in my mouth and in my mind, and I walk in wisdom today.",
        "think_it": "What would change today if I treated scripture as my first reference point rather than my last resort?",
        "do_it": "Read the verse aloud twice, write one line from it, and obey its clearest instruction before the day ends.",
        "prophets_promise": "Where the word is honored, direction becomes clearer and strength grows under pressure.",
        "daily_application": "Anchor one decision today in scripture before you respond emotionally or impulsively.",
    }


def _fallback_prayer(title: str, petition_seed: str, scripture_mode: ScriptureMode) -> str:
    if scripture_mode == "GITA":
        return (
            f"{title}\n\n"
            f"I offer this intention with humility: {petition_seed}. Establish my mind in steadiness, purify my motives, "
            "and guide my action according to dharma. May my labor be sincere, my speech disciplined, and my heart devoted. "
            "Let what is meant to flourish do so under divine order and wise effort."
        )
    return (
        f"{title}\n\n"
        f"Father, I bring this petition before You: {petition_seed}. Order my steps, steady my heart, and align my desires with Your will. "
        "Let Your word govern my speech, strengthen my faith, and establish what is righteous, timely, and good. "
        "I receive grace to persevere, wisdom to obey, and peace while I wait."
    )


def _fallback_scripture(book: str, chapter: int, version: str, scripture_mode: ScriptureMode) -> list[dict[str, Any]]:
    book_label = "Bhagavad Gita" if scripture_mode == "GITA" else book
    reference_base = f"{book_label} {chapter}"
    if scripture_mode == "GITA":
        return [
            {
                "verses": [
                    {"ref": f"{reference_base}:1-3", "text": f"Opening teaching flow from {book_label} chapter {chapter}, rendered in a {version or 'devotional'} translation style."},
                    {"ref": f"{reference_base}:4-5", "text": "The scene establishes the moral and spiritual tension that prepares the instruction."},
                ],
                "interpretation": "The opening movement frames the inner conflict behind action. The teaching begins by exposing confusion so wisdom can reorder the heart.",
            },
            {
                "verses": [
                    {"ref": f"{reference_base}:6-9", "text": "A central instruction turns the seeker toward discipline, discernment, and surrendered effort."},
                    {"ref": f"{reference_base}:10-12", "text": "The chapter develops a path of clear-minded devotion instead of fear-driven reaction."},
                ],
                "interpretation": "These verses emphasize disciplined consciousness. Right understanding becomes practical when thought, intention, and action are aligned.",
            },
        ]
    return [
        {
            "verses": [
                {"ref": f"{reference_base}:1-4", "text": f"Opening portion from {book} chapter {chapter} in {version or 'KJV'} style."},
                {"ref": f"{reference_base}:5-8", "text": "The chapter sets out its first major movement with an emphasis on God's character and human response."},
            ],
            "interpretation": "This first paragraph establishes the spiritual setting for the chapter. It invites the reader to see both the need addressed and the divine response offered.",
        },
        {
            "verses": [
                {"ref": f"{reference_base}:9-12", "text": "A middle movement draws out the promise, command, or warning at the heart of the chapter."},
                {"ref": f"{reference_base}:13-16", "text": "The text then turns toward lived obedience, trust, and spiritual formation."},
            ],
            "interpretation": "This section moves from revelation into response. The chapter becomes most fruitful when its truth is not only admired, but practiced.",
        },
    ]


def _fallback_confession(category: str, user_name: str, scripture_mode: ScriptureMode) -> str:
    name = user_name.strip() or "Beloved soul"
    if scripture_mode == "GITA":
        return (
            f"I, {name}, stand in disciplined remembrance. In the area of {category}, my mind is steadied, my duty is clear, and my heart is not ruled by fear. "
            "I act with devotion, restraint, and trust, and I release restless attachment to outcomes."
        )
    return (
        f"I, {name}, declare by faith that in the area of {category}, God's word is governing my heart, my mind, and my steps. "
        "I reject fear, receive grace, and walk in obedience, peace, and holy confidence today."
    )


def _fallback_situation(situation: str, scripture_mode: ScriptureMode) -> dict[str, str]:
    if scripture_mode == "GITA":
        return {
            "analysis": f"The situation around '{situation}' appears to involve tension between attachment, duty, and emotional turbulence. The first need is inner steadiness so action can arise from discernment rather than agitation.",
            "miracle_story": "Arjuna's paralysis on the battlefield gave way to clarity when he received divine instruction and aligned action with devotion.",
            "narrative": "Pause, become inwardly steady, clarify what is truly yours to do, and move in disciplined obedience one step at a time.",
        }
    return {
        "analysis": f"The situation around '{situation}' seems to carry emotional strain and a need for wisdom, not panic. Scripture would call for honest prayer, clear obedience, and trust that God can work even under pressure.",
        "miracle_story": "When Peter stepped onto the water, fear disrupted him, but the Lord still met him, corrected him, and kept him from sinking.",
        "narrative": "Name the fear plainly, return to prayer, take the next obedient step, and let faith become practical before it becomes dramatic.",
    }


def _fallback_kingdom_vision(goal: str, user_name: str) -> dict[str, Any]:
    clean_name = user_name.strip() or "Servant"
    return {
        "mandate": f"{clean_name} is called to pursue {goal} with integrity, disciplined excellence, and visible spiritual substance.",
        "scripture": "Proverbs 16:3",
        "action_plan": [
            "Clarify the mission in one sentence and refine it until it is measurable.",
            "Identify one service outcome your work should consistently produce for others.",
            "Build a weekly rhythm for skill growth, stewardship, and review.",
            "Pray over every major decision before committing public energy to it.",
        ],
        "blueprint_prompt": f"Dark indigo visionary blueprint for {goal}, elegant gold linework, symbolic of ordered stewardship, service, integrity, and flourishing impact.",
    }


def _fallback_glory_scrolls(user_name: str, scripture_mode: ScriptureMode) -> list[dict[str, str]]:
    name = user_name.strip() or "Beloved"
    if scripture_mode == "GITA":
        return [
            {
                "category": "WORD",
                "title": "Steady the Inner Voice",
                "content": f"{name}, wisdom will grow where your mind is returned again and again to truth rather than to agitation.",
                "verse": "Bhagavad Gita 6:26",
            },
            {
                "category": "WALK",
                "title": "Discipline Before Display",
                "content": "Do not hurry toward recognition. Let disciplined action shape your path and let composure become your witness.",
                "verse": "Bhagavad Gita 2:48",
            },
            {
                "category": "MARKETPLACE",
                "title": "Offer the Work",
                "content": "Consecrate your labor. Work offered in devotion gains a different quality than work driven only by anxiety or image.",
                "verse": "Bhagavad Gita 3:19",
            },
        ]
    return [
        {
            "category": "WORD",
            "title": "Light for the Next Step",
            "content": f"{name}, clarity will come as you keep the word near and obey the part already revealed.",
            "verse": "Psalm 119:105",
        },
        {
            "category": "WALK",
            "title": "Strength for Quiet Obedience",
            "content": "The Lord is forming steadiness in you. Quiet obedience in hidden places is preparing public fruit.",
            "verse": "Isaiah 40:31",
        },
        {
            "category": "MARKETPLACE",
            "title": "Favor for Faithful Work",
            "content": "Bring excellence, honesty, and peace into your work. What is built with clean hands carries a different weight.",
            "verse": "Colossians 3:23",
        },
    ]


def _reference_uri(reference: str, scripture_mode: ScriptureMode) -> str:
    if scripture_mode == "GITA":
        match = _GITA_REF_PATTERN.search(reference)
        if match:
            chapter, verse = match.groups()
            return f"https://vedabase.io/en/library/bg/{chapter}/{verse}/"
        return "https://vedabase.io/en/library/bg/"
    return f"https://www.biblegateway.com/passage/?search={quote_plus(reference)}"


async def _anthropic_client():
    try:
        from anthropic import AsyncAnthropic  # type: ignore
    except Exception:
        return None

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    return AsyncAnthropic(api_key=api_key)


def _image_payload(image_base64: str) -> dict[str, Any] | None:
    raw = (image_base64 or "").strip()
    if not raw:
        return None

    media_type = "image/png"
    data = raw
    if raw.startswith("data:"):
        header, _, encoded = raw.partition(",")
        data = encoded or raw
        media_match = re.match(r"data:(image/[-+.\w]+);base64", header, re.IGNORECASE)
        if media_match:
            media_type = media_match.group(1)

    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": data,
        },
    }


async def _call_json(
    prompt: str,
    *,
    model: str,
    max_tokens: int,
    temperature: float = 0.45,
    image_base64: str | None = None,
) -> Any:
    client = await _anthropic_client()
    if client is None:
        return None

    content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
    image_block = _image_payload(image_base64 or "")
    if image_block:
        content.append(image_block)

    try:
        response = await client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": content}],
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


async def generate_daily_verse_breakdown(scripture_mode: str) -> dict[str, str]:
    normalized = normalize_scripture_mode(scripture_mode)
    verse = get_daily_scripture(normalized)
    prompt = f"""
You are writing the Lumina daily scripture breakdown for Everyday Horoscope.

Rules:
- Return valid JSON only.
- Keep the tone pastoral, warm, scripture-grounded, and theologically precise.
- {_scripture_frame(normalized)}
- Use the provided verse exactly as the anchor text.
- The response is for a premium spiritual companion app, so make it emotionally resonant but concise.

Verse reference: {verse["reference"]}
Verse text: {verse["text"]}

Return JSON with keys:
- verse_reference
- verse_text
- revelation_context
- speak_it
- think_it
- do_it
- prophets_promise
- daily_application
""".strip()
    content = await _call_json(prompt, model=FAST_MODEL, max_tokens=700, temperature=0.4)
    if not isinstance(content, dict):
        return _daily_fallback(normalized)

    fallback = _daily_fallback(normalized)
    return {
        key: str(content.get(key) or fallback[key])
        for key in (
            "verse_reference",
            "verse_text",
            "revelation_context",
            "speak_it",
            "think_it",
            "do_it",
            "prophets_promise",
            "daily_application",
        )
    }


async def generate_chaplain_response(question: str, image_base64: str | None, scripture_mode: str) -> dict[str, Any]:
    normalized = normalize_scripture_mode(scripture_mode)
    prompt = f"""
You are Lumina's AI Chaplain.

Rules:
- Return valid JSON only.
- {_scripture_frame(normalized)}
- Answer with pastoral care, spiritual discernment, and practical next steps.
- Do not be alarmist, manipulative, or absolute.
- If the user attached an image, only reference visually obvious details and say less rather than more.
- Provide 2 to 4 source objects using scripture references that support the counsel.

User question:
{question}

Return JSON with keys:
- text
- sources

Each source must be an object with:
- title
- uri
""".strip()
    content = await _call_json(prompt, model=FAST_MODEL, max_tokens=950, temperature=0.45, image_base64=image_base64)
    if not isinstance(content, dict):
        fallback = _daily_fallback(normalized)
        return {
            "text": (
                "Take a slow breath and return to the center of what is true. "
                f"Let {fallback['verse_reference']} guide your next step: {fallback['daily_application']}"
            ),
            "sources": [{"title": fallback["verse_reference"], "uri": _reference_uri(fallback["verse_reference"], normalized)}],
        }

    sources = []
    for item in content.get("sources") or []:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or "").strip()
        if not title:
            continue
        uri = str(item.get("uri") or _reference_uri(title, normalized)).strip()
        sources.append({"title": title, "uri": uri})

    if not sources:
        verse = get_daily_scripture(normalized)
        sources.append({"title": verse["reference"], "uri": _reference_uri(verse["reference"], normalized)})

    return {
        "text": str(content.get("text") or "").strip() or _daily_fallback(normalized)["daily_application"],
        "sources": sources,
    }


async def generate_scripture_paragraphs(book: str, chapter: int, version: str, scripture_mode: str) -> list[dict[str, Any]]:
    normalized = normalize_scripture_mode(scripture_mode)
    prompt = f"""
You are preparing Lumina's scripture reader content.

Rules:
- Return valid JSON only.
- {_scripture_frame(normalized)}
- The response must stay inside the requested chapter.
- Group the chapter into 2 to 6 logical paragraphs.
- Each paragraph must contain a verses array with ref and text, then a 2-sentence interpretation.
- Keep verse text respectful and readable. Do not include commentary inside verse text.

Requested scripture:
- Book: {book}
- Chapter: {chapter}
- Version: {version}

Return a JSON array of objects with keys:
- verses
- interpretation
""".strip()
    content = await _call_json(prompt, model=FAST_MODEL, max_tokens=1600, temperature=0.25)
    if not isinstance(content, list):
        return _fallback_scripture(book, chapter, version, normalized)

    paragraphs: list[dict[str, Any]] = []
    for paragraph in content:
        if not isinstance(paragraph, dict):
            continue
        verses: list[dict[str, str]] = []
        for verse in paragraph.get("verses") or []:
            if not isinstance(verse, dict):
                continue
            ref = str(verse.get("ref") or "").strip()
            text = str(verse.get("text") or "").strip()
            if ref and text:
                verses.append({"ref": ref, "text": text})
        interpretation = str(paragraph.get("interpretation") or "").strip()
        if verses and interpretation:
            paragraphs.append({"verses": verses, "interpretation": interpretation})

    return paragraphs or _fallback_scripture(book, chapter, version, normalized)


async def compose_prayer_declaration(
    *,
    title: str,
    petition_seed: str,
    scripture_mode: str = "BIBLE",
) -> str:
    normalized = normalize_scripture_mode(scripture_mode)
    prompt = f"""
You are composing a Lumina prayer declaration.

Rules:
- Return valid JSON only.
- {_scripture_frame(normalized)}
- Write a first-person declaration that feels prayerful, composed, and spiritually grounded.
- Keep it between 110 and 180 words.
- Do not add markdown.

Prayer title: {title}
Petition seed: {petition_seed}

Return JSON with key:
- content
""".strip()
    content = await _call_json(prompt, model=QUALITY_MODEL, max_tokens=650, temperature=0.5)
    if not isinstance(content, dict):
        return _fallback_prayer(title, petition_seed, normalized)
    text = str(content.get("content") or "").strip()
    return text or _fallback_prayer(title, petition_seed, normalized)


async def generate_confession(category: str, user_name: str, scripture_mode: str) -> str:
    normalized = normalize_scripture_mode(scripture_mode)
    prompt = f"""
You are writing a Lumina faith confession.

Rules:
- Return valid JSON only.
- {_scripture_frame(normalized)}
- Write in first person.
- Keep it declarative, compact, and spiritually strong.
- Use 4 to 6 sentences.

Category: {category}
User name: {user_name}

Return JSON with key:
- text
""".strip()
    content = await _call_json(prompt, model=FAST_MODEL, max_tokens=450, temperature=0.45)
    if not isinstance(content, dict):
        return _fallback_confession(category, user_name, normalized)
    text = str(content.get("text") or "").strip()
    return text or _fallback_confession(category, user_name, normalized)


async def generate_situation_insight(situation: str, scripture_mode: str) -> dict[str, str]:
    normalized = normalize_scripture_mode(scripture_mode)
    prompt = f"""
You are generating a Lumina situation discernment card.

Rules:
- Return valid JSON only.
- {_scripture_frame(normalized)}
- Keep the answer compassionate, grounded, and practical.
- miracle_story should cite a fitting scriptural episode.

Situation:
{situation}

Return JSON with keys:
- analysis
- miracle_story
- narrative
""".strip()
    content = await _call_json(prompt, model=FAST_MODEL, max_tokens=700, temperature=0.4)
    if not isinstance(content, dict):
        return _fallback_situation(situation, normalized)

    fallback = _fallback_situation(situation, normalized)
    return {
        "analysis": str(content.get("analysis") or fallback["analysis"]),
        "miracle_story": str(content.get("miracle_story") or fallback["miracle_story"]),
        "narrative": str(content.get("narrative") or fallback["narrative"]),
    }


async def generate_kingdom_vision(goal: str, user_name: str) -> dict[str, Any]:
    prompt = f"""
You are writing a Lumina Kingdom Vision response for Everyday Horoscope.

Rules:
- Return valid JSON only.
- Use a warm, pastoral, strategically clear tone.
- Do not promise guaranteed outcomes.
- action_plan must be 4 to 6 concrete, short steps.
- scripture must be a single supportive scripture reference.

Goal:
{goal}

User name:
{user_name}

Return JSON with keys:
- mandate
- scripture
- action_plan
- blueprint_prompt
""".strip()
    content = await _call_json(prompt, model=QUALITY_MODEL, max_tokens=900, temperature=0.5)
    if not isinstance(content, dict):
        return _fallback_kingdom_vision(goal, user_name)

    fallback = _fallback_kingdom_vision(goal, user_name)
    action_plan = [str(step).strip() for step in (content.get("action_plan") or []) if str(step).strip()]
    return {
        "mandate": str(content.get("mandate") or fallback["mandate"]),
        "scripture": str(content.get("scripture") or fallback["scripture"]),
        "action_plan": action_plan or fallback["action_plan"],
        "blueprint_prompt": str(content.get("blueprint_prompt") or fallback["blueprint_prompt"]),
    }


async def generate_glory_scrolls(user_name: str, scripture_mode: str) -> list[dict[str, str]]:
    normalized = normalize_scripture_mode(scripture_mode)
    prompt = f"""
You are generating Lumina Glory Scrolls.

Rules:
- Return valid JSON only.
- {_scripture_frame(normalized)}
- Produce exactly three scrolls with categories WORD, WALK, and MARKETPLACE.
- Each scroll should feel prophetic yet grounded and usable.
- Each scroll must include a title, content, and verse.

User name: {user_name}

Return a JSON array of objects with keys:
- category
- title
- content
- verse
""".strip()
    content = await _call_json(prompt, model=FAST_MODEL, max_tokens=900, temperature=0.5)
    if not isinstance(content, list):
        return _fallback_glory_scrolls(user_name, normalized)

    normalized_scrolls: list[dict[str, str]] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        category = str(item.get("category") or "").strip().upper()
        title = str(item.get("title") or "").strip()
        body = str(item.get("content") or "").strip()
        verse = str(item.get("verse") or "").strip()
        if category in {"WORD", "WALK", "MARKETPLACE"} and title and body and verse:
            normalized_scrolls.append(
                {
                    "category": category,
                    "title": title,
                    "content": body,
                    "verse": verse,
                }
            )

    if len(normalized_scrolls) != 3:
        return _fallback_glory_scrolls(user_name, normalized)
    return normalized_scrolls
