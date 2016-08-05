import logging
from timeit import default_timer
from contextlib import contextmanager
from colorlog import ColoredFormatter


# Execution time measuring context manager for logging purpose
@contextmanager
def elapsed_timer():
    start = default_timer()

    def elapser():
        return default_timer() - start

    yield lambda: elapser()


# Logging handler and formatter
__FLEA_LOG_STREAM_HANDLER__ = logging.StreamHandler()
__FLEA_LOG_FORMATTER__ = ColoredFormatter(
    '%(asctime)s %(name)-4s %(log_color)s%(message)s',
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white'
    },
    secondary_log_colors={},
    style='%'
)

# Configure handler with formatter
__FLEA_LOG_STREAM_HANDLER__.setFormatter(__FLEA_LOG_FORMATTER__)

# Configure logger
__FLEA_LOGGER__ = logging.getLogger('FLEA')
__FLEA_LOGGER__.addHandler(__FLEA_LOG_STREAM_HANDLER__)

# Export logger alias
logger = __FLEA_LOGGER__
logger.propagate = False
logger.enable = lambda: logger.setLevel('DEBUG')
logger.disable = lambda: logger.setLevel('CRITICAL')
logger.enable()



class LoggingMixin(object):
    ENABLE_LOGGING = True

    def log(self, message, tag='debug'):
        if self.ENABLE_LOGGING:
            logging_method = getattr(logger, tag)
            logging_method('{}: {}'.format(self.__log_title, message))

    @property
    def __log_title(self):
        return self.__class__.__name__
