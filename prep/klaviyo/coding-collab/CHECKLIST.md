# Coding Collab — Universal Checklist

Run through this mentally on ANY code you're handed. Order = priority.

---

## 1. SECURITY (check first, mention first)

- [ ] **SQL Injection** — Any string formatting (`%s`, f-strings, `.format()`) in SQL? → Use parameterized queries (`?` placeholders)
- [ ] **Secrets in code** — API keys, passwords, tokens hardcoded? → Env vars / secrets manager
- [ ] **Secrets in responses** — Are signing keys, internal IDs, or tokens returned to callers?
- [ ] **Auth model** — Is auth per-function or centralized middleware? Is it constant-time (`hmac.compare_digest`)?
- [ ] **Multi-tenancy** — Can user A see/modify user B's data? Are queries scoped to the caller?
- [ ] **Input validation** — URLs validated (SSRF)? Emails validated? Fields whitelisted? HTML escaped (XSS)?
- [ ] **Template injection** — Naive string replacement (`str.replace`) for templates? → Use Jinja2 with auto-escaping

## 2. CORRECTNESS (bugs that cause incidents)

- [ ] **Division by zero** — Any division where denominator could be 0?
- [ ] **Bare `except:`** — Swallows KeyboardInterrupt, SystemExit. → `except Exception as e:` + log it
- [ ] **String vs list membership** — `x in some_string` vs `x in some_list` — are JSON strings being parsed before checking?
- [ ] **Idempotency** — Can calling the same function twice cause duplicate side effects? (double sends, double charges)
- [ ] **Partial failure** — If a loop crashes halfway, is state consistent? Can you resume?
- [ ] **Atomic operations** — Multiple writes that should be in a transaction but aren't?
- [ ] **Blocking calls** — Any `time.sleep()` or synchronous HTTP in a request path?
- [ ] **Off-by-one / edge cases** — Empty lists, None values, first/last element handling

## 3. SCALABILITY (will it break at volume)

- [ ] **N+1 queries** — Loop that queries the DB per item? → Use JOINs or batch queries
- [ ] **No pagination** — `fetchall()` or unbounded `SELECT *`? → Add LIMIT/OFFSET or cursor pagination
- [ ] **Row-by-row inserts** — Loop of individual INSERTs? → `executemany()` or bulk insert
- [ ] **Missing indexes** — Columns used in WHERE/JOIN/ORDER BY without indexes?
- [ ] **Synchronous fan-out** — Sending to N endpoints/recipients sequentially? → Async, threading, or task queue
- [ ] **Global DB connection** — Single connection shared across threads? → Connection pool
- [ ] **Unbounded retries** — Retry loops with no max count or backoff? → Exponential backoff + dead letter

## 4. DATA MODEL (design-level issues)

- [ ] **JSON in text columns** — Lists/relations stored as JSON strings? → Normalize into join tables
- [ ] **Timestamps as strings** — Datetime stored/compared as text? → Use proper timestamp types
- [ ] **Flags vs timestamps** — Boolean `sent=1` when you also need to know WHEN? → Store the timestamp
- [ ] **No `created_at` / `updated_at`** — Can you audit when records changed?
- [ ] **No soft delete** — Hard DELETE loses history. Consider `deleted_at` flag

## 5. CODE QUALITY (mention last, fix if time)

- [ ] **No type hints** — Parameters and return types untyped
- [ ] **Magic indices** — `row[0]`, `row[3]` instead of named access (`row["email"]`)
- [ ] **God function** — One function doing 5 things? → Split into focused helpers
- [ ] **No logging** — Zero observability into failures, latency, throughput
- [ ] **Hardcoded config** — Timeouts, URLs, limits as magic numbers? → Config / constants
- [ ] **No docstrings on non-obvious functions**

## 6. RESILIENCE (production-readiness)

- [ ] **No timeout on HTTP calls** — `requests.post()` with no timeout hangs forever
- [ ] **No circuit breaker** — Keeps hammering a dead endpoint? → Auto-disable after N failures
- [ ] **Fire-and-forget threads** — `threading.Thread` started but never joined, no error handling
- [ ] **No dead letter / DLQ** — Failed items just disappear? → Queue them for inspection
- [ ] **No idempotency key** — Retries cause duplicates for downstream consumers

---

## How to Use During the Interview

**First 5 minutes:** Read the code top to bottom. Don't speak yet.

**Next 5 minutes:** Say out loud:
> "Before I start changing anything, let me call out the issues I see..."

Walk through Security → Correctness → Scalability in that order. This shows you triage by severity.

**Remaining 50 minutes:** Fix issues while narrating:
> "I'm changing this because..." / "The trade-off here is..." / "In production I'd also want..."

**Power phrases Victor wants to hear:**
- "This is a SQL injection vector — I'd use parameterized queries"
- "This won't scale because it's O(N) per request — I'd batch this"
- "This isn't idempotent — if it runs twice we'd double-send"
- "This blocks the request path — I'd move it to a task queue"
- "There's no observability here — I'd add structured logging"
