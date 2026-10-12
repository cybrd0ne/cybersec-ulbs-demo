# Contributing

Every change arrives as a pull request. `main` is protected: direct pushes are rejected
and failing checks block the merge.

## Pull request workflow

1. Branch from `main`. Use conventional commit subjects, for example
   `feat(detect): long DNS TXT rule`.
2. Open the pull request. The first line of the description names the risk IDs it
   addresses, for example `Addresses: R-01, R-02`.
3. Wait for the required checks: `lint`, `test`, `scan`, and the AI review on
   `review.yml`. They must pass before merge.
4. A reviewer approves. On a solo repository the governance workflow is the standing
   evidence that the change arrived through a pull request.

## Secrets

Never commit a plaintext secret. Add new secrets to a SOPS-encrypted file under
`secrets/`. The pre-commit gitleaks hook will reject a commit that carries a key.

## Local checks before you push

Run `pre-commit run --all-files` and `make test`. Install the hooks once with
`pre-commit install` so the `no-commit-to-branch` guard is active in your clone.
