# Install the pack to another repo

This pack is portable. Copy it into any project's `.claude/` and `.cursor/` and use it as-is. No project-specific edits required.

## 7-step install checklist

1. **Copy skill pack** — `.claude/skills/` → `<target>/.claude/skills/`
2. **Copy commands** — `.claude/commands/` → `<target>/.claude/commands/`
3. **Copy sub-agent personas** — `.claude/agents/` → `<target>/.claude/agents/`
4. **Copy hooks** — `.claude/hooks/` → `<target>/.claude/hooks/` + merge `.claude/settings.json` (additive — see below)
5. **Copy Cursor rules** — `.cursor/rules/` → `<target>/.cursor/rules/` (3 `.mdc` files, `alwaysApplied: true`)
6. **Copy Cursor mirror** — `.cursor/skills/` + `.cursor/commands/` + `.cursor/hooks.json`
7. **Verify** — open Cursor in target repo → 3 rules auto-load; in Claude Code, `/eval` activates `eval-driven-development`.

Optional: copy `docs/skill-anatomy.md` and `docs/adrs/0001-*.md` if you want the format spec and attribution in the target. Not required for operation.

## Conflict avoidance

### Skill name clashes

If the target repo already has a skill with the same name (common with addyosmani's `eval-driven-development`, `code-review-and-quality`, `incremental-implementation`, etc.):

- **Option A (recommended)**: rename our skill's directory to `ml-<name>` and update the `name:` field in frontmatter + any references in commands.
- **Option B**: drop the conflicting upstream skill if our ML-tailored version supersedes it.
- **Option C**: keep both, prefix commands (`/ml-eval` vs `/eval`) to disambiguate.

Run `ls <target>/.claude/skills/` before copying to detect clashes.

### `settings.json` merge

`.claude/settings.json` here wires hooks. If the target already has one, **merge** keys — do not overwrite:

```jsonc
// Merge: combine "hooks" arrays, "permissions" objects, etc.
{
  "hooks": {
    "UserPromptSubmit": [
      // existing target hooks...
      { "command": ".claude/hooks/spec-before-code.sh" }   // our addition
    ]
  }
}
```

### `hooks.json` (Cursor) merge

Same additive principle for `.cursor/hooks.json`.

### Hook path portability

All hook scripts use **relative paths** (e.g. `.claude/.sync-log`, not `/abs/path/to/log`). They run from the target repo's root. Verify by `bash .claude/hooks/spec-before-code.sh` from target root — should `exit 0` cleanly.

## Symlink alternative (single-source-of-truth)

If you want one canonical copy and all other repos to point at it:

```bash
# From target repo
ln -s /path/to/applied-ai-lab/.claude/skills .claude/skills
ln -s /path/to/applied-ai-lab/.cursor/rules .cursor/rules
# ...etc
```

Caveats:
- Symlinks work on macOS/Linux. On Windows, use `mklink /D` (admin) or stick to copy.
- Cursor on Windows has historically had issues loading rules through symlinks — verify before committing to this approach.
- A symlinked pack means a single edit affects all repos using it — convenient for updates, risky for instability.

## After install: smoke test

```bash
# In target repo
grep -ri "applied-ai-lab\|L1\b\|L8\b\|8-layer" .claude/skills/ .claude/agents/ .claude/commands/ .cursor/rules/
# Expected: 0 matches (pack stays portable)
```

If matches appear, the pack was edited with project-specific references — clean them up before committing.
