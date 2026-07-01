---
description: Specify an ML/LLM/agentic system from business problem to eval + fallback plan, before coding. Activates spec-ml-system skill.
---

Activate the `spec-ml-system` skill and walk me through writing a spec for the ask below. Do NOT write any code in this turn — output a spec doc.

Spec doc sections to fill:
1. Problem (one sentence the user will agree with)
2. Success criteria — offline (metric + current + target + tolerance) and online (validation plan)
3. Data plan — sources, freshness, point-in-time, split strategy, golden set freeze
4. Eval plan — metric formulas, judge config, slicing dimensions
5. Fallback strategy — fallback ladder + which level the eval will test
6. Risks — top 3 + which need ADRs
7. Open questions — list, even if empty after I answer

Ask me one question at a time, in order. Don't batch. If my answer is ambiguous, push back (Karpathy "Think Before Coding").

Save the completed spec to `docs/specs/<short-title>.md` (create the dir if missing) and link it from the eventual implementing PR.

Ask: $ARGUMENTS
