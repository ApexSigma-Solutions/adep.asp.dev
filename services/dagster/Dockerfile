FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt/dagster/app

# Install Dagster and dependencies
RUN pip install dagster dagster-webserver dagster-postgres psycopg2-binary

# Copy application files
COPY definitions.py /opt/dagster/app/
COPY workspace.yaml /opt/dagster/dagster_home/
COPY dagster.yaml /opt/dagster/dagster_home/

# Create dagster user
RUN useradd -m -s /bin/bash dagster
RUN chown -R dagster:dagster /opt/dagster
USER dagster

# Expose port
EXPOSE 3000

# Default command
CMD ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000", "-w", "/opt/dagster/dagster_home/workspace.yaml"]
