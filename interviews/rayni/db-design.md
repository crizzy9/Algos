Backend Design Exercise — Database Schema

Multi-tenant knowledge platform for scientific instruments
Setup

You're designing the data layer for a B2B SaaS product. Customers are research organizations — universities, biotech labs, pharma companies. The product helps lab staff get expert answers about their scientific instruments by chatting with an AI that's been trained on each instrument's documentation, photos, and prior conversations.

All of this will live in a multi-tenant Postgres database.
How this exercise runs

Phase 1 — Entity-relationship mapping (start here).

Don't jump straight into tables and columns. First, work through the requirements below and probe for the entities and how they relate:

    Identify the core entities in the system.
    Map the relationships between them — one-to-one, one-to-many, many-to-many — and the cardinality/optionality that matters.
    Ask clarifying questions to pin down anything ambiguous. This is a conversation, not a monologue; use us to resolve the unknowns.
    Produce a clear entity-relationship map (an ERD sketch, boxes-and-lines, or a list of entities with their relationships — whatever communicates it).

Phase 2 — Detailed design (on the interviewer's cue).

Once the entity-relationship map is in good shape, pause and check in with the interviewer. We'll pick a specific part — or several parts — of the system for you to design in depth. For each part we call out, we want:

    The tables, with primary keys, foreign keys, and the columns that matter for the requirements below.
    The indexes you'd add for the obvious access patterns. and others...

Business requirements

1. Organizations, teams, and users

   The platform serves multiple customer Organizations.
   Each Organization has one or more Teams (labs, departments, project groups).
   New teams can be added at any time. Teams can be renamed or removed.
   Users belong to the Organization (not to a specific Team).
   A user can be a member of one or more teams. Users can move between teams over time.

2. Instruments

   Each Instrument has a vendor, a model, a name, and a description.
   An Instrument can be assigned to one or more teams within its organization — sharing across teams is expected.
   All knowledge about an instrument lives at the instrument level — documents, configuration notes, photos, prior chats. If a team loses access to an instrument, that knowledge stays put. The instrument is the unit, not the team.
   Sometimes a chat is about more than one instrument at once. The model should support a named Instrument Combination — a saveable group of instruments that can be the subject of a chat.

**3. Authorization**

Three roles, assigned at the Organization level:

    Admin — everything, including billing and user management.
    Expert — can create, modify, and delete instrument data (files, configs, etc.).
    Basic user — read-only across instruments and chats.

All API actions need to respect these roles. Your schema should support efficient enforcement.

1. CRUD with recovery

   Standard create / read / update / delete on Organizations, Teams, Instruments, and Instrument Combinations.
   Soft delete, not hard delete — a mistaken deletion has to be recoverable, and the rows that hang off the deleted row should behaviorally disappear too (and come back when it's restored).

2. Chats and messages

   Users have Chats with the AI. A chat is scoped to one Instrument or one Instrument Combination.
   A chat has many Messages (turns) — from the user, and from the AI.
   The AI's answers may include citations that point to specific files / pages in the instrument's documents. Citations must resolve to the actual source row.
   We track per-message metadata (model, token counts, cost, timing) for billing and observability.

3. Files and ingestion

   Users upload Files to an instrument — usually PDFs (manuals), but also photos.
   Each upload kicks off an asynchronous ingestion job that may take minutes. The job's status must be visible to the user (queued / processing / done / failed, with an error message).
   Ingestion produces Assets — extracted images and tables — and Chunks, the retrievable pieces of text that the AI cites against (assume one embedding per chunk; you don't need to design vector search).
   We need to answer:
   "What files are on this instrument?"
   "What's the status of file X's ingestion?"
   "Given a citation in an answer, what file / page / asset does it point to?"

In scope

Tables, columns, primary keys, foreign keys, soft-delete strategy, RBAC modeling, useful indexes, and trade-off notes.
Out of scope (don't spend time here)

    Vector search internals (just acknowledge that a chunk has an embedding; you don't need to design pgvector).
    The agent / LLM code itself.
    API request/response shapes.
    Auth / SSO / IdP integration.
    Sharding and horizontal scale.
