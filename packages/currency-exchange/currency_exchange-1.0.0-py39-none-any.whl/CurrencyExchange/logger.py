import logging


class LowerThanFilter(logging.Filter):

    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno <= self.level


def setup_logging(level=0):

    logger = logging.getLogger(__name__)
    if level == 0:
        logger.setLevel(logging.WARNING)
    if level == 1:
        logger.setLevel(logging.INFO)
    if level == 2:
        logger.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ltw = LowerThanFilter(logging.ERROR)

    h1 = logging.StreamHandler()
    h1.addFilter(ltw)
    h1.setFormatter(log_formatter)

    h2 = logging.FileHandler('sample.log')
    h2.setFormatter(log_formatter)
    h2.addFilter(ltw)

    logger.addHandler(h1)
    logger.addHandler(h2)

    return logger


if __name__ == '__main__':
    log = setup_logging(2)
    log.debug('This is a debug message')
    log.info('This is an info message')
    log.warning('This is a warning message')
    log.error('This is an error message')
    log.critical('This is a critical message')
