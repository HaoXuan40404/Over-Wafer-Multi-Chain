import os

from pys import ansible, utils
from pys.chain import data
<<<<<<< HEAD
from pys.chain import meta
from pys.log import logger


def check_environment(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('check_environment action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k,v in mm.get_nodes().items():
        logger.debug('host ip is ' + k)
        ansible.environment_module(k, ansible.get_dir() + '/' + chain_id)
=======
from pys.log import logger


def check_environment(chain_id, chain_version):
    dir = data.Data().dir(chain_id, chain_version)
    if not os.path.isdir(dir):
        logger.warn('check_environment error  ')
        return
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.environment_module(host, ansible.get_dir() + '/' + chain_id)
>>>>>>> 0f634a1a0102382713c8547e9bc68598218afea3

