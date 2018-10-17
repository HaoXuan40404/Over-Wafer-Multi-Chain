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


    cmd = path + '--version'

    status,output = commands.getstatusoutput(cmd)

    version = output.split()

    logger.debug('function fisco_version status => %s' + status)
    consoler.info('fisco bcos version => %s', version[2])

    return version[2]