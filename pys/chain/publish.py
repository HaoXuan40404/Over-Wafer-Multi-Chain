import os

from pys import utils
from pys import ansible
from pys.chain import data
from pys.log import logger
from pys.chain import meta


def publish_server(chain_id, chain_version):
    dir = data.package_dir(chain_id,chain_version)
    if not os.path.isdir(dir):
        logger.warn('dir not exist, dir is ' + dir)
        return
    mm = meta.Meta(chain_id)
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.mkdir_module(host, ansible.get_dir() + '/' + chain_id)
            ansible.copy_module(host, dir  + '/' + host  + '/', ansible.get_dir() + '/' + chain_id)
            mm.append(meta.MetaNode(chain_version, host, 0, 0, 0))
        else:
            logger.debug('skip, not invalid host_ip ' + dir)
    mm.write_to_file()
