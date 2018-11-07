#coding:utf-8

import os
import logging
import logging.config

from pys import path

# logging init
logging.config.fileConfig(path.get_path() + '/conf/logging.conf')
# 
logger = logging.getLogger('instance')
consoler = logging.getLogger('console')