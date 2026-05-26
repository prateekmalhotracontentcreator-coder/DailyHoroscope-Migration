#!/usr/bin/env python3
"""Round 5 spot-fix integration -- 22 entries across 6 clusters."""

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

    # ── CLUSTER A: durga-puja vs gurupurab ────────────────────────────────────

    ("durga-puja", "haryana", '''    ("durga-puja", "haryana"): (
        "The echoing thunder of dhaak beats introduces the autumn structural shift inside localized Haryana residential complexes. "
        "Worshippers gather to engage in competitive dhunuchi naach moves before the heavy incense burners are placed near the stage. "
        "The ritual night finishes with families distributing sweet sandesh variants across visiting neighbor networks."
    ),'''),

    ("gurupurab", "haryana", '''    ("gurupurab", "haryana"): (
        "A loud prabhat pheri moves through Haryana village streets during the pristine early morning hours. "
        "The congregation gathers for an intense shabad kirtan recitation inside the main hall to praise the historical lineage. "
        "The agrarian holiday is completed by offering continuous langar seva alongside warm, buttery kada prasad."
    ),'''),

    ("durga-puja", "meghalaya", '''    ("durga-puja", "meghalaya"): (
        "Devout families prepare for a grand evening of pandal hopping as temporary structures light up the hills of Meghalaya. "
        "Women organize the emotional sindoor khela items to bless their relatives during the final seasonal adjustments. "
        "The seasonal gathering is highlighted by presenting large trays of chalar payesh to visiting friends."
    ),'''),

    ("gurupurab", "meghalaya", '''    ("gurupurab", "meghalaya"): (
        "The solemn echo of amrit vela prayers begins the dawn assembly inside local Meghalaya prayer rooms. "
        "Devotees look to the local head priest as a full-length Gurbani recitation clears the surrounding mountain valley. "
        "The winter gathering is highlighted by providing dedicated langar seva paired with hot kada prasad options."
    ),'''),

    ("durga-puja", "mizoram", '''    ("durga-puja", "mizoram"): (
        "A grand morning pushpanjali ritual commences behind beautifully decorated clay idols inside private diaspora halls in Mizoram. "
        "Devotees gather to watch an intricate kumari puja ceremony designed to highlight traditional maternal protection. "
        "The spring occasion is highlighted by distributing sweet rasgulla formulas among remote neighborhood blocks."
    ),'''),

    ("gurupurab", "mizoram", '''    ("gurupurab", "mizoram"): (
        "The holy sound of a shabad kirtan session loops through private diaspora apartments across Mizoram. "
        "The small local community organizes a quiet prabhat pheri to announce the structural winter new year. "
        "The diaspora gathering concludes with sharing custom kada prasad items cooked inside the langar seva hub."
    ),'''),

    ("durga-puja", "nagaland", '''    ("durga-puja", "nagaland"): (
        "A spectacular indoor visarjan procession is arranged across Nagaland spaces to finalize the multi-day goddess celebration. "
        "Worshippers offer silent pushpanjali prayers to invoke the supreme strength and defensive shielding of the deity. "
        "The sacred time involves sharing delicious narkel naru portions alongside traditional clan feast treats."
    ),'''),

    ("gurupurab", "nagaland", '''    ("gurupurab", "nagaland"): (
        "A majestic nagar kirtan procession takes over public pathways in Nagaland to mark the ancestral lineage safety. "
        "Worshippers complete a slow, meditative sarovar snan simulation before the main text reading cycles open. "
        "The peaceful seasonal gathering is highlighted by organizing an open langar seva paired with sweet kada prasad."
    ),'''),

    # ── CLUSTER B: ram-navami vs hanuman-jayanti ──────────────────────────────

    ("ram-navami", "madhya-pradesh", '''    ("ram-navami", "madhya-pradesh"): (
        "A grand Sita-Ram wedding reenactment takes over the historic Orchha palace grounds across Madhya Pradesh at noon. "
        "Devotees observe a strict midday fast to coincide precisely with the glorious moment of the avatar's birth. "
        "The local evening hospitality centers on sharing chilled panchamrit collections with visiting temple crowds."
    ),'''),

    ("hanuman-jayanti", "madhya-pradesh", '''    ("hanuman-jayanti", "madhya-pradesh"): (
        "A full-volume Hanuman Chalisa marathon echoes through historic hilltop mandirs across Madhya Pradesh at sunrise. "
        "Bustling youth groups wave bright banners during an energetic akhara procession that winds through old lanes. "
        "The local evening hospitality features distributing massive batches of sweet boondi laddoo bhog to visitors."
    ),'''),

    ("ram-navami", "manipur", '''    ("ram-navami", "manipur"): (
        "A continuous Ramcharitmanas akhand path fills local Manipuri temples, establishing a pristine devotional setting. "
        "Extended families gather around the central navami havan fire to invite righteousness into their settlements. "
        "The daily celebration concludes with families distributing pure charan amrit fluids directly to visiting relative networks."
    ),'''),

    ("hanuman-jayanti", "manipur", '''    ("hanuman-jayanti", "manipur"): (
        "A continuous Sunderkand path recitation bridges local Manipur harmony with the global focus on the warrior deity. "
        "Worshippers complete a slow, meditative parikrama of Hanuman temple while flying traditional triangular pennants. "
        "The festive week concludes with organizers distributing large trays of handcrafted motichoor laddoo bhog to clans."
    ),'''),

    # ── CLUSTER C: navratri vs baisakhi ──────────────────────────────────────

    ("navratri", "himachal-pradesh", '''    ("navratri", "himachal-pradesh"): (
        "An intense Durga Saptashati recitation echoes through hillside temples in Himachal Pradesh to anchor the mountain air. "
        "Clans travel down winding paths to participate in a sacred navami havan designed to invoke maternal protection. "
        "The spiritual afternoon is comforted by serving warm kuttu atta halwa alongside classic mountain-style meals."
    ),'''),

    ("baisakhi", "himachal-pradesh", '''    ("baisakhi", "himachal-pradesh"): (
        "A vibrant bhangra performance brings high-energy dhol rhythms to mountain valley settlements across Himachal Pradesh. "
        "Worshippers complete a holy bathing at sarovar to honor the historic spring agricultural calendar reset. "
        "The joyful afternoon is comforted by distributing large bowls of hot sarson da saag around shared hearths."
    ),'''),

    ("navratri", "odisha", '''    ("navratri", "odisha"): (
        "Swirling dandiya sticks and intricate home decorations transform local living rooms across Odisha during the autumn months. "
        "Devotees coordinate peaceful community kanya puja sessions to offer collective gratitude for family health. "
        "The holy days are accompanied by distributing traditional sabudana khichdi mixtures along with classic temple sweets."
    ),'''),

    ("baisakhi", "odisha", '''    ("baisakhi", "odisha"): (
        "A grand Khalsa procession takes over urban roads in Odisha to celebrate the vibrant Punjabi new year milestone. "
        "Youth groups wave bright banners during a lively Vaisakhi mela that winds through historic neighborhoods. "
        "The holy days are accompanied by distributing traditional makki di roti spreads directly from communal kitchens."
    ),'''),

    # ── CLUSTER D: ganesh-chaturthi vs maha-shivaratri ────────────────────────

    ("ganesh-chaturthi", "tripura", '''    ("ganesh-chaturthi", "tripura"): (
        "A grand Ganesh sthapana ritual transforms family inner courtyards across Tripura as the autumn cycle begins. "
        "Worshippers beat rhythmic dhol tasha drums during the evening to accompany high-energy family aarti selections. "
        "The evening hospitality is highlighted by sharing fresh coconut-jaggery modak portions with neighborhood guests."
    ),'''),

    ("maha-shivaratri", "tripura", '''    ("maha-shivaratri", "tripura"): (
        "An intense jaagran vigil keeps Tripura devotees awake all night inside highly decorated temple yards. "
        "Worshippers perform a continuous Shiva linga abhishek using cold milk, honey, and fresh bilva leaves. "
        "The winter evening is marked by distributing traditional thandai fluids directly to exhausted participants."
    ),'''),

    # ── CLUSTER E: navratri vs ganesh-chaturthi ───────────────────────────────

    ("navratri", "sikkim", '''    ("navratri", "sikkim"): (
        "Swirling dandiya sticks turn hillside pathways vibrant in Sikkim as the early autumn mist clears. "
        "Devotees gather around home altars to read the intensive Durga Saptashati recitation for family well-being. "
        "The local hospitality involves sharing sweet kuttu atta halwa formulas among remote mountain settlements."
    ),'''),

    ("ganesh-chaturthi", "sikkim", '''    ("ganesh-chaturthi", "sikkim"): (
        "A sacred Ganesh sthapana commences behind beautifully sculpted clay Ganesha idols along Sikkim mountain ridges. "
        "Local youth groups beat high-energy dhol tasha tracks to announce the structural holiday arrival. "
        "The local gathering is highlighted by presenting large bowls of handcrafted coconut-jaggery modak to mountain clans."
    ),'''),

    # ── CLUSTER F: onam vs baisakhi ───────────────────────────────────────────

    ("onam", "nri-new-york", '''    ("onam", "nri-new-york"): (
        "A magnificent pookalam floral carpet is laid out across New York apartment entryways to preserve coastal traditions. "
        "Diaspora families wear traditional white attire to share a grand Onam Sadhya on banana leaves during the afternoon. "
        "The diaspora gathering concludes with serving bowls of sweet payasam inside local residential networks."
    ),'''),

    ("baisakhi", "nri-new-york", '''    ("baisakhi", "nri-new-york"): (
        "A majestic Khalsa procession takes over central avenues in New York, celebrating the vibrant Punjabi new year. "
        "Youth groups execute high-energy bhangra performance sequences to mark the completion of the global wheat harvest. "
        "The diaspora gathering concludes with sharing custom makki di roti spreads within local community center networks."
    ),'''),

]

for festival, region, new_block in entries:
    content = replace_entry(content, festival, region, new_block)
    print(f"  ✓  ({festival}, {region})")

open(f, 'w').write(content)
print(f"\nDone. File size: {len(content)} chars")
