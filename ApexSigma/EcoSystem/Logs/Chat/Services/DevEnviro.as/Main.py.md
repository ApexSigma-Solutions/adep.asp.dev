---
title: Main.py
date created: Sunday, September 21st 2025, 2:49:39 pm
date modified: Sunday, September 21st 2025, 2:54:09 pm
---

# Main.py

```python
import logging
import os
from pathlib import Path
import sys
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Ensure the project root is in the Python path
sys.path.append("/app")
project_root = Path(__file__).parent.parent

from src.core.enhanced_initialization_manager import EnhancedInitializationManager
from src.core.orchestrator import Orchestrator
from src.core.observability import DevEnviroObservability
from src.seed_knowledge import seed_knowledge_documents
from src.core.migrations_runner import apply_migrations
# CORRECTED IMPORT: Use absolute path from the 'app' root
from Workflows.author_reviewer_workflow import create_demo_author_reviewer_task

# Initialize observability system
observability = DevEnviroObservability()

# Global variable to track initialization status
initialization_status = {
    "initialized": False,
    "error": None,
    "services": {
        "database": False,
        "observability": False,
        "agents": False,
        "communication": False
    }
}

app = FastAPI()

# Add prometheus instrumentator
Instrumentator().instrument(app).expose(app)

def setup_logging():
    """
    Configure logging for the application to output INFO-level logs to both the console and a file, and set the "pika" logger to WARNING level.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('devenviro_society.log')
        ]
    )
    logging.getLogger("pika").setLevel(logging.WARNING)


def check_environment_variables():
    """
    Check for required environment variables and provide helpful error messages if missing.
    
    Returns:
        tuple: (is_valid: bool, missing_vars: list, suggestions: list)
    """
    required_vars = {
        # Database connection
        'POSTGRES_DB': 'Database name (e.g., devenviro_db)',
        'POSTGRES_USER': 'Database username (e.g., postgres)',
        'POSTGRES_PASSWORD': 'Database password',

        # Message queue
        'RABBITMQ_USER': 'RabbitMQ username (e.g., myuser)',
        'RABBITMQ_PASSWORD': 'RabbitMQ password',
    }

    missing_vars = []
    suggestions = []

    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(var)
            suggestions.append(f"  {var}={description}")

    return len(missing_vars) == 0, missing_vars, suggestions


def create_env_template():
    """
    Create a .env.template file with all required environment variables.
    """
    template_content = """# DevEnviro Environment Variables Template
    
# Copy this file to .env and fill in your values

# Database Configuration
POSTGRES_DB=devenviro_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# RabbitMQ Configuration  
RABBITMQ_USER=myuser
RABBITMQ_PASSWORD=mypassword
RABBITMQ_HOST=rabbitmq

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# API Keys (Optional - for LLM integrations)
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Observability (Optional)
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
JAEGER_ENDPOINT=http://jaeger:14268/api/traces
OTLP_ENDPOINT=http://jaeger:4317

# Agent Tokens (Auto-generated if not provided)
AGENT_ORCHESTRATOR_TOKEN=supersecrettoken_orchestrator
AGENT_BACKEND_SPECIALIST_TOKEN=supersecrettoken_backend
AGENT_DEVOPS_ENGINEER_TOKEN=supersecrettoken_devops
AGENT_FRONTEND_SPECIALIST_TOKEN=supersecrettoken_frontend
AGENT_QA_ENGINEER_TOKEN=supersecrettoken_qa
AGENT_SECURITY_ENGINEER_TOKEN=supersecrettoken_security
"""

    template_path = project_root / ".env.template"
    if not template_path.exists():
        template_path.write_text(template_content)
        return str(template_path)
    return None

@app.on_event("startup")
async def startup_event():
    """
    Gracefully handles startup initialization for the DevEnviro FastAPI application.
    
    This startup handler checks for required environment variables, creates helpful
    templates and error messages if configuration is missing, and only proceeds
    with full initialization if all requirements are met.
    """
    setup_logging()
    logger = logging.getLogger("DevEnviro")
    logger.info("🚀 Awakening the Society of Agents...")

    global initialization_status

    # Check if .env file exists and environment variables are set
    env_file_path = project_root / ".env"
    env_valid, missing_vars, suggestions = check_environment_variables()

    if not env_valid:
        logger.warning("⚠️ Required environment variables are missing")
        logger.warning(f"Missing variables: {', '.join(missing_vars)}")

        # Create .env.template if it doesn't exist
        template_created = create_env_template()
        if template_created:
            logger.info(f"📋 Created .env.template at: {template_created}")

        # Set graceful degradation status
        initialization_status["error"] = {
            "type": "missing_environment_variables",
            "message": f"Missing required environment variables: {', '.join(missing_vars)}",
            "missing_variables": missing_vars,
            "suggestions": suggestions,
            "env_file_exists": env_file_path.exists(),
            "template_path": str(project_root / ".env.template") if template_created else None
        }

        logger.warning("🔧 System running in degraded mode - configuration required")
        logger.info("📖 Please check the API status at /health for detailed setup instructions")
        return

    # Environment is valid, proceed with full initialization
    logger.info("✅ Environment configuration validated")

    try:
        # Initialize observability system
        logger.info("🔍 Initializing observability stack...")
        if observability.initialize_observability():
            logger.info("✅ OpenTelemetry telemetry initialized")
            initialization_status["services"]["observability"] = True
            # Instrument FastAPI after OpenTelemetry is set up
            FastAPIInstrumentor.instrument_app(app)
        else:
            logger.warning("⚠️ OpenTelemetry initialization failed - running without telemetry")

        logger.info("🔍 LLM observability configured within main observability system")

        # Database initialization
        logger.info("🗄️ Applying database migrations...")
        apply_migrations()
        initialization_status["services"]["database"] = True
        logger.info("✅ Database migrations completed")

        # Initialize core services
        logger.info("⚙️ Initializing core services...")
        init_manager = EnhancedInitializationManager(project_root=project_root)
        seed_knowledge_documents()
        init_manager.initialize_all_services()
        initialization_status["services"]["agents"] = True
        initialization_status["services"]["communication"] = True
        logger.info("✅ Core services initialized")

        # Initialize orchestrator
        comm_manager = init_manager.get_communications_manager()
        agent_registry = init_manager.get_agent_registry()

        logger.info("🎭 Initializing the Orchestrator...")
        orchestrator = Orchestrator()
        orchestrator.initialize_orchestrator(comm_manager, agent_registry)

        if orchestrator:
            initialization_status["initialized"] = True
            logger.info("🎉 Orchestrator initialized successfully. System is fully operational.")
            logger.info("🌐 API documentation available at: http://localhost:8090/docs")
        else:
            raise Exception("Failed to initialize the Orchestrator")

    except Exception as e:
        logger.critical(f"💥 Critical error during initialization: {e}", exc_info=True)
        initialization_status["error"] = {
            "type": "initialization_failure", 
            "message": str(e),
            "services_status": initialization_status["services"]
        }
        logger.warning("🔧 System running in degraded mode due to initialization failure")

@app.get("/")
async def root():
    """
    Handle the root GET endpoint and return a status message indicating the API is running.
    
    Returns:
        dict: A JSON object with a message confirming the API status.
    """
    global initialization_status

    if initialization_status["initialized"]:
        return {
            "message": "🎉 DevEnviro Society of Agents API is fully operational",
            "status": "operational",
            "services": initialization_status["services"],
            "docs": "/docs",
            "health": "/health"
        }
    elif initialization_status["error"]:
        return JSONResponse(
            status_code=503,
            content={
                "message": "⚠️ DevEnviro API is running in degraded mode",
                "status": "degraded", 
                "error": initialization_status["error"]["type"],
                "health": "/health"
            }
        )
    else:
        return {
            "message": "🚀 DevEnviro API is starting up...",
            "status": "starting",
            "health": "/health"
        }


@app.get("/health")
async def health_check():
    """
    Detailed health check endpoint that provides configuration guidance when needed.
    
    Returns:
        dict: Comprehensive system status and setup instructions.
    """
    global initialization_status

    if initialization_status["initialized"]:
        return {
            "status": "healthy",
            "message": "🎉 All systems operational",
            "services": initialization_status["services"],
            "uptime": "System running normally",
            "endpoints": {
                "api_docs": "/docs",
                "metrics": "/metrics"
            }
        }

    elif initialization_status["error"]:
        error_info = initialization_status["error"]

        if error_info["type"] == "missing_environment_variables":
            response_content = {
                "status": "configuration_required",
                "message": "🔧 System requires configuration to start",
                "error": error_info["message"],
                "missing_variables": error_info["missing_variables"],
                "setup_instructions": {
                    "step_1": "Create a .env file in your project root",
                    "step_2": f"Copy variables from .env.template (created at: {error_info.get('template_path', 'N/A')})",
                    "step_3": "Fill in your actual values for database and RabbitMQ credentials",
                    "step_4": "Restart the application"
                },
                "required_variables": error_info["suggestions"],
                "template_available": error_info.get("template_path") is not None
            }
        else:
            response_content = {
                "status": "initialization_failed",
                "message": "💥 System failed to initialize properly",
                "error": error_info["message"],
                "services_status": error_info.get("services_status", {}),
                "recommendation": "Check logs for detailed error information"
            }

        return JSONResponse(
            status_code=503,
            content=response_content
        )

    return {
        "status": "starting",
        "message": "🚀 System initialization in progress...",
        "services": initialization_status["services"]
    }
```
