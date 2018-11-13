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
        (status, result) = utils.getstatusoutput('sudo echo ""| bash ' + path.get_path() + '/scripts/hostsname.sh' + ' ' + hosts_conf)
        if status != 0:
            logger.warn(' hostsname.sh init failed! status is %d, output is %s.', status, result)
            raise MCError('hostsname.sh failed! status is %d, output is %s.' % (status, result))
        logger.info(' hostsname.sh init success! status is %d, output is %s', status, result)
    except MCError as me:
        consoler.error(' \033[1;31m %s \033[0m', me)
    except Exception as e:
        consoler.error(' \033[1;31m hostsname.sh init failed! excepion is %s.\033[0m', e)
        logger.error('  hostsname.sh init failed! Result is %s'%result)
    
    try:
        (status, result) = utils.getstatusoutput('bash ' + path.get_path() + '/scripts/ssh_copy_add.sh' + ' ' + hosts_conf)
        if status != 0:
            logger.warn(' ssh_copy_add.sh init failed! status is %d, output is %s.', status, result)
            raise MCError('ssh_copy_add.sh failed! status is %d, output is %s.' % (status, result))
        logger.info(' ssh_copy_add.shinit success! status is %d, output is %s', status, result)
    except MCError as me:
        consoler.error(' \033[1;31m %s \033[0m', me)
    except Exception as e:
        consoler.error(' \033[1;31m ssh_copy_add.sh init failed! excepion is %s.\033[0m', e)
        logger.error('  ssh_copy_add.sh init failed! Result is %s'%result)
