import os
from pys import utils
from pys.log import logger
from pys.chain import data

class Ver:
    """管理一条链对应版本的所有安装包信息
    """

    def __init__(self, chain_id, chain_version):
        self.chain_id = chain_id
        self.chain_version = chain_version
        self.pkg_list = []

    def __repr__(self):
        return 'chain_id = %s, chain_version = %s, list = %s' % (self.chain_id, self.chain_version, self.pkg_list)

    def get_chain_id(self):
        return self.chain_id
    
    def get_pkg_list(self):
        return self.pkg_list

    def get_chain_version(self):
        return self.chain_version

    def append(self, node):
        self.pkg_list.append(node)

    def clear(self):
        self.pkg_list = []

    def load(self):

        self.clear()
        dir = data.package_dir(self.chain_id, self.chain_version)
        if not os.path.exists(dir):
            logger.info('dir not exist, chain_id is %s, chain_version is %s, dir is %s',
                        self.chain_id, self.chain_version, dir)
            return

        logger.debug('load begin, chain_id is %s, chain_version is %s, dir is %s',
                     self.chain_id, self.chain_version, dir)

        for node in os.listdir(dir):
            if utils.valid_ip(node):
                self.append(node)
                logger.debug('node is %s', node)
            else:
                logger.debug('skip, not invalid host_ip ' + dir)

        logger.debug('load end, len is %d', len(self.get_pkg_list()))


class Package:
    """管理一条链所有的安装包信息
    """

    def __init__(self, chain_id):
        self.chain_id = chain_id
        self.ver_list = []
    
    def __repr__(self):
        return 'chain_is is %s, list is %s' % (self.chain_id, self.ver_list)
    
    def get_chain_id(self):
        return self.chain_id
    
    def get_version_list(self):
        return self.ver_list

    def append(self, v):
        self.ver_list.append(v)
    
    def clear(self):
        self.ver_list = []

    def load(self):
        self.clear()

        dir = data.package_chain_dir(self.chain_id)
        if not os.path.exists(dir):
            logger.info('dir not exist, chain_id is %s, dir is %s',
                        self.chain_id, dir)
            return
        
        logger.info('load begin, chain_id is %s, dir is %s',
                     self.chain_id, dir)
        
        for chain_version in os.listdir(dir):
            ver = Ver(self.get_chain_id(), chain_version)
            ver.load()
            self.append(ver)

        logger.info('load end, len is %d', len(self.get_version_list()))

def list(chains, is_host):
    if len(chains) == 0:
        print('chains empty.')

    logger.info('load, chains is %s, is_host is %s', chains, is_host)

    pkg_list = []
    if chains[0] == "all":
        dir = data.package_dir_base()
        for chain_id in os.listdir(dir):
            p = Package(chain_id)
            p.load()
            pkg_list.append(p)
    else:
        for chain_id in chains:
            p = Package(chain_id)
            p.load()
            pkg_list.append(p)

    for p in pkg_list:
        print('chain_id => %s', p.get_chain_id())
        for v in p.get_version_list():
            print('\t %s ', v.get_chain_version())
            if isinstance(is_host, 'bool') and is_host:
                for h in v.get_pkg_list():
                    print('\t\t %s ', h)

    logger.info('load end')
