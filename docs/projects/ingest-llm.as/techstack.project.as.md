```markdown
# InGest-LLM.as: Technology Stack Version: 1.0

## Core Framework
*   Python 3.11
*   FastAPI: (Used for potential health check endpoints, though the service is primarily a background worker).

## Core Dependencies
*   `watchdog`: For monitoring file system events.
*   `qdrant-client`: To connect to the shared Qdrant vector database.
*   `pika`: To publish completion messages to RabbitMQ.
*   `lmstudio`: The SDK for interacting with the local embedding model.
*   `pydantic-settings`: For managing configuration and environment variables.

## Environment & Deployment
*   Docker & Docker Compose: The service will be fully containerized and integrated into the main `docker-compose.yml` file.
*   Shared Volumes: A Docker volume will be used for the `/ingest` directory to allow easy placement of files to be processed.

```