.PHONY: install eval test test-smoke lint typecheck clean

install:
	pip install -e ".[dev]"

# Run full eval suite (DeepEval regression — requires OPENAI_API_KEY or DEEPEVAL_MODEL endpoint)
eval:
	pytest tests/ -m eval --deepeval

# Run smoke tests only (no LLM call, fast — for CI without secrets)
test-smoke:
	pytest tests/ -m smoke

# Run all tests
test:
	pytest tests/

lint:
	ruff check . --fix

typecheck:
	mypy eval/ tests/

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache .deepeval_cache __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
