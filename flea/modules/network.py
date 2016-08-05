import json
import tornado.gen
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer
from ..utils.commands import Command
from ..utils.logging import LoggingMixin


class CommandTCPServer(LoggingMixin, TCPServer):
    def __init__(self, on_connect=None, on_close=None, on_command=None, 
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_connect = on_connect or (lambda stream, address: (stream, address))
        self._on_close = on_close or (lambda stream, address: (stream, address))
        self._on_command = on_command or (lambda command: command)

    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        self.log('Connected from {}'.format(address))
        self._on_connect(stream, address)
        try:
            while True:
                data = yield stream.read_until(Command.DELIMITER_BYTES)
                self.receive(data)
        except StreamClosedError:
            self.log(
                'Closed the connection from {}'.format(address), 
                tag='warning'
            )


    def receive(self, data):
        try:
            command = Command.parse(data)
            self._on_command(command)
        except json.JSONDecodeError:
            self.log('Invalid JSON data: {}'.format(data), tag='error')
        except ValueError as e:
            self.log(str(e), tag='error')
