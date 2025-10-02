# Asgard Rebirth memOS MCP Upgrade Plan 6p0.5 Refactored

<poml>
  <role>Project Execution Agent</role>
  <task>
    Parse and execute the granular tasks defined in the 'Asgard Rebirth v6p0.5' plan. Adhere strictly to the defined implementer/reviewer roles, sequential order, and 'Done means Done' criteria for each task ID.
  </task>
  <document source="Operation_Asgard_Rebirth_-_memOS_MCP_Upgrade_Plan_(v6p0.5).md">
    <obj name="metadata">
      <property name="operation">Asgard Rebirth</property>
      <property name="version">v6p0.5 Refactored</property>
      <property name="subject">memOS MCP Upgrade Plan</property>
      <property name="tags">
        <list>
          <item>ApexSigma</item>
          <item>API</item>
          <item>FastMCP</item>
          <item>MAR</item>
          <item>Plan</item>
          <item>MCP</item>
          <item>Python</item>
          <item>Upgrade</item>
          <item>Monorepo</item>
          <item>Strategic-Evolution</item>
          <item>Granular-Tasking</item>
          <item>Observability</item>
          <item>Governance</item>
        </list>
      </property>
    </obj>

    <section name="Protocols and References">
      <p><b>Workflow Protocol:</b> Governed by Single Source of Truth, Strict Sequential Order, and Monorepo-First principles.</p>
      <obj name="reference">
        <property name="name">Infrastructure Blueprint</property>
        <property name="description">Single source of truth for service configurations, images, ports, and network topology.</property>
        <property name="path"><code>C:\Users\steyn\ApexSigmaProjects.Dev\docs\Config Files\Infrastructure\Docker Network\VERIFIED_DOCKER_NETWORK_MAP.md</code></property>
        <property name="applies_to_tasks">
          <list>
            <item>MEMOS-P0-T2.1</item>
            <item>MEMOS-P0-T2.1.1</item>
          </list>
        </property>
      </obj>
    </section>

    <section name="Phase 0: Monorepo Foundation & Integration (Granular Refactor)">
      <p><b>Strategic Imperative:</b> Establish foundational monorepo infrastructure with maximum clarity and verifiability before core service development.</p>
      <list>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T1.1</property>
            <property name="description">Initialize the apexsigma-core library as a formal Python package using Poetry.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">The directory `libs/apexsigma-core/` exists with a valid `pyproject.toml` and package structure.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T1.2</property>
            <property name="description">Define the core Pydantic data models for inter-service communication protocols.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">A `models` module exists with base models (`AgentPersona`, `Task`, etc.) and passing unit tests.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T1.3</property>
            <property name="description">Define the abstract storage interfaces using Python's `abc` module.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">A `storage` module exists with ABCs for Cache, Persistent, Vector, and Graph storage.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T1.4</property>
            <property name="description">Implement initial shared utilities for configuration and standardized logging.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">A `utils` module is created with unit-tested configuration and logging helpers.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T1.5</property>
            <property name="description">Configure a CI pipeline for apexsigma-core and verify its installability.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">A CI pipeline for the library is active, and it can be installed via `pip install -e` in another service.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T2.1</property>
            <property name="description">Define the base data infrastructure services (databases, message queues) in the root `docker-compose.yml`, referencing the official network map.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">`docker-compose.yml` exists at the root, defining and successfully starting PostgreSQL, Redis, Qdrant, and Neo4j with persistent data volumes, exactly as specified in the reference document.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T2.1.1</property>
            <property name="description">Integrate the complete, existing observability stack (Jaeger, Prometheus, Loki, Grafana, Langfuse) into the root `docker-compose.yml`, referencing the official network map.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">All specified observability services are defined in the root `docker-compose.yml` per the reference document and start successfully. The Grafana UI is accessible and configured.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T2.2</property>
            <property name="description">Integrate the existing application services (`memos.as`, `tools.as`, etc.) into the root `docker-compose.yml`.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">All application services are defined in the `docker-compose.yml` and start successfully, with verifiable network connectivity.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T2.3</property>
            <property name="description">Implement and verify the hierarchical environment variable strategy.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">A root `.env` and service-specific `.env` files are correctly loaded by Docker Compose.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T2.4</property>
            <property name="description">Audit and refactor all Python import statements across all services for monorepo compatibility.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">All services start without any `ModuleNotFoundError`.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T2.5</property>
            <property name="description">Audit and standardize all service-level configuration files (`Dockerfile`, `pyproject.toml`) and remove legacy orchestration files.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">Legacy `docker-compose.yml` files are deleted; service-level `Dockerfile` and `pyproject.toml` files are updated for the monorepo structure.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T3.1</property>
            <property name="description">Add Dagster services to the root `docker-compose.yml`.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">Dagster services are defined in `docker-compose.yml`, and the UI is accessible.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T3.2</property>
            <property name="description">Create and configure the root `workspace.yaml` for Dagster.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">A `workspace.yaml` exists at the root, configured to load code locations.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T3.3</property>
            <property name="description">Define `memos.as` as the first Dagster code location.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">The `memos.as` code location and a sample asset are visible in the Dagster UI.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-T3.4</property>
            <property name="description">Verify a Dagster asset can import from `libs/apexsigma-core`.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="dod">A sample asset in `memos.as` successfully imports a model from `apexsigma_core` and materializes without error.</property>
          </obj>
        </item>
        <item>
          <obj name="task">
            <property name="id">MEMOS-P0-OMEGA</property>
            <property name="description">Produce the new, VERIFIED docker network map for the monorepo infrastructure. This document will serve as the official baseline for Phase 1 and beyond.</property>
            <property name="implementer">Gemini (CLI)</property>
            <property name="reviewer">Qwen</property>
            <property name="final_sign_off">SigmaDev11</property>
            <property name="dod">
              <list>
                <item>A new markdown document, `VERIFIED_DOCKER_NETWORK_MAP_V2.md`, is created.</item>
                <item>The document accurately reflects the state of the running docker-compose stack.</item>
                <item>The document contains explicit, recorded sign-offs from Implementer, Reviewer, and Supervisor.</item>
                <item>The old network map is moved to an `_archive` directory.</item>
              </list>
            </property>
          </obj>
        </item>
      </list>
    </section>
  </document>
</poml>
