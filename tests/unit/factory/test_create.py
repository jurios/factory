from types import SimpleNamespace
from unittest.mock import patch

from tests.unit.fixtures.factories.profile import ProfileFactory
from tests.unit.fixtures.factories.user import UserFactory


class TestCreate:
    def test_persists_single_object(self, session):
        user = UserFactory().create(session)

        session.add.assert_called_once_with(user)
        session.commit.assert_called_once()
        session.refresh.assert_called_once_with(user)

    def test_persists_collection(self, session):
        users = UserFactory().create(session, count=3)

        session.add_all.assert_called_once_with(users)
        session.commit.assert_called_once()
        assert session.refresh.call_count == 3

    def test_resolves_callback(self, session):
        profile = ProfileFactory().create(session)

        assert profile.token == "fixed-token"

    def test_passes_session_to_callback(self, session):

        with patch(
            "tests.unit.fixtures.factories.profile.UserFactory"
        ) as mock_user_factory:
            mock_user_factory.return_value.create.return_value = SimpleNamespace(id=123)
            ProfileFactory().create(session)

        mock_user_factory.return_value.create.assert_called_once_with(session)

    def test_override_beats_callback(self, session):
        profile = ProfileFactory().with_attributes(token="manual").create(session)

        assert profile.token == "manual"
