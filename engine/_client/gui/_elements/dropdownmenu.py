from .base_element import BaseElement
from pygame_gui.elements import UIDropDownMenu

__all__ = ['DropDownMenu']


class DropDownMenu(BaseElement):
    def __init__(self, id_, manager, kwargs):
        options = kwargs.get('options', [f'dropdownmenu (empty) {i}' for i in range(5)])
        start = options[0]
        super().__init__(id_, manager, UIDropDownMenu,
                         relative_rect=kwargs['rect'],
                         options_list=options,
                         starting_option=start)
