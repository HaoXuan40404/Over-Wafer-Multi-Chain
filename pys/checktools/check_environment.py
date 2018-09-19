import os

from pys import ansible, utils
from pys.chain import data
from pys.chain import meta
from pys.log import logger


def check_environment(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('check_environment action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k,v in mm.get_nodes().items():
        logger.debug('host ip is ' + k)
        ansible.environment_module(k, ansible.get_dir() + '/' + chain_id)


