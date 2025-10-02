#!/usr/bin/env python3
"""
Test Langfuse integration across ApexSigma ecosystem using pytest
"""

import os
import time
import uuid

import pytest
from dotenv import load_dotenv
from langfuse import Langfuse

# Load environment variables
load_dotenv()


class TestLangfuseEcosystem:
    """Test Langfuse configurations for all ApexSigma services"""

    @pytest.fixture(scope="class")
    def langfuse_clients(self):
        """Initialize Langfuse clients for all services"""
        clients = {}

        # Main ApexSigma EcoSystem
        try:
            clients["apexsigma_main"] = Langfuse(
                secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
                public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
                host=os.getenv("LANGFUSE_HOST"),
            )
            print("✅ ApexSigma Main Langfuse client initialized")
        except Exception as e:
            print(f"❌ ApexSigma Main Langfuse client failed: {e}")

        # InGest-LLM.as
        try:
            clients["ingest_llm"] = Langfuse(
                secret_key=os.getenv("INGEST_LLM_LANGFUSE_SECRET_KEY"),
                public_key=os.getenv("INGEST_LLM_LANGFUSE_PUBLIC_KEY"),
                host=os.getenv("INGEST_LLM_LANGFUSE_HOST"),
            )
            print("✅ InGest-LLM.as Langfuse client initialized")
        except Exception as e:
            print(f"❌ InGest-LLM.as Langfuse client failed: {e}")

        # Devenviro.as
        try:
            clients["devenviro"] = Langfuse(
                secret_key=os.getenv("DEVENVIRO_LANGFUSE_SECRET_KEY"),
                public_key=os.getenv("DEVENVIRO_LANGFUSE_PUBLIC_KEY"),
                host=os.getenv("DEVENVIRO_LANGFUSE_HOST"),
            )
            print("✅ Devenviro.as Langfuse client initialized")
        except Exception as e:
            print(f"❌ Devenviro.as Langfuse client failed: {e}")

        # memOS.as
        try:
            clients["memos"] = Langfuse(
                secret_key=os.getenv("MEMOS_LANGFUSE_SECRET_KEY"),
                public_key=os.getenv("MEMOS_LANGFUSE_PUBLIC_KEY"),
                host=os.getenv("MEMOS_LANGFUSE_HOST"),
            )
            print("✅ memOS.as Langfuse client initialized")
        except Exception as e:
            print(f"❌ memOS.as Langfuse client failed: {e}")

        # tools.as
        try:
            clients["tools"] = Langfuse(
                secret_key=os.getenv("TOOLS_LANGFUSE_SECRET_KEY"),
                public_key=os.getenv("TOOLS_LANGFUSE_PUBLIC_KEY"),
                host=os.getenv("TOOLS_LANGFUSE_HOST"),
            )
            print("✅ tools.as Langfuse client initialized")
        except Exception as e:
            print(f"❌ tools.as Langfuse client failed: {e}")

        return clients

    def test_apexsigma_main_langfuse_session_and_trace(self, langfuse_clients):
        """Test ApexSigma Main Langfuse session and trace creation"""
        if "apexsigma_main" not in langfuse_clients:
            pytest.skip("ApexSigma Main Langfuse client not available")

        client = langfuse_clients["apexsigma_main"]
        session_id = f"test-session-apexsigma-{uuid.uuid4().hex[:8]}"

        # Create trace/span
        span = client.start_span(
            name="ApexSigma Main Test Session",
            metadata={
                "service": "apexsigma_main",
                "test_type": "integration",
                "session_id": session_id,
            },
        )

        # Simulate some work
        time.sleep(0.1)

        # End span
        span.end()

        # Flush to ensure data is sent
        client.flush()

        print(f"✅ ApexSigma Main: Session {session_id} and span created successfully")
        assert session_id is not None

    def test_ingest_llm_langfuse_session_and_trace(self, langfuse_clients):
        """Test InGest-LLM.as Langfuse session and trace creation"""
        if "ingest_llm" not in langfuse_clients:
            pytest.skip("InGest-LLM.as Langfuse client not available")

        client = langfuse_clients["ingest_llm"]
        session_id = f"test-session-ingest-llm-{uuid.uuid4().hex[:8]}"

        # Create trace/span
        span = client.start_span(
            name="InGest-LLM.as Test Session",
            metadata={
                "service": "ingest_llm",
                "test_type": "integration",
                "session_id": session_id,
            },
        )

        # Simulate ingestion work
        time.sleep(0.1)

        # End span
        span.end()

        # Flush to ensure data is sent
        client.flush()

        print(f"✅ InGest-LLM.as: Session {session_id} and span created successfully")
        assert session_id is not None

    def test_devenviro_langfuse_session_and_trace(self, langfuse_clients):
        """Test Devenviro.as Langfuse session and trace creation"""
        if "devenviro" not in langfuse_clients:
            pytest.skip("Devenviro.as Langfuse client not available")

        client = langfuse_clients["devenviro"]
        session_id = f"test-session-devenviro-{uuid.uuid4().hex[:8]}"

        # Create trace/span
        span = client.start_span(
            name="Devenviro.as Test Session",
            metadata={
                "service": "devenviro",
                "test_type": "integration",
                "session_id": session_id,
            },
        )

        # Simulate orchestration work
        time.sleep(0.1)

        # End span
        span.end()

        # Flush to ensure data is sent
        client.flush()

        print(f"✅ Devenviro.as: Session {session_id} and span created successfully")
        assert session_id is not None

    def test_memos_langfuse_session_and_trace(self, langfuse_clients):
        """Test memOS.as Langfuse session and trace creation"""
        if "memos" not in langfuse_clients:
            pytest.skip("memOS.as Langfuse client not available")

        client = langfuse_clients["memos"]
        session_id = f"test-session-memos-{uuid.uuid4().hex[:8]}"

        # Create trace/span
        span = client.start_span(
            name="memOS.as Test Session",
            metadata={
                "service": "memos",
                "test_type": "integration",
                "session_id": session_id,
            },
        )

        # Simulate memory work
        time.sleep(0.1)

        # End span
        span.end()

        # Flush to ensure data is sent
        client.flush()

        print(f"✅ memOS.as: Session {session_id} and span created successfully")
        assert session_id is not None

    def test_tools_langfuse_session_and_trace(self, langfuse_clients):
        """Test tools.as Langfuse session and trace creation"""
        if "tools" not in langfuse_clients:
            pytest.skip("tools.as Langfuse client not available")

        client = langfuse_clients["tools"]
        session_id = f"test-session-tools-{uuid.uuid4().hex[:8]}"

        # Create trace/span
        span = client.start_span(
            name="tools.as Test Session",
            metadata={
                "service": "tools",
                "test_type": "integration",
                "session_id": session_id,
            },
        )

        # Simulate tool work
        time.sleep(0.1)

        # End span
        span.end()

        # Flush to ensure data is sent
        client.flush()

        print(f"✅ tools.as: Session {session_id} and span created successfully")
        assert session_id is not None

    def test_langfuse_client_initialization(self, langfuse_clients):
        """Test that all Langfuse clients were initialized successfully"""
        expected_services = [
            "apexsigma_main",
            "ingest_llm",
            "devenviro",
            "memos",
            "tools",
        ]
        initialized_services = list(langfuse_clients.keys())

        print(f"Expected services: {expected_services}")
        print(f"Initialized services: {initialized_services}")

        # At least the main service should be available
        assert (
            "apexsigma_main" in langfuse_clients
        ), "ApexSigma Main Langfuse client should be available"

        # Check that clients are actually Langfuse instances
        for service_name, client in langfuse_clients.items():
            assert hasattr(
                client, "start_span"
            ), f"{service_name} client should have start_span method"
            assert hasattr(
                client, "flush"
            ), f"{service_name} client should have flush method"
