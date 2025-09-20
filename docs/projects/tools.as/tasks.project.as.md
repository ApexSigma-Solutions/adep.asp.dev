# Project Tasks: tools.as

This file tracks the specific, actionable tasks for the current development cycle.

## Phase 2: Tool Expansion & Hardening

*   [ ] Create API endpoint specifications for the File System tool.
*   [ ] Implement read_file function for the FS tool.
*   [ ] Implement write_file function for the FS tool, ensuring path safety.
*   [ ] Implement list_directory function for the FS tool.
*   [ ] Write unit tests for all File System tool functions.
*   [ ] Implement /tools/calculate endpoint.
*   [ ] Add input validation and parsing for the Calculator tool to prevent injection attacks.
*   [ ] Write unit tests for the Calculator tool.
*   [ ] Add Prometheus metric counters for each tool endpoint invocation.
*   [ ] Integrate Jaeger tracing for all inbound requests and outbound API calls.
*   [ ] Create a security review checklist.
*   [ ] Perform a security review of the Search and To-Do list tools.

## Backlog / Future Tasks

*   [ ] Design the schema for the To-Do list in PostgreSQL.
*   [ ] Write Alembic migration script for the new schema.
*   [ ] Refactor database connection logic to use the central PostgreSQL service.
*   [ ] Research and design the plugin architecture interface.