import re
import subprocess
from dataclasses import dataclass, field
from .server_worker_proxy import ServerWorkerProxy


@dataclass(frozen=True)
class ServerEvent:
    ticks: int = 0
    raw_string: str = ''
    worker: ServerWorkerProxy = None
    stream: int = -2


@dataclass(frozen=True)
class SessionCompleted(ServerEvent):
    car_count: int = 0
    connection_count: int = 0
    session_type: str = ''


@dataclass(frozen=True)
class SessionPhaseChanged(ServerEvent):
    session_type: str = ''
    this_phase: str = ''
    next_phase: str = ''


@dataclass(frozen=True)
class EventEnd(ServerEvent):
    # Has no additional fields
    pass


class BaseEventCreator:

    def test(self, string: str) -> bool:
        pass

    def parse(self, string: str) -> ServerEvent:
        pass


class RegExpEventCreator(BaseEventCreator):

    pattern = re.compile(r'')

    event_data_class = ServerEvent

    type_convert_table = {}

    def test(self, string: str) -> bool:
        match = self.pattern.match(string)
        return match is not None

    def parse(self, string: str, **additional_params) -> event_data_class:
        match = self.pattern.match(string)
        groups = match.groupdict()
        for key, value in groups.items():
            if key in self.type_convert_table:
                groups[key] = self.type_convert_table[key](value)
        groups.update(additional_params)
        return self.event_data_class(**groups)


class EventCreators:

    class SessionComplete(RegExpEventCreator):
        pattern = re.compile(r'(?P<timestamp>\d+):\s+Session completed: (?P<session_type>[a-zA-Z]+)'
                             r'/<session completed> with (?P<car_count>\d+) cars and (?P<connection_count>\d+) connections')

        event_data_class = SessionCompleted

        type_convert_table = {
            'timestamp': int,
            'car_count': int,
            'connection_count': int
        }

    class SessionPhaseChanged(RegExpEventCreator):
        pattern = re.compile(r'(?P<timestamp>\d+):\s+Detected\s+sessionPhase\s+<(?P<this_phase>[\w\d\s]+)>\s+'
                             r'->\s+<(?P<next_phase>[\w\d\s]+)>\s+\((?P<session_type>[a-zA-Z]+)\)')

        event_data_class = SessionPhaseChanged

        type_convert_table = {
            'timestamp': int
        }

    class EventEnd(RegExpEventCreator):
        pattern = re.compile(r'(?P<timestamp>\d+):.+Weekend reset,.+')

        event_data_class = EventEnd

        type_convert_table = {
            'timestamp': int
        }
