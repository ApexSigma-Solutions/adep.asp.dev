# ApexSigma SOP: The TaskMaster Generation Protocol

## 1\. Objective

To establish a mandatory, standardized template for the creation of all project and operational task plans. This protocol ensures that every plan is clear, actionable, verifiable, and fully integrated with our core governance principles (MAR Protocol, Omega Ingest Laws).

## 2\. Foundation

All task plans will be structured according to the principles of the **TaskMaster MCP Framework**. They will begin with a high-level objective and be broken down into granular, executable tasks.

## 3\. Mandatory Task Components

Every individual task listed in a plan must contain the following five components without exception:

### A. Task ID

- [ ] A unique, human-readable identifier (e.g., PROJECT-PHASE-TASKNUM) for clear tracking and communication.

### B. Description

- [ ] A concise, unambiguous statement of the work to be performed.

### C. Implementer

- [ ] The designated agent responsible for executing the task. This section must include a **Role Description** defining their specific duties (e.g., "Execute all technical aspects, write code, and submit for review.").

### D. Reviewer

- [ ] The designated agent responsible for quality assurance under the **MAR Protocol**. The Role Description must define their duties, including: "Awaiting submission. Upon receipt, conduct a formal review against 'Done means Done' criteria. **Upon approval, the Reviewer must mark the task's checkbox as complete in the human-readable Markdown document.**"

### E. "Done means Done" Criteria

- [ ] A list of objective, measurable, and verifiable conditions that must be met for the task to be considered complete. **This list must always include "The work has been reviewed and signed off by the Reviewer."**

## 4\. Governing Protocols

Every task plan document must begin with a header section that explicitly defines the overarching rules of engagement:

### A. Workflow Protocol

- [ ] **Strict Sequential Order**: The workflow for each task is strictly sequential. The Reviewer's role cannot begin until the Implementer has formally submitted their work. The project **cannot proceed** to the next task in the sequence until the Reviewer has formally approved the current task and marked its checkbox as complete in the Markdown plan.
- [ ] **Asynchronous Execution (Concurrency)**: Tasks are not to be completed asynchronously. The only exception is if the task plan explicitly defines a multi-agent team for a specific task (e.g., two Implementers and one Reviewer, such as Implementers: \[Gemini (CLI), Qwen\], Reviewer: \[GitHub Co-Pilot\]). In such cases, the defined agents may work in parallel, but the single Reviewer's sign-off is still the final gate.

### B. MAR Protocol Integration

- [ ] The plan must affirm that the **Mandatory Agent Review (MAR) Protocol** is in effect for every task, with the Reviewer's sign-off acting as the final quality gate.

### C. Omega Ingest Mandate

- [ ] The plan must include tasks for performing an **Omega Ingest** at the conclusion of major phases or the entire project to ensure all outcomes are permanently recorded.

## 5\. Output Formats

All task plans must be generated in two distinct, parallel formats to serve both human and machine agents:

### A. Human-Readable Markdown (.md)

- [ ] **Purpose**: For human project management, legibility, and progress tracking.
- [ ] **Format**: A clearly structured, outlined markdown document. It must use headings, sections, and interactive checkboxes (- \[ \]) for each task to allow for manual tracking by the Reviewer.

### B. LLM Ingestion POML (.poml)

- [ ] **Purpose**: For efficient, accurate, and automated ingestion by LLM agents and other systems.
- [ ] **Format**: A token-efficient, non-verbose, XML-based POML (Prompt Orchestration Markup Language) document. This format is optimized for machine parsing and will be the version used for all automated workflows.
