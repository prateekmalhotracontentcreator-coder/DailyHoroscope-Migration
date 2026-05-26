#!/usr/bin/env python3
"""Round 8 integration -- 50 entries: Durga Puja first 20 + Gurupurab all 30."""

f = '/Users/apple/DailyHoroscope-Migration/backend/seo_m3_festival_summaries.py'
content = open(f, 'r').read()

def replace_entry(content, festival, region, new_block):
    anchor = f'    ("{festival}", "{region}"): ('
    old_start = content.find(anchor)
    if old_start == -1:
        raise ValueError(f"NOT FOUND: ({festival}, {region})")
    old_end = content.find('\n    ),', old_start) + len('\n    ),')
    if old_end < old_start:
        raise ValueError(f"Closing ), not found for: ({festival}, {region})")
    return content[:old_start] + new_block + content[old_end:]

entries = [

    # ── DURGA PUJA -- first 20 regions (andhra-pradesh → punjab) ──────────────

    ("durga-puja", "andhra-pradesh", '''    ("durga-puja", "andhra-pradesh"): (
        "The echoing thunder of dhaak beats introduces the autumn structural shift inside localized Andhra Pradesh residential complexes. "
        "Worshippers gather to engage in competitive dhunuchi naach moves before the heavy incense burners are placed near the stage. "
        "The ritual night finishes with families distributing sweet sandesh variants across visiting neighbor networks."
    ),'''),

    ("durga-puja", "arunachal-pradesh", '''    ("durga-puja", "arunachal-pradesh"): (
        "Brightly lit pandal hopping routes draw large crowds across Arunachal Pradesh valleys, welcoming the magnificent arrival of the goddess. "
        "Worshippers offer intense pushpanjali prayers to invoke the supreme strength and shielding guidance of the protective deity. "
        "The auspicious evening concludes with households gathering to share sweet rasgulla formulas alongside regional festive rice dishes."
    ),'''),

    ("durga-puja", "assam", '''    ("durga-puja", "assam"): (
        "The structural cadence of the visarjan procession alters the autumn landscape in Assam, reflecting a deep goddess celebration. "
        "Neighborhood circles gather for synchronized pushpanjali recitations to celebrate the supreme glory of Durga mata. "
        "The cultural transition is completed as kitchens prepare rich chalar payesh alongside traditional Assamese pitha varieties."
    ),'''),

    ("durga-puja", "bihar", '''    ("durga-puja", "bihar"): (
        "Intricate clay craftsmanship and massive temporary pandal hopping tracks transform neighborhood lines across Bihar during the holy week. "
        "Women organize the emotional sindoor khela items to bless their relatives during the late-night twilight prayer slots. "
        "Extended families celebrate the transition by eating custom sandesh portions alongside classic home-cooked Bihari items."
    ),'''),

    ("durga-puja", "chhattisgarh", '''    ("durga-puja", "chhattisgarh"): (
        "Thick incense smoke and echoing dhunuchi naach competitions fill public squares across Chhattisgarh, initiating the autumn celebration. "
        "Vibrant temporary structures attract large community lines for nightly stotra recitations honoring the forms of the goddess. "
        "Kitchens prepare specialized chalar payesh portions and home-style desserts to distribute as sacred prasad."
    ),'''),

    ("durga-puja", "goa", '''    ("durga-puja", "goa"): (
        "Beautifully styled pandal hopping routes illuminate local coastal squares across Goa, channeling a wave of deep devotion. "
        "Devotees coordinate grand morning pushpanjali rituals to invite spiritual prosperity and defensive shielding into their living spaces. "
        "The sacred time involves sharing delicious rasgulla items alongside coastal coconut desserts with visiting families."
    ),'''),

    ("durga-puja", "gujarat", '''    ("durga-puja", "gujarat"): (
        "The heavy beats of the dhaak resonate beautifully with localized structural templates across Gujarat under bright lights. "
        "Massive open-air grounds host spectacular dhunuchi naach routines where thousands dance late into the night to honor the goddess. "
        "Dancers replenish their energy by sharing large plates of sandesh along with festive local snacks."
    ),'''),

    ("durga-puja", "haryana", '''    ("durga-puja", "haryana"): (
        "The echoing thunder of dhaak beats introduces the autumn structural shift inside localized Haryana residential complexes. "
        "Worshippers gather to engage in competitive dhunuchi naach moves before the heavy incense burners are placed near the stage. "
        "The ritual night finishes with families distributing sweet sandesh variants across visiting neighbor networks."
    ),'''),

    ("durga-puja", "himachal-pradesh", '''    ("durga-puja", "himachal-pradesh"): (
        "Resounding dhaak beats echo through hillside temples in Himachal Pradesh, anchoring the mountain air in the autumn festival. "
        "Local clans travel across valleys to participate in grand temple-style pushpanjali reading gatherings. "
        "The spiritual afternoon is comforted by serving warm rasgulla formulas alongside rich mountain-style meals."
    ),'''),

    ("durga-puja", "jharkhand", '''    ("durga-puja", "jharkhand"): (
        "Spectacular clay art and grand temporary pandal hopping routes decorate residential colonies in Jharkhand, marking the seasonal alignment. "
        "Devotees coordinate peaceful community dhunuchi naach sessions to offer collective gratitude for family health and well-being. "
        "The holiday period is supported by sharing unique sandesh mixtures with neighboring families."
    ),'''),

    ("durga-puja", "karnataka", '''    ("durga-puja", "karnataka"): (
        "The grand welcoming of the goddess and beautifully decorated pandal hopping stages transform local districts across Karnataka. "
        "Youth groups coordinate localized dhunuchi naach routines inside temple courtyards to celebrate the glory of Durga mata. "
        "The evening feast is defined by preparing delicious chalar payesh variations alongside classic southern treats."
    ),'''),

    ("durga-puja", "kerala", '''    ("durga-puja", "kerala"): (
        "The rare dynamic invocation and specialized pushpanjali rituals inside ancient coastal shrines transform Kerala during October. "
        "Women complete their elaborate sindoor khela decorations before dressing children in pristine traditional finery. "
        "The concluding hour is celebrated by serving sweet rasgulla variants alongside elaborate banana leaf spreads."
    ),'''),

    ("durga-puja", "madhya-pradesh", '''    ("durga-puja", "madhya-pradesh"): (
        "High-energy public spaces host spectacular dhunuchi naach competitions across Madhya Pradesh, showcasing the grand scale of the festival. "
        "Devotional pandal hopping setups draw thousands of residents into illuminated public streets after sunset for collective prayers. "
        "The local evening hospitality features sharing rows of chalar payesh along with regional street savouries."
    ),'''),

    ("durga-puja", "maharashtra", '''    ("durga-puja", "maharashtra"): (
        "The grand welcoming of the clay idol and early-morning pushpanjali anchor home altars across Maharashtra during the autumn days. "
        "Bustling society spaces turn into lively centers for nightly dhunuchi naach sessions and collective aarti routines. "
        "The family gathering centers on preparing fresh sandesh portions along with traditional Maharashtrian sweets."
    ),'''),

    ("durga-puja", "manipur", '''    ("durga-puja", "manipur"): (
        "Resounding dhaak beats and classical devotional movements fill local Manipuri mandaps during the grand autumn descent. "
        "Worshippers coordinate an elaborate kumari puja ceremony to honor young girls as living forms of divine energy. "
        "The sacred week concludes with families distributing sweet sandesh portions alongside specialized local sweets."
    ),'''),

    ("durga-puja", "meghalaya", '''    ("durga-puja", "meghalaya"): (
        "Devout families prepare for a grand evening of pandal hopping as temporary structures light up the hills of Meghalaya. "
        "Women organize the emotional sindoor khela items to bless their relatives during the final seasonal adjustments. "
        "The seasonal gathering is highlighted by presenting large trays of chalar payesh to visiting friends."
    ),'''),

    ("durga-puja", "mizoram", '''    ("durga-puja", "mizoram"): (
        "A grand morning pushpanjali ritual commences behind beautifully decorated clay idols inside private diaspora halls in Mizoram. "
        "Devotees gather to watch an intricate kumari puja ceremony designed to highlight traditional maternal protection. "
        "The spring occasion is highlighted by distributing sweet rasgulla formulas among remote neighborhood blocks."
    ),'''),

    ("durga-puja", "nagaland", '''    ("durga-puja", "nagaland"): (
        "A spectacular indoor visarjan procession is arranged across Nagaland spaces to finalize the multi-day goddess celebration. "
        "Worshippers offer silent pushpanjali prayers to invoke the supreme strength and defensive shielding of the deity. "
        "The sacred time involves sharing delicious narkel naru portions alongside traditional clan feast treats."
    ),'''),

    ("durga-puja", "odisha", '''    ("durga-puja", "odisha"): (
        "The grand morning pushpanjali rituals inside ancient Cuttack shrines transform local districts across Odisha. "
        "Intricate designs line the paths where families gather for the beautiful evening kumari puja blessings. "
        "The holy days are accompanied by distributing traditional rasgulla items alongside classic temple sweets."
    ),'''),

    ("durga-puja", "punjab", '''    ("durga-puja", "punjab"): (
        "The festive rhythm of echoing dhaak beats fills local residential areas across Punjab during the grand goddess celebration. "
        "Neighborhood families coordinate vibrant dhunuchi naach tracks inside community centres to praise the protective deity. "
        "The auspicious eighth day is marked by sharing warm sandesh portions alongside festive local rotis."
    ),'''),

    # ── GURUPURAB -- all 30 regions ────────────────────────────────────────────

    ("gurupurab", "andhra-pradesh", '''    ("gurupurab", "andhra-pradesh"): (
        "A melodious shabad kirtan session resonates throughout early morning congregations across Andhra Pradesh to mark the holy birth anniversary. "
        "Devotees volunteer for intensive langar seva tracks to serve thousands of visitors regardless of background. "
        "The sacred assembly concludes with organizers handing out warm, velvety blocks of sweet kada prasad to the community."
    ),'''),

    ("gurupurab", "arunachal-pradesh", '''    ("gurupurab", "arunachal-pradesh"): (
        "A loud prabhat pheri winds through pristine Arunachal Pradesh valley settlements during the quiet amrit vela hours. "
        "Worshippers join for a grand Gurbani recitation inside local prayer halls to ground their seasonal focus. "
        "The spiritual morning concludes with families coordinating extensive langar seva paired with hot kada prasad."
    ),'''),

    ("gurupurab", "assam", '''    ("gurupurab", "assam"): (
        "The holy resonance of early morning shabad kirtan recitations transforms local community centers across Assam at dawn. "
        "The congregation participates in a grand nagar kirtan procession that carries historical markers through decorated paths. "
        "The winter milestone is celebrated by arranging selfless langar seva combined with sweet kada prasad distributions."
    ),'''),

    ("gurupurab", "bihar", '''    ("gurupurab", "bihar"): (
        "A peaceful sarovar snan simulation initiates the sacred winter dawn at historic Patna gurdwaras across Bihar. "
        "Devotees gather to hear a full-length Gurbani recitation to invite spiritual clarity and protective order into their homes. "
        "The historic milestone is celebrated by running non-stop langar seva kitchens packed with hot kada prasad options."
    ),'''),

    ("gurupurab", "chhattisgarh", '''    ("gurupurab", "chhattisgarh"): (
        "Bright illuminations decorate gurdwara gateways across Chhattisgarh, initiating the joyful evening cycle of guru remembrance. "
        "Worshippers gather for selfless langar seva and midnight prayer sessions to honor the timeless teachings of the faith. "
        "The domestic hospitality centers on distributing large steel bowls of rich kada prasad to visiting relative circles."
    ),'''),

    ("gurupurab", "goa", '''    ("gurupurab", "goa"): (
        "Bustling coastal prayer halls echo with peaceful shabad kirtan tracks, drawing together local Goan diaspora communities. "
        "Worshippers spend the amrit vela hours cleaning the premises before the main congregational text readings open. "
        "The holy day concludes with volunteers managing an open langar seva paired with rich kada prasad portions."
    ),'''),

    ("gurupurab", "gujarat", '''    ("gurupurab", "gujarat"): (
        "A grand prabhat pheri moves through historic old town lanes across Gujarat during the pristine amrit vela phase. "
        "Local business units pause operations as merchants participate in extensive langar seva routines to serve the public. "
        "Extended families wind down the joyous day by sharing sweet kada prasad along with festive local thali items."
    ),'''),

    ("gurupurab", "haryana", '''    ("gurupurab", "haryana"): (
        "The solemn completion of a continuous akhand path anchors rural Haryana gurdwaras during the high-energy holiday. "
        "Agrarian families coordinate massive langar seva assemblies where community elders lead traditional devotional singing. "
        "The holy celebration is enriched by serving hot kada prasad paired with farm-style dairy delicacies to visitors."
    ),'''),

    ("gurupurab", "himachal-pradesh", '''    ("gurupurab", "himachal-pradesh"): (
        "Continuous Gurbani recitation lines echo through mountain valley gurdwaras in Himachal Pradesh, casting a beautiful winter contrast. "
        "Local clans travel down winding paths to participate in grand community-style langar seva gatherings around the fire. "
        "The spiritual afternoon is comforted by serving warm kada prasad formulas alongside rich mountain-style meals."
    ),'''),

    ("gurupurab", "jharkhand", '''    ("gurupurab", "jharkhand"): (
        "Traditional early-morning prabhat pheri groups sing melodic hymns inside illuminated residential colonies across Jharkhand. "
        "Devotees coordinate beautiful shabad kirtan platforms to illustrate foundational values to neighborhood youth groups. "
        "The daytime holiday is supported by managing non-stop langar seva nodes packed with sweet kada prasad."
    ),'''),

    ("gurupurab", "karnataka", '''    ("gurupurab", "karnataka"): (
        "The holy sarovar snan rituals re-energize local congregations across Karnataka neighborhoods before the main prayer cycles open. "
        "Worshippers gather for deep shabad kirtan meditation to offer collective gratitude for family health and well-being. "
        "Visiting guests are welcomed into local langar seva halls with delicious hot meals and sweet kada prasad."
    ),'''),

    ("gurupurab", "kerala", '''    ("gurupurab", "kerala"): (
        "A profound Gurbani recitation sets a deeply meditative stage inside pristine Kerala prayer rooms at dawn. "
        "Devotees organize extensive langar seva platforms to distribute free hot lunches to local hospital workers and travelers. "
        "The concluding hour is celebrated by serving sweet kada prasad variants alongside elaborate banana leaf spreads."
    ),'''),

    ("gurupurab", "madhya-pradesh", '''    ("gurupurab", "madhya-pradesh"): (
        "Melodic shabad kirtan notes fill local gurdwara properties across Madhya Pradesh during the holy amrit vela hours. "
        "Worshippers coordinate an early morning prabhat pheri that traces through historic neighborhoods singing sacred hymns. "
        "The local evening hospitality centers on serving hot kada prasad to the selfless langar seva workers."
    ),'''),

    ("gurupurab", "maharashtra", '''    ("gurupurab", "maharashtra"): (
        "A majestic nagar kirtan procession takes over roads across Mumbai and greater Maharashtra, showcasing the vibrant community spirit. "
        "Worshippers manage extensive langar seva queues inside illuminated community complexes to feed the local public. "
        "The household celebration centers on preparing fresh kada prasad formulas along with traditional Maharashtrian sweets."
    ),'''),

    ("gurupurab", "manipur", '''    ("gurupurab", "manipur"): (
        "A peaceful Gurbani recitation echoes throughout Manipuri prayer halls, beautifully tracking the dawn of guru remembrance. "
        "The congregation participates in a grand nagar kirtan procession that carries the Guru Granth Sahib parkash through decorated paths. "
        "The festive week concludes with volunteers arranging an open langar seva paired with sweet kada prasad."
    ),'''),

    ("gurupurab", "meghalaya", '''    ("gurupurab", "meghalaya"): (
        "The solemn echo of amrit vela prayers begins the dawn assembly inside local Meghalaya prayer rooms. "
        "Devotees look to the local head priest as a full-length Gurbani recitation clears the surrounding mountain valley. "
        "The winter gathering is highlighted by providing dedicated langar seva paired with hot kada prasad options."
    ),'''),

    ("gurupurab", "mizoram", '''    ("gurupurab", "mizoram"): (
        "The holy sound of a shabad kirtan session loops through private diaspora apartments across Mizoram. "
        "The small local community organizes a quiet prabhat pheri to announce the structural winter new year. "
        "The diaspora gathering concludes with sharing custom kada prasad items cooked inside the langar seva hub."
    ),'''),

    ("gurupurab", "nagaland", '''    ("gurupurab", "nagaland"): (
        "A majestic nagar kirtan procession takes over public pathways in Nagaland to mark the ancestral lineage safety. "
        "Worshippers complete a slow, meditative sarovar snan simulation before the main text reading cycles open. "
        "The peaceful seasonal gathering is highlighted by organizing an open langar seva paired with sweet kada prasad."
    ),'''),

    ("gurupurab", "odisha", '''    ("gurupurab", "odisha"): (
        "The holy sarovar snan rituals at historic gurdwaras initiate the sacred winter dawn across Odisha districts. "
        "Devotees gather to hear the profound Gurbani recitation and meditate on the teachings of the lineage. "
        "The holy days are accompanied by distributing rich kada prasad directly from the central langar seva kitchen."
    ),'''),

    ("gurupurab", "punjab", '''    ("gurupurab", "punjab"): (
        "Deep shabad kirtan recitations echo from the Golden Temple at the absolute peak of the global amrit vela hour. "
        "Millions of residents join spectacular nagar kirtan processions across Amritsar to mark the holy birth anniversary. "
        "The historic milestone is celebrated by running non-stop langar seva hubs delivering massive batches of sweet kada prasad."
    ),'''),

    ("gurupurab", "rajasthan", '''    ("gurupurab", "rajasthan"): (
        "Grand early morning prabhat pheri assemblies and beautiful winter light displays fill historic gurdwara courtyards across Rajasthan. "
        "Delicate courtyard spaces are swept clean for the long-form Gurbani recitation lines that loop until noon. "
        "The culinary gathering centers on serving sweet kada prasad variations directly from the continuous langar seva kitchen."
    ),'''),

    ("gurupurab", "sikkim", '''    ("gurupurab", "sikkim"): (
        "A solemn amrit vela prayer session brings mountain settlements together across the freezing ridges of Sikkim. "
        "Families gather inside localized prayer halls to complete their shared langar seva responsibilities for the valley. "
        "The local hospitality involves sharing custom sweet kada prasad formulas alongside warm festive rice dishes."
    ),'''),

    ("gurupurab", "tamil-nadu", '''    ("gurupurab", "tamil-nadu"): (
        "Massive shabad kirtan services inside urban gurdwaras transform Chennai neighborhoods long before sunrise. "
        "Worshippers organize extensive langar seva platforms to provide hot meals to local labor colonies and transit yards. "
        "The sacred day is celebrated by preparing sweet kada prasad variants alongside traditional southern snacks."
    ),'''),

    ("gurupurab", "telangana", '''    ("gurupurab", "telangana"): (
        "The spectacular early morning gurdwara turnouts in Hyderabad and Secunderabad define the peak of Telangana's holy calendar. "
        "Worshippers participate in a grand nagar kirtan procession featuring traditional martial arts displays on open roads. "
        "The primary household table is filled with sweet kada prasad portions alongside continuous langar seva items."
    ),'''),

    ("gurupurab", "tripura", '''    ("gurupurab", "tripura"): (
        "Beautiful early morning prabhat pheri walks fill community paths across Tripura, mirroring the winter arrival of the holiday. "
        "Worshippers assemble inside illuminated spaces to hear the profound Gurbani recitation and clean the community kitchen. "
        "The evening hospitality is highlighted by sharing traditional kada prasad items alongside local festive rice dishes."
    ),'''),

    ("gurupurab", "uttar-pradesh", '''    ("gurupurab", "uttar-pradesh"): (
        "The beautiful winter decorations at historic city gurdwaras transform public lanes across Uttar Pradesh at dawn. "
        "Bustling compound gates are packed with thousands of visitors participating in the selfless langar seva distributions. "
        "The high-energy days include distributing famous sweet kada prasad portions alongside traditional city items."
    ),'''),

    ("gurupurab", "uttarakhand", '''    ("gurupurab", "uttarakhand"): (
        "Shabad kirtan recitations in pristine alpine valley gurdwara spaces define the local community experience across Uttarakhand. "
        "Families gather around wood fires during the amrit vela phase to complete their shared scripture reading loops. "
        "The spiritual gathering is completed by serving sweet kada prasad formulas alongside custom langar seva meals."
    ),'''),

    ("gurupurab", "west-bengal", '''    ("gurupurab", "west-bengal"): (
        "Grand morning nagar kirtan assemblies and holy book processions transform the urban space of Kolkata and greater West Bengal. "
        "Worshippers don pristine white garments to manage extensive langar seva counters for the local working districts. "
        "The cultural transition is accompanied by distributing custom sweet kada prasad bowls to every household visitor."
    ),'''),

    ("gurupurab", "nri-london", '''    ("gurupurab", "nri-london"): (
        "Massive park assemblies and indoor shabad kirtan workshops connect the London diaspora for a unified spiritual milestone. "
        "Expatriates coordinate grand nagar kirtan processions that wind through local boroughs to showcase the heritage to the public. "
        "Families celebrate the winter transition by setting up non-stop langar seva counters packed with hot kada prasad."
    ),'''),

    ("gurupurab", "nri-new-york", '''    ("gurupurab", "nri-new-york"): (
        "Community centers host high-energy Gurbani recitation sessions and continuous amrit vela prayers across New York districts. "
        "Ornate diaspora halls and family video calls connect relatives across long distances for simultaneous holiday greetings. "
        "The diaspora gathering concludes with sharing custom sweet kada prasad variations inside local langar seva hubs."
    ),'''),

]

for festival, region, new_block in entries:
    content = replace_entry(content, festival, region, new_block)
    print(f"  ✓  ({festival}, {region})")

open(f, 'w').write(content)
print(f"\nDone. {len(entries)} entries applied. File size: {len(content)} chars")
