from .._config import Config

__all__ = ['TimeController']


class TimeController:
    __slots__ = ('_time', '_step', '_speed', '_dtime')

    def __init__(self):
        config = Config.instance()
        self._time = 0
        self._step = config.time.initstep
        self._speed = config.time.initspeed
        self._dtime = 0

    def reset(self):
        self._time = 0

    def update(self):
        self._dtime = self._step * self._speed
        self._time += self._dtime
        return self._dtime

    def dtime(self):
        return self._dtime

    def time(self):
        return self._time

    def set_speed(self, speed: float):
        self._speed = speed
