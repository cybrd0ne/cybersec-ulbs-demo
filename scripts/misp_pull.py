"""Pull IP indicators from MISP into the Logstash translate dictionary (R-04).

Reads MISP_URL and MISP_KEY from the environment. Writes enrich/ioc_ip.yml, which the
Logstash translate filter reads. The output file holds live indicators and is gitignored;
each operator generates their own.

Usage:
    MISP_URL=https://localhost MISP_KEY=... python scripts/misp_pull.py
"""
import os
import pymisp

m = pymisp.PyMISP(os.environ["MISP_URL"], os.environ["MISP_KEY"], ssl=False)
attrs = m.search(
    controller="attributes",
    type_attribute=["ip-dst", "ip-src"],
    to_ids=True,
    pythonify=True,
)

with open("enrich/ioc_ip.yml", "w") as f:
    for a in attrs:
        f.write(f'"{a.value}": "misp:{a.event_id}:{a.category}"\n')

print(len(attrs), "indicators written")
