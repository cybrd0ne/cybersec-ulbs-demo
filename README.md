# secops-demo

A small self-hosted security telemetry stack, built as the reference project for
Cybersecurity Master's Module 4A at ULBS. It ingests Suricata-style telemetry, normalises
it to the Elastic Common Schema, runs tested Sigma detection content, enriches events
against live MISP threat intelligence, and operates behind CI/CD governance and an
observability stack. The engineering is driven from AI configuration in this repository,
and every change lands through a governed pull request.

This is the end state students build toward. Each of the seven sessions adds one working
increment, tagged `v0.1-session1` through `v1.0`.

## Scope and risk

The project is defined by its risk register, not the other way round. `RISK-REGISTER.md`
holds five rows across three registers: operational risk from the AI agent in the
engineering loop, internal risk in the security function, and external risk from the
threat landscape. Every control in the repository answers one row, and every pull request
names the rows it closes.

| ID | Register | What it addresses | Where it lands |
|----|----------|-------------------|----------------|
| R-01 | Operational | AI agent commits bypassing review | ruleset + governance workflow + pre-commit |
| R-02 | Operational | Plaintext secret committed | gitleaks + SOPS/age |
| R-03 | Internal | Broken normalisation blinds detections | pytest with positive and negative samples in CI |
| R-04 | External | Known-bad traffic goes unflagged | MISP to translate filter, telemetry tagged and scored |
| R-05 | External | Exposed service indexed by Shodan | daily Shodan diff and alert |

## Architecture

```
  Suricata EVE JSON ─▶ Logstash ─▶ OpenSearch ─▶ Dashboards ─▶ nginx front door (mTLS/TLS)
                         │  ECS mapping             ▲
                         │  MISP translate enrich   │
  MISP ──▶ ioc_ip.yml ───┘                          │
                                                     │
  elasticsearch-exporter ─▶ Prometheus ─▶ Alertmanager
                                  └────▶ Grafana
```

Components, all pinned by digest in `compose.yaml`: OpenSearch and Dashboards, a Logstash
pipeline, an nginx front door served with a cert from the lab PKI, an Elasticsearch
exporter, Prometheus, Alertmanager, and Grafana. Ports come from `.env`. Secrets come from
`.env.secrets`, decrypted at deploy time from the SOPS files under `secrets/`.

## The three graded items

**Security risk project.** Scope derived from `RISK-REGISTER.md`; working components that
build and run; a CI/CD pipeline (`.github/workflows/ci.yml`) that lints, tests, scans, and
releases on every pull request and tag, each job mapped to a risk in `docs/ci.md`; a
protected `main` enforced by the ruleset (`docs/ruleset-main.json`) and, on GitHub Free,
by the governance workflow.

**AI-driven configuration.** A root `CLAUDE.md` defining role, voice, banned patterns,
stack conventions and default commands; a compounding memory system under
`.claude/memory/` indexed by `MEMORY.md`; a repeatable workflow in `.claude/skills/check/
SKILL.md`; infrastructure-as-code generated and governed from this configuration; and an
Actions-based AI reviewer (`.github/workflows/review.yml`, `scripts/review.py`).

**Threat intelligence enrichment.** MISP pulled into `enrich/ioc_ip.yml` by
`scripts/misp_pull.py`, read by the Logstash `translate` filter in
`pipelines/suricata.conf`. A destination that matches a known-bad indicator is tagged
`threat.indicator.matched` and scored; a clean one is untouched. Shodan exposure comes
from `scripts/exposure_check.py`. Setup and evidence are in `docs/misp-setup.md`.

## Repository map

```
RISK-REGISTER.md        the register every control answers
CLAUDE.md               AI onboarding: role, conventions, banned patterns, commands
.claude/                memory (indexed by MEMORY.md) and skills
compose.yaml            the stack, images pinned by digest, ports from .env
Makefile                up / down / test / lint / secrets
.sops.yaml, secrets/    SOPS/age config and the encrypted admin secret (ciphertext only)
nginx/                  front door config and Dockerfile
pipelines/              Logstash ECS mapping and MISP enrichment
detections/             Sigma rule and its converted OpenSearch query
tests/                  pytest and the positive/negative sample corpus
scripts/                MISP pull, Shodan exposure check, AI PR reviewer
enrich/                 indicator dictionary (live file gitignored; .example committed)
monitoring/             Prometheus, Alertmanager, alert rules, Grafana provisioning
.github/workflows/      ci.yml, governance.yml, review.yml
docs/                   ci, pki, misp-setup, runbooks, evaluation walkthrough, evidence
```

## Run it

Prerequisites: Docker and Docker Compose v2, Make, Python 3.11 or later, plus `sops` and
`age` for secrets. On Linux set `vm.max_map_count=262144` or OpenSearch will not start.

```
cp .env.example .env
cp enrich/ioc_ip.yml.example enrich/ioc_ip.yml   # or run scripts/misp_pull.py
make up                                          # decrypts secrets, brings the stack up
make test                                        # runs the detection tests
make down                                        # tears down and removes .env.secrets
```

The admin secret in `secrets/opensearch.enc.yaml` is encrypted to an age key. Decrypting
it needs the private key at `~/.config/sops/age/keys.txt`. The committed file is ciphertext
only, so it is an example of shape; generate your own key and re-encrypt for a working
stack of your own.

## Account plan

This reference runs on a GitHub Free account, so the repository is public and governance
is proven by evidence: the ruleset where the account allows it, and otherwise the
`no-commit-to-branch` pre-commit hook plus the governance workflow that fails on any commit
reaching `main` outside a merged pull request. See `CONTRIBUTING.md`.

## Authorisation

This is teaching material for isolated lab targets. Threat-intelligence and exposure
queries stay lawful and scoped to assets the operator owns or is authorised to assess.
