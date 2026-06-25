#!/usr/bin/env python3
"""Add pedagogical pattern fields to ABAP content JSON files."""
import json
import os

CONTENT_DIR = "/Users/kallolchakraborty/ABAP bytes - Github Pages/abap-bytes/content/abap"

# Define all edits: (filename, [(section_title, field_name, field_data), ...])
edits = {
    "abap-cds.json": [
        ("CDS as Design Paradigm", "decisionTree", {
            "prompt": "Should this data retrieval be a CDS view, AMDP method, or Open SQL query?",
            "firstQuestion": "\"Is this a declarative data model or a procedural transformation?\" Declarative = CDS view. Procedural = AMDP. Simple read = Open SQL.",
            "branches": [
                {"condition": "Declarative data model with associations and aggregations", "path": "CDS view. ~20 lines of DDL. Optimizer pushes predicates to HANA. Use for analytical queries, OData projections, transactional read models."},
                {"condition": "Procedural multi-step transformations with SQLScript", "path": "AMDP. Complex set-based operations in HANA. Use for data migrations, pivot tables, window functions. Avoid when logic needs RFC calls."},
                {"condition": "Simple SELECT with <10K rows, subsequent ABAP processing", "path": "Open SQL. Best when subsequent processing needs ABAP runtime (ALV, field symbols). Avoid when same data is needed by multiple consumers."}
            ],
            "staffPlusTip": "CDS views are your semantic data model layer. AMDP is compute pushdown. Open SQL is application integration. Each has a role in the layered architecture."
        }),
        ("Association vs JOIN", "quantifiedTradeoff", {
            "title": "Association vs JOIN — Performance Cost of Pattern Misuse",
            "variables": [
                {"name": "Query volume", "value": "1,000 QPS", "source": "Fiori app serving 500 concurrent users"},
                {"name": "Rows per query", "value": "100 headers × 10 items each", "source": "Average sales order query pattern"},
                {"name": "Association reuse", "value": "Consumer accesses items 30% of the time", "source": "UI analytics from AppInsight"}
            ],
            "calculation": {
                "formula": "TotalCost = QueryVolume × (ResolutionCost × UsageRate + UnusedCost × (1 - UsageRate))",
                "assoc": {"writeLatency": "0ms (no eager fetch)", "monthlyPenalty": "$0 — No cost when items not needed. When needed, 2ms latency for lazy resolution."},
                "join": {"writeLatency": "5ms per query", "monthlyPenalty": "$3,200 — All 1,000 queries fetch items. 70% of the time, data goes unused. Wastes ~350,000 row transfers/day."},
                "breakeven": "At >60% item access rate, JOIN is cheaper because lazy resolution overhead (2 additional SELECTs) exceeds eager JOIN cost. Profile actual access patterns before optimizing."
            }
        }),
        ("CDS Table Functions", "decisionTree", {
            "prompt": "When should I use a CDS Table Function instead of a regular CDS view?",
            "firstQuestion": "\"Can the logic be expressed declaratively?\" If the data model is a single SELECT with filters and projections, use a regular CDS view. If you need procedural SQLScript (loops, temp tables, error handling), use a Table Function.",
            "branches": [
                {"condition": "Single SELECT with joins, filters, aggregations", "path": "Regular CDS view. Declarative, optimizer-friendly, supports predicate pushdown. ~5 lines of DDL. Opaque to the optimizer inside the SQLScript."},
                {"condition": "Procedural logic with temp tables, loops, or dynamic SQL", "path": "CDS Table Function. Exposes results as a CDS entity but implements via AMDP SQLScript. Use for hierarchical rollups, fuzzy search, stock projections."},
                {"condition": "Call HANA-specific features (PAL, APL, spatial, series)", "path": "CDS Table Function. HANA-specific libraries are only accessible via SQLScript. The Table Function wraps these and exposes results as standard CDS."}
            ],
            "staffPlusTip": "Table Functions are the escape hatch. Use them when CDS declarative syntax is insufficient. Always add @ObjectModel.resultSetType and @ObjectModel.usageType annotations so the optimizer can plan around the opaque function call."
        }),
        ("CDS Hierarchy", "quantifiedTradeoff", {
            "title": "CDS Hierarchy vs Recursive ABAP — Database-Level vs App-Level Traversal",
            "variables": [
                {"name": "Hierarchy depth", "value": "12 levels", "source": "Large enterprise org structure (CEO → regional VP → ... → team lead)"},
                {"name": "Node count", "value": "50,000 nodes", "source": "Global company with 50K employees"},
                {"name": "Query frequency", "value": "500 queries/hour", "source": "Org management Fiori app peak usage"}
            ],
            "calculation": {
                "formula": "TotalTime = QueryCount × (SingleQueryTime + DataTransferTime)",
                "cds_hierarchy": {"writeLatency": "50ms per query", "monthlyPenalty": "$0 — 500 queries/h × 50ms × 730h = 10.1 hours DB time. All computation in HANA. No ABAP work process overhead."},
                "abap_recursive": {"writeLatency": "2s per traversal (ABAP recursive FM)", "monthlyPenalty": "$4,800 — 500 queries/h × 2s × 730h = 202 hours. Work process utilization spikes. Each level adds a DB round-trip."},
                "breakeven": "At 6+ levels or 10K+ nodes, CDS Hierarchy is 40x faster. Below 4 levels and 1K nodes, ABAP recursion is simpler to implement and debug."
            }
        }),
        ("CDS DCL", "adversarialResponse", {
            "challenge": "\"Your DCL policy is too restrictive. The sales team can't see any data because their PFCG roles don't have full authorization objects configured.\"",
            "badResponse": "\"Tell the sales team to fix their PFCG roles.\" (no empathy, no solution)",
            "goodResponse": "\"You raise a real operational concern. DCL enforces row-level security at the database layer, which means incomplete PFCG roles result in empty result sets — not an error message. Let me address this with a tiered approach: (1) Add a DCL fallback — if no authorization values are found, grant access to a minimal default set (e.g., company code '0001') instead of blocking all rows. This prevents the 'empty screen' problem. (2) Create a DCL health check CDS view that shows users their effective authorizations — they can self-diagnose role issues. (3) Add an explicit error message via @AccessControl.authorizationCheck: #CHECK that tells users 'Contact admin to assign VKORG authorization' instead of silently returning zero rows. The key design principle: DCL should enforce security boundaries, but it must also provide feedback when authorization fails.\"",
            "pattern": "empathy-and-tiered-fix — acknowledge the operational pain, provide multiple layers of remediation (fallback defaults, self-diagnosis, clear error messages), and reframe security as a spectrum, not a binary."
        }),
        ("CDS Extensibility", "adversarialResponse", {
            "challenge": "\"Your CDS extensibility architecture is over-engineered. We could just modify the SAP standard view directly and save weeks of work.\"",
            "badResponse": "\"You should never modify SAP standard objects.\" (dogmatic, no pragmatic tradeoff)",
            "goodResponse": "\"I understand the time pressure — modifying the standard view takes 1 day, and building an extension view takes 3 days. However, the math changes when you consider upgrades. Every SAP upgrade overwrites standard views. If you modify the standard view directly, you must reapply the change after every upgrade — that's 3 days × 4 upgrades/year × 5 years = 60 days of rework. The extension view, by contrast, survives upgrades automatically because SAP's upgrade tooling does not touch customer extension includes. Over 5 years, the extension approach costs 3 days upfront + 0 days rework = 3 days total. The modification approach costs 1 day + 60 days rework = 61 days. The breakeven is at the second upgrade. Additionally, extension views support the Clean Core strategy required for S/4HANA Cloud — without it, your system cannot pass the cloud readiness check.\"",
            "pattern": "quantified-tradeoff — acknowledge the short-term gain, quantify the long-term cost including upgrade cycles, show the breakeven point, and connect to strategic constraints (Clean Core, cloud readiness)."
        }),
        ("CDS Annotation Framework", "decisionTree", {
            "prompt": "Which annotation domains should I apply to this CDS view?",
            "firstQuestion": "\"Who consumes this view?\" Fiori UI needs @UI.* annotations. OData services need @OData.publish. Analytics needs @Analytics.*. Enterprise search needs @Search.*.",
            "branches": [
                {"condition": "Fiori Elements UI consumption", "path": "Add @UI.lineItem, @UI.headerInfo, @UI.facet. These drive Fiori elements table and form layouts. One annotation change rebuilds the DPC/MPC at activation."},
                {"condition": "Analytics / SAP Analytics Cloud consumption", "path": "Add @Analytics.query: true with @Analytics.measure and @Analytics.dimension annotations. Enables aggregation and currency conversion at the database level."},
                {"condition": "Search / Enterprise Search consumption", "path": "Add @Search.searchable: true with @Search.fuzziness and @Search.decomposition. Eliminates custom search index builds."}
            ],
            "staffPlusTip": "Annotations implement convention-over-configuration. @OData.publish: true eliminates OData service creation entirely. One annotation change => full DPC/MPC regeneration at activation."
        }),
        ("CDS Performance Patterns", "adversarialResponse", {
            "challenge": "\"Your CDS view is slow. A simple SELECT on the table takes 200ms, but your CDS view takes 12 seconds.\"",
            "badResponse": "\"The CDS view is just a definition — it shouldn't be slow. Maybe HANA is having issues.\" (defensive, blames infrastructure)",
            "goodResponse": "\"Let me systematically diagnose the performance regression. A 60x slowdown suggests the CDS optimizer has surrendered — it's no longer pushing predicates down to the base tables. I'll check three things: (1) View complexity — how many tables and nested layers? If >20 table references, the optimizer may give up on global optimization. I would decompose the view into intermediate layers. (2) Association cardinality — if a [1..1] association is actually [0..1] in data, the optimizer generates an INNER JOIN that scans unnecessary rows. I'd verify cardinality annotations match actual data distribution. (3) Parameterization — the view likely lacks mandatory parameters. Without parameters, HANA can't prune partitions or use selective indexes. I'd add @Environment.systemField for date-based pruning. Let me trace the generated SQL via ST05 PlanViz to confirm which operator is the bottleneck — it's likely a full table scan on a non-partitioned column.\"",
            "pattern": "systematic-diagnosis — accept the problem as valid, propose a structured root-cause analysis using specific tools (ST05, PlanViz), identify common patterns (optimizer surrender, cardinality mismatch, missing parameters), and offer concrete fixes."
        }),
    ],
    "abap-rap-managed.json": [
        ("Transactional Composition Internals", "decisionTree", {
            "prompt": "Should you use managed or unmanaged RAP for this business object?",
            "firstQuestion": "\"How much of the standard CRUD behavior matches your requirement?\" If CREATE/UPDATE/DELETE is standard data persistence with simple validations, managed is correct. If you need custom locking, late numbering with complex business rules, or non-standard transaction control, unmanaged is required.",
            "branches": [
                {"condition": "Standard CRUD with simple validations and determinations", "path": "Managed scenario. ~50 lines of behavior pool code. Built-in draft, locking, numbering. Save ~80% boilerplate vs unmanaged. Use for: simple master data, standard document processing."},
                {"condition": "Complex create with legacy number ranges, cross-BO validation", "path": "Unmanaged scenario. Manual CREATE/UPDATE/DELETE implementations. ~400+ lines per entity. Required for: integration scenarios, legacy BAPI wrappers."},
                {"condition": "Existing BAPI/function module needs RAP wrapper", "path": "Unmanaged with BAPI call in create/update methods. This is the migration pattern: wrap existing function modules in RAP behavior, migrate to managed incrementally."}
            ],
            "staffPlusTip": "Use managed for 80% of entities. For the 20% that need custom logic, isolate it in a dedicated class and migrate to managed when the framework catches up."
        }),
        ("EML Deep Dive", "quantifiedTradeoff", {
            "title": "EML Overhead Per Operation — Framework Cost vs Manual SQL",
            "variables": [
                {"name": "Operation mix", "value": "60% READ, 30% MODIFY, 10% EXECUTE", "source": "Fiori app telemetry for Travel BO"},
                {"name": "Entity depth", "value": "3 levels (Travel → Booking → Supplement)", "source": "Composition tree depth"},
                {"name": "Concurrent users", "value": "500 concurrent", "source": "Peak load estimate"}
            ],
            "calculation": {
                "formula": "EMLOverhead = ParserTime + AuthCheckTime + BufferMgmtTime + DeterminationTime",
                "eml": {"writeLatency": "12ms avg per EML call (framework overhead)", "monthlyPenalty": "$1,800 — 500 users × 20 operations/min × 12ms × 730h = ~1,460 hours of framework overhead. However, this includes auth checks, buffering, and draft handling that you'd need to build manually."},
                "manual_sql": {"writeLatency": "3ms per raw SQL call", "monthlyPenalty": "$450 — Pure SQL is faster per operation but you lose: draft management, automatic locking, authorization framework, and determination orchestration. Building these manually costs ~$40K in development."},
                "breakeven": "EML overhead pays for itself if your BO needs >3 of these features: draft, locking, auth, determinations, validations. At 500+ users, the framework overhead is ~9ms per call, but manual implementation of the same features would add 15-25ms of custom ABAP code."
            }
        }),
        ("Early vs Late Numbering", "decisionTree", {
            "prompt": "Should I use early or late numbering for this business object?",
            "firstQuestion": "\"Does the key depend on business logic that runs during the save sequence?\" If the key can be assigned at MODIFY time (independent of other business data), use early numbering. If the key depends on fields set by determinations or on fiscal year context, use late numbering.",
            "branches": [
                {"condition": "Simple sequential number, no dependency on other fields", "path": "Early numbering. Key assigned at MODIFY time. Available immediately in mapped response. Child entities can reference through %pid. Draft record has final key from creation."},
                {"condition": "Key depends on document type, fiscal year, or determination output", "path": "Late numbering. Key assigned at SAVE time. Use %cid references in child entities. Draft record has temporary key until activation."},
                {"condition": "OData service needs immediate key in create response", "path": "Early numbering. OData create response includes the final key. Late numbering requires a separate READ after activation to get the key."}
            ],
            "staffPlusTip": "Early numbering is simpler and preferred unless you have an explicit dependency on save-time data. Late numbering adds complexity to draft handling and child entity references."
        }),
        ("Early vs Late Numbering", "quantifiedTradeoff", {
            "title": "Early vs Late Numbering — Key Assignment Cost",
            "variables": [
                {"name": "Create throughput", "value": "200 creates/hour", "source": "Document processing peak"},
                {"name": "Child entities per create", "value": "5 on average", "source": "Typical document with line items"},
                {"name": "Late numbering complexity", "value": "3 additional methods in behavior pool", "source": "Number range + %pid mapping + activation"}
            ],
            "calculation": {
                "formula": "DevCost + RuntimeCost = (ImplementationDays × DailyRate) + (ExtraCPUTime × HourlyRate × Hours)",
                "early": {"writeLatency": "0ms overhead (framework-managed)", "monthlyPenalty": "$0 — Early numbering is built into the framework. No additional implementation cost. Zero runtime overhead for key assignment."},
                "late": {"writeLatency": "5ms per create (number range call + %pid mapping)", "monthlyPenalty": "$7,200 — Late numbering: 3 extra methods × 2 days each = 6 dev days ($7,200). Runtime: 5ms per create × 200 creates/h × 730h = 0.2 hours/month extra CPU. Acceptable overhead but adds complexity."},
                "breakeven": "Early numbering is strictly cheaper on both dev cost and runtime. Only use late numbering when business rules require save-time key assignment (e.g., fiscal year + document type composite key)."
            }
        }),
        ("Determination Execution Order", "adversarialResponse", {
            "challenge": "\"My determinations are firing in the wrong order. D4 calculates total price before D1 sets the status, so the price is always zero.\"",
            "badResponse": "\"Re-order the determinations in the BDEF.\" (oversimplified, doesn't address the real issue)",
            "goodResponse": "\"This is a classic determination ordering problem. Let me analyze it: Determinations within the same trigger group fire in BDEF definition order — D1 before D4. If D4 sees a zero price, the issue isn't ordering but dependency. D4 likely depends on a field that D1 hasn't set yet, OR D4 is reading from an entity that hasn't been fully populated. Three solutions: (1) Add a field-level constraint to D4 — specify that D4 depends on the status field set by D1. The framework then automatically re-executes D4 after D1 completes. (2) Use on save instead of on modify for D4 — the framework guarantees all on-modify determinations complete before any on-save determination runs. (3) If D4 must run on modify but depends on D1's output, implement an explicit READ ENTITIES in D4 to get the current state rather than relying on the passed keys. The root cause is usually that D4 receives the %tky before D1 has modified the entity — D4 should either use %control fields or explicitly read the updated state.\"",
            "pattern": "root-cause-analysis — identify the actual cause (dependency vs ordering), provide multiple solutions with tradeoffs, and explain the framework behavior (field-level constraints, trigger groups, before/after images)."
        }),
        ("Validation Semantics", "adversarialResponse", {
            "challenge": "\"Our validations are running but not preventing the save. Data is committed even when validations fail.\"",
            "badResponse": "\"You must have a bug in your validation implementation.\" (blames developer, no systematic debugging)",
            "goodResponse": "\"Let me trace the validation execution path. There are three common reasons validations fail to prevent saves: (1) The validation is defined as on modify but should be on save. on modify validations run during MODIFY phase — if the framework gets a SAVE before the next dialog step, the on-save validations may not execute. Check your BDEF: validation on save is the correct trigger for preventing commits. (2) Your validation is returning errors in reported but not populating the failed table. The framework only prevents the commit if failed is populated — reported messages are informational. Ensure you're APPENDING to failed-<entity> for each failing record. (3) There's an early save or finalize save method that bypasses validation. If you've implemented custom save methods, you may be calling COMMIT WORK before the validation framework runs. Check for explicit COMMIT WORK in your behavior pool or BAPI calls. The fix: ensure all validations are on save, populate both failed and reported, and never call COMMIT WORK outside of the framework's save sequence.\"",
            "pattern": "systematic-triage — list the specific failure modes (trigger type, failed table population, early commit) with precise ABAP API references, and provide a step-by-step debugging approach."
        }),
        ("Feature Control", "decisionTree", {
            "prompt": "How should I implement dynamic enablement of operations for this business object?",
            "firstQuestion": "\"Does the availability of operations depend on the entity's state?\" If an action should be enabled only when Status = 'Open', you need instance feature control. If the same operations are always available for all instances, you don't need dynamic control.",
            "branches": [
                {"condition": "Operations depend on entity state (status-based enablement)", "path": "Instance feature control. Implement get_instance_features in behavior pool. Returns %features bitmask with %features-+update, %features-+delete, %features-+action-<name>."},
                {"condition": "Operations depend on user authorization only", "path": "Global authorization control via BDEF authorization master (instance). Use get_instance_authorizations to check PFCG roles. Simpler than feature control if state independence holds."},
                {"condition": "Fields should be read-only in certain states", "path": "Instance field control. Add field ( features : instance ) to BDEF. Return %field-<name> = if_abap_behv=>fc-fld-enabled or fc-fld-read_only in get_instance_features."}
            ],
            "staffPlusTip": "Feature control implements the State pattern at the framework level. The entity's status field determines which operations are available. This is the same pattern used in workflow engines and state machines."
        }),
        ("Draft Handling", "quantifiedTradeoff", {
            "title": "Draft Lifecycle Overhead — Framework-Managed vs Custom Draft",
            "variables": [
                {"name": "Draft creation rate", "value": "1,000 drafts/hour", "source": "Peak Fiori usage during month-end"},
                {"name": "Draft activation rate", "value": "600 activations/hour", "source": "60% of drafts are activated, 40% discarded"},
                {"name": "Draft auto-save interval", "value": "5 seconds", "source": "Default Fiori draft auto-save setting"}
            ],
            "calculation": {
                "formula": "DraftCost = (DraftCreateCount + DraftUpdateCount) × PerOperationCost + StorageCost",
                "managed_draft": {"writeLatency": "2ms per draft operation", "monthlyPenalty": "$500 — Framework-managed: 1,000 creates/h × 2ms + 6,000 auto-saves/h × 2ms = ~14ms/s of DB time. Draft tables in HANA use column-store with minimal overhead."},
                "custom_draft": {"writeLatency": "15ms per operation", "monthlyPenalty": "$4,200 — Custom draft: manual INSERT/SELECT on draft tables. 1,000 creates/h × 15ms + 6,000 auto-saves/h × 15ms = ~105ms/s. Plus development cost of ~$24K for draft lifecycle implementation."},
                "breakeven": "Managed draft is 7x cheaper in runtime and effectively free in development cost. Custom draft only makes sense when you need non-standard behavior like pre-approval workflows or unique constraint enforcement across draft/active."
            }
        }),
        ("Draft Handling", "adversarialResponse", {
            "challenge": "\"Our draft handling is causing deadlocks under high concurrency. 100 users editing the same document type are blocking each other.\"",
            "badResponse": "\"Increase the number of work processes.\" (band-aid, not solving the root cause)",
            "goodResponse": "\"Deadlocks under high concurrent draft editing point to a lock contention problem, not insufficient resources. Let me diagnose: (1) RAP managed scenario locks the root entity during draft editing. If 100 users edit different documents, there should be no contention — each document has its own lock. If they're editing the SAME document (e.g., a shared template), that's a design issue — consider optimistic locking via ETag instead of pessimistic ENQUEUE locks. (2) Check if the draft auto-save interval (default 5 seconds) is too aggressive. Each auto-save triggers a write lock. Reduce to 30 seconds for low-priority documents. (3) The most common cause: a secondary index on the draft table is causing lock escalation. HANA may escalate row-level locks to table-level locks if a single transaction touches too many rows. Add a dedicated draft timestamp index to reduce scan range. (4) For truly high-contention scenarios, implement a custom draft store using a dedicated HANA table with light-weight optimistic locking and application-level conflict resolution.\"",
            "pattern": "analyze-then-optimize — identify the specific lock contention pattern, propose tiered solutions (config changes, index optimization, architectural redesign), and show understanding of HANA lock escalation behavior."
        }),
    ],
    "abap-rap-unmanaged.json": [
        ("When to Choose Unmanaged", "decisionTree", {
            "prompt": "Should I choose unmanaged RAP for this business object?",
            "firstQuestion": "\"Does your business object require custom persistence, legacy BAPI integration, or non-standard draft behavior?\" Answer yes to any = unmanaged candidate. Otherwise, start with managed and migrate only when you hit framework limits.",
            "branches": [
                {"condition": "Data spans multiple legacy tables or external systems", "path": "Unmanaged. Custom persistence requires manual CREATE/UPDATE/DELETE. The framework cannot auto-generate SQL for multi-table or external persistence."},
                {"condition": "Must wrap existing BAPIs/RFCs with standard commit behavior", "path": "Unmanaged. BAPIs call COMMIT WORK internally, breaking RAP's managed transaction assumption. Implement BAPI calls in create/update methods, handle double-commit prevention via set_update_state."},
                {"condition": "Standard CRUD on single CDS-backed table with simple validations", "path": "Managed. Use managed scenario. Save ~80% boilerplate. Unmanaged is 10x more code for no additional benefit."}
            ],
            "staffPlusTip": "Unmanaged is the escape valve for the 20% of entities that don't fit the managed pattern. Start managed, migrate to unmanaged only when you hit a concrete framework limitation."
        }),
        ("Manual CRUD Implementation", "quantifiedTradeoff", {
            "title": "Development Cost vs Flexibility Tradeoff in Unmanaged CRUD",
            "variables": [
                {"name": "Entity count", "value": "10 entities", "source": "Order-to-cash business object family"},
                {"name": "Entity complexity", "value": "4 simple, 4 medium, 2 complex", "source": "Simple = 1 table, Medium = 3 tables, Complex = legacy BAPI"},
                {"name": "Team experience", "value": "2 engineers, 1 with RAP experience", "source": "Typical SAP development team"}
            ],
            "calculation": {
                "formula": "TotalDevCost = Sum(EntityComplexity × ImplementationDays) × DailyRate + MaintenanceCost",
                "managed": {"writeLatency": "N/A", "monthlyPenalty": "$36,000 — Managed: 10 entities × avg 3 days × $1,200/day = $36K. Draft + locking included. 80% less code."},
                "unmanaged": {"writeLatency": "N/A", "monthlyPenalty": "$132,000 — Unmanaged: 10 entities × avg 11 days × $1,200/day = $132K. Every CREATE/UPDATE/DELETE + locking + draft + save must be implemented manually."},
                "breakeven": "Unmanaged is 3.7x more expensive in development. It only makes financial sense when >60% of operations are custom — the managed framework would require so many workarounds that the productivity advantage disappears."
            }
        }),
        ("Custom Locking", "adversarialResponse", {
            "challenge": "\"Our custom locking in unmanaged RAP is causing frequent timeouts. Users report 'Object locked by user XYZ' even when that user's session ended hours ago.\"",
            "badResponse": "\"Increase the lock timeout parameter.\" (treats symptom, not cause)",
            "goodResponse": "\"Lock timeouts from stale locks indicate the enqueue was never released. This is a classic lock leak pattern. In unmanaged RAP, you must explicitly release locks via DEQUEUE calls — the framework does not auto-release them like managed scenario. The three most common causes: (1) The lock is acquired in the MODIFY method but not released in the error path. If an exception occurs after ENQUEUE but before SAVE, the DEQUEUE never runs. Wrap ENQUEUE calls in TRY/CATCH with CLEANUP block that calls DEQUEUE. (2) The user's ABAP session terminated abnormally (program dump, network disconnect). SAP's enqueue server has a 'lock timeout' (enque/delay_roll, default 60s) that cleans up locks from terminated sessions — but this only works if the enqueue entry has the correct _scope parameter. Ensure _scope = '1' (rollback release) not '2' (manual release). (3) You're using SAP standard lock objects but the lock module ENQUEUE_EZ_* requires a RFC destination that's unavailable. Check SM12 for orphaned lock entries and implement a cleanup job that runs every 5 minutes to release locks older than 30 minutes.\"",
            "pattern": "root-cause-triage — identify specific failure modes (error-path leaks, session termination, lock scope) with precise SAP parameter references, and provide both immediate cleanup and long-term prevention strategies."
        }),
        ("Integration with Existing BAPIs/RFCs", "decisionTree", {
            "prompt": "How should I integrate existing BAPIs into RAP unmanaged scenario?",
            "firstQuestion": "\"Does the BAPI commit internally or expect the caller to commit?\" If the BAPI calls BAPI_TRANSACTION_COMMIT internally, you must handle double-commit prevention. If it only fills BAPIRET2 tables, you control the commit via the RAP save sequence.",
            "branches": [
                {"condition": "BAPI calls COMMIT internally (most legacy BAPIs)", "path": "Call BAPI in create/update method, then call BAPI_TRANSACTION_COMMIT. Prevent framework double-commit via set_update_state( if_abap_behv=>update_state-committed ) in save method."},
                {"condition": "BAPI returns data, caller decides when to commit", "path": "Call BAPI in create/update method. Defer COMMIT to RAP save sequence. Map BAPIRET2 messages to failed/reported structures in the save method."},
                {"condition": "BAPI is read-only (no database changes)", "path": "Call in determination or validation. No commit handling needed. Map return messages to reported structure for user feedback."}
            ],
            "staffPlusTip": "BAPI integration in unmanaged RAP creates a transaction boundary challenge. The BAPI's internal commit and RAP's framework commit are two separate LUWs — you must prevent double-commit explicitly."
        }),
        ("Transaction Control", "quantifiedTradeoff", {
            "title": "Transaction Control — Framework-Managed vs Custom LUW Boundary",
            "variables": [
                {"name": "Transaction complexity", "value": "5 entities per save (1 parent + 4 children)", "source": "Business object composition depth"},
                {"name": "External system calls", "value": "2 BAPI calls per save", "source": "Legacy BAPI integration in create/update"},
                {"name": "Concurrent saves", "value": "50 saves/minute", "source": "Peak transaction load"}
            ],
            "calculation": {
                "formula": "LUWCost = (BAPITime + ABAPTime + DBTime) × TransactionCount",
                "managed_luw": {"writeLatency": "~50ms total per transaction", "monthlyPenalty": "$0 — Framework-managed LUW: auto-commit, auto-rollback, auto-buffering. 0 development cost for transaction control. Cannot integrate BAPIs that commit independently."},
                "unmanaged_luw": {"writeLatency": "~150ms (custom save sequence)", "monthlyPenalty": "$2,400 — Unmanaged: 50ms BAPI time + 50ms ABAP processing + 50ms DB commit = 150ms per save. Development cost: ~$12K for save/finalize_save/early_save implementation."},
                "breakeven": "Managed is always cheaper for pure-SAP scenarios. Unmanaged only adds value when BAPI integration is required — the cost of working around managed's transaction limitations exceeds the unmanaged implementation cost."
            }
        }),
        ("Transaction Control", "adversarialResponse", {
            "challenge": "\"Our unmanaged RAP transaction control is unreliable. Sometimes data is saved even when validation fails.\"",
            "badResponse": "\"Check your validation code.\" (dismissive, no systematic approach)",
            "goodResponse": "\"This is a critical issue — partial saves with failed validations indicate the save sequence is not properly halting on errors. Let me identify the likely causes: (1) You're calling COMMIT WORK in the create/update methods instead of deferring to the save method. In unmanaged RAP, only the save method should trigger database commits. If you call COMMIT in create, the data is committed before validations run. Move all DB writes to the save method. (2) Your save method doesn't check the failed table before proceeding. The framework checks failed before committing, but if you bypass the framework by calling COMMIT WORK inside save, you override this safeguard. Never call COMMIT WORK directly — let the framework handle it. (3) You have an early_save method that writes to the database but doesn't participate in rollback. If early_save fails, data written to the database is NOT automatically rolled back. Make early_save idempotent and use temporary tables that can be cleaned up on failure. (4) BAPI calls that commit internally are creating nested LUWs. Isolate BAPI calls with RFC destination 'NONE' to prevent them from committing your transaction context.\"",
            "pattern": "audit-and-fix — identify the specific transaction boundary violations (early COMMIT, unchecked failures, BAPI nesting) with exact code patterns to avoid, and provide a save sequence checklist."
        }),
        ("Draft Hand-Written Implementation", "decisionTree", {
            "prompt": "Should I implement custom draft handling in unmanaged RAP?",
            "firstQuestion": "\"Does your business object need draft support?\" If users need to save incomplete work and resume later, you need draft. If all operations are complete-and-done (batch, API-to-API), you don't need draft.",
            "branches": [
                {"condition": "Fiori UI requires draft for user experience", "path": "Implement custom draft. Must implement draft_create, draft_resume, draft_activate, draft_discard. Requires 4 methods and a dedicated draft persistence table. ~200 lines of code minimum."},
                {"condition": "API-to-API with no user interaction", "path": "Skip draft. Use direct create/update/delete without draft lifecycle. Simpler, faster, no draft table cleanup needed. Not suitable for Fiori UIs."},
                {"condition": "Need Fiori draft but unmanaged complexity is too high", "path": "Consider managed scenario instead. If 80%+ of your use case fits managed, use managed for the draft lifecycle and implement only custom logic via determinations/actions."}
            ],
            "staffPlusTip": "Custom draft in unmanaged is the most complex RAP implementation. If you need Fiori UI support, consider whether you can switch to managed scenario for the draft layer alone."
        }),
    ],
    "abap-amdp.json": [
        ("AMDP Class Design Patterns", "decisionTree", {
            "prompt": "How should I structure AMDP classes for maintainability?",
            "firstQuestion": "\"Is this AMDP a stateless, reusable procedure or a one-off data migration script?\" Stateless reusable procedures should be in dedicated AMDP classes with interfaces. One-off scripts can be inline AMDP methods.",
            "branches": [
                {"condition": "Reusable procedure called by multiple consumers", "path": "Dedicated AMDP class with interface. Define INTERFACE ZIF_AMDP_SALES with method declarations. Implement in ZCL_AMDP_SALES. Enables plan cache reuse and unit testing via test doubles."},
                {"condition": "One-off data migration or ad-hoc analysis", "path": "Inline AMDP method in the consuming class. Use BY DATABASE PROCEDURE directly in the report or migration class. Simpler, no interface overhead. Can be refactored later."},
                {"condition": "CDS Table Function implementation", "path": "AMDP class with BY DATABASE FUNCTION method. Must implement the exact signature defined by the CDS Table Function. The @ObjectModel annotations on the CDS side control optimizer behavior."}
            ],
            "staffPlusTip": "Stateless AMDP methods produce the same SQL text for the same inputs — maximizing HANA plan cache hit rate. Never use instance attributes in AMDP classes."
        }),
        ("SQLScript vs ABAP", "quantifiedTradeoff", {
            "title": "SQLScript vs ABAP — The Boundary Decision Cost",
            "variables": [
                {"name": "Data volume", "value": "1M rows", "source": "Month-end sales data processing"},
                {"name": "Network latency", "value": "0.5ms (LAN)", "source": "AS ABAP to HANA on same server"},
                {"name": "ABAP processing speed", "value": "50K rows/sec per WP", "source": "LOOP + internal table operations"}
            ],
            "calculation": {
                "formula": "TotalTime = DataTransferTime + (DataVolume / ProcessingSpeed)",
                "amdp_sqlscript": {"writeLatency": "2s total", "monthlyPenalty": "$0 — 1M rows processed entirely in HANA. Zero data transfer cost. HANA column store processes 1M rows in ~1-2 seconds for set-based operations. No ABAP work process consumed during execution."},
                "abap_loop": {"writeLatency": "22s total", "monthlyPenalty": "$180 — 0.5s network transfer + 20s ABAP loop time (1M/50K = 20s at 50K rows/sec) + 1.5s FOR ALL ENTRIES SELECTs. Consumes a DIA work process for 22 seconds — blocking other users."},
                "breakeven": "At 10K rows, AMDP is only 2x faster. At 1M rows, AMDP is 11x faster. The breakeven is ~5K rows where context switch overhead equals processing time savings. Below 5K rows, ABAP is simpler to write and debug."
            }
        }),
        ("Exception Handling in AMDP", "adversarialResponse", {
            "challenge": "\"Our AMDP exception handling is useless. When the AMDP fails, we get 'CX_AMDP_EXECUTION_ERROR' with a generic message. We can't tell which step failed.\"",
            "badResponse": "\"Catch the exception and show the full error text.\" (doesn't address the lack of granularity)",
            "goodResponse": "\"The generic error happens because HANA exceptions are opaque to the ABAP runtime by default — you only get the top-level error code. The fix is to add structured error handling inside your SQLScript. First, use DECLARE EXIT HANDLER FOR SQLEXCEPTION in your AMDP to catch database errors and SIGNAL a custom error code with a specific MESSAGE_TEXT that identifies the failing step. For example, SIGNAL sql_error_code 'Z_STEP_3_FAILED' SET MESSAGE_TEXT = 'Aggregation failed at step 3: ' || ::SQL_ERROR_MESSAGE. Second, add a debug mode parameter to your AMDP that logs intermediate results to a temporary table when active — this lets you trace the exact step that fails without modifying production code. Third, use SQLScript's MAP statement with default error handling for lookup failures. The pattern: IF <condition> THEN SIGNAL ... ELSE ... END IF. This turns a generic 'execution error' into a pinpoint diagnostic with the specific step, input values, and database error code.\"",
            "pattern": "proactive-instrumentation — address the root cause (opaque HANA errors) by adding structured SQLScript error handling with EXIT HANDLER, SIGNAL, and debug mode logging."
        }),
        ("CDS Table Function Integration", "decisionTree", {
            "prompt": "Should I implement this as a CDS Table Function or a standalone AMDP?",
            "firstQuestion": "\"Does the result need to be consumed by other CDS views, OData services, or analytics?\" If yes, use a CDS Table Function — it exposes the result as a CDS entity. If the result is only consumed by ABAP code, a standalone AMDP is simpler.",
            "branches": [
                {"condition": "Result consumed by CDS views, OData, or Fiori", "path": "CDS Table Function. Define the interface via define table function. Implement with BY DATABASE FUNCTION. Add @ObjectModel annotations for optimizer hints. Enables predicate pushdown and projection pruning."},
                {"condition": "Result consumed only by ABAP report or class", "path": "Standalone AMDP method. Simpler: no CDS view needed. Call directly via method call. Avoids CDS activation overhead during development."},
                {"condition": "Complex multi-step calculation with intermediate results", "path": "CDS Table Function with @ObjectModel.resultSetType: #CALCULATION_ENGINE. This annotation tells HANA to allocate sufficient memory and not to inline the function into outer queries."}
            ],
            "staffPlusTip": "CDS Table Function + AMDP implements the Strategy pattern at the database layer. The CDS view is the stable interface; the AMDP is the replaceable implementation."
        }),
        ("Memory Limits & Parallel Execution", "quantifiedTradeoff", {
            "title": "Memory vs Performance Tradeoff in Large AMDP Operations",
            "variables": [
                {"name": "Data volume", "value": "50M rows", "source": "Year-end financial data processing"},
                {"name": "Row width", "value": "200 bytes", "source": "Standard finance table row size"},
                {"name": "HANA memory limit", "value": "2GB statement_memory_limit", "source": "Default HANA parameter"}
            ],
            "calculation": {
                "formula": "MemoryRequired = RowCount × RowWidth + IntermediateResults × OverheadFactor",
                "in_memory": {"writeLatency": "30s (full in-memory processing)", "monthlyPenalty": "$0 — 50M × 200B = 10GB raw data + ~5GB intermediate = 15GB. Requires increasing statement_memory_limit from 2GB to 16GB. Parallel execution across 8 CPU cores."},
                "chunked_disk": {"writeLatency": "450s (chunked with disk spilling)", "monthlyPenalty": "$1,200 — Processing in 2GB chunks: 8 passes × ~55s each. Disk I/O for spilling intermediate results is 15x slower than in-memory. No DBA intervention needed."},
                "breakeven": "At <5GB total data, in-memory is always better. At 15GB+, the DBA cost of increasing statement_memory_limit ($500 one-time tuning) pays for itself after 3 months of monthly runs. At 50GB+, switch to chunked processing regardless of memory."
            }
        }),
        ("Memory Limits & Parallel Execution", "adversarialResponse", {
            "challenge": "\"Our AMDP crashes every month-end with 'SQL_ERROR_MEMORY_LIMIT_EXCEEDED' when processing the financial close.\"",
            "badResponse": "\"Ask the DBA to increase statement_memory_limit.\" (pushes responsibility, no architectural fix)",
            "goodResponse": "\"The memory limit error (SQL code 257) means your AMDP exceeds the 2GB default statement_memory_limit. There are three approaches, each with different tradeoffs: (1) Short-term fix: request DBA to increase statement_memory_limit to 8GB for the specific RFC user that runs this AMDP. Use ALTER USER SET STATEMENT MEMORY LIMIT. Risk: if another large query runs concurrently, HANA may OOM. (2) Architectural fix: rewrite the AMDP to process data in chunks. Add a WHILE loop in SQLScript that processes date ranges or material ranges, accumulating results with UNION ALL. This keeps each chunk under 2GB. The tradeoff: slightly slower (chunking overhead), but doesn't require DBA changes and works regardless of data growth. (3) Strategic fix: push aggregation to the database level. Instead of loading 50M detail rows into memory, use HANA's aggregate pushdown — GROUP BY at the table level, returning only summary rows. The SELECT only returns the aggregated result (~1K rows), avoiding the memory issue entirely. I recommend approach 2 for immediate relief and approach 3 for the permanent solution.\"",
            "pattern": "tiered-remediation — provide immediate tactical fix (DBA tuning), medium-term architectural fix (chunking), and long-term strategic fix (aggregate pushdown). Quantify the tradeoff of each approach."
        }),
        ("Debugging AMDP", "quantifiedTradeoff", {
            "title": "AMDP Debugging Tools — Time Investment vs Diagnostic Value",
            "variables": [
                {"name": "Debugging frequency", "value": "5 AMDP issues/month", "source": "Team of 8 developers"},
                {"name": "Developer hourly cost", "value": "$100/hour", "source": "Fully-loaded cost"},
                {"name": "Debugging time per issue", "value": "Varies by tool", "source": "Engineering estimate"}
            ],
            "calculation": {
                "formula": "MonthlyCost = IssuesPerMonth × (SetupTime + DiagnosticTime) × HourlyRate",
                "st05_trace": {"writeLatency": "5 minutes per debugging session", "monthlyPenalty": "$333 — 5 issues × (2min setup + 3min trace read) × $100/h = $42. Also captures SQL text, duration, and row counts. Best first step for any AMDP issue."},
                "adp_debugger": {"writeLatency": "30 minutes per session", "monthlyPenalty": "$2,000 — 5 issues × (5min setup + 25min stepping) × $100/h = $250. Step-by-step debugging is powerful but time-consuming. Use only when the trace shows unexpected intermediate results."},
                "plan_viz": {"writeLatency": "45 minutes per deep dive", "monthlyPenalty": "$3,750 — 5 issues × (10min setup + 35min analysis) × $100/h = $375. Use for performance issues only (memory spills, suboptimal join order, missing indexes). Not for logic bugs."},
                "breakeven": "ST05 trace is the most cost-effective first step for 80% of issues. Use PlanViz only when trace shows high duration but low row counts (index/join problem). Use ADT debugger only for logic bugs in complex stored procedures."
            }
        }),
    ],
    "abap-internal-tables.json": [
        ("Hash Table Collision Resolution", "decisionTree", {
            "prompt": "Should I use a HASHED table or a SORTED table for this lookup?",
            "firstQuestion": "\"Do you need O(1) key-based lookups independent of table size, or do you also need ordered iteration and range queries?\" HASHED gives O(1) lookups but no ordering. SORTED gives O(log N) lookups with ordering.",
            "branches": [
                {"condition": "Need O(1) key lookup, never iterate in order, never range search", "path": "HASHED table. O(1) amortized lookup. ~100MB memory for 1M entries. Rehash at load factor >0.75 causes latency spikes. INITIAL SIZE should be (expected rows / 0.75)."},
                {"condition": "Need ordered iteration or range-based key access", "path": "SORTED table. O(log N) lookup, O(1) sequential iteration. ~80MB memory for 1M entries. Supports READ TABLE ... WITH KEY ... >= value for range queries."},
                {"condition": "Need index-based access or sequential processing only", "path": "STANDARD table. O(1) index access. Lowest memory overhead (~40MB for 1M entries). O(N) key lookup — use secondary SORTED key if key lookups are needed."}
            ],
            "staffPlusTip": "For large tables (>100K entries), HASHED is optimal for pure key lookups. For tables <10K entries, the O(log N) vs O(1) difference is negligible — use SORTED for flexibility."
        }),
        ("Secondary Key Index Construction", "quantifiedTradeoff", {
            "title": "Secondary Key — Read Performance vs Write Amplification",
            "variables": [
                {"name": "Table size", "value": "500K entries", "source": "Material master export table"},
                {"name": "Reads per second", "value": "100/sec (key-based)", "source": "Production order BOM explosion"},
                {"name": "Writes per second", "value": "10/sec (INSERT + MODIFY)", "source": "Material master update from legacy system"}
            ],
            "calculation": {
                "formula": "TotalCost = ReadCost × ReadCount + WriteCost × WriteCount",
                "no_secondary": {"writeLatency": "0ms extra (no index maintenance)", "monthlyPenalty": "$0 — O(N) reads take ~250K comparisons on average = 5ms. 100 reads/s × 5ms = 500ms/s CPU. No write penalty."},
                "with_secondary": {"writeLatency": "1ms extra per write (O(log N) index update)", "monthlyPenalty": "$1,200 — O(log N) reads take ~19 comparisons = 0.04ms. 100 reads/s × 0.04ms = 4ms/s CPU. Each write: 1ms extra × 10/s = 10ms/s."},
                "breakeven": "At 100:1 read/write ratio (your scenario), secondary key saves 496ms/s of CPU at a cost of 10ms/s — net 486ms/s savings. At 10:1 read/write ratio, the savings shrink to 46ms/s. At 1:1 ratio (equal reads/writes), there's no net benefit — use no secondary key."
            }
        }),
        ("GROUP BY & FILTER Operations", "decisionTree", {
            "prompt": "Should I use GROUP BY or procedural LOOP for aggregating internal table data?",
            "firstQuestion": "\"Is the aggregation a simple SUM/COUNT with one or two group keys, or does it require complex multi-pass logic?\" Simple aggregation = GROUP BY. Complex logic with conditionals = LOOP with inline accumulation.",
            "branches": [
                {"condition": "Simple SUM/COUNT aggregation on sorted or unique group key", "path": "GROUP BY via VALUE #( FOR GROUPS ... ). Hash-based grouping O(N). Acceptable for tables up to ~1M entries. Shorter code, fewer bugs."},
                {"condition": "Complex multi-pass logic with conditionals per group", "path": "LOOP + inline accumulation. More control for complex business rules. Pre-sort by group key to avoid hash table overhead."},
                {"condition": "Need filtered subset without copying data", "path": "FILTER ALL OF. Lazy-evaluated view — no data copy. Use with FILTER IN (hash-based) for large filter tables. O(N+M) performance."}
            ],
            "staffPlusTip": "GROUP BY is hash-based for STANDARD/HASHED tables and sort-based for SORTED tables. Pre-sorting by group key before GROUP BY makes it O(N) instead of O(N log N)."
        }),
        ("GROUP BY & FILTER Operations", "quantifiedTradeoff", {
            "title": "GROUP BY vs LOOP — Computational Cost Comparison",
            "variables": [
                {"name": "Table size", "value": "100K rows", "source": "Monthly sales data export"},
                {"name": "Group count", "value": "5,000 unique groups", "source": "Sales by company code + fiscal year"},
                {"name": "Aggregation", "value": "SUM(amount) + COUNT(items)", "source": "Standard financial aggregation"}
            ],
            "calculation": {
                "formula": "AggregationCost = BuildCost + ProbeCost",
                "group_by_declarative": {"writeLatency": "15ms total", "monthlyPenalty": "$0 — Hash-based: build hash on group key (5ms) + probe all 100K rows (10ms). ~100 lines of code replaced by 1 expression. No mutation bugs."},
                "loop_procedural": {"writeLatency": "85ms total", "monthlyPenalty": "$0 — LOOP + READ TABLE on unsorted table: 100K loops × ~0.85μs each = 85ms. ~25 lines of code. Higher risk of bugs (uninitialized accumulators, missing group handling)."},
                "breakeven": "GROUP BY is 5.7x faster at 100K rows. At 1K rows, both take ~1-2ms — use LOOP for readability with small tables. At 1M rows, GROUP BY is 10x+ faster and should always be preferred."
            }
        }),
        ("FOR Expressions", "adversarialResponse", {
            "challenge": "\"Your FOR expressions are too complex and hard to debug. I can't set breakpoints inside a VALUE #( FOR ... ) expression.\"",
            "badResponse": "\"FOR expressions are best practice. You should learn to read them.\" (dismissive, no empathy)",
            "goodResponse": "\"I understand the debugging concern — FOR expressions are single-line constructs that can't be stepped into with the debugger. This is a valid tradeoff. Let me suggest a pragmatic approach: (1) Start simple — use FOR expressions for straightforward transformations (map, filter, simple aggregation). Keep them to 5 lines or fewer. (2) For complex logic, extract the transformation into a helper method that returns the result. Call the helper from the FOR expression — you can set breakpoints in the helper. (3) Use a two-phase approach during development: write the logic as a LOOP first (debuggable), verify correctness, then refactor to FOR expression (production). Keep the LOOP version as a comment for future debugging. (4) If you have ABAP 7.55+, use the REDUCE operator with inline LET expressions — these are still functional but can be broken into smaller, testable pieces. The key insight: FOR expressions reduce bugs in production (no mutation issues) at the cost of harder debugging. For a team with junior developers, use FOR only for simple cases and keep LOOPs for complex logic.\"",
            "pattern": "empathy-with-pragmatic-migration — acknowledge the debugging pain, provide incremental adoption strategy, and suggest testing patterns that compensate for the debugging limitation."
        }),
        ("Memory Pressure Behavior", "quantifiedTradeoff", {
            "title": "Memory Pressure — Heap vs Extended Memory Cost of Large Internal Tables",
            "variables": [
                {"name": "Table size", "value": "2M entries", "source": "Year-end material document extract"},
                {"name": "Row width", "value": "150 bytes", "source": "Standard document structure"},
                {"name": "Work process heap limit", "value": "200MB", "source": "abap/heap_area_dia default"}
            ],
            "calculation": {
                "formula": "MemoryUsed = (RowCount × RowWidth) + InternalOverhead × StructureFactor",
                "standard_table": {"writeLatency": "~310MB total", "monthlyPenalty": "$0 — 2M × 150B = 300MB data + ~10MB block overhead = 310MB. Exceeds 200MB heap limit → rolls out to extended memory. Roll-out adds ~50ms latency per dialog step."},
                "sorted_table": {"writeLatency": "~350MB total", "monthlyPenalty": "$0 — 300MB data + ~50MB B-tree index overhead. Higher memory but supports binary search without secondary index."},
                "hashed_table": {"writeLatency": "~480MB total", "monthlyPenalty": "$0 — 300MB data + ~180MB hash table overhead (buckets + chaining pointers). Exceeds heap + extended memory → TSV_TNEW_PAGE_ALLOC_FAILED dump."},
                "breakeven": "Below 500K entries (75MB data), all table types fit in heap. Between 500K-1.5M entries, STANDARD is most memory-efficient. Above 1.5M entries, use STANDARD with PACKAGE SIZE processing — never load the full table into memory."
            }
        }),
        ("Memory Pressure Behavior", "adversarialResponse", {
            "challenge": "\"Our production system crashed with TSV_TNEW_PAGE_ALLOC_FAILED because a background job loaded too much data into an internal table. We lost 2 hours of processing.\"",
            "badResponse": "\"We should increase abap/heap_area_dia.\" (band-aid, no systemic fix)",
            "goodResponse": "\"TSV_TNEW_PAGE_ALLOC_FAILED means the work process heap is exhausted. Increasing the limit just delays the problem — data volumes grow, and the crash returns. Let me implement a three-layer defense: (1) Immediate fix — add a row count check before loading: IF expected_rows > 100000 THEN RAISE EXCEPTION TYPE cx_capacity_exceeded. This fails fast with a meaningful error instead of crashing the work process. (2) Architectural fix — rewrite the job to use PACKAGE SIZE processing: SELECT ... PACKAGE SIZE 10000 INTO TABLE @lt_chunk. Process each chunk, free memory with FREE lt_chunk, then fetch the next chunk. This limits peak memory to 10K rows regardless of total data volume. (3) Monitoring — add memory usage tracking at the start of each batch step using cl_abap_runtime=>get_used_heap_size( ). If usage exceeds 80% of the heap limit, log a warning and activate data throttling. The systemic lesson: never write SELECT * INTO TABLE without a UP TO or PACKAGE SIZE guard in production jobs.\"",
            "pattern": "defense-in-depth — implement immediate fail-fast protection, architectural redesign for bounded memory, and proactive monitoring. The Staff+ signal is preventing the same class of failure across all batch jobs, not fixing one instance."
        }),
        ("Table Type Decision Framework", "decisionTree", {
            "prompt": "How should I merge two internal tables efficiently?",
            "firstQuestion": "\"Are both tables sorted by the join key?\" If yes, use the MERGE statement (O(N+M)). If not, you must sort first or use a LOOP + READ TABLE pattern.",
            "branches": [
                {"condition": "Both tables sorted by the same key", "path": "MERGE statement. O(N+M) — single pass over both tables. ~5 lines of code. Must have same key order and direction (ASC/DESC). Best performance for sorted data."},
                {"condition": "Only one table sorted, other has unique key", "path": "LOOP on sorted table + READ TABLE on hashed/secondary key. O(N log M) for sorted-secondary key or O(N) for hashed key. Convert unsorted table to HASHED or add secondary SORTED key."},
                {"condition": "Neither table sorted, both large (>50K)", "path": "Sort both tables by the key first (O(N log N + M log M)), then use MERGE (O(N+M)). The sort cost is worth it — the MERGE on sorted data is 10x faster than nested LOOP."}
            ],
            "staffPlusTip": "The classic ABAP nesting LOOP ... READ TABLE is O(N × log M). MERGE on sorted tables is O(N+M). For tables >10K rows, always sort first then MERGE. The sort overhead pays off after ~1K iterations."
        }),
    ],
    "abap-oop.json": [
        ("Abstract vs Interface Decision Framework", "decisionTree", {
            "prompt": "Should I use an abstract class or an interface for this API?",
            "firstQuestion": "\"Do the implementers share common state or behavior?\" If yes, abstract class (inheritance + shared code). If they only share a contract (different implementations, no shared code), use interface.",
            "branches": [
                {"condition": "Implementers share state (attributes) and default behavior", "path": "Abstract class. Use for template method pattern. Protected attributes + abstract methods. Adding a concrete method is non-breaking. Single inheritance only."},
                {"condition": "Unrelated classes need the same contract but no shared code", "path": "Interface. Multiple implements allowed. Pure contract — no state, no implementation. Adding a method breaks all implementations. Use for published APIs and BADIs."},
                {"condition": "Both shared behavior AND multiple-type contract needed", "path": "Abstract class implementing interface. Best of both: abstract class provides shared state + default methods. Interface provides the polymorphic contract. Common ABAP pattern for BADI base classes."}
            ],
            "staffPlusTip": "In ABAP, interfaces are the only way to achieve multiple-type inheritance. Use interfaces for stable published APIs. Use abstract classes for internal framework code where adding methods shouldn't break consumers."
        }),
        ("Factory Pattern & Dynamic Runtime Type Creation", "decisionTree", {
            "prompt": "Should I use a factory pattern for creating this object?",
            "firstQuestion": "\"Does the caller know the exact concrete class at compile time?\" If yes, direct instantiation (NEW/ CREATE OBJECT) is simpler. If the class depends on runtime configuration, input data, or customizing, use a factory.",
            "branches": [
                {"condition": "Class determined by customizing table or configuration", "path": "Factory with dynamic type creation. CREATE OBJECT ro_instance TYPE (lv_class_name). Class name from customizing table. No compile-time dependency. Enables plugin architecture."},
                {"condition": "Object creation requires complex parameter validation or dependency injection", "path": "Factory method with constructor injection. Factory validates parameters, creates dependencies, and wires them via constructor injection. Caller gets a fully-initialized object."},
                {"condition": "Simple creation with known concrete class", "path": "Direct instantiation (NEW cls( )). No factory overhead. ~1 line of code. Prefer this unless you anticipate needing subclass swapping in the future."}
            ],
            "staffPlusTip": "Factory pattern enables the Open/Closed Principle — open for extension (new classes via customizing), closed for modification (no changes to calling code). Essential for SaaS extension frameworks."
        }),
        ("Dependency Injection in ABAP", "adversarialResponse", {
            "challenge": "\"ABAP has no Spring or Guice framework. Dependency injection is over-engineered for ABAP. Just call the function module directly.\"",
            "badResponse": "\"ABAP needs a DI framework. SAP should build one.\" (defensive, no practical solution)",
            "goodResponse": "\"You're right that ABAP lacks a built-in DI container, but the principles still apply and there are pragmatic ABAP-native ways to implement DI. The value isn't the framework — it's the testability. When you CALL FUNCTION 'BAPI_SALESORDER_CREATE' directly in your method, you cannot unit test that method without creating test data in the database. Here's the pragmatic approach without a framework: (1) Use constructor injection with interfaces. Define an interface IF_SALESORDER_CREATOR with a create method. Implement CL_SALESORDER_CREATOR that calls the BAPI. Your business class receives IF_SALESORDER_CREATOR in its constructor. (2) For unit tests, implement CL_MOCK_SALESORDER_CREATOR that returns canned responses. Inject it instead. (3) Use a factory class (not a DI container) to wire production dependencies. The factory is the only place that knows the concrete classes. Total overhead: one interface, two implementations, one factory — ~100 lines of boilerplate for the entire application. Not over-engineering — it's the minimum investment for testability. For large projects, there's also CL_OSQL_REPLACE for replacing database tables with test doubles in Open SQL statements without any DI wiring.\"",
            "pattern": "pragmatic-minimalism — acknowledge the lack of framework, provide a lightweight ABAP-native alternative (constructor injection + factory), quantify the overhead (100 lines), and connect to the specific benefit (unit testability)."
        }),
        ("Observer Pattern in SAP", "decisionTree", {
            "prompt": "Should I use ABAP events, BADIs, or direct method calls for this notification?",
            "firstQuestion": "\"How many handlers need to react to this event?\" 1-2 handlers = direct call or BADI. 3+ handlers = ABAP events or enhanced BADI. If handlers vary by customer/context, use BADIs with filter conditions.",
            "branches": [
                {"condition": "Single handler, tightly coupled", "path": "Direct method call. Simplest, fastest. O(1) dispatch. Use when the caller and handler are in the same class or closely related classes. No decoupling benefit needed."},
                {"condition": "Multiple handlers, same enhancement spot, varying by customer", "path": "BADI (Business Add-In). CL_EXITHANDLER manages multiple implementations with filter-based subscription. Use GET BADI + CALL BADI pattern. Supports activation/deactivation per customer."},
                {"condition": "Multiple handlers, decoupled architecture, no SAP enhancement framework", "path": "ABAP events (RAISE EVENT + SET HANDLER). Synchronous multicast. Handlers in registration order. Use for internal application events where handler composition is known at design time."}
            ],
            "staffPlusTip": "BADIs are the SAP-standard observer pattern for customer enhancements. ABAP events are better for internal application-level decoupling. Prefer BADIs for customer-facing extensibility; prefer events for internal architecture."
        }),
        ("Casting Rules — UPCAST vs DOWNCAST", "adversarialResponse", {
            "challenge": "\"Your design uses too many interface casts. The code is full of 'lo_instance ?= lo_interface' and half of them dump at runtime.\"",
            "badResponse": "\"You need to use TRY/CATCH around all downcasts.\" (correct but insufficient — doesn't address the design issue)",
            "goodResponse": "\"Frequent downcasts are a design smell, not just a coding issue. Every ?= cast means the static type (interface) doesn't provide enough information — you're doing runtime type detection. Let me fix this systematically: (1) First, audit where the downcasts happen. If you're downcasting from if_some in 10 places, it means the interface is too generic — add specific methods to the interface to eliminate the casts. For example, instead of downcasting to call get_currency(), add get_currency() to the interface. (2) For the remaining unavoidable downcasts (e.g., factory returns an interface and you need a specific subtype), use the IS INSTANCE OF pattern: IF lo_instance IS INSTANCE OF zcl_concrete. lo_concrete ?= lo_instance. ENDIF. This is clearer than bare TRY/CATCH. (3) For polymorphic dispatch, replace the downcast + CALL METHOD pattern with a method on the interface itself. Instead of downcasting to check the type, add a get_type( ) method or use the VISITOR pattern. (4) Only use TRY/CATCH ?= for truly exceptional cases where the type is genuinely unknown at design time. The goal: zero downcasts in business logic, only in factory/deserialization code.\"",
            "pattern": "smell-driven-refactoring — identify the root cause (overly generic interfaces), provide a systematic fix (add methods to interfaces, use IS INSTANCE OF pattern, replace type-dispatch with polymorphic dispatch), and set a measurable goal (zero downcasts in business logic)."
        }),
        ("ABAP 7.4+ Functional Programming", "quantifiedTradeoff", {
            "title": "Builder Pattern — Code Overhead vs API Clarity Tradeoff",
            "variables": [
                {"name": "Object complexity", "value": "15+ optional parameters", "source": "Sales order create API with pricing, shipping, text, and conditions"},
                {"name": "Usage frequency", "value": "500 calls/day", "source": "Integration layer receiving orders from e-commerce"},
                {"name": "Parameter combinations", "value": "200+ valid combinations", "source": "Optional pricing + optional shipping + optional text combinations"}
            ],
            "calculation": {
                "formula": "TotalCost = DevelopmentCost + (MisuseCost × ErrorRate × UsageCount)",
                "builder": {"writeLatency": "1 day to implement (100 lines)", "monthlyPenalty": "$1,200 — Builder: 1 dev day = $1,200. Builder ensures only valid parameter combinations compile. Chainable set methods with compile-time validation. ~2 lines per call."},
                "constructor": {"writeLatency": "0 additional days", "monthlyPenalty": "$13,500 — Constructor with 15 parameters: 0 dev days for the pattern, but 15+ parameters in constructor = high misuse rate. Estimated 3% of calls have wrong parameter order = 15 errors/day × 30min debugging = $3,600/month in developer time + $9,900 in production issues."},
                "breakeven": "Builder pays for itself at 5+ optional parameters or 100+ calls/day. Below that, a constructor with documentation is sufficient. At 15+ parameters, builder is the minimum viable pattern — the constructor option is not realistically maintainable."
            }
        }),
    ],
    "abap-opensql.json": [
        ("FOR ALL ENTRIES Execution Plan Analysis", "quantifiedTradeoff", {
            "title": "FOR ALL ENTRIES — Cardinality Cost Analysis",
            "variables": [
                {"name": "Driving table size", "value": "10K entries", "source": "Material document header keys from batch job"},
                {"name": "Batch size", "value": "500 (rsdb/max_blocking_factor)", "source": "Default SAP profile parameter"},
                {"name": "Rows per FAE call", "value": "50 items per header on average", "source": "Item-to-header ratio"}
            ],
            "calculation": {
                "formula": "TotalCost = Ceiling(DrivingTableSize / BatchSize) × (QueryCost + DataTransferCost)",
                "fae_10k": {"writeLatency": "~2s total (20 queries)", "monthlyPenalty": "$450 — 10K entries / 500 batch = 20 queries. Each query: OR-expanded WHERE with 500 conditions. Average execution: 100ms per query. 20 queries × 100ms = 2s. Network: 20 round-trips × 0.5ms = 10ms."},
                "join_itab": {"writeLatency": "~150ms (1 query)", "monthlyPenalty": "$0 — Single query using JOIN @itab syntax (ABAP 7.40+). HANA receives a table-valued parameter. One query, one round-trip. 150ms total execution."},
                "breakeven": "FAE is faster than JOIN @itab only when the driving table has <100 entries (1 batch). At 500 entries (1 batch), both are similar. Above 500 entries, JOIN @itab is 5-13x faster. At 50K+ entries, FAE can cause database statement buffer overflow."
            }
        }),
        ("FOR ALL ENTRIES Execution Plan Analysis", "adversarialResponse", {
            "challenge": "\"Our FOR ALL ENTRIES query is killing the database. The HANA CPU spikes to 100% every time this report runs.\"",
            "badResponse": "\"Add more indexes to the database table.\" (doesn't address the root cause — FAE's OR expansion)",
            "goodResponse": "\"FOR ALL ENTRIES with a large driving table generates OR-expanded SQL that overwhelms the HANA optimizer. The CPU spike happens because the optimizer tries to find an optimal plan for a WHERE clause with thousands of OR conditions — it often gives up and does a full table scan. The fix depends on the driving table size: (1) If the driving table has <500 entries, add an index on the joined field AND increase rsdb/max_blocking_factor to match — this keeps FAE in a single batch. (2) If 500-10K entries, replace FAE with JOIN @itab (ABAP 7.40+). The syntax: SELECT ... FROM mseg JOIN @lt_mkpf AS mkpf ON mseg~mblnr = mkpf~mblnr. This sends the driving table as a table-valued parameter — the optimizer handles it as a single query with an optimal plan. (3) If >10K entries, use manual batching: split the driving table into chunks of 500 and loop over FAE calls. This keeps each batch within reasonable limits while avoiding the memory overhead of a single massive JOIN. I recommend option 2 for immediate relief — one code change, measurable CPU reduction.\"",
            "pattern": "cardinality-tiered-solution — identify the root cause (OR expansion at scale), provide three tiered solutions based on driving table size, and recommend the best option with quantified improvement."
        }),
        ("Subquery Factoring (WITH clause) and CDS Views", "decisionTree", {
            "prompt": "Should I use a WITH clause (CTE), a CDS view, or a nested subquery?",
            "firstQuestion": "\"Is this subquery reused multiple times in the same statement?\" If reused, WITH clause or CDS view. If used once, nested subquery or inline CDS reference is simpler.",
            "branches": [
                {"condition": "Subquery used multiple times in the same statement", "path": "WITH clause (CTE). Named subquery, factored once, referenced multiple times. HANA may materialize or inline based on cardinality. Best for complex analytics with shared sub-expressions."},
                {"condition": "Subquery used by multiple different programs/reports", "path": "CDS view. Reusable across the entire system. Compiled once, cached in HANA's plan cache. Supports annotations, DCL, and OData exposure. The standard ABAP approach for shared data models."},
                {"condition": "Subquery used once, simple enough for inline expression", "path": "Nested subquery (scalar or EXISTS). Simple, self-contained. No reuse needed. Use for single-use filter conditions like WHERE EXISTS (SELECT ...)."}
            ],
            "staffPlusTip": "CDS views are the preferred reusable data model in modern ABAP. Use WITH clauses for statement-local factoring. Use nested subqueries for single-use filters. Avoid deeply nested subqueries — they hurt readability and optimizer performance."
        }),
        ("Open SQL to HANA SQL Translation", "quantifiedTradeoff", {
            "title": "UNION vs Multiple SELECTs — Database vs Application Layer Set Combination",
            "variables": [
                {"name": "Source tables", "value": "3 (sales, purchases, transfers)", "source": "Combined material movement report"},
                {"name": "Rows per source", "value": "50K each", "source": "Monthly document volume"},
                {"name": "Client-side processing", "value": "ABAP LOOP + APPEND", "source": "Traditional pattern"}
            ],
            "calculation": {
                "formula": "TotalTime = QueryExecutionTime + DataTransferTime + SortTime",
                "sql_union": {"writeLatency": "~750ms total (1 query)", "monthlyPenalty": "$0 — Single SELECT with UNION ALL: HANA executes 3 branches in parallel (each ~200ms) + merge (150ms) = ~750ms. One round-trip. Result is already sorted if ORDER BY is specified."},
                "multiple_selects": {"writeLatency": "~3s total (3 queries + ABAP merge)", "monthlyPenalty": "$180 — 3 separate SELECTs: each returns 50K rows + 3 round-trips (1.5ms) + ABAP APPEND + SORT (50-150ms) = ~3s total. 3x more network data transfer. Three times the work process time."},
                "breakeven": "UNION is 4x faster at 150K total rows and the gap grows with data volume. For <5K total rows (small config data), multiple SELECTs are simpler to code. For any report >10K rows, UNION is both faster and cleaner."
            }
        }),
        ("Native SQL Pitfalls", "decisionTree", {
            "prompt": "Should I use Native SQL (ADBC) or Open SQL for this database access?",
            "firstQuestion": "\"Does the query require database-specific features that Open SQL doesn't support?\" If you need window functions, MERGE, full-text search, or HANA-specific optimizations, Native SQL is necessary. Otherwise, prefer Open SQL.",
            "branches": [
                {"condition": "Need HANA-specific features (window functions, full-text, spatial)", "path": "ADBC (CL_SQL_STATEMENT). Modern, catchable exceptions (CX_SQL_EXCEPTION). Prepared statements prevent SQL injection. ST05 traceable. Always close result sets with CLOSE( )."},
                {"condition": "Standard CRUD with DDIC integration needed", "path": "Open SQL. DDIC checks at compile time, automatic client handling, authorization checks, table buffering. Preferred for 95% of use cases. Use ADBC only when you hit a specific Open SQL limitation."},
                {"condition": "Need EXEC SQL (legacy code maintenance only)", "path": "EXEC SQL. Avoid in new development. No syntax check, no trace, no exception handling. Risks: no prepared statements (SQL injection), hard-to-debug runtime dumps. Migrate to ADBC or Open SQL."}
            ],
            "staffPlusTip": "ADBC is the only safe way to use native SQL in ABAP. EXEC SQL should never appear in new code. The rule: Open SQL by default, ADBC when needed, EXEC SQL never."
        }),
        ("Native SQL Pitfalls", "adversarialResponse", {
            "challenge": "\"We use EXEC SQL everywhere because it's faster than Open SQL. Our senior developer insists it's the only way to get real HANA performance.\"",
            "badResponse": "\"EXEC SQL is dangerous. You must stop using it.\" (dogmatic, doesn't address the performance belief)",
            "goodResponse": "\"I understand the performance concern — EXEC SQL sends SQL directly to HANA without the DBSL translation overhead. However, the performance difference is negligible (usually <1ms per query) compared to the risks. Let me address the belief with data: (1) Modern Open SQL translates very efficiently to HANA — the DBSL layer adds ~0.1-0.5ms per query. For a report that executes 100 queries, that's 10-50ms total overhead — invisible to users. (2) EXEC SQL is invisible to ST05 trace, meaning you can't performance-analyze it. If an EXEC SQL query is slow, you have no way to find out why. (3) EXEC SQL has zero compile-time checks — typos in table names are only caught at runtime, causing production dumps. (4) ADBC provides the same direct HANA access with proper error handling, prepared statements (SQL injection protection), and ST05 traceability. My recommendation: migrate all EXEC SQL to ADBC as a first step (one-to-one replacement, minimal risk), then evaluate which queries can be migrated to Open SQL for DDIC integration. The performance myth is not worth the operational risk.\"",
            "pattern": "data-driven-refutation — acknowledge the belief, provide counter-evidence with specific numbers (<1ms overhead), highlight the hidden costs (no traceability, no error handling), and propose a phased migration (EXEC SQL → ADBC → Open SQL)."
        }),
        ("JOIN vs SELECT + LOOP Decision", "quantifiedTradeoff", {
            "title": "Bulk INSERT/UPDATE — Row-by-Row vs Batch Performance",
            "variables": [
                {"name": "Record count", "value": "50,000 records", "source": "Daily bank statement upload"},
                {"name": "Table columns", "value": "30 columns", "source": "Standard finance document table"},
                {"name": "Database round-trip", "value": "0.5ms (LAN)", "source": "AS ABAP to HANA on same host"}
            ],
            "calculation": {
                "formula": "BatchTime = RecordCount × (RoundTripTime / BatchSize + PerRecordSQLTime)",
                "row_by_row": {"writeLatency": "~250s total", "monthlyPenalty": "$4,500 — 50,000 × (1 MODIFY + 1 COMMIT) = 100,000 round-trips × 0.5ms = 50s + 50,000 × 4ms per MODIFY = 200s. Work process blocked for 4+ minutes."},
                "batch_1000": {"writeLatency": "~25s total", "monthlyPenalty": "$450 — 50 batches × 1000 = 50 round-trips × 0.5ms = 0.025s + 50,000 × 0.5ms per row in batch = 25s. MODIFY TABLE with batch of 1000. 10x faster than row-by-row."},
                "batch_5000": {"writeLatency": "~15s total", "monthlyPenalty": "$0 — 10 batches × 5000 = 10 round-trips × 0.5ms = 0.005s + 50,000 × 0.3ms per row = 15s. Optimal batch size for standard tables. Above 5000, database lock escalation may occur."},
                "breakeven": "Batch of 5000 is 16.7x faster than row-by-row. Even batch of 100 is 5x faster. Always batch bulk operations. The optimal batch size is 1000-5000 rows — below that, round-trip overhead dominates; above that, database lock escalation may occur."
            }
        }),
    ],
    "abap-odata.json": [
        ("OData V2 vs V4 Decision", "decisionTree", {
            "prompt": "Should I use OData V2 or V4 for this service?",
            "firstQuestion": "\"What is the primary client type?\" Fiori Elements / SAPUI5 = V4 is preferred (RAP-generated). Legacy mobile apps / existing SAP Gateway integrations = V2 for backward compatibility.",
            "branches": [
                {"condition": "New Fiori Elements app with RAP backend", "path": "OData V4 with RAP. Built-in $apply aggregation, reduced payload (JSON), nested $expand with $filter. V4 reduces roundtrips by 60% for aggregation-heavy workloads."},
                {"condition": "Existing SAP Gateway custom service with complex DPC/MPC", "path": "OData V2. Migration to V4 would require full service rewrite. V2 is stable and well-supported. Upgrade when the service undergoes major redesign."},
                {"condition": "Mobile or low-bandwidth clients", "path": "OData V4. JSON format reduces payload by 30-50% vs V2 Atom. Built-in delta tracking and server-side paging with @nextLink. Better for unreliable networks."}
            ],
            "staffPlusTip": "SAP's direction is V4 with RAP. New development should be V4 by default. V2 is for maintenance of existing services. The payload savings alone (30-50%) justify V4 for high-throughput scenarios."
        }),
        ("Deep Entity Operations", "quantifiedTradeoff", {
            "title": "Deep Entity Operations — N+1 Query Cost vs Batch Cost",
            "variables": [
                {"name": "Parent entities per request", "value": "50", "source": "Sales order batch sync from e-commerce"},
                {"name": "Children per parent", "value": "10 line items", "source": "Average order size"},
                {"name": "Navigation depth", "value": "3 levels (order → items → schedules)", "source": "Multi-level BOM"}
            ],
            "calculation": {
                "formula": "TotalQueries = Levels × (EntityCount + ExpandFactor)",
                "deep_with_expand": {"writeLatency": "~3 queries for full tree", "monthlyPenalty": "$0 — Optimized: 1 query fetches all headers, 1 query fetches all items (FOR ALL ENTRIES), 1 query fetches all schedules. ~150ms total. 3 round-trips regardless of depth."},
                "n_plus_one": {"writeLatency": "1 + 50 + 500 = 551 queries", "monthlyPenalty": "$6,000 — Naive: 1 for headers + 50 for items + 500 for schedules = 551 round-trips × 2ms = 1.1s network alone + query execution = ~6s total. At 100 concurrent requests, this saturates the database connection pool."},
                "breakeven": "Optimized deep expand is 40x faster at 3 levels of depth. Even at 1 level (parent + children), the optimized approach (2 queries) is 25x faster than N+1 (1+50=51 queries). Always implement batch loading for $expand."
            }
        }),
        ("Custom vs RAP-Generated Decision", "adversarialResponse", {
            "challenge": "\"Our deep insert for sales orders is unreliable. Sometimes the header is created but the items fail, and we end up with orphan headers.\"",
            "badResponse": "\"Wrap the deep insert in a BAPI instead of using OData.\" (workaround, doesn't fix the OData service)",
            "goodResponse": "\"Orphan headers on deep insert failure mean the operation is not atomic. In OData V2 custom services, the parent and child creates are separate operations — if a child fails after the parent commits, there's no automatic rollback. The fix depends on your stack: (1) If using RAP (OData V4), the framework automatically wraps deep operations in a single LUW — if any child fails, the entire operation rolls back. Confirm your BDEF uses managed scenario. (2) If using custom SAP Gateway (V2), you must implement manual transaction handling: execute all creates in a temporary buffer, validate everything, then commit with COMMIT WORK. If any step fails, call ROLLBACK WORK and return a meaningful error. Use a 'savepoint' pattern — write header with status 'PENDING', write items, then update header to 'COMPLETE'. A cleanup job removes any records stuck in 'PENDING' for >1 hour. (3) Add idempotency keys to the request — if the client retries after a timeout, the service should detect the duplicate and return the existing result instead of creating a duplicate header.\"",
            "pattern": "atomicity-restoration — identify the root cause (atomicity gap in non-RAP OData), provide stack-specific solutions (RAP LUW vs custom transaction handling), and add defense mechanisms (savepoints, cleanup jobs, idempotency keys)."
        }),
        ("Batch Operations", "quantifiedTradeoff", {
            "title": "OData Batch — Throughput Improvement vs Complexity Cost",
            "variables": [
                {"name": "Operations per batch", "value": "50", "source": "Mobile app sync of 50 sales orders"},
                {"name": "Individual request time", "value": "150ms each", "source": "Average OData CRUD latency"},
                {"name": "Network round-trip", "value": "50ms (WAN, mobile client)", "source": "4G network from warehouse"}
            ],
            "calculation": {
                "formula": "BatchSavings = IndividualTotalTime - BatchTotalTime",
                "individual_requests": {"writeLatency": "50 × 150ms + 50 × 50ms = 10s total", "monthlyPenalty": "$9,000 — 50 sequential requests: each adds 50ms network + 150ms processing = 200ms × 50 = 10,000ms. Mobile connection may not survive 10s of continuous requests."},
                "batched_request": {"writeLatency": "50 × 150ms + 1 × 50ms = 7.55s total", "monthlyPenalty": "$1,200 — Single batch with 50 operations: 1 round-trip (50ms) + 50 × 150ms serialized = 7,550ms. 24% improvement over individual. But main benefit is reliability — 1 request vs 50."},
                "parallel_batch": {"writeLatency": "Max(10ms batch overhead + 150ms processing) = 160ms", "monthlyPenalty": "$0 — SAP Gateway processes change sets sequentially within a changeset but can parallelize independent change sets. 5 changesets × 10 ops = 5 parallel tracks × 150ms = ~160ms total. 62x faster than individual."},
                "breakeven": "Batch always wins for >3 operations. The breakeven is at 3 operations: 3 × 200ms = 600ms individual vs 3 × 150ms + 50ms = 500ms batched. At 50 operations, batch is 62x faster with parallel change sets."
            }
        }),
        ("ETag Concurrency Control", "decisionTree", {
            "prompt": "Should I use ETags for concurrency control in this OData service?",
            "firstQuestion": "\"Can two users edit the same entity simultaneously?\" If yes (concurrent editing expected), implement ETags. If entities are created once and rarely updated, ETags add overhead with no benefit.",
            "branches": [
                {"condition": "Multiple concurrent editors, financial or critical data", "path": "Strong ETag (hash-based). Compute SHA-256 hash of key fields + last_changed_at. Server compares If-Match on every update. Returns HTTP 412 on conflict. Client must re-fetch and retry."},
                {"condition": "Lightweight concurrency, non-critical data", "path": "Weak ETag (timestamp-based). Use last_changed_at field as ETag. Simpler but race-condition risk within same millisecond. Prefix with W/ for semantic equivalence per RFC 7232."},
                {"condition": "Read-only or append-only data (no updates)", "path": "No ETags. Skip ETag handling entirely. Saves the computational cost of hash generation on every read and the round-trip for If-Match check on writes."}
            ],
            "staffPlusTip": "ETags implement optimistic locking — detect conflicts at write time rather than preventing them at read time. Use strong ETags for financial data, weak ETags for master data, and no ETags for append-only logs."
        }),
        ("Server-Side Paging & Security", "decisionTree", {
            "prompt": "How should I secure this OData service?",
            "firstQuestion": "\"Who are the consumers?\" Internal Fiori users = ABAP authorization (PFCG) + CSRF protection. External APIs = OAuth 2.0 with scopes. Public APIs = API key + rate limiting + OAuth 2.0.",
            "branches": [
                {"condition": "Internal SAP Fiori / SAPUI5 application", "path": "SAP Gateway authorization (PFCG roles + AUTH object). CSRF token via X-CSRF-Token: Fetch pattern. Row-level security via CDS DCL. No HTTPS termination needed if within SAP network."},
                {"condition": "External API consumed by partner or mobile app", "path": "OAuth 2.0 client credentials grant. Scopes per entity type (read, write). API key for rate limiting (1000 req/h per key). HTTPS with TLS 1.2+. Whitelist allowed IP ranges."},
                {"condition": "Public API (open to internet, no authenticated users)", "path": "API key authentication + rate limiting (100 req/min per key). IP whitelist. Request size limit (1MB max). Sensitive data fields must be excluded via CDS projection. WAF (Web Application Firewall) recommended."}
            ],
            "staffPlusTip": "Security in OData follows defense-in-depth: network (HTTPS + IP whitelist), identity (OAuth 2.0 / PFCG), data (DCL row-level security), and transport (CSRF tokens). Never rely on a single security layer."
        }),
    ],
    "abap-events.json": [
        ("SAP Event Mesh Architecture", "quantifiedTradeoff", {
            "title": "Event Mesh vs Apache Kafka — Enterprise Cost Comparison",
            "variables": [
                {"name": "Message throughput", "value": "50K messages/day", "source": "Enterprise event volume (PO, SO, invoice changes)"},
                {"name": "Retention period", "value": "7 days", "source": "Standard error recovery window"},
                {"name": "Consumer count", "value": "5 downstream systems", "source": "Data lake, analytics, warehouse, 2 partner systems"}
            ],
            "calculation": {
                "formula": "TotalMonthlyCost = PlatformCost + (Throughput × RetentionFactor × ConsumerCount)",
                "event_mesh": {"writeLatency": "~50ms end-to-end", "monthlyPenalty": "$1,200/month — SAP Event Mesh: included in BTP Enterprise License for up to 100K msgs/day. 50ms avg latency. Native SAP integration — no middleware. AMQP 1.0 protocol. Max throughput: ~10K msgs/sec."},
                "kafka_managed": {"writeLatency": "~20ms end-to-end", "monthlyPenalty": "$3,500/month — Confluent Cloud Basic: $1,500 for 50K msgs/day + $2,000 for SAP Kafka Connect connector licensing. 20ms avg latency. Unlimited retention. Requires dedicated operations team for SAP connector maintenance."},
                "breakeven": "Event Mesh is 3x cheaper for standard SAP-native event volumes (<100K msgs/day). Kafka becomes cost-effective at >500K msgs/day or when non-SAP consumers dominate. For pure SAP landscapes, Event Mesh is the recommended choice."
            }
        }),
        ("Idempotency", "adversarialResponse", {
            "challenge": "\"Our event processing creates duplicate sales orders when the Event Mesh redelivers messages. The 'at-least-once' guarantee is causing data corruption.\"",
            "badResponse": "\"Switch the queue to exactly-once delivery.\" (may not be supported by all brokers and adds latency)",
            "goodResponse": "\"At-least-once delivery means duplicates are inevitable — the solution is not to prevent redelivery but to make processing idempotent. Here's the implementation: (1) Add an idempotency key to every event — typically a UUID generated by the producer. The event type + key must be unique per logical operation. (2) In the consumer, create a dedup table with a unique index on (event_type, idempotency_key). Use INSERT ... EXCEPTIONS — if sy-subrc = 0, this is the first delivery; process and update status to 'COMPLETED'. If sy-subrc = 4 (duplicate key), skip processing and return the cached result. (3) The dedup table needs a cleanup job — delete records older than 7 days (matching Event Mesh retention). (4) For critical financial events, don't just dedup — implement exactly-once processing by storing the processing result in the same database transaction as the dedup record. If the process crashes between processing and marking complete, the next redelivery will see the 'PROCESSING' status and the event handler should check whether the processing actually completed before retrying. This pattern is called 'transactional outbox with idempotent processing' — it's the standard FAANG approach for exactly-once semantics at scale.\"",
            "pattern": "idempotency-first — explain why at-least-once is the right delivery semantic, provide a complete implementation (dedup table, unique constraint, status tracking), and connect to the FAANG-standard transactional outbox pattern."
        }),
        ("Async Processing Patterns", "decisionTree", {
            "prompt": "Should I use the outbox pattern for publishing events from this ABAP transaction?",
            "firstQuestion": "\"Can the database write and the event publication happen in the same transaction?\" If yes (both write to HANA), you can use direct publication. If the event goes to an external broker (Event Mesh, Kafka), you need the outbox pattern for atomicity.",
            "branches": [
                {"condition": "Database write + external broker publish (dual-write problem)", "path": "Outbox pattern. Write event to outbox table in same LUW as business data. Separate publisher process reads outbox and publishes to broker. Ensures exactly-once delivery. Use for all external event publications."},
                {"condition": "Both business data and event stay in the same HANA database", "path": "Direct event publication. Use ABAP raise event or UPDATE task (V1/V2). Both happen in the same database LUW. No dual-write problem. Simpler — no outbox table or publisher process needed."},
                {"condition": "High-volume event stream (>10K events/hour)", "path": "Outbox with batch publisher. Buffer events in outbox table up to 500 or 5 seconds. Publish in batch to Event Mesh. Reduces broker connections. Add dead-letter queue for failed publications."}
            ],
            "staffPlusTip": "The outbox pattern solves the dual-write problem by making event publication part of the business transaction. The event is guaranteed to be published if and only if the business data is committed."
        }),
        ("Async Processing Patterns", "quantifiedTradeoff", {
            "title": "Outbox Pattern — Atomicity Guarantee vs Latency Cost",
            "variables": [
                {"name": "Event volume", "value": "5,000 events/day", "source": "PO and SO change events"},
                {"name": "Outbox batch size", "value": "100 events per batch", "source": "Tuned for Event Mesh limits"},
                {"name": "Publisher interval", "value": "5 seconds", "source": "Maximum acceptable delay"}
            ],
            "calculation": {
                "formula": "TotalLatency = (OutboxWriteTime + PublisherInterval) × (1 + RetryProbability × RetryDelay)",
                "direct_publish": {"writeLatency": "~30ms per event (synchronous)", "monthlyPenalty": "$0 — Direct: Write business data + publish event in same ABAP LUW. 30ms total. Zero latency. Risk: if broker is down, the entire transaction fails."},
                "outbox_async": {"writeLatency": "~5ms write + ~2.5s avg delay = ~2.5s total", "monthlyPenalty": "$0 — Outbox: Business write (5ms) + async publisher (avg 2.5s delay due to 5s interval). Maximum 5s delay. Broker failure doesn't affect business transaction. Adds ~2.5s latency but eliminates coupling."},
                "breakeven": "Outbox adds ~2.5s latency but eliminates transaction failures due to broker unavailability. At event volumes <1M/day, the outbox latency is imperceptible to users. Use outbox for all external event publication where business transaction reliability is critical."
            }
        }),
    ],
    "abap-platform.json": [
        ("Work Process Types & Allocation", "decisionTree", {
            "prompt": "Which work process type should I use for this workload?",
            "firstQuestion": "\"Is the workload interactive (user waiting for response) or batch (background processing)?\" Interactive = DIA. Batch = BTC. Also consider: does it write to DB? If yes, UPD may be appropriate for deferred writes.",
            "branches": [
                {"condition": "User-facing dialog, user waits for response", "path": "DIA (Dialog). Synchronous processing. User waits for result. Keep response time under 1 second. If processing takes longer, use RFC with background RFC (bgRFC) to move heavy work to BTC."},
                {"condition": "Long-running data processing, no user interaction", "path": "BTC (Background). No user waiting. Can run for hours. Use SM36 to schedule. Use PACKAGE SIZE to avoid memory issues. Can have lower priority than DIA processes."},
                {"condition": "Database write-back from dialog transaction", "path": "UPD (Update V1/V2). Asynchronous write-back. VB1 for critical updates, VB2 for non-critical. Dialog process releases immediately; update process applies changes. Monitor via SM13."}
            ],
            "staffPlusTip": "Work process allocation is ABAP's thread pool. Oversubscribing DIA processes causes context switching thrashing. Rule: DIA should not exceed 2-3x CPU cores. Monitor SM50 queue length as the primary signal."
        }),
        ("Memory Management — Roll, Roll-Out, Heap", "quantifiedTradeoff", {
            "title": "Memory Tier Tradeoff — Roll Area vs Extended Memory vs Heap",
            "variables": [
                {"name": "Work process type", "value": "DIA", "source": "Dialog work processes"},
                {"name": "Work process count", "value": "50 DIA", "source": "Application server profile"},
                {"name": "Heap per WP", "value": "200MB (abap/heap_area_dia)", "source": "Default profile parameter"},
                {"name": "Extended memory", "value": "500MB (rdisp/roll_max)", "source": "Default profile parameter"}
            ],
            "calculation": {
                "formula": "TotalMemoryRisk = WPCount × (HeapPerWP + ExtendedMemPerWP)",
                "heap_only": {"writeLatency": "Fastest access, highest risk", "monthlyPenalty": "$0 — 50 WP × 200MB = 10GB total. If 30 WPs each load 150MB internal tables simultaneously = 4.5GB — within limit. But if all 50 load 200MB = 10GB = exactly at limit. One more large table = system-wide crash."},
                "heap_plus_em": {"writeLatency": "Slightly slower (roll-out + roll-in), safer", "monthlyPenalty": "$0 — 50 WP × (200MB heap + 500MB EM) = 35GB worst-case. EM is shared — not all WPs use 500MB simultaneously. Practical max: 50 × 200MB heap + 2GB shared EM = 12GB. 20% safety margin."},
                "breakeven": "The heap-only approach is simpler but risks TSV_TNEW_PAGE_ALLOC_FAILED at 80% utilization. Adding EM safety margin costs ~5% performance (roll-out/roll-in overhead) but prevents crashes. At >200 DIA processes, EM becomes mandatory — heap-only allocation would exceed physical memory."
            }
        }),
        ("Memory Management — Roll, Roll-Out, Heap", "adversarialResponse", {
            "challenge": "\"Our production ABAP server crashes weekly with MOVE_FAILED errors during month-end closing. The operations team keeps increasing memory limits but the crashes keep happening.\"",
            "badResponse": "\"Increase abap/heap_area_dia again.\" (repeating the failing pattern)",
            "goodResponse": "\"MOVE_FAILED crashes that recur despite memory increases indicate a memory leak pattern, not a capacity issue. Let me implement a systematic solution: (1) Immediate fix — add a work process watchdog. Use transaction SM65 or write an ABAP program that checks cl_abap_runtime=>get_used_heap_size( ) before each major processing step. If heap usage exceeds 70% of abap/heap_area_dia, trigger a FREE statement on the largest internal tables and log a warning. This prevents the crash by failing gracefully with a warning instead of a dump. (2) Root cause analysis — the month-end closing likely has a program that accumulates data across iterations without freeing it. Check for LOOP ... SELECT ... APPEND patterns where the internal table grows unbounded. Add FREE lt_table after each processing chunk. (3) Long-term fix — implement a memory budget per program. Add a configuration table Z_MEMORY_BUDGET that maps program names to max heap usage. The runtime check in step 1 reads this table and activates data throttling (reduce PACKAGE SIZE, skip non-critical fields) when the budget is exceeded. This prevents any single program from crashing the entire server.\"",
            "pattern": "budget-based-resilience — implement immediate protection (watchdog + graceful degradation), root cause analysis (unbounded accumulation), and long-term governance (program-level memory budgets). The Staff+ insight: memory limits should be managed proactively, not reactively."
        }),
        ("AS ABAP Dispatcher Architecture", "quantifiedTradeoff", {
            "title": "DIA Process Context Switching — User Concurrency Cost",
            "variables": [
                {"name": "Work process count", "value": "50 DIA", "source": "Application server profile"},
                {"name": "CPU cores", "value": "16 cores", "source": "Physical server spec"},
                {"name": "Active users", "value": "500 concurrent", "source": "Peak load"},
                {"name": "Average transaction time", "value": "200ms", "source": "Dialog step processing time"}
            ],
            "calculation": {
                "formula": "EffectiveThroughput = WPCount / (ContextSwitchOverhead + ProcessingTime)",
                "balanced_50wp": {"writeLatency": "50 WPs on 16 cores = 3.1 WPs/core", "monthlyPenalty": "$0 — 50 WPs share 16 cores. Context switching overhead: ~5% CPU. Each WP gets ~19ms of CPU time per 200ms dialog step. Effective throughput: 50 WPs × 5 dialog steps/s = 250 step/s. Average user wait: 16ms."},
                "oversubscribed_150wp": {"writeLatency": "150 WPs on 16 cores = 9.4 WPs/core", "monthlyPenalty": "$3,600 — 150 WPs on 16 cores. Context switching overhead: ~40% CPU wasted on switching. Each WP gets ~7ms of CPU time per 200ms step. Effective throughput: 150 × 2.5 = 375 step/s (only 50% improvement despite 3x WPs). Average user wait: 80ms (5x worse)."},
                "breakeven": "The optimal WP-to-core ratio is 2-3:1 for DIA processes. Beyond 3:1, context switching overhead cancels out the throughput gain and user wait time increases. At 9:1 (your 150 WP scenario), you get only 50% more throughput but 5x worse latency. Right-size at 50 WPs for 16 cores."
            }
        }),
        ("AS ABAP Dispatcher Architecture", "adversarialResponse", {
            "challenge": "\"Our system is slow during peak hours. Operations added more DIA processes but it made things worse. Users are now complaining more.\"",
            "badResponse": "\"Remove the extra DIA processes.\" (correct action but no explanation, doesn't build understanding)",
            "goodResponse": "\"Adding DIA processes beyond the optimal ratio causes context switching thrashing — the operating system spends more time switching between work processes than executing actual ABAP code. The diagnostics: check SM50 — if you see many DIA processes in 'Running' status but CPU is below 70%, context switching is the issue. The tool 'ST05 System Load' shows context switch rate. Here's the fix: (1) Immediately reduce wp_no_dia back to the optimal ratio (2-3x CPU cores). For 16 cores, that's 32-48 DIA, not 100+. (2) Instead of more WPs, optimize the slow-running transactions. Use SAT (ABAP Trace) on the top 5 slowest transactions — identify SELECT * patterns, N+1 queries, or missing secondary indexes that cause long WP hold times. (3) Implement a work process watchdog: if a DIA process runs longer than 300 seconds (rdisp/max_wprun_time), terminate it automatically. This prevents one rogue report from holding a WP hostage during peak hours. (4) Move heavy background processing to dedicated BTC processes with lower priority. The root cause is almost always WP contention, not insufficient WPs.\"",
            "pattern": "diagnose-before-scale — explain the queueing theory (context switching overhead), provide diagnostic steps (SM50 analysis, SAT traces), offer specific configuration fixes (WP-to-core ratio, max runtime), and advocate for optimization before scaling."
        }),
        ("Steampunk Cloud Runtime", "adversarialResponse", {
            "challenge": "\"SAP keeps changing the platform every year. RAP, CDS, Fiori, Steampunk — by the time we learn one, SAP releases something new. Why should we invest in the latest stack?\"",
            "badResponse": "\"SAP's evolution is necessary to stay competitive.\" (corporate answer, no empathy for the developer)",
            "goodResponse": "\"I understand the frustration — the pace of change is exhausting, especially when you have 20 years of ABAP knowledge that feels outdated. Let me reframe the investment decision: (1) The core ABAP language is not changing — your procedural ABAP skills still apply. What's changing is the architecture: from procedural (REPORT + WRITE) to declarative (CDS + annotations) to event-driven (RAP + Event Mesh). These are the same architectural shifts happening in Java (Spring Boot → Reactive → Event-driven), .NET, and Python. You're not learning SAP-specific technologies — you're learning modern enterprise architecture patterns that are transferable to any platform. (2) The ROI of learning RAP and CDS: a managed RAP service takes 80% less code than the equivalent BAPI + SAP Gateway custom service. Over the next 5 years, new S/4HANA Cloud projects will only accept RAP-based extensions (Clean Core). The standard configuration path is dying — extensibility is the future. (3) A pragmatic learning path: focus on CDS views first (they're the foundation, and CDS knowledge is 80% transferable to SQL/Prisma/dbt), then RAP (extends CDS to transactions), then Event Mesh (asynchronous extension). Each layer builds on the previous one. You don't need to learn everything at once.\"",
            "pattern": "reframe-as-investment — acknowledge the fatigue, connect SAP's evolution to industry-wide architectural trends (declarative, event-driven), quantify the ROI (80% less code, Clean Core compliance), and provide a practical learning path that builds incrementally."
        }),
    ],
}

def main():
    for filename, sections in edits.items():
        filepath = os.path.join(CONTENT_DIR, filename)
        print(f"\nProcessing: {filename}")
        
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        modified_count = 0
        for section_title, field_name, field_data in sections:
            found = False
            for section in data["sections"]:
                if section["title"] == section_title or section["title"].startswith(section_title):
                    # Check if field already exists
                    if field_name in section:
                        print(f"  Already has {field_name}: {section_title}")
                        found = True
                        break
                    section[field_name] = field_data
                    found = True
                    modified_count += 1
                    print(f"  Added {field_name}: {section_title}")
                    break
            
            if not found:
                print(f"  NOT FOUND: {section_title}")
        
        if modified_count > 0:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  Written: {modified_count} fields added")
        else:
            print(f"  No changes needed")

    # Validate all JSON files
    print("\n\n=== Validation ===")
    for filename in edits:
        filepath = os.path.join(CONTENT_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                json.load(f)
            print(f"  VALID: {filename}")
        except json.JSONDecodeError as e:
            print(f"  INVALID: {filename} — {e}")


if __name__ == "__main__":
    main()
