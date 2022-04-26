import pytest

from deflatabledict import DeflatableDict


@pytest.fixture()
def nested_dict():
    return {
        "b": [
            -1,
            -2,
            -3,
            {
                "1": "string",
                "2": [0, 0, 0, 0],
                "3": True,
            },
            {
                "a": 1e9,
                "b": r"s\n",
            },
        ],
    }


@pytest.fixture()
def flat_dict_append_list():
    return [
        ("b.[*]", -1),
        ("b.[*]", -2),
        ("b.[*]", -3),
        ("b.[*].1", "string"),
        ("b.[*].2.[*]", 0),
        ("b.[*].2.[*]", 0),
        ("b.[*].2.[*]", 0),
        ("b.[*].2.[*]", 0),
        ("b.[*].3", True),
        ("b.[*].a", 1e9),
        ("b.[*].b", r"s\n"),
    ]


@pytest.fixture()
def flat_dict():
    return {
        "b.[0]": -1,
        "b.[1]": -2,
        "b.[2]": -3,
        "b.[3].1": "string",
        "b.[3].2.[0]": 0,
        "b.[3].2.[1]": 0,
        "b.[3].2.[2]": 0,
        "b.[3].2.[3]": 0,
        "b.[3].3": True,
        "b.[4].a": 1e9,
        "b.[4].b": r"s\n",
    }


def test_nested_equality(nested_dict):
    dd = DeflatableDict(nested_dict, _delimiter=".", _flatten_lists=True)

    assert dd == nested_dict


def test_inflating_items(nested_dict, flat_dict_append_list):
    dd = DeflatableDict(_delimiter=".", _flatten_lists=True)
    dd.update(flat_dict_append_list)

    assert dd == nested_dict


def test_flat_indexing(nested_dict, flat_dict):
    dd = DeflatableDict(_delimiter=".", _flatten_lists=True)

    dd["inner"] = nested_dict

    for key, value in flat_dict.items():
        flat_key = f"inner.{key}"
        assert dd[flat_key] == value
