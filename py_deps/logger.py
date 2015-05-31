# -*- coding: utf-8 -*-
"""py_deps.logger module."""
import sys
import logging


def trace_log(level='info'):
    """Traceback loggging."""
    _type, _val, _tb = sys.exc_info()
    msg = ("%s\n  CODE: %s\n  LINE: %s\n  NAME: %s\n  MSG : %s" %
           (_type,
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
