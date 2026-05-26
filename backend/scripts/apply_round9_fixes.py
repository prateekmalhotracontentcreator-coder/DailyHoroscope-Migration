#!/usr/bin/env python3
"""Round 9 spot-fix integration -- 6 final entries, 3 borderline regions."""

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

    # ── REGION 1: karnataka -- ram-navami vs hanuman-jayanti ──────────────────

    ("ram-navami", "karnataka", '''    ("ram-navami", "karnataka"): (
        "Surya puja at noon marks the exact alignment of solar rays across principal Karnataka temples to celebrate the divine birth hour. "
        "Extended family units join together around a sacred navami havan fire to chant Vedic mantras for household cosmic order. "
        "Priests pour a refreshing stream of liquid panchamrit directly into the copper vessels of waiting worshippers."
    ),'''),

    ("hanuman-jayanti", "karnataka", '''    ("hanuman-jayanti", "karnataka"): (
        "Sunderkand path recitations resonate throughout early morning assemblies in Karnataka to honor the ultimate loyalty of the deity. "
        "A high-energy Hanuman Chalisa marathon brings large neighborhood crowds together for collective protection and strength. "
        "The day ends with the distribution of massive spheres of sweet boondi laddoo bhog inside the main temple courtyard."
    ),'''),

    # ── REGION 2: uttar-pradesh -- christmas vs gurupurab ─────────────────────

    ("christmas", "uttar-pradesh", '''    ("christmas", "uttar-pradesh"): (
        "Glowing star lanterns are hung across porches in Uttar Pradesh to welcome the cold winter nativity atmosphere. "
        "Families bundle up to attend a solemn midnight mass service filled with classical choral sequences. "
        "The festive holiday morning is celebrated by slicing pieces of rich, dark homemade plum cake."
    ),'''),

    ("gurupurab", "uttar-pradesh", '''    ("gurupurab", "uttar-pradesh"): (
        "The continuous akhand path reaches its solemn conclusion at dawn inside illuminated gurdwaras across Uttar Pradesh. "
        "Dozens of volunteers manage the non-stop langar seva kitchen lines to feed thousands of local visitors sitting in synchronized rows. "
        "Gratitude fills the air as community members receive warm, sweet blocks of kada prasad directly from the distribution counters."
    ),'''),

    # ── REGION 3: uttarakhand -- ganesh-chaturthi vs maha-shivaratri ──────────

    ("ganesh-chaturthi", "uttarakhand", '''    ("ganesh-chaturthi", "uttarakhand"): (
        "A sacred Ganesh sthapana takes place behind beautifully sculpted clay Ganesha idols to welcome the autumn cycle in Uttarakhand. "
        "Local youth groups beat high-energy dhol tasha drum patterns to accompany the grand arrival of the deity through alpine streets. "
        "The festive gathering concludes with kitchens steaming fresh, sweet batches of handmade coconut-jaggery modak."
    ),'''),

    ("maha-shivaratri", "uttarakhand", '''    ("maha-shivaratri", "uttarakhand"): (
        "A jaagran vigil keeps local Uttarakhand devotees completely awake until morning hours to honor the supreme cosmic energy. "
        "Worshippers offer fresh green bilva leaves while executing a continuous Shiva linga abhishek with honey and raw milk. "
        "The freezing mountain night is comforted by sharing traditional cups of cold, herb-infused thandai."
    ),'''),

]

for festival, region, new_block in entries:
    content = replace_entry(content, festival, region, new_block)
    print(f"  ✓  ({festival}, {region})")

open(f, 'w').write(content)
print(f"\nDone. File size: {len(content)} chars")
