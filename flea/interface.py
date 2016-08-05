import abc
import functools
from six import with_metaclass
from tornado.ioloop import IOLoop
from .modules.network import CommandTCPServer
from .utils.logging import LoggingMixin
from . import config



class Interface(with_metaclass(abc.ABCMeta)):
    def __init__(self, controller, on_connect=None, on_close=None):
        """Abstract base class for flea control interfaces.

        Every concrete interfaces should implement :meth:`~serve` with it's
        own serving logics using :meth:`~_on_command` callback method.

        """
        self.controller = controller
        self._on_connect = on_connect or (lambda stream, address: (stream, address))        
        self._on_close = on_close or (lambda stream, address: (stream, address))

    @abc.abstractmethod
    def serve(self, *args, **kwargs):
        """Any concrete interfaces must implement serving logic within this 
        method."""
        raise NotImplementedError

    def _on_command(self, command):
        self.controller.feed(command)


class TCPInterface(LoggingMixin, Interface):
    def __init__(self, controller, on_connect=None, on_close=None):
        super().__init__(
            controller=controller, 
            on_connect=on_connect, 
            on_close=on_close
        )
        self.server = CommandTCPServer(
            on_connect=self._on_connect,
            on_close=self._on_close,
            on_command=self._on_command)

    def serve(self, port=config.INTERFACE_PORT):
        self.log('Listening at port {}'.format(port))
        self.server.listen(port)
        IOLoop.current().start()


class BluetoothInterface(LoggingMixin, Interface):
    def serve(self, port):
        # TODO: NOT IMPLEMENTED YET
        pass
