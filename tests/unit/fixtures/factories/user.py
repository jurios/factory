from typing import Any

from faker import Faker

from factory.factory import BaseFactory
from tests.unit.fixtures.models.user import User


class UserFactory(BaseFactory[User]):
    model = User

    @classmethod
    def defaults(cls, faker: Faker) -> dict[str, Any]:
        return {
            "name": faker.name(),
            "email": faker.email(),
            "age": faker.pyint(min_value=18, max_value=99),
        }
