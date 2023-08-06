from python_log_indenter import IndentedLoggerAdapter
import logging
import sys

logger = IndentedLoggerAdapter(logging.getLogger(__name__))


def set_up_logging(log_file, log_to_stdout):
    """Set up logging according the parameters.

    Parameters
    ----------
    log_file
        To which file will be a progress of computation logged.
    log_to_stdout : bool
        Whether to print the log messages to standard output.
    """
    logger.handlers = []

    handlers = []
    if log_to_stdout:
        handlers.append(logging.StreamHandler(stream=sys.stdout))

    handlers.append(
        logging.FileHandler(str(log_file) + '.log', mode='w')
    )

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M',
        handlers=handlers
    )


def shut_down():
    logging.shutdown()


def change_indent(indent: int = 0):
    if indent > 0:
        logger.add(indent)
    elif indent < 0:
        logger.sub(-indent)
    else:  # indent = 0
        pass


def log(level, msg, indent: int, *args, **kwargs):
    if indent > 0:
        logger.log(level, msg, *args, **kwargs)
        logger.add(indent)
    elif indent == 0:
        logger.log(level, msg, *args, **kwargs)
    else:
        logger.sub(-indent)
        logger.log(level, msg, *args, **kwargs)


def debug(msg, indent, *args, **kwargs):
    log(logging.DEBUG, msg, indent, *args, **kwargs)


def info(msg, indent, *args, **kwargs):
    log(logging.INFO, msg, indent, *args, **kwargs)


def warning(msg, indent, *args, **kwargs):
    log(logging.WARNING, msg, indent, *args, **kwargs)


def error(msg, indent, *args, **kwargs):
    log(logging.ERROR, msg, indent, *args, **kwargs)


def critical(msg, indent, *args, **kwargs):
    log(logging.CRITICAL, msg, indent, *args, **kwargs)

# def _make_log_function(level):
#     def f(msg, indent, *args, **kwargs):
#         log(level, msg, indent, *args, **kwargs)
#     return f
#
#
# _LEVELS = [
#     ('debug', logging.INFO),
#     ('info', logging.INFO),
#     ('warning', logging.INFO),
#     ('error', logging.INFO),
#     ('critical', logging.INFO),
# ]
#
# for name, log_level in _LEVELS:
#     globals()[name] = _make_log_function(log_level)
