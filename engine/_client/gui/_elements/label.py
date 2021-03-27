from .base_element import BaseElement
from pygame_gui.elements import UILabel

__all__ = ['Label']


class Label(BaseElement):
    def __init__(self, id_, manager, kwargs):
        super().__init__(id_, manager, UILabel,
                         relative_rect=kwargs['rect'],
                         text=kwargs.get('text', ''))
