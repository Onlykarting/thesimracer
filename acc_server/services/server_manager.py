import time
from datetime import timedelta, datetime
from .base_server_manager import BaseServerManager
from .server_worker_proxy import ServerWorkerProxy
from .server_event import EventCreators
from .server_worker import ServerWorker
from typing import Dict, Any
from acc_server.models import AccEvent


class ServerWorkerManager(BaseServerManager):

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ServerWorkerManager, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.__workers: Dict[Any, ServerWorker] = {}
        self.__handlers = []
        self.__event_creators = [
            EventCreators.EventEnd(),
            EventCreators.SessionComplete(),
            EventCreators.SessionPhaseChanged()
        ]

    def __len__(self):
        return len(self.__workers)

    def __getitem__(self, item):
        return ServerWorkerProxy(self.__workers[item], self)

    def create_worker(self, event: AccEvent) -> ServerWorkerProxy:
        if not self.__workers.get(event.id):
            self.__workers[event.id] = ServerWorker(event, self, event.id)
        return ServerWorkerProxy(event.id, self)

    def terminate_worker(self, worker_id):
        self.__workers[worker_id].terminate()

    def run_worker(self, worker_id):
        self.__workers[worker_id].run()

    def kill_all(self):
        for worker in self.__workers.values():
            worker.terminate()

    def init_worker_cwd(self, worker_id):
        self.__workers[worker_id].init_cwd()

    def polling(self, delay: timedelta = timedelta(minutes=1), blocking: bool = True):
        while True:
            events_to_be_started = AccEvent.objects.filter(event__starts_at__lte=datetime.utcnow())
            for event in events_to_be_started:
                worker = self.create_worker(event)
                worker.run()
            time.sleep(delay.total_seconds())

    @property
    def event_creators(self) -> list:
        return self.__event_creators

    @property
    def handlers(self) -> list:
        return self.__handlers
