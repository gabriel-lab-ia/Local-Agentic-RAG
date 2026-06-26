.PHONY: lint format test check rag validate

lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	uv run pytest

check: format lint test validate
	git diff --check

rag:
	uv run python -m src.rag.chat_technical

validate:
	uv run python scripts/validate_repository.py
