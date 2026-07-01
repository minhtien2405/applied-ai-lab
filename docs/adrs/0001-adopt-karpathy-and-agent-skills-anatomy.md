# ADR-0001 — Adopt Karpathy 4 principles + addyosmani SKILL.md anatomy for the AI/ML Applied Systems Engineer workflow pack

- **Status**: Accepted
- **Date**: 2026-07-01
- **Deciders**: repo owner
- **Context**: AI/ML Applied Systems Engineer workflow pack (`applied-ai-lab/.claude/` + `.cursor/`)

## Context

The pack needs a **shape** (how skills are structured, how the lifecycle is divided) and a **discipline baseline** (always-on rules that prevent common LLM failure modes). Two public repos address these well:

1. **`forrestchang/andrej-karpathy-skills`** (MIT) — distills Andrej Karpathy's observations on LLM coding pitfalls into 4 principles: Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution. Single `CLAUDE.md`, ~50 lines, framework-agnostic.

2. **`addyosmani/agent-skills`** (MIT) — production-grade skill pack for AI coding agents. Defines a `SKILL.md` anatomy (Frontmatter → Overview → When → Process → Rationalizations → Red Flags → Verification), a lifecycle shape (DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP), and design choices ("process not prose", "anti-rationalization table", "verification non-negotiable", "progressive disclosure"). 24 skills, 8 commands, 4 personas, 7 reference checklists. Content is web/fullstack-heavy.

## Decision

Adopt **principles and anatomy** from both repos. **Do not copy files.** Write all content from scratch, tailored to the work of an AI/ML Applied Systems Engineer (ML, LLM, agentic, RAG, model serving, drift, incident response).

### Borrowed (with attribution)

| From | What we borrow | How it's adapted |
|---|---|---|
| `forrestchang/andrej-karpathy-skills` | 4 principles + "state assumptions, surface tradeoffs, success criteria verifiable" | Adapted to ML context (e.g. "state eval hypothesis before code", "don't tune baseline without ADR"). Lives in `.cursor/rules/karpathy-4-principles.mdc` as always-on rule. |
| `addyosmani/agent-skills` | `SKILL.md` anatomy (7 sections); lifecycle shape; "process not prose"; anti-rationalization table; "verification non-negotiable"; progressive disclosure; sub-agent persona pattern; "personas don't invoke personas" rule | Applied to ML-specific workflows (eval-driven-development, spec-ml-system, model-serving-design, drift-and-sliced-eval, etc.). Lifecycle extended with OPERATE + DOCUMENT phases (incident response, ADRs). `/test` renamed `/eval` (eval is primary verification for ML, not unit tests). |

### Not borrowed

- 24 skill contents (web/fullstack-heavy: frontend-ui-engineering, web-performance-auditor, browser-testing-with-devtools, etc.)
- 4 persona contents (web-perf auditor, generic code-reviewer)
- 8 command contents (verbatim)
- `plugin.json`, `.gemini/`, `.opencode/`, `.claude-plugin/` packaging
- The Karpathy repo's exact `CLAUDE.md` wording

### Why from scratch

1. **Audience fit.** addyosmani targets general software engineers working on web/fullstack. Our audience is AI/ML Applied Systems Engineers working on ML/LLM/agentic systems. The failure modes differ (non-determinism, drift, judge variance, fallback storms, offline-vs-online gap) and require ML-specific workflows.

2. **Portability.** Skills must work in any target repo (big tech, side project, day job) without referencing a specific architecture. Borrowed files often embed assumptions about their home repo.

3. **IP cleanliness.** Writing from scratch keeps the pack uncontaminated by upstream-specific framing. Attribution is explicit (this ADR + pack README + each `SKILL.md` footer where relevant).

## Alternatives considered

- **Full pack install (addyosmani plugin marketplace).** Rejected: imports 24 skills with web-irrelevant content; noise in context window; lock-in to upstream release cadence; hard to customize for ML.
- **Vendor copy of addyosmani + Karpathy files.** Rejected: would inherit upstream framing; harder to keep ML-tailored; license-compliant but semantically wrong shape for ML work.
- **Separate repo for the pack.** Postponed: adds maintenance overhead before the pack is proven. Current plan: prove in `applied-ai-lab/` first, extract to its own repo when stable (post-ADR-0002 if needed).

## Consequences

- **Positive**: Pack is ML-tailored, portable, IP-clean, dual-publishes to Claude Code + Cursor.
- **Positive**: Attribution clear; upstreams credited in pack README + this ADR.
- **Negative**: More upfront writing work than vendor-copy.
- **Negative**: Must keep upstream anatomy in sync manually (if addyosmani evolves the SKILL.md format, we adopt changes deliberately, not automatically).

## Attribution

- Karpathy principles source: <https://github.com/forrestchang/andrej-karpathy-skills> (MIT) — original observations by Andrej Karpathy.
- SKILL.md anatomy + lifecycle source: <https://github.com/addyosmani/agent-skills> (MIT) — by Addy Osmani and contributors.

Both upstreams are MIT-licensed. This pack is also MIT (see root `LICENSE`).
