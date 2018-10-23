# coding:utf-8
import os
import shutil
from pys import utils
from pys.chain import data
from pys.log import consoler, logger
from pys.opr import opr_tools

def export_package(export_list, dest):
    """[export package into dest]
    
    Arguments:
        export_list {[list]} -- [chain_id:version]
        dest {[mkdir]} -- [destination]
    """

    chain_get = opr_tools.valid_cmd(export_list)
    
    if utils.valid_chain_id(chain_get[0]):
        dir = data.package_dir(chain_get[0], chain_get[1])
        for host in os.listdir(dir):
            if utils.valid_ip(host):
                shutil.copytree(dir + '/' + host, dest + '/' + host)
                for file_common in os.listdir(dir + '/common'):
                    if os.path.isdir(dir + '/common/' + file_common):
                        shutil.copytree(dir + '/common/' + file_common, dest + '/' + host + '/' + file_common)      
                    elif os.path.isfile(dir + '/common/' + file_common):
                        shutil.copy(dir + '/common/' + file_common, dest + '/' + host + '/')
            else:
                logger.debug('not invalid host_ip ' + host)    
    else:
        consoler.error('invalid chain_id format. %s %s', chain_get[0], chain_get[1])