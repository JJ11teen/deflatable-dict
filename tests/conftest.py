from typing import DefaultDict

import pytest


@pytest.fixture()
def nested_dict():
    return {
        "a": {
            "1": False,
            "2": {
                "a": 1,
                "b": 2,
                "c": {
                    "1": "3",
                    "2": b"4",
                },
                "d": {
                    "1": 1.0,
                    "2": 2.0,
                },
            },
        },
        "b": [-1, -2],
    }


@pytest.fixture()
def flat_period_delimited_dict():
    return {
        "a.1": False,
        "a.2.a": 1,
        "a.2.b": 2,
        "a.2.c.1": "3",
        "a.2.c.2": b"4",
        "a.2.d.1": 1.0,
        "a.2.d.2": 2.0,
        "b": [-1, -2],
    }


@pytest.fixture()
def flat_slash_delimited_dict():
    return {
        "a/1": False,
        "a/2/a": 1,
        "a/2/b": 2,
        "a/2/c/1": "3",
        "a/2/c/2": b"4",
        "a/2/d/1": 1.0,
        "a/2/d/2": 2.0,
        "b": [-1, -2],
    }


def pytest_generate_tests(metafunc):
    if "d" in metafunc.fixturenames:
        metafunc.parametrize(
            "d",
            [{}, DefaultDict()],
        )
