# applied-ai-lab — Claude Code operating context

> **AI Systems Lab** — greenfield, public, MIT. 8-layer architecture (L1 Model Gateway → L8 Deploy). See [`README.md`](README.md) for the full architecture and roadmap.

## Agentic workflow pack

This repo ships a **portable AI/ML Applied Systems Engineer workflow pack** under [`.claude/skills/`](.claude/skills/) + [`.cursor/rules/`](.cursor/rules/). The pack is project-agnostic — it can be copied to any other repo and used as-is.

- **Pack overview**: [`.claude/skills/README.md`](.claude/skills/README.md) — 12 skills, 10 commands, 4 personas, 3 rules, 3 hooks.
- **Skill format**: [`docs/skill-anatomy.md`](docs/skill-anatomy.md)
- **Install elsewhere**: [`docs/install-to-other-repo.md`](docs/install-to-other-repo.md)
- **Attribution**: [`docs/adrs/0001-*.md`](docs/adrs/0001-adopt-karpathy-and-agent-skills-anatomy.md)

## Always-on rules (auto-loaded by Cursor)

- `karpathy-4-principles.mdc` — Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution (ML-adapted)
- `ml-honesty-discipline.mdc` — no inflated benchmark, no data leakage, offline-vs-online gap honest, ownership boundary
- `ml-production-mindset.mdc` — eval-gate before merge, fallback-first, observability-as-you-build, ADR for irreversible

## Commands (Claude Code)

`/spec` · `/plan` · `/build` · `/eval` ⭐ · `/review` · `/ship` · `/incident` · `/adr` · `/design` · `/skills-help`

See [`.claude/commands/`](.claude/commands/) for each command's wired skills.

## Project-specific notes (NOT part of the portable pack)

The block below is project-specific to `applied-ai-lab` and intentionally lives here, not in the pack.

### Current module status

- `eval/` — Tier 1 (skeleton landed): DeepEval + 10 golden + smoke tests + CI gate via [`.github/workflows/eval-gate.yml`](.github/workflows/eval-gate.yml)
- `modules/streaming-fraud-mini/` — Tier 0 (scaffolded, spec only)
- Other layers — planned per roadmap in [`README.md`](README.md)

### Lab principles (project-level, supplement the pack rules)

1. **One repo, evolving** — never spawn a new repo for a new tech; add a module
2. **Every PR has eval or benchmark** — no merging unmeasured code
3. **`docker compose up` + CI** — not Jupyter demos
4. **Pluggable, not rewritten** — new framework lands in a branch, gets benchmarked, then merged
5. **Public trace** — commits, benchmark reports, write-ups act as evidence of continuous learning

### Greenfield & IP boundary

This repo is fresh from scratch. It does not copy, fork, or reuse code from any current or former employer, or from any freelance/contract project. Design patterns are not copyrightable — implementing a pattern in clean, original code is skill demonstration, not IP reuse. See [`README.md`](README.md) "Greenfield & IP boundary".

## When the pack and the project conflict

The pack is generic; this `CLAUDE.md` is project-specific. If a project instruction conflicts with a pack rule, **project wins for this repo, pack wins for portability**. Resolve by editing this file (project override), not the pack.
