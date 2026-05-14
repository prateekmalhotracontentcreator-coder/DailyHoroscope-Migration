import sys
from pymongo import MongoClient

client = MongoClient(sys.argv[1])
col = client['horoscope_db']['knowledge_rules']

# Sample first 5 and last 5 of 1028-1125
print("=== IDs 1028-1125 -- first 5 ===")
for r in col.find({'science_id': 'lalkitab_strategist', 'id': {'$gte': 1028, '$lte': 1032}},
                  {'id':1,'mission_name':1,'strategy':1,'segment':1,'approval_status':1,'_id':0}).sort('id',1):
    print(f"  {r['id']}: {r.get('mission_name') or r.get('strategy','?')} [{r.get('segment','?')}] -- {r.get('approval_status')}")

print("\n=== IDs 1028-1125 -- last 5 ===")
for r in col.find({'science_id': 'lalkitab_strategist', 'id': {'$gte': 1121, '$lte': 1125}},
                  {'id':1,'mission_name':1,'strategy':1,'segment':1,'approval_status':1,'_id':0}).sort('id',1):
    print(f"  {r['id']}: {r.get('mission_name') or r.get('strategy','?')} [{r.get('segment','?')}] -- {r.get('approval_status')}")

print("\n=== IDs 1201-1225 -- all 25 ===")
for r in col.find({'science_id': 'lalkitab_strategist', 'id': {'$gte': 1201, '$lte': 1225}},
                  {'id':1,'mission_name':1,'strategy':1,'segment':1,'surrogate_type':1,'industry':1,'approval_status':1,'_id':0}).sort('id',1):
    name = r.get('mission_name') or r.get('strategy','?')
    extra = r.get('surrogate_type') or r.get('segment','')
    print(f"  {r['id']}: {name} [{extra}] -- {r.get('approval_status')}")

print("\n=== ID 817 -- neighbors to understand the gap ===")
for r in col.find({'science_id': 'lalkitab_strategist', 'id': {'$gte': 815, '$lte': 819}},
                  {'id':1,'mission_name':1,'strategy':1,'_id':0}).sort('id',1):
    print(f"  {r['id']}: {r.get('mission_name') or r.get('strategy','?')}")
