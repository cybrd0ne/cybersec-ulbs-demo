# MISP and threat-intelligence enrichment (R-04)

The project reasons about the live threat landscape by pulling indicators from MISP and
correlating telemetry against them. A destination that matches a known-bad indicator is
tagged `threat.indicator.matched` and risk-scored; a clean destination is untouched. That
difference is the evidence that enrichment changes an outcome.

## Stand up MISP

1. Clone and start the official `misp-docker` images. First boot takes several minutes.
2. In the MISP UI, enable one public feed (the CIRCL OSINT feed is reliable): Sync
   Actions, List Feeds, fetch it, confirm attributes appear in the event list.
3. Note the admin API key: Administration, List Auth Keys.

## Pull indicators

```
export MISP_URL=https://localhost
export MISP_KEY=<your-misp-api-key>
python scripts/misp_pull.py
```

This writes `enrich/ioc_ip.yml`, the dictionary the Logstash `translate` filter reads.
The file is mounted into the Logstash container at `/enrich` and reloaded every 300
seconds (see `pipelines/suricata.conf`).

For an offline demo without MISP running, copy the example:

```
cp enrich/ioc_ip.yml.example enrich/ioc_ip.yml
```

## Prove the enrichment changes an outcome

`tests/samples/eve.json` carries two flow records: one to a known-bad indicator
(`203.0.113.66`, present in the dictionary) and one to a clean host (`10.0.0.5`). Bring
the stack up with `make up`, then in Dashboards filter `tags:threat_match`:

- The bad record is tagged `threat_match`, carries `event.risk_score: 80`, and shows the
  MISP event ID in `threat.indicator.matched`.
- The clean record is untouched.

Capture that side-by-side view into `docs/evidence/`.

## External exposure (R-05)

```
export SHODAN_KEY=<your-shodan-api-key>
export OWN_PUBLIC_IP=<an-ip-you-own>
python scripts/exposure_check.py
```

Run it daily in CI and diff against yesterday. A new open port or banner opens an issue
and feeds the Alertmanager rule in `monitoring/alerts.yml`.

## Handling secrets

Never commit `MISP_KEY`, `SHODAN_KEY`, or `enrich/ioc_ip.yml`. The keys belong in your
environment or in a SOPS-encrypted file under `secrets/`; the indicator file is gitignored.
Keep every query lawful and scoped to assets you own or are authorised to assess.
