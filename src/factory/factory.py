from collections.abc import Callable
from inspect import signature
from typing import Any, TypeVar, overload

from faker import Faker
from sqlmodel import Session

faker = Faker()

Model = TypeVar("Model")


class BaseFactory[Model]:
    model: type[Model]
    faker: Faker

    def __init__(self, *, overrides: dict[str, Any] | None = None):
        self.faker = faker
        self._overrides = overrides or {}

    def with_attributes(self, **kwargs: Any) -> "BaseFactory[Model]":
        return self.__class__(
            overrides={**self._overrides, **kwargs},
        )

    @overload
    def make(self, count: None = None) -> Model: ...

    @overload
    def make(self, count: int) -> list[Model]: ...

    def make(self, count: int | None = None) -> Model | list[Model]:
        if count is None:
            return self._build_one(session=None, resolve_callbacks=False)

        return [
            self._build_one(session=None, resolve_callbacks=False) for _ in range(count)
        ]

    @overload
    def create(self, session: Session, count: None = None) -> Model: ...

    @overload
    def create(self, session: Session, *, count: int) -> list[Model]: ...

    def create(
        self,
        session: Session,
        *,
        count: int | None = None,
    ) -> Model | list[Model]:
        if count is None:
            objs = self._build_one(session=session, resolve_callbacks=True)
        else:
            objs = [
                self._build_one(session=session, resolve_callbacks=True)
                for _ in range(count)
            ]

        if isinstance(objs, list):
            session.add_all(objs)
            session.commit()

            for obj in objs:
                session.refresh(obj)

            return objs

        session.add(objs)
        session.commit()
        session.refresh(objs)

        return objs

    @overload
    def only(self, *fields: str) -> dict[str, Any]: ...

    @overload
    def only(self, *fields: str, count: int) -> list[dict[str, Any]]: ...

    def only(
        self,
        *fields: str,
        count: int | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        objs = self.make(count=count)

        if isinstance(objs, list):
            return [{field: getattr(obj, field) for field in fields} for obj in objs]

        return {field: getattr(objs, field) for field in fields}

    def _build_one(
        self,
        *,
        session: Session | None,
        resolve_callbacks: bool,
    ) -> Model:
        data = self.defaults(self.faker)

        for key, value in data.items():
            if callable(value):
                data[key] = (
                    self._resolve_callback(value, session)
                    if resolve_callbacks
                    else None
                )

        data.update(self._overrides)

        return self.model(**data)

    def _resolve_callback(
        self,
        callback: Callable[..., Any],
        session: Session | None,
    ) -> Any:
        params = signature(callback).parameters

        if len(params) == 0:
            return callback()

        return callback(session)

    @classmethod
    def defaults(cls, faker: Faker) -> dict[str, Any]:
        raise NotImplementedError
