#coding:utf-8
from pys.chain.package import * 
from pys.chain.package import *
from pys.chain.chain import Chain
from pys.node import config
from pys.exp import MCError

class Port:
    """Port object contains rpc port、channel port、p2p port.
    """

    def __init__(self, rpc_port, p2p_port, channel_port):
        self.rpc_port = rpc_port
        self.p2p_port =  p2p_port
        self.channel_port = channel_port
    
    def set_rpc_port(self, rpc_port):
        self.rpc_port = rpc_port

    def set_p2p_port(self, p2p_port):
        self.p2p_port = p2p_port
    
    def set_channel_port(self, channel_port):
        self.channel_port = channel_port
        
    def get_rpc_port(self):
        return self.rpc_port
    
    def get_p2p_port(self):
        return self.p2p_port
    
    def get_channel_port(self):
        return self.channel_port
    
    def to_port(self, index):
        return Port(self.get_rpc_port() + index, self.get_p2p_port() + index, self.get_channel_port() + index)
    
    def __repr__(self):
        return '[rpc] %d, [p2p] %d, [channel] %d' % (self.rpc_port, self.p2p_port, self.channel_port)

class HostPort:
    def __init__(self, chain_id, chain_version, host):
        self.ports = {}
        self.chain_id = chain_id
        self.chain_version = chain_version
        self.host = host
        self.load()
    
    def __repr__(self):
        return ' chain id is %s, chain version is %s, host is %s, ports is %s' % (self.chain_id, self.chain_version, self.host, self.ports)
    
    def get_by_index(self, index):
        if self.ports.has_key(index):
            return self.ports[index]
        raise MCError(' not found, chain id is %s, chain version is %s, host is %s, index is %d' % (
            self.chain_id, self.chain_version, self.host, index))
    
    def get_chain_id(self):
        return self.chain_id

    def get_chain_version(self):
        return self.chain_version
    
    def get_host(self):
        return self.host
    
    def clear(self):
        self.ports = {}
    
    def load(self):
        self.clear()

        hn = HostNodeDirs(self.chain_id, self.chain_version, self.host)
        host_dir = Chain(self.chain_id, self.chain_version).data_dir() + '/' + self.host + '/' 
        for node in hn.get_node_dirs():
            cfg_json = host_dir + '/' + node + '/config.json'
            cf = config.Config(self.chain_id)
            if cf.fromJson(cfg_json):
                p = Port(int(cf.get_rpc_port()), int(cf.get_p2p_port()), int(cf.get_channel_port()))
                self.ports[node] = p
                logger.debug(' append node, node is %d, port is %s', node, p)

        logger.info('load end, hp ports is %s', self)
    
class ChainVerPort:

    def __init__(self, chain_id, chain_version):
        self.chain_version = chain_version
        self.chain_id = chain_id
        self.ports = {}
        self.load()

    def __repr__(self):
        return ' chain id is %s, chain version is %s, ports is %s' % (self.chain_id, self.chain_version, self.ports)
    
    def get_chain_id(self):
        return self.chain_id

    def get_chain_version(self):
        return self.chain_version

    def get_by_host(self, host):
        if self.ports.has_key(host):
            return self.ports[host]
        raise MCError(' not found, chain id is %s, chain version is %s, host is %s' % (
            self.chain_id, self.chain_version, host))
    
    def clear(self):
        self.ports = {}
    
    def exist(self):
        dir = Chain(self.chain_id, self.chain_version).data_dir()
        return os.path.exists(dir)

    def load(self):

        self.clear()
        vh = VerHosts(self.chain_id, self.chain_version)
        for host in vh.get_pkg_list():
            hp = HostPort(self.chain_id, self.chain_version, host)
            self.ports[host] = hp

        logger.info('load end, cv ports is %s', self)

class ChainPort:

    def __init__(self, chain_id):
        self.chain_id = chain_id
        self.ports = {}
        self.load()
    
    def __repr__(self):
        return ' chain id is %s, ports is %s' % (self.chain_id, self.ports)

    def clear(self):
        self.ports = {}

    def get_chain_id(self):
        return self.chain_id
    
    def get_by_chain_version(self, version):
        if self.ports.has_key(version):
            return self.ports[version]
        raise MCError(' not found, chain id is %s, chain version is %s' % (self.chain_id, version))
    
    def load(self):

        cv = ChainVers(self.chain_id)
        for version in cv.get_ver_list():
            hp = ChainVerPort(self.chain_id, version)
            self.ports[version] = hp
        
        logger.info('load end, cp ports is %s', self)

class AllChainPort:
    def __init__(self):
        self.ports = {}
        self.load()
    
    def clear(self):
        self.ports = {}
    
    def __repr__(self):
        return ' ports is %s' % (self.ports)
    
    def get_by_chain_id(self, chain_id):
        if self.ports.has_key(chain_id):
            return self.ports[chain_id]
        raise MCError(' not found, chain id is %s' % (chain_id))
    
    def load(self):
    
        ac = AllChain()
        for chain_id in ac.get_chains():
            hp = ChainPort(chain_id)
            self.ports[chain_id] = hp
        
        logger.info('load end, acp ports is %s', self)
    
