``` markdown
# Project-Specific Rules & Coding Standards

These rules supplement globalrules.md.

## Naming Conventions

*   **Files & Folders:** snake\_case (Python standard)
*   **Variables & Functions:** snake\_case
*   **Constants:** UPPER\_SNAKE\_CASE
*   **Classes, Types, Interfaces, Components:** PascalCase

## Code Formatting (Enforced by Black/Ruff)

*   **Indentation:** 4 spaces
*   **Quotes:** Double quotes "" where appropriate
*   **Line Length:** 88 characters (Black default)
*   **Import Order:** isort standard

## General Rules

*   **API Error Handling:** All API routes must return standardized JSON error objects (e.g., `{ "error": "..." }`).
*   **Modularity:** Functions should be concise and focused on a single responsibility.
*   **Constants:** Avoid magic strings/numbers. Define in a central config.py or a dedicated constants file.
*   **Testing:** Every new feature must be accompanied by tests, aiming for high code coverage.

```