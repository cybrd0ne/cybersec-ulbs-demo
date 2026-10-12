"""Automated pull-request reviewer.

Reads a unified diff, loads the project rules (CLAUDE.md) and the risk register as context,
and asks Claude for concrete findings tied to risk IDs. Posts the result as a sticky PR
comment via review.yml. The model is a cheaper execution model (Sonnet) deliberately; the
stronger model is kept for human judgment.

Usage:
    python scripts/review.py pr.diff > review.md
"""
import sys
import pathlib
import anthropic

# Current Sonnet model id. The lab guide wrote "claude-sonnet-5-5"; the id is this.
MODEL = "claude-sonnet-5"

diff = pathlib.Path(sys.argv[1]).read_text()[:60000]
if not diff.strip():
    print("## Automated review\n\nNo diff to review.")
    sys.exit(0)

ctx = "\n\n".join(
    pathlib.Path(f).read_text()
    for f in ("CLAUDE.md", "RISK-REGISTER.md")
    if pathlib.Path(f).exists()
)

msg = anthropic.Anthropic().messages.create(
    model=MODEL,
    max_tokens=2000,
    system=(
        "You review pull requests for a security engineering project. Follow the project "
        "rules below. Report concrete findings only, each with file, line, severity and "
        "the related risk ID. If there are none, say so in one line.\n\n" + ctx
    ),
    messages=[{"role": "user", "content": "Review this diff:\n\n" + diff}],
)

text = "".join(block.text for block in msg.content if block.type == "text")
print("## Automated review\n\n" + text)
