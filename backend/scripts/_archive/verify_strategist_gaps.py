import sys
from pymongo import MongoClient
from collections import Counter

client = MongoClient(sys.argv[1])
col = client['horoscope_db']['knowledge_rules']

all_records = list(col.find(
    {'science_id': 'lalkitab_strategist'},
    {'id': 1, 'approval_status': 1, 'mission_name': 1, 'strategy': 1, '_id': 0}
))

ids = sorted([r['id'] for r in all_records])

# Known ranges
known = set()
for i in range(651, 676):   known.add(i)   # surrogates
for i in range(701, 745):   known.add(i)   # battlefield
for i in range(745, 952):   known.add(i)   # siege ops
for i in range(952, 976):   known.add(i)   # window + hurdles
for i in range(976, 1028):  known.add(i)   # peak + exit + golden hour
for i in range(1126, 1138): known.add(i)   # salvage patch

outside = [i for i in ids if i not in known]
print(f"Total records: {len(ids)}")
print(f"IDs outside known ranges ({len(outside)}):")

# Group into ranges for readability
if outside:
    groups = []
    start = outside[0]
    prev = outside[0]
    for i in outside[1:]:
        if i == prev + 1:
            prev = i
        else:
            groups.append((start, prev))
            start = i
            prev = i
    groups.append((start, prev))
    for s, e in groups:
        if s == e:
            rec = next((r for r in all_records if r['id'] == s), {})
            name = rec.get('mission_name') or rec.get('strategy', '?')
            print(f"  ID {s}: {name}")
        else:
            print(f"  IDs {s}-{e} ({e-s+1} records)")

# Missing from siege ops (745-951)
siege_ids = set(r['id'] for r in all_records if 745 <= r['id'] <= 951)
missing_siege = [i for i in range(745, 952) if i not in siege_ids]
print(f"\nMissing from Siege Ops (745-951): {missing_siege}")

# LK Remedies approval status breakdown
lk_statuses = Counter(
    r['approval_status']
    for r in col.find({'science_id': 'jyotish_lk_remedies'}, {'approval_status': 1, '_id': 0})
)
print(f"\nLK Remedies approval breakdown: {dict(lk_statuses)}")
