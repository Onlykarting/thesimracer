from .default_event_handlers import OnSessionCompleted, OnEventEnd, OnSessionPhaseChanged
from .server_event import ServerEvent, SessionCompleted, SessionPhaseChanged


class KillServer(OnEventEnd):

    @staticmethod
    def handler(event: ServerEvent):
        print("Killing server")
        event.worker.terminate()


class LogSessionPhaseChanged(OnSessionPhaseChanged):

    @staticmethod
    def handler(event: SessionPhaseChanged):
        print("Session phase changed {} -> {}".format(event.this_phase, event.next_phase))
