import threading
from dataclasses import dataclass
from queue import Queue, Empty
from typing import Any


class StreamReader:

    @dataclass
    class Context:
        line: str
        stream_type: str
        worker: Any
        encoding: str

    def __init__(self, worker, stream_type, stream, queue, encoding='utf-8'):
        self.worker = worker
        self.stream_type = stream_type
        self.stream = stream
        self.encoding = encoding
        self.queue = queue
        self.thread = threading.Thread(target=self.__reader)
        self.thread.run()

    def __reader(self):
        for line in self.stream:
            self.queue.put(self.Context(line, self.stream_type, self.worker, self.encoding))
