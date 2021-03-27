from .base_element import BaseElement
from pygame_gui.elements import UIPanel

__all__ = ['Panel']


class Panel(BaseElement):
    def __init__(self, id_, manager, kwargs):
        super().__init__(id_, manager, UIPanel,
                         relative_rect=kwargs['rect'],
                         starting_layer_height=kwargs['starting_layer_height'])
