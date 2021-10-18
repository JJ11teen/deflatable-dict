import pytest
from deflatabledict import DeflatableDict


def test_invalid_key_errors():
    dd = DeflatableDict(delimiter=".")

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
    dd = DeflatableDict(nested_dict, delimiter=".")

    assert dd == nested_dict


def test_inflating_items(nested_dict, flat_period_delimited_dict):
    dd1 = DeflatableDict(flat_period_delimited_dict, delimiter=".")
    dd2 = DeflatableDict(delimiter=".")
    dd2.update(flat_period_delimited_dict)

    assert dd1 == nested_dict
    assert dd2 == nested_dict


def test_flat_indexing(nested_dict, flat_period_delimited_dict):
    dd = DeflatableDict(delimiter=".")

    dd["inner"] = nested_dict

    for key, value in flat_period_delimited_dict.items():
        flat_key = f"inner.{key}"
        assert dd[flat_key] == value


def test_deflating(nested_dict, flat_period_delimited_dict):
    dd = DeflatableDict(nested_dict, delimiter=".")

    assert dd.deflate() == flat_period_delimited_dict


def test_flat_string_repr(nested_dict, flat_period_delimited_dict):
    dd = DeflatableDict(nested_dict, delimiter=".")

    assert str(dd) == str(flat_period_delimited_dict)


def test_specifying_delimiter(nested_dict, flat_slash_delimited_dict):
    dd = DeflatableDict(nested_dict, delimiter="/")

    assert "a/1" in dd
    assert "a/2/a" in dd

    assert "a.1" not in dd
    assert "a.2.a" not in dd

    assert dd.deflate() == flat_slash_delimited_dict
