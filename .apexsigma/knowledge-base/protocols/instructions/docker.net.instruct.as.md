```markdown
# Guide: Docker Network Configuration for ApexSigma

This is a step-by-step manual for configuring the `docker-compose.yml` file to ensure all 13 containers can communicate correctly, both internally and with the host machine.

## Communication Flow Diagram

This diagram illustrates how the services communicate over the shared `apexsigma_net` Docker network.

```mermaid
graph TD
    subgraph External Access
        Developer/User -->|HTTP API Calls| Memos_API[memos.as];
        Developer/User -->|HTTP API Calls| Ingest_API[ingest-llm.as];
        Developer/User -->|Web UI on Port 3000| Grafana;
    end

    subgraph "ApexSigma Docker Network (apexsigma_net)"
        subgraph Core Services
            Memos_API -->|Reads/Writes Data| Postgres_Memos[PostgreSQL for memOS];
            Memos_API -->|Caches Data| Redis_Memos[Redis for memOS];
            Memos_API -->|Pub/Sub Events| RabbitMQ;
            Ingest_API -->|Sends Tasks| RabbitMQ;
        end

        subgraph Dependency Services
            Postgres_Memos;
            Redis_Memos;
            RabbitMQ;
            Qdrant;
            Postgres_Langfuse[PostgreSQL for Langfuse];
            Redis_Langfuse[Redis for Langfuse];
            Langfuse_Server[Langfuse Server];
        end

        subgraph Observability Stack
            Prometheus -->|Scrapes Metrics| Memos_API;
            Prometheus -->|Scrapes Metrics| Ingest_API;
            Loki -->|Collects Logs| Memos_API;
            Jaeger -->|Collects Traces| Memos_API;
            Grafana -->|Queries Data| Prometheus;
            Grafana -->|Queries Logs| Loki;
            Grafana -->|Queries Traces| Jaeger;
        end

        %% Connections
        Memos_API --> Qdrant;
        Ingest_API --> Qdrant;
        Langfuse_Server --> Postgres_Langfuse;
        Langfuse_Server --> Redis_Langfuse;
    end

    style Developer/User fill:#f9f,stroke:#333,stroke-width:2px

```

## Step 1: Define a Custom Network

First, create a custom **bridge network** to provide better isolation and allow containers to resolve each other by name. Add this block at the very end of your `docker-compose.yml` file:

```yaml
networks:
  apexsigma_net:
    driver: bridge

```

## Step 2: Assign All Services to the Custom Network

For **every service** defined in your `docker-compose.yml` file, you must tell it to connect to the `apexsigma_net`.

**Example (memos-api service):**

```yaml
services:
  memos-api:
    image: memos-api-image:latest
    container_name: memos-api
    # ... other configurations like environment variables ...
    networks:
      - apexsigma_net

```

**Instruction:** Apply this `networks` block to all 13 services.

## Step 3: Internal Communication (Container-to-Container)

Once on the same network, services communicate using their **service name as the hostname**.

Example:

The `memos-api` service needs to connect to its PostgreSQL database, which is named `postgres-memos` in `docker-compose.yml`.

  * **Service Name:** `postgres-memos`
  * **Database Port (internal):** `5432`
  * **Connection String:** `postgresql://user:password@postgres-memos:5432/memos_db`

Docker's internal DNS will automatically resolve `postgres-memos` to the correct container's internal IP address. **Do not use `localhost` or an IP address for inter-service communication.**

## Step 4: External Access (Connecting from Your Machine)

To access a container from your host machine (e.g., browser, Postman), you must map a port from the container to your host using the `ports` directive in the format `"HOST_PORT:CONTAINER_PORT"`.

Example (memos-api service):

The API runs on port `8000` inside its container. To access it from your computer, map it to a port on your host, like `8001`.

```yaml
services:
  memos-api:
    # ... other configurations ...
    ports:
      - "8001:8000" # Exposes container port 8000 on host port 8001
    networks:
      - apexsigma_net

```

**Instruction:** Now, to send a request to the API from your machine, you would use `http://localhost:8001`.

Apply this logic to any service that needs external access:

  * **Grafana:** map to `3000:3000` to access the UI at `http://localhost:3000`.
  * **Langfuse:** map to `3300:3000` to access its UI at `http://localhost:3300`.

<!-- end list -->

``` 
 
```
