FROM python:3.13-slim

WORKDIR /workspace

# Install basic tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

CMD ["sleep", "infinity"]