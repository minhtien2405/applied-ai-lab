#!/usr/bin/env bash
# Hook: UserPromptSubmit (Claude Code) / preToolUse (Cursor, type=UserPrompt)
# Mục đích: NHẮC (advisory) chạy /eval trước khi ship/merge/PR/deploy nếu chưa có eval artifact gần đây.
# stdout (exit 0) -> context cho assistant. Hook KHÔNG tự chạy eval. LUÔN exit 0.

proj="${CLAUDE_PROJECT_DIR:-$PWD}"
log="$proj/.claude/.sync-log"

# Parse prompt
prompt=$(python3 -c 'import sys,json
try:
    data = sys.stdin.read()
    try:
        print(json.loads(data).get("prompt","") or "")
    except Exception:
        print(data if data else "")
except Exception:
    print("")' 2>/dev/null)

# Keyword gate — fire khi prompt có ý ship/merge/PR/deploy
if ! printf '%s' "$prompt" | grep -iqE 'ship|merge|pr |pull request|deploy|land|push to main|release|rollout|go live'; then
  exit 0
fi

# Bỏ qua nếu prompt đã nói đến eval — agent đã biết
if printf '%s' "$prompt" | grep -iqE '/eval|make eval|eval (run|result|output|delta|pass|fail)|regression|baseline'; then
  exit 0
fi

# Check artifact eval gần đây (eval/results/, .deepeval/, eval-results/) — trong 1 ngày
has_recent_eval=0
for d in "$proj/eval/results" "$proj/.deepeval" "$proj/eval-results" "$proj/.eval"; do
  if [ -d "$d" ]; then
    # Tìm file modified trong 24h
    if [ -n "$(find "$d" -type f -mtime -1 2>/dev/null | head -1)" ]; then
      has_recent_eval=1
      break
    fi
  fi
done

if [ "$has_recent_eval" -eq 0 ]; then
  printf '🪝 [pre-commit-eval] No eval artifact modified in the last 24h (checked eval/results/, .deepeval/, eval-results/). Before shipping, run `/eval` — eval evidence (aggregate + sliced, no slice regressing beyond tolerance) is required for any model/prompt/retrieval/threshold/data change. See `eval-driven-development` skill and `ml-production-mindset` rule.\n'
  printf '[%s] pre-commit-eval fired: no recent eval artifact\n' "$(date -u +%FT%TZ 2>/dev/null || date)" >> "$log" 2>/dev/null
fi

exit 0
