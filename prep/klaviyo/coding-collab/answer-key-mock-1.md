# Answer Key — Mock 1: Webhook Delivery Service

## Clarifying Questions to Ask First
- What's the expected volume? (webhooks/sec)
- What's our SLA for delivery latency?
- Do we need exactly-once delivery or at-least-once?
- How should we handle endpoints that are permanently down?
- Is there a max payload size?
- Do merchants configure webhooks via API or UI?

---

## Issues Found (Priority Order)

### CRITICAL — Security
1. **SQL Injection everywhere** — String formatting (`%s`) into SQL. Use parameterized queries: `db.execute("... VALUES (?, ?, ?, ?)", (url, secret, ...))`
2. **Secrets returned in get_webhooks()** — `wh["secret"]` is exposed in the response. Never return secrets in API responses.
3. **No HMAC signature on webhook payloads** — The `secret` is stored but never used. Webhooks should be signed with HMAC-SHA256 so merchants can verify authenticity.
4. **No URL validation** — `register_webhook` accepts any string as URL. Could be internal IPs (SSRF), `file://` paths, etc.

### CRITICAL — Correctness
5. **`time.sleep(3600)` in handle_abandoned_cart** — Blocks the entire process for 1 hour. This should be a scheduled job / task queue (Celery, RabbitMQ).
6. **`events` field checked with `in` on a JSON string** — `event_type in wh["events"]` does string containment, not list membership. `"cart"` would match `"abandoned_cart"`. Need `json.loads(wh["events"])` first.
7. **Bare `except:` clauses** — Swallows all errors including KeyboardInterrupt, SystemExit. Use `except Exception as e:` and log the error.
8. **retry_failed has no retry limit** — Will retry forever. Need exponential backoff + max retry count, then mark as `dead_letter`.

### HIGH — Scalability
9. **Global `db` connection** — Single connection, not thread-safe. Use connection pool or create connection per request.
10. **Synchronous webhook delivery** — `send_webhook` calls each endpoint sequentially. One slow endpoint blocks all others. Should be async (asyncio/threading/queue).
11. **No pagination on get_deliveries** — `fetchall()` loads everything into memory. Add LIMIT/OFFSET.
12. **30s timeout on requests.post** — Way too long. Use 5-10s for initial timeout, queue for retry.

### MEDIUM — Code Quality
13. **No type hints** — Add return types, parameter types.
14. **No logging** — `print()` or nothing. Need structured logging (delivery attempts, failures, retries).
15. **No webhook deactivation logic** — If an endpoint fails repeatedly, it should be auto-disabled.
16. **Hardcoded values** — Timeout, retry logic should be configurable.
17. **`check_health` uses GET** — Some endpoints may not support GET. Use HEAD or a dedicated health path.
18. **No idempotency key** — Retries could cause duplicate delivery. Include a delivery ID in payload so merchants can dedupe.

### LOW — Data Model
19. **`events` stored as JSON string in TEXT column** — Should be a separate webhook_events join table for proper querying.
20. **No index on deliveries.webhook_id** — Queries will full-scan as data grows.
21. **`created_at` as TEXT** — Should be a proper timestamp type.
