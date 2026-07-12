import pytest

from tests.unit.fixtures.factories.profile import ProfileFactory
from tests.unit.fixtures.factories.user import UserFactory
from tests.unit.fixtures.models.user import User


class TestMake:
    def test_without_count_returns_single_instance(self):
        result = UserFactory().make()

        assert isinstance(result, User)

    @pytest.mark.parametrize("count", [0, 3])
    def test_count_returns_list_of_given_length(self, count):
        result = UserFactory().make(count=count)

        assert isinstance(result, list)
        assert len(result) == count

    def test_callbacks_collapse_to_none(self):
        profile = ProfileFactory().make()

        assert profile.token is None

    def test_override_beats_default(self):
        user = UserFactory().with_attributes(name="Ada Lovelace").make()

        assert user.name == "Ada Lovelace"

    def test_override_beats_callback(self):
        # Un override estático debe ganar incluso a un campo definido como callback.
        profile = ProfileFactory().with_attributes(token="manual").make()

        assert profile.token == "manual"

    def test_callback_override_becomes_none(self):
        profile = ProfileFactory().with_attributes(token=lambda: "x").make()

        assert profile.token is None
