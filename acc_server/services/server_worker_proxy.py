

class ServerWorkerProxy:

    def __init__(self, worker_id, manager):
        self.__worker_id = worker_id
        self.__manager = manager

    @property
    def manager(self):
        return self.__manager

    def terminate(self):
        self.manager.terminate_worker(self.__worker_id)

    def run(self):
        self.manager.init_worker_cwd(self.__worker_id)
        self.manager.run_worker(self.__worker_id)

    def init_cwd(self):
        self.manager.init_worker_cwd(self.__worker_id)
