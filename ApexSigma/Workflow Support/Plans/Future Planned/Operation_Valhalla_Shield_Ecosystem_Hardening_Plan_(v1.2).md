# Operation Valhalla Shield Ecosystem Hardening Plan (v1.2)

<poml>
  <role>DevSecOps Engineer</role>
  <task>
    Implement the 'Valhalla Shield' ecosystem hardening plan. Your mission is to automate security, governance, and resilience by provisioning CI/CD infrastructure, implementing policy-as-code, and introducing chaos engineering principles.
  </task>
  <document source="Operation_Valhalla_Shield_-_Ecosystem_Hardening_Plan_(v1.2).md">
    <obj name="metadata">
      <property name="operation">Valhalla Shield</property>
      <property name="version">v1.2</property>
      <property name="subject">Ecosystem Hardening Plan</property>
      <property name="tags">
        <list>
          <item>ApexSigma</item>
          <item>Security</item>
          <item>DevOps</item>
          <item>CI-CD</item>
          <item>Governance</item>
          <item>PolicyAsCode</item>
          <item>ChaosEngineering</item>
          <item>Observability</item>
          <item>Resilience</item>
          <item>DevEx</item>
        </list>
      </property>
      <property name="strategic_context">Sister initiative to Asgard Rebirth. Sole purpose is to harden the ecosystem against failure, drift, and security vulnerabilities. Executed in parallel with development.</property>
    </obj>

    <section name="Phase 0: The Forge (Infrastructure Prerequisites)">
      <p><b>Strategic Imperative:</b> Build a dedicated, controlled environment for automated quality and security checks.</p>
      <list>
        <item>
          <obj name="task">
            <property name="id">VS-P0-T1</property>
            <property name="title">Provision Self-Hosted CI/CD Runner</property>
            <property name="description">Deploy a self-hosted GitHub Actions runner for full environmental control.</property>
            <property name="implementation">
              <stepwise-instructions>
                <item>Create `docker-compose.ci.yml`.</item>
                <item>Define `github-runner` service using an official image.</item>
                <item>Configure service with registration tokens and repo info.</item>
                <item>Mount host Docker socket (`/var/run/docker.sock`) into the container.</item>
              </stepwise-instructions>
            </property>
            <property name="dod">Runner service starts, registers with GitHub repo, appears as "Idle", and can run a basic test workflow.</property>
          </obj>
        </item>
      </list>
    </section>

    <section name="Phase 1: The Guard Rails (Automated Governance)">
      <p><b>Strategic Imperative:</b> Automate rules and encode best practices into automated gates.</p>
      <list>
        <item>
          <obj name="task">
            <property name="id">VS-P1-T1</property>
            <property name="title">Implement Fortified Pre-Commit Hooks</property>
            <property name="description">Enforce code quality and security at the source before commit.</property>
            <property name="implementation">
              <p>Install and configure `pre-commit` framework at monorepo root with eight mandatory hooks:</p>
              <list>
                <item>`ruff check` (Linting)</item>
                <item>`ruff format` (Formatting)</item>
                <item>`trufflehog` (Secret Scanning)</item>
                <item>`check-yaml` & `check-toml` (Config Syntax)</item>
                <item>`check-added-large-files` (Max 5MB)</item>
                <item>`check-merge-conflict`</item>
                <item>`interrogate` (Enforce >85% docstring coverage)</item>
                <item>`darglint` (Docstring correctness)</item>
              </list>
            </property>
            <property name="dod">`git commit` fails with a clear error if any rule is violated.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">VS-P1-T2</property>
            <property name="title">Codify Architectural Contracts with OPA</property>
            <property name="description">Establish a Policy as Code (PaC) baseline where architectural rules become testable artifacts.</property>
            <property name="implementation">
              <stepwise-instructions>
                <item>Create `ObservableService` ABC in `apexsigma-core` to define observability contract.</item>
                <item>Create directory `infra/policies/`.</item>
                <item>Add Rego policy `enforce_observability.rego` to enforce new FastAPI services inherit from `ObservableService`.</item>
                <item>Add CI step to run `opa test ./infra/policies`.</item>
              </stepwise-instructions>
            </property>
            <property name="dod">A PR adding a new service without implementing `ObservableService` fails the CI build at "Policy Check".</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">VS-P1-T3</property>
            <property name="title">Automate the MAR Protocol via CI</property>
            <property name="description">Evolve MAR protocol from a manual gate to a fully automated quality gate in CI/CD.</property>
            <property name="implementation">
              <stepwise-instructions>
                <item>Create a `pr-quality-gate.yml` GitHub Actions workflow.</item>
                <item>Workflow runs all tests, scans, and policy checks on the self-hosted runner.</item>
                <item>Set branch protection rules on `main` to require this workflow to pass before merge.</item>
              </stepwise-instructions>
            </property>
            <property name="dod">The "Merge" button in a PR is disabled until all automated checks have passed.</property>
          </obj>
        </item>
      </list>
    </section>

    <section name="Phase 2: The Chaos Engine (Operational Resilience)">
      <p><b>Strategic Imperative:</b> Assume failure is inevitable. Build a system that anticipates and survives chaos.</p>
      <list>
        <item>
          <obj name="task">
            <property name="id">VS-P2-T1</property>
            <property name="title">Enforce Observability Contracts</property>
            <property name="description">Make deep system visibility a non-negotiable feature of every service.</property>
            <property name="implementation">Refactor all existing services (`memos.as`, `tools.as`, etc.) to inherit from and implement the `ObservableService` ABC.</property>
            <property name="dod">All services start and run correctly while adhering to the observability contract.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">VS-P2-T2</property>
            <property name="title">Deploy 'Loki', the Chaos Agent</property>
            <property name="description">Introduce controlled, automated chaos into the staging environment.</property>
            <property name="implementation">
              <stepwise-instructions>
                <item>Create a new `loki-chaos-agent` service in `docker-compose.override.yml`.</item>
                <item>The service will be a Python script that randomly stops other running containers.</item>
              </stepwise-instructions>
            </property>
            <property name="dod">In staging, the system remains functional and recovers gracefully despite Loki agent's actions.</property>
          </obj>
        </item>
      </list>
    </section>

    <section name="Phase 3: Developer Experience & Velocity">
      <p><b>Strategic Imperative:</b> Automate tedious parts of development to increase focus and velocity.</p>
      <list>
        <item>
          <obj name="task">
            <property name="id">VS-P3-T1</property>
            <property name="title">Implement Conventional Commit Framework</property>
            <property name="description">Enforce the Conventional Commits standard for a machine-readable git history.</property>
            <property name="implementation">
              <stepwise-instructions>
                <item>Install and configure `commitizen` for guided commit message creation.</item>
                <item>Add a CI check to enforce the Conventional Commits standard.</item>
              </stepwise-instructions>
            </property>
            <property name="dod">Commits are standardized, enabling automated changelog generation.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">VS-P3-T2</property>
            <property name="title">Develop 'as-commit' AI Assistant</property>
            <property name="description">Create an AI-powered tool to automatically generate commit messages from staged changes.</property>
            <property name="implementation">
              <stepwise-instructions>
                <item>Create a new CLI script in the `tools.as` service.</item>
                <item>Script takes `git diff --cached` output, sends it to an LLM, and uses the response to create the commit.</item>
              </stepwise-instructions>
            </property>
            <property name="dod">A developer can run `as-commit` to have a perfectly formatted, descriptive commit message generated and applied automatically.</property>
          </obj>
        </item>
      </list>
    </section>
  </document>
</poml>
