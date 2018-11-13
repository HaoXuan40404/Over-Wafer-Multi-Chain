# coding:utf-8
import os
import json
import shutil
from pys import path
from pys.tool import utils
from pys.log import logger
from pys.log import consoler
from pys.error.exp import MCError

def init_chain(hosts_conf):
    try:
        (status, result) = utils.getstatusoutput('bash ' + path.get_path() + '/scripts/hostsname.sh' + ' ' + hosts_conf)
        if status != 0:
            logger.warn(' host.conf init failed! status is %d, output is %s, dir is %s.', status, result, dir)
            raise MCError('host.conf failed! status is %d, output is %s, dir is %s.' % (status, result, dir))
        logger.info(' host.conf init success! status is %d, output is %s, dir is %s.', status, result, dir)
    except MCError as me:
        consoler.error(' \033[1;31m %s \033[0m', me)
    except Exception as e:
        consoler.error(' \033[1;31m host.conf init failed! excepion is %s.\033[0m', e)
        logger.error('  host.conf init failed! Result is %s'%result)
    
    try:
        (status, result) = utils.getstatusoutput('bash ' + path.get_path() + '/scripts/ssh_copy_add.sh' + ' ' + hosts_conf)
        if status != 0:
            logger.warn(' host.conf init failed! status is %d, output is %s, dir is %s.', status, result, dir)
            raise MCError('host.conf failed! status is %d, output is %s, dir is %s.' % (status, result, dir))
        logger.info(' host.conf init success! status is %d, output is %s, dir is %s.', status, result, dir)
    except MCError as me:
        consoler.error(' \033[1;31m %s \033[0m', me)
    except Exception as e:
        consoler.error(' \033[1;31m host.conf init failed! excepion is %s.\033[0m', e)
        logger.error('  host.conf init failed! Result is %s'%result)
