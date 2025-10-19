# CI/CD Cleanup Check Workflow

**File**: `.github/workflows/cleanup-check.yml`  
**Status**: ✅ Active  
**Created**: October 19, 2025  
**Purpose**: Automated repository cleanup validation for ApexSigma ecosystem

---

## Overview

The **Repository Cleanup Check** workflow provides **remote validation** that complements local pre-commit hooks. It runs on GitHub Actions to enforce repository hygiene standards across all contributors, preventing artifacts and temporary files from entering the codebase.

This workflow is part of the **Valhalla Shield** engineering standard and integrates with the MAR (Mandatory Agent Review) Protocol.

---

## Architecture

### Workflow Triggers

- **Pull Requests** to `alpha` or `main` branches
- **Direct pushes** to `alpha` or `main` branches  
- **Manual dispatch** via GitHub Actions UI

### Job Structure

The workflow uses **parallel job execution** for fast feedback:

```
check-python-bytecode     ──┐
check-dagster-temps       ──┤
check-root-test-scripts   ──┼──> cleanup-summary (aggregates results)
check-os-artifacts        ──┤
check-env-files           ──┘
```

Each job runs independently and reports to the summary job for final status aggregation.

---

## Validation Checks

### 1. Python Bytecode Detection (`check-python-bytecode`)

**Purpose**: Prevent compiled Python bytecode from entering version control

**Detects**:
- `__pycache__/` directories
- `*.pyc` files (Python 2.x bytecode)
- `*.pyo` files (optimized bytecode)

**Why**: Bytecode is platform/Python-version-specific, pollutes diffs, and increases repo size unnecessarily.

**Remediation**:
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
```

### 2. Dagster Temporary Directories (`check-dagster-temps`)

**Purpose**: Prevent Dagster orchestration temporary files from being committed

**Detects**:
- `tmps_*` directories (Dagster temporary storage)
- `tmp*_dagster_*` directories (Dagster process temps)
- `dagster_home/storage/*` files (Dagster run artifacts)

**Why**: Dagster generates large temporary files during pipeline execution. These are runtime artifacts that should never be version-controlled.

**Remediation**:
```bash
find . -type d -name "tmps_*" -exec rm -rf {} +
find . -type d -name "tmp*_dagster_*" -exec rm -rf {} +
# Note: dagster_home/storage/ should be .gitignored
```

### 3. Root-Level Test Scripts (`check-root-test-scripts`)

**Purpose**: Enforce test file organization standards

**Detects**:
- `test_*.py` files in repository root (maxdepth 1)
- `*_test.py` files in repository root (maxdepth 1)

**Why**: Root-level test scripts clutter the repository. Tests should be organized in `tests/` directories or specialized `scripts/` directories.

**Remediation**:
```bash
# Move to appropriate location
mv test_*.py tests/
# OR for utility scripts
mv test_*.py scripts/
```

### 4. OS Artifacts (`check-os-artifacts`)

**Purpose**: Prevent OS-specific metadata files from polluting the repository

**Detects**:
- `.DS_Store` files (macOS Finder metadata)
- `Thumbs.db` files (Windows thumbnail cache)
- `*.log` files (warning only - doesn't fail workflow)

**Why**: OS artifacts are platform-specific, add no value to version control, and create noise in diffs.

**Remediation**:
```bash
find . -name ".DS_Store" -delete
find . -name "Thumbs.db" -delete
```

**Note**: Log file check is **non-blocking** (warning only) since some logs may be intentional documentation.

### 5. Environment Files (`check-env-files`)

**Purpose**: **CRITICAL SECURITY CHECK** - Prevent secrets from being committed

**Detects**:
- `.env` files (excluding `.env.example`)

**Why**: `.env` files typically contain secrets (API keys, database passwords, tokens). Committing these is a **severe security violation**.

**Remediation**:
```bash
# Remove from git (but keep locally)
git rm --cached .env

# Ensure .gitignore has this pattern
echo ".env" >> .gitignore
echo "!.env.example" >> .gitignore
```

**Alternative**: Use `.env.example` as a template with placeholder values.

---

## Integration with Pre-Commit Hooks

The CI/CD workflow **mirrors** the local pre-commit hooks (`.pre-commit-config.yaml`) to provide **defense in depth**:

| Check | Local (Pre-Commit) | Remote (CI/CD) | Purpose |
|-------|-------------------|----------------|---------|
| Python Bytecode | ✅ Instant feedback | ✅ Team enforcement | Developers can skip hooks; CI cannot be bypassed |
| Dagster Temps | ✅ Instant feedback | ✅ Team enforcement | Catches artifacts from CI/CD runs |
| Test Scripts | ✅ Instant feedback | ✅ Team enforcement | Consistent organization enforcement |
| OS Artifacts | ✅ Instant feedback | ✅ Team enforcement | Multi-platform development protection |
| .env Files | ✅ Instant feedback | ✅ Team enforcement | **Security-critical** - double validation |

**Why Both?**
- **Local hooks**: Fast developer feedback (catches 99% of issues before commit)
- **Remote CI/CD**: Team-wide enforcement (prevents bypassed hooks from reaching main branch)

Developers can bypass local hooks with `git commit --no-verify`, but **CI/CD workflow always runs** on PRs.

---

## Workflow Outputs

### GitHub Actions Summary

Each job generates a **markdown summary** visible in the GitHub Actions UI:

**Success Example**:
```
✅ Python Bytecode Check
=========================
✅ No __pycache__ directories found
✅ No .pyc files found
✅ No .pyo files found
```

**Failure Example**:
```
❌ Python Bytecode Detected
===========================
Found `__pycache__` directories:
./services/memos.as/app/__pycache__
./services/devenviro.as/app/__pycache__
```

### Pull Request Checks

The workflow integrates with GitHub's **required status checks**:

- **Status**: ✅ Pass / ❌ Fail
- **Details**: Click to view full job summary
- **PR Blocking**: Can be configured as required check (see Configuration below)

---

## Configuration

### Enable as Required Status Check

To **block PR merges** when checks fail:

1. Navigate to: **Settings** → **Branches** → **Branch protection rules** → `alpha` or `main`
2. Enable **Require status checks to pass before merging**
3. Select: `Repository Cleanup Check / cleanup-summary`
4. Save changes

### Customize Triggers

Edit `.github/workflows/cleanup-check.yml`:

```yaml
on:
  pull_request:
    branches:
      - alpha
      - main
      - feat/*  # Add feature branch protection
  push:
    branches:
      - alpha
      - main
  schedule:
    - cron: '0 0 * * 0'  # Weekly scan on Sundays
```

### Adjust Check Strictness

To make log file check **blocking** (currently warning-only):

```yaml
- name: Check for large log files
  id: check-log-files
  run: |
    # ... existing search code ...
    exit 1  # Add this line to fail on log files
```

---

## Troubleshooting

### Issue: Workflow fails on old commits

**Symptom**: Workflow runs on historical commits and fails due to existing artifacts

**Solution**: 
```bash
# Clean up repository first
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete
git add -u
git commit -m "chore: cleanup artifacts for CI/CD compliance"
```

### Issue: False positive on allowed files

**Symptom**: Workflow detects files that should be allowed (e.g., `tests/test_fixtures.py`)

**Solution**: Adjust search paths in workflow:
```yaml
# Change from:
if find . -type f -name "test_*.py" | grep -q .; then

# To (exclude tests/ directory):
if find . -maxdepth 1 -type f -name "test_*.py" | grep -q .; then
```

### Issue: Workflow takes too long

**Symptom**: Jobs take 5+ minutes on large repositories with submodules

**Solution**: Limit submodule depth:
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    submodules: recursive
    fetch-depth: 1  # Shallow clone for speed
```

### Issue: .env.example triggers false positive

**Symptom**: Workflow blocks `.env.example` files

**Verification**: Check the exclusion pattern in the workflow:
```bash
find . -type f -name ".env" ! -name ".env.example"
```

This pattern **should** exclude `.env.example`. If it doesn't, verify your bash version supports `! -name`.

---

## Maintenance

### Update Patterns

When adding new temporary file patterns to `.gitignore`, also update the workflow:

1. Edit `.github/workflows/cleanup-check.yml`
2. Add new check or update existing patterns
3. Test locally with `act` (GitHub Actions local runner):
   ```bash
   act pull_request -j check-python-bytecode
   ```
4. Commit and push

### Sync with Pre-Commit Hooks

When updating `.pre-commit-config.yaml`, review `cleanup-check.yml` for alignment:

```bash
# Compare custom hooks in pre-commit-config.yaml
grep -A 5 "id: check-" .pre-commit-config.yaml

# Compare with CI/CD job names
grep "^  check-" .github/workflows/cleanup-check.yml
```

### Monitor Workflow Performance

Track workflow execution time in GitHub Actions:

1. Navigate to **Actions** tab
2. Select **Repository Cleanup Check**
3. Review execution times (target: < 2 minutes for parallel jobs)
4. Optimize slow jobs by reducing `find` depth or parallelizing further

---

## Best Practices

### 1. Run Locally First

Before pushing, run pre-commit hooks locally:
```bash
pre-commit run --all-files
```

This catches issues before triggering CI/CD (faster feedback loop).

### 2. Use Workflow Dispatch for Testing

After making workflow changes, test manually:
1. Go to **Actions** → **Repository Cleanup Check**
2. Click **Run workflow**
3. Select branch and run
4. Verify all checks pass

### 3. Keep Workflow and Hooks in Sync

When adding new checks:
- Add to **both** `.pre-commit-config.yaml` (local) **and** `cleanup-check.yml` (remote)
- Document in this file
- Test both paths

### 4. Review Failed Workflows Before Override

If a workflow fails on a PR:
1. **Don't bypass** - investigate the failure
2. Click **Details** to see which files triggered the failure
3. Clean up the artifacts locally
4. Push updated commit
5. Workflow re-runs automatically

**Only override** for legitimate infrastructure commits (e.g., updating the workflow itself).

---

## Integration with ApexSigma Ecosystem

### MAR Protocol Compliance

This workflow supports the **Mandatory Agent Review (MAR) Protocol**:

- **Automated Review**: CI/CD checks act as first-line review before human/agent review
- **Audit Trail**: All check results logged in GitHub Actions for compliance verification
- **Immutable Verification**: Workflow results cannot be modified retroactively

### Omega Ingest Laws

Workflow execution data is available for ingestion into the knowledge graph:

- **GitHub Actions API**: Retrieve workflow run data
- **Structured Logs**: JSON-formatted job summaries
- **Event Triggers**: Webhook integration for real-time ingestion

### Valhalla Shield Standard

This workflow enforces **Valhalla Shield** repository hygiene standards:

- ✅ Zero tolerance for secrets in commits
- ✅ Consistent file organization (tests in `tests/`)
- ✅ Clean diffs (no bytecode, no OS artifacts)
- ✅ Reproducible builds (no platform-specific files)

---

## References

- **Pre-Commit Config**: `.pre-commit-config.yaml`
- **GitIgnore Patterns**: `.gitignore`
- **Branch Protection**: GitHub Settings → Branches
- **Workflow Logs**: GitHub Actions → Repository Cleanup Check
- **MAR Protocol**: `AGENTS.md`
- **Valhalla Shield**: `docs/Infrastructure/VALHALLA_SHIELD_STANDARD.md` (if exists)

---

## Changelog

### October 19, 2025 - Initial Implementation
- Created workflow with 5 parallel check jobs
- Integrated with pre-commit hooks for defense-in-depth
- Configured GitHub Actions summary reports
- Added comprehensive remediation commands
- Implemented security-critical `.env` file detection

---

## Contributing

When proposing changes to this workflow:

1. **Update this documentation** to reflect new checks or behavior changes
2. **Test locally** using `act` or manual workflow dispatch
3. **Sync with pre-commit hooks** to maintain consistency
4. **Follow MAR Protocol** - request agent review before merging
5. **Update `.gitignore`** if adding new file pattern checks

---

**Status**: ✅ Operational  
**Owner**: ApexSigma Infrastructure Team  
**Last Updated**: October 19, 2025
