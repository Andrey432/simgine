from .base_element import BaseElement
from pygame_gui.elements import UISelectionList

__all__ = ['List']


class List(BaseElement):
    def __init__(self, id_, manager, kwargs):
        items = kwargs.get('items', [(f'Test {i}', f'{i}') for i in range(5)])
        super().__init__(id_, manager, UISelectionList,
                         relative_rect=kwargs['rect'],
                         item_list=items)
