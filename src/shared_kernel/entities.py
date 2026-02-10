from typing import TypeVar


EntityType = TypeVar("EntityType", bound="Entity")


class Entity:
    """Base entity model"""

    pass


class AggregateRoot(Entity):
    """
    An entry point of aggregate.
    """

    pass
