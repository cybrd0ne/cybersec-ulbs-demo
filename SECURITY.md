# Security policy

Report issues privately to the repository owner. Do not open a public issue for a
vulnerability.

Secrets are never committed in plaintext (R-02). All secrets are SOPS-encrypted under
`secrets/` and decrypted only at deploy time; the age private key stays on the machine.

All changes land through a reviewed pull request (R-01). Direct pushes to `main` are
rejected by the ruleset, or on a GitHub Free account by the governance workflow and the
`no-commit-to-branch` pre-commit hook.

## Supported scope

This is a teaching reference stack for isolated lab targets. Intelligence queries and
exposure checks stay lawful and scoped to assets the operator owns or is authorised to
assess.
