```sh
ApexSigmaProjects.Dev
└── services
    ├── dagster
    │   └── Dockerfile
    ├── devenviro.as
    │   ├── .codacy
    │   ├── .md
    │   │   └── .persist
    │   │       └── logs
    │   ├── ${workspaceFolder}
    │   │   └── context_portal
    │   │       └── .md
    │   │           └── .persist
    │   │               └── logs
    │   ├── agentsmith
    │   │   ├── agentsmith.types.ts
    │   │   └── globals.json
    │   ├── app
    │   │   ├── agents
    │   │   │   ├── personas
    │   │   │   │   └── __init__.py
    │   │   │   └── __init__.py
    │   │   ├── bridge
    │   │   │   ├── __init__.py
    │   │   │   ├── agent_proxy.py
    │   │   │   └── config.py
    │   │   ├── listeners
    │   │   │   └── github_copilot_listener.py
    │   │   ├── migrations
    │   │   │   ├── 006_1_add_missing_columns.sql
    │   │   │   ├── 006_create_agent_registry.sql
    │   │   │   └── 006_create_session_prompts.sql
    │   │   ├── src
    │   │   │   ├── api
    │   │   │   │   ├── __init__.py
    │   │   │   │   └── poml.py
    │   │   │   ├── core
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── agent_database.py
    │   │   │   │   ├── database.py
    │   │   │   │   ├── enhanced_initialization_manager.py
    │   │   │   │   ├── migrations_runner.py
    │   │   │   │   ├── observability.py
    │   │   │   │   └── orchestrator.py
    │   │   │   ├── services
    │   │   │   │   ├── poml
    │   │   │   │   │   ├── templates
    │   │   │   │   │   │   ├── agent_communication.poml
    │   │   │   │   │   │   ├── observability_report.poml
    │   │   │   │   │   │   └── task_orchestration.poml
    │   │   │   │   │   ├── __init__.py
    │   │   │   │   │   ├── library.py
    │   │   │   │   │   └── test_poml.py
    │   │   │   │   ├── __init__.py
    │   │   │   │   └── database_migration.py
    │   │   │   ├── __init__.py
    │   │   │   ├── main.py
    │   │   │   ├── seed_knowledge.py
    │   │   │   └── test_poml_api.py
    │   │   ├── tests
    │   │   │   ├── core
    │   │   │   │   └── test_database.py
    │   │   │   ├── services
    │   │   │   │   └── test_database_migration.py
    │   │   │   ├── conftest.py
    │   │   │   ├── test_agent_database.py
    │   │   │   ├── test_coverage_verification.py
    │   │   │   └── test_main.py
    │   │   ├── __init__.py
    │   │   └── config.py
    │   ├── config
    │   │   ├── env-templates
    │   │   │   └── .env.standardized
    │   │   ├── grafana
    │   │   │   └── provisioning
    │   │   ├── grafana.ini
    │   │   ├── loki-config.yml
    │   │   ├── prometheus.yml
    │   │   └── promtail-config.yml
    │   ├── scripts
    │   │   ├── ApexSigma Session Start Sequence.md
    │   │   ├── Boot Command Guide.md
    │   │   ├── Boot Sequence Configuration.toml
    │   │   ├── CLAUDE.local.md
    │   │   └── Systems_Boot_Sequence_Script.py
    │   ├── .env.vault
    │   ├── .pre-commit-config.yaml
    │   ├── CLAUDE.md
    │   ├── COPILOT.md
    │   ├── Dockerfile
    │   ├── GEMINI.md
    │   ├── poetry.lock
    │   ├── pyproject.toml
    │   ├── QWEN.md
    │   ├── run_pytest.bat
    │   ├── run_pytest.py
    │   ├── run_tests.bat
    │   ├── run_tests.sh
    │   └── TESTING.md
    ├── InGest-LLM.as
    │   ├── .github
    │   │   └── workflows
    │   │       └── pull_request_check.yml
    │   ├── .ingest
    │   │   ├── raw_documents
    │   │   │   ├── code
    │   │   │   │   ├── beta.ingest.as.json
    │   │   │   │   ├── carchat27082025.ingest.as.json
    │   │   │   │   ├── Omega Ingest Guardian.poml
    │   │   │   │   ├── Omega Ingest Update V26.poml.xml
    │   │   │   │   ├── omega.ingest.as.v17.json
    │   │   │   │   └── session.ingest.as.poml
    │   │   │   └── text
    │   │   │       ├── 1_chat26082025.ingest.as.md
    │   │   │       ├── 1_chat27082025.ingest.as.md
    │   │   │       ├── 1_chat28082025.ingest.as.md
    │   │   │       ├── 2_chat26082025.ingest.as.md
    │   │   │       ├── 2_chat28082025.ingest.as.md
    │   │   │       ├── 20250830-Omega.ingest.as.md
    │   │   │       ├── 3_chat26082025.ingest.as.md
    │   │   │       ├── Agent Tasks .md
    │   │   │       ├── chat26082025.ingest.as.md
    │   │   │       ├── constrat.poml.ingest.as.md
    │   │   │       ├── High Tasks .md
    │   │   │       ├── High-Level Agent Task List 20082025.md
    │   │   │       ├── High-Level Task List 18082025.md
    │   │   │       ├── High-Level Task List 19082025.md
    │   │   │       └── High-Level Task List 20082025.md
    │   │   ├── .ingest_config
    │   │   ├── OPERATIONS_SUMMARY.md
    │   │   ├── process_and_cleanup.ps1
    │   │   └── PROCESSING_STATUS_REPORT.md
    │   ├── .md
    │   │   ├── .project
    │   │   │   ├── architecture.project.as.md
    │   │   │   ├── brand.project.as.md
    │   │   │   ├── brief.project.as.md
    │   │   │   ├── plan.project.as.md
    │   │   │   ├── task.project.as.md
    │   │   │   └── techstack.project.as.md
    │   │   └── .projects
    │   │       ├── current_context.md
    │   │       ├── ECOSYSTEM_CONSOLIDATION_PLAN.md
    │   │       ├── integration_progress_20250819_010446.md
    │   │       ├── integration_progress_20250819.md
    │   │       ├── KNOWLEDGE_BASE_MIGRATION.md
    │   │       ├── pypi.plan.project.as.md
    │   │       ├── SPRINT_EXECUTION_LOG_20250824.md
    │   │       └── SPRINT_PLAN_20250824.md
    │   ├── ${workspaceFolder}
    │   │   └── context_portal
    │   │       └── logs
    │   │           └── conport.log
    │   ├── app
    │   │   └── services
    │   │       └── e2e_tracing.py
    │   ├── docs
    │   │   ├── reference
    │   │   │   ├── analysis.md
    │   │   │   ├── index.md
    │   │   │   ├── ingestion.md
    │   │   │   ├── observability.md
    │   │   │   └── services.md
    │   │   ├── api_ingestion_endpoints.md
    │   │   ├── docker-compose.README.md
    │   │   ├── ECOSYSTEM_INGESTION_COMPLETE.md
    │   │   ├── EMBEDDING_AGENT_ARCHITECTURE.md
    │   │   ├── EMBEDDING_AGENT_IMPLEMENTATION.md
    │   │   ├── EMBEDDING_INTEGRATION_COMPLETE.md
    │   │   ├── File_Processing_Operations_Manual.md
    │   │   ├── INTEGRATION_TESTING.md
    │   │   ├── nomic_system_prompt.md
    │   │   ├── observability-dashboard.md
    │   │   ├── observability-implementation-summary.md
    │   │   ├── PROGRESS_TRANSFER_SUMMARY.md
    │   │   ├── PROGRESS.md
    │   │   ├── QWEN_PROJECT_ANALYSIS.md
    │   │   ├── REPOSITORY_PROGRESS_TRACKING.md
    │   │   ├── STATUS.md
    │   │   └── Training_Guide.md
    │   ├── integration
    │   │   └── tools_as_integration.py
    │   ├── prompts
    │   │   ├── agent_context_bullet_20250819.poml
    │   │   ├── agent_context_template.poml
    │   │   ├── critical_blocker.poml
    │   │   ├── mission_brief.poml
    │   │   ├── priority_tasks.poml
    │   │   └── project_status.poml
    │   ├── scripts
    │   │   ├── analyze_embedding_efficiency.py
    │   │   ├── analyze_repository.py
    │   │   ├── build_docs.py
    │   │   ├── chat_thread_summarizer.py
    │   │   ├── eod_ecosystem_update.py
    │   │   ├── generate_context_bullet.py
    │   │   ├── generate_embedding_docs.py
    │   │   ├── generate_project_docs.py
    │   │   ├── qwen_demo_success.py
    │   │   ├── qwen_project_analysis.py
    │   │   ├── run_core_integration_tests.py
    │   │   ├── simple_ecosystem_test.py
    │   │   ├── simple_qwen_test.py
    │   │   └── simple_repo_analysis.py
    │   ├── src
    │   │   └── ingest_llm_as
    │   │       ├── api
    │   │       │   ├── __init__.py
    │   │       │   ├── analysis.py
    │   │       │   ├── ecosystem.py
    │   │       │   ├── ingestion.py
    │   │       │   ├── omega_ingest_simple.py
    │   │       │   ├── omega_ingest.py
    │   │       │   └── repository.py
    │   │       ├── observability
    │   │       │   ├── __init__.py
    │   │       │   ├── langfuse_client.py
    │   │       │   ├── logging.py
    │   │       │   ├── metrics.py
    │   │       │   ├── setup.py
    │   │       │   └── tracing.py
    │   │       ├── parsers
    │   │       │   ├── __init__.py
    │   │       │   └── python_ast_parser.py
    │   │       ├── routers
    │   │       │   └── eod_logs.py
    │   │       ├── services
    │   │       │   ├── __init__.py
    │   │       │   ├── ecosystem_ingestion.py
    │   │       │   ├── llm_cache.py
    │   │       │   ├── memos_client.py
    │   │       │   ├── nomic_code_analyzer.py
    │   │       │   ├── omega_ingest_guardian.py
    │   │       │   ├── progress_logger.py
    │   │       │   ├── project_analyzer.py
    │   │       │   ├── project_documentation_generator.py
    │   │       │   ├── repository_processor.py
    │   │       │   └── vectorizer.py
    │   │       ├── utils
    │   │       │   ├── __init__.py
    │   │       │   └── content_processor.py
    │   │       ├── __init__.py
    │   │       ├── config.py
    │   │       ├── main.py
    │   │       └── models.py
    │   ├── test_output
    │   │   ├── chat_summary_20250819_031314.json
    │   │   ├── chat_summary_20250819_031314.md
    │   │   ├── chat_summary_20250819_060853.json
    │   │   ├── chat_summary_20250819_060853.md
    │   │   ├── chat_summary_20250819_061008.json
    │   │   └── chat_summary_20250819_061008.md
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── context_bullet_test.md
    │   │   ├── embedding_integration_demo.py
    │   │   ├── pytest.ini
    │   │   ├── test_chat_sample.txt
    │   │   ├── test_chat_summarizer.py
    │   │   ├── test_ecosystem_ingestion.py
    │   │   ├── test_ingestion_e2e.py
    │   │   ├── test_langfuse_connection.py
    │   │   ├── test_langfuse_decorator.py
    │   │   ├── test_llm_trace.py
    │   │   ├── test_memos_integration_core.py
    │   │   ├── test_nomic_embeddings.py
    │   │   ├── test_qwen_integration.py
    │   │   └── test_repository_ingestion.py
    │   ├── .dockerignore
    │   ├── .largefiles
    │   ├── .pre-commit-config.yaml
    │   ├── # COPILOT.md
    │   ├── # QWEN.md
    │   ├── 20250822_ingest-llm_bundle.md
    │   ├── api_ingestion_endpoints.md
    │   ├── CLAUDE.md
    │   ├── debug_test.py
    │   ├── Dockerfile
    │   ├── GEMINI.md
    │   ├── mkdocs.yml
    │   ├── OPERATION_ASGARD_BASELINE_BUNDLE.md
    │   ├── poetry.lock
    │   ├── pyproject.toml
    │   ├── pytest.ini
    │   └── QWEN.md
    ├── memos.as
    │   ├── .cursor
    │   │   ├── rules
    │   │   │   ├── taskmaster
    │   │   │   │   ├── dev_workflow.mdc
    │   │   │   │   └── taskmaster.mdc
    │   │   │   ├── cursor_rules.mdc
    │   │   │   └── self_improve.mdc
    │   │   └── mcp.json
    │   ├── .gemini
    │   │   └── settings.json
    │   ├── .github
    │   │   ├── workflows
    │   │   │   ├── pull_request_check.yml
    │   │   │   └── python-app.yml
    │   │   ├── architect.chatmode.md
    │   │   ├── ask.chatmode.md
    │   │   ├── code.chatmode.md
    │   │   ├── copilot-instructions.md
    │   │   └── debug.chatmode.md
    │   ├── .ingest
    │   │   ├── omega.ingest.as
    │   │   │   ├── Copilot.ingest.as.yml
    │   │   │   ├── omega.ingest.as.json
    │   │   │   └── Qwen.ingest.as.yml
    │   │   ├── app.ini
    │   │   └── beta.ingest.as.json
    │   ├── .md
    │   │   ├── .instruct
    │   │   │   ├── ettiquette.instruct.md
    │   │   │   ├── mar_protocol.instruct.md
    │   │   │   ├── mkdocs.instruct.as.md
    │   │   │   └── mkdocs.instruct.md
    │   │   ├── .persist
    │   │   │   ├── .mcp.json
    │   │   │   ├── log_import_error_troubleshooting.py
    │   │   │   ├── log_progress.py
    │   │   │   ├── PROGRESS_LOG.md
    │   │   │   └── session_2025-08-17.poml
    │   │   ├── .project
    │   │   │   ├── 20250813_memos.project.ingest.as.json
    │   │   │   ├── architecture.project.as.md
    │   │   │   ├── brand.project.as.md
    │   │   │   ├── brief.project.as.md
    │   │   │   ├── mcp.task.project.as.md
    │   │   │   ├── observability.completed.md
    │   │   │   ├── pip_freeze.ini
    │   │   │   ├── plan.project.as.md
    │   │   │   ├── plan.project.asV1.archived..md
    │   │   │   ├── security.project.as.md
    │   │   │   ├── task.project.as.md
    │   │   │   ├── task.project.asV1.archived.md
    │   │   │   └── techstsack.project.as.md
    │   │   ├── 20250122_memos_as_production_bundle.md
    │   │   ├── CLAUDE.md
    │   │   ├── COPILOT.md
    │   │   ├── DEPLOYMENT_SUCCESS.md
    │   │   ├── GEMINI.md
    │   │   ├── MEMOS_PROGRESS_UPDATE.md
    │   │   ├── OBSERVABILITY_COMPLETE.md
    │   │   ├── OBSERVABILITY_STATUS.md
    │   │   ├── OBSERVABILITY.md
    │   │   ├── OPERATION_ASGARD_REBIRTH_BASELINE.md
    │   │   └── QWEN.md
    │   ├── .taskmaster
    │   │   ├── docs
    │   │   │   ├── Creating and Registering Tools in FastMCP.md
    │   │   │   ├── FINAL Sprint Plan MCP HTTP Client Implementation.md
    │   │   │   ├── prd.txt
    │   │   │   └── tools_verbose.yml
    │   │   ├── tasks
    │   │   │   └── tasks.json
    │   │   ├── templates
    │   │   │   └── example_prd.txt
    │   │   ├── config.json
    │   │   └── state.json
    │   ├── ${workspaceFolder}
    │   │   └── context_portal
    │   ├── app
    │   │   ├── dagster
    │   │   │   ├── __init__.py
    │   │   │   ├── assets.py
    │   │   │   └── repository.py
    │   │   ├── progress_logs
    │   │   │   └── 20250824_redis_observability_enhancement.md
    │   │   ├── services
    │   │   │   ├── __init__.py
    │   │   │   ├── database_health.py
    │   │   │   ├── e2e_tracing.py
    │   │   │   ├── neo4j_client.py
    │   │   │   ├── observability_decorators.py
    │   │   │   ├── observability.py
    │   │   │   ├── postgres_client.py
    │   │   │   ├── qdrant_client.py
    │   │   │   ├── redis_client.py
    │   │   │   ├── redis_lock.py
    │   │   │   └── redis_utils.py
    │   │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── background_worker.py
    │   │   ├── config.py
    │   │   ├── log_progress.md
    │   │   ├── log_progress.py
    │   │   ├── main_observability.py
    │   │   ├── main.py
    │   │   ├── mcp_server.py
    │   │   ├── models.py
    │   │   ├── schemas.py
    │   │   └── tools.py
    │   ├── config
    │   │   ├── grafana
    │   │   │   ├── dashboards
    │   │   │   │   ├── memos-logs.json
    │   │   │   │   └── memos-observability.json
    │   │   │   └── provisioning
    │   │   │       ├── dashboards
    │   │   │       │   └── dashboards.yml
    │   │   │       └── datasources
    │   │   │           └── datasources.yml
    │   │   ├── alert_rules.yml
    │   │   ├── loki-config.yaml
    │   │   ├── otel-collector-config.yaml
    │   │   ├── prometheus.yml
    │   │   └── promtail-config.yaml
    │   ├── docs
    │   │   ├── how-to
    │   │   │   └── index.md
    │   │   ├── reference
    │   │   │   ├── index.md
    │   │   │   ├── omega-ingest-knowledge-graph-prompt.md
    │   │   │   └── services.md
    │   │   ├── summaries
    │   │   │   ├── memos_chat_summary_20250819_061434.json
    │   │   │   └── memos_chat_summary_20250819_061434.md
    │   │   ├── tutorials
    │   │   │   └── index.md
    │   │   ├── AGENT.md
    │   │   ├── ECOSYSTEM_STATUS_REPORT.md
    │   │   ├── GEMINI.md
    │   │   └── index.md
    │   ├── memory-bank
    │   │   ├── activeContext.md
    │   │   ├── architect.md
    │   │   ├── decisionLog.md
    │   │   ├── productContext.md
    │   │   ├── progress.md
    │   │   ├── projectBrief.md
    │   │   └── systemPatterns.md
    │   ├── memos
    │   │   └── __init__.py
    │   ├── progress_logs
    │   │   ├── 20250824_achievements.json
    │   │   ├── 20250824_phase2_session_metadata.json
    │   │   ├── 20250825_achievements.json
    │   │   └── 20250825_orchestrator_fix_metadata.json
    │   ├── scripts
    │   │   ├── chat_thread_summarizer.py
    │   │   ├── init_database.py
    │   │   ├── instrumentation_example.py
    │   │   ├── integrate_observability.py
    │   │   ├── log_orchestrator_fix_progress.py
    │   │   ├── log_phase2_progress.py
    │   │   ├── log_progress.py
    │   │   ├── log_tiered_storage_progress.py
    │   │   ├── log_troubleshooting.py
    │   │   ├── seed_tools.py
    │   │   ├── setup_observability.py
    │   │   └── setup_test_databases.py
    │   ├── .pre-commit-config.yaml
    │   ├── Dockerfile
    │   ├── GEMINI.md
    │   ├── mcp.memos.as.code-workspace
    │   ├── mkdocs.yml
    │   ├── poetry.lock
    │   ├── pyproject.toml
    │   ├── requirements-observability.txt
    │   └── VERIFIED_DOCKER_NETWORK_MAP.md
    ├── memos.as.bak
    │   ├── .cursor
    │   │   ├── rules
    │   │   │   ├── taskmaster
    │   │   │   │   ├── dev_workflow.mdc
    │   │   │   │   └── taskmaster.mdc
    │   │   │   ├── cursor_rules.mdc
    │   │   │   └── self_improve.mdc
    │   │   └── mcp.json
    │   ├── .gemini
    │   │   └── settings.json
    │   ├── .github
    │   │   ├── workflows
    │   │   │   ├── pull_request_check.yml
    │   │   │   └── python-app.yml
    │   │   ├── architect.chatmode.md
    │   │   ├── ask.chatmode.md
    │   │   ├── code.chatmode.md
    │   │   ├── copilot-instructions.md
    │   │   └── debug.chatmode.md
    │   ├── .ingest
    │   │   ├── omega.ingest.as
    │   │   │   ├── Copilot.ingest.as.yml
    │   │   │   ├── omega.ingest.as.json
    │   │   │   └── Qwen.ingest.as.yml
    │   │   ├── app.ini
    │   │   └── beta.ingest.as.json
    │   ├── .md
    │   │   ├── .instruct
    │   │   │   ├── ettiquette.instruct.md
    │   │   │   ├── mar_protocol.instruct.md
    │   │   │   ├── mkdocs.instruct.as.md
    │   │   │   └── mkdocs.instruct.md
    │   │   ├── .persist
    │   │   │   ├── .mcp.json
    │   │   │   ├── log_import_error_troubleshooting.py
    │   │   │   ├── log_progress.py
    │   │   │   ├── PROGRESS_LOG.md
    │   │   │   └── session_2025-08-17.poml
    │   │   ├── .project
    │   │   │   ├── 20250813_memos.project.ingest.as.json
    │   │   │   ├── architecture.project.as.md
    │   │   │   ├── brand.project.as.md
    │   │   │   ├── brief.project.as.md
    │   │   │   ├── mcp.task.project.as.md
    │   │   │   ├── observability.completed.md
    │   │   │   ├── pip_freeze.ini
    │   │   │   ├── plan.project.as.md
    │   │   │   ├── plan.project.asV1.archived..md
    │   │   │   ├── security.project.as.md
    │   │   │   ├── task.project.as.md
    │   │   │   ├── task.project.asV1.archived.md
    │   │   │   └── techstsack.project.as.md
    │   │   ├── 20250122_memos_as_production_bundle.md
    │   │   ├── CLAUDE.md
    │   │   ├── COPILOT.md
    │   │   ├── DEPLOYMENT_SUCCESS.md
    │   │   ├── GEMINI.md
    │   │   ├── MEMOS_PROGRESS_UPDATE.md
    │   │   ├── OBSERVABILITY_COMPLETE.md
    │   │   ├── OBSERVABILITY_STATUS.md
    │   │   ├── OBSERVABILITY.md
    │   │   ├── OPERATION_ASGARD_REBIRTH_BASELINE.md
    │   │   └── QWEN.md
    │   ├── .taskmaster
    │   │   ├── docs
    │   │   │   ├── Creating and Registering Tools in FastMCP.md
    │   │   │   ├── FINAL Sprint Plan MCP HTTP Client Implementation.md
    │   │   │   ├── prd.txt
    │   │   │   └── tools_verbose.yml
    │   │   ├── reports
    │   │   ├── tasks
    │   │   │   └── tasks.json
    │   │   ├── templates
    │   │   │   └── example_prd.txt
    │   │   ├── config.json
    │   │   └── state.json
    │   ├── ${workspaceFolder}
    │   │   └── context_portal
    │   ├── app
    │   │   ├── progress_logs
    │   │   │   └── 20250824_redis_observability_enhancement.md
    │   │   ├── services
    │   │   │   ├── __init__.py
    │   │   │   ├── database_health.py
    │   │   │   ├── e2e_tracing.py
    │   │   │   ├── neo4j_client.py
    │   │   │   ├── observability_decorators.py
    │   │   │   ├── observability.py
    │   │   │   ├── postgres_client.py
    │   │   │   ├── qdrant_client.py
    │   │   │   ├── redis_client.py
    │   │   │   ├── redis_lock.py
    │   │   │   └── redis_utils.py
    │   │   ├── tests
    │   │   │   ├── integration
    │   │   │   └── unit
    │   │   ├── __init__.py
    │   │   ├── background_worker.py
    │   │   ├── config.py
    │   │   ├── log_progress.md
    │   │   ├── log_progress.py
    │   │   ├── main_observability.py
    │   │   ├── main.py
    │   │   ├── mcp_server.py
    │   │   ├── models.py
    │   │   ├── schemas.py
    │   │   └── tools.py
    │   ├── config
    │   │   ├── grafana
    │   │   │   ├── dashboards
    │   │   │   │   ├── memos-logs.json
    │   │   │   │   └── memos-observability.json
    │   │   │   └── provisioning
    │   │   │       ├── dashboards
    │   │   │       │   └── dashboards.yml
    │   │   │       └── datasources
    │   │   │           └── datasources.yml
    │   │   ├── alert_rules.yml
    │   │   ├── loki-config.yaml
    │   │   ├── otel-collector-config.yaml
    │   │   ├── prometheus.yml
    │   │   └── promtail-config.yaml
    │   ├── docs
    │   │   ├── how-to
    │   │   │   └── index.md
    │   │   ├── reference
    │   │   │   ├── index.md
    │   │   │   ├── omega-ingest-knowledge-graph-prompt.md
    │   │   │   └── services.md
    │   │   ├── summaries
    │   │   │   ├── memos_chat_summary_20250819_061434.json
    │   │   │   └── memos_chat_summary_20250819_061434.md
    │   │   ├── tutorials
    │   │   │   └── index.md
    │   │   ├── AGENT.md
    │   │   ├── ECOSYSTEM_STATUS_REPORT.md
    │   │   ├── GEMINI.md
    │   │   └── index.md
    │   ├── mcp_client
    │   ├── memory-bank
    │   │   ├── activeContext.md
    │   │   ├── architect.md
    │   │   ├── decisionLog.md
    │   │   ├── productContext.md
    │   │   ├── progress.md
    │   │   ├── projectBrief.md
    │   │   └── systemPatterns.md
    │   ├── progress_logs
    │   │   ├── 20250824_achievements.json
    │   │   ├── 20250824_phase2_session_metadata.json
    │   │   ├── 20250825_achievements.json
    │   │   └── 20250825_orchestrator_fix_metadata.json
    │   ├── scripts
    │   │   ├── chat_thread_summarizer.py
    │   │   ├── init_database.py
    │   │   ├── instrumentation_example.py
    │   │   ├── integrate_observability.py
    │   │   ├── log_orchestrator_fix_progress.py
    │   │   ├── log_phase2_progress.py
    │   │   ├── log_progress.py
    │   │   ├── log_tiered_storage_progress.py
    │   │   ├── log_troubleshooting.py
    │   │   ├── seed_tools.py
    │   │   ├── setup_observability.py
    │   │   └── setup_test_databases.py
    │   ├── tests
    │   ├── .pre-commit-config.yaml
    │   ├── docker-compose.unified.yml
    │   ├── Dockerfile
    │   ├── GEMINI.md
    │   ├── mcp.memos.as.code-workspace
    │   ├── mkdocs.yml
    │   ├── poetry.lock
    │   ├── pyproject.toml
    │   ├── requirements-observability.txt
    │   ├── requirements.txt
    │   └── VERIFIED_DOCKER_NETWORK_MAP.md
    └── tools.as
        ├── .claude
        │   └── settings.local.json
        ├── .github
        │   ├── workflows
        │   │   └── pull_request_check.yml
        │   └── copilot-instructions.md
        ├── .ingest
        │   ├── beta.ingest.as.json
        │   └── omega.ingest.as.json
        ├── .md
        │   ├── .instruct
        │   │   └── mkdocs.instruct.as.md
        │   ├── .persist
        │   │   ├── test.db
        │   │   └── toolkit.db
        │   ├── .project
        │   │   ├── architecture.project.as.md
        │   │   ├── brand.project.as.md
        │   │   ├── brief.project.as.md
        │   │   ├── plan.project.as.md
        │   │   ├── security.project.as.md
        │   │   ├── tasks.project.as.md
        │   │   ├── techstack.project.as.md
        │   │   └── workflow.project.as.md
        │   ├── .rules
        │   │   └── naming.rules.as.md
        │   ├── .tools
        │   │   ├── .command
        │   │   │   └── create_readme_python.toml
        │   │   ├── .commands
        │   │   │   ├── changelog.toml
        │   │   │   ├── clip.toml
        │   │   │   ├── create_readme_node.command.as.toml
        │   │   │   ├── create_readme_node.toml
        │   │   │   ├── create_readme_python.command.as.toml
        │   │   │   ├── create_readme_python.toml
        │   │   │   ├── create_readme.toml
        │   │   │   ├── design_decompose_request.toml
        │   │   │   ├── design_update_architecture.toml
        │   │   │   ├── design_validate_plan.toml
        │   │   │   ├── dev-log-search.toml
        │   │   │   ├── dev-telemetry-status.toml
        │   │   │   ├── dev-trace-last-request.toml
        │   │   │   ├── eod (2).toml
        │   │   │   ├── eod.command.as.toml
        │   │   │   ├── eod.toml
        │   │   │   ├── extract_design.toml
        │   │   │   ├── format_toml.py
        │   │   │   ├── iterate_design.toml
        │   │   │   ├── outdated_package.toml
        │   │   │   ├── outline (2).toml
        │   │   │   ├── outline.command.as.toml
        │   │   │   ├── outline.toml
        │   │   │   ├── parallel_tasks.toml
        │   │   │   ├── prep.toml
        │   │   │   ├── scaffold (2).toml
        │   │   │   ├── scaffold.command.as.toml
        │   │   │   ├── scaffold.toml
        │   │   │   ├── scratchpad.toml
        │   │   │   ├── sod.command.as.toml
        │   │   │   ├── sod.toml
        │   │   │   ├── stack-status.toml
        │   │   │   ├── trace-last.toml
        │   │   │   └── ui_ux_expert.toml
        │   │   ├── .mcp
        │   │   │   └── claudecode.mcp.md
        │   │   ├── create_readme_node.command.as.toml
        │   │   ├── create_readme_python.command.as.toml
        │   │   ├── eod.command.as.toml
        │   │   ├── eod.ecosystem.command.as.toml
        │   │   ├── mcp.tools.as.md
        │   │   ├── outline.command.as.toml
        │   │   ├── scaffold.command.as.toml
        │   │   └── sod.command.as.toml
        │   ├── CLAUDE.md
        │   └── GEMINI.md
        ├── .pytest_cache
        ├── ${workspaceFolder}
        │   └── context_portal
        │       └── logs
        │           └── conport.log
        ├── app
        │   ├── services
        │   │   ├── e2e_tracing.py
        │   │   └── observability.py
        │   ├── tests
        │   │   ├── __init__.py
        │   │   └── test_main.py
        │   ├── __init__.py
        │   ├── database.py
        │   ├── main.py
        │   ├── models.py
        │   └── schemas.py
        ├── docs
        │   └── reference
        │       ├── api.md
        │       ├── index.md
        │       ├── models.md
        │       └── schemas.md
        ├── scripts
        │   ├── chat_thread_summarizer.py
        │   ├── docker-dev.sh
        │   └── init-db.sql
        ├── summaries
        │   ├── tools_chat_summary_20250819_061326.json
        │   ├── tools_chat_summary_20250819_061326.md
        │   ├── tools_chat_summary_20250819_061351.json
        │   └── tools_chat_summary_20250819_061351.md
        ├── tests
        │   ├── test_chat_thread_summarizer.py
        │   ├── test_main.py
        │   ├── test_models.py
        │   └── test_schemas.py
        ├── .dockerignore
        ├── .flake8
        ├── .pylintrc
        ├── .python-version
        ├── # COPILOT.md
        ├── 20250122_tools_as_production_bundle.md
        ├── CLAUDE.md
        ├── Dockerfile
        ├── GEMINI.md
        ├── mkdocs.yml
        ├── OBSERVABILITY.md
        ├── poetry.lock
        ├── pyproject.toml
        ├── QWEN.md
        ├── requirements.txt
        ├── test_observability.py
        ├── test.db
        ├── toolkit.db
        ├── TOOLS_AS_OPERATION_ASGARD_BASELINE_BUNDLE.md
        └── uv.lock

171 directories, 603 files
```