-----

title: "Sprint 1 Plan - ADEP Foundation (Hardened Protocol v2)"
tags:

  - sprint-plan
  - ADEP
  - CI/CD
  - GitHub
  - protocol
  - DevEx
    aliases:
  - "ADEP Foundation Sprint 1"
  - "Hardened Protocol v2 Sprint Plan"

-----

# Sprint 1 Plan: ADEP Foundation (Hardened Protocol v2)

## Sprint Goal

To establish the foundational, \[\[MAR-compliant repository structure\]\] and implement the core \[\[CI quality gate\]\]. By the end of this sprint, any code push will automatically trigger linting, testing, and a build validation, and the `main` branch will be fully protected against non-compliant merges.

## Protocol Mandate

Each task herein is subject to the full \[\[ApexSigma operational doctrine\]\]. The assigned Implementor is responsible for execution. The assigned Reviewer is responsible for enforcing the \[\[MAR Protocol\]\]. All outcomes must be logged according to the \[\[Omega Ingest Laws\]\]. The Orchestrator (SigmaDev11) provides final strategic approval.

## Epic: ADEP-01: Enhanced Repository Configuration

### Task ID: S1-01 - Initialize DevEx Pipeline Directory

  * **Description:** Initialize the directory structure for the new \[\[DevEx pipeline\]\] within the `/ApexSigmaProjects.Dev/` monorepo. Create the `.github/workflows` directory.
  * **Implementor:** Gemini CLI
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * The necessary directories exist in the monorepo structure.
      * A `README.md` is added explaining the purpose of the new pipeline directory.
      * **Omega Ingest:** The final directory structure and its rationale are documented and ingested into the \[\[knowledge graph\]\].

### Task ID: S1-02 - Configure Main Branch Protection

  * **Description:** Configure the `main` branch as the default and protected branch in the \[\[GitHub repository settings\]\].
  * **Implementor:** Gemini CLI
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * `main` is the default branch.
      * The "Require a pull request before merging" setting is enabled.
      * The "Require status checks to pass before merging" setting is enabled.
      * The "Disallow force pushes" setting is enabled.
      * **Omega Ingest:** The final branch protection ruleset is documented with screenshots and ingested.

## Epic: ADEP-02: Optimized CI Integration with ApexSigma Tooling

### Task ID: S1-03 - Create Base CI Workflow File

  * **Description:** Create the base `ci.yml` \[\[GitHub Actions workflow\]\] file. Configure it to trigger on push events for all branches except `main`.
  * **Implementor:** Gemini CLI
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * `.github/workflows/ci.yml` exists.
      * Pushing to a feature branch successfully triggers the workflow run.
      * Pushing to `main` does *not* trigger this specific workflow.
      * **Omega Ingest:** The base `ci.yml` code and trigger configuration are documented and ingested.

### Task ID: S1-04 - Implement Linting Job

  * **Description:** Implement the "Linting" job in `ci.yml`. This job must use the existing \[\[ApexSigma formatting standards\]\] and fail the workflow if linting errors are found.
  * **Implementor:** Gemini CLI (leveraging Qwen 3 Coder Plus for YAML generation)
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * A lint job is defined in the workflow.
      * The job successfully checks out the code, installs dependencies, and runs the linter.
      * A PR with code that violates linting rules shows a "failed" status for this job.
      * **Omega Ingest:** The final lint job YAML snippet and a summary of the linting rules are ingested.

### Task ID: S1-05 - Implement Testing Job

  * **Description:** Implement the "Testing" job in `ci.yml`. This job must connect to the existing \[\[pytest infrastructure\]\] and run the full test suite.
  * **Implementor:** Gemini CLI (leveraging Qwen 3 Coder Plus for YAML generation)
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * A test job is defined in the workflow that depends on the lint job's success.
      * The job runs all unit and integration tests.
      * A PR with failing tests shows a "failed" status for this job and blocks the merge.
      * **Omega Ingest:** The final test job YAML snippet is ingested, along with a reference to the test suite it executes.

### Task ID: S1-06 - Implement Build Validation Job

  * **Description:** Implement the "Build Validation" job in `ci.yml`. This job will use the established \[\[Docker networking\]\] to attempt a build of the relevant service.
  * **Implementor:** Gemini CLI (leveraging Qwen 3 Coder Plus for YAML generation)
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * A build-validate job is defined in the workflow that depends on the test job's success.
      * The job attempts a docker build using the correct \[\[Dockerfile\]\].
      * A PR with a broken Dockerfile or non-compiling code fails this job.
      * **Omega Ingest:** The final build-validate job YAML snippet and the target Dockerfile are documented and ingested.

### Task ID: S1-07 - Finalize Branch Protection Rules

  * **Description:** Finalize branch protection rules. Configure the "status checks" requirement to explicitly require the lint, test, and build-validate jobs to pass before a PR can be merged into `main`.
  * **Implementor:** Gemini CLI
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * The branch protection settings for `main` list the three CI jobs as required.
      * It is physically impossible to merge a PR on GitHub if any of the three jobs have failed.
      * **Omega Ingest:** A final confirmation screenshot of the mandatory status checks is ingested, closing the loop on \[\[Task S1-02\]\].
        Final response to user: \`\`\`

-----

title: "Sprint 1 Plan - ADEP Foundation (Hardened Protocol v2)"
tags:

  - sprint-plan
  - ADEP
  - CI/CD
  - GitHub
  - protocol
  - DevEx
    aliases:
  - "ADEP Foundation Sprint 1"
  - "Hardened Protocol v2 Sprint Plan"

-----

# Sprint 1 Plan: ADEP Foundation (Hardened Protocol v2)

## Sprint Goal

To establish the foundational, \[\[MAR-compliant repository structure\]\] and implement the core \[\[CI quality gate\]\]. By the end of this sprint, any code push will automatically trigger linting, testing, and a build validation, and the `main` branch will be fully protected against non-compliant merges.

## Protocol Mandate

Each task herein is subject to the full \[\[ApexSigma operational doctrine\]\]. The assigned Implementor is responsible for execution. The assigned Reviewer is responsible for enforcing the \[\[MAR Protocol\]\]. All outcomes must be logged according to the \[\[Omega Ingest Laws\]\]. The Orchestrator (SigmaDev11) provides final strategic approval.

## Epic: ADEP-01: Enhanced Repository Configuration

### Task ID: S1-01 - Initialize DevEx Pipeline Directory

  * **Description:** Initialize the directory structure for the new \[\[DevEx pipeline\]\] within the `/ApexSigmaProjects.Dev/` monorepo. Create the `.github/workflows` directory.
  * **Implementor:** Gemini CLI
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * The necessary directories exist in the monorepo structure.
      * A `README.md` is added explaining the purpose of the new pipeline directory.
      * **Omega Ingest:** The final directory structure and its rationale are documented and ingested into the \[\[knowledge graph\]\].

### Task ID: S1-02 - Configure Main Branch Protection

  * **Description:** Configure the `main` branch as the default and protected branch in the \[\[GitHub repository settings\]\].
  * **Implementor:** Gemini CLI
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * `main` is the default branch.
      * The "Require a pull request before merging" setting is enabled.
      * The "Require status checks to pass before merging" setting is enabled.
      * The "Disallow force pushes" setting is enabled.
      * **Omega Ingest:** The final branch protection ruleset is documented with screenshots and ingested.

## Epic: ADEP-02: Optimized CI Integration with ApexSigma Tooling

### Task ID: S1-03 - Create Base CI Workflow File

  * **Description:** Create the base `ci.yml` \[\[GitHub Actions workflow\]\] file. Configure it to trigger on push events for all branches except `main`.
  * **Implementor:** Gemini CLI
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * `.github/workflows/ci.yml` exists.
      * Pushing to a feature branch successfully triggers the workflow run.
      * Pushing to `main` does *not* trigger this specific workflow.
      * **Omega Ingest:** The base `ci.yml` code and trigger configuration are documented and ingested.

### Task ID: S1-04 - Implement Linting Job

  * **Description:** Implement the "Linting" job in `ci.yml`. This job must use the existing \[\[ApexSigma formatting standards\]\] and fail the workflow if linting errors are found.
  * **Implementor:** Gemini CLI (leveraging Qwen 3 Coder Plus for YAML generation)
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * A lint job is defined in the workflow.
      * The job successfully checks out the code, installs dependencies, and runs the linter.
      * A PR with code that violates linting rules shows a "failed" status for this job.
      * **Omega Ingest:** The final lint job YAML snippet and a summary of the linting rules are ingested.

### Task ID: S1-05 - Implement Testing Job

  * **Description:** Implement the "Testing" job in `ci.yml`. This job must connect to the existing \[\[pytest infrastructure\]\] and run the full test suite.
  * **Implementor:** Gemini CLI (leveraging Qwen 3 Coder Plus for YAML generation)
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * A test job is defined in the workflow that depends on the lint job's success.
      * The job runs all unit and integration tests.
      * A PR with failing tests shows a "failed" status for this job and blocks the merge.
      * **Omega Ingest:** The final test job YAML snippet is ingested, along with a reference to the test suite it executes.

### Task ID: S1-06 - Implement Build Validation Job

  * **Description:** Implement the "Build Validation" job in `ci.yml`. This job will use the established \[\[Docker networking\]\] to attempt a build of the relevant service.
  * **Implementor:** Gemini CLI (leveraging Qwen 3 Coder Plus for YAML generation)
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * A build-validate job is defined in the workflow that depends on the test job's success.
      * The job attempts a docker build using the correct \[\[Dockerfile\]\].
      * A PR with a broken Dockerfile or non-compiling code fails this job.
      * **Omega Ingest:** The final build-validate job YAML snippet and the target Dockerfile are documented and ingested.

### Task ID: S1-07 - Finalize Branch Protection Rules

  * **Description:** Finalize branch protection rules. Configure the "status checks" requirement to explicitly require the lint, test, and build-validate jobs to pass before a PR can be merged into `main`.
  * **Implementor:** Gemini CLI
  * **Reviewer (MAR Protocol):** Gemini
  * **"Done means Done":**
      * The branch protection settings for `main` list the three CI jobs as required.
      * It is physically impossible to merge a PR on GitHub if any of the three jobs have failed.
      * **Omega Ingest:** A final confirmation screenshot of the mandatory status checks is ingested, closing the loop on \[\[Task S1-02\]\].

<!-- end list -->

```
```
