from .base_element import BaseElement
from pygame_gui.elements import UIImage
from pygame import Surface, SRCALPHA

__all__ = ['Image']


class Image(BaseElement):
    def __init__(self, id_, manager, kwargs):
        img = kwargs.get('img', Surface(kwargs['rect'][:2]))  # , SRCALPHA))
        super().__init__(id_, manager, UIImage,
                         relative_rect=kwargs['rect'],
                         image_surface=img)
