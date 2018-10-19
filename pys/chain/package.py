#coding:utf-8

import os
from pys import utils
from pys.log import logger, consoler
from pys.chain import data
from pys.chain.chain import Chain

class Ver:
    """all package of chain of the version
    """

    def __init__(self, chain_id, chain_version):
        self.chain_id = chain_id
        self.chain_version = chain_version
        self.chain = Chain(self.chain_id, self.chain_version)
        self.pkg_list = []

    def __repr__(self):
        return 'chain is %s, list = %s' % (self.chain, self.pkg_list)

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
    
    def empty(self):
        return len(self.pkg_list) == 0
    
    def exist(self):
        dir = self.chain.data_dir()
        return os.path.exists(dir)

    def load(self):

        self.clear()
        if not self.exist():
            logger.info('dir not exist, chain_id is %s, chain_version is %s',
                        self.chain_id, self.chain_version)
            return
        
        dir = self.chain.data_dir()
        logger.debug('load begin, chain_id is %s, chain_version is %s, dir is %s',
                     self.chain_id, self.chain_version, dir)

        for node in os.listdir(dir):
            if utils.valid_ip(node):
                self.append(node)
                logger.debug(' chain id %s, chain version %s, node is %s', self.chain_id, self.chain_version, node)
            else:
                logger.debug(' skip, not invalid host_ip, chain id is %s, chain version is %s,  node is %s', self.chain_id, self.chain_version, node)

        logger.info('load end, len is %d', len(self.get_pkg_list()))


class Package:
    """all package of chain
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
    
    def empty(self):
        return len(self.ver_list) == 0

    def append(self, v):
        self.ver_list.append(v)
    
    def clear(self):
        self.ver_list = []
    
    def exist(self):
        dir = data.package_chain_dir(self.chain_id)
        return os.path.exists(dir)

    def load(self):
        self.clear()

        if not self.exist():
            logger.warn('dir not exist, chain_id is %s',
                        self.chain_id)
            return

        dir = data.package_chain_dir(self.chain_id)
        logger.info('load begin, chain_id is %s, dir is %s',
                     self.chain_id, dir)
        
        for chain_version in os.listdir(dir):
            ver = Ver(self.get_chain_id(), chain_version)
            ver.load()
            self.append(ver)

        logger.info('load end, len is %d', len(self.get_version_list()))
