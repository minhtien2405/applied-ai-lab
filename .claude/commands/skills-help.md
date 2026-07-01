---
description: Meta command — list all skills, commands, agents, and rules in this pack with a decision matrix for when to use each.
---

Show me a decision matrix for this AI/ML Applied Systems Engineer workflow pack.

## Skills (12)

| Skill | Phase | When to use |
|---|---|---|
| `eval-driven-development` ⭐ | BUILD/VERIFY | Every model/prompt/data change — primary verification |
| `spec-ml-system` | DEFINE | Starting a new ML feature or significant change |
| `incremental-implementation` | BUILD | Change touches > 1 file |
| `model-serving-design` | DESIGN | Building gateway / fallback / cache / routing |
| `rag-system-design` | DESIGN | Building retrieval / RAG / rerank |
| `mcp-tool-server-build` | DESIGN | Building MCP server / tool calling |
| `drift-and-sliced-eval` | VERIFY/MONITOR | Production monitoring, post-deploy validation |
| `observability-for-ml-systems` | OPERATE | Shipping to production, adding telemetry |
| `debugging-ml-failures` | VERIFY | Non-deterministic failures, eval flakiness |
| `code-review-ml` | REVIEW | Before merging any ML-relevant change |
| `ml-incident-response` | OPERATE | Active production incident |
| `documentation-and-adrs-ml` | DOCUMENT | Irreversible decision, runbook |

## Commands (10)

| Command | Activates | Phase |
|---|---|---|
| `/spec` | spec-ml-system | DEFINE |
| `/plan` | inline | PLAN |
| `/build` | incremental-implementation + eval-driven-development | BUILD |
| `/eval` ⭐ | eval-driven-development | VERIFY |
| `/review` | code-review-ml + drift-and-sliced-eval | REVIEW |
| `/ship` | inline + observability-for-ml-systems | SHIP |
| `/incident` | ml-incident-response | OPERATE |
| `/adr` | documentation-and-adrs-ml | DOCUMENT |
| `/design` | routes to model-serving / rag / mcp | DESIGN |
| `/skills-help` | this | META |

## Sub-agent personas (4)

| Persona | When to invoke via Task tool |
|---|---|
| `eval-engineer` | Design golden set, pick metric, regression tolerance |
| `ml-staff-reviewer` | Pre-ship staff-bar review |
| `ml-incident-responder` | Triage non-deterministic incident |
| `model-serving-architect` | Gateway / fallback / cache design review |

Rule: personas don't invoke personas.

## Always-on rules (3, in `.cursor/rules/`)

- `karpathy-4-principles.mdc` — Think Before Coding / Simplicity / Surgical / Goal-Driven
- `ml-honesty-discipline.mdc` — no inflated benchmark, no data leakage, offline-vs-online honest
- `ml-production-mindset.mdc` — eval-gate, fallback-first, observability-as-you-build, ADR for irreversible

## Quick decision guide

| Situation | Use |
|---|---|
| Vague ask, don't know what to build | `/spec` |
| Have a spec, need to break it down | `/plan` |
| Ready to code a slice | `/build` |
| Need to verify a change | `/eval` |
| PR ready, want staff review | `/review` |
| Want to ship | `/ship` |
| Production is broken | `/incident` |
| Irreversible decision pending | `/adr` |
| Designing serving / RAG / MCP | `/design` |
| Lost, need a map | `/skills-help` (this) |
