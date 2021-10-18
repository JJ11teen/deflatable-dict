from typing import MutableMapping

import pytest
from deflatabledict import DeflatableDict


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


def test_dict_iter(d: MutableMapping, flat_dict):
    d.update(flat_dict)
    for ((k1, v1), (k2, v2)) in zip(d.items(), flat_dict.items()):
        assert k1 == k2
        assert v1 == v2
