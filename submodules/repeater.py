import threading


class Repeater(object):
    def __init__(self, delay, worker, *args, **kwargs):
        self.worker = lambda: worker(*args, **kwargs)
        self.delay = delay

    def do(self):

        threading.Timer(self.delay, self.do).start()
        self.worker()
