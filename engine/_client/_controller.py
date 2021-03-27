from .._special import ProcessBridge
from ._application import Application


class Controller(ProcessBridge):
    __slots__ = ('_app',)

    def __init__(self, inp, out, encoding):
        super().__init__(inp, out, encoding)
        self._app = Application(self)

    def run(self):
        app, rb = self._app, self._reset_buffer
        while app.running:
            app.update()
            rb()
