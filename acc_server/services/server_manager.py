from .server_worker_proxy import ServerWorkerProxy
from .server_worker import ServerWorker
from typing import Dict, Any
from acc_server.models import ServerWorkerSettings


class ServerWorkerManager:

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ServerWorkerManager, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.__workers: Dict[Any, ServerWorker] = {}
        self.callbacks = []

    def __len__(self):
        return len(self.__workers)

    def __getitem__(self, item):
        return ServerWorkerProxy(self.__workers[item], self)

    def create_worker(self, worker_settings: ServerWorkerSettings) -> ServerWorkerProxy:
        if not self.__workers.get(worker_settings.id):
            self.__workers[worker_settings.id] = ServerWorker(worker_settings)
        return ServerWorkerProxy(worker_settings.id, self)

    def terminate_worker(self, worker_id):
        self.__workers[worker_id].terminate()

    def run_worker(self, worker_id):
        self.__workers[worker_id].run()

    def kill_all(self):
        for worker in self.__workers.values():
            worker.terminate()

    def init_worker_cwd(self, worker_id):
        self.__workers[worker_id].init_cwd()
