import pytest
from faker import Faker

from factory.factory import BaseFactory


def test_defaults_must_be_overridden():
    with pytest.raises(NotImplementedError):
        BaseFactory.defaults(Faker())
