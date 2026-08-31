# -*- coding: utf-8 -*-
"""
Phase 8 canonical entity map — Case 001 (2026 AI Coding Agent Landscape).

Single source of truth for Phase 8 validation gates. All values are copied
VERBATIM from the locked Phase 1–7 research record; nothing here is
recomputed. Scores are historical Phase 3 records that may only be read and
compared, never recalculated (Phase 8 spec §28–31, §36).

Research Snapshot: 2026-08-31
"""

# ---------------------------------------------------------------------------
# Locked Phase 3 Top 10 — order and composite scores verbatim from
# 03-top10-selection.md §3.1 / §9. (Research ranking, NOT user-count ranking.)
# ---------------------------------------------------------------------------

EXPECTED_TOP10 = [
    "Claude Code",
    "Codex",
    "Cursor",
    "GitHub Copilot",
    "Devin",
    "Google Antigravity",
    "Replit Agent",
    "OpenCode",
    "Qoder",
    "Factory",
]

# name -> (market, capability, innovation, ecosystem, momentum, composite)
# Composite printed in the source document; NOT recomputed here.
EXPECTED_SCORES = {
    "Claude Code":         (5.0, 5.0, 5.0, 5.0, 5.0, 5.00),
    "Codex":               (5.0, 5.0, 5.0, 5.0, 5.0, 5.00),
    "Cursor":              (5.0, 5.0, 5.0, 5.0, 4.5, 4.95),
    "GitHub Copilot":      (5.0, 4.5, 4.5, 5.0, 4.5, 4.70),
    "Devin":               (4.0, 5.0, 5.0, 5.0, 4.5, 4.65),
    "Google Antigravity":  (3.5, 5.0, 5.0, 5.0, 5.0, 4.55),
    "Replit Agent":        (4.0, 4.5, 5.0, 4.5, 4.5, 4.45),
    "OpenCode":            (3.5, 4.5, 5.0, 4.5, 5.0, 4.35),
    "Qoder":               (3.5, 4.5, 5.0, 4.5, 5.0, 4.35),
    "Factory":             (2.5, 5.0, 5.0, 4.5, 5.0, 4.20),
    # Near-miss / boundary candidates (03-top10-selection.md §3.1)
    "TRAE":                (3.5, 4.5, 4.5, 4.5, 4.5, 4.20),
    "Kiro":                (2.5, 4.5, 5.0, 5.0, 5.0, 4.10),
    "OpenHands":           (3.0, 4.5, 4.5, 4.5, 4.0, 4.00),
    "Augment Code":        (2.5, 5.0, 4.5, 4.0, 4.5, 4.00),
    "JetBrains AI / Junie":(3.5, 4.0, 4.0, 5.0, 4.0, 3.95),
    "Tencent CodeBuddy":   (2.5, 4.0, 4.5, 4.5, 4.5, 3.75),
    "Kimi Code":           (2.5, 4.0, 4.5, 4.0, 5.0, 3.75),
    "Cline":               (3.0, 4.0, 4.0, 4.0, 4.0, 3.70),
    # Jules: source document prints 3.70; its dimension scores compute to 3.75
    # under the stated formula. The printed value is preserved verbatim and
    # flagged in 08-sources.md (Known discrepancies).
    "Jules":               (2.0, 4.5, 4.5, 4.5, 4.5, 3.70),
    "Qwen Code":           (2.0, 4.0, 4.5, 4.0, 4.5, 3.55),
}

# ---------------------------------------------------------------------------
# Phase 1 candidate universe classes (01-candidate-universe.md)
# ---------------------------------------------------------------------------

PHASE1_CLASS_CORE = [
    "Claude Code", "Codex", "GitHub Copilot", "Cursor", "Devin",
    "Google Antigravity", "Kiro", "Replit Agent", "OpenCode", "OpenHands",
    "Cline", "Qoder", "TRAE", "Tencent CodeBuddy", "JetBrains AI / Junie",
    "Kimi Code", "Amazon Q Developer",
]

PHASE1_CLASS_SECONDARY = [
    "Jules", "Mistral Vibe", "Qwen Code", "Goose", "Aider", "SWE-agent",
    "mini-SWE-agent", "Kilo Code", "Warp", "Continue", "Amp", "Augment Code",
    "Factory", "Poolside", "Zed AI", "Bolt.new", "v0", "CodeRabbit", "Qodo",
]

PHASE1_CLASS_WATCHLIST = [
    "DeepSeek Reasonix", "Lovable", "Plandex", "Crush", "Refact.ai",
    "Greptile", "Cubic", "Tabnine",
]

# Phase 1 excluded table (01-candidate-universe.md §8) — 6 objects.
PHASE1_CLASS_EXCLUDED = [
    "Pure Models (GPT / Claude / Gemini / Qwen / DeepSeek)",
    "Roo Code",
    "Sweep",
    "Gemini CLI",
    "Tongyi Lingma",
    "Plugin-only coding extensions",
]

# Baidu Comate: appears in Phase 1 §5.1 China signals with sources but has no
# formal class/grade row in the Phase 1 tables. Included with class "Unknown"
# per Phase 8 spec §5.1 (standard Unknown for missing data).
PHASE1_CLASS_UNKNOWN = ["Comate (Baidu)"]

# Canonical universe: candidate_name -> phase1_class (single lookup used by
# the validator and CSV builders). Core/Secondary/Watchlist from
# 01-candidate-universe.md §4–§6; Excluded from §8 (6 objects verbatim);
# Comate with class "Unknown" per spec §5.1.
CANDIDATE_UNIVERSE = {}
for _name in PHASE1_CLASS_CORE:
    CANDIDATE_UNIVERSE[_name] = "Core"
for _name in PHASE1_CLASS_SECONDARY:
    CANDIDATE_UNIVERSE[_name] = "Secondary"
for _name in PHASE1_CLASS_WATCHLIST:
    CANDIDATE_UNIVERSE[_name] = "Watchlist"
for _name in PHASE1_CLASS_EXCLUDED:
    CANDIDATE_UNIVERSE[_name] = "Excluded"
for _name in PHASE1_CLASS_UNKNOWN:
    CANDIDATE_UNIVERSE[_name] = "Unknown"

# ---------------------------------------------------------------------------
# Phase 3 selection statuses (03-top10-selection.md)
# ---------------------------------------------------------------------------

SELECTION_STATUSES = {
    # Selected — exactly the locked Top 10
    "Claude Code": "Selected", "Codex": "Selected", "Cursor": "Selected",
    "GitHub Copilot": "Selected", "Devin": "Selected",
    "Google Antigravity": "Selected", "Replit Agent": "Selected",
    "OpenCode": "Selected", "Qoder": "Selected", "Factory": "Selected",
    # Near-miss (scored, not selected)
    "TRAE": "Near-miss", "Kiro": "Near-miss", "OpenHands": "Near-miss",
    "Augment Code": "Near-miss", "JetBrains AI / Junie": "Near-miss",
    "Tencent CodeBuddy": "Near-miss", "Kimi Code": "Near-miss",
    "Cline": "Near-miss", "Qwen Code": "Near-miss",
    # Boundary — Phase 3 labels Jules "Boundary / Reserve" (compound label;
    # kept in rationale text, single vocabulary value "Boundary" in CSV)
    "Jules": "Boundary",
    # Amazon Q Developer: Phase 3 does not score it; treated as legacy /
    # migration lineage into Kiro, explicitly outside the modern ranking
    # population (03-top10-selection.md §7.4)
    "Amazon Q Developer": "Excluded",
    # Remaining Phase 1 Secondary/Watchlist candidates: no Phase 3 score,
    # no explicit Phase 3 status
    "Mistral Vibe": "Not-in-final-top10", "Goose": "Not-in-final-top10",
    "Aider": "Not-in-final-top10", "SWE-agent": "Not-in-final-top10",
    "mini-SWE-agent": "Not-in-final-top10", "Kilo Code": "Not-in-final-top10",
    "Warp": "Not-in-final-top10", "Continue": "Not-in-final-top10",
    "Amp": "Not-in-final-top10", "Poolside": "Not-in-final-top10",
    "Zed AI": "Not-in-final-top10", "Bolt.new": "Not-in-final-top10",
    "v0": "Not-in-final-top10", "CodeRabbit": "Not-in-final-top10",
    "Qodo": "Not-in-final-top10", "DeepSeek Reasonix": "Not-in-final-top10",
    "Lovable": "Not-in-final-top10", "Plandex": "Not-in-final-top10",
    "Crush": "Not-in-final-top10", "Refact.ai": "Not-in-final-top10",
    "Greptile": "Not-in-final-top10", "Cubic": "Not-in-final-top10",
    "Tabnine": "Not-in-final-top10",
    "Comate (Baidu)": "Not-in-final-top10",
}

# ---------------------------------------------------------------------------
# Phase 6 Agent Matrix (06-cross-product-analysis.md §6) — verbatim C/P/U.
# Capability columns shared with products.csv. "P/C" (Antigravity
# verification) maps to "Partial" in the CSV with a note.
# ---------------------------------------------------------------------------

EXPECTED_CAPABILITY_MATRIX = {
    "Claude Code": {
        "planning": "C", "context": "C", "tools": "C", "execution": "C",
        "verification": "C", "repair": "C", "long_running": "C",
        "multi_agent": "C", "memory": "C",
    },
    "Codex": {
        "planning": "C", "context": "C", "tools": "C", "execution": "C",
        "verification": "C", "repair": "C", "long_running": "C",
        "multi_agent": "C", "memory": "P",
    },
    "Cursor": {
        "planning": "C", "context": "C", "tools": "C", "execution": "C",
        "verification": "C", "repair": "C", "long_running": "C",
        "multi_agent": "C", "memory": "P",
    },
    "GitHub Copilot": {
        "planning": "C", "context": "C", "tools": "C", "execution": "C",
        "verification": "C", "repair": "C", "long_running": "C",
        "multi_agent": "C", "memory": "C",
    },
    "Devin": {
        "planning": "C", "context": "C", "tools": "C", "execution": "C",
        "verification": "C", "repair": "C", "long_running": "C",
        "multi_agent": "C", "memory": "C",
    },
    "Google Antigravity": {
        "planning": "C", "context": "C", "tools": "C", "execution": "C",
        "verification": "P/C", "repair": "C", "long_running": "C",
        "multi_agent": "C", "memory": "P",
    },
    "Replit Agent": {
        "planning": "C", "context": "C", "tools": "C", "execution": "C",
        "verification": "C", "repair": "C", "long_running": "C",
        "multi_agent": "C", "memory": "P",
    },
    "OpenCode": {
        "planning": "C", "context": "C", "tools": "C", "execution": "C",
        "verification": "C", "repair": "C", "long_running": "P",
        "multi_agent": "C", "memory": "P",
    },
    "Qoder": {
        "planning": "C", "context": "C", "tools": "C", "execution": "C",
        "verification": "C", "repair": "C", "long_running": "C",
        "multi_agent": "C", "memory": "C",
    },
    "Factory": {
        "planning": "C", "context": "C", "tools": "C", "execution": "C",
        "verification": "C", "repair": "C", "long_running": "C",
        "multi_agent": "C", "memory": "P",
    },
}

# Phase 4-derived expected states for the four columns NOT in the Phase 6
# matrix (04-products/*.md capability sections, normalized per the Phase 8
# spec §7.3 mapping). Values: Confirmed / Partial / Unknown / Not primary.
EXPECTED_CAPABILITY_MATRIX_PH4 = {
    "Claude Code": {"mcp": "Confirmed", "skills": "Confirmed",
                    "sandbox": "Confirmed", "cloud_agent": "Confirmed"},
    "Codex": {"mcp": "Confirmed", "skills": "Confirmed",
              "sandbox": "Confirmed", "cloud_agent": "Confirmed"},
    "Cursor": {"mcp": "Confirmed", "skills": "Confirmed",
               "sandbox": "Confirmed", "cloud_agent": "Confirmed"},
    "GitHub Copilot": {"mcp": "Confirmed", "skills": "Confirmed",
                       "sandbox": "Confirmed", "cloud_agent": "Confirmed"},
    "Devin": {"mcp": "Confirmed", "skills": "Partial",
              "sandbox": "Confirmed", "cloud_agent": "Confirmed"},
    "Google Antigravity": {"mcp": "Confirmed", "skills": "Confirmed",
                           "sandbox": "Confirmed", "cloud_agent": "Partial"},
    "Replit Agent": {"mcp": "Partial", "skills": "Partial",
                     "sandbox": "Confirmed", "cloud_agent": "Confirmed"},
    "OpenCode": {"mcp": "Confirmed", "skills": "Confirmed",
                 "sandbox": "Partial", "cloud_agent": "Not primary"},
    "Qoder": {"mcp": "Confirmed", "skills": "Confirmed",
              "sandbox": "Confirmed", "cloud_agent": "Confirmed"},
    "Factory": {"mcp": "Confirmed", "skills": "Partial",
                "sandbox": "Confirmed", "cloud_agent": "Partial"},
}

# ---------------------------------------------------------------------------
# Phase 7 canonical vocabularies (07-decision.md) — verbatim labels
# ---------------------------------------------------------------------------

# Leadership map (07 §8) — category judgments, NOT an overall ranking.
LEADERSHIP_LABELS = [
    "Market Adoption Leader",
    "Terminal SWE Agent Leader",
    "Open-source Agent Harness Leader",
    "AI-native IDE / Distributed Workspace Leader",
    "GitHub Lifecycle Leader",
    "Delegated Multi-agent Leader",
    "Agent-Fleet / Autonomous SWE Leader",
    "Agent Command Center Leader",
    "Idea-to-Production Leader",
    "Persistent Task-centric Leader",
    "Enterprise Deploy-anywhere Runtime Leader",
]

LEADERSHIP_MAP = {
    "Claude Code": ["Market Adoption Leader", "Terminal SWE Agent Leader"],
    "OpenCode": ["Open-source Agent Harness Leader"],
    "Cursor": ["AI-native IDE / Distributed Workspace Leader"],
    "GitHub Copilot": ["GitHub Lifecycle Leader"],
    "Codex": ["Delegated Multi-agent Leader"],
    "Devin": ["Agent-Fleet / Autonomous SWE Leader"],
    "Google Antigravity": ["Agent Command Center Leader"],
    "Replit Agent": ["Idea-to-Production Leader"],
    "Qoder": ["Persistent Task-centric Leader"],
    "Factory": ["Enterprise Deploy-anywhere Runtime Leader"],
}

# Category map (07 §6) — categories allow overlap.
CATEGORY_LABELS = [
    "Terminal SWE Agent",
    "AI-native IDE / Distributed Workspace",
    "GitHub Lifecycle Agent",
    "Delegated Multi-agent SWE",
    "Persistent Task-centric Agent",
    "Idea-to-Production Agent",
    "Enterprise Autonomous SWE Control Plane",
    "Open / Provider-agnostic Harness",
]

CATEGORY_MAP = {
    "Terminal SWE Agent": ["Claude Code", "OpenCode", "Codex"],
    "AI-native IDE / Distributed Workspace": ["Cursor", "Qoder"],
    "GitHub Lifecycle Agent": ["GitHub Copilot"],
    "Delegated Multi-agent SWE": ["Codex", "Devin", "Google Antigravity"],
    "Persistent Task-centric Agent": ["Qoder"],
    "Idea-to-Production Agent": ["Replit Agent"],
    "Enterprise Autonomous SWE Control Plane": ["Factory", "Devin"],
    "Open / Provider-agnostic Harness": ["OpenCode"],
}

# Strategic layer model (07 §5) — stack order, bottom to top.
STRATEGIC_LAYERS = [
    "Model", "Harness", "Runtime", "Context / Memory", "Tools",
    "Orchestration", "Workflow", "Distribution",
]

# Workflow evolution chain (07 §10.1) — verbatim, 8 stages.
WORKFLOW_CHAIN = [
    "Code Completion",
    "Code / File Editing",
    "Issue / Task Resolution",
    "Repository-level Execution",
    "Project / Product Work",
    "Delegated Agent Workstream",
    "Parallel Agent Portfolio",
    "Engineering Workflow Automation",
]

# Strategic scenarios (07 §12) — labels verbatim; no Bull/Bear/Base exist.
SCENARIO_LABELS = [
    "Scenario A — Model Dominates",
    "Scenario B — Agent System Dominates",
    "Scenario C — Workflow Platform Dominates",
]

# Capability commoditization tiers (07 §9) — verbatim item lists.
COMMODITIZATION = {
    "Commodity": [
        "Basic code generation",
        "Repository search / basic codebase context",
        "Terminal access",
        "Basic planning",
        "Basic testing / command execution",
        "MCP support",
        "Skills / reusable instructions",
        "Multi-file editing",
    ],
    "Differentiating": [
        "Reliable verification / repair",
        "Long-running execution",
        "Context / memory quality",
        "Agent orchestration",
        "Environment integration",
        "Human steering / review UX",
    ],
    "Potential moat": [
        "Runtime infrastructure",
        "Workflow integration",
        "Orchestration / control plane",
        "Organizational memory / context graph",
        "Verification / evaluation system",
        "Distribution",
    ],
}

# ---------------------------------------------------------------------------
# Controlled vocabularies (Phase 8 spec §6.3, §7.3, §8)
# ---------------------------------------------------------------------------

PHASE1_CLASS_VOCAB = ["Core", "Secondary", "Watchlist", "Excluded", "Unknown"]
PHASE3_STATUS_VOCAB = ["Selected", "Near-miss", "Boundary", "Reserve",
                       "Not-in-final-top10", "Excluded"]
CAPABILITY_VALUE_VOCAB = ["Confirmed", "Partial", "Unknown", "Not primary"]
EVIDENCE_GRADE_VOCAB = ["A", "B", "C", "D"]
CONFIDENCE_VOCAB = ["High", "Medium-High", "Medium", "Medium-Low", "Low"]
AGENTIC_LEVEL_VOCAB = [
    "Agentic Coding Tool",
    "Software Engineering Agent",
    "Autonomous Software Engineering Agent",
]
CLAIM_TYPE_VOCAB = [
    "Fact", "Market Evidence", "Product Evidence", "Benchmark Evidence",
    "Analysis", "Judgment", "Hypothesis", "Unknown",
]
SOURCE_TYPE_VOCAB = [
    "Official Product", "Official Documentation", "Official Blog",
    "Official Release Note", "Official Company Announcement",
    "Independent Survey", "Independent Research", "Benchmark",
    "Technical Paper", "Community", "Individual Review",
]

# ---------------------------------------------------------------------------
# Banned patterns (Phase 8 spec §30) — positive claims that must NOT appear.
# The allowed negative statements (e.g. "no defensible market-share table")
# are deliberately NOT matched by these patterns.
# ---------------------------------------------------------------------------

BANNED_PATTERNS = [
    # Unsupported market-share claims
    "市占率",                # any positive "% 市占率" phrasing
    "市场份额",              # "X 拥有全球市场份额 / 控制市场份额"
    "market share of",      # positive share claims
    "controls .*%",         # e.g. "controls 39% of global market"
    "全球第二", "全球第一",  # unsupported global rank claims
    "best AI coding agent",
    "best agent",
    "best coding agent",
    "2026 Best",
    "Overall Rating",
    "Best Product",
    "Most Powerful Agent",
    "Best Architecture",
    "Best Benchmark",
    "Best Enterprise Agent",
    "capability score",
    "moat score",
    "leadership score",
    "scenario probability",
    "will own .*%",
    "2028 forecast",
    "2030 forecast",
    "by 2028",
    "by 2030",
    "8/10",
    "9/10",
    # Invented architecture claims / false precision
    "planner architecture X",
    "uses .* planner",
]

# ---------------------------------------------------------------------------
# Verbatim judgment-locked strings (Phase 7) — assets must contain these
# exact strings (positive gate, checked by the validator).
# ---------------------------------------------------------------------------

JUDGMENT_LOCKED = [
    "As of August 31, 2026, AI Coding Agent is best understood as an umbrella market of agentic software-engineering systems, not a single homogeneous product category. The technical substrate is converging; the product boundary is diverging.",
    "Model",
    "Agent System",
    "Workflow",
    "There is no defensible single global AI Coding Agent market-share table for August 2026 using the evidence reviewed here.",
    "The technical substrate is converging; the product boundary is diverging.",
]
