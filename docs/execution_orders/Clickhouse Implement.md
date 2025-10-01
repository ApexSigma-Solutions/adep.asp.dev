# Clickhouse Implementation Snippets


'prometheus' Remote Write Yaml 

```yaml
remote_write:
  - url: "http://clickhouse:8123/"
    queue_config:
      capacity: 10000
      max_shards: 10
      max_samples_per_send: 5000
    write_relabel_configs:
      - source_labels: [__name__]
        regex: '.*'
        target_label: source
        replacement: 'prometheus'
```

```env
# ClickHouse Configuration
CLICKHOUSE_HOST=clickhouse
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=clickhouse_user
CLICKHOUSE_PASSWORD=change_me_securely
CLICKHOUSE_DB=apexsigma_observability
CLICKHOUSE_NATIVE_PORT=9000
```