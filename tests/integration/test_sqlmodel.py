from collections.abc import Iterator
from typing import Any

import pytest
from faker import Faker
from sqlmodel import Field, Session, SQLModel, create_engine

from factory import BaseFactory, Persister


class Widget(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    sku: str


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
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestSqlModel:
    def test_sqlmodel_session_satisfies_persister(self, session: Session):
        # Structural typing: a real sqlmodel Session is a valid Persister.
        assert isinstance(session, Persister)

    def test_persists_single_object(self, session: Session):
        widget = WidgetFactory().create(session)

        assert widget.id is not None
        assert session.get(Widget, widget.id) is widget

    def test_persists_collection(self, session: Session):
        widgets = WidgetFactory().create(session, count=3)

        assert len(widgets) == 3
        assert all(w.id is not None for w in widgets)

    def test_make_does_not_touch_the_database(self, session: Session):
        widget = WidgetFactory().make()

        assert widget.id is None
