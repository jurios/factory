from tests.unit.fixtures.factories.user import UserFactory


class TestOnly:
    def test_returns_only_requested_fields(self):
        data = UserFactory().only("name", "email")

        assert set(data) == {"name", "email"}

    def test_count_returns_list_of_projections(self):
        rows = UserFactory().only("name", count=2)

        assert len(rows) == 2
        assert all(set(row) == {"name"} for row in rows)

    def test_applies_overrides(self):
        data = UserFactory().with_attributes(name="Edsger").only("name")

        assert data == {"name": "Edsger"}
