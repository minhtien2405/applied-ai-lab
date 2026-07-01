---
description: Five-axis code review for ML/LLM/agentic PRs — correctness, eval discipline, production-readiness, honesty, maintainability. Activates code-review-ml + drift-and-sliced-eval.
---

Activate the `code-review-ml` and `drift-and-sliced-eval` skills. Review the PR / diff I name below.

Run the five-axis review:
1. **Correctness** — edge cases, data flow (point-in-time features, train/eval split), caching, concurrency.
2. **Eval discipline** — eval case added? eval result attached (aggregate + sliced)? baseline unchanged without ADR? slice regressions?
3. **Production-readiness** — fallback for new external dep? feature flag? observability added? cost delta estimated? rollback path?
4. **Honesty** — claims match eval evidence? no over-claim of ownership (check git blame if needed)? offline-vs-online gap stated? no silent baseline/threshold/golden-set edit?
5. **Maintainability** — readable? no speculative abstraction? no orphaned code? matched existing style? tests will fail loudly on regression?

For each axis: verdict (approve / request changes / block) + 1-line justification.

Label every comment: Block / Request changes / Nit / FYI.

End with:
- **Verdict**: approve / request changes / block
- **Staff-engineer bar**: would a staff ML engineer approve this? If no, what's missing?
- **Top 1-2 fixes** (if any)

Don't merge if any Block is unresolved.

Target: $ARGUMENTS
