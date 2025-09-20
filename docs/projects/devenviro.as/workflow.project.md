``` markdown
**DevEnviro Agent Workflows & Standard Operating Procedures**

This document outlines the standard workflows and procedures for all agents within the DevEnviro platform. It serves as a guide for how to initiate, execute, and validate tasks, ensuring consistency and collaboration. All workflows are orchestrated by the central Orchestrator agent.

**1. The Core Development Workflow**

This is the standard, high-level process for implementing any new feature or solving a complex problem.

1.  **Request Decomposition (/design:decompose-request)**:
    *   **Initiated by**: The Orchestrator agent, upon receiving a complex user request.
    *   **Action**: The Orchestrator uses the /design:decompose-request command to break the request into a list of smaller, discrete sub-tasks.
    *   **Output**: A detailed plan that outlines each sub-task, its dependencies, and the a-priori designated agent (e.g., Gemini for implementation, Gemma for boilerplate).

2.  **Task Implementation**:
    *   **Initiated by**: The Orchestrator delegates a sub-task to a specialist agent (e.g., Gemini).
    *   **Action**: The specialist agent implements the task, adhering to the Code Quality and Adherence to Spec mandates. The agent must proactively instrument the code with OpenTelemetry for observability.
    *   **Output**: A completed artifact (e.g., source code, configuration file) and a signal back to the Orchestrator that the task is finished.

3.  **Mandatory Agent Review (MAR Protocol)**:
    *   **Initiated by**: The Orchestrator, upon receiving a completed task from an implementer agent.
    *   **Action**: The Orchestrator delegates a review task to a Reviewer agent (e.g., Qodo for automated checks, Claude for architectural review). The reviewer validates the work against the project's rules, quality standards, and architectural blueprint.
    *   **Output**: An approval or a detailed, actionable report of issues that need to be addressed by the implementer agent.

4.  **Integration & Verification**:
    *   **Initiated by**: The Orchestrator, upon receiving a successful review.
    *   **Action**: The Orchestrator integrates the completed artifact into the project and performs final system-level verification, such as running end-to-end tests.
    *   **Output**: The user is notified of the completed task.

**2. Standardized Agent-to-Agent (A2A) Communication**

All communication between agents, including task delegation and status updates, must follow these principles:

*   **Asynchronous Messaging**: Use the RabbitMQ message queue for all communication. This ensures loose coupling and system resilience.
*   **Structured Payloads**: All messages must conform to the AgentMessage schema, which includes fields for sender\_agent\_id, recipient\_agent\_id, task\_id, and a structured payload.
*   **Database Persistence**: Every message exchange (sent and received) must be logged to the agent\_communications table in PostgreSQL for a complete audit trail.

**3. Observability and Monitoring Workflows**

These workflows are critical for maintaining system health and are typically initiated by a developer or the Orchestrator as a proactive measure.

*   **Health Check (/dev:telemetry-status)**:
    *   **Initiated by**: A developer or the Orchestrator as a scheduled task.
    *   **Action**: A DevOps agent uses the /dev:telemetry-status command to check the health of the observability stack (Prometheus, Loki, Jaeger).
    *   **Output**: A report in the console indicating the status of each service.

*   **Trace Analysis (/dev:trace-last-request)**:
    *   **Initiated by**: A developer when investigating a performance issue.
    *   **Action**: A DevOps agent uses the /dev:trace-last-request command to fetch the most recent trace for a given service.
    *   **Output**: A link to the trace visualization in the Jaeger UI for deep analysis.

*   **Log Retrieval (/dev:log-search)**:
    *   **Initiated by**: A developer or an agent during a debugging session.
    *   **Action**: A DevOps agent uses the /dev:log-search command to query Loki for specific log messages based on a given LogQL query.
    *   **Output**: A formatted snippet of the relevant logs in the console.

These workflows provide the blueprint for a predictable and reliable development process, ensuring that every task is executed, reviewed, and verified systematically within the "Society of Agents."

```