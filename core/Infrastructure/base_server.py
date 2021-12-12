from abc import ABCMeta, abstractmethod, abstractproperty


class BaseServer(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self): pass

    @abstractproperty
    def online(self): pass

    @abstractmethod
    def handle_request(self): pass

    @abstractmethod
    def run(self): pass
