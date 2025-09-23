"""Interfaces for different storage types used in the ApexSigma ecosystem."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class CacheStorage(ABC):
    """Abstract base class for a cache storage system."""

    @abstractmethod
    def get(self, key: str) -> Any:
        """Retrieves an item from the cache.

        Args:
            key: The key of the item to retrieve.

        Returns:
            The cached item, or None if the item is not found.
        """
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Stores an item in the cache.

        Args:
            key: The key to store the item under.
            value: The item to store.
            ttl: The time-to-live for the item in seconds.
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Deletes an item from the cache.

        Args:
            key: The key of the item to delete.
        """
        pass

class PersistentStorage(ABC):
    """Abstract base class for a persistent storage system."""

    @abstractmethod
    def get(self, id: str) -> Dict:
        """Retrieves an item from persistent storage.

        Args:
            id: The ID of the item to retrieve.

        Returns:
            The retrieved item as a dictionary.
        """
        pass

    @abstractmethod
    def save(self, data: Dict) -> str:
        """Saves an item to persistent storage.

        Args:
            data: The item to save, as a dictionary.

        Returns:
            The ID of the saved item.
        """
        pass

    @abstractmethod
    def update(self, id: str, data: Dict) -> None:
        """Updates an item in persistent storage.

        Args:
            id: The ID of the item to update.
            data: The new data for the item.
        """
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        """Deletes an item from persistent storage.

        Args:
            id: The ID of the item to delete.
        """
        pass

class VectorStorage(ABC):
    """Abstract base class for a vector storage system."""

    @abstractmethod
    def search(self, query_vector: List[float], top_k: int) -> List[Dict]:
        """Searches for similar vectors in the storage.

        Args:
            query_vector: The vector to search for.
            top_k: The number of similar vectors to return.

        Returns:
            A list of dictionaries, each representing a similar item.
        """
        pass

    @abstractmethod
    def upsert(self, vectors: List[Dict]) -> None:
        """Inserts or updates vectors in the storage.

        Args:
            vectors: A list of vectors to upsert. Each vector is a dictionary
                     containing the vector data and metadata.
        """
        pass

class GraphStorage(ABC):
    """Abstract base class for a graph database storage system."""

    @abstractmethod
    def execute_query(self, query: str, params: Optional[Dict] = None) -> Any:
        """Executes a query against the graph database.

        Args:
            query: The query to execute (e.g., Cypher, Gremlin).
            params: Optional parameters for the query.

        Returns:
            The result of the query.
        """
        pass
