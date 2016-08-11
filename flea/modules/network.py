import abc
from six import with_metaclass
import json
import tornado.gen
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer
from ..utils.commands import Command
from ..utils.logging import LoggingMixin


class CommandServerMixin(object):
    def __init__(self, on_connect=None, on_close=None, on_command=None, 
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_connect = on_connect or (lambda stream, address: (stream, address))
        self._on_close = on_close or (lambda stream, address: (stream, address))
        self._on_command = on_command or (lambda command: command)

    def receive(self, data):
        try:
            self.on_command(Command.parse(data))
        except json.JSONDecodeError:
            self.log('Invalid JSON data: {}'.format(data), tag='error')
        except ValueError as e:
            self.log(str(e), tag='error')

    def configure_on_command(self, on_command):
        self._on_command = on_command

    @property
    def on_connect(self):
        return self._on_connect

    @property
    def on_close(self):
        return self._on_close

    @property
    def on_command(self):
        return self._on_command


class CommandTCPServer(LoggingMixin, CommandServerMixin, TCPServer):
    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        self.log('Connected from {}'.format(address))
        self.on_connect(stream, address)
        try:
            while True:
                data = yield stream.read_until(Command.DELIMITER_BYTES)
                self.receive(data)
        except StreamClosedError:
            self.on_close(stream, address)
            self.log('Closed the connection from {}'
                     .format(address), tag='warning')


class CommandBluetoothServer(LoggingMixin, CommandServerMixin):
    # TODO: NOT IMPLEMENTED YET
    pass
