---
name: mcp-tool-server-build
description: Guides agents through building MCP (Model Context Protocol) servers and tool-calling interfaces — tool boundary, idempotency, error semantics, schema discipline, eval for tool-use. Use when building MCP servers, tool functions for LLM agents, or tool-calling pipelines.
---

# mcp-tool-server-build

## Overview

Build MCP servers and LLM tool-calling interfaces that are safe, predictable, and evaluable. The hard parts are not "register a function" — they're tool boundary design (what's a tool vs a prompt vs a resource), idempotency (called twice ≠ double charge), error semantics (return structured errors, don't throw), and eval for tool selection (does the model call the right tool at the right time?).

## When to Use

- Building an MCP server
- Adding tools to an LLM agent
- Designing a tool-calling pipeline (planner → tool → executor)
- Hitting "the model calls the wrong tool" or "the tool fails silently" symptoms

Do **not** use for: internal helper functions the model never calls directly (just write them normally).

## Process

1. **Decide tool boundary.**
   - Tool: model invokes, gets structured result back, side effects happen. (e.g. `search_docs`, `send_email`, `query_db`).
   - Resource: model reads, no side effects. (e.g. `file://docs/policy.md`).
   - Prompt: reusable prompt template, no execution. (e.g. `code-review-prompt`).
   - Heuristic: if it has side effects or returns dynamic data → tool. If it's static reference → resource. If it's a reusable instruction → prompt.
   - Exit criteria: tool/resource/prompt classification for each capability.

2. **Design tool schemas.**
   - JSON Schema for inputs. Required vs optional explicit. Enum for constrained fields. Description for every field — the model reads these to decide what to pass.
   - Output: structured object, not free text. Include `success: bool`, `error_code: str | null`, `data: ...`, `metadata: {latency_ms, cost, ...}`.
   - Don't overload one tool with many modes — split into focused tools. The model picks better from a clear menu than from a flag-heavy function.
   - Exit criteria: schema for each tool, with descriptions and example outputs.

3. **Design idempotency.**
   - Tools with side effects (write, send, charge) must be idempotent: same call twice = same effect as once.
   - Idempotency key: caller passes a unique key; server tracks processed keys within a TTL.
   - Without idempotency, a retry doubles the side effect (double email, double charge).
   - Exit criteria: idempotency strategy for every side-effecting tool.

4. **Design error semantics.**
   - Return errors as structured responses, not exceptions. `{"success": false, "error_code": "rate_limited", "retry_after_s": 60}`.
   - Error codes are part of the schema — the model can learn to retry, fall back, or report to the user.
   - Don't throw — exceptions inside a tool call break the model's ability to reason about what happened.
   - Exit criteria: error code enum + per-code schema (fields, retry hint).

5. **Design permissions and sandboxing.**
   - Tools have least-privilege scope. A `read_docs` tool shouldn't have filesystem write.
   - Side-effecting tools require explicit user confirmation in the agent runtime (HITL).
   - Sandbox network and filesystem access — don't let a tool escape its scope.
   - Exit criteria: permission scope per tool + HITL list for side-effecting tools.

6. **Design tool-selection eval.**
   - Golden set: prompts + reference tools that should be called + reference arguments.
   - Metric: tool selection accuracy (right tool called), argument correctness (right args passed), call efficiency (no redundant calls), recovery (handles tool error gracefully).
   - Failure-mode cases: prompt that should call no tool, prompt that should call 3 tools in sequence, prompt where the model is tempted to call the wrong tool.
   - Exit criteria: eval harness for tool selection, with golden set frozen.

7. **Design observability.**
   - Per-call trace: tool name, arguments, result, latency, success/error code, idempotency key, caller (model + request ID).
   - Aggregate metrics: calls per tool, error rate per tool, p95 latency per tool, retry rate, HITL confirmation rate.
   - Alert on: error rate spike per tool, latency spike, unexpected tool call patterns.
   - Exit criteria: trace schema + per-tool metric list + alert thresholds.

8. **Write the design doc / ADR.**
   - Tool inventory, schemas, idempotency, error semantics, permissions, eval, observability — all in one doc.
   - Exit criteria: ADR committed before implementation.

## Rationalizations

| Excuse | Rebuttal |
|---|---|
| "Idempotency is overkill for v1" | Without idempotency, the first retry doubles the side effect. Add it with the tool, not after. |
| "Throwing exceptions is simpler" | Exceptions break model reasoning. Structured errors let the model decide: retry, fall back, or report. |
| "One tool with many flags is easier to maintain" | Models pick worse from flag-heavy functions. Split into focused tools; the model's selection accuracy will improve. |
| "Tool descriptions are nice-to-have" | The model reads descriptions to choose tools and args. Missing descriptions → wrong tool or wrong args. |
| "Tool eval can wait until the agent works" | Without tool-selection eval, you can't tell if a fix improved selection or broke it. Build the eval with the tools. |
| "Permissions can be tightened later" | Loosening permissions later is easy; tightening after a tool has escaped its scope requires a security incident. Start least-privilege. |
| "HITL is friction" | HITL on side-effecting tools is the difference between "model sent an email" and "model sent 10,000 emails". Friction is the point. |

## Red Flags

- Tool throws exceptions instead of returning structured errors — model can't reason about failures.
- Side-effecting tool with no idempotency key — retry doubles the effect.
- One tool with 8 flags — model will pick wrong flags. Split it.
- Tool descriptions empty or vague — model will misuse the tool.
- No tool-selection eval — you're tuning blind.
- Side-effecting tool without HITL confirmation — accident waiting to happen.
- Tool has broader filesystem/network access than it needs — escape scope risk.
- Per-tool error rate not tracked — silent tool degradation.

## Verification

Before this skill is complete:

- **Tool inventory**: each tool classified (tool/resource/prompt) with reason.
- **Schemas**: input JSON Schema with descriptions + output structured shape with `success/error_code/data/metadata`.
- **Idempotency**: strategy for every side-effecting tool (idempotency key + TTL).
- **Error semantics**: error code enum + per-code schema (fields, retry hint).
- **Permissions**: least-privilege scope per tool; HITL list for side-effecting tools.
- **Eval**: tool-selection accuracy + argument correctness + call efficiency + recovery; golden set frozen; failure-mode cases included.
- **Observability**: trace schema + per-tool metric list + alert thresholds.
- **ADR**: committed before implementation.
