---
description: Route to the right ML system design skill — model-serving-design, rag-system-design, or mcp-tool-server-build — based on what's being designed.
---

I need to design an ML system. First, classify which design skill applies based on the ask below, then activate that skill and walk me through it.

Routing rules:
- **Model serving / LLM gateway / inference routing / fallback / cache / cost-aware routing** → `model-serving-design`
- **RAG / retrieval / hybrid search / rerank / grounding / RAGAS-style eval** → `rag-system-design`
- **MCP server / LLM tool calling / tool functions / tool selection** → `mcp-tool-server-build`
- Mixed? Pick the primary one and note the secondary.

If the ask is ambiguous, ask me one clarifying question to disambiguate before picking. Don't silently pick.

After picking, run the chosen skill's process: state requirements → design → write the design doc / ADR. Do NOT write implementation code in this turn — design first, implement via `/build` later.

Constraints:
- Numbers for requirements (latency / cost / quality / availability), not "fast and cheap".
- ADR / design doc committed before implementation.
- Failure modes named with eval cases.

Ask: $ARGUMENTS
