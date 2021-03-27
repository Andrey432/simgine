from .._constants.multiprocessing import *
from .._client import run_client
from .._config import Config
from .. import _special as sp
import multiprocessing as mp

__all__ = ['ApplicationController']


class ApplicationController(sp.Singleton):
    __slots__ = ('_bridge', '_running', '_app_proc', '_gui_events')

    # noinspection PyTypeChecker
    def __init__(self):
        super().__init__()
        self._bridge = None    # type: sp.ProcessBridge
        self._app_proc = None  # type: mp.Process
        self._running = False
        self._gui_events = sp.Buffer(64)

    @property
    def gui(self):
        return self._gui_events.buffer()

    def _create_app(self, config):
        in_stream = mp.Pipe(False)
        out_stream = mp.Pipe(False)
        encoding = config.multiprocessing.encoding
        kwargs = {"input_": out_stream[0],
                  "output": in_stream[1],
                  "encoding": encoding}

        self._app_proc = mp.Process(target=run_client, kwargs=kwargs)
        self._bridge = sp.ProcessBridge(in_stream[0], out_stream[1], encoding)

    def _handle_command(self, command, *args):
        if command == SHUTDOWN:
            self.shutdown(repeat=False)
        elif command == GUI_EVENT:
            if args[0] == 'onclick':
                print(args)
            self._gui_events.safe_push(args)

    def init(self):
        config = Config.instance()
        self._create_app(config)
        self._running = True
        self._app_proc.start()
        self._bridge.send(STARTUP, config.application.all())

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
