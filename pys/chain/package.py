#coding:utf-8

import os
from pys import utils
from pys.log import logger, consoler
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
    
    def exist(self):
        dir = data.package_dir(self.chain_id, self.chain_version)
        return os.path.exists(dir)

    def load(self):

        self.clear()
        if not self.exist():
            logger.warn('dir not exist, chain_id is %s, chain_version is %s',
                        self.chain_id, self.chain_version)
            return
        
        dir = data.package_dir(self.chain_id, self.chain_version)
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
