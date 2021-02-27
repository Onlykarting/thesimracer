import os
import shutil
from pathlib import Path
from acc_server.models import ServerWorkerSettings
from thesimracer.settings import ACC_SERVER_CONFIG
from .dumpers import ServerConfigDumper, ServerSettingsDumper, AssistRulesDumper, \
    EventSettingsDumper, EventRulesDumper


class ServerWorker:

    def __init__(self, settings: ServerWorkerSettings):
        self.settings = settings
        self.dumpers = [
            EventSettingsDumper(self),
            EventRulesDumper(self),
            AssistRulesDumper(self),
            ServerSettingsDumper(self),
            ServerConfigDumper(self),
        ]

    @property
    def deploy_path(self):
        root_dir = Path(ACC_SERVER_CONFIG["ROOT_DIR"]).absolute()
        template = ACC_SERVER_CONFIG["SERVER_INSTANCE_NAME_TEMPLATE"]
        dir_name = template(id=self.settings.id)
        return root_dir / dir_name

    @property
    def config_path(self):
        return self.deploy_path / 'cfg'

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
