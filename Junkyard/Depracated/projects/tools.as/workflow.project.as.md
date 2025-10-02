``` markdown
# Development Workflow: tools.as

This document outlines the standard development workflow for contributing to the tools.as repository. Adherence to this workflow ensures code quality, consistency, and stability.

## 1. Branching Strategy

- **alpha**: The main development branch. All new work is merged into this branch.
- **feature/...**: All new features or bug fixes must be developed in a feature branch, created from the latest alpha.
  - Example: `feature/add-calculator-tool`

## 2. Local Development

1.  **Create Branch**: `git checkout -b feature/my-new-feature alpha`
2.  **Code**: Implement your changes.
3.  **Lint**: Before committing, run the linters to ensure code quality.
    `pylint $(git ls-files '*.py')`
    `flake8 .`
4.  **Test**: Run the test suite to ensure no existing functionality has been broken.
    `pytest`
5.  **Commit**: Commit your changes with a clear and descriptive message.

## 3. Code Review & Merging

1.  **Push**: Push your feature branch to the remote repository.
    `git push origin feature/my-new-feature`
2.  **Pull Request (PR)**: Open a Pull Request on GitHub from your feature branch to the alpha branch.
3.  **CI Checks**: The GitHub Actions workflows (`pylint.yml`, `python-app.yml`) will automatically run. The PR cannot be merged if these checks fail.
4.  **Peer Review**: At least one other developer or a designated review agent must approve the PR.
5.  **Merge**: Once approved and all checks have passed, the PR can be merged into alpha.

## 4. Dependency Management

- All new Python dependencies must be added to the `requirements.txt` file.
- Run `pip freeze > requirements.txt` after installing a new package to ensure the file is up-to-date.

```