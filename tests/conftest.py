import pytest


@pytest.fixture()
def flat_dict():
    return {"a": False, "b": 1, "c": 2, "d": "3", "e": b"4"}


@pytest.fixture()
def flat_deliminated_dict():
    return {"a.a": False, "a.b.a": 1, "a.b.b": 2, "a.b.c.a": "3", "a.b.c.b": b"4"}


@pytest.fixture()
def nested_dict():
    return {"a": {"a": False, "b": {"a": 1, "b": 2, "c": {"a": "3", "b": b"4"}}}}
