import os

from pys import utils
from pys import ansible
from pys.chain import data
from pys.log import logger


def publish_server(chain_id, chain_version):
    dir = data.Data().dir(chain_id,chain_version)
    if not os.path.isdir(dir):
        logger.warn('dir not exist, dir is ' + dir)
        return
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.mkdir_module(host, ansible.get_dir() + '/' + chain_id)
            ansible.copy_module(host, dir  + '/' + host  + '/', ansible.get_dir() + '/' + chain_id)
        else:
            print("wrong host_ip!",host)
            logger.warn('wrong host_ip ' + dir)
