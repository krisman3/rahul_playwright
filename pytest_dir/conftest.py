import pytest

@pytest.fixture(scope="session")
def pre_work():
    print("I setup browser instance.")