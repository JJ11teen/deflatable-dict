from typing import Any, Iterator, MutableMapping


class DeflatableMap(MutableMapping):
    def __init__(self, d=None, sep=".") -> None:
        self._sep = sep
        self.d = {}
        if d:
            self.inflate(d)

    def inflate(self, d) -> None:
        for k, v in d.items():
            self.__setitem__(k, v)

    def deflate(self) -> MutableMapping:
        items = []
        for k, v in self.d.items():
            if v and isinstance(v, MutableMapping):
                for dk, dv in DeflatableMap(v, sep=self._sep).deflate().items():
                    items.append((f"{k}{self._sep}{dk}", dv))
            else:
                items.append((k, v))
        return dict(items)

    def __getitem__(self, k) -> Any:
        value = self.d
        for level in k.split(self._sep):
            if not isinstance(value, MutableMapping):
                raise KeyError(f"Key {k} does not exist")
            else:
                value = value[level]
        return value

    def __setitem__(self, k, v) -> None:
        context = self.d
        levels = k.split(self._sep)
        for sub_key in levels[:-1]:
            if sub_key not in context:
                context[sub_key] = DeflatableMap()
            context = context[sub_key]
        if isinstance(v, MutableMapping):
            v = DeflatableMap(v)
        context[levels[-1]] = v

    def __delitem__(self, k) -> None:
        levels = k.split(self._sep)
        for sub_key in levels[:-1]:
            context = context[sub_key]
        del context[levels[-1]]
        if len(context) == 0:
            self.__delitem__(self._sep.join(levels[:-1]))

    def __iter__(self) -> Iterator:
        return self.d.__iter__()

    def __len__(self) -> int:
        return self.d.__len__()

    def __repr__(self) -> str:
        return self.deflate().__repr__()
