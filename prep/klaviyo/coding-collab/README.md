# Coding Collab Prep — Round 3

## Format
- 1hr on CodeSignal with "Victor"
- Given intern-level code → uplevel to senior/staff quality
- Think out loud the ENTIRE time
- Gather requirements FIRST before touching code

## What They Grade On
1. **Requirement gathering** — Do you ask clarifying questions or just start coding?
2. **Issue identification** — Can you spot bugs, security holes, scalability problems?
3. **Trade-off discussion** — Do you explain WHY you'd change something, not just WHAT?
4. **Code quality** — Naming, typing, structure, separation of concerns
5. **Proactiveness** — Do you notice things they didn't ask about?

## Checklist of Things to Look For
- [ ] SQL injection / raw string formatting in queries
- [ ] API keys hardcoded or stored insecurely
- [ ] Missing input validation
- [ ] No error handling / bare excepts
- [ ] Bad variable names (single letters, abbreviations)
- [ ] No type hints
- [ ] Global mutable state
- [ ] Missing caching opportunities (repeated DB calls, expensive computations)
- [ ] N+1 query patterns
- [ ] No pagination on list endpoints
- [ ] Webhook retry logic missing
- [ ] No idempotency on writes
- [ ] Race conditions on concurrent access
- [ ] Hardcoded config values (timeouts, URLs, limits)
- [ ] Missing logging/observability

## Practice Problems
- `mock-1-webhook-service.py` — Webhook delivery service (intern code)
- `mock-2-campaign-api.py` — Email campaign CRUD API (intern code)
- `mock-3-event-ingestion.py` — Event tracking pipeline (intern code)

## How to Practice
1. Set a 60-min timer
2. Open the intern code file
3. Spend first 5-10 min reading + asking clarifying questions (write them down)
4. Identify all issues before fixing any
5. Prioritize: security > correctness > scalability > code quality
6. Fix issues while narrating your reasoning out loud
