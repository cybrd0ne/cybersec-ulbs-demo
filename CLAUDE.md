# CLAUDE.md — secops-demo

The onboarding file for the AI assistant working in this repository. It governs the code
and infrastructure the assistant generates. Read it at the start of every session, and
read `.claude/memory/MEMORY.md` for standing corrections.

## Role

You are the engineering assistant for a self-hosted security telemetry project: a
Logstash enrichment pipeline feeding OpenSearch, with Sigma detection content, MISP
threat-intelligence enrichment, and an observability stack. The work is driven from this
configuration and lands through governed pull requests.

## Conventions

- Stack: Docker Compose v2, Logstash 8.x, OpenSearch 2.x, Python 3.11, Bash.
- Pipelines live in `pipelines/`, tests in `tests/`, detection content in `detections/`,
  helper scripts in `scripts/`, docs in `docs/`.
- Every pipeline or rule gets a pytest with one positive and one negative sample.
- Never hardcode ports or hostnames; read them from `.env`.
- Images are pinned by digest, never by a floating tag.
- Secrets are SOPS-encrypted files under `secrets/`; never write a plaintext secret.
- Every change references the risk IDs it addresses (see `RISK-REGISTER.md`), and the
  pull request description opens with `Addresses: R-0x`.

## Banned patterns

- Floating image tags (`:latest`, bare `:2.19.1` without a digest).
- Hardcoded ports, hostnames, passwords, or API keys anywhere in tracked files.
- `mutate { gsub => ... }` on the raw `message` field before it is parsed; parse first,
  then mutate (see `.claude/memory/no-gsub-on-raw-message.md`).
- Em dashes, and filler words such as "delve", "leverage", "furthermore", "it is
  important to note".

## Writing

Plain English, active voice, no em dashes, no filler. Lead with the point. Lists are for
data or sequential steps, not for prose.

## Default commands

- `make up` — decrypt secrets and bring the stack up.
- `make down` — tear the stack down and remove the decrypted env file.
- `make test` — run the detection and pipeline tests.
- `make lint` — run ShellCheck, hadolint, and Semgrep locally.
- `make secrets` — decrypt `secrets/*.enc.yaml` into `.env.secrets`.

## How to work here

Plan before large changes. Keep each pull request scoped to one risk row where possible.
When you are corrected, write the correction to `.claude/memory/` as its own file and add
a line to `.claude/memory/MEMORY.md`, so the rule persists into the next session.
