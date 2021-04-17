from .server_event import ServerEvent
from typing import Callable


class ServerHandler:

    @staticmethod
    def checker(event: ServerEvent):
        return False

    @staticmethod
    def handler(event: ServerEvent):
        pass

    def execute(self, event: ServerEvent) -> bool:
        if self.checker(event):
            self.handler(event)
            return True
        else:
            return False
