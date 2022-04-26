from typing import MutableMapping

import pytest


def test_dict_get_set(d: MutableMapping):
    d["a"] = 0
    d["b"] = "string"

    assert d["a"] == 0
    assert d["b"] == "string"


def test_dict_mixins(d: MutableMapping):
    assert len(d) == 0
    assert "a" not in d

    d.update({"a": 0, "b": 1.0})
    d["c"] = "string"

    assert "a" in d

    del d["b"]
    assert len(d) == 2


def test_dict_errors(d: MutableMapping):
    with pytest.raises(KeyError):
        d["a"]

    with pytest.raises(KeyError):
        del d["b"]


def test_dict_iter(d: MutableMapping):
    standard_dict = {"a": False, "b": 1, "c": 2, "d": "3", "e": b"4"}

    d.update(standard_dict)
    for ((k1, v1), (k2, v2)) in zip(d.items(), standard_dict.items()):
        assert k1 == k2
        assert v1 == v2


def test_inner_list(d: MutableMapping):
    d["a"] = ["one", "two", "three"]

    assert len(d["a"]) == 3

    assert d["a"][0] == "one"
    assert d["a"][1] == "two"
    assert d["a"][2] == "three"
