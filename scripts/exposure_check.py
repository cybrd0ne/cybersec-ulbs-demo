"""Query Shodan for the stack's own public IP and print the exposure (R-05).

Reads SHODAN_KEY and OWN_PUBLIC_IP from the environment. Run it daily in CI and diff the
output against yesterday's: a new open port or banner is the signal the Session 7 alert
fires on. Only ever query an IP you own or are authorised to assess.

Usage:
    SHODAN_KEY=... OWN_PUBLIC_IP=203.0.113.10 python scripts/exposure_check.py
"""
import os
import json
import shodan

api = shodan.Shodan(os.environ["SHODAN_KEY"])
h = api.host(os.environ["OWN_PUBLIC_IP"])
print(json.dumps(
    {
        "ip": h["ip_str"],
        "ports": h["ports"],
        "org": h.get("org"),
        "last_update": h["last_update"],
    },
    indent=2,
))
