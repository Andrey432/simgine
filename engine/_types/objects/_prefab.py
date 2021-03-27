__all__ = ['Prefab']


class Prefab:
    __slots__ = ('name', 'class_', 'kwargs')

    def __init__(self, name: str, class_: type, kwargs=None):
        self.name = name
        self.class_ = class_
        self.kwargs = kwargs if kwargs is not None else {}

    def __repr__(self):
        return f"Prefab {self.name}" \
               f"(class={self.class_.__name__ if self.class_ is not None else None} {self.kwargs})"

    def set_kwargs(self, kwargs: dict):
        self.kwargs = dict(kwargs)

    def create(self, kwargs: dict):
        kw = dict(self.kwargs)
        kw.update(kwargs)
        return self.class_(**kw)
