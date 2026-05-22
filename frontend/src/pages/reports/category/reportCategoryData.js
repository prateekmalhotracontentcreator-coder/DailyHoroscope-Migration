const SITE = 'https://www.everydayhoroscope.in';

export const CATEGORY_STEPS = [
  {
    number: '01',
    title: 'Enter your birth details',
    body: 'Provide your date, time, and place of birth so the underlying Vedic engine has the chart inputs it needs.',
  },
  {
    number: '02',
    title: 'Our Vedic engine calculates your chart',
    body: 'Swiss Ephemeris, KP Jyotish logic, and timing systems compute the chart structure behind each premium reading.',
  },
  {
    number: '03',
    title: 'Receive your personalised report',
    body: 'Each report focuses on a specific life domain and turns your chart into a practical interpretation, not a generic sign reading.',
  },
];

export const REPORT_CATEGORY_DATA = {
  kundali: {
    slug: 'kundali',
    title: 'Kundali Reports - Your Complete Vedic Birth Chart',
    seoTitle: 'Kundali & Birth Chart Reports - Vedic Astrology',
    description: 'Your Kundali is the blueprint of your life: a precise map of planetary positions at the moment of your birth, calculated using KP Jyotish and Swiss Ephemeris.',
    metaDescription: 'Explore Kundali and birth chart reports. Full D1 chart, Brihat Kundali, Kundali Milan, and Karmic Debt analysis powered by KP Jyotish and Swiss Ephemeris.',
    route: '/reports/kundali',
    primaryCta: { label: 'Explore Birth Chart Reports', href: '/birth-chart' },
    discover: [
      {
        title: 'See your foundational chart structure',
        body: 'Understand Lagna, Moon sign, houses, grahas, and the core architecture that shapes every major reading.',
      },
      {
        title: 'Pinpoint timing and karmic patterns',
        body: 'Surface Dasha patterns, karmic loops, and chart dynamics that explain why specific life themes keep repeating.',
      },
      {
        title: 'Choose the right depth for your question',
        body: 'Move from a foundational Lagna chart to Brihat Kundali, compatibility, or focused karmic reports based on your need.',
      },
    ],
    reports: [
      {
        name: 'Birth Chart (Lagna Kundali)',
        route: '/birth-chart',
        description: 'The foundational Vedic chart with D1 structure, planetary placements, core houses, and introductory timing context.',
        reveals: ['Lagna and Moon sign dynamics', 'Planetary positions and house strength', 'Core life themes and chart orientation'],
        badge: 'Most Popular',
      },
      {
        name: 'Brihat Kundali Pro',
        route: '/brihat-kundli',
        description: 'A deeper chart workspace with divisional charts, richer timing layers, and more advanced interpretive detail.',
        reveals: ['Divisional chart layers', 'Expanded planetary context', 'Higher-resolution Vedic analysis'],
        badge: 'Premium',
      },
      {
        name: 'Kundali Milan',
        route: '/kundali-milan',
        description: 'Traditional compatibility analysis using the classic 36-point system, with deeper relationship alignment context.',
        reveals: ['Ashtakoot matching score', 'Marriage harmony factors', 'Compatibility strengths and friction zones'],
        badge: 'Premium',
      },
      {
        name: 'Karmic Debt Analysis',
        route: '/karmic-debt-report',
        description: 'A focused report on inherited patterns, unfinished lessons, and chart signatures that keep returning as pressure points.',
        reveals: ['Recurring karmic themes', 'South Node and Saturn lessons', 'Release and remediation directions'],
        badge: 'Premium',
      },
      {
        name: 'Life Cycles Report',
        route: '/life-cycles-report',
        description: 'A timing-oriented reading that explains the larger chapter you are in and the one that is quietly rising next.',
        reveals: ['Current Dasha chapter', 'Upcoming life transitions', 'Timing windows for change'],
        badge: 'Premium',
      },
    ],
    faq: [
      {
        question: 'What is a Kundali?',
        answer: 'A Kundali is your Vedic birth chart. It maps the planetary positions at your birth and becomes the foundation for timing, compatibility, karma, and life-pattern interpretation.',
      },
      {
        question: 'What is an Ashi?',
        answer: 'People often use this loosely while asking about rashi or chart identity. In practice, the core chart questions are usually about your Lagna, Moon sign, and how the full Kundali is calculated.',
      },
      {
        question: 'How accurate is Vedic birth chart calculation?',
        answer: 'Accuracy depends on precise birth inputs, especially time and place. With reliable data, the planetary positions and chart structure can be calculated very precisely.',
      },
      {
        question: 'What is KP Jyotish?',
        answer: 'KP Jyotish is a predictive framework within Vedic astrology that uses precise cuspal and stellar logic to sharpen timing and interpretation.',
      },
    ],
    related: ['numerology', 'love', 'career'],
  },
  numerology: {
    slug: 'numerology',
    title: 'Numerology Reports - The Hidden Code in Your Name and Birth Date',
    seoTitle: 'Numerology Reports - Vedic Ankjyotish Readings',
    description: 'Vedic numerology, or Ankjyotish, reveals the vibrational patterns in your name and birth date. Your numbers are as unique as your fingerprint.',
    metaDescription: 'Discover your numerology reports: Life Path, Name Correction, Relationship Compatibility, and Annual Forecast. Vedic Ankjyotish for deep personal insight.',
    route: '/reports/numerology',
    primaryCta: { label: 'Explore Numerology Reports', href: '/numerology' },
    discover: [
      {
        title: 'Decode your core numbers',
        body: 'Reveal the number patterns behind your life path, destiny, personality, timing cycles, and personal strengths.',
      },
      {
        title: 'Understand name vibration',
        body: 'Compare your birth vibration with your current name usage to spot alignment, friction, and public energy drift.',
      },
      {
        title: 'Use numbers for timing and compatibility',
        body: 'Explore how numerology supports relationships, career planning, and more conscious decisions around change.',
      },
    ],
    reports: [
      {
        name: 'Life Path Report',
        route: '/numerology',
        description: 'A foundational numerology reading covering your Life Path, Destiny, Soul Urge, and Personality numbers.',
        reveals: ['Core birth-date vibration', 'Natural strengths and patterns', 'Primary growth themes'],
        badge: 'Most Popular',
      },
      {
        name: 'Name Correction Report',
        route: '/numerology',
        description: 'A focused view of how your current public name aligns or clashes with your deeper numerological signature.',
        reveals: ['Name and destiny resonance', 'Energetic alignment gaps', 'Correction and naming guidance'],
        badge: 'Premium',
      },
      {
        name: 'Relationship Compatibility',
        route: '/numerology',
        description: 'A numbers-based compatibility analysis that compares how two people interact across temperament and life rhythm.',
        reveals: ['Harmony and friction patterns', 'Communication compatibility', 'Long-term alignment clues'],
        badge: 'Premium',
      },
      {
        name: 'Career Blueprint',
        route: '/numerology',
        description: 'Numerology translated into work style, vocation themes, and environments that best support your success.',
        reveals: ['Career path fit', 'Work rhythm and motivation', 'Professional strengths'],
        badge: 'Premium',
      },
      {
        name: 'Annual Forecast',
        route: '/numerology',
        description: 'A timing-led numerology reading that highlights the energy of your personal year and how to work with it.',
        reveals: ['Personal year number', 'Decision timing themes', 'Best focus for the year'],
        badge: 'Premium',
      },
      {
        name: 'Name Compatibility',
        route: '/compatibility/name',
        description: 'A quick free tool that compares two names through Chaldean numerology and returns an instant score.',
        reveals: ['Name number resonance', 'Quick compatibility score', 'Shareable public reading'],
        badge: 'Free',
      },
    ],
    faq: [
      {
        question: 'What is numerology?',
        answer: 'Numerology is the symbolic study of number vibrations in your birth date and name. It is used to understand patterns in personality, timing, compatibility, and life direction.',
      },
      {
        question: 'Is Chaldean or Pythagorean numerology more accurate?',
        answer: 'Different systems emphasise different logic. This project uses Chaldean methods for name compatibility and broader numerology logic where it best fits the existing engine.',
      },
      {
        question: 'What is a Life Path number?',
        answer: 'Your Life Path number comes from your birth date and points to the broad life lesson, temperament, and style of growth you are likely to carry through this incarnation.',
      },
      {
        question: 'Can numerology help with name changes?',
        answer: 'Yes. Name-based reports are especially useful when you want to understand whether a current or proposed name supports your wider life vibration.',
      },
    ],
    related: ['kundali', 'love', 'career'],
  },
  love: {
    slug: 'love',
    title: 'Love and Compatibility Reports - Your Relationship Blueprint',
    seoTitle: 'Love & Compatibility Reports - Vedic Astrology',
    description: 'Vedic astrology reveals relationship dynamics with precision, from Kundali matching to timing windows for love, commitment, and karmic connection.',
    metaDescription: 'Love and compatibility reports using Vedic astrology. Kundali Milan, Love Weather, Soulmate Timing, Soul Connection, and more for your relationship blueprint.',
    route: '/reports/love',
    primaryCta: { label: 'Explore Love Reports', href: '/kundali-milan' },
    discover: [
      {
        title: 'Understand compatibility from multiple angles',
        body: 'Blend chart matching, relationship timing, karmic patterns, and numerology-based chemistry instead of relying on one score alone.',
      },
      {
        title: 'See current romantic weather clearly',
        body: 'Some reports focus on lifelong alignment, while others highlight the current season for intimacy, reconnection, or new encounters.',
      },
      {
        title: 'Choose between free tools and premium depth',
        body: 'Start with a quick public calculator, then move into chart-based reports when you want a more specific relationship blueprint.',
      },
    ],
    reports: [
      {
        name: 'Kundali Milan',
        route: '/kundali-milan',
        description: 'Traditional chart-based marriage compatibility using the 36-point framework and deeper Vedic matching logic.',
        reveals: ['Compatibility score', 'Marriage harmony patterns', 'Areas that need conscious support'],
        badge: 'Most Popular',
      },
      {
        name: 'Love Weather Report',
        route: '/love-weather-report',
        description: 'A timing-based reading of the current romantic climate around you and how to move with it.',
        reveals: ['Current relationship atmosphere', 'Best and caution windows', 'Short-term romantic focus'],
        badge: 'Premium',
      },
      {
        name: 'Romance and Creative Report',
        route: '/romance-creative-report',
        description: 'A Venus-led reading around attraction, creative magnetism, pleasure, and emotional expression.',
        reveals: ['Romantic timing', 'Attraction style', 'Creative-emotional openings'],
        badge: 'Premium',
      },
      {
        name: 'Partnership Window Report',
        route: '/partnership-window-report',
        description: 'A relationship timing report designed to surface stronger windows for commitment and meaningful connection.',
        reveals: ['Upcoming relationship windows', 'Commitment timing', 'Marriage-oriented periods'],
        badge: 'Premium',
      },
      {
        name: 'Intimacy and Vitality Report',
        route: '/intimacy-vitality-report',
        description: 'A report focused on chemistry, energy, desire, and how physical and emotional closeness interact.',
        reveals: ['Physical chemistry signals', 'Energy and desire patterns', 'Relationship vitality themes'],
        badge: 'Premium',
      },
      {
        name: 'Soulmate Timing Report',
        route: '/soulmate-timing-report',
        description: 'A timing-based reading that looks for significant relationship openings and partnership milestones.',
        reveals: ['Major love timing windows', 'Soulmate-style opportunities', 'Long-term partnership periods'],
        badge: 'Premium',
      },
      {
        name: 'Soul Connection Report',
        route: '/soul-connection-report',
        description: 'A karmic relationship analysis that focuses on deeper spiritual and evolutionary ties between people.',
        reveals: ['Karmic bond patterns', 'Emotional intensity themes', 'Growth lessons in connection'],
        badge: 'Premium',
      },
      {
        name: 'Love Calculator',
        route: '/love-calculator',
        description: 'A free quick-check tool that compares names or birth dates to generate a shareable compatibility score.',
        reveals: ['Instant compatibility score', 'Name or DOB mode', 'Shareable public result'],
        badge: 'Free',
      },
      {
        name: 'Relationship Numerology',
        route: '/numerology',
        description: 'A numerology-first route into romantic compatibility, useful when you want number-based chemistry insights.',
        reveals: ['Name and number resonance', 'Relationship vibration', 'Alternative compatibility lens'],
        badge: 'Premium',
      },
    ],
    faq: [
      {
        question: 'What is Kundali matching?',
        answer: 'Kundali matching compares two Vedic birth charts to assess compatibility for marriage and long-term partnership using traditional and chart-specific factors.',
      },
      {
        question: 'What is a compatibility score?',
        answer: 'A compatibility score is a summary signal, not the whole story. It helps you orient quickly, but the deeper reports explain where harmony or friction actually comes from.',
      },
      {
        question: 'Can astrology predict when I will find love?',
        answer: 'Astrology is strongest at showing timing windows, relational themes, and periods of openness. It does not replace choice, but it can highlight when the weather becomes more supportive.',
      },
      {
        question: 'Should I use numerology or Kundali Milan first?',
        answer: 'If you want a quick public snapshot, start with a free tool like the Love Calculator. If you want marriage-focused depth, Kundali Milan is the stronger first step.',
      },
    ],
    related: ['kundali', 'numerology', 'career'],
  },
  career: {
    slug: 'career',
    title: 'Career and Life Purpose Reports - Your Professional Blueprint',
    seoTitle: 'Career & Life Purpose Reports - Vedic Astrology',
    description: 'Vedic astrology maps your career potential, timing windows, and professional destiny through planetary positions, Dasha timing, and yoga analysis.',
    metaDescription: 'Career and life purpose reports using Vedic astrology. Career Blueprint, The Strategist, Dharma Purpose, Wealth Blueprint, and more powered by KP Jyotish.',
    route: '/reports/career',
    primaryCta: { label: 'Explore Career Reports', href: '/career-blueprint-report' },
    discover: [
      {
        title: 'Map work style and professional direction',
        body: 'Understand what your chart says about vocation, strengths, leadership style, and the environments where you perform best.',
      },
      {
        title: 'Read timing, momentum, and opportunity',
        body: 'Career is not only about talent. Timing matters, and these reports help surface windows for growth, visibility, and financial expansion.',
      },
      {
        title: 'Connect career with purpose',
        body: 'The strongest professional path is often the one that aligns your earning power with your dharma, motivation, and long-term mission.',
      },
    ],
    reports: [
      {
        name: 'Career Blueprint Report',
        route: '/career-blueprint-report',
        description: 'A focused career report that translates your Vedic chart into work patterns, potential, and strategic direction.',
        reveals: ['Career strengths and fit', 'Public success themes', 'Timing windows for moves'],
        badge: 'Most Popular',
      },
      {
        name: 'The Strategist',
        route: '/the-strategist',
        description: 'A more tactical intelligence system that blends structured guidance, career prioritisation, and decision support.',
        reveals: ['Strategic work direction', 'Mission-style planning', 'Action-oriented guidance'],
        badge: 'Premium',
      },
      {
        name: 'Dharma and Purpose Report',
        route: '/dharma-purpose-report',
        description: 'A chart-based reading on life mission, meaning, and the deeper thread your work is meant to serve.',
        reveals: ['Soul purpose themes', 'Values-aligned direction', 'Mission clarity'],
        badge: 'Premium',
      },
      {
        name: 'Wealth Blueprint Report',
        route: '/wealth-blueprint-report',
        description: 'A financial potential reading that looks at earning style, abundance timing, and chart signatures around wealth.',
        reveals: ['Income potential factors', 'Abundance timing', 'Money-building patterns'],
        badge: 'Premium',
      },
      {
        name: 'Gains and Network Report',
        route: '/gains-network-report',
        description: 'An 11th-house style reading around networks, income streams, alliances, and long-term professional support.',
        reveals: ['Income stream potential', 'Network leverage', 'Aspirational growth signals'],
        badge: 'Premium',
      },
      {
        name: 'Arc Angel',
        route: '/arc-angel',
        description: 'A broad 12-area framework that helps you see career inside the wider ecosystem of your life and timing cycles.',
        reveals: ['Whole-life pattern view', 'Multiple domain timing', 'Career inside life balance'],
        badge: 'Premium',
      },
    ],
    faq: [
      {
        question: 'Which planet rules career in Vedic astrology?',
        answer: 'Career analysis usually considers several factors, especially the 10th house, its lord, Saturn, Sun, and timing systems. There is rarely only one planet that tells the full story.',
      },
      {
        question: 'What is a Dasha?',
        answer: 'A Dasha is a planetary timing cycle used in Vedic astrology. It helps explain why different themes rise to prominence during different chapters of life.',
      },
      {
        question: 'How does KP Jyotish predict career timing?',
        answer: 'KP Jyotish sharpens prediction through cuspal and stellar logic, helping identify when career movement, results, or role changes are more likely to surface.',
      },
      {
        question: 'Can astrology help with career changes?',
        answer: 'Yes. It can show when you are better supported for a shift, what patterns you are leaving, and which strengths are ready to be used more fully.',
      },
    ],
    related: ['kundali', 'numerology', 'love'],
  },
};

export function buildCategorySchema(config) {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'ItemList',
        name: config.title,
        itemListElement: config.reports.map((report, index) => ({
          '@type': 'ListItem',
          position: index + 1,
          name: report.name,
          url: `${SITE}${report.route}`,
        })),
      },
      {
        '@type': 'FAQPage',
        mainEntity: config.faq.map((item) => ({
          '@type': 'Question',
          name: item.question,
          acceptedAnswer: {
            '@type': 'Answer',
            text: item.answer,
          },
        })),
      },
    ],
  };
}
