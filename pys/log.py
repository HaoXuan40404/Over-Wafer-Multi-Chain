#coding:utf-8

import os
import logging
import logging.config

from pys import path

# logging init
logging.config.fileConfig(os.getcwd() + '/conf/logging.conf')
logger = logging.getLogger('instance')
# log start
logger.info('init_logging init. ')