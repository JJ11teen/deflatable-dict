import pytest
from deflatabledict import DeflatableDict


def test_errors():
    dd = DeflatableDict(sep=".")

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


def test_inflating_items(flat_deliminated_dict, nested_dict):
    dd = DeflatableDict(
        flat_deliminated_dict,
        sep=".",
    )

    assert dd == nested_dict
    for key in flat_deliminated_dict.keys():
        assert key in dd


def test_auto_flattening(flat_deliminated_dict, nested_dict):
    dd = DeflatableDict(sep=".")

    dd["inner"] = nested_dict

    for key, value in flat_deliminated_dict.items():
        assert dd[f"inner.{key}"] == value


def test_deflating(flat_deliminated_dict, nested_dict):
    dd = DeflatableDict(nested_dict, sep=".")

    assert dd == nested_dict
    assert dd.deflate() == flat_deliminated_dict

    # This tests the __repr__
    assert str(dd) == str(flat_deliminated_dict)
