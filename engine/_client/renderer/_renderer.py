from .. import application


class Renderer:
    def __init__(self, cam):
        self._cam = cam
        self._app = application.Application.instance()  # type: application.Application

    def render(self):
        pass
