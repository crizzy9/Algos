# Mock 2: Overloaded API Analytics Pipeline

## Context
Klaviyo's DevX team runs an API Analytics system that processes 160,000+ events per second. Every API call made by external developers and partners is logged for usage tracking, rate limiting, billing, and developer-facing dashboards. The current system is struggling.

## System Diagram (The "Flawed" Version)

```
        External Developers / Partners
        (OAuth2 API keys)
                    │
                    ▼
        ┌──────────────────────┐
        │   API Gateway        │
        │   (nginx + Django)   │
        │ • Auth + rate limit  │
        │ • Logs EVERY request │──→ PostgreSQL (api_events table)
        │   to DB directly     │    • Single writer
        │                      │    • 500M+ rows
        │ • In-memory counter  │    • No partitioning
        │   for rate limiting  │    • Full table scans
        │   (per-process, lost │      for dashboard queries
        │   on restart)        │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   Analytics Dashboard│
        │   (React app)        │
        │ • Queries PostgreSQL │
        │   directly           │
        │ • SELECT COUNT(*)    │
        │   GROUP BY endpoint  │
        │   WHERE timestamp >  │
        │   NOW() - '1 hour'   │
        │ • 30s refresh        │
        │ • No caching         │
        └──────────────────────┘
```

## Known Issues to Find

### Critical
1. **Synchronous DB writes on every API call** — At 160K events/sec, PostgreSQL is the bottleneck. Every API request blocks on an INSERT before returning the response. This adds latency to every external API call.
2. **In-memory rate limiting (per-process)** — Rate limits reset on deploy/restart. Multiple API gateway processes each track their own counters → a client can exceed limits by hitting different processes.
3. **Dashboard queries hit the write DB** — Full table scans with `COUNT(*) GROUP BY` on 500M+ rows compete with INSERT writes. This causes lock contention and query timeouts.

### High
4. **No partitioning on api_events** — 500M rows in a single table. No time-based partitioning, so old data can't be efficiently archived or dropped.
5. **No write buffering** — Events go directly to PostgreSQL instead of being buffered in a queue. A brief DB hiccup means API calls fail or queue in the application layer.
6. **30-second dashboard refresh with no caching** — Every refresh re-executes expensive aggregation queries. 100 developers viewing dashboards = 100 identical queries every 30s.
7. **No sampling or aggregation** — Every single request is logged with full detail. At 160K/sec that's ~14B rows/day.

### Medium
8. **No data retention policy** — Table grows unbounded. No TTL, no archival to cold storage.
9. **No pre-aggregated metrics** — Dashboard always computes from raw events instead of pre-computed rollups (per-minute, per-hour counts by endpoint).
10. **OAuth tokens validated on every request** — No token cache; every request hits the auth DB.
11. **No anomaly detection** — Can't detect abuse patterns (sudden spike from one API key) without post-hoc analysis.

---

## Ideal Improved Architecture

```
        External Developers / Partners
                    │
                    ▼
        ┌──────────────────────┐
        │   API Gateway        │
        │   (nginx + Django)   │
        │ • Auth via Redis     │──→ Redis Cluster
        │   cached tokens      │    • Rate limit counters
        │ • Rate limit via     │      (sliding window)
        │   Redis sliding      │    • Token cache (5min TTL)
        │   window             │
        │ • Fire-and-forget    │
        │   event to Kafka     │
        └──────────┬───────────┘
                   │ (async, non-blocking)
                   ▼
        ┌──────────────────────┐
        │   Kafka              │
        │ • Topic: api_events  │
        │ • Partitioned by     │
        │   api_key hash       │
        │ • Retention: 7 days  │
        │ • Replication: 3     │
        └──────────┬───────────┘
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
    ┌──────────┐ ┌─────┐ ┌──────────────┐
    │Raw Event │ │Agg  │ │  Anomaly     │
    │Consumer  │ │Svc  │ │  Detector    │
    │→Clickhse │ │     │ │  (streaming) │
    └──────┬───┘ └──┬──┘ └──────────────┘
           │        │
           ▼        ▼
    ┌──────────┐ ┌──────────────────┐
    │Clickhouse│ │  PostgreSQL      │
    │(raw logs)│ │  (pre-aggregated │
    │• TTL 90d │ │   rollups table) │
    │• Partitnd│ │  • per-minute    │
    │  by day  │ │  • per-hour      │
    │          │ │  • per-day       │
    └──────────┘ └────────┬─────────┘
                          │
                          ▼
               ┌──────────────────────┐
               │   Analytics Dashboard│
               │   (React + React Qry)│
               │ • Reads pre-agg      │
               │   rollups (fast)     │
               │ • Redis cache layer  │
               │   (60s TTL)          │
               │ • Drill-down queries │
               │   → Clickhouse       │
               └──────────────────────┘
```

### Key Improvements

1. **Async event logging** — API Gateway fires event to Kafka (non-blocking), never writes to DB on the hot path. Zero added latency to API responses.

2. **Redis for rate limiting** — Sliding window algorithm in Redis Cluster. Atomic, shared across all gateway processes, survives restarts. Use `MULTI/EXEC` or Lua scripts for atomicity.

3. **Kafka as buffer** — Absorbs traffic spikes. If consumers fall behind, events are durably stored (7-day retention). Consumers process at their own pace.

4. **Clickhouse for raw events** — Column-oriented, designed for high-write append workloads and fast aggregation queries. Partition by day, TTL at 90 days. Handles 160K+ inserts/sec easily.

5. **Pre-aggregated rollups** — A streaming aggregation service (Flink or custom Kafka consumer) computes per-minute/hour/day counts by (api_key, endpoint, status_code) and writes to PostgreSQL. Dashboard reads these tiny rollup tables instead of scanning billions of rows.

6. **Dashboard caching** — Redis cache with 60s TTL for dashboard queries. 100 developers viewing = 1 query per minute, not 200.

7. **Tiered storage:**
   - Hot (0-7 days): Kafka for replay
   - Warm (7-90 days): Clickhouse for drill-down queries
   - Cold (90+ days): S3 Parquet for compliance/archival

8. **Token caching** — OAuth tokens cached in Redis with 5min TTL. Token revocation publishes invalidation event.

9. **Anomaly detection** — Streaming consumer watches for sudden spikes per API key, auto-triggers rate limit reduction or alerts.

---

## Sizing Math (Show This in Interview)

```
160,000 events/sec × 86,400 sec/day = ~13.8 billion events/day

Avg event size: ~500 bytes (timestamp, api_key, endpoint, status, latency, metadata)
Daily raw storage: 13.8B × 500B = ~6.9 TB/day uncompressed
Clickhouse compression: ~10:1 → ~690 GB/day
90-day retention: ~62 TB in Clickhouse

Pre-aggregated rollups (per-minute, ~1000 unique api_key×endpoint combos):
1000 × 1440 minutes/day × 100 bytes = ~144 MB/day → trivial for PostgreSQL
```

---

## Practice Questions

1. "Why Clickhouse over PostgreSQL with TimescaleDB?" → Clickhouse is purpose-built for this pattern: high-write append, column-oriented compression (10:1 on event data), and vectorized aggregation queries. TimescaleDB is viable but adds complexity on top of PostgreSQL and doesn't match Clickhouse's raw throughput at this scale.

2. "What if Kafka consumers fall behind?" → Monitor consumer lag (Burrow or built-in metrics). If lag exceeds threshold, auto-scale consumer group. Kafka retains events for 7 days so nothing is lost — this is the beauty of the log-based architecture.

3. "How do you handle a Clickhouse node going down?" → Clickhouse runs as a replicated cluster (ReplicatedMergeTree). Writes go to any replica via a distributed table. Reads are served from any available replica. Zookeeper/ClickHouse Keeper manages replication.

4. "Can you guarantee exactly-once event processing?" → At this scale, we design for at-least-once with idempotent consumers. Each event has a unique event_id. Clickhouse's ReplacingMergeTree deduplicates on merge. For rollups, the aggregation service uses Kafka offsets for checkpointing.

5. "How would you migrate from the current system without downtime?" → Dual-write phase: keep writing to PostgreSQL AND Kafka. Run consumers in shadow mode, compare outputs. Once validated, cut dashboard to read from new sources. Then drain and decomission the old PostgreSQL table.
