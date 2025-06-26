.PHONY: ruff clean build run

ruff:
	uv run ruff format
	uv run ruff check --fix

clean:
	find . -name '*.pyc' -exec rm -f {} + || true
	find . -name '*.pyo' -exec rm -f {} + || true
	find . -name '*~' -exec rm -f {} + || true
	find . -name '__pycache__' -exec rm -fr {} + || true
	find . -name '.pytest_cache' -exec rm -fr {} + || true
	uv run ruff clean

build:
	docker compose -f docker/docker-compose.yaml build

run: build
	docker compose -f docker/docker-compose.yaml up