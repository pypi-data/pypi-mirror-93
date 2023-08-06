loggers = {}


def logger(func):
    import logging
    global loggers
    if loggers.get(func):
        return loggers.get(func)
    logger = logging.getLogger(func)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s\t%(name)s.%(funcName)s()\t%(levelname)s\t%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    loggers[func] = logger
    return logger
