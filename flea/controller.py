import time
from queue import Queue, Empty, Full
from threading import Thread
from .utils.logging import LoggingMixin
from .utils.directions import Direction
from .modules import motor
from . import config


class Controller(LoggingMixin):
    def __init__(self, motors):
        """Controlls all internal modules of the flea robot via a 
        command queue and it's consumer thread.

        :param motors: A dictionary of motor definitions with direction keys
            and GPIO number values.
        :type motors: :class:`~dict`

        """
        self._motors = motors
        self._commands = Queue(maxsize=config.COMMAND_QUEUE_SIZE)
        self._thread = None
        self._running = False

    
    def start(self):
        """Setup modules and start a command queue comsumer thread."""
        if self._thread and self._running:
            self.log('Already running in other thread. Ignoring!', tag='error')
            return

        self.log('Setting up motors')
        motor.setup_motors(motors)

        self._running = True
        self._thread = self._create_consumer_thread()
        self._thread.start()
        self.log('Started a new consumer thread')

    def stop(self):
        """Cleanup modules and stop currently running consumer thread."""
        self.log('Stopping the consumer thread')
        self._running = False

        self.log('Cleaning up motors')
        motor.cleanup_motors(motors)

    def feed(self, command):
        """Feed a command into the command queue of the controller."""
        try:
            self._commands.put(
                command, 
                timeout=config.COMMAND_QUEUE_FEED_TIMEOUT
            )
            self.log(
                'Feed command \"{}\". Current command queue size: {}'
                .format(command.name, self._commands.qsize())
            )
        except Full:
            # ignore the command if commands queue is full until the timeout
            self.log('Command queue full. Ignoring the command', tag='warning')

    def consume(self):
        """Consume a command from the command queue of the controller."""
        try:
            self._run(self._commands.get(
                timeout=config.COMMAND_QUEUE_CONSUME_TIMEOUT
            ))
        except Empty:
            # do nothing if the queue is empty until the timeout
            self.log('Command queue empty', tag='warning')

    def _run(self, command):
        self.log('Running {} with data {}'.format(command.name, command.data))
        method = getattr(self, '__{}__'.format(command.name))
        method(command.data)

    def _consume_forever(self):
        while self._running:
            self.consume()
            time.sleep(config.COMMAND_QUEUE_CONSUME_DELAY)

    def _create_consumer_thread(self):
        return Thread(target=self._consume_forever)

    @property
    def running(self):
        return self._running

    @property
    def commands(self):
        return self._commands

    @property
    def idle(self):
        return self._commands.empty()

    # ========
    # Commands
    # ========

    def __drive__(self, data):
        direction = Direction(data['direction'])
        speed = data['speed']
        motor.drive(self._motors, direction, speed)

    def __jump__(self, data):
        # TODO: NOT IMPLEMENTED YET
        pass

    def __track__(self, data):
        # TODO: NOT IMPLEMENTED YET
        pass
