from collections.abc import Iterator
from typing import Any

import pytest
from faker import Faker
from sqlalchemy import String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
)

from factory import BaseFactory, Persister


class Base(DeclarativeBase):
    pass


class Widget(Base):
    __tablename__ = "widget"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    sku: Mapped[str] = mapped_column(String(120))


class WidgetFactory(BaseFactory[Widget]):
    model = Widget

    @classmethod
    def defaults(cls, faker: Faker) -> dict[str, Any]:
        return {
            "name": faker.word(),
            "sku": faker.bothify(text="???-#####"),
        }


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestSqlAlchemy:
    def test_sqlalchemy_session_satisfies_persister(self, session: Session):
        # Structural typing: a plain SQLAlchemy Session is a valid Persister.
        assert isinstance(session, Persister)

    def test_persists_single_object(self, session: Session):
        widget = WidgetFactory().create(session)

        assert widget.id is not None
        assert session.get(Widget, widget.id) is widget

    def test_persists_collection(self, session: Session):
        widgets = WidgetFactory().create(session, count=3)

        assert len(widgets) == 3
        assert all(a.id is not None for a in widgets)

    def test_make_does_not_touch_the_database(self, session: Session):
        widget = WidgetFactory().make()

        assert widget.id is None
