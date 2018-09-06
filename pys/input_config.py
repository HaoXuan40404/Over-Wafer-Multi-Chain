import configparser

import ports
import node
import utils

class InputConfig:
    
    def __init__(self, config_file_path):
        self.config = config_file_path
        self.chain_id = ''
        self.chain_verion = ''
        self.install_dir = ''
        self.ports = ports.Ports(0, 0, 0)
        self.nodes = []
    
    def __repr__(self):
        return 'InputConfig [ chain_id %s, chain_version %s, install_dir %s, ports %s]' % (self.chain_id, self.chain_verion, self.install_dir, self.ports)

    def do_parser(self):
        if not utils.valid_string(self.config):
            raise Exception('invalid config_file_path', self.config)
        
        # read and parser config file
        cf = configparser.ConfigParser()
        cf.read(self.config)

        self.chain_id = cf.get('chain', 'id')
        self.chain_verion = cf.get('chain', 'version')
        self.install_dir = cf.get('chain', 'install_dir')

        try:
            self.ports.set_rpc_port(cf.getint('ports', 'rpc_port'))
        except:
            pass

        try:
            self.ports.set_p2p_port(cf.getint('ports', 'p2p_port'))
        except:
            pass
        
        try:
            self.ports.set_channel_port(cf.getint('ports', 'channel_port'))
        except:
            pass

        index = 0
        while True:
            try:
                nd = node.Node(cf.get('nodes', 'node%u' % index))
                nd.doNodeParser()
                self.nodes.append()
            except:
                break
            index = (index + 1)

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