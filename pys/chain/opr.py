import os

from pys import ansible, utils
from pys.chain import meta
from pys.log import logger


def start_server(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('start action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k, v in mm.get_nodes().items():
        logger.debug('host ip is ' + k)
        ansible.start_module(k, ansible.get_dir() + '/' + chain_id)


def stop_server(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('stop action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k, v in mm.get_nodes().items():
        logger.debug('host ip is ' + k)
        ansible.stop_module(k, ansible.get_dir() + '/' + chain_id)


def check_server(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('check action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k, v in mm.get_nodes().items():
        logger.debug('host ip is ' + k)
        ansible.check_module(k, ansible.get_dir() + '/' + chain_id)


def monitor_server(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('monitor_server action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k, v in mm.get_nodes().items():
        logger.debug('host ip is ' + k)
        ansible.monitor_module(k, ansible.get_dir() + '/' + chain_id)
