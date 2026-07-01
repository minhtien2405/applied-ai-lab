# AGENTS.md — Cursor agent operating context for applied-ai-lab

> AI Systems Lab — greenfield, public, MIT. 8-layer architecture. See [`README.md`](README.md).

## Agentic workflow pack

A portable **AI/ML Applied Systems Engineer** workflow pack lives in this repo:

| Path | Purpose |
|------|---------|
| [`.claude/skills/`](.claude/skills/) | 12 skills (process workflows). Mirror at [`.cursor/skills/`](.cursor/skills/) |
| [`.claude/commands/`](.claude/commands/) | 10 slash commands. Mirror at [`.cursor/commands/`](.cursor/commands/) |
| [`.claude/agents/`](.claude/agents/) | 4 sub-agent personas (Task tool) |
| [`.claude/hooks/`](.claude/hooks/) | 3 hook scripts + `settings.json` wiring |
| [`.cursor/rules/`](.cursor/rules/) | 3 always-on rules (`alwaysApplied: true`) |
| [`.cursor/hooks.json`](.cursor/hooks.json) | Cursor hook wiring |
| [`docs/skill-anatomy.md`](docs/skill-anatomy.md) | `SKILL.md` format spec |
| [`docs/install-to-other-repo.md`](docs/install-to-other-repo.md) | Copy pack to another repo |
| [`docs/adrs/0001-*.md`](docs/adrs/0001-adopt-karpathy-and-agent-skills-anatomy.md) | Attribution to upstream repos |

## Quick entry for agents

1. Read [`CLAUDE.md`](CLAUDE.md) for project context.
2. Read [`.claude/skills/README.md`](.claude/skills/README.md) for the pack overview.
3. The 3 rules in [`.cursor/rules/`](.cursor/rules/) are **always-on** — no need to invoke them.
4. Slash commands (`/spec`, `/build`, `/eval` ⭐, `/review`, `/ship`, `/incident`, `/adr`, `/design`, `/plan`, `/skills-help`) activate the relevant skills.

## Project vs pack

- **Project** (this repo): 8-layer architecture, `eval/` skeleton, `modules/streaming-fraud-mini/` spec, roadmap in `README.md`, Lab principles (every PR has eval, pluggable-not-rewritten, docker-compose-up, public trace).
- **Pack** (portable): skills/rules/agents/commands/hooks — no reference to this repo's architecture. Safe to copy elsewhere.

If a project instruction conflicts with a pack rule, **project wins for this repo**, **pack wins for portability**. Edit `CLAUDE.md` (project override), not the pack.
