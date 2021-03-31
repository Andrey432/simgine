import multiprocessing as mp
from .._constants.multiprocessing import *
from .. import _client, _special as sp
from ._config import Config

__all__ = ['ApplicationController']


class ApplicationController(sp.Singleton):
    __slots__ = ('_bridge', '_running', '_app_proc')

    # noinspection PyTypeChecker
    def __init__(self):
        super().__init__()
        self._bridge = None    # type: sp.ProcessBridge
        self._app_proc = None  # type: mp.Process
        self._running = False

    def _create_app(self, config):
        in_stream = mp.Pipe(False)
        out_stream = mp.Pipe(False)
        encoding = config.get('multiprocessing/encoding')
        kwargs = {"input_": out_stream[0],
                  "output": in_stream[1],
                  "encoding": encoding}

        self._app_proc = mp.Process(target=_client.run_client, kwargs=kwargs)
        self._bridge = sp.ProcessBridge(in_stream[0], out_stream[1], encoding)

    def _handle_command(self, command, *args):
        if command == SHUTDOWN:
            self.shutdown(repeat=False)

    def init(self):
        config = Config.instance()
        self._create_app(config)
        self._running = True
        self._app_proc.start()
        self._bridge.send(STARTUP, config.get('application'))

    def is_running(self):
        return self._running

    def send(self, command, *args):
        self._bridge.send(command, args)

    def shutdown(self, repeat=True):
        if repeat:
            self.send(SHUTDOWN)
        self._running = False

    def join_app_proc(self):
        self._app_proc.join()

    def update(self):
        if self._app_proc.is_alive():
            for i in self._bridge.read_all():
                for cmd in i:
                    self._handle_command(*cmd)
            self._bridge.tr_end()
        else:
            self.shutdown(False)
