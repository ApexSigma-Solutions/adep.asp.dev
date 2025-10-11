# .devcontainer/Dockerfile - ApexSigma Ecosystem Development Environment
FROM python:3.13-slim

# Install system dependencies required for the ecosystem
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    postgresql-client \
    redis-tools \
    jq \
    bc \
    htop \
    tree \
    vim \
    nano \
    unzip \
    netcat-openbsd \
    dnsutils \
    iputils-ping \
    telnet \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry with version pinning for reproducibility
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Install pre-commit for quality gates
RUN pip install --no-cache-dir pre-commit

# Install Node.js 20 for Node.js services (if any)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs

# Configure Poetry for containerized development
RUN poetry config virtualenvs.create false && \
    poetry config virtualenvs.in-project false && \
    poetry config cache-dir /tmp/poetry-cache

# Create workspace directory
WORKDIR /workspace

# Copy project files for dependency installation
COPY libs/ ./libs/
COPY services/ ./services/
COPY pyproject.toml poetry.lock* ./

# Install Python dependencies
RUN for service_dir in services/*/; do \
        if [ -f "$service_dir/pyproject.toml" ]; then \
            echo "Installing dependencies for $(basename "$service_dir")..." && \
            cd "$service_dir" && \
            poetry install --no-root && \
            cd /workspace; \
        fi; \
    done

# Install shared library dependencies
RUN if [ -f "libs/apexsigma-core/pyproject.toml" ]; then \
        cd libs/apexsigma-core && \
        poetry install --no-root && \
        cd /workspace; \
    fi

# Clean up package cache to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash vscode
USER vscode

# Set up entrypoint
CMD ["sleep", "infinity"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python --version || exit 1