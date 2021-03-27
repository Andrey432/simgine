from .base_element import BaseElement
from pygame_gui.elements import UIHorizontalSlider

__all__ = ['ScrollBar']


class ScrollBar(BaseElement):
    def __init__(self, id_, manager, kwargs):
        range_ = kwargs.get('range', (0, 100))
        start = kwargs.get('start', 0)
        super().__init__(id_, manager, UIHorizontalSlider,
                         relative_rect=kwargs['rect'],
                         value_range=range_,
                         start_value=start)
