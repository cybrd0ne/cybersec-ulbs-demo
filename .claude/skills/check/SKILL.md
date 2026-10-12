---
name: check
description: Run lint and tests, summarise failures by file, propose the smallest fix.
---

Run this when the user says `/check` or asks to validate the repository before a commit
or pull request.

1. Run `make lint` and `make test`.
2. Group failures by file. For each, quote the failing line.
3. Propose the minimal change. Do not apply it without confirmation.

Report nothing but the grouped failures and the proposed fixes. If both commands pass,
say so in one line.
