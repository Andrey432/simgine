from pygame import Rect
from typing import Callable

__all__ = ['BaseElement', 'Field']


class Field:
    __slots__ = ('_value', '_handlers', '_handler_flag')

    def __init__(self):
        self._value = None
        self._handlers = {}
        self._handler_flag = False

    def __set__(self, instance, value):
        self._value = value
        if not self._handler_flag and instance.id in self._handlers:
            self._handler_flag = True
            for h in self._handlers[instance.id]:
                h(instance, value)
            self._handler_flag = False

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._value

    def add_handler(self, target_id: str, callback: Callable) -> None:
        self._handlers.setdefault(target_id, []).append(callback)


class BaseElement:
    __slots__ = ('_elem', '_id')

    def __init__(self, id_, manager, class_, **attrs):
        rname = 'rect' if 'rect' in attrs else 'relative_rect'
        attrs[rname] = Rect(attrs[rname])
        self._elem = class_(manager=manager, object_id=id_, **attrs)
        self._id = id_

    @property
    def id(self):
        return self._id

    def set_handler(self, param: str, callback: Callable) -> None:
        t = type(self)
        if not hasattr(t, param) or not isinstance(getattr(t, param), Field):
            raise AttributeError(f'{type(self).__name__} has no attribute "{param}"')
        getattr(t, param).add_handler(self._id, callback)

    def handle_event(self, event) -> tuple:
        return ()
