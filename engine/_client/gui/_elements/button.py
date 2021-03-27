from .base_element import BaseElement
from pygame_gui.elements import UIButton

__all__ = ['Button']


class Button(BaseElement):
    def __init__(self, id_, manager, kwargs):
        super().__init__(id_, manager, UIButton,
                         relative_rect=kwargs['rect'],
                         text=kwargs.get('text', ''))
