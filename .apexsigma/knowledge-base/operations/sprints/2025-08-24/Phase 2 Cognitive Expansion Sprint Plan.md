# Phase 2: Cognitive Expansion Sprint Plan

## Sprint Objectives:

*   Harden ecosystem reliability.
*   Expand Agent Society with Sigma Coder integration.
*   Close critical technical debt.
*   Strengthen cross-service testing & observability.

---

## 🔴 Critical Tasks

### P2-CRIT-01: Harden TASK-IG-20 - Create dedicated integration test suite

*   **Project:** InGest-LLM.as
*   **Agent:** Gemini CLI
*   **(File:** `tests/test_repository_ingestion.py`)

### P2-CRIT-02: Harden TASK-IG-20 - Write formal API documentation

*   **Project:** InGest-LLM.as
*   **Agent:** Claude Code
*   **(File:** `api_ingestion_endpoints.md`)

### P2-CRIT-03: Execute end-to-end integration tests between InGest-LLM.as and memOS.as

*   **Project:** Ecosystem-Wide
*   **Agent:** Gemini CLI

### P2-CRIT-04: Integrate Sigma Coder (Qwen3-6B GGUF) into DevEnviro.as and develop parsing logic for `<tool_call>` output

*   **Project:** DevEnviro.as
*   **Agent:** Sigma Coder

---

## 🟠 High Priority Tasks

### P2-HIGH-01: Create a high-priority bug ticket for sqlalchemy.exc.OperationalError to track technical debt and design a long-term schema fix

*   **Project:** InGest-LLM.as
*   **Agent:** Claude Code

### P2-HIGH-02: Address Pydantic warnings in DevEnviro.as test suite

*   **Project:** DevEnviro.as
*   **Agent:** Gemini CLI

### P2-HIGH-03: Formally define and document Agent Society Roles and update Sentinel protocols based on Phase 1 outcomes

*   **Project:** DevEnviro.as
*   **Agent:** The Sentinel

---

## 🟢 Stretch Goals

### P2-STRETCH-01: Extend .apexsigma Knowledge Base with POML templates for structured task orchestration

*   **Project:** Ecosystem-Wide
*   **Agent:** Claude Code

### P2-STRETCH-02: Verify and document Langfuse + GitHub Actions observability and CI/CD workflows

*   **Project:** Ecosystem-Wide
*   **Agent:** Gemini CLI

```