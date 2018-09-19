import os

from pys import ansible, utils
from pys.chain import meta
from pys.log import logger

def start_server(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('start action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k,v in mm.get_nodes().items():
        logger.debug('host ip is ' + k)
        ansible.start_module(k, ansible.get_dir() + '/' + chain_id)

<<<<<<< HEAD
def stop_server(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('stop action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k,v in mm.get_nodes().items():
        logger.debug('host ip is ' + k)
        ansible.stop_module(k, ansible.get_dir() + '/' + chain_id)
=======
def start_server(chain_id, chain_version):
    dir = data.Data().dir(chain_id, chain_version)
    if not os.path.isdir(dir):
        logger.warn('start_server wrong, your node is at  ' + dir)
        return
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.start_module(host, ansible.get_dir() + '/' + chain_id)
>>>>>>> 0f634a1a0102382713c8547e9bc68598218afea3

def check_server(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('check action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k,v in mm.get_nodes().items():
        logger.debug('host ip is ' + k)
        ansible.check_module(k, ansible.get_dir() + '/' + chain_id)

<<<<<<< HEAD

def monitor_server(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('monitor_server action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k,v in mm.get_nodes().items():
        logger.debug('host ip is ' + k)
        ansible.monitor_module(k, ansible.get_dir() + '/' + chain_id)
=======
def stop_server(chain_id, chain_version):
    dir = data.Data().dir(chain_id, chain_version)
    if not os.path.isdir(dir):
        logger.warn('stop_server wrong, your node is at  ' + dir)
        return
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.stop_module(host, ansible.get_dir() + '/' + chain_id)


def check_server(chain_id, chain_version):
    dir = data.Data().dir(chain_id, chain_version)
    if not os.path.isdir(dir):
        logger.warn('check_server wrong, your node is at  ' + dir)
        return
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.check_module(host, ansible.get_dir() + '/' + chain_id)

def monitor_server(chain_id, chain_version):
    dir = data.Data().dir(chain_id, chain_version)
    if not os.path.isdir(dir):
        logger.warn('monitor_server wrong, your node is at  ' + dir)
        return
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.monitor_module(host, ansible.get_dir() + '/' + chain_id)
>>>>>>> 0f634a1a0102382713c8547e9bc68598218afea3
