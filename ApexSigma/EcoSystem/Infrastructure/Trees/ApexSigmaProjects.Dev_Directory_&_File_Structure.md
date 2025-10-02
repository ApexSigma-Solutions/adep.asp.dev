# ApexSigmaProjects.Dev Directory & File Structure

Based on the give requirements and the current state of the `ApexSigmaProjects.Dev` directory, here is implemented file structure. This design cleans up the root, establishes clear boundaries between different parts of the ecosystem, and sets us up for scalable development.

### Proposed Monorepo Structure

```
/ApexSigmaProjects.Dev/
|
├── 📂 .github/             # Global GitHub Actions workflows (e.g., repo-wide linting)
├── 📂 .vscode/             # Shared VSCode workspace settings for a unified dev experience
|
├── 📂 services/            # HOUSES ALL INDEPENDENT, DEPLOYABLE MICROSERVICES
│   ├── 📂 memos-as/        # The core memory service (tracks original remote)
│   ├── 📂 devenviro-as/    # The agent orchestrator service
│   ├── 📂 ingest-llm-as/   # The data ingestion service
│   └── 📂 tools-as/        # The tool registry service
|
├── 📂 agents/              # CODE FOR THE AGENT SWARM AND CLIENTS
│   └── 📂 mcp-client/      # Your forked client for memory recall (dogfooding happens here)
|
├── 📂 libs/                # SHARED LIBRARIES & PACKAGES USED ACROSS SERVICES
│   └── 📂 apexsigma-core/  # Common utilities, data models, protocols, etc.
|
├── 📂 docs/                # THE MASTER DOCUMENT LIBRARY (OUR SINGLE SOURCE OF TRUTH)
│   ├── 📂 adrs/            # Architectural Decision Records
│   ├── memos_upgrade_task_plan_v5.md
│   ├── task_plan_generation_protocol.md
│   └── ...
|
├── 📂 scripts/             # Repo-wide utility scripts (e.g., dev environment setup, migrations)
|
├── 📜 .gitignore           # Root gitignore that covers all services and tools
├── 📜 README.md             # High-level overview of the ApexSigma monorepo
└── 📜 apexsigma.code-workspace # VSCode workspace file to open everything at once
```

-----

### Rationale and Benefits

1.  **Clarity and Organization**: The root directory is no longer a dumping ground. The `services/` directory clearly separates your deployable applications from everything else. This immediately solves the "messy and unstructured" problem.

2.  **Automated Dogfooding**: This structure is built for our dogfooding requirement. The `agents/mcp-client` can be developed in the same workspace as the `services/memos-as` it consumes. When you submit a PR for `memos-as`, your CI/CD pipeline can automatically run tests using the `mcp-client` to ensure you don't break the primary consumer of your service—your own agents.

3.  **Single Workspace**: The `apexsigma.code-workspace` file is the key to our need for "one workspace". When you open this file in VS Code, the entire project structure, with all services and libraries, will be available. It simplifies development, debugging, and cross-service refactoring immensely.

4.  **Code Reusability**: The `libs/` directory prevents code duplication. If multiple services need to use the same data models or utility functions, you define them once in a shared library and import them where needed. This is efficient and reduces errors.

5.  **Centralized Governance**: All your master documents, protocols, and plans live in one `docs/` folder. Your CI/CD configuration in `.github/` can manage the entire ecosystem from one place. This enforces consistency and makes governance easier.

This is a clean, professional, and scalable structure. It's the standard for managing complex, interconnected projects and will serve as a solid foundation for building out the ApexSigma ecosystem.