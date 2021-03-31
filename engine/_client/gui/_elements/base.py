from pygame_gui import core
from pygame import Rect
from typing import Callable

__all__ = ['BaseElement', 'Field']


class Field:
    __slots__ = ('_value', '_type', '_base_handler', '_handlers', '_triggering')

    def __init__(self, type_: type, base_handler=lambda i, v: None):
        self._value = None
        self._type = type_
        self._base_handler = base_handler
        self._handlers = {}
        self._triggering = False

    def __set__(self, instance, value):
        if type(value) is not self._type:
            raise TypeError(f'Invalid value type (expected {self._type.__name__}, got {type(value).__name__})')
        self._value = value
        self._base_handler(instance, value)
        self._trigger(instance, value)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._value

    def _trigger(self, instance, value):
        if not self._triggering and instance.id in self._handlers:
            self._triggering = True
            for h in self._handlers[instance.id]:
                h(instance, value)
            self._triggering = False

    def add_handler(self, target_id: str, callback: Callable) -> None:
        self._handlers.setdefault(target_id, []).append(callback)


class BaseElement:
    __slots__ = ('_elem', '_id')

    def __change_visibility(self, value): self._elem.show() if value else self._elem.hide()
    displayed = Field(bool, __change_visibility)

    def __change_enabled(self, state): self._elem.enable() if state else self._elem.disable()
    enabled = Field(bool, __change_enabled)

    def __change_layer(self, layer): self._elem.change_layer(layer)
    layer = Field(int, __change_layer)

    def __change_xsize(self, value): self._elem.set_dimensions((value, self._elem.relative_rect.height))
    xsize = Field(int, __change_xsize)

    def __change_ysize(self, value): self._elem.set_dimensions((self._elem.relative_rect.width, value))
    ysize = Field(int, __change_ysize)

    def __change_xposition(self, value): self._elem.set_position((value, self._elem.relative_rect.y))
    xposition = Field(int, __change_xposition)

    def __change_yposition(self, value): self._elem.set_position((self._elem.relative_rect.x, value))
    yposition = Field(int, __change_yposition)

    def __init__(self, id_, manager, class_, **attrs):
        rname = 'rect' if 'rect' in attrs else 'relative_rect'
        attrs[rname] = Rect(attrs[rname])
        self._elem = class_(manager=manager, object_id=id_, **attrs)  # type: core.UIElement
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
