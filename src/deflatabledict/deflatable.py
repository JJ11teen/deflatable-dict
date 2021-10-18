from collections import UserDict
from typing import Any, MutableMapping


class DeflatableDict(UserDict):
    def __init__(self, d=None, sep=".") -> None:
        self._sep = sep
        self.data = {}
        if d:
            self.inflate(d)

    def inflate(self, d) -> None:
        for k, v in d.items():
            self.__setitem__(k, v)

    def deflate(self) -> MutableMapping:
        items = []
        for k, v in self.data.items():
            if v and isinstance(v, MutableMapping):
                for dk, dv in DeflatableDict(v, sep=self._sep).deflate().items():
                    items.append((f"{k}{self._sep}{dk}", dv))
            else:
                items.append((k, v))
        return dict(items)

    def __getitem__(self, k) -> Any:
        v = self.data
        for sub_key in k.split(self._sep):
            if not isinstance(v, MutableMapping):
                raise KeyError(k)
            else:
                v = v[sub_key]
        return v

    def __setitem__(self, k, v) -> None:
        if k.startswith(self._sep) or k.startswith(self._sep):
            raise KeyError("Key cannot start or end with delimiter")
        context = self.data
        sub_keys = k.split(self._sep)
        for sub_key in sub_keys[:-1]:
            if sub_key not in context:
                context[sub_key] = DeflatableDict()
            context = context[sub_key]
        if isinstance(v, MutableMapping):
            v = DeflatableDict(v)
        context[sub_keys[-1]] = v

    def __delitem__(self, k) -> None:
        if k.startswith(self._sep) or k.startswith(self._sep):
            raise KeyError("Key cannot start or end with delimiter")
        context = self.data
        sub_keys = k.split(self._sep)
        for sub_key in sub_keys[:-1]:
            context = context[sub_key]
        del context[sub_keys[-1]]
        if len(context) == 0:
            self.__delitem__(self._sep.join(sub_keys[:-1]))

    def __contains__(self, k) -> bool:
        if k.startswith(self._sep) or k.startswith(self._sep):
            return False
        context = self.data
        sub_keys = k.split(self._sep)
        for sub_key in sub_keys[:-1]:
            print(sub_key)
            if sub_key not in context:
                return False
            if not isinstance(context, MutableMapping):
                return False
            else:
                context = context[sub_key]
        return sub_keys[-1] in context

    def __repr__(self) -> str:
        return self.deflate().__repr__()
