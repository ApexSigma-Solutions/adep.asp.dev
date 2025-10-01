FROM python:3.11-slim

RUN pip install dagster dagster-webserver

WORKDIR /app/dagster_home

COPY . .

EXPOSE 8080

CMD ["dagster-webserver", "-h", "0.0.0.0", "-p", "8080"]
