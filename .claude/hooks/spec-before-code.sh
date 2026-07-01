#!/usr/bin/env bash
# Hook: UserPromptSubmit (Claude Code) / preToolUse (Cursor, type=UserPrompt)
# Mục đích: NHẮC (advisory) chạy /spec trước khi code nếu prompt có ý "implement/fix/build X"
#   mà chưa có spec/ADR cho topic đó. stdout (exit 0) -> context cho assistant.
# Hook KHÔNG tự viết spec. LUÔN exit 0.

proj="${CLAUDE_PROJECT_DIR:-$PWD}"
log="$proj/.claude/.sync-log"
specs_dir="$proj/docs/specs"
adrs_dir="$proj/docs/adrs"

# Parse prompt từ JSON stdin (Claude Code gửi JSON; một số Cursor config gửi plain text)
prompt=$(python3 -c 'import sys,json
try:
    data = sys.stdin.read()
    try:
        print(json.loads(data).get("prompt","") or "")
    except Exception:
        print(data if data else "")
except Exception:
    print("")' 2>/dev/null)

# Keyword gate — chỉ fire khi prompt có ý implement/fix
if ! printf '%s' "$prompt" | grep -iqE 'implement|fix|build|add (a |an |the )?|create|develop|tune|refactor|optimize|train|fine-tune|prompt tweak|change the (model|prompt|retrieval|threshold)'; then
  exit 0
fi

# Bỏ qua nếu prompt đã nói đến spec/adr/eval — agent đã biết
if printf '%s' "$prompt" | grep -iqE '/spec|/adr|spec-ml-system|already spec|eval-driven|hypothesis'; then
  exit 0
fi

# Check xem có spec/ADR hay không (nếu dirs trống -> nhắc)
has_specs=0
has_adrs=0
[ -d "$specs_dir" ] && [ -n "$(ls -A "$specs_dir" 2>/dev/null)" ] && has_specs=1
[ -d "$adrs_dir" ] && [ -n "$(ls -A "$adrs_dir" 2>/dev/null)" ] && has_adrs=1

if [ "$has_specs" -eq 0 ] && [ "$has_adrs" -eq 0 ]; then
  printf '🪝 [spec-before-code] No specs in docs/specs/ and no ADRs in docs/adrs/. Before coding, consider `/spec` — state the metric the change should move (current baseline → target → reason). Eval hypothesis before implementation (Karpathy "Think Before Coding"). If the change is irreversible (model choice, threshold, schema), also run `/adr`.\n'
  printf '[%s] spec-before-code fired: no specs/ADRs found\n' "$(date -u +%FT%TZ 2>/dev/null || date)" >> "$log" 2>/dev/null
elif [ "$has_adrs" -eq 0 ]; then
  printf '🪝 [spec-before-code] Specs exist but no ADRs in docs/adrs/. If this change is irreversible (model choice, threshold, schema, eval framework), run `/adr` before merging.\n'
fi

exit 0
