from collections import UserDict
from typing import Any, MutableMapping, MutableSequence

from idna import check_initial_combiner


class DeflatableDict(UserDict):
    def __init__(
        self,
        *args,
        _delimiter=".",
        _flatten_lists=True,
        _delimiter_list_start="[",
        _delimiter_list_end="]",
        _list_append_key=None,
        **kwargs,
    ) -> None:
        self.data = dict()
        initial_data = dict(*args, **kwargs)

        self._delimiter = _delimiter
        self._flatten_lists = _flatten_lists
        self._delimiter_list_start = _delimiter_list_start
        self._delimiter_list_end = _delimiter_list_end
        self._list_append_key = _list_append_key

        if self._flatten_lists:
            delimiters = set(
                [self._delimiter, self._delimiter_list_start, self._delimiter_list_end, self._list_append_key]
            )
            if len(delimiters) < 4:
                raise ValueError(
                    "All four of delimiter, list delimiters, and list append key must be unique. Only got {delimiters}."
                )

        for k, v in initial_data.items():
            self.__setitem__(k, v)

    def deflate(self) -> MutableMapping:
        # Collect flat K:V tuples into this list
        items = []
        # Traverse our context through the child layers, recursively calling deflate on each:
        for k, v in self.data.items():
            if v and isinstance(v, MutableMapping):
                for dk, dv in DeflatableDict(v, _delimiter=self._delimiter).deflate().items():
                    items.append((f"{k}{self._delimiter}{dk}", dv))
            else:
                items.append((k, v))
        # Return a shallow (flat) dict
        return dict(items)

    def __getitem__(self, k) -> Any:
        # Traverse our context through the child layers:
        v = self.data
        for sub_key in k.split(self._delimiter):
            if isinstance(v, MutableMapping):
                v = v[sub_key]
            elif self._flatten_lists and isinstance(v, MutableSequence):
                v = v[int(sub_key[len(self._delimiter_list_start) : -len(self._delimiter_list_end)])]
            else:
                raise KeyError(k)

        # Check if this is a delimited list, if so convert back to a list:
        if (
            self._flatten_lists
            and isinstance(v, MutableMapping)
            and len(v) > 0
            and not any(
                [
                    not k.startswith(self._delimiter_list_start) or not k.endswith(self._delimiter_list_end)
                    for k in v.keys()
                ]
            )
        ):
            keys = [k[len(self._delimiter_list_start) : -len(self._delimiter_list_end)] for k in v.keys()]
            if not any([not k.isdecimal() for k in keys]):
                v = [item[1] for item in sorted(v.items(), key=lambda i: i[0])]

        # Return the relevant value (possibly converted)
        return v

    def __setitem__(self, k, v) -> None:
        # Quick validation of key values:
        if k.startswith(self._delimiter) or k.startswith(self._delimiter):
            raise KeyError("Key cannot start or end with delimiter")

        # Check if this is a list to delimit, if so convert to a delimited list (really a dict):
        if self._flatten_lists and isinstance(v, MutableSequence):
            v = {f"{self._delimiter_list_start}{i}{self._delimiter_list_end}": dv for i, dv in enumerate(v)}

        # Convert nested mappings (ie handle child layers first)
        if isinstance(v, MutableMapping):
            v = DeflatableDict(v)

        # Traverse our context through the children, ensuring each child layer exists:
        context = self.data
        sub_keys = k.split(self._delimiter)
        for sub_key in sub_keys[:-1]:
            if isinstance(context, MutableMapping):
                if sub_key not in context:
                    context[sub_key] = DeflatableDict()
            context = context[sub_key]

        # Insert our (possibly converted) value into our context.
        # If out context is a list, we need to handle indexing & appending,
        # otherwise it is a dict and we can just assign
        if self._flatten_lists and isinstance(context, MutableSequence):
            i_str = sub_keys[-1][len(self._delimiter_list_start) : -len(self._delimiter_list_end)]
            if self._list_append_key is not None and i_str == self._list_append_key:
                context.append(v)
            else:
                i = int(i_str)
                if len(context) > i:
                    context[i] = v
                else:
                    raise IndexError(
                        f"Cannot assign to '{k}' as the innermost list assignment index is out of range. "
                        f"Use the list append key '{self._list_append_key}' to append instead of assigning."
                    )
        else:
            context[sub_keys[-1]] = v

    def __delitem__(self, k) -> None:
        # Quick validation of key values:
        if k.startswith(self._delimiter) or k.startswith(self._delimiter):
            raise KeyError("Key cannot start or end with delimiter")

        # Traverse our context through the child layers:
        context = self.data
        sub_keys = k.split(self._delimiter)
        for sub_key in sub_keys[:-1]:
            context = context[sub_key]

        # Remove the specified key
        del context[sub_keys[-1]]

        # If this was the last key of a child, remove it:
        if len(context) == 0:
            self.__delitem__(self._delimiter.join(sub_keys[:-1]))

    def __contains__(self, k) -> bool:
        # Quick validation of key values:
        if k.startswith(self._delimiter) or k.startswith(self._delimiter):
            return False

        # Traverse our context through the child layers, stopping one early and ensuring
        # each layer has depth (ie is a dict):
        context = self.data
        sub_keys = k.split(self._delimiter)
        for sub_key in sub_keys[:-1]:
            if sub_key not in context:
                return False
            if not isinstance(context, MutableMapping):
                return False
            else:
                context = context[sub_key]

        # Reuse the __contains__ from the level one-up from specified key:
        return sub_keys[-1] in context

    def __repr__(self) -> str:
        return self.deflate().__repr__()
