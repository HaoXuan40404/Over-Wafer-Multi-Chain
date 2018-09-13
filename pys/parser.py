import configparser
import logging

import utils
import log

# create logger
logger = logging.getLogger("instance")

class Ports:
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
    
    def __repr__(self):
        return 'Ports [rpc_port %u, p2p_port %u, channel_port %u]' % (self.rpc_port, self.p2p_port, self.channel_port)

class NodeEle:
    def __init__(self, node_desc):
        self.node_desc = node_desc.strip()
        self.host_ip = ''
        self.p2p_ip = ''
        self.node_num = 0
    
    def do_parser(self):
        if isinstance(self.node_desc, str):
            l = self.node_desc.split()
            if len(l) != 3:
                raise Exception("node_desc invalid ", self.node_desc)
            if not utils.valid_ip(l[0]):
                raise Exception("invalid host_ip ", l[0])
            if not utils.valid_ip(l[1]):
                raise Exception("invalid p2p_ip ", l[1])
            if l[2] <= 0:
                raise Exception("num lt 0 ", l[2])
            self.host_ip = l[0]
            self.p2p_ip = l[1]
            self.node_num = l[2]
        else:
            raise Exception("node_desc not string ", self.node_desc)

    def get_host_ip(self):
        return self.host_ip

    def get_p2p_ip(self):
        return self.p2p_ip
    
    def get_node_num(self):
        return self.node_num
    
    def __repr__(self):
        return 'Node [host_ip %s, p2p_ip %s, node_num %u]' % (self.host_ip, self.p2p_ip, self.node_num)

class ConfParser:
    '''
    '''
    def __init__(self, cfg):
        self.config = cfg
        self.chain_id = ''
        self.chain_verion = ''
        self.install_dir = ''
        self.ports = Ports(0, 0, 0)
        self.nodes = []
    
    def __repr__(self):
        return 'ConfParser [ chain_id %s, chain_version %s, install_dir %s, ports %s]' % (self.chain_id, self.chain_verion, self.install_dir, self.ports)

    def do_parser(self):

        logger.info('cfg parser %s', self.config)
        
        if not utils.valid_string(self.config):
            raise Exception('config not string ', self.config)
        
        # read and parser config file
        cf = configparser.ConfigParser()
        cf.read(self.config)

        self.chain_id = cf.get('chain', 'chainid')
        self.chain_verion = cf.get('chain', 'version')
        self.install_dir = cf.get('chain', 'install_dir')

        self.ports.set_rpc_port(cf.getint('ports', 'rpc_port'))
        self.ports.set_p2p_port(cf.getint('ports', 'p2p_port'))
        self.ports.set_channel_port(cf.getint('ports', 'channel_port'))

        index = 0
        while True:
            try:
                n = NodeEle(cf.get('nodes', 'node%u' % index))
                n.do_parser()
                self.nodes.append(n)
            except:
                break
            index = (index + 1)

        logger.info('cfg parser end, result is %s', self)

    def get_chain_id(self):
        return self.chain_id
    
    def get_chain_version(self):
        return self.chain_verion
    
    def get_install_dir(self):
        return self.install_dir

    def get_ports(self):
        return self.ports
    
    def get_nodes(self):
        return self.nodes

def parser_test():
    log.init_logging('../conf/logging.conf')
    confparser = ConfParser('config.ini')
    confparser.do_parser()

if __name__ == '__main__':
    parser_test()