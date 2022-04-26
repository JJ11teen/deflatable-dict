import pytest

from deflatabledict import DeflatableDict


def test_lists_flatten(nested_dict):
    dd = DeflatableDict(nested_dict, delimiter=".")

    assert dd["b"] == [-1, -2]
    assert dd["b.[0]"] == -1
    assert dd["b.[1]"] == -2
