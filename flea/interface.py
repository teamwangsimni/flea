import abc
import functools
from six import with_metaclass
from tornado.ioloop import IOLoop
from .modules.network import CommandTCPServer, CommandBluetoothServer
from .utils.logging import LoggingMixin
from . import config



class Interface(with_metaclass(abc.ABCMeta)):
    def __init__(self, on_connect=None, on_close=None):
        """Abstract base class for flea control interfaces.

        Every concrete interfaces should implement :meth:`~serve` with it's
        own serving logics using :meth:`~_on_command` callback method.

        """
        self._on_connect = on_connect or (lambda stream, address: (stream, address))        
        self._on_close = on_close or (lambda stream, address: (stream, address))
        self.controller = None
        self.server = None

    @abc.abstractmethod
    def serve(self, controller, *args, **kwargs):
        """Any concrete interfaces must implement serving logic within this 
        method. Note that the interface will connect to the controller before
        starting serving.

        :note: Every concrete interfaces should call this super method to
            connect to the controller.

        """
        self.server.configure_on_command(controller.feed)


    @property
    def on_connect(self):
        return self._on_connect

    @property
    def on_close(self):
        return self._on_close


class TCPInterface(LoggingMixin, Interface):
    def __init__(self, on_connect=None, on_close=None):
        super().__init__(on_connect=on_connect, on_close=on_close)
        self.server = CommandTCPServer(
            on_connect=self.on_connect,
            on_close=self.on_close,
        )

    def serve(self, controller, port=config.INTERFACE_PORT):
        super().serve(controller, port=port)
        self.server.listen(port)
        self.log('Listening at port {}'.format(port))
        IOLoop.current().start()


class BluetoothInterface(LoggingMixin, Interface):
    def __init__(self, on_connect=None, on_close=None):
        super().__init__(on_connect=on_connect, on_close=on_close)
        self.server = CommandBluetoothServer(
            on_connect=on_connect, 
            on_close=on_close,
        )

    def serve(self, controller, port=config.INTERFACE_PORT):
        super().serve(controller, port=port)
        # TODO: NOT IMPLEMENTED YET
        pass
