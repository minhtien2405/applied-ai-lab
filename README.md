# applied-ai-lab

> **AI Systems Lab** — a personal, production-grade playground for experimenting with production AI systems: agentic AI, model gateway, evaluation harness, observability, memory, MCP, multi-agent orchestration.
>
> Not a demo. Not a startup. A long-running lab (2–3 years) where each new technology (MCP, harness, loop engineering, vLLM, SGLang, OpenAI Agents SDK...) gets **plugged in as a module** rather than spawning a new repo.

## Why this exists

Primary day job is Fraud/Risk ML at scale. This lab keeps the LLM/Agentic/AI-Systems lane sharp in parallel — so the answer to *"do you still do LLM?"* is never *"I used to, at a previous company"*, but rather:

> *"In parallel to my Fraud ML role, I maintain an AI Systems Lab where I integrate and benchmark new technologies — agentic orchestration, MCP, evaluation harness, model routing, memory, observability — before they go mainstream. Every change runs through an eval harness; every quarter a new capability lands."*

## Architecture — 8 layers

```text
                  ┌─────────────────┐
                  │     Portal      │   ← API gateway / minimal UI
                  └────────┬────────┘
                           │
   ┌───────────┬───────────┼───────────┬───────────┬───────────┬───────────┬───────────┐
   ▼           ▼           ▼           ▼           ▼           ▼           ▼           ▼
 L1 Model   L2 Agent    L3 Knowledge L4 Memory   L5 Tool     L6 Eval     L7 Observ  L8 Deploy
 Gateway    Runtime                                  System     Harness    ability
```

| Layer | Purpose | Stack (target) |
|---|---|---|
| **L1 Model Gateway** | One interface for all models; swap models without touching business logic | LiteLLM · OpenAI · Anthropic · Gemini · Qwen · vLLM · Ollama · Bedrock |
| **L2 Agent Runtime** | Where LangGraph / OpenAI Agents SDK / A2A live; graph execution, state, checkpoint, HITL | LangGraph · OpenAI Agents SDK · planner/executor/reflection |
| **L3 Knowledge** | Vector + hybrid search + rerank; plug new embeddings easily | Qdrant · BM25 · bge-reranker · embedding models · semantic cache |
| **L4 Memory** | Conversation → long-term → semantic → episodic → user profile | Redis · Postgres · vectorized memory |
| **L5 Tool System** | Standard tool calling — MCP is default | MCP servers · REST · SQL · filesystem · browser |
| **L6 Evaluation Harness** ⭐ | Every prompt/model change → press Evaluate → run N tests → know if better | RAGAS · custom judge (cross-family) · golden set · regression · CI gate |
| **L7 Observability** | "Grafana for Agents" — trace, latency, cost, hallucination, failure | OpenTelemetry · LangSmith / Langfuse · dashboards |
| **L8 Deployment** | Real production — not a Jupyter demo | Docker · FastAPI · Redis · queue · GPU · autoscaling |

## Module status

| Module | Layer | Tier | Status |
|---|---|---|---|
| `eval/` | L6 | 0 | 🚧 Q3 2026 — first capability |
| `gateway/` | L1 | 0 | planned Q2 2027 |
| `runtime/` | L2 | 0 | planned Q4 2026 |
| `knowledge/` | L3 | 0 | planned Q1 2027 |
| `memory/` | L4 | 0 | planned Q4 2027 |
| `tools/` | L5 | 0 | planned Q4 2026 |
| `obs/` | L7 | 0 | planned 2028 |
| `deploy/` | L8 | 0 | planned Q3 2027 |

**Tier definitions:**

- **Tier 0** — planned, not started
- **Tier 1 (skeleton)** — folder + module README + 1 smoke test
- **Tier 2 (functional)** — `docker compose up` works + 1 demo use-case + tracing
- **Tier 3 (production-grade)** — eval harness + CI gate + benchmark report + architecture doc

## Roadmap

| Quarter | Capability | Layer | Target tier |
|---|---|---|---|
| **Q3 2026** | Eval Harness + CI Gate | L6 | skeleton → functional |
| Q4 2026 | MCP Tool Server + Agent Use-Case | L5 + L2 | skeleton → functional |
| Q1 2027 | Voice/Streaming Path (or Multimodal) | L1 + L3 | functional |
| Q2 2027 | Multi-Agent Orchestration (A2A) | L2 | functional |
| Q3 2027 | Benchmark Inference + Cost Routing | L1 + L8 | production-grade (L1) |
| Q4 2027 | Memory Layers | L4 | functional |
| 2028 | Observability + Production Hardening | L7 + L8 | production-grade |

> Quarters may shift with day-job workload, but **no skipping 2 consecutive quarters**. Minimum for a busy quarter: 1 small capability + 1 write-up.

## Principles

1. **One repo, evolving** — never spawn a new repo for a new tech; add a module
2. **Every PR has eval or benchmark** — no merging unmeasured code
3. **`docker compose up` + CI** — not Jupyter demos
4. **Pluggable, not rewritten** — new framework lands in a branch, gets benchmarked, then merged
5. **Public trace** — commits, benchmark reports, write-ups act as evidence of continuous learning

## Anti-patterns avoided

- ❌ Chat-PDF / chatbot / RAG demo (everyone has one in 2026)
- ❌ New repo every quarter, abandon the old one
- ❌ Jupyter-only demos
- ❌ Unmeasured "I read the paper" claims — every integration has a number

## Quick start (placeholder)

```bash
# Target once Q3 2026 L6 lands:
git clone https://github.com/minhtien2405/applied-ai-lab.git
cd applied-ai-lab
docker compose up -d
make eval          # run eval harness on golden subset
make bench         # benchmark inference configs
```

Until then, this README is the contract.

## License

MIT (or specify later).
