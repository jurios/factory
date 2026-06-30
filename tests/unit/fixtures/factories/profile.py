from typing import Any

from faker import Faker

from factory.factory import BaseFactory
from tests.unit.fixtures.factories.user import UserFactory
from tests.unit.fixtures.models.profile import Profile


class ProfileFactory(BaseFactory[Profile]):
    model = Profile

    @classmethod
    def defaults(cls, faker: Faker) -> dict[str, Any]:
        return {
            "handle": faker.user_name(),
            "token": lambda: "fixed-token",
            "user_id": lambda session: UserFactory().create(session).id,
        }
