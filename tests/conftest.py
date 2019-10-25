import pytest
from faker import Factory as FakerFactory


@pytest.fixture(scope="session")
def faker():
    return FakerFactory.create(locale="en_GB")
