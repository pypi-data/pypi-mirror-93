import logging
import os
import sys
from datetime import datetime
from functools import lru_cache
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Tuple, Any

from refinitiv.dataplatform.tools._specification import BaseSpecification

# ---------------------------------------------------------------------------
#   Conversion from TS/JS to Python
# ---------------------------------------------------------------------------

TRACE = 5

py_grade = logging._nameToLevel.copy()
py_grade['TRACE'] = TRACE
# add an additional level
logging.addLevelName(TRACE, 'TRACE')
py_grade = {f'py_{lname}': {'name': lname, 'level': llevel} for lname, llevel in py_grade.items()}

ts_grade = {
    'ts_trace': {'name': 'trace', 'level': 0},
    'ts_debug': {'name': 'debug', 'level': 1},
    'ts_info': {'name': 'info', 'level': 2},
    'ts_warn': {'name': 'warn', 'level': 3},
    'ts_error': {'name': 'error', 'level': 4},
    'ts_silent': {'name': 'silent', 'level': 5},
    }

conversion_schema = [
    ('ts_trace', 'py_TRACE'),
    ('ts_debug', 'py_DEBUG'),
    ('ts_info', 'py_INFO'),
    ('ts_warn', 'py_WARNING'),
    ('ts_error', 'py_ERROR'),
    ('ts_silent', 'py_CRITICAL'),
    ]

py_by_ts_nameToName = {ts_grade[ts_]['name']: py_grade[py_]['name'] for ts_, py_ in conversion_schema}
py_by_ts_levelToLevel = {ts_grade[ts_]['level']: py_grade[py_]['level'] for ts_, py_ in conversion_schema}

# ---------------------------------------------------------------------------
#   File handler
# ---------------------------------------------------------------------------


bytes_by_suffix = {
    'B': 1,  # B
    'K': 2 ** 10,  # KiB
    'M': 2 ** 20,  # MiB
    'G': 2 ** 30,  # GiB
    }


def convert_filesize(s) -> int:
    if isinstance(s, int):
        return s

    if isinstance(s, str):
        suffix_ = s[-1]
        count_ = int(s[:-1])
        bytes_ = bytes_by_suffix[suffix_]
        count_bytes_ = count_ * bytes_
        return count_bytes_


def convert_interval(s) -> Tuple[int, str]:
    when_ = s[-1]
    interval_ = int(s[:-1])

    # Months
    if when_ == 'M':
        when_ = 'D'
        interval_ = interval_ * 30

    return interval_, when_


class TimedSizedRotatingHandler(TimedRotatingFileHandler, RotatingFileHandler):

    def __init__(self, filename, file_mode='a', max_bytes=0,
                 backup_count=0, encoding='ascii', delay=False, when='h',
                 interval=1, utc=False, at_time=None, *args, **kwargs):

        if file_mode.startswith('w'):
            try:
                os.remove(filename)
            except Exception:
                pass

        self.filename = filename
        RotatingFileHandler.__init__(self, filename=filename,
                                     mode=file_mode, maxBytes=max_bytes,
                                     backupCount=backup_count,
                                     encoding=encoding, delay=delay)
        TimedRotatingFileHandler.__init__(self, filename=filename,
                                          when=when, interval=interval,
                                          backupCount=backup_count,
                                          encoding=encoding,
                                          delay=delay, utc=utc,
                                          atTime=at_time)

    def shouldRollover(self, record):
        timed_rollover = TimedRotatingFileHandler.shouldRollover(self, record)
        sized_rollover = RotatingFileHandler.shouldRollover(self, record)
        return timed_rollover or sized_rollover

    def doRollover(self):
        super(TimedRotatingFileHandler, self).doRollover()

    def getFilesToDelete(self):
        return super(TimedRotatingFileHandler, self).getFilesToDelete()


def _filenamer(baseFilename):
    basename_ = os.path.basename(baseFilename)
    date_, time_, pid_, *name_, name_with_count_ = basename_.split("-")
    *name_chunk_, count_ = name_with_count_.split('.')
    name_.append(".".join(name_chunk_))
    name_ = '-'.join(name_)
    new_basename_ = '-'.join([date_, time_, count_, pid_, name_])
    return baseFilename.replace(basename_, new_basename_)


_file_handler_formatter = logging.Formatter(
    '[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(module)s] - [%(funcName)s] - %(message)s'
    )


def _create_log_file_handler():
    from refinitiv.dataplatform import configure

    # file name
    name_ = configure.get_str(configure.keys.log_filename)
    now_ = datetime.now()
    date_ = now_.strftime('%Y%m%d')
    time_ = now_.strftime('%H%M')
    process_id_ = os.getpid()
    filename_ = f'{date_}-{time_}-{process_id_}-{name_}'

    # file size
    file_size_ = configure.get_str(configure.keys.log_file_size)
    file_size_ = convert_filesize(file_size_)

    # max files count
    max_files_ = configure.get_int(configure.keys.log_max_files)

    # interval
    interval_ = configure.get_str(configure.keys.log_interval)
    interval_, when_ = convert_interval(interval_)

    handler_ = TimedSizedRotatingHandler(
        filename_,
        max_bytes=file_size_,
        when=when_,
        interval=interval_,
        backup_count=max_files_,
        encoding='utf-8',
        delay=True
        )
    handler_.namer = _filenamer
    handler_.setFormatter(_file_handler_formatter)
    return handler_


# ---------------------------------------------------------------------------
#   Stdout handler
# ---------------------------------------------------------------------------

_stdout_formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - [%(name)s] - [%(thread)d] | %(threadName)s\n%(message)s')


def _create_log_stdout_handler():
    handler_ = logging.StreamHandler(sys.stdout)
    handler_.setFormatter(_stdout_formatter)
    return handler_


# ---------------------------------------------------------------------------
#   Filtering
# ---------------------------------------------------------------------------


class NotLog(BaseSpecification):
    def is_satisfied_by(self, record: Any) -> bool:
        return False


class LogEverything(BaseSpecification):
    def is_satisfied_by(self, record: Any) -> bool:
        return True


class NotLogWithName(BaseSpecification):

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def is_satisfied_by(self, record: Any) -> bool:
        return self.name != record.name


class LogWithName(BaseSpecification):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def is_satisfied_by(self, record: Any) -> bool:
        return self.name == record.name


class LogStartsWithName(BaseSpecification):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def is_satisfied_by(self, record: Any) -> bool:
        return record.name.startswith(self.name)


class NotLogStartsWithName(BaseSpecification):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def is_satisfied_by(self, record: Any) -> bool:
        return not record.name.startswith(self.name)


default_log_filter = "*"


def join_by_and_(prev_spec, spec):
    return prev_spec and prev_spec.and_(spec) or spec


def join_by_or_(prev_spec, spec):
    return prev_spec and prev_spec.or_(spec) or spec


def make_filter(text):
    ss = [s.strip() for s in text.split(',') if s]

    if not ss:
        can_log = NotLog()

    else:
        can_log = None
        for s in ss:
            if s == "*":
                can_log = join_by_or_(can_log, LogEverything())
            elif s.startswith("-") and s.endswith("*"):
                can_log = join_by_and_(can_log, NotLogStartsWithName(s[1:-1]))
            elif s.startswith("-"):
                can_log = join_by_and_(can_log, NotLogWithName(s[1:]))
            elif s.endswith("*"):
                can_log = join_by_or_(can_log, LogStartsWithName(s[:-1]))
            else:
                can_log = join_by_or_(can_log, LogWithName(s))

    def inner(record):
        return can_log.is_satisfied_by(record)

    return inner


# ---------------------------------------------------------------------------
#   Log level
# ---------------------------------------------------------------------------

def convert_log_level(level) -> int:
    py_level_ = None

    if isinstance(level, str):
        level_ = level.strip()
        py_level_ = py_by_ts_nameToName.get(level_)

        if py_level_ is None:
            py_level_ = level

        py_level_ = logging._nameToLevel.get(py_level_)

    elif isinstance(level, int):
        py_level_ = py_by_ts_levelToLevel.get(level)

        if py_level_ is None:
            py_level_ = level

    return py_level_ or logging.INFO


def read_log_level_config():
    from refinitiv.dataplatform import configure

    level_ = configure.get_str(configure.keys.log_level)
    return convert_log_level(level_)


# ---------------------------------------------------------------------------
#   Create and dispose logger
# ---------------------------------------------------------------------------

_log_file_handler = _create_log_file_handler()
_log_stream_handler = _create_log_stdout_handler()

_existing_loggers = []


@lru_cache(None)
def create_logger(name):
    from refinitiv.dataplatform import configure

    # construct the logger object for session
    logger_ = logging.getLogger(name)

    log_file_enabled_ = configure.get(configure.keys.log_file_enabled, True)
    if log_file_enabled_:
        logger_.addHandler(_log_file_handler)

    log_console_enabled_ = configure.get(configure.keys.log_console_enabled, True)
    if log_console_enabled_:
        logger_.addHandler(_log_stream_handler)

    log_level_ = read_log_level_config()

    if log_level_ != logger_.level:
        logger_.setLevel(log_level_)

    log_filter_ = configure.get(configure.keys.log_filter, default_log_filter)
    logger_.addFilter(make_filter(log_filter_))

    _existing_loggers.append(name)

    return logger_


def get_logger(name):
    return create_logger(name)


def set_log_level(logger_name, level):
    logger = get_logger(logger_name)
    logger.setLevel(level)
    return logger


def existing_loggers():
    return _existing_loggers


def dispose_logger(logger):
    if isinstance(logger, str):
        logger = get_logger(logger)

    handlers_ = logger.handlers[:]

    for hdlr_ in handlers_:
        hdlr_.close()
        logger.removeHandler(hdlr_)

    return logger


# ---------------------------------------------------------------------------
#   Root logger
# ---------------------------------------------------------------------------

root_logger = create_logger("rdp")
