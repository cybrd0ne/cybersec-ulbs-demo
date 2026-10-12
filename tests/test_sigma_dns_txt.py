"""Rule logic test for the long DNS TXT detection (R-03).

Tests the detection logic, not the OpenSearch backend. A stronger version replays the
samples through Logstash into a test index and queries it; that is left as extra credit.
"""
import json
import re
import pathlib

RULE_RE = re.compile(r'^.{200,}$')
SAMPLES = pathlib.Path(__file__).parent / "samples"


def matches(rec):
    d = rec.get("dns", {})
    return (
        rec.get("event_type") == "dns"
        and d.get("type") == "answer"
        and d.get("rrtype") == "TXT"
        and bool(RULE_RE.match(d.get("rdata", "")))
    )


def load(name):
    return [
        json.loads(line)
        for line in (SAMPLES / name).read_text().splitlines()
        if line.strip()
    ]


def test_positive():
    assert any(matches(r) for r in load("eve_dns_txt_positive.json"))


def test_negative():
    assert not any(matches(r) for r in load("eve_dns_txt_negative.json"))
