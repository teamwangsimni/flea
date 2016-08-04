import tornado.gen
from tornado.tcpserver import TCPServer
from ..utils.commands import Command


class CommandTCPServer(TCPServer):
    def __init__(self, listen=8888, on_connect=None, 
                 on_close=None, on_command=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listen(listen)
        self._on_connect = on_connect or (lambda stream, address: (stream, address))
        self._on_close = on_close or (lambda stream, address: (stream, address))
        self._on_command = on_command or (lambda command: command)

    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        print('connected from {}'.format(address))
        self._on_connect(stream, address)
        try:
            while True:
                yield stream.read_until(
                    Command.DELIMITER_BYTES, 
                    callback=self._receive
                )
        except Exception:
            self._on_close(stream, address)
        else:
            self._on_close(stream, address)


    def _receive(self, data):
        command = Command.parse(data)
        self._on_command(command)
