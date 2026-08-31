# Phase 8 — Canonical Research Model

> Case 001 — 2026 AI Coding Agent Landscape
> Phase: 8 — Research Asset Production (Task 1 of 5)
> Research cutoff: August 2026 · Research snapshot: 2026-08-31
> Research unit: **Product / Product Family**
> Governing document: `00-research-charter.md` (v1.1)
> Artifact status: **Normative specification for Phase 8** — not a research deliverable
> Scope: read-only formalization of Phase 0–7. No new research, no new ranking, no new judgment.

---

## 0. Status & Scope of This Artifact

### 0.1 What this document is

This is the **single normative model** that all later Phase 8 assets must be generated from:

```text
08-research-note.md
08-dataset/candidates.csv
08-dataset/products.csv
08-sources.md
08-presentation/landscape.html
08-presentation/executive-summary.pptx
```

It defines: the entity model, the provenance model, the controlled vocabularies, the
content-authority map, the semantic locks, the dependency graph, the consistency-hazard
register, and the validation strategy.

### 0.2 What this document explicitly is NOT

- Not a research phase. Phase 8 is **Knowledge / Asset Production** (Charter §15.2). It adds
  no candidate, no score, no market number, no architecture inference, no strategic judgment.
- Not a re-run of Phase 3. The Top 10 is read, never recomputed.
- Not a correction mechanism. Where Phase 1–7 contains an internal discrepancy, this model
  **preserves the historical value and registers the discrepancy** (see §9). Correction is a
  separate, human-approved, versioned action.

### 0.3 Deviation note (Charter §18)

Charter §18 lists only `08-research-note.md`, `08-sources.md`, `08-dataset/`, `08-presentation/`.
This file is added as a Phase-8 prefixed internal specification. It does not change any Phase
numbering or redefine any core deliverable, which is the only thing §18 forbids.

### 0.4 Out of scope for automated banned-pattern scanning

The banned-token list in `08-dataset/tools/phase8_data.py` (`BANNED_PATTERNS`) applies to
**generated presentation assets**. This document necessarily *names* hazard categories while
describing them; those occurrences are descriptive and must not be treated as asset content.

---

## 1. Implementation Plan for Tasks 2–5

### Guiding principle

> **One registry, many renderings.** All six assets are projections of one canonical registry.
> No asset may contain a value that is hand-authored rather than projected. This is what makes
> cross-asset consistency a mechanical property rather than a review burden.

### Task 2 — Canonical Registry, Dataset & Source Ledger

| Step | Deliverable | Work |
|---|---|---|
| 2.1 | canonical registry | Instantiate §3 entities from Phase 1–7. Assign IDs per §4.2. Read-only; every row carries `(source_file, section)` provenance. |
| 2.2 | `08-dataset/candidates.csv` | One row per Phase 1 candidate object. Universe = 44 active (17 Core / 19 Secondary / 8 Watchlist) + 6 excluded rows. See §9 H-14 for the count discrepancy and §9 H-15 for Comate. |
| 2.3 | `08-dataset/products.csv` | 10 rows (locked Top 10) × identity / architecture / workflow / 21 capability cells / Phase 3 scores / category / leadership fields. |
| 2.4 | `08-sources.md` | Unified `S###` ledger: dedupe the **four competing source schemes** (§9 H-11), crosswalk table, tier/type/date, per-claim usage map, and a **Known Discrepancies** section. |

Exit gates: G0, G2, G4, G6, G8 (§10).

### Task 3 — Research Note (`08-research-note.md`)

Structure mirrors the decision chain rather than the phase order, because the note is a
knowledge asset, not a process log:

```text
Core question → Method & constraints → Market structure (strata + denominator caveat)
→ Capability & workflow paradigms → Category & leadership maps
→ Capability commoditization → Strategic layer model → Workflow evolution
→ Stable judgments → Emerging hypotheses → Registered unknowns → Risks
→ Future research questions → Asset map & update procedure
```

Rules: every judgment carries its `J###`; every hypothesis is labeled hypothesis; every
unknown is carried forward; no new analysis. Exit gates: G1, G3, G9, G10.

### Task 4 — HTML Explorer (`08-presentation/landscape.html`)

Views: Locked Top 10 · Capability matrix (21 × 10) · Architecture matrix · Category map ·
Leadership map · Workflow evolution · Benchmark panel · Source & evidence drawer ·
Unknowns register.

Hard constraints:
- The Top 10 view is **non-sortable by default**; if user-sorting is offered, the locked rank
  column stays visible and the "research ranking, not market-share" caption stays pinned.
- `Unknown` renders as "Unknown" — never blank, never `—`, never `0`, never `No`.
- Capability cells render with the `*_raw` qualifier on hover/detail, so normalization is
  always inspectable.
- Data is injected from the registry as generated JSON, never hand-written.

Exit gates: G1, G3, G5, G7, G9.

### Task 5 — Executive PPT (`08-presentation/executive-summary.pptx`)

12 slides per Charter §17.4. PPT is the highest distortion risk because compression removes
qualifiers. Additional rules beyond the shared gates:
- Every number on a slide carries its qualifier inline (survey signal / vendor claim / estimate).
- No slide may show the JetBrains figures as parts of a whole (§7 LOCK-04).
- Strategic scenarios are shown as three named scenarios with their support ordering and the
  verbatim "not a calibrated probability forecast" caption — never as percentages.
- **Compression-distortion review** is a required human gate before the file is final.

Exit gates: G1, G3, G7, G9 + human compression review.

### Task ordering constraint

Tasks 2 → 3 → 4 → 5 strictly. Task 3 may not begin before the registry passes G0/G2/G4/G6/G8;
Tasks 4–5 may not begin before Task 3 passes G1/G9/G10 (the note is the semantic reference text).

---

## 2. Locked Research Decisions (frozen Phase 3 inputs)

### 2.1 Locked Top 10 — historical research judgment

| # | Product Family | Phase 4 file | Composite |
|---:|---|---|---:|
| 1 | Claude Code | `product-01.md` | 5.00 |
| 2 | Codex | `product-02.md` | 5.00 |
| 3 | Cursor | `product-03.md` | 4.95 |
| 4 | GitHub Copilot | `product-04.md` | 4.70 |
| 5 | Devin | `product-05.md` | 4.65 |
| 6 | Google Antigravity | `product-06.md` | 4.55 |
| 7 | Replit Agent | `product-07.md` | 4.45 |
| 8 | OpenCode | `product-08.md` | 4.35 |
| 9 | Qoder | `product-09.md` | 4.35 |
| 10 | Factory | `product-10.md` | 4.20 |

Source: `03-top10-selection.md` §3.1 / §9 / §16.

**Invariant (verified):** the `product-NN` file index equals the locked rank for all ten. This
1:1 mapping is a load-bearing consistency property and must be asserted by the validator.

**Interpretation lock:** this is `Market Significance × Technology / Product Significance`
(Charter §3.2), i.e. **Market Leaders / Representative Leaders**. It is explicitly **not** a
user-count Top 10 and **not** a capability ranking. Assets must state this label verbatim.

### 2.2 Non-negotiable consequences

- Factory stays at #10 despite the lowest composite among the ten. Its selection is a recorded
  Research Judgment override (`03-top10-selection.md` §8.1). It must not be dropped, re-ranked
  or footnoted as "weakest".
- TRAE and Kiro stay Near-miss. They must not be promoted into the Top 10 in any rendering.
- Replit Agent and Factory stay in, precisely because they stretch the category boundary
  (`06-cross-product-analysis.md` §18.5).

---

## 3. Canonical Entity Model

### 3.1 Core structural spine (Charter §2.3)

```text
Company
   ↓
Product Family          ← MAIN RESEARCH UNIT
   ↓
Product Surface
   ↓
Agent Capability
```

`ProductFamily` is the unit of counting, ranking and comparison. Company, Surface and Capability
are never counted as independent research objects.

### 3.2 Primary entities

| # | Entity | ID form | Definition | Key attributes | Authority |
|---:|---|---|---|---|---|
| 1 | **Candidate** | `CAND-nnn` | A named entry in the Phase 1 Candidate Universe. May be a family, an alias merged into a family, or an excluded object. | `name`, `company`, `region`, `phase1_class`, `product_family_id?`, `agentic_level`, `evidence_grade`, `dedup_note` | Phase 1 |
| 2 | **ProductFamily** | `PF-nn` | The Charter research unit. Ten instances for the Top 10; also instantiated for non-Top-10 families referenced by Phase 2/6 (e.g. Kiro, TRAE, Junie). | `canonical_name`, `company_id`, `region`, `agentic_level`, `surfaces[]`, `member_aliases[]`, `dedup_rationale` | Phase 1 §6, Phase 3 §2.2 |
| 3 | **ProductSurface** | `SURF-nnn` | A delivery/entry surface of a family. | `family_id`, `surface_type`, `evidence_state`, `note` | Phase 1 §4, Phase 4 §1 |
| 4 | **ProductCapability** | `CAP-nnn` | **Relation entity**: one (family × capability key) cell. Capability is never a property of the family alone. | `family_id`, `capability_key`, `evidence_state`, `evidence_state_raw`, `authority_phase`, `note` | See §3.4 |
| 5 | **Benchmark** | `B-nnn` | A public benchmark or independent study. | `name`, `organization`, `version`, `date`, `evaluation_unit`, `task_type`, `metric`, `relevance`, `limitations`, `proves`, `does_not_prove`, `source_id` | Phase 5 |
| 6 | **Claim** | `C-nnn` | The atomic assertion carried into assets. | `claim_type`, `statement`, `subject_ref`, `phase`, `evidence_ids[]`, `confidence` | Phase 0–7 |
| 7 | **Evidence** | `E-nnn` | What backs a claim. | `claim_id`, `source_id`, `date_or_period`, `evidence_grade`, `market_signal_type`, `note` | Phase 2/4/5 |
| 8 | **Source** | `S-nnn` | A citable document. | `title`, `publisher`, `url_canonical`, `url_alternates[]`, `tier`, `source_type`, `date`, `used_in_phases[]` | Phase 8 ledger |
| 9 | **Category** | `CAT-nn` | One of 8 overlapping market categories. | `label`, `members[]`, `primary_user`, `workflow_unit`, `architecture_unit`, `competitive_intensity`, `strategic_importance` | Phase 7 §6 |
| 10 | **LeadershipRole** | `LEAD-nn` | One of 11 category-representative roles. **Not a ranking.** | `label`, `representative_id`, `confidence` | Phase 7 §8 |
| 11 | **StrategicLayer** | `SL-nn` | One of 8 layers in the ordered stack. | `name`, `stack_order`, `importance`, `differentiation`, `commoditization_risk`, `moat`, `evidence_confidence` | Phase 7 §5 |
| 12 | **WorkflowParadigm** | `WP-nn` | Workflow form (A–H), architecture paradigm (A–H), or an evolution-chain stage. | `paradigm_set`, `label`, `members[]`, `chain_order` | Phase 6 §10–11, Phase 7 §10.1 |
| 13 | **Phase** | `PH-n` | Phase 0–8. Owns content types. | `number`, `name`, `owns[]`, `exit_criteria` | Charter §15 |
| 14 | **Judgment** | `J-nnn` | A Phase 7 stable judgment. | `statement`, `confidence`, `supporting_claim_ids[]` | Phase 7 §18 |
| 15 | **Hypothesis** | `H-nnn` | A Phase 7 emerging hypothesis. **Explicitly not a fact.** | `statement` | Phase 7 §18 |
| 16 | **Unknown** | `U-nnn` | A registered unknown. **Never resolved during Phase 8.** | `statement`, `why_it_matters`, `status` | Phase 7 §14 + Phase 2/3/5 gaps |

### 3.3 Supporting entities (relation / read-only records)

| Entity | ID form | Purpose | Authority |
|---|---|---|---|
| Company | `CO-nn` | Required by Charter §2.3 spine. Captures corporate-status changes as **strategic context**, never as capability. | Phase 1/4 |
| Score | `SCORE-nn` | Phase 3 five-dimension + composite. **Read-only historical record. Never recomputed.** | Phase 3 §3.1 |
| SelectionDecision | `SEL-nn` | Phase 3 status + rationale + divergence flag. | Phase 3 §3.1/§8 |
| MarketSignal | `MS-nnn` | A typed adoption/scale figure (independent / vendor / ecosystem). | Phase 2 §3, Phase 7 §2.3 |
| CompetitionRelation | `CR-nnn` | Typed pair relation (direct / adjacent / workflow alternative / architecture alternative / substitute). | Phase 6 §9, Phase 7 §7 |

### 3.4 Capability key set — 21 keys

Phase 4 §6 (17 rows) and Phase 6 §6 Agent Matrix (10 columns) are **two different schemas**.
Neither is a subset of the other. The canonical key set is the union:

| Source | Keys | Count |
|---|---|---:|
| Phase 4 only | `coding`, `repository_understanding`, `terminal`, `browser_external_tools`, `testing`, `debugging`, `refactoring`, `mcp`, `skills`, `sandbox`, `cloud_agent` | 11 |
| Shared | `planning`, `context_management`, `tool_use`, `long_running`, `multi_agent`, `memory` | 6 |
| Phase 6 only | `execution`, `verification`, `repair`, `human_steering` | 4 |
| **Total** | | **21** |

**Authority rule:**
- Shared 6 + Phase-6-only 4 → **Phase 6 Agent Matrix is authoritative** (it is the normalized
  cross-product view); Phase 4 wording supplies `evidence_state_raw` and notes.
- Phase-4-only 11 → **Phase 4 is authoritative**; no Phase 6 equivalent exists.

**Rule validated:** all 10 × 6 = 60 shared cells were cross-checked between Phase 6 and Phase 4.
**Zero contradictions.** Phase 6's C/P/U normalization is faithful to Phase 4.

---

## 4. Provenance Model

### 4.1 Mandatory chain

```text
Claim (C-nnn)
   ↓
Evidence (E-nnn)
   ↓
Source (S-nnn)
   ↓
Date
   ↓
Evidence Grade (A/B/C/D)
   ↓
Confidence (High → Low)
   ↓
Phase (0–8)
```

No asset may present a Claim without a renderable path down this chain.

### 4.2 Identifier strategy

| Prefix | Entity | Form | Example |
|---|---|---|---|
| `CAND-` | Candidate | `CAND-014` | sequence over Phase 1 order |
| `PF-` | Product Family | `PF-03` | `01..10` = locked Top 10 |
| `SURF-` | Product Surface | `SURF-021` | |
| `CAP-` | Capability cell | `CAP-147` | |
| `B-` | Benchmark | `B-02` | |
| `C-` | Claim | `C-031` | |
| `E-` | Evidence | `E-058` | |
| `S-` | Source | `S-007` | |
| `CAT-` | Category | `CAT-04` | |
| `LEAD-` | Leadership role | `LEAD-02` | |
| `SL-` | Strategic layer | `SL-03` | |
| `WP-` | Workflow paradigm | `WP-05` | |
| `J-` | Judgment | `J-04` | |
| `H-` | Hypothesis | `H-02` | |
| `U-` | Unknown | `U-07` | |

**ID rules (non-negotiable):**

1. **Opaque.** IDs carry sequence only. They must never encode rank, quality, grade, date,
   region or ordinal meaning.
   - Forbidden: `PF-CLAUDECODE-RANK1`, `GRADE-A-S007`, `CAP-2026-Q3-04`.
2. **Rank lives in a field, not an ID.** The only place rank exists is
   `SelectionDecision.locked_rank` (`1..10`, nullable), typed as
   `record_type = Historical Research Judgment`, `phase = 3`. The fact that `PF-01` happens to
   equal locked rank 1 is a documented mapping convenience, not a semantic claim — it must be
   asserted as an invariant, never marketed as an ordering embedded in IDs.
3. **Stable and non-reusable.** Once assigned, an ID is never renumbered or reused. Removed
   entities are tombstoned with a `deprecated` flag.
4. **Every referenced ID resolves.** Dangling references fail G4.
5. **Dates are separate fields.** Never encode dates in IDs; dates live in `date_or_period`
   with an explicit precision (`day` / `month` / `year` / `period`).

### 4.3 Provenance requirements per asset type

| Asset | Minimum provenance |
|---|---|
| CSV rows | `source_file`, `source_section`, `phase` per row |
| Research note | `C-nnn` on every judgment; `S-nnn` on every factual number |
| HTML | evidence drawer reachable from every rendered claim/number |
| PPT | source phase + qualifier inline on every number |

---

## 5. Controlled Vocabularies

### 5.1 Required core vocabularies

**Evidence Grade** — `A` · `B` · `C` · `D` (Charter §11.1). Measures strength of support for a
claim, **not** product quality.

**Confidence** — `High` · `Medium-High` · `Medium` · `Medium-Low` · `Low`

**Capability evidence state** — `Confirmed` · `Partial` · `Unknown` · `Not primary`

**Claim type** — `Fact` · `Market Evidence` · `Product Evidence` · `Benchmark Evidence` ·
`Analysis` · `Judgment` · `Hypothesis` · `Unknown`

### 5.2 Additional vocabularies required by the record

These exist because Phase 1–7 uses them. Leaving them undefined is what produces the
scale-conflation hazard (§9 H-01).

| Vocabulary | Values | Authority |
|---|---|---|
| Phase 1 candidate class | `Core` · `Secondary` · `Watchlist` · `Excluded` · `Unknown` | Phase 1 §3–§4, §8 |
| Phase 3 selection status | `Selected` · `Near-miss` · `Boundary` · `Not-in-final-top10` · `Excluded` | Phase 3 §3.1 |
| Market signal type | `Independent signal` · `Vendor claim` · `Ecosystem signal` · `Unknown` | Phase 6 §2.3 |
| Product surface | `CLI` · `IDE` · `Desktop` · `Cloud` · `Plugin` | Charter §2.4 |
| Source tier | `Tier 1 Primary` · `Tier 2 Independent` · `Tier 3 Community/Discovery` · `Tier 4 Individual Review` | Charter §10 |
| Source type | `Official Product` · `Official Documentation` · `Official Blog` · `Official Release Note` · `Official Company Announcement` · `Independent Survey` · `Independent Research` · `Benchmark` · `Technical Paper` · `Community` · `Individual Review` | Phase 2 §18 |
| Agentic level | `Agentic Coding Tool` · `Software Engineering Agent` · `Autonomous Software Engineering Agent` | Charter §2.2 |
| Benchmark evaluation unit | `Model` · `Model + Prompt/Scaffold` · `Agent + Harness` · `Agent + Runtime` · `Product` | Phase 5 §2.2 |
| Competition relation | `Direct` · `Adjacent` · `Workflow alternative` · `Architecture alternative` · `Strategic substitute` | Phase 6 §9, Phase 7 §7 |
| Commoditization tier | `Commodity` · `Differentiating` · `Potential moat` | Phase 7 §9 |
| Region | `Global` · `Global + China` · `China + Global-facing` | Phase 1 §4 |
| Phase ownership | `0` … `8` | Charter §15 |

### 5.3 Compound-value normalization rules

Phase 1–7 contains many compound values (`A/B`, `B+/A-`, `P/C`, `Confirmed / task dependent`).
**Rule: never silently normalize. Canonical field takes a single controlled value; the verbatim
string is always preserved in a paired `*_raw` field.**

| Domain | Compound | Canonical | Raw field | Rule |
|---|---|---|---|---|
| Candidate evidence grade | — | Phase 1 single letter | `phase1_evidence_grade` | Phase 1 grades are all single-valued (verified: 44/44). **No normalization needed.** |
| Phase 2 evidence coverage | `A/B`, `B+/A-` | first token in `phase2_coverage_primary` | `phase2_coverage_raw` | Kept as a **separate field**, never merged into `evidence_grade`. |
| Capability (Phase 6 matrix) | `P/C` | **Partial** | `evidence_state_raw` | Conservative member. Capability must never be overstated. |
| Capability (Phase 6 matrix) | `C*` | **Confirmed** | `evidence_state_raw` + note | The `*` caveat is mandatory note text, never dropped. |
| Capability (Phase 4) | `Confirmed / <dependency qualifier>` | **Partial** | `evidence_state_raw` | Qualifiers: task-, surface-, environment-, deployment-, orchestration-, integration-dependent; partially public; partially visible. |
| Capability (Phase 4) | `Confirmed / <detail qualifier>` | **Confirmed** | `evidence_state_raw` | Qualifiers: internal detail limited; not always central; extensible. |
| Capability (Phase 4) | `Partially confirmed` | **Partial** | `evidence_state_raw` | |
| Capability (Phase 4) | `Not primary` | **Not primary** | — | Source: OpenCode cloud agent. |
| Identity evidence state | `Strongly indicated`, `Confirmed at conceptual level`, `Confirmed at project level` | separate `identity_evidence_state` field | `identity_state_raw` | **Not** the capability vocabulary. Do not collapse into §5.1. |
| Selection status | `Boundary / Reserve` | **Boundary** | `status_label_verbatim` | `Reserve` never occurs standalone in Phase 3; it is not a vocabulary value. |

**Mandatory: normalization decision log.** Every row where the mapping required judgment must
appear in a reviewable table (`Appendix A`) with `entity_id`, `raw`, `canonical`, `rule_applied`,
`reviewer_signoff`. This is what makes normalization auditable rather than invisible.

---

## 6. Content Authority (Phase Ownership)

| Phase | Owns | May NOT be changed by |
|---|---|---|
| 0 | Definitions, taxonomy, method, weights, evidence rules | all |
| 1 | Candidate Universe, classification, dedup, exclusions | 2–8 |
| 2 | Market / evidence base, evidence grades, vendor-claim labeling | 3–8 |
| 3 | Ranking, composite scores, Top 10, selection rationale | 4–8 |
| 4 | Product-level evidence, architecture, agent loop, workflow | 5–8 (cross-checked only) |
| 5 | Benchmark selection, methodology review, model/agent/product layering | 6–8 |
| 6 | Cross-product matrices, paradigms, competition structure | 7–8 |
| 7 | Strategic judgments, leadership, scenarios, risks, unknowns | 8 |
| 8 | **Rendering, projection, packaging — no content creation** | — |

**Phase 8 self-constraint:** if producing an asset appears to require a value that no phase owns,
the correct output is `Unknown` — never a plausible-looking value.

---

## 7. Semantic Locks

Each lock freezes an object and records what must not be implied. "Anti-pattern" columns are
automated check targets (gate G1).

| Lock | Frozen object | Authority | Anti-patterns (must never appear) |
|---|---|---|---|
| **LOCK-01** | Top 10 membership **and order** | `03` §9/§16 | Re-sorting by adoption/capability/benchmark; "user-count Top 10"; dropping Factory; promoting TRAE/Kiro |
| **LOCK-02** | Phase 3 scores (5 dims + composite, 20 candidates) | `03` §3.1 | Recomputation; new index from dimension sums; rounding; silently fixing the discrepancy (§9 H-02) |
| **LOCK-03** | Market-share denominator caveat | `07` §4.3 | Any computed share figure; the caveat's absence on any slide containing numbers |
| **LOCK-04** | JetBrains survey figures (39/21/16/12/7/6, ~9% Junie; May–Jul 2026; 15,000+ devs; 90% weekly / 68% daily) | `02` §3.1, `07` §2.3 | Summing; normalizing to 100%; pie/donut rendering; share-of-total framing; swapping the "AI tools" vs "AI coding agents" referent (§9 H-04) |
| **LOCK-05** | Market strata A/B/C | `07` §4.2, `06` §4.2 | Intra-stratum ranking; reading strata as product-quality tiers |
| **LOCK-06** | `Model → Agent System → Workflow` | `07` §3/§23 | "Model no longer matters"; per-product score for this direction |
| **LOCK-07** | Strategic layer model (8 layers, ordered) | `07` §5 | Reordering; adding/removing layers; layer scores |
| **LOCK-08** | Commoditization conclusions (8 / 6 / 6) | `07` §9 | Reclassification; per-product "moat score"; "Product X has a moat" |
| **LOCK-09** | Category map (8 overlapping categories) | `07` §6 | Mutually exclusive bucketing; ranking by category |
| **LOCK-10** | Leadership map (11 roles, 1 representative, +confidence) | `07` §8 | Merging into an overall ranking; "overall winner"; dropping confidence labels |
| **LOCK-11** | Workflow evolution (8 stages; happened / emerging / not-yet-proven) | `07` §10 | "End-to-end autonomy achieved"; product maturity levels without the "not a ranking" caveat (§9 H-17) |
| **LOCK-12** | Strategic scenarios A/B/C; support order B > C > A | `07` §12 | Probabilities; percentages; timelines; "most likely X%" |
| **LOCK-13** | Risks (10) & Unknowns (11+) | `07` §13–14, `02` §14, `03` §13, `05` §19 | Resolving an Unknown; dropping one; rendering Unknown as blank/No/0 |
| **LOCK-14** | Product-family deduplication (8 families + 4 recorded merges) | `01` §6, `03` §2.2 | Re-splitting; counting surfaces as candidates; double-counting Google (Antigravity + Gemini CLI) or AWS (Q + Kiro) |
| **LOCK-15** | Benchmark's supporting-evidence status | `05` §22 | Product ranking from benchmark; "best at SWE-bench"; treating `agent + model` configs as product results |
| **LOCK-16** | Vendor-claim separation | `02` §2.3, `03` §3.2/§7.2 | Any vendor number losing its `Vendor claim` label; vendor → independent upgrade |
| **LOCK-17** | Competitive relations (3 direct pairs + adjacent + alternatives) | `06` §9, `07` §7 | Converting relations to a ranking; presenting the §9.5 map as positional scoring |
| **LOCK-18** | Paradigm sets (8 architecture + 8 workflow) | `06` §10–11 | Collapsing into one taxonomy; dropping Workflow A (historical baseline) though Phase 6 Q3 lists 7 |
| **LOCK-19** | Snapshot dates | `01`–`07` headers | Presenting Aug-2026 facts as current; using Phase 1's 2026-08-30 state where Phase 2/3 issued a versioned correction (Q→Kiro) |
| **LOCK-20** | Boundary-inclusion rationale (Replit, Factory) | `06` §18.5 | Framing Replit as "a weaker repo-centric agent" or Factory as "weak evidence" without the paradigm rationale |

---

## 8. Implementation Dependency Graph

```text
Phase 0–7 research record (read-only)
        │
        ▼
┌───────────────────────────────────────────────────┐
│ Task 1 — CANONICAL ENTITY / PROVENANCE MODEL      │  ← this document
│   entity model · provenance · vocabularies        │
│   semantic locks · hazards · validation gates     │
└───────────────────────────────────────────────────┘
        │  gates: model completeness, lock coverage
        ▼
┌───────────────────────────────────────────────────┐
│ Task 2 — CANONICAL REGISTRY + SOURCE LEDGER       │
│   registry (§3 entities, §4 IDs)                  │
│     ├── 08-dataset/candidates.csv                 │
│     ├── 08-dataset/products.csv                   │
│     └── 08-sources.md  (unified S### + crosswalk) │
└───────────────────────────────────────────────────┘
        │  gates: G0 G2 G4 G6 G8
        ▼
┌───────────────────────────────────────────────────┐
│ Task 3 — RESEARCH NOTE (08-research-note.md)      │
└───────────────────────────────────────────────────┘
        │  gates: G1 G3 G9 G10
        ├──────────────────────┐
        ▼                      ▼
┌────────────────────┐  ┌──────────────────────────┐
│ Task 4 — HTML      │  │ Task 5 — EXECUTIVE PPT   │
│  landscape.html    │  │  executive-summary.pptx  │
│ gates G1 G3 G5 G7  │  │ gates G1 G3 G7 G9        │
│       G9           │  │ + compression review     │
└────────────────────┘  └──────────────────────────┘
        └──────────────┬───────────────┘
                       ▼
        ┌──────────────────────────────────┐
        │ FINAL VALIDATION                 │
        │ G0–G10 over all six assets       │
        │ + cross-asset diff (G7)          │
        │ + human sign-off on decision log │
        └──────────────────────────────────┘
```

**Hard edges:** no asset may be authored before its upstream passes. The registry is the only
allowed data source for Tasks 3–5.

---

## 9. Consistency Hazards Register

Discovered by cross-reading Phase 0–7. Each hazard is carried into Task 2 as a decision the
registry must make explicitly. **None is silently fixed.**

### H-01 — Six overlapping evidence scales (highest risk)

The record uses **six** different scales that an unwary dataset would collapse into one column:

| Scale | Values | Where |
|---|---|---|
| Evidence grade | `A/B/C/D` | Charter §11.1, Phase 1 §4, Phase 2 §12.1 |
| Confidence | `High / Medium-High / Medium / Medium-Low / Low` | Phase 2 §11, Phase 7 |
| Identity evidence state | `Confirmed / Partially confirmed / Strongly indicated / Confirmed at conceptual level / Confirmed at project level` | Phase 4 §1 |
| Capability evidence state | `Confirmed / Partial / Unknown / Not primary` (+ ~14 slash variants) | Phase 4 §6 |
| Phase 6 capability | `C / P / U / P/C / C*` | Phase 6 §6 |
| Phase 6 market signal | `Independent signal / Vendor claim / Ecosystem signal / Unknown` | Phase 6 §2.3 |

**Mitigation:** six distinct fields, never one. See §5.2–5.3.

### H-02 — Jules composite score does not match the stated formula

`03-top10-selection.md` §3.1: Jules = Market 2.0, Capability 4.5, Workflow 4.5, Ecosystem 4.5,
Momentum 4.5, **printed composite 3.70**. Under the stated weights
(30/30/20/10/10) the value computes to **3.75**.

All other 19 candidates were re-derived and match exactly.

**Mitigation:** preserve `3.70` verbatim; set `score_discrepancy_flag = true`; record in
`08-sources.md` → Known Discrepancies. Never "correct" to 3.75 in an asset.

### H-03 — Phase 2 contains a chronologically impossible date

Phase 2 §3.2, Claude Code row: "Anthropic reported >$2.5B run-rate revenue and weekly active
users **doubled since Jan 2026** in an **Aug 2025** disclosure | **2025-08** historical baseline".
A 2025 disclosure cannot reference Jan 2026.

**Mitigation:** carry with `date_quality = suspect`; do not use the `$2.5B` figure as a dated
market number in assets; flag for human resolution.

### H-04 — The 90% figure changes referent across phases

- Phase 1 §2.5: ~90% of developers regularly use **at least one AI tool** for coding/development.
- Phase 2 §3.1 / Phase 7 §2.3: 90% use **AI coding agents** at work **weekly**.

**Mitigation:** one `MarketSignal` entity per phase-specific formulation; never merged; each
rendering carries its referent.

### H-05 — Two different URLs for the same JetBrains Aug-2026 report

- Phase 1 §12: `blog.jetbrains.com/ai/2026/08/ai-coding-agents-adoption-trends/`
- Phase 2 S01 / Phase 3 §17 / Phase 6 §22.3: `blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/`

**Mitigation:** one `S-` entry; the second URL stored in `url_alternates[]`. No live
link-checking was performed (that would add evidence outside the record); resolution, if
wanted, is a source-hygiene step to be approved separately.

### H-06 — Two different URLs for the same Reuters article

- Phase 3 §17: `…openai-end-partnership-with-spacexs-cursor-2026-08-29/`
- Phase 6 §22.3: `…openai-end-partnership-with-spacexs-cursor-escalating-feud-with-musk-2026-08-29/`

**Mitigation:** as H-05.

### H-07 — Two GitHub orgs for OpenCode

- Phase 1 §12, Phase 4 product-08, Phase 6 §22.3 → `github.com/anomalyco/opencode`
- Phase 3 §17 → `github.com/sst/opencode`

**Mitigation:** `anomalyco` as canonical (3 of 4 occurrences, incl. the Phase 4 dossier);
`sst` recorded as alternate with a rename-lineage note.

### H-08 — Phase 2 uses a non-canonical evidence grade

Phase 2 §12.1 grades Devin as **`B+/A-`**, which is not in the `A/B/C/D` vocabulary. Phase 1 §4.1
grades Devin **`B`**.

**Mitigation:** `evidence_grade = B` (Phase 1 owns candidate grade); `phase2_coverage_raw =
"B+/A-"`; `phase2_coverage_primary = B`. The compound must never reach a canonical grade column.

### H-09 — `Reserve` is not a real status value

Phase 3 §3.1 labels Jules `Boundary / Reserve` (one compound label). No candidate is ever
`Reserve` alone.

**Mitigation:** vocabulary value is `Boundary`; verbatim `Boundary / Reserve` preserved.
Note: `08-dataset/tools/phase8_data.py` currently lists `Reserve` as a vocabulary value —
recommend removal (see §11).

### H-10 — Two capability schemas, neither a subset of the other

Phase 4 §6 has 17 capability rows; Phase 6 §6 has 10 columns; union is 21 (§3.4).

**Mitigation:** 21-key canonical set with an explicit authority rule per key.

### H-11 — Four competing source-identification schemes

| Scheme | Where |
|---|---|
| `S01`–`S32` | Phase 2 §18 |
| `1`–`26` (plain numbers) | Phase 5 §24 |
| Named table rows, no IDs | Phase 6 §22.2, Phase 7 §22 |
| Footnote keys (`[^market1]` etc.) | Phase 1, Phase 3 |
| Unnumbered URL lists | Phase 4 product files |

**Mitigation:** a single `S-nnn` ledger in `08-sources.md` with a full crosswalk. This is the
single largest Task 2 work item.

### H-12 — Phase 5 contradicts itself on DevBench's status

Phase 5 §3.1 marks DevBench / DevEval **"Supporting"**; Phase 5 §3.2 lists it as item **8 of the
core benchmark set**.

**Mitigation:** follow §3.1 (`Supporting`) and register the conflict; §3.2's list is treated as
an enumeration of *reviewed* benchmarks, not a status assignment.

### H-13 — Phase 2 cites a benchmark superseded by Phase 5

Phase 2 §10.3 discusses **Terminal-Bench 2.0**; Phase 5 and Phase 6 use **2.1** (which Phase 5
§11 describes as a correction of 2.0). Phase 2 §10.2 cites **SWE-rebench** results (Codex Agent
58.0%, Junie Agent 61.8%) that Phase 5 does not include in its benchmark set or source ledger.

**Mitigation:** version every benchmark entity; never merge 2.0 with 2.1; carry SWE-rebench as
an unvalidated Phase 2 benchmark result with `validated_in_phase5 = false`.

### H-14 — Phase 1's excluded-object count contradicts its own table

Phase 1 §13 states "**5** explicitly excluded / merged objects" and "about **49** total".
The Phase 1 §8 table has **6** rows (44 + 6 = 50).

**Mitigation:** dataset carries 6 rows (table is authoritative); both counts recorded and the
discrepancy registered.

### H-15 — Baidu Comate is unclassified

Comate appears in Phase 1 §5.1 and §9.2 with sources, but has **no row** in the Phase 1 §4
classification tables — hence no class and no evidence grade.

**Mitigation (proposed, requires human sign-off):** include in `candidates.csv` with
`phase1_class = Unknown`, `selection_status = Not-in-final-top10`, and a mandatory
`provenance_note`: *"Named in Phase 1 §5.1/§9.2; no row in the Phase 1 §4 classification tables.
Class is Unknown — not assigned by Phase 1."*
The alternative (drop entirely) loses a Phase-1-named first-layer China representative. **This
is a decision point, not an implementation detail — flag for approval before Task 2.**

### H-16 — Phase 1 class and Phase 3 status are orthogonal

`Amazon Q Developer` is Phase 1 **Core** (#17) yet Phase 3 excludes it from the modern ranking
population as a migration lineage into Kiro. Collapsing these into one column would either
invent a Core candidate outside the population or erase a Phase 1 classification.

**Mitigation:** keep `phase1_class` and `phase3_status` as separate fields with separate
provenance. Same issue for Factory and Augment Code (Phase 1 Secondary → Phase 3 Selected /
Near-miss).

### H-17 — "Work-unit Level 3–6" is an undefined ordinal scale

Phase 6 §15.2 places products at "Level 3–4", "Level 4–6" etc. without ever defining the levels.
Phase 6 states the table "is not an overall ranking".

**Mitigation:** carry as qualitative placement with Phase 6's own caveat attached; do **not**
render as a numeric axis in HTML/PPT.

### H-18 — Adoption figures are multi-select and must not sum

The JetBrains figures sum to 110% (39+21+16+12+7+6+9). Any chart normalizing them to a whole
would fabricate market share.

**Mitigation:** bar chart with an explicit "multi-select survey; does not sum to 100%" caption;
pie/donut/stacked-100% renderings are **forbidden** (LOCK-04).

### H-19 — 6 of 10 products have no usable public price point

Concrete published tiers exist for only **4** of 10: GitHub Copilot ($10 / $39 / $100), Replit
($20 / $100), Qoder ($20 / $60 / $200), Factory (~$20 / $100 / $200 / $60 per user).

The other **6** lack a comparable figure:

| Product | Situation |
|---|---|
| Claude Code | Plan-level only (Max 5x $100 / Max 20x $200); **Medium** confidence; date recorded as "2025/2026 doc" |
| Codex | No individual tier prices; bundled into ChatGPT plans plus token-based PAYG |
| Devin | No figures; ACU-based, "exact packaging is time-sensitive" |
| Google Antigravity | No consumer figures; enterprise via Google Cloud |
| Cursor | Pricing page cited, but the ledger records **no numbers** |
| OpenCode | Zen is pay-as-you-go per 1M tokens; no tier prices |

**Mitigation:** no numeric price chart anywhere in the assets. Economics is rendered as
qualitative text with explicit `Unknown`s, and the Claude Code figure carries its `Medium`
confidence and suspect date (H-03) wherever it appears.

### H-20 — Augment Code scores 5.0 on capability but has no Phase 4 dossier

Phase 3 §3.1 gives Augment Code Capability **5.0** — equal to Claude Code, Codex, Devin,
Antigravity and Factory — yet it is Near-miss with no `04-products/` file. A capability chart
drawn from the score table would show an unresearched product at the top.

**Mitigation:** capability visualizations use the **Phase 4/6 capability matrix** (21 keys),
never the Phase 3 capability score, for the Top 10. Near-miss scores are shown only in the
Phase 3 score table, never in a capability view.

### H-21 — Cursor acquisition date granularity differs by phase

Phase 4 product-03 / Phase 6 §19.6 / Phase 3 say "Aug 2026"; Phase 7 §2.3 states completion
on **2026-08-14**, with the OpenAI model-supply announcement on **2026-08-28** and Reuters
reporting on **2026-08-29**.

**Mitigation:** three distinct dated facts (completed / announced / reported) as separate
`MarketSignal` rows. Never collapse into "the August acquisition".

### H-22 — TRAE scale figures use two different metrics

Phase 3 §8.2 cites "6M registered users, ~60M sessions (end of 2025)"; Phase 2 §4.1 cites
"hundreds of thousands of developers historically".

**Mitigation:** separate rows with distinct metric types; never merged or averaged.

### H-23 — The 47% agent-generated-code figure is a derived estimate

Phase 7 §10.2: "roughly 47% of produced code was fully agent-generated on average **using
midpoint calculations across buckets**"; ~22% of developers in the >80% bucket.

**Mitigation:** `claim_type = Analysis`, with the midpoint-derivation method stated inline
wherever the number appears. It is not a measured fact.

### H-24 — METR time-savings are an explicitly bounded figure

Phase 5 §13.3: task time-savings factor **1.5×–13×**, which METR itself calls a **soft upper
bound**.

**Mitigation:** never rendered without "soft upper bound". Forbidden: "Claude Code makes
engineers 13× more productive".

### H-25 — Stack Overflow evidence is from 2025, not 2026

Phase 1 §12 and Phase 5 §13.6 both cite the **Stack Overflow 2025** Developer Survey.

**Mitigation:** date label is mandatory; never presented as 2026 evidence.

### H-26 — Benchmark results are `agent + model` configurations, not products

Phase 5 §10 (Kotlin Benchmark): "Claude Code + Opus 4.7 xhigh 85.71%", "Junie + Opus 4.7 max
81.9%", "Codex + GPT-5.5 xhigh 81.9%". Phase 5 §11 (Terminal-Bench 2.1) similarly couples
model and CLI.

**Mitigation:** benchmark results attach to `Benchmark`, not to `ProductFamily`, and carry
`evaluation_unit` + `configuration` fields. No product-level benchmark score column.

### H-27 — Non-Top-10 product beats a Top-10 product on one benchmark

SWE-rebench (Phase 2 §10.2) shows Junie Agent (61.8%) above Codex Agent (58.0%). Junie is
Near-miss.

**Mitigation:** Phase 5 §22 governs — benchmark results do not alter the Top 10. Assets must
not present this as an inconsistency in the selection.

### H-28 — GitHub's Pro plan bundles competitor agents

Phase 4 product-04 evidence ledger: "Third-party agents Claude Code and Codex are available
through Pro" (GitHub Plans & Pricing). Not surfaced in Phase 6/7.

**Mitigation:** record as a `Product Evidence` claim. It is a distribution fact, **not** a
ranking input and **not** an endorsement.

### H-29 — Cursor's historical adoption baselines are from different surveys

Phase 1 §2.5 cites an Apr-2026-published survey (Jan 2026 data): Copilot ~29%, Cursor ~18%,
Claude Code ~18%. Phase 2/3/6/7 use May–Jul 2026: Copilot 21%, Cursor 12%, Claude Code 39%.
Phase 6 mentions only Cursor's 18%→12% decline, not Claude Code's 18%→39% rise.

**Mitigation:** each figure bound to its own survey wave; never mixed in one series without a
wave label.

### H-30 — Workflow paradigms: 8 defined, 7 listed

Phase 6 §11 defines Workflow **A–H** (8), but Phase 6 §20 Q3 lists only **7** (B–H). Workflow A
is described as the historical baseline, not a current form.

**Mitigation:** entity set contains all 8; `is_current_form = false` for A. Do not drop A.

---

## 10. Validation Strategy

### 10.1 Gates

| Gate | Name | Assertion | Applied at |
|---|---|---|---|
| **G0** | Source-of-truth | Every value traces to a `(file, section)` anchor in Phase 0–7 | Task 2 |
| **G1** | Semantic-lock | Every lock in §7 is byte-identical to source (ordering, membership, numeric strings) | Tasks 3–5 |
| **G2** | Vocabulary | Every categorical value ∈ its §5 vocabulary; no compound in a canonical field | Task 2 |
| **G3** | No-new-research | No new candidate, score, adoption number, architecture inference, or judgment | Tasks 3–5 |
| **G4** | Provenance-completeness | Every Claim has ≥1 Evidence; every Evidence has 1 Source; every Source has tier+type+date-or-Unknown; no dangling IDs | Task 2 |
| **G5** | Anti-inference | Nothing marked `Confirmed` where source says `Partial`/`Unknown`; `Unknown` never renders as blank/`No`/`0` | Task 4 |
| **G6** | Date discipline | Every time-sensitive fact carries a date; no Phase-1 state used where Phase 2/3 issued a versioned correction | Task 2 |
| **G7** | Cross-asset consistency | Identical entity/value across note, CSVs, HTML, PPT — guaranteed by single-registry projection | Final |
| **G8** | Numeric fidelity | Scores/percentages/counts compared as **strings**, not floats; known discrepancies asserted as preserved-with-flag | Task 2 |
| **G9** | Ranking contamination | No ordering other than the locked Top 10; no composite other than Phase 3's; leadership/category lists carry the "not a ranking" caption | Tasks 3–5 |
| **G10** | Unknown preservation | Count of `Unknown` entities in assets ≥ registry count; none silently dropped | Tasks 3–5 |

### 10.2 Additional mechanical checks

- **Invariant:** `product-NN` file index == `locked_rank` for all 10 (verified; must stay true).
- **Invariant:** 10 selected, 9 near-miss, 1 boundary in the Phase 3 score table.
- **Invariant:** 44 active candidates (17/19/8).
- **Invariant:** 20 Phase 3 scored candidates = 17 Core − 1 (Amazon Q) + 4 Secondary
  (Augment Code, Factory, Jules, Qwen Code). Verified.
- **Invariant:** shared capability cells — 60/60 agreement between Phase 4 and Phase 6 (verified).
- **Banned-pattern scan:** the `BANNED_PATTERNS` list in `08-dataset/tools/phase8_data.py`,
  run over the four generated presentation/dataset assets only (see §0.4).
- **Sum check:** JetBrains adoption figures must never be rendered as a normalized whole.

### 10.3 Human review gates (Charter §16.10)

Automation cannot approve judgment. Required human sign-off on:

1. The **normalization decision log** (Appendix A) — every judgment-based compound mapping.
2. **H-15 (Comate)** — whether to include an unclassified Phase 1 mention.
3. **H-02 / H-03 / H-12 / H-14** — whether to raise formal versioned corrections.
4. **PPT compression-distortion review** — confirm no qualifier was lost in compression.
5. Final acceptance of all six assets.

### 10.4 Escalation rule

> **Phase 8 never edits history.** If validation surfaces a genuine factual error in Phase 1–7,
> the response is: preserve the value in the asset, record it in `08-sources.md` →
> *Known Discrepancies*, and raise it as a **proposed** versioned correction. Silent in-place
> correction is prohibited.

---

## Appendix A — Normalization Decision Log (template)

| # | entity_id | field | raw value | canonical | rule applied | requires sign-off |
|---|---|---|---|---|---|---|
| 1 | `PF-05` | `phase2_coverage` | `B+/A-` | `B` | §5.3 row 2 | yes |
| 2 | `PF-06` | `CAP.verification` | `P/C` | `Partial` | §5.3 conservative member | yes |
| 3 | `PF-10` | `CAP.long_running` | `C*` | `Confirmed` + note | §5.3 `C*` rule | yes |
| … | | | | | | |

Populated during Task 2; sign-off required before Task 3.

---

## Appendix B — Relation to `08-dataset/tools/phase8_data.py`

An untracked partial registry already exists at `08-dataset/tools/phase8_data.py`. It is a
usable head start for Task 2 and is **not modified by this Task 1**. Required refinements when
Task 2 adopts it:

1. **Remove `Reserve`** from `PHASE3_STATUS_VOCAB` (H-09).
2. **Add `*_raw` companion fields** for every normalized value (§5.3). Currently the module
   stores canonical values without the verbatim source string.
3. **Split the two evidence scales** — `EXPECTED_SCORES` is fine as a read-only record, but
   evidence grade must not be merged with Phase 2 coverage grade (H-01, H-08).
4. **Add `score_discrepancy_flag`** rather than relying only on the inline comment for Jules
   (H-02).
5. **Add a `provenance_note` column** for records whose Phase 1 provenance is narrative-only
   (H-15).
6. **Keep `EXPECTED_CAPABILITY_MATRIX` (Phase 6, 10 columns) and `EXPECTED_CAPABILITY_MATRIX_PH4`
   (4 columns) as the seed of the 21-key set**, and extend to the full union (§3.4).

The module's `BANNED_PATTERNS` and `JUDGMENT_LOCKED` lists are retained as-is and are the
mechanical basis for gates G3 and G1 respectively.

---

## Research Status

**Task 1 complete.** Established: entity model (§3), provenance model (§4), controlled
vocabularies (§5), content authority (§6), 20 semantic locks (§7), dependency graph (§8),
30 consistency hazards (§9), validation strategy (§10).

**No research content was created.** No ranking was introduced; no adoption or share number was
computed; no architecture detail was inferred; no product claim was asserted; no historical
judgment was modified.

**Open decision points for human sign-off before Task 2:** H-15 (Comate), H-02/H-03/H-12/H-14
(versioned corrections), and the §5.3 normalization decision log.
