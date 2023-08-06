import datetime
import pathlib
import threading

from queue import Queue


__all__ = ['get', 'debug', 'info', 'warn', 'error', 'fatal']

_loggers = {}


def debug(msg, logger='CORE'):
    get(name=logger).debug(msg)


def info(msg, logger='CORE'):
    get(name=logger).info(msg)


def warn(msg, logger='CORE'):
    get(name=logger).warn(msg)


def error(msg, logger='CORE'):
    get(name=logger).error(msg)


def fatal(msg, logger='CORE'):
    get(name=logger).fatal(msg)


def get(name='CORE', **kwargs):
    '''
    gets/creates a logger with own thread

    Keyword Arguments:

    name -- name of the logger/thread (default 'logger')

    filename -- name of the file to log to (default "'today'.log")

    encoding -- enconding to write (default "utf-8")

    log_directory -- directory to write the log files to (default '.')
    '''
    global _loggers
    if name not in _loggers:
        _loggers[name] = Logger(name=name, **kwargs)
        thread = threading.Thread(
            target=__consumer_logger,
            args=(_loggers[name],), daemon=True, name=f'{name}-thread'
        )
        setattr(_loggers[name], 'thread', thread)
        thread.start()
    return _loggers[name]


def __consumer_logger(logger):
    with logger.cv:
        while True:
            logger.cv.wait_for(lambda: not logger.queue.empty())
            logger.log(logger.queue.get())


class Logger:
    '''
    class to simplify logging to files
    not threaded
    '''
    _loggers = {}

    @classmethod
    def get(cls, name='logger', **kwargs):
        '''
        gets/creates a static logger

        Keyword Arguments:

        name -- name of the logger (default 'default_logger')

        filename -- name of the file to log to (default "'today'.log")

        encoding -- enconding to write (default "utf-8")

        log_directory -- directory to write the log files to (default '.')
        '''
        if name not in cls._loggers:
            cls._loggers[name] = Logger(name=name, **kwargs)
        return cls._loggers[name]

    def __init__(self, **kwargs):
        now = datetime.datetime.now()
        self.name = kwargs.get('name')
        self.filename = kwargs.get(
            'filename',
            f'{now.year}-{now.month}-{now.day}.log')
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.log_directory = kwargs.get('log_directory', './logs')
        _log_path = pathlib.Path(self.log_directory)
        if not _log_path.exists():
            _log_path.mkdir()
        self.log_path = _log_path
        self.queue = Queue()
        self.cv = threading.Condition()

    def log(self, msg):
        with open(
            self.log_path/self.filename, 'a', encoding=self.encoding
        ) as f:
            f.write(msg)
            f.write('\n')
            f.flush()
        return True

    def debug(self, msg):
        return self._log(msg, level='DEBUG')

    def info(self, msg):
        return self._log(msg, level='INFO ')

    def warn(self, msg):
        return self._log(msg, level='WARN ')

    def error(self, msg):
        return self._log(msg, level='ERROR')

    def fatal(self, msg):
        return self._log(msg, level='FATAL')

    def _log(self, msg, level):
        with self.cv:
            s = (f'[{__class__.__now_str()}: {self.name}-'
                f'{self.thread.native_id}/{level}] {msg}')
            self.queue.put(s)
            self.cv.notify_all()
        # return self.log(msg=s)

    @staticmethod
    def __now_str():
        now = datetime.datetime.now()
        return (f'{now.strftime("%Y/%m/%d %H:%M:%S")},'
                f'{str(now.microsecond)[:3]}')
