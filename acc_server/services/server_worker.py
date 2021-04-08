import os
import shutil
import subprocess
from threading import Thread
from pathlib import Path
from typing import Optional, Callable, List
from acc_server.models import AccEvent
from thesimracer.settings import ACC_SERVER_CONFIG
from .dumpers import ServerConfigDumper, ServerSettingsDumper, AssistRulesDumper, \
    EventSettingsDumper, EventRulesDumper


class ServerWorker(Thread):

    def __init__(self, event: AccEvent):
        super(ServerWorker, self).__init__()
        self.event = event
        self.dumpers = [
            EventSettingsDumper(self),
            EventRulesDumper(self),
            AssistRulesDumper(self),
            ServerSettingsDumper(self),
            ServerConfigDumper(self),
        ]
        self.process: Optional[subprocess.Popen] = None

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
        with self.process as process:
            print("stdout:", self.process.stdout.readline())
            print("stderr:", self.process.stderr.readline())

    def terminate(self):
        self.process.terminate()

    # def __del__(self):
    #     self.terminate()
