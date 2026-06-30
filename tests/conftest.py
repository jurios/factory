from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest
from faker import Faker
from sqlmodel import Session


@pytest.fixture(autouse=True)
def _seed_faker() -> None:
    Faker.seed(0)


@pytest.fixture
def session() -> Iterator[Session]:
    session = MagicMock()
    session.marker = "session"
    return session
