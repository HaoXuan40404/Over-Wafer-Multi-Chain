import os

from pys import ansible, utils
from pys.chain import data
from pys.log import logger


def start_server(chain_id, chain_version, dest_dir):
    dir = data.Data().dir(chain_id, chain_version)
    if not os.path.isdir(dir):
        logger.warn('not this node, your node is at  ' + dir)
        return
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.start_module(host, dest_dir + '/' + chain_id)


def stop_server(chain_id, chain_version, dest_dir):
    dir = data.Data().dir(chain_id, chain_version)
    if not os.path.isdir(dir):
        logger.warn('not this node, your node is at  ' + dir)
        return
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.stop_module(host, dest_dir + '/' + chain_id)


def check_server(chain_id, chain_version, dest_dir):
    dir = data.Data().dir(chain_id, chain_version)
    if not os.path.isdir(dir):
        logger.warn('not this node, your node is at  ' + dir)
        return
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.check_module(host, dest_dir + '/' + chain_id)
