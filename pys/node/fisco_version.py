#coding:utf-8

import re
import commands
from pys.log import logger
from pys.log import consoler

def get_version(path):
    """[check fisco-bcos version]
    
    Arguments:
        path {[dir]} -- [fisco-bcos path]
    
    Returns:
        [string] -- [fisco-bcos version]
    """


    cmd = path + ' --version'

    status,output = commands.getstatusoutput(cmd)

    version = output.split()

    if version[0] == 'FISCO-BCOS':
        logger.debug('function fisco_version status => ' %(status))
        consoler.info('fisco bcos version => '  %(version[2]))
    else:
        logger.debug('fisco bcos not exists, dir => ' %(output))
        consoler.info('fisco bcos not exists, dir => ' %(path))

    return version[2]