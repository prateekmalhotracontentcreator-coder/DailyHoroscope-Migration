#!/usr/bin/env python3
"""Round 6 spot-fix integration -- 10 entries across 3 clusters."""

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

    # ── CLUSTER A: navratri vs baisakhi (3 northeast regions) ────────────────

    ("navratri", "tripura", '''    ("navratri", "tripura"): (
        "Garba raas movements transform private inner courtyards across Tripura into dynamic hubs of sacred art. "
        "Devotees organize focused twilight stotra sessions to invoke protective cosmic order during the nine-night upvas. "
        "The domestic ritual phase concludes with families distributing warm kuttu atta halwa to visiting relatives."
    ),'''),

    ("baisakhi", "tripura", '''    ("baisakhi", "tripura"): (
        "Vaisakhi mela arrays bring an energetic northern rhythm to local assembly grounds across Tripura at sunrise. "
        "The assembly beats high-pitched dhols while youth groups execute fast-paced coordinated folk steps. "
        "The holiday is highlighted by preparing hot sarson da saag portions to share with the neighborhood."
    ),'''),

    ("navratri", "mizoram", '''    ("navratri", "mizoram"): (
        "Durga Saptashati recitation paths ground private diaspora residences in Mizoram with a deeply meditative spiritual energy. "
        "Worshippers light traditional brass lamps to channel the holy frequencies of the nine-night upvas. "
        "Fasting participants complete their daily strictness by consuming sweet sabudana khichdi inside their home sanctuaries."
    ),'''),

    ("baisakhi", "mizoram", '''    ("baisakhi", "mizoram"): (
        "Khalsa procession groups wave bright yellow banners across local Mizoram townships to mark the solar new year. "
        "The diaspora gathers inside decorated spaces to exchange traditional warm spring greetings and blessings. "
        "The seasonal gathering concludes with families serving hot makki di roti spreads within their local networks."
    ),'''),

    ("navratri", "nagaland", '''    ("navratri", "nagaland"): (
        "Dandiya sticks click in rhythmic synchronization across Nagaland spaces to anchor the sacred autumn calendar. "
        "Worshippers coordinate a strict navami havan to invite divine feminine protection and strength into their settlements. "
        "The evening hospitality features distributing small bowls of sweet kuttu atta halwa to visiting relative clans."
    ),'''),

    ("baisakhi", "nagaland", '''    ("baisakhi", "nagaland"): (
        "Bhangra performance sequences bring vibrant energy to residential colonies in Nagaland as the early morning mist clears. "
        "Worshippers complete a slow, meditative walk around agricultural flags to honor the massive wheat harvest threshing milestones. "
        "The peaceful seasonal milestone is highlighted by presenting large platters of hot sarson da saag to guests."
    ),'''),

    # ── CLUSTER B: maha-shivaratri vs baisakhi (sikkim) ──────────────────────

    ("maha-shivaratri", "sikkim", '''    ("maha-shivaratri", "sikkim"): (
        "A jaagran vigil keeps Sikkim devotees awake all night inside highly decorated high-altitude valley shrines. "
        "Worshippers complete an intensive Shiva linga abhishek using pristine mountain spring water, cold milk, and honey. "
        "The freezing midnight hours are comforted by distributing traditional warm thandai fluids directly to participants."
    ),'''),

    ("baisakhi", "sikkim", '''    ("baisakhi", "sikkim"): (
        "A grand Khalsa procession winds along hillside pathways in Sikkim, celebrating the vibrant Punjabi new year milestone. "
        "Youth groups execute high-energy bhangra performance steps to the rhythm of booming street dhols. "
        "The local harvest gathering is highlighted by preparing delicious sarson da saag spreads for mountain clans."
    ),'''),

    # ── CLUSTER C: navratri vs ganesh-chaturthi (manipur) ────────────────────

    ("navratri", "manipur", '''    ("navratri", "manipur"): (
        "Durga Saptashati recitation verses fill local Manipuri community halls, establishing an exclusive devotional scriptural path. "
        "Devotees coordinate peaceful kanya puja sessions to honor young girls as living expressions of divine strength. "
        "The nine-night upvas phase concludes with families sharing sweet kuttu atta halwa with extended relative networks."
    ),'''),

    ("ganesh-chaturthi", "manipur", '''    ("ganesh-chaturthi", "manipur"): (
        "Ganesh sthapana rituals initiate the grand autumn schedule inside a massive 10-day pandal enclosure in Manipur. "
        "Worshippers beat high-decibel dhol tasha drums to accompany the grand arrival of the clay Ganesha idol. "
        "The festive week concludes with organizers distributing large trays of handcrafted coconut-jaggery modak to clans."
    ),'''),

]

for festival, region, new_block in entries:
    content = replace_entry(content, festival, region, new_block)
    print(f"  ✓  ({festival}, {region})")

open(f, 'w').write(content)
print(f"\nDone. File size: {len(content)} chars")
