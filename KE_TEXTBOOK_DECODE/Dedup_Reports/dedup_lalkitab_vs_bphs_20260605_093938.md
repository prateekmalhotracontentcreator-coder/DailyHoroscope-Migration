============================================================
Lal Kitab Ch19-29 -- Retroactive Positional Conflict Dedup
Batch:  lalkitab_all_v2_20260605
Run:    20260605_093938
============================================================

--- STEP 0: Export LK rules from MongoDB → /tmp/lalkitab_rules_for_dedup ---
Traceback (most recent call last):
  File "<stdin>", line 21, in <module>
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/cursor.py", line 1289, in __next__
    return self.next()
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/cursor.py", line 1265, in next
    if len(self._data) or self._refresh():
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/cursor.py", line 1213, in _refresh
    self._send_message(q)
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/cursor.py", line 1108, in _send_message
    response = client._run_operation(
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/_csot.py", line 125, in csot_wrapper
    return func(self, *args, **kwargs)
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/mongo_client.py", line 1938, in _run_operation
    return self._retryable_read(
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/mongo_client.py", line 2048, in _retryable_read
    return self._retry_internal(
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/_csot.py", line 125, in csot_wrapper
    return func(self, *args, **kwargs)
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/mongo_client.py", line 2003, in _retry_internal
    return _ClientConnectionRetryable(
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/mongo_client.py", line 2763, in run
    return self._read() if self._is_read else self._write()
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/mongo_client.py", line 2908, in _read
    self._server = self._get_server()
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/mongo_client.py", line 2856, in _get_server
    return self._client._select_server(
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/mongo_client.py", line 1833, in _select_server
    server = topology.select_server(
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/topology.py", line 428, in select_server
    server = self._select_server(
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/topology.py", line 402, in _select_server
    servers = self.select_servers(
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/topology.py", line 298, in select_servers
    server_descriptions = self._select_servers_loop(
  File "/Users/apple/Library/Python/3.9/lib/python/site-packages/pymongo/synchronous/topology.py", line 359, in _select_servers_loop
    raise ServerSelectionTimeoutError(
pymongo.errors.ServerSelectionTimeoutError: ac-sctwdlf-shard-00-02.bqtc8l9.mongodb.net:27017: timed out (configured timeouts: socketTimeoutMS: 20000.0ms, connectTimeoutMS: 20000.0ms), Timeout: 20.0s, Topology Description: <TopologyDescription id: 6a224c03645f452e50ecccca, topology_type: ReplicaSetNoPrimary, servers: [<ServerDescription ('ac-sctwdlf-shard-00-00.bqtc8l9.mongodb.net', 27017) server_type: Unknown, rtt: None>, <ServerDescription ('ac-sctwdlf-shard-00-01.bqtc8l9.mongodb.net', 27017) server_type: Unknown, rtt: None>, <ServerDescription ('ac-sctwdlf-shard-00-02.bqtc8l9.mongodb.net', 27017) server_type: Unknown, rtt: None, error=NetworkTimeout('ac-sctwdlf-shard-00-02.bqtc8l9.mongodb.net:27017: timed out (configured timeouts: socketTimeoutMS: 20000.0ms, connectTimeoutMS: 20000.0ms)')>]>
