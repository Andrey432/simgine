from ..._loaders import YAML_format
from .. import _application
from ._layout import Layout
from ._elements import BaseElement
import pygame_gui as gui
import pygame


_REPR_TABLE = {
    'ui_button_pressed': 'onclick',
    'ui_text_box_link_clicked': 'onclick',
    'ui_text_entry_finished': 'input',
    'ui_drop_down_menu_changed': 'onclick',
    2: 'doubleclick',
    3: 'hover',
    4: 'unhover',
    6: 'input',
    9: 'scrolling',
    10: 'onclick',
    12: 'doubleclick',
    13: 'close',
    15: 'dialog',
    16: 'dialog',
    17: 'dialog',
}


class GUIManager:
    def __init__(self):
        super().__init__()
        self._layouts = {}  # type: dict[str, Layout]
        self._elements = {}  # type: dict[str, BaseElement]
        self._app = _application.Application.instance()  # type: _application.Application
        self._mng = None  # type: gui.UIManager

    def init(self, settings) -> None:
        self._mng = gui.UIManager(settings['resolution'])

        file = settings['gui_config']
        data = YAML_format(file)
        for space_name in data:
            lt = Layout(data[space_name], manager=self._mng)
            self._layouts[space_name] = lt
            for elem in lt.elements_list():
                self._elements[elem.id] = elem

    def handle_event(self, event: pygame.event.Event) -> [None, tuple]:
        if event.type == pygame.USEREVENT:
            if event.user_type in _REPR_TABLE:
                element = event.ui_object_id.split('.')[0]
                event.user_type = _REPR_TABLE[event.user_type]
                return event.user_type, element, *self._elements[element].handle_event(event)
            return
        self._mng.process_events(event)

    def update(self) -> None:
        win = self._app.window
        self._mng.update(win.frame_time())
        self._mng.draw_ui(win.canvas())
