from .base_element import BaseElement
from pygame_gui.elements import UIWindow

__all__ = ['Window']


class Window(BaseElement):
    def __init__(self, id_, manager, kwargs):
        super().__init__(id_, manager, UIWindow,
                         rect=kwargs['rect'],
                         resizable=kwargs['resizable'])
