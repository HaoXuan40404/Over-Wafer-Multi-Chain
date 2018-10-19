
from pys.chain.package import * 
from pys.chain.chain import Chain
from pys.chain.node import config

class Port:
    """Port object contains rpc port、channel port、p2p port.
    """

    def __init__(self, rpc_port, p2p_port, channel_port):
        self.rpc_port = rpc_port
        self.p2p_port = p2p_port
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
        return '[rpc_port] %d, [p2p_port] %d, [channel_port] %d' % (self.rpc_port, self.p2p_port, self.channel_port)

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
        return Port(0, 0, 0)
    
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
        host_dir = Chain(self.chain_id, self.chain_version).data_dir() + '/' + self.host + '/'
        if not os.path.exists(host_dir):
            logger.info(' host dir not exist, chain_id is %s, chain_version is %s, host is %s',
                        self.chain_id, self.chain_version, self.host)
            return

        logger.debug(' load begin, chain_id is %s, chain_version is %s, host is %s',
                     self.chain_id, self.chain_version, self.host)

        for list_dir in os.listdir(host_dir):
            if 'node' in list_dir:
                cfg_json = host_dir + '/' + list_dir + '/config.json'
                cf = config.Config(chain_id)
                if cf.fromJson(cfg_json):
                    index = int(list_dir[4:])
                    p = Port(cf.get_rpc_port(), cf.get_p2p_port(), cf.get_channel_port())
                    m[index] = p
                    logger.debug(' append node, index is %d, port is %s', index, p)
        
        logger.info('load end, ports is %d', self)
    
class ChainVerPort:

    def __init__(self, chain_id, chain_version):
        self.chain_version = chain_version
        self.chain_id = chain_id
        self.ports = {}

    def __repr__(self):
        return ' chain id is %s, chain version is %s, ports is %s' % (self.chain_id, self.chain_version, self.ports)
    
    def get_chain_id(self):
        return self.chain_id

    def get_chain_version(self):
        return self.chain_version

    def get_by_host_index(self, host, index):
        pass
    
    def clear(self):
        self.ports = {}
    
    def exist(self):
        dir = Chain(self.chain_id, self.chain_version).data_dir()
        return os.path.exists(dir)

    def load(self):
        self.clear()
        if not self.exist():
            logger.info('dir not exist, chain_id is %s, chain_version is %s',
                        self.chain_id, self.chain_version)
            return

        dir = Chain(self.chain_id, self.chain_version).data_dir()
        logger.debug('load begin, chain_id is %s, chain_version is %s, dir is %s',
                     self.chain_id, self.chain_version, dir)

        for host in os.listdir(dir):
            if utils.valid_ip(host):
                self.ports[host] = HostPort(self.chain_id, self.chain_version, host)
                logger.debug(' chain id %s, chain version %s, host is %s, ports is %s',
                             self.chain_id, self.chain_version, host, )
            else:
                logger.debug(' skip, not invalid host_ip, chain id is %s, chain version is %s,  host is %s',
                             self.chain_id, self.chain_version, host)

        logger.info('load end, ports is %d', self)

class ChainPort:
    pass

class AllChainPort:
    def __init__(self):
        self.ports = {}
    
