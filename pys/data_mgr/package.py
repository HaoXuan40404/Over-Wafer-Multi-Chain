#coding:utf-8

import os
import shutil
from pys import utils
from pys.log import logger, consoler
from pys.data_mgr import data
from pys.data_mgr.chain import Chain

class HostNodeDirs:
    def __init__(self, chain_id, chain_version, host):
        self.chain_id = chain_id
        self.chain_version = chain_version
        self.host = host
        self.node_dirs = []
        self.max_index = -1
        self.load()

    def __repr__(self):
        return ' chain id : %s, chain version : %s, max_index : %d, node_dirs : %s' % (self.chain_id, self.chain_version, self.max_index, self.node_dirs)

    def clear(self):
        self.node_dirs = []
        self.max_index = -1

    def get_node_dir(self, index):
        return Chain(self.chain_id, self.chain_version).data_dir() + '/' + self.host + '/' + str(index) + '/'

    def get_host_dir(self):
        return Chain(self.chain_id, self.chain_version).data_dir() + '/' + self.host + '/'

    def get_node_dirs(self):
        return self.node_dirs

    def get_max_index(self):
        return self.max_index

    def create(self):
        if not self.exist():
            host_dir = Chain(self.chain_id, self.chain_version).data_dir() + '/' + self.host + '/'
            os.makedirs(host_dir)
            return True
        return self.exist()
    
    def remove(self):
        if self.exist():
            host_dir = Chain(self.chain_id, self.chain_version).data_dir() + '/' + self.host + '/'
            shutil.rmtree(host_dir)
        return not self.exist()

    def exist(self):
        host_dir = Chain(self.chain_id, self.chain_version).data_dir() + '/' + self.host + '/'
        return os.path.exists(host_dir)

    def load(self):
        self.clear()
        host_dir = Chain(
            self.chain_id, self.chain_version).data_dir() + '/' + self.host + '/'
        if not os.path.exists(host_dir):
            logger.info(' host dir not exist, chain_id is %s, chain_version is %s, host is %s',
                        self.chain_id, self.chain_version, self.host)
            return

        logger.debug('load begin, chain_id is %s, chain_version is %s, host is %s',
                     self.chain_id, self.chain_version, self.host)

        for list_dir in os.listdir(host_dir):
            if 'node' in list_dir:
                self.node_dirs.append(list_dir)
                index = int(list_dir[4:])
                if index > self.max_index:
                    self.max_index = index
                logger.debug(' append node%d, dir is %s', index, list_dir)

        logger.info(' load end, info %s', self)


class VerHosts:
    """all package of chain of the version
    """

    def __init__(self, chain_id, chain_version):
        self.chain_id = chain_id
        self.chain_version = chain_version
        self.chain = Chain(self.chain_id, self.chain_version)
        self.pkg_list = []
        self.load()

    def __repr__(self):
        return 'chain is %s, list = %s' % (self.chain, self.pkg_list)

    def get_chain_id(self):
        return self.chain_id

    def get_pkg_list(self):
        return self.pkg_list

    def get_chain_version(self):
        return self.chain_version

    def get_version_dir(self):
        ver_dir = Chain(self.chain_id, self.chain_version).data_dir()
        return ver_dir

    def get_host_dir(self, host):
        host_dir = Chain(
            self.chain_id, self.chain_version).data_dir() + '/' + host + '/'
        return host_dir

    def append(self, host):
        self.pkg_list.append(host)

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

        for host in os.listdir(dir):
            if utils.valid_ip(host):
                self.append(host)
                logger.debug(' chain id %s, chain version %s, host is %s',
                             self.chain_id, self.chain_version, host)
            else:
                logger.debug(' skip, not invalid host_ip, chain id is %s, chain version is %s,  host is %s',
                             self.chain_id, self.chain_version, host)

        logger.info('load end, len is %d', len(self.get_pkg_list()))


class ChainVers:
    """all package of chain of the version
    """

    def __init__(self, chain_id):
        self.chain_id = chain_id
        self.ver_list = []
        self.load()

    def __repr__(self):
        return 'chain is %s, list = %s' % (self.chain_id, self.ver_list)

    def get_chain_id(self):
        return self.chain_id

    def get_ver_list(self):
        return self.ver_list

    def append(self, ver):
        self.ver_list.append(ver)

    def clear(self):
        self.ver_list = []

    def empty(self):
        return len(self.ver_list) == 0

    def get_chain_dir(self):
        return data.package_chain_dir(self.chain_id)

    def exist(self):
        return os.path.exists(self.get_chain_dir())

    def load(self):

        self.clear()
        if not self.exist():
            logger.info(' dir not exist, chain_id is %s', self.chain_id)
            return

        dir = self.get_chain_dir()
        logger.debug(' load begin, chain_id is %s ', self.chain_id)

        for v in os.listdir(dir):
            self.append(v)
            logger.debug(' chain id %s, ver is %s', self.chain_id, v)

        logger.info(' load end, ver list is %s', self.get_ver_list())


class AllChain:

    def __init__(self):
        self.chains = []
        self.load()

    def clear(self):
        self.chains = []

    def get_chains(self):
        return self.chains

    def get_dir(self):
        dir = data.package_dir_base()
        return dir
    
    def create(self):
        if not os.path.exists(self.get_dir()):
            os.makedirs(self.get_dir())

    def load(self):
        dir = data.package_dir_base()
        if os.path.exists(dir):
            for list_dir in os.listdir(dir):
                if utils.valid_chain_id(list_dir):
                    self.chains.append(list_dir)
                    logger.info(' append chain , chain id is %s', list_dir)

        logger.info(' chains is %s', self.chains)