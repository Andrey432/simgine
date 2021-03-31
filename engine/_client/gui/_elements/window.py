from .base import *
from pygame_gui.elements import UIWindow

__all__ = ['Window']


class Window(BaseElement):
    def __init__(self, id_, manager, kwargs):
        super().__init__(id_, manager, UIWindow,
                         rect=kwargs['rect'],
                         resizable=kwargs['resizable'])

    def handle_event(self, event) -> tuple:
        if event.user_type == 'onclick':
            if event.ui_element.object_ids[1] == '#close_button':
                self._elem.kill()
        return super().handle_event(event)
