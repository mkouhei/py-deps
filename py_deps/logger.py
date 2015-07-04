# -*- coding: utf-8 -*-
"""py_deps.logger module."""
import sys
import logging


def trace_log(level='info'):
    """Traceback loggging."""
    _type, _val, _tb = sys.exc_info()
    msg = ("{0}\n  CODE: {1}\n  LINE: {2}\n  NAME: {3}\n  MSG : {4}".format(
        _type,
        _tb.tb_frame.f_code.co_filename,
        _tb.tb_lineno,
        _tb.tb_frame.f_code.co_name,
        _val))
    if level == 'info':
        logging.info(msg)
    elif level == 'warning':
        logging.warning(msg)
    elif level == 'error':
        logging.error(msg)
    elif level == 'critical':
        logging.critical(msg)
    elif level == 'debug':
        logging.debug(msg)
