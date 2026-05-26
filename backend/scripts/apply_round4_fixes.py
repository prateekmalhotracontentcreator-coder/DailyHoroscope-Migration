#!/usr/bin/env python3
"""Round 4 spot-fix integration -- 38 entries across 4 clusters."""

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

    # ── CLUSTER 1: ram-navami vs hanuman-jayanti ──────────────────────────────

    ("ram-navami", "gujarat", '''    ("ram-navami", "gujarat"): (
        "Surya puja at noon marks the exact alignment of solar rays across principal Gujarati shrines to welcome the avatar. "
        "Devotees assemble to participate in grand janmotsav processions that feature beautifully decorated dynamic chariot replicas. "
        "Fasting families break their strict daylight restrictions by distributing sacred charan amrit to local temple crowds."
    ),'''),

    ("hanuman-jayanti", "gujarat", '''    ("hanuman-jayanti", "gujarat"): (
        "Sunderkand path recitations resonate throughout historic Gujarati neighborhoods as early morning crowds salute the deity. "
        "Bustling youth groups carry out intense saffron flag hoisting routines across town squares before the main communal assemblies. "
        "The energetic daytime celebration concludes with local temples distributing massive quantities of boondi laddoo bhog."
    ),'''),

    ("ram-navami", "himachal-pradesh", '''    ("ram-navami", "himachal-pradesh"): (
        "Kalash sthapana rituals initiate the sacred spring dawn inside remote Himachal Pradesh mountain valley shrines. "
        "Clans travel down winding paths to receive a cleansing panchamrit abhishek of Ram icon from the temple priests. "
        "The cold afternoon is warmed as families gather around home altars to consume warm ceremonial charan amrit."
    ),'''),

    ("hanuman-jayanti", "himachal-pradesh", '''    ("hanuman-jayanti", "himachal-pradesh"): (
        "A Hanuman Chalisa marathon echoes through hillside temples in Himachal Pradesh to invoke immediate spiritual defense. "
        "Local youth gather on open village grounds to participate in dynamic dangal and kushti wrestling matches under traditional rules. "
        "The high-energy afternoon concludes with community elders handing out rich besan laddoo bhog to exhausted participants."
    ),'''),

    ("ram-navami", "nagaland", '''    ("ram-navami", "nagaland"): (
        "A Ramcharitmanas akhand path commences behind decorated home altars in Nagaland, establishing a pristine devotional setting. "
        "Diaspora families coordinate an elegant Sita-Ram wedding reenactment to display timeless spiritual milestones to the youth. "
        "The holy day is honored by serving light fasting meals paired with fresh fruit juices."
    ),'''),

    ("hanuman-jayanti", "nagaland", '''    ("hanuman-jayanti", "nagaland"): (
        "A solemn veer Hanuman invocation brings small diaspora circles together across Nagaland to anchor the early morning prayers. "
        "Worshippers complete a slow, meditative parikrama of Hanuman temple while flying traditional triangular pennants. "
        "The high-energy gathering concludes with organizers distributing large trays of handcrafted laddoo bhog to visitors."
    ),'''),

    ("ram-navami", "haryana", '''    ("ram-navami", "haryana"): (
        "The unveiling of a pristine Ram Lalla icon transforms Haryana courtyard shrines as the precise midday hour strikes. "
        "Extended agrarian families complete a sacred navami havan to invite protective blessings into their farmlands. "
        "The holy celebration involves distributing liquid panchamrit abhishek of Ram icon directly from polished brass vessels."
    ),'''),

    ("hanuman-jayanti", "haryana", '''    ("hanuman-jayanti", "haryana"): (
        "An intense akhara procession takes over public roads across Haryana, showcasing traditional physical prowess and agility. "
        "Local farmers host high-energy dangal wrestling tournaments to honor the immense strength of the deity. "
        "The rustic holiday is enriched by distributing massive spheres of sweet laddoo bhog to working field hands."
    ),'''),

    ("ram-navami", "sikkim", '''    ("ram-navami", "sikkim"): (
        "A solemn kalash sthapana ritual is executed along Sikkim mountain ridges to orient the community toward righteousness. "
        "Devotees look to the sky for a synchronized Surya puja at noon long before any fasting boundaries are broken. "
        "The local hospitality involves sharing pure charan amrit mixtures among remote hillside settlements."
    ),'''),

    ("hanuman-jayanti", "sikkim", '''    ("hanuman-jayanti", "sikkim"): (
        "Vibrant saffron flag hoisting routines turn hillside pathways golden in Sikkim as the early morning mist clears. "
        "Worshippers join together for a long, dedicated parikrama of Hanuman temple to pray for spiritual shielding. "
        "The local gathering is highlighted by presenting large bowls of motichoor laddoo bhog to mountain clans."
    ),'''),

    ("ram-navami", "tripura", '''    ("ram-navami", "tripura"): (
        "A continuous Ramcharitmanas akhand path fills family inner courtyards across Tripura, guiding the domestic focus toward righteousness. "
        "Families coordinate an elaborate Sita-Ram wedding reenactment using traditional ceremonial garments and brass oil lamps. "
        "The spring evening is marked by sharing pure charan amrit portions alongside local fasting delicacies."
    ),'''),

    ("hanuman-jayanti", "tripura", '''    ("hanuman-jayanti", "tripura"): (
        "A full-volume Hanuman Chalisa marathon echoes through local public blocks in Tripura to salute the warrior deity. "
        "Worshippers organize a spectacular akhara procession featuring complex maneuvers with traditional staff implements. "
        "The evening hospitality is highlighted by presenting massive platters of boondi laddoo bhog to neighborhood guests."
    ),'''),

    ("ram-navami", "west-bengal", '''    ("ram-navami", "west-bengal"): (
        "The sacred panchamrit abhishek of Ram icon alters the morning domestic rhythm inside traditional West Bengal households. "
        "Devotees coordinate a magnificent janmotsav procession that features beautifully styled clay tableaux across town squares. "
        "The cultural transition involves distributing liquid charan amrit directly to visiting relative networks."
    ),'''),

    ("hanuman-jayanti", "west-bengal", '''    ("hanuman-jayanti", "west-bengal"): (
        "A solemn Sunderkand path recitation initiates the early morning hours inside neighborhood shrines across West Bengal. "
        "Youth groups wave bright banners during a lively parikrama of Hanuman temple that winds through historic old lanes. "
        "The high-energy day includes distributing famous sweet motichoor laddoo bhog to exhausted participants."
    ),'''),

    ("ram-navami", "meghalaya", '''    ("ram-navami", "meghalaya"): (
        "A pristine kalash sthapana setup defines the local community experience inside Meghalaya prayer halls at sunrise. "
        "Devotees observe a strict midday fast while listening to traditional stories regarding the avatar's childhood. "
        "The warm afternoon hospitality features sharing pure charan amrit portions within multi-generational families."
    ),'''),

    ("hanuman-jayanti", "meghalaya", '''    ("hanuman-jayanti", "meghalaya"): (
        "Bright saffron flag hoisting routines introduce an intense spiritual energy across the hills of Meghalaya. "
        "Worshippers gather for a high-energy Hanuman Chalisa marathon to pray for ancestral lineage safety and defense. "
        "The seasonal gathering is highlighted by presenting large boxes of besan laddoo bhog to visiting friends."
    ),'''),

    ("ram-navami", "mizoram", '''    ("ram-navami", "mizoram"): (
        "The beautiful installation of a Ram Lalla icon inside private diaspora spaces in Mizoram grounds the spring holiday. "
        "Worshippers coordinate a strict navami havan to invite protective cosmic order into their temporary residences. "
        "The spring occasion is highlighted by distributing pure panchamrit abhishek of Ram icon mixtures among clans."
    ),'''),

    ("hanuman-jayanti", "mizoram", '''    ("hanuman-jayanti", "mizoram"): (
        "A continuous Sunderkand path recitation bridges local diaspora harmony with the global focus on the warrior deity. "
        "Worshippers complete a slow, meditative parikrama of Hanuman temple while chanting ancient protection verses. "
        "The daytime gathering concludes with sharing sweet laddoo bhog variations across local townships."
    ),'''),

    ("ram-navami", "nri-london", '''    ("ram-navami", "nri-london"): (
        "A grand Sita-Ram wedding reenactment takes over hired community assembly halls across London to preserve ancestral traditions. "
        "Expatriates perform a precise Surya puja at noon to align with simultaneous global birth hour events. "
        "Families mark the spring milestone by packing small flasks of charan amrit to distribute to diaspora networks."
    ),'''),

    ("hanuman-jayanti", "nri-london", '''    ("hanuman-jayanti", "nri-london"): (
        "A full-scale Hanuman Chalisa marathon connects families across London boroughs for a unified spiritual shield. "
        "Children participate in a symbolic veer Hanuman invocation that details historical tales of courage and focus. "
        "The diaspora gathering concludes with distributing massive batches of boondi laddoo bhog inside local cultural centers."
    ),'''),

    # ── CLUSTER 2: durga-puja vs gurupurab ────────────────────────────────────

    ("durga-puja", "manipur", '''    ("durga-puja", "manipur"): (
        "Resounding dhaak beats and classical devotional movements fill local Manipuri mandaps during the grand autumn descent. "
        "Worshippers coordinate an elaborate kumari puja ceremony to honor young girls as living forms of divine energy. "
        "The sacred week concludes with families distributing sweet sandesh portions alongside specialized local sweets."
    ),'''),

    ("gurupurab", "manipur", '''    ("gurupurab", "manipur"): (
        "A peaceful Gurbani recitation echoes throughout Manipuri prayer halls, beautifully tracking the dawn of guru remembrance. "
        "The congregation participates in a grand nagar kirtan procession that carries the Guru Granth Sahib parkash through decorated paths. "
        "The festive week concludes with volunteers arranging an open langar seva paired with sweet kada prasad."
    ),'''),

    ("durga-puja", "madhya-pradesh", '''    ("durga-puja", "madhya-pradesh"): (
        "Spectacular pandal hopping routes draw thousands of residents into illuminated public streets across Madhya Pradesh after sunset. "
        "Devotees join together for high-energy dhunuchi naach competitions to celebrate the supreme strength of the goddess. "
        "The local evening hospitality features sharing rows of chalar payesh alongside regional street savouries."
    ),'''),

    ("gurupurab", "madhya-pradesh", '''    ("gurupurab", "madhya-pradesh"): (
        "Melodic shabad kirtan notes fill local gurdwara properties across Madhya Pradesh during the holy amrit vela hours. "
        "Worshippers coordinate an early morning prabhat pheri that traces through historic neighborhoods singing sacred hymns. "
        "The local evening hospitality centers on serving hot kada prasad to the selfless langar seva workers."
    ),'''),

    ("durga-puja", "odisha", '''    ("durga-puja", "odisha"): (
        "The grand morning pushpanjali rituals inside ancient Cuttack shrines transform local districts across Odisha. "
        "Extended family units join together for the emotional sindoor khela greetings before the final immersion phase. "
        "The holy days are accompanied by distributing traditional rasgulla items alongside classic temple sweets."
    ),'''),

    ("gurupurab", "odisha", '''    ("gurupurab", "odisha"): (
        "The holy sarovar snan rituals at historic gurdwaras initiate the sacred winter dawn across Odisha districts. "
        "Devotees gather to hear the profound Gurbani recitation and meditate on the teachings of the lineage. "
        "The holy days are accompanied by distributing rich kada prasad directly from the central langar seva kitchen."
    ),'''),

    # ── CLUSTER 3: navratri vs baisakhi ──────────────────────────────────────

    ("navratri", "karnataka", '''    ("navratri", "karnataka"): (
        "Swirling dandiya sticks and traditional home decorations alter the domestic atmosphere across Karnataka during the autumn months. "
        "Devotees read the intensive Durga Saptashati recitation to invite protective cosmic order into their living spaces. "
        "The evening feast is defined by preparing delicious kuttu atta halwa variations alongside classic southern treats."
    ),'''),

    ("baisakhi", "karnataka", '''    ("baisakhi", "karnataka"): (
        "A grand Khalsa procession takes over urban roads across Karnataka, celebrating the vibrant Punjabi new year milestone. "
        "Youth groups coordinate high-energy bhangra performance sequences to the rhythm of booming street dhols. "
        "The daytime feast involves preparing delicious sarson da saag distribution spreads for the gathered community."
    ),'''),

    ("navratri", "kerala", '''    ("navratri", "kerala"): (
        "The traditional ghat sthapana pot installation and deep shakti invocation rituals reshape the Kerala household routine. "
        "Young children gather for the beautiful kanya puja blessings inside pristine coastal temple corridors. "
        "The concluding milestone is celebrated by serving sweet fasting dishes alongside elaborate banana leaf spreads."
    ),'''),

    ("baisakhi", "kerala", '''    ("baisakhi", "kerala"): (
        "A colorful Vaisakhi mela transforms local assembly fields in Kerala, bringing a refreshing northern rhythm to the state. "
        "Worshippers complete a holy bathing at sarovar to honor the historic spring agricultural calendar reset. "
        "The daytime gathering concludes with sharing custom wheat flatbreads within local diaspora networks."
    ),'''),

    ("navratri", "uttar-pradesh", '''    ("navratri", "uttar-pradesh"): (
        "Endless Garba raas circles and spectacular temporary shrines transform public squares across Uttar Pradesh under bright lights. "
        "Extended families complete an intense navami havan to conclude their strict nine-night upvas boundaries. "
        "The high-energy days include distributing famous kuttu atta halwa alongside traditional city sweets."
    ),'''),

    ("baisakhi", "uttar-pradesh", '''    ("baisakhi", "uttar-pradesh"): (
        "Vibrant wheat harvest threshing displays and high-energy rural fairs transform agricultural districts across Uttar Pradesh. "
        "Local communities gather for a majestic amrit sanchar ceremony to preserve the foundational warrior code. "
        "The high-energy days include distributing hot sarson da saag alongside rustic country treats."
    ),'''),

    ("navratri", "uttarakhand", '''    ("navratri", "uttarakhand"): (
        "A high-altitude Vaishno Devi darshan pilgrimage defines the local experience in Uttarakhand during the autumn months. "
        "Remote mountain settlements participate in quiet Durga Saptashati recitation paths to invoke protective maternal energy. "
        "The spiritual gathering is completed by serving sweet fasting desserts alongside custom alpine treats."
    ),'''),

    ("baisakhi", "uttarakhand", '''    ("baisakhi", "uttarakhand"): (
        "Traditional gidda movements and high-energy dhol beats fill open valley spaces in Uttarakhand during the spring harvest. "
        "Devotees complete a holy bathing at sarovar to receive seasonal blessings long before any family meals are served. "
        "The spiritual gathering is completed by serving hot sarson da saag meals alongside custom alpine treats."
    ),'''),

    # ── CLUSTER 4: isolated spot-fixes ───────────────────────────────────────

    ("maha-shivaratri", "nri-new-york", '''    ("maha-shivaratri", "nri-new-york"): (
        "An intense jaagran vigil keeps New York diaspora families awake all night inside high-rise apartment spaces. "
        "Devotees perform a precise Shiva linga abhishek using fresh milk and imported bilva leaves to invite absolute inner calm. "
        "The diaspora gathering concludes with worshippers chanting Om Namah Shivaya lines around the holy altar."
    ),'''),

    ("ram-navami", "nri-new-york", '''    ("ram-navami", "nri-new-york"): (
        "A continuous Ramcharitmanas akhand path connects long-distance relatives via video calls to New York temple halls. "
        "Parents assemble a pristine kalash sthapana setup before the afternoon janmotsav procession begins down city avenues. "
        "The diaspora gathering concludes with sharing custom charan amrit formulas within local apartment networks."
    ),'''),

    ("baisakhi", "maharashtra", '''    ("baisakhi", "maharashtra"): (
        "A majestic Khalsa procession takes over streets in Pune and Mumbai, uniting the vibrant local Punjabi community in Maharashtra. "
        "Youth groups execute high-energy bhangra performance sequences to mark the completion of the global wheat harvest. "
        "The modern urban holiday is celebrated by launching a lively Vaisakhi mela filled with traditional culinary booths."
    ),'''),

    ("ram-navami", "maharashtra", '''    ("ram-navami", "maharashtra"): (
        "The sacred kalash sthapana ritual anchors home altars across Maharashtra, initiating the spring day of the avatar. "
        "Families coordinate a pristine panchamrit abhishek before gathering around the central navami havan fire. "
        "The family gathering centers on preparing light fasting items alongside traditional Maharashtrian sweets."
    ),'''),

]

for festival, region, new_block in entries:
    content = replace_entry(content, festival, region, new_block)
    print(f"  ✓  ({festival}, {region})")

open(f, 'w').write(content)
print(f"\nDone. File size: {len(content)} chars")
