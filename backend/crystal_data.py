from __future__ import annotations

from functools import lru_cache


SITE_URL = "https://www.everydayhoroscope.in"

CRYSTAL_SLUGS = [
    "ruby",
    "pearl",
    "red-coral",
    "emerald",
    "yellow-sapphire",
    "diamond",
    "blue-sapphire",
    "hessonite-garnet",
    "cats-eye",
    "amethyst",
    "rose-quartz",
    "clear-quartz",
    "black-tourmaline",
    "citrine",
    "lapis-lazuli",
    "obsidian",
    "selenite",
    "malachite",
    "carnelian",
    "moonstone",
    "labradorite",
    "pyrite",
    "amazonite",
    "sodalite",
    "aventurine",
    "tigers-eye",
    "jade",
    "hematite",
    "lepidolite",
    "rhodonite",
    "fluorite",
    "aquamarine",
    "chrysocolla",
    "sunstone",
    "bloodstone",
    "turquoise",
    "garnet",
    "onyx",
    "shungite",
    "rhodochrosite",
    "prehnite",
    "calcite",
    "apatite",
    "angelite",
    "celestite",
    "kunzite",
    "kyanite",
    "larimar",
    "moldavite",
    "nuummite",
]

INTENTION_DEFINITIONS = {
    "love-relationships": {
        "display": "Love & Relationships",
        "intro": "Crystals for love are chosen to soften the heart, restore trust, and help affection flow with more honesty. They are often used when you want to attract warmth, repair emotional strain, or deepen the quality of your bonds.",
        "top_crystals": ["rose-quartz", "rhodonite", "moonstone", "emerald", "ruby"],
        "how_to_use": [
            "Wear your chosen stone near the heart so your emotional reactions stay softer during the day.",
            "Keep a pair of relationship crystals on your bedside table to anchor calm, affectionate energy at home.",
            "Hold the crystal for a minute before difficult conversations and set one simple intention for connection.",
            "Cleanse weekly so old emotional residue does not build up around the stone.",
        ],
        "affirmation": "I welcome love that feels honest, warm, and emotionally safe.",
    },
    "anxiety-stress": {
        "display": "Anxiety & Stress Relief",
        "intro": "Stress-support crystals are usually grounding, soothing, and mentally cooling. They are helpful when you want to quiet overstimulation, regulate your mood, and return to a steadier rhythm.",
        "top_crystals": ["amethyst", "lepidolite", "black-tourmaline", "selenite", "hematite"],
        "how_to_use": [
            "Carry one grounding crystal in your left pocket so you can touch it when your nervous system feels overloaded.",
            "Place a calming stone beside your bed or under your pillow for gentler sleep energy.",
            "Use one minute of slow breathing while holding the crystal to reinforce the state you want your body to remember.",
            "Choose only one or two stones at a time so the ritual feels simple and sustainable.",
        ],
        "affirmation": "I return to calm one breath and one grounded choice at a time.",
    },
    "protection": {
        "display": "Protection & Grounding",
        "intro": "Protective crystals are selected for boundary work, energetic clearing, and steadiness under pressure. They are often kept near entrances, workspaces, or the body when life feels heavy or noisy.",
        "top_crystals": ["black-tourmaline", "obsidian", "shungite", "onyx", "nuummite"],
        "how_to_use": [
            "Keep one protection stone by your front door or work desk to steady the tone of the space.",
            "Carry a dense grounding crystal when you expect draining conversations or crowded environments.",
            "Pair one clearing crystal with one softer support stone so you feel protected without becoming emotionally shut down.",
            "Cleanse after travel or intense weeks when the stone has been doing more shielding work than usual.",
        ],
        "affirmation": "My energy is steady, protected, and rooted in what is mine.",
    },
    "abundance-money": {
        "display": "Abundance & Money",
        "intro": "Abundance crystals are used to support momentum, focus, and a receptive mindset around prosperity. They work best when paired with clear action, disciplined planning, and gratitude for growth in progress.",
        "top_crystals": ["citrine", "pyrite", "tigers-eye", "jade", "yellow-sapphire"],
        "how_to_use": [
            "Place your abundance stone where you make financial decisions so it becomes part of a practical prosperity ritual.",
            "Choose one crystal for confidence and one for clarity rather than stacking too many wealth symbols together.",
            "Review goals while holding the stone so your intention stays linked to action and structure.",
            "Recharge the crystal during major planning cycles or new income milestones.",
        ],
        "affirmation": "I meet prosperity with clarity, courage, and wise action.",
    },
    "clarity-focus": {
        "display": "Clarity & Focus",
        "intro": "Clarity stones are useful when the mind feels scattered or overloaded. They support cleaner thinking, better decision-making, and a stronger ability to hold your attention on what matters.",
        "top_crystals": ["clear-quartz", "sodalite", "fluorite", "apatite", "emerald"],
        "how_to_use": [
            "Keep a focus crystal near your laptop or notebook to mark the start of deep work.",
            "Use one stone for concentration and one for communication when your day involves study, writing, or strategy.",
            "Hold the crystal before planning sessions and name the one task that deserves your best attention.",
            "Cleanse after high-pressure mental work so the stone feels fresh rather than busy.",
        ],
        "affirmation": "My mind is clear, organized, and able to choose wisely.",
    },
    "confidence": {
        "display": "Confidence & Courage",
        "intro": "Confidence crystals are warming, activating stones that support bold movement and stronger self-trust. They are especially helpful when you are rebuilding momentum after doubt, fear, or hesitation.",
        "top_crystals": ["tigers-eye", "carnelian", "sunstone", "ruby", "garnet"],
        "how_to_use": [
            "Wear your confidence stone close to the solar plexus or throat before presentations or difficult decisions.",
            "Use one activating crystal at a time so the energy feels focused instead of overstimulating.",
            "Speak your intention aloud while holding the stone to reinforce self-belief with a real decision.",
            "Reach for calmer support at night so your courage ritual does not turn into restlessness.",
        ],
        "affirmation": "I trust my voice, my timing, and my ability to move forward.",
    },
    "sleep": {
        "display": "Sleep & Relaxation",
        "intro": "Sleep-support crystals are chosen for softness, emotional quiet, and a slower energetic pace. They are often placed beside the bed, under the pillow, or used as part of an evening wind-down ritual.",
        "top_crystals": ["selenite", "moonstone", "amethyst", "lepidolite", "celestite"],
        "how_to_use": [
            "Keep one calming stone on the bedside table rather than creating a crowded sleep altar.",
            "Hold the crystal for a minute while you slow your breathing and let the day come to a close.",
            "Avoid highly activating abundance or courage stones near your bed if your sleep is already light.",
            "Wipe or moon-cleanse your rest crystals regularly so they stay gentle and clear.",
        ],
        "affirmation": "I release the day and welcome deep, nourishing rest.",
    },
    "grief-healing": {
        "display": "Grief & Emotional Healing",
        "intro": "Grief-support crystals are often tender heart stones that allow emotion to move without forcing the process. They are meant to offer steadiness, compassion, and room for your healing to unfold at a humane pace.",
        "top_crystals": ["rhodonite", "rose-quartz", "rhodochrosite", "kunzite", "amethyst"],
        "how_to_use": [
            "Choose one heart-centered stone and keep it close when difficult memories surface.",
            "Use the crystal during journaling or prayer so the ritual feels supportive rather than performative.",
            "Let the stone remind you to soften around your feelings instead of rushing to fix them.",
            "Cleanse gently and consistently, especially after heavy emotional releases.",
        ],
        "affirmation": "I honor what I have felt and allow healing to arrive with grace.",
    },
    "spiritual-growth": {
        "display": "Spiritual Growth",
        "intro": "Spiritual-growth crystals are used to deepen reflection, intuition, and trust in a larger rhythm. They are often chosen for meditation, prayer, dreamwork, or periods of meaningful inner change.",
        "top_crystals": ["amethyst", "labradorite", "moldavite", "celestite", "blue-sapphire"],
        "how_to_use": [
            "Use your chosen crystal in a consistent meditation seat so the space gathers a stable spiritual tone over time.",
            "Pair an expansive stone with a grounding one if your practice tends to leave you uncentered.",
            "Keep a notebook nearby and record any patterns, insights, or symbols that repeat after practice.",
            "Take breaks from very intense stones when your energy feels overstretched.",
        ],
        "affirmation": "I grow in wisdom, trust, and alignment with my deeper path.",
    },
    "intuition": {
        "display": "Intuition & Psychic Ability",
        "intro": "Intuition crystals are usually linked with the third eye, dreams, and pattern recognition. They help create quiet enough inside the mind that subtle signals can be noticed and trusted.",
        "top_crystals": ["lapis-lazuli", "moonstone", "labradorite", "fluorite", "amethyst"],
        "how_to_use": [
            "Hold the stone before meditation, dreamwork, or divination so the mind settles into a receptive state.",
            "Use one intuitive crystal with one grounding stone when you want insight that still feels practical.",
            "Keep the crystal near your journal to reinforce the habit of listening to subtle impressions.",
            "Avoid overusing intense stones when your intuition starts feeling mixed with anxiety.",
        ],
        "affirmation": "I trust clear inner knowing and receive guidance with balance.",
    },
    "creativity": {
        "display": "Creativity",
        "intro": "Creative crystals are chosen to loosen rigidity, awaken joy, and restore movement where inspiration has gone flat. They support artists, writers, builders, and anyone trying to make something new.",
        "top_crystals": ["carnelian", "sunstone", "apatite", "amazonite", "citrine"],
        "how_to_use": [
            "Keep one energizing crystal in your workspace to mark the beginning of creative play.",
            "Choose stones that feel warm and expressive when you need momentum more than perfection.",
            "Hold the crystal before brainstorming and ask a single question you want fresh ideas around.",
            "Rotate stones when a project changes from ideation into disciplined finishing work.",
        ],
        "affirmation": "Creative energy moves through me with joy, courage, and flow.",
    },
    "communication": {
        "display": "Communication",
        "intro": "Communication crystals support truth, articulation, and emotional steadiness in conversation. They are especially useful when you want to speak clearly without becoming harsh or avoidant.",
        "top_crystals": ["amazonite", "aquamarine", "sodalite", "turquoise", "emerald"],
        "how_to_use": [
            "Wear or hold the crystal before meetings, difficult talks, or public speaking moments.",
            "Pair a throat-chakra stone with a grounding stone if nerves usually overtake your words.",
            "State your message in one sentence before the conversation so the crystal supports precision, not rambling.",
            "Cleanse after conflict-heavy periods so the stone does not feel loaded.",
        ],
        "affirmation": "I speak clearly, kindly, and in full alignment with the truth.",
    },
    "health-vitality": {
        "display": "Health & Vitality",
        "intro": "Vitality stones are commonly chosen to restore momentum, warmth, and resilience. They are best approached as supportive symbolic tools that reinforce healthy routines rather than replace proper care.",
        "top_crystals": ["bloodstone", "red-coral", "carnelian", "garnet", "calcite"],
        "how_to_use": [
            "Use the crystal alongside practical routines like hydration, movement, and rest so the ritual stays grounded.",
            "Carry an energizing stone during demanding stretches when you want steadier physical motivation.",
            "Choose calmer support if your system is already inflamed or overstimulated.",
            "Cleanse after intense work periods or recovery phases.",
        ],
        "affirmation": "My body, energy, and daily choices support a stronger life force.",
    },
    "travel-protection": {
        "display": "Travel Protection",
        "intro": "Travel crystals are selected for steadiness, protection, and emotional grounding during movement. They are often kept in bags, vehicles, or pockets to create a calmer field while away from home.",
        "top_crystals": ["black-tourmaline", "turquoise", "tigers-eye", "shungite", "obsidian"],
        "how_to_use": [
            "Keep one protective crystal in your travel bag so it becomes a familiar anchor wherever you go.",
            "Use a lighter pocket stone for the journey and a larger stone at your temporary stay.",
            "Set a simple intention for safe passage each time you begin a trip.",
            "Cleanse after returning home, especially after crowded or tiring travel.",
        ],
        "affirmation": "I move through the world protected, aware, and well guided.",
    },
    "career-success": {
        "display": "Career Success",
        "intro": "Career crystals are often chosen for strategy, confidence, leadership, and resilience. They can help keep your ambitions steady when you are building, pitching, negotiating, or stepping into greater responsibility.",
        "top_crystals": ["pyrite", "yellow-sapphire", "emerald", "tigers-eye", "sunstone"],
        "how_to_use": [
            "Keep a career stone on your desk where important decisions and focused work actually happen.",
            "Use one crystal for confidence and one for communication when your work requires both presence and precision.",
            "Review your weekly priorities while holding the stone to anchor ambition in structure.",
            "Recharge during key transitions such as interviews, launches, or promotions.",
        ],
        "affirmation": "I build success through clarity, discipline, and courageous action.",
    },
    "new-beginnings": {
        "display": "New Beginnings",
        "intro": "New-beginning crystals support release, renewal, and faith in fresh starts. They are helpful when you are shifting identity, starting over, or trying to move with less attachment to an older chapter.",
        "top_crystals": ["moonstone", "clear-quartz", "sunstone", "fluorite", "moldavite"],
        "how_to_use": [
            "Use one crystal to clear the old and one to welcome the new so the transition feels balanced.",
            "Hold your stone during first steps, not just big milestones, so change stays embodied.",
            "Choose gentler renewal stones when life already feels intense enough.",
            "Refresh your intention weekly while the transition is still unfolding.",
        ],
        "affirmation": "I release the old with grace and welcome the new with trust.",
    },
    "fertility": {
        "display": "Fertility & Pregnancy",
        "intro": "Fertility-support crystals are traditionally used to cultivate softness, receptivity, and emotional steadiness. They are often chosen for comfort and ritual support, not as a substitute for medical guidance.",
        "top_crystals": ["moonstone", "rose-quartz", "pearl", "jade", "carnelian"],
        "how_to_use": [
            "Choose soft, nurturing stones and use them in calm rituals rather than highly charged practices.",
            "Keep the crystal near your rest space or hold it during moments of prayer or visualization.",
            "Focus on emotional safety and gentle consistency over intensity.",
            "Avoid rough cleansing methods for delicate or porous stones in this group.",
        ],
        "affirmation": "I welcome softness, trust, and nurturing support into this journey.",
    },
    "forgiveness": {
        "display": "Forgiveness & Release",
        "intro": "Forgiveness crystals help soften emotional armor and loosen old stories that keep repeating. They are useful when you want to release resentment without losing your boundaries or your self-respect.",
        "top_crystals": ["rhodonite", "rhodochrosite", "rose-quartz", "malachite", "kunzite"],
        "how_to_use": [
            "Hold the crystal while naming what you are ready to release and what still needs protection.",
            "Use this ritual in short sessions so you stay compassionate without becoming overwhelmed.",
            "Journal after working with the stone because insight often follows emotional softening.",
            "Cleanse after heavy release work so the crystal does not feel saturated.",
        ],
        "affirmation": "I release what I no longer need and keep what strengthens my heart.",
    },
    "truth-honesty": {
        "display": "Truth & Honesty",
        "intro": "Truth-support crystals are chosen for clear speech, integrity, and the courage to stay aligned with what is real. They help when you want to communicate directly without abandoning kindness.",
        "top_crystals": ["sodalite", "lapis-lazuli", "turquoise", "kyanite", "aquamarine"],
        "how_to_use": [
            "Work with one throat or third-eye stone before conversations that need courage and precision.",
            "Name the truth you want to speak in one clean sentence before the interaction begins.",
            "Pair a truth stone with a heart stone if you need honesty to land gently.",
            "Cleanse after emotionally loaded conversations or conflict repair work.",
        ],
        "affirmation": "I honor truth with courage, clarity, and compassion.",
    },
    "meditation": {
        "display": "Meditation & Mindfulness",
        "intro": "Meditation crystals are selected for stillness, spaciousness, and inner attunement. They are helpful when you want practice to feel more focused, embodied, and easier to return to each day.",
        "top_crystals": ["amethyst", "clear-quartz", "selenite", "celestite", "prehnite"],
        "how_to_use": [
            "Use the same crystal in the same practice spot so the body starts recognizing the ritual more quickly.",
            "Choose a calmer stone when your goal is steady mindfulness rather than dramatic spiritual intensity.",
            "Hold the crystal lightly or place it nearby so attention stays on the practice, not on performing the ritual.",
            "Cleanse regularly to keep the meditation space feeling open and uncluttered.",
        ],
        "affirmation": "I settle into presence with steadiness, openness, and ease.",
    },
}

TAG_COPY = {
    "peace": ("promotes emotional quiet during demanding seasons", "supports meditative calm and inner stillness"),
    "protection": ("helps you maintain stronger emotional boundaries", "creates a steadier field for spiritual protection"),
    "grounding": ("steadies scattered feelings and lowers overwhelm", "anchors insight so it feels usable in real life"),
    "love": ("encourages tenderness, receptivity, and trust", "opens the heart to gentler spiritual connection"),
    "abundance": ("softens scarcity thinking and supports optimism", "strengthens receptivity to growth and blessing"),
    "clarity": ("cuts through emotional fog and mixed signals", "sharpens perception when you need cleaner guidance"),
    "confidence": ("supports courage when self-doubt rises", "helps your energy move outward with conviction"),
    "creativity": ("loosens rigidity and restores playful flow", "reawakens inspiration and original expression"),
    "intuition": ("helps you trust subtle inner signals", "deepens third-eye awareness and symbolic perception"),
    "communication": ("encourages honest expression without excess force", "aligns the voice with insight and integrity"),
    "healing": ("supports emotional recovery after heavy periods", "encourages restoration and subtle energetic repair"),
    "courage": ("reduces hesitation when action is needed", "strengthens personal will in spiritual practice"),
    "transformation": ("supports release when life is changing quickly", "accelerates inner change and perspective shifts"),
    "purification": ("helps clear stale emotional residue", "refreshes the energy field and sacred space"),
    "sleep": ("settles nighttime restlessness and emotional noise", "supports dreamwork and peaceful night energy"),
    "focus": ("improves steadiness when the mind is distracted", "supports disciplined attention in practice"),
    "release": ("helps soften attachment to old stories", "assists energetic letting-go and closure"),
    "vitality": ("restores motivation when energy feels low", "rebuilds life force and spiritual stamina"),
    "compassion": ("makes room for softer self-talk and empathy", "supports heart-led awareness and forgiveness"),
    "truth": ("helps you stay emotionally honest with yourself", "strengthens alignment with truth and discernment"),
    "manifestation": ("supports decisive movement toward goals", "amplifies intention when paired with grounded action"),
    "joy": ("lightens emotional heaviness and invites warmth", "reconnects you with creative, solar energy"),
    "resilience": ("supports emotional endurance under pressure", "helps you hold steady through karmic lessons"),
    "boundaries": ("reduces emotional leakage and overextension", "reinforces energetic sovereignty"),
    "expansion": ("encourages faith in bigger possibilities", "opens awareness to growth, wisdom, and guidance"),
    "forgiveness": ("softens resentment without erasing healthy boundaries", "supports heart-led release and reconciliation"),
    "grief-healing": ("creates room for grief to move at a humane pace", "supports spiritual comfort during loss and emotional healing"),
    "meditation": ("helps the mind return to stillness more easily", "deepens mindful presence and quiet attention"),
    "new-beginnings": ("supports emotional openness to a fresh chapter", "helps you align with renewal and forward movement"),
    "spiritual-growth": ("encourages trust in deeper inner guidance", "supports awakening, reflection, and meaningful inner expansion"),
}

NAVARATNA_DETAILS = {
    "ruby": {
        "vedic_name": "Manik",
        "wearing": {
            "metal": "Gold",
            "finger": "Ring finger",
            "day": "Sunday",
            "mantra": "Om Hram Hreem Hroum Sah Suryaya Namah",
            "activation": "Wear during Shukla Paksha on Sunday at sunrise after cleansing in raw milk and Ganga jal.",
        },
        "synergy": ["yellow-sapphire", "red-coral"],
        "conflict": ["blue-sapphire", "diamond", "hessonite-garnet"],
    },
    "pearl": {
        "vedic_name": "Moti",
        "wearing": {
            "metal": "Silver",
            "finger": "Little finger",
            "day": "Monday",
            "mantra": "Om Shram Shreem Shroum Sah Chandraya Namah",
            "activation": "Wear on a Monday near moonrise after resting the stone in milk or moonlight overnight.",
        },
        "synergy": ["yellow-sapphire", "ruby"],
        "conflict": ["hessonite-garnet", "cats-eye", "blue-sapphire"],
    },
    "red-coral": {
        "vedic_name": "Moonga",
        "wearing": {
            "metal": "Gold or copper",
            "finger": "Ring finger",
            "day": "Tuesday",
            "mantra": "Om Kram Kreem Kroum Sah Bhaumaya Namah",
            "activation": "Wear during Shukla Paksha on Tuesday after rinsing with red sandalwood water or Ganga jal.",
        },
        "synergy": ["ruby", "yellow-sapphire", "pearl"],
        "conflict": ["emerald", "diamond", "blue-sapphire"],
    },
    "emerald": {
        "vedic_name": "Panna",
        "wearing": {
            "metal": "Gold",
            "finger": "Little finger",
            "day": "Wednesday",
            "mantra": "Om Bram Breem Broum Sah Budhaya Namah",
            "activation": "Wear on Wednesday morning after placing the stone on fresh green moong or a clean altar cloth.",
        },
        "synergy": ["diamond", "blue-sapphire"],
        "conflict": ["pearl", "red-coral"],
    },
    "yellow-sapphire": {
        "vedic_name": "Pukhraj",
        "wearing": {
            "metal": "Gold",
            "finger": "Index finger",
            "day": "Thursday",
            "mantra": "Om Gram Greem Groum Sah Gurave Namah",
            "activation": "Wear on a Thursday morning after cleansing in turmeric water, honey, or sacred water.",
        },
        "synergy": ["ruby", "pearl", "red-coral"],
        "conflict": ["emerald", "diamond"],
    },
    "diamond": {
        "vedic_name": "Heera",
        "wearing": {
            "metal": "Platinum or gold",
            "finger": "Middle finger",
            "day": "Friday",
            "mantra": "Om Dram Dreem Droum Sah Shukraya Namah",
            "activation": "Wear on Friday sunrise after washing in rose water and offering a clean white-cloth intention.",
        },
        "synergy": ["emerald", "blue-sapphire"],
        "conflict": ["ruby", "pearl", "red-coral", "yellow-sapphire"],
    },
    "blue-sapphire": {
        "vedic_name": "Neelam",
        "wearing": {
            "metal": "Silver or iron",
            "finger": "Middle finger",
            "day": "Saturday",
            "mantra": "Om Pram Preem Proum Sah Shanischaraya Namah",
            "activation": "Trial the stone first, then wear on Saturday around sunset after mustard-oil or sacred-water cleansing.",
        },
        "synergy": ["diamond", "emerald"],
        "conflict": ["ruby", "pearl", "red-coral"],
    },
    "hessonite-garnet": {
        "vedic_name": "Gomed",
        "wearing": {
            "metal": "Silver",
            "finger": "Middle finger",
            "day": "Saturday",
            "mantra": "Om Bhram Bhreem Bhroum Sah Rahave Namah",
            "activation": "Wear during Krishna Paksha on a Saturday evening after cleansing in Ganga jal or another sacred rinse.",
        },
        "synergy": ["blue-sapphire"],
        "conflict": ["ruby", "pearl", "yellow-sapphire"],
    },
    "cats-eye": {
        "vedic_name": "Lehsunia",
        "wearing": {
            "metal": "Silver",
            "finger": "Middle finger",
            "day": "Tuesday",
            "mantra": "Om Sram Sreem Sroum Sah Ketave Namah",
            "activation": "Wear during Krishna Paksha on Tuesday dawn after cleansing in milk and resting the stone briefly on ash or wood.",
        },
        "synergy": ["hessonite-garnet"],
        "conflict": ["ruby", "pearl"],
    },
}

PLANET_CRYSTAL_MAP = {
    "Sun": {"primary_slug": "ruby", "secondary_slugs": ["sunstone", "garnet"]},
    "Moon": {"primary_slug": "pearl", "secondary_slugs": ["moonstone", "selenite"]},
    "Mars": {"primary_slug": "red-coral", "secondary_slugs": ["bloodstone", "carnelian"]},
    "Mercury": {"primary_slug": "emerald", "secondary_slugs": ["aventurine", "amazonite"]},
    "Jupiter": {"primary_slug": "yellow-sapphire", "secondary_slugs": ["citrine", "tigers-eye"]},
    "Venus": {"primary_slug": "diamond", "secondary_slugs": ["clear-quartz", "rose-quartz"]},
    "Saturn": {"primary_slug": "blue-sapphire", "secondary_slugs": ["amethyst", "obsidian"]},
    "Rahu": {"primary_slug": "hessonite-garnet", "secondary_slugs": ["labradorite", "obsidian"]},
    "Ketu": {"primary_slug": "cats-eye", "secondary_slugs": ["fluorite", "lepidolite"]},
}

INTENTION_BOOSTERS = {
    "love-relationships": ["rose-quartz", "rhodonite"],
    "anxiety-stress": ["lepidolite", "amethyst"],
    "protection": ["black-tourmaline", "obsidian"],
    "abundance-money": ["pyrite", "citrine"],
    "clarity-focus": ["clear-quartz", "sodalite"],
    "confidence": ["tigers-eye", "carnelian"],
    "sleep": ["selenite", "moonstone"],
    "grief-healing": ["rhodonite", "kunzite"],
    "spiritual-growth": ["labradorite", "amethyst"],
    "intuition": ["lapis-lazuli", "moonstone"],
    "creativity": ["carnelian", "apatite"],
    "communication": ["amazonite", "aquamarine"],
    "health-vitality": ["bloodstone", "calcite"],
    "travel-protection": ["turquoise", "black-tourmaline"],
    "career-success": ["pyrite", "yellow-sapphire"],
    "new-beginnings": ["moonstone", "clear-quartz"],
    "fertility": ["moonstone", "rose-quartz"],
    "forgiveness": ["rhodochrosite", "rhodonite"],
    "truth-honesty": ["sodalite", "kyanite"],
    "meditation": ["selenite", "amethyst"],
}

CRYSTAL_DEFINITIONS = {
    "ruby": {
        "display_name": "Ruby",
        "tagline": "The royal stone of vitality, courage, and heart-led leadership",
        "color": "Deep red",
        "chakras": ["Root", "Heart"],
        "element": "Fire",
        "planet": "Sun",
        "zodiac": ["Leo", "Aries", "Scorpio"],
        "hardness_mohs": 9,
        "benefit_tags": ["confidence", "courage", "vitality", "joy"],
        "physical_support": ["supports healthy motivation", "encourages warmth and circulation rituals", "helps counter emotional fatigue"],
        "best_intentions": ["confidence", "career-success", "love-relationships", "health-vitality"],
        "how_to_use": ["Wear as a ring or pendant when you need stronger confidence.", "Hold during sunrise prayer or affirmation work.", "Keep on a work desk when leadership and visibility matter."],
        "cleansing_methods": ["Moonlight", "Sound cleansing", "Soft-cloth wipe"],
        "pairs_well_with": ["yellow-sapphire", "garnet", "sunstone"],
        "avoid_with": ["blue-sapphire", "hessonite-garnet"],
        "affirmation": "I radiate courage, vitality, and heart-centered leadership.",
        "caution": "Strong solar energy may feel too intense during already heated emotional periods.",
    },
    "pearl": {
        "display_name": "Pearl",
        "tagline": "A cooling lunar gem for emotional softness and peace",
        "color": "White to cream",
        "chakras": ["Crown", "Heart"],
        "element": "Water",
        "planet": "Moon",
        "zodiac": ["Cancer", "Pisces", "Taurus"],
        "hardness_mohs": 3.5,
        "benefit_tags": ["peace", "sleep", "compassion", "intuition"],
        "physical_support": ["supports evening calm", "encourages gentler emotional processing", "pairs well with rest rituals"],
        "best_intentions": ["sleep", "anxiety-stress", "fertility", "love-relationships"],
        "how_to_use": ["Wear close to the skin when emotional sensitivity runs high.", "Keep near your bed for softer nighttime energy.", "Use during journaling when you need tenderness rather than pressure."],
        "cleansing_methods": ["Moonlight", "Soft dry cloth", "Sound cleansing"],
        "pairs_well_with": ["moonstone", "selenite", "rose-quartz"],
        "avoid_with": ["hessonite-garnet", "blue-sapphire"],
        "affirmation": "I move with softness, emotional balance, and peace.",
        "caution": "Pearls are delicate and should be kept away from harsh chemicals or long water exposure.",
    },
    "red-coral": {
        "display_name": "Red Coral",
        "tagline": "A martial talisman for courage, stamina, and decisive action",
        "color": "Red to vermilion",
        "chakras": ["Root", "Sacral"],
        "element": "Fire",
        "planet": "Mars",
        "zodiac": ["Aries", "Scorpio", "Capricorn"],
        "hardness_mohs": 3.5,
        "benefit_tags": ["courage", "confidence", "vitality", "manifestation"],
        "physical_support": ["supports disciplined action", "encourages energetic follow-through", "helps when motivation feels depleted"],
        "best_intentions": ["confidence", "health-vitality", "career-success", "new-beginnings"],
        "how_to_use": ["Wear in a ring or pendant when you need decisive movement.", "Keep near your training or work area for momentum.", "Use in short energizing rituals before demanding tasks."],
        "cleansing_methods": ["Incense smoke", "Soft cloth", "Brief moonlight"],
        "pairs_well_with": ["ruby", "bloodstone", "garnet"],
        "avoid_with": ["emerald", "blue-sapphire"],
        "affirmation": "I act with courage, clarity, and disciplined strength.",
        "caution": "Red coral can feel overstimulating if you are already agitated or energetically inflamed.",
    },
    "emerald": {
        "display_name": "Emerald",
        "tagline": "The green intelligence stone of wisdom, speech, and graceful strategy",
        "color": "Rich green",
        "chakras": ["Heart", "Throat"],
        "element": "Earth",
        "planet": "Mercury",
        "zodiac": ["Gemini", "Virgo", "Libra"],
        "hardness_mohs": 7.5,
        "benefit_tags": ["clarity", "communication", "abundance", "truth"],
        "physical_support": ["supports steadier nerves during communication", "encourages balanced focus", "pairs well with study or planning"],
        "best_intentions": ["communication", "clarity-focus", "career-success", "love-relationships"],
        "how_to_use": ["Wear near the throat or heart when you need clean communication.", "Place on your desk during study, planning, or business work.", "Use before negotiations to reinforce poise and discernment."],
        "cleansing_methods": ["Moonlight", "Smoke cleansing", "Soft dry wipe"],
        "pairs_well_with": ["diamond", "amazonite", "sodalite"],
        "avoid_with": ["pearl", "red-coral"],
        "affirmation": "My mind is clear, my words are precise, and my heart stays balanced.",
        "caution": "Many emeralds are treated stones, so avoid aggressive cleansing or heat.",
    },
    "yellow-sapphire": {
        "display_name": "Yellow Sapphire",
        "tagline": "A Jupiter gem for wisdom, fortune, and expansive guidance",
        "color": "Golden yellow",
        "chakras": ["Solar Plexus", "Crown"],
        "element": "Ether",
        "planet": "Jupiter",
        "zodiac": ["Sagittarius", "Pisces", "Cancer"],
        "hardness_mohs": 9,
        "benefit_tags": ["abundance", "expansion", "clarity", "truth"],
        "physical_support": ["supports optimistic energy", "encourages faith during growth cycles", "pairs well with study and mentorship rituals"],
        "best_intentions": ["abundance-money", "career-success", "clarity-focus", "spiritual-growth"],
        "how_to_use": ["Wear when you want to strengthen wisdom, prosperity, or guidance rituals.", "Keep on your desk for studies, teaching, or planning work.", "Use in Thursday intention setting or gratitude practice."],
        "cleansing_methods": ["Moonlight", "Sound cleansing", "Soft-cloth wipe"],
        "pairs_well_with": ["ruby", "citrine", "tigers-eye"],
        "avoid_with": ["diamond", "emerald"],
        "affirmation": "I grow through wisdom, faith, and aligned abundance.",
        "caution": "Choose clear, well-cut stones and avoid wearing if the energy feels mentally excessive.",
    },
    "diamond": {
        "display_name": "Diamond",
        "tagline": "A Venus gem for refinement, attraction, and clear amplification",
        "color": "Clear to icy white",
        "chakras": ["Crown", "Heart"],
        "element": "Air",
        "planet": "Venus",
        "zodiac": ["Libra", "Taurus", "Pisces"],
        "hardness_mohs": 10,
        "benefit_tags": ["love", "clarity", "manifestation", "joy"],
        "physical_support": ["supports a refined energetic field", "encourages graceful self-presentation", "pairs well with beauty and harmony rituals"],
        "best_intentions": ["love-relationships", "career-success", "truth-honesty", "abundance-money"],
        "how_to_use": ["Wear as jewelry when you want beauty and clarity to move together.", "Use during Friday gratitude or relationship rituals.", "Pair with heart-centered practices rather than overstimulating stacks."],
        "cleansing_methods": ["Water rinse", "Moonlight", "Soft-cloth polish"],
        "pairs_well_with": ["emerald", "clear-quartz", "rose-quartz"],
        "avoid_with": ["ruby", "red-coral"],
        "affirmation": "I welcome love, elegance, and clear energetic refinement.",
        "caution": "Diamond amplifies energy strongly, so intention and emotional tone matter.",
    },
    "blue-sapphire": {
        "display_name": "Blue Sapphire",
        "tagline": "A Saturn gem for discipline, maturity, and karmic steadiness",
        "color": "Deep blue",
        "chakras": ["Third Eye", "Throat"],
        "element": "Air",
        "planet": "Saturn",
        "zodiac": ["Capricorn", "Aquarius", "Libra"],
        "hardness_mohs": 9,
        "benefit_tags": ["resilience", "truth", "focus", "protection"],
        "physical_support": ["supports disciplined routines", "encourages steadier energy under pressure", "pairs well with long-term commitment work"],
        "best_intentions": ["career-success", "truth-honesty", "protection", "clarity-focus"],
        "how_to_use": ["Wear only when the energy feels steady and appropriate for you.", "Use in meditation when you need sobriety, patience, or karmic focus.", "Keep near work that demands endurance rather than speed."],
        "cleansing_methods": ["Smoke cleansing", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["amethyst", "obsidian", "emerald"],
        "avoid_with": ["ruby", "red-coral"],
        "affirmation": "I meet life with discipline, truth, and grounded endurance.",
        "caution": "Blue sapphire is traditionally considered intense and is often approached slowly or with a trial period.",
    },
    "hessonite-garnet": {
        "display_name": "Hessonite Garnet",
        "tagline": "A Rahu gem for clearing confusion and navigating unusual transitions",
        "color": "Honey brown",
        "chakras": ["Sacral", "Root"],
        "element": "Air",
        "planet": "Rahu",
        "zodiac": ["Aquarius", "Gemini", "Virgo"],
        "hardness_mohs": 7,
        "benefit_tags": ["clarity", "protection", "transformation", "focus"],
        "physical_support": ["supports steadiness during disruptive cycles", "encourages practical grounding", "pairs well with change management rituals"],
        "best_intentions": ["protection", "new-beginnings", "clarity-focus", "career-success"],
        "how_to_use": ["Use during periods of uncertainty when you need sharper discrimination.", "Keep near your workspace when choices feel confusing or unstable.", "Pair with grounding stones if the energy feels too airy."],
        "cleansing_methods": ["Smoke cleansing", "Moonlight", "Soft dry cloth"],
        "pairs_well_with": ["blue-sapphire", "labradorite", "obsidian"],
        "avoid_with": ["ruby", "yellow-sapphire"],
        "affirmation": "I move through uncertainty with clarity, protection, and composure.",
        "caution": "Hessonite can feel intense during already volatile Rahu-style periods, so use with grounding support.",
    },
    "cats-eye": {
        "display_name": "Cat's Eye",
        "tagline": "A Ketu gem for insight, detachment, and focused spiritual protection",
        "color": "Honey green to grey",
        "chakras": ["Third Eye", "Root"],
        "element": "Ether",
        "planet": "Ketu",
        "zodiac": ["Scorpio", "Pisces", "Sagittarius"],
        "hardness_mohs": 8.5,
        "benefit_tags": ["intuition", "protection", "release", "focus"],
        "physical_support": ["supports energetic detachment", "encourages steadiness during inward phases", "pairs well with dream and meditation work"],
        "best_intentions": ["intuition", "spiritual-growth", "meditation", "protection"],
        "how_to_use": ["Use when you want stronger spiritual focus and less outer noise.", "Pair with grounding stones in meditation or dreamwork.", "Work with it gently during times of detachment or karmic reset."],
        "cleansing_methods": ["Moonlight", "Smoke cleansing", "Sound cleansing"],
        "pairs_well_with": ["fluorite", "lepidolite", "hessonite-garnet"],
        "avoid_with": ["ruby", "pearl"],
        "affirmation": "I trust quiet insight and release what no longer serves my path.",
        "caution": "Cat's Eye can magnify inwardness, so balance it with grounding if life already feels isolating.",
    },
    "amethyst": {
        "display_name": "Amethyst",
        "tagline": "The classic stone of peace, protection, and spiritual calm",
        "color": "Purple to violet",
        "chakras": ["Third Eye", "Crown"],
        "element": "Air",
        "planet": "Saturn / Neptune",
        "zodiac": ["Aquarius", "Pisces", "Capricorn"],
        "hardness_mohs": 7,
        "benefit_tags": ["peace", "intuition", "protection", "sleep"],
        "physical_support": ["supports better bedtime rituals", "encourages calmer mental pacing", "helps settle overstimulation"],
        "best_intentions": ["anxiety-stress", "sleep", "spiritual-growth", "intuition", "meditation"],
        "how_to_use": ["Place on the bedside table for calmer sleep energy.", "Hold during meditation to quiet mental chatter.", "Keep in a room corner as part of a simple protection layout."],
        "cleansing_methods": ["Moonlight", "Smoke cleansing", "Selenite slab"],
        "pairs_well_with": ["clear-quartz", "black-tourmaline", "selenite"],
        "avoid_with": ["citrine"],
        "affirmation": "I am calm, protected, and deeply connected to inner wisdom.",
        "caution": "Long direct sunlight can fade the purple color over time.",
    },
    "rose-quartz": {
        "display_name": "Rose Quartz",
        "tagline": "The heart crystal of tenderness, softness, and emotional repair",
        "color": "Soft pink",
        "chakras": ["Heart"],
        "element": "Water",
        "planet": "Venus",
        "zodiac": ["Taurus", "Libra", "Cancer"],
        "hardness_mohs": 7,
        "benefit_tags": ["love", "compassion", "healing", "peace"],
        "physical_support": ["supports soothing bedtime energy", "encourages softer breathing and emotional release", "pairs well with nurturing rituals"],
        "best_intentions": ["love-relationships", "grief-healing", "forgiveness", "fertility"],
        "how_to_use": ["Keep in the bedroom or on a self-care altar.", "Hold over the heart during gentle breathing work.", "Wear as a pendant when you want more warmth and softness through the day."],
        "cleansing_methods": ["Moonlight", "Smoke cleansing", "Water rinse"],
        "pairs_well_with": ["rhodonite", "moonstone", "clear-quartz"],
        "avoid_with": ["obsidian"],
        "affirmation": "I am worthy of love that is gentle, honest, and nourishing.",
        "caution": "Rose quartz can fade with prolonged strong sunlight.",
    },
    "clear-quartz": {
        "display_name": "Clear Quartz",
        "tagline": "A master amplifier for focus, intention, and energetic clarity",
        "color": "Clear to milky white",
        "chakras": ["All", "Crown"],
        "element": "Storm",
        "planet": "Sun / Moon",
        "zodiac": ["All signs"],
        "hardness_mohs": 7,
        "benefit_tags": ["clarity", "focus", "purification", "manifestation"],
        "physical_support": ["supports organized thinking", "pairs well with clean work habits", "encourages a fresh energetic baseline"],
        "best_intentions": ["clarity-focus", "new-beginnings", "meditation", "abundance-money"],
        "how_to_use": ["Keep on your desk when you need a simple focus anchor.", "Program with one clear intention at a time.", "Use to amplify another stone in a pair or grid."],
        "cleansing_methods": ["Water rinse", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["amethyst", "citrine", "rose-quartz"],
        "avoid_with": [],
        "affirmation": "My energy is clear, focused, and aligned with my intention.",
        "caution": "Quartz amplifies whatever state you bring to it, so reset your intention regularly.",
    },
    "black-tourmaline": {
        "display_name": "Black Tourmaline",
        "tagline": "A classic shield stone for protection, boundaries, and grounding",
        "color": "Black",
        "chakras": ["Root"],
        "element": "Earth",
        "planet": "Saturn",
        "zodiac": ["Capricorn", "Scorpio", "Libra"],
        "hardness_mohs": 7.5,
        "benefit_tags": ["protection", "grounding", "boundaries", "resilience"],
        "physical_support": ["supports a steadier nervous system", "helps when environments feel draining", "pairs well with practical grounding habits"],
        "best_intentions": ["protection", "anxiety-stress", "travel-protection", "career-success"],
        "how_to_use": ["Place near your front door or workspace.", "Carry in a pocket during heavy social or travel days.", "Pair with selenite when you want both protection and clearing."],
        "cleansing_methods": ["Smoke cleansing", "Sound cleansing", "Dry salt nearby"],
        "pairs_well_with": ["selenite", "obsidian", "hematite"],
        "avoid_with": [],
        "affirmation": "I stay grounded, protected, and clear in every environment.",
        "caution": "Raw pieces can be brittle and should be handled with care.",
    },
    "citrine": {
        "display_name": "Citrine",
        "tagline": "A bright prosperity stone for confidence, joy, and momentum",
        "color": "Golden yellow",
        "chakras": ["Solar Plexus", "Sacral"],
        "element": "Fire",
        "planet": "Jupiter / Sun",
        "zodiac": ["Leo", "Gemini", "Aries"],
        "hardness_mohs": 7,
        "benefit_tags": ["abundance", "joy", "confidence", "manifestation"],
        "physical_support": ["supports energized action", "encourages lighter motivation", "pairs well with business and planning rituals"],
        "best_intentions": ["abundance-money", "confidence", "career-success", "creativity"],
        "how_to_use": ["Keep in a wallet corner, cash box, or desk area.", "Use during planning sessions for business or income goals.", "Pair with pyrite when you want strategy plus optimism."],
        "cleansing_methods": ["Smoke cleansing", "Sunlight briefly", "Sound cleansing"],
        "pairs_well_with": ["pyrite", "tigers-eye", "clear-quartz"],
        "avoid_with": ["amethyst"],
        "affirmation": "I welcome prosperity with confidence, joy, and wise action.",
        "caution": "Many citrine pieces are heat-treated amethyst and can fade in constant harsh sun.",
    },
    "lapis-lazuli": {
        "display_name": "Lapis Lazuli",
        "tagline": "A wisdom stone for truth, intuition, and inner authority",
        "color": "Royal blue with gold flecks",
        "chakras": ["Third Eye", "Throat"],
        "element": "Air",
        "planet": "Jupiter",
        "zodiac": ["Sagittarius", "Libra", "Virgo"],
        "hardness_mohs": 5.5,
        "benefit_tags": ["truth", "intuition", "communication", "clarity"],
        "physical_support": ["supports thoughtful communication", "encourages reflective calm", "pairs well with study and spiritual inquiry"],
        "best_intentions": ["intuition", "truth-honesty", "communication", "spiritual-growth"],
        "how_to_use": ["Wear near the throat for clearer expression.", "Use in meditation or journaling for insight work.", "Keep close when truth-telling feels emotionally loaded."],
        "cleansing_methods": ["Smoke cleansing", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["sodalite", "moonstone", "clear-quartz"],
        "avoid_with": [],
        "affirmation": "I speak my truth and trust what deeper wisdom reveals.",
        "caution": "Because lapis is porous, avoid soaking it in water for long periods.",
    },
    "obsidian": {
        "display_name": "Obsidian",
        "tagline": "A mirror-like protector for truth, release, and shadow work",
        "color": "Black",
        "chakras": ["Root"],
        "element": "Earth",
        "planet": "Saturn / Pluto",
        "zodiac": ["Scorpio", "Capricorn", "Sagittarius"],
        "hardness_mohs": 5.5,
        "benefit_tags": ["protection", "truth", "release", "grounding"],
        "physical_support": ["supports heavy clearing rituals", "helps create emotional containment", "pairs well with structured shadow work"],
        "best_intentions": ["protection", "forgiveness", "anxiety-stress", "truth-honesty"],
        "how_to_use": ["Use in short sessions when you want honest self-reflection.", "Keep near an entrance for a dense protective tone.", "Pair with a softer heart stone if the energy feels too stark."],
        "cleansing_methods": ["Smoke cleansing", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["black-tourmaline", "amethyst", "labradorite"],
        "avoid_with": ["rose-quartz"],
        "affirmation": "I release what is false and stand firmly in the truth.",
        "caution": "Obsidian can feel intense for sensitive people, so build slowly.",
    },
    "selenite": {
        "display_name": "Selenite",
        "tagline": "A luminous cleansing crystal for peace, sleep, and sacred space",
        "color": "White to translucent",
        "chakras": ["Crown"],
        "element": "Air",
        "planet": "Moon",
        "zodiac": ["Cancer", "Taurus", "Pisces"],
        "hardness_mohs": 2,
        "benefit_tags": ["purification", "peace", "sleep", "intuition"],
        "physical_support": ["supports slower evening transitions", "encourages cleaner room energy", "pairs well with sleep and meditation routines"],
        "best_intentions": ["sleep", "meditation", "anxiety-stress", "spiritual-growth"],
        "how_to_use": ["Place beside the bed or meditation seat.", "Use as a charging slab for smaller crystals.", "Keep in a room that needs a lighter, cleaner atmosphere."],
        "cleansing_methods": ["Sound cleansing", "Moonlight", "Dry-cloth wipe"],
        "pairs_well_with": ["amethyst", "black-tourmaline", "moonstone"],
        "avoid_with": [],
        "affirmation": "My space, mind, and spirit are clear and gently renewed.",
        "caution": "Selenite should be kept dry because it can soften or damage in water.",
    },
    "malachite": {
        "display_name": "Malachite",
        "tagline": "A bold transformation stone for release, courage, and heart power",
        "color": "Banded green",
        "chakras": ["Heart", "Solar Plexus"],
        "element": "Earth",
        "planet": "Venus / Pluto",
        "zodiac": ["Scorpio", "Capricorn", "Taurus"],
        "hardness_mohs": 3.5,
        "benefit_tags": ["transformation", "courage", "healing", "boundaries"],
        "physical_support": ["supports strong emotional processing", "encourages decisive change", "pairs well with release rituals"],
        "best_intentions": ["forgiveness", "new-beginnings", "confidence", "grief-healing"],
        "how_to_use": ["Use in short, focused rituals when you are ready for change.", "Pair with grounding stones if life already feels intense.", "Keep near the heart or solar plexus in transition work."],
        "cleansing_methods": ["Smoke cleansing", "Sound cleansing", "Dry-cloth wipe"],
        "pairs_well_with": ["rose-quartz", "clear-quartz", "hematite"],
        "avoid_with": [],
        "affirmation": "I release old fear and choose brave, heart-led transformation.",
        "caution": "Raw malachite should not be soaked or handled carelessly because the dust is not meant for inhalation.",
    },
    "carnelian": {
        "display_name": "Carnelian",
        "tagline": "A warm creative stone for courage, action, and joyful momentum",
        "color": "Orange to reddish orange",
        "chakras": ["Sacral", "Root"],
        "element": "Fire",
        "planet": "Mars / Sun",
        "zodiac": ["Aries", "Leo", "Virgo"],
        "hardness_mohs": 7,
        "benefit_tags": ["creativity", "confidence", "courage", "joy"],
        "physical_support": ["supports active motivation", "encourages movement and enthusiasm", "pairs well with productivity rituals"],
        "best_intentions": ["creativity", "confidence", "health-vitality", "new-beginnings"],
        "how_to_use": ["Carry before creative work, meetings, or performance moments.", "Place in a studio or active workspace.", "Use in short energizing rituals when you need momentum fast."],
        "cleansing_methods": ["Water rinse", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["sunstone", "tigers-eye", "bloodstone"],
        "avoid_with": [],
        "affirmation": "I create boldly, move freely, and trust my own fire.",
        "caution": "If you are already overstimulated, rotate carnelian with calmer stones.",
    },
    "moonstone": {
        "display_name": "Moonstone",
        "tagline": "A gentle lunar crystal for intuition, transitions, and emotional flow",
        "color": "Cream, white, or iridescent",
        "chakras": ["Sacral", "Third Eye", "Crown"],
        "element": "Water",
        "planet": "Moon",
        "zodiac": ["Cancer", "Pisces", "Libra"],
        "hardness_mohs": 6,
        "benefit_tags": ["intuition", "peace", "new-beginnings", "sleep"],
        "physical_support": ["supports emotional regulation", "encourages gentler cycle awareness", "pairs well with rest and reflection"],
        "best_intentions": ["intuition", "sleep", "new-beginnings", "fertility", "love-relationships"],
        "how_to_use": ["Keep by your bed or carry during transitions.", "Use in moon rituals, journaling, or dreamwork.", "Wear near the heart or sacral area for softer emotional flow."],
        "cleansing_methods": ["Moonlight", "Smoke cleansing", "Soft water rinse"],
        "pairs_well_with": ["rose-quartz", "selenite", "lapis-lazuli"],
        "avoid_with": ["hessonite-garnet"],
        "affirmation": "I trust change, intuition, and the gentle unfolding of my path.",
        "caution": "Moonstone can scratch more easily than harder crystals, so store it gently.",
    },
    "labradorite": {
        "display_name": "Labradorite",
        "tagline": "A mystical stone for intuition, protection, and threshold moments",
        "color": "Grey with blue-green flash",
        "chakras": ["Third Eye", "Throat"],
        "element": "Storm",
        "planet": "Rahu / Uranus",
        "zodiac": ["Aquarius", "Scorpio", "Sagittarius"],
        "hardness_mohs": 6.5,
        "benefit_tags": ["intuition", "protection", "transformation", "focus"],
        "physical_support": ["supports energetic resilience", "encourages steadiness during change", "pairs well with spiritual practice that still needs grounding"],
        "best_intentions": ["spiritual-growth", "intuition", "protection", "new-beginnings"],
        "how_to_use": ["Carry during transitions or spiritually intense seasons.", "Use in meditation when you want insight with protection.", "Pair with black tourmaline when you need both magic and grounding."],
        "cleansing_methods": ["Moonlight", "Smoke cleansing", "Sound cleansing"],
        "pairs_well_with": ["amethyst", "black-tourmaline", "moonstone"],
        "avoid_with": [],
        "affirmation": "I move through change protected, aware, and open to insight.",
        "caution": "Labradorite works best when balanced with grounding habits and enough rest.",
    },
    "pyrite": {
        "display_name": "Pyrite",
        "tagline": "A strategic prosperity stone for confidence, protection, and drive",
        "color": "Brassy gold",
        "chakras": ["Solar Plexus"],
        "element": "Fire",
        "planet": "Mars / Sun",
        "zodiac": ["Leo", "Aries", "Capricorn"],
        "hardness_mohs": 6.5,
        "benefit_tags": ["abundance", "confidence", "protection", "manifestation"],
        "physical_support": ["supports productive energy", "helps hold focus around goals", "pairs well with business structure and ambition"],
        "best_intentions": ["abundance-money", "career-success", "confidence", "travel-protection"],
        "how_to_use": ["Keep in your workspace, money corner, or business planning area.", "Pair with citrine for wealth rituals rooted in action.", "Use before interviews, launches, or negotiations."],
        "cleansing_methods": ["Smoke cleansing", "Sound cleansing", "Dry-cloth wipe"],
        "pairs_well_with": ["citrine", "tigers-eye", "clear-quartz"],
        "avoid_with": [],
        "affirmation": "I protect my energy and build prosperity with courage and strategy.",
        "caution": "Pyrite can oxidize if repeatedly soaked, so keep cleansing methods dry.",
    },
    "amazonite": {
        "display_name": "Amazonite",
        "tagline": "A soothing truth stone for calm expression and balanced boundaries",
        "color": "Blue-green",
        "chakras": ["Throat", "Heart"],
        "element": "Water",
        "planet": "Mercury / Uranus",
        "zodiac": ["Virgo", "Aquarius", "Libra"],
        "hardness_mohs": 6,
        "benefit_tags": ["communication", "truth", "peace", "boundaries"],
        "physical_support": ["supports calmer speech", "encourages emotional regulation in conversations", "pairs well with journaling and conflict repair"],
        "best_intentions": ["communication", "truth-honesty", "anxiety-stress", "clarity-focus"],
        "how_to_use": ["Wear near the throat for honest but softened communication.", "Keep on your desk during writing or difficult conversations.", "Use when you need to state a boundary without losing warmth."],
        "cleansing_methods": ["Smoke cleansing", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["aquamarine", "sodalite", "emerald"],
        "avoid_with": [],
        "affirmation": "I speak from truth, calm, and clear emotional balance.",
        "caution": "Amazonite is best handled gently and not left in long direct sun.",
    },
    "sodalite": {
        "display_name": "Sodalite",
        "tagline": "A reasoning stone for truth, focus, and composed communication",
        "color": "Blue with white veining",
        "chakras": ["Throat", "Third Eye"],
        "element": "Air",
        "planet": "Mercury",
        "zodiac": ["Sagittarius", "Virgo", "Aquarius"],
        "hardness_mohs": 5.5,
        "benefit_tags": ["clarity", "truth", "communication", "focus"],
        "physical_support": ["supports organized thought", "encourages calm speaking under pressure", "pairs well with study and strategic work"],
        "best_intentions": ["clarity-focus", "truth-honesty", "communication", "career-success"],
        "how_to_use": ["Keep beside your notebook, laptop, or reading chair.", "Hold before important conversations or writing sessions.", "Use in planning rituals when you need logic without emotional noise."],
        "cleansing_methods": ["Smoke cleansing", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["clear-quartz", "lapis-lazuli", "amazonite"],
        "avoid_with": [],
        "affirmation": "My thoughts are orderly, truthful, and ready to be expressed clearly.",
        "caution": "Sodalite works best in focused rituals rather than chaotic multi-stone combinations.",
    },
    "aventurine": {
        "display_name": "Green Aventurine",
        "tagline": "A luck and renewal stone for gentle growth and opportunity",
        "color": "Soft green",
        "chakras": ["Heart"],
        "element": "Earth",
        "planet": "Mercury / Venus",
        "zodiac": ["Taurus", "Virgo", "Libra"],
        "hardness_mohs": 7,
        "benefit_tags": ["abundance", "healing", "new-beginnings", "joy"],
        "physical_support": ["supports fresh momentum", "encourages emotional lightness", "pairs well with growth-oriented routines"],
        "best_intentions": ["abundance-money", "new-beginnings", "love-relationships", "career-success"],
        "how_to_use": ["Carry when you want a lighter, luckier tone around a new chapter.", "Keep near job applications, goals, or study plans.", "Pair with clear quartz when you want both luck and intention."],
        "cleansing_methods": ["Water rinse", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["emerald", "citrine", "jade"],
        "avoid_with": [],
        "affirmation": "I welcome growth, luck, and fresh opportunity with an open heart.",
        "caution": None,
    },
    "tigers-eye": {
        "display_name": "Tiger's Eye",
        "tagline": "A stabilizing power stone for confidence, money, and discernment",
        "color": "Golden brown",
        "chakras": ["Solar Plexus", "Root"],
        "element": "Earth",
        "planet": "Sun / Mars",
        "zodiac": ["Leo", "Capricorn", "Gemini"],
        "hardness_mohs": 7,
        "benefit_tags": ["confidence", "abundance", "grounding", "focus"],
        "physical_support": ["supports decisive action", "helps stabilize ambition", "pairs well with work and finance rituals"],
        "best_intentions": ["confidence", "abundance-money", "career-success", "travel-protection"],
        "how_to_use": ["Carry during negotiations, interviews, or travel.", "Keep on a desk when decisions require grounded confidence.", "Use in prosperity rituals where courage matters as much as luck."],
        "cleansing_methods": ["Smoke cleansing", "Sunlight briefly", "Sound cleansing"],
        "pairs_well_with": ["pyrite", "citrine", "carnelian"],
        "avoid_with": [],
        "affirmation": "I act with grounded confidence and wise discernment.",
        "caution": None,
    },
    "jade": {
        "display_name": "Jade",
        "tagline": "A nourishing prosperity stone for harmony, luck, and long-term balance",
        "color": "Green",
        "chakras": ["Heart"],
        "element": "Earth",
        "planet": "Venus / Jupiter",
        "zodiac": ["Taurus", "Libra", "Pisces"],
        "hardness_mohs": 6.5,
        "benefit_tags": ["abundance", "peace", "healing", "compassion"],
        "physical_support": ["supports balanced pacing", "encourages sustainable growth", "pairs well with nurturing self-care rituals"],
        "best_intentions": ["abundance-money", "fertility", "love-relationships", "health-vitality"],
        "how_to_use": ["Keep in your wallet area, bedroom, or personal altar.", "Use for abundance work that aims for steadiness, not just speed.", "Pair with rose quartz when prosperity and harmony both matter."],
        "cleansing_methods": ["Water rinse", "Moonlight", "Soft-cloth wipe"],
        "pairs_well_with": ["aventurine", "rose-quartz", "citrine"],
        "avoid_with": [],
        "affirmation": "I build a life of peace, prosperity, and lasting balance.",
        "caution": None,
    },
    "hematite": {
        "display_name": "Hematite",
        "tagline": "A dense grounding stone for boundaries, focus, and energetic stability",
        "color": "Metallic grey",
        "chakras": ["Root"],
        "element": "Earth",
        "planet": "Saturn / Mars",
        "zodiac": ["Capricorn", "Aries", "Aquarius"],
        "hardness_mohs": 5.5,
        "benefit_tags": ["grounding", "protection", "focus", "boundaries"],
        "physical_support": ["supports a sense of steadiness in the body", "helps with practical focus", "pairs well with stress-reduction routines"],
        "best_intentions": ["anxiety-stress", "protection", "clarity-focus", "travel-protection"],
        "how_to_use": ["Carry when you feel floaty, scattered, or drained.", "Use before work that demands practical focus.", "Pair with amethyst when you want calm without losing grounding."],
        "cleansing_methods": ["Smoke cleansing", "Sound cleansing", "Dry-cloth wipe"],
        "pairs_well_with": ["black-tourmaline", "amethyst", "obsidian"],
        "avoid_with": [],
        "affirmation": "I am rooted, contained, and strong in my own energy.",
        "caution": "Keep hematite dry if it is polished with a coating that can wear over time.",
    },
    "lepidolite": {
        "display_name": "Lepidolite",
        "tagline": "A soft lilac stone for stress relief, rest, and emotional reset",
        "color": "Lilac to lavender",
        "chakras": ["Heart", "Third Eye", "Crown"],
        "element": "Water",
        "planet": "Moon / Saturn",
        "zodiac": ["Libra", "Pisces", "Aquarius"],
        "hardness_mohs": 2.5,
        "benefit_tags": ["peace", "sleep", "release", "healing"],
        "physical_support": ["supports bedtime calm", "encourages emotional decompression", "pairs well with stress-recovery rituals"],
        "best_intentions": ["anxiety-stress", "sleep", "grief-healing", "meditation"],
        "how_to_use": ["Keep beside the bed or in a self-soothing space.", "Hold when racing thoughts need to slow down.", "Use with selenite or amethyst for a gentle calming trio."],
        "cleansing_methods": ["Moonlight", "Sound cleansing", "Smoke cleansing"],
        "pairs_well_with": ["amethyst", "selenite", "moonstone"],
        "avoid_with": [],
        "affirmation": "I release tension and allow calm to return naturally.",
        "caution": "Lepidolite is relatively soft and should not be scrubbed or soaked aggressively.",
    },
    "rhodonite": {
        "display_name": "Rhodonite",
        "tagline": "A balanced heart stone for forgiveness, compassion, and emotional repair",
        "color": "Rose pink with black veining",
        "chakras": ["Heart"],
        "element": "Earth",
        "planet": "Mars / Venus",
        "zodiac": ["Taurus", "Libra", "Aries"],
        "hardness_mohs": 5.5,
        "benefit_tags": ["healing", "compassion", "forgiveness", "love"],
        "physical_support": ["supports emotional regulation during conflict repair", "encourages grounded heart work", "pairs well with grief rituals"],
        "best_intentions": ["love-relationships", "forgiveness", "grief-healing", "anxiety-stress"],
        "how_to_use": ["Keep close during healing conversations or journaling.", "Place over the heart during forgiveness practice.", "Pair with rose quartz when tenderness and accountability are both needed."],
        "cleansing_methods": ["Smoke cleansing", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["rose-quartz", "rhodochrosite", "moonstone"],
        "avoid_with": [],
        "affirmation": "My heart heals with compassion, honesty, and steady love.",
        "caution": None,
    },
    "fluorite": {
        "display_name": "Fluorite",
        "tagline": "A precision stone for focus, cleansing, and mental order",
        "color": "Green, purple, or rainbow",
        "chakras": ["Third Eye", "Crown"],
        "element": "Air",
        "planet": "Mercury",
        "zodiac": ["Pisces", "Capricorn", "Gemini"],
        "hardness_mohs": 4,
        "benefit_tags": ["focus", "clarity", "purification", "intuition"],
        "physical_support": ["supports study and concentration rituals", "helps reduce mental clutter", "pairs well with disciplined routines"],
        "best_intentions": ["clarity-focus", "intuition", "meditation", "new-beginnings"],
        "how_to_use": ["Keep near books, screens, or planning tools.", "Use before study or meditation to sharpen the mind.", "Pair with clear quartz for amplified precision."],
        "cleansing_methods": ["Smoke cleansing", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["clear-quartz", "sodalite", "amethyst"],
        "avoid_with": [],
        "affirmation": "My mind is organized, clear, and able to receive insight cleanly.",
        "caution": "Fluorite is softer than quartz, so protect it from impact and harsh water routines.",
    },
    "aquamarine": {
        "display_name": "Aquamarine",
        "tagline": "A cooling throat stone for truthful speech and emotional ease",
        "color": "Pale blue",
        "chakras": ["Throat", "Heart"],
        "element": "Water",
        "planet": "Moon / Mercury",
        "zodiac": ["Pisces", "Libra", "Gemini"],
        "hardness_mohs": 7.5,
        "benefit_tags": ["communication", "peace", "truth", "compassion"],
        "physical_support": ["supports calm public speaking", "encourages softer emotional processing", "pairs well with breath-based rituals"],
        "best_intentions": ["communication", "truth-honesty", "anxiety-stress", "love-relationships"],
        "how_to_use": ["Wear near the throat before important discussions.", "Use during journaling or prayer when emotional honesty matters.", "Pair with amazonite for calm but clear self-expression."],
        "cleansing_methods": ["Moonlight", "Water rinse", "Sound cleansing"],
        "pairs_well_with": ["amazonite", "turquoise", "rose-quartz"],
        "avoid_with": [],
        "affirmation": "I speak with calm clarity and let truth move through me gently.",
        "caution": None,
    },
    "chrysocolla": {
        "display_name": "Chrysocolla",
        "tagline": "A wise feminine stone for soothing communication and emotional flow",
        "color": "Blue-green",
        "chakras": ["Throat", "Heart"],
        "element": "Water",
        "planet": "Venus / Mercury",
        "zodiac": ["Taurus", "Gemini", "Virgo"],
        "hardness_mohs": 2.5,
        "benefit_tags": ["communication", "healing", "peace", "compassion"],
        "physical_support": ["supports emotional softness in speech", "encourages slower pacing", "pairs well with healing conversations"],
        "best_intentions": ["communication", "grief-healing", "forgiveness", "truth-honesty"],
        "how_to_use": ["Use in heart-to-heart conversations or self-reflection.", "Keep near a writing desk when you need gentler language.", "Work with it in quiet rituals rather than high-intensity layouts."],
        "cleansing_methods": ["Smoke cleansing", "Sound cleansing", "Moonlight"],
        "pairs_well_with": ["rose-quartz", "aquamarine", "amazonite"],
        "avoid_with": [],
        "affirmation": "I communicate with softness, honesty, and emotional wisdom.",
        "caution": "Chrysocolla is soft and should be kept away from soaking or rough handling.",
    },
    "sunstone": {
        "display_name": "Sunstone",
        "tagline": "A bright stone of joy, leadership, and radiant confidence",
        "color": "Peach to coppery orange",
        "chakras": ["Sacral", "Solar Plexus"],
        "element": "Fire",
        "planet": "Sun",
        "zodiac": ["Leo", "Libra", "Aries"],
        "hardness_mohs": 6.5,
        "benefit_tags": ["joy", "confidence", "creativity", "manifestation"],
        "physical_support": ["supports upbeat energy", "encourages motivation after stagnation", "pairs well with visibility and leadership rituals"],
        "best_intentions": ["confidence", "creativity", "career-success", "new-beginnings"],
        "how_to_use": ["Wear or carry when you need extra brightness and presence.", "Place on a workspace to spark optimism.", "Use before social or leadership moments that call for warmth."],
        "cleansing_methods": ["Sunlight briefly", "Smoke cleansing", "Sound cleansing"],
        "pairs_well_with": ["carnelian", "ruby", "pyrite"],
        "avoid_with": [],
        "affirmation": "I move with warmth, joy, and confident visibility.",
        "caution": None,
    },
    "bloodstone": {
        "display_name": "Bloodstone",
        "tagline": "A resilient warrior stone for vitality, courage, and grounded stamina",
        "color": "Dark green with red flecks",
        "chakras": ["Root", "Heart"],
        "element": "Earth",
        "planet": "Mars",
        "zodiac": ["Aries", "Scorpio", "Pisces"],
        "hardness_mohs": 6.5,
        "benefit_tags": ["vitality", "courage", "resilience", "grounding"],
        "physical_support": ["supports active recovery rituals", "encourages staying power", "pairs well with training or stamina goals"],
        "best_intentions": ["health-vitality", "confidence", "protection", "career-success"],
        "how_to_use": ["Carry during physically demanding or recovery-focused periods.", "Use in short grounding rituals before action.", "Pair with red coral or carnelian for strength with steadiness."],
        "cleansing_methods": ["Water rinse", "Smoke cleansing", "Moonlight"],
        "pairs_well_with": ["red-coral", "carnelian", "hematite"],
        "avoid_with": [],
        "affirmation": "I meet challenge with stamina, grounded strength, and courage.",
        "caution": None,
    },
    "turquoise": {
        "display_name": "Turquoise",
        "tagline": "A traveler and truth stone for protection, calm, and expression",
        "color": "Turquoise blue",
        "chakras": ["Throat", "Heart"],
        "element": "Air",
        "planet": "Jupiter / Venus",
        "zodiac": ["Sagittarius", "Pisces", "Aquarius"],
        "hardness_mohs": 5.5,
        "benefit_tags": ["protection", "communication", "peace", "truth"],
        "physical_support": ["supports emotional ease while traveling", "encourages relaxed communication", "pairs well with amulets and talismans"],
        "best_intentions": ["travel-protection", "communication", "truth-honesty", "protection"],
        "how_to_use": ["Carry in a bag or wear during journeys.", "Use before heartfelt conversations to encourage calm honesty.", "Keep near a door or car for protective symbolism."],
        "cleansing_methods": ["Smoke cleansing", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["aquamarine", "black-tourmaline", "amazonite"],
        "avoid_with": [],
        "affirmation": "I travel protected and speak my truth with an open heart.",
        "caution": "Turquoise is porous and should be protected from perfumes and soaking.",
    },
    "garnet": {
        "display_name": "Garnet",
        "tagline": "A deep red anchor for passion, stamina, and rooted commitment",
        "color": "Burgundy red",
        "chakras": ["Root"],
        "element": "Fire",
        "planet": "Mars",
        "zodiac": ["Aries", "Capricorn", "Leo"],
        "hardness_mohs": 7,
        "benefit_tags": ["vitality", "confidence", "love", "resilience"],
        "physical_support": ["supports grounded passion", "encourages staying power", "pairs well with long projects and devotion"],
        "best_intentions": ["love-relationships", "health-vitality", "confidence", "career-success"],
        "how_to_use": ["Wear when you want devotion, courage, and stamina together.", "Use in rituals for commitment and grounded desire.", "Keep near work that needs long-haul consistency."],
        "cleansing_methods": ["Water rinse", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["ruby", "bloodstone", "sunstone"],
        "avoid_with": [],
        "affirmation": "I bring passion, loyalty, and grounded strength to what I love.",
        "caution": None,
    },
    "onyx": {
        "display_name": "Onyx",
        "tagline": "A disciplined grounding stone for self-control and protection",
        "color": "Black",
        "chakras": ["Root"],
        "element": "Earth",
        "planet": "Saturn",
        "zodiac": ["Capricorn", "Leo", "Scorpio"],
        "hardness_mohs": 6.5,
        "benefit_tags": ["protection", "focus", "resilience", "boundaries"],
        "physical_support": ["supports emotional containment", "encourages disciplined pacing", "pairs well with long-term focus work"],
        "best_intentions": ["protection", "clarity-focus", "travel-protection", "career-success"],
        "how_to_use": ["Carry when you need clean boundaries and restraint.", "Place on your desk during demanding concentration work.", "Use in rituals that require self-control rather than expansion."],
        "cleansing_methods": ["Smoke cleansing", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["hematite", "black-tourmaline", "obsidian"],
        "avoid_with": [],
        "affirmation": "I stay composed, protected, and loyal to what matters most.",
        "caution": None,
    },
    "shungite": {
        "display_name": "Shungite",
        "tagline": "A modern grounding ally for clearing, shielding, and reset",
        "color": "Matte black",
        "chakras": ["Root"],
        "element": "Earth",
        "planet": "Saturn",
        "zodiac": ["Capricorn", "Aquarius", "Scorpio"],
        "hardness_mohs": 4,
        "benefit_tags": ["protection", "purification", "grounding", "boundaries"],
        "physical_support": ["supports environmental reset rituals", "encourages practical grounding", "pairs well with device-heavy spaces"],
        "best_intentions": ["protection", "travel-protection", "anxiety-stress", "clarity-focus"],
        "how_to_use": ["Keep near electronics or a workspace that feels overstimulating.", "Carry during travel or long screen-heavy days.", "Pair with selenite for clearing plus grounding."],
        "cleansing_methods": ["Smoke cleansing", "Dry-cloth wipe", "Sound cleansing"],
        "pairs_well_with": ["selenite", "black-tourmaline", "hematite"],
        "avoid_with": [],
        "affirmation": "I clear excess noise and stay rooted in my own field.",
        "caution": "Shungite is softer and may leave residue if rubbed against delicate surfaces.",
    },
    "rhodochrosite": {
        "display_name": "Rhodochrosite",
        "tagline": "A heart-healing stone for tenderness, worthiness, and emotional release",
        "color": "Rose pink to coral",
        "chakras": ["Heart", "Solar Plexus"],
        "element": "Water",
        "planet": "Venus",
        "zodiac": ["Leo", "Scorpio", "Taurus"],
        "hardness_mohs": 3.5,
        "benefit_tags": ["healing", "compassion", "forgiveness", "love"],
        "physical_support": ["supports emotional softness", "encourages self-worth rituals", "pairs well with grief and inner-child work"],
        "best_intentions": ["grief-healing", "forgiveness", "love-relationships", "fertility"],
        "how_to_use": ["Hold during self-compassion or inner-healing practices.", "Keep near your bed or journal.", "Pair with rhodonite or rose quartz for layered heart support."],
        "cleansing_methods": ["Moonlight", "Smoke cleansing", "Sound cleansing"],
        "pairs_well_with": ["rose-quartz", "rhodonite", "kunzite"],
        "avoid_with": [],
        "affirmation": "I soften into worthiness and allow the heart to heal.",
        "caution": "Rhodochrosite is soft, so avoid harsh scrubbing and repeated soaking.",
    },
    "prehnite": {
        "display_name": "Prehnite",
        "tagline": "A peaceful intuition stone for heart-led insight and mindful space",
        "color": "Soft green",
        "chakras": ["Heart", "Solar Plexus"],
        "element": "Earth",
        "planet": "Venus / Jupiter",
        "zodiac": ["Libra", "Virgo", "Pisces"],
        "hardness_mohs": 6.5,
        "benefit_tags": ["peace", "intuition", "healing", "meditation"],
        "physical_support": ["supports quiet restorative routines", "encourages gentle embodiment", "pairs well with reflective evening practice"],
        "best_intentions": ["meditation", "spiritual-growth", "anxiety-stress", "grief-healing"],
        "how_to_use": ["Use in meditation when you want insight to stay gentle and heart-led.", "Keep in a healing room or reflective corner.", "Pair with selenite for a light, calming setup."],
        "cleansing_methods": ["Moonlight", "Smoke cleansing", "Sound cleansing"],
        "pairs_well_with": ["selenite", "rose-quartz", "clear-quartz"],
        "avoid_with": [],
        "affirmation": "I receive insight with peace, softness, and trust.",
        "caution": None,
    },
    "calcite": {
        "display_name": "Calcite",
        "tagline": "A cleansing momentum stone for vitality, optimism, and fresh movement",
        "color": "Yellow, orange, or clear",
        "chakras": ["Solar Plexus", "Sacral"],
        "element": "Fire",
        "planet": "Sun / Jupiter",
        "zodiac": ["Leo", "Cancer", "Pisces"],
        "hardness_mohs": 3,
        "benefit_tags": ["vitality", "clarity", "joy", "purification"],
        "physical_support": ["supports energy reset rituals", "encourages cleaner motivation", "pairs well with practical recovery habits"],
        "best_intentions": ["health-vitality", "clarity-focus", "creativity", "new-beginnings"],
        "how_to_use": ["Keep in a bright workspace when you need fresh momentum.", "Use in short rituals after emotional or mental heaviness.", "Pair with citrine for optimism without excess intensity."],
        "cleansing_methods": ["Smoke cleansing", "Sound cleansing", "Dry-cloth wipe"],
        "pairs_well_with": ["citrine", "clear-quartz", "sunstone"],
        "avoid_with": [],
        "affirmation": "Fresh energy moves through me with optimism and clarity.",
        "caution": "Calcite is soft and can scratch or dissolve in repeated water exposure.",
    },
    "apatite": {
        "display_name": "Apatite",
        "tagline": "A vivid inspiration stone for focus, ideas, and expressive flow",
        "color": "Blue to teal",
        "chakras": ["Throat", "Third Eye"],
        "element": "Air",
        "planet": "Mercury",
        "zodiac": ["Gemini", "Sagittarius", "Aquarius"],
        "hardness_mohs": 5,
        "benefit_tags": ["creativity", "focus", "communication", "manifestation"],
        "physical_support": ["supports idea generation with structure", "encourages articulate momentum", "pairs well with writing and vision work"],
        "best_intentions": ["creativity", "clarity-focus", "communication", "career-success"],
        "how_to_use": ["Keep near sketchbooks, notebooks, or planning boards.", "Use before brainstorming or content creation.", "Pair with carnelian when you want ideas plus action."],
        "cleansing_methods": ["Smoke cleansing", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["carnelian", "clear-quartz", "amazonite"],
        "avoid_with": [],
        "affirmation": "Ideas move through me clearly and become meaningful action.",
        "caution": "Apatite is softer than quartz and should be protected from knocks.",
    },
    "angelite": {
        "display_name": "Angelite",
        "tagline": "A serene crystal for prayer, comfort, and spiritual gentleness",
        "color": "Soft blue",
        "chakras": ["Throat", "Crown"],
        "element": "Air",
        "planet": "Moon / Neptune",
        "zodiac": ["Aquarius", "Pisces", "Cancer"],
        "hardness_mohs": 3.5,
        "benefit_tags": ["peace", "intuition", "compassion", "meditation"],
        "physical_support": ["supports soothing prayerful states", "encourages emotional comfort", "pairs well with gentle spiritual routines"],
        "best_intentions": ["meditation", "grief-healing", "spiritual-growth", "sleep"],
        "how_to_use": ["Place in a prayer corner or on a bedside altar.", "Hold during grief, prayer, or soft contemplation.", "Use when you want spiritual practice to feel comforting rather than intense."],
        "cleansing_methods": ["Smoke cleansing", "Sound cleansing", "Moonlight"],
        "pairs_well_with": ["selenite", "celestite", "rose-quartz"],
        "avoid_with": [],
        "affirmation": "I am comforted, guided, and held in gentle spiritual peace.",
        "caution": "Angelite should be kept dry because water can damage the stone.",
    },
    "celestite": {
        "display_name": "Celestite",
        "tagline": "A high-frequency crystal for peace, sleep, and quiet guidance",
        "color": "Pale sky blue",
        "chakras": ["Crown", "Third Eye"],
        "element": "Air",
        "planet": "Moon / Jupiter",
        "zodiac": ["Pisces", "Libra", "Cancer"],
        "hardness_mohs": 3.5,
        "benefit_tags": ["sleep", "peace", "intuition", "meditation"],
        "physical_support": ["supports gentle bedtime rituals", "encourages emotional decompression", "pairs well with spiritual rest practices"],
        "best_intentions": ["sleep", "meditation", "spiritual-growth", "anxiety-stress"],
        "how_to_use": ["Keep by the bed or in a meditation corner.", "Use when you want peaceful, subtle spiritual support.", "Pair with selenite for a light sleep setup."],
        "cleansing_methods": ["Moonlight", "Sound cleansing", "Smoke cleansing"],
        "pairs_well_with": ["selenite", "amethyst", "angelite"],
        "avoid_with": [],
        "affirmation": "Peace flows through my mind, dreams, and spiritual practice.",
        "caution": "Celestite is fragile and best left in a stable place rather than carried daily.",
    },
    "kunzite": {
        "display_name": "Kunzite",
        "tagline": "A refined heart stone for tenderness, grief work, and emotional trust",
        "color": "Pale pink to lilac",
        "chakras": ["Heart", "Crown"],
        "element": "Water",
        "planet": "Venus",
        "zodiac": ["Taurus", "Libra", "Pisces"],
        "hardness_mohs": 6.5,
        "benefit_tags": ["love", "healing", "compassion", "grief-healing"],
        "physical_support": ["supports emotional softness after heartbreak", "encourages calm openness", "pairs well with rest and reflection"],
        "best_intentions": ["grief-healing", "love-relationships", "forgiveness", "sleep"],
        "how_to_use": ["Wear close to the heart when emotional tenderness is needed.", "Use in grief rituals, journaling, or breathwork.", "Pair with rose quartz or rhodochrosite for layered heart support."],
        "cleansing_methods": ["Moonlight", "Smoke cleansing", "Sound cleansing"],
        "pairs_well_with": ["rose-quartz", "rhodochrosite", "rhodonite"],
        "avoid_with": [],
        "affirmation": "My heart is safe enough to soften, feel, and heal.",
        "caution": "Kunzite can fade in strong light, so store it away from constant sun.",
    },
    "kyanite": {
        "display_name": "Kyanite",
        "tagline": "A direct alignment stone for truth, communication, and energetic order",
        "color": "Blue",
        "chakras": ["Throat", "Third Eye"],
        "element": "Air",
        "planet": "Mercury / Saturn",
        "zodiac": ["Libra", "Pisces", "Aries"],
        "hardness_mohs": 5,
        "benefit_tags": ["truth", "communication", "clarity", "focus"],
        "physical_support": ["supports clean energetic alignment", "encourages concise expression", "pairs well with difficult truth-telling"],
        "best_intentions": ["truth-honesty", "communication", "clarity-focus", "meditation"],
        "how_to_use": ["Use before honest conversations or decision-making sessions.", "Keep near your desk when alignment and precision matter.", "Pair with sodalite or aquamarine for balanced truth work."],
        "cleansing_methods": ["Sound cleansing", "Moonlight", "Smoke cleansing"],
        "pairs_well_with": ["sodalite", "aquamarine", "clear-quartz"],
        "avoid_with": [],
        "affirmation": "I return to alignment and speak what is true with steadiness.",
        "caution": "Raw kyanite blades can be delicate and are best handled gently.",
    },
    "larimar": {
        "display_name": "Larimar",
        "tagline": "A tranquil oceanic stone for calm speech and emotional cooling",
        "color": "Sea blue",
        "chakras": ["Throat", "Heart"],
        "element": "Water",
        "planet": "Venus / Moon",
        "zodiac": ["Leo", "Pisces", "Cancer"],
        "hardness_mohs": 5,
        "benefit_tags": ["peace", "communication", "compassion", "healing"],
        "physical_support": ["supports emotional cooling during conflict", "encourages gentler pacing", "pairs well with rest and nervous-system care"],
        "best_intentions": ["anxiety-stress", "communication", "love-relationships", "sleep"],
        "how_to_use": ["Use when you need calm expression and emotional cooling.", "Keep in a rest space or wear during tense conversations.", "Pair with aquamarine for a very soft throat-centered combination."],
        "cleansing_methods": ["Moonlight", "Smoke cleansing", "Sound cleansing"],
        "pairs_well_with": ["aquamarine", "rose-quartz", "selenite"],
        "avoid_with": [],
        "affirmation": "I soften, cool, and communicate from a peaceful heart.",
        "caution": "Larimar is softer and should be protected from scratching or harsh cleansing.",
    },
    "moldavite": {
        "display_name": "Moldavite",
        "tagline": "A catalytic tektite for accelerated change and spiritual awakening",
        "color": "Olive green",
        "chakras": ["Heart", "Third Eye", "Crown"],
        "element": "Storm",
        "planet": "Ketu / Uranus",
        "zodiac": ["Scorpio", "Aquarius", "Sagittarius"],
        "hardness_mohs": 5.5,
        "benefit_tags": ["transformation", "spiritual-growth", "expansion", "release"],
        "physical_support": ["supports breakthrough periods", "encourages movement out of stagnation", "pairs best with strong grounding support"],
        "best_intentions": ["spiritual-growth", "new-beginnings", "meditation", "intuition"],
        "how_to_use": ["Use in small doses during major personal transitions.", "Always pair with a grounding stone like hematite or black tourmaline.", "Rest from it when life already feels too accelerated."],
        "cleansing_methods": ["Smoke cleansing", "Moonlight", "Sound cleansing"],
        "pairs_well_with": ["black-tourmaline", "labradorite", "clear-quartz"],
        "avoid_with": [],
        "affirmation": "I welcome transformation that is aligned, awake, and grounded.",
        "caution": "Moldavite is famously intense and may feel overwhelming if used too much at once.",
    },
    "nuummite": {
        "display_name": "Nuummite",
        "tagline": "An ancient shadow stone for protection, grounding, and inner strength",
        "color": "Black with iridescent flashes",
        "chakras": ["Root", "Third Eye"],
        "element": "Earth",
        "planet": "Saturn / Pluto",
        "zodiac": ["Scorpio", "Capricorn", "Aquarius"],
        "hardness_mohs": 5.5,
        "benefit_tags": ["protection", "grounding", "truth", "resilience"],
        "physical_support": ["supports deep boundary work", "encourages staying centered in intensity", "pairs well with disciplined inner work"],
        "best_intentions": ["protection", "truth-honesty", "spiritual-growth", "anxiety-stress"],
        "how_to_use": ["Use in shadow work or protection rituals when you need depth and stability.", "Pair with softer heart stones if the process feels emotionally heavy.", "Keep in a private practice space rather than carrying constantly."],
        "cleansing_methods": ["Smoke cleansing", "Sound cleansing", "Moonlight"],
        "pairs_well_with": ["black-tourmaline", "obsidian", "amethyst"],
        "avoid_with": [],
        "affirmation": "I stand in my own depth with protection, honesty, and strength.",
        "caution": "Nuummite is best suited to intentional use rather than casual all-day exposure.",
    },
}


def _label_from_slug(slug: str) -> str:
    if slug in INTENTION_DEFINITIONS:
        return INTENTION_DEFINITIONS[slug]["display"]
    crystal = CRYSTAL_DEFINITIONS.get(slug)
    if crystal:
        return crystal["display_name"]
    return slug.replace("-", " ").title()


def _meta_description(profile: dict) -> str:
    top_tags = profile["benefit_tags"][:2]
    keywords = " and ".join(top_tags) if top_tags else "balance"
    crystal_name = profile["display_name"]
    return (
        f"{crystal_name} supports {keywords}. Discover its healing properties, chakra links, best uses, and practical ways to work with it every day."
    )


def _build_faq(profile: dict) -> list[dict]:
    name = profile["display_name"]
    chakra_text = ", ".join(profile["chakras"])
    cleansing_text = ", ".join(profile["cleansing_methods"][:3])
    intentions = ", ".join(_label_from_slug(slug) for slug in profile["best_intentions"][:3])
    return [
        {
            "q": f"What is {name} good for?",
            "a": f"{name} is often chosen for {intentions.lower()} because it naturally supports themes like {', '.join(profile['benefit_tags'][:3])}.",
        },
        {
            "q": f"Which chakra is {name} connected to?",
            "a": f"{name} is most commonly linked with {chakra_text}, which is why people use it for both emotional and spiritual balancing.",
        },
        {
            "q": f"How do I cleanse {name}?",
            "a": f"A simple cleansing routine for {name} includes {cleansing_text.lower()}. Choose the gentlest option if the stone is soft or porous.",
        },
        {
            "q": f"Can I use {name} every day?",
            "a": f"Yes, many people work with {name} daily. If the energy feels too strong, rotate it with a softer companion stone and give yourself rest days.",
        },
        {
            "q": f"Who should work with {name}?",
            "a": f"{name} tends to suit people who want support around {intentions.lower()} and who resonate with its {profile['element'].lower()}-element tone.",
        },
    ]


def _build_healing_properties(profile: dict) -> dict:
    emotional = [TAG_COPY[tag][0] for tag in profile["benefit_tags"][:4] if tag in TAG_COPY]
    spiritual = [TAG_COPY[tag][1] for tag in profile["benefit_tags"][:4] if tag in TAG_COPY]
    return {
        "emotional": emotional[:4],
        "physical": profile["physical_support"][:3],
        "spiritual": spiritual[:4],
    }


def _build_crystal_doc(slug: str, profile: dict) -> dict:
    doc = {
        "slug": slug,
        "display_name": profile["display_name"],
        "tagline": profile["tagline"],
        "color": profile["color"],
        "chakras": profile["chakras"],
        "element": profile["element"],
        "planet": profile["planet"],
        "zodiac": profile["zodiac"],
        "hardness_mohs": profile["hardness_mohs"],
        "healing_properties": _build_healing_properties(profile),
        "best_intentions": profile["best_intentions"],
        "how_to_use": profile["how_to_use"],
        "cleansing_methods": profile["cleansing_methods"],
        "pairs_well_with": profile["pairs_well_with"],
        "avoid_with": profile["avoid_with"],
        "affirmation": profile["affirmation"],
        "caution": profile.get("caution"),
        "faq": _build_faq(profile),
        "meta_title": f"{profile['display_name']} Crystal - Healing Properties, Chakra & How to Use",
        "meta_description": _meta_description(profile),
    }
    vedic = NAVARATNA_DETAILS.get(slug)
    if vedic:
        doc["vedic_name"] = vedic["vedic_name"]
        doc["wearing"] = vedic["wearing"]
        doc["synergy"] = vedic["synergy"]
        doc["conflict"] = vedic["conflict"]
    return doc


def _build_top_crystal_card(slug: str) -> dict:
    crystal = get_crystal_docs()[slug]
    return {
        "slug": slug,
        "display_name": crystal["display_name"],
        "tagline": crystal["tagline"],
        "color": crystal["color"],
        "chakras": crystal["chakras"],
        "intentions": crystal["best_intentions"],
    }


def _build_intention_doc(slug: str, payload: dict) -> dict:
    top_crystals = payload["top_crystals"]
    display = payload["display"]
    crystal_cards = [_build_top_crystal_card(crystal_slug) for crystal_slug in top_crystals]
    top_name = crystal_cards[0]["display_name"] if crystal_cards else "Crystal"
    faq = [
        {
            "q": f"What crystal is best for {display.lower()}?",
            "a": f"There is no single answer for everyone, but {top_name} is one of the most commonly chosen crystals for {display.lower()} because of its energetic fit.",
        },
        {
            "q": f"How do I use crystals for {display.lower()}?",
            "a": f"Choose one or two stones, set a clear intention, and keep them close to your body or in the space where this theme shows up most strongly.",
        },
        {
            "q": f"Can I combine multiple crystals for {display.lower()}?",
            "a": "Yes. Many people pair one grounding or clarifying crystal with one heart or intuition crystal so the effect feels balanced.",
        },
        {
            "q": f"How often should I cleanse crystals for {display.lower()}?",
            "a": "Weekly cleansing is a good baseline, and you can do it more often during emotionally intense or fast-changing periods.",
        },
        {
            "q": f"Do crystals replace practical action for {display.lower()}?",
            "a": "No. Crystals work best as supportive symbolic tools that reinforce choices, routines, communication, and care in the real world.",
        },
    ]
    return {
        "slug": slug,
        "display": display,
        "intro": payload["intro"],
        "top_crystals": top_crystals,
        "top_crystal_cards": crystal_cards,
        "how_to_use": payload["how_to_use"],
        "affirmation": payload["affirmation"],
        "faq": faq,
        "meta_title": f"Best Crystals for {display} - {top_name} & More",
        "meta_description": f"Looking for crystals for {display.lower()}? Discover the top stones, how to use them, and how to work with their energy more intentionally.",
    }


@lru_cache(maxsize=1)
def get_crystal_docs() -> dict[str, dict]:
    return {
        slug: _build_crystal_doc(slug, CRYSTAL_DEFINITIONS[slug])
        for slug in CRYSTAL_SLUGS
    }


@lru_cache(maxsize=1)
def get_intention_docs() -> dict[str, dict]:
    return {
        slug: _build_intention_doc(slug, payload)
        for slug, payload in INTENTION_DEFINITIONS.items()
    }


PLANET_CRYSTAL_DATA = {
    "sun": {
        "display": "Sun",
        "primary_slug": "ruby",
        "intro": "The Sun in Vedic astrology governs vitality, self-respect, authority, and the steady radiance of identity. When Sun energy is healthy, confidence feels warm and centered rather than loud or brittle.",
        "supporting_crystals": [
            {"slug": "sunstone", "why": "Sunstone carries a solar brightness that supports confidence, visibility, and leadership momentum."},
            {"slug": "garnet", "why": "Garnet reinforces stamina and devotion when Sun work requires commitment rather than performance."},
            {"slug": "citrine", "why": "Citrine supports optimistic action and helps solar confidence feel constructive and generous."},
        ],
        "crystals_to_avoid": ["blue-sapphire", "hessonite-garnet"],
        "who_should_wear": "Ruby is traditionally considered when Sun is weak, dignity is low, or leadership, recognition, and vitality need careful strengthening through a Vedic lens.",
        "how_to_use": [
            "Use the primary gemstone for direct solar strengthening and keep a softer support crystal on your desk during work hours.",
            "Begin Sunday rituals at sunrise with one short intention around confidence, clarity, or leadership.",
            "If the energy feels too heating, rotate ruby with gentler solar allies like sunstone rather than wearing everything at once.",
        ],
    },
    "moon": {
        "display": "Moon",
        "primary_slug": "pearl",
        "intro": "The Moon rules emotional rhythm, nourishment, intuition, and the mind's reflective surface. Balanced Moon energy feels restful, responsive, and emotionally intelligent rather than reactive or foggy.",
        "supporting_crystals": [
            {"slug": "moonstone", "why": "Moonstone helps restore emotional flow and supports transitions that need softness rather than force."},
            {"slug": "selenite", "why": "Selenite clears psychic residue and creates a lighter field for sleep, peace, and intuition."},
            {"slug": "rose-quartz", "why": "Rose quartz supports a gentler heart state when Moon themes involve sensitivity, grief, or relationship healing."},
        ],
        "crystals_to_avoid": ["hessonite-garnet", "blue-sapphire"],
        "who_should_wear": "Pearl is often considered when the Moon is stressed by Saturn, Rahu, or debility and the chart suggests emotional cooling is appropriate.",
        "how_to_use": [
            "Keep lunar stones near the bed or heart rather than in a loud, stimulating workspace.",
            "Use Moon-aligned crystals during evening reflection, prayer, or journaling when emotions need settling.",
            "If you are highly sensitive, work with one calming stone at a time so the ritual stays grounded.",
        ],
    },
    "mars": {
        "display": "Mars",
        "primary_slug": "red-coral",
        "intro": "Mars governs courage, heat, action, boundaries, and the ability to move from instinct into decisive action. Balanced Mars energy feels brave and constructive instead of impulsive, combative, or depleted.",
        "supporting_crystals": [
            {"slug": "bloodstone", "why": "Bloodstone supports endurance and grounded courage when Mars needs stamina more than raw heat."},
            {"slug": "carnelian", "why": "Carnelian restores creative fire, confidence, and movement when motivation has gone flat."},
            {"slug": "garnet", "why": "Garnet helps devotion and passion stay rooted instead of scattering into frustration."},
        ],
        "crystals_to_avoid": ["emerald", "blue-sapphire"],
        "who_should_wear": "Red Coral is usually approached when Mars needs strengthening for courage, protection, drive, or physical resilience and the full chart supports it.",
        "how_to_use": [
            "Work with Mars stones before exercise, difficult conversations, or projects that need decisive movement.",
            "Keep the ritual short and clear so energizing crystals do not spill into agitation.",
            "When anger is already high, choose the steadier Mars allies first and build up slowly.",
        ],
    },
    "mercury": {
        "display": "Mercury",
        "primary_slug": "emerald",
        "intro": "Mercury governs speech, discernment, trade, curiosity, and the skill of holding complexity without losing coherence. Healthy Mercury energy feels articulate, adaptable, and mentally elegant.",
        "supporting_crystals": [
            {"slug": "aventurine", "why": "Green Aventurine keeps Mercury's intelligence growth-oriented and emotionally lighter."},
            {"slug": "amazonite", "why": "Amazonite softens the throat and helps honest speech stay calm instead of nervous or sharp."},
            {"slug": "sodalite", "why": "Sodalite supports precise thinking, pattern recognition, and measured communication."},
        ],
        "crystals_to_avoid": ["pearl", "red-coral"],
        "who_should_wear": "Emerald is often considered when Mercury is weak, combust, or when communication, commerce, and decision-making need careful strengthening.",
        "how_to_use": [
            "Place Mercury stones near your notebook, laptop, or planning space so they support real communication work.",
            "Use them before writing, studying, meetings, or negotiations that need thoughtful articulation.",
            "Keep the intention specific so Mercury energy sharpens rather than scattering into overthinking.",
        ],
    },
    "jupiter": {
        "display": "Jupiter",
        "primary_slug": "yellow-sapphire",
        "intro": "Jupiter governs wisdom, grace, teachers, abundance, faith, and the bigger meaning behind a path. Balanced Jupiter energy feels generous, principled, and expansive without becoming inflated or vague.",
        "supporting_crystals": [
            {"slug": "citrine", "why": "Citrine adds optimism and momentum to Jupiter themes around prosperity and confident growth."},
            {"slug": "tigers-eye", "why": "Tiger's Eye keeps big Jupiter vision practical, disciplined, and financially grounded."},
            {"slug": "lapis-lazuli", "why": "Lapis deepens philosophical clarity and supports the truth-seeking side of Jupiter."},
        ],
        "crystals_to_avoid": ["emerald", "diamond"],
        "who_should_wear": "Yellow Sapphire is traditionally considered when Jupiter needs strengthening for guidance, marriage wisdom, prosperity, ethics, or teacher blessings.",
        "how_to_use": [
            "Work with Jupiter stones on Thursdays, during study, teaching, gratitude, or wisdom-centered planning.",
            "Pair a prosperity crystal with a truth crystal when you want growth that stays ethical and aligned.",
            "Keep Jupiter rituals spacious and intentional instead of hurried or transactional.",
        ],
    },
    "venus": {
        "display": "Venus",
        "primary_slug": "diamond",
        "intro": "Venus governs beauty, relationship harmony, pleasure, artistry, and refined magnetism. Balanced Venus energy feels graceful, receptive, and relationally intelligent rather than indulgent or emotionally entangled.",
        "supporting_crystals": [
            {"slug": "clear-quartz", "why": "Clear Quartz helps Venus intentions feel clean and intentional rather than overly sentimental."},
            {"slug": "rose-quartz", "why": "Rose Quartz softens the heart and supports affection, self-worth, and relationship healing."},
            {"slug": "jade", "why": "Jade supports gentle prosperity, peace, and long-term harmony in Venus-centered work."},
        ],
        "crystals_to_avoid": ["ruby", "red-coral"],
        "who_should_wear": "Diamond is traditionally considered when Venus needs strengthening around attraction, marriage, art, comfort, or relational grace and the chart supports that amplification.",
        "how_to_use": [
            "Keep Venus rituals aesthetically simple and emotionally sincere rather than crowded with too many stones.",
            "Use Friday as a day for gratitude, beauty rituals, and relational intention setting.",
            "When Venus themes feel tender, pair the gemstone with one heart crystal rather than stacking multiple amplifiers.",
        ],
    },
    "saturn": {
        "display": "Saturn",
        "primary_slug": "blue-sapphire",
        "intro": "Saturn governs discipline, karma, patience, consequences, and the maturity that comes from sustained effort. Balanced Saturn energy feels stable, truthful, and durable instead of heavy, fearful, or rigid.",
        "supporting_crystals": [
            {"slug": "amethyst", "why": "Amethyst helps Saturn lessons feel spiritually anchored and less emotionally harsh."},
            {"slug": "obsidian", "why": "Obsidian supports truth-telling and shadow work when Saturn is exposing what can no longer be avoided."},
            {"slug": "black-tourmaline", "why": "Black Tourmaline grounds Saturn energy into boundaries, steadiness, and environmental protection."},
        ],
        "crystals_to_avoid": ["ruby", "red-coral"],
        "who_should_wear": "Blue Sapphire is approached carefully when Saturn needs strengthening for discipline, protection, endurance, or karmic stabilization, and many practitioners prefer a gradual trial approach.",
        "how_to_use": [
            "Use Saturn stones for disciplined routines, boundaries, recovery from chaos, and long-cycle focus.",
            "Keep the ritual sober and steady; Saturn responds better to consistency than intensity.",
            "If the energy feels too heavy, move to the softer support stones before returning to the main gem.",
        ],
    },
    "rahu": {
        "display": "Rahu",
        "primary_slug": "hessonite-garnet",
        "intro": "Rahu governs amplification, obsession, foreignness, sudden turns, and the strange hunger that pushes growth beyond the familiar. Balanced Rahu energy feels innovative and strategic instead of chaotic or addictive.",
        "supporting_crystals": [
            {"slug": "labradorite", "why": "Labradorite helps Rahu transitions feel intuitive and protected rather than disorienting."},
            {"slug": "obsidian", "why": "Obsidian helps expose illusions and strengthens boundaries when Rahu clouds judgment."},
            {"slug": "shungite", "why": "Shungite adds modern grounding and shielding in overstimulating digital or social environments."},
        ],
        "crystals_to_avoid": ["ruby", "yellow-sapphire"],
        "who_should_wear": "Hessonite is typically considered when Rahu needs targeted balancing in the chart and when the native is navigating confusion, sudden change, or unusual karmic acceleration.",
        "how_to_use": [
            "Use Rahu stones when life feels overstimulating, seductive, or directionless and grounding is essential.",
            "Pair one intuitive stone with one protective stone so insight does not turn into more noise.",
            "Keep the ritual practical: desk placement, pocket carrying, or specific transition work tends to suit Rahu better than vague ceremony.",
        ],
    },
    "ketu": {
        "display": "Ketu",
        "primary_slug": "cats-eye",
        "intro": "Ketu governs detachment, moksha, karmic pruning, and the mysterious clarity that comes when outer noise falls away. Balanced Ketu energy feels intuitive, clean, and spiritually focused rather than dissociated or isolating.",
        "supporting_crystals": [
            {"slug": "fluorite", "why": "Fluorite keeps Ketu insight sharp, organized, and mentally usable."},
            {"slug": "lepidolite", "why": "Lepidolite softens anxiety when Ketu themes create emptiness, withdrawal, or over-detachment."},
            {"slug": "moonstone", "why": "Moonstone helps spiritual sensitivity stay emotionally humane and embodied."},
        ],
        "crystals_to_avoid": ["ruby", "pearl"],
        "who_should_wear": "Cat's Eye is traditionally considered when Ketu needs strengthening for insight, spiritual focus, or protection in difficult karmic phases and the full chart supports it.",
        "how_to_use": [
            "Use Ketu stones in meditation, dreamwork, and quiet reflective practice rather than highly social settings.",
            "Balance intense spiritual crystals with one soothing or grounding ally if life already feels detached.",
            "Short, regular rituals usually work better here than dramatic one-time ceremonies.",
        ],
    },
}

SIGN_CRYSTAL_DATA = {
    "aries": {
        "display": "Aries",
        "element": "Fire",
        "ruling_planet": "Mars",
        "traits": "bold, fast-moving, initiating, competitive",
        "intro": "Aries energy is direct, pioneering, and action-first. The best crystals for Aries support brave movement while helping fire become purposeful instead of impulsive.",
        "signature_crystals": [
            {"slug": "red-coral", "why": "Supports confident Mars-driven action with a classical Vedic edge.", "how_to_use": "Wear or carry when you need courage and clean follow-through."},
            {"slug": "carnelian", "why": "Adds creative fire and joyful momentum without overcomplicating the signal.", "how_to_use": "Keep in a workspace or pocket before high-energy tasks."},
            {"slug": "bloodstone", "why": "Builds stamina and helps Aries energy stay durable instead of burning too fast.", "how_to_use": "Use before exercise, training, or demanding action phases."},
            {"slug": "sunstone", "why": "Keeps Aries warmth radiant and enthusiastic rather than combative.", "how_to_use": "Use for leadership, visibility, and confidence rituals."},
        ],
        "shadow_crystals": [
            {"slug": "amethyst", "challenge": "impulsiveness", "why": "Amethyst slows the nervous system and helps action stay wiser."},
            {"slug": "hematite", "challenge": "impatience", "why": "Hematite grounds restless fire so the body can hold steadier timing."},
        ],
        "monthly_ritual": [
            "At the start of each month, hold one fire stone and name the single goal that deserves Aries effort most.",
            "Place a grounding stone beside it so courage stays disciplined throughout the month.",
            "Review progress halfway through the month and refine the goal instead of scattering energy across too many starts.",
        ],
    },
    "taurus": {
        "display": "Taurus",
        "element": "Earth",
        "ruling_planet": "Venus",
        "traits": "steady, sensory, loyal, comfort-seeking",
        "intro": "Taurus energy values stability, beauty, rhythm, and tangible results. The best crystals for Taurus preserve calm and abundance while preventing comfort from becoming stagnation.",
        "signature_crystals": [
            {"slug": "rose-quartz", "why": "Matches Taurus softness, loyalty, and heart-centered Venus energy.", "how_to_use": "Keep near the heart or bedside for relational steadiness."},
            {"slug": "jade", "why": "Supports grounded prosperity and calm long-term growth.", "how_to_use": "Place in a wallet area or home abundance corner."},
            {"slug": "emerald", "why": "Refines Venus and Mercury expression for Taurus people building graceful success.", "how_to_use": "Use during planning, finances, or thoughtful communication."},
            {"slug": "aventurine", "why": "Keeps growth light and optimistic when Taurus needs a fresh chapter.", "how_to_use": "Carry during change-heavy periods or new opportunities."},
        ],
        "shadow_crystals": [
            {"slug": "fluorite", "challenge": "stubbornness", "why": "Fluorite introduces flexibility and cleaner perspective."},
            {"slug": "citrine", "challenge": "inertia", "why": "Citrine restores movement and motivation when comfort becomes a rut."},
        ],
        "monthly_ritual": [
            "Choose one crystal for beauty and one for stability at the start of the month.",
            "Refresh your personal space with them so your environment supports the life you want to maintain.",
            "End the month with gratitude practice and a practical prosperity review.",
        ],
    },
    "gemini": {
        "display": "Gemini",
        "element": "Air",
        "ruling_planet": "Mercury",
        "traits": "curious, witty, adaptive, mentally quick",
        "intro": "Gemini energy is mobile, curious, expressive, and mentally alive. The best crystals for Gemini help thoughts flow clearly while reducing nervous scattering and mixed signals.",
        "signature_crystals": [
            {"slug": "emerald", "why": "A classic Mercury stone for speech, strategy, and mental grace.", "how_to_use": "Use near writing, study, or communication work."},
            {"slug": "amazonite", "why": "Softens the throat and supports calmer self-expression.", "how_to_use": "Wear or hold before important conversations."},
            {"slug": "sodalite", "why": "Improves order, truth, and concentration when the mind is moving too fast.", "how_to_use": "Keep by your notebook or laptop."},
            {"slug": "apatite", "why": "Feeds lively ideas while keeping them usable and expressive.", "how_to_use": "Use in brainstorming and creative planning."},
        ],
        "shadow_crystals": [
            {"slug": "hematite", "challenge": "mental scattering", "why": "Hematite grounds a busy mind into one clear next step."},
            {"slug": "amethyst", "challenge": "overstimulation", "why": "Amethyst lowers mental noise and helps rest return."},
        ],
        "monthly_ritual": [
            "Start the month by choosing one communication goal and one learning goal.",
            "Pair a Mercury crystal with a grounding stone on your desk.",
            "Once a week, journal what ideas deserve action and what needs to be released.",
        ],
    },
    "cancer": {
        "display": "Cancer",
        "element": "Water",
        "ruling_planet": "Moon",
        "traits": "protective, sensitive, intuitive, nurturing",
        "intro": "Cancer energy is emotionally intelligent, protective, and deeply tied to home and belonging. The best crystals for Cancer support softness and intuition while keeping sensitivity from turning into overwhelm.",
        "signature_crystals": [
            {"slug": "pearl", "why": "Pearl mirrors Cancer's lunar need for emotional cooling and peace.", "how_to_use": "Wear gently or keep near rest spaces."},
            {"slug": "moonstone", "why": "Supports intuition, transitions, and emotional flow.", "how_to_use": "Use in moon rituals, journaling, or bedtime practice."},
            {"slug": "selenite", "why": "Clears heavy room energy and helps Cancer spaces feel calmer.", "how_to_use": "Place in the bedroom or a quiet corner of home."},
            {"slug": "rose-quartz", "why": "Supports tenderness and emotional repair without pushing too hard.", "how_to_use": "Keep close during relationship or grief work."},
        ],
        "shadow_crystals": [
            {"slug": "black-tourmaline", "challenge": "emotional over-absorption", "why": "Black Tourmaline helps create boundaries around what you take in."},
            {"slug": "fluorite", "challenge": "mood fog", "why": "Fluorite restores mental structure when feelings become cloudy."},
        ],
        "monthly_ritual": [
            "Refresh your bedroom or altar space at the start of the month with one lunar crystal and one boundary stone.",
            "Use them while naming the emotional tone you want your home to hold.",
            "At month end, cleanse the stones and release what the space no longer needs to carry.",
        ],
    },
    "leo": {
        "display": "Leo",
        "element": "Fire",
        "ruling_planet": "Sun",
        "traits": "radiant, loyal, expressive, proud",
        "intro": "Leo energy wants to create, shine, and lead from the heart. The best crystals for Leo nourish healthy confidence while preventing pride, burnout, or validation-seeking from taking over.",
        "signature_crystals": [
            {"slug": "ruby", "why": "Ruby strengthens solar leadership, dignity, and life force.", "how_to_use": "Use during confidence, leadership, or visibility rituals."},
            {"slug": "sunstone", "why": "Sunstone keeps Leo expression playful, bright, and charismatic.", "how_to_use": "Carry before performance or social leadership moments."},
            {"slug": "citrine", "why": "Citrine adds optimism and creative solar momentum.", "how_to_use": "Place in a studio or workspace."},
            {"slug": "garnet", "why": "Garnet supports loyalty and staying power underneath the shine.", "how_to_use": "Wear when devotion and consistency matter."},
        ],
        "shadow_crystals": [
            {"slug": "amethyst", "challenge": "ego reactivity", "why": "Amethyst cools the system so confidence stays centered."},
            {"slug": "rose-quartz", "challenge": "validation hunger", "why": "Rose Quartz reconnects Leo pride with warmth and heart."},
        ],
        "monthly_ritual": [
            "Choose one solar crystal at the start of the month and pair it with a heart crystal.",
            "Name where you want to lead, create, or be seen with integrity.",
            "At the end of the month, reflect on what felt authentic versus performative.",
        ],
    },
    "virgo": {
        "display": "Virgo",
        "element": "Earth",
        "ruling_planet": "Mercury",
        "traits": "precise, service-oriented, analytical, refining",
        "intro": "Virgo energy notices detail, seeks usefulness, and wants systems that actually work. The best crystals for Virgo preserve discernment while easing perfectionism, worry, and overcorrection.",
        "signature_crystals": [
            {"slug": "emerald", "why": "Supports clarity, reasoning, and skillful communication for practical Virgo work.", "how_to_use": "Keep near planning, study, or service-oriented tasks."},
            {"slug": "sodalite", "why": "Sodalite organizes thought and helps Virgo communicate cleanly under pressure.", "how_to_use": "Use during writing, analysis, and decision work."},
            {"slug": "fluorite", "why": "Fluorite supports clean mental structure without emotional clutter.", "how_to_use": "Place near books, schedules, or a work desk."},
            {"slug": "amazonite", "why": "Softens self-criticism and helps truth stay calm and humane.", "how_to_use": "Use before difficult conversations or feedback."},
        ],
        "shadow_crystals": [
            {"slug": "rose-quartz", "challenge": "self-criticism", "why": "Rose Quartz makes room for compassion inside high standards."},
            {"slug": "hematite", "challenge": "anxious over-analysis", "why": "Hematite grounds the mind when loops become unhelpful."},
        ],
        "monthly_ritual": [
            "At the start of each month, write the three systems you most want to improve.",
            "Choose one clarity stone and one compassion stone to keep beside that list.",
            "Review weekly and simplify rather than adding more pressure.",
        ],
    },
    "libra": {
        "display": "Libra",
        "element": "Air",
        "ruling_planet": "Venus",
        "traits": "harmonizing, relational, aesthetic, diplomatic",
        "intro": "Libra energy seeks harmony, proportion, and graceful relating. The best crystals for Libra support beauty and connection while helping indecision, people-pleasing, or over-accommodation soften.",
        "signature_crystals": [
            {"slug": "diamond", "why": "Supports refined Venus energy, elegance, and clear relational values.", "how_to_use": "Use in self-worth and relationship rituals."},
            {"slug": "rose-quartz", "why": "Keeps Libra tenderness present without losing softness.", "how_to_use": "Wear near the heart or keep by the bed."},
            {"slug": "amazonite", "why": "Helps Libra speak truth without sacrificing peace.", "how_to_use": "Use before conversations that need balance and honesty."},
            {"slug": "jade", "why": "Supports calm harmony and graceful prosperity.", "how_to_use": "Keep in a home or personal altar space."},
        ],
        "shadow_crystals": [
            {"slug": "tigers-eye", "challenge": "indecision", "why": "Tiger's Eye adds grounded conviction when Libra wavers too long."},
            {"slug": "hematite", "challenge": "people-pleasing", "why": "Hematite helps Libra remember its own center and boundaries."},
        ],
        "monthly_ritual": [
            "Clear and beautify one shared space at the start of the month.",
            "Place one Venus crystal and one boundary crystal there with an intention for honest harmony.",
            "Mid-month, review where peace is real and where it is only avoidance.",
        ],
    },
    "scorpio": {
        "display": "Scorpio",
        "element": "Water",
        "ruling_planet": "Mars / Ketu",
        "traits": "intense, private, transformative, loyal",
        "intro": "Scorpio energy moves toward depth, secrecy, intensity, and transformation. The best crystals for Scorpio support emotional truth and psychic resilience without tipping into suspicion, obsession, or self-protection that never softens.",
        "signature_crystals": [
            {"slug": "red-coral", "why": "Supports strength, protection, and decisive emotional courage.", "how_to_use": "Use in focused rituals for empowerment and protection."},
            {"slug": "obsidian", "why": "Helps Scorpio face shadow material honestly and with structure.", "how_to_use": "Use in short shadow-work or truth-clearing sessions."},
            {"slug": "labradorite", "why": "Supports intuitive depth while keeping transitions protected.", "how_to_use": "Carry during emotionally or spiritually intense periods."},
            {"slug": "malachite", "why": "Encourages transformation when the heart is ready for real change.", "how_to_use": "Use in release rituals or transition work."},
        ],
        "shadow_crystals": [
            {"slug": "rose-quartz", "challenge": "emotional armor", "why": "Rose Quartz helps softness return without erasing strength."},
            {"slug": "amethyst", "challenge": "obsessive intensity", "why": "Amethyst cools the inner fire so insight does not become fixation."},
        ],
        "monthly_ritual": [
            "Choose one protection crystal and one heart crystal at the start of the month.",
            "Name what you are ready to release and what deserves deeper loyalty.",
            "At month end, cleanse the stones and write down what truth became visible.",
        ],
    },
    "sagittarius": {
        "display": "Sagittarius",
        "element": "Fire",
        "ruling_planet": "Jupiter",
        "traits": "visionary, adventurous, philosophical, candid",
        "intro": "Sagittarius energy seeks truth, movement, meaning, and big horizons. The best crystals for Sagittarius support expansion while keeping honesty grounded and enthusiasm focused enough to become real.",
        "signature_crystals": [
            {"slug": "yellow-sapphire", "why": "Aligns with Jupiter's wisdom, grace, and growth-oriented abundance.", "how_to_use": "Use in study, teaching, or prosperity rituals."},
            {"slug": "lapis-lazuli", "why": "Supports truth-seeking, philosophy, and higher perspective.", "how_to_use": "Keep nearby during journaling, study, or spiritual inquiry."},
            {"slug": "tigers-eye", "why": "Helps big visions become strategic and grounded.", "how_to_use": "Use during planning or travel-related work."},
            {"slug": "citrine", "why": "Adds optimism and momentum to expansion that needs action.", "how_to_use": "Place in an abundance or creative workspace."},
        ],
        "shadow_crystals": [
            {"slug": "fluorite", "challenge": "scattered big vision", "why": "Fluorite sharpens focus so the mission stays coherent."},
            {"slug": "amazonite", "challenge": "blunt honesty", "why": "Amazonite helps truth land with more grace and balance."},
        ],
        "monthly_ritual": [
            "At the start of the month, define one belief, study path, or expansion goal you want to strengthen.",
            "Work with one Jupiter stone and one focus stone while writing your next real steps.",
            "Close the month by noting what broadened you and what was only escapism.",
        ],
    },
    "capricorn": {
        "display": "Capricorn",
        "element": "Earth",
        "ruling_planet": "Saturn",
        "traits": "disciplined, strategic, reserved, enduring",
        "intro": "Capricorn energy is purposeful, patient, and built for long-range effort. The best crystals for Capricorn reinforce structure and resilience while softening heaviness, pessimism, or over-identification with duty.",
        "signature_crystals": [
            {"slug": "blue-sapphire", "why": "Supports Saturn's discipline, truth, and karmic steadiness when appropriate.", "how_to_use": "Use carefully in structured, deliberate rituals."},
            {"slug": "black-tourmaline", "why": "Grounds pressure into usable boundaries and steadiness.", "how_to_use": "Keep near a desk, entryway, or during heavy work periods."},
            {"slug": "hematite", "why": "Adds grounded endurance and a strong bodily sense of containment.", "how_to_use": "Carry during demanding or over-structured days."},
            {"slug": "garnet", "why": "Brings warmth, devotion, and staying power to Capricorn effort.", "how_to_use": "Wear when long-term work needs heart as well as discipline."},
        ],
        "shadow_crystals": [
            {"slug": "rose-quartz", "challenge": "emotional hardening", "why": "Rose Quartz reintroduces softness where duty has become armor."},
            {"slug": "citrine", "challenge": "pessimism", "why": "Citrine brightens the field so ambition feels alive rather than burdened."},
        ],
        "monthly_ritual": [
            "Choose one Saturn stone and one warmth-giving stone at the start of the month.",
            "Set a realistic structure for the month and place the crystals where that work happens.",
            "At month end, review not just output, but how sustainable the effort felt.",
        ],
    },
    "aquarius": {
        "display": "Aquarius",
        "element": "Air",
        "ruling_planet": "Saturn / Rahu",
        "traits": "inventive, detached, visionary, independent",
        "intro": "Aquarius energy blends systems-thinking with future-facing imagination. The best crystals for Aquarius support originality and intuitive intelligence while preventing emotional disconnection or mental overdistance.",
        "signature_crystals": [
            {"slug": "amethyst", "why": "Keeps Aquarius insight spiritually clear and less mentally overdriven.", "how_to_use": "Use in meditation, sleep, or calm-intuition rituals."},
            {"slug": "labradorite", "why": "Supports innovation, threshold work, and visionary intuition.", "how_to_use": "Carry during change or creative ideation."},
            {"slug": "fluorite", "why": "Brings order to complex ideas and future-facing strategy.", "how_to_use": "Keep near planning boards, books, or screens."},
            {"slug": "shungite", "why": "Adds grounding and modern protection for tech-heavy, overstimulated environments.", "how_to_use": "Place near devices or at a desk."},
        ],
        "shadow_crystals": [
            {"slug": "moonstone", "challenge": "emotional detachment", "why": "Moonstone helps Aquarius stay in relationship with feeling."},
            {"slug": "rose-quartz", "challenge": "cool distance", "why": "Rose Quartz restores warmth and interpersonal softness."},
        ],
        "monthly_ritual": [
            "Start the month by naming one future-facing idea you want to make more embodied.",
            "Pair a visionary crystal with a grounding stone in the place where that idea becomes work.",
            "Mid-month, ask whether your clarity is connected or detached, then adjust accordingly.",
        ],
    },
    "pisces": {
        "display": "Pisces",
        "element": "Water",
        "ruling_planet": "Jupiter / Ketu",
        "traits": "sensitive, mystical, imaginative, compassionate",
        "intro": "Pisces energy is porous, intuitive, imaginative, and spiritually receptive. The best crystals for Pisces support dreaminess and compassion while preventing confusion, depletion, or emotional boundary loss.",
        "signature_crystals": [
            {"slug": "yellow-sapphire", "why": "Brings Jupiter wisdom and ethical expansion to Pisces sensitivity.", "how_to_use": "Use in prayer, study, or gratitude practice."},
            {"slug": "amethyst", "why": "Supports peace, spiritual attunement, and protected intuition.", "how_to_use": "Keep by the bed or meditation seat."},
            {"slug": "moonstone", "why": "Encourages gentle intuitive flow and emotional steadiness.", "how_to_use": "Use in moon rituals, rest, or dreamwork."},
            {"slug": "celestite", "why": "Offers a serene, devotional tone for sleep and spiritual softness.", "how_to_use": "Place in a quiet room or beside the bed."},
        ],
        "shadow_crystals": [
            {"slug": "black-tourmaline", "challenge": "energetic porousness", "why": "Black Tourmaline gives Pisces much-needed containment and grounding."},
            {"slug": "fluorite", "challenge": "confusion", "why": "Fluorite helps insight become clearer and more structured."},
        ],
        "monthly_ritual": [
            "At the start of the month, choose one dream-support stone and one grounding stone.",
            "Use them during a quiet ritual focused on compassion, boundaries, and spiritual clarity.",
            "End the month by writing what intuition proved useful and what was only emotional fog.",
        ],
    },
}

PROBLEM_CRYSTAL_DATA = {
    "insomnia": {
        "display": "Broken Sleep / Insomnia",
        "intro": "Insomnia often has an energetic signature of overstimulation, emotional residue, or a room that never fully settles. The most helpful crystals here are usually cooling, clearing, and sleep-supportive rather than strongly activating.",
        "top_crystals": [
            {"slug": "selenite", "why": "Selenite clears room energy and encourages a cleaner transition into rest.", "usage": "Place beside the bed or sweep it gently around the sleep space."},
            {"slug": "amethyst", "why": "Amethyst calms racing thoughts and supports a more meditative bedtime tone.", "usage": "Keep on the bedside table or hold during slow breathing."},
            {"slug": "moonstone", "why": "Moonstone softens emotional restlessness and supports gentler nighttime cycles.", "usage": "Place under the pillow or near the heart during evening reflection."},
        ],
        "supporting_crystals": [
            {"slug": "lepidolite", "why": "Supports nervous-system decompression before sleep."},
            {"slug": "celestite", "why": "Creates a quiet, devotional atmosphere around rest."},
            {"slug": "pearl", "why": "Adds lunar cooling when emotions are keeping the mind awake."},
        ],
        "crystal_grid": {
            "name": "Sleep Field Grid",
            "stones": ["selenite", "amethyst", "moonstone", "lepidolite"],
            "how_to_use": "Place one stone on each bedside corner and one calming stone close to the pillow, then remove activating stones from the room.",
        },
        "affirmation": "I release the day and allow my body to remember rest.",
    },
    "relationship-conflict": {
        "display": "Relationship Conflict",
        "intro": "Relationship conflict often carries mixed signals between the heart, throat, and root. Helpful crystals here soothe reactivity, support truth, and make it easier to stay soft without abandoning boundaries.",
        "top_crystals": [
            {"slug": "rose-quartz", "why": "Rose Quartz softens defensiveness and restores warmth.", "usage": "Keep in the bedroom or hold before difficult conversations."},
            {"slug": "rhodonite", "why": "Rhodonite supports repair, accountability, and emotional regulation.", "usage": "Carry during conflict-repair talks or journaling sessions."},
            {"slug": "amazonite", "why": "Amazonite helps truth come through more calmly and clearly.", "usage": "Wear near the throat or keep by your phone or notebook."},
        ],
        "supporting_crystals": [
            {"slug": "moonstone", "why": "Softens emotional cycles and helps reactions cool."},
            {"slug": "aquamarine", "why": "Encourages calm speech and gentler honesty."},
            {"slug": "emerald", "why": "Supports thoughtful communication and relational strategy."},
        ],
        "crystal_grid": {
            "name": "Repair Grid",
            "stones": ["rose-quartz", "rhodonite", "amazonite", "moonstone"],
            "how_to_use": "Place the heart stones in the center and the throat stone above them, then sit nearby and set one intention for clarity and goodwill.",
        },
        "affirmation": "I choose truth, tenderness, and repair over reactivity.",
    },
    "career-stagnation": {
        "display": "Career Stagnation",
        "intro": "Career stagnation often feels like blocked momentum, low confidence, or a mismatch between ambition and structure. The most useful crystals here restore strategy, willpower, and grounded movement.",
        "top_crystals": [
            {"slug": "pyrite", "why": "Pyrite supports confident ambition and a practical prosperity mindset.", "usage": "Keep on your desk or near work plans."},
            {"slug": "tigers-eye", "why": "Tiger's Eye grounds decisions and helps hesitant action become decisive.", "usage": "Carry during meetings, interviews, or strategy sessions."},
            {"slug": "yellow-sapphire", "why": "Yellow Sapphire supports growth, guidance, and long-range opportunity.", "usage": "Use during Thursday planning or mentoring rituals."},
        ],
        "supporting_crystals": [
            {"slug": "citrine", "why": "Adds optimism and movement to stalled effort."},
            {"slug": "sunstone", "why": "Restores visibility and professional confidence."},
            {"slug": "emerald", "why": "Improves thought clarity and strategic communication."},
        ],
        "crystal_grid": {
            "name": "Momentum Grid",
            "stones": ["pyrite", "tigers-eye", "yellow-sapphire", "citrine"],
            "how_to_use": "Place the primary stone near your work device and the others around your weekly priorities so action and intention stay linked.",
        },
        "affirmation": "My next step is clear, grounded, and already in motion.",
    },
    "financial-loss": {
        "display": "Financial Loss",
        "intro": "Financial loss can create both fear and energetic contraction. Supportive crystals here help rebuild steadiness, confidence, and a wiser relationship with prosperity rather than chasing quick fixes.",
        "top_crystals": [
            {"slug": "citrine", "why": "Citrine supports optimism and practical abundance work after setbacks.", "usage": "Keep near your budget, accounts, or planning notebook."},
            {"slug": "pyrite", "why": "Pyrite reinforces strategy, confidence, and protective prosperity energy.", "usage": "Place on your desk or in a money corner."},
            {"slug": "jade", "why": "Jade steadies the field and supports calmer long-term rebuilding.", "usage": "Keep in a wallet space or home altar."},
        ],
        "supporting_crystals": [
            {"slug": "aventurine", "why": "Encourages new openings and a lighter growth mindset."},
            {"slug": "tigers-eye", "why": "Helps decisions stay grounded under pressure."},
            {"slug": "clear-quartz", "why": "Keeps intentions clean and practical."},
        ],
        "crystal_grid": {
            "name": "Recovery Grid",
            "stones": ["citrine", "pyrite", "jade", "tigers-eye"],
            "how_to_use": "Set the grid near the place where financial decisions happen and pair it with one practical recovery action each week.",
        },
        "affirmation": "I rebuild with clarity, patience, and wise stewardship.",
    },
    "exam-stress": {
        "display": "Exam Stress / Study Focus",
        "intro": "Exam stress often combines mental overload, self-pressure, and nervous system fatigue. The best crystals here sharpen focus while helping the body feel less flooded.",
        "top_crystals": [
            {"slug": "fluorite", "why": "Fluorite supports concentration and mental order under pressure.", "usage": "Keep beside books, notes, or a laptop."},
            {"slug": "sodalite", "why": "Sodalite helps information feel more organized and easier to express.", "usage": "Hold before revision or oral exams."},
            {"slug": "apatite", "why": "Apatite restores mental engagement and idea flow without becoming chaotic.", "usage": "Use during planning and active study sessions."},
        ],
        "supporting_crystals": [
            {"slug": "clear-quartz", "why": "Amplifies a clean study intention."},
            {"slug": "amethyst", "why": "Helps lower panic and pre-exam overthinking."},
            {"slug": "emerald", "why": "Supports precision and mental agility."},
        ],
        "crystal_grid": {
            "name": "Study Grid",
            "stones": ["fluorite", "sodalite", "apatite", "clear-quartz"],
            "how_to_use": "Place one focus stone at the top of your notes and one grounding stone to the side so studying feels organized rather than frantic.",
        },
        "affirmation": "My mind is focused, calm, and ready to remember what matters.",
    },
    "grief": {
        "display": "Grief / Bereavement",
        "intro": "Grief carries both heaviness and tenderness. The most supportive crystals here create room for feeling, soften self-protection, and help the heart process loss without forcing closure too fast.",
        "top_crystals": [
            {"slug": "rhodonite", "why": "Rhodonite helps emotional first aid and steady repair after shock or loss.", "usage": "Carry close to the heart or hold during tears and prayer."},
            {"slug": "rose-quartz", "why": "Rose Quartz supports tenderness, self-compassion, and softer breathing.", "usage": "Keep at the bedside or on a comfort altar."},
            {"slug": "kunzite", "why": "Kunzite supports grief work that needs gentleness and emotional safety.", "usage": "Wear near the heart or use during evening reflection."},
        ],
        "supporting_crystals": [
            {"slug": "rhodochrosite", "why": "Supports worthiness and inner healing when loss shakes identity."},
            {"slug": "amethyst", "why": "Adds spiritual calm and restfulness during heavy nights."},
            {"slug": "angelite", "why": "Brings a quiet devotional tone to grief rituals."},
        ],
        "crystal_grid": {
            "name": "Heart Support Grid",
            "stones": ["rhodonite", "rose-quartz", "kunzite", "amethyst"],
            "how_to_use": "Build a small altar with one candle, then place the heart stones around it and sit with one memory or prayer instead of trying to solve the grief.",
        },
        "affirmation": "I honor my grief and let healing arrive in its own time.",
    },
    "anxiety-attacks": {
        "display": "Anxiety Attacks",
        "intro": "Anxiety attacks often create sudden energetic fragmentation, racing thought, and a loss of bodily steadiness. The best crystal support here emphasizes grounding, calming, and reducing excess stimulation.",
        "top_crystals": [
            {"slug": "lepidolite", "why": "Lepidolite supports decompression and a slower internal pace.", "usage": "Keep in a pocket or hold during grounding breaths."},
            {"slug": "hematite", "why": "Hematite brings attention back into the body and out of spiraling thought.", "usage": "Carry on the receiving side or keep at a desk."},
            {"slug": "black-tourmaline", "why": "Black Tourmaline helps reinforce energetic boundaries and stability.", "usage": "Place near the front door, bed, or workspace."},
        ],
        "supporting_crystals": [
            {"slug": "amethyst", "why": "Helps the mind soften after the peak of anxiety."},
            {"slug": "selenite", "why": "Clears room heaviness and resets the field."},
            {"slug": "moonstone", "why": "Soothes emotional fluctuation underneath stress."},
        ],
        "crystal_grid": {
            "name": "Grounding Grid",
            "stones": ["hematite", "black-tourmaline", "lepidolite", "amethyst"],
            "how_to_use": "Keep the denser stones at the base of your space and the softer calming stone close to the bed or chair where you regulate.",
        },
        "affirmation": "I return to my body, my breath, and the safety of this moment.",
    },
    "low-confidence": {
        "display": "Low Self-Confidence",
        "intro": "Low confidence often shows up as collapsed solar energy, unclear boundaries, or a disconnection from personal agency. Helpful crystals here restore warmth, courage, and a steadier sense of worth.",
        "top_crystals": [
            {"slug": "tigers-eye", "why": "Tiger's Eye strengthens grounded confidence and clearer decision-making.", "usage": "Carry before interviews, meetings, or difficult decisions."},
            {"slug": "carnelian", "why": "Carnelian restores creative courage and helps action feel possible again.", "usage": "Use before social, artistic, or visibility moments."},
            {"slug": "sunstone", "why": "Sunstone brings brightness, joy, and a more radiant self-expression.", "usage": "Keep in a workspace or wear when you need visibility."},
        ],
        "supporting_crystals": [
            {"slug": "ruby", "why": "Supports deeper solar dignity when the issue is energetic collapse."},
            {"slug": "garnet", "why": "Adds stamina and devotion to self-belief."},
            {"slug": "citrine", "why": "Helps optimism return in practical ways."},
        ],
        "crystal_grid": {
            "name": "Solar Confidence Grid",
            "stones": ["tigers-eye", "carnelian", "sunstone", "citrine"],
            "how_to_use": "Place the grid where you prepare for work or social visibility and speak one confidence-building intention out loud.",
        },
        "affirmation": "I trust my voice, my presence, and my right to take up space.",
    },
    "toxic-workplace": {
        "display": "Toxic Work Environment",
        "intro": "A toxic workplace often creates chronic energetic leakage, emotional vigilance, and dense environmental residue. The strongest crystal support here usually combines shielding, truth, and nervous-system grounding.",
        "top_crystals": [
            {"slug": "black-tourmaline", "why": "Black Tourmaline creates strong boundaries in draining spaces.", "usage": "Keep near your desk or carry on high-contact days."},
            {"slug": "shungite", "why": "Shungite helps clear modern environmental overload and dense desk energy.", "usage": "Place near devices or a workspace."},
            {"slug": "amazonite", "why": "Amazonite supports calm self-expression and cleaner boundary-setting.", "usage": "Use before meetings or difficult exchanges."},
        ],
        "supporting_crystals": [
            {"slug": "hematite", "why": "Keeps your energy rooted in the body instead of the drama around you."},
            {"slug": "obsidian", "why": "Supports truth and discernment when manipulation is present."},
            {"slug": "pyrite", "why": "Protects confidence and professional steadiness."},
        ],
        "crystal_grid": {
            "name": "Desk Shield Grid",
            "stones": ["black-tourmaline", "shungite", "hematite", "amazonite"],
            "how_to_use": "Keep the heavier stones at the edge of the desk and the communication stone close to where you work and write.",
        },
        "affirmation": "I stay protected, clear, and rooted in my own standards.",
    },
    "addiction": {
        "display": "Addiction Recovery",
        "intro": "Addiction recovery often involves cooling compulsive loops, strengthening clarity, and creating new forms of grounding. The most helpful crystals here support steadiness and interruption of triggers rather than intense stimulation.",
        "top_crystals": [
            {"slug": "amethyst", "why": "Amethyst has long been associated with cooling excess and interrupting compulsive cycles.", "usage": "Keep near the bed, dining area, or a known trigger zone."},
            {"slug": "lepidolite", "why": "Lepidolite supports decompression when urges are driven by overwhelm.", "usage": "Carry during vulnerable emotional periods."},
            {"slug": "hematite", "why": "Hematite helps return attention to the body and present-moment structure.", "usage": "Use during grounding routines, walks, or breathwork."},
        ],
        "supporting_crystals": [
            {"slug": "obsidian", "why": "Grounds excess energy and helps hidden trigger patterns become more visible."},
            {"slug": "black-tourmaline", "why": "Protects boundaries around environments or people tied to relapse patterns."},
            {"slug": "selenite", "why": "Keeps the living space feeling cleaner and less emotionally heavy."},
        ],
        "crystal_grid": {
            "name": "Detox Support Grid",
            "stones": ["amethyst", "lepidolite", "hematite", "black-tourmaline"],
            "how_to_use": "Place the main stone in the room where urges peak and keep one grounding stone on the body throughout the day.",
        },
        "affirmation": "I choose clarity, grounding, and one steady step toward freedom.",
    },
    "chronic-fatigue": {
        "display": "Chronic Fatigue",
        "intro": "Chronic fatigue often has an energetic pattern of depletion, low fire, and difficulty holding steady life-force output. Supportive crystals here restore warmth and stamina gently rather than pushing the system too hard.",
        "top_crystals": [
            {"slug": "bloodstone", "why": "Bloodstone supports resilience and grounded life-force rebuilding.", "usage": "Carry during recovery-focused days or gentle movement."},
            {"slug": "red-coral", "why": "Red Coral brings targeted Mars strength when depleted will and vitality need support.", "usage": "Use in short energizing rituals rather than all-day overload."},
            {"slug": "calcite", "why": "Calcite refreshes sluggish energy and supports lighter motivation.", "usage": "Keep in a bright workspace or morning ritual area."},
        ],
        "supporting_crystals": [
            {"slug": "carnelian", "why": "Restores motivation and warm movement."},
            {"slug": "garnet", "why": "Adds grounded stamina and committed rebuilding."},
            {"slug": "sunstone", "why": "Brings gentle brightness when heaviness dominates."},
        ],
        "crystal_grid": {
            "name": "Vitality Grid",
            "stones": ["bloodstone", "red-coral", "calcite", "garnet"],
            "how_to_use": "Place the stones where you begin the day and pair the ritual with hydration, rest, and one realistic energy-supporting action.",
        },
        "affirmation": "My energy rebuilds with patience, warmth, and wise pacing.",
    },
    "digestive-issues": {
        "display": "Digestive Issues",
        "intro": "Digestive imbalance often reflects disturbed solar plexus rhythm, stress, or difficulty processing life as well as food. Supportive crystals here usually calm anxiety while restoring grounded fire and steadier embodiment.",
        "top_crystals": [
            {"slug": "citrine", "why": "Citrine supports solar plexus brightness and a healthier sense of energetic digestion.", "usage": "Place near the upper abdomen during rest or keep nearby at meals."},
            {"slug": "yellow-sapphire", "why": "Yellow Sapphire supports Jupiter's regulating wisdom around nourishment and balance.", "usage": "Use in Thursday healing or gratitude rituals."},
            {"slug": "carnelian", "why": "Carnelian helps restore embodied warmth and movement when stress has created stagnation.", "usage": "Use in short grounding rituals near the lower abdomen."},
        ],
        "supporting_crystals": [
            {"slug": "calcite", "why": "Refreshes sluggish energy around the solar field."},
            {"slug": "moonstone", "why": "Helps emotional triggers around the gut soften."},
            {"slug": "hematite", "why": "Grounds stress back into the body."},
        ],
        "crystal_grid": {
            "name": "Solar Balance Grid",
            "stones": ["citrine", "yellow-sapphire", "carnelian", "moonstone"],
            "how_to_use": "Place the brighter stones above the navel area during rest and the calming stone lower to help the whole body settle.",
        },
        "affirmation": "I digest life with steadiness, warmth, and trust.",
    },
    "heart-chakra-blockage": {
        "display": "Heart Chakra Blockage",
        "intro": "Heart chakra blockage can feel like numbness, guardedness, grief, or difficulty receiving love cleanly. The most supportive crystals here soften the chest, reconnect emotion to safety, and encourage gentle openness.",
        "top_crystals": [
            {"slug": "rose-quartz", "why": "Rose Quartz is the classic heart-softening stone for tenderness and self-worth.", "usage": "Place over the heart during rest or keep by the bed."},
            {"slug": "rhodonite", "why": "Rhodonite helps emotional repair, forgiveness, and safe processing.", "usage": "Carry close during healing work or hard conversations."},
            {"slug": "kunzite", "why": "Kunzite adds a gentle, high heart frequency when the chest feels guarded.", "usage": "Wear near the heart or use in evening rituals."},
        ],
        "supporting_crystals": [
            {"slug": "jade", "why": "Supports peaceful long-term heart balance."},
            {"slug": "rhodochrosite", "why": "Encourages self-worth and compassionate inner repair."},
            {"slug": "prehnite", "why": "Brings calm, heart-led spiritual softness."},
        ],
        "crystal_grid": {
            "name": "Heart Opening Grid",
            "stones": ["rose-quartz", "rhodonite", "kunzite", "jade"],
            "how_to_use": "Create a diamond shape with the stones around the chest area while resting and breathe gently into the center of the heart.",
        },
        "affirmation": "My heart is safe to soften, receive, and love again.",
    },
    "third-eye-activation": {
        "display": "Third Eye Activation",
        "intro": "Third-eye work is about perception, symbolism, intuition, and inner listening. The healthiest crystal support here sharpens insight while keeping the nervous system grounded enough to process what arrives.",
        "top_crystals": [
            {"slug": "lapis-lazuli", "why": "Lapis supports wisdom, intuition, and truth-centered inner vision.", "usage": "Use during meditation, divination, or journaling."},
            {"slug": "amethyst", "why": "Amethyst opens intuitive space while maintaining calm and protection.", "usage": "Place near the brow during meditation or keep at the bedside."},
            {"slug": "fluorite", "why": "Fluorite helps intuitive impressions stay ordered and discernible.", "usage": "Use before study, dreamwork, or symbolic reflection."},
        ],
        "supporting_crystals": [
            {"slug": "moonstone", "why": "Adds softer intuitive flow and dream sensitivity."},
            {"slug": "labradorite", "why": "Supports threshold work and protected insight."},
            {"slug": "selenite", "why": "Keeps the ritual space clean and clear."},
        ],
        "crystal_grid": {
            "name": "Ajna Grid",
            "stones": ["lapis-lazuli", "amethyst", "fluorite", "moonstone"],
            "how_to_use": "Keep the central intuitive stone at the brow line during rest and the clearer stones slightly above and beside it.",
        },
        "affirmation": "I receive insight clearly, calmly, and with discernment.",
    },
    "root-chakra-imbalance": {
        "display": "Root Chakra Imbalance",
        "intro": "Root imbalance often shows up as instability, fear, disconnection from the body, or difficulty feeling safe in ordinary life. The best support stones here are grounding, dense, and physically anchoring.",
        "top_crystals": [
            {"slug": "black-tourmaline", "why": "Black Tourmaline is a reliable root stabilizer for boundaries and energetic grounding.", "usage": "Place near the feet, front door, or carry in a pocket."},
            {"slug": "hematite", "why": "Hematite brings attention back into the body and supports physical steadiness.", "usage": "Carry during stressful days or use in grounding meditation."},
            {"slug": "red-coral", "why": "Red Coral helps rebuild courage and rooted life-force when fear is draining action.", "usage": "Use in brief energizing rituals when safe activation is needed."},
        ],
        "supporting_crystals": [
            {"slug": "onyx", "why": "Adds composure and self-control."},
            {"slug": "bloodstone", "why": "Builds resilient stamina from the ground up."},
            {"slug": "shungite", "why": "Helps clear environmental overload that destabilizes the root."},
        ],
        "crystal_grid": {
            "name": "Rooting Grid",
            "stones": ["black-tourmaline", "hematite", "red-coral", "onyx"],
            "how_to_use": "Place the stones at the corners of the room or near the feet while sitting so the body receives a clear grounding signal.",
        },
        "affirmation": "I am safe, grounded, and fully here in my own body.",
    },
    "emf-sensitivity": {
        "display": "EMF / Tech Sensitivity",
        "intro": "Tech sensitivity often feels like overstimulation, scattered attention, headaches, or a subtle inability to rest around devices. Helpful crystals here lean toward shielding, grounding, and clearing modern environmental residue.",
        "top_crystals": [
            {"slug": "shungite", "why": "Shungite is widely used for digital-age grounding and environmental shielding.", "usage": "Place near routers, laptops, or phones rather than wearing constantly."},
            {"slug": "black-tourmaline", "why": "Black Tourmaline creates stronger energetic boundaries in device-heavy spaces.", "usage": "Keep at the desk edge or between you and a dense tech area."},
            {"slug": "hematite", "why": "Hematite helps pull awareness back into the body after overstimulation.", "usage": "Carry during long screen-based workdays."},
        ],
        "supporting_crystals": [
            {"slug": "selenite", "why": "Clears the room after long periods of screen exposure."},
            {"slug": "fluorite", "why": "Restores order to a tech-frayed mind."},
            {"slug": "amethyst", "why": "Helps with calming down after digital overload."},
        ],
        "crystal_grid": {
            "name": "Tech Boundary Grid",
            "stones": ["shungite", "black-tourmaline", "hematite", "selenite"],
            "how_to_use": "Place the shielding stones near the devices and the clearing stone slightly behind your main work position to refresh the space.",
        },
        "affirmation": "I stay grounded, clear, and sovereign in digital spaces.",
    },
    "negative-energy": {
        "display": "Negative Energy Clearing",
        "intro": "Negative energy clearing is often really about removing stale emotional residue, psychic heaviness, or environmental density. The most useful crystals here both absorb and clear without leaving the space feeling flat.",
        "top_crystals": [
            {"slug": "black-tourmaline", "why": "Absorbs and grounds heavy or intrusive energy effectively.", "usage": "Place near entrances, room corners, or on your person."},
            {"slug": "selenite", "why": "Selenite clears and reseals the field with a lighter tone.", "usage": "Sweep it through the room or keep it in the main living space."},
            {"slug": "obsidian", "why": "Obsidian helps cut through dense emotional residue and hidden heaviness.", "usage": "Use in short clearing rituals or at thresholds."},
        ],
        "supporting_crystals": [
            {"slug": "shungite", "why": "Supports environmental detox in modern spaces."},
            {"slug": "amethyst", "why": "Restores spiritual calm after clearing work."},
            {"slug": "labradorite", "why": "Protects sensitive people during psychic cleanup work."},
        ],
        "crystal_grid": {
            "name": "Clearing Grid",
            "stones": ["black-tourmaline", "selenite", "obsidian", "amethyst"],
            "how_to_use": "Start with the denser protection stones at room thresholds, then keep the clearing stone elevated in the main space.",
        },
        "affirmation": "I clear what is heavy and welcome what is clean and true.",
    },
    "past-trauma": {
        "display": "Past Trauma Release",
        "intro": "Trauma release needs safety, pacing, and a strong sense of grounding. Supportive crystals here do not force catharsis; they help the body and heart process what is ready to move with more steadiness.",
        "top_crystals": [
            {"slug": "rhodonite", "why": "Rhodonite helps emotional first aid and grounded repair after deep hurt.", "usage": "Carry close to the heart or use in therapy-adjacent reflection."},
            {"slug": "rose-quartz", "why": "Rose Quartz restores tenderness and self-compassion after long self-protection.", "usage": "Place over the heart during rest or journaling."},
            {"slug": "obsidian", "why": "Obsidian helps buried truth surface carefully when shadow work is appropriate.", "usage": "Use only in short, intentional sessions with grounding support."},
        ],
        "supporting_crystals": [
            {"slug": "kunzite", "why": "Supports emotional safety and softer vulnerability."},
            {"slug": "hematite", "why": "Keeps the body grounded during processing."},
            {"slug": "amethyst", "why": "Adds spiritual calm and recovery after difficult release."},
        ],
        "crystal_grid": {
            "name": "Safe Release Grid",
            "stones": ["rhodonite", "rose-quartz", "hematite", "amethyst"],
            "how_to_use": "Keep the grounding stone closest to the body and use the heart stones in a calm, private practice space rather than during emotionally flooded moments.",
        },
        "affirmation": "I release only what I am ready to heal, and I stay safe in the process.",
    },
    "manifestation-block": {
        "display": "Manifestation Block",
        "intro": "Manifestation block often reflects mixed signals between desire, confidence, and follow-through. The best crystal support here aligns intention with practical action so wanting something and moving toward it become one process.",
        "top_crystals": [
            {"slug": "clear-quartz", "why": "Clear Quartz sharpens intention and keeps the signal focused.", "usage": "Program with one exact goal at a time."},
            {"slug": "citrine", "why": "Citrine supports optimism, abundance, and willingness to move.", "usage": "Keep near your planning or money space."},
            {"slug": "tigers-eye", "why": "Tiger's Eye brings grounded courage and reduces indecision.", "usage": "Carry when you need to act on what you say you want."},
        ],
        "supporting_crystals": [
            {"slug": "carnelian", "why": "Adds creative momentum and personal fire."},
            {"slug": "pyrite", "why": "Supports strategic action and energetic confidence."},
            {"slug": "sunstone", "why": "Brings warmth and visibility to your goal field."},
        ],
        "crystal_grid": {
            "name": "Intention Grid",
            "stones": ["clear-quartz", "citrine", "tigers-eye", "pyrite"],
            "how_to_use": "Place the clearest intention stone in the center with one written goal beneath it, then surround it with action-support stones.",
        },
        "affirmation": "My desire, clarity, and action now move in the same direction.",
    },
    "loneliness": {
        "display": "Loneliness / Isolation",
        "intro": "Loneliness often has both a heart component and a nervous-system component. Helpful crystals here support belonging, emotional warmth, and the courage to reach back toward life and connection.",
        "top_crystals": [
            {"slug": "rose-quartz", "why": "Rose Quartz restores softness, self-worth, and emotional warmth.", "usage": "Keep close during evenings or tender periods of isolation."},
            {"slug": "moonstone", "why": "Moonstone supports emotional flow when isolation has turned the inner world heavy.", "usage": "Use in evening reflection or moon rituals."},
            {"slug": "sunstone", "why": "Sunstone helps restore warmth, visibility, and social brightness.", "usage": "Carry when re-entering social spaces or shared work."},
        ],
        "supporting_crystals": [
            {"slug": "rhodonite", "why": "Supports healing around relational wounds that create withdrawal."},
            {"slug": "kunzite", "why": "Encourages tenderness and heart safety."},
            {"slug": "citrine", "why": "Helps emotional heaviness feel lighter and more open."},
        ],
        "crystal_grid": {
            "name": "Belonging Grid",
            "stones": ["rose-quartz", "moonstone", "sunstone", "rhodonite"],
            "how_to_use": "Place the warming stone above the heart stones and sit with one intention around connection, friendship, or re-entry into community.",
        },
        "affirmation": "I am worthy of warmth, belonging, and meaningful connection.",
    },
}


def _crystal_link_card(slug: str, why: str, how_to_use: str | None = None) -> dict:
    crystal = get_crystal_docs()[slug]
    return {
        "slug": slug,
        "display_name": crystal["display_name"],
        "tagline": crystal["tagline"],
        "color": crystal["color"],
        "why": why,
        "how_to_use": how_to_use,
    }


def _build_planet_faq(display: str, primary_doc: dict) -> list[dict]:
    return [
        {
            "q": f"What is the main Vedic gemstone for {display}?",
            "a": f"The primary Vedic gemstone for {display} is {primary_doc['display_name']}, which is traditionally used to strengthen that planetary current when the chart supports it.",
        },
        {
            "q": f"Which finger is used for the {display} gemstone?",
            "a": f"{primary_doc['display_name']} is commonly worn on the {primary_doc.get('wearing', {}).get('finger', 'recommended finger')} in the appropriate metal when prescribed traditionally.",
        },
        {
            "q": f"Can I wear {primary_doc['display_name']} without consulting an astrologer?",
            "a": f"Healing crystals are generally gentler, but strong Vedic gemstones are usually best approached with chart context, especially if you are working directly with planetary amplification.",
        },
        {
            "q": f"What are softer support stones for {display}?",
            "a": f"Softer support stones are the companion healing crystals on this page. They help you work with the planet's themes in a more gradual and lifestyle-friendly way.",
        },
        {
            "q": f"How often should I cleanse {display} crystals?",
            "a": "A weekly rhythm works well for most people, with extra cleansing during stressful, emotionally dense, or highly transitional periods.",
        },
    ]


def _build_sign_faq(display: str) -> list[dict]:
    return [
        {
            "q": f"What crystals are best for {display}?",
            "a": f"The best crystals for {display} usually support the sign's natural strengths while balancing its shadow side. The signature stones on this page give you the clearest starting point.",
        },
        {
            "q": f"Should {display} use only its ruling-planet stone?",
            "a": "Not necessarily. A ruling-planet stone can be powerful, but many people benefit just as much from softer support crystals that match daily emotional or practical needs.",
        },
        {
            "q": f"How many crystals should a {display} person use at once?",
            "a": "Usually one main crystal and one balancing crystal is enough. Simpler combinations are easier to feel and easier to keep consistent.",
        },
        {
            "q": f"Can I use these crystals even if {display} is not my sun sign?",
            "a": "Yes. These pages work well for people exploring their moon sign, rising sign, or simply a quality they want to strengthen right now.",
        },
    ]


def _build_problem_faq(display: str) -> list[dict]:
    return [
        {
            "q": f"What is the best crystal for {display.lower()}?",
            "a": f"There is rarely just one answer, which is why this page gives a top three. Start with the crystal whose usage pattern feels most realistic in your life now.",
        },
        {
            "q": f"How do I use crystals for {display.lower()}?",
            "a": "Choose one main stone, keep it close to the body or the relevant room, and reinforce it with one simple daily intention or habit.",
        },
        {
            "q": f"Can I make a crystal grid for {display.lower()}?",
            "a": "Yes. A small three-to-five-stone grid is often enough, especially when you already know the emotional or environmental theme you want to shift.",
        },
        {
            "q": f"How quickly do crystals help with {display.lower()}?",
            "a": "Most people experience crystals as gradual symbolic support rather than instant change. Consistent use matters more than intensity.",
        },
        {
            "q": f"Do crystals replace practical care for {display.lower()}?",
            "a": "No. They are best used as support alongside real-world care, routines, communication, and when relevant professional guidance.",
        },
    ]


def _build_planet_doc(slug: str, payload: dict) -> dict:
    primary_doc = get_crystal_docs()[payload["primary_slug"]]
    supporting_cards = [
        _crystal_link_card(item["slug"], item["why"])
        for item in payload["supporting_crystals"]
        if item["slug"] in get_crystal_docs()
    ]
    return {
        "slug": slug,
        "display": payload["display"],
        "intro": payload["intro"],
        "primary_crystal": {
            "slug": payload["primary_slug"],
            "display_name": primary_doc["display_name"],
            "tagline": primary_doc["tagline"],
            "wearing": primary_doc.get("wearing", {}),
            "who_should_wear": payload["who_should_wear"],
            "synergy": primary_doc.get("synergy", []),
            "conflict": primary_doc.get("conflict", []),
        },
        "supporting_crystals": supporting_cards,
        "avoid_cards": [
            _crystal_link_card(
                avoid_slug,
                f"{get_crystal_docs()[avoid_slug]['display_name']} can feel discordant with the traditional {primary_doc['display_name']} current and is usually approached more cautiously here.",
            )
            for avoid_slug in payload["crystals_to_avoid"]
            if avoid_slug in get_crystal_docs()
        ],
        "how_to_use": payload["how_to_use"],
        "faq": _build_planet_faq(payload["display"], primary_doc),
        "meta_title": f"Best Crystals for {payload['display']} - Vedic Gemstones & Healing Stones",
        "meta_description": f"Discover the best crystals for {payload['display']} in Vedic astrology, including the main gemstone, softer support stones, usage guidance, and crystal conflicts to watch.",
    }


def _build_sign_doc(slug: str, payload: dict) -> dict:
    return {
        "slug": slug,
        "display": payload["display"],
        "element": payload["element"],
        "ruling_planet": payload["ruling_planet"],
        "traits": payload["traits"],
        "intro": payload["intro"],
        "signature_crystals": [
            _crystal_link_card(item["slug"], item["why"], item["how_to_use"])
            for item in payload["signature_crystals"]
            if item["slug"] in get_crystal_docs()
        ],
        "shadow_crystals": [
            {
                **_crystal_link_card(item["slug"], item["why"]),
                "challenge": item["challenge"],
            }
            for item in payload["shadow_crystals"]
            if item["slug"] in get_crystal_docs()
        ],
        "monthly_ritual": payload["monthly_ritual"],
        "faq": _build_sign_faq(payload["display"]),
        "meta_title": f"Best Crystals for {payload['display']} - Healing Stones for {payload['display']} Energy",
        "meta_description": f"Explore the best crystals for {payload['display']}, including signature stones, shadow-side support crystals, and a monthly ritual for this sign's energy.",
    }


def _build_problem_doc(slug: str, payload: dict) -> dict:
    return {
        "slug": slug,
        "display": payload["display"],
        "intro": payload["intro"],
        "top_crystals": [
            _crystal_link_card(item["slug"], item["why"], item["usage"])
            for item in payload["top_crystals"]
            if item["slug"] in get_crystal_docs()
        ],
        "supporting_crystals": [
            _crystal_link_card(item["slug"], item["why"])
            for item in payload["supporting_crystals"]
            if item["slug"] in get_crystal_docs()
        ],
        "crystal_grid": {
            "name": payload["crystal_grid"]["name"],
            "stones": [
                _crystal_link_card(stone_slug, get_crystal_docs()[stone_slug]["tagline"])
                for stone_slug in payload["crystal_grid"]["stones"]
                if stone_slug in get_crystal_docs()
            ],
            "how_to_use": payload["crystal_grid"]["how_to_use"],
        },
        "affirmation": payload["affirmation"],
        "faq": _build_problem_faq(payload["display"]),
        "meta_title": f"Crystals for {payload['display']} - Best Healing Stones",
        "meta_description": f"Find the best crystals for {payload['display'].lower()}, including top stones, support crystals, a simple grid suggestion, and practical ways to use them.",
    }


@lru_cache(maxsize=1)
def get_planet_crystal_docs() -> dict[str, dict]:
    return {
        slug: _build_planet_doc(slug, payload)
        for slug, payload in PLANET_CRYSTAL_DATA.items()
    }


@lru_cache(maxsize=1)
def get_sign_crystal_docs() -> dict[str, dict]:
    return {
        slug: _build_sign_doc(slug, payload)
        for slug, payload in SIGN_CRYSTAL_DATA.items()
    }


@lru_cache(maxsize=1)
def get_problem_crystal_docs() -> dict[str, dict]:
    return {
        slug: _build_problem_doc(slug, payload)
        for slug, payload in PROBLEM_CRYSTAL_DATA.items()
    }


def get_planet_crystal_sitemap_urls() -> list[str]:
    return [f"{SITE_URL}/crystals/for/planet/{slug}" for slug in PLANET_CRYSTAL_DATA]


def get_sign_crystal_sitemap_urls() -> list[str]:
    return [f"{SITE_URL}/crystals/for/sign/{slug}" for slug in SIGN_CRYSTAL_DATA]


def get_problem_crystal_sitemap_urls() -> list[str]:
    return [f"{SITE_URL}/crystals/for/problem/{slug}" for slug in PROBLEM_CRYSTAL_DATA]


def get_crystal_list_payload() -> dict:
    docs = get_crystal_docs()
    list_items = []
    chakras: set[str] = set()
    elements: set[str] = set()
    planets: set[str] = set()
    for slug in CRYSTAL_SLUGS:
        doc = docs[slug]
        chakras.update(doc["chakras"])
        elements.add(doc["element"])
        planets.add(doc["planet"])
        list_items.append(
            {
                "slug": slug,
                "display_name": doc["display_name"],
                "tagline": doc["tagline"],
                "color": doc["color"],
                "chakras": doc["chakras"],
                "element": doc["element"],
                "planet": doc["planet"],
                "best_intentions": doc["best_intentions"],
            }
        )
    return {
        "crystals": list_items,
        "intentions": [
            {"slug": slug, "display": payload["display"]}
            for slug, payload in INTENTION_DEFINITIONS.items()
        ],
        "planet_pages": [
            {"slug": slug, "display": payload["display"], "primary_slug": payload["primary_slug"]}
            for slug, payload in PLANET_CRYSTAL_DATA.items()
        ],
        "sign_pages": [
            {
                "slug": slug,
                "display": payload["display"],
                "element": payload["element"],
                "ruling_planet": payload["ruling_planet"],
            }
            for slug, payload in SIGN_CRYSTAL_DATA.items()
        ],
        "problem_pages": [
            {"slug": slug, "display": payload["display"]}
            for slug, payload in PROBLEM_CRYSTAL_DATA.items()
        ],
        "filters": {
            "chakras": sorted(chakras),
            "elements": sorted(elements),
            "planets": sorted(planets),
        },
    }


def get_crystal_sitemap_urls() -> list[str]:
    urls = [f"{SITE_URL}/crystals"]
    urls.extend(f"{SITE_URL}/crystals/{slug}" for slug in CRYSTAL_SLUGS)
    urls.extend(f"{SITE_URL}/crystals/for/{slug}" for slug in INTENTION_DEFINITIONS)
    urls.extend(get_planet_crystal_sitemap_urls())
    urls.extend(get_sign_crystal_sitemap_urls())
    urls.extend(get_problem_crystal_sitemap_urls())
    urls.append(f"{SITE_URL}/crystals/calculator")
    return urls
