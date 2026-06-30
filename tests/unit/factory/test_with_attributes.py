"""`with_attributes()`: API inmutable que deriva nuevas factories."""

from tests.unit.fixtures.factories.user import UserFactory


class TestWithAttributes:
    def test_merges_keys(self):
        user = (
            UserFactory()
            .with_attributes(name="Grace")
            .with_attributes(email="grace@navy.mil")
            .make()
        )

        assert user.name == "Grace"
        assert user.email == "grace@navy.mil"

    def test_last_write_wins_on_same_key(self):
        user = (
            UserFactory()
            .with_attributes(name="Grace")
            .with_attributes(name="Ada")
            .make()
        )

        assert user.name == "Ada"
