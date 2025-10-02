```markdown
---
title: "Sprint 1 Plan: ADEP Foundation"
tags:
  - ADEP
  - SprintPlan
  - GitHub
  - CI/CD
  - Monorepo
aliases: ["ADEP Sprint 1", "Foundation Sprint Plan"]
---

# Sprint 1 Plan: ADEP Foundation

## Sprint Goal

To establish the foundational, MAR-compliant repository structure and implement the core CI quality gate. By the end of this sprint, any code push will automatically trigger linting, testing, and a build validation, and the main branch will be fully protected against non-compliant merges.

## Epic: ADEP-01: Enhanced Repository Configuration

### Task ID: [[S1-01]]

**Description:** Initialize the directory structure for the new [[DevEx pipeline]] within the `/ApexSigmaProjects.Dev/` [[Monorepo]]. Create the `.github/workflows` directory.

**"Done means Done":**
- [ ] The necessary directories exist in the monorepo structure.
- [ ] A `README.md` is added explaining the purpose of the new pipeline directory.

### Task ID: [[S1-02]]

**Description:** Configure the `main` branch as the default and protected branch in the [[GitHub]] repository settings.

**"Done means Done":**
- [ ] `main` is the default branch.
- [ ] The "Require a pull request before merging" setting is enabled.
- [ ] The "Require status checks to pass before merging" setting is enabled.
- [ ] The "Disallow force pushes" setting is enabled.

## Epic: ADEP-02: Optimized CI Integration with ApexSigma Tooling

### Task ID: [[S1-03]]

**Description:** Create the base `ci.yml` [[GitHub Actions]] workflow file. Configure it to trigger on push events for all branches except `main`.

**"Done means Done":**
- [ ] `.github/workflows/ci.yml` exists.
- [ ] Pushing to a feature branch successfully triggers the workflow run in the GitHub Actions tab.
- [ ] Pushing to `main` does *not* trigger this specific workflow.

### Task ID: [[S1-04]]

**Description:** Implement the "Linting" job in `ci.yml`. This job must use the existing [[ApexSigma]] formatting standards and fail the workflow if linting errors are found.

**"Done means Done":**
- [ ] A lint job is defined in the workflow.
- [ ] The job successfully checks out the code.
- [ ] The job installs dependencies and runs the linter.
- [ ] A PR with code that violates linting rules shows a "failed" status for this job.

### Task ID: [[S1-05]]

**Description:** Implement the "Testing" job in `ci.yml`. This job must connect to the existing [[pytest]] infrastructure and run the full test suite.

**"Done means Done":**
- [ ] A test job is defined in the workflow that depends on the lint job's success.
- [ ] The job runs all unit and integration tests.
- [ ] A PR with failing tests shows a "failed" status for this job and blocks the merge.

### Task ID: [[S1-06]]

**Description:** Implement the "Build Validation" job in `ci.yml`. This job will use the established [[Docker]] networking to attempt a build of the relevant service.

**"Done means Done":**
- [ ] A build-validate job is defined in the workflow that depends on the test job's success.
- [ ] The job attempts a docker build using the correct `Dockerfile`.
- [ ] A PR with a broken `Dockerfile` or non-compiling code fails this job.

### Task ID: [[S1-07]]

**Description:** Finalize branch protection rules. Configure the "status checks" requirement to explicitly require the lint, test, and build-validate jobs to pass before a PR can be merged into `main`.

**"Done means Done":**
- [ ] The branch protection settings for `main` list the three CI jobs as required.
- [ ] It is physically impossible to merge a PR on GitHub if any of the three jobs have failed.