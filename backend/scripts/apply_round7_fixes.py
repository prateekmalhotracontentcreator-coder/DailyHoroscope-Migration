#!/usr/bin/env python3
"""Round 7 spot-fix integration -- 4 final entries, 2 regions."""

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

    # ── REGION 1: manipur -- maha-shivaratri vs baisakhi ──────────────────────

    ("maha-shivaratri", "manipur", '''    ("maha-shivaratri", "manipur"): (
        "Shiva linga abhishek rituals performed at local shrines transform the night into a period of deep spiritual focus across Manipur. "
        "Worshippers maintain a strict night-long fast while carefully washing the sacred stone with raw milk and honey. "
        "Exhausted devotees conclude their intensive meditation sessions by consuming cups of freshly strained thandai."
    ),'''),

    ("baisakhi", "manipur", '''    ("baisakhi", "manipur"): (
        "Khalsa procession marches snake through the streets of Manipur to honor the historic foundational memories of the faith. "
        "Vibrant youth groups beat heavy drums and leap into high-energy bhangra patterns to gather the local community. "
        "The daytime gathering draws to a close as volunteers distribute large steel platters of hot sarson da saag."
    ),'''),

    # ── REGION 2: nagaland -- ganesh-chaturthi vs maha-shivaratri ─────────────

    ("ganesh-chaturthi", "nagaland", '''    ("ganesh-chaturthi", "nagaland"): (
        "Ganesh sthapana ceremonies initiate the festive schedule in Nagaland as families welcome the deity into their homes. "
        "Worshippers strike heavy brass cymbals and play dhol tasha instruments to signal the formal beginning of the rituals. "
        "The household gathering culminates in distributing sweet steaming batches of coconut-jaggery modak."
    ),'''),

    ("maha-shivaratri", "nagaland", '''    ("maha-shivaratri", "nagaland"): (
        "A jaagran vigil keeps local devotees completely awake until daylight hours inside traditional hillside structures across Nagaland. "
        "Devout individuals repeatedly offer fresh green bilva leaves while softly counting holy prayer beads in absolute silence. "
        "The deep meditation cycle finishes when the participants drink a traditional beverage containing cooling bhaang."
    ),'''),

]

for festival, region, new_block in entries:
    content = replace_entry(content, festival, region, new_block)
    print(f"  ✓  ({festival}, {region})")

open(f, 'w').write(content)
print(f"\nDone. File size: {len(content)} chars")
