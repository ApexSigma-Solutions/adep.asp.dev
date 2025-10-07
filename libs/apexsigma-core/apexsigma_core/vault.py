"""
HashiCorp Vault client for ApexSigma ecosystem.
Provides secure secrets management across all services.
"""

import os
import logging
from typing import Optional, Dict, Any
from functools import lru_cache

import hvac

logger = logging.getLogger(__name__)


class VaultClient:
    """HashiCorp Vault client for secrets management."""

    def __init__(
        self,
        url: str = None,
        token: Optional[str] = None,
        mount_point: str = "secret"
    ):
        """
        Initialize Vault client.

        Args:
            url: Vault server URL (auto-detected based on environment)
            token: Vault authentication token
            mount_point: KV mount point (default: secret)
        """
        # Auto-detect URL based on environment
        if url is None:
            # If running inside Docker network, use container name
            # If running on host, use localhost
            import socket
            try:
                # Try to resolve container name (works inside Docker network)
                socket.gethostbyname('apexsigma_vault')
                url = "http://apexsigma_vault:8200"
            except socket.gaierror:
                # Fallback to localhost (works on host machine)
                url = "http://localhost:8200"

        self.url = url
        self.token = token or os.getenv("VAULT_TOKEN") or "apexsigma-root-token-2025"
        self.mount_point = mount_point
        self._client: Optional[hvac.Client] = None

    @property
    def client(self) -> hvac.Client:
        """Lazy-loaded Vault client."""
        if self._client is None:
            self._client = hvac.Client(url=self.url, token=self.token)
        return self._client

    def is_authenticated(self) -> bool:
        """Check if client is authenticated with Vault."""
        try:
            return self.client.is_authenticated()
        except Exception as e:
            logger.warning(f"Vault authentication check failed: {e}")
            return False

    def get_secret(self, path: str, key: str) -> Optional[str]:
        """
        Retrieve a specific secret value from Vault.

        Args:
            path: Secret path
            key: Secret key

        Returns:
            Secret value or None if not found
        """
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point=self.mount_point
            )
            data = response['data']['data']
            return data.get(key)
        except Exception as e:
            logger.warning(f"Failed to retrieve secret {path}/{key}: {e}")
            return None

    def set_secret(self, path: str, data: Dict[str, Any]) -> bool:
        """
        Store a secret in Vault.

        Args:
            path: Secret path
            data: Secret data dictionary

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=data,
                mount_point=self.mount_point
            )
            logger.info(f"Successfully stored secret at {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to store secret at {path}: {e}")
            return False


@lru_cache(maxsize=1)
def get_vault_client() -> VaultClient:
    """Get singleton Vault client instance."""
    return VaultClient()


def get_secret(path: str, key: str) -> Optional[str]:
    """
    Convenience function to retrieve a secret from Vault.

    Args:
        path: Secret path
        key: Secret key

    Returns:
        Secret value
    """
    client = get_vault_client()
    return client.get_secret(path, key)


def set_secret(path: str, data: Dict[str, Any]) -> bool:
    """
    Convenience function to store a secret in Vault.

    Args:
        path: Secret path
        data: Secret data

    Returns:
        True if successful
    """
    client = get_vault_client()
    return client.set_secret(path, data)