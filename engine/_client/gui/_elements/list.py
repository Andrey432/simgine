from .base import *
from pygame_gui.elements import UISelectionList

__all__ = ['List']


class List(BaseElement):
    def __init__(self, id_, manager, kwargs):
        items = kwargs.get('items', [f'Test {i}' for i in range(5)])
        super().__init__(id_, manager, UISelectionList,
                         relative_rect=kwargs['rect'],
                         item_list=items)

    def get_selected_items(self) -> list[str]:
        if self._elem.allow_multi_select:
            return self._elem.get_multi_selection()
        selected = self._elem.get_single_selection()
        if selected is not None:
            return [selected]
        return []
