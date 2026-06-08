import pytest


@pytest.fixture(scope="function")
def pre_work():
    print("I setup browser instance.")


@pytest.fixture(scope="function")
def second_work():
    print("I setup second work instance.")
    yield
    print("tear down validation")


def test_initial_test(pre_work):
    print("This is first test")



def test_second_check(pre_work, second_work):
    print("This is second test.")