from .base import *
from pygame_gui.elements import UILabel

__all__ = ['Label']


class Label(BaseElement):
    def __change_text(self, text): self._elem.set_text(text)
    text = Field(str, __change_text)

    def __init__(self, id_, manager, kwargs):
        super().__init__(id_, manager, UILabel,
                         relative_rect=kwargs['rect'],
                         text=kwargs.get('text', ''))
