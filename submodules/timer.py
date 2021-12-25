import threading
from time import time


class Timer(object):
    def __init__(self):
        self.start = time()

    @property
    def elsaped(self):
        return time() - self.start

    def do(self, func, delay, *args, **kwargs):

        threading.Timer(delay, self.do).start()
        func(*args, **kwargs)
