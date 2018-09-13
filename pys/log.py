import logging
import logging.config

def init_logging(log_conf_path):
    # logging module init
    logging.config.fileConfig(log_conf_path)
    # create logger
    logger = logging.getLogger("instance")
    # log start
    logger.info('init_logging init. ')