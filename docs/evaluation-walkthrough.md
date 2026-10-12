# Evaluation walkthrough

The order to read this repository in, and what each item demonstrates. The professor
clones the repo for evaluation. The `v1.0` tag is the reference state.

## Read in this order

1. `RISK-REGISTER.md` — the five rows every control answers. Start here; the rest of the
   repository is this register implemented.
2. `README.md` — scope, architecture, and the map of which folder serves which graded item.
3. `CLAUDE.md`, `.claude/memory/`, `.claude/skills/` — the AI configuration that drives the
   work. The memory file is a real correction that persists across sessions.
4. `compose.yaml`, `Makefile`, `.sops.yaml`, `secrets/` — the stack as code, images pinned
   by digest, secrets encrypted. `git show HEAD:secrets/opensearch.enc.yaml` shows
   ciphertext only.
5. `.github/workflows/ci.yml` + `docs/ci.md` — each job mapped to the risk it guards.
6. `.github/workflows/governance.yml` + `docs/ruleset-main.json` — the R-01 controls and
   the GitHub Free evidence route.
7. `detections/`, `pipelines/`, `tests/` — the Sigma rule, its converted query, the ECS
   pipeline, and the pytest with positive and negative samples.
8. `scripts/misp_pull.py`, `pipelines/suricata.conf`, `docs/misp-setup.md` — the enrichment
   that changes an outcome (R-04), with evidence in `docs/evidence/`.
9. `monitoring/`, `docs/runbooks/` — Prometheus, Alertmanager, Grafana, and the alert whose
   runbook ships in the repo.
10. `.github/workflows/review.yml`, `scripts/review.py` — the automated reviewer that
    comments before a human approves.

## Release tags

| Tag | Session | Adds |
|-----|---------|------|
| v0.1-session1 | 1 | Risk register, ruleset, CODEOWNERS, SECURITY, pre-commit, governance |
| v0.2-session2 | 2 | CLAUDE.md, memory, skill |
| v0.3-session3 | 3 | Compose stack, SOPS secret, Makefile, PKI, front door |
| v0.4-session4 | 4 | CI pipeline, SBOM, signing, release |
| v0.5-session5 | 5 | Sigma rule, converted query, ECS pipeline, tests |
| v0.6-session6 | 6 | MISP pull, translate enrichment, Shodan exposure |
| v1.0 | 7 | Observability, alerting, automated review, documentation |

## What to probe

Every part of the submission should be understood and defensible. Good questions: why are
approvals set to 0 in the ruleset, why does the memory rule forbid gsub on the raw message,
what makes the enrichment change an outcome rather than just add a field, and how keyless
signing proves provenance without a stored key.
