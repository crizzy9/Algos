# Leadership Interview Prep — Round 2 (VP of Data Infrastructure)

## Format
Open-ended discussion with VP of Engineering for the Data Infrastructure pillar. This is NOT a coding round — it's about how you think, lead, and understand the business.

## Framework: Talk Like a Senior/Staff Engineer

### Problem-Solving at Scale (Your Framework)
When asked "How do you address engineering problems at scale?":

1. **Understand the blast radius** — "First I scope the problem. Is this affecting one tenant or all? Is it a performance cliff or gradual degradation?"
2. **Instrument before guessing** — "I add observability before making assumptions. Metrics tell me where the bottleneck actually is vs where I think it is."
3. **Solve for the 90th percentile, design for the 99th** — "The fix for most users might be simple. The edge cases need careful design. I separate the two."
4. **Ship incrementally** — "I break large problems into shippable milestones. Each milestone delivers value and reduces risk for the next."
5. **Document decisions** — "I write ADRs for non-obvious choices so future engineers understand why, not just what."

### Klaviyo Business Understanding
You MUST understand the product lifecycle. When asked "What happens when a user clicks an email?":

```
User clicks link in email
    → Click tracker (Klaviyo-hosted redirect URL) logs the event
    → Event flows into the event pipeline (Kafka)
    → Real-time profile update (user X clicked campaign Y at time T)
    → Triggers any flow automations ("if clicked → wait 1 day → send follow-up")
    → Updates engagement scoring for the profile
    → Feeds back into segmentation engine
      (user is now in "engaged clickers" segment)
    → Future campaign targeting uses updated segment membership
    → Analytics dashboard updates for the campaign owner
```

**Key insight to articulate:** "Every click is both a delivery confirmation AND a signal for future personalization. The latency from click to profile update directly affects how timely the next automated message is. That's why the event pipeline needs to be real-time, not batch."

### Testing Philosophy
When asked "What is testing good for?":

**Good for:**
- **Confidence in refactoring** — "Tests are a safety net that lets me move fast. Without them, every refactor is a gamble."
- **Contract enforcement** — "Integration tests verify that service A and service B agree on the API contract. This matters especially when different teams own each side."
- **Regression prevention** — "The best test is one written alongside a bug fix. It encodes institutional knowledge about what went wrong."
- **Design feedback** — "If code is hard to test, it's usually poorly designed. Tests force you to think about interfaces and dependencies."

**Not good for:**
- **Replacing production observability** — "100% test coverage doesn't mean the system works in production. You still need monitoring, alerting, and canary deploys."
- **Testing implementation details** — "Tests that break when you refactor internals (without changing behavior) are net-negative. Test behavior, not implementation."
- **Catching all bugs** — "Tests verify known scenarios. Production surfaces unknown ones. Both are needed."

**Testing pyramid:**
- Many unit tests (fast, cheap, isolated)
- Fewer integration tests (service boundaries, DB queries)
- Minimal E2E tests (critical user journeys only)
- Property-based testing for data pipelines (generate random inputs, verify invariants)

### Mentoring & Team Leadership
Prep these stories:

1. **Bulk content system (5 engineers):**
   - How you broke down the work so junior engineers could own pieces
   - How you handled when someone was stuck or going in the wrong direction
   - How you balanced technical guidance vs letting them learn

2. **Cross-regional team (recommendation platform):**
   - Timezone challenges and async communication
   - How you aligned on architecture across regions
   - How you resolved disagreements on technical approach

3. **AI strategy roadmap:**
   - How you collaborated with PM to scope what was feasible
   - How you said "no" to unrealistic asks while proposing alternatives
   - How you presented technical trade-offs in business terms

### Working with PMs
"I see my role as translating between business intent and technical reality. When a PM says 'we need real-time,' I ask 'what latency is actually acceptable?' because the difference between 100ms and 5 seconds is a fundamentally different architecture. I also proactively share technical constraints early so the PM can adjust scope before we're deep into implementation."

---

## Hypothetical API Design Problem

**Likely prompt:** "Design an API for external developers to register webhook endpoints, configure retry policies, and view delivery analytics."

### Your approach (talk through this):

**Step 1 — Clarify requirements:**
- "How many external developers? Thousands? Tens of thousands?"
- "How many webhook configs per developer on average?"
- "What auth model — OAuth2, API key, both?"
- "Are developers configuring this via UI, API, or both?"

**Step 2 — Resource model:**
```
POST   /api/v2/webhooks                    # Create webhook config
GET    /api/v2/webhooks                    # List all webhooks for this account
GET    /api/v2/webhooks/{id}               # Get specific webhook
PUT    /api/v2/webhooks/{id}               # Update webhook config
DELETE /api/v2/webhooks/{id}               # Delete webhook
POST   /api/v2/webhooks/{id}/test          # Send a test event
GET    /api/v2/webhooks/{id}/deliveries    # Delivery history + analytics
```

**Step 3 — Key design decisions to discuss:**
- **Versioning:** `/api/v2/` prefix. Mention Klaviyo's actual API versioning strategy.
- **Auth:** OAuth2 bearer token + API key header. Rate limited per-key.
- **Webhook config schema:**
```json
{
  "url": "https://customer.com/webhook",
  "events": ["email.opened", "email.clicked", "profile.updated"],
  "secret": "auto-generated-hmac-secret",
  "retry_policy": {
    "max_retries": 5,
    "backoff": "exponential",
    "initial_delay_seconds": 60
  },
  "active": true
}
```
- **HMAC signing:** Every webhook delivery includes `X-Klaviyo-Signature` header. Customer verifies with their `secret`.
- **Idempotency:** Each delivery has a unique `X-Klaviyo-Delivery-Id`. Customers can deduplicate.
- **Pagination:** Cursor-based pagination for deliveries (not offset — offset is O(n) on large tables).

---

## Reverse Interview Questions (Ask the VP)

1. **"What does the Data Infrastructure team's reliability story look like right now — are there specific scaling challenges you're tackling as the platform grows?"**
   - Shows you think about operational maturity, not just features
   - Opens discussion about real problems you'd work on

2. **"How does the DevX team's work on Public APIs influence internal developer experience? Is there cross-pollination between internal and external tooling?"**
   - Shows you understand platform teams create leverage
   - Signals you think about developer experience holistically

3. **"What does 'senior engineer impact' look like on this team — is it more about technical depth on critical systems, or breadth across the platform?"**
   - Directly tells you what they value
   - Shows you're thinking about how to maximize your impact from day one
