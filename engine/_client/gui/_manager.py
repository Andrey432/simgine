from ..._loaders import YamlLoader
from .. import application
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
        self._app = None  # type: application.Application
        self._mng = None  # type: gui.UIManager

    def init(self) -> None:
        self._app = application.Application.instance()  # type: application.Application
        config = self._app.config

        self._mng = gui.UIManager(config.get('application/resolution'))

        file = config.get('project/gui_config')
        data = YamlLoader.load(file)
        layouts = data['layouts']
        references = data['refs']

        for lt_name in layouts:
            lt = Layout(layouts[lt_name], manager=self._mng)
            self._layouts[lt_name] = lt
            for elem in lt.elements_list():
                self._elements[elem.id] = elem

        md_ctrl = self._app.md_controller
        for ref, handler in references.items():
            lt, elem, param = ref.split('.')
            clb = md_ctrl.get_attr(handler)
            self._layouts[lt].get(elem).set_handler(param, clb)

    def get_element(self, name: str) -> BaseElement:
        return self._elements[name]

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.USEREVENT:
            if event.user_type in _REPR_TABLE:
                element = event.ui_element.object_ids[0]
                event.user_type = _REPR_TABLE[event.user_type]
                self._elements[element].handle_event(event)
        else:
            self._mng.process_events(event)

    def update(self) -> None:
        win = self._app.window
        self._mng.update(win.frame_time())
        self._mng.draw_ui(win.canvas())
