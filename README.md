# ApexSigma Projects Development Environment

## Overview
This is the unified development environment for the ApexSigma ecosystem, featuring a Society of Agents architecture for intelligent automation and content management. This monorepo contains all the services, libraries, and scripts necessary to run the ecosystem.

## Projects

### `libs/apexsigma-core`
The core library for the ApexSigma ecosystem. It contains the data models and interfaces used by all services.

### `services/memos.as`
The main application for knowledge management. It provides a memory and tool discovery hub for the AI agents in the ecosystem.

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Poetry
- Git

### Setup
1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```
2.  **Install dependencies:**
    This project uses Poetry for dependency management. To install the dependencies for all projects, you can run the following command from the root of the repository:
    ```bash
    # For apexsigma-core
    poetry install --with docs -C libs/apexsigma-core

    # For memos.as
    pip install -r services/memos.as.bak/requirements.txt
    pip install -r services/memos.as.bak/requirements-observability.txt
    ```
3.  **Start the services:**
    The entire ecosystem can be started with a single Docker Compose command:
    ```bash
    docker-compose -f docker-compose.unified.yml up -d
    ```
    This will start all the services, including the databases, messaging queues, and the main applications.

### Usage
Once the services are running, you can interact with them through their respective APIs. The main entry point for the ecosystem is the `devenviro.as` service, which orchestrates the other services.

## Documentation
This repository contains comprehensive documentation for all its projects, built with MkDocs.

### Building the Documentation
To build the documentation for all projects, run the following command from the root of the repository:
```bash
python scripts/build_ecosystem_docs.py build
```
This will generate the static documentation sites in the `site` directory of each project.

### Viewing the Documentation
After building the documentation, you can view it by opening the `index.html` file in the `site` directory of each project. For example:
-   **apexsigma-core:** `libs/apexsigma-core/site/index.html`
-   **memos.as:** `services/memos.as.bak/site/index.html`

You can also serve the documentation locally using the following command:
```bash
# For apexsigma-core
mkdocs serve -f libs/apexsigma-core/mkdocs.yml

# For memos.as
mkdocs serve -f services/memos.as.bak/mkdocs.yml
```

## Directory Structure

```
.
├── libs/
│   └── apexsigma-core/  # Core library with data models and interfaces
├── services/
│   └── memos.as.bak/    # The main knowledge management service
├── scripts/             # Utility and automation scripts
├── docs/                # General documentation for the ecosystem
├── tests/               # Integration and end-to-end tests
└── docker-compose.unified.yml
```

---

**Last Updated**: September 22, 2025
**Ecosystem Status**: ✅ Operational
