# Answer Key — Mock 3: Event Ingestion Pipeline

## Clarifying Questions to Ask First
- What's our event throughput? (Klaviyo processes billions — are we talking 1K/sec? 100K/sec?)
- Are events ordered? Do we need to process them in order?
- What's the consistency requirement? Eventual OK or strict?
- How many segments per account? How often do rules change?
- What happens if we lose an event? Is at-least-once acceptable?
- Are profiles cross-tenant or per-account?

---

## Issues Found (Priority Order)

### CRITICAL — Security
1. **SQL Injection in EVERY function** — String formatting into SQL everywhere. `ingest_event`, `evaluate_segments`, `get_profile`, `get_events`, `update_profile`, `create_segment`, `get_segment_members`, `cleanup_old_events` — all vulnerable.
2. **update_profile allows arbitrary column injection** — `"UPDATE profiles SET %s = '%s'"` where `key` comes from user input. Attacker can set `email = 'admin@evil.com'` or modify any column. Must whitelist allowed fields.
3. **export_segment: SSRF vulnerability** — `requests.post(webhook_url, ...)` with no URL validation. Attacker could hit internal services.
4. **No authentication at all** — Every function is publicly callable. No API key, no auth check.

### CRITICAL — Correctness
5. **compute_metrics: ZeroDivisionError** — `revenue / purchases` crashes when `purchases == 0`.
6. **Bare `except:` in ingest_event** — Swallows ALL exceptions. A `KeyError` on `properties["total"]` silently fails. You'd never know events are being dropped.
7. **Global mutable counters** — `events_processed` and `errors` are global vars. Not thread-safe, lost on restart, useless for monitoring. Use metrics system (Prometheus, StatsD).
8. **async_ingest is fire-and-forget** — Thread is started but never joined. No error handling, no result, no acknowledgment. Caller gets `{"status": "processing"}` even if everything fails.
9. **sqlite3 not thread-safe** — `async_ingest` spawns a thread that uses the global `db` connection. SQLite doesn't support concurrent writes from different threads. Will corrupt data.
10. **bulk_ingest returns wrong count** — Returns `len(events)` even if some failed. Should count actual successes.
11. **evaluate_segments: delete-then-insert race** — DELETE + INSERT is not atomic. Concurrent evaluation could drop a user from a segment briefly. Use UPSERT or transaction.

### HIGH — Scalability
12. **evaluate_segments runs for EVERY event** — Loads ALL segments, evaluates ALL rules for the user. At Klaviyo scale (billions of events, thousands of segments), this is catastrophic. Should be async, batched, or incremental.
13. **get_segment_members N+1 query** — Fetches all member rows, then calls `get_profile()` for each one individually. Use a JOIN.
14. **No indexes** — `events.user_email`, `events.event_type`, `segment_members.segment_id`, `segment_members.email` all need indexes.
15. **get_events loads up to 100 events with full payloads** — Properties could be large JSON. Consider separate event detail endpoint.
16. **cleanup_old_events: mass DELETE** — Deleting millions of rows in one statement locks the DB. Batch the deletes.
17. **Single SQLite database** — Won't scale past a single machine. Events should go to a queue (Kafka/RabbitMQ) → worker → time-series store (ClickHouse).

### MEDIUM — Code Quality
18. **No type hints anywhere** — Functions accept and return untyped dicts.
19. **Magic column indices** — `profile[3]`, `profile[5]`, `seg[2]` everywhere. Use `Row` factory or ORM.
20. **`check_rules` tightly coupled to tuple indices** — `profile[5]` for revenue, `profile[4]` for last_active. Breaks if schema changes.
21. **No logging** — Zero observability. No way to debug dropped events or segment evaluation failures.
22. **No input validation** — No email format check, no event_type whitelist, no properties schema validation.
23. **`time.time()` used directly** — Non-deterministic, hard to test. Should accept timestamp as parameter.

### LOW — Architecture
24. **Everything in one module** — Event ingestion, profile management, segmentation, metrics, and export all in one file. Should be separate services/modules.
25. **No dead letter queue** — Failed events just increment a counter and disappear.
26. **No event schema versioning** — If properties format changes, old events break `compute_metrics`.
27. **export_segment is synchronous** — Could timeout on large segments. Should be async job.
