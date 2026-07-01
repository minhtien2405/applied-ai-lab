# AI/ML Applied Systems Engineer — Agentic Workflow Pack

> Production-grade skill pack for AI/ML **Applied Systems Engineers** working on ML, LLM, agentic, RAG, and model-serving systems in any environment (big tech, day job, side project). Portable by design — copy to any repo and use.

This pack is **project-agnostic**. It contains no references to any specific repo, architecture, or product. It can be dropped into any project's `.claude/` and `.cursor/` and used as-is.

## What's inside

- **12 skills** — workflows an AI/ML Applied Systems Engineer follows across the lifecycle
- **10 slash commands** — entry points that activate skills
- **4 sub-agent personas** — specialist reviewers called via the Task tool
- **3 always-on rules** — Karpathy 4 principles (ML-adapted) + ML honesty + ML production mindset
- **3 hooks** — shell-level reminders for spec-before-code, eval-before-ship, baseline-tamper guard

## Lifecycle

```text
  DEFINE          PLAN           BUILD          VERIFY         REVIEW          SHIP
 ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
 │ Spec │ ───▶ │ Plan │ ───▶ │ Build│ ───▶ │ Eval │ ───▶ │Review│ ───▶ │ Ship │
 │ ML   │      │Tasks │      │Slice │      │Regress│     │ 5-axis│     │Observe│
 └──────┘      └──────┘      └──────┘      └──────┘      └──────┘      └──────┘
  /spec          /plan          /build        /eval         /review        /ship

                                                       OPERATE          DOCUMENT
                                                      ┌──────┐         ┌──────┐
                                                      │Incident│       │ ADR  │
                                                      │ Response│      │ Runbook│
                                                      └──────┘         └──────┘
                                                       /incident        /adr
```

## Skills

| # | Skill | Phase | Use when |
|---|---|---|---|
| ⭐ | `eval-driven-development` | BUILD/VERIFY | Every model/prompt/data change — primary verification for the pack |
| 1 | `spec-ml-system` | DEFINE | Starting a new ML feature or significant change |
| 2 | `incremental-implementation` | BUILD | Any change touching more than one file |
| 3 | `model-serving-design` | DESIGN | Building model gateway, fallback, cache, routing |
| 4 | `rag-system-design` | DESIGN | Building retrieval, rerank, RAG pipeline |
| 5 | `mcp-tool-server-build` | DESIGN | Building MCP server / tool calling |
| 6 | `drift-and-sliced-eval` | VERIFY/MONITOR | Production monitoring, post-deploy validation |
| 7 | `observability-for-ml-systems` | OPERATE | Adding telemetry, shipping to production |
| 8 | `debugging-ml-failures` | VERIFY | Tests fail, eval regresses, behavior is non-deterministic |
| 9 | `code-review-ml` | REVIEW | Before merging any ML-relevant change |
| 10 | `ml-incident-response` | OPERATE | Production ML incident — regression, drift, fallback storm |
| 11 | `documentation-and-adrs-ml` | DOCUMENT | Architectural decisions, runbooks, API docs |

## Commands

| Command | Activates | Phase |
|---|---|---|
| `/spec` | `spec-ml-system` | DEFINE |
| `/plan` | inline task breakdown | PLAN |
| `/build` | `incremental-implementation` + `eval-driven-development` | BUILD |
| `/eval` ⭐ | `eval-driven-development` | VERIFY |
| `/review` | `code-review-ml` + `drift-and-sliced-eval` | REVIEW |
| `/ship` | inline ship checklist + `observability-for-ml-systems` | SHIP |
| `/incident` | `ml-incident-response` | OPERATE |
| `/adr` | `documentation-and-adrs-ml` | DOCUMENT |
| `/design` | routes to `model-serving-design` / `rag-system-design` / `mcp-tool-server-build` | DESIGN |
| `/skills-help` | meta — list everything + decision matrix | META |

## Sub-agent personas (Task tool)

| Persona | Lens |
|---|---|
| `eval-engineer` | "Prove-It" — golden set design, regression tolerance, judge variance |
| `ml-staff-reviewer` | "Staff ML engineer approve?" — 5-axis review + eval-not-skipped + data-leakage |
| `ml-incident-responder` | Non-deterministic failure triage — flakiness vs real regression |
| `model-serving-architect` | Gateway, fallback ladder, cache, routing — never-500, cost-aware |

Rule: **personas don't invoke personas** — prevents orchestration loops.

## Always-on rules (`.cursor/rules/`)

- `karpathy-4-principles.mdc` — Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution, adapted for ML
- `ml-honesty-discipline.mdc` — no inflated benchmark, no data leakage, offline-vs-online gap honest, ownership boundary
- `ml-production-mindset.mdc` — eval-gate before merge, fallback-first, observability-as-you-build, ADR for irreversible

## Install to any repo

See [`docs/install-to-other-repo.md`](../../docs/install-to-other-repo.md) for the 7-step copy/symlink checklist + conflict-avoidance rules.

## Attribution

This pack borrows (does not copy):
- The **SKILL.md anatomy** (Frontmatter → Overview → When → Process → Rationalizations → Red Flags → Verification) and the **lifecycle shape** (DEFINE→PLAN→BUILD→VERIFY→REVIEW→SHIP) from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT).
- The **4 Karpathy principles** (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution) from [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) (MIT) — original observations by Andrej Karpathy.

All skill/rule/hook/agent content is written from scratch. No files were copied from either upstream repo. See [`docs/adrs/0001-adopt-karpathy-and-agent-skills-anatomy.md`](../../docs/adrs/0001-adopt-karpathy-and-agent-skills-anatomy.md).

## License

MIT — see root `LICENSE` (or specify). Use freely in any project, team, or company.
