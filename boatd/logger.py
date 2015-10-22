import logging


def setup_logging():
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)-8s %(message)s',
        level=logging.DEBUG)
    logging.debug('Logging configured')
