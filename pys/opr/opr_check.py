# coding:utf-8
import os

from pys import ansible, utils
from pys.chain import data
from pys.chain.meta import *
from pys.log import consoler, logger

def check_chain(chain):
    """[Check if the nodes is running normally.]
    
    Arguments:
        chain {[list]} -- [get chain_id:host_ip from command Line]
    """
    
    if chain[0] == 'all':
        dir = data.meta_dir_base()
        if os.path.exists(dir):
            for chain_id in os.listdir(dir):
                check_server(chain_id)
        else:
            consoler.info(' No published chain exist, do nothing.')
    else:
        for i in range(len(chain)):
            chain_get = chain[i].split(':')
            if len(chain_get) == 1:
                if utils.valid_chain_id(chain_get[0]):
                    check_server(chain_get[0])
                else:
                    consoler.info(' skip, invalid chain_id, chain_id is %s', chain_get[0])
            elif len(chain_get) == 2:
                if utils.valid_chain_id(chain_get[0]):
                    if utils.valid_ip(chain_get[1]):
                        ansible.check_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                    else:
                        consoler.info(' skip, invalid host, chain_id is %s, host is %s', chain_get[0], chain_get[1])
                else:
                    consoler.info(' skip, invalid chain_id, chain_id is %s, host is %s', chain_get[0], chain_get[1])

            else:
                consoler.info(' skip, invalid format, not chain_id:host, input %s', chain_get)
        

def check_server(chain_id):
    """[Using scheck.sh check all nodes of a chain]
    
    Arguments:
        chain_id {[string]} -- [chain_id:version]
    """

    mm = Meta(chain_id)
    if not mm.exist():
        logger.warn('chain meta is not exist, maybe the chain is not published, chain_id is %s', chain_id)
        consoler.warn('chain is not published, can not check action, chain_id is %s', chain_id)
        return 

    logger.info('check action, chain_id is ' + chain_id)
    consoler.info(' => check all node of chain %s', chain_id)
    for k in mm.get_nodes().keys():
        logger.debug('host ip is ' + k)
        ansible.check_module(k, ansible.get_dir() + '/' + chain_id)