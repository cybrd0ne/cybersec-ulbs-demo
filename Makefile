.PHONY: up down test lint secrets clean

# Decrypt secrets to .env.secrets, then bring the stack up with both env files.
up: secrets
	docker compose --env-file .env --env-file .env.secrets up -d

# Tear down and remove the decrypted secrets so they never linger on disk.
down:
	docker compose down -v && rm -f .env.secrets

# Decrypt every SOPS file under secrets/ into KEY=VALUE lines in .env.secrets.
secrets:
	sops -d secrets/opensearch.enc.yaml | sed 's/: /=/' > .env.secrets

# Detection and pipeline tests.
test:
	pip install -r requirements-dev.txt -q && pytest -q

# Local static analysis, mirroring the lint job in ci.yml.
lint:
	shellcheck $$(git ls-files '*.sh') 2>/dev/null || true
	hadolint nginx/Dockerfile
	semgrep scan --config p/ci --error

clean: down
	rm -f .env.secrets
