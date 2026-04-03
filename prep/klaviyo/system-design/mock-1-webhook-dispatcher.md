# Mock 1: Flawed Webhook Dispatcher

## Context
Klaviyo allows customers to configure webhook endpoints that receive real-time notifications when events occur (email opened, link clicked, profile updated, etc.). This is the current system:

## System Diagram (The "Flawed" Version)

```
                        ┌──────────────┐
                        │   Klaviyo    │
                        │  Event Bus   │
                        │  (internal)  │
                        └──────┬───────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Webhook Service    │
                    │   (Django app)       │
                    │                      │
                    │ • Receives events    │
                    │ • Looks up configs   │  ← Single PostgreSQL
                    │ • Sends HTTP POST    │    (webhook_configs table)
                    │   SYNCHRONOUSLY      │
                    │ • Stores API keys    │  ← Plaintext in DB column
                    │   in webhook_configs │
                    │ • No retry logic     │
                    │ • Single process     │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │   Single Redis       │
                    │   (rate limiting     │
                    │    + config cache)   │
                    │   • No persistence   │
                    │   • No sentinel      │
                    │   • 1 instance       │
                    └──────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                 ▼
        ┌──────────┐   ┌──────────┐      ┌──────────┐
        │Customer A│   │Customer B│      │Customer C│
        │ Endpoint │   │ Endpoint │      │ Endpoint │
        │ (fast)   │   │ (slow)   │      │ (down)   │
        └──────────┘   └──────────┘      └──────────┘
```

## Known Issues to Find

### Critical
1. **Synchronous webhook delivery** — A slow/down customer endpoint blocks the entire service. If Customer C is down, all webhooks queue behind it.
2. **API keys stored in plaintext** — The `webhook_configs` table has an `api_key VARCHAR(255)` column with raw keys. SQL dump = full compromise.
3. **No retry logic** — If a delivery fails, the event is lost forever. No dead letter queue, no exponential backoff.
4. **Single Redis instance** — No Sentinel/Cluster. Redis crash = no rate limiting + stale cache reads + potential thundering herd on PostgreSQL.

### High
5. **Single PostgreSQL** — No read replicas. Config lookups and webhook delivery analytics compete for the same DB.
6. **No webhook signature verification** — Customers can't verify that webhooks actually came from Klaviyo (no HMAC signing).
7. **No per-tenant rate limiting** — One noisy tenant generating millions of events can starve others.
8. **No observability** — No metrics on delivery success rate, latency percentiles, or queue depth.

### Medium
9. **No idempotency** — Duplicate events can be delivered if the system retries at any layer.
10. **No circuit breaker** — Keeps hammering a down endpoint instead of backing off.
11. **Config cache has no invalidation strategy** — Stale configs served after customer updates their endpoint URL.
12. **No event ordering guarantees** — Events may arrive out of order at customer endpoints.

---

## Ideal Improved Architecture

```
                        ┌──────────────┐
                        │   Klaviyo    │
                        │  Event Bus   │
                        └──────┬───────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Webhook Router     │
                    │   (stateless)        │
                    │ • Validates event    │
                    │ • Looks up config    │──→ Redis Cluster (cache)
                    │ • Enqueues delivery  │         │
                    └──────────┬───────────┘    (miss → PostgreSQL
                               │                  primary + replica)
                               ▼
                    ┌──────────────────────┐
                    │   Kafka / RabbitMQ   │
                    │ • Partitioned by     │
                    │   tenant_id          │
                    │ • Retry topics       │
                    │   (1m, 5m, 30m, 4h)  │
                    │ • Dead letter topic  │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                 ▼
        ┌──────────┐   ┌──────────┐      ┌──────────┐
        │  Worker  │   │  Worker  │      │  Worker  │
        │  Pool 1  │   │  Pool 2  │      │  Pool N  │
        │(Celery)  │   │(Celery)  │      │(Celery)  │
        └─────┬────┘   └─────┬────┘      └─────┬────┘
              │              │                  │
              │    ┌─────────┴──────────┐       │
              │    │  Circuit Breaker   │       │
              │    │  (per endpoint)    │       │
              │    └─────────┬──────────┘       │
              ▼              ▼                  ▼
        ┌──────────┐   ┌──────────┐      ┌──────────┐
        │Customer A│   │Customer B│      │Customer C│
        │(HMAC sig)│   │(HMAC sig)│      │(HMAC sig)│
        └──────────┘   └──────────┘      └──────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Delivery Analytics  │
                    │  (Clickhouse)        │
                    │  • Success/fail rate │
                    │  • Latency p50/p99   │
                    │  • Per-tenant stats  │
                    └──────────────────────┘
```

### Key Improvements
1. **Async delivery** — Router enqueues, workers deliver. Slow endpoints don't block others.
2. **Kafka partitioning by tenant** — Ordered delivery per-tenant, parallel across tenants.
3. **Retry with exponential backoff** — Separate retry topics (1m, 5m, 30m, 4h) → DLQ after exhaustion.
4. **API keys encrypted at rest** — Use KMS-encrypted column or secrets manager reference, never plaintext.
5. **HMAC webhook signing** — Each delivery signed with customer's secret; customers verify authenticity.
6. **Redis Cluster** — HA caching, no single point of failure.
7. **Read replica** — Analytics queries go to replica, writes to primary.
8. **Circuit breaker per endpoint** — Stop hammering down endpoints, auto-recover when they come back.
9. **Per-tenant rate limiting** — Token bucket in Redis per tenant, configurable limits.
10. **Clickhouse for analytics** — Delivery metrics in a column store optimized for aggregation queries.
11. **Idempotency keys** — Each event gets a unique ID; customers can deduplicate.
12. **Observability** — Prometheus metrics + Grafana dashboards + PagerDuty alerts on DLQ growth / delivery failure spikes.

---

## Practice Questions the Interviewer Might Ask

1. "What happens if Kafka itself goes down?" → Kafka is designed for durability (replication factor 3, ISR). If the cluster is truly down, the router should buffer in-memory briefly and return 503. Alerting catches this fast.

2. "How do you handle a tenant generating 10M events/hour when others generate 1K?" → Per-tenant rate limiting at the router level. Excess events either queued with lower priority or rejected with 429. Separate Kafka partitions prevent noisy-neighbor at the worker level.

3. "Why not just use RabbitMQ instead of Kafka?" → Kafka gives us replay capability (re-deliver failed webhooks from any point in time), ordered delivery per partition, and better throughput at 160K+ events/sec. RabbitMQ is simpler but doesn't support replay.

4. "How do you monitor if webhooks are actually being received correctly by customers?" → Delivery receipts (log HTTP status code), customer-facing dashboard showing delivery status per event, and a "test webhook" endpoint so customers can verify their setup.
