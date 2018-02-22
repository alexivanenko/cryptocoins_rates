import logging


def log(error_type, msg):
    """
    Write error or debug message to the log file

    :param int error_type: logging.ERROR, logging.WARNING, logging.DEBUG, etc
    :param string msg: error message
    :return: void
    """
    logger = logging.getLogger()
    logger.log(error_type, msg)
