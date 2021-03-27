from engine.api.objects import GameObject
import time


class FrameRateMeter(GameObject):
    __slots__ = ('last', 'prev', 'sum', 'cnt', 'delay', 'enabled')

    def __init__(self, enabled, delta):
        super().__init__()
        self.last = time.time()
        self.prev = time.time()
        self.sum = 0
        self.cnt = 0
        self.delay = delta
        self.enabled = enabled

    def update(self, timedelta: float) -> None:
        if self.enabled:
            cur = time.time()
            self.sum += cur - self.prev
            self.prev = cur
            self.cnt += 1
            if cur - self.last >= self.delay:
                print(f'Time: {self.sum:.3f}, Total: {self.cnt}, Avg: {self.sum / self.cnt:.6f}')
                self.sum = 0
                self.cnt = 0
                self.last = cur
