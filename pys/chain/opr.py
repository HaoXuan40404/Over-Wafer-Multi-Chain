from pys.chain import data
import os
from pys import ansible
from pys import utils
from pys.log import logger

dest_dir = '~/data/' 

def start_server(chain_id, chain_version):
    dir = data.Data().dir(chain_id,chain_version)
    if not os.path.isdir(dir):
        logger.warn('not this node, your node is at  ' + dir)
        return
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.start_module(host, dest_dir + chain_id + '/')
        else:
            logger.debug('cant start node at  ' + host)

def stop_server(chain_id, chain_version):
    dir = data.Data().dir(chain_id,chain_version)
    if not os.path.isdir(dir):
        logger.warn('not this node, your node is at  ' + dir)
        return
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.stop_module(host, dest_dir + chain_id + '/')
        else:
            logger.debug('cant stop node at  ' + host)


def check_server(chain_id, chain_version):
    dir = data.Data().dir(chain_id,chain_version)
    if not os.path.isdir(dir):
        logger.warn('not this node, your node is at  ' + dir)
        return
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.check_module(host, dest_dir + chain_id + '/')
        else:
            logger.debug('cant stop node at  ' + host)
