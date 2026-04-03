# System Design Crash Course — 30 Min Dense Review

## The RADIO Framework (Your Skeleton for Every Answer)

**R**equirements → **A**rchitecture walkthrough → **D**eep-dive weakest component → **I**ssues/failure modes → **O**ptimizations with trade-offs

First 2-3 minutes: ask clarifying questions. "What's the throughput? What's the SLA? Is this customer-facing or internal? What's the consistency requirement?"

---

## The 6 Pillars

### 1. DATA INGESTION — How Events Get In

**The pattern at Klaviyo:** 160K+ events/sec. Emails opened, links clicked, profiles updated.

**Bad:** Synchronous writes to DB on the hot path. Every API request blocks on INSERT.

**Good:** Fire-and-forget to Kafka (async, non-blocking). Consumers process at their own pace.

**Key talking points:**
- Kafka gives you **durability** (replication factor 3), **replay** (re-process from any offset), and **ordering per partition**
- Partition by tenant_id → ordered within one customer, parallel across customers
- Consumer groups for horizontal scaling — add consumers to scale reads
- If Kafka itself is slow → check consumer lag, auto-scale consumer group, events are safe (7-day retention)

**Your Intuit anchor:** "At Intuit, I built a Kafka event consumer pipeline for targeted offers. We partitioned by user segment and processed at ~50K events/sec. Same pattern applies here at 3x scale."

---

### 2. DATABASE SELECTION BY ACCESS PATTERN

| Access Pattern | Pick | Why |
|---|---|---|
| High-write event stream (append-only) | **Clickhouse** | Column-oriented, 10:1 compression, vectorized aggregation |
| Key-value lookups (API keys, sessions, tokens) | **Redis** | Sub-ms reads, perfect for hot lookups |
| Relational data (accounts, apps, webhook configs) | **PostgreSQL/MySQL** | ACID, joins, foreign keys, constraints |
| Flexible/nested documents (webhook payloads) | **DocumentDB/MongoDB** | Schema-flexible, nested data |
| Full-text search | **Elasticsearch/OpenSearch** | Inverted index, relevance scoring |
| Time-series analytics | **Clickhouse or TimescaleDB** | Range queries + aggregation optimized |

**When they ask "why not just PostgreSQL for everything?":**
"PostgreSQL is great for relational data but at 160K events/sec, a single Postgres writer will choke. Column stores like Clickhouse are purpose-built for append-heavy analytical workloads — 10:1 compression ratio and vectorized query execution."

---

### 3. REDIS CACHING — Know This Cold

**Caching strategies:**
- **Cache-aside** (most common): Read cache → miss → read DB → populate cache. You control what gets cached.
- **Write-through**: Write to DB + cache simultaneously. Consistent but adds write latency.
- **Write-behind**: Write to cache, async flush to DB. Fast writes but risk data loss.

**What to cache:** OAuth tokens (5min TTL), rate limit counters, hot config, computed aggregates, session data.

**What NOT to cache:** Frequently mutating user state, large blobs, anything needing strict consistency.

**The 4 failure scenarios:**

| Failure | What Happens | Fix |
|---|---|---|
| **Cache Stampede** | Key expires, 1000 requests simultaneously hit DB | Mutex lock on cache rebuild OR staggered TTLs |
| **Cache Penetration** | Requests for keys that don't exist always hit DB | Bloom filter OR cache null with short TTL |
| **Cache Avalanche** | Many keys expire at once → DB flood | Randomize TTLs (base + random jitter) |
| **Redis SPOF** | Redis down = no rate limiting + no cache → DB crushed | Redis Sentinel (HA) or Redis Cluster |

**Memory pressure:** Set `maxmemory-policy allkeys-lru`. Monitor eviction rate.

---

### 4. SCALING MECHANISMS

**Horizontal scaling:**
- Stateless API servers behind a load balancer → add instances
- Celery workers behind RabbitMQ/Kafka → add workers
- Kafka consumers in a consumer group → add consumers (up to partition count)

**Vertical scaling (when to mention):**
- "Before adding complexity with sharding, can we just use a bigger DB instance?" Shows pragmatism.

**Sharding:** By tenant_id for multi-tenant SaaS. Cross-shard queries are expensive — design to avoid them.

**Read replicas:** Route analytics/dashboard queries to replicas. Writes to primary only. Replication lag is a trade-off.

**Connection pooling:** PgBouncer for PostgreSQL. Without it, each Django process holds a connection → exhaustion at scale.

---

### 5. QUEUING

| System | Use When | Key Trade-off |
|---|---|---|
| **Kafka** | High-throughput event streaming, need replay, ordering matters | Complex ops, overkill for simple task queues |
| **Celery + RabbitMQ** | Task execution, retries, priority queues, delayed tasks | Simpler but no replay, lower throughput ceiling |
| **Apache Pulsar** | Multi-tenant messaging, tiered storage, geo-replication | Newer ecosystem, less tooling |
| **Redis Pub/Sub** | Lightweight real-time notifications | No persistence, at-most-once delivery |

**Retry pattern:**
- Exponential backoff + jitter: `delay = base * 2^attempt + random(0, base)`
- Retry topics: 1min → 5min → 30min → 4hr → **Dead Letter Queue**
- DLQ alerts → human reviews failures. Never silently drop events.

---

### 6. OBSERVABILITY & FAILURE HANDLING

**Metrics:** p50/p95/p99 latency, error rate, queue depth/consumer lag, cache hit ratio, DB connection pool utilization

**Failure handling:**
- **DB outage:** Failover to read replica (promote), circuit breaker on writes, serve stale cache
- **Webhook overload:** Per-tenant rate limiting, backpressure via queue depth limits, circuit breaker per endpoint
- **Maintenance:** Graceful drain (stop accepting new, finish in-flight), blue-green deployment

**Circuit breaker:** Fails N times → OPEN (stop calling) → cooldown → HALF-OPEN (try one) → success → CLOSED (resume)

---

## Back-of-Envelope Math Template

```
160,000 events/sec × 86,400 sec/day = ~13.8B events/day
Event size: ~500 bytes
Daily raw: 13.8B × 500B = ~6.9 TB/day
With compression (10:1): ~690 GB/day
90-day retention: ~62 TB
```

---

## The "Critique" Checklist (Run on Every Diagram)

1. Any **synchronous** calls on the hot path? → Make async
2. **Single points of failure?** → Add redundancy/HA
3. **Plaintext secrets?** → Encrypt at rest, use KMS/secrets manager
4. **No retry logic?** → Add exponential backoff + DLQ
5. **Dashboard hitting the write DB?** → Read replica or separate analytics store
6. **No caching?** → Add Redis with appropriate strategy
7. **No rate limiting?** → Add per-tenant rate limiting in Redis
8. **No observability?** → Metrics, tracing, alerting
9. **No partitioning on large tables?** → Time-based partitioning, TTL
10. **No data retention?** → Define TTL, cold storage archival

---

## Golden Rules

1. **Think out loud** — silence is death
2. **Ask before diving** — 2-3 clarifying questions minimum
3. **State trade-offs for every decision** — "We could do X which gives us Y but costs us Z"
4. **Anchor to your experience** — every answer includes "At Intuit, I..."
