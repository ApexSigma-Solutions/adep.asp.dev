``` markdown
**Global Rules for DevEnviro Agent Operations**

This document establishes the overarching principles and workflows that all agents in the ApexSigma Solutions 'Society of Agents' must follow. Adherence to these rules is non-negotiable and ensures system-wide consistency, safety, and efficiency.

**1. Hierarchical Context is King**

All agents MUST ground every response and action in the context provided by the project's .md files. This is the single source of truth for the project's state, rules, and direction. Agents must synthesize information from the following hierarchy, from most-specific to most-general:

1.  **projectrules.md**: Specific rules and coding standards for THIS project.
2.  **architecture.md**: The architectural blueprint for the project.
3.  **techstack.md**: The ONLY technologies permitted for this project.
4.  **security.md**: Hard security rules. NEVER violate these.
5.  **globalrules.md**: Organization-wide mandates (this file).

**2. Atomic, Task-Centric Workflow**

All work must be broken down into discrete, atomic tasks. No agent should attempt a large, multi-step operation without first breaking it down into a granular plan.

**3. Verification & Validation Protocol (VVP)**

Before completing a task, an agent MUST validate its work. This involves a multi-step check:

*   **Static Analysis:** Does the code/artifact conform to the project's Style & Structure rules?
*   **Dynamic Check:** Do all tests pass? Do the build, linting, and type-checking commands run without errors?
*   **Contextual Alignment:** Does the output align with the plan.md and task.md files?

**4. Inter-Agent Communication**

All communication between agents MUST be routed through the central message queue system (RabbitMQ), as defined in architecture.md. Agents must log all sent and received messages to the agent\_communications table in PostgreSQL for audit and analysis.

**5. No Hallucination, Ever**

If an agent cannot find a definitive answer or course of action in the provided context, it MUST NOT invent one. It should return a structured error message detailing the missing information and propose a plan for how to acquire it (e.g., asking the user for clarification, or delegating a research task).

```