# System Design Prep — Round 1

## Format
You receive an existing system diagram (Klaviyo architecture). You must:
1. Critique it — find flaws, bottlenecks, failure modes
2. State assumptions explicitly
3. Gather requirements (throughput, latency, durability, consistency)
4. Propose improvements with trade-offs

## Framework: RADIO
1. **R**equirements — Clarify functional + non-functional
2. **A**rchitecture — Walk the diagram, trace a request end-to-end
3. **D**esign deep-dive — Zoom into the weakest component
4. **I**ssues — Name failure modes, bottlenecks, scaling limits
5. **O**ptimizations — Propose changes with trade-offs

## Key Topics

### Redis Caching
- **Strategies:** TTL-based expiry, write-through (write DB + cache), write-behind (write cache, async DB), cache-aside (read from cache, miss → DB → populate cache)
- **What to cache:** Hot API keys/tokens, rate limit counters, frequently read config, session data, computed aggregates
- **What NOT to cache:** Frequently mutating user state, large blobs, data with strict consistency requirements
- **Failure scenarios:**
  - **Cache stampede / thundering herd:** Many requests hit expired key simultaneously → use lock-based cache rebuild or staggered TTLs
  - **Cache penetration:** Requests for non-existent keys always hit DB → use bloom filter or cache null results with short TTL
  - **Cache avalanche:** Many keys expire at once → randomize TTLs
  - **Redis single point of failure:** Redis Sentinel or Redis Cluster for HA
  - **Memory pressure:** Set maxmemory policy (allkeys-lru), monitor evictions

### Database Selection by Access Pattern
| Access Pattern | Best Choice | Why |
|---|---|---|
| High-write event ingestion | Clickhouse / Kafka + consumer | Column-oriented, append-optimized |
| Key-value lookups (API keys, sessions) | Redis / DynamoDB | Sub-ms reads, simple access |
| Relational data (accounts, apps) | PostgreSQL / MySQL | ACID, joins, constraints |
| Document storage (webhook configs) | DocumentDB / MongoDB | Flexible schema, nested data |
| Time-series analytics | Clickhouse / TimescaleDB | Efficient range queries, aggregation |
| Full-text search | Elasticsearch / OpenSearch | Inverted index, relevance scoring |

### Scaling Mechanisms
- **Horizontal scaling:** Celery workers behind RabbitMQ/Kafka, stateless API servers behind LB
- **Kafka partitioning:** Partition by tenant ID for ordered processing per-tenant, consumer groups for parallel processing
- **Read replicas:** Route analytics/reporting queries to replicas, keep writes on primary
- **Connection pooling:** PgBouncer for PostgreSQL, connection limits per service
- **Sharding:** By tenant/account ID for multi-tenant SaaS

### Queueing Deep Dive
| System | When to Use | Trade-offs |
|---|---|---|
| Celery + RabbitMQ | Task execution, retries, priority queues | Simple but limited throughput at extreme scale |
| Kafka | Event streaming, high-throughput ordered logs | Complex but durable, replayable |
| Apache Pulsar | Multi-tenant messaging, tiered storage | Newer, less ecosystem but flexible |
| Redis Pub/Sub | Lightweight real-time notifications | No persistence, at-most-once |

### Observability
- **Metrics:** p50/p95/p99 latency, queue depth, error rates, cache hit ratio, DB connection pool utilization
- **Distributed tracing:** Trace request through API → queue → worker → DB (Jaeger/Datadog)
- **Alerting:** Alert on queue depth growth (backpressure), error rate spikes, latency degradation, cache eviction rate
- **Dashboards:** Per-service health, API endpoint latency heatmap, consumer lag

### Failure Handling
- **DB outage:** Failover to read replica (promote), circuit breaker on writes, serve stale cache
- **Webhook server overload:** Rate limiting per-tenant, backpressure via queue depth limits, circuit breaker pattern
- **Scheduled maintenance:** Graceful drain (stop accepting new work, finish in-flight), blue-green deployment, feature flags
- **Retry strategy:** Exponential backoff + jitter, dead letter queue after N retries, idempotency keys

---

## Mock Scenarios

### Mock 1: Flawed Webhook Dispatcher
See [mock-1-webhook-dispatcher.md](./mock-1-webhook-dispatcher.md)

### Mock 2: Overloaded API Analytics Pipeline
See [mock-2-api-analytics.md](./mock-2-api-analytics.md)
