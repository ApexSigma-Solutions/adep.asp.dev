#!/usr/bin/env python3
"""
End-to-End Distributed Tracing Setup for ApexSigma Ecosystem

This script configures distributed tracing across all ApexSigma services:
- devenviro.as (orchestrator)
- memos.as (memory service)
- InGest-LLM.as (data ingestion)
- tools.as (tool registry)

Features:
- Cross-service trace propagation
- Request correlation IDs
- Service dependency mapping
- Performance bottleneck identification
- Error propagation tracking
"""

import os
import json
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from contextlib import contextmanager

# OpenTelemetry imports
from opentelemetry import trace, propagate, baggage
from opentelemetry.sdk.trace import TracerProvider, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.propagators.jaeger import JaegerPropagator
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


@dataclass
class ServiceConfig:
    """Configuration for a service in the ApexSigma ecosystem."""
    name: str
    version: str
    base_url: str
    health_endpoint: str
    metrics_endpoint: str
    service_type: str


class E2ETracingManager:
    """
    Manages end-to-end distributed tracing across ApexSigma services.
    """
    
    # Service configurations
    SERVICES = {
        "devenviro": ServiceConfig(
            name="devenviro-as",
            version="1.0.0",
            base_url="http://localhost:8090",
            health_endpoint="/health",
            metrics_endpoint="/metrics",
            service_type="orchestrator"
        ),
        "memos": ServiceConfig(
            name="memos-as", 
            version="1.0.0",
            base_url="http://localhost:8091",
            health_endpoint="/health",
            metrics_endpoint="/metrics",
            service_type="memory"
        ),
        "ingest": ServiceConfig(
            name="ingest-llm-as",
            version="1.0.0", 
            base_url="http://localhost:8000",
            health_endpoint="/health",
            metrics_endpoint="/metrics",
            service_type="ingestion"
        ),
        "tools": ServiceConfig(
            name="tools-as",
            version="0.2.0",
            base_url="http://localhost:8092", 
            health_endpoint="/health",
            metrics_endpoint="/metrics",
            service_type="tools"
        )
    }
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.service_config = None
        
        # Find service config
        for key, config in self.SERVICES.items():
            if config.name == service_name or key == service_name:
                self.service_config = config
                break
        
        if not self.service_config:
            raise ValueError(f"Unknown service: {service_name}")
        
        self.setup_tracing()
        
    def setup_tracing(self):
        """Initialize OpenTelemetry distributed tracing."""
        
        # Create resource with service information
        resource = Resource.create({
            "service.name": self.service_config.name,
            "service.version": self.service_config.version,
            "service.type": self.service_config.service_type,
            "deployment.environment": os.getenv("DEPLOYMENT_ENV", "development"),
            "ecosystem": "apexsigma"
        })
        
        # Set up tracer provider
        tracer_provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(tracer_provider)
        
        # Configure Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name=os.getenv("JAEGER_AGENT_HOST", "localhost"),
            agent_port=int(os.getenv("JAEGER_AGENT_PORT", 14268)),
        )
        
        # Add batch span processor
        span_processor = BatchSpanProcessor(jaeger_exporter)
        tracer_provider.add_span_processor(span_processor)
        
        # Set up propagators for cross-service context
        propagate.set_global_textmap(
            CompositePropagator([
                TraceContextTextMapPropagator(),
                B3MultiFormat(),
                JaegerPropagator(),
            ])
        )
        
        # Instrument HTTP clients
        RequestsInstrumentor().instrument()
        HTTPXClientInstrumentor().instrument()
        
        self.tracer = trace.get_tracer(self.service_config.name)
        
        print(f"✅ E2E tracing initialized for {self.service_config.name}")
    
    @contextmanager 
    def start_operation(self, operation_name: str, **attributes):
        """Start a traced operation with service context."""
        with self.tracer.start_as_current_span(operation_name) as span:
            # Add service context
            span.set_attributes({
                "service.name": self.service_config.name,
                "service.type": self.service_config.service_type,
                "operation.name": operation_name,
                **attributes
            })
            
            yield span
    
    def create_cross_service_headers(self) -> Dict[str, str]:
        """Create HTTP headers for cross-service trace propagation."""
        headers = {}
        propagate.inject(headers)
        
        # Add custom ApexSigma correlation headers
        headers.update({
            "X-ApexSigma-Service": self.service_config.name,
            "X-ApexSigma-Version": self.service_config.version,
            "X-ApexSigma-Correlation-ID": self.get_correlation_id()
        })
        
        return headers
    
    def extract_cross_service_context(self, headers: Dict[str, str]):
        """Extract trace context from incoming HTTP headers."""
        context = propagate.extract(headers)
        return context
    
    def get_correlation_id(self) -> str:
        """Get the current trace correlation ID."""
        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            return f"{span_context.trace_id:032x}"
        return f"no-trace-{int(time.time())}"
    
    @contextmanager
    def trace_service_call(self, target_service: str, operation: str, **metadata):
        """Trace a call to another ApexSigma service."""
        target_config = self.SERVICES.get(target_service)
        if not target_config:
            target_config = ServiceConfig(
                name=target_service,
                version="unknown",
                base_url="unknown",
                health_endpoint="/health", 
                metrics_endpoint="/metrics",
                service_type="unknown"
            )
        
        with self.start_operation(f"call_{target_service}_{operation}") as span:
            span.set_attributes({
                "target.service": target_config.name,
                "target.service_type": target_config.service_type,
                "target.operation": operation,
                "call.type": "inter_service",
                **metadata
            })
            
            yield span
    
    def trace_workflow(self, workflow_id: str, workflow_type: str):
        """Create a workflow-level trace span."""
        return self.start_operation(f"workflow_{workflow_type}", 
                                   workflow_id=workflow_id,
                                   workflow_type=workflow_type)
    
    def trace_agent_delegation(self, agent_id: str, agent_type: str, task_type: str):
        """Trace agent task delegation."""
        return self.start_operation(f"delegate_{agent_type}",
                                   agent_id=agent_id,
                                   agent_type=agent_type, 
                                   task_type=task_type)
    
    def get_service_map(self) -> Dict[str, Any]:
        """Generate a service dependency map."""
        return {
            "services": {
                name: {
                    "name": config.name,
                    "type": config.service_type,
                    "version": config.version,
                    "endpoints": {
                        "base": config.base_url,
                        "health": config.health_endpoint,
                        "metrics": config.metrics_endpoint
                    }
                }
                for name, config in self.SERVICES.items()
            },
            "dependencies": {
                "devenviro": ["memos", "ingest", "tools"],  # Orchestrator calls all services
                "memos": [],                                # Memory service is leaf
                "ingest": ["memos"],                        # Ingestion stores to memory
                "tools": []                                 # Tools service is leaf
            },
            "flow_patterns": {
                "user_request": ["devenviro", "memos", "tools"],
                "data_ingestion": ["ingest", "memos"],
                "agent_workflow": ["devenviro", "tools", "memos"],
                "memory_query": ["devenviro", "memos"]
            }
        }


def create_e2e_tracing_config():
    """Create configuration files for E2E tracing setup."""
    
    config = {
        "tracing": {
            "enabled": True,
            "service_name_detection": "auto",
            "propagators": ["tracecontext", "b3multi", "jaeger"],
            "exporters": {
                "jaeger": {
                    "endpoint": "http://localhost:14268/api/traces",
                    "agent_host": "localhost", 
                    "agent_port": 14268
                },
                "otlp": {
                    "endpoint": "http://localhost:4317",
                    "headers": {}
                }
            }
        },
        "correlation": {
            "header_name": "X-ApexSigma-Correlation-ID",
            "baggage_enabled": True,
            "custom_headers": [
                "X-ApexSigma-Service",
                "X-ApexSigma-Version", 
                "X-ApexSigma-User-ID",
                "X-ApexSigma-Session-ID"
            ]
        },
        "sampling": {
            "default_rate": 1.0,  # 100% sampling for development
            "service_rates": {
                "devenviro-as": 1.0,
                "memos-as": 1.0,
                "ingest-llm-as": 1.0,
                "tools-as": 1.0
            }
        }
    }
    
    return config


def setup_service_instrumentation(service_name: str):
    """Set up instrumentation for a specific service."""
    
    manager = E2ETracingManager(service_name)
    
    # Create service-specific configuration
    service_config = {
        "service": service_name,
        "tracing": manager.get_service_map(),
        "configuration": create_e2e_tracing_config()
    }
    
    return manager, service_config


def demonstrate_e2e_tracing():
    """Demonstrate E2E tracing across services."""
    
    print("🚀 Setting up E2E Distributed Tracing Demo")
    print("=" * 50)
    
    # Initialize tracing for DevEnviro (orchestrator)
    orchestrator_manager = E2ETracingManager("devenviro-as")
    
    # Simulate a cross-service workflow
    with orchestrator_manager.trace_workflow("workflow-001", "user_task") as workflow_span:
        print("📋 Starting workflow: user_task")
        
        # Step 1: Call tools service for search
        with orchestrator_manager.trace_service_call("tools", "web_search", 
                                                    query="machine learning") as tools_span:
            print("🔍 Calling tools.as for web search")
            headers = orchestrator_manager.create_cross_service_headers()
            print(f"   Headers: {list(headers.keys())}")
            
            # Simulate processing time
            time.sleep(0.1)
            
        # Step 2: Call memos service to store results
        with orchestrator_manager.trace_service_call("memos", "store_memory",
                                                    content_type="search_results") as memos_span:
            print("💾 Calling memos.as to store search results")
            time.sleep(0.05)
            
        # Step 3: Delegate to agent
        with orchestrator_manager.trace_agent_delegation("agent-001", "backend-specialist", 
                                                        "analyze_results") as agent_span:
            print("🤖 Delegating analysis to backend-specialist agent")
            time.sleep(0.2)
    
    correlation_id = orchestrator_manager.get_correlation_id()
    print(f"\n✅ Workflow completed with correlation ID: {correlation_id}")
    
    # Generate service map
    service_map = orchestrator_manager.get_service_map()
    print(f"\n📊 Service Dependencies:")
    for service, deps in service_map["dependencies"].items():
        print(f"   {service} -> {deps if deps else 'none'}")
        
    return correlation_id


if __name__ == "__main__":
    print("ApexSigma E2E Distributed Tracing Setup")
    print("=" * 40)
    
    try:
        # Run demonstration
        correlation_id = demonstrate_e2e_tracing()
        
        print(f"\n🎯 Tracing demonstration completed!")
        print(f"🔍 View traces at: http://localhost:16686")
        print(f"📋 Search for correlation ID: {correlation_id}")
        print(f"📊 Check Grafana dashboards: http://localhost:3000")
        
    except Exception as e:
        print(f"❌ Error setting up E2E tracing: {e}")
        import traceback
        traceback.print_exc()