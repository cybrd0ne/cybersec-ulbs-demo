# CI/CD and the risk it guards

The pipeline in `.github/workflows/ci.yml` refuses to ship an unvalidated or unverified
artifact. Each job maps to a row in `RISK-REGISTER.md`, so the pipeline is the register
enforced on every change.

| Job | What it does | Risk it guards |
|-----|--------------|----------------|
| `lint` | ShellCheck on shell, hadolint on the Dockerfile, Semgrep with the `p/ci` ruleset | R-02 (Semgrep flags hardcoded secrets and unsafe patterns), general code quality |
| `test` | `pytest` over the detection and pipeline tests, with positive and negative samples | R-03 (a change that breaks normalisation fails the build) |
| `scan` | Build `frontdoor:ci`, scan with Trivy, fail on HIGH or CRITICAL | Supply-chain: a vulnerable or outdated base image cannot merge |
| `release` | Push to GHCR, generate an SBOM with Syft, sign the image with Cosign keyless, cut a release with generated notes | Supply-chain integrity: the shipped image is inventoried and signed |

## How the gate holds

`lint`, `test`, and `scan` are required status checks on `main` (see
`docs/ruleset-main.json`). A pull request cannot merge while any of them is red, and a
direct push to `main` is rejected. On a GitHub Free account the governance workflow adds
the evidence that the change arrived through a merged pull request.

`release` runs only on a tag that starts with `v`, and only after `lint`, `test`, and
`scan` have passed. Keyless signing uses the OIDC token from Actions as the identity:
Fulcio issues a short-lived certificate and Rekor records the signature, so no long-lived
signing key is stored.

## Verifying a release from outside

```
cosign verify ghcr.io/cybrd0ne/secops-demo/frontdoor:v0.4-session4 \
  --certificate-identity-regexp "github.com/cybrd0ne/secops-demo" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
syft ghcr.io/cybrd0ne/secops-demo/frontdoor:v0.4-session4 -o table | head
```
