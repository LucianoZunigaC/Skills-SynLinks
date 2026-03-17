from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

Entity = TypeVar("Entity")
ID = TypeVar("ID")


class BaseRepository(ABC, Generic[Entity, ID]):
    """Base repository class defining standard CRUD operations.

    Generic type parameters:
        Entity: The model/entity type this repository handles
        ID: The key/ID type used to identify entities
    """

    @abstractmethod
    def create(self, entity: Entity) -> Entity:
        """Create a new entity.

        Args:
            entity: The entity instance to create

        Returns:
            The created entity instance
        """
        pass

    @abstractmethod
    def delete(self, entity_id: ID) -> None:
        """Delete an entity by its ID.

        Args:
            entity_id: The ID of the entity to delete
        """
        pass

    @abstractmethod
    def get(self, entity_id: ID) -> Optional[Entity]:
        """Retrieve an entity by its ID.

        Args:
            entity_id: The ID of the entity to retrieve

        Returns:
            The entity instance if found, None otherwise
        """
        pass

    @abstractmethod
    def list(self, page_size: int = 50, offset: int = 0) -> List[Entity]:
        """Retrieve a paginated list of entities.

        Args:
            page_size: Maximum number of items to return (default: 50). 
                      A smaller default helps with performance and memory usage.
            offset: Starting offset for pagination (default: 0)

        Returns:
            List of entity instances
        """
        pass

    @abstractmethod
    def update(self, entity_id: ID, updated_entity: Entity) -> Entity:
        """Update an existing entity.

        Args:
            entity_id: The ID of the entity to update
            updated_entity: The updated entity instance

        Returns:
            The updated entity instance
        """
        pass
