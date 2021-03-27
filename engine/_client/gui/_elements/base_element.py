from pygame import Rect


class BaseElement:
    __slots__ = ('_elem', '_id')

    def __init__(self, id_, manager, class_, **attrs):
        rname = 'rect' if 'rect' in attrs else 'relative_rect'
        attrs[rname] = Rect(attrs[rname])
        self._elem = class_(manager=manager, object_id=id_, **attrs)
        self._id = id_

    @property
    def id(self):
        return self._id

    def handle_event(self, event) -> tuple:
        return ()


"""
UIImage
UIButton
UIHorizontalSlider
UIVerticalScrollBar
UIHorizontalScrollBar
UILabel
UIPanel
UIScreenSpaceHealthBar
UISelectionList
UITextBox
UITooltip
UIDropDownMenu
UIWorldSpaceHealthBar
UITextEntryLine
UIWindow
UIScrollingContainer
"""
