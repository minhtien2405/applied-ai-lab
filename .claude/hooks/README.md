# Hooks

Three shell-level reminders for the AI/ML Applied Systems Engineer workflow pack. All hooks are **advisory only** — they print reminders to stdout (which becomes context for the assistant to act on). They never write semantic content themselves; the LLM does that. All hooks `exit 0` always.

## Design rules (non-negotiable)

- **Always `exit 0`** — never block the agent, even on error.
- **Relative paths** — use `$CLAUDE_PROJECT_DIR` (Claude Code) or `$PWD` fallback. No absolute paths.
- **APPEND-only log** — write to `.claude/.sync-log`, never overwrite.
- **Keyword-gated** — only fire reminders when the prompt matches relevant keywords. Don't spam every turn.
- **JSON parse via `python3`** — portable across macOS / Linux / Windows git-bash. Don't rely on `jq` being installed.

## Hooks

| Hook | Trigger | Fires when | Reminder |
|---|---|---|---|
| `spec-before-code.sh` | UserPromptSubmit | Prompt mentions "implement / fix / build / add / create" + no spec in `docs/specs/` or ADR in `docs/adrs/` matches the topic | "Consider `/spec` before coding — state the eval hypothesis first" |
| `pre-commit-eval-reminder.sh` | UserPromptSubmit | Prompt mentions "ship / merge / PR / deploy / land" + no recent eval artifact | "Run `/eval` before shipping — eval evidence required" |
| `baseline-guard.sh` | PostToolUse (Write\|Edit\|MultiEdit) | Tool edited a file matching `**/baseline.json` | "baseline.json was edited — requires an ADR + fresh eval run; see `ml-honesty-discipline` rule" |

## Wiring

- **Claude Code**: `.claude/settings.json` — hooks block with `matcher` + `command`.
- **Cursor**: `.cursor/hooks.json` — hooks block with `command` + `matcher`.

Both files use additive wiring — when copying to a target repo with existing hooks, **merge** the arrays, don't overwrite. See `docs/install-to-other-repo.md`.

## Log file

`.claude/.sync-log` — APPEND-only record of hook fires. Truncate manually after acting on reminders:

```bash
: > .claude/.sync-log
```

The log is gitignored — add to `.gitignore` if not already:
```
.claude/.sync-log
```

## Portability

Tested on:
- macOS (bash 3.2+, python3)
- Linux (bash 4+, python3)
- Windows (git-bash + python3 in PATH)

If `python3` is not in PATH, the JSON parse silently returns empty string and the hook still exits 0 — graceful degradation.
