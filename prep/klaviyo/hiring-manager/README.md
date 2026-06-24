# Hiring Manager Interview Prep — Dan

## Format
Two parts in one session:
1. **AI Usage Deep-Dive** — How AI has transformed your workflow (must demonstrate "Level 3" / 90% usage)
2. **System Diagram Walkthrough** — Draw a system you built on Google Draw, explain tech choices, component interactions, collaboration

---

## Part 1: AI Usage Deep-Dive

### What Dan Wants to Hear
- You use AI in **90%+ of your workflow** — not just autocomplete, but architecture, debugging, testing, code review
- Your usage has **evolved over time** — you didn't start at Level 3
- You have **concrete examples** with real outcomes (time saved, bugs caught, quality improvements)
- You understand the **limitations** and know when NOT to use AI

### The 3 Levels (Klaviyo Framework)
- **Level 1:** Autocomplete, simple code generation, basic Q&A
- **Level 2:** Refactoring, test generation, code review assistance, debugging
- **Level 3:** Architecture design, system design collaboration, production code generation, AI-driven workflows end-to-end

### Your AI Story Arc (Narrative)

**Phase 1 — Early adoption (Level 1)**
- Started with Copilot for autocomplete and boilerplate
- Used ChatGPT for quick lookups instead of Stack Overflow
- "It was faster than searching docs but I still wrote most code myself"

**Phase 2 — Integration into daily workflow (Level 2)**
- Started using AI for refactoring legacy code at Intuit
- Test generation — "I'd write the implementation, then have AI generate edge case tests"
- Debugging — "I'd paste stack traces and error logs, AI would narrow down root cause faster than I could grep through logs"
- Code review prep — run code through AI before PR to catch issues early

**Phase 3 — AI as a collaborator (Level 3) — WHERE YOU ARE NOW**
- **MCP Server project** — Used AI to design the architecture, generate the scaffold, iterate on the API contract
- **Claude Code as pair programmer** — Architecture discussions, implementation, testing all in one flow
- **Bulk Content System** — AI generated dynamic template logic, I reviewed and refined. AI wrote the test suite, I validated coverage
- **AI Marketing Agent (SymphonyAI)** — LangChain + MCPs, the product IS AI, and AI built AI
- **NixOS homelab** — AI helps manage declarative configs, rollback strategies, system design

### Questions Dan Will Ask + Answers

**"How has AI changed how you write production code?"**
> "It's fundamentally changed my loop. Before, I'd spend 30% of time on boilerplate and 30% on debugging. Now AI handles the boilerplate entirely and accelerates debugging by giving me hypotheses to test. My time has shifted to architecture decisions, code review, and edge case thinking — the parts that actually need human judgment. On the Bulk Content System, AI generated the initial template rendering pipeline. I spent my time on the data model design and making sure the caching layer was correct, not writing CRUD endpoints."

**"Give me a specific example of AI improving code quality."**
> "On the Kafka event consumer pipeline, I used AI to generate property-based tests that found an edge case in our audience targeting logic — a race condition where a user could receive duplicate offers if two events arrived within the same processing window. I wouldn't have written that test myself because I was thinking about happy paths. The AI generated 40+ edge case scenarios and 3 of them caught real bugs."

**"What are the limitations? When do you NOT use AI?"**
> "Three areas: security-critical code paths where I need to verify every line, performance-critical sections where I need to understand the exact algorithmic complexity, and cross-team architectural decisions where context about org politics and priorities matters more than technical correctness. AI doesn't know that the payments team just froze their API and we need to work around it."

**"How do you validate AI-generated code?"**
> "Three checks: First, I read it line by line — AI can generate plausible but subtly wrong code, especially around edge cases. Second, I run it through the test suite, including AI-generated tests. Third, I check for security issues — AI sometimes generates code with SQL injection or hardcoded secrets because that's what it saw in training data. Basically the same rigor as reviewing a junior engineer's PR."

---

## Part 2: System Diagram — Bulk Content System

### Why This Project
- Led 5 engineers — shows leadership
- 1400% capacity increase — shows measurable impact
- Dynamic templates + audience segmentation — directly maps to Klaviyo's product
- Clear architecture with multiple components — good for diagramming

### The Diagram (draw this on Google Draw)

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Marketing  │────▶│  Campaign API    │────▶│  Template Engine │
│  Dashboard  │     │  (Django REST)   │     │  (Jinja2 + LLM) │
│  (React)    │     │                  │     │                  │
└─────────────┘     └──────┬───────────┘     └────────┬────────┘
                           │                          │
                           ▼                          ▼
                    ┌──────────────┐          ┌───────────────┐
                    │  PostgreSQL  │          │  Redis Cache   │
                    │  (campaigns, │          │  (templates,   │
                    │   segments,  │          │   rendered     │
                    │   audiences) │          │   content)     │
                    └──────┬───────┘          └───────────────┘
                           │
                           ▼
                    ┌──────────────────┐     ┌─────────────────┐
                    │  Kafka / Queue   │────▶│  Content Worker  │
                    │  (render jobs)   │     │  (Celery)        │
                    │                  │     │  - bulk render   │
                    └──────────────────┘     │  - personalize   │
                                            │  - validate      │
                                            └────────┬─────────┘
                                                     │
                                                     ▼
                                            ┌─────────────────┐
                                            │  Delivery Queue  │
                                            │  (email/SMS      │
                                            │   send jobs)     │
                                            └─────────────────┘
```

### Talking Points Per Component

**Campaign API (Django REST)**
- "Central orchestrator. Receives campaign creation requests, validates segments, kicks off render pipeline"
- "Chose DRF because team had Django expertise and we needed rapid iteration. FastAPI would've been faster but onboarding cost wasn't worth it"

**Template Engine (Jinja2 + LLM)**
- "Dynamic templates with variable substitution + AI-generated content variants"
- "LLM generates subject lines and body copy variations, Jinja2 handles the personalization merge"
- "Caching rendered templates in Redis — same segment + same template = cache hit"

**PostgreSQL**
- "Source of truth for campaigns, audience segments, and delivery status"
- "Chose Postgres over MySQL for JSONB support — segment rules are flexible and schema-less"

**Redis Cache**
- "Two uses: template cache (rendered content) and rate limiting on the API"
- "Cache invalidation on template edit — publish event to invalidate"

**Kafka Queue**
- "Decouples the API from the heavy rendering work. Campaign creation returns immediately, rendering happens async"
- "Partitioned by segment ID so all users in a segment get processed by the same worker — better cache locality"

**Content Worker (Celery)**
- "Pulls render jobs from Kafka, personalizes content per user, validates output"
- "This is where the 1400% capacity increase came from — horizontal scaling of workers + batch rendering"

**Delivery Queue**
- "Final stage — rendered content goes to email/SMS provider"
- "Separate queue so rendering backlog doesn't block sends"

### Collaboration & Going Above and Beyond

**Leadership:**
> "Led 5 engineers. I designed the architecture, wrote the technical spec, and divided work by component. Each engineer owned one piece end-to-end. I did weekly architecture reviews and made sure interfaces between components were clean."

**Above and beyond:**
> "The original ask was just 'make bulk email faster.' I saw that the template rendering was the bottleneck, so I proposed the caching layer and the LLM content generation — neither was in the original requirements. The caching alone gave us 3x throughput, and the LLM content generation became a feature the marketing team didn't know they wanted."

**Conflict / challenge:**
> "The biggest challenge was convincing the team to use Kafka instead of just scaling the Celery workers. Two engineers wanted the simpler path. I built a prototype showing that at 10x volume, Celery's broker would be the bottleneck. Data won the argument."

---

## Part 2 (Alternate): MCP Server

### If Dan asks about the AI Agent / MCP Server instead

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  User /     │────▶│  LangChain Agent │────▶│  MCP Server      │
│  CLI /      │     │  (Orchestrator)  │     │  (Tool Provider)  │
│  Chat UI    │     │                  │     │  - create campaign│
└─────────────┘     └──────┬───────────┘     │  - fetch segments │
                           │                 │  - generate copy  │
                           ▼                 └────────┬──────────┘
                    ┌──────────────┐                  │
                    │  LLM (Claude │                  ▼
                    │   / GPT-4)   │          ┌───────────────┐
                    │              │          │  Marketing    │
                    └──────────────┘          │  Platform API │
                                             └───────────────┘
```

**Why it's impressive:**
- "90% reduction in campaign go-live time"
- "AI building AI — the agent uses AI to generate content, and I used AI to build the agent"
- "MCP protocol means any LLM can use the tools — not locked to one provider"
