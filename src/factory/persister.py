from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Persister(Protocol):
    """Structural interface for anything able to persist model instances.

    Any object exposing these four methods satisfies the protocol, so both
    ``sqlmodel.Session`` and ``sqlalchemy.orm.Session`` (and any compatible
    Unit of Work) work without the factory depending on a concrete ORM.
    """

    def add(self, instance: Any) -> Any: ...

    def add_all(self, instances: Any) -> Any: ...

    def commit(self) -> Any: ...

    def refresh(self, instance: Any) -> Any: ...
