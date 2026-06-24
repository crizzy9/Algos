# Answer Key — Mock 2: Email Campaign API

## Clarifying Questions to Ask First
- Is this a REST API behind a framework (Django/FastAPI) or standalone?
- Multi-tenant? Can one API key see another's campaigns?
- What's the max recipient list size? (10? 10M?)
- Do we need to handle HTML sanitization in templates?
- Is there a send rate limit from our email provider?
- How do we handle bounces/complaints?

---

## Issues Found (Priority Order)

### CRITICAL — Security
1. **API key hardcoded in source** — `API_KEY = "sk_live_klaviyo_abc123def456"` is in the code. Must come from env var / secrets manager. This would be committed to git.
2. **SQL Injection in EVERY query** — String formatting (`%s`) everywhere. All of `create_campaign`, `get_campaign`, `add_recipients`, `search_campaigns`, `delete_campaign`, `schedule_campaign`, `render_template`, etc. Use parameterized queries.
3. **Template injection in render_template** — Naive `str.replace()` for `{{var}}` substitution. Malicious data values could inject HTML/JS (XSS). Use a proper template engine (Jinja2) with auto-escaping.
4. **search_campaigns SQL injection via LIKE** — `'%%%s%%' % query` is doubly dangerous. Parameterized query with `LIKE ?` and `f"%{query}%"` passed as param.
5. **authenticate() is plaintext comparison** — API key compared directly. Should use constant-time comparison (`hmac.compare_digest`) to prevent timing attacks.
6. **No authorization / multi-tenancy** — Any valid key can see/modify ANY campaign. Need to scope queries to the key's owner.

### CRITICAL — Correctness
7. **get_campaign_stats: ZeroDivisionError** — `opened / total * 100` crashes when `total == 0`. Need `total > 0` guard.
8. **send_campaign has no idempotency** — Calling it twice sends the campaign twice. Need to check `status != 'sent'` first.
9. **send_campaign doesn't actually send email** — Just prints. But more importantly, it updates DB row-by-row in a loop. One failure mid-loop = partial send with no way to resume.
10. **process_scheduled uses internal API_KEY** — Hardcoded key in a scheduler function. Should use service-level auth, not user API keys.
11. **Datetime comparison as strings** — `scheduled_for <= now` compares string lexicographically. Works for ISO format but fragile. Use proper datetime column type.

### HIGH — Scalability
12. **list_campaigns N+1 query** — Fetches all campaigns, then calls `get_campaign()` for each one (re-querying the DB). Just return the data from the initial query.
13. **add_recipients: row-by-row inserts** — Loop of individual INSERT statements. For 1M recipients this is catastrophically slow. Use `executemany()` or bulk insert.
14. **No pagination anywhere** — `list_campaigns`, `get_recipients` fetch ALL rows. Need LIMIT/OFFSET or cursor-based pagination.
15. **Global DB connection** — Not thread-safe. Use connection pool.
16. **send_campaign is synchronous** — Blocks while iterating all recipients. Should be queued as a background job.

### MEDIUM — Code Quality
17. **No type hints** — Functions return dicts with no structure. Use dataclasses or TypedDict.
18. **Magic column indices** — `row[0]`, `row[1]`, etc. Use `conn.row_factory = sqlite3.Row` for named access.
19. **No logging** — No visibility into send operations, failures, or timing.
20. **No input validation** — No check for empty name/subject, valid email format, valid scheduled_for format.
21. **No error handling on send_campaign** — If DB update fails mid-loop, partial state with no recovery.
22. **delete_campaign non-atomic** — Two separate DELETE statements. If the second fails, orphaned recipients remain. Use a transaction.

### LOW — Data Model
23. **No indexes** — `recipients.campaign_id`, `events.user_email` need indexes.
24. **`sent`, `opened`, `clicked` as INTEGER flags** — Should be timestamps so you know WHEN, not just IF.
25. **No `updated_at` column** — Can't audit when campaigns were modified.
