import os

from pys import ansible, utils
from pys.chain import data
from pys.log import logger


def check_environment(chain_id, chain_version):
    dir = data.Data().dir(chain_id, chain_version)
    if not os.path.isdir(dir):
        logger.warn('check_environment error  ')
        return
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.environment_module(host, ansible.get_dir() + '/' + chain_id)

