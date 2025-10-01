```
title: "ApexSigma Task Workflow"
tags:
  - workflow
  - ApexSigma
  - task management
  - development process
aliases: ["ApexSigma Workflow", "Task Lifecycle"]
```

# ApexSigma Task Workflow

This document outlines the mandatory five-stage lifecycle for all tasks within the [[ApexSigma]] ecosystem. Adherence to this workflow is non-negotiable and ensures a structured, transparent, and accountable development process.

## Stage 1: Backlog

*   **Definition:** The holding area for all identified, unrefined, and unprioritized work items.
*   **Entry Criteria:** An idea or requirement has been identified and captured using the v3 task template.
*   **Exit Criteria:** The task has been reviewed, deemed valuable, and is ready for prioritization.

## Stage 2: Todo

*   **Definition:** A prioritized list of tasks that are fully defined, approved, and ready for implementation.
*   **Entry Criteria:** A task from the [[Backlog]] has been prioritized for the current work cycle. All dependencies are met.
*   **Exit Criteria:** An implementer (human or agent) has selected the task and is ready to begin work.

## Stage 3: In-Progress

*   **Definition:** The task is actively being worked on.
*   **Entry Criteria:** The implementer successfully executes the session-start command, formally initiating a documented work session. This is the **only** way a task can enter this state.
*   **Exit Criteria:** The core implementation work is complete, and the resulting artifact is ready for review.

## Stage 4: MAR (Mandatory Agent Review)

*   **Definition:** A critical quality gate where the completed work is reviewed against all project standards before it can be considered "Done."
*   **Entry Criteria:** An implementer submits their work for review.
*   **Exit Criteria:** The work has been verified to meet all requirements and standards as defined in [[STANDARDS.md]].

## Stage 5: Done

*   **Definition:** The task is 100% complete, reviewed, merged, and deployed where applicable.
*   **Entry Criteria:** The task has successfully passed the [[MAR (Mandatory Agent Review)|MAR]] stage.
*   **Exit Criteria:** None. The task is considered finished and archived.