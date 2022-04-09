import threading
from time import time


class Timer(object):
    def __init__(self):
        self.start: float = time()

    @property
    def elsaped(self) -> float:
        return time() - self.start

    def do(self, func, delay, *args, **kwargs) -> None:

        threading.Timer(delay, self.do).start()
        func(*args, **kwargs)
