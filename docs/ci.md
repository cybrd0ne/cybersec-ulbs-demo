# CI/CD and the risk it guards

The pipeline in `.github/workflows/ci.yml` refuses to ship an unvalidated or unverified
artifact. Each job maps to a row in `RISK-REGISTER.md`, so the pipeline is the register
enforced on every change.

| Job | What it does | Risk it guards |
|-----|--------------|----------------|
| `lint` | ShellCheck on shell, hadolint on the Dockerfile, Semgrep with the `p/ci` ruleset | R-02 (Semgrep flags hardcoded secrets and unsafe patterns), general code quality |
| `test` | `pytest` over the detection and pipeline tests, with positive and negative samples | R-03 (a change that breaks normalisation fails the build) |
| `scan` | Build `frontdoor:ci`, scan with Trivy, fail on HIGH or CRITICAL | R-06: a vulnerable or outdated base image cannot merge |
| `release` | Push to GHCR, generate an SBOM with Syft, sign the image with Cosign keyless, cut a release with generated notes | R-06: the shipped image is inventoried and signed |

## Actions are pinned by commit SHA

Every `uses:` line names a full 40-character commit SHA, with the version in a comment:

```
- uses: aquasecurity/trivy-action@ed142fd0673e97e23eac54620cfb913e5ce36c25 # v0.36.0
```

A tag such as `@v4` or `@0.28.0` is a movable pointer. On 19 March 2026 attackers used
stolen credentials to force-push 76 of the 77 `trivy-action` tags to code that read CI
secrets (CVE-2026-33634, GHSA-69fq-xp46-6x23). Every pipeline that referenced those tags
ran the payload with its own tokens. A SHA cannot be repointed, so a pinned workflow keeps
running the code that was reviewed. This repository's first version used tags; Semgrep's
`github-actions-mutable-action-tag` rule in the `lint` job blocked it, and Dependabot
raised the advisory. That is R-06.

To update a pin, resolve the release you want to its commit and review the diff first:

```
gh api repos/aquasecurity/trivy-action/commits/v0.36.0 --jq .sha
```

`.github/dependabot.yml` has Dependabot read the trailing version comment and propose SHA
bumps as pull requests, for actions, pip, and the front door base image. A 7-day cooldown
holds back brand-new releases, since a hijacked release is usually caught within hours.
The front door base is pinned by tag and digest, and the Dockerfile applies Alpine security
fixes at build time, so the Trivy gate fails only on what is still unpatched.

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
