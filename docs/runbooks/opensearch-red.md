# Runbook: OpenSearch cluster is red

Fired by the `OpenSearchClusterRed` alert in `monitoring/alerts.yml`. A red cluster means
at least one primary shard is unassigned, so writes and detections may be failing.

## Confirm

```
curl -ks -u admin:"$OPENSEARCH_INITIAL_ADMIN_PASSWORD" \
  https://localhost:${OS_HTTP_PORT}/_cluster/health?pretty
curl -ks -u admin:"$OPENSEARCH_INITIAL_ADMIN_PASSWORD" \
  "https://localhost:${OS_HTTP_PORT}/_cat/shards?v&h=index,shard,prirep,state,unassigned.reason"
```

## Common causes and fixes

- **Container restarted or out of memory.** Check `docker compose logs opensearch`. Raise
  `OPENSEARCH_JAVA_OPTS` heap in `compose.yaml` if the host has the RAM, then `make up`.
- **Disk watermark hit.** The cluster blocks writes when disk is low. Free space or lower
  the watermark, then re-enable allocation.
- **Single-node and the data volume is corrupt.** For the lab stack you can reset with
  `make down` then `make up`, which recreates the `os-data` volume. This loses indexed
  data, so only do it in the lab.

## After recovery

Confirm the cluster is green, re-run the Session 5 Discover query, and note the incident
in `docs/evidence/` if it happened during an evaluation.
