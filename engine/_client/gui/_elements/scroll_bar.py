from .base import *
from pygame_gui.elements import UIHorizontalSlider

__all__ = ['ScrollBar']


class ScrollBar(BaseElement):
    def __change_scroll(self, value): self._elem.set_current_value(value)
    scroll_value = Field(int, __change_scroll)

    def __init__(self, id_, manager, kwargs):
        range_ = kwargs.get('range', (0, 100))
        start = kwargs.get('start', 0)
        super().__init__(id_, manager, UIHorizontalSlider,
                         relative_rect=kwargs['rect'],
                         value_range=range_,
                         start_value=start)
        self.scroll_value = start

    def handle_event(self, event) -> tuple:
        if event.user_type == 'scrolling':
            self.scroll_value = event.value
        return super().handle_event(event)
