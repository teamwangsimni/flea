from .utils.logging import LoggingMixin


class Flea(LoggingMixin):
    def __init__(self, controller, interface):
        self.controller = controller
        self.interface = interface

    def start(self):
        controller.start()
        interface.serve()

    def stop(self):
        controller.stop()
        interface.stop()
