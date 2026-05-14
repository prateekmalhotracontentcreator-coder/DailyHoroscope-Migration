import sys
from pymongo import MongoClient

client = MongoClient(sys.argv[1])
col = client['horoscope_db']['knowledge_rules']

# LK Remedies
lk = col.count_documents({'science_id': 'jyotish_lk_remedies'})
lk_approved = col.count_documents({'science_id': 'jyotish_lk_remedies', 'approval_status': 'approved'})

# Strategist totals
st = col.count_documents({'science_id': 'lalkitab_strategist'})
st_approved = col.count_documents({'science_id': 'lalkitab_strategist', 'approval_status': 'approved'})
st_phr = col.count_documents({'science_id': 'lalkitab_strategist', 'approval_status': 'pending_human_review'})

# Strategist ID blocks
st_surrogates = col.count_documents({'science_id': 'lalkitab_strategist', 'id': {'$gte': 651, '$lte': 675}})
st_battlefield = col.count_documents({'science_id': 'lalkitab_strategist', 'id': {'$gte': 701, '$lte': 744}})
st_siege = col.count_documents({'science_id': 'lalkitab_strategist', 'id': {'$gte': 745, '$lte': 951}})
st_window_hurdles = col.count_documents({'science_id': 'lalkitab_strategist', 'id': {'$gte': 952, '$lte': 975}})
st_peak = col.count_documents({'science_id': 'lalkitab_strategist', 'id': {'$gte': 976, '$lte': 1027}})
st_patch = col.count_documents({'science_id': 'lalkitab_strategist', 'id': {'$gte': 1126, '$lte': 1137}})

print("=== LK REMEDIES (jyotish_lk_remedies) ===")
print(f"Total: {lk} | Approved: {lk_approved}")
print()
print("=== STRATEGIST (lalkitab_strategist) ===")
print(f"Total: {st} | Approved: {st_approved} | PHR: {st_phr}")
print(f"  Surrogates    (651-675): {st_surrogates}  [expected 25]")
print(f"  Battlefield   (701-744): {st_battlefield}  [expected 44]")
print(f"  Siege Ops     (745-951): {st_siege}  [expected 207]")
print(f"  Window+Hurdle (952-975): {st_window_hurdles}  [expected 24]")
print(f"  Peak+Exit+GH  (976-1027): {st_peak}  [expected 51]")
print(f"  Salvage Patch (1126-1137): {st_patch}  [expected 12]")
print()
print(f"GRAND TOTAL (both science_ids): {lk + st}")
