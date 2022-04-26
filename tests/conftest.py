import pytest

from deflatabledict.deflatable import DeflatableDict


def pytest_generate_tests(metafunc):
    if "d" in metafunc.fixturenames:
        metafunc.parametrize(
            "d",
            [
                {},
                DeflatableDict(_delimiter=".", _flatten_lists=False),
                DeflatableDict(_delimiter="/", _flatten_lists=False),
                DeflatableDict(_delimiter=".", _flatten_lists=True),
                DeflatableDict(_delimiter="/", _flatten_lists=True),
            ],
        )
