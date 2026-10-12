# Evidence

Screenshots and captured output that prove each control works. Referenced from the risk
register and the session artefacts. Capture these during the demonstration and drop the
files here.

| File to capture | Proves | Risk |
|-----------------|--------|------|
| `push-rejected.png` | A direct push to `main` is refused, or gitleaks blocks a fake key | R-01, R-02 |
| `governance-red.png`, `governance-green.png` | The governance workflow fails on a direct commit and passes on a merged PR | R-01 |
| `secret-ciphertext.png` | `git show HEAD:secrets/opensearch.enc.yaml` reveals ciphertext only | R-02 |
| `trivy-fail.png` | Trivy fails the scan job on an outdated base image | supply chain |
| `cosign-verify.txt` | `cosign verify` confirms the signed release image | supply chain |
| `dashboards-hit.png` | The long DNS TXT rule matches in Dashboards Discover | R-03 |
| `threat-match.png` | The known-bad flow is tagged `threat_match` with risk score 80; the clean flow is untouched | R-04 |
| `exposure-diff.txt` | `scripts/exposure_check.py` output, with a new port flagged against yesterday | R-05 |
| `alert-firing.png` | `OpenSearchClusterRed` fires in Alertmanager and the Grafana panel goes red | operations |
| `ai-review-comment.png` | The automated reviewer comments on a sloppy PR before any human approves | R-01 |

Keep captured evidence free of real secrets and real third-party IP addresses.
