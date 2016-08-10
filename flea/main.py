from . import Flea, config
from .controller import Controller
from .interface import TCPInterface


controller = Controller(config.MOTORS)
interface = TCPInterface(controller)
flea = Flea(controller, interface)


if __name__ == '__main__':
    flea.start()
