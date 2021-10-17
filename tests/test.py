from deflatablemap import DeflatableMap


def test_dict_get_set():
    df = DeflatableMap(sep=".")

    df["a"] = 0
    df["b"] = "string"

    assert df["a"] == 0
    assert df["b"] == "string"


def test_dict_len_update():
    df = DeflatableMap(sep=".")

    assert len(df) == 0

    df.update({"a": 0, "b": 1.0})
    df["c"] = "string"

    assert len(df) == 3


def test_dict_iter(flat_dict):
    df = DeflatableMap(flat_dict, sep=".")

    for ((k1, v1), (k2, v2)) in zip(df.items(), flat_dict.items()):
        assert k1 == k2
        assert v1 == v2


def test_inflating_items(flat_deliminated_dict, nested_dict):
    df = DeflatableMap(
        flat_deliminated_dict,
        sep=".",
    )

    assert df == nested_dict
    for key in flat_deliminated_dict.keys():
        assert key in df


def test_auto_flattening(flat_deliminated_dict, nested_dict):
    df = DeflatableMap(sep=".")

    df["inner"] = nested_dict

    for key, value in flat_deliminated_dict.items():
        assert df[f"inner.{key}"] == value


def test_deflating(flat_deliminated_dict, nested_dict):
    df = DeflatableMap(nested_dict, sep=".")

    assert df == nested_dict
    assert df.deflate() == flat_deliminated_dict
