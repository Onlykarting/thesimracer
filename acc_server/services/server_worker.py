import os
import queue
import shutil
import subprocess
from pathlib import Path
from typing import Optional
from acc_server.models import AccEvent
from queue import Queue
from acc_server.services.stream_reader import StreamReader
from .base_server_worker import BaseServerWorker
from .base_server_manager import BaseServerManager
from .server_worker_proxy import ServerWorkerProxy
from thesimracer.settings import ACC_SERVER_CONFIG
from .dumpers import ServerConfigDumper, ServerSettingsDumper, AssistRulesDumper, \
    EventSettingsDumper, EventRulesDumper


class ServerWorker(BaseServerWorker):

    def __init__(self, event: AccEvent, manager: BaseServerManager, worker_id: int):
        super(BaseServerWorker, self).__init__()
        self.event = event
        self.worker_id = worker_id
        self.manager = manager
        self.dumpers = [
            EventSettingsDumper(self),
            EventRulesDumper(self),
            AssistRulesDumper(self),
            ServerSettingsDumper(self),
            ServerConfigDumper(self),
        ]
        self.process: Optional[subprocess.Popen] = None
        self.queue = queue.Queue()
        self.stderr_reader = None
        self.stdout_reader = None
        self.stopped = False

    @property
    def deploy_path(self):
        root_dir = Path(ACC_SERVER_CONFIG["ROOT_DIR"]).absolute()
        template = ACC_SERVER_CONFIG["SERVER_INSTANCE_NAME_TEMPLATE"]
        dir_name = template(id=self.event.id)
        return root_dir / dir_name

    @property
    def config_path(self):
        return self.deploy_path / 'cfg'

    @property
    def run_command(self):
        if ACC_SERVER_CONFIG.get("CUSTOM_RUN_COMMAND") is not None:
            return ACC_SERVER_CONFIG["CUSTOM_RUN_COMMAND"]
        else:
            return ACC_SERVER_CONFIG["SERVER_EXECUTABLE_PATH"]

    def init_cwd(self):
        if not self.deploy_path.exists():
            os.mkdir(self.deploy_path)
        elif not ACC_SERVER_CONFIG["ROOT_DIR"]:
            raise OSError(f"{self.deploy_path} directory already exists")
        else:
            shutil.rmtree(self.deploy_path)
            os.mkdir(self.deploy_path)
        os.mkdir(self.config_path)
        for dumper in self.dumpers:
            dumper.dump()

    def run(self):
        self.process = subprocess.Popen(self.run_command,
                                        cwd=self.deploy_path,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        self.stderr_reader = StreamReader('stderr', self.process.stderr, self.queue)
        self.stdout_reader = StreamReader('stdout', self.process.stdout, self.queue)
        while not self.stopped:
            context = self.queue.get()
            self.parse_event(context)

    def parse_event(self, context):
        for creator in self.manager.event_creators:
            if creator.test(context.line):
                creator.parse(context.line, {
                    'worker': ServerWorkerProxy(self.worker_id, self.manager),
                    'stream': context.stream_type
                })

    def terminate(self):
        self.stopped = True
        self.process.terminate()
