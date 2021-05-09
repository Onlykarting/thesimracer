from threading import Thread
from abc import ABCMeta, abstractmethod


class BaseServerWorker(Thread, metaclass=ABCMeta):

    @abstractmethod
    def init_cwd(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def terminate(self):
        pass
