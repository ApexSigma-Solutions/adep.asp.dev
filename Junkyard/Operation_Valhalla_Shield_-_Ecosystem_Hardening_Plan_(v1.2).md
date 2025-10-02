# Operation: Valhalla Shield - Ecosystem Hardening Plan (v1.2)

**Tags:** [[ApexSigma]] [[Security]] [[DevOps]] [[CI-CD]] [[Governance]] [[PolicyAsCode]] [[ChaosEngineering]] [[Observability]] [[Resilience]] [[DevEx]]

---

## 1. Strategic Context

Operation Valhalla Shield is the sister initiative to Operation Asgard Rebirth. Its sole purpose is to harden the ecosystem against failure, drift, and security vulnerabilities. This plan will be executed in parallel with application development.

---

## 2. Phase 0: The Forge (Infrastructure Prerequisites)

### Strategic Imperative: Build the workshop before we forge the shield. We need a dedicated, controlled environment to run our automated quality and security checks.

- [ ] **Task ID: VS-P0-T1 - Provision Self-Hosted CI/CD Runner**
  - **Description:** Deploy a self-hosted GitHub Actions runner to execute all CI/CD workflows. This gives us full control over the environment and eliminates recurring cloud costs.
  - **Implementation:**
    1. Create a new `docker-compose.ci.yml` file.
    2. Define a new service, `github-runner`, using an official runner image.
    3. Configure the service with the necessary registration tokens and repository information from GitHub.
    4. Mount the host's Docker socket (`/var/run/docker.sock`) into the container so the runner can build and manage other Docker containers.
  - **Done means Done:** The runner service starts successfully, registers itself with our main GitHub repository, and appears as "Idle" in the Settings > Actions > Runners page. It can successfully pick up and run a basic "hello world" test workflow.

---

## 3. Phase 1: The Guard Rails (Automated Governance)

### Strategic Imperative: Automate our rules. Humans are fallible; a CI pipeline is not. We encode our best practices into automated gates that nothing can bypass.

- [ ] **Task ID: VS-P1-T1 - Implement Fortified Pre-Commit Hooks**
  - **Description:** Enforce code quality and security at the source. Before code is even committed, it must meet our baseline standard.
  - **Implementation:**
    1. Install and configure the `pre-commit` framework at the monorepo root.
    2. The configuration will include the following eight mandatory hooks:
      - `ruff check` (Linting)
      - `ruff format` (Formatting)
      - `trufflehog` (Secret Scanning)
      - `check-yaml` & `check-toml` (Config Syntax)
      - `check-added-large-files` (Prevent repo bloat, max 5MB)
      - `check-merge-conflict` (Prevent merge markers)
      - `interrogate` (Enforce >85% docstring coverage)
      - `darglint` (Ensure docstring correctness)
  - **Done means Done:** A developer running `git commit` on code that violates any of these eight rules will see the commit fail with a clear error message.

- [ ] **Task ID: VS-P1-T2 - Codify Architectural Contracts with OPA**
  - **Description:** Establish a Policy as Code (PaC) baseline. Our architectural rules become testable artifacts enforced by the CI pipeline.
  - **Implementation:**
    1. Create an `ObservableService` Abstract Base Class in `apexsigma-core` to define the observability contract.
    2. Create a new directory: `infra/policies/`.
    3. Add a policy in Rego: `enforce_observability.rego`. This policy will enforce that any new FastAPI service class *must* inherit from our `ObservableService` contract.
    4. Add a step to the main CI workflow that runs `opa test ./infra/policies`.
  - **Done means Done:** A Pull Request that adds a new service without implementing the `ObservableService` contract fails the CI build at the "Policy Check" step.

- [ ] **Task ID: VS-P1-T3 - Automate the MAR Protocol via CI**
  - **Description:** Evolve the MAR protocol from a manual gate into a fully automated quality gate within our CI/CD pipeline.
  - **Implementation:**
    1. Create a `pr-quality-gate.yml` GitHub Actions workflow.
    2. The workflow will run all tests, security scans, and policy checks on our self-hosted runner.
    3. Set branch protection rules on `main` to require this workflow to pass before a merge is allowed.
  - **Done means Done:** The "Merge" button in a Pull Request is disabled until all automated checks have passed.

---

## 4. Phase 2: The Chaos Engine (Operational Resilience)

### Strategic Imperative: Assume failure is inevitable. Build a system that anticipates and survives chaos.

- [ ] **Task ID: VS-P2-T1 - Enforce Observability Contracts**
  - **Description:** Make deep system visibility a non-negotiable feature of every service by enforcing the contract defined in VS-P1-T2.
  - **Implementation:**
    1. Refactor all existing services (`memos.as`, `tools.as`, etc.) to inherit from and correctly implement the `ObservableService` ABC.
  - **Done means Done:** All services start and run correctly while adhering to the observability contract.

- [ ] **Task ID: VS-P2-T2 - Deploy "Loki", the Chaos Agent**
  - **Description:** Introduce controlled, automated chaos into our staging environment to force the development of resilient services.
  - **Implementation:**
    1. Create a new `loki-chaos-agent` service in a `docker-compose.override.yml` file.
    2. The service will be a Python script that randomly stops other running containers on the network.
  - **Done means Done:** In a staging environment, the system remains functional and recovers gracefully despite the Loki agent periodically terminating services.

---

## 5. Phase 3: Developer Experience & Velocity

### Strategic Imperative: Automate the tedious parts of development to increase focus and velocity.

- [ ] **Task ID: VS-P3-T1 - Implement Conventional Commit Framework**
  - **Description:** Enforce the Conventional Commits standard for a machine-readable and predictable git history.
  - **Implementation:**
    1. Install and configure `commitizen` for guided commit message creation.
    2. Add a CI check to enforce that all commits in a PR adhere to the Conventional Commits standard.
  - **Done means Done:** Commits are standardized, enabling automated changelog generation.

- [ ] **Task ID: VS-P3-T2 - Develop 'as-commit' AI Assistant**
  - **Description:** Create an AI-powered tool to automatically generate commit messages from staged changes.
  - **Implementation:**
    1. Create a new CLI script in the `tools.as` service.
    2. The script will take the output of `git diff --cached`, send it to an LLM via API call, and use the response to create the commit.
  - **Done means Done:** A developer can run a single command (`as-commit`) to have a perfectly formatted, descriptive commit message generated and applied automatically.