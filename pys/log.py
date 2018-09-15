#coding:utf-8

import logging
import logging.config

LOGGER_NAME = 'instance'

logger = logging.getLogger(LOGGER_NAME)

def init_logging(log_conf_path):
    # logging init
    logging.config.fileConfig(log_conf_path)
    
    logger = logging.getLogger(LOGGER_NAME)
    # log start
    logger.info('init_logging init. ')