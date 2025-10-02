## Workflow Protocol

1.  **Single Source of Truth**: This document and its POML counterpart are the master plan.
2.  **Strict Sequential Order**: The project cannot proceed to the next task until the Reviewer has formally approved the current task and marked its checkbox as complete.
3.  **Asynchronous Execution (Concurrency)**: Tasks are sequential unless a multi-agent team is explicitly defined. For such tasks, the primary Implementer's work must be completed before the Reviewer can approve, but support agents may work in parallel.

## Phase 1: Foundational Scaffolding

-   [x] **Task ID**: MONO-P1-T1
    -   **Description**: Create the core monorepo directory structure: `services/`, `agents/`, `libs/`, `docs/`, `_archive/`, `scripts/`, `.github/`, and `.vscode/`.
    -   **Implementer**: Gemini (CLI)
    -   **Reviewer**: Qwen
    -   **Done means Done**: All specified directories exist at the root level. The work has been reviewed and signed off by the Reviewer.

-   [x] **Task ID**: MONO-P1-T2
    -   **Description**: Relocate all existing service projects (`memos.as`, `devenviro.as`, `InGest-LLM.as`, `tools.as`) into the `services/` directory.
    -   **Implementer**: Gemini (CLI)
    -   **Reviewer**: Qwen
    -   **Done means Done**: The project root is clean of service folders, and they reside within `services/`. All paths are updated. The work has been reviewed and signed off by the Reviewer.

-   [x] **Task ID**: MONO-P1-T3
    -   **Description**: Create and populate the workspace configuration files: `apexsigma.code-workspace`, `.vscode/settings.json`, and the root `.gitignore`. The `.gitignore` must include a rule to ignore the `_archive/` directory.
    -   **Implementer**: Gemini (CLI)
    -   **Reviewer**: Qwen
    -   **Done means Done**: The workspace can be opened from the `.code-workspace` file, and temporary files in `_archive/` are untracked by Git. The work has been reviewed and signed off by the Reviewer.

## Phase 2: Agent & Protocol Integration

-   [x] **Task ID**: MONO-P2-T1
    -   **Description**: Create the master agent priming document, `AGENTS.md`, at the root of the workspace.
    -   **Implementer**: Gemini (CLI)
    -   **Reviewer**: Qwen
    -   **Done means Done**: The `AGENTS.md` file is created and populated with the complete TaskMaster Generation Protocol, MAR Protocol, Omega Ingest Laws, the monorepo structure, and the Safe-Delete workflow. This serves as the boot-up context for all agents. The work has been reviewed and signed off by the Reviewer.

## Phase 3: Shared Tooling Initialization

-   [x] **Task ID**: MONO-P3-T1 (Multi-Agent Task)
    -   **Description**: Initialize shared tooling directories and populate them with boilerplate configurations.
    -   **Implementers**:
        -   Gemini (CLI) (Primary)
            -   **Role**: Create the primary directory structures: `libs/apexsigma-core/`, `scripts/utils/`, and `ast-grep/`.
        -   GitHub Co-Pilot (Support)
            -   **Role**: Asynchronously populate the created directories with starter content: move the `trash.sh` script to `scripts/utils/`, and add standard Python rules to `ast-grep/`.
    -   **Reviewer**: Qwen
    -   **Done means Done**: All directories are created and populated with their initial content. The review is conducted after the Primary Implementer's work is complete. The work has been reviewed and signed off by the Reviewer.

-   [x] **Task ID**: MONO-P3-T2
    -   **Description**: Create the Bash/Zsh shell function to override the `rm` command, redirecting it to the `_archive/trash/` directory. Provide clear instructions for adding it to the `.bashrc` or `.zshrc` profile.
    -   **Implementer**: Gemini (CLI)
    -   **Reviewer**: Qwen
    -   **Done means Done**: The shell function code is correct and documented in a setup script. Instructions for installation are clear. The work has been reviewed and signed off by the Reviewer.

-   [x] **Task ID**: MONO-P3-T3
    -   **Description**: Create the PowerShell function to override the `Remove-Item` command (and its aliases `rm`, `del`), redirecting it to the `_archive/trash/` directory. Provide clear instructions for adding it to the PowerShell `$PROFILE`.
    -   **Implementer**: Gemini (CLI)
    -   **Reviewer**: Qwen
    -   **Done means Done**: The PowerShell function code is correct and documented in a setup script. Instructions for installation are clear. The work has been reviewed and signed off by the Reviewer.

## Phase 4: Cleanup & Finalization

-   [x] **Task ID**: MONO-P4-T1 (Automated Housekeeping)
    -   **Description**: Perform a full cleanup of the root directory, removing all old cache files, redundant logs, and temporary files left over from the previous structure.
    -   **Implementer**: GitHub Co-Pilot
        -   **Role**: Execute a cleanup script to recursively find and remove specified temporary files (e.g., `__pycache__`, `.pytest_cache`, `.ruff_cache`). This task can be triggered via webhook on phase completion.
    -   **Reviewer**: Qwen
    -   **Done means Done**: The repository root is completely clean, containing only the directories and files defined by the new monorepo structure. The work has been reviewed and signed off by the Reviewer.

-   [x] **Task ID**: MONO-P4-OMEGA
    -   **Description**: Perform an **Omega Ingest** of the new monorepo architecture, the `AGENTS.md` file, and all MAR sign-off reports for this operation.
    -   **Done means Done**: The new organizational structure is formally documented and verifiable in the master knowledge graph.
