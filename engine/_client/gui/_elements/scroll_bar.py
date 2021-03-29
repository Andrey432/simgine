from .base_element import *
from pygame_gui.elements import UIHorizontalSlider

__all__ = ['ScrollBar']


class ScrollBar(BaseElement):
    current_value = Field()

    def __init__(self, id_, manager, kwargs):
        range_ = kwargs.get('range', (0, 100))
        start = kwargs.get('start', 0)
        super().__init__(id_, manager, UIHorizontalSlider,
                         relative_rect=kwargs['rect'],
                         value_range=range_,
                         start_value=start)
        self.current_value = start

    def handle_event(self, event) -> tuple:
        if event.user_type == 'scrolling':
            self.current_value = event.value
        return super().handle_event(event)
