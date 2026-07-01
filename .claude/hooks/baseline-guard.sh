#!/usr/bin/env bash
# Hook: PostToolUse (Write|Edit|MultiEdit) — Claude Code & Cursor
# Mục đích: NHẮC (advisory) khi baseline.json bị edit — yêu cầu ADR + fresh eval run
#   để chống "tuning baseline for pass". stdout (exit 0) -> context. LUÔN exit 0.

proj="${CLAUDE_PROJECT_DIR:-$PWD}"
log="$proj/.claude/.sync-log"

# Parse tool input từ JSON stdin — Claude Code PostToolUse gửi JSON có tool_name + tool_input.file_path
payload=$(python3 -c 'import sys,json
try:
    data = sys.stdin.read()
    try:
        obj = json.loads(data)
        # Claude Code shape
        ti = obj.get("tool_input") or {}
        fp = ti.get("file_path") or ti.get("path") or ""
        tn = obj.get("tool_name") or ""
        print(tn + "\t" + fp)
    except Exception:
        print("")
except Exception:
    print("")' 2>/dev/null)

file_path=$(printf '%s' "$payload" | cut -f2-)

# Gate — chỉ fire khi file path kết thúc bằng baseline.json
if [ -z "$file_path" ]; then
  exit 0
fi
case "$file_path" in
  *baseline.json|*baseline_scores.json|*golden_baseline.json)
    ;;
  *)
    exit 0
    ;;
esac

# Đã đủ cảnh báo — in nhắc
printf '🪝 [baseline-guard] %s was edited. Baseline updates require: (1) a documented reason (model upgrade, golden set expansion, metric definition change); (2) an ADR at docs/adrs/ (run /adr); (3) a fresh eval run proving the new baseline is real. Tuning the baseline to pass a regression is dishonest — see ml-honesty-discipline rule. If this edit was unintended (e.g. auto-format), revert it.\n' "$file_path"
printf '[%s] baseline-guard fired: %s\n' "$(date -u +%FT%TZ 2>/dev/null || date)" "$file_path" >> "$log" 2>/dev/null

exit 0
