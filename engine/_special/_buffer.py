import itertools


class Buffer:
    __slots__ = ('_main', '_buffer', '_last', '_null')

    def __init__(self, size, null=None):
        self._main = [null for _ in range(size)]
        self._buffer = [null for _ in range(size)]
        self._last = 0
        self._null = null

    def __len__(self):
        return self._last

    @property
    def nulltype(self):
        return self._null

    def size(self):
        return len(self._main)

    def full(self):
        return self._last == len(self._main)

    def empty(self):
        return self._last == 0

    def expand(self):
        size = len(self._main)
        null = self._null
        self._main.extend(null for _ in range(size))
        self._buffer.extend(null for _ in range(size))

    def push(self, elem):
        self._main[self._last] = elem
        self._last += 1

    def safe_push(self, elem):
        if self.full():
            self.expand()
        self.push(elem)

    def buffer(self):
        iter_ = itertools.islice(self._main, self._last)
        self._last = 0
        self._main, self._buffer = self._buffer, self._main
        return iter_
