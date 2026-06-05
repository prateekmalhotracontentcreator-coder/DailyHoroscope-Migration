============================================================
Longevity Unnatural -- Retroactive Positional Conflict Dedup
Method: Full MongoDB export (excludes batch longevity_unnatural_v1)
Run: 20260603_040546
============================================================

--- STEP 1/3: Export MongoDB → /tmp/mongo_existing_rules_dedup ---
Cleared stale export directory: /tmp/mongo_existing_rules_dedup
Traceback (most recent call last):
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/srv_resolver.py", line 108, in _resolve_uri
    results = _resolve(
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/srv_resolver.py", line 53, in _resolve
    return resolver.resolve(*args, **kwargs)
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/dns/resolver.py", line 1564, in resolve
    return get_default_resolver().resolve(
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/dns/resolver.py", line 1301, in resolve
    resolution = _Resolution(
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/dns/resolver.py", line 651, in __init__
    qname = dns.name.from_text(qname, None)
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/dns/name.py", line 1047, in from_text
    raise EmptyLabel
dns.name.EmptyLabel: A DNS label is empty.

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/apple/DailyHoroscope-Migration/backend/scripts/export_mongo_for_dedup.py", line 140, in <module>
    main()
  File "/Users/apple/DailyHoroscope-Migration/backend/scripts/export_mongo_for_dedup.py", line 75, in main
    client = MongoClient(args.mongo_url, serverSelectionTimeoutMS=15000)
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/mongo_client.py", line 891, in __init__
    self._get_topology()  # type: ignore[unused-coroutine]
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/mongo_client.py", line 1758, in _get_topology
    self._resolve_srv()
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/mongo_client.py", line 910, in _resolve_srv
    res = uri_parser._parse_srv(
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/uri_parser.py", line 168, in _parse_srv
    nodes = dns_resolver.get_hosts()
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/srv_resolver.py", line 148, in get_hosts
    _, nodes = self._get_srv_response_and_hosts(True)
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/srv_resolver.py", line 122, in _get_srv_response_and_hosts
    results = self._resolve_uri(encapsulate_errors)
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/srv_resolver.py", line 116, in _resolve_uri
    raise ConfigurationError(str(exc)) from exc
pymongo.errors.ConfigurationError: A DNS label is empty.
