from abc import ABCMeta, abstractmethod


class BaseServerManager(metaclass=ABCMeta):
    @abstractmethod
    def create_worker(self, event):
        pass

    @abstractmethod
    def terminate_worker(self, worker_id):
        pass

    @abstractmethod
    def run_worker(self, worker_id):
        pass

    @abstractmethod
    def kill_all(self):
        pass

    @abstractmethod
    def init_worker_cwd(self, worker_id):
        pass

    @abstractmethod
    def polling(self, delay, blocking):
        pass

    @property
    @abstractmethod
    def handlers(self) -> list:
        pass

    @property
    @abstractmethod
    def event_creators(self) -> list:
        pass