from .. import _application


class Renderer:
    def __init__(self, cam):
        self._cam = cam
        self._app = _application.Application.instance()  # type: _application.Application

    def render(self):
        pass
