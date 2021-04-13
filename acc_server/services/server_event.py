import re
import subprocess
from .server_worker_proxy import ServerWorkerProxy
from .utils import try_parse_int


class ServerEvent:

    pattern = re.compile(r'(?P<timestamp>\d+):\s+')

    def __init__(self,
                 raw_string: str = None,
                 worker: ServerWorkerProxy = None,
                 out_stream_type: int = subprocess.STDOUT):
        self.out_stream_type = out_stream_type
        self.worker = worker
        self.raw_string = raw_string
        self.timestamp: int = -1
        self.offset: int = 0
        self.suffix: str = ''
        ServerEvent.parse(self)

    def parse(self):
        self.suffix = self.raw_string
        match = ServerEvent.pattern.match(self.suffix)
        if match:
            self.timestamp = int(match.groupdict().get('timestamp', -1))
            self.suffix = self.suffix[match.span()[1]:]
            self.offset += match.span()[1]


class SessionCompleted(ServerEvent):

    pattern = re.compile(r'Session completed: (?P<session_type>[a-zA-Z]+)/<session completed> with'
                         r' (?P<car_count>\d+) cars and (?P<connection_count>\d+) connections')

    def __init__(self,
                 raw_string: str = None,
                 worker: ServerWorkerProxy = None,
                 out_stream_type: int = subprocess.STDOUT):
        super(SessionCompleted, self).__init__(raw_string, worker, out_stream_type)
        self.car_count = -1
        self.connection_count = -1
        self.session_type = ''
        SessionCompleted.parse(self)

    def parse(self):
        match = SessionCompleted.pattern.match(self.suffix)
        if match:
            groups = match.groupdict()
            self.session_type = groups.get('session_type', '')
            self.car_count, ok = try_parse_int(groups.get('car_count'), -1)
            self.connection_count, ok = try_parse_int(groups.get('connection_count', ''), -1)
            self.suffix = self.suffix[match.span()[1]:]
            self.offset += match.span()[1]


class SessionPhaseChanged(ServerEvent):

    pattern = re.compile(r'Detected\s+sessionPhase\s+<(?P<previouse_pahse>[\w\d\s]+)>\s+'
                         r'->\s+<(?P<current_pahse>[\w\d\s]+)>\s+\((?P<session_type>[a-zA-Z]+)\)')

    def __init__(self,
                 raw_string: str = None,
                 worker: ServerWorkerProxy = None,
                 out_stream_type: int = subprocess.STDOUT):
        super(SessionPhaseChanged, self).__init__(raw_string, worker, out_stream_type)
        self.session_type: str = ''
        self.previous_phase: str = ''
        self.current_phase: str = ''
        SessionPhaseChanged.parse(self)

    def parse(self):
        match = self.pattern.match(self.suffix)
        if match:
            groups = match.groupdict()
            self.session_type = groups.get('session_type', '')
            self.previous_phase = groups.get('previous_phase', '')
            self.current_phase = groups.get('current_phase', '')
            self.offset += match.span()[1]
            self.suffix = self.suffix[match.span()[1]:]
