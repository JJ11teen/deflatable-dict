# deflatable-dict

A dictionary that can be flattened and re-inflated. Particularly useful if you're interacting with yaml, for example.

[![Build](https://github.com/JJ11teen/deflatable-dict/actions/workflows/build.yaml/badge.svg)](https://github.com/JJ11teen/deflatable-dict/actions/workflows/build.yaml)
[![PyPI version](https://badge.fury.io/py/deflatable-dict.svg)](https://pypi.org/project/deflatable-dict/)

## Installation

with pip:
```
pip install deflatable-dict
```
`deflatable-dict` does not have any dependencies beyond standard python libraries.

## Instantiation

```python
from deflatabledict import DeflatableDict

dd = DeflatableDict({
    "a": {
        "1": True,
        "2": False,
    },
    "b": 20,
})

dd["a.1"] # True
dd["a.2"] # False
dd["b"] # 20
dd["a"] # { "1": True, "2": False }
```

## Deflation
A DeflatableDict can be deflated with `.deflate()`. This returns a standard dictionary object with flattened keys constructed by concatenating the nested keys with the DeflatableDict's delimiter. A DeflatableDict uses it's deflated form for its string representation.

## Delimiter
A DeflatableDict can have it's delimiter specified by passing the desired delimiter as the `delimiter` parameter to the DeflatableDict constructor. If not explicitly specified the delimiter is `.`.

## Inflation
A DeflatableDict will automatically inflate any values that are inserted into it. For example:
```python
from deflatabledict import DeflatableDict

dd = DeflatableDict()
dd["a.1"] = True
dd["a.2"] = False

dd["a"] # { "1": True, "2": False }
```

# Development

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project uses `.devcontainer` to describe the environment to use for development. You may use the environment described in this directory (it integrates automatically with vscode's 'remote containers' extension), or you may create your own environment with the same dependencies.

## Dependencies
Install development dependencies with:

`pip install .[tests]`

## Tests
Run tests with:
```bash
pytest
```