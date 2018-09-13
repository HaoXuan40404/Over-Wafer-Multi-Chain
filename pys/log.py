import logging
import logging.config

LOGGER_NAME = 'instance'

def init_logging(log_conf_path):
    # logging init
    logging.config.fileConfig(log_conf_path)
    # create logger
    logger = logging.getLogger(LOGGER_NAME)
    # log start
    logger.info('init_logging init. ')

def get_logger():
    # create logger
    logger = logging.getLogger(LOGGER_NAME)
    return logger