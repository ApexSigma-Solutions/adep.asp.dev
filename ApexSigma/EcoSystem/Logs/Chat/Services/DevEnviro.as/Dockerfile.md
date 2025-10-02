---
title: Dockerfile
date created: Sunday, September 21st 2025, 3:00:28 pm
date modified: Sunday, September 21st 2025, 3:02:33 pm
---

# Dockerfile

```dockerfile
# 1. Base Image
FROM python:3.11-slim

# 2. Install System Dependencies (Unchanged)
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# 3. Install dotenvx
RUN npm install -g @dotenvx/dotenvx

# 4. Set up Working Environment (Unchanged)
WORKDIR /app

# 5. Install Python Dependencies with UV (Optimized)
# Use the new docker-specific requirements file
COPY ./requirements-docker.txt /app/requirements-docker.txt
RUN pip install uv && \
    uv pip install --system --no-cache-dir -r /app/requirements-docker.txt && \
    pip uninstall -y uv

# 6. Copy Application Code 
COPY ./app /app

# 8. Expose Port (Unchanged)
EXPOSE 8090

# 9. Define Start Command for TESTING
# This now runs our test script directly and will keep the container alive.
CMD ["dotenvx", "run", "--", "python", "-u", "/app/src/main.py"]
```
