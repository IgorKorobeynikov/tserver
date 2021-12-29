import threading


class Repeater(object):
    def __init__(self, delay, worker, *args, **kwargs):
        self.worker = lambda: worker(*args, **kwargs)
        self.delay = delay
        self.__run = True

    def break_(self):
        self.__run = False

    def do(self):
        if self.__run:
            threading.Timer(self.delay, self.do).start()
            self.worker()
