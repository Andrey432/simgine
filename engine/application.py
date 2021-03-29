from ._client import application
from ._special import Singleton


class Application(Singleton):
    def __init__(self):
        super().__init__()
        self._app = application.Application.instance()  # type: application.Application

    @classmethod
    def instance(cls) -> 'Application':
        if not cls.exists_instance():
            cls.create_instance()
        return super().instance()

    def shutdown(self):
        self._app.shutdown()

    def get_ui_element(self, name: str):
        return self._app.gui.get_element(name)
