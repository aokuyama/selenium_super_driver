from logging import getLogger, StreamHandler, DEBUG, CRITICAL


def get_logger(name=None, level=DEBUG):
    logger = getLogger(name)
    handler = StreamHandler()
    handler.setLevel(level)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False
    return logger

def get_test_logger():
    return get_logger('test', CRITICAL)