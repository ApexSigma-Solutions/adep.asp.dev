CI & Security Pipelines
=======================

This document explains the two GitHub Actions workflows added to the repository to implement the ApexSigma PR Quality Gate and the Scheduled Security Scans.

Files added
- `.github/workflows/pull_request_quality_gate.yml` — fast PR gate that runs Trunk (including Semgrep), tests and a light build.
- `.github/workflows/scheduled_security_scans.yml` — scheduled (nightly) Trivy container scan and OWASP ZAP baseline scan.

Required GitHub Actions Secrets
- `STAGING_URL` — URL of a staging deployment that ZAP can scan (e.g. https://staging.example.com). Keep this secret to avoid exposing the environment URL publicly.
- (Optional) `TRIVY_TOKEN` — if you use the Trivy cloud service, set this secret; otherwise Trivy works offline for local image scans.

How to enable and configure Trunk/Semgrep
1. Install Trunk locally and run `trunk init` in the repo to create `trunk.yaml` if one does not exist.
2. Configure any Semgrep rules in `trunk.yaml` or via a shared ruleset.

Validation & Testing
- Create a test branch/PR targeting `alpha` and push a change with a deliberate Semgrep-detectable issue to confirm the PR gate fails.
- Manually trigger the `ApexSigma Scheduled Security Scans` workflow from the Actions tab and observe logs for Trivy and ZAP jobs.

Notes
- Do not commit secrets to the repository. Use GitHub Actions Secrets for all environment tokens.
- If you need to change the image name used by Trivy, update the `image-ref` value in the scheduled workflow.

Next Steps
- If you're happy with these workflows, I can open a PR with these files on a feature branch and configure the Trunk merge queue as requested.

Contact
- Implementer: @GitHub Co-Pilot
