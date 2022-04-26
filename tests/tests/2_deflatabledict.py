import pytest

from deflatabledict import DeflatableDict


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
def flat_dict():
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


def test_invalid_key_errors():
    dd = DeflatableDict(_delimiter=".", _flatten_lists=False)

    with pytest.raises(KeyError) as excinfo:
        dd["."]
        assert "Key cannot start or end with delimiter" in excinfo.value

    with pytest.raises(KeyError) as excinfo:
        dd[".invalid"]
        assert "Key cannot start or end with delimiter" in excinfo.value

    with pytest.raises(KeyError) as excinfo:
        del dd["invalid."]
        assert "Key cannot start or end with delimiter" in excinfo.value

    with pytest.raises(KeyError) as excinfo:
        dd[".invalid."]
        assert "Key cannot start or end with delimiter" in excinfo.value


def test_nested_equality(nested_dict):
    dd = DeflatableDict(nested_dict, _delimiter=".", _flatten_lists=False)

    assert dd == nested_dict


def test_inflating_items(nested_dict, flat_dict):
    dd1 = DeflatableDict(flat_dict, _delimiter=".", _flatten_lists=False)
    dd2 = DeflatableDict(_delimiter=".", _flatten_lists=False)
    dd2.update(flat_dict)

    assert dd1 == nested_dict
    assert dd2 == nested_dict


def test_flat_indexing(nested_dict, flat_dict):
    dd = DeflatableDict(_delimiter=".", _flatten_lists=False)

    dd["inner"] = nested_dict

    for key, value in flat_dict.items():
        flat_key = f"inner.{key}"
        assert dd[flat_key] == value


def test_deflating(nested_dict, flat_dict):
    dd = DeflatableDict(nested_dict, _delimiter=".", _flatten_lists=False)

    assert dd.deflate() == flat_dict


def test_flat_string_repr(nested_dict, flat_dict):
    dd = DeflatableDict(nested_dict, _delimiter=".", _flatten_lists=False)

    assert str(dd) == str(flat_dict)


def test_specifying_delimiter(nested_dict, flat_dict):
    dd = DeflatableDict(nested_dict, _delimiter="/", _flatten_lists=False)

    assert "a/1" in dd
    assert "a/2/a" in dd

    assert "a.1" not in dd
    assert "a.2.a" not in dd

    flat_slash_dict = {k.replace(".", "/"): v for k, v in flat_dict.items()}

    assert dd.deflate() == flat_slash_dict
